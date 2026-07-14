import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate_learning_trajectory import validate_evidence_summary


class EvidenceSummaryValidatorTests(unittest.TestCase):
    def test_valid_summary_passes(self) -> None:
        summary = {
            "summary_id": "sum-1",
            "objective_id": "obj-1",
            "evidence_ids": ["ev-1", "ev-2", "ev-3"],
            "point_count": 3,
            "latest_status": "secure",
            "first_observed_at": "2026-06-01",
            "latest_observed_at": "2026-07-14",
            "flags": [],
        }
        self.assertEqual(validate_evidence_summary(summary), [])

    def test_point_count_must_match_evidence_length(self) -> None:
        summary = {
            "summary_id": "sum-1",
            "objective_id": "obj-1",
            "evidence_ids": ["ev-1", "ev-2"],
            "point_count": 3,
            "latest_status": "developing",
            "first_observed_at": "2026-06-01",
            "latest_observed_at": "2026-07-14",
        }
        self.assertIn(
            "point_count must equal the length of evidence_ids",
            validate_evidence_summary(summary),
        )

    def test_first_observed_must_not_exceed_latest(self) -> None:
        summary = {
            "summary_id": "sum-1",
            "objective_id": "obj-1",
            "evidence_ids": ["ev-1"],
            "point_count": 1,
            "latest_status": "emerging",
            "first_observed_at": "2026-07-14",
            "latest_observed_at": "2026-06-01",
        }
        self.assertIn(
            "first_observed_at must be earlier than or equal to latest_observed_at",
            validate_evidence_summary(summary),
        )

    def test_latest_status_must_be_valid(self) -> None:
        summary = {
            "summary_id": "sum-1",
            "objective_id": "obj-1",
            "evidence_ids": ["ev-1"],
            "point_count": 1,
            "latest_status": "invalid_status",
            "first_observed_at": "2026-06-01",
            "latest_observed_at": "2026-07-14",
        }
        self.assertIn(
            "latest_status must be one of emerging, developing, secure, not_observed",
            validate_evidence_summary(summary),
        )

    def test_flags_must_be_valid_subset(self) -> None:
        summary = {
            "summary_id": "sum-1",
            "objective_id": "obj-1",
            "evidence_ids": ["ev-1"],
            "point_count": 1,
            "latest_status": "emerging",
            "first_observed_at": "2026-06-01",
            "latest_observed_at": "2026-07-14",
            "flags": ["unknown_flag"],
        }
        errors = validate_evidence_summary(summary)
        self.assertTrue(
            any("flags must be a subset of" in error for error in errors),
        )

    def test_empty_evidence_list_is_rejected(self) -> None:
        summary = {
            "summary_id": "sum-1",
            "objective_id": "obj-1",
            "evidence_ids": [],
            "point_count": 0,
            "latest_status": "emerging",
            "first_observed_at": "2026-06-01",
            "latest_observed_at": "2026-07-14",
        }
        self.assertIn(
            "evidence_ids must be a non-empty list",
            validate_evidence_summary(summary),
        )

    def test_duplicate_evidence_ids_are_rejected(self) -> None:
        summary = {
            "summary_id": "sum-1",
            "objective_id": "obj-1",
            "evidence_ids": ["ev-1", "ev-1"],
            "point_count": 2,
            "latest_status": "developing",
            "first_observed_at": "2026-06-01",
            "latest_observed_at": "2026-07-14",
        }
        self.assertIn(
            "evidence_ids must be unique",
            validate_evidence_summary(summary),
        )


class CliWrapperTests(unittest.TestCase):
    def test_cli_rejects_missing_argument(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch(
                "sys.argv",
                ["validate_learning_trajectory.py"],
            ):
                from scripts.validate_learning_trajectory import main

                self.assertEqual(main(), 2)

    def test_cli_rejects_missing_file(self) -> None:
        with patch(
            "sys.argv",
            ["validate_learning_trajectory.py", "/nonexistent/trajectory.json"],
        ):
            from scripts.validate_learning_trajectory import main

            with self.assertRaises(FileNotFoundError):
                main()

    def test_cli_validates_learning_trajectory_via_shared_contract(self) -> None:
        """Verify the script calls the shared contracts validator."""
        data = {
            "schema_version": "zamery-learning-trajectory.v1",
            "trajectory_id": "trajectory-1",
            "card_id": "card-1",
            "objective_id": "obj-1",
            "objective_evidence": [
                {"evidence_id": "ev-1", "observed_at": "2026-06-01", "status": "emerging", "authority": "teacher_reviewed"},
                {"evidence_id": "ev-2", "observed_at": "2026-06-21", "status": "developing", "authority": "teacher_reviewed"},
                {"evidence_id": "ev-3", "observed_at": "2026-07-14", "status": "secure", "authority": "teacher_reviewed"},
            ],
            "trend": "improving",
            "review_due_at": "2026-08-01",
        }

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "valid-trajectory.json"
            path.write_text(json.dumps(data), encoding="utf-8")

            with patch("sys.argv", ["validate_learning_trajectory.py", str(path)]):
                from scripts.validate_learning_trajectory import main

                self.assertEqual(main(), 0)

    def test_cli_returns_one_on_validation_errors(self) -> None:
        """When the shared validator reports errors, main() returns 1."""
        invalid = {
            "schema_version": "zamery-learning-trajectory.v1",
            "trajectory_id": "trajectory-1",
            "card_id": "card-1",
            "objective_id": "obj-1",
            "objective_evidence": [
                {"evidence_id": "ev-1", "observed_at": "2026-06-01", "status": "emerging", "authority": "teacher_reviewed"},
            ],
            "trend": "improving",
            "review_due_at": "2026-08-01",
        }

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "invalid-trajectory.json"
            path.write_text(json.dumps(invalid), encoding="utf-8")

            with patch("sys.argv", ["validate_learning_trajectory.py", str(path)]):
                from scripts.validate_learning_trajectory import main

                result = main()
                # With fewer than 3 points and trend "improving",
                # the shared validator should return an error.
                self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
