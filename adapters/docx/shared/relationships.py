from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from lxml import etree

REL_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}


def external_relationships(path: str | Path) -> tuple[str, ...]:
    found: list[str] = []
    with ZipFile(path) as archive:
        for name in archive.namelist():
            if not name.endswith(".rels"):
                continue
            root = etree.fromstring(archive.read(name))
            for rel in root.xpath("//r:Relationship[@TargetMode='External']", namespaces=REL_NS):
                found.append(str(rel.attrib.get("Target", "")))
    return tuple(sorted(found))
