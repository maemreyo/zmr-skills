from __future__ import annotations

from collections.abc import Mapping

from zamery_education_v4.kernel.canonical_json import canonical_json_bytes
from zamery_education_v4.kernel.hashing import content_hash, sha256_bytes
from zamery_education_v4.kernel.migrations.runner import MigrationContext
from zamery_education_v4.kernel.records.migration import (
    FieldClassification,
    MigrationOutcome,
    MigrationReceipt,
)

SELF_ATTESTED = {
    "approved",
    "reopened_after_export",
    "visual_qa_passed",
    "crc_passed",
    "visually_checked",
}


def classify_and_migrate(
    payload: dict[str, object],
    context: MigrationContext,
    *,
    source_schema: str,
    target_schema: str,
    preserved: set[str],
    transformed: Mapping[str, str] | None = None,
    review_required: set[str] | None = None,
    rejected: set[str] | None = None,
) -> MigrationOutcome:
    transformed = transformed or {}
    review_required = review_required or set()
    rejected = rejected or set()
    output: dict[str, object] = {"schema_version": "4.0.0"}
    classifications: list[FieldClassification] = []
    for path, value in _leaves(payload):
        root = path.split(".", 1)[0].split("[", 1)[0]
        if root in SELF_ATTESTED:
            classifications.append(FieldClassification(path=path, disposition="discarded", reason="self_attested_quality"))
        elif root in rejected:
            classifications.append(FieldClassification(path=path, disposition="rejected", reason="unsupported_source_claim"))
        elif root in review_required:
            classifications.append(FieldClassification(path=path, disposition="review_required", reason="requires_human_authority"))
        elif root in transformed:
            target = transformed[root]
            output[target] = value
            classifications.append(FieldClassification(path=path, disposition="transformed", reason="renamed_v4_field", target_path=target))
        elif root in preserved:
            output[root] = payload[root]
            classifications.append(FieldClassification(path=path, disposition="preserved", reason="authoritative_explicit_value", target_path=root))
        else:
            classifications.append(FieldClassification(path=path, disposition="review_required", reason="unmapped_v3_field"))
    source_hash = sha256_bytes(canonical_json_bytes(payload))
    output_hash = content_hash(output)
    receipt = MigrationReceipt(
        record_id=f"migration:{source_hash.split(':', 1)[1][:16]}",
        source_schema=source_schema,
        target_schema=target_schema,
        source_hash=source_hash,
        output_hashes=(output_hash,),
        classifications=tuple(classifications),
    )
    status = "rejected" if receipt.rejected_fields else ("review_required" if receipt.review_required_fields else "migrated")
    return MigrationOutcome(migrated_payloads=(output,), receipt=receipt, status=status)


def _leaves(value: object, prefix: str = "") -> list[tuple[str, object]]:
    if isinstance(value, dict):
        result: list[tuple[str, object]] = []
        if not value:
            return [(prefix, value)] if prefix else []
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            result.extend(_leaves(item, path))
        return result
    if isinstance(value, list):
        result: list[tuple[str, object]] = []
        if not value:
            return [(prefix, value)]
        for index, item in enumerate(value):
            result.extend(_leaves(item, f"{prefix}[{index}]"))
        return result
    return [(prefix, value)]
