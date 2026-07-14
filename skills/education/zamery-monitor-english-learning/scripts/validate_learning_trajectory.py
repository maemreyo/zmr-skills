from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_REPO_ROOT))

from skills.education._shared.contracts import (  # noqa: E402
    validate_evidence_summary,
    validate_learning_trajectory,
)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_learning_trajectory.py TRAJECTORY.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate_learning_trajectory(data)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
