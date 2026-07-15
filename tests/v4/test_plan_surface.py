from pathlib import Path


REQUIRED_SURFACES = (
    "pyproject.toml",
    "src/zamery_education_v4/kernel/canonical_json.py",
    "src/zamery_education_v4/kernel/records/migration.py",
    "src/zamery_education_v4/kernel/graph/invariants.py",
    "src/zamery_education_v4/kernel/storage/rebuild.py",
    "src/zamery_education_v4/kernel/approvals/service.py",
    "src/zamery_education_v4/application/request_resolution/resolver.py",
    "src/zamery_education_v4/protocol/manifest.py",
    "src/zamery_education_v4/kernel/execution/runner.py",
    "src/zamery_education_v4/kernel/execution/output_validation.py",
    "src/zamery_education_v4/application/run_planning/planner.py",
    "src/zamery_education_v4/kernel/execution/scheduler.py",
    "src/zamery_education_v4/application/impact_analysis/service.py",
    "capabilities/reference/python_echo/main.py",
    "capabilities/reference/node_echo/main.mjs",
    "src/zamery_education_v4/cli/app.py",
    "src/zamery_education_v4/kernel/evidence/registry.py",
    "src/zamery_education_v4/kernel/gates/engine.py",
    "capabilities/verification/source_lineage/main.py",
    "adapters/docx/inspect/main.py",
    "adapters/pptx/inspect/main.py",
    "adapters/pdf/inspect/main.py",
    "capabilities/verification/privacy_homework/main.py",
    "src/zamery_education_v4/application/repair_planning/service.py",
    "src/zamery_education_v4/application/publication/verify.py",
    "src/zamery_education_v4/kernel/migrations/registry.py",
    "migrations/v4/teaching_brief_v3_to_v4.py",
    "goldens/v4/unit1-lesson1/negative/route-misclassification.json",
    "goldens/v4/unit1-lesson1/production/manifest.json",
    "goldens/v4/item-bank-300/manifest.json",
    "src/zamery_education_v4/application/comparison/service.py",
    "src/zamery_education_v4/kernel/observability/redaction.py",
    "security/v4/runtime-digests.yaml",
    ".github/workflows/education-v4-release.yml",
    "scripts/v4/run_determinism_replay.py",
    "docs/operations/education-v4/operator-guide.md",
    "src/zamery_education_v4/application/cutover/service.py",
    "scripts/v4/archive_v3_inventory.py",
)


def test_all_38_task_surfaces_are_present() -> None:
    missing = [path for path in REQUIRED_SURFACES if not Path(path).is_file()]
    assert not missing
