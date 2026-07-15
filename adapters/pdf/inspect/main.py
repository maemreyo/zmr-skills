from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from adapters.shared import normalize_visible_text, semantic_text_fingerprint
from zamery_education_v4.kernel.hashing import sha256_file


def inspect_pdf(path: str | Path) -> dict[str, object]:
    path = Path(path)
    findings: list[str] = []
    try:
        reader = PdfReader(path)
    except Exception:
        return {
            "result": "fail",
            "findings": ["PDF_REOPEN_FAILED"],
            "binary_hash": sha256_file(path),
        }
    metadata = reader.metadata or {}
    if not metadata.get("/Title"):
        findings.append("PDF_TITLE_MISSING")
    texts: list[str] = []
    for index, page in enumerate(reader.pages, 1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
            findings.append(f"PDF_TEXT_EXTRACTION_FAILED:{index}")
        texts.append(text)
        if "/Annots" in page:
            findings.append(f"PDF_ANNOTATIONS_PRESENT:{index}")
        if not text.strip():
            findings.append(f"PDF_RASTER_OR_BLANK_PAGE:{index}")
    visible = normalize_visible_text("\n".join(texts))
    return {
        "result": "fail" if findings else "pass",
        "findings": sorted(set(findings)),
        "binary_hash": sha256_file(path),
        "page_count": len(reader.pages),
        "visible_text": visible,
        "semantic_fingerprint": semantic_text_fingerprint(visible),
    }
