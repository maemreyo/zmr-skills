from __future__ import annotations

import json
import sys
from collections.abc import Mapping
from pathlib import Path

TEACHER_ONLY_KEYS = {"answer", "answer_key", "correct_answer", "explanation", "rubric", "teacher_notes"}
MEDIA_TYPES = {"audio", "image", "media", "video"}
V2_PALETTE = {"ink_navy": "#17324D", "root_terracotta": "#B85435", "growth_teal": "#2B746F", "warm_sand": "#F4EEE4", "sky_mist": "#DCEAF2", "charcoal": "#202B33", "paper_white": "#FFFFFF"}


def _walk_student(value: object, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).casefold() in TEACHER_ONLY_KEYS:
                errors.append(f"teacher-only data at {child_path}")
            if key == "type" and child in MEDIA_TYPES:
                for field in ("alt_text", "fallback_text"):
                    text = value.get(field)
                    if not isinstance(text, str) or not text.strip():
                        errors.append(f"media block at {path} requires non-empty {field}")
            errors.extend(_walk_student(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_walk_student(child, f"{path}[{index}]"))
    return errors


def validate_deck_manifest(data: dict[str, object]) -> list[str]:
    """Validate deck identity, objective lineage, teacher separation, and brand authority."""
    errors: list[str] = []
    if data.get("design_system") != "zamery-core.v2":
        errors.append("design_system must be zamery-core.v2")
    if data.get("template_id") != "classroom-slides-v2":
        errors.append("template_id must be classroom-slides-v2")
    if data.get("reopened_after_export") is not True:
        errors.append("final PPTX must be reopened after export")
    if not isinstance(data.get("deck_id"), str) or not str(data["deck_id"]).strip():
        errors.append("deck_id must be a non-empty string")
    declared = data.get("objective_ids")
    known = (
        {value for value in declared if isinstance(value, str) and value.strip()}
        if isinstance(declared, list)
        else set()
    )
    if not known:
        errors.append("objective_ids must be a non-empty string list")

    brand = data.get("brand")
    if not isinstance(brand, dict):
        errors.append("brand must be an object")
    else:
        if brand.get("name") != "zamery" or brand.get("tagline") != "rooted in strength":
            errors.append("brand name and tagline must match the supplied Zamery identity")
        if brand.get("primary_family") != "Arial":
            errors.append("brand primary_family must be Arial")
        if brand.get("palette") != V2_PALETTE:
            errors.append("brand palette must match Zamery Core V2")

    slides = data.get("slides")
    slide_ids: list[str] = []
    covered: set[str] = set()
    if not isinstance(slides, list) or not slides:
        errors.append("slides must be a non-empty list")
    else:
        for index, slide in enumerate(slides):
            if not isinstance(slide, dict):
                errors.append(f"slide {index} must be an object")
                continue
            slide_id = slide.get("slide_id")
            if not isinstance(slide_id, str) or not slide_id.strip():
                errors.append(f"slide {index} requires a non-empty slide_id")
                continue
            slide_ids.append(slide_id)
            if slide.get("surface") != "student":
                errors.append(f"slide {slide_id} surface must be student")
            refs = slide.get("objective_ids")
            if not isinstance(refs, list) or not refs:
                errors.append(f"slide {slide_id} requires objective_ids")
            else:
                for objective_id in refs:
                    if objective_id not in known:
                        errors.append(f"slide {slide_id} cites unknown objective {objective_id}")
                    else:
                        covered.add(str(objective_id))
            errors.extend(_walk_student(slide, f"slides[{index}]"))
        if len(slide_ids) != len(set(slide_ids)):
            errors.append("slide IDs must be unique")
    for objective_id in declared if isinstance(declared, list) else []:
        if objective_id not in covered:
            errors.append(f"objective {objective_id} is not covered by any slide")

    notes = data.get("teacher_notes")
    note_ids: list[str] = []
    if not isinstance(notes, list):
        errors.append("teacher_notes must be a list")
    else:
        for index, note in enumerate(notes):
            if not isinstance(note, dict):
                errors.append(f"teacher note {index} must be an object")
                continue
            slide_id = note.get("slide_id")
            if not isinstance(slide_id, str):
                errors.append(f"teacher note {index} requires slide_id")
                continue
            note_ids.append(slide_id)
            if slide_id not in set(slide_ids):
                errors.append(f"teacher notes reference unknown slide {slide_id}")
        if len(note_ids) != len(set(note_ids)):
            errors.append("teacher note slide IDs must be unique")
        if set(note_ids) != set(slide_ids):
            errors.append("teacher notes must map exactly once to every slide")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_deck_manifest.py DECK.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate_deck_manifest(data)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
