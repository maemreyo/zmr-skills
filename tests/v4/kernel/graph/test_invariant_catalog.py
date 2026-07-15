from datetime import datetime, timezone

from zamery_education_v4.kernel.graph import EdgeType, GraphEdge, PackGraph, validate_graph
from zamery_education_v4.kernel.records.approvals import ApprovalRecord
from zamery_education_v4.kernel.records.artifacts import ArtifactSpec, GeneratedArtifact
from zamery_education_v4.kernel.records.content import AnswerRecord, ItemRecord
from zamery_education_v4.kernel.records.context import SourceRecord, TeachingBrief
from zamery_education_v4.kernel.records.evidence import EvidenceReceipt
from zamery_education_v4.kernel.records.planning import AssessmentDecisionRule, ObjectiveRecord

HASH_A = "sha256:" + "a" * 64
HASH_B = "sha256:" + "b" * 64
HASH_C = "sha256:" + "c" * 64


def codes(graph: PackGraph, records: dict[str, object]) -> set[str]:
    return {item.code for item in validate_graph(graph, records)}


def test_invalid_edge_shape_and_generated_spec_are_reported() -> None:
    brief = TeachingBrief(
        record_id="brief:1",
        duration_minutes=90,
        learner_level="A2",
        source_ids=(),
    )
    artifact = GeneratedArtifact(
        record_id="artifact:1",
        spec_id="spec:missing",
        blob_hash=HASH_A,
        media_type="application/pdf",
    )
    graph = PackGraph.from_records(
        "graph:invalid",
        (brief, artifact),
        (
            GraphEdge(
                source_id=brief.record_id,
                target_id=artifact.record_id,
                edge_type=EdgeType.GENERATED_FROM,
            ),
        ),
    )
    found = codes(graph, {brief.record_id: brief, artifact.record_id: artifact})
    assert "INVALID_EDGE_SHAPE" in found
    assert "GENERATED_ARTIFACT_SPEC_MISSING" in found


def test_receipt_hash_and_approval_target_are_exact() -> None:
    item = ItemRecord(record_id="item:1", prompt="Prompt", scored=False)
    receipt = EvidenceReceipt(
        record_id="receipt:1",
        receipt_type="content",
        subject_hash=HASH_B,
        checker_id="checker",
        checker_version="4.0.0",
        checker_runtime_digest=HASH_C,
        policy_version="content@4",
        result="pass",
    )
    approval = ApprovalRecord(
        record_id="approval:1",
        scope="content",
        approved_hashes=(HASH_A,),
        approver_role="teacher",
        approved_at=datetime.now(timezone.utc),
    )
    graph = PackGraph.from_records(
        "graph:receipt",
        (item, receipt, approval),
        (
            GraphEdge(
                source_id=item.record_id,
                target_id=receipt.record_id,
                edge_type=EdgeType.VERIFIED_BY,
            ),
        ),
    )
    found = codes(
        graph,
        {
            item.record_id: item,
            receipt.record_id: receipt,
            approval.record_id: approval,
        },
    )
    assert "RECEIPT_SUBJECT_HASH_MISMATCH" in found
    assert "APPROVAL_TARGET_MISSING" in found


def test_student_answer_leakage_and_answer_authority_are_reported() -> None:
    item = ItemRecord(
        record_id="item:1",
        prompt="Correct answer: B",
        scored=True,
        surface="student",
    )
    answer = AnswerRecord(
        record_id="answer:1",
        item_id="item:other",
        answer="B",
        authority_source_ids=("source:1",),
    )
    spec = ArtifactSpec(
        record_id="spec:student",
        artifact_kind="worksheet",
        audience="student",
        content_record_ids=(answer.record_id,),
        format="docx",
    )
    graph = PackGraph.from_records("graph:answers", (item, answer, spec))
    found = codes(
        graph,
        {
            item.record_id: item,
            answer.record_id: answer,
            spec.record_id: spec,
        },
    )
    assert "STUDENT_ANSWER_LEAKAGE" in found
    assert "ANSWER_AUTHORITY_MISSING" in found


def test_cross_surface_rule_mismatch_is_reported() -> None:
    first = AssessmentDecisionRule(
        record_id="rule:student",
        member_item_ids=("item:1",),
        threshold=1,
        outcome="reteach",
    )
    second = AssessmentDecisionRule(
        record_id="rule:teacher",
        member_item_ids=("item:1", "item:2"),
        threshold=2,
        outcome="reteach",
    )
    graph = PackGraph.from_records("graph:rules", (first, second))
    assert "CROSS_SURFACE_DECISION_RULE_MISMATCH" in codes(
        graph,
        {first.record_id: first, second.record_id: second},
    )


def test_core_source_replacement_requires_approval() -> None:
    core = SourceRecord(
        record_id="source:core",
        title="Coursebook",
        authority="core",
    )
    replacement = SourceRecord(
        record_id="source:new",
        title="Supplement",
        authority="supplementary",
    )
    graph = PackGraph.from_records(
        "graph:source",
        (core, replacement),
        (
            GraphEdge(
                source_id=replacement.record_id,
                target_id=core.record_id,
                edge_type=EdgeType.INVALIDATES,
            ),
        ),
    )
    assert "CORE_SOURCE_REPLACED_WITHOUT_APPROVAL" in codes(
        graph,
        {core.record_id: core, replacement.record_id: replacement},
    )


def test_untracked_bundle_file_is_reported() -> None:
    objective = ObjectiveRecord(record_id="objective:1", description="Read")
    graph = PackGraph.from_records("graph:bundle", (objective,))
    assert "BUNDLE_UNTRACKED_FILE" in {
        item.code
        for item in validate_graph(
            graph,
            bundle_members={"workbook.docx"},
            actual_bundle_files={"workbook.docx", "secret.txt"},
        )
    }
