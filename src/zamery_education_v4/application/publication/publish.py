from __future__ import annotations

from ...kernel.records.artifacts import PublishedBundleRecord
from ...kernel.records.evidence import GateDecision


def publish_bundle(
    *, record_id: str, bundle_spec_id: str, archive_hash: str, graph_hash: str,
    gate_decisions: tuple[GateDecision, ...], publication_approval_hash: str,
) -> PublishedBundleRecord:
    required = {"brief", "pedagogy", "content", "safety", "accessibility", "presentation", "pack"}
    by_gate = {decision.gate: decision for decision in gate_decisions}
    if set(by_gate) != required or any(decision.decision != "pass" or decision.subject_graph_hash != graph_hash for decision in by_gate.values()):
        raise PermissionError("seven current gate passes are required")
    return PublishedBundleRecord(record_id=record_id, bundle_spec_id=bundle_spec_id, archive_hash=archive_hash, graph_hash=graph_hash, gate_decision_hashes=tuple(decision.calculated_hash for decision in gate_decisions), publication_approval_hash=publication_approval_hash)
