# ObjectiveEvidenceSummary data model

The `ObjectiveEvidenceSummary` is a per-objective roll-up of the evidence ledger. It is used for teacher review, progress reporting, and downstream consumption by design, reteaching, and materials skills.

## Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `summary_id` | string | yes | Stable ID for this summary record |
| `objective_id` | string | yes | The stable objective ID |
| `evidence_ids` | list[string] | yes | Ordered list of evidence IDs that support this summary |
| `point_count` | integer | yes | Number of evidence points (must match length of `evidence_ids`) |
| `latest_status` | string | yes | Status of the most recent evidence point: `emerging`, `developing`, `secure`, or `not_observed` |
| `first_observed_at` | string | yes | ISO 8601 date of the first evidence point |
| `latest_observed_at` | string | yes | ISO 8601 date of the most recent evidence point |
| `flags` | list[string] | no | Zero or more of: `plateau`, `regression`, `missing_evidence`, `review_due` |

## Flag detection rules

- **`plateau`**: Last three points have the same `status`.
- **`regression`**: Latest `status` is lower than the status two points before.
- **`missing_evidence`**: More than 30 days since `latest_observed_at` with no new point.
- **`review_due`**: The `review_due_at` date from the parent trajectory has passed.

## Validation

- `point_count` must be ≥ 1 and equal to the length of `evidence_ids`.
- `latest_status` must be one of the defined status values.
- `first_observed_at` must be earlier than or equal to `latest_observed_at`.
- Flags must only contain recognised values; empty flags list means no flags.
