from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from ..hashing import content_hash
from ..types import RecordId


class CanonicalRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    record_type: ClassVar[str]
    schema_version: str = "4.0.0"
    record_id: RecordId

    def canonical_payload(self) -> dict[str, object]:
        payload = self.model_dump(mode="json", exclude_none=True)
        payload["record_type"] = self.record_type
        return payload

    @property
    def calculated_hash(self) -> str:
        return content_hash(self.canonical_payload())
