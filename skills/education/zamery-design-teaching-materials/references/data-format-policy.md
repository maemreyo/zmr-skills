# Data Format Policy

Use CSV or TSV for flat, repeated records such as question banks, vocabulary banks, scores, and registries. Use UTF-8, RFC 4180 quoting, stable header order, unique IDs, and no formulas unless explicitly requested. Reopen the export and verify delimiter, headers, and row count.

Use JSONL for portable canonical item streams and JSON for nested design tokens, manifests, dependencies, render reports, and delivery metadata. Use SQLite once work needs resumable batches, stable versions, deduplication, relational source anchors, or governed reuse—even at 80–400 items. CSV remains a teacher review projection; nested cells use explicit JSON and never pipe-delimited options. Use Markdown for guidance and DOCX/PDF/PPTX/offline HTML for classroom-facing artifacts. QTI and H5P are delivery exports, not authoring databases.
