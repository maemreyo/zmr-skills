---
name: zamery-review-publish-pack
description: Use when a teacher asks to check, finalize, print, package, export, or publish existing English K–12 teaching materials or a complete teaching pack.
---

# Zamery Review and Publish Pack

Review first, then render only supported deliverables that pass every applicable hard gate.

## Workflow

1. Inventory each artifact's ID, type, audience, version, objective IDs, source, dependencies, and requested format. Recover the approved Teaching Brief.
2. Build the pack manifest from `references/pack-manifest-contract.md`; record detected PII and answer leakage in `safety_findings`. Pass the manifest pathname as the sole argument to `python3 scripts/validate_pack_manifest.py`.
3. Apply Brief, Pedagogy, Content, Safety, Presentation, and Pack gates in that order using `references/six-quality-gates.md`. Hard failures block rendering.
4. Repair non-material copy, layout, and accessibility failures within the affected artifact. Present the exact impact and request confirmation before material pedagogical, objective, source, or assessment changes.
5. Use `references/delivery-formats.md` to invoke the applicable Documents, Presentations, PDF, Spreadsheets, QTI, H5P, JSONL, or SQLite workflow. Never fake an unsupported exporter.
6. Render and inspect DOCX, PDF, and PPTX according to `references/visual-qa.md`. Validate JSONL/SQLite/QTI/H5P with `scripts/validate_structured_exports.py`. Build the final ZIP, verify its CRC and nested OOXML, re-extract it, reopen/rerender classroom files, and revalidate extracted structured exports before setting evidence flags true.
7. Deliver separate student and teacher files, exact approved artifact versions, a concise gate report, and explicit unsupported-capability notes.

## Non-negotiable blocks

- Stop before rendering when PII, student answer leakage, unknown objective lineage, stale dependencies, or unsupported requested formats remain.
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
