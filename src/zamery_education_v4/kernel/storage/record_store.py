from __future__ import annotations

import json
from pathlib import Path

from ..canonical_json import canonical_json_bytes
from ..hashing import sha256_bytes
from ..records.base import CanonicalRecord
from ..records.registry import RecordRegistry, default_registry
from .atomic import atomic_write
from .errors import ContentHashMismatch, RecordNotFound
from .layout import StoreLayout, digest_name


class RecordStore:
    def __init__(self, root: str | Path, registry: RecordRegistry | None = None) -> None:
        self.layout = StoreLayout(Path(root))
        self.registry = registry or default_registry()

    def path_for(self, digest: str, record_type: str | None = None) -> Path:
        if record_type:
            return self.layout.records_root / record_type / f"{digest_name(digest)}.json"
        matches = list(self.layout.records_root.glob(f"*/{digest_name(digest)}.json"))
        if len(matches) == 1:
            return matches[0]
        raise RecordNotFound(digest)

    def commit(self, record: CanonicalRecord) -> str:
        payload = canonical_json_bytes(record.canonical_payload())
        digest = sha256_bytes(payload)
        path = self.path_for(digest, record.record_type)
        if path.exists():
            if sha256_bytes(path.read_bytes()) != digest:
                raise ContentHashMismatch(str(path))
            return digest
        atomic_write(path, payload)
        if sha256_bytes(path.read_bytes()) != digest:
            raise ContentHashMismatch(str(path))
        return digest

    def load(self, digest: str, record_type: str | None = None) -> CanonicalRecord:
        path = self.path_for(digest, record_type)
        payload = path.read_bytes()
        if sha256_bytes(payload) != digest:
            raise ContentHashMismatch(str(path))
        decoded = json.loads(payload)
        record = self.registry.parse(decoded)
        if record.calculated_hash != digest:
            raise ContentHashMismatch(record.record_id)
        return record

    def iter_paths(self) -> tuple[Path, ...]:
        return tuple(sorted(self.layout.records_root.glob("*/*.json")))
