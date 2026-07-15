from __future__ import annotations
from pydantic import BaseModel, ConfigDict

class ComparisonReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    v3_deliverables: tuple[str, ...]
    v4_deliverables: tuple[str, ...]
    metrics: dict[str, int | bool | str]
    severe_regressions: tuple[str, ...]
    acceptable: bool
