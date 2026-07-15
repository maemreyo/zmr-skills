import pytest

from zamery_education_v4.kernel.canonical_json import canonical_json_bytes
from zamery_education_v4.kernel.hashing import content_hash


def test_key_order_and_unicode_do_not_change_bytes() -> None:
    left = {"b": "e\u0301", "a": [2, 1]}
    right = {"a": [2, 1], "b": "é"}
    assert canonical_json_bytes(left) == canonical_json_bytes(right)


def test_nonfinite_numbers_are_rejected() -> None:
    with pytest.raises(ValueError):
        canonical_json_bytes(float("nan"))


def test_mapping_order_does_not_change_hash() -> None:
    assert content_hash({"b": 2, "a": 1}) == content_hash({"a": 1, "b": 2})
