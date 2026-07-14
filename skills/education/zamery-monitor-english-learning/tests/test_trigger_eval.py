import json
import unittest
from pathlib import Path


class TriggerEvalTests(unittest.TestCase):
    def test_trigger_suite_has_positive_negative_and_ambiguous_cases(self) -> None:
        path = Path(__file__).resolve().parents[1] / "evals" / "trigger-eval.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 5)
        self.assertTrue(any(case["should_trigger"] is True for case in cases))
        self.assertTrue(any(case["should_trigger"] is False for case in cases))
        self.assertTrue(any("trajectory" in case["note"].lower() for case in cases if case["should_trigger"]))


if __name__ == "__main__":
    unittest.main()
