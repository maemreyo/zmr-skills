from __future__ import annotations

from ..hashing import content_hash
from ..records.evidence import EvidenceReceipt, Finding

RUNTIME = "sha256:" + "f" * 64


def inspect_safety(payload: dict[str, object], policy_version: str = "safety-policy@4.0.0") -> tuple[EvidenceReceipt, EvidenceReceipt]:
    safety_findings: list[Finding] = []
    privacy_findings: list[Finding] = []
    for mission in payload.get("missions", []):
        requires_private = any(bool(mission.get(key)) for key in ("requires_face", "requires_room", "requires_family_member"))
        safeguards = all(mission.get(key) for key in ("neutral_alternative", "consent", "private_submission", "retention_policy", "deletion_policy"))
        if requires_private and not safeguards:
            privacy_findings.append(Finding(code="MEDIA_PRIVACY_ALTERNATIVE_MISSING", message="private media task lacks complete safeguards", affected_ids=(str(mission.get("record_id", "unknown")),), severity="critical"))
    subject = content_hash(payload)
    common = dict(subject_hash=subject, checker_version="4.0.0", checker_runtime_digest=RUNTIME, policy_version=policy_version)
    safety = EvidenceReceipt(record_id=f"receipt:safety:{subject[-12:]}", receipt_type="safety", checker_id="v4.safety", result="fail" if safety_findings else "pass", findings=tuple(safety_findings), **common)
    privacy = EvidenceReceipt(record_id=f"receipt:privacy:{subject[-12:]}", receipt_type="privacy", checker_id="v4.privacy", result="fail" if privacy_findings else "pass", findings=tuple(privacy_findings), **common)
    return safety, privacy


def inspect_accessibility(payload: dict[str, object], policy_version: str = "accessibility-policy@4.0.0") -> EvidenceReceipt:
    findings: list[Finding] = []
    for accommodation in payload.get("accommodations", []):
        if accommodation.get("assessment_construct") == "unaided_recall" and accommodation.get("adds_word_bank"):
            findings.append(Finding(code="ACCOMMODATION_CHANGES_CONSTRUCT", message="word bank changes unaided recall construct", affected_ids=(str(accommodation.get("record_id", "unknown")),)))
    subject = content_hash(payload)
    return EvidenceReceipt(record_id=f"receipt:accessibility:{subject[-12:]}", receipt_type="accessibility", subject_hash=subject, checker_id="v4.accessibility", checker_version="4.0.0", checker_runtime_digest=RUNTIME, policy_version=policy_version, result="fail" if findings else "pass", findings=tuple(findings))


def inspect_answer_separation(payload: dict[str, object], policy_version: str = "accessibility-policy@4.0.0") -> EvidenceReceipt:
    findings: list[Finding] = []
    for artifact in payload.get("student_artifacts", []):
        text = str(artifact.get("visible_text", "")).casefold()
        if "answer:" in text or artifact.get("contains_answer_key"):
            findings.append(Finding(code="STUDENT_ANSWER_LEAKAGE", message="student artifact exposes answers", affected_ids=(str(artifact.get("record_id", "unknown")),), severity="critical"))
    subject = content_hash(payload)
    return EvidenceReceipt(record_id=f"receipt:answer-separation:{subject[-12:]}", receipt_type="answer_separation", subject_hash=subject, checker_id="v4.answer_separation", checker_version="4.0.0", checker_runtime_digest=RUNTIME, policy_version=policy_version, result="fail" if findings else "pass", findings=tuple(findings))
