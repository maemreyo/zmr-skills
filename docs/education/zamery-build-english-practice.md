Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-build-english-practice
```

```bash
npx skills update zamery-build-english-practice
```

[Source](https://github.com/maemreyo/zmr-skills/tree/main/skills/education/zamery-build-english-practice)

## What it does

`zamery-build-english-practice` produces one-off student-facing worksheets, drills, homework sets, flashcards, reading passages, and differentiated exercises for a single teaching session — not reusable item banks or graded assessments.

Every student surface is **answer-free**. The skill never places answers, rubrics, explanations, or wrong-reason metadata on the student's copy. This is non-negotiable: practice is for rehearsal, not for evaluation. The student artifact shows only the task, the space to respond, and the instructions. Answers and scoring guidance stay on a separate teacher surface.

## When to reach for it

Type `/zamery-build-english-practice`, or the agent reaches for it automatically when a task fits — any request for a one-off worksheet, drill, homework set, flashcards, reading passage, or differentiated student exercises.

Reach for it when you need practice for *this* lesson, *these* students, *this* concept — a one-time thing. If you need a reusable pool of 80-400+ items with deduplication and version control, use [zamery-build-english-item-banks](https://aihero.dev/skills-zamery-build-english-item-banks) instead. If you need a graded quiz or exam with forms and answer sets, use [zamery-compose-english-assessments](https://aihero.dev/skills-zamery-compose-english-assessments). If the practice needs IELTS-aligned constraints, use [zamery-create-ielts-practice](https://aihero.dev/skills-zamery-create-ielts-practice). For practice tied to video media, use [zamery-build-video-learning](https://aihero.dev/skills-zamery-build-video-learning).

## Progression, not just exercises

The leading idea is the **progression** — exercises are sequenced along a cognitive ramp. The skill uses a practice progression model: worked example first (the student sees how it's done), then guided practice (scaffolded), then independent practice (the student on their own), then retrieval (spaced, from earlier material), then transfer (the concept applied in a slightly new context). A shorter sequence is allowed only when the material doesn't support every stage.

Every item carries an independent choice of interaction type, response mode, cognitive operation, evidence type, scoring approach, and context — so variety changes what the learner *does*, not just how the worksheet looks.

## Where it fits

`zamery-build-english-practice` is a **chain step** that runs after a concept has been taught or a blueprint has been approved, and before materials design or presentation creation adds layout and branding:

```txt
(design → concept teaching →) practice → materials / slides
```

Its closest neighbour is [zamery-teach-english-concepts](https://aihero.dev/skills-zamery-teach-english-concepts), which feeds the concept that the practice drills. After practice is built, the output can be handed to [zamery-design-teaching-materials](https://aihero.dev/skills-zamery-design-teaching-materials) for branded DOCX or PDF layout, or to [zamery-create-english-presentations](https://aihero.dev/skills-zamery-create-english-presentations) for classroom slide projection. When the request is broad or ambiguous, route through [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) first.
