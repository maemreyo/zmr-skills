import json
from pathlib import Path


def test_reteaching_keeps_student_card_out_of_canonical_artifacts() -> None:
    data = json.loads(Path("goldens/v4/reteaching-loop/manifest.json").read_text())
    assert data["student_card_downstream"] is False
    assert data["monitoring_evidence"]
    assert data["human_decision"]
    assert data["reassessment_linked"]
