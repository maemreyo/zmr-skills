import json
import unittest
from pathlib import Path


class TriggerEvalTests(unittest.TestCase):
    def test_trigger_eval_covers_youtube_transcript_and_h5p(self) -> None:
        cases = json.loads((Path(__file__).resolve().parents[1] / "evals" / "trigger-eval.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 10)
        positive = " ".join(case["query"].casefold() for case in cases if case["should_trigger"])
        for term in ("youtube", "transcript", "h5p"):
            self.assertIn(term, positive)
        self.assertTrue(any(not case["should_trigger"] for case in cases))


if __name__ == "__main__":
    unittest.main()
