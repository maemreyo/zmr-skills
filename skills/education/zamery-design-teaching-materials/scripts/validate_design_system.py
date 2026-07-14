from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

EXPECTED_PALETTE = {
    "ink_navy": "#17324D",
    "root_terracotta": "#B85435",
    "growth_teal": "#2B746F",
    "warm_sand": "#F4EEE4",
    "sky_mist": "#DCEAF2",
    "charcoal": "#202B33",
    "paper_white": "#FFFFFF",
}
REGISTRIES = {
    "component-registry.csv": (
        "component_id",
        {"audience", "artifact_type", "purpose", "min_height_mm", "allowed_page_roles", "required_fields", "column_ratios"},
    ),
    "response-space-registry.csv": (
        "item_type",
        {"expected_response_lines", "min_height_mm", "preferred_layout"},
    ),
    "artifact-template-registry.csv": (
        "template_id",
        {"artifact_type", "audience", "page_budget", "color_mode", "required_page_roles", "asset_path"},
    ),
}


def load_registry(path: Path, key_field: str) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error):
        return [], [f"{path.name} is not readable UTF-8 CSV"]
    keys: list[str] = []
    for row in rows:
        key = (row.get(key_field) or "").strip()
        if not key:
            errors.append(f"{path.name} has an empty primary key")
        elif key in keys:
            errors.append(f"{path.name} has duplicate primary key {key}")
        keys.append(key)
    return rows, errors


def validate_design_system(root: Path) -> list[str]:
    errors: list[str] = []
    token_path = root / "design-tokens.json"
    try:
        tokens = json.loads(token_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        tokens = {}
        errors.append("design-tokens.json is not readable JSON")
    if tokens.get("system_id") != "zamery-core.v2":
        errors.append("design system_id must be zamery-core.v2")
    if tokens.get("palette") != EXPECTED_PALETTE:
        errors.append("palette must exactly match Zamery Core V2")
    typography = tokens.get("typography")
    if not isinstance(typography, dict) or typography.get("primary_family") != "Arial":
        errors.append("primary typography must be Arial")
    elif typography.get("print_body_min_pt") != 9.5:
        errors.append("print body minimum must be 9.5 pt")
    brand = tokens.get("brand")
    if not isinstance(brand, dict) or brand.get("name") != "zamery" or brand.get("tagline") != "rooted in strength":
        errors.append("brand identity must be zamery — rooted in strength")

    for filename, (key_field, required_fields) in REGISTRIES.items():
        path = root / filename
        rows, registry_errors = load_registry(path, key_field)
        errors.extend(registry_errors)
        if not rows:
            errors.append(f"{filename} must contain at least one record")
            continue
        headers = set(rows[0].keys())
        missing = required_fields - headers
        if missing:
            errors.append(f"{filename} is missing headers {', '.join(sorted(missing))}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("assets_root", type=Path)
    args = parser.parse_args()
    errors = validate_design_system(args.assets_root)
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
