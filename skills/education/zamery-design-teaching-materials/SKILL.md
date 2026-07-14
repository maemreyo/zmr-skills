---
name: zamery-design-teaching-materials
description: Use when approved English K–12 content needs branded visual composition into a teacher guide, worksheet, long workbook, exam paper, answer sheet/key, administration guide, print-ready DOCX/PDF, offline HTML, or CSV/TSV export, or when existing classroom materials need document UX redesign.
---

# Zamery Design Teaching Materials

Turn approved content into classroom-facing materials that are easy to teach from, complete, and visually intentional. Preserve content authority; this skill owns composition, not pedagogy.

## Workflow

1. Recover the approved brief, content artifacts, objective IDs, audiences, versions, response types, and answer authority. Stop if a material content conflict remains.
2. Read `references/zamery-core-brand.md` and validate `assets/` with `python3 scripts/validate_design_system.py assets`.
3. Choose the closest entry in `assets/artifact-template-registry.csv`. Use the actual files under `assets/templates/`; do not recreate a generic document when a matching template exists.
4. Read the artifact-specific contract: teacher guide, student worksheet, long workbook/exam, answer key, or data-format policy. Map each content unit to a deliberate component from `assets/component-registry.csv`. Use dedicated workbook/exam/answer-sheet/administration templates for long or graded outputs; never stretch the 1–2 page worksheet template to 80–400 items.
5. Allocate student response space from `assets/response-space-registry.csv`. Never give every item the same answer area when response demands differ.
6. Create a `zamery-layout.v2` manifest containing visible text, brand applications, page roles, grids, items, and planned page occupancy. Run `scripts/validate_layout_manifest.py` before rendering.
7. Use the Documents workflow for DOCX, PDF for fixed print output, Spreadsheets for CSV/TSV, and the presentation specialist for PPTX. Preserve the selected template's tokens and structure.
8. Render every page, run `scripts/analyze_rendered_pages.py`, and inspect each image at full size using `references/render-qa.md`. Repair and rerender until clean.
9. Hand the exact files, manifests, and render report to `zamery-review-publish-pack`. The final archive must pass `scripts/verify_delivery_bundle.py` after extraction.

## Hard blocks

- Do not expose original prompts, route plans, snake-case brief fields, manifests, generation commentary, or QA ledgers in classroom-facing files.
- Do not change objectives, pedagogy, question meaning, answer authority, or source versions silently.
- Do not treat a footer tagline as sufficient branding; use the opening block, section accents, and page furniture.
- Do not ship equal-width number/prompt/response columns, undersized response areas, sparse orphan pages, broken numbering, single-row continuation pages, corrupt OOXML, or an untested ZIP.
- Keep student and teacher surfaces structurally separate.

## Output contract

Return the requested classroom files plus an internal layout manifest and render report for final review. Use DOCX/PDF/HTML for designed materials and CSV/TSV only for genuinely tabular banks or registries.
