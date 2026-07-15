from __future__ import annotations

from pathlib import Path
from zipfile import BadZipFile, ZipFile

from pptx import Presentation

from adapters.shared import normalize_visible_text, semantic_text_fingerprint
from zamery_education_v4.kernel.hashing import sha256_file

from .geometry import inspect_geometry
from .notes import inspect_notes


def _visible_text(path: Path) -> str:
    presentation = Presentation(path)
    chunks: list[str] = []
    for slide in presentation.slides:
        title = slide.shapes.title
        if title is None or not title.text.strip():
            chunks.append("[MISSING_SLIDE_TITLE]")
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False):
                chunks.append(shape.text)
    return normalize_visible_text("\n".join(chunks))


def inspect_pptx(path: str | Path) -> dict[str, object]:
    path = Path(path)
    findings: list[str] = []
    visible = ""
    try:
        findings.extend(inspect_notes(path))
        findings.extend(inspect_geometry(path))
        visible = _visible_text(path)
        if "[MISSING_SLIDE_TITLE]" in visible:
            findings.append("PPTX_SLIDE_TITLE_MISSING")
        with ZipFile(path) as archive:
            for name in archive.namelist():
                if name.endswith(".rels") and b'TargetMode="External"' in archive.read(name):
                    findings.append("PPTX_EXTERNAL_RELATIONSHIP")
                if (
                    name.startswith("ppt/slides/slide")
                    and name.endswith(".xml")
                    and b'show="0"' in archive.read(name)
                ):
                    findings.append("PPTX_HIDDEN_SLIDE")
    except (BadZipFile, KeyError, ValueError):
        findings.append("PPTX_REOPEN_FAILED")
    return {
        "result": "fail" if findings else "pass",
        "findings": sorted(set(findings)),
        "binary_hash": sha256_file(path),
        "visible_text": visible,
        "semantic_fingerprint": semantic_text_fingerprint(visible),
    }
