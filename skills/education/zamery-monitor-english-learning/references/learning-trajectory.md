# LearningTrajectory data model

The `LearningTrajectory` is the per-objective longitudinal evidence record. It is a time-series, not a profile. No predictive or behavioural data is stored here.

## Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | Must be `zamery-learning-trajectory.v1` |
| `trajectory_id` | string | yes | Stable ID for this trajectory record |
| `card_id` | string | yes | StudentCard or pseudonym ID the trajectory belongs to; used for protected-store linking only |
| `objective_id` | string | yes | The stable objective ID this trajectory tracks |
| `objective_evidence` | list[EvidencePoint] | yes | Ordered list (by `observed_at`) of evidence points; at least one required |
| `trend` | string | yes | One of `improving`, `stable`, `plateau`, `regressing`, `insufficient`. Must have ≥3 points for any trend other than `insufficient` |
| `review_due_at` | string | yes | ISO 8601 date by which new evidence should be reviewed |

## EvidencePoint

| Field | Type | Required | Description |
|---|---|---|---|
| `evidence_id` | string | yes | Stable ID linking to the source evidence record |
| `observed_at` | string | yes | ISO 8601 date the evidence was collected |
| `status` | string | yes | One of `emerging`, `developing`, `secure`, `not_observed` |
| `authority` | string | yes | Must be `teacher_reviewed` — every evidence point must be teacher-reviewed before it enters the trajectory |

## Rules

- `trend` is `insufficient` when fewer than three evidence points exist. A descriptive trend label requires at least three dated points.
- `review_due_at` must be a date after the most recent `observed_at`.
- All evidence points must share the same `objective_id` as the parent trajectory.
- Evidence points are ordered by `observed_at`; no two points may share the same `evidence_id`.
- The `authority` field protects against unreviewed automated scoring — only `teacher_reviewed` is accepted.

## Trend semantics

| Trend | Meaning | Min points |
|---|---|---|
| `improving` | Most recent status is higher (closer to `secure`) than the first; no recent regression | 3 |
| `stable` | Status is consistent across points within one level | 3 |
| `plateau` | Status has not changed across the last three points | 3 |
| `regressing` | Most recent status is lower than earlier points | 3 |
| `insufficient` | Not enough data to compute a trend | 0–2 |

These are descriptive labels only. They do not predict future performance or recommend interventions.
