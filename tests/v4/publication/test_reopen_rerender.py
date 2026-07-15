from pathlib import Path

from adapters.docx.generate import generate_docx
from zamery_education_v4.application.publication import verify_extracted_bundle


def test_extracted_docx_reopens_and_rerenders(tmp_path: Path) -> None:
    root = tmp_path / "bundle"
    root.mkdir()
    generate_docx(
        {
            "title": "Unit 1",
            "blocks": [
                {"kind": "heading", "level": 1, "text": "Unit 1"},
                {"kind": "paragraph", "text": "Practice vocabulary."},
            ],
        },
        root / "workbook.docx",
    )
    result = verify_extracted_bundle(root)
    assert result["reopened"]
    assert result["rerendered"]
    assert not any(
        finding.startswith("RERENDER_FAILED")
        for finding in result["findings"]
    )
