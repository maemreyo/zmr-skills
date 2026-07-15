from __future__ import annotations

from datetime import UTC, datetime

from ..evidence.freshness import receipt_applies
from ..evidence.registry import EvidenceRegistry
from ..records.evidence import Finding, GateDecision
from .order import prior_gates
from .policy import DEFAULT_POLICIES, GatePolicy


class GateEngine:
    def __init__(self, evidence: EvidenceRegistry | None = None, policies: dict[str, GatePolicy] | None = None) -> None:
        self.evidence = evidence or EvidenceRegistry()
        self.policies = policies or DEFAULT_POLICIES
        self.decisions: list[GateDecision] = []

    def latest_decision(self, gate: str, graph_hash: str) -> GateDecision | None:
        candidates = [d for d in self.decisions if d.gate == gate and d.subject_graph_hash == graph_hash]
        return candidates[-1] if candidates else None

    def evaluate(self, gate: str, graph_hash: str) -> GateDecision:
        policy = self.policies[gate]
        findings: list[Finding] = []
        evidence_hashes: list[str] = []
        review_hashes: list[str] = []

        for prior in prior_gates(gate):
            prior_decision = self.latest_decision(prior, graph_hash)
            if prior_decision is None or prior_decision.decision != "pass":
                findings.append(Finding(code="PRIOR_GATE_NOT_PASSED", message=f"prior gate {prior} has not passed", affected_ids=(prior,)))

        for receipt_type in policy.required_receipt_types:
            candidates = [r for r in self.evidence.receipts(receipt_type=receipt_type, subject_hash=graph_hash) if receipt_applies(r, subject_hash=graph_hash, policy_version=policy.version)]
            if not candidates:
                code = {
                    "reopen": "REOPEN_RECEIPT_MISSING", "rerender": "RERENDER_RECEIPT_MISSING",
                    "speaker_notes": "SPEAKER_NOTES_RECEIPT_MISSING",
                }.get(receipt_type, f"{receipt_type.upper()}_RECEIPT_MISSING")
                findings.append(Finding(code=code, message=f"required receipt missing: {receipt_type}"))
                continue
            receipt = candidates[-1]
            evidence_hashes.append(receipt.calculated_hash)
            findings.extend(receipt.findings)
            if receipt.result in {"fail", "error"} and not receipt.findings:
                findings.append(Finding(code=f"{receipt_type.upper()}_FAILED", message=f"receipt failed: {receipt_type}"))

        if policy.required_review_rubric:
            reviews = [r for r in self.evidence.reviews(rubric_version=policy.required_review_rubric, subject_hash=graph_hash) if r.decision == "accept"]
            if not reviews:
                findings.append(Finding(code="HUMAN_REVIEW_MISSING", message=f"accepted review missing: {policy.required_review_rubric}"))
            else:
                review_hashes.append(reviews[-1].calculated_hash)
                findings.extend(reviews[-1].findings)

        hard = any(f.code in policy.hard_block_codes or f.severity in {"error", "critical"} for f in findings)
        warning = bool(findings) and not hard
        decision = "fail" if hard else ("warn" if warning else "pass")
        record = GateDecision(
            record_id=f"gate:{gate}:{graph_hash[-12:]}:{len(self.decisions)+1}", gate=gate,
            policy_version=policy.version, subject_graph_hash=graph_hash,
            consumed_evidence_hashes=tuple(evidence_hashes), consumed_review_hashes=tuple(review_hashes),
            decision=decision, severity="hard_block" if hard else ("warning" if warning else "none"),
            findings=tuple(findings), invalidation_conditions=("subject_graph_hash_changes", "policy_version_changes", "evidence_expires"),
        )
        self.decisions.append(record)
        return record
