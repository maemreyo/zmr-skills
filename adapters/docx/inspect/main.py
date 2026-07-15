from __future__ import annotations

from pathlib import Path
from zipfile import BadZipFile, ZipFile

from docx import Document

from adapters.docx.shared.relationships import external_relationships
from adapters.shared import normalize_visible_text, semantic_text_fingerprint
from zamery_education_v4.kernel.hashing import sha256_file


def _visible_text(document: Document) -> str:
    chunks = [paragraph.text for paragraph in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            chunks.extend(cell.text for cell in row.cells)
    return normalize_visible_text("\n".join(chunks))


def inspect_docx(path: str | Path) -> dict[str, object]:
    path = Path(path)
    findings: list[str] = []
    try:
        with ZipFile(path) as archive:
            names = set(archive.namelist())
            if any(name.endswith("vbaProject.bin") for name in names):
                findings.append("DOCX_MACRO_PRESENT")
            if "word/comments.xml" in names:
                findings.append("DOCX_COMMENTS_PRESENT")
            document_xml = archive.read("word/document.xml")
            if b"<w:ins" in document_xml or b"<w:del" in document_xml:
                findings.append("DOCX_TRACKED_CHANGES_PRESENT")
    except (BadZipFile, KeyError):
        return {
            "result": "fail",
            "findings": ["DOCX_INVALID_PACKAGE"],
            "binary_hash": sha256_file(path),
        }
    if external_relationships(path):
        findings.append("DOCX_EXTERNAL_RELATIONSHIP")
    visible = ""
    try:
        document = Document(path)
        visible = _visible_text(document)
        if not document.core_properties.title:
            findings.append("DOCX_TITLE_MISSING")
        if not any(
            paragraph.style.name.startswith("Heading")
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ):
            findings.append("DOCX_HEADING_HIERARCHY_MISSING")
        if document.core_properties.author not in {None, "", "Zamery"}:
            findings.append("DOCX_UNEXPECTED_AUTHOR_METADATA")
        for table_index, table in enumerate(document.tables, 1):
            if table.rows and not all(cell.text.strip() for cell in table.rows[0].cells):
                findings.append(f"DOCX_TABLE_HEADER_EMPTY:{table_index}")
    except Exception:
        findings.append("DOCX_REOPEN_FAILED")
    return {
        "result": "fail" if findings else "pass",
        "findings": sorted(set(findings)),
        "binary_hash": sha256_file(path),
        "visible_text": visible,
        "semantic_fingerprint": semantic_text_fingerprint(visible),
    }
