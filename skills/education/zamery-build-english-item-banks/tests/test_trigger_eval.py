import json
import unittest
from pathlib import Path


class TriggerEvalTests(unittest.TestCase):
    def test_eval_has_positive_and_negative_boundaries(self) -> None:
        path = Path(__file__).resolve().parents[1] / "evals" / "trigger-eval.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data), 8)
        self.assertTrue(any(case["should_trigger"] for case in data))
        self.assertTrue(any(not case["should_trigger"] for case in data))
        self.assertTrue(any("400" in case["query"] for case in data))


if __name__ == "__main__":
    unittest.main()
