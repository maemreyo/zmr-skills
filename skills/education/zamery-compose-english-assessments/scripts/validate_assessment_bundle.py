from __future__ import annotations

import json
import sys
import unicodedata
from collections.abc import Mapping
from pathlib import Path

LEAK_FIELDS = {
    "answer",
    "answer_key",
    "accepted_answers",
    "correct_answer",
    "correct_option_ids",
    "correct_option_index",
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


def _normalized(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).split()).casefold()


def _walk_student(value: object, path: str = "student_artifact") -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).casefold() in LEAK_FIELDS:
                errors.append(f"student answer leakage at {child_path}")
            errors.extend(_walk_student(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_walk_student(child, f"{path}[{index}]"))
    return errors


def validate_assessment_bundle(data: dict[str, object]) -> list[str]:
    """Validate identity, alignment, item count, response semantics, and answer separation."""
    student = data.get("student_artifact")
    answer_set = data.get("answer_set")
    if not isinstance(student, dict) or not isinstance(answer_set, dict):
        return ["assessment bundle requires separate student_artifact and answer_set objects"]

    errors: list[str] = []
    if student.get("audience") != "student":
        errors.append("student artifact audience must be student")
    if answer_set.get("audience") != "teacher":
        errors.append("AnswerSet audience must be teacher")
    errors.extend(_walk_student(student))

    declared = student.get("objective_ids")
    known = (
        {value for value in declared if isinstance(value, str) and value.strip()}
        if isinstance(declared, list)
        else set()
    )
    if not known or not isinstance(declared, list) or len(known) != len(declared):
        errors.append("student artifact objective_ids must be a non-empty string list")

    questions = student.get("questions")
    answers = answer_set.get("answers")
    if not isinstance(questions, list) or not isinstance(answers, list):
        errors.append("questions and answers must be lists")
        return errors

    requested = data.get("requested_item_count")
    if requested is not None and requested != len(questions):
        errors.append("requested_item_count does not match generated questions")

    question_ids: list[str] = []
    question_by_id: dict[str, dict[str, object]] = {}
    covered: set[str] = set()
    actual_difficulty: dict[str, int] = {}
    for index, question in enumerate(questions):
        if not isinstance(question, dict):
            errors.append(f"question {index} must be an object")
            continue
        question_id = question.get("question_id")
        if not isinstance(question_id, str) or not question_id.strip():
            errors.append(f"question {index} requires a non-empty question_id")
            continue
        question_ids.append(question_id)
        question_by_id[question_id] = question
        refs = question.get("objective_ids")
        if not isinstance(refs, list) or not refs:
            errors.append(f"question {question_id} requires objective_ids")
        else:
            for objective_id in refs:
                if objective_id not in known:
                    errors.append(f"question {question_id} cites unknown objective {objective_id}")
                else:
                    covered.add(str(objective_id))

        difficulty = question.get("difficulty")
        if isinstance(difficulty, str) and difficulty:
            actual_difficulty[difficulty] = actual_difficulty.get(difficulty, 0) + 1
        else:
            errors.append(f"question {question_id} requires difficulty")

        response_type = question.get("response_type")
        if response_type not in RESPONSE_LINE_MINIMUMS:
            errors.append(f"question {question_id} has unsupported response_type")
        else:
            lines = question.get("expected_response_lines")
            minimum = RESPONSE_LINE_MINIMUMS[response_type]
            if not isinstance(lines, int) or isinstance(lines, bool) or lines < minimum:
                errors.append(f"question {question_id} requires at least {minimum} response lines for {response_type}")
        if not isinstance(question.get("layout_intent"), str) or not str(question["layout_intent"]).strip():
            errors.append(f"question {question_id} requires layout_intent")
        if response_type == "selected_response":
            options = question.get("options")
            if not isinstance(options, list) or len(options) < 2 or not all(isinstance(option, str) for option in options):
                errors.append(f"question {question_id} requires at least two text options")
            else:
                normalized = [_normalized(option) for option in options]
                if len(normalized) != len(set(normalized)):
                    errors.append(f"question {question_id} has duplicate normalized options")

    if len(question_ids) != len(set(question_ids)):
        errors.append("question IDs must be unique")
    for objective_id in declared if isinstance(declared, list) else []:
        if objective_id not in covered:
            errors.append(f"objective {objective_id} is not covered by any question")
    requested_distribution = data.get("requested_difficulty_distribution")
    if requested_distribution is not None and requested_distribution != actual_difficulty:
        errors.append("requested difficulty distribution does not match generated questions")

    answer_ids: list[str] = []
    answer_by_id: dict[str, dict[str, object]] = {}
    for index, answer in enumerate(answers):
        if not isinstance(answer, dict):
            errors.append(f"answer {index} must be an object")
            continue
        question_id = answer.get("question_id")
        if not isinstance(question_id, str) or not question_id.strip():
            errors.append(f"answer {index} requires a non-empty question_id")
            continue
        answer_ids.append(question_id)
        answer_by_id[question_id] = answer
    if len(answer_ids) != len(set(answer_ids)):
        errors.append("AnswerSet question IDs must be unique")
    if set(question_ids) != set(answer_ids):
        errors.append("AnswerSet question IDs must exactly match student question IDs")

    for question_id in set(question_ids) & set(answer_ids):
        question = question_by_id[question_id]
        answer = answer_by_id[question_id]
        if question.get("response_type") == "selected_response":
            if "correct_option_index" not in answer and "correct_option_ids" not in answer:
                errors.append(f"answer {question_id} must identify a selected-response option")
        elif question.get("response_type") in RESPONSE_LINE_MINIMUMS and not answer.get("accepted_answers") and not answer.get("rubric"):
            errors.append(f"answer {question_id} requires accepted_answers or rubric")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_assessment_bundle.py BUNDLE.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate_assessment_bundle(data)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
