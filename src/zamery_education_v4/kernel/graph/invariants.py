from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict

from ..records.approvals import ApprovalRecord
from ..records.artifacts import ArtifactSpec, DeliveryBundleSpec, GeneratedArtifact
from ..records.base import CanonicalRecord
from ..records.content import AnswerRecord, ItemRecord
from ..records.evidence import EvidenceReceipt
from ..records.planning import AssessmentDecisionRule
from .edges import EdgeType
from .model import PackGraph


class GraphFinding(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    code: str
    message: str
    affected_ids: tuple[str, ...] = ()
    severity: str = "error"


_EDGE_SHAPES: Mapping[EdgeType, tuple[set[str] | None, set[str] | None]] = {
    EdgeType.IMPLEMENTS_OBJECTIVE: ({"item", "artifact_spec"}, {"objective"}),
    EdgeType.USES_AUTHORITY: ({"item", "answer"}, {"source"}),
    EdgeType.USES_DURATION: ({"artifact_spec", "execution_node"}, {"teaching_brief"}),
    EdgeType.GENERATED_FROM: ({"generated_artifact"}, {"artifact_spec"}),
    EdgeType.RENDERED_FROM: ({"generated_artifact"}, {"generated_artifact"}),
    EdgeType.VERIFIED_BY: (None, {"evidence_receipt"}),
    EdgeType.APPROVED_BY: (None, {"approval"}),
    EdgeType.SUPERSEDES: ({"approval"}, {"approval"}),
    EdgeType.REVOKES: ({"approval"}, {"approval"}),
    EdgeType.PACKAGES: ({"delivery_bundle_spec"}, {"generated_artifact"}),
}


def _finding(code: str, message: str, *affected_ids: str) -> GraphFinding:
    return GraphFinding(
        code=code,
        message=message,
        affected_ids=tuple(sorted(set(affected_ids))),
    )


def _cycle_findings(graph: PackGraph) -> list[GraphFinding]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    indegree = {record.record_id: 0 for record in graph.records}
    for edge in graph.edges:
        if edge.source_id in indegree and edge.target_id in indegree:
            if edge.target_id not in adjacency[edge.source_id]:
                adjacency[edge.source_id].add(edge.target_id)
                indegree[edge.target_id] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for target in sorted(adjacency[node]):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited == len(indegree):
        return []
    cycle_nodes = tuple(sorted(node for node, degree in indegree.items() if degree > 0))
    return [_finding("GRAPH_CYCLE", "graph contains a cycle", *cycle_nodes)]


def _validate_edge_shapes(graph: PackGraph) -> list[GraphFinding]:
    types = {record.record_id: record.record_type for record in graph.records}
    findings: list[GraphFinding] = []
    for edge in graph.edges:
        shape = _EDGE_SHAPES.get(edge.edge_type)
        if shape is None or edge.source_id not in types or edge.target_id not in types:
            continue
        allowed_sources, allowed_targets = shape
        source_type = types[edge.source_id]
        target_type = types[edge.target_id]
        if (
            allowed_sources is not None
            and source_type not in allowed_sources
            or allowed_targets is not None
            and target_type not in allowed_targets
        ):
            findings.append(
                _finding(
                    "INVALID_EDGE_SHAPE",
                    f"{edge.edge_type} does not allow {source_type} -> {target_type}",
                    edge.source_id,
                    edge.target_id,
                )
            )
    return findings


def _validate_records(
    graph: PackGraph,
    records: Mapping[str, CanonicalRecord],
) -> list[GraphFinding]:
    findings: list[GraphFinding] = []
    graph_hashes = {record.record_hash for record in graph.records}
    graph_ids = {record.record_id for record in graph.records}
    ref_hashes = {record.record_id: record.record_hash for record in graph.records}
    answers = {
        record.item_id
        for record in records.values()
        if isinstance(record, AnswerRecord)
        and record.authority_source_ids
    }

    decision_rules: dict[str, list[AssessmentDecisionRule]] = defaultdict(list)
    for record in records.values():
        if isinstance(record, AssessmentDecisionRule):
            decision_rules[record.outcome.casefold()].append(record)
            if record.threshold > len(record.member_item_ids):
                findings.append(
                    _finding(
                        "DECISION_THRESHOLD_EXCEEDS_MEMBERSHIP",
                        "decision threshold exceeds unique membership",
                        record.record_id,
                    )
                )
        elif isinstance(record, ItemRecord):
            if record.scored and record.record_id not in answers:
                findings.append(
                    _finding(
                        "ANSWER_AUTHORITY_MISSING",
                        "scored item has no current answer authority",
                        record.record_id,
                    )
                )
            prompt = record.prompt.casefold()
            if record.surface == "student" and (
                "answer:" in prompt or "correct answer" in prompt
            ):
                findings.append(
                    _finding(
                        "STUDENT_ANSWER_LEAKAGE",
                        "student surface contains answer material",
                        record.record_id,
                    )
                )
        elif isinstance(record, ArtifactSpec):
            if record.audience.casefold() == "student":
                leaked = [
                    content_id
                    for content_id in record.content_record_ids
                    if isinstance(records.get(content_id), AnswerRecord)
                ]
                if leaked:
                    findings.append(
                        _finding(
                            "STUDENT_ANSWER_LEAKAGE",
                            "student artifact includes answer records",
                            record.record_id,
                            *leaked,
                        )
                    )
        elif isinstance(record, GeneratedArtifact):
            if record.spec_id not in graph_ids or not isinstance(
                records.get(record.spec_id), ArtifactSpec
            ):
                findings.append(
                    _finding(
                        "GENERATED_ARTIFACT_SPEC_MISSING",
                        "generated artifact does not resolve to an artifact spec",
                        record.record_id,
                        record.spec_id,
                    )
                )
        elif isinstance(record, EvidenceReceipt):
            subject_edges = [
                edge
                for edge in graph.edges
                if edge.edge_type == EdgeType.VERIFIED_BY
                and edge.target_id == record.record_id
            ]
            if subject_edges and all(
                ref_hashes.get(edge.source_id) != record.subject_hash
                for edge in subject_edges
            ):
                findings.append(
                    _finding(
                        "RECEIPT_SUBJECT_HASH_MISMATCH",
                        "evidence receipt does not match the verified subject hash",
                        record.record_id,
                        *(edge.source_id for edge in subject_edges),
                    )
                )
        elif isinstance(record, ApprovalRecord):
            missing_hashes = sorted(set(record.approved_hashes) - graph_hashes)
            if missing_hashes:
                findings.append(
                    _finding(
                        "APPROVAL_TARGET_MISSING",
                        "approval targets hashes outside the graph",
                        record.record_id,
                    )
                )
        elif isinstance(record, DeliveryBundleSpec):
            packaged_ids = {
                edge.target_id
                for edge in graph.edges
                if edge.edge_type == EdgeType.PACKAGES
                and edge.source_id == record.record_id
            }
            declared_artifacts = {
                artifact.record_id
                for artifact in records.values()
                if isinstance(artifact, GeneratedArtifact)
                and artifact.blob_hash in set(record.members.values())
            }
            if declared_artifacts - packaged_ids:
                findings.append(
                    _finding(
                        "INVALID_EDGE_SHAPE",
                        "bundle membership lacks PACKAGES edges",
                        record.record_id,
                        *(declared_artifacts - packaged_ids),
                    )
                )

    for rules in decision_rules.values():
        signatures = {
            (rule.member_item_ids, rule.threshold)
            for rule in rules
        }
        if len(signatures) > 1:
            findings.append(
                _finding(
                    "CROSS_SURFACE_DECISION_RULE_MISMATCH",
                    "decision rules for the same outcome disagree on membership or threshold",
                    *(rule.record_id for rule in rules),
                )
            )

    replaced_core_sources = {
        edge.target_id
        for edge in graph.edges
        if edge.edge_type == EdgeType.INVALIDATES
        and getattr(records.get(edge.target_id), "authority", "").casefold()
        in {"core", "coursebook_core", "primary"}
    }
    publication_approvals = [
        record
        for record in records.values()
        if isinstance(record, ApprovalRecord)
        and str(record.scope) in {"content", "publication"}
    ]
    for source_id in sorted(replaced_core_sources):
        source_hash = ref_hashes.get(source_id)
        if source_hash is not None and not any(
            source_hash in approval.approved_hashes
            for approval in publication_approvals
        ):
            findings.append(
                _finding(
                    "CORE_SOURCE_REPLACED_WITHOUT_APPROVAL",
                    "core source replacement lacks exact-hash approval",
                    source_id,
                )
            )
    return findings


def validate_graph(
    graph: PackGraph,
    records: Mapping[str, CanonicalRecord] | None = None,
    *,
    bundle_members: set[str] | None = None,
    actual_bundle_files: set[str] | None = None,
) -> tuple[GraphFinding, ...]:
    findings: list[GraphFinding] = []
    ids = {record.record_id for record in graph.records}
    for edge in graph.edges:
        if edge.source_id not in ids:
            findings.append(
                _finding(
                    "MISSING_EDGE_SOURCE",
                    "edge source missing",
                    edge.source_id,
                )
            )
        if edge.target_id not in ids:
            findings.append(
                _finding(
                    "MISSING_EDGE_TARGET",
                    "edge target missing",
                    edge.target_id,
                )
            )
    findings.extend(_cycle_findings(graph))
    findings.extend(_validate_edge_shapes(graph))
    if records:
        findings.extend(_validate_records(graph, records))
    if bundle_members is not None and actual_bundle_files is not None:
        for path in sorted(actual_bundle_files - bundle_members):
            findings.append(
                _finding(
                    "BUNDLE_UNTRACKED_FILE",
                    "bundle has untracked file",
                    path,
                )
            )
    unique = {
        (finding.code, finding.message, finding.affected_ids, finding.severity): finding
        for finding in findings
    }
    return tuple(
        sorted(
            unique.values(),
            key=lambda finding: (
                finding.code,
                finding.affected_ids,
                finding.message,
            ),
        )
    )
