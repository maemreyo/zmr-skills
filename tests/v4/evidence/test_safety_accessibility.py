from zamery_education_v4.kernel.evidence.safety import inspect_accessibility, inspect_safety


def test_unsafe_media_mission_fails() -> None:
    _, privacy = inspect_safety({"missions":[{"record_id":"mission:1","requires_face":True}]})
    assert privacy.result == "fail"
    assert privacy.findings[0].code == "MEDIA_PRIVACY_ALTERNATIVE_MISSING"


def test_construct_preservation() -> None:
    receipt = inspect_accessibility({"accommodations":[{"record_id":"a1","assessment_construct":"unaided_recall","adds_word_bank":True}]})
    assert receipt.findings[0].code == "ACCOMMODATION_CHANGES_CONSTRUCT"
