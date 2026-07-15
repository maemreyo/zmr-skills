# Claim Graph

## Verified claims

- C-01: The nine-file pack is technically valid but not production-ready.
- C-02: Cross-artifact coherence exists at the arc level but is not operationally traceable.
- C-03: Threshold membership/denominators are not deterministically governed.
- C-04: IELTS labeling is cautious, but textbook/item source authority is insufficient.
- C-05: Student safety separation passes; content/metadata correctness does not fully pass.
- C-06: Accessibility/presentation cannot claim a pass without notes, metadata, readable projected type, and QA receipts.
- C-07: The exact request is routed to the wrong primary specialist.
- C-08: Render/content gate enforcement is materially weaker than declared policy.

## Claim nodes

| claim_id | statement | type | risk | intent ids | support | contradiction search | primary backing | status | synthesis location |
|---|---|---|---|---|---|---|---|---|---|
| C-01 | Pack is a valid prototype, not a publishable production pack. | evaluative | high | I-01 | O-01–O-09, O-24–O-29 | Searched for corruption/content loss; none found, but gates still fail. | Local binaries + gate policy | supported | Executive conclusion |
| C-02 | Coherence requires teacher inference because mappings are absent. | causal | high | I-02 | O-10–O-16 | Tested “mutually incompatible” claim; refuted and replaced with missing lineage. | Local artifact text | supported | Confirmed defects 1, 5 |
| C-03 | Decision thresholds lack deterministic item membership. | content | high | I-02 | O-13–O-16 | Reading/grammar may have plausible sets; vocabulary 8/10 remains unmapped. | Local guide/deck/items | supported | Confirmed defect 2 |
| C-04 | IELTS label safety passes but item-level source authority fails. | authority | high | I-03 | O-17–O-20 | Counter-searched official/public source and copyright limits. | Cambridge/IELTS sources + local answer pack | supported | Confirmed defect 1, 6 |
| C-05 | No student PII/answers leak, but a teacher-facing rationale is grammatically wrong. | safety/content | normal | I-04 | O-21–O-23 | Searched hidden OOXML fields and student surfaces. | Local OOXML/text | supported | Confirmed defect 6 |
| C-06 | Accessibility/presentation pass is unproven. | accessibility | high | I-05 | O-24–O-29 | Corrected false claims about headings/header rows and retained confirmed gaps. | Local OOXML/PDF/PPTX + visual QA policy | supported | Accessibility and hygiene |
| C-07 | Current router misclassifies the exact request as IELTS practice. | executable | high | I-06 | O-30 | Executed exact command. | route_advisor.py | supported | Why skills allowed this output |
| C-08 | Render/content enforcement is weaker than skill contracts. | executable | high | I-06 | O-31–O-36 | Executed analyzer/tests and inspected validators. | Local code/tests | supported | Why skills allowed this output |

## Refuted claims

- R-01: Deck source reading and homework transfer reading are necessarily incompatible.
- R-02: D19 answer authority fails to correct `catch to the bus`.
- R-03: Diagnostic prompt tables use equal-width columns.
- R-04: DOCX files have no semantic section headings or table header rows.
