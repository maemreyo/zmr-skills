Quickstart:

```bash
npx skills add maemreyo/zmr-skills@zmr-dev --skill=zamery-plan-english-reteaching
```

```bash
npx skills update zamery-plan-english-reteaching
```

[Source](https://github.com/maemreyo/zmr-skills/tree/zmr-dev/skills/education/zamery-plan-english-reteaching)

## What it does

`zamery-plan-english-reteaching` plans the smallest effective reteaching intervention for a known misconception or error pattern in English K–12. It produces a **reteaching plan** — one documented Teacher Action Plan scoped to a single objective — with a six-phase instructional loop: reconnect the prerequisite, contrast the error with the target, guide discrimination, rehearse correctively, transfer to new contexts, and schedule reassessment. The defining constraint: this skill **plans but does not execute** — it hands off every phase to a downstream specialist and records the plan as a handoff document. Direct invocation asserts the approved brief and analysis or trajectory versions before planning; stale or unapproved evidence is rejected.

## When to reach for it

Type `/zamery-plan-english-reteaching`, or the agent reaches for it automatically when a task fits — any time a teacher needs a structured reteaching plan grounded in prior analysis or monitoring evidence.

Reach for it when you have confirmed a misconception (two or more observations, probing-validated, or trajectory-confirmed) and need a plan for what to do next. For analysing student work in the first place, use [zamery-analyze-student-work](https://aihero.dev/skills-zamery-analyze-student-work). For executing the reteaching — explaining a concept, building practice exercises, or composing a reassessment — the plan hands off to [zamery-teach-english-concepts](https://aihero.dev/skills-zamery-teach-english-concepts), [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice), and the downstream assessment skill.

## Evidence gate

The skill refuses to plan without evidence. The minimum bar is two independent observations of the same error pattern, one high-confidence probing diagnosis, or a flat monitoring trajectory across three or more time points. Below that, every recommendation is labelled `provisional: true`, and the evidence gap is stated in the plan rationale — no automatic downstream execution is permitted for a provisional plan.

This gate prevents the most common reteaching mistake: intervening on a pattern that is not actually a pattern.

## The smallest move

The skill ranks interventions from smallest to largest and defaults to the smallest that fits the evidence:

1. **Exemplar contrast** — correct and incorrect side by side, student identifies the difference.
2. **Guided discrimination** — student classifies examples, explaining each decision.
3. **Corrective rehearsal** — scaffolded production that fades to independence.
4. **Re-teach concept** — full re-explanation from the prerequisite up.
5. **Remediate prerequisite** — the student lacks a foundation skill first.

Most reteaching plans start at step one. Evidence that the student has no acquaintance with the rule at all is required to skip straight to step four.

## The six-phase loop

Every plan follows these phases in order. A phase may be skipped only when evidence proves it unnecessary, and the skip is labelled with a reason.

1. **Reconnect prerequisite** — surface what the student already knows with one recall prompt.
2. **Contrast** — present a minimal pair of target and error forms; student identifies the difference.
3. **Guided discrimination** — classify examples with immediate feedback.
4. **Corrective rehearsal** — produce the correct form in scaffolded contexts that fade to independence.
5. **Transfer** — apply the form to new contexts (near transfer mandatory, far transfer recommended).
6. **Reassessment** — specify what success looks like, on what schedule, and with how many items.

## Handoff boundaries

This skill is a **planning node** in the Zamery system. It does not own feedback (that stays in `zamery-analyze-student-work`), concept instruction (`zamery-teach-english-concepts`), practice construction (`zamery-build-english-practice`), or reassessment delivery (the downstream composition skill). Each phase of the loop names its owning skill, so the downstream specialist can pick up the plan and execute the phase without re-deriving the context.

## It's working if

- The reteaching plan passes `validate_reteaching_plan` with zero errors.
- Every phase has a named owner or a labelled skip reason.
- The misconception field has exactly one competing explanation.
- The Teacher Action Plan preserves `shared_objective`, `assessment_construct`, and `learner_dignity`.
- Provisional plans are clearly labelled and include a stated evidence gap.

## Where it fits

`zamery-plan-english-reteaching` is a **chain step** — it sits between `zamery-analyze-student-work` (which feeds in) and the execution skills (`zamery-teach-english-concepts`, `zamery-build-english-practice`, and the assessment skill that owns reassessment). It is also reachable from `zamery-monitor-english-learning`, when a monitoring trajectory triggers a reteaching need.

When you are not sure which Zamery skill fits, start at [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot). For the wider skill set, see [ask-matt](https://aihero.dev/skills-ask-matt).
