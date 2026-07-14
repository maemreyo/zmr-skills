---
name: zamery-create-english-presentations
description: Use when a teacher asks for English K–12 slides, a deck, PowerPoint, classroom visuals, speaker notes, or presentation-ready adaptation of approved teaching content.
---

# Zamery Create English Presentations

Convert approved teaching content into classroom presentation surfaces without silently redesigning the pedagogy.

## Workflow

1. Recover the approved source, objective IDs, learner band, language, classroom mode, duration, teacher-note needs, and supplied brand assets. Apply `../_shared/references/brief-version-contract.md` to the approved brief and every source, template, brand, and authority dependency; reject stale or unapproved input even when invoked directly.
2. Ask for confirmation before any material change to objectives, methodology, content authority, or assessment scope.
3. Plan each slide by purpose and classroom action using `references/slide-pedagogy.md`; do not paste lesson-plan prose onto slides.
4. Build student slides, separate teacher notes, and print fallbacks according to `references/deck-contract.md`, `references/teacher-notes-and-safety.md`, and `../_shared/references/accessibility-assessment-ai-safety.md`.
5. Apply `references/zamery-presentation-contract.md` and the material-design specialist's `classroom-slides-v2` template. Preserve the exact Zamery Core V2 tokens.
6. Validate structured JSON by passing its pathname as the sole argument to `python3 scripts/validate_deck_manifest.py`.
7. Render every slide and inspect accessibility, cognitive load, classroom participation, CJK text, legibility, and leakage. Never place named learner cues or protected profile data on projected surfaces.
8. Reopen the final PPTX bundle, then deliver the PPTX, separate teacher-note surface, and a concise QA result.
