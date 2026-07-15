from __future__ import annotations

import hashlib
import json
import sys
import unicodedata
from pathlib import Path
from typing import TextIO


def normalize(value: object) -> object:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        normalized: dict[str, object] = {}
        for key, item in value.items():
            canonical_key = unicodedata.normalize("NFC", str(key))
            if canonical_key in normalized:
                raise ValueError(f"duplicate canonical key: {canonical_key}")
            normalized[canonical_key] = normalize(item)
        return normalized
    return value


def canonical(value: object) -> bytes:
    return json.dumps(
        normalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def run(stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout) -> int:
    invocation = json.load(stdin)
    record = {
        "record_type": "source",
        "schema_version": "4.0.0",
        "record_id": "source:echo",
        "title": "Echo",
        "authority": "reference",
        "source_kind": "reference",
    }
    payload = canonical(record)
    digest = "sha256:" + hashlib.sha256(payload).hexdigest()
    output = Path(invocation["output_mount"]) / "echo.json"
    output.write_bytes(payload)
    json.dump(
        {
            "protocol_version": "zamery-capability.v1",
            "status": "success",
            "invocation_id": invocation["invocation_id"],
            "outputs": [
                {
                    "output_type": "echo_record",
                    "path": "echo.json",
                    "declared_hash": digest,
                    "record_type": "source",
                }
            ],
            "metrics": {},
        },
        stdout,
        sort_keys=True,
        separators=(",", ":"),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
