# Standalone Education Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and certify sixteen self-contained Zamery Education skill packages that can be uploaded independently without the source monorepo or a sibling `_shared` directory.

**Architecture:** Keep `skills/education/_shared` as the canonical development source. A standard-library Python builder copies each skill into `dist/education-standalone`, vendors the shared runtime inside that skill, rewrites monorepo-only paths and imports, certifies the isolated package, and creates deterministic ZIP archives.

**Tech Stack:** Python 3.9+ standard library, `unittest`, GitHub Actions, ZIP/JSON manifests.

## Global Constraints

- Keep `skills/education/_shared` as the only hand-maintained shared source.
- Generate exactly sixteen promoted `zamery-*` Education skills by default.
- Every generated skill must contain its own `_shared` runtime and references.
- No generated text may import `skills.education._shared` or use `parents[4]` repo-root bootstrapping.
- Every `_shared/...` path in generated text must resolve to an existing target inside the same skill root.
- Runtime packages exclude `tests/`, `evals/`, caches, and shared development fixtures/scripts.
- Python output must compile under Python 3.9+.
- Per-skill and suite ZIP files must be deterministic and pass CRC validation.

---

### Task 1: Add failing standalone-build tests

**Files:**
- Create: `tests/test_build_education_standalone.py`

**Interfaces:**
- Consumes: a synthetic repository matching `skills/education/<skill>` and `skills/education/_shared`.
- Produces: executable behavioral requirements for `build_suite()`, `certify_standalone_skill()`, and deterministic ZIP output.

- [x] Write tests for path rewriting, vendored references, local Python imports, isolated script execution, exact sixteen-skill discovery, nested shared references, dev-file exclusion, package manifests, ZIP CRC, and reproducibility.
- [x] Run `python3 -m unittest discover -s tests -v` and confirm failures occur before implementation.

### Task 2: Implement the standalone builder

**Files:**
- Create: `scripts/build_education_standalone.py`

**Interfaces:**
- Produces: `discover_skill_dirs(Path) -> list[Path]`.
- Produces: `rewrite_python_runtime(str) -> str`.
- Produces: `certify_standalone_skill(Path) -> dict[str, object]`.
- Produces: `build_suite(Path, Path, expected_skill_count=16) -> list[BuildResult]`.

- [x] Copy each skill runtime while excluding development-only directories.
- [x] Vendor `_shared` into every generated skill and create `_shared/__init__.py`.
- [x] Rewrite file-relative shared references according to the location of each source file.
- [x] Rewrite monorepo Python imports to local `_shared` imports and replace repo-root bootstrapping with skill-root bootstrapping.
- [x] Validate frontmatter names, symlink absence, path containment, shared-target existence, forbidden imports, and Python syntax.
- [x] Generate per-skill and suite manifests.
- [x] Generate deterministic ZIPs with fixed metadata and verify CRC.
- [x] Run the complete test suite and confirm all tests pass.

### Task 3: Document distribution and CI usage

**Files:**
- Create: `docs/education/STANDALONE-DISTRIBUTION.md`
- Create: `.github/workflows/education-standalone.yml`

**Interfaces:**
- Consumes: `scripts/build_education_standalone.py`.
- Produces: local build instructions and a downloadable GitHub Actions artifact.

- [x] Document source-versus-distribution boundaries, commands, output layout, upload procedure, and failure conditions.
- [x] Add a Python 3.9 CI job that runs tests, builds all sixteen packages, and uploads the generated directory.

### Task 4: Final verification and delivery

**Files:**
- Create: `zmr-education-standalone.patch` outside the repository checkout for delivery.

**Interfaces:**
- Consumes: all implementation files and test results.
- Produces: one Git patch that can be applied to the `zmr-dev` branch.

- [x] Run `python3 -m unittest discover -s tests -v`.
- [x] Run `python3 -m py_compile scripts/build_education_standalone.py tests/test_build_education_standalone.py`.
- [x] Scan patch files for placeholders and monorepo dependencies introduced into generated output logic.
- [x] Generate a clean Git patch and verify it applies to an empty index representation of the added files.
