---
name: zamery-design-english-learning-sequences
description: >-
  Use when a teacher asks to plan, sequence, or redesign a long-horizon English K–12 learning journey — a course, term, semester, or year-long sequence spanning multiple weeks — including objective/prerequisite maps, standards coverage, spaced retrieval and review scheduling, assessment windows, transfer design, and sequence revision. Triggers: "course plan", "term outline", "year-long map", "unit sequence", "learning journey map", "scope and sequence", "curriculum map", "spaced schedule", "sequence revision", "redesign my course", "re-sequence this unit". Do NOT use for a single lesson/unit blueprint (use zamery-design-english-learning), for a one-off worksheet (zamery-build-english-practice), or for assessing/reteaching individual students (zamery-monitor-english-learning/zamery-plan-english-reteaching).
---

# Zamery Design English Learning Sequences

Design the **long-horizon learning journey** — the course map, term sequence, or year-long scope and sequence — and stop before any lesson/unit blueprint or student-facing artifact. This skill owns the **course/term seam**; it produces a LearningSequenceMap. Downstream skills (lesson design, practice, assessment, reteaching) consume that map but do not redraw it.

## The seam — course/term vs lesson/unit

The leading idea is the **seam** — a hard boundary between the long-horizon sequence map and any single lesson or unit blueprint:

| Owned here | NOT owned here |
|---|---|
| Which objectives are taught, in what order, and across which sessions | How a single session is structured (phases, timing, methodology) |
| Prerequisite dependency edges between objectives | Specific teaching techniques for a given objective |
| Spaced retrieval schedule spanning the whole term | One-off retrieval practice items for a session |
| Assessment windows (which objectives are measured when) | The actual assessment form, items, or rubrics |
| Transfer design (near and far application targets) | Worksheet, slide, or presentation content |
| Standards coverage map (CEFR, national, exam board) | Per-objective differentiation tracks |
| Revision history — versioned changes with evidence | Reteaching plans for individual students |

When a request touches both the sequence map *and* a specific lesson plan, this skill produces the map first and then hands the baton to `zamery-design-english-learning` for each lesson/unit. It never produces a lesson plan itself.

## Workflow

Before drawing or revising the map, apply `../_shared/references/brief-version-contract.md` to the approved brief and every curriculum, ClassProfile, snapshot, prior sequence, and authority dependency. Reject stale or unapproved input even when this skill was invoked directly.

### Phase 1 — Recover context

Read the conversation history, any attached Teaching Brief, and any existing LearningSequenceMap (if this is a revision). Establish:
- Is this a new sequence or a revision of an existing one?
- What is the span? (term, semester, year)
- How many sessions per week and total?

### Phase 2 — Establish source authority

Before drawing the map, pin down the **source authority** for every curriculum decision. Apply the order from the Teaching Brief: (1) safety/privacy/legal blocks, (2) teacher's explicit instruction, (3) teacher-supplied required sources, (4) the approved Teaching Brief, (5) teacher-supplied preferred/reference sources, (6) inferred values and defaults. Never default to `model_generated` when a teacher-supplied source exists.

If the teacher has not supplied a curriculum source, state the authority as `model_generated` and explain what that means: the map is based on typical CEFR or national-curriculum progressions, not on a governed source pack.

### Phase 3 — Build the objective/prerequisite map

List every learning objective the sequence must cover. Each gets a stable `objective_id` that will not change across revisions unless the objective itself changes.

Determine `prerequisite_edges`: which objectives depend on which. The graph must be acyclic. If the teacher names A then B then C, check whether C actually depends on B or on A directly — mis-ordered prerequisites are the most common source of assessment-window failure later.

### Phase 4 — Schedule coverage

Distribute objectives across sessions. Every objective appears in at least two sessions. The first session of an objective is its initial instruction; subsequent sessions are varied-context re-exposure or deepening.

Use the `references/learning-sequence-map.md` coverage rules: session numbers are dense 1..N across the whole sequence, gaps allowed (holidays), but every referenced session number falls within the implied session count.

### Phase 5 — Design the spaced retrieval schedule

Place `review_schedule` entries at intervals that follow a **expanding** pattern: the first review of an objective happens soon after its last coverage session (1–2 sessions later), the next review farther out, and so on. The goal is to catch forgetting before it compounds.

Every review session must be **at least one session before** any assessment window that measures the same objective — retrieval before measurement, never measurement without retrieval.

### Phase 6 — Set assessment windows

Place `assessment_windows` at natural milestones: end of a block of related objectives, mid-term, and/or end-of-term. Each window names the objectives it measures. Windows are checkpoints, not the whole of assessment — formative observation happens throughout.

### Phase 7 — Design for transfer

Explicitly declare `transfer_levels`:
- **Near transfer**: apply the concept in a slightly varied context (e.g., change from conversations to written sentences, or from one text type to another with similar structure).
- **Far transfer**: apply the concept in a distinctly different domain (e.g., use past-tense narrative skills learned in English class to write a lab report in science class).

If the teacher does not request far transfer, the sequence must still include near transfer. A sequence with only direct-repetition practice and no transfer is not valid.

### Phase 8 — Map standards coverage

Record `standards_coverage` as an object mapping standard identifiers to their descriptors. Each entry has a `standard_id` and an `authority`. Use this to declare alignment with:
- CEFR levels (A1–C2 descriptors)
- National curriculum standards (key stage, grade-level expectations)
- Exam board specifications (IELTS, Cambridge English, TOEFL Junior, local board exam)

Do not claim certified alignment without a governed reference pack. If the teacher says "this is for Grade 8 in Vietnam" and no official Vietnamese curriculum document is supplied, mark the authority as `model_generated` and explain the gap.

### Phase 9 — Validate and materialise

1. Assemble the full sequence as a `zamery-learning-sequence.v1` JSON object.
2. Run `python3 scripts/validate_learning_sequence.py <path>` and repair every reported error.
3. Present the validated map to the teacher for review, with a short list of unresolved decisions (e.g., "you said 12 weeks but the coverage requires 14 sessions — recommend reducing obj-X coverage or extending the term").

### Phase 10 — Revision handling

If this is a revision of an existing sequence (triggered by assessment data, a teacher request, or a curriculum shift), follow `references/sequence-revision.md`:
1. Diagnose the specific gap with evidence.
2. Trace impact through prerequisite edges, review schedule, assessment windows, and transfer activities.
3. Choose the repair mode: resequence, reallocate, or split.
4. Bump version, set `prior_sequence_id`, write a `revision_note` citing specific evidence.
5. Validate and present for teacher approval.

## Completion criterion

This skill is complete when:

1. A valid `zamery-learning-sequence.v1` JSON object has been produced, passed `validate_learning_sequence.py`, and been recorded in the session.
2. Every objective in the map appears in at least two coverage sessions.
3. The spaced retrieval schedule has at least one review entry before every assessment window.
4. Transfer levels include near (and far if applicable).
5. Source authority is declared for every curriculum choice.
6. If the sequence is a revision, version is bumped, prior_sequence_id is set, and the revision note cites specific evidence.
7. The teacher has approved the map — approval is an explicit human signal in the conversation, not a machine default.
8. If the conversation also needs lesson/unit blueprints, this skill hands off to `zamery-design-english-learning` with the `sequence_id` and relevant `objective_ids`, and does not produce the blueprints itself.
