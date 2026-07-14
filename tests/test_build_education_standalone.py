from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_education_standalone.py"
SPEC = importlib.util.spec_from_file_location("build_education_standalone", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


SHARED_CONTRACTS = """from __future__ import annotations\n\nfrom .learning_contracts import validate_student_card\n"""
SHARED_LEARNING = """from __future__ import annotations\n\ndef validate_student_card(data: dict[str, object]) -> list[str]:\n    return [] if data.get('ok') is True else ['not ok']\n"""
HARD_DEP_SCRIPT = """from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_REPO_ROOT))

from skills.education._shared.contracts import validate_student_card  # noqa: E402


def main() -> int:
    return 0 if validate_student_card({'ok': True}) == [] else 1


if __name__ == '__main__':
    raise SystemExit(main())
"""


class StandaloneEducationBuildTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.education = self.repo / "skills" / "education"
        self.shared = self.education / "_shared"
        (self.shared / "references").mkdir(parents=True)
        (self.shared / "references" / "brief-version-contract.md").write_text(
            "# Brief Version Contract\n", encoding="utf-8"
        )
        (self.shared / "brand-contract.json").write_text("{}\n", encoding="utf-8")
        (self.shared / "contracts.py").write_text(SHARED_CONTRACTS, encoding="utf-8")
        (self.shared / "learning_contracts.py").write_text(SHARED_LEARNING, encoding="utf-8")
        (self.shared / "tests").mkdir()
        (self.shared / "tests" / "must-not-ship.py").write_text("raise AssertionError\n", encoding="utf-8")
        (self.shared / "fixtures").mkdir()
        (self.shared / "fixtures" / "must-not-ship.json").write_text("{}\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _make_skill(self, name: str, *, hard_dependency: bool = False) -> Path:
        skill = self.education / name
        (skill / "agents").mkdir(parents=True)
        (skill / "references").mkdir()
        skill_md = f"""---
name: {name}
description: Synthetic test skill.
---

# {name}

Apply `../_shared/references/brief-version-contract.md` before generation.
"""
        (skill / "SKILL.md").write_text(skill_md, encoding="utf-8")
        (skill / "agents" / "openai.yaml").write_text(
            "policy:\n  products: [chatgpt]\n", encoding="utf-8"
        )
        if hard_dependency:
            (skill / "scripts").mkdir()
            (skill / "scripts" / "validate.py").write_text(HARD_DEP_SCRIPT, encoding="utf-8")
        (skill / "tests").mkdir()
        (skill / "tests" / "must-not-ship.py").write_text("raise AssertionError\n", encoding="utf-8")
        (skill / "evals").mkdir()
        (skill / "evals" / "must-not-ship.json").write_text("{}\n", encoding="utf-8")
        return skill

    def test_rewrites_shared_reference_and_vendors_shared_runtime(self) -> None:
        self._make_skill("zamery-alpha")
        output = self.root / "dist"

        results = builder.build_suite(self.repo, output, expected_skill_count=1)

        self.assertEqual([result.skill_name for result in results], ["zamery-alpha"])
        built = output / "skills" / "zamery-alpha"
        skill_md = (built / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("`_shared/references/brief-version-contract.md`", skill_md)
        self.assertNotIn("../_shared", skill_md)
        self.assertTrue((built / "_shared" / "references" / "brief-version-contract.md").is_file())
        self.assertTrue((built / "_shared" / "contracts.py").is_file())
        self.assertTrue((built / "_shared" / "__init__.py").is_file())
        self.assertFalse((built / "_shared" / "tests").exists())
        self.assertFalse((built / "_shared" / "fixtures").exists())
        self.assertFalse((built / "tests").exists())
        self.assertFalse((built / "evals").exists())

    def test_rewrites_monorepo_package_name_inside_vendored_reference(self) -> None:
        self._make_skill("zamery-reference")
        source_reference = self.shared / "references" / "brief-version-contract.md"
        source_reference.write_text(
            "Apply `validate_brief_version_assertion()` from "
            "`skills.education._shared.contracts`.\n",
            encoding="utf-8",
        )
        output = self.root / "dist"

        builder.build_suite(self.repo, output, expected_skill_count=1)

        built_reference = (
            output
            / "skills"
            / "zamery-reference"
            / "_shared"
            / "references"
            / "brief-version-contract.md"
        )
        content = built_reference.read_text(encoding="utf-8")
        self.assertIn("`_shared.contracts`", content)
        self.assertNotIn("skills.education._shared", content)

    def test_rewrites_monorepo_import_and_script_runs_outside_repo(self) -> None:
        self._make_skill("zamery-hard", hard_dependency=True)
        output = self.root / "dist"
        builder.build_suite(self.repo, output, expected_skill_count=1)
        built = output / "skills" / "zamery-hard"
        script = built / "scripts" / "validate.py"
        content = script.read_text(encoding="utf-8")

        self.assertIn("from _shared.contracts import validate_student_card", content)
        self.assertIn("_SKILL_ROOT = Path(__file__).resolve().parents[1]", content)
        self.assertNotIn("skills.education._shared", content)
        self.assertNotIn("parents[4]", content)

        import subprocess

        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_certification_rejects_external_shared_reference(self) -> None:
        skill = self.root / "zamery-broken"
        (skill / "_shared" / "references").mkdir(parents=True)
        (skill / "_shared" / "__init__.py").write_text("", encoding="utf-8")
        (skill / "SKILL.md").write_text(
            "---\nname: zamery-broken\ndescription: x\n---\n\nRead ../_shared/x.md\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(builder.BuildError, "parent-directory shared dependency"):
            builder.certify_standalone_skill(skill)

    def test_builds_per_skill_and_suite_zips_with_manifests(self) -> None:
        self._make_skill("zamery-alpha")
        self._make_skill("zamery-beta", hard_dependency=True)
        output = self.root / "dist"

        results = builder.build_suite(self.repo, output, expected_skill_count=2)

        self.assertEqual(len(results), 2)
        for result in results:
            self.assertTrue(result.zip_path.is_file())
            with zipfile.ZipFile(result.zip_path) as archive:
                self.assertIsNone(archive.testzip())
                names = set(archive.namelist())
                self.assertIn(f"{result.skill_name}/SKILL.md", names)
                self.assertIn(f"{result.skill_name}/BUILD-MANIFEST.json", names)
        suite_zip = output / "zamery-education-standalone.zip"
        self.assertTrue(suite_zip.is_file())
        with zipfile.ZipFile(suite_zip) as archive:
            names = set(archive.namelist())
            self.assertIn("zamery-alpha/SKILL.md", names)
            self.assertIn("zamery-beta/SKILL.md", names)
        suite_manifest = json.loads((output / "SUITE-MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(suite_manifest["skill_count"], 2)
        self.assertEqual(len(suite_manifest["skills"]), 2)
        self.assertEqual(len(suite_manifest["suite_zip_sha256"]), 64)

    def test_default_contract_builds_exactly_sixteen_skills(self) -> None:
        names = [
            "zamery-teacher-copilot",
            "zamery-understand-learners",
            "zamery-monitor-english-learning",
            "zamery-plan-english-reteaching",
            "zamery-design-english-learning-sequences",
            "zamery-design-english-learning",
            "zamery-teach-english-concepts",
            "zamery-build-english-practice",
            "zamery-build-english-item-banks",
            "zamery-compose-english-assessments",
            "zamery-create-ielts-practice",
            "zamery-build-video-learning",
            "zamery-design-teaching-materials",
            "zamery-create-english-presentations",
            "zamery-analyze-student-work",
            "zamery-review-publish-pack",
        ]
        for index, name in enumerate(names):
            self._make_skill(name, hard_dependency=index < 4)

        output = self.root / "dist"
        results = builder.build_suite(self.repo, output)

        self.assertEqual(len(results), 16)
        self.assertEqual({result.skill_name for result in results}, set(names))
        suite = json.loads((output / "SUITE-MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(suite["skill_count"], 16)

    def test_nested_reference_rewrites_to_existing_internal_shared_file(self) -> None:
        skill = self._make_skill("zamery-nested")
        (skill / "references" / "nested.md").write_text(
            "Read `../../_shared/references/brief-version-contract.md`.\n",
            encoding="utf-8",
        )
        output = self.root / "dist"

        builder.build_suite(self.repo, output, expected_skill_count=1)

        built = output / "skills" / "zamery-nested"
        nested = built / "references" / "nested.md"
        content = nested.read_text(encoding="utf-8")
        self.assertIn("`../_shared/references/brief-version-contract.md`", content)
        self.assertNotIn("../../_shared", content)
        target = (nested.parent / "../_shared/references/brief-version-contract.md").resolve()
        self.assertTrue(target.is_file())

    def test_repeated_builds_are_byte_for_byte_reproducible(self) -> None:
        self._make_skill("zamery-alpha", hard_dependency=True)
        first = self.root / "dist-one"
        second = self.root / "dist-two"

        builder.build_suite(self.repo, first, expected_skill_count=1)

        import time
        time.sleep(2.1)
        builder.build_suite(self.repo, second, expected_skill_count=1)

        self.assertEqual(
            builder._sha256(first / "zips" / "zamery-alpha.zip"),
            builder._sha256(second / "zips" / "zamery-alpha.zip"),
        )
        self.assertEqual(
            builder._sha256(first / "zamery-education-standalone.zip"),
            builder._sha256(second / "zamery-education-standalone.zip"),
        )


if __name__ == "__main__":
    unittest.main()
