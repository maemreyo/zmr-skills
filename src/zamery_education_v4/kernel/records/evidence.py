from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

from ..types import RecordHash
from .base import CanonicalRecord


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    code: str
    message: str
    severity: Literal["info", "warning", "error", "critical"] = "error"
    affected_ids: tuple[str, ...] = ()
    remediation: str | None = None

    @field_validator("affected_ids")
    @classmethod
    def sorted_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted(set(values)))


class EvidenceReceipt(CanonicalRecord):
    record_type = "evidence_receipt"
    receipt_type: str
    subject_hash: RecordHash
    checker_id: str
    checker_version: str
    checker_runtime_digest: RecordHash
    policy_version: str
    result: Literal["pass", "warn", "fail", "error"]
    findings: tuple[Finding, ...] = ()
    execution_receipt_hash: RecordHash | None = None
    issued_at: datetime | None = None
    expires_at: datetime | None = None

    @field_validator("findings")
    @classmethod
    def stable_findings(cls, values: tuple[Finding, ...]) -> tuple[Finding, ...]:
        return tuple(sorted(values, key=lambda item: (item.code, item.affected_ids, item.message)))


class ReviewRecord(CanonicalRecord):
    record_type = "review"
    rubric_version: str
    reviewer_role: str
    subject_hashes: tuple[RecordHash, ...]
    ratings: dict[str, int | str | bool]
    findings: tuple[Finding, ...] = ()
    decision: Literal["accept", "revise", "reject"]
    reviewed_at: datetime

    @field_validator("subject_hashes")
    @classmethod
    def sorted_hashes(cls, values: tuple[RecordHash, ...]) -> tuple[RecordHash, ...]:
        return tuple(sorted(set(values)))


class GateDecision(CanonicalRecord):
    record_type = "gate_decision"
    gate: str
    policy_version: str
    subject_graph_hash: RecordHash
    consumed_evidence_hashes: tuple[RecordHash, ...]
    consumed_review_hashes: tuple[RecordHash, ...] = ()
    decision: Literal["pass", "warn", "fail"]
    severity: Literal["none", "warning", "hard_block"]
    findings: tuple[Finding, ...] = ()
    invalidation_conditions: tuple[str, ...] = ()

    @field_validator("consumed_evidence_hashes", "consumed_review_hashes", "invalidation_conditions")
    @classmethod
    def sorted_unique(cls, values: tuple) -> tuple:
        return tuple(sorted(set(values)))
