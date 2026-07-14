---
name: zamery-design-english-learning
description: Use when a teacher asks to plan, structure, sequence, or redesign an English K–12 lesson or unit before creating worksheets, assessments, slides, or a full teaching pack.
---

# Zamery Design English Learning

Design the instructional blueprint; do not generate finished worksheets, assessments, or slides unless another installed specialist is explicitly in scope.

## Workflow

1. Recover prior context and attachments before asking anything.
2. Build the Teaching Brief using `references/teaching-brief.md`. Mark each captured value `explicit`, `inferred`, `defaulted`, or `unresolved`.
3. Ask exactly one question only when an unresolved material field would change objectives, grade/CEFR adaptation, methodology, assessment scope, language, duration, or artifact scope. Continue with a labelled assumption for non-material gaps.
4. Keep school grade and CEFR independent. Read `references/grade-cefr.md`; leave CEFR unset unless supplied or independently assessed.
5. For current, niche, factual, curriculum, or source-sensitive claims, research primary sources and record them with authority. Surface conflicts; do not claim certified curriculum alignment without a governed reference pack.
6. Create stable objective IDs, observable success evidence, prerequisite and misconception notes, timed phases, methodology with rationale, differentiation, assessment plan, and recommended downstream artifacts.
7. Preserve a teacher-pinned methodology. If it conflicts with the objective, explain the conflict and request confirmation before changing it.
8. Check the structure against `references/blueprint-contract.md`. When you materialize blueprint JSON, pass its pathname as the sole argument to `python3 scripts/validate_blueprint.py` and repair every reported error.
9. Return the blueprint and a short list of unresolved decisions. Stop at the blueprint boundary.
