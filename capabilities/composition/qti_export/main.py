from __future__ import annotations
from xml.etree.ElementTree import Element, SubElement, tostring

def export_qti(items: list[dict[str, object]]) -> bytes:
    assessment = Element("assessmentTest", {"identifier":"zamery-v4","title":"Zamery Assessment"})
    section = SubElement(assessment, "testPart", {"identifier":"main","navigationMode":"linear","submissionMode":"individual"})
    seen: set[str] = set()
    for item in items:
        identifier = str(item["id"])
        if identifier in seen: raise ValueError(f"duplicate QTI identifier: {identifier}")
        seen.add(identifier)
        SubElement(section, "assessmentItemRef", {"identifier":identifier,"href":f"items/{identifier}.xml"})
    return tostring(assessment, encoding="utf-8", xml_declaration=True)
