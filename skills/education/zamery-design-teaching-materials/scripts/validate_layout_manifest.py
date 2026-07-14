from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate_design_system import load_registry

FORBIDDEN_VISIBLE_TERMS = (
    "original prompt",
    "example user prompt",
    "route plan",
    "review_publish",
    "raw_request",
    "grade_band",
    "instruction_language",
    "qa gate",
)
REQUIRED_TEACHER_ROLES = {"command_center", "teach", "respond", "answers"}


def _response_registry(root: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    rows, errors = load_registry(root / "response-space-registry.csv", "item_type")
    return {row["item_type"]: row for row in rows if row.get("item_type")}, errors


def validate_layout_manifest(data: dict[str, object], registry_root: Path) -> list[str]:
    errors: list[str] = []
    if data.get("layout_version") != "zamery-layout.v2":
        errors.append("layout_version must be zamery-layout.v2")
    for field in ("artifact_id", "artifact_type", "audience"):
        if not isinstance(data.get(field), str) or not str(data[field]).strip():
            errors.append(f"{field} must be a non-empty string")

    visible_text = data.get("visible_text")
    if not isinstance(visible_text, list):
        errors.append("visible_text must be a list")
    else:
        visible = "\n".join(str(value) for value in visible_text).casefold()
        for term in FORBIDDEN_VISIBLE_TERMS:
            if term in visible:
                errors.append(f"visible content contains forbidden internal term {term}")

    brand = data.get("brand")
    if not isinstance(brand, dict) or brand.get("system_id") != "zamery-core.v2":
        errors.append("layout must use zamery-core.v2")
    else:
        applications = brand.get("applications")
        if not isinstance(applications, list) or not applications:
            errors.append("brand applications must be a non-empty list")
        elif not any(value != "footer_text" for value in applications):
            errors.append("brand must be applied beyond footer text")
        elif "opening_block" not in applications or "page_furniture" not in applications:
            errors.append("brand applications must include opening_block and page_furniture")

    grids = data.get("grids", [])
    if not isinstance(grids, list):
        errors.append("grids must be a list")
    else:
        for grid in grids:
            if not isinstance(grid, dict):
                errors.append("grid must be an object")
                continue
            if grid.get("component_id") != "prompt_response_grid":
                continue
            ratios = grid.get("column_ratios")
            if not isinstance(ratios, list) or len(ratios) != 3 or not all(isinstance(value, (int, float)) for value in ratios):
                errors.append("prompt_response_grid requires three numeric column ratios")
                continue
            if abs(sum(float(value) for value in ratios) - 1) > 0.001:
                errors.append("prompt_response_grid column ratios must sum to 1")
            if float(ratios[0]) > 0.08:
                errors.append("prompt_response_grid number rail must not exceed 8%")
            if not 0.52 <= float(ratios[1]) <= 0.58:
                errors.append("prompt_response_grid prompt column must be 52–58%")
            if not 0.34 <= float(ratios[2]) <= 0.40:
                errors.append("prompt_response_grid response column must be 34–40%")

    response_types, registry_errors = _response_registry(registry_root)
    errors.extend(registry_errors)
    items = data.get("items", [])
    if not isinstance(items, list):
        errors.append("items must be a list")
    else:
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"item {index} must be an object")
                continue
            item_id = str(item.get("item_id", index))
            response_type = item.get("response_type")
            rule = response_types.get(str(response_type))
            if rule is None:
                errors.append(f"item {item_id} has unknown response type {response_type}")
                continue
            height = item.get("response_height_mm")
            minimum = float(rule["min_height_mm"])
            if not isinstance(height, (int, float)) or isinstance(height, bool):
                errors.append(f"item {item_id} requires numeric response_height_mm")
            elif float(height) < minimum:
                errors.append(
                    f"item {item_id} response height {float(height):.1f}mm is below "
                    f"{response_type} minimum {minimum:.1f}mm"
                )
            lines = item.get("expected_response_lines")
            minimum_lines = int(rule["expected_response_lines"])
            if not isinstance(lines, int) or isinstance(lines, bool) or lines < minimum_lines:
                errors.append(f"item {item_id} expected response lines are below {response_type} minimum {minimum_lines}")

    page_roles = data.get("page_roles")
    if not isinstance(page_roles, list) or not page_roles:
        errors.append("page_roles must be a non-empty list")
        declared_roles: set[str] = set()
    else:
        declared_roles = {str(role) for role in page_roles}
    if data.get("artifact_type") == "teacher_guide" and not REQUIRED_TEACHER_ROLES.issubset(declared_roles):
        errors.append("teacher guide requires command_center, teach, respond, and answers page roles")

    pages = data.get("pages")
    actual_roles: set[str] = set()
    if not isinstance(pages, list) or not pages:
        errors.append("pages must be a non-empty list")
    else:
        for index, page in enumerate(pages):
            if not isinstance(page, dict):
                errors.append(f"page {index} must be an object")
                continue
            if isinstance(page.get("role"), str):
                actual_roles.add(str(page["role"]))
            ratio = page.get("occupied_ratio")
            if not isinstance(ratio, (int, float)) or isinstance(ratio, bool) or not 0 <= ratio <= 1:
                errors.append(f"page {index} occupied_ratio must be between 0 and 1")
            elif float(ratio) < 0.25 and not page.get("intentional_sparse"):
                errors.append(f"page {index} is unintentionally sparse at {round(float(ratio) * 100)}% occupancy")
    for role in declared_roles:
        if role not in actual_roles:
            errors.append(f"page role {role} is not represented")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--assets-root", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate_layout_manifest(data, args.assets_root)
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
