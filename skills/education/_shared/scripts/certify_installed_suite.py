from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from contracts import ZAMERY_SKILL_NAMES

DEFAULT_SKILLS_ROOT = Path("/root/.codex/skills/remote-skills")
DEFAULT_QUICK_VALIDATE = Path(
    "/root/.codex/skills/oai/skill-creator/scripts/quick_validate.py"
)


def _frontmatter_name(skill_file: Path) -> str | None:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return None
        if stripped.startswith("name:"):
            value = stripped.removeprefix("name:").strip()
            return value or None
    return None


def discover_skill_dirs(
    skills_root: Path,
    expected: tuple[str, ...],
) -> tuple[dict[str, Path], list[str]]:
    """Return unique name-to-directory matches and missing/duplicate errors."""
    candidates: dict[str, list[Path]] = {name: [] for name in expected}
    if skills_root.exists():
        for skill_file in sorted(skills_root.glob("*/SKILL.md")):
            name = _frontmatter_name(skill_file)
            if name in candidates:
                candidates[name].append(skill_file.parent)

    found: dict[str, Path] = {}
    errors: list[str] = []
    for name in expected:
        matches = candidates[name]
        if not matches:
            errors.append(f"missing skill {name}")
        elif len(matches) > 1:
            errors.append(f"duplicate skill {name}: {len(matches)} matches")
        else:
            found[name] = matches[0]
    return found, errors


def validate_skill(
    skill_dir: Path,
    quick_validate: Path,
) -> subprocess.CompletedProcess[str]:
    """Run quick_validate.py against one installed skill directory."""
    return subprocess.run(
        [sys.executable, str(quick_validate), str(skill_dir)],
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument("--quick-validate", type=Path, default=DEFAULT_QUICK_VALIDATE)
    args = parser.parse_args()

    found, errors = discover_skill_dirs(args.skills_root, ZAMERY_SKILL_NAMES)
    print(f"{len(found)}/{len(ZAMERY_SKILL_NAMES)} Zamery skills discovered")
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1

    failed = False
    for name in ZAMERY_SKILL_NAMES:
        result = validate_skill(found[name], args.quick_validate)
        if result.returncode != 0:
            failed = True
            print(f"validation failed for {name}", file=sys.stderr)
            if result.stdout:
                print(result.stdout.rstrip(), file=sys.stderr)
            if result.stderr:
                print(result.stderr.rstrip(), file=sys.stderr)
    if failed:
        return 1

    print("suite certification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
