# Batch generation for 80–400+ items

1. Allocate blueprint cells before drafting. Each cell declares count, objective, interaction, difficulty band, cognitive operation, and source scope.
2. Use deterministic batch IDs and seeds. Recommended chunk size is 20–50.
3. Generate to JSONL, one complete item per line. A failed line must not invalidate other lines.
4. Ingest immediately. Store line-level rejection evidence and correct only rejected records.
5. At every chunk boundary, compare actual counts with remaining blueprint deficits.
6. Run duplicate detection within the new chunk and against the full bank.
7. Resume using the same manifest. Do not regenerate accepted items.
8. Complete only when distinct accepted IDs meet the requested count and distribution gates pass.

For parallel variants, use a `variant_group_id` in extension metadata and require deliberate changes in surface context while preserving the tested construct. Variants are not duplicates merely because they share a construct, but near-identical stems should still be reviewed.
