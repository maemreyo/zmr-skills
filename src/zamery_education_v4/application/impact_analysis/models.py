from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ImpactReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    changed_ids: tuple[str, ...]
    invalidated_ids: tuple[str, ...]
    preserved_ids: tuple[str, ...]
    reasons: dict[str, tuple[str, ...]]
    material: bool
