from pathlib import Path

from adapters.pptx.generate import generate_pptx
from adapters.pptx.inspect import inspect_pptx


def test_present_but_empty_notes_fail(tmp_path: Path) -> None:
    path = generate_pptx({"slides":[{"title":"Title","body":"Body","notes":""}]}, tmp_path / "empty-notes.pptx")
    receipt = inspect_pptx(path)
    assert receipt["result"] == "fail"
    assert "EMPTY_SPEAKER_NOTES" in receipt["findings"]
