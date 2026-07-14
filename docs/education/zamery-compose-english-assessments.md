Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-compose-english-assessments
```

```bash
npx skills update zamery-compose-english-assessments
```

[Source](https://github.com/mattpocock/skills/tree/main/skills/education/zamery-compose-english-assessments)

## What it does

Compose reproducible, blueprint-exact quizzes, tests, exams, and mocks from approved item banks or content. The defining constraint is that form assembly, student projection, teacher scoring data, and visual composition are kept structurally separate -- the same blueprint can produce multiple parallel forms (A/B/C) with deterministic, balanced allocation. Counts in the blueprint are exact constraints, not guidelines.

## When to reach for it

- **Invocation mode.** Type `/zamery-compose-english-assessments`, or the agent reaches for it automatically when a task fits.
- **Trigger boundary.** Reach for this when you need a blueprint-constrained assessment with exact section counts, difficulty targets, and separate student and teacher surfaces. For generating the item bank itself, use `zamery-build-english-item-banks`. For marking student work, use `zamery-analyze-student-work`.

## Prerequisites

The skill reads from an approved item bank (canonical JSONL or SQLite). The source bank must exist and have been validated before composition. You need `scripts/form_composer.py`, `scripts/validate_assessment_bundle.py`, and optionally `scripts/qti_export.py` in your environment.

## Blueprint-first assembly

Every assessment starts with a `zamery-assessment-blueprint.v3` that locks purpose, objective IDs, grade band, CEFR claim, time, section counts, allowed interactions, difficulty targets, scoring, accommodations, and form IDs. The form composer allocates items disjointly across forms using a deterministic seed. Duplicate IDs across forms are blocked, and mean difficulty must stay inside declared tolerance.

The student projection carries no answer-bearing fields. The teacher AnswerSet is structurally separate but preserves item IDs and versions so scoring data stays aligned. This separation is what makes parallel forms trustworthy -- each form is an independent instrument, not a reshuffled copy with a shared answer key.

When more than one form is composed, the skill produces an equivalence report that verifies counts match and difficulty balance is inside tolerance. If the approved pool is too small for disjoint allocation, the skill blocks rather than silently reusing items.

## It's working if

- Exact section and item counts are met.
- Unique item IDs within each form with stable positive versions.
- Regeneration from the same bank snapshot, blueprint, form IDs, and seed is deterministic.
- No cross-form reuse when the pool supports disjoint allocation.
- Every declared objective is covered.
- Student artifacts contain no answer, rationale, rubric, or distractor-reason fields.

## Where it fits

- **Role.** A composition step between item banks (upstream) and material design or review-publish (downstream).
- **Neighbours.** `zamery-build-english-item-banks` at https://aihero.dev/skills-zamery-build-english-item-banks supplies the item pool. `zamery-design-teaching-materials` at https://aihero.dev/skills-zamery-design-teaching-materials turns the composition into branded print-ready files.
- **The map.** Point to https://aihero.dev/skills-zamery-teacher-copilot.
