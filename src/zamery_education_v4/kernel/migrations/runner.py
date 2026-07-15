from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MigrationContext(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    actor: str = "migration-tool"
    allow_inference: bool = False
