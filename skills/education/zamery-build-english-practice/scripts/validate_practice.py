from __future__ import annotations

import json
import sys
from collections.abc import Mapping
from pathlib import Path

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

RESPONSE_LINE_MINIMUMS = {
    "selected_response": 1,
    "short_answer": 2,
    "explanation": 4,
    "two_sentence_transfer": 5,
}
INTERACTIONS = {
    "single_choice", "multiple_choice", "true_false", "matching", "ordering",
    "categorization", "fill_blank", "cloze", "dropdown_cloze", "short_answer",
    "extended_response", "error_correction", "sentence_transformation",
    "sentence_combining", "word_formation", "table_completion", "note_completion",
    "summary_completion", "labeling", "hotspot", "drag_drop", "dictation", "essay",
    "oral_response", "audio_recording", "dialogue_completion",
    "timestamped_video_response", "portfolio_evidence",
}
RESPONSE_MODES = {"selected", "constructed", "spoken", "performance", "mixed"}
COGNITIVE_OPERATIONS = {"remember", "understand", "apply", "analyze", "evaluate", "create"}


def _non_empty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _leaks(value: object, path: str = "student_artifact") -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).casefold() in LEAK_FIELDS:
                errors.append(f"student answer leakage at {child_path}")
            errors.extend(_leaks(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_leaks(child, f"{path}[{index}]"))
    return errors


def validate_practice(data: dict[str, object]) -> list[str]:
    """Validate student-only practice identity, alignment, progression, and leakage."""
    errors: list[str] = []
    if not isinstance(data.get("artifact_id"), str) or not str(data["artifact_id"]).strip():
        errors.append("artifact_id must be a non-empty string")
    if data.get("audience") != "student":
        errors.append("practice audience must be student")

    declared = data.get("objective_ids")
    if not _non_empty_strings(declared):
        errors.append("objective_ids must be a non-empty list")
        known: set[str] = set()
    else:
        known = set(declared)

    errors.extend(_leaks(data))

    items = data.get("items")
    item_ids: list[str] = []
    covered: set[str] = set()
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty list")
    else:
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"item {index} must be an object")
                continue
            item_id = item.get("item_id")
            if not isinstance(item_id, str) or not item_id.strip():
                errors.append(f"item {index} requires a non-empty item_id")
                continue
            item_ids.append(item_id)
            if data.get("schema_version") == "zamery-practice.v3":
                if item.get("interaction") not in INTERACTIONS:
                    errors.append(f"item {item_id} has unsupported interaction")
                if item.get("response_mode") not in RESPONSE_MODES:
                    errors.append(f"item {item_id} has unsupported response_mode")
                if item.get("cognitive_operation") not in COGNITIVE_OPERATIONS:
                    errors.append(f"item {item_id} has unsupported cognitive_operation")
            response_type = item.get("response_type")
            if response_type not in RESPONSE_LINE_MINIMUMS:
                errors.append(f"item {item_id} has unsupported response_type")
            else:
                lines = item.get("expected_response_lines")
                minimum = RESPONSE_LINE_MINIMUMS[response_type]
                if not isinstance(lines, int) or isinstance(lines, bool) or lines < minimum:
                    errors.append(f"item {item_id} requires at least {minimum} response lines for {response_type}")
            if not isinstance(item.get("layout_intent"), str) or not str(item["layout_intent"]).strip():
                errors.append(f"item {item_id} requires layout_intent")
            refs = item.get("objective_ids")
            if not _non_empty_strings(refs):
                errors.append(f"item {item_id} objective_ids must be a non-empty list")
                continue
            for objective_id in refs:
                if objective_id not in known:
                    errors.append(f"item {item_id} cites unknown objective {objective_id}")
                else:
                    covered.add(str(objective_id))
        if len(item_ids) != len(set(item_ids)):
            errors.append("item IDs must be unique")

    for objective_id in declared if isinstance(declared, list) else []:
        if objective_id not in covered:
            errors.append(f"objective {objective_id} is not covered by any item")

    progression = data.get("progression")
    if not isinstance(progression, list) or not {"guided", "independent"}.issubset(progression):
        errors.append("progression requires guided and independent practice")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_practice.py PRACTICE.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate_practice(data)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
