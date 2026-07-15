from zamery_education_v4.kernel.evidence.inspectors import inspect_source_lineage


def test_deterministic_inspector_produces_same_receipt_hash() -> None:
    payload = {"items": [{"record_id": "item:1", "source_ids": ["source:1"]}]}
    first = inspect_source_lineage(payload)
    second = inspect_source_lineage(payload)
    assert first.calculated_hash == second.calculated_hash
