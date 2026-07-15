from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from lxml import etree

NS = {"a":"http://schemas.openxmlformats.org/drawingml/2006/main"}


def inspect_notes(path: str | Path) -> list[str]:
    findings: list[str] = []
    with ZipFile(path) as archive:
        names = sorted(name for name in archive.namelist() if name.startswith("ppt/notesSlides/notesSlide") and name.endswith(".xml"))
        slide_count = len([name for name in archive.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")])
        if len(names) != slide_count:
            findings.append("SPEAKER_NOTES_RELATIONSHIP_MISMATCH")
        for name in names:
            root = etree.fromstring(archive.read(name))
            text = " ".join(value for value in root.xpath("//a:t/text()", namespaces=NS) if value.strip())
            if not text.strip():
                findings.append("EMPTY_SPEAKER_NOTES")
    return findings
