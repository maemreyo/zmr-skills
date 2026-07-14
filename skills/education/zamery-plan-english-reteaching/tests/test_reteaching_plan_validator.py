import io
import json
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

from scripts.validate_reteaching_plan import validate_reteaching_plan


def valid_plan() -> dict[str, object]:
    return {
        "schema_version": "zamery-reteaching-plan.v1",
        "plan_id": "reteach-irregular-past-001",
        "objective_ids": ["obj-irreg-past"],
        "evidence_ids": ["ev-analysis-03", "ev-probe-04"],
        "misconception": {
            "statement": "Regular past-tense rule is overgeneralised to irregular verbs",
            "confidence": "medium",
            "competing_explanations": [
                "The student has not encountered the irregular forms in writing before",
            ],
        },
        "phases": [
            "reconnect_prerequisite",
            "contrast",
            "guided_discrimination",
            "corrective_rehearsal",
            "transfer",
        ],
        "teacher_action": {
            "action_id": "action-irregular-past-001",
            "based_on_snapshot_id": "snapshot-irregular-past-001",
            "snapshot_expires_at": "2026-08-14",
            "target": "obj-irreg-past",
            "evidence_ids": ["ev-analysis-03", "ev-probe-04"],
            "proposed_move": "exemplar_contrast",
            "rationale": "The evidence supports beginning with a minimal contrast",
            "preserves": [
                "shared_objective",
                "assessment_construct",
                "learner_dignity",
            ],
            "trial_window": "two sessions",
            "teacher_approval": True,
            "trial_sessions": 2,
            "expected_signal": "Distinguishes regular and irregular forms in a new context",
            "result": "not-yet-tried",
            "confounding_factors": [],
            "teacher_interpretation": None,
            "review_date": "2026-07-21",
        },
        "reassessment": {
            "objective_ids": ["obj-irreg-past"],
            "success_evidence": "Correctly produces irregular past forms in a new writing task",
            "item_count": 5,
            "wait_days": 2,
            "auto_schedule": True,
        },
    }


class ReteachingPlanValidatorTests(unittest.TestCase):
    def test_valid_plan_passes(self) -> None:
        self.assertEqual(validate_reteaching_plan(valid_plan()), [])

    def test_missing_schema_version(self) -> None:
        plan = valid_plan()
        plan["schema_version"] = "wrong"
        errors = validate_reteaching_plan(plan)
        self.assertIn("schema_version must be zamery-reteaching-plan.v1", errors)

    def test_missing_plan_id(self) -> None:
        plan = valid_plan()
        del plan["plan_id"]
        errors = validate_reteaching_plan(plan)
        self.assertIn("plan_id must be a non-empty string", errors)

    def test_missing_objective_ids(self) -> None:
        plan = valid_plan()
        plan["objective_ids"] = []
        errors = validate_reteaching_plan(plan)
        self.assertIn("objective_ids must be a non-empty list", errors)

    def test_missing_evidence_ids(self) -> None:
        plan = valid_plan()
        del plan["evidence_ids"]
        errors = validate_reteaching_plan(plan)
        self.assertIn("evidence_ids must be a non-empty list", errors)

    def test_invalid_misconception_confidence(self) -> None:
        plan = valid_plan()
        plan["misconception"]["confidence"] = "certain"
        errors = validate_reteaching_plan(plan)
        self.assertIn("misconception.confidence must be low, medium, or high", errors)

    def test_phases_must_follow_canonical_sequence(self) -> None:
        plan = valid_plan()
        plan["phases"] = ["contrast", "reconnect_prerequisite", "transfer"]
        errors = validate_reteaching_plan(plan)
        self.assertIn("reteaching phases must follow the approved corrective sequence", errors)

    def test_phases_must_be_exact_canonical_set(self) -> None:
        plan = valid_plan()
        plan["phases"] = ["reconnect_prerequisite", "quiz"]
        errors = validate_reteaching_plan(plan)
        self.assertIn("reteaching phases must follow the approved corrective sequence", errors)

    def test_teacher_action_preserves_required_fields(self) -> None:
        plan = valid_plan()
        plan["teacher_action"]["preserves"] = ["learner_dignity"]
        errors = validate_reteaching_plan(plan)
        self.assertIn(
            "teacher action must preserve shared_objective, assessment_construct, and learner_dignity",
            errors,
        )

    def test_teacher_action_requires_evidence_to_result_fields(self) -> None:
        plan = valid_plan()
        del plan["teacher_action"]["action_id"]
        del plan["teacher_action"]["expected_signal"]
        plan["teacher_action"]["result"] = "guaranteed"
        errors = validate_reteaching_plan(plan)
        self.assertIn("teacher_action.action_id must be a non-empty string", errors)
        self.assertIn("teacher_action.expected_signal must be a non-empty string", errors)
        self.assertIn("teacher_action.result is invalid", errors)

    def test_missing_reassessment(self) -> None:
        plan = valid_plan()
        del plan["reassessment"]
        errors = validate_reteaching_plan(plan)
        self.assertIn("reteaching plan requires a reassessment object", errors)

    def test_reassessment_requires_success_evidence(self) -> None:
        plan = valid_plan()
        del plan["reassessment"]["success_evidence"]
        errors = validate_reteaching_plan(plan)
        self.assertIn("reassessment.success_evidence must be a non-empty string", errors)

    def test_cli_validates_via_file(self) -> None:
        from scripts.validate_reteaching_plan import main as cli_main

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(valid_plan(), f)
            temp_path = f.name

        try:
            argv = ["validate", temp_path, "--verbose"]
            original_argv = list(sys.argv)
            try:
                sys.argv = argv
                with (
                    unittest.mock.patch("sys.stderr", io.StringIO()) as stderr,
                    unittest.mock.patch("sys.stdout", io.StringIO()) as stdout,
                ):
                    exit_code = cli_main()
                    self.assertEqual(exit_code, 0)
            finally:
                sys.argv = original_argv
        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
