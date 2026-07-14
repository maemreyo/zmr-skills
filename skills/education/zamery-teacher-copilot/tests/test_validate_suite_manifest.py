import json
import unittest
from pathlib import Path

from scripts.validate_suite_manifest import validate_manifest

ROOT = Path(__file__).resolve().parents[1]


class SuiteManifestTests(unittest.TestCase):
    def test_committed_manifest_is_valid(self) -> None:
        data = json.loads((ROOT / "suite-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_manifest(data), [])

    def test_duplicate_intent_owner_is_rejected(self) -> None:
        data = {
            "manifest_version": "zamery-suite.v2",
            "routes": [
                {"intent": "practice", "skill": "a"},
                {"intent": "practice", "skill": "b"},
            ],
        }
        self.assertIn("intent owners must be unique", validate_manifest(data))

    def test_exact_fifteen_specialist_targets_are_required(self) -> None:
        data = {
            "manifest_version": "zamery-suite.v3",
            "routes": [
                {"intent": "design", "skill": "zamery-design-english-learning"}
            ],
        }
        self.assertIn("manifest must declare exactly fifteen specialist targets", validate_manifest(data))

    def test_v3_manifest_contains_new_workflow_boundaries(self) -> None:
        data = json.loads((ROOT / "suite-manifest.json").read_text(encoding="utf-8"))
        routes = {route["intent"]: route["skill"] for route in data["routes"]}
        self.assertEqual(routes["item_bank"], "zamery-build-english-item-banks")
        self.assertEqual(routes["assessment_composition"], "zamery-compose-english-assessments")
        self.assertEqual(routes["ielts_practice"], "zamery-create-ielts-practice")
        self.assertEqual(routes["video_learning"], "zamery-build-video-learning")
        self.assertEqual(routes["understand_learners"], "zamery-understand-learners")
        self.assertEqual(routes["monitor_learning"], "zamery-monitor-english-learning")
        self.assertEqual(routes["reteach"], "zamery-plan-english-reteaching")
        self.assertEqual(routes["sequence_design"], "zamery-design-english-learning-sequences")


if __name__ == "__main__":
    unittest.main()
