from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from ..canonical_json import canonical_json_bytes
from ..hashing import sha256_bytes
from ..records.migration import MigrationOutcome
from .errors import UnreportedMigrationLoss
from .runner import MigrationContext

MigrationFunction = Callable[[dict[str, object], MigrationContext], MigrationOutcome]


@dataclass(frozen=True, slots=True)
class MigrationDefinition:
    source_schema: str
    target_schema: str
    migrate: MigrationFunction


class MigrationRegistry:
    def __init__(self) -> None:
        self._definitions: dict[tuple[str, str], MigrationDefinition] = {}

    def register(self, definition: MigrationDefinition) -> None:
        key = (definition.source_schema, definition.target_schema)
        if key in self._definitions:
            raise ValueError(f"duplicate migration: {key}")
        self._definitions[key] = definition

    def migrate(
        self,
        payload: dict[str, object],
        source_schema: str,
        target_schema: str,
        context: MigrationContext | None = None,
    ) -> MigrationOutcome:
        try:
            definition = self._definitions[(source_schema, target_schema)]
        except KeyError as error:
            raise ValueError(f"migration not registered: {source_schema} -> {target_schema}") from error
        outcome = definition.migrate(payload, context or MigrationContext())
        classified = {item.path for item in outcome.receipt.classifications}
        input_paths = _leaf_paths(payload)
        missing = sorted(input_paths - classified)
        extra = sorted(classified - input_paths)
        if missing or extra:
            raise UnreportedMigrationLoss(
                f"field classification mismatch; missing={missing}, extra={extra}"
            )
        expected_hash = sha256_bytes(canonical_json_bytes(payload))
        if outcome.receipt.source_hash != expected_hash:
            raise ValueError("migration receipt source hash mismatch")
        return outcome


def _leaf_paths(value: object, prefix: str = "") -> set[str]:
    if isinstance(value, dict):
        result: set[str] = set()
        if not value:
            return {prefix} if prefix else set()
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            result.update(_leaf_paths(item, path))
        return result
    if isinstance(value, list):
        result: set[str] = set()
        if not value:
            return {prefix}
        for index, item in enumerate(value):
            result.update(_leaf_paths(item, f"{prefix}[{index}]"))
        return result
    return {prefix}
