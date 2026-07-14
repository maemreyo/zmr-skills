import unittest

from scripts.validate_practice import validate_practice


VALID = {
    "artifact_id": "worksheet-1",
    "artifact_type": "worksheet",
    "audience": "student",
    "objective_ids": ["obj-1"],
    "progression": ["worked_example", "guided", "independent", "retrieval", "transfer"],
    "items": [
        {"item_id": "i1", "objective_ids": ["obj-1"], "prompt": "Complete the sentence.", "response_type": "short_answer", "expected_response_lines": 2, "layout_intent": "prompt_with_ruled_response"},
        {"item_id": "i2", "objective_ids": ["obj-1"], "prompt": "Use the form in a new context.", "response_type": "two_sentence_transfer", "expected_response_lines": 5, "layout_intent": "full_width_transfer"},
    ],
}


class PracticeValidatorTests(unittest.TestCase):
    def test_valid_practice_passes(self) -> None:
        self.assertEqual(validate_practice(VALID), [])

    def test_answer_fields_are_blocked_recursively(self) -> None:
        changed = {**VALID, "items": [{**VALID["items"][0], "correct_answer": "went"}]}
        self.assertTrue(any(error.startswith("student answer leakage at") for error in validate_practice(changed)))

    def test_item_objectives_must_be_declared(self) -> None:
        changed = {**VALID, "items": [{**VALID["items"][0], "objective_ids": ["obj-unknown"]}]}
        self.assertIn("item i1 cites unknown objective obj-unknown", validate_practice(changed))

    def test_item_ids_must_be_unique(self) -> None:
        changed = {**VALID, "items": [VALID["items"][0], VALID["items"][0]]}
        self.assertIn("item IDs must be unique", validate_practice(changed))

    def test_progression_requires_guided_and_independent_practice(self) -> None:
        changed = {**VALID, "progression": ["retrieval"]}
        self.assertIn("progression requires guided and independent practice", validate_practice(changed))

    def test_every_declared_objective_must_be_practiced(self) -> None:
        changed = {**VALID, "objective_ids": ["obj-1", "obj-2"]}
        self.assertIn("objective obj-2 is not covered by any item", validate_practice(changed))

    def test_response_layout_metadata_is_required(self) -> None:
        item = {key: value for key, value in VALID["items"][0].items() if key != "layout_intent"}
        changed = {**VALID, "items": [item, VALID["items"][1]]}
        self.assertIn("item i1 requires layout_intent", validate_practice(changed))

    def test_response_space_must_match_response_type(self) -> None:
        item = {**VALID["items"][1], "expected_response_lines": 2}
        changed = {**VALID, "items": [VALID["items"][0], item]}
        self.assertIn("item i2 requires at least 5 response lines for two_sentence_transfer", validate_practice(changed))

    def test_v3_practice_requires_independent_taxonomy_axes(self) -> None:
        items = [
            {
                **item,
                "interaction": "ordering" if index == 0 else "extended_response",
                "response_mode": "selected" if index == 0 else "constructed",
                "cognitive_operation": "apply" if index == 0 else "create",
            }
            for index, item in enumerate(VALID["items"])
        ]
        changed = {**VALID, "schema_version": "zamery-practice.v3", "items": items}
        self.assertEqual(validate_practice(changed), [])
        items[0]["interaction"] = "decorative_spinner"
        self.assertIn("item i1 has unsupported interaction", validate_practice(changed))


if __name__ == "__main__":
    unittest.main()
