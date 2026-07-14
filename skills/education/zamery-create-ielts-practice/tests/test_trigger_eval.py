import json
import unittest
from pathlib import Path


class TriggerEvalTests(unittest.TestCase):
    def test_trigger_boundaries_cover_all_sections(self) -> None:
        cases = json.loads((Path(__file__).resolve().parents[1] / "evals" / "trigger-eval.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 10)
        joined = " ".join(case["query"].casefold() for case in cases if case["should_trigger"])
        for section in ("listening", "reading", "writing", "speaking"):
            self.assertIn(section, joined)
        self.assertTrue(any(not case["should_trigger"] for case in cases))


if __name__ == "__main__":
    unittest.main()
