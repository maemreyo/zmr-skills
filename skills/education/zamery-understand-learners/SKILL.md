---
name: zamery-understand-learners
description: Use when a teacher asks to understand a learner or class, create or update a StudentCard, run an intake or baseline learner study, collect student voice, understand engagement conditions, or prepare learner context before planning. Also when another skill needs ClassProfile or an approved Learner Context Snapshot before downstream generation.
---

# Zamery Understand Learners

This skill owns **learner discovery** — the governed, multi-source workflow that produces a StudentCard, a privacy-safe ClassProfile, and a time-bounded Learner Context Snapshot. It does not administer personality tests, psychological screening, emotion recognition, risk prediction, or placement decisions.

## Hard gates

No real-student data may enter StudentCard until all gates below are closed — synthetic-data prototyping is permitted:

1. **Jurisdiction and profiling determination** — qualified legal/privacy review determines whether the system constitutes prohibited child profiling or high-risk AI under applicable law.
2. **Purpose and field-level consent architecture** — every field category has a named educational purpose, lawful basis, school authority, consent requirement, expiry, and independent revocability.
3. **School-controlled persistence design** — cards live in a tenant-isolated, encrypted school store with access auditing, correction, deletion, and legal hold.
4. **Safeguarding protocol** — input containing possible serious harm, abuse, or distress is held from the card and shown only to an authorised human.
5. **Age and deployment policy** — age-appropriate assent, observation, and trend-inference rules per grade band, with K–2 algorithmic trend prohibition.

## Workflow

Before generation, apply `../_shared/references/brief-version-contract.md` to the approved brief and every supplied dependency, including prior StudentCard or trajectory versions. Reject stale or unapproved input even when this skill was invoked directly.

1. **Confirm purpose and consent.** Retrieve approved consent scopes. Reject requests that lack a named educational purpose or required authorisation. Refuse collection for personality profiling, psychological screening, emotion recognition, risk scoring, or placement decisions.
2. **Orchestrate the Learner Discovery Pack** — collect evidence in four separate channels:
   - **Academic diagnostic**: current evidence against named English objectives. Grade and CEFR remain independent; CEFR is never inferred from grade.
   - **Student voice**: interests, co-authored goals, perceived success, participation choices — shown verbatim and separately from teacher interpretation. Self-report fields declare whether they are ordinary instructional feedback or protected wellbeing/psychological items (disabled by default).
   - **Structured teacher observation**: date, learning context, task, observable action, strength or successful condition, support tried, immediate effect, counterexample if any, observer. Free-form labels are not accepted.
   - **Optional parent/caregiver input**: structured choices and purpose-limited short answers. Validation blocks health, psychological, family-conflict, income, religion, disciplinary, identity, and other sensitive content.
3. **Validate and redact.** Run the input through `scripts/validate_student_card.py` against the StudentCard contract. Reject prohibited labels, missing/expired authority or consent, stale evidence, and unresolved safeguarding holds.
4. **Generate StudentCard.** Record dated evidence with required metadata per item: source, authority, observed_at, context, evidence_id, confidence, counterevidence, expires_at, consent_scope_id, dispute_status.
5. **Generate ClassProfile** (whole-class planning) — aggregate objective distribution, common strengths and misconceptions with evidence counts, accessibility requirements, interest clusters only when large enough to avoid re-identification. Never include names, card IDs, diagnoses, individual behaviour narratives, or sensitive reports. Do not resolve contradictory evidence into a single score.
6. **Generate Learner Context Snapshot** (individual practice) — current objective and success evidence, prerequisite evidence, relevant strengths and misconceptions, authorised accommodations, recently effective strategies, one or two interests if useful, current goal, evidence dates and expiry. Teacher approves before use.
7. **Produce missing/conflicting/stale evidence report.** Optionally propose two or three evidence-linked teaching hypotheses, each with a concrete teaching move, rationale, observable success signal, and trial window — require teacher approval before downstream use.

## Input boundary

- Approved purpose and consent scopes.
- Teacher context and structured observations.
- Student self-report and co-authored goals.
- Parent/caregiver input when authorised.
- Academic diagnostic evidence from assessment or student-work analysis.
- Optional prior StudentCard or LearningTrajectory summaries.

## Output boundary

- `StudentCard` — longitudinal, evidence-heavy, interpretation-light learner record.
- `ClassProfile` — privacy-safe whole-class aggregate for lesson planning.
- `LearnerContextSnapshot` — time-bounded minimum context for one teaching purpose.
- Missing/conflicting/stale evidence report.
- Optional teacher-action hypotheses (reversible, teacher-approved).

Full StudentCard never reaches downstream generation skills. Copilot routes through this skill before design when longitudinal learner context is available or explicitly requested.

## Completion criteria

- Every recommendation links to dated evidence and a teacher-approved purpose.
- Every interpretation is distinguishable from observation and includes confidence and counterevidence.
- No personality type, diagnosis, emotion-recognition result, predicted outcome, comparative ranking, or prohibited label is stored.
- Students can contribute, view age-appropriate explanations, challenge an entry, and have stale entries corrected.
- Consent withdrawal prevents future use and triggers the configured deletion process.
- Whole-class generation consumes ClassProfile, not individual cards.
- Individual generation consumes only an approved, time-bounded snapshot.
- Shared objectives and assessment constructs are not silently changed by a card.
- Card content does not leak into student-facing or published artifacts.
- The system records whether a recommended teaching move helped, not only whether the learner complied.
- Serious-concern content is never stored as a card attribute or algorithmic risk result — it follows the school's human safeguarding route.

## Prohibited fields and outputs

- Personality type or trait score.
- Clinical diagnosis, disability category, psychological score, mental-health risk, or emotion-recognition result.
- Predicted dropout, misconduct, future attainment, or other future-outcome score.
- Race, religion, family income, socioeconomic rank, or demographic comparison.
- Comparative class ranking or labels such as `low`, `weak`, `lazy`, `naughty`, `unmotivated`, `addicted`, or `problem student`.
- Unstructured teacher notes.
- Raw PII in evidence copied into downstream artifacts.
- Any automatic placement, track, intervention, accommodation, parent notification, or change to assessment construct.
