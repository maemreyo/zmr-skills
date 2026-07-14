import unittest

from scripts.ielts_profile import (
    LISTENING_TASK_FAMILIES,
    READING_TASK_FAMILIES,
    score_objective_section,
    validate_blueprint,
    validate_criterion_feedback,
    validate_ielts_item,
)


VALID_BLUEPRINT = {
    "schema_version": "zamery-ielts-blueprint.v3",
    "profile": "academic",
    "authority_label": "ielts_aligned_practice",
    "full_test": True,
    "sections": {
        "listening": {"parts": 4, "question_count": 40, "minutes": 30},
        "reading": {"parts": 3, "question_count": 40, "minutes": 60},
        "writing": {
            "minutes": 60,
            "tasks": [
                {"task_number": 1, "genre": "visual_description", "minimum_words": 150, "weight": 1},
                {"task_number": 2, "genre": "discursive_essay", "minimum_words": 250, "weight": 2},
            ],
        },
        "speaking": {"parts": [1, 2, 3], "minutes_min": 11, "minutes_max": 14},
    },
}


class IELTSProfileTests(unittest.TestCase):
    def test_official_task_family_sets_are_complete(self) -> None:
        self.assertEqual(len(LISTENING_TASK_FAMILIES), 6)
        self.assertGreaterEqual(len(READING_TASK_FAMILIES), 11)
        self.assertIn("plan_map_diagram_labelling", LISTENING_TASK_FAMILIES)
        self.assertIn("true_false_not_given", READING_TASK_FAMILIES)
        self.assertIn("yes_no_not_given", READING_TASK_FAMILIES)

    def test_full_academic_blueprint_enforces_four_sections(self) -> None:
        self.assertEqual(validate_blueprint(VALID_BLUEPRINT), [])

    def test_official_claim_and_wrong_counts_are_blocked(self) -> None:
        changed = {
            **VALID_BLUEPRINT,
            "authority_label": "official_ielts",
            "sections": {**VALID_BLUEPRINT["sections"], "reading": {"parts": 3, "question_count": 39, "minutes": 60}},
        }
        errors = validate_blueprint(changed)
        self.assertIn("generated material may not claim official IELTS status", errors)
        self.assertIn("full listening and reading sections require 40 questions", errors)

    def test_general_training_task_one_requires_a_letter(self) -> None:
        changed = {
            **VALID_BLUEPRINT,
            "profile": "general_training",
            "sections": {
                **VALID_BLUEPRINT["sections"],
                "writing": {
                    "minutes": 60,
                    "tasks": VALID_BLUEPRINT["sections"]["writing"]["tasks"],
                },
            },
        }
        self.assertIn("General Training Writing Task 1 must be a letter", validate_blueprint(changed))

    def test_completion_item_requires_explicit_word_number_policy(self) -> None:
        item = {
            "section": "listening",
            "task_family": "form_note_table_flowchart_summary_completion",
            "prompt": "Complete the note.",
            "accepted_answers": ["city centre", "city center"],
            "case_sensitive": False,
            "spelling_policy": "declared_variants_only",
        }
        self.assertIn("completion items require max_words or max_numbers", validate_ielts_item(item))
        item["max_words"] = 2
        self.assertEqual(validate_ielts_item(item), [])

    def test_objective_scoring_returns_raw_practice_result_not_official_band(self) -> None:
        report = score_objective_section(
            ["B", "city centre", "False"],
            [
                {"accepted_answers": ["B"], "case_sensitive": False},
                {"accepted_answers": ["city centre", "city center"], "case_sensitive": False},
                {"accepted_answers": ["TRUE"], "case_sensitive": False},
            ],
        )
        self.assertEqual(report["raw_score"], 2)
        self.assertEqual(report["max_score"], 3)
        self.assertIsNone(report["official_band"])
        self.assertEqual(report["label"], "IELTS-aligned practice result")

    def test_criterion_feedback_requires_evidence_before_estimate(self) -> None:
        feedback = {
            "section": "speaking",
            "authority_label": "estimated_practice_feedback",
            "criteria": {
                "fluency_and_coherence": {"evidence": "Maintains a long turn with two pauses.", "next_step": "Use signposting."},
                "lexical_resource": {"evidence": "Uses topic vocabulary with repetition.", "next_step": "Paraphrase key nouns."},
                "grammatical_range_and_accuracy": {"evidence": "Complex clauses are attempted.", "next_step": "Check article use."},
                "pronunciation": {"evidence": "Word stress is usually clear.", "next_step": "Practise sentence stress."},
            },
            "estimated_band_range": [5.5, 6.0],
        }
        self.assertEqual(validate_criterion_feedback(feedback), [])
        feedback["criteria"]["pronunciation"].pop("evidence")
        self.assertIn("criterion pronunciation requires evidence before an estimate", validate_criterion_feedback(feedback))


if __name__ == "__main__":
    unittest.main()
