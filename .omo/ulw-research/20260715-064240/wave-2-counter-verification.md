# Wave 2 — Counter-verification

## Executed checks

- Router returned `ielts_practice` for the exact coursebook lesson request.
- `analyze_rendered_pages.py` crashed on a real rendered page with `AttributeError`.
- Material tests: 22 passed, 2 failed; both failures come from the broken page analyzer.
- All OOXML archives passed CRC and contained `[Content_Types].xml`.
- All PDFs opened, exposed text, and matched their DOCX token sets.
- All 14 slide canvases contained every shape; no out-of-bounds geometry.
- All 14 notes surfaces contained no text.
- All four DOCX files had empty title/language metadata.
- No brief/blueprint/manifest/gate/render/README artifacts existed in the output directory.
- OOXML geometry confirmed diagnostic tables at 7.4/57.4/35.3 and semantic repeat-header rows.

## Refuted or narrowed claims

- **Refuted:** source deck and generated reading are automatically incompatible. They can be core+transfer; lineage is missing.
- **Refuted:** D19 ignores the preposition error. `catch + noun` plus the repaired answer addresses it.
- **Refuted:** diagnostic main tables are equal width or violate the layout grid.
- **Refuted:** all DOCX headings/header rows are nonsemantic.
- **Narrowed:** denominator mismatch is proven for vocabulary `8/10`; grammar/reading denominators may refer to combined/source sets but are not deterministically mapped.

## Convergence

No unchecked artifact or code-enforcement lead remains. The missing Real-Life Homework file is explicitly scoped as teacher-supplied evidence only.
