import unittest

from scripts.validate_methodology_plan import validate_methodology_plan


class MethodologyPlanTests(unittest.TestCase):
    def test_valid_inverse_thinking_plan_passes(self) -> None:
        plan = {
            "requested_methodology": "inverse_thinking",
            "selected_methodology": "inverse_thinking",
            "pinned": True,
            "rationale": "The distinctions are easiest to learn from typical failures.",
            "stages": ["disaster", "clues", "safe_zone", "rule", "transfer"],
        }
        self.assertEqual(validate_methodology_plan(plan), [])

    def test_pinned_methodology_cannot_change(self) -> None:
        plan = {
            "requested_methodology": "inverse_thinking",
            "selected_methodology": "active_recall",
            "pinned": True,
            "rationale": "Changed silently.",
            "stages": [],
        }
        self.assertIn("pinned methodology changed", validate_methodology_plan(plan))

    def test_inverse_thinking_requires_exact_stage_order(self) -> None:
        plan = {
            "requested_methodology": "inverse_thinking",
            "selected_methodology": "inverse_thinking",
            "pinned": False,
            "rationale": "Misconception-driven lesson.",
            "stages": ["rule", "practice"],
        }
        self.assertIn("inverse thinking stages are incomplete or out of order", validate_methodology_plan(plan))

    def test_vocabulary_board_requires_five_columns(self) -> None:
        plan = {
            "requested_methodology": None,
            "selected_methodology": "semantic_anchoring",
            "pinned": False,
            "rationale": "Meaning needs a memorable anchor.",
            "board_columns": ["word", "meaning"],
        }
        self.assertIn("vocabulary board columns are incomplete", validate_methodology_plan(plan))

    def test_unknown_methodology_is_rejected(self) -> None:
        plan = {
            "requested_methodology": None,
            "selected_methodology": "generic_fun_activity",
            "pinned": False,
            "rationale": "It sounds engaging.",
            "stages": [],
        }
        self.assertIn("selected_methodology is not approved", validate_methodology_plan(plan))


if __name__ == "__main__":
    unittest.main()
