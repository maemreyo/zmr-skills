Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-design-english-learning
```

```bash
npx skills update zamery-design-english-learning
```

[Source](https://github.com/maemreyo/zmr-skills/tree/main/skills/education/zamery-design-english-learning)

## What it does

`zamery-design-english-learning` produces a structured instructional blueprint for an English K-12 lesson or unit — the objectives, evidence criteria, timed phases, methodology, differentiation, and assessment plan — before any worksheet, slide, or exam is created.

It **stops at the blueprint boundary**. The skill will not generate finished student-facing or teacher-facing artifacts. It exits with an approved blueprint and a short list of unresolved decisions, leaving downstream specialists to handle the actual content generation. This is the design-before-build discipline applied to teaching: settle the structure and the evidence criteria first, so everything downstream builds against a fixed target.

## When to reach for it

Type `/zamery-design-english-learning`, or the agent reaches for it automatically when a task fits — any request to plan, structure, sequence, or redesign an English K-12 lesson or unit.

Reach for it when you need a lesson sequence or unit laid out before creating the materials. If the goal is to teach a single concept (vocabulary, grammar point, pronunciation) without a full unit plan, use [zamery-teach-english-concepts](https://aihero.dev/skills-zamery-teach-english-concepts) instead. If you already have an approved blueprint and just need one-off worksheets, skip the design step and go straight to [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice).

## The blueprint before the build

The leading idea is the **blueprint** — a structured plan with stable objective IDs, observable success evidence, prerequisite and misconception notes, timed phases, methodology with rationale, differentiation tracks, and a downstream artifact map. The skill builds a Teaching Brief from the conversation context, marks each field as explicitly given, inferred, defaulted, or unresolved, and asks exactly one question at a time only when a material gap would change the objectives, grade or CEFR adaptation, methodology, assessment scope, or duration.

Grade band and CEFR level are kept independent. CEFR is never assumed from grade alone.

## Where it fits

`zamery-design-english-learning` is a **chain step** that runs before any content generation:

```txt
zamery-teacher-copilot (optional) → blueprint → practice / assessments / materials / slides
```

Once the blueprint is approved, the baton passes to specialists that build against it: [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice) for one-off rehearsal, [zamery-compose-english-assessments](https://aihero.dev/skills-zamery-compose-english-assessments) for graded tests, [zamery-design-teaching-materials](https://aihero.dev/skills-zamery-design-teaching-materials) for branded worksheets and print-ready output, or [zamery-create-english-presentations](https://aihero.dev/skills-zamery-create-english-presentations) for classroom slides. When the request is broad or ambiguous, route through [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) first.
