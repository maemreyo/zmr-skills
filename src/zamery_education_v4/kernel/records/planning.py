from __future__ import annotations

from pydantic import Field, field_validator

from .base import CanonicalRecord


class ObjectiveRecord(CanonicalRecord):
    record_type = "objective"
    description: str
    evidence_item_ids: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()

    @field_validator("evidence_item_ids", "source_ids")
    @classmethod
    def sorted_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted(set(values)))


class AssessmentDecisionRule(CanonicalRecord):
    record_type = "assessment_decision_rule"
    member_item_ids: tuple[str, ...]
    threshold: int = Field(ge=0)
    outcome: str

    @field_validator("member_item_ids")
    @classmethod
    def member_ids_are_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted(set(values)))
