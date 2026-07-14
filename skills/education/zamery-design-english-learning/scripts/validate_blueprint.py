from __future__ import annotations

import json
import sys
from pathlib import Path

GRADE_BANDS = {"k_2", "grades_3_5", "grades_6_8", "grades_9_12"}


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_blueprint(data: dict[str, object]) -> list[str]:
    """Return stable human-readable contract errors; return [] on success."""
    errors: list[str] = []
    for field in (
        "blueprint_id",
        "grade_band",
        "target_language",
        "instruction_language",
    ):
        if not _non_empty_string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if data.get("grade_band") not in GRADE_BANDS:
        errors.append("grade_band must be a supported K–12 band")

    duration = data.get("duration_minutes")
    if isinstance(duration, bool) or not isinstance(duration, int) or not 10 <= duration <= 180:
        errors.append("duration_minutes must be an integer from 10 through 180")

    objectives = data.get("objectives")
    objective_ids: list[str] = []
    if not isinstance(objectives, list) or not objectives:
        errors.append("objectives must be a non-empty list")
    else:
        for index, objective in enumerate(objectives):
            if not isinstance(objective, dict) or not _non_empty_string(objective.get("objective_id")):
                errors.append(f"objective {index} requires a non-empty objective_id")
                continue
            objective_ids.append(str(objective["objective_id"]))
        if len(objective_ids) != len(set(objective_ids)):
            errors.append("objective IDs must be unique")

    phases = data.get("phases")
    phase_minutes = 0
    covered_objectives: set[str] = set()
    if not isinstance(phases, list) or not phases:
        errors.append("phases must be a non-empty list")
    else:
        known = set(objective_ids)
        for index, phase in enumerate(phases):
            if not isinstance(phase, dict):
                errors.append(f"phase {index} must be an object")
                continue
            minutes = phase.get("minutes")
            if isinstance(minutes, bool) or not isinstance(minutes, int) or minutes <= 0:
                errors.append(f"phase {index} minutes must be a positive integer")
            else:
                phase_minutes += minutes
            refs = phase.get("objective_ids")
            if not isinstance(refs, list) or not refs:
                errors.append(f"phase {index} objective_ids must be a non-empty list")
            else:
                for objective_id in refs:
                    if objective_id not in known:
                        errors.append(f"phase {index} cites unknown objective {objective_id}")
                    else:
                        covered_objectives.add(str(objective_id))

    for objective_id in objective_ids:
        if objective_id not in covered_objectives:
            errors.append(f"objective {objective_id} is not covered by any phase")
    if isinstance(duration, int) and not isinstance(duration, bool) and phase_minutes != duration:
        errors.append("phase minutes must equal duration_minutes")

    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("provenance must be an object")
    elif provenance.get("cefr") == "derived_from_grade":
        errors.append("cefr provenance may not be derived_from_grade")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_blueprint.py BLUEPRINT.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate_blueprint(data)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
