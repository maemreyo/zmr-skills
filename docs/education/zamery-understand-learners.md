Quickstart:

```bash
npx skills add maemreyo/zmr-skills@zmr-dev --skill=zamery-understand-learners
```

```bash
npx skills update zamery-understand-learners
```

[Source](https://github.com/maemreyo/zmr-skills/tree/zmr-dev/skills/education/zamery-understand-learners)

## What it does

`zamery-understand-learners` builds a governed, evidence-heavy learner record — the StudentCard — from academic evidence, student voice, structured teacher observations, and optional parent input. It then derives a privacy-safe ClassProfile for whole-class planning or a minimal Learner Context Snapshot for individual reteaching and practice.

The defining constraint: **it never stores a personality type, diagnosis, emotion, risk score, or prohibited label.** Every interpretation is dated, has confidence and counterevidence attached, and is distinguishable from observation. The output is deliberately evidence-heavy and interpretation-light — a teacher sees what the learner currently demonstrates and what teaching was tried, not a permanent category. Direct invocation still asserts the approved brief and dependency versions before generation; stale or unapproved learner evidence is rejected rather than silently replaced.

## When to reach for it

Type `/zamery-understand-learners`, or the agent reaches for it automatically when a task fits — any time a teacher asks to understand a learner or class, create or update a StudentCard, run an intake study, collect student voice, or prepare learner context before design.

Reach for it when you need a longitudinal learner view before planning a lesson, practice set, or assessment. If you already have a specific lesson or unit in mind without a learner context, go directly to [zamery-design-english-learning](https://aihero.dev/skills-zamery-design-english-learning). If you need to analyse existing student work rather than build a profile, use [zamery-analyze-student-work](https://aihero.dev/skills-zamery-analyze-student-work).

## Learner discovery

The workflow is a multi-source **learner discovery** — not a single intake form. The skill collects evidence in four separate channels, each with its own purpose, consent boundary, and validation rules:

- **Academic diagnostic** — current evidence against named English objectives. Grade and CEFR are always independent.
- **Student voice** — interests, co-authored goals, confidence, and participation choices. Shown verbatim and separately from teacher interpretation. Reviewed every 4–6 weeks.
- **Structured teacher observation** — dated, contextual, action-based records that separate what the learner did from what the teacher tried. Free-form labels are rejected.
- **Optional parent input** — structured choices and limited free text. Sensitive content (health, diagnosis, family conflict) is blocked from entering the card and routed to an authorised human.

The skill then applies a validation gate: prohibited labels (lazy, unmotivated, addicted, naughty, low, weak, problem student) are rejected wherever they appear. Every evidence item requires an ID, source, authority, date, expiry, confidence, and optional counterevidence. No statement exists as an undated permanent trait.

## Three output objects

| Object | Scope | Purpose | Never includes |
|--------|-------|---------|----------------|
| **StudentCard** | One learner | Longitudinal evidence record | Personality, diagnosis, risk score, prohibited labels |
| **ClassProfile** | Whole class | Lesson planning aggregate | Names, card IDs, individual narratives, single resolved scores |
| **Learner Context Snapshot** | One teaching purpose | Minimum context for reteaching or practice | Full card, sensitive parent reports, past observations not relevant to this purpose |

The full StudentCard never reaches downstream content-generation skills. Copilot delivers only the approved ClassProfile or snapshot.

## It's working if

- Every recommendation is linked to dated evidence with a teacher-approved purpose.
- Prohibited labels are never stored — the validator rejects them.
- Student voice is reported verbatim, not interpreted by the model.
- Contradictory evidence is shown side by side, not collapsed into a single score.
- Serious-concern input is held for authorised human handling, never stored in the card.
- The teacher approves every snapshot and action hypothesis before it is used downstream.

## Where it fits

`zamery-understand-learners` is a **chain step** — it runs before any learner-sensitive design, practice, or reteaching:

```txt
zamery-teacher-copilot → understand-learners → design / teach / practice / assess
```

Its neighbour [zamery-analyze-student-work](https://aihero.dev/skills-zamery-analyze-student-work) feeds evidence back into the card after teaching, closing the loop. For reteaching based on what the card reveals, [zamery-plan-english-reteaching](https://aihero.dev/skills-zamery-plan-english-reteaching) is the downstream consumer. Use [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) for Zamery routing and [ask-matt](https://aihero.dev/skills-ask-matt) for the wider skill set.
