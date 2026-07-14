# Reteaching Plan — schema layout

A reteaching plan is a JSON object conforming to `zamery-reteaching-plan.v1`. Each plan is scoped to a single objective and records the evidence, the hypothesised misconception, the six-phase loop specification, and the teacher action agreement.

## Required fields

| Field | Type | Description |
|---|---|---|
| `schema_version` | `"zamery-reteaching-plan.v1"` | Fixed literal. |
| `plan_id` | string | Unique plan identifier within the skill scope. |
| `objective_ids` | `[string]` | The objective(s) targeted. Typically one; a second only when the error spans a boundary. |
| `evidence_ids` | `[string]` | References to the evidence records in the student card or analysis output that justify this plan. |
| `misconception` | object | See below. |
| `phases` | `[string]` | Ordered list of phase names from the six-phase loop. Must be a subsequence of `["reconnect_prerequisite", "contrast", "guided_discrimination", "corrective_rehearsal", "transfer", "reassessment"]`. |
| `teacher_action` | object | The Teacher Action Plan — see `teacher-action-plan.md`. |
| `reassessment` | object | See below. |

## Misconception object

| Field | Type | Description |
|---|---|---|
| `statement` | string | One-sentence description of the hypothesised misconception. |
| `confidence` | `"low" | "medium" | "high"` | How confident the evidence makes this hypothesis. |
| `competing_explanations` | `[string]` | Exactly one alternative explanation for the same evidence. May be empty only when `confidence` is `"high"`. |

## Phase entry in the plan

Each phase that is not skipped may include:

| Field | Type | Description |
|---|---|---|
| `phase_name` | string | One of the six canonical names. |
| `owner_skill` | string | The skill that executes this phase. |
| `completion_criterion` | string | Observable outcome that ends the phase. |
| `skip_reason` | string | Present only when the phase is skipped; explains why evidence justified skipping. |

Phases may be recorded as a flat list in `phases` or as an annotated list of objects depending on the level of detail the teacher requests. The minimal valid plan records just the phase name strings.

## Reassessment object

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `objective_ids` | `[string]` | yes | — | Which objectives to reassess. |
| `success_evidence` | string | yes | — | Observable outcome that proves the reteaching held. |
| `item_count` | integer | no | `5` | Minimum items for a reliable signal. |
| `wait_days` | integer | no | `2` | Days after the last transfer session before reassessment. Range 0–7. |
| `auto_schedule` | boolean | no | `true` | Whether the reassessment fires automatically or waits for teacher trigger. |

## Provisional plans

When a plan is created without meeting the evidence-sufficiency bar, set `provisional: true` at the top level and include a `rationale` field that states the specific evidence gap. Provisional plans must not be executed automatically; they require teacher review before any phase begins.
