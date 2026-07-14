from __future__ import annotations

from collections.abc import Mapping

from .learning_contracts import (
    validate_brief_version_assertion,
    validate_communication,
    validate_evidence_summary,
    validate_learning_sequence,
    validate_learning_trajectory,
    validate_reteaching_plan,
    validate_student_card,
)

__all__ = (
    "validate_brief_version_assertion",
    "validate_communication",
    "validate_evidence_summary",
    "validate_learning_sequence",
    "validate_learning_trajectory",
    "validate_reteaching_plan",
    "validate_student_card",
)

PROVENANCE = {"explicit", "inferred", "defaulted", "unresolved"}
GRADE_BANDS = {"k_2", "grades_3_5", "grades_6_8", "grades_9_12"}
LEAK_FIELDS = {
    "answer",
    "answer_key",
    "accepted_answers",
    "correct_answer",
    "correct_option_ids",
    "explanation",
    "rubric",
    "wrong_reasons",
}
ZAMERY_SKILL_NAMES = (
    "zamery-design-english-learning",
    "zamery-teach-english-concepts",
    "zamery-build-english-practice",
    "zamery-build-english-item-banks",
    "zamery-compose-english-assessments",
    "zamery-create-ielts-practice",
    "zamery-build-video-learning",
    "zamery-design-teaching-materials",
    "zamery-create-english-presentations",
    "zamery-analyze-student-work",
    "zamery-review-publish-pack",
    "zamery-teacher-copilot",
    "zamery-understand-learners",
    "zamery-monitor-english-learning",
    "zamery-plan-english-reteaching",
    "zamery-design-english-learning-sequences",
)

RESPONSE_INTERACTIONS = {
    "single_choice",
    "multiple_choice",
    "true_false",
    "matching",
    "ordering",
    "categorization",
    "fill_blank",
    "cloze",
    "dropdown_cloze",
    "short_answer",
    "extended_response",
    "error_correction",
    "sentence_transformation",
    "sentence_combining",
    "word_formation",
    "table_completion",
    "note_completion",
    "summary_completion",
    "labeling",
    "hotspot",
    "drag_drop",
    "dictation",
    "essay",
    "oral_response",
    "audio_recording",
    "dialogue_completion",
    "timestamped_video_response",
    "portfolio_evidence",
}
ITEM_STATUSES = {"draft", "review", "approved", "retired"}
RESPONSE_MODES = {"selected", "constructed", "spoken", "performance", "mixed"}
COGNITIVE_OPERATIONS = {
    "remember",
    "understand",
    "apply",
    "analyze",
    "evaluate",
    "create",
}
SOURCE_AUTHORITIES = {
    "teacher_supplied",
    "licensed",
    "public_primary_source",
    "authorized_channel",
    "model_generated",
}

ZAMERY_PALETTE = {
    "ink_navy": "#17324D",
    "root_terracotta": "#B85435",
    "growth_teal": "#2B746F",
    "warm_sand": "#F4EEE4",
    "sky_mist": "#DCEAF2",
    "charcoal": "#202B33",
    "paper_white": "#FFFFFF",
}
FORBIDDEN_VISIBLE_TERMS = (
    "original prompt",
    "example user prompt",
    "route plan",
    "review_publish",
    "raw_request",
    "grade_band",
    "instruction_language",
    "qa gate",
)


def _non_empty_list(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item for item in value)
    )


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_canonical_item(data: dict[str, object]) -> list[str]:
    """Validate the portable Zamery V3 item record used by JSONL and SQLite."""
    errors: list[str] = []
    if data.get("schema_version") != "zamery-item.v3":
        errors.append("schema_version must be zamery-item.v3")
    for field in ("item_id", "language", "domain", "skill", "stem", "rationale"):
        if not _non_empty_string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    version = data.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version < 1:
        errors.append("version must be a positive integer")
    if data.get("status") not in ITEM_STATUSES:
        errors.append("status must be draft, review, approved, or retired")
    if data.get("grade_band") not in GRADE_BANDS:
        errors.append("grade_band must be a supported K–12 band")
    if not _non_empty_string(data.get("cefr")):
        errors.append("cefr must be a non-empty string")
    if not _non_empty_list(data.get("objective_ids")):
        errors.append("objective_ids must be a non-empty list")
    interaction = data.get("interaction")
    if interaction not in RESPONSE_INTERACTIONS:
        errors.append("interaction is not in the Zamery V3 taxonomy")
    if data.get("response_mode") not in RESPONSE_MODES:
        errors.append("response_mode is invalid")
    if data.get("cognitive_operation") not in COGNITIVE_OPERATIONS:
        errors.append("cognitive_operation is invalid")
    difficulty = data.get("difficulty")
    if (
        isinstance(difficulty, bool)
        or not isinstance(difficulty, (int, float))
        or not 0 <= difficulty <= 1
    ):
        errors.append("difficulty must be a number between 0 and 1")
    if not isinstance(data.get("answer"), dict) or not data["answer"]:
        errors.append("answer must be a non-empty object")
    if not isinstance(data.get("tags"), list):
        errors.append("tags must be a list")

    anchors = data.get("source_anchors")
    if not isinstance(anchors, list) or not anchors:
        errors.append("source_anchors must be a non-empty list")
    else:
        for index, anchor in enumerate(anchors):
            if not isinstance(anchor, dict):
                errors.append(f"source anchor {index} must be an object")
                continue
            if not _non_empty_string(anchor.get("source_id")):
                errors.append(f"source anchor {index} source_id must be a non-empty string")
            if anchor.get("authority") not in SOURCE_AUTHORITIES:
                errors.append(f"source anchor {index} authority is invalid")
            if not _non_empty_string(anchor.get("locator")):
                errors.append(f"source anchor {index} locator must be a non-empty string")

    if interaction in {"single_choice", "multiple_choice"}:
        options = data.get("options")
        answer = data.get("answer")
        option_ids: list[object] = []
        if not isinstance(options, list) or len(options) < 2:
            errors.append("choice items require at least two options")
        else:
            option_ids = [option.get("option_id") for option in options if isinstance(option, dict)]
            if len(option_ids) != len(options) or len(option_ids) != len(set(option_ids)):
                errors.append("option IDs must be present and unique")
        correct_ids = answer.get("correct_option_ids") if isinstance(answer, dict) else None
        if not isinstance(correct_ids, list) or not correct_ids:
            errors.append("choice answer requires correct_option_ids")
        elif not set(correct_ids).issubset(set(option_ids)):
            errors.append("correct option IDs must exist in options")
    return errors


def validate_batch_manifest(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-batch.v3":
        errors.append("schema_version must be zamery-batch.v3")
    if not _non_empty_string(data.get("batch_id")):
        errors.append("batch_id must be a non-empty string")
    count = data.get("requested_count")
    chunk = data.get("chunk_size")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        errors.append("requested_count must be a positive integer")
    if (
        isinstance(chunk, bool)
        or not isinstance(chunk, int)
        or chunk < 1
        or not isinstance(count, int)
        or isinstance(count, bool)
        or chunk > count
    ):
        errors.append("chunk_size must be between 1 and requested_count")
    completed = data.get("completed_item_ids")
    if not isinstance(completed, list):
        errors.append("completed_item_ids must be a list")
    elif len(completed) != len(set(completed)):
        errors.append("completed_item_ids must be unique")
    elif isinstance(count, int) and not isinstance(count, bool) and len(completed) > count:
        errors.append("completed_item_ids cannot exceed requested_count")
    seed = data.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        errors.append("seed must be an integer")
    if data.get("status") not in {"planned", "in_progress", "complete", "failed"}:
        errors.append("batch status is invalid")
    return errors


def validate_form_manifest(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-form.v3":
        errors.append("schema_version must be zamery-form.v3")
    for field in ("form_id", "blueprint_id"):
        if not _non_empty_string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    seed = data.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        errors.append("seed must be an integer")
    items = data.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty list")
    else:
        ids: list[object] = []
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"form item {index} must be an object")
                continue
            ids.append(item.get("item_id"))
            if not _non_empty_string(item.get("item_id")):
                errors.append(f"form item {index} item_id must be a non-empty string")
            version = item.get("version")
            if isinstance(version, bool) or not isinstance(version, int) or version < 1:
                errors.append(f"form item {index} version must be a positive integer")
            if not _non_empty_string(item.get("section_id")):
                errors.append(f"form item {index} section_id must be a non-empty string")
        if len(ids) != len(set(ids)):
            errors.append("form item IDs must be unique")
    return errors


def validate_media_manifest(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-media.v3":
        errors.append("schema_version must be zamery-media.v3")
    for field in ("media_id", "url"):
        if not _non_empty_string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    duration = data.get("duration_seconds")
    if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration <= 0:
        errors.append("duration_seconds must be positive")
    transcript = data.get("transcript")
    if not isinstance(transcript, dict):
        errors.append("transcript must be an object")
    else:
        authority = transcript.get("authority")
        status = transcript.get("grounding_status")
        if authority not in {
            "teacher_supplied",
            "authorized_channel",
            "licensed",
            "public_link_only",
            "none",
        }:
            errors.append("transcript authority is invalid")
        if status not in {"verified", "grounded", "ungrounded", "unavailable"}:
            errors.append("transcript grounding_status is invalid")
        if authority == "public_link_only" and status in {"verified", "grounded"}:
            errors.append("public_link_only transcripts cannot be marked verified")
        required = transcript.get("teacher_verification_required")
        if authority == "public_link_only" and required is not True:
            errors.append("public_link_only requires teacher verification")
    accessibility = data.get("accessibility")
    if not isinstance(accessibility, dict):
        errors.append("accessibility must be an object")
    else:
        if not isinstance(accessibility.get("captions_available"), bool):
            errors.append("captions_available must be boolean")
        if not isinstance(accessibility.get("alternative_text"), bool):
            errors.append("alternative_text must be boolean")
    return errors


def validate_teaching_brief(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for field in (
        "brief_id",
        "raw_request",
        "grade_band",
        "target_language",
        "instruction_language",
    ):
        if not isinstance(data.get(field), str) or not data[field]:
            errors.append(f"{field} must be a non-empty string")
    if data.get("grade_band") not in GRADE_BANDS:
        errors.append("grade_band must be a supported K–12 band")
    if not _non_empty_list(data.get("artifact_types")):
        errors.append("artifact_types must be a non-empty list")
    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("provenance must be an object")
        return errors
    for field in ("grade_band", "cefr"):
        value = provenance.get(field)
        if value not in PROVENANCE and value != "not_supplied":
            errors.append(f"{field} provenance is invalid")
    if provenance.get("cefr") == "derived_from_grade":
        errors.append("cefr provenance may not be derived_from_grade")
    return errors


def validate_brand_contract(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("system_id") != "zamery-core.v2":
        errors.append("system_id must be zamery-core.v2")
    if data.get("brand_name") != "zamery" or data.get("tagline") != "rooted in strength":
        errors.append("brand name and tagline must match Zamery Core")
    wordmark = data.get("wordmark")
    if not isinstance(wordmark, dict) or wordmark.get("text") != "zamery":
        errors.append("wordmark must declare lowercase zamery text")
    palette = data.get("palette")
    if palette != ZAMERY_PALETTE:
        errors.append("palette must exactly match Zamery Core V2")
    typography = data.get("typography")
    if not isinstance(typography, dict) or typography.get("primary_family") != "Arial":
        errors.append("typography must use Arial as the primary family")
    elif typography.get("print_body_min_pt") != 9.5:
        errors.append("print body minimum must be 9.5 pt")
    if data.get("logo") is not None:
        errors.append("pictorial logo must remain null until supplied")
    return errors


def validate_layout_contract(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("layout_version") != "zamery-layout.v2":
        errors.append("layout_version must be zamery-layout.v2")
    for field in ("artifact_id", "artifact_type", "audience"):
        if not isinstance(data.get(field), str) or not str(data[field]).strip():
            errors.append(f"{field} must be a non-empty string")

    page_roles = data.get("page_roles")
    if not _non_empty_list(page_roles):
        errors.append("page_roles must be a non-empty string list")

    visible_text = data.get("visible_text")
    if not isinstance(visible_text, list):
        errors.append("visible_text must be a list")
    else:
        visible = "\n".join(str(value) for value in visible_text).casefold()
        for term in FORBIDDEN_VISIBLE_TERMS:
            if term in visible:
                errors.append(f"visible content contains forbidden internal term {term}")

    brand = data.get("brand")
    if not isinstance(brand, dict) or brand.get("system_id") != "zamery-core.v2":
        errors.append("layout must use zamery-core.v2")
    else:
        applications = brand.get("applications")
        if not isinstance(applications, list) or not applications:
            errors.append("brand applications must be a non-empty list")
        elif not any(application != "footer_text" for application in applications):
            errors.append("brand must be applied beyond footer text")

    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        errors.append("pages must be a non-empty list")
    else:
        actual_roles: set[str] = set()
        for index, page in enumerate(pages):
            if not isinstance(page, dict):
                errors.append(f"page {index} must be an object")
                continue
            role = page.get("role")
            if isinstance(role, str):
                actual_roles.add(role)
            ratio = page.get("occupied_ratio")
            if not isinstance(ratio, (int, float)) or isinstance(ratio, bool) or not 0 <= ratio <= 1:
                errors.append(f"page {index} occupied_ratio must be between 0 and 1")
            elif ratio < 0.25 and not page.get("intentional_sparse"):
                errors.append(f"page {index} is unintentionally sparse")
        if isinstance(page_roles, list):
            for role in page_roles:
                if role not in actual_roles:
                    errors.append(f"page role {role} is not represented")
    return errors


def validate_artifact(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for field in (
        "artifact_id",
        "artifact_type",
        "audience",
        "brief_id",
        "grade_band",
        "target_language",
        "instruction_language",
        "authority",
    ):
        if not isinstance(data.get(field), str) or not data[field]:
            errors.append(f"{field} must be a non-empty string")
    version = data.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version < 1:
        errors.append("version must be a positive integer")
    if data.get("grade_band") not in GRADE_BANDS:
        errors.append("grade_band must be a supported K–12 band")
    if not _non_empty_list(data.get("objective_ids")):
        errors.append("objective_ids must be a non-empty list")
    if not _non_empty_list(data.get("methodology_lineage")):
        errors.append("methodology_lineage must be a non-empty list")
    if not isinstance(data.get("source_references"), list):
        errors.append("source_references must be a list")
    if not isinstance(data.get("accessibility"), dict):
        errors.append("accessibility must be an object")
    if not isinstance(data.get("dependencies"), list):
        errors.append("dependencies must be a list")
    brand = data.get("brand")
    if not isinstance(brand, dict):
        errors.append("brand must be an object")
    elif brand.get("name") != "zamery" or brand.get("tagline") != "rooted in strength":
        errors.append("brand name and tagline must match the Zamery contract")
    return errors


def _walk(value: object, path: str = "student_artifact") -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).casefold() in LEAK_FIELDS:
                errors.append(f"student answer leakage at {child_path}")
            errors.extend(_walk(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_walk(child, f"{path}[{index}]"))
    return errors


def validate_assessment_bundle(data: dict[str, object]) -> list[str]:
    student = data.get("student_artifact")
    answer_set = data.get("answer_set")
    if not isinstance(student, dict) or not isinstance(answer_set, dict):
        return ["assessment bundle requires student_artifact and answer_set objects"]
    errors = validate_artifact(student)
    errors.extend(validate_artifact(answer_set))
    if answer_set.get("audience") != "teacher":
        errors.append("AnswerSet must be teacher-only")
    if answer_set.get("source_artifact_id") != student.get("artifact_id"):
        errors.append("AnswerSet source_artifact_id must match the student artifact")
    errors.extend(_walk(student))
    questions = student.get("questions")
    answers = answer_set.get("answers")
    if not isinstance(questions, list) or not isinstance(answers, list):
        errors.append("questions and answers must be lists")
        return errors
    question_ids = [item.get("question_id") for item in questions if isinstance(item, dict)]
    answer_ids = [item.get("question_id") for item in answers if isinstance(item, dict)]
    if len(question_ids) != len(set(question_ids)):
        errors.append("question IDs must be unique")
    if set(question_ids) != set(answer_ids):
        errors.append("AnswerSet question IDs must exactly match student question IDs")
    return errors
