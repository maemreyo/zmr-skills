from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

from .base import CanonicalRecord


FieldDisposition = Literal["preserved", "transformed", "discarded", "review_required", "rejected"]


class FieldClassification(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    path: str
    disposition: FieldDisposition
    reason: str
    target_path: str | None = None


class MigrationReceipt(CanonicalRecord):
    record_type = "migration_receipt"
    source_schema: str
    target_schema: str
    source_hash: str
    output_hashes: tuple[str, ...] = ()
    classifications: tuple[FieldClassification, ...]

    @field_validator("classifications")
    @classmethod
    def stable_classifications(
        cls, values: tuple[FieldClassification, ...]
    ) -> tuple[FieldClassification, ...]:
        paths = [item.path for item in values]
        if len(paths) != len(set(paths)):
            raise ValueError("each input field path must be classified exactly once")
        return tuple(sorted(values, key=lambda item: item.path))

    @property
    def discarded_fields(self) -> tuple[str, ...]:
        return tuple(item.path for item in self.classifications if item.disposition == "discarded")

    @property
    def review_required_fields(self) -> tuple[str, ...]:
        return tuple(item.path for item in self.classifications if item.disposition == "review_required")

    @property
    def rejected_fields(self) -> tuple[str, ...]:
        return tuple(item.path for item in self.classifications if item.disposition == "rejected")

    @property
    def discard_reasons(self) -> dict[str, str]:
        return {item.path: item.reason for item in self.classifications if item.disposition == "discarded"}


class MigrationOutcome(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    migrated_payloads: tuple[dict[str, object], ...] = ()
    receipt: MigrationReceipt
    status: Literal["migrated", "review_required", "rejected"]
