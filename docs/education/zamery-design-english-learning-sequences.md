Quickstart:

```bash
npx skills add maemreyo/zmr-skills@zmr-dev --skill=zamery-design-english-learning-sequences
```

```bash
npx skills update zamery-design-english-learning-sequences
```

[Source](https://github.com/maemreyo/zmr-skills/tree/zmr-dev/skills/education/zamery-design-english-learning-sequences)

## What it does

`zamery-design-english-learning-sequences` produces a structured **LearningSequenceMap** for a long-horizon English K-12 learning journey — a course, term, semester, or year. It declares which objectives are taught in which order, how they depend on each other, when they are assessed and reviewed for spaced retrieval, how the learning transfers to new contexts, and what curriculum standards the sequence covers.

The defining constraint is the **course/term vs lesson/unit seam**: this skill owns the long-range map and stops before any single lesson blueprint or student-facing artifact. It surfaces the architecture of the learning journey — the *what* and the *when* — and leaves the *how* (lesson structure, methodology, differentiation, materials) to downstream specialists that consume the map. Direct invocation asserts the approved brief and curriculum, learner-context, prior-sequence, and authority versions before drawing or revising the map.

## When to reach for it

Type `/zamery-design-english-learning-sequences`, or the agent reaches for it automatically when a task fits — any request for a course plan, term outline, year-long scope and sequence, curriculum map, spaced retrieval schedule, or sequence revision.

Reach for it when you need to plan a whole term or year before designing individual lessons. If you need a single lesson or unit blueprint (the *how* for one session or a short series), use [zamery-design-english-learning](https://aihero.dev/skills-zamery-design-english-learning) instead. If you need to revise an existing sequence based on assessment data, this skill handles that too — it carries its own revision workflow with evidence-based diagnosis, impact tracing, and versioned history.

## The LearningSequenceMap

The leading idea is the **LearningSequenceMap** — a versioned JSON document (`zamery-learning-sequence.v1`) that encodes the full architecture of a long-horizon learning journey. The map is not a lesson plan, not a syllabus, and not a set of worksheets. It is the structural skeleton that every downstream artifact builds against.

The map answers five design questions:

- **Objective/prerequisite map**: Which concepts depend on which, in what order must they appear, and which edges form the dependency graph?
- **Standards coverage**: What curriculum standards (CEFR, national, exam board) does the sequence align to, and who authorised that alignment?
- **Spaced retrieval schedule**: When does the learner re-encounter each objective after initial instruction, at expanding intervals designed to catch forgetting before it compounds?
- **Assessment windows**: At which milestones is each objective measured, with retrieval scheduled at least one session before every assessment?
- **Transfer design**: Is the learner expected to apply the concept in near contexts (slightly varied), far contexts (distinctly different domain), or both?

A sequence that includes far transfer must schedule at least one session where the concept is applied outside its original domain. A sequence with only direct repetition and no transfer is incomplete.

## The revision discipline

A sequence revision is not a light edit. Every version bump follows a four-step cycle:

1. **Diagnose the gap** with specific evidence — not "the class struggled" but "session 12 assessment showed 68% not secure on obj-past-perfect."
2. **Trace impact** through the prerequisite graph to see which downstream objectives inherit the gap.
3. **Choose the repair** — resequence (change order), reallocate (shift sessions between objectives), or split (one objective was really two skills).
4. **Document the change** — bump version, set `prior_sequence_id`, and write a `revision_note` that cites the evidence and names the repair mode.

The revision is not complete until the teacher has approved the changed map.

## Where it fits

`zamery-design-english-learning-sequences` is a **chain step** that runs before any lesson design or content generation happens for a term or course:

```txt
copilot → sequence map → lesson/unit blueprints → practice / assessments / materials / slides
```

Once the LearningSequenceMap is approved, the baton passes to [zamery-design-english-learning](https://aihero.dev/skills-zamery-design-english-learning) for individual lesson blueprints (one per session or unit in the map), then to [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice) for rehearsal materials, [zamery-compose-english-assessments](https://aihero.dev/skills-zamery-compose-english-assessments) for the assessment windows, [zamery-plan-english-reteaching](https://aihero.dev/skills-zamery-plan-english-reteaching) for corrective loops, and [zamery-monitor-english-learning](https://aihero.dev/skills-zamery-monitor-english-learning) to track progress against the map. The map is the shared contract; every downstream consumer reads the same `objective_ids`, `coverage`, `review_schedule`, and `assessment_windows` to know what to build and when.

When the request is broad or ambiguous (the teacher is not sure whether they need a term map, a lesson, or something else), route through [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) first. For orientation across the whole skill set, see [ask-matt](https://aihero.dev/skills-ask-matt).
