import pytest
from zamery_education_v4.testing import GoldenRunner

@pytest.mark.parametrize(("fixture", "code"), [
    ("route-misclassification", "WORKFLOW_GOAL_MISMATCH"),
    ("missing-lineage", "MISSING_SOURCE_LINEAGE"),
    ("threshold-denominator", "DECISION_RULE_DENOMINATOR_MISMATCH"),
    ("preexposed-diagnostic", "DIAGNOSTIC_PREEXPOSED_CUES"),
    ("missing-source-answers", "MISSING_SOURCE_ANSWER_AUTHORITY"),
    ("empty-speaker-notes", "EMPTY_SPEAKER_NOTES"),
    ("self-attested-pack-qa", "REOPEN_RECEIPT_MISSING"),
    ("render-analyzer-crash", "INSPECTOR_EXECUTION_FAILED"),
    ("unsafe-media-homework", "MEDIA_PRIVACY_ALTERNATIVE_MISSING"),
])
def test_negative_fixture_fails_closed(fixture: str, code: str) -> None:
    result = GoldenRunner().run_negative("unit1-lesson1", fixture)
    assert code in result.finding_codes
    assert not result.published
