from zamery_education_v4.application.request_resolution import TeachingRequestRecord, resolve_workflow


def test_coursebook_pack_is_not_reduced_to_ielts_practice() -> None:
    request = TeachingRequestRecord(
        record_id="request:unit1", lifecycle_goal="publish_teaching_pack",
        requested_deliverables=("student_workbook", "teacher_guide", "presentation"),
        source_kinds=("textbook",), domain_terms=("IELTS",), quantity=None,
    )
    plan = resolve_workflow(request)
    assert plan.primary_goal == "publish_teaching_pack"
    assert plan.stages == (
        "resolve_source_authority", "build_teaching_brief", "design_learning_blueprint",
        "author_practice_content", "compose_student_materials", "compose_teacher_materials",
        "compose_presentation", "review_publish",
    )
    assert plan.domain_profiles == ("ielts_foundation_coursebook",)
