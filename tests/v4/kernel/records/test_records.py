import pytest
from pydantic import ValidationError

from zamery_education_v4.kernel.records.context import TeachingBrief
from zamery_education_v4.kernel.records.registry import default_registry


def make_brief() -> TeachingBrief:
    return TeachingBrief(record_id="brief:unit1", duration_minutes=90, learner_level="A2", source_ids=("source:1",))


def test_record_is_frozen() -> None:
    brief = make_brief()
    with pytest.raises(ValidationError):
        brief.duration_minutes = 105  # type: ignore[misc]


@pytest.mark.parametrize("field", ["approved", "build_status", "absolute_path", "process_id"])
def test_unknown_mutable_fields_are_rejected(field: str) -> None:
    payload = {"record_id": "brief:unit1", "duration_minutes": 90, "learner_level": "A2", "source_ids": ["source:1"], field: True}
    with pytest.raises(ValidationError):
        TeachingBrief.model_validate(payload)


def test_registry_round_trip() -> None:
    brief = make_brief()
    parsed = default_registry().parse(brief.canonical_payload())
    assert parsed == brief
    assert parsed.calculated_hash == brief.calculated_hash
