from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class RepairPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    affected_ids: tuple[str, ...]
    invalidated_ids: tuple[str, ...]
    preserved_ids: tuple[str, ...]
    required_reruns: tuple[str, ...]
    required_approval_scopes: tuple[str, ...]
    expected_receipt_types: tuple[str, ...]
    original_finding_hashes: tuple[str, ...]
    material: bool
