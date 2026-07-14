import unittest

from scripts.validate_deck_manifest import validate_deck_manifest


VALID = {
    "deck_id": "deck-1",
    "design_system": "zamery-core.v2",
    "template_id": "classroom-slides-v2",
    "reopened_after_export": True,
    "grade_band": "grades_6_8",
    "objective_ids": ["obj-1"],
    "brand": {"name": "zamery", "tagline": "rooted in strength", "primary_family": "Arial", "palette": {"ink_navy": "#17324D", "root_terracotta": "#B85435", "growth_teal": "#2B746F", "warm_sand": "#F4EEE4", "sky_mist": "#DCEAF2", "charcoal": "#202B33", "paper_white": "#FFFFFF"}},
    "slides": [
        {
            "slide_id": "s1",
            "objective_ids": ["obj-1"],
            "surface": "student",
            "blocks": [{"type": "heading", "text": "Past or present?"}],
        },
        {
            "slide_id": "s2",
            "objective_ids": ["obj-1"],
            "surface": "student",
            "blocks": [{"type": "prompt", "text": "What clue shows finished time?"}],
        },
    ],
    "teacher_notes": [
        {"slide_id": "s1", "notes": "Elicit yesterday before explaining the rule."},
        {"slide_id": "s2", "notes": "Accept any correct finished-time marker."},
    ],
}


class DeckManifestTests(unittest.TestCase):
    def test_valid_manifest_passes(self) -> None:
        self.assertEqual(validate_deck_manifest(VALID), [])

    def test_teacher_notes_cannot_appear_in_student_slides(self) -> None:
        slide = {**VALID["slides"][0], "teacher_notes": "The answer is past simple."}
        changed = {**VALID, "slides": [slide, VALID["slides"][1]]}
        self.assertTrue(any(error.startswith("teacher-only data at") for error in validate_deck_manifest(changed)))

    def test_slide_ids_must_be_unique(self) -> None:
        changed = {**VALID, "slides": [VALID["slides"][0], VALID["slides"][0]]}
        self.assertIn("slide IDs must be unique", validate_deck_manifest(changed))

    def test_notes_must_reference_known_slides(self) -> None:
        changed = {**VALID, "teacher_notes": [{"slide_id": "missing", "notes": "x"}]}
        self.assertIn("teacher notes reference unknown slide missing", validate_deck_manifest(changed))

    def test_exact_v2_palette_is_required(self) -> None:
        changed = {**VALID, "brand": {**VALID["brand"], "palette": {**VALID["brand"]["palette"], "ink_navy": "#000000"}}}
        self.assertIn("brand palette must match Zamery Core V2", validate_deck_manifest(changed))

    def test_export_must_be_reopened(self) -> None:
        changed = {**VALID, "reopened_after_export": False}
        self.assertIn("final PPTX must be reopened after export", validate_deck_manifest(changed))

    def test_every_declared_objective_must_appear_on_a_slide(self) -> None:
        changed = {**VALID, "objective_ids": ["obj-1", "obj-2"]}
        self.assertIn("objective obj-2 is not covered by any slide", validate_deck_manifest(changed))


if __name__ == "__main__":
    unittest.main()
