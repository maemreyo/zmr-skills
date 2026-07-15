from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..kernel.types import RecordHash


class OutputDeclaration(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    output_type: str
    path: str
    declared_hash: RecordHash
    record_type: str | None = None
    media_type: str | None = None


class CapabilityResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    protocol_version: Literal["zamery-capability.v1"] = "zamery-capability.v1"
    status: Literal["success"] = "success"
    invocation_id: str
    outputs: tuple[OutputDeclaration, ...]
    metrics: dict[str, int | float | str] = Field(default_factory=dict)

    @field_validator("outputs")
    @classmethod
    def unique_paths(cls, values: tuple[OutputDeclaration, ...]) -> tuple[OutputDeclaration, ...]:
        paths = [value.path for value in values]
        if len(paths) != len(set(paths)):
            raise ValueError("duplicate output path")
        return tuple(sorted(values, key=lambda value: value.path))


class CapabilityFailure(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    protocol_version: Literal["zamery-capability.v1"] = "zamery-capability.v1"
    status: Literal["failure"] = "failure"
    invocation_id: str
    failure_code: str
    message: str
    retryable: bool = False
    affected_ids: tuple[str, ...] = ()
