from __future__ import annotations

from ..records.evidence import GateDecision


def explain_gate(decision: GateDecision) -> dict[str, object]:
    return {
        "gate": decision.gate,
        "policy_version": decision.policy_version,
        "subject_graph_hash": decision.subject_graph_hash,
        "decision": decision.decision,
        "evidence_hashes": list(decision.consumed_evidence_hashes),
        "review_hashes": list(decision.consumed_review_hashes),
        "finding_codes": [finding.code for finding in decision.findings],
        "affected_ids": sorted({item for finding in decision.findings for item in finding.affected_ids}),
        "required_repair": decision.decision != "pass",
    }
