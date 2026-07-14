# Canonical item model

`zamery-item.v3` is one atomic, versioned item. The canonical JSON object includes:

| Group | Required fields | Rule |
|---|---|---|
| Identity | `item_id`, `version`, `status` | IDs remain stable; any content change increments version. |
| Audience | `language`, `grade_band`, `cefr` | Grade and CEFR are separate claims. |
| Instruction | `domain`, `skill`, `objective_ids` | Objectives must trace to the bank blueprint. |
| Interaction | `interaction`, `response_mode` | A visual format and a response mode are not the same axis. |
| Demand | `cognitive_operation`, `difficulty` | Difficulty is 0–1 and must be reviewed against evidence. |
| Prompt | `stem`, optional `options`/stimulus fields | The stem is student-visible; answer metadata is not. |
| Scoring | `answer`, `rationale`, optional rubric | Selected responses use stable option IDs. |
| Evidence | `source_anchors` | Each anchor has `source_id`, `authority`, and `locator`. |
| Search | `tags` | Tags supplement rather than replace structured fields. |

An item can have multiple versions, but only the latest approved version is normally exported to a new form. Retired versions remain available for audit.

Never silently edit a stored version. Re-ingesting identical content is safe and counted as `unchanged`; different content under the same key is rejected.
