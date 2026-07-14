from __future__ import annotations

import argparse
import json
import sqlite3
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def _validate_sqlite(path: Path) -> dict[str, object]:
    errors: list[str] = []
    count = 0
    try:
        with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as connection:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity != "ok":
                errors.append(f"SQLite integrity failure: {integrity}")
            tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "items" not in tables:
                errors.append("SQLite export requires items table")
            else:
                count = connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    except (OSError, sqlite3.Error) as error:
        errors.append(f"invalid SQLite database: {error}")
    return {"valid": not errors, "record_count": count, "errors": errors}


def _validate_jsonl(path: Path) -> dict[str, object]:
    errors: list[str] = []
    count = 0
    ids: list[object] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return {"valid": False, "record_count": 0, "errors": [f"unreadable JSONL: {error}"]}
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"line {line_number} invalid JSON: {error.msg}")
            continue
        if not isinstance(record, dict):
            errors.append(f"line {line_number} must be an object")
            continue
        count += 1
        if "item_id" in record:
            ids.append(record["item_id"])
    if ids and len(ids) != len(set(ids)):
        errors.append("JSONL item IDs must be unique in an export projection")
    return {"valid": not errors, "record_count": count, "errors": errors}


def _validate_qti(path: Path) -> dict[str, object]:
    errors: list[str] = []
    count = 0
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if archive.testzip():
                errors.append("QTI package has a CRC failure")
            for required in ("imsmanifest.xml", "assessmentTest.xml"):
                if required not in names:
                    errors.append(f"missing {required}")
            item_files = sorted(name for name in names if name.startswith("items/") and name.endswith(".xml"))
            count = len(item_files)
            if not item_files:
                errors.append("QTI package contains no item XML")
            for name in [required for required in ("imsmanifest.xml", "assessmentTest.xml") if required in names] + item_files:
                try:
                    ET.fromstring(archive.read(name))
                except ET.ParseError as error:
                    errors.append(f"invalid XML {name}: {error}")
    except (OSError, zipfile.BadZipFile) as error:
        errors.append(f"invalid QTI ZIP: {error}")
    return {"valid": not errors, "record_count": count, "errors": errors}


def _validate_h5p(path: Path) -> dict[str, object]:
    errors: list[str] = []
    count = 0
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if archive.testzip():
                errors.append("H5P package has a CRC failure")
            for required in ("h5p.json", "content/content.json"):
                if required not in names:
                    errors.append(f"missing {required}")
            if {"h5p.json", "content/content.json"} <= names:
                try:
                    definition = json.loads(archive.read("h5p.json"))
                    content = json.loads(archive.read("content/content.json"))
                except (json.JSONDecodeError, UnicodeDecodeError) as error:
                    errors.append(f"invalid H5P JSON: {error}")
                else:
                    for field in ("title", "mainLibrary", "language", "embedTypes", "preloadedDependencies"):
                        if not definition.get(field):
                            errors.append(f"h5p.json missing {field}")
                    interactions = content.get("assets", {}).get("interactions", [])
                    if not isinstance(interactions, list):
                        errors.append("H5P interactions must be a list")
                    else:
                        count = len(interactions)
    except (OSError, zipfile.BadZipFile) as error:
        errors.append(f"invalid H5P ZIP: {error}")
    return {"valid": not errors, "record_count": count, "errors": errors}


def validate_export(path: Path, kind: str) -> dict[str, object]:
    validators = {
        "sqlite": _validate_sqlite,
        "jsonl": _validate_jsonl,
        "qti": _validate_qti,
        "h5p": _validate_h5p,
    }
    if kind not in validators:
        return {"valid": False, "record_count": 0, "errors": [f"unsupported structured export kind {kind}"]}
    return validators[kind](path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Zamery V3 structured delivery export.")
    parser.add_argument("kind", choices=("sqlite", "jsonl", "qti", "h5p"))
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    report = validate_export(args.path, args.kind)
    print(json.dumps(report, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
