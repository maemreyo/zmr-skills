from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def digest_name(digest: str) -> str:
    return digest.removeprefix("sha256:")


@dataclass(frozen=True)
class StoreLayout:
    root: Path

    @property
    def records_root(self) -> Path:
        return self.root / ".zamery" / "records"

    @property
    def blobs_root(self) -> Path:
        return self.root / ".zamery" / "blobs"

    @property
    def index_path(self) -> Path:
        return self.root / ".zamery" / "graph.sqlite"
