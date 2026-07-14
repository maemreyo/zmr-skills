from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_ROUTES = {
    "understand_learners": "zamery-understand-learners",
    "monitor_learning": "zamery-monitor-english-learning",
    "sequence_design": "zamery-design-english-learning-sequences",
    "design": "zamery-design-english-learning",
    "concept_teaching": "zamery-teach-english-concepts",
    "practice": "zamery-build-english-practice",
    "item_bank": "zamery-build-english-item-banks",
    "assessment_composition": "zamery-compose-english-assessments",
    "ielts_practice": "zamery-create-ielts-practice",
    "video_learning": "zamery-build-video-learning",
    "material_design": "zamery-design-teaching-materials",
    "presentation": "zamery-create-english-presentations",
    "student_work_analysis": "zamery-analyze-student-work",
    "reteach": "zamery-plan-english-reteaching",
    "review_publish": "zamery-review-publish-pack",
}


def _frontmatter_name(path: Path) -> str | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return None
        if stripped.startswith("name:"):
            name = stripped.removeprefix("name:").strip()
            return name or None
    return None


def validate_manifest(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("manifest_version") != "zamery-suite.v3":
        errors.append("manifest_version must be zamery-suite.v3")
    routes = data.get("routes")
    if not isinstance(routes, list):
        return [*errors, "routes must be a list"]

    intents: list[str] = []
    skills: list[str] = []
    actual: dict[str, str] = {}
    for index, route in enumerate(routes):
        if not isinstance(route, dict):
            errors.append(f"route {index} must be an object")
            continue
        intent = route.get("intent")
        skill = route.get("skill")
        if not isinstance(intent, str) or not isinstance(skill, str):
            errors.append(f"route {index} requires string intent and skill")
            continue
        intents.append(intent)
        skills.append(skill)
        actual[intent] = skill
    if len(intents) != len(set(intents)):
        errors.append("intent owners must be unique")
    if len(skills) != len(set(skills)):
        errors.append("specialist targets must be unique")
    if len(set(skills)) != 15:
        errors.append("manifest must declare exactly fifteen specialist targets")
    if actual != EXPECTED_ROUTES:
        errors.append("routes must exactly match the approved intent owners")
    return errors


def discover_installed_targets(skills_root: Path, names: tuple[str, ...]) -> list[str]:
    matches: dict[str, int] = {name: 0 for name in names}
    if skills_root.exists():
        for skill_file in sorted(skills_root.glob("*/SKILL.md")):
            name = _frontmatter_name(skill_file)
            if name in matches:
                matches[name] += 1
    errors: list[str] = []
    for name in names:
        if matches[name] == 0:
            errors.append(f"missing installed specialist {name}")
        elif matches[name] > 1:
            errors.append(f"duplicate installed specialist {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--skills-root", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate_manifest(data)
    errors.extend(discover_installed_targets(args.skills_root, tuple(EXPECTED_ROUTES.values())))
    for error in errors:
        print(error)
    if errors:
        return 1
    print("15/15 specialist targets discovered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
