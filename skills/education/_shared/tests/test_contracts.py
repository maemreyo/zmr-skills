import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from skills.education._shared import contracts
from skills.education._shared.contracts import (
    ZAMERY_SKILL_NAMES,
    validate_artifact,
    validate_assessment_bundle,
    validate_brand_contract,
    validate_brief_version_assertion,
    validate_communication,
    validate_layout_contract,
    validate_teaching_brief,
)
from skills.education._shared.scripts.certify_installed_suite import discover_skill_dirs

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

    def test_current_approved_brief_versions_pass(self) -> None:
        self.assertEqual(
            validate_brief_version_assertion(fixture("valid-brief-version-assertion.json")),
            [],
        )

    def test_stale_brief_dependency_is_rejected(self) -> None:
        assertion = fixture("valid-brief-version-assertion.json")
        dependencies = assertion.get("dependencies")
        self.assertIsInstance(dependencies, list)
        dependency = dependencies[0] if isinstance(dependencies, list) else None
        self.assertIsInstance(dependency, dict)
        if isinstance(dependency, dict):
            dependency["current_version"] = 3
        self.assertIn("dependency 0 is stale", validate_brief_version_assertion(assertion))

    def test_approved_positive_factual_communication_passes(self) -> None:
        self.assertEqual(validate_communication(fixture("valid-communication.json")), [])

    def test_communication_rejects_unapproved_or_protected_content(self) -> None:
        communication = {
            **fixture("valid-communication.json"),
            "consent_confirmed": False,
            "student_card_id": "card-123",
        }
        errors = validate_communication(communication)
        self.assertIn("consent_confirmed must be true", errors)
        self.assertIn("protected learner data at communication.student_card_id", errors)

    def test_communication_message_must_cite_an_approved_fact(self) -> None:
        communication = fixture("valid-communication.json")
        messages = communication.get("messages")
        self.assertIsInstance(messages, list)
        message = messages[0] if isinstance(messages, list) else None
        self.assertIsInstance(message, dict)
        if isinstance(message, dict):
            message["fact_ids"] = ["fact-not-approved"]
        self.assertIn(
            "message 0 cites an unapproved fact",
            validate_communication(communication),
        )

    def test_artifact_requires_objective_identity(self) -> None:
        errors = validate_artifact({"artifact_id": "a-1", "artifact_type": "worksheet", "audience": "student"})
        self.assertIn("objective_ids must be a non-empty list", errors)

    def test_valid_assessment_bundle_passes(self) -> None:
        self.assertEqual(validate_assessment_bundle(fixture("valid-assessment-bundle.json")), [])

    def test_student_answer_leakage_blocks_bundle(self) -> None:
        errors = validate_assessment_bundle(fixture("leaked-assessment-bundle.json"))
        self.assertTrue(any(error.startswith("student answer leakage at") for error in errors))

    def test_suite_declares_exactly_sixteen_unique_names(self) -> None:
        self.assertEqual(len(ZAMERY_SKILL_NAMES), 16)
        self.assertEqual(len(set(ZAMERY_SKILL_NAMES)), 16)
        self.assertIn("zamery-design-teaching-materials", ZAMERY_SKILL_NAMES)
        self.assertIn("zamery-understand-learners", ZAMERY_SKILL_NAMES)
        self.assertIn("zamery-monitor-english-learning", ZAMERY_SKILL_NAMES)
        self.assertIn("zamery-plan-english-reteaching", ZAMERY_SKILL_NAMES)
        self.assertIn("zamery-design-english-learning-sequences", ZAMERY_SKILL_NAMES)

    def test_every_specialist_declares_direct_version_preflight(self) -> None:
        education_root = ROOT.parent
        specialists = set(ZAMERY_SKILL_NAMES) - {"zamery-teacher-copilot"}
        missing = sorted(
            skill_name
            for skill_name in specialists
            if "../_shared/references/brief-version-contract.md"
            not in (education_root / skill_name / "SKILL.md").read_text(encoding="utf-8")
        )
        self.assertEqual(missing, [])

    def test_student_card_accepts_governed_evidence_and_rejects_prohibited_labels(self) -> None:
        card = fixture("valid-student-card.json")
        self.assertEqual(contracts.validate_student_card(card), [])
        evidence = card.get("learning_evidence")
        self.assertIsInstance(evidence, list)
        first_evidence = evidence[0] if isinstance(evidence, list) else None
        self.assertIsInstance(first_evidence, dict)
        if isinstance(first_evidence, dict):
            first_evidence["observation"] = "lazy and addicted to games"
        errors = contracts.validate_student_card(card)
        self.assertIn("learning evidence 0 contains prohibited learner label lazy", errors)

    def test_student_card_does_not_match_prohibited_labels_inside_ordinary_words(self) -> None:
        card = fixture("valid-student-card.json")
        evidence = card.get("learning_evidence")
        self.assertIsInstance(evidence, list)
        first_evidence = evidence[0] if isinstance(evidence, list) else None
        self.assertIsInstance(first_evidence, dict)
        if isinstance(first_evidence, dict):
            first_evidence["observation"] = (
                "Can follow instructions and showed slow improvement below expectations"
            )
        self.assertEqual(contracts.validate_student_card(card), [])

    def test_learning_trajectory_requires_three_points_for_a_descriptive_trend(self) -> None:
        trajectory = fixture("valid-learning-trajectory.json")
        self.assertEqual(contracts.validate_learning_trajectory(trajectory), [])
        evidence = trajectory.get("objective_evidence")
        self.assertIsInstance(evidence, list)
        trajectory["objective_evidence"] = evidence[:2] if isinstance(evidence, list) else []
        trajectory["trend"] = "improving"
        self.assertIn(
            "descriptive trend requires at least three dated evidence points",
            contracts.validate_learning_trajectory(trajectory),
        )

    def test_learning_trajectory_rejects_unknown_trends(self) -> None:
        trajectory = {**fixture("valid-learning-trajectory.json"), "trend": "banana"}
        self.assertIn(
            "trend must be improving, stable, plateau, regressing, or insufficient",
            contracts.validate_learning_trajectory(trajectory),
        )

    def test_reteaching_plan_preserves_objective_and_requires_reassessment(self) -> None:
        plan = fixture("valid-reteaching-plan.json")
        self.assertEqual(contracts.validate_reteaching_plan(plan), [])
        teacher_action = plan.get("teacher_action")
        self.assertIsInstance(teacher_action, dict)
        if isinstance(teacher_action, dict):
            teacher_action["preserves"] = ["learner_dignity"]
        plan["reassessment"] = None
        errors = contracts.validate_reteaching_plan(plan)
        self.assertIn(
            "teacher action must preserve shared_objective, assessment_construct, and learner_dignity",
            errors,
        )
        self.assertIn("reteaching plan requires a reassessment object", errors)

    def test_learning_sequence_requires_coverage_spacing_and_transfer(self) -> None:
        sequence = fixture("valid-learning-sequence.json")
        self.assertEqual(contracts.validate_learning_sequence(sequence), [])
        sequence["review_schedule"] = []
        sequence["transfer_levels"] = ["near"]
        errors = contracts.validate_learning_sequence(sequence)
        self.assertIn("review_schedule must be a non-empty list", errors)
        self.assertIn("transfer_levels must include near and far", errors)

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
