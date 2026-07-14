import argparse
from pathlib import Path

from item_bank import ingest_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description="Resumably ingest Zamery V3 JSONL items.")
    parser.add_argument("database", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--requested-count", type=int, required=True)
    parser.add_argument("--chunk-size", type=int)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    print(ingest_jsonl(args.database, args.source, batch_id=args.batch_id,
        requested_count=args.requested_count, chunk_size=args.chunk_size, seed=args.seed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
