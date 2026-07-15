from zamery_education_v4.application.comparison import compare_outcomes

def test_lost_deliverable_is_severe() -> None:
    report=compare_outcomes({"deliverables":["workbook","deck"]},{"deliverables":["workbook"],"core_source_preserved":True,"binary_reopen":True,"teacher_command_surface":True})
    assert not report.acceptable
    assert "LOST_SUPPORTED_DELIVERABLE" in report.severe_regressions
