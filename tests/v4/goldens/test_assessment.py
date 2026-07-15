import json
from pathlib import Path

from capabilities.composition.qti_export import export_qti


def test_assessment_membership_and_qti_ids_are_exact() -> None:
    data = json.loads(Path("goldens/v4/assessment-100/manifest.json").read_text())
    ids = data["active_item_ids"]
    assert len(ids) == len(set(ids)) == 100
    assert not data["answer_leakage"]
    qti = export_qti([{"id": item_id} for item_id in ids])
    assert qti.count(b"assessmentItemRef") == 100
