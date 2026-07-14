Quickstart:

```bash
npx skills add maemreyo/zmr-skills@zmr-dev --skill=zamery-build-english-practice
```

```bash
npx skills update zamery-build-english-practice
```

[Source](https://github.com/maemreyo/zmr-skills/tree/zmr-dev/skills/education/zamery-build-english-practice)

## What it does

`zamery-build-english-practice` produces one-off student-facing worksheets, drills, homework sets, flashcards, reading passages, and differentiated exercises for a single teaching session — not reusable item banks or graded assessments.

Every student surface is **answer-free**. The skill never places answers, rubrics, explanations, or wrong-reason metadata on the student's copy. This is non-negotiable: practice is for rehearsal, not for evaluation. The student artifact shows only the task, the space to respond, and the instructions. Answers and scoring guidance stay on a separate teacher surface. Direct invocation asserts the approved brief and every blueprint, concept, reteaching-plan, learner-context, and authority version before item generation.

## When to reach for it

Type `/zamery-build-english-practice`, or the agent reaches for it automatically when a task fits — any request for a one-off worksheet, drill, homework set, flashcards, reading passage, or differentiated student exercises.

Reach for it when you need practice for *this* lesson, *these* students, *this* concept — a one-time thing. If you need a reusable pool of 80-400+ items with deduplication and version control, use [zamery-build-english-item-banks](https://aihero.dev/skills-zamery-build-english-item-banks) instead. If you need a graded quiz or exam with forms and answer sets, use [zamery-compose-english-assessments](https://aihero.dev/skills-zamery-compose-english-assessments). If the practice needs IELTS-aligned constraints, use [zamery-create-ielts-practice](https://aihero.dev/skills-zamery-create-ielts-practice). For practice tied to video media, use [zamery-build-video-learning](https://aihero.dev/skills-zamery-build-video-learning).

## Progression, not just exercises

The leading idea is the **progression** — exercises are sequenced along a cognitive ramp. The skill uses worked examples, faded guidance, independent practice, spaced retrieval, interleaving, and near or far transfer when appropriate. A shorter sequence is allowed only when the material does not support every stage.

Every item carries an independent choice of interaction type, response mode, cognitive operation, evidence type, scoring approach, and context — so variety changes what the learner *does*, not just how the worksheet looks.

## Where it fits

`zamery-build-english-practice` is a **chain step** that runs after a concept has been taught or a blueprint has been approved, and before materials design or presentation creation adds layout and branding:

```txt
(design → concept teaching →) practice → materials / slides
```

Its closest neighbours are [zamery-teach-english-concepts](https://aihero.dev/skills-zamery-teach-english-concepts), which feeds the taught concept, and [zamery-plan-english-reteaching](https://aihero.dev/skills-zamery-plan-english-reteaching), which can request targeted misconception, scaffold, transfer, and reassessment practice. After practice is built, hand it to materials or presentation specialists for layout. Use [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) for Zamery routing and [ask-matt](https://aihero.dev/skills-ask-matt) for the wider skill set.
