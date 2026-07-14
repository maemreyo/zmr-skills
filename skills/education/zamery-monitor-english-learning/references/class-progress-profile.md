# ClassProgressProfile data model

The `ClassProgressProfile` is a class-level aggregation of per-learner `LearningTrajectory` records. It answers: which objectives are covered, how fresh is the evidence, and where are the group-level gaps.

## Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `profile_id` | string | yes | Stable ID for this profile |
| `class_id` | string | yes | Class or group identifier |
| `generated_at` | string | yes | ISO 8601 timestamp when the profile was generated |
| `coverage` | list[ObjectiveCoverage] | yes | Per-objective coverage across learners in the class |
| `evidence_freshness` | string | yes | One of `recent` (all objectives reviewed ≤30 days), `aging` (any ≤60 days), `stale` (any >60 days) |
| `group_gaps` | list[string] | no | Description of group-level evidence gaps |

## ObjectiveCoverage

| Field | Type | Required | Description |
|---|---|---|---|
| `objective_id` | string | yes | The stable objective ID |
| `learner_count` | integer | yes | Number of learners with ≥1 evidence point for this objective |
| `latest_observed_at` | string | yes | Most recent evidence date across all learners for this objective |
| `secure_count` | integer | yes | Number of learners at `secure` status |
| `developing_count` | integer | yes | Number of learners at `developing` status |
| `emerging_count` | integer | yes | Number of learners at `emerging` status |
| `not_observed_count` | integer | yes | Number of learners with `not_observed` or no data |

## Rules

- `learner_count` must not exceed the total number of learners in the class.
- The status counts (`secure_count` + `developing_count` + `emerging_count` + `not_observed_count`) must equal `learner_count`.
- `evidence_freshness` is the worst-case across all objectives: if any objective has evidence >60 days old, the class profile is `stale`.
- `group_gaps` lists objectives where fewer than half the learners have at least one evidence point.
- The profile is a snapshot — it does not track changes between generations.
