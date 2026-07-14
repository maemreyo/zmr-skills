---
name: zamery-build-english-practice
description: Use when a teacher asks for a one-off English K–12 worksheet, drill, homework set, flashcards, reading passage, guided practice, retrieval, transfer, or differentiated student exercises rather than a graded assessment or reusable 80–400+ item bank.
---

# Zamery Build English Practice

Create student-facing practice, not an authoritative assessment or answer key.

## Workflow

1. Recover the approved objective IDs, learner band, source lesson or concept, language, count, difficulty, and delivery constraints. When no blueprint exists, ask exactly one question only for a material gap.
2. Read `references/exercise-catalog.md`. Choose interaction, response mode, cognitive operation, evidence, scoring, and context independently; variety must change the learning action, not only decoration. For every item, also set the renderer projection `response_type`, `expected_response_lines`, and `layout_intent` so the printable worksheet receives enough writing space.
3. Use `references/practice-progression.md`: worked example, guided, independent, retrieval, and transfer when applicable. A shorter sequence is allowed only under the stated conditions.
4. When variants are requested, follow `references/differentiation.md`; keep the same objective IDs across support, core, and challenge.
5. Build stable item IDs and objective lineage. Keep every student surface free of answers, rubrics, explanations, and wrong-reason metadata as defined in `references/student-artifact-contract.md`.
6. When practice is structured JSON, pass its pathname as the sole argument to `python3 scripts/validate_practice.py` and repair every error.
7. Request DOCX or offline HTML projection only when asked. Route reusable pools, typically 80–400+ items with version/deduplication needs, to `zamery-build-english-item-banks`. Route graded forms/AnswerSets to `zamery-compose-english-assessments`, IELTS profiles to `zamery-create-ielts-practice`, and linked-video work to `zamery-build-video-learning`.
