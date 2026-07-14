# Storage policy

| Format | Role | Why |
|---|---|---|
| JSONL | Canonical portable stream | One recoverable record per line; model- and diff-friendly. |
| SQLite | Operational database | Transactions, versions, indexes, batches, resume state, integrity checks. |
| CSV | Teacher review projection | Easy filtering and comments; nested values use JSON cells. |
| QTI | Assessment interchange export | LMS delivery; generated from an approved form. |
| H5P | Interactive learning export | Media/formative delivery; generated from a verified lesson. |

Use CSV alone only for a disposable flat list. Once the work needs reuse, stable versions, many-to-many source anchors, batch state, or 80–400 governed items, create SQLite plus canonical JSONL.
