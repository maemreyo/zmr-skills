from __future__ import annotations

from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, ConfigDict

from ..records.evidence import EvidenceReceipt


class EvidenceFreshnessPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    policy_version: str
    max_age_seconds: int | None = None


def receipt_applies(
    receipt: EvidenceReceipt,
    *,
    subject_hash: str,
    policy_version: str,
    now: datetime | None = None,
    max_age: timedelta | None = None,
) -> bool:
    if receipt.subject_hash != subject_hash or receipt.policy_version != policy_version:
        return False
    now = now or datetime.now(UTC)
    if receipt.expires_at is not None and now >= receipt.expires_at:
        return False
    if max_age is not None and receipt.issued_at is not None and now - receipt.issued_at > max_age:
        return False
    return True
