from pathlib import Path

from pypdf import PdfWriter

from adapters.pdf.inspect import inspect_pdf


def test_blank_pdf_page_is_not_self_attested_as_valid(tmp_path: Path) -> None:
    path = tmp_path / "blank.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_metadata({"/Title": "Blank fixture"})
    with path.open("wb") as stream:
        writer.write(stream)
    result = inspect_pdf(path)
    assert result["result"] == "fail"
    assert "PDF_RASTER_OR_BLANK_PAGE:1" in result["findings"]
