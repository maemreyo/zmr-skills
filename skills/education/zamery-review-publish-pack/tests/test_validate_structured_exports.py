import json
import sqlite3
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.validate_structured_exports import validate_export


class StructuredExportTests(unittest.TestCase):
    def test_validates_sqlite_integrity_and_jsonl_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "bank.sqlite"
            with sqlite3.connect(database) as connection:
                connection.execute("CREATE TABLE items(item_id TEXT PRIMARY KEY)")
                connection.executemany("INSERT INTO items VALUES (?)", [("i1",), ("i2",)])
            jsonl = root / "bank.jsonl"
            jsonl.write_text('{"item_id":"i1"}\n{"item_id":"i2"}\n', encoding="utf-8")
            self.assertEqual(validate_export(database, "sqlite")["record_count"], 2)
            self.assertEqual(validate_export(jsonl, "jsonl"), {"valid": True, "record_count": 2, "errors": []})

    def test_validates_qti_and_h5p_package_structure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            qti = root / "test.qti.zip"
            with zipfile.ZipFile(qti, "w") as archive:
                archive.writestr("imsmanifest.xml", "<manifest/>")
                archive.writestr("assessmentTest.xml", "<assessmentTest/>")
                archive.writestr("items/i1.xml", "<assessmentItem/>")
            h5p = root / "lesson.h5p"
            with zipfile.ZipFile(h5p, "w") as archive:
                archive.writestr("h5p.json", json.dumps({"title":"Lesson","mainLibrary":"H5P.InteractiveVideo","language":"en","embedTypes":["div"],"preloadedDependencies":[{"machineName":"H5P.InteractiveVideo","majorVersion":1,"minorVersion":28}]}))
                archive.writestr("content/content.json", json.dumps({"assets":{"interactions":[]}}))
            self.assertTrue(validate_export(qti, "qti")["valid"])
            self.assertTrue(validate_export(h5p, "h5p")["valid"])

    def test_rejects_malformed_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.h5p"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("h5p.json", "{}")
            report = validate_export(path, "h5p")
            self.assertFalse(report["valid"])
            self.assertIn("missing content/content.json", report["errors"])


if __name__ == "__main__":
    unittest.main()
