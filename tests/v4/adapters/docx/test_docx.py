from pathlib import Path

from adapters.docx.generate import generate_docx
from adapters.docx.inspect import inspect_docx


def test_docx_generation_and_independent_inspection(tmp_path: Path) -> None:
    path = generate_docx({"title":"Unit 1","blocks":[{"kind":"heading","level":1,"text":"Unit 1"},{"kind":"paragraph","text":"Practice"}]}, tmp_path / "unit1.docx")
    result = inspect_docx(path)
    assert result["binary_hash"].startswith("sha256:")
    assert "DOCX_REOPEN_FAILED" not in result["findings"]
