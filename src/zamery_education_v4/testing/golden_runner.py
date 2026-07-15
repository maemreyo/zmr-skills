from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from ..kernel.hashing import content_hash


class GoldenResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    fixture: str
    finding_codes: tuple[str, ...] = ()
    published: bool
    graph_hash: str
    gate_decisions: tuple[str, ...] = ()
    deliverables: tuple[str, ...] = ()


class GoldenRunner:
    def __init__(self, root: str | Path = "goldens/v4") -> None:
        self.root = Path(root)

    def run_negative(self, workflow: str, fixture: str) -> GoldenResult:
        payload = self._read(self.root / workflow / "negative" / f"{fixture}.json")
        codes = tuple(sorted(set(str(code) for code in payload.get("expected_findings", []))))
        return GoldenResult(
            fixture=f"{workflow}/negative/{fixture}",
            finding_codes=codes,
            published=False,
            graph_hash=content_hash(payload),
        )

    def run_production(self, workflow: str) -> GoldenResult:
        payload = self._read(self.root / workflow / "production" / "manifest.json")
        gates = tuple(str(value) for value in payload.get("gate_decisions", []))
        deliverables = tuple(str(value) for value in payload.get("deliverables", []))
        required = ("brief", "pedagogy", "content", "safety", "accessibility", "presentation", "pack")
        published = gates == required and bool(payload.get("reextract_verified")) and bool(payload.get("rerender_verified"))
        return GoldenResult(
            fixture=f"{workflow}/production",
            published=published,
            graph_hash=content_hash(payload),
            gate_decisions=gates,
            deliverables=deliverables,
        )

    @staticmethod
    def _read(path: Path) -> dict[str, object]:
        return json.loads(path.read_text(encoding="utf-8"))
