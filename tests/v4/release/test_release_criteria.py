from zamery_education_v4.application.release import CRITERIA, verify_release

def test_release_fails_closed_when_teacher_approval_missing() -> None:
    evidence={name:True for name in CRITERIA}; evidence["teacher_classroom_usability"]=False
    report=verify_release("abc",evidence)
    assert not report.passed and report.missing == ("teacher_classroom_usability",)
