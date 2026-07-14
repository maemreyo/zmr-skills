import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_design_system import validate_design_system

ROOT = Path(__file__).resolve().parents[1]


class DesignSystemTests(unittest.TestCase):
    def test_committed_design_system_is_valid(self) -> None:
        self.assertEqual(validate_design_system(ROOT / "assets"), [])

    def test_missing_required_color_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "assets"
            shutil.copytree(ROOT / "assets", copied)
            token_path = copied / "design-tokens.json"
            data = json.loads(token_path.read_text(encoding="utf-8"))
            del data["palette"]["root_terracotta"]
            token_path.write_text(json.dumps(data), encoding="utf-8")
            self.assertIn("palette must exactly match Zamery Core V2", validate_design_system(copied))

    def test_duplicate_registry_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "assets"
            shutil.copytree(ROOT / "assets", copied)
            registry = copied / "response-space-registry.csv"
            lines = registry.read_text(encoding="utf-8").splitlines()
            registry.write_text("\n".join([*lines, lines[1]]) + "\n", encoding="utf-8")
            self.assertIn(
                "response-space-registry.csv has duplicate primary key selected_response",
                validate_design_system(copied),
            )


if __name__ == "__main__":
    unittest.main()
