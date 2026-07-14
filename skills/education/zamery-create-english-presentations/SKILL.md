---
name: zamery-create-english-presentations
description: Use when a teacher asks for English K–12 slides, a deck, PowerPoint, classroom visuals, speaker notes, or presentation-ready adaptation of approved teaching content.
---

# Zamery Create English Presentations

Convert approved teaching content into classroom presentation surfaces without silently redesigning the pedagogy.

## Workflow

1. Recover the approved source, objective IDs, learner band, language, classroom mode, duration, teacher-note needs, and supplied brand assets.
2. Ask for confirmation before any material change to objectives, methodology, content authority, or assessment scope.
3. Plan each slide by purpose and classroom action using `references/slide-pedagogy.md`; do not paste lesson-plan prose onto slides.
4. Build student slides, separate teacher notes, and print fallbacks according to `references/deck-contract.md` and `references/teacher-notes-and-safety.md`.
5. Apply `references/zamery-presentation-contract.md` and the material-design specialist's `classroom-slides-v2` template. Preserve the exact Zamery Core V2 tokens.
6. Validate structured JSON by passing its pathname as the sole argument to `python3 scripts/validate_deck_manifest.py`.
7. Use the Presentations skill to create PPTX, render every slide, inspect legibility and leakage, and repair only affected slides. Re-render after every repair.
8. Reopen the final PPTX bundle, then deliver the PPTX, separate teacher-note surface, and a concise QA result.
