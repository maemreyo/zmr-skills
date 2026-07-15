from __future__ import annotations

from typing import NewType

from ..hashing import content_hash

CacheKey = NewType("CacheKey", str)


def calculate_cache_key(
    *,
    capability_id: str,
    capability_version: str,
    runtime_digest: str,
    input_hashes: tuple[str, ...],
    configuration: dict[str, object],
    protocol_version: str,
    policy_version: str,
    temp_dir: str | None = None,
    hostname: str | None = None,
) -> str:
    del temp_dir, hostname
    return content_hash({
        "capability_id": capability_id,
        "capability_version": capability_version,
        "runtime_digest": runtime_digest,
        "input_hashes": sorted(input_hashes),
        "configuration": configuration,
        "protocol_version": protocol_version,
        "policy_version": policy_version,
    })


class CacheStore:
    def __init__(self) -> None:
        self._values: dict[str, object] = {}

    def get(self, key: str) -> object | None:
        return self._values.get(key)

    def put(self, key: str, value: object) -> None:
        self._values[key] = value
