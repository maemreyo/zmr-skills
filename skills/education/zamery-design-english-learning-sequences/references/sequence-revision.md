# Sequence Revision

A LearningSequenceMap changes over time as assessment data reveals gaps, the curriculum shifts, or a teacher's lived experience shows the original plan was too ambitious for the actual class. This reference governs the revision process.

## When to revise — not every change is a revision

| Trigger | Is a revision? | Action |
|---|---|---|
| Teacher spots a typo in a session number | No | Fix in place, no version bump |
| Assessment data shows 70%+ of the class did not reach secure on objective X | **Yes** | Revise the coverage map: add sessions, adjust prerequisite order, or split the objective |
| Teacher has a better sequencing idea mid-term based on classroom feel | **Maybe** — log it and wait for evidence before revising. A feeling is not data. |
| School adopts a new textbook that shifts the order of topics | **Yes** | Redraw the map from the new source authority |
| A reteaching plan resolves a misconception permanently | No — the reteaching plan is a tactical overlay on top of the current map. The map itself only changes when the overlay becomes structural (i.e. the same reteach happens two terms in a row). |
| Teacher wants to add standards coverage metadata | No — metadata-only changes do not affect delivery and do not need a version bump |

## Revision workflow

### Step 1 — Diagnose the gap

Identify which specific objective or session is failing. Use evidence from:
- Assessment window results (formative or summative)
- Trajectory data from `zamery-monitor-english-learning`
- Reteaching plans that cycled back with no improvement

Name the **least precise location**: not "the class struggled with grammar" but "session 12 coverage of obj-past-perfect did not transfer to the session 18 assessment window."

### Step 2 — Trace impact

Before changing anything, trace the cascade:

1. Which prerequisite edges originate from the failing objective? Every downstream objective that depends on this one will inherit the gap.
2. Which review sessions reference the failing objective? Those reviews will produce unreliable data until the gap is resolved.
3. Which assessment windows measure the failing objective? Results from those windows are not actionable until the sequence is repaired.
4. Which transfer activities assume the objective is secure? Far-transfer activities that depend on it must be deferred or scaffolded.

### Step 3 — Choose the repair

Three modes, chosen by depth of the gap:

| Mode | When | What changes |
|---|---|---|
| **Resequence** | The objective order is wrong — B was taught before A, but A is prerequisite | Swap or shift sessions in `coverage`. Update `prerequisite_edges` if relationship changes. |
| **Reallocate** | The objective needs more sessions, or a session currently assigned to a secure objective would be better spent elsewhere | Shift session assignments between objectives. Decrease coverage for over-resourced objectives. |
| **Split** | The objective is actually two separate skills that were conflated in the original map | Add a new `objective_id`, split sessions, add edges, update every downstream reference. Bump the map version. |

### Step 4 — Bump and document

1. Increment `version` by 1.
2. Set `prior_sequence_id` to the current `sequence_id`.
3. Write a `revision_note` that names the trigger, the evidence, and the repair mode. Example: `"Resequenced obj-reported-speech after obj-past-perfect (session 5 before session 3); assessment window 6 showed 68% not secure on backshift. Reallocated two sessions from obj-conditional-3 to obj-reported-speech."`
4. Run `validate_learning_sequence.py` against the revised map — repair every error before publishing the new version.

## Completion criteria for a revision

A revision is complete when:

1. **Every referenced objective exists** in `objective_ids` — no orphan references in coverage, review, or assessment entries.
2. **Prerequisite edges form an acyclic graph** consistent with the session ordering.
3. **Every objective has at least two coverage sessions** — a revision that reduces an objective to a single exposure must explain the regression in the `revision_note`.
4. **The revision note cites specific evidence** — not "to improve outcomes" but "session 12 assessment window showed 68% not secure on obj-past-perfect."
5. **`version` is incremented** and `prior_sequence_id` points at the replaced version.
6. **The teacher has approved** the revised map before it is consumed downstream. The approval is a human decision, not a machine check — this skill never pushes a revision without review.
