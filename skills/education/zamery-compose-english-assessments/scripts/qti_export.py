from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

QTI = "http://www.imsglobal.org/xsd/imsqti_v2p2"
IMSCP = "http://www.imsglobal.org/xsd/imscp_v1p1"
ET.register_namespace("", QTI)


def _identifier(value: object) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value))
    if not cleaned or not cleaned[0].isalpha():
        cleaned = f"ID_{cleaned}"
    return cleaned


def _xml(element: ET.Element) -> bytes:
    return ET.tostring(element, encoding="utf-8", xml_declaration=True)


def _item_xml(item: dict[str, object]) -> bytes:
    identifier = _identifier(item["item_id"])
    root = ET.Element(f"{{{QTI}}}assessmentItem", {
        "identifier": identifier,
        "title": str(item.get("stem", identifier))[:80],
        "adaptive": "false",
        "timeDependent": "false",
    })
    interaction = item.get("interaction")
    answer = item.get("answer", {})
    if interaction in {"single_choice", "multiple_choice", "true_false"}:
        cardinality = "single" if interaction != "multiple_choice" else "multiple"
        declaration = ET.SubElement(root, f"{{{QTI}}}responseDeclaration", {
            "identifier": "RESPONSE", "cardinality": cardinality, "baseType": "identifier"
        })
        correct = ET.SubElement(declaration, f"{{{QTI}}}correctResponse")
        for option_id in answer.get("correct_option_ids", []):
            ET.SubElement(correct, f"{{{QTI}}}value").text = _identifier(option_id)
        body = ET.SubElement(root, f"{{{QTI}}}itemBody")
        choice = ET.SubElement(body, f"{{{QTI}}}choiceInteraction", {
            "responseIdentifier": "RESPONSE",
            "shuffle": "false",
            "maxChoices": "1" if cardinality == "single" else str(len(answer.get("correct_option_ids", []))),
        })
        ET.SubElement(choice, f"{{{QTI}}}prompt").text = str(item.get("stem", ""))
        for option in item.get("options", []):
            ET.SubElement(choice, f"{{{QTI}}}simpleChoice", {
                "identifier": _identifier(option.get("option_id"))
            }).text = str(option.get("text", ""))
    else:
        ET.SubElement(root, f"{{{QTI}}}responseDeclaration", {
            "identifier": "RESPONSE", "cardinality": "single", "baseType": "string"
        })
        body = ET.SubElement(root, f"{{{QTI}}}itemBody")
        ET.SubElement(body, f"{{{QTI}}}p").text = str(item.get("stem", ""))
        ET.SubElement(body, f"{{{QTI}}}extendedTextInteraction", {
            "responseIdentifier": "RESPONSE", "expectedLines": str(item.get("expected_response_lines", 4))
        })
    return _xml(root)


def _zip_write(archive: zipfile.ZipFile, name: str, content: bytes) -> None:
    info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, content)


def export_qti(form: dict[str, object], destination: Path) -> None:
    form_id = _identifier(form["form_id"])
    test = ET.Element(f"{{{QTI}}}assessmentTest", {"identifier": form_id, "title": form_id})
    part = ET.SubElement(test, f"{{{QTI}}}testPart", {
        "identifier": f"{form_id}_part", "navigationMode": "linear", "submissionMode": "individual"
    })
    section = ET.SubElement(part, f"{{{QTI}}}assessmentSection", {
        "identifier": f"{form_id}_section", "title": form_id, "visible": "true"
    })
    manifest = ET.Element(f"{{{IMSCP}}}manifest", {"identifier": f"MANIFEST_{form_id}"})
    resources = ET.SubElement(manifest, f"{{{IMSCP}}}resources")
    test_resource = ET.SubElement(resources, f"{{{IMSCP}}}resource", {
        "identifier": f"RES_TEST_{form_id}", "type": "imsqti_test_xmlv2p2", "href": "assessmentTest.xml"
    })
    ET.SubElement(test_resource, f"{{{IMSCP}}}file", {"href": "assessmentTest.xml"})
    item_files: list[tuple[str, bytes]] = []
    for item in form.get("items", []):
        item_id = _identifier(item["item_id"])
        href = f"items/{item_id}.xml"
        ET.SubElement(section, f"{{{QTI}}}assessmentItemRef", {"identifier": f"REF_{item_id}", "href": href})
        resource = ET.SubElement(resources, f"{{{IMSCP}}}resource", {
            "identifier": f"RES_{item_id}", "type": "imsqti_item_xmlv2p2", "href": href
        })
        ET.SubElement(resource, f"{{{IMSCP}}}file", {"href": href})
        ET.SubElement(test_resource, f"{{{IMSCP}}}dependency", {"identifierref": f"RES_{item_id}"})
        item_files.append((href, _item_xml(item)))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w") as archive:
        _zip_write(archive, "imsmanifest.xml", _xml(manifest))
        _zip_write(archive, "assessmentTest.xml", _xml(test))
        for name, content in item_files:
            _zip_write(archive, name, content)


def validate_qti_package(path: Path) -> dict[str, object]:
    errors: list[str] = []
    item_count = 0
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            for required in ("imsmanifest.xml", "assessmentTest.xml"):
                if required not in names:
                    errors.append(f"missing {required}")
            bad_crc = archive.testzip()
            if bad_crc:
                errors.append(f"CRC failure in {bad_crc}")
            if not errors:
                try:
                    manifest = ET.fromstring(archive.read("imsmanifest.xml"))
                    test = ET.fromstring(archive.read("assessmentTest.xml"))
                except ET.ParseError as error:
                    errors.append(f"invalid XML: {error}")
                else:
                    refs = test.findall(f".//{{{QTI}}}assessmentItemRef")
                    item_count = len(refs)
                    hrefs = {ref.get("href") for ref in refs}
                    missing = sorted(href for href in hrefs if href not in names)
                    if missing:
                        errors.append(f"missing item files: {', '.join(missing)}")
                    manifest_hrefs = {node.get("href") for node in manifest.findall(f".//{{{IMSCP}}}file")}
                    if not hrefs <= manifest_hrefs:
                        errors.append("manifest does not declare every item file")
                    for href in hrefs - set(missing):
                        try:
                            root = ET.fromstring(archive.read(href))
                        except ET.ParseError as error:
                            errors.append(f"invalid item XML {href}: {error}")
                        else:
                            if root.tag != f"{{{QTI}}}assessmentItem":
                                errors.append(f"{href} is not a QTI assessmentItem")
    except (OSError, zipfile.BadZipFile) as error:
        errors.append(f"invalid package: {error}")
    return {"valid": not errors, "item_count": item_count, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a Zamery form to IMS QTI 2.2.")
    parser.add_argument("form", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if not args.validate_only:
        export_qti(json.loads(args.form.read_text(encoding="utf-8")), args.destination)
    report = validate_qti_package(args.destination)
    print(json.dumps(report, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
