import re
import unittest
from pathlib import Path


class TaxonomyReferenceTests(unittest.TestCase):
    def test_catalog_has_independent_axes_and_at_least_28_patterns(self) -> None:
        text = (Path(__file__).resolve().parents[1] / "references" / "exercise-catalog.md").read_text(encoding="utf-8")
        for axis in ("Interaction", "Response mode", "Cognitive operation", "Evidence", "Scoring", "Context"):
            self.assertIn(axis, text)
        patterns = re.findall(r"^\| P\d{2} ", text, flags=re.MULTILINE)
        self.assertGreaterEqual(len(patterns), 28)
