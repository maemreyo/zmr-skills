import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_learning_sequence import validate_learning_sequence  # noqa: E402

VALID: dict[str, object] = {
    "schema_version": "zamery-learning-sequence.v1",
    "sequence_id": "seq-2026-term1",
    "source_authority": "teacher_supplied",
    "duration_weeks": 16,
    "objective_ids": ["obj-past-perfect", "obj-reported-speech", "obj-conditional-3"],
    "prerequisite_edges": [
        {"from": "obj-past-perfect", "to": "obj-reported-speech"},
        {"from": "obj-reported-speech", "to": "obj-conditional-3"},
    ],
    "coverage": [
        {"objective_id": "obj-past-perfect", "sessions": [1, 2, 5]},
        {"objective_id": "obj-reported-speech", "sessions": [3, 4, 6, 8]},
        {"objective_id": "obj-conditional-3", "sessions": [7, 9, 10]},
    ],
    "review_schedule": [
        {"session": 4, "objective_ids": ["obj-past-perfect"]},
        {"session": 7, "objective_ids": ["obj-past-perfect", "obj-reported-speech"]},
        {"session": 10, "objective_ids": ["obj-conditional-3"]},
    ],
    "assessment_windows": [
        {"session": 6, "objective_ids": ["obj-reported-speech"]},
        {"session": 11, "objective_ids": ["obj-past-perfect", "obj-reported-speech", "obj-conditional-3"]},
    ],
    "transfer_levels": ["near", "far"],
    "standards_coverage": {
        "cefr_b1": {"standard_id": "CEFR-B1-Reporting", "authority": "teacher_supplied"},
    },
    "version": 1,
}


class LearningSequenceValidatorTests(unittest.TestCase):
    def test_valid_sequence_passes(self) -> None:
        self.assertEqual(validate_learning_sequence(VALID), [])

    def test_schema_version_must_match(self) -> None:
        changed = {**VALID, "schema_version": "zamery-learning-sequence.v0"}
        self.assertIn(
            "schema_version must be zamery-learning-sequence.v1",
            validate_learning_sequence(changed),
        )

    def test_sequence_id_must_be_non_empty(self) -> None:
        changed = {**VALID, "sequence_id": ""}
        self.assertIn(
            "sequence_id must be a non-empty string",
            validate_learning_sequence(changed),
        )

    def test_source_authority_must_be_valid(self) -> None:
        changed = {**VALID, "source_authority": "unverified_blog"}
        errors = validate_learning_sequence(changed)
        self.assertTrue(any("source_authority must be one of" in e for e in errors))

    def test_duration_weeks_must_be_positive(self) -> None:
        changed = {**VALID, "duration_weeks": 0}
        self.assertIn(
            "duration_weeks must be a positive integer",
            validate_learning_sequence(changed),
        )

    def test_objective_ids_must_be_non_empty(self) -> None:
        changed = {**VALID, "objective_ids": []}
        self.assertIn(
            "objective_ids must be a non-empty list of strings",
            validate_learning_sequence(changed),
        )

    def test_objective_ids_must_be_unique(self) -> None:
        changed = {**VALID, "objective_ids": ["obj-A", "obj-A"]}
        self.assertIn(
            "objective_ids must be unique",
            validate_learning_sequence(changed),
        )

    def test_prerequisite_edge_refers_to_known_objective(self) -> None:
        changed = {**VALID, "prerequisite_edges": [{"from": "obj-unknown", "to": "obj-past-perfect"}]}
        errors = validate_learning_sequence(changed)
        self.assertTrue(
            any("'obj-unknown' is not in objective_ids" in e for e in errors)
        )

    def test_coverage_requires_all_objectives(self) -> None:
        changed = {
            **VALID,
            "coverage": [{"objective_id": "obj-past-perfect", "sessions": [1]}],
            "objective_ids": ["obj-past-perfect", "obj-orphan"],
        }
        self.assertIn(
            "objective 'obj-orphan' has no coverage entries",
            validate_learning_sequence(changed),
        )

    def test_coverage_session_numbers_must_be_unique(self) -> None:
        changed = {
            **VALID,
            "coverage": [
                {"objective_id": "obj-past-perfect", "sessions": [1, 5, 5]},
                {"objective_id": "obj-reported-speech", "sessions": [3, 4, 6, 8]},
                {"objective_id": "obj-conditional-3", "sessions": [7, 9, 10]},
            ],
        }
        errors = validate_learning_sequence(changed)
        self.assertTrue(any("session numbers must be unique" in e for e in errors))

    def test_review_schedule_must_be_non_empty(self) -> None:
        changed = {**VALID, "review_schedule": []}
        self.assertIn(
            "review_schedule must be a non-empty list",
            validate_learning_sequence(changed),
        )

    def test_assessment_windows_requires_valid_objective(self) -> None:
        changed = {
            **VALID,
            "assessment_windows": [{"session": 5, "objective_ids": ["obj-ghost"]}],
        }
        errors = validate_learning_sequence(changed)
        self.assertTrue(any("cites unknown objective 'obj-ghost'" in e for e in errors))

    def test_transfer_levels_must_include_near_and_far(self) -> None:
        changed = {**VALID, "transfer_levels": ["near"]}
        self.assertIn(
            "transfer_levels must include near and far",
            validate_learning_sequence(changed),
        )

    def test_transfer_levels_must_be_valid_set(self) -> None:
        changed = {**VALID, "transfer_levels": ["near", "far", "intermediate"]}
        errors = validate_learning_sequence(changed)
        self.assertTrue(any("transfer_levels entries must be from" in e for e in errors))

    def test_standards_coverage_optional_and_validated_when_present(self) -> None:
        changed = {**VALID, "standards_coverage": {"bad": {"standard_id": ""}}}
        errors = validate_learning_sequence(changed)
        self.assertTrue(any("standard_id must be a non-empty string" in e for e in errors))

    def test_version_must_be_positive_integer_when_present(self) -> None:
        changed = {**VALID, "version": 0}
        self.assertIn(
            "version must be a positive integer when supplied",
            validate_learning_sequence(changed),
        )

    def test_prior_sequence_id_must_be_non_empty_when_present(self) -> None:
        changed = {**VALID, "prior_sequence_id": ""}
        self.assertIn(
            "prior_sequence_id must be a non-empty string when supplied",
            validate_learning_sequence(changed),
        )

    def test_revision_note_must_be_non_empty_when_present(self) -> None:
        changed = {**VALID, "revision_note": ""}
        self.assertIn(
            "revision_note must be a non-empty string when supplied",
            validate_learning_sequence(changed),
        )


class LearningSequenceCLITests(unittest.TestCase):
    def test_cli_validates_json_from_path(self) -> None:
        import subprocess
        import tempfile

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(VALID, f)
            path = f.name

        script = str(ROOT / "scripts" / "validate_learning_sequence.py")
        result = subprocess.run(
            [sys.executable, script, path],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_cli_reports_errors_to_stderr(self) -> None:
        import subprocess
        import tempfile

        invalid = {**VALID, "transfer_levels": ["near"]}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(invalid, f)
            path = f.name

        script = str(ROOT / "scripts" / "validate_learning_sequence.py")
        result = subprocess.run(
            [sys.executable, script, path],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("transfer_levels must include near and far", result.stderr)

    def test_cli_reports_usage_error_with_wrong_arg_count(self) -> None:
        import subprocess

        script = str(ROOT / "scripts" / "validate_learning_sequence.py")
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
