---
name: zamery-build-english-item-banks
description: Use when a teacher needs a reusable English K–12 question or item bank, especially 80–400+ items, semester pools, parallel variants, resumable bulk generation, deduplication, version control, source grounding, or JSONL/SQLite/CSV bank exports. Do not use for a one-off worksheet, composing an exam from an existing bank, marking student work, or visual document layout.
---

# Zamery Build English Item Banks

Build governed collections of atomic assessment or practice items. Treat the bank as structured curriculum data, not as a very long worksheet.

## Boundary

- Use `zamery-build-english-practice` for a one-off worksheet or homework set.
- Use this skill when items must be reusable, reviewable, versioned, deduplicated, or generated at bulk scale.
- Hand approved items to `zamery-compose-english-assessments` for exam forms.
- Hand selected items to `zamery-design-teaching-materials` for branded workbook composition.
- Hand the completed bank to `zamery-review-publish-pack` for final certification.

## Required workflow

1. Define the bank blueprint before drafting any item. Apply `../_shared/references/brief-version-contract.md` to the approved brief and every curriculum, source, blueprint, and authority dependency; reject stale or unapproved input even when invoked directly. Record grade band and CEFR independently; objective IDs; target counts by domain, skill, interaction, difficulty, cognitive operation, misconception family, and source; exclusions; seed; and batch size.
2. Choose 20–50 item chunks. Never ask a model to produce 400 final items in one undifferentiated response.
3. Create the SQLite operational store with `scripts/init_item_bank.py`.
4. Generate each chunk as canonical `zamery-item.v3` JSONL. Use `assets/canonical-item.schema.json` and `references/canonical-item-model.md`.
5. Ingest each chunk with `scripts/ingest_jsonl.py`. Resume with the same batch ID, requested count, chunk size, and seed.
6. Reject records with missing source anchors, answer evidence, invalid interaction data, or mutated content under an existing `(item_id, version)`.
7. Run `scripts/deduplicate_items.py`. Review exact and near pairs; never auto-delete.
8. Export canonical JSONL and a UTF-8 CSV review view with `scripts/export_bank.py`.
9. Run `scripts/validate_item_bank.py` before handoff.

## Storage decision

- JSONL is the portable canonical stream and model-generation boundary.
- SQLite is the operational store for versions, batches, resume state, indexes, and QA evidence.
- CSV is a teacher review/export projection. Nested values remain JSON strings in explicit `_json` columns; never encode options with pipes.
- QTI and H5P are downstream interchange packages, never the authoring database.

Read `references/storage-policy.md` before choosing or changing formats.

## Quality gates

- Every item has stable `item_id` and positive integer `version`.
- Same ID/version/content is idempotent; same ID/version/different content is blocked.
- Every item has at least one source anchor with authority and locator.
- Objective, domain, skill, interaction, response mode, cognitive operation, and difficulty are independent fields.
- Choice keys point to declared option IDs; teacher answers never leak into student projections.
- Exact and near duplicates are reported with scores.
- Batch completion is measured by distinct item IDs and is resumable.
- The final bank matches the blueprint distribution, not only the total count.
- The bank records validity, bias/DIF review, exposure/security, and oral-language evidence metadata from `../_shared/references/accessibility-assessment-ai-safety.md` and `../_shared/references/english-oral-language-playbook.md`.
- Reusable banks never encode an individual StudentCard, ClassProfile, behaviour observation, or learner label.

## References

- `references/canonical-item-model.md` — field semantics and version rules.
- `references/batch-generation.md` — 80–400+ generation loop and resume behavior.
- `references/question-taxonomy.md` — independent axes and classroom patterns.
- `references/lifecycle-and-qa.md` — statuses, review gates, deduplication, exposure.
- `references/storage-policy.md` — JSONL/SQLite/CSV responsibilities.
