from zamery_education_v4.testing import GoldenRunner

def test_unit1_production_passes_all_gates_and_revalidation() -> None:
    result = GoldenRunner().run_production("unit1-lesson1")
    assert result.published
    assert result.gate_decisions == ("brief", "pedagogy", "content", "safety", "accessibility", "presentation", "pack")
    assert {"student_workbook.docx", "teacher_guide.docx", "presentation.pptx"} <= set(result.deliverables)
