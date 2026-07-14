import unittest

from scripts.impact_diff import impact_diff


BEFORE = {
    "topic": "Past tenses",
    "grade_band": "grades_9_12",
    "cefr": None,
    "methodology": "inverse_thinking",
    "duration_minutes": 45,
    "artifact_types": ["lesson", "worksheet", "quiz", "slide_deck"],
    "must_include": "time markers",
}


class ImpactDiffTests(unittest.TestCase):
    def test_copy_edit_is_non_material(self) -> None:
        result = impact_diff(BEFORE, {**BEFORE, "must_include": "clear time markers"})
        self.assertFalse(result["requires_confirmation"])

    def test_methodology_change_is_material_and_fans_out(self) -> None:
        result = impact_diff(BEFORE, {**BEFORE, "methodology": "active_recall"})
        self.assertTrue(result["requires_confirmation"])
        self.assertEqual(
            result["affected_intents"],
            [
                "concept_teaching",
                "practice",
                "item_bank",
                "assessment_composition",
                "ielts_practice",
                "video_learning",
                "material_design",
                "presentation",
                "review_publish",
            ],
        )

    def test_copy_edit_to_layout_field_routes_to_material_design(self) -> None:
        result = impact_diff(BEFORE, {**BEFORE, "layout_style": "more response space"})
        self.assertFalse(result["requires_confirmation"])
        self.assertEqual(result["affected_intents"], ["material_design"])

    def test_artifact_scope_change_is_material(self) -> None:
        result = impact_diff(BEFORE, {**BEFORE, "artifact_types": ["lesson", "worksheet"]})
        self.assertTrue(result["requires_confirmation"])
        self.assertIn("review_publish", result["affected_intents"])

    def test_item_count_change_reaches_bank_exam_and_layout(self) -> None:
        before = {**BEFORE, "item_count": 80}
        result = impact_diff(before, {**before, "item_count": 400})
        self.assertTrue(result["requires_confirmation"])
        self.assertEqual(
            result["affected_intents"],
            ["practice", "item_bank", "assessment_composition", "ielts_practice", "video_learning", "material_design", "review_publish"],
        )

    def test_approved_snapshot_change_reaches_learner_sensitive_routes(self) -> None:
        before = {**BEFORE, "learner_context_snapshot_id": "snapshot-1"}
        result = impact_diff(before, {**before, "learner_context_snapshot_id": "snapshot-2"})
        self.assertTrue(result["requires_confirmation"])
        self.assertEqual(
            result["affected_intents"],
            ["design", "concept_teaching", "practice", "video_learning", "reteach"],
        )

    def test_learning_sequence_change_reaches_dependent_design_and_assessment(self) -> None:
        before = {**BEFORE, "learning_sequence_id": "sequence-1"}
        result = impact_diff(before, {**before, "learning_sequence_id": "sequence-2"})
        self.assertTrue(result["requires_confirmation"])
        self.assertEqual(
            result["affected_intents"],
            ["sequence_design", "design", "item_bank", "assessment_composition", "review_publish"],
        )


if __name__ == "__main__":
    unittest.main()
