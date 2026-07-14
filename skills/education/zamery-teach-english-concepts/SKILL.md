---
name: zamery-teach-english-concepts
description: Use when a teacher wants to understand or explain an English K–12 vocabulary, grammar, pronunciation, reading, writing, listening, speaking, or language-use concept before turning it into practice, assessment, or slides.
---

# Zamery Teach English Concepts

Teach the concept clearly and memorably. Do not expand into worksheets, assessments, or presentation files unless another specialist is explicitly requested.

## Workflow

1. Recover the learner band, concept, target and instruction language, available time, any teacher-pinned methodology, and the minimum approved ClassProfile or snapshot context. Apply `../_shared/references/brief-version-contract.md` to the approved brief and every source lesson, ClassProfile, snapshot, reteaching plan, and authority dependency; reject stale or unapproved input even when invoked directly.
2. Ask exactly one question only if a missing material value changes the teaching approach. Otherwise continue with a labelled assumption.
3. Read `references/methodology-registry.md`; select the smallest method that fits and give a one-sentence rationale. Preserve a pinned method or surface the conflict before changing it.
4. Build a concept model, prediction, misconception contrast, counterexample, concise board representation, memorable examples, self-explanation or teach-back, comprehension checks, and one transfer prompt. Use `references/english-domain-playbooks.md`, `../_shared/references/english-oral-language-playbook.md`, and `../_shared/references/learning-science-protocols.md` as applicable.
5. For inverse thinking, read `references/inverse-thinking.md`. For a vocabulary board, follow `references/board-plan-contract.md`.
6. When the plan is structured JSON, pass its pathname as the sole argument to `python3 scripts/validate_methodology_plan.py` and repair every error.
7. Return teacher moves, expected learner thinking, board plan, checks, and transfer. Stop at concept teaching.
