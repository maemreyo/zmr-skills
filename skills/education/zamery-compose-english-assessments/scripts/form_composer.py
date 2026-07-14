from __future__ import annotations

import argparse
import json
import random
import sqlite3
from collections import Counter
from pathlib import Path


def _load_bank(path: Path) -> list[dict[str, object]]:
    if path.suffix.casefold() in {".sqlite", ".db"}:
        with sqlite3.connect(path) as connection:
            rows = connection.execute(
                """SELECT content_json FROM items i WHERE status = 'approved'
                AND version = (SELECT MAX(version) FROM items WHERE item_id = i.item_id)
                ORDER BY item_id"""
            ).fetchall()
        return [json.loads(row[0]) for row in rows]
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    latest: dict[str, dict[str, object]] = {}
    for item in records:
        if not isinstance(item.get("item_id"), str):
            continue
        previous = latest.get(item["item_id"])
        if previous is None or int(item.get("version", 0)) > int(previous.get("version", 0)):
            latest[item["item_id"]] = item
    return [latest[key] for key in sorted(latest) if latest[key].get("status") == "approved"]


def _matches(item: dict[str, object], filters: dict[str, object]) -> bool:
    for field, expected in filters.items():
        actual = item.get(field)
        if field == "difficulty" and isinstance(expected, dict):
            if not isinstance(actual, (int, float)):
                return False
            if "min" in expected and actual < expected["min"]:
                return False
            if "max" in expected and actual > expected["max"]:
                return False
        elif isinstance(expected, list):
            if actual not in expected:
                return False
        elif actual != expected:
            return False
    return True


def validate_blueprint(blueprint: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if blueprint.get("schema_version") != "zamery-assessment-blueprint.v3":
        errors.append("schema_version must be zamery-assessment-blueprint.v3")
    if not isinstance(blueprint.get("blueprint_id"), str) or not blueprint["blueprint_id"].strip():
        errors.append("blueprint_id must be a non-empty string")
    sections = blueprint.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("sections must be a non-empty list")
    else:
        ids: list[object] = []
        for index, section in enumerate(sections):
            if not isinstance(section, dict):
                errors.append(f"section {index} must be an object")
                continue
            ids.append(section.get("section_id"))
            if not isinstance(section.get("section_id"), str) or not section["section_id"].strip():
                errors.append(f"section {index} requires section_id")
            count = section.get("count")
            if isinstance(count, bool) or not isinstance(count, int) or count < 1:
                errors.append(f"section {index} count must be positive")
            if not isinstance(section.get("filters", {}), dict):
                errors.append(f"section {index} filters must be an object")
        if len(ids) != len(set(ids)):
            errors.append("section IDs must be unique")
    return errors


def assemble_forms(
    bank_path: Path,
    blueprint: dict[str, object],
    form_ids: list[str],
    *,
    seed: int,
) -> list[dict[str, object]]:
    errors = validate_blueprint(blueprint)
    if errors:
        raise ValueError("; ".join(errors))
    if not form_ids or len(form_ids) != len(set(form_ids)) or not all(form_ids):
        raise ValueError("form IDs must be non-empty and unique")
    bank = _load_bank(bank_path)
    forms = [
        {
            "schema_version": "zamery-form.v3",
            "form_id": form_id,
            "blueprint_id": blueprint["blueprint_id"],
            "seed": seed,
            "items": [],
        }
        for form_id in form_ids
    ]
    for section in blueprint["sections"]:
        count = section["count"]
        filters = section.get("filters", {})
        candidates = [item for item in bank if _matches(item, filters)]
        rng = random.Random(f"zamery:{seed}:{blueprint['blueprint_id']}:{section['section_id']}")
        rng.shuffle(candidates)
        required = count * len(forms)
        if len(candidates) < required:
            raise ValueError(
                f"insufficient approved items for section {section['section_id']}: "
                f"need {required}, found {len(candidates)}"
            )
        selected_pool = candidates[:required]
        selected_pool.sort(key=lambda item: float(item.get("difficulty", 0)))
        buckets: list[list[dict[str, object]]] = [[] for _ in forms]
        for index, item in enumerate(selected_pool):
            round_index, position = divmod(index, len(forms))
            form_index = position if round_index % 2 == 0 else len(forms) - 1 - position
            buckets[form_index].append(item)
        for form, selected in zip(forms, buckets, strict=True):
            form["items"].extend({**item, "section_id": section["section_id"]} for item in selected)
    return forms


def validate_form_equivalence(
    forms: list[dict[str, object]], blueprint: dict[str, object]
) -> dict[str, object]:
    errors: list[str] = []
    expected = {section["section_id"]: section["count"] for section in blueprint["sections"]}
    counts: dict[str, dict[str, int]] = {}
    means: dict[str, float] = {}
    interactions: dict[str, dict[str, int]] = {}
    item_ids_by_form: dict[str, set[object]] = {}
    cross_form_overlap: list[dict[str, object]] = []
    for form in forms:
        form_id = str(form.get("form_id"))
        items = form.get("items", [])
        ids = [item.get("item_id") for item in items if isinstance(item, dict)]
        item_ids_by_form[form_id] = set(ids)
        if len(ids) != len(set(ids)):
            errors.append(f"form {form_id} contains duplicate item IDs")
        counts[form_id] = dict(Counter(item.get("section_id") for item in items))
        if counts[form_id] != expected:
            errors.append(f"form {form_id} section counts do not match blueprint")
        difficulties = [float(item["difficulty"]) for item in items if isinstance(item.get("difficulty"), (int, float))]
        means[form_id] = round(sum(difficulties) / len(difficulties), 6) if difficulties else 0.0
        interactions[form_id] = dict(Counter(str(item.get("interaction")) for item in items))
    form_ids = list(item_ids_by_form)
    for left_index, left_id in enumerate(form_ids):
        for right_id in form_ids[left_index + 1:]:
            shared = sorted(str(item_id) for item_id in item_ids_by_form[left_id] & item_ids_by_form[right_id])
            if shared:
                errors.append(f"forms {left_id} and {right_id} share item IDs")
                cross_form_overlap.append({"forms": [left_id, right_id], "item_ids": shared})
    tolerance = float(blueprint.get("equivalence_tolerances", {}).get("mean_difficulty", 0.0))
    if means and max(means.values()) - min(means.values()) > tolerance:
        errors.append("mean difficulty difference exceeds tolerance")
    return {
        "equivalent": not errors,
        "errors": errors,
        "section_counts": counts,
        "mean_difficulty": means,
        "interaction_counts": interactions,
        "cross_form_overlap": cross_form_overlap,
        "tolerance": tolerance,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble deterministic, blueprint-exact forms.")
    parser.add_argument("bank", type=Path)
    parser.add_argument("blueprint", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--forms", nargs="+", required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    blueprint = json.loads(args.blueprint.read_text(encoding="utf-8"))
    forms = assemble_forms(args.bank, blueprint, args.forms, seed=args.seed)
    args.output.mkdir(parents=True, exist_ok=True)
    for form in forms:
        destination = args.output / f"form-{str(form['form_id']).casefold()}.json"
        destination.write_text(json.dumps(form, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = validate_form_equivalence(forms, blueprint)
    (args.output / "equivalence-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0 if report["equivalent"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
