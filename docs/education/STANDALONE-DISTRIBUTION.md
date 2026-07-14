# Standalone Education Skill Distribution

The development tree keeps one canonical shared implementation at:

```text
skills/education/_shared/
```

Do not upload a source skill directory directly. Source skills intentionally reference the canonical shared tree so contracts and teaching protocols are maintained once.

Use the standalone builder to create uploadable packages:

```bash
python3 scripts/build_education_standalone.py
```

Python 3.9 or newer is sufficient. The builder uses only the standard library.

## Output

```text
dist/education-standalone/
├── skills/
│   ├── zamery-teacher-copilot/
│   ├── zamery-understand-learners/
│   └── ... fourteen more standalone skills
├── zips/
│   ├── zamery-teacher-copilot.zip
│   ├── zamery-understand-learners.zip
│   └── ... fourteen more per-skill archives
├── SUITE-MANIFEST.json
└── zamery-education-standalone.zip
```

Each generated skill includes its own:

- `SKILL.md`;
- `agents/openai.yaml` when present in source;
- local references, scripts, and assets;
- `_shared/` contract and teaching-protocol runtime;
- `BUILD-MANIFEST.json` with source revision and certification evidence.

The suite ZIP contains sixteen sibling skill directories. For an individual ChatGPT Skills upload, use the corresponding file from `dist/education-standalone/zips/`.

## What the builder changes

The builder works only in `dist/`; it does not mutate source skills.

It converts source references such as:

```text
../_shared/references/brief-version-contract.md
```

into a path that resolves to the vendored `_shared` directory inside the generated skill.

It converts Python imports such as:

```python
from skills.education._shared.contracts import validate_student_card
```

into skill-local imports:

```python
from _shared.contracts import validate_student_card
```

Scripts that previously searched four parents upward for the repository root receive a local skill-root bootstrap instead.

## Runtime package policy

Generated upload packages exclude:

- `tests/`;
- `evals/`;
- Python caches;
- `_shared/fixtures/`;
- `_shared/scripts/`;
- `_shared/tests/`.

These files remain in the repository for development and CI. They are not needed for ChatGPT skill execution.

## Certification gates

The build fails if:

- the Education tree does not contain exactly sixteen promoted skills;
- a folder name differs from its `SKILL.md` frontmatter name;
- a generated package contains a symlink;
- a shared path resolves outside the generated skill or points to a missing file;
- a generated Python file still imports `skills.education._shared`;
- a generated script still contains the old `parents[4]` bootstrap;
- Python compilation fails;
- ZIP CRC verification fails.

Archives use stable ordering, timestamps, and Unix mode metadata. Identical source revisions therefore produce identical archive hashes.

## Commands

Run the unit tests:

```bash
python3 -m unittest discover -s tests -v
```

Build to a custom location:

```bash
python3 scripts/build_education_standalone.py \
  --output /tmp/zamery-education-standalone
```

Temporarily disable the exact-count gate for a development fixture:

```bash
python3 scripts/build_education_standalone.py \
  --expected-skill-count 0
```

Production and CI builds should keep the default count of sixteen.
