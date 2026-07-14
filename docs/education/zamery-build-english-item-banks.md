Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-build-english-item-banks
```

```bash
npx skills update zamery-build-english-item-banks
```

[Source](https://github.com/mattpocock/skills/tree/main/skills/education/zamery-build-english-item-banks)

## What it does

Build reusable, governed collections of atomic assessment or practice items -- 80 to 400+ items in a single run. The defining constraint is that this skill treats the bank as structured curriculum data (JSONL to SQLite to CSV), not as a very long worksheet. Items get stable IDs, versions, source anchors, and explicit deduplication. The bank is the canonical source of truth that downstream skills draw from.

## When to reach for it

- **Invocation mode.** Type `/zamery-build-english-item-banks`, or the agent reaches for it automatically when a task fits.
- **Trigger boundary.** Reach for this when you need reusable items that must be reviewable, versioned, deduplicated, or generated at bulk scale. For a one-off worksheet or homework set, use `zamery-build-english-practice` instead.

## Prerequisites

The skill writes into a workspace it initialises with SQLite and JSONL files. You need the scripts in `scripts/` -- `init_item_bank.py`, `ingest_jsonl.py`, `deduplicate_items.py`, `export_bank.py`, and `validate_item_bank.py` -- available in your environment.

## The bank is data

This skill operates on three storage tiers, each with a distinct job:

- **JSONL** is the portable canonical stream and the model-generation boundary. You generate items as JSONL, never directly into the database.
- **SQLite** is the operational store for versions, batches, resume state, indexes, and QA evidence.
- **CSV** is a teacher review and export projection. Nested values stay as JSON strings in explicit `_json` columns.

QTI and H5P are downstream interchange packages. They are not the authoring database.

Generation happens in 20 to 50 item chunks. The skill never asks a model to produce 400 final items in one undifferentiated response. Each chunk is validated on ingest: records with missing source anchors, answer evidence, invalid interaction data, or mutated content under an existing `(item_id, version)` are rejected.

## It's working if

- Every item has a stable `item_id` and positive integer `version`.
- Same ID/version/content is idempotent; same ID/version with different content is blocked.
- Every item traces to at least one source anchor with authority and locator.
- Batch completion is measured by distinct item IDs and is resumable.
- The final bank matches the blueprint distribution, not just the total count.

## Where it fits

- **Role.** A build-once, refresh-anytime data skill. It is the canonical source of truth for items that downstream skills consume.
- **Neighbours.** `zamery-build-english-practice` for one-off worksheet items (no bank required). `zamery-compose-english-assessments` at https://aihero.dev/skills-zamery-compose-english-assessments to select from the bank and assemble exam forms.
- **The map.** Point to https://aihero.dev/skills-zamery-teacher-copilot.
