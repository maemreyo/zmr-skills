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
        self.assertTrue(any("Ambiguous" in case["note"] for case in cases))

    def test_no_analysis_only_triggers(self) -> None:
        path = Path(__file__).resolve().parents[1] / "evals" / "trigger-eval.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        for case in cases:
            if "Mark" in case["query"] and "rubric" in case["query"]:
                self.assertFalse(case["should_trigger"])

    def test_single_observation_is_ambiguous(self) -> None:
        path = Path(__file__).resolve().parents[1] / "evals" / "trigger-eval.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        single_obs = [c for c in cases if "one student" in c["query"]]
        self.assertTrue(single_obs, "Missing single-observation ambiguous case")


if __name__ == "__main__":
    unittest.main()
