from __future__ import annotations

from pathlib import Path

from ..hashing import sha256_bytes, sha256_file
from .atomic import atomic_write
from .errors import ContentHashMismatch, RecordNotFound
from .layout import StoreLayout, digest_name


class BlobStore:
    def __init__(self, root: str | Path) -> None:
        self.layout = StoreLayout(Path(root))

    def path_for(self, digest: str) -> Path:
        return self.layout.blobs_root / digest_name(digest)

    def commit_bytes(self, payload: bytes) -> str:
        digest = sha256_bytes(payload)
        path = self.path_for(digest)
        if not path.exists():
            atomic_write(path, payload)
        if sha256_file(path) != digest:
            raise ContentHashMismatch(str(path))
        return digest

    def commit_file(self, source: str | Path) -> str:
        return self.commit_bytes(Path(source).read_bytes())

    def open(self, digest: str, mode: str = "rb"):
        path = self.path_for(digest)
        if not path.exists():
            raise RecordNotFound(digest)
        if sha256_file(path) != digest:
            raise ContentHashMismatch(str(path))
        return path.open(mode)
