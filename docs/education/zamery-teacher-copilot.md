Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-teacher-copilot
```

```bash
npx skills update zamery-teacher-copilot
```

[Source](https://github.com/maemreyo/zmr-skills/tree/main/skills/education/zamery-teacher-copilot)

## What it does

`zamery-teacher-copilot` is the router over the 11 Zamery specialist skills for English K-12 teaching. You describe the teaching situation you're in; it orients you and dispatches work to the right specialist.

It **does no teaching itself**. It doesn't design a lesson, explain a grammar point, build a worksheet, or compose an assessment — it only classifies the intent and hands off to the specialist that owns it. It exists because the 11 specialists are **model-invoked**: the agent might reach for any of them on its own, but only the copilot holds the full map of which intents route to which skills and in what order to run them when a request spans multiple artifacts.

## When to reach for it

You invoke this by typing `/zamery-teacher-copilot` — the agent won't reach for it on its own.

Reach for it when the request is broad, ambiguous, or crosses more than one artifact type: "I need a lesson on past simple with worksheets and a quiz" (spans design, practice, assessment). If you already know exactly which specialist you need — a single worksheet, a concept explanation, an IELTS reading set — skip the copilot and invoke that specialist directly.

## The routing discipline

The routing table maps 11 intents to 11 specialists. The idea to hold onto is **intent before count**: a 300-question drill pool routes to the item bank constructor, but a 100-question end-of-term exam routes to the assessment composer, and a long ungraded worksheet might pass through the item bank constructor first and then the materials designer for layout. The copilot follows ordering rules — design before generation, bank before form assembly, materials and presentations after approved content, review and publish last — and passes the same brief ID, objectives, and constraints across every handoff so nothing is lost.

It never emulates a missing specialist. If a required specialist isn't installed, the copilot states the blocker instead of trying to fill in.

## Where it fits

`zamery-teacher-copilot` is the **router** — the entry point into the whole Zamery suite, sitting at the top rather than inside any chain. From here you land on any of the 11 specialists: [zamery-design-english-learning](https://aihero.dev/skills-zamery-design-english-learning) for lesson/unit blueprints, [zamery-teach-english-concepts](https://aihero.dev/skills-zamery-teach-english-concepts) for concept explanations, [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice) for one-off worksheets, [zamery-build-english-item-banks](https://aihero.dev/skills-zamery-build-english-item-banks) for reusable item pools, [zamery-compose-english-assessments](https://aihero.dev/skills-zamery-compose-english-assessments) for graded exams, [zamery-create-ielts-practice](https://aihero.dev/skills-zamery-create-ielts-practice) for IELTS prep, [zamery-build-video-learning](https://aihero.dev/skills-zamery-build-video-learning) for video-based sequences, [zamery-design-teaching-materials](https://aihero.dev/skills-zamery-design-teaching-materials) for branded worksheets and print-ready output, [zamery-create-english-presentations](https://aihero.dev/skills-zamery-create-english-presentations) for classroom slides, [zamery-analyze-student-work](https://aihero.dev/skills-zamery-analyze-student-work) for marking and feedback, and [zamery-review-publish-pack](https://aihero.dev/skills-zamery-review-publish-pack) for final QA and packaging. When you're unsure which specialist fits, the copilot is the node to start from.
