from __future__ import annotations

MATERIAL_FIELDS = (
    "objective_ids",
    "grade_band",
    "cefr",
    "target_language",
    "instruction_language",
    "methodology",
    "duration_minutes",
    "artifact_types",
    "answer_authority",
    "required_sources",
    "item_count",
    "assessment_profile",
    "media_source_authority",
    "form_ids",
    "seed",
    "learner_context_snapshot_id",
    "learning_sequence_id",
)
ROUTE_ORDER = (
    "understand_learners",
    "monitor_learning",
    "sequence_design",
    "design",
    "concept_teaching",
    "practice",
    "item_bank",
    "assessment_composition",
    "ielts_practice",
    "video_learning",
    "material_design",
    "presentation",
    "student_work_analysis",
    "reteach",
    "review_publish",
)
CONTENT_INTENTS = {
    "design",
    "concept_teaching",
    "practice",
    "item_bank",
    "assessment_composition",
    "ielts_practice",
    "video_learning",
    "material_design",
    "presentation",
    "review_publish",
}
FIELD_IMPACT = {
    "objective_ids": set(ROUTE_ORDER),
    "grade_band": CONTENT_INTENTS,
    "cefr": CONTENT_INTENTS,
    "target_language": set(ROUTE_ORDER),
    "instruction_language": set(ROUTE_ORDER),
    "methodology": {"concept_teaching", "practice", "item_bank", "assessment_composition", "ielts_practice", "video_learning", "material_design", "presentation", "review_publish"},
    "duration_minutes": {"design", "concept_teaching", "practice", "item_bank", "assessment_composition", "ielts_practice", "video_learning", "material_design", "presentation", "review_publish"},
    "answer_authority": {"item_bank", "assessment_composition", "ielts_practice", "video_learning", "student_work_analysis", "review_publish"},
    "required_sources": set(ROUTE_ORDER),
    "item_count": {"practice", "item_bank", "assessment_composition", "ielts_practice", "video_learning", "material_design", "review_publish"},
    "assessment_profile": {"item_bank", "assessment_composition", "ielts_practice", "material_design", "review_publish"},
    "media_source_authority": {"item_bank", "assessment_composition", "ielts_practice", "video_learning", "material_design", "review_publish"},
    "form_ids": {"assessment_composition", "material_design", "review_publish"},
    "seed": {"item_bank", "assessment_composition", "review_publish"},
    "learner_context_snapshot_id": {"design", "concept_teaching", "practice", "video_learning", "reteach"},
    "learning_sequence_id": {"sequence_design", "design", "item_bank", "assessment_composition", "review_publish"},
}
ARTIFACT_OWNER = {
    "lesson": "design",
    "unit": "design",
    "blueprint": "design",
    "board_plan": "concept_teaching",
    "concept_explanation": "concept_teaching",
    "worksheet": "practice",
    "practice": "practice",
    "homework": "practice",
    "flashcards": "practice",
    "item_bank": "item_bank",
    "question_bank": "item_bank",
    "quiz": "assessment_composition",
    "test": "assessment_composition",
    "exam": "assessment_composition",
    "exit_ticket": "assessment_composition",
    "rubric": "assessment_composition",
    "ielts_practice": "ielts_practice",
    "video_lesson": "video_learning",
    "h5p": "video_learning",
    "workbook": "material_design",
    "exam_pack": "material_design",
    "qti": "assessment_composition",
    "slide_deck": "presentation",
    "slides": "presentation",
    "pptx": "presentation",
    "student_work_analysis": "student_work_analysis",
    "feedback": "student_work_analysis",
}


def _artifact_scope_impact(before: object, after: object) -> set[str]:
    old = set(before) if isinstance(before, list) else set()
    new = set(after) if isinstance(after, list) else set()
    affected = {"design", "review_publish"}
    for artifact_type in old ^ new:
        owner = ARTIFACT_OWNER.get(str(artifact_type))
        if owner:
            affected.add(owner)
    return affected


def impact_diff(before: dict[str, object], after: dict[str, object]) -> dict[str, object]:
    ordered_keys = list(dict.fromkeys([*before.keys(), *after.keys()]))
    changes = [
        {"field": field, "before": before.get(field), "after": after.get(field)}
        for field in ordered_keys
        if before.get(field) != after.get(field)
    ]
    material_changes = [change for change in changes if change["field"] in MATERIAL_FIELDS]
    affected: set[str] = set()
    for change in material_changes:
        field = str(change["field"])
        if field == "artifact_types":
            affected.update(_artifact_scope_impact(change["before"], change["after"]))
        else:
            affected.update(FIELD_IMPACT[field])
    if any(change["field"] in {"layout_style", "page_size", "visual_density", "response_space"} for change in changes):
        affected.add("material_design")
    return {
        "changes": changes,
        "material_fields": [change["field"] for change in material_changes],
        "requires_confirmation": bool(material_changes),
        "affected_intents": [intent for intent in ROUTE_ORDER if intent in affected],
    }
