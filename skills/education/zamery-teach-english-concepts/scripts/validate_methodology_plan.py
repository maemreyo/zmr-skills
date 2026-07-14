from __future__ import annotations

import json
import sys
from pathlib import Path

INVERSE_STAGES = ["disaster", "clues", "safe_zone", "rule", "transfer"]
VOCAB_COLUMNS = ["word", "core_meaning", "selection_clues", "collocations", "memorable_example"]
APPROVED_METHODS = {
    "inverse_thinking",
    "semantic_anchoring",
    "contrastive_pairs",
    "active_recall",
    "why_wrong_reasoning",
    "concept_mapping",
    "roleplay",
    "film_based_learning",
    "timed_practice",
}


def validate_methodology_plan(data: dict[str, object]) -> list[str]:
    """Validate method authority and method-specific structural invariants."""
    errors: list[str] = []
    selected = data.get("selected_methodology")
    rationale = data.get("rationale")
    if not isinstance(selected, str) or not selected.strip():
        errors.append("selected_methodology must be a non-empty string")
    elif selected not in APPROVED_METHODS:
        errors.append("selected_methodology is not approved")
    if not isinstance(rationale, str) or not rationale.strip():
        errors.append("rationale must be a non-empty string")

    requested = data.get("requested_methodology")
    if data.get("pinned") is True and requested and requested != selected:
        errors.append("pinned methodology changed")
    if selected == "inverse_thinking" and data.get("stages") != INVERSE_STAGES:
        errors.append("inverse thinking stages are incomplete or out of order")
    if "board_columns" in data and data.get("board_columns") != VOCAB_COLUMNS:
        errors.append("vocabulary board columns are incomplete")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_methodology_plan.py PLAN.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate_methodology_plan(data)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
