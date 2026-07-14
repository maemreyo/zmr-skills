import argparse
from pathlib import Path

from item_bank import export_jsonl, export_review_csv


def main() -> int:
    parser = argparse.ArgumentParser(description="Export an item bank to JSONL or review CSV.")
    parser.add_argument("database", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--format", choices=("jsonl", "csv"), required=True)
    args = parser.parse_args()
    count = export_jsonl(args.database, args.destination) if args.format == "jsonl" else export_review_csv(args.database, args.destination)
    print(count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
