import unittest
from pathlib import Path

from scripts.validate_layout_manifest import validate_layout_manifest

ROOT = Path(__file__).resolve().parents[1]

VALID = {
    "layout_version": "zamery-layout.v2",
    "artifact_id": "worksheet-1",
    "artifact_type": "worksheet",
    "audience": "student",
    "page_roles": ["practice", "transfer", "exit"],
    "visible_text": ["Notice the clue", "Explain your choice"],
    "brand": {
        "system_id": "zamery-core.v2",
        "applications": ["opening_block", "section_accents", "page_furniture"],
    },
    "grids": [
        {"component_id": "prompt_response_grid", "column_ratios": [0.08, 0.55, 0.37]}
    ],
    "items": [
        {
            "item_id": "q1",
            "response_type": "selected_response",
            "expected_response_lines": 1,
            "response_height_mm": 8,
        },
        {
            "item_id": "q2",
            "response_type": "explanation",
            "expected_response_lines": 4,
            "response_height_mm": 28,
        },
    ],
    "pages": [
        {"role": "practice", "occupied_ratio": 0.62, "intentional_sparse": False},
        {"role": "transfer", "occupied_ratio": 0.55, "intentional_sparse": False},
        {"role": "exit", "occupied_ratio": 0.42, "intentional_sparse": False},
    ],
}


class LayoutManifestTests(unittest.TestCase):
    def validate(self, data: dict[str, object]) -> list[str]:
        return validate_layout_manifest(data, ROOT / "assets")

    def test_valid_layout_passes(self) -> None:
        self.assertEqual(self.validate(VALID), [])

    def test_equal_width_prompt_grid_is_rejected(self) -> None:
        changed = {**VALID, "grids": [{"component_id": "prompt_response_grid", "column_ratios": [1 / 3, 1 / 3, 1 / 3]}]}
        self.assertIn("prompt_response_grid number rail must not exceed 8%", self.validate(changed))

    def test_internal_metadata_and_footer_only_branding_are_rejected(self) -> None:
        changed = {
            **VALID,
            "visible_text": ["Route plan", "review_publish"],
            "brand": {"system_id": "zamery-core.v2", "applications": ["footer_text"]},
        }
        errors = self.validate(changed)
        self.assertIn("visible content contains forbidden internal term route plan", errors)
        self.assertIn("brand must be applied beyond footer text", errors)

    def test_response_space_below_registry_minimum_is_rejected(self) -> None:
        item = {**VALID["items"][1], "response_height_mm": 10}
        changed = {**VALID, "items": [VALID["items"][0], item]}
        self.assertIn("item q2 response height 10.0mm is below explanation minimum 28.0mm", self.validate(changed))

    def test_sparse_orphan_page_is_rejected(self) -> None:
        pages = [*VALID["pages"][:2], {"role": "exit", "occupied_ratio": 0.08, "intentional_sparse": False}]
        changed = {**VALID, "pages": pages}
        self.assertIn("page 2 is unintentionally sparse at 8% occupancy", self.validate(changed))


if __name__ == "__main__":
    unittest.main()
