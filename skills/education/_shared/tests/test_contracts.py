import json
import tempfile
import unittest
from pathlib import Path

from contracts import (
    ZAMERY_SKILL_NAMES,
    validate_artifact,
    validate_assessment_bundle,
    validate_brand_contract,
    validate_layout_contract,
    validate_teaching_brief,
)
from scripts.certify_installed_suite import discover_skill_dirs

ROOT = Path(__file__).resolve().parents[1]


def fixture(name: str) -> dict[str, object]:
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


class ContractTests(unittest.TestCase):
    def test_valid_brief_passes(self) -> None:
        self.assertEqual(validate_teaching_brief(fixture("valid-teaching-brief.json")), [])

    def test_grade_and_cefr_must_have_independent_provenance(self) -> None:
        errors = validate_teaching_brief(fixture("invalid-grade-cefr-brief.json"))
        self.assertIn("cefr provenance may not be derived_from_grade", errors)

    def test_grade_band_must_be_inside_k12(self) -> None:
        changed = {**fixture("valid-teaching-brief.json"), "grade_band": "college"}
        self.assertIn("grade_band must be a supported K–12 band", validate_teaching_brief(changed))

    def test_artifact_requires_objective_identity(self) -> None:
        errors = validate_artifact({"artifact_id": "a-1", "artifact_type": "worksheet", "audience": "student"})
        self.assertIn("objective_ids must be a non-empty list", errors)

    def test_valid_assessment_bundle_passes(self) -> None:
        self.assertEqual(validate_assessment_bundle(fixture("valid-assessment-bundle.json")), [])

    def test_student_answer_leakage_blocks_bundle(self) -> None:
        errors = validate_assessment_bundle(fixture("leaked-assessment-bundle.json"))
        self.assertTrue(any(error.startswith("student answer leakage at") for error in errors))

    def test_suite_declares_exactly_twelve_unique_names(self) -> None:
        self.assertEqual(len(ZAMERY_SKILL_NAMES), 12)
        self.assertEqual(len(set(ZAMERY_SKILL_NAMES)), 12)
        self.assertIn("zamery-design-teaching-materials", ZAMERY_SKILL_NAMES)

    def test_approved_v2_brand_contract_passes(self) -> None:
        data = json.loads((ROOT / "brand-contract.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_brand_contract(data), [])

    def test_valid_layout_contract_passes(self) -> None:
        self.assertEqual(validate_layout_contract(fixture("valid-layout-manifest.json")), [])

    def test_internal_metadata_and_footer_only_branding_are_rejected(self) -> None:
        errors = validate_layout_contract(fixture("invalid-internal-metadata-layout.json"))
        self.assertIn("visible content contains forbidden internal term route plan", errors)
        self.assertIn("brand must be applied beyond footer text", errors)

    def test_discovers_frontmatter_names_and_reports_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "skill-a"
            second = root / "skill-b"
            first.mkdir()
            second.mkdir()
            (first / "SKILL.md").write_text(
                "---\nname: zamery-design-english-learning\ndescription: x\n---\n",
                encoding="utf-8",
            )
            (second / "SKILL.md").write_text(
                "---\nname: unrelated-skill\ndescription: x\n---\n",
                encoding="utf-8",
            )

            found, errors = discover_skill_dirs(
                root,
                (
                    "zamery-design-english-learning",
                    "zamery-build-english-practice",
                ),
            )

            self.assertEqual(found, {"zamery-design-english-learning": first})
            self.assertEqual(errors, ["missing skill zamery-build-english-practice"])


if __name__ == "__main__":
    unittest.main()
