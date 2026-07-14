import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.form_composer import _load_bank, assemble_forms, validate_form_equivalence
from scripts.qti_export import export_qti, validate_qti_package


def item(index: int, *, domain: str, section: str) -> dict[str, object]:
    return {
        "schema_version": "zamery-item.v3",
        "item_id": f"{domain}-{index:03d}",
        "version": 1,
        "status": "approved",
        "grade_band": "grades_6_8",
        "cefr": "A2",
        "domain": domain,
        "skill": section,
        "objective_ids": [f"OBJ-{domain.upper()}"],
        "interaction": "single_choice",
        "response_mode": "selected",
        "cognitive_operation": "apply",
        "difficulty": 0.3 + (index % 4) * 0.1,
        "stem": f"{domain.title()} question {index}",
        "options": [
            {"option_id": "A", "text": "Option A"},
            {"option_id": "B", "text": "Option B"},
            {"option_id": "C", "text": "Option C"},
        ],
        "answer": {"correct_option_ids": ["B"]},
        "rationale": "The rule supports option B.",
        "source_anchors": [{"source_id": "teacher", "authority": "teacher_supplied", "locator": "brief"}],
        "tags": [],
    }


BLUEPRINT = {
    "schema_version": "zamery-assessment-blueprint.v3",
    "blueprint_id": "midterm-g7",
    "sections": [
        {"section_id": "grammar", "count": 4, "filters": {"domain": "grammar"}},
        {"section_id": "reading", "count": 3, "filters": {"domain": "reading"}},
    ],
    "equivalence_tolerances": {"mean_difficulty": 0.11},
}


class FormComposerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.bank = self.root / "bank.jsonl"
        items = [item(index, domain="grammar", section="language_use") for index in range(1, 13)]
        items += [item(index, domain="reading", section="comprehension") for index in range(1, 11)]
        self.bank.write_text("".join(json.dumps(record) + "\n" for record in items), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_assembles_deterministic_disjoint_blueprint_exact_forms(self) -> None:
        first = assemble_forms(self.bank, BLUEPRINT, ["A", "B"], seed=2026)
        second = assemble_forms(self.bank, BLUEPRINT, ["A", "B"], seed=2026)
        self.assertEqual(first, second)
        self.assertEqual([len(form["items"]) for form in first], [7, 7])
        for form in first:
            ids = [entry["item_id"] for entry in form["items"]]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(
                {section: sum(entry["section_id"] == section for entry in form["items"]) for section in ("grammar", "reading")},
                {"grammar": 4, "reading": 3},
            )
            self.assertTrue(all(entry["version"] == 1 for entry in form["items"]))
        self.assertTrue(
            set(entry["item_id"] for entry in first[0]["items"]).isdisjoint(
                entry["item_id"] for entry in first[1]["items"]
            )
        )

    def test_changed_seed_changes_selection(self) -> None:
        first = assemble_forms(self.bank, BLUEPRINT, ["A"], seed=1)
        second = assemble_forms(self.bank, BLUEPRINT, ["A"], seed=2)
        self.assertNotEqual(first[0]["items"], second[0]["items"])

    def test_jsonl_loader_excludes_an_item_when_its_latest_version_is_retired(self) -> None:
        retired_v1 = item(90, domain="grammar", section="language_use")
        retired_v2 = {**retired_v1, "version": 2, "status": "retired"}
        active = item(91, domain="grammar", section="language_use")
        source = self.root / "version-status.jsonl"
        source.write_text(
            "".join(json.dumps(record) + "\n" for record in (retired_v1, retired_v2, active)),
            encoding="utf-8",
        )
        loaded = _load_bank(source)
        self.assertEqual([record["item_id"] for record in loaded], [active["item_id"]])

    def test_equivalence_report_checks_counts_distributions_and_difficulty(self) -> None:
        forms = assemble_forms(self.bank, BLUEPRINT, ["A", "B"], seed=2026)
        report = validate_form_equivalence(forms, BLUEPRINT)
        self.assertTrue(report["equivalent"])
        self.assertEqual(report["section_counts"]["A"], {"grammar": 4, "reading": 3})

    def test_equivalence_report_rejects_items_shared_across_forms(self) -> None:
        forms = assemble_forms(self.bank, BLUEPRINT, ["A", "B"], seed=2026)
        forms[1]["items"][0] = forms[0]["items"][0]
        report = validate_form_equivalence(forms, BLUEPRINT)
        self.assertFalse(report["equivalent"])
        self.assertIn("forms A and B share item IDs", report["errors"])

    def test_insufficient_disjoint_pool_is_blocked(self) -> None:
        blueprint = {**BLUEPRINT, "sections": [{"section_id": "grammar", "count": 7, "filters": {"domain": "grammar"}}]}
        with self.assertRaisesRegex(ValueError, "insufficient approved items"):
            assemble_forms(self.bank, blueprint, ["A", "B"], seed=7)

    def test_qti_package_contains_manifest_test_and_every_item(self) -> None:
        form = assemble_forms(self.bank, BLUEPRINT, ["A"], seed=2026)[0]
        package = self.root / "midterm-a.qti.zip"
        export_qti(form, package)
        report = validate_qti_package(package)
        self.assertEqual(report, {"valid": True, "item_count": 7, "errors": []})
        with zipfile.ZipFile(package) as archive:
            self.assertIn("imsmanifest.xml", archive.namelist())
            self.assertIn("assessmentTest.xml", archive.namelist())
            self.assertEqual(len([name for name in archive.namelist() if name.startswith("items/")]), 7)


if __name__ == "__main__":
    unittest.main()
