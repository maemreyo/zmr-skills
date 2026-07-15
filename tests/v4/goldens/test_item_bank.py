import json
from pathlib import Path


def test_item_bank_has_300_deterministic_authoritative_items() -> None:
    data = json.loads(Path("goldens/v4/item-bank-300/manifest.json").read_text())
    assert len(data["item_ids"]) == 300
    assert data["item_ids"] == sorted(data["item_ids"])
    assert len(set(data["item_ids"])) == 300
    assert data["duplicate_prompts"] == 0
    assert data["jsonl_authority"] and data["sqlite_rebuildable"]
