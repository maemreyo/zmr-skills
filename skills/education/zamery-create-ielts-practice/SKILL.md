---
name: zamery-create-ielts-practice
description: Use when a teacher asks for IELTS Academic or General Training aligned Listening, Reading, Writing, or Speaking practice; an IELTS-style mock; official task-family constraints; completion word/number rules; criterion-based Writing or Speaking feedback; or safely labeled practice scoring. Do not claim generated materials are official IELTS, infer definitive official bands, or use this profile for ordinary K–12 English work.
---

# Zamery Create IELTS Practice

Apply an explicit IELTS profile to English-learning content. Preserve official format distinctions while labeling all generated work as practice or mock material.

## Workflow

1. Confirm Academic or General Training, target section(s), full mock or partial practice, learner goal, time, source material, and desired output. Apply `../_shared/references/brief-version-contract.md` to the approved brief and every source, profile, exemplar, and authority dependency; reject stale or unapproved input even when invoked directly.
2. Build `zamery-ielts-blueprint.v3` using `references/ielts-profile.md`.
3. Use only task families valid for that section. Read `references/listening-reading-task-families.md`.
4. For completion items, store `max_words`, `max_numbers`, accepted alternatives, case sensitivity, and spelling policy as data fields.
5. For Writing and Speaking, gather observable evidence under all four criteria before giving any estimated range. Use benchmarked exemplars and teacher rater calibration; read `references/writing-speaking-feedback.md`.
6. Validate blueprints, objective items, and criterion feedback with `scripts/ielts_profile.py`.
7. Export teacher-approved criterion evidence to `zamery-monitor-english-learning`. Route reusable items, mock forms, and visual files to their existing owners.

## Non-negotiable labeling

- Allowed: “IELTS-aligned practice”, “IELTS-aligned mock”, “estimated practice feedback”, “practice raw score”.
- Blocked: “official IELTS”, “official band”, “equivalent to a live test”, or any guaranteed score prediction.
- Listening/Reading award one mark per correct answer. Report raw score. Do not hard-code one raw-to-band table across test versions or across Academic and General Training Reading.
- Writing/Speaking estimates follow criterion evidence and remain explicitly provisional.

## Quality gates

- Full Listening and Reading each have 40 questions; partial practice declares `full_test: false`.
- Academic and General Training share Listening/Speaking but use distinct Reading/Writing profiles.
- Academic Writing Task 1 is visual description; General Training Task 1 is a letter; Task 2 is a 250-word discursive essay weighted twice Task 1.
- Speaking includes Parts 1, 2, and 3 with correct long-turn and timing expectations.
- Completion answer policies are machine-readable, not hidden only in instructions.
- Generated materials cite their source/authority and remain within supplied or authorized content.
