from __future__ import annotations

from pydantic import Field, field_validator

from .base import CanonicalRecord


def _sorted_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


class SourceRecord(CanonicalRecord):
    record_type = "source"
    title: str
    authority: str
    locator: str | None = None
    source_kind: str = "reference"
    content_fingerprint: str | None = None


class TeachingBrief(CanonicalRecord):
    record_type = "teaching_brief"
    duration_minutes: int = Field(gt=0, le=1440)
    learner_level: str
    source_ids: tuple[str, ...]
    lifecycle_goal: str = "publish_teaching_pack"
    requested_deliverables: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()

    _source_ids = field_validator("source_ids")(_sorted_unique)
    _requested_deliverables = field_validator("requested_deliverables")(_sorted_unique)
    _constraints = field_validator("constraints")(_sorted_unique)
