from __future__ import annotations

MISCONCEPTION_CONFIDENCE = {"low", "medium", "high"}
PROPOSED_MOVES = {
    "exemplar_contrast",
    "guided_discrimination",
    "corrective_rehearsal",
    "reteach_concept",
    "remediate_prerequisite",
}
ACTION_RESULTS = {"not-yet-tried", "helped", "mixed", "did-not-help"}
RETEACHING_PHASES = (
    "reconnect_prerequisite",
    "contrast",
    "guided_discrimination",
    "corrective_rehearsal",
    "transfer",
)


def _string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(_string(item) for item in value)


def validate_reteaching_plan(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-reteaching-plan.v1":
        errors.append("schema_version must be zamery-reteaching-plan.v1")
    if not _string(data.get("plan_id")):
        errors.append("plan_id must be a non-empty string")
    for field in ("objective_ids", "evidence_ids"):
        if not _string_list(data.get(field)):
            errors.append(f"{field} must be a non-empty list")

    misconception = data.get("misconception")
    if not isinstance(misconception, dict):
        errors.append("misconception must be an object")
    else:
        if not _string(misconception.get("statement")):
            errors.append("misconception.statement must be a non-empty string")
        if misconception.get("confidence") not in MISCONCEPTION_CONFIDENCE:
            errors.append("misconception.confidence must be low, medium, or high")
        if not isinstance(misconception.get("competing_explanations"), list):
            errors.append("misconception.competing_explanations must be a list")

    if data.get("phases") != list(RETEACHING_PHASES):
        errors.append("reteaching phases must follow the approved corrective sequence")
    action = data.get("teacher_action")
    if not isinstance(action, dict):
        errors.append("teacher_action must be an object")
    else:
        for field in (
            "action_id",
            "based_on_snapshot_id",
            "snapshot_expires_at",
            "target",
            "rationale",
            "trial_window",
            "expected_signal",
            "review_date",
        ):
            if not _string(action.get(field)):
                errors.append(f"teacher_action.{field} must be a non-empty string")
        if not _string_list(action.get("evidence_ids")):
            errors.append("teacher_action.evidence_ids must be a non-empty list")
        if action.get("proposed_move") not in PROPOSED_MOVES:
            errors.append("teacher_action.proposed_move is invalid")
        preserves = action.get("preserves")
        required = {"shared_objective", "assessment_construct", "learner_dignity"}
        if not isinstance(preserves, list) or not required.issubset(set(preserves)):
            errors.append(
                "teacher action must preserve shared_objective, assessment_construct, and learner_dignity"
            )
        trial_sessions = action.get("trial_sessions")
        if (
            isinstance(trial_sessions, bool)
            or not isinstance(trial_sessions, int)
            or not 1 <= trial_sessions <= 5
        ):
            errors.append("teacher_action.trial_sessions must be an integer from 1 through 5")
        if action.get("teacher_approval") is not True:
            errors.append("teacher action requires teacher approval")
        if action.get("result") not in ACTION_RESULTS:
            errors.append("teacher_action.result is invalid")
        if not isinstance(action.get("confounding_factors"), list):
            errors.append("teacher_action.confounding_factors must be a list")
        interpretation = action.get("teacher_interpretation")
        if interpretation is not None and not _string(interpretation):
            errors.append("teacher_action.teacher_interpretation must be non-empty when supplied")

    reassessment = data.get("reassessment")
    if not isinstance(reassessment, dict):
        errors.append("reteaching plan requires a reassessment object")
    else:
        if not _string_list(reassessment.get("objective_ids")):
            errors.append("reassessment.objective_ids must be a non-empty list")
        if not _string(reassessment.get("success_evidence")):
            errors.append("reassessment.success_evidence must be a non-empty string")
        item_count = reassessment.get("item_count", 5)
        if isinstance(item_count, bool) or not isinstance(item_count, int) or item_count < 1:
            errors.append("reassessment.item_count must be a positive integer")
        wait_days = reassessment.get("wait_days", 2)
        if (
            isinstance(wait_days, bool)
            or not isinstance(wait_days, int)
            or not 0 <= wait_days <= 7
        ):
            errors.append("reassessment.wait_days must be an integer from 0 through 7")
        if not isinstance(reassessment.get("auto_schedule", True), bool):
            errors.append("reassessment.auto_schedule must be boolean")
    return errors
