import csv
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from scripts.item_bank import (
    deduplicate_bank,
    export_jsonl,
    export_review_csv,
    ingest_jsonl,
    init_database,
    validate_database,
)


def make_item(index: int, *, stem: str | None = None, version: int = 1) -> dict[str, object]:
    return {
        "schema_version": "zamery-item.v3",
        "item_id": f"grammar-g6-{index:04d}",
        "version": version,
        "status": "approved",
        "language": "en",
        "grade_band": "grades_6_8",
        "cefr": "A2",
        "domain": "grammar",
        "skill": "language_use",
        "objective_ids": ["OBJ-SVA-01"],
        "interaction": "single_choice",
        "response_mode": "selected",
        "cognitive_operation": "apply",
        "difficulty": round(0.2 + (index % 7) * 0.1, 2),
        "stem": stem or f"Choose the correct verb for sentence number {index}.",
        "options": [
            {"option_id": "A", "text": "walk"},
            {"option_id": "B", "text": "walks"},
            {"option_id": "C", "text": "walking"},
        ],
        "answer": {"correct_option_ids": ["B"]},
        "rationale": "A singular third-person subject takes -s.",
        "source_anchors": [
            {
                "source_id": "teacher-brief-01",
                "authority": "teacher_supplied",
                "locator": f"objective-{index % 4}",
            }
        ],
        "tags": ["present-simple", "subject-verb-agreement"],
    }


def write_jsonl(path: Path, items: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in items),
        encoding="utf-8",
    )


class ItemBankTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.database = self.root / "bank.sqlite"
        init_database(self.database)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_initializes_versioned_operational_schema(self) -> None:
        with sqlite3.connect(self.database) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
        self.assertTrue({"items", "batches", "ingest_events", "duplicate_pairs"} <= tables)

    def test_resumes_a_400_item_batch_idempotently(self) -> None:
        first = self.root / "first.jsonl"
        all_items = self.root / "all.jsonl"
        write_jsonl(first, [make_item(index) for index in range(1, 201)])
        write_jsonl(all_items, [make_item(index) for index in range(1, 401)])

        first_result = ingest_jsonl(
            self.database, first, batch_id="bulk-400", requested_count=400, chunk_size=40, seed=17
        )
        resumed = ingest_jsonl(
            self.database, all_items, batch_id="bulk-400", requested_count=400, chunk_size=40, seed=17
        )

        self.assertEqual(first_result, {"inserted": 200, "unchanged": 0, "rejected": 0})
        self.assertEqual(resumed, {"inserted": 200, "unchanged": 200, "rejected": 0})
        self.assertEqual(validate_database(self.database)["approved_items"], 400)
        with sqlite3.connect(self.database) as connection:
            status, completed = connection.execute(
                "SELECT status, completed_count FROM batches WHERE batch_id = ?", ("bulk-400",)
            ).fetchone()
        self.assertEqual((status, completed), ("complete", 400))

    def test_preserves_versions_and_rejects_mutating_same_version(self) -> None:
        source = self.root / "versions.jsonl"
        item_v1 = make_item(1)
        item_v2 = make_item(1, version=2, stem="Choose the best present-simple form.")
        write_jsonl(source, [item_v1, item_v2])
        self.assertEqual(
            ingest_jsonl(self.database, source, batch_id="versions", requested_count=2)["inserted"],
            2,
        )

        changed_same_version = make_item(1, stem="Silently changed stem")
        write_jsonl(source, [changed_same_version])
        result = ingest_jsonl(self.database, source, batch_id="versions", requested_count=2)
        self.assertEqual(result, {"inserted": 0, "unchanged": 0, "rejected": 1})
        self.assertEqual(validate_database(self.database)["item_versions"], 2)

    def test_exports_round_trip_jsonl_and_teacher_review_csv(self) -> None:
        source = self.root / "source.jsonl"
        write_jsonl(source, [make_item(1), make_item(2), make_item(3)])
        ingest_jsonl(self.database, source, batch_id="export", requested_count=3)
        jsonl_out = self.root / "export.jsonl"
        csv_out = self.root / "review.csv"

        self.assertEqual(export_jsonl(self.database, jsonl_out), 3)
        self.assertEqual(export_review_csv(self.database, csv_out), 3)
        exported = [json.loads(line) for line in jsonl_out.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([item["item_id"] for item in exported], sorted(item["item_id"] for item in exported))
        with csv_out.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 3)
        self.assertIn("options_json", rows[0])
        self.assertIsInstance(json.loads(rows[0]["options_json"]), list)

    def test_reports_exact_and_near_duplicates_without_deleting_items(self) -> None:
        exact = "Choose the correct form of the verb in this present simple sentence."
        near = "Choose the correct form of a verb in this present simple sentence."
        source = self.root / "dupes.jsonl"
        write_jsonl(
            source,
            [make_item(1, stem=exact), make_item(2, stem=exact), make_item(3, stem=near)],
        )
        ingest_jsonl(self.database, source, batch_id="dupes", requested_count=3)
        report = self.root / "duplicates.csv"

        pairs = deduplicate_bank(self.database, report, threshold=0.75)

        self.assertGreaterEqual(pairs, 3)
        report_text = report.read_text(encoding="utf-8")
        self.assertIn("exact", report_text)
        self.assertIn("near", report_text)
        self.assertEqual(validate_database(self.database)["approved_items"], 3)

    def test_invalid_records_are_rejected_with_line_level_evidence(self) -> None:
        invalid = make_item(1)
        invalid["source_anchors"] = []
        source = self.root / "invalid.jsonl"
        write_jsonl(source, [invalid])

        result = ingest_jsonl(self.database, source, batch_id="invalid", requested_count=1)

        self.assertEqual(result["rejected"], 1)
        rejection_path = source.with_suffix(".rejections.jsonl")
        rejection = json.loads(rejection_path.read_text(encoding="utf-8").strip())
        self.assertEqual(rejection["line"], 1)
        self.assertIn("source_anchors must be a non-empty list", rejection["errors"])

    def test_missing_cefr_and_malformed_options_are_rejected_without_crashing_batch(self) -> None:
        missing_cefr = make_item(1)
        missing_cefr.pop("cefr")
        malformed_option = make_item(2)
        malformed_option["options"][0] = {"option_id": "", "text": ""}
        source = self.root / "invalid-required-fields.jsonl"
        write_jsonl(source, [missing_cefr, malformed_option])

        result = ingest_jsonl(
            self.database,
            source,
            batch_id="invalid-required-fields",
            requested_count=2,
        )

        self.assertEqual(result, {"inserted": 0, "unchanged": 0, "rejected": 2})
        rejections = [
            json.loads(line)
            for line in source.with_suffix(".rejections.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        self.assertIn("cefr must be a non-empty string", rejections[0]["errors"])
        self.assertIn("choice options require non-empty option_id and text", rejections[1]["errors"])


if __name__ == "__main__":
    unittest.main()
