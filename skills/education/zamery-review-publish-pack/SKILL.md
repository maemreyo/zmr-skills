---
name: zamery-review-publish-pack
description: Use when a teacher asks to check, finalize, print, package, export, or publish existing English K–12 teaching materials or a complete teaching pack.
---

# Zamery Review and Publish Pack

Review first, then render only supported deliverables that pass every applicable hard gate.

## Workflow

1. Inventory each artifact's ID, type, audience, version, objective IDs, source, dependencies, and requested format. Recover the approved Teaching Brief and apply `../_shared/references/brief-version-contract.md` to it and every artifact, source, manifest, and authority dependency; reject stale or unapproved input even when invoked directly.
2. Build the pack manifest from `references/pack-manifest-contract.md`; record PII, answer leakage, StudentCard leakage, prohibited learner labels, and unsupported claims in `safety_findings`.
3. Apply Brief, Pedagogy, Content, Safety, Accessibility, Presentation, and Pack gates in that order using `references/seven-quality-gates.md` and `../_shared/references/accessibility-assessment-ai-safety.md`. Apply `../_shared/references/communication-contract.md` to every learner progress report, family update, and student goal review.
4. Repair non-material copy, layout, and accessibility failures within the affected artifact. Present the exact impact and request confirmation before material pedagogical, objective, source, or assessment changes.
5. Use `references/delivery-formats.md` to invoke the applicable Documents, Presentations, PDF, Spreadsheets, QTI, H5P, JSONL, or SQLite workflow. Never fake an unsupported exporter.
6. Render and inspect DOCX, PDF, and PPTX according to `references/visual-qa.md`. Validate JSONL/SQLite/QTI/H5P with `scripts/validate_structured_exports.py`. Build the final ZIP, verify its CRC and nested OOXML, re-extract it, reopen/rerender classroom files, and revalidate extracted structured exports before setting evidence flags true.
7. Verify descriptor-level CEFR alignment for every CEFR claim or require a non-certified alignment label. Deliver separate student and teacher files, exact approved versions, a gate report, and explicit limitations.

## Non-negotiable blocks

- Stop before rendering when PII, student answer leakage, StudentCard leakage, prohibited labels, unsupported claims, unknown objective lineage, stale dependencies, or unsupported formats remain.
- Do not silently change material pedagogy, objectives, assessment authority, or source meaning.
- Preserve Zamery Core V2 exactly; do not add a pictorial logo or substitute brand tokens.
- Do not claim a file passed visual QA until it was rendered, inspected, repaired as needed, and reopened.

## Output contract

Return:

- gate results with evidence and affected artifact IDs;
- scoped repairs and their impact;
- separate student and teacher deliverables;
- supported files: DOCX, PDF, PPTX, offline HTML, TSV, CSV, canonical JSONL, SQLite item banks, IMS QTI packages, and host-resolved H5P content packages;
- explicit alternatives when GIFT, Anki `.apkg`, generated audio, or generated video is requested.
