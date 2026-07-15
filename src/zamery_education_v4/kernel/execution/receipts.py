from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import field_validator

from ..records.base import CanonicalRecord
from ..types import RecordHash


class ExecutionReceipt(CanonicalRecord):
    record_type = "execution_receipt"
    node_id: str
    plan_hash: RecordHash
    cache_key: RecordHash
    status: Literal["success", "failure", "cache_hit", "blocked"]
    output_hashes: tuple[RecordHash, ...] = ()
    failure_code: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    @field_validator("output_hashes")
    @classmethod
    def sorted_unique(cls, values: tuple[RecordHash, ...]) -> tuple[RecordHash, ...]:
        return tuple(sorted(set(values)))
