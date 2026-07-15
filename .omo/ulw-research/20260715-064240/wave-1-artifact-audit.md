# Wave 1 — Artifact Audit Digest

## Coverage

- Teacher semantic audit: all four teacher files.
- Student semantic audit: all five student files.
- Visual lane: worker stalled; direct render and teacher-supplied visual review replaced it.

## High-value observations

- All nine files are valid and readable.
- DOCX/PDF pairs are semantically faithful.
- PPTX is the strongest visual artifact but all notes are empty.
- Student practice has no answer leakage.
- Teacher guide and answer pack do not preserve deterministic source/item lineage.
- Visible answer-key error: `They takes the base form.`

## Counterevidence requiring expansion

- Worker claim: PPTX/source reading and generated homework reading are mutually incompatible.
- Worker claim: D19 omits the `catch to` error.
- Worker claim: diagnostic tables violate number/prompt/response ratios.
- Worker claim: DOCX headings/table headers are not semantic.

## EXPAND

- Check whether the two reading sets are core+transfer rather than contradictory.
- Inspect D19 clue semantics.
- Extract OOXML table geometry and header-row tags.
- Inspect paragraph styles, metadata, notes, and slide bounds.
