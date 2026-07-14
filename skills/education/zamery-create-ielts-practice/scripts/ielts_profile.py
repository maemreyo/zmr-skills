from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

LISTENING_TASK_FAMILIES = {
    "multiple_choice",
    "matching",
    "plan_map_diagram_labelling",
    "form_note_table_flowchart_summary_completion",
    "sentence_completion",
    "short_answer",
}
READING_TASK_FAMILIES = {
    "multiple_choice",
    "true_false_not_given",
    "yes_no_not_given",
    "matching_information",
    "matching_headings",
    "matching_features",
    "matching_sentence_endings",
    "sentence_completion",
    "summary_note_table_flowchart_completion",
    "diagram_label_completion",
    "short_answer",
}
COMPLETION_FAMILIES = {
    "form_note_table_flowchart_summary_completion",
    "sentence_completion",
    "summary_note_table_flowchart_completion",
    "diagram_label_completion",
    "short_answer",
}
WRITING_CRITERIA = {
    "task_achievement_or_response",
    "coherence_and_cohesion",
    "lexical_resource",
    "grammatical_range_and_accuracy",
}
SPEAKING_CRITERIA = {
    "fluency_and_coherence",
    "lexical_resource",
    "grammatical_range_and_accuracy",
    "pronunciation",
}


def validate_blueprint(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-ielts-blueprint.v3":
        errors.append("schema_version must be zamery-ielts-blueprint.v3")
    profile = data.get("profile")
    if profile not in {"academic", "general_training"}:
        errors.append("profile must be academic or general_training")
    if data.get("authority_label") not in {"ielts_aligned_practice", "ielts_aligned_mock"}:
        errors.append("generated material may not claim official IELTS status")
    full_test = data.get("full_test")
    if not isinstance(full_test, bool):
        errors.append("full_test must be boolean")
    sections = data.get("sections")
    if not isinstance(sections, dict):
        return errors + ["sections must be an object"]
    if full_test and set(sections) != {"listening", "reading", "writing", "speaking"}:
        errors.append("a full test requires listening, reading, writing, and speaking")
    for section_name in ("listening", "reading"):
        section = sections.get(section_name)
        if section is None:
            continue
        if not isinstance(section, dict):
            errors.append(f"{section_name} must be an object")
            continue
        count = section.get("question_count")
        if full_test and count != 40:
            errors.append("full listening and reading sections require 40 questions")
        elif not full_test and (isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 40):
            errors.append(f"partial {section_name} question_count must be 1 to 40")
        expected_parts = 4 if section_name == "listening" else 3
        if full_test and section.get("parts") != expected_parts:
            errors.append(f"full {section_name} requires {expected_parts} parts")
    writing = sections.get("writing")
    if writing is not None:
        if not isinstance(writing, dict) or not isinstance(writing.get("tasks"), list):
            errors.append("writing requires a tasks list")
        else:
            tasks = {task.get("task_number"): task for task in writing["tasks"] if isinstance(task, dict)}
            if full_test and set(tasks) != {1, 2}:
                errors.append("full writing requires Tasks 1 and 2")
            task_one, task_two = tasks.get(1), tasks.get(2)
            if task_one:
                expected_genre = "visual_description" if profile == "academic" else "letter"
                if task_one.get("genre") != expected_genre:
                    label = "Academic visual description" if profile == "academic" else "General Training Writing Task 1 must be a letter"
                    errors.append(label)
                if task_one.get("minimum_words") != 150:
                    errors.append("Writing Task 1 minimum_words must be 150")
                if task_one.get("weight") != 1:
                    errors.append("Writing Task 1 weight must be 1")
            if task_two:
                if task_two.get("genre") != "discursive_essay":
                    errors.append("Writing Task 2 must be a discursive essay")
                if task_two.get("minimum_words") != 250:
                    errors.append("Writing Task 2 minimum_words must be 250")
                if task_two.get("weight") != 2:
                    errors.append("Writing Task 2 must carry twice the Task 1 weight")
    speaking = sections.get("speaking")
    if speaking is not None:
        if not isinstance(speaking, dict):
            errors.append("speaking must be an object")
        else:
            if full_test and speaking.get("parts") != [1, 2, 3]:
                errors.append("full speaking requires Parts 1, 2, and 3")
            if full_test and (speaking.get("minutes_min"), speaking.get("minutes_max")) != (11, 14):
                errors.append("full speaking timing must be 11 to 14 minutes")
    return errors


def validate_ielts_item(item: dict[str, object]) -> list[str]:
    errors: list[str] = []
    section = item.get("section")
    family = item.get("task_family")
    allowed = LISTENING_TASK_FAMILIES if section == "listening" else READING_TASK_FAMILIES if section == "reading" else None
    if allowed is None:
        errors.append("objective items must declare listening or reading section")
    elif family not in allowed:
        errors.append(f"task_family is invalid for {section}")
    if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
        errors.append("prompt must be a non-empty string")
    if family in COMPLETION_FAMILIES:
        max_words, max_numbers = item.get("max_words"), item.get("max_numbers")
        if not any(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in (max_words, max_numbers)):
            errors.append("completion items require max_words or max_numbers")
        if not isinstance(item.get("accepted_answers"), list) or not item["accepted_answers"]:
            errors.append("completion items require accepted_answers")
        if not isinstance(item.get("case_sensitive"), bool):
            errors.append("completion items require case_sensitive policy")
        if not isinstance(item.get("spelling_policy"), str) or not item["spelling_policy"].strip():
            errors.append("completion items require spelling_policy")
    return errors


def _normalize(value: object, case_sensitive: bool) -> str:
    text = " ".join(str(value).split())
    return text if case_sensitive else text.casefold()


def _limit_ok(response: str, key: dict[str, object]) -> bool:
    words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", response)
    numbers = re.findall(r"\d+(?:[.,]\d+)?", response)
    if isinstance(key.get("max_words"), int) and len(words) > key["max_words"]:
        return False
    if isinstance(key.get("max_numbers"), int) and len(numbers) > key["max_numbers"]:
        return False
    return True


def score_objective_section(
    responses: list[object], answer_key: list[dict[str, object]]
) -> dict[str, object]:
    if len(responses) != len(answer_key):
        raise ValueError("responses and answer_key lengths must match")
    marks: list[int] = []
    for response, key in zip(responses, answer_key, strict=True):
        case_sensitive = bool(key.get("case_sensitive", False))
        accepted = {_normalize(value, case_sensitive) for value in key.get("accepted_answers", [])}
        text = str(response)
        marks.append(int(_limit_ok(text, key) and _normalize(text, case_sensitive) in accepted))
    raw = sum(marks)
    maximum = len(answer_key)
    return {
        "label": "IELTS-aligned practice result",
        "raw_score": raw,
        "max_score": maximum,
        "percentage": round(raw / maximum * 100, 2) if maximum else 0.0,
        "item_marks": marks,
        "official_band": None,
        "note": "Raw-to-band thresholds vary by test version; no official band is inferred.",
    }


def validate_criterion_feedback(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    section = data.get("section")
    required = SPEAKING_CRITERIA if section == "speaking" else WRITING_CRITERIA if section == "writing" else set()
    if not required:
        errors.append("criterion feedback section must be writing or speaking")
    if data.get("authority_label") != "estimated_practice_feedback":
        errors.append("feedback must be labeled estimated_practice_feedback")
    criteria = data.get("criteria")
    if not isinstance(criteria, dict):
        errors.append("criteria must be an object")
    else:
        for criterion in sorted(required):
            entry = criteria.get(criterion)
            if not isinstance(entry, dict) or not isinstance(entry.get("evidence"), str) or not entry["evidence"].strip():
                errors.append(f"criterion {criterion} requires evidence before an estimate")
            if not isinstance(entry, dict) or not isinstance(entry.get("next_step"), str) or not entry["next_step"].strip():
                errors.append(f"criterion {criterion} requires a next_step")
    estimate = data.get("estimated_band_range")
    if estimate is not None:
        if not isinstance(estimate, list) or len(estimate) != 2 or not all(
            isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 9 and value * 2 == int(value * 2)
            for value in estimate
        ):
            errors.append("estimated_band_range must contain two half-band values from 0 to 9")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an IELTS-aligned blueprint, item, or feedback file.")
    parser.add_argument("kind", choices=("blueprint", "item", "feedback"))
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8"))
    validator = {"blueprint": validate_blueprint, "item": validate_ielts_item, "feedback": validate_criterion_feedback}[args.kind]
    errors = validator(data)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
