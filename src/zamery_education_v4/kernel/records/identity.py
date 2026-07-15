from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from ..types import RecordHash, RecordId


class RecordRef(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    record_id: RecordId
    record_type: str
    record_hash: RecordHash
