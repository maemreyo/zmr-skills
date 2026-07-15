from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import field_validator

from ..types import RecordHash
from .base import CanonicalRecord


class ApprovalScope(StrEnum):
    TEACHING_BRIEF = "teaching_brief"
    PEDAGOGY = "pedagogy"
    CONTENT = "content"
    SAFETY = "safety"
    ACCESSIBILITY = "accessibility"
    PRESENTATION = "presentation"
    PUBLICATION = "publication"


class ApprovalRecord(CanonicalRecord):
    record_type = "approval"
    scope: ApprovalScope | str
    approved_hashes: tuple[RecordHash, ...]
    approver_role: str
    approved_at: datetime
    accepted_assumptions: tuple[str, ...] = ()
    accepted_limitations: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    revokes: tuple[str, ...] = ()

    @field_validator("approved_hashes", "accepted_assumptions", "accepted_limitations", "supersedes", "revokes")
    @classmethod
    def sorted_unique(cls, values: tuple) -> tuple:
        return tuple(sorted(set(values)))
