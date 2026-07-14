---
name: zamery-plan-english-reteaching
description: Use when a teacher needs a structured reteaching plan for English K–12 based on prior analysis evidence — misconceptions, error taxonomies, or monitoring data. Produces a reteaching plan with evidence sufficiency, an alternative explanation, the smallest corrective move, and a reconnect→contrast→guided discrimination→corrective rehearsal→transfer→reassessment loop. Does not own feedback, concept teaching, practice construction, or reassessment delivery — those are handed off to downstream specialists. Triggers: plan reteaching, reteach X concept, what to do next after analysis, fix the misconception, address the error pattern, reteaching plan.
---

# Zamery Plan English Reteaching

This skill plans the smallest effective reteaching intervention for a known misconception or error pattern. It produces a **reteaching plan** — one documented Teacher Action Plan scoped to a single objective. It does not own feedback ownership (that stays in `zamery-analyze-student-work`), concept instruction (`zamery-teach-english-concepts`), practice construction (`zamery-build-english-practice`), or reassessment delivery (the downstream specialist). The plan is a handoff document.

Before planning, apply `../_shared/references/brief-version-contract.md` to the approved brief and every analysis, trajectory, objective, and authority dependency. Reject stale or unapproved input even when this skill was invoked directly.

## Evidence sufficiency — gate

Do not plan a reteaching intervention without meeting the evidence bar.

**Minimum bar.** At least one of:
- Two+ independent observations of the same error pattern across different items or contexts, with comparable task demands.
- One high-confidence diagnostic from `zamery-analyze-student-work` where the probing protocol confirmed the misconception.
- A monitoring trend (`zamery-monitor-english-learning` trajectory) showing flat or declining performance on the same objective over three or more time points.

**Below-bar action.** Do not plan. Instead request the missing evidence. If the teacher asks you to proceed anyway, label every recommendation `provisional: true` in the reteaching plan and state the evidence gap in the plan rationale.

**Misconception confidence.** Label each planned intervention with `confidence: low | medium | high`. A single observation on one item is `low`. Two+ consistent observations across items is `medium`. Probing-confirmed or trajectory-confirmed is `high`.

## Alternative explanation — before you move to the plan

For every planned misconception, generate exactly one **competing explanation** that could account for the same evidence. Record it as `competing_explanations` in the reteaching plan. Competing explanations are limited to:

| Category | Example |
|---|---|
| **Task misunderstanding** | The student did what the question asked, but the question was ambiguous. |
| **Careless slip** | Correct knowledge, wrong execution under time or cognitive load. |
| **Overgeneralisalying a different rule** | Applying a regular past-tense rule to an irregular verb — the student _has_ a rule, just the wrong domain. |
| **Attentional / fatigue** | Errors cluster at the end of the exercise or on low-significance items. |
| **Misheard or misread prompt** | The student responded to a different word or phrase. |

If the competing explanation is as or more plausible than the primary hypothesis, do not plan a reteaching intervention. Instead recommend a focused probe session via `zamery-analyze-student-work`.

## Smallest corrective move

Choose the **smallest move** that addresses the evidence. Rank from smallest to largest:

1. **Exemplar contrast** — Show the correct and incorrect form side by side; ask the student to identify the difference.
2. **Guided discrimination** — Present a set of examples where the student must select which ones match the rule and which do not.
3. **Corrective rehearsal** — The student produces the correct form in a scaffolded, narrow context with immediate feedback.
4. **Re-teach concept** — The concept needs re-explanation from the prerequisite up (`zamery-teach-english-concepts`).
5. **Remediate prerequisite** — The student lacks a prerequisite skill; the reteaching cannot succeed without rebuilding that foundation first (handoff to `zamery-design-english-learning` for sequence redesign).

The smallest move is almost never "start over from the beginning." Default to exemplar contrast unless evidence shows the student has no acquaintance with the rule at all.

## The reteaching loop

Every plan follows six phases **in order**. Skip a phase only when the student's evidence proves the phase is unnecessary; label the skip `skip_reason` in the plan.

### 1. Reconnect prerequisite

Activate the knowledge the student already has that the new learning depends on. Do not reteach the prerequisite — just surface it with one recall prompt or recognition task.

**Completion criterion.** The student produces or identifies the correct prerequisite form/rule from memory. One correct response is sufficient.

### 2. Contrast

Present the target form and the student's error form side by side, in the same context, and ask the student to identify what is different and which one matches the expected rule. The contrast must be a minimal pair differing only on the feature being targeted.

**Completion criterion.** The student correctly identifies which form matches the rule and can state the difference in their own words.

### 3. Guided discrimination

The student receives a set of examples — some matching the target rule, some not — and classifies each one, explaining their decision aloud. Feedback after each decision is immediate and labels the feature they should attend to.

**Completion criterion.** 4 out of 5 consecutive items correctly classified and explained.

### 4. Corrective rehearsal

The student produces the correct form in scaffolded, narrow contexts. Scaffolding fades across the phase: start with close deletion (fill the blank in an otherwise complete sentence), move to cued production (a prompt that strongly implies the form), then to independent production with only a brief context.

**Completion criterion.** 3 out of 3 consecutive independent productions are correct.

### 5. Transfer

The student applies the form/rule in a new context — new vocabulary, new situational frame, or (for far transfer) a different skill domain that nevertheless depends on the same form/rule.

**Transfer levels.** The plan must specify `near` (same domain, novel content) and, where the teacher approves, `far` (different domain, same form). Near transfer is mandatory; far transfer is recommended if the teacher accepts the session count.

**Completion criterion.** Near transfer: correct application in 2 of 2 novel contexts. Far transfer: correct application in 1 of 1 novel domain context (optional based on teacher approval).

### 6. Reassessment

The plan defines a reassessment event — what success looks like, which objective it targets, and how many items to present. Reassessment is a **new artifact** owned by the reassessment specialist (the downstream composition skill); the reteaching plan only specifies the requirements.

**Reassessment requirements.** In the plan record:
- `objective_ids` — which objectives to reassess.
- `success_evidence` — what observable outcome counts as evidence the reteaching held.
- `item_count` — minimum items for a reliable signal (default: 5).
- `wait_days` — how long after the last transfer session before reassessment (default: 2, range 0–7).
- `auto_schedule` — whether the reassessment fires automatically (default: true, but the teacher may override to manual).

## Handoff boundaries

This skill produces a single artifact: a **reteaching plan** conforming to `zamery-reteaching-plan.v1`. It does not execute the reteaching. Execution is distributed:

| Phase | Owner | Artifact |
|---|---|---|
| Reconnect prerequisite | `zamery-teach-english-concepts` | One concept explanation or recall prompt |
| Contrast | `zamery-teach-english-concepts` | Minimal-pair contrast set |
| Guided discrimination | `zamery-build-english-practice` | Discrimination exercise set |
| Corrective rehearsal | `zamery-build-english-practice` | Scaffolded production exercise |
| Transfer | `zamery-build-english-practice` | Transfer exercise set (near / far) |
| Reassessment | downstream composition skill | Assessment form (5+ items) |
| Student card update | `zamery-understand-learners` | Evidence appended to `learning_evidence` |

The reteaching plan references `evidence_ids` from the prior analysis and includes the `objective_ids` each phase targets. The receiving skill loads the plan and executes its assigned phase.

Do **not** regenerate materials that already exist in the reteaching plan's referenced prior analyses. The plan references by `evidence_id` and `plan_id`; the downstream skill loads the record it needs.

## Completion criteria

The reteaching plan is complete when all of the following are true:

1. **Evidence sufficiency met** — the gate passed with at least one of the minimum-bar conditions (or the plan is labelled provisional with the gap stated).
2. **Alternative explanation recorded** — the plan's `misconception.statement` has a corresponding `competing_explanations` entry.
3. **Smallest corrective move selected** — the `teacher_action.proposed_move` names the smallest move that fits the evidence.
4. **All six phases scoped** — each phase has a target objective and completion criterion, or a labelled `skip_reason`.
5. **Reassessment specified** — the plan includes `reassessment` with `objective_ids`, `success_evidence`, `item_count`, `wait_days`, and `auto_schedule`.
6. **Handoff targets named** — every phase beyond reconnect is associated with the owning skill name.
7. **Teacher approval captured** — `teacher_action.teacher_approval` set to `true`, or the plan is labelled `draft`.

Do not hold the plan for downstream execution. The plan is a document; execution is a separate concern.
