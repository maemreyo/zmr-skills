import argparse
import json
from pathlib import Path

from item_bank import validate_database


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SQLite integrity and all stored items.")
    parser.add_argument("database", type=Path)
    args = parser.parse_args()
    report = validate_database(args.database)
    print(json.dumps(report, indent=2))
    return 0 if report["integrity"] == "ok" and not report["invalid_json"] and not report["invalid_items"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
