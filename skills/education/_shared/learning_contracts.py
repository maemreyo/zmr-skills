from __future__ import annotations

from collections.abc import Mapping

from .learner_contracts import (
    validate_evidence_summary,
    validate_learning_trajectory,
    validate_student_card,
)
from .reteaching_contract import validate_reteaching_plan
from .sequence_contract import validate_learning_sequence

COMMUNICATION_AUDIENCES = {"student", "family"}
COMMUNICATION_TYPES = {
    "family_update_letter",
    "learner_progress_report",
    "student_goal_review",
}
PROTECTED_COMMUNICATION_FIELDS = {
    "behaviour_narrative",
    "diagnosis",
    "protected_profile_data",
    "student_card",
    "student_card_id",
}

__all__ = (
    "validate_brief_version_assertion",
    "validate_communication",
    "validate_evidence_summary",
    "validate_learning_sequence",
    "validate_learning_trajectory",
    "validate_reteaching_plan",
    "validate_student_card",
)


def _non_empty_list(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item for item in value)
    )


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_brief_version_assertion(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-brief-version-assertion.v1":
        errors.append("schema_version must be zamery-brief-version-assertion.v1")
    if not _non_empty_string(data.get("brief_id")):
        errors.append("brief_id must be a non-empty string")
    brief_version = data.get("brief_version")
    if isinstance(brief_version, bool) or not isinstance(brief_version, int) or brief_version < 1:
        errors.append("brief_version must be a positive integer")
    if data.get("teacher_approved") is not True:
        errors.append("teacher_approved must be true")
    if not _non_empty_list(data.get("objective_ids")):
        errors.append("objective_ids must be a non-empty list")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, list):
        errors.append("dependencies must be a list")
        return errors
    for index, dependency in enumerate(dependencies):
        if not isinstance(dependency, dict):
            errors.append(f"dependency {index} must be an object")
            continue
        if not _non_empty_string(dependency.get("artifact_id")):
            errors.append(f"dependency {index} artifact_id must be a non-empty string")
        approved_version = dependency.get("approved_version")
        current_version = dependency.get("current_version")
        for field, value in (
            ("approved_version", approved_version),
            ("current_version", current_version),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                errors.append(f"dependency {index} {field} must be a positive integer")
        if (
            isinstance(approved_version, int)
            and not isinstance(approved_version, bool)
            and isinstance(current_version, int)
            and not isinstance(current_version, bool)
            and approved_version != current_version
        ):
            errors.append(f"dependency {index} is stale")
    return errors


def _find_protected_communication_fields(value: object, path: str = "communication") -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).casefold() in PROTECTED_COMMUNICATION_FIELDS:
                errors.append(f"protected learner data at {child_path}")
            errors.extend(_find_protected_communication_fields(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_find_protected_communication_fields(child, f"{path}[{index}]"))
    return errors


def validate_communication(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-communication.v1":
        errors.append("schema_version must be zamery-communication.v1")
    for field in ("communication_id", "brief_id", "consent_scope_id"):
        if not _non_empty_string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if data.get("communication_type") not in COMMUNICATION_TYPES:
        errors.append("communication_type is invalid")
    if data.get("audience") not in COMMUNICATION_AUDIENCES:
        errors.append("audience must be student or family")
    if data.get("framing") != "positive_factual":
        errors.append("framing must be positive_factual")
    if data.get("source_scope") != "approved_progress_facts":
        errors.append("source_scope must be approved_progress_facts")
    if data.get("consent_confirmed") is not True:
        errors.append("consent_confirmed must be true")
    approved_fact_ids = data.get("approved_fact_ids")
    if not _non_empty_list(approved_fact_ids):
        errors.append("approved_fact_ids must be a non-empty list")
    approved = set(approved_fact_ids) if isinstance(approved_fact_ids, list) else set()
    messages = data.get("messages")
    if not isinstance(messages, list) or not messages:
        errors.append("messages must be a non-empty list")
    else:
        for index, message in enumerate(messages):
            if not isinstance(message, dict):
                errors.append(f"message {index} must be an object")
                continue
            if not _non_empty_string(message.get("text")):
                errors.append(f"message {index} text must be a non-empty string")
            fact_ids = message.get("fact_ids")
            if not _non_empty_list(fact_ids):
                errors.append(f"message {index} fact_ids must be a non-empty list")
            elif isinstance(fact_ids, list) and not set(fact_ids).issubset(approved):
                errors.append(f"message {index} cites an unapproved fact")
    errors.extend(_find_protected_communication_fields(data))
    return errors
