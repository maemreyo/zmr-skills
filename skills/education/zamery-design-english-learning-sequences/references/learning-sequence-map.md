# LearningSequenceMap

The LearningSequenceMap is the structured plan for a long-horizon English K–12 learning journey — typically a **course** or **term** spanning multiple weeks, not a single lesson/unit. It declares how a set of objectives are distributed across time, how they depend on one another, and when they are assessed, practised, and transferred.

## Schema contract

A valid sequence is a JSON object with `schema_version: "zamery-learning-sequence.v1"`. The `scripts/validate_learning_sequence.py` CLI enforces this contract.

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | `"zamery-learning-sequence.v1"` |
| `sequence_id` | string | yes | Stable identifier for this sequence version. Used downstream by assessment and reteaching skills. |
| `source_authority` | string | yes | One of: `teacher_supplied`, `licensed`, `public_primary_source`, `authorized_channel`, `model_generated`. Declares who authored the curriculum decisions embedded in the map. **Never default to `model_generated` when a teacher-supplied source exists.** |
| `duration_weeks` | positive int | yes | Total calendar span of the sequence. |
| `objective_ids` | string list | yes | All objectives this sequence covers. Must be unique. Every ID appears in at least one `coverage` entry. |
| `prerequisite_edges` | object list | yes | Declares prerequisite relationships: `{"from": "obj-A", "to": "obj-B"}` means A must be taught before B. Both endpoints must exist in `objective_ids`. Empty list when no prerequisites. |
| `coverage` | object list | yes | Maps each objective to the session numbers where it is explicitly taught. Each entry: `{"objective_id": "...", "sessions": [1, 3, 7]}`. Session numbers are positive ints. An objective with no coverage entry is an error — it is declared but not scheduled. |
| `review_schedule` | object list | yes | Spaced-retrieval reviews. Each entry: `{"session": 5, "objective_ids": ["..."]}`. All cited objectives must exist. Empty list is an error — every sequence needs at least one review point. |
| `assessment_windows` | object list | yes | Formative or summative assessment points. Each entry: `{"session": 8, "objective_ids": ["..."]}`. All cited objectives must exist. At least one window is required. |
| `transfer_levels` | string list | yes | Must include `"near"` and `"far"`. Near transfer applies the same concept in a slightly varied context; far transfer applies it in a distinctly different context or skill domain. |
| `standards_coverage` | object | optional | A map of standard identifiers to their descriptors. Each value is `{"standard_id": "...", "authority": "..."}`. The authority, when present, must be a valid source authority. Use this to declare curriculum alignment (CEFR, national standards, exam board). |
| `version` | int | optional | Positive integer. Increment every time the sequence is revised. |
| `prior_sequence_id` | string | optional | The `sequence_id` of the version this revision replaces. A new sequence omits this. |
| `revision_note` | string | optional | Human-readable summary of what changed in this revision. Required when `prior_sequence_id` is set; disallowed on first versions. |

## Session numbering

Sessions are numbered **1..N** across the whole sequence. A 16-week course meeting twice a week has 32 sessions; a weekly meeting has 16. The numbering is dense — every session from 1 to the highest number in any coverage/review/assessment entry must be accounted for across the full sequence duration. Gaps are allowed (a holiday week with no sessions assigned), but every session number referenced in any array must fall within the sequence's session count implied by `duration_weeks`.

## Design rules

1. **Every objective is covered at least twice.** A single exposure is insufficient for long-term retention. The second exposure should be in a different context or task type.
2. **Review sessions precede assessment windows.** A retrieval review (spaced) should occur at least one session before the assessment that measures that objective.
3. **Prerequisite ordering is acyclic.** The directed graph formed by prerequisite edges must not contain cycles. If A requires B and B requires C, then C must be covered in an earlier session than B, and B earlier than A.
4. **Transfer is designed, not assumed.** A sequence that includes far transfer must schedule at least one session where the learner applies the concept in a domain not used during initial instruction. Near transfer is the minimum expectation.
5. **Standards coverage is sourced, not asserted.** Every standard identifier carries an authority field. `model_generated` is valid only when no teacher-supplied or licensed curriculum alignment exists.

## Downstream consumers

The LearningSequenceMap is consumed by:

- **Assessment composition** (`zamery-compose-english-assessments`): uses `assessment_windows` and `objective_ids` to select items and schedule forms.
- **Practice generation** (`zamery-build-english-practice`): uses `coverage` and `review_schedule` to align problem sets with the current session.
- **Reteaching** (`zamery-plan-english-reteaching`): uses `prerequisite_edges` and `coverage` to identify which prerequisite to re-teach when an objective is not secure.
- **Learner monitoring** (`zamery-monitor-english-learning`): tracks progress against `objective_ids` and `assessment_windows`.
