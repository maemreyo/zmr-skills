from __future__ import annotations

import pytest

from migrations.v4 import default_v3_registry
from zamery_education_v4.kernel.migrations import UnreportedMigrationLoss
from zamery_education_v4.kernel.migrations.registry import MigrationDefinition, MigrationRegistry
from zamery_education_v4.kernel.records.migration import MigrationOutcome, MigrationReceipt
from zamery_education_v4.kernel.hashing import content_hash


def test_v3_trust_boolean_is_explicitly_discarded() -> None:
    registry = default_v3_registry()
    payload = {"duration_minutes": 90, "source_id": "book:unit1", "visual_qa_passed": True}
    result = registry.migrate(payload, "teaching-brief.v3", "teaching-brief.v4")
    assert "visual_qa_passed" in result.receipt.discarded_fields
    assert result.receipt.discard_reasons["visual_qa_passed"] == "self_attested_quality"


def test_registry_rejects_unclassified_input_field() -> None:
    registry = MigrationRegistry()
    def broken(payload, context):
        receipt = MigrationReceipt(
            record_id="migration:broken",
            source_schema="a", target_schema="b", source_hash=content_hash(payload),
            classifications=(),
        )
        return MigrationOutcome(receipt=receipt, status="migrated")
    registry.register(MigrationDefinition("a", "b", broken))
    with pytest.raises(UnreportedMigrationLoss):
        registry.migrate({"field": 1}, "a", "b")
