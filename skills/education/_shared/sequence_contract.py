from __future__ import annotations

SOURCE_AUTHORITIES = {
    "authorized_channel",
    "licensed",
    "model_generated",
    "public_primary_source",
    "teacher_supplied",
}
TRANSFER_LEVELS = {"near", "far"}


def _string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(_string(item) for item in value)


def _validate_objective_entries(
    entries: object,
    field: str,
    known: set[str],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(entries, list) or not entries:
        return [f"{field} must be a non-empty list"]
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"{field}[{index}] must be an object")
            continue
        session = entry.get("session")
        if isinstance(session, bool) or not isinstance(session, int) or session < 1:
            errors.append(f"{field}[{index}] session must be a positive integer")
        objective_ids = entry.get("objective_ids")
        if (
            not isinstance(objective_ids, list)
            or not objective_ids
            or not all(_string(objective_id) for objective_id in objective_ids)
        ):
            errors.append(f"{field}[{index}] objective_ids must be a non-empty list")
            continue
        normalized_objective_ids = [
            objective_id for objective_id in objective_ids if isinstance(objective_id, str)
        ]
        for objective_id in normalized_objective_ids:
            if objective_id not in known:
                errors.append(f"{field}[{index}] cites unknown objective '{objective_id}'")
    return errors


def validate_learning_sequence(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-learning-sequence.v1":
        errors.append("schema_version must be zamery-learning-sequence.v1")
    if not _string(data.get("sequence_id")):
        errors.append("sequence_id must be a non-empty string")
    if data.get("source_authority") not in SOURCE_AUTHORITIES:
        errors.append(f"source_authority must be one of {', '.join(sorted(SOURCE_AUTHORITIES))}")

    duration = data.get("duration_weeks")
    if isinstance(duration, bool) or not isinstance(duration, int) or duration < 1:
        errors.append("duration_weeks must be a positive integer")

    raw_objective_ids = data.get("objective_ids")
    if not _string_list(raw_objective_ids):
        errors.append("objective_ids must be a non-empty list of strings")
    objective_ids = (
        [objective_id for objective_id in raw_objective_ids if isinstance(objective_id, str)]
        if isinstance(raw_objective_ids, list)
        else []
    )
    if len(objective_ids) != len(set(objective_ids)):
        errors.append("objective_ids must be unique")
    known = set(objective_ids)

    edges = data.get("prerequisite_edges")
    if not isinstance(edges, list):
        errors.append("prerequisite_edges must be a list")
    else:
        for index, edge in enumerate(edges):
            if not isinstance(edge, dict):
                errors.append(f"prerequisite_edges[{index}] must be an object")
                continue
            for key in ("from", "to"):
                value = edge.get(key)
                if not _string(value):
                    errors.append(f"prerequisite_edges[{index}] {key} must be a non-empty string")
                elif value not in known:
                    errors.append(f"prerequisite_edges[{index}] {key} '{value}' is not in objective_ids")

    coverage = data.get("coverage")
    if not isinstance(coverage, list) or not coverage:
        errors.append("coverage must be a non-empty list")
    else:
        covered: set[str] = set()
        for index, entry in enumerate(coverage):
            if not isinstance(entry, dict):
                errors.append(f"coverage[{index}] must be an object")
                continue
            objective_id = entry.get("objective_id")
            if not _string(objective_id):
                errors.append(f"coverage[{index}] objective_id must be a non-empty string")
            elif isinstance(objective_id, str) and objective_id not in known:
                errors.append(f"coverage[{index}] cites unknown objective '{objective_id}'")
            elif isinstance(objective_id, str):
                covered.add(objective_id)
            sessions = entry.get("sessions")
            if not isinstance(sessions, list) or not sessions:
                errors.append(f"coverage[{index}] sessions must be a non-empty list of ints")
            else:
                for session_index, session in enumerate(sessions):
                    if isinstance(session, bool) or not isinstance(session, int) or session < 1:
                        errors.append(f"coverage[{index}] sessions[{session_index}] must be a positive integer")
                if len(sessions) != len(set(sessions)):
                    errors.append(f"coverage[{index}] session numbers must be unique")
        for objective_id in objective_ids:
            if objective_id not in covered:
                errors.append(f"objective '{objective_id}' has no coverage entries")

    errors.extend(_validate_objective_entries(data.get("review_schedule"), "review_schedule", known))
    errors.extend(_validate_objective_entries(data.get("assessment_windows"), "assessment_windows", known))

    transfer_levels = data.get("transfer_levels")
    if not isinstance(transfer_levels, list) or not transfer_levels:
        errors.append("transfer_levels must be a non-empty list")
    else:
        provided = set(transfer_levels)
        if not provided.issubset(TRANSFER_LEVELS):
            errors.append(f"transfer_levels entries must be from {', '.join(sorted(TRANSFER_LEVELS))}")
        if not TRANSFER_LEVELS.issubset(provided):
            errors.append("transfer_levels must include near and far")

    standards = data.get("standards_coverage")
    if standards is not None:
        if not isinstance(standards, dict):
            errors.append("standards_coverage must be an object")
        else:
            for key, value in standards.items():
                if not isinstance(value, dict) or not _string(value.get("standard_id")):
                    errors.append(f"standards_coverage.{key}.standard_id must be a non-empty string")
                    continue
                authority = value.get("authority")
                if authority is not None and authority not in SOURCE_AUTHORITIES:
                    errors.append(f"standards_coverage.{key}.authority is invalid")

    version = data.get("version")
    if version is not None and (
        isinstance(version, bool) or not isinstance(version, int) or version < 1
    ):
        errors.append("version must be a positive integer when supplied")
    prior = data.get("prior_sequence_id")
    if prior is not None and not _string(prior):
        errors.append("prior_sequence_id must be a non-empty string when supplied")
    revision_note = data.get("revision_note")
    if revision_note is not None and not _string(revision_note):
        errors.append("revision_note must be a non-empty string when supplied")
    return errors
