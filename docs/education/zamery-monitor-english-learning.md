Quickstart:

```bash
npx skills add maemreyo/zmr-skills@zmr-dev --skill=zamery-monitor-english-learning
```

```bash
npx skills update zamery-monitor-english-learning
```

[Source](https://github.com/maemreyo/zmr-skills/tree/zmr-dev/skills/education/zamery-monitor-english-learning)

## What it does

`zamery-monitor-english-learning` aggregates dated assessment and student-work evidence into a per-objective **learning trajectory** — a time-series of teacher-reviewed evidence points with a descriptive trend (improving, stable, plateau, regressing, or insufficient data) and a review-due indicator.

It owns longitudinal aggregation, not learner discovery. The defining constraint is that it never produces a predictive score, behavioural label, or intervention recommendation. Every trend label is purely descriptive — it summarises what the evidence shows, never what it predicts. Direct invocation asserts the approved brief and evidence versions before aggregation, so stale or unapproved records cannot enter a trajectory.

## When to reach for it

Type `/zamery-monitor-english-learning`, or the agent reaches for it automatically when a task fits — any request to check progress, find which objectives are secure, see where growth has stalled, review what evidence changed, or produce a class-level progress summary.

Reach for it when you have assessment results or analysed student work and need to see the trajectory across time. If you need to create or update a learner's initial profile or StudentCard instead, use [zamery-understand-learners](https://aihero.dev/skills-zamery-understand-learners). If the evidence confirms a gap that needs reteaching, [zamery-plan-english-reteaching](https://aihero.dev/skills-zamery-plan-english-reteaching) is the downstream step.

## Trajectory, not profile

The leading idea is the **learning trajectory** — a dated sequence of evidence points against one stable objective. Three points are the minimum for a descriptive trend label; fewer than three yields `insufficient` and the skill says so. This prevents premature conclusions from sparse data.

The skill accepts evidence only at `teacher_reviewed` authority. An automated score or unverified observation cannot enter the trajectory until a teacher has reviewed it. This is a hard gate: no teacher review, no trajectory point.

Objective evidence is bucketed by objective ID, sorted by date, and summarised per objective as an `ObjectiveEvidenceSummary` — count, latest status, first and latest dates, and flags for plateau, regression, missing evidence, or review due. When the teacher asks about a whole class, the skill produces a `ClassProgressProfile` with coverage tables and evidence-freshness ratings.

## It's working if

- Every trajectory has a `trend` label, and every label is either a descriptive one (improving, stable, plateau, regressing) with ≥3 points or `insufficient`.
- The teacher can see at a glance which objectives have confirmed trends and which need more data.
- No output contains a predictive score, risk label, or intervention suggestion.
- Every evidence point in the output is labelled `teacher_reviewed`.
- The `review_due_at` field is set, so the teacher knows when to check back.

## Where it fits

`zamery-monitor-english-learning` is a **chain step** that runs after evidence is created and before reteaching or progress communication:

```txt
assessments / student-work analysis → monitor_learning → reteach / design / communicate
```

It feeds facts to [zamery-plan-english-reteaching](https://aihero.dev/skills-zamery-plan-english-reteaching) (when a gap is confirmed), [zamery-design-english-learning](https://aihero.dev/skills-zamery-design-english-learning) (when current progress informs the next blueprint), and materials design (for approved progress facts). It never directly changes those artifacts — it supplies the evidence they depend on.

For routing broad or ambiguous Zamery requests, start at [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot). For the wider skill set, see [ask-matt](https://aihero.dev/skills-ask-matt).
