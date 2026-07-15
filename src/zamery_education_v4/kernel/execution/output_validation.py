from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...protocol.manifest import CapabilityManifest
from ...protocol.result import CapabilityResult
from ..hashing import sha256_file
from ..records.base import CanonicalRecord
from ..records.registry import RecordRegistry
from .errors import OutputHashMismatch, OutputValidationError


@dataclass(frozen=True)
class ValidatedCapabilityOutputs:
    records: tuple[CanonicalRecord, ...]
    files: tuple[Path, ...]


def _contained(root: Path, relative: str) -> Path:
    if Path(relative).is_absolute():
        raise OutputValidationError("absolute output path")
    target = (root / relative).resolve()
    if root.resolve() not in target.parents:
        raise OutputValidationError("output path escapes mount")
    return target


def validate_outputs(
    result: CapabilityResult,
    *,
    output_root: Path,
    manifest: CapabilityManifest,
    registry: RecordRegistry,
    known_record_ids: set[str] | None = None,
) -> ValidatedCapabilityOutputs:
    records: list[CanonicalRecord] = []
    files: list[Path] = []
    allowed = set(manifest.outputs)
    for output in result.outputs:
        if output.output_type not in allowed:
            raise OutputValidationError(f"undeclared output type: {output.output_type}")
        path = _contained(output_root, output.path)
        if not path.is_file():
            raise OutputValidationError(f"missing output file: {output.path}")
        if output.record_type:
            import json
            payload = json.loads(path.read_text(encoding="utf-8"))
            record = registry.parse(payload)
            if output.record_type != record.record_type:
                raise OutputValidationError("record type mismatch")
            if record.calculated_hash != output.declared_hash:
                raise OutputHashMismatch(output.path)
            records.append(record)
        else:
            if sha256_file(path) != output.declared_hash:
                raise OutputHashMismatch(output.path)
            files.append(path)
    if known_record_ids is not None:
        produced = {record.record_id for record in records}
        if produced & known_record_ids:
            raise OutputValidationError("capability attempted to replace existing record id")
    return ValidatedCapabilityOutputs(tuple(records), tuple(files))
