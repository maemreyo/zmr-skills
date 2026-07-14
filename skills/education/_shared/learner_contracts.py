from __future__ import annotations

import re

PROHIBITED_LEARNER_LABELS = (
    "addicted",
    "lazy",
    "low ability",
    "low",
    "naughty",
    "problem student",
    "unmotivated",
    "weak",
)
EVIDENCE_STATUSES = {"emerging", "developing", "secure"}
EVIDENCE_AUTHORITIES = {"teacher_reviewed", "authorised_school_record"}
SUMMARY_STATUSES = {*EVIDENCE_STATUSES, "not_observed"}
SUMMARY_FLAGS = {"plateau", "regression", "missing_evidence", "review_due"}
TREND_LABELS = {"improving", "stable", "plateau", "regressing", "insufficient"}
INTERPRETATION_CONFIDENCE = {"low", "medium", "high"}
PROHIBITED_LABEL_PATTERNS = tuple(
    (label, re.compile(rf"\b{re.escape(label)}\b", re.IGNORECASE))
    for label in PROHIBITED_LEARNER_LABELS
)


def _string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(_string(item) for item in value)


def _prohibited_labels(value: object, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            errors.extend(_prohibited_labels(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_prohibited_labels(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        for label, pattern in PROHIBITED_LABEL_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path} contains prohibited learner label {label}")
    return errors


def validate_student_card(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-student-card.v1":
        errors.append("schema_version must be zamery-student-card.v1")
    for field in ("card_id", "purpose"):
        if not _string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if data.get("owner") != "teacher-or-school":
        errors.append("owner must be teacher-or-school")

    consent = data.get("consent")
    if not isinstance(consent, dict):
        errors.append("consent must be an object")
    else:
        if consent.get("school_authority") is not True:
            errors.append("student card requires documented school authority")
        if not _string_list(consent.get("field_scope_ids")):
            errors.append("consent field_scope_ids must be a non-empty list")

    lifecycle = data.get("lifecycle")
    if not isinstance(lifecycle, dict):
        errors.append("lifecycle must be an object")
    else:
        for field in ("created_at", "reviewed_at", "next_review_at", "delete_at"):
            if not _string(lifecycle.get(field)):
                errors.append(f"lifecycle.{field} must be a non-empty string")

    if not isinstance(data.get("student_voice"), dict):
        errors.append("student_voice must be an object")
    evidence = data.get("learning_evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("learning_evidence must be a non-empty list")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"learning evidence {index} must be an object")
                continue
            for field in (
                "evidence_id",
                "objective_id",
                "observation",
                "source",
                "authority",
                "observed_at",
                "context",
                "evidence_reference",
                "expires_at",
                "reviewed_by",
                "review_status",
                "consent_scope_id",
                "dispute_status",
            ):
                if not _string(item.get(field)):
                    errors.append(f"learning_evidence {index}.{field} must be a non-empty string")
            if item.get("confidence") not in INTERPRETATION_CONFIDENCE:
                errors.append(f"learning_evidence {index}.confidence must be low, medium, or high")
            if not isinstance(item.get("counterevidence"), list):
                errors.append(f"learning_evidence {index}.counterevidence must be a list")
            observation = str(item.get("observation", ""))
            for label, pattern in PROHIBITED_LABEL_PATTERNS:
                if pattern.search(observation):
                    errors.append(f"learning evidence {index} contains prohibited learner label {label}")
    learning_conditions = data.get("learning_conditions")
    if not isinstance(learning_conditions, dict):
        errors.append("learning_conditions must be an object")
    else:
        for field in ("observations", "strategies_tried"):
            if not isinstance(learning_conditions.get(field), list):
                errors.append(f"learning_conditions.{field} must be a list")
    interests_and_routines = data.get("interests_and_routines")
    if not isinstance(interests_and_routines, dict):
        errors.append("interests_and_routines must be an object")
    else:
        for field in ("interest_tags", "reported_schedule_conflicts"):
            if not isinstance(interests_and_routines.get(field), list):
                errors.append(f"interests_and_routines.{field} must be a list")
    if not isinstance(data.get("authorised_support"), list):
        errors.append("authorised_support must be a list")
    if not isinstance(data.get("disputes"), list):
        errors.append("disputes must be a list")
    provenance = data.get("provenance")
    if not isinstance(provenance, dict) or not provenance:
        errors.append("provenance must be a non-empty object")
    errors.extend(_prohibited_labels(data, "student_card"))
    return errors


def validate_learning_trajectory(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-learning-trajectory.v1":
        errors.append("schema_version must be zamery-learning-trajectory.v1")
    for field in ("trajectory_id", "card_id", "objective_id", "review_due_at"):
        if not _string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    evidence = data.get("objective_evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("objective_evidence must be a non-empty list")
        return errors
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            errors.append(f"objective evidence {index} must be an object")
            continue
        for field in ("evidence_id", "observed_at"):
            if not _string(item.get(field)):
                errors.append(f"objective evidence {index} {field} must be a non-empty string")
        if item.get("status") not in EVIDENCE_STATUSES:
            errors.append(f"objective evidence {index} status is invalid")
        if item.get("authority") not in EVIDENCE_AUTHORITIES:
            errors.append(f"objective evidence {index} authority is invalid")
    trend = data.get("trend")
    if trend not in TREND_LABELS:
        errors.append("trend must be improving, stable, plateau, regressing, or insufficient")
    elif trend == "insufficient" and len(evidence) >= 3:
        errors.append("insufficient trend requires fewer than three dated evidence points")
    elif trend != "insufficient" and len(evidence) < 3:
        errors.append("descriptive trend requires at least three dated evidence points")
    return errors


def validate_evidence_summary(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for field in ("summary_id", "objective_id"):
        if not _string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")

    evidence_ids = data.get("evidence_ids")
    if not _string_list(evidence_ids):
        errors.append("evidence_ids must be a non-empty list")
    normalized_evidence_ids = (
        [item for item in evidence_ids if isinstance(item, str)]
        if isinstance(evidence_ids, list)
        else []
    )
    if normalized_evidence_ids and len(normalized_evidence_ids) != len(set(normalized_evidence_ids)):
        errors.append("evidence_ids must be unique")

    point_count = data.get("point_count")
    if isinstance(point_count, bool) or not isinstance(point_count, int) or point_count < 1:
        errors.append("point_count must be a positive integer")
    elif normalized_evidence_ids and point_count != len(normalized_evidence_ids):
        errors.append("point_count must equal the length of evidence_ids")

    if data.get("latest_status") not in SUMMARY_STATUSES:
        errors.append("latest_status must be one of emerging, developing, secure, not_observed")
    for field in ("first_observed_at", "latest_observed_at"):
        if not _string(data.get(field)):
            errors.append(f"{field} must be a non-empty ISO 8601 date string")
    first = str(data.get("first_observed_at", ""))
    latest = str(data.get("latest_observed_at", ""))
    if first and latest and first > latest:
        errors.append("first_observed_at must be earlier than or equal to latest_observed_at")

    flags = data.get("flags")
    if flags is not None:
        if not isinstance(flags, list):
            errors.append("flags must be a list")
        elif not set(flags).issubset(SUMMARY_FLAGS):
            errors.append(f"flags must be a subset of {SUMMARY_FLAGS}")
    return errors
