from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_REPO_ROOT))

from skills.education._shared.contracts import validate_reteaching_plan  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a reteaching plan against zamery-reteaching-plan.v1",
    )
    parser.add_argument("file", help="Path to the reteaching plan JSON file")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"error: invalid JSON: {error}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("error: JSON root must be an object", file=sys.stderr)
        return 1
    errors = validate_reteaching_plan(data)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    if args.verbose:
        print("reteaching plan is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
