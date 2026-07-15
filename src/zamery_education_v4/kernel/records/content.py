from __future__ import annotations

from pydantic import field_validator

from .base import CanonicalRecord


class ItemRecord(CanonicalRecord):
    record_type = "item"
    prompt: str
    objective_ids: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()
    scored: bool = True
    surface: str = "student"
    response_mode: str = "written"
    cues: tuple[str, ...] = ()

    @field_validator("objective_ids", "source_ids", "cues")
    @classmethod
    def sorted_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted(set(values)))


class AnswerRecord(CanonicalRecord):
    record_type = "answer"
    item_id: str
    answer: str
    authority_source_ids: tuple[str, ...]
    rationale: str | None = None

    @field_validator("authority_source_ids")
    @classmethod
    def sorted_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted(set(values)))
