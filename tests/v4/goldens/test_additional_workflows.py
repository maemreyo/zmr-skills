import json
from pathlib import Path

def load(name: str):
    return json.loads(Path(f"goldens/v4/{name}/manifest.json").read_text())

def test_worksheet_memberships_are_distinct() -> None:
    data=load("worksheet-basic")
    assert not (set(data["guided_ids"]) & set(data["independent_ids"]) | set(data["retrieval_ids"]) & set(data["guided_ids"]))
    assert data["answer_separated"]

def test_item_bank_has_exactly_300_stable_ids() -> None:
    data=load("item-bank-300")
    assert len(data["item_ids"]) == len(set(data["item_ids"])) == 300
    assert data["sqlite_rebuildable"] and data["jsonl_authority"]

def test_assessment_has_100_items_and_no_leakage() -> None:
    data=load("assessment-100")
    assert len(data["active_item_ids"]) == 100 and not data["answer_leakage"] and data["qti_valid"]

def test_video_and_reteaching_boundaries() -> None:
    video=load("video-learning"); loop=load("reteaching-loop")
    assert all(video.values())
    assert loop["student_card_downstream"] is False and loop["human_decision"]
