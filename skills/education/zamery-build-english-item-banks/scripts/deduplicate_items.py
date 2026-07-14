import argparse
from pathlib import Path

from item_bank import deduplicate_bank


def main() -> int:
    parser = argparse.ArgumentParser(description="Report exact and near-duplicate item pairs.")
    parser.add_argument("database", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--threshold", type=float, default=0.86)
    args = parser.parse_args()
    print(deduplicate_bank(args.database, args.report, threshold=args.threshold))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
