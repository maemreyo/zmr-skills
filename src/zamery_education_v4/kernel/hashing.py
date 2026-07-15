from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from .canonical_json import canonical_json_bytes


def sha256_bytes(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    digest = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def content_hash(value: object) -> str:
    return sha256_bytes(canonical_json_bytes(value))
