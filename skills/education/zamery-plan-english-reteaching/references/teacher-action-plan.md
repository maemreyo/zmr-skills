# Teacher Action Plan

The Teacher Action Plan is the `teacher_action` field in the reteaching plan. It records what the teacher has agreed to and what constraints the plan operates under.

## Required fields

| Field | Type | Description |
|---|---|---|
| `action_id` | string | Stable identifier for this teacher-approved teaching experiment. |
| `based_on_snapshot_id` | string | Approved Learner Context Snapshot that supplied the minimum context. |
| `snapshot_expires_at` | string | Date after which the plan must not execute without renewed context. |
| `target` | string | Named objective or observed barrier the move addresses. |
| `evidence_ids` | `[string]` | Dated evidence records supporting the move. |
| `proposed_move` | string | The smallest corrective move selected (from the rank in SKILL.md). One of: `exemplar_contrast`, `guided_discrimination`, `corrective_rehearsal`, `reteach_concept`, `remediate_prerequisite`. |
| `rationale` | string | Why this reversible move might help, stated as a hypothesis. |
| `preserves` | `[string]` | What the reteaching must not compromise. Always includes at minimum `["shared_objective", "assessment_construct"]`. Must also include `"learner_dignity"`. |
| `trial_window` | string | Human-readable one-to-three-session trial window. |
| `teacher_approval` | boolean | Whether the teacher has reviewed and accepted the plan. `true` means the plan is ready for downstream execution. |
| `trial_sessions` | integer | How many consecutive sessions the plan runs before the teacher reviews progress. Default `2`, range `1`–`5`. |
| `expected_signal` | string | Observable evidence that would support the hypothesis. |
| `result` | string | One of `not-yet-tried`, `helped`, `mixed`, or `did-not-help`. |
| `confounding_factors` | `[string]` | Teacher-reviewed context that could affect interpretation. |
| `review_date` | string | Date the teacher reviews the result. |

## Preserves field — what must not be compromised

The `preserves` array enumerates the design constraints the reteaching plan must respect:

| Value | Meaning |
|---|---|
| `shared_objective` | The reteaching targets the same objective originally assessed — it does not change the goal. |
| `assessment_construct` | The reassessment uses the same construct definition as the original assessment. A same-construct item may differ in surface features (vocabulary, context) but must demand the same cognitive operation. |
| `learner_dignity` | The reteaching must not label, sort, or compare learners, and must not repeat the student's error back in a way that humiliates or mocks. This is a hard constraint. |

## Optional fields

| Field | Type | Description |
|---|---|---|
| `teacher_notes` | string | Free-text notes from the teacher that constrain the plan — scheduling preferences, known student circumstances, or specific examples to use or avoid. |
| `session_duration_minutes` | integer | How long each trial session should last. Default `20`. |
| `grouping` | `"individual" | "small_group" | "whole_class"` | Whether the reteaching is delivered individually, in a small group, or to the whole class. Default `"individual"`. |
| `teacher_interpretation` | string or null | Optional attribution recorded as teacher interpretation, never as learner fact. |
