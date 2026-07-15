from migrations.v4 import default_v3_registry


def test_inferred_cefr_requires_review_and_reopen_boolean_is_discarded() -> None:
    result = default_v3_registry().migrate(
        {"duration_minutes": 90, "source_id": "book:1", "cefr_inferred": "A2", "reopened_after_export": True},
        "teaching-brief.v3", "teaching-brief.v4",
    )
    assert result.status == "review_required"
    assert "cefr_inferred" in result.receipt.review_required_fields
    assert "reopened_after_export" in result.receipt.discarded_fields


def test_unsupported_source_claim_is_rejected() -> None:
    result = default_v3_registry().migrate(
        {"duration_minutes": 90, "source_id": "book:1", "unsupported_source_claim": "copied in full"},
        "teaching-brief.v3", "teaching-brief.v4",
    )
    assert result.status == "rejected"
