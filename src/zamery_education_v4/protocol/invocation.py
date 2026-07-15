from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..kernel.types import RecordHash


class CapabilityInvocation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    protocol_version: Literal["zamery-capability.v1"] = "zamery-capability.v1"
    invocation_id: str
    capability_id: str
    capability_version: str
    input_records: tuple[RecordHash, ...] = ()
    configuration: dict[str, object] = Field(default_factory=dict)
    input_mount: str = "inputs"
    output_mount: str = "outputs"

    @field_validator("input_records")
    @classmethod
    def sorted_unique(cls, values: tuple[RecordHash, ...]) -> tuple[RecordHash, ...]:
        return tuple(sorted(set(values)))
