---
name: zamery-compose-english-assessments
description: Use when a teacher needs an English K–12 quiz, test, exam, mock exam, exit ticket, parallel Forms A/B/C, blueprint-constrained selection from an approved item bank, answer sheet/key, rubric, administration guide, form-equivalence report, or QTI export. Do not use to generate an 80–400+ reusable bank, mark submitted student work, or visually lay out final DOCX/PDF files.
---

# Zamery Compose English Assessments

Compose reproducible, blueprint-exact assessments from approved content or an approved item bank. Keep form assembly, student projection, teacher scoring data, and visual composition separate.

## Boundary

- Route reusable bulk generation and deduplication to `zamery-build-english-item-banks`.
- This skill selects approved item versions, assembles forms, produces aligned answer data, and exports QTI.
- Route IELTS-specific mocks or task families through `zamery-create-ielts-practice` before composition.
- Route branded exam paper, answer sheet, key, and administration guide layout to `zamery-design-teaching-materials`.
- Route actual student responses to `zamery-analyze-student-work`.

## Workflow

1. Lock purpose, objective IDs, grade band, CEFR claim and provenance, source authority, time, section counts, allowed interactions, difficulty targets, scoring, accommodations, form IDs, and seed.
2. Create `zamery-assessment-blueprint.v3` using `references/blueprint-and-form-contract.md`. Counts are exact constraints.
3. If selecting from a bank, accept canonical JSONL or SQLite. Use only the latest approved version of each stable item ID.
4. Run `scripts/form_composer.py` to allocate disjoint forms. The algorithm is deterministic by seed and balances difficulty across forms.
5. Review the equivalence report. Counts must match; duplicate IDs are blocked; mean difficulty must remain inside the declared tolerance.
6. Create a student projection with no answer-bearing fields and a structurally separate teacher AnswerSet. Preserve item IDs and versions in both.
7. Validate any legacy student/teacher JSON projection with `scripts/validate_assessment_bundle.py`.
8. Optionally export a composed form with `scripts/qti_export.py`. QTI is an interchange package, not the canonical bank.
9. Hand the approved composition to the material-design skill for branded files, then to review/publish for certification.

## Required deliverables

- assessment blueprint;
- immutable form manifest for every form;
- equivalence report when more than one form exists;
- student paper or LMS projection;
- separate teacher AnswerSet and scoring/rubric data;
- optional answer sheet and administration notes;
- optional IMS QTI 2.2 package plus validation report.

## Quality gates

- Exact section and item counts.
- Unique item IDs within each form and stable positive versions.
- Deterministic regeneration from bank snapshot, blueprint, form IDs, and seed.
- No cross-form reuse when the approved pool supports disjoint allocation; insufficient pools are blocked rather than silently reused.
- Every declared objective is covered.
- Choice options are distinct after Unicode normalization and keys point to valid options.
- Constructed and spoken responses use accepted evidence or rubrics, not fake multiple-choice semantics.
- Student artifacts contain no answer, rationale, rubric, or distractor-reason fields.
- QTI packages pass CRC, XML, manifest, test-reference, and item-count checks.

Read `references/item-quality.md`, `references/difficulty-and-rubrics.md`, `references/blueprint-and-form-contract.md`, `references/assessment-contract.md`, and `references/answer-set-contract.md` as applicable.
