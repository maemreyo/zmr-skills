# Observation Manifest

| observation_id | source path or URL | evidence layer | observer group | independence basis | observer | observed_at | valid_at / claim_valid_at | artifact path | quote or line anchor | contamination notes |
|---|---|---|---|---|---|---|---|---|---|---|
| O-01 | docs/output/.../classroom-deck...pptx | binary | direct-audit | OOXML extraction | Sisyphus | 2026-07-15 | commit 78f1b83 | artifact-extract.json | 14 slides, valid OOXML | none |
| O-02 | docs/output/.../diagnostic...docx/pdf | binary | direct-audit | OOXML + PDF parity | Sisyphus | 2026-07-15 | commit 78f1b83 | layout-metrics.json | no DOCX tokens missing in PDF | none |
| O-03 | docs/output/.../practice-homework...docx/pdf | binary | direct-audit | OOXML + PDF parity | Sisyphus | 2026-07-15 | commit 78f1b83 | layout-metrics.json | no DOCX tokens missing in PDF | none |
| O-04 | docs/output/.../teacher-guide...docx/pdf | binary | direct-audit | OOXML + PDF parity | Sisyphus | 2026-07-15 | commit 78f1b83 | layout-metrics.json | valid pair | none |
| O-05 | docs/output/.../answer-observation...docx/pdf | binary | direct-audit | OOXML + PDF parity | Sisyphus | 2026-07-15 | commit 78f1b83 | layout-metrics.json | valid pair | none |
| O-10 | classroom deck slide 7 | content | direct-audit | PPTX text extraction | Sisyphus | 2026-07-15 | commit 78f1b83 | artifact-extract.json | Ava/Michael/Nina + Unit 1 pages 3–4 | source/core set |
| O-11 | workbook P06–P10 | content | direct-audit | DOCX extraction | Sisyphus | 2026-07-15 | commit 78f1b83 | artifact-extract.json | Linh/Mateo/Sara | generated transfer candidate |
| O-12 | output directory | governance | direct-audit | filesystem inventory | Sisyphus | 2026-07-15 | commit 78f1b83 | command output | no brief/blueprint/manifest/gate/render/README | none |
| O-13 | teacher guide | content | direct-audit | DOCX/PDF text | Sisyphus | 2026-07-15 | commit 78f1b83 | teacher guide lines 44–58 | 8/10, 5/7, 8/10 | membership absent |
| O-17 | answer pack | authority | direct-audit | DOCX/PDF text | Sisyphus | 2026-07-15 | commit 78f1b83 | answer pack line 5 | vague combined source label | none |
| O-21 | student OOXML | safety | direct-audit | hidden-field scan | Sisyphus | 2026-07-15 | commit 78f1b83 | artifact-extract.json | no leak fields/StudentCard/IELTS/CEFR | none |
| O-22 | answer pack P03 | content | two independent extractions | DOCX and PDF text | Sisyphus | 2026-07-15 | commit 78f1b83 | PDF line 72 | “They takes the base form.” | none |
| O-24 | all DOCX files | accessibility | direct-audit | python-docx metadata/styles | Sisyphus | 2026-07-15 | commit 78f1b83 | layout-metrics.json | empty title/language; Heading 1 present | corrects worker claim |
| O-25 | diagnostic tables | accessibility/layout | direct-audit | OOXML geometry/header flags | Sisyphus | 2026-07-15 | commit 78f1b83 | layout-metrics.json | 7.4/57.4/35.3; repeat headers true | refutes equal-width claim |
| O-26 | PPTX | accessibility | direct-audit | python-pptx geometry/fonts/notes | Sisyphus | 2026-07-15 | commit 78f1b83 | layout-metrics.json | no bounds overflow; no title placeholders; empty notes | none |
| O-27 | all 14 PDF pages | presentation | direct-audit | corrected pixel occupancy algorithm | Sisyphus | 2026-07-15 | commit 78f1b83 | command output | 7.2–15.4% occupied (<25%) | analyzer metric is crude |
| O-30 | route advisor | executable | direct-audit | real command | Sisyphus | 2026-07-15 | commit 78f1b83 | command output | exact request → ielts_practice | none |
| O-31 | analyze_rendered_pages.py | executable | direct-audit | real script execution | Sisyphus | 2026-07-15 | commit 78f1b83 | traceback | get_flattened_data AttributeError | none |
| O-32 | material tests | executable | direct-audit | pytest | Sisyphus | 2026-07-15 | commit 78f1b83 | 22 pass, 2 fail | both analyzer failures | none |
