from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..kernel.types import RecordHash


class CapabilityManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    capability_id: str
    capability_version: str
    protocol_version: Literal["zamery-capability.v1"] = "zamery-capability.v1"
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...]
    deterministic: bool
    side_effects: Literal["none", "model", "binary", "network", "human"] = "none"
    timeout_seconds: int = Field(default=60, gt=0, le=3600)
    memory_mb: int = Field(default=512, gt=0)
    runtime_kind: Literal["python", "node", "native"]
    runtime_version: str
    runtime_digest: RecordHash
    lockfile_hash: RecordHash
    lockfile_path: str | None = None
    filesystem_read: Literal["input_mount_only"] = "input_mount_only"
    filesystem_write: Literal["output_mount_only"] = "output_mount_only"
    network_domains: tuple[str, ...] = ()
    cache_enabled: bool = True
    failure_codes: tuple[str, ...] = ()

    @field_validator("inputs", "outputs", "network_domains", "failure_codes")
    @classmethod
    def sorted_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted(set(values)))
