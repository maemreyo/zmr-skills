import json
from pathlib import Path


def test_worksheet_profiles_are_distinct_and_print_safe() -> None:
    data = json.loads(Path("goldens/v4/worksheet-basic/manifest.json").read_text())
    assert set(data["guided_ids"]).isdisjoint(data["independent_ids"])
    assert set(data["retrieval_ids"]).isdisjoint(data["guided_ids"])
    assert data["answer_separated"]
    assert data["print_profile"] == "a4"
