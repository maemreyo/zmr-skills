Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-teach-english-concepts
```

```bash
npx skills update zamery-teach-english-concepts
```

[Source](https://github.com/maemreyo/zmr-skills/tree/main/skills/education/zamery-teach-english-concepts)

## What it does

`zamery-teach-english-concepts` explains a vocabulary, grammar, pronunciation, reading, writing, listening, speaking, or language-use concept clearly and memorably — building a concept model, a misconception contrast, a board representation, and comprehension checks — without generating worksheets, assessments, or slides.

It **stays inside the teaching moment**. The skill will not expand into practice exercises, graded items, presentation files, or any downstream artifact. Its job is the live classroom explanation: what the teacher says, what the teacher writes on the board, what the learner is expected to think at each step, and how to verify the learner understood before moving on. This is the concept-teaching discipline separated from the materials-building discipline so each can be reached for independently and composed as needed.

## When to reach for it

Type `/zamery-teach-english-concepts`, or the agent reaches for it automatically when a task fits — any request to understand or explain an English K-12 concept before turning it into practice or assessment.

Reach for it when you need a single concept taught well: what the present perfect means, how syllable stress works in academic vocabulary, how to structure a paragraph. If you need the concept *and* a worksheet in one pass, route through [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) which will sequence concept teaching before practice generation. If instead you need a full lesson or unit plan with objectives and timed phases, use [zamery-design-english-learning](https://aihero.dev/skills-zamery-design-english-learning).

## The teaching move

The skill selects a methodology from its registry — the smallest method that fits — and gives a one-sentence rationale. It then builds four things that together make a concept teachable:

- **A concept model** — what the concept is, stated precisely for the learner's band, using the relevant domain guidance (grammar playbook, vocabulary playbook, pronunciation playbook, and so on).
- **A misconception contrast** — the specific mistake the learner is likely to make and how to differentiate the target from its nearest confusable.
- **A board plan** — what goes on the board, how it builds across the teaching phase, and when each element appears.
- **Comprehension checks and a transfer prompt** — how to verify understanding in the moment and one prompt that asks the learner to use the concept in a slightly new context.

The output is four things: teacher moves, expected learner thinking, the board plan, checks, and the transfer prompt. No more.

## Where it fits

`zamery-teach-english-concepts` is a **standalone teaching step** that can be used on its own or sequenced inside a larger flow. When it runs as part of a multi-artifact request, it comes after the blueprint (if one exists) and before practice, assessment, or slides — the concept is taught and verified before any student-facing or teacher-facing artifact is built. Its closest neighbour is [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice), which turns the taught concept into drillable exercises; the two are designed to be chained. When the request is broad or ambiguous, route through [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) first.
