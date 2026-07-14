from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_REPO_ROOT))

from skills.education._shared.contracts import validate_student_card  # noqa: E402


def get_validator():
    return validate_student_card


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_student_card.py STUDENT_CARD.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"error: {path} is not a file", file=sys.stderr)
        return 2
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_student_card(data)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
