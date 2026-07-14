---
name: zamery-monitor-english-learning
description: Use when a teacher asks how a learner or class is progressing, which objectives are secure, where growth has stalled, what evidence changed, or requests a progress summary, trajectory, or dashboard. Do not use for initial learner profiling, consent collection, or psychological/behavioural risk scoring.
---

# Zamery Monitor English Learning

Aggregate longitudinal assessment and student-work evidence into a dated, teacher-reviewed trajectory. Own the objective-evidence ledger; do not profile learners, predict outcomes, or recommend interventions.

## Discovery vs trajectory boundary

This skill owns **trajectory** — the time-series aggregation of evidence against stable objectives. It does not own **learner discovery** (initial profiling, consent, StudentCard creation). Before trajectory work, confirm a StudentCard has at least one approved evidence point; if none exists, state that discovery must run first and stop. This skill consumes approved summaries from discovery; it never re-ingests raw longitudinal evidence independently.

## Does not own

- Learner profiling, consent collection, or StudentCard creation — use `zamery-understand-learners`.
- Psychological, behavioural, future-outcome, placement, or intervention risk scores.
- Predictive rankings, causal claims without teacher review, or pacing recommendations.
- Document layout, family communication prose, or presentation generation.
- Causal claims that a strategy worked without teacher review.

## Inputs

- Objective IDs and curriculum references from the approved Teaching Brief or blueprint.
- Evidence records from `zamery-compose-english-assessments` (scored results) and `zamery-analyze-student-work` (diagnosed submissions), each with `objective_id`, `observed_at`, `status`, and `authority`.
- Strategy-result records from reteaching and lesson enactment when the teacher supplies them with explicit success signals.
- StudentCard ID for linking inside the protected store — never as downstream content.

## Outputs

- **LearningTrajectory** — dated sequence of objective-level evidence with a descriptive trend and review-due indicator.
- **ObjectiveEvidenceSummary** — per-objective roll-up: point count, latest status, first-observed date, plateau/regression/missing-evidence flags, and a list of the evidence IDs that support the summary.
- **ClassProgressProfile** — coverage table across objectives and learners, evidence freshness, and group-level gaps.
- Review-due and evidence-gap indicators with explicit dates.
- Approved progress facts for downstream materials, family communication, and report generation.

## Workflow

Before generation, apply `../_shared/references/brief-version-contract.md` to the approved brief and every evidence, StudentCard, objective, and authority dependency. Reject stale or unapproved input even when this skill was invoked directly.

1. Confirm the input evidence ledger has at least one approved point for the requested learner or class. If zero points exist, state that no longitudinal evidence is available and stop — do not simulate a trajectory from a single snapshot.
2. Bucket evidence records by `objective_id`. For each objective, sort by `observed_at` and build the evidence sequence.
3. For each objective with three or more dated points, compute a descriptive trend label (`improving`, `stable`, `plateau`, `regressing`, `insufficient`). Fewer than three points yields `insufficient` — no trend label is valid with fewer points.
4. Build the `ObjectiveEvidenceSummary` for every objective that has at least one point: count, latest status, first date, plateau/regression/missing-evidence flags.
5. Build the `LearningTrajectory` as the ordered set of objective-level trajectories. Set `review_due_at` to the next date by which new evidence should be reviewed.
6. When the teacher asks about a class, build the `ClassProgressProfile` from the per-learner trajectories: coverage, evidence freshness, group-level gaps.
7. Run `python3 scripts/validate_learning_trajectory.py` against every `LearningTrajectory` and every `ObjectiveEvidenceSummary` produced. Repair every reported error before delivery.
8. Output the trajectory, summaries, and review-due indicators. Never output a predictive rank, behavioural label, or intervention suggestion.

## Completion criteria

- Every output `LearningTrajectory` passes `validate_learning_trajectory()` from the shared contracts.
- Every `ObjectiveEvidenceSummary` passes the summary validation rules in `references/objective-evidence-summary.md`.
- Every trend label is either `insufficient` (fewer than three points) or one of the defined descriptive labels.
- No output contains a predictive score, behavioural risk label, causal claim unapproved by the teacher, or intervention recommendation.
- The `review_due_at` field is set for every trajectory.
- Evidence gaps are reported, not silently assumed.
- The teacher can distinguish at a glance which objectives have confirmed trends and which need more data.

## References

- `references/learning-trajectory.md` — the LearningTrajectory data model, field semantics, version rules.
- `references/objective-evidence-summary.md` — per-objective roll-up rules, plateau/regression/missing-evidence detection.
- `references/class-progress-profile.md` — class-level coverage, freshness, and gap reporting.
