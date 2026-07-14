import argparse
from pathlib import Path

from item_bank import init_database


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a Zamery V3 SQLite item bank.")
    parser.add_argument("database", type=Path)
    args = parser.parse_args()
    init_database(args.database)
    print(args.database)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
