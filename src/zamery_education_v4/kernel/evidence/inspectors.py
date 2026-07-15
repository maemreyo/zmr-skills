from __future__ import annotations

from typing import Callable

from ..hashing import content_hash
from ..records.evidence import EvidenceReceipt, Finding

RUNTIME = "sha256:" + "e" * 64


def _receipt(receipt_type: str, payload: dict[str, object], policy: str, findings: list[Finding]) -> EvidenceReceipt:
    subject = content_hash(payload)
    return EvidenceReceipt(
        record_id=f"receipt:{receipt_type}:{subject[-12:]}", receipt_type=receipt_type,
        subject_hash=subject, checker_id=f"v4.{receipt_type}", checker_version="4.0.0",
        checker_runtime_digest=RUNTIME, policy_version=policy,
        result="fail" if findings else "pass", findings=tuple(findings)
    )


def inspect_source_lineage(payload: dict[str, object], policy: str = "brief-policy@4.0.0") -> EvidenceReceipt:
    findings: list[Finding] = []
    for item in payload.get("items", []):
        if not item.get("source_ids"):
            findings.append(Finding(code="MISSING_SOURCE_LINEAGE", message="item has no source lineage", affected_ids=(str(item.get("record_id", "unknown")),)))
    return _receipt("source_lineage", payload, policy, findings)


def inspect_objective_coverage(payload: dict[str, object], policy: str = "pedagogy-policy@4.0.0") -> EvidenceReceipt:
    findings: list[Finding] = []
    objectives = {str(item) for item in payload.get("objective_ids", [])}
    covered = {str(obj) for item in payload.get("items", []) for obj in item.get("objective_ids", [])}
    for missing in sorted(objectives - covered):
        findings.append(Finding(code="OBJECTIVE_NOT_COVERED", message="objective has no evidence item", affected_ids=(missing,)))
    return _receipt("objective_coverage", payload, policy, findings)


def inspect_answer_authority(payload: dict[str, object], policy: str = "content-policy@4.0.0") -> EvidenceReceipt:
    findings: list[Finding] = []
    answers = {str(item.get("item_id")): item for item in payload.get("answers", [])}
    for item in payload.get("items", []):
        item_id = str(item.get("record_id"))
        if item.get("scored", True) and (item_id not in answers or not answers[item_id].get("authority_source_ids")):
            findings.append(Finding(code="MISSING_SOURCE_ANSWER_AUTHORITY", message="scored item lacks source-backed answer", affected_ids=(item_id,)))
    return _receipt("answer_authority", payload, policy, findings)


def inspect_decision_rule(payload: dict[str, object], policy: str = "content-policy@4.0.0") -> EvidenceReceipt:
    findings: list[Finding] = []
    for rule in payload.get("decision_rules", []):
        members = set(rule.get("member_item_ids", []))
        denominator = int(rule.get("denominator", len(members)))
        threshold = int(rule.get("threshold", 0))
        if denominator != len(members):
            findings.append(Finding(code="DECISION_RULE_DENOMINATOR_MISMATCH", message="denominator differs from active membership", affected_ids=(str(rule.get("record_id", "unknown")),)))
        if threshold > len(members):
            findings.append(Finding(code="DECISION_THRESHOLD_EXCEEDS_MEMBERSHIP", message="threshold exceeds active membership", affected_ids=(str(rule.get("record_id", "unknown")),)))
    return _receipt("decision_rule", payload, policy, findings)
