from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict
class PipelineConfig(BaseModel):
    model_config=ConfigDict(extra="forbid", frozen=True, strict=True)
    mode: Literal["v3","v4-canary","v4"]
    final_v3_tag: str
    commit: str | None=None
    verification_report_hash: str | None=None
    canary_accepted: bool=False
    actor: str | None=None
    reason: str | None=None
    changed_at: str | None=None
