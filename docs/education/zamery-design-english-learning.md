Quickstart:

```bash
npx skills add maemreyo/zmr-skills@zmr-dev --skill=zamery-design-english-learning
```

```bash
npx skills update zamery-design-english-learning
```

[Source](https://github.com/maemreyo/zmr-skills/tree/zmr-dev/skills/education/zamery-design-english-learning)

## What it does

`zamery-design-english-learning` produces a structured instructional blueprint for an English K-12 lesson or unit — the objectives, evidence criteria, timed phases, methodology, differentiation, and assessment plan — before any worksheet, slide, or exam is created.

It **stops at the blueprint boundary**. The skill will not generate finished student-facing or teacher-facing artifacts. It exits with an approved blueprint and a short list of unresolved decisions, leaving downstream specialists to handle the actual content generation. This is the design-before-build discipline applied to teaching: settle the structure and the evidence criteria first, so everything downstream builds against a fixed target. Direct invocation asserts the approved brief and every learner-context, sequence, curriculum, and authority version before design begins.

## When to reach for it

Type `/zamery-design-english-learning`, or the agent reaches for it automatically when a task fits — any request to plan, structure, sequence, or redesign an English K-12 lesson or unit.

Reach for it when you need a lesson sequence or unit laid out before creating the materials. If the goal is to teach a single concept (vocabulary, grammar point, pronunciation) without a full unit plan, use [zamery-teach-english-concepts](https://aihero.dev/skills-zamery-teach-english-concepts) instead. If you already have an approved blueprint and just need one-off worksheets, skip the design step and go straight to [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice).

## The blueprint before the build

The leading idea is the **blueprint** — a structured plan with stable objective IDs, observable success evidence, prior-knowledge activation, worked examples, prerequisite and misconception notes, timed phases, methodology with rationale, differentiation, spacing hooks, near and far transfer, and a downstream artifact map. It may consume a ClassProfile for whole-class planning or an approved Learner Context Snapshot for individual work, but never a full StudentCard.

Grade band and CEFR level are kept independent. CEFR is never assumed from grade alone.

## Where it fits

`zamery-design-english-learning` is a **chain step** that runs before any content generation:

```txt
zamery-teacher-copilot (optional) → blueprint → practice / assessments / materials / slides
```

For course, term, or year planning, [zamery-design-english-learning-sequences](https://aihero.dev/skills-zamery-design-english-learning-sequences) owns the parent map; each lesson blueprint must align with its objectives, prerequisites, review schedule, transfer, and assessment windows. Once approved, the baton passes to practice, assessment, materials, or presentation specialists. Use [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) for Zamery routing and [ask-matt](https://aihero.dev/skills-ask-matt) for the wider skill set.
