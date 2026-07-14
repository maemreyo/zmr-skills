Quickstart:

```bash
npx skills add maemreyo/zmr-skills@zmr-dev --skill=zamery-create-english-presentations
```

```bash
npx skills update zamery-create-english-presentations
```

[Source](https://github.com/maemreyo/zmr-skills/tree/zmr-dev/skills/education/zamery-create-english-presentations)

## What it does

`zamery-create-english-presentations` converts approved English K-12 teaching content into classroom slide decks with separate teacher notes.

It preserves the pedagogy the content was designed for. The skill plans each slide by its classroom purpose and the action the teacher or student takes on it — not by how much text fits the box. A slide that drills vocabulary works differently from one that models a reading strategy, and the deck structure reflects that. Teacher notes are a separate surface, never hidden in speaker notes that students could reach. Direct invocation asserts the approved brief and every source, template, brand, and authority version before deck planning.

## When to reach for it

Type `/zamery-create-english-presentations`, or the agent reaches for it automatically when a task fits — any time approved teaching content needs converting into a classroom deck.

Reach for it when the lesson or unit plan is settled and what remains is the presentation surface. If the content structure itself is still being designed, use [zamery-design-english-learning](https://aihero.dev/skills-zamery-design-english-learning) first. For page-layout materials (worksheets, workbooks, exam papers) instead of slides, use [zamery-design-teaching-materials](https://aihero.dev/skills-zamery-design-teaching-materials).

## Pedagogy-first slide planning

The skill opens every session by reading `references/slide-pedagogy.md`, which classifies slides not by template but by classroom action: a concept-introduction slide, a guided-practice slide, a whole-class-discussion slide, an independent-work slide. Each type has a deliberate layout — how much text, where the example sits, whether the answer appears on the student slide or only in the teacher notes.

A deck is only as good as its plan, so the skill plans every slide by purpose and action before touching any visual design. The output is a structured deck manifest (validated by `scripts/validate_deck_manifest.py`) that captures each slide's role, its content, and the classroom action it supports. Student slides, teacher notes, and print fallbacks are kept structurally separate throughout.

Every slide is reopened and inspected for accessibility, cognitive load, classroom participation, CJK text, legibility, and leakage. Named learner cues and protected profile data are prohibited on projected surfaces. Repairs target only the affected slides, then the deck re-renders from the validated manifest.

## It's working if

- Every slide has a clear classroom action that a teacher could name from looking at it.
- Teacher notes are a separate surface, not hidden speaker notes.
- The deck manifest is validated before rendering, not after.
- No internal metadata (prompts, field names, generation commentary) appears on any student-facing slide.

## Where it fits

`zamery-create-english-presentations` is a chain step in the Zamery flow, producing presentations from settled teaching content.

Its sibling [zamery-design-teaching-materials](https://aihero.dev/skills-zamery-design-teaching-materials) handles page layouts while this skill handles slide decks. Both feed into [zamery-review-publish-pack](https://aihero.dev/skills-zamery-review-publish-pack) for final gating and delivery. Use [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) for Zamery routing and [ask-matt](https://aihero.dev/skills-ask-matt) for the wider skill set.
