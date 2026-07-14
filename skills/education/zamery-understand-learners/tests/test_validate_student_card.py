"""Tests for scripts/validate_student_card.py — validates StudentCard contract."""

import json
import unittest
from pathlib import Path

from scripts.validate_student_card import validate_student_card, get_validator

VALID_CARD: dict[str, object] = {
    "schema_version": "zamery-student-card.v1",
    "card_id": "student-local-001",
    "owner": "teacher-or-school",
    "purpose": "instructional_support",
    "consent": {"school_authority": True, "field_scope_ids": ["scope-learning"]},
    "lifecycle": {
        "created_at": "2026-07-14",
        "reviewed_at": "2026-07-14",
        "next_review_at": "2026-08-14",
        "delete_at": "2027-07-14",
    },
    "student_voice": {"goals": ["Explain tense choices clearly"], "interests": ["space exploration"]},
    "learning_evidence": [
        {
            "evidence_id": "ev-1",
            "objective_id": "obj-1",
            "observation": "Selected the finished-time form in four of five items",
            "source": "assessment",
            "authority": "teacher_reviewed",
            "observed_at": "2026-07-14",
            "context": "five-item tense diagnostic",
            "evidence_reference": "assessment-2026-07-14:item-1-5",
            "confidence": "high",
            "counterevidence": [],
            "expires_at": "2026-09-14",
            "reviewed_by": "teacher-local-01",
            "review_status": "approved",
            "consent_scope_id": "scope-learning",
            "dispute_status": "undisputed",
        }
    ],
    "learning_conditions": {"observations": [], "strategies_tried": []},
    "interests_and_routines": {
        "interest_tags": ["space exploration"],
        "reported_schedule_conflicts": [],
    },
    "authorised_support": [],
    "disputes": [],
    "provenance": {
        "learning_evidence": {
            "source": "assessment",
            "authority": "teacher_reviewed",
            "date": "2026-07-14",
            "confidence": "high",
            "expiry": "2026-09-14",
        }
    },
}


def _shared_fixture(name: str) -> dict[str, object]:
    path = Path(__file__).resolve().parents[2] / "_shared" / "fixtures" / name
    return json.loads(path.read_text(encoding="utf-8"))


class StudentCardValidationTests(unittest.TestCase):
    def test_valid_card_passes(self) -> None:
        self.assertEqual(validate_student_card(VALID_CARD), [])

    def test_shared_fixture_passes(self) -> None:
        card = _shared_fixture("valid-student-card.json")
        self.assertEqual(validate_student_card(card), [])

    def test_prohibited_label_in_evidence_observation_is_rejected(self) -> None:
        card = {**VALID_CARD, "learning_evidence": [{**VALID_CARD["learning_evidence"][0]}]}  # type: ignore[index]
        card["learning_evidence"][0]["observation"] = "lazy and addicted to games"
        errors = validate_student_card(card)
        self.assertIn(
            "learning evidence 0 contains prohibited learner label lazy",
            errors,
        )
        self.assertIn(
            "learning evidence 0 contains prohibited learner label addicted",
            errors,
        )

    def test_prohibited_label_anywhere_in_card_is_rejected(self) -> None:
        card = {**VALID_CARD, "student_voice": "this student is lazy and unmotivated"}  # type: ignore[dict-item]
        errors = validate_student_card(card)
        self.assertIn(
            "student_card.student_voice contains prohibited learner label lazy",
            errors,
        )
        self.assertIn(
            "student_card.student_voice contains prohibited learner label unmotivated",
            errors,
        )

    def test_missing_schema_version_is_rejected(self) -> None:
        card = {**VALID_CARD, "schema_version": "wrong"}  # type: ignore[dict-item]
        self.assertIn(
            "schema_version must be zamery-student-card.v1",
            validate_student_card(card),
        )

    def test_missing_card_id_is_rejected(self) -> None:
        card = {**VALID_CARD, "card_id": ""}  # type: ignore[dict-item]
        self.assertIn("card_id must be a non-empty string", validate_student_card(card))

    def test_missing_lifecycle_fields_are_rejected(self) -> None:
        card = {**VALID_CARD, "lifecycle": {"reviewed_at": ""}}  # type: ignore[dict-item]
        errors = validate_student_card(card)
        self.assertIn("lifecycle.created_at must be a non-empty string", errors)
        self.assertIn("lifecycle.reviewed_at must be a non-empty string", errors)
        self.assertIn("lifecycle.next_review_at must be a non-empty string", errors)
        self.assertIn("lifecycle.delete_at must be a non-empty string", errors)

    def test_missing_evidence_fields_are_rejected(self) -> None:
        card = {**VALID_CARD, "learning_evidence": [{"observation": "ok"}]}  # type: ignore[dict-item]
        errors = validate_student_card(card)
        self.assertIn(
            "learning_evidence 0.evidence_id must be a non-empty string",
            errors,
        )
        self.assertIn("learning_evidence 0.source must be a non-empty string", errors)

    def test_get_validator_returns_callable(self) -> None:
        fn = get_validator()
        self.assertTrue(callable(fn))

    def test_missing_consent_is_rejected(self) -> None:
        card = {**VALID_CARD, "consent": None}  # type: ignore[dict-item]
        self.assertIn("consent must be an object", validate_student_card(card))

    def test_terms_that_are_not_prohibited_pass(self) -> None:
        card = {
            **VALID_CARD,
            "learning_evidence": [{**VALID_CARD["learning_evidence"][0]}],  # type: ignore[index]
        }
        card["learning_evidence"][0]["observation"] = (
            "The learner can follow instructions and showed slow but steady improvement below grade expectations"
        )
        self.assertEqual(validate_student_card(card), [])

    def test_governance_sections_and_evidence_metadata_are_required(self) -> None:
        evidence = {**VALID_CARD["learning_evidence"][0]}  # type: ignore[index]
        del evidence["consent_scope_id"]
        card = {
            **VALID_CARD,
            "owner": "",
            "learning_conditions": None,
            "interests_and_routines": None,
            "provenance": {},
            "learning_evidence": [evidence],
        }
        errors = validate_student_card(card)
        self.assertIn("owner must be teacher-or-school", errors)
        self.assertIn("learning_conditions must be an object", errors)
        self.assertIn("interests_and_routines must be an object", errors)
        self.assertIn("provenance must be a non-empty object", errors)
        self.assertIn(
            "learning_evidence 0.consent_scope_id must be a non-empty string",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
