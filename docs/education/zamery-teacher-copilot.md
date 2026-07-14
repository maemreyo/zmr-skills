Quickstart:

```bash
npx skills add maemreyo/zmr-skills@zmr-dev --skill=zamery-teacher-copilot
```

```bash
npx skills update zamery-teacher-copilot
```

[Source](https://github.com/maemreyo/zmr-skills/tree/zmr-dev/skills/education/zamery-teacher-copilot)

## What it does

`zamery-teacher-copilot` is the router over 15 Zamery specialist skills for English K-12 teaching. You describe the teaching situation you're in; it orients you and dispatches work to the right specialist.

It **does no teaching itself**. It classifies intent, governs the Teaching Brief, and hands off to the specialist that owns each result. Full StudentCards remain outside downstream context; only approved snapshots and summaries cross boundaries.

## When to reach for it

You invoke this by typing `/zamery-teacher-copilot` — the agent won't reach for it on its own.

Reach for it when the request is broad, ambiguous, or crosses more than one artifact type: "I need a lesson on past simple with worksheets and a quiz" (spans design, practice, assessment). If you already know exactly which specialist you need — a single worksheet, a concept explanation, an IELTS reading set — skip the copilot and invoke that specialist directly.

## The routing discipline

The routing table maps 15 intents to 15 specialists. The idea to hold onto is **intent before count**: learner discovery precedes learner-sensitive design, monitoring precedes reteaching or progress communication, long-horizon sequence design precedes lesson design, bank generation precedes form assembly, and review/publish remains last. Before every handoff, the copilot asserts the approved brief and dependency versions. If evidence is missing, stale, contradictory, or needs protected human judgment, it stops the affected path and names the evidence, human owner, and safe next action instead of filling the gap with model inference. A specialist failure preserves valid partial state and retries only from the failed boundary.

It never emulates a missing specialist. If a required specialist isn't installed, the copilot states the blocker instead of trying to fill in.

## Where it fits

`zamery-teacher-copilot` is the **router** at the top of the suite. Its four new neighbours are [zamery-understand-learners](https://aihero.dev/skills-zamery-understand-learners), [zamery-monitor-english-learning](https://aihero.dev/skills-zamery-monitor-english-learning), [zamery-plan-english-reteaching](https://aihero.dev/skills-zamery-plan-english-reteaching), and [zamery-design-english-learning-sequences](https://aihero.dev/skills-zamery-design-english-learning-sequences); the existing eleven owners still handle lesson design, concepts, practice, item banks, assessments, IELTS, video, materials, presentations, student-work analysis, and publication. For the wider repository map, see [ask-matt](https://aihero.dev/skills-ask-matt).
