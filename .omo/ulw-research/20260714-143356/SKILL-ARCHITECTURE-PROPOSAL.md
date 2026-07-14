# Proposed Zamery Education Skill Architecture

**Goal:** convert the audit and StudentCard direction into a small number of deep, independently invocable skills, while keeping cross-cutting quality rules mandatory and avoiding micro-skill sprawl.

## Architecture rule

A capability becomes a new skill only when all five conditions hold:

1. It has an independent teacher trigger.
2. It owns a multi-step workflow with meaningful decisions.
3. It has a distinct input and output contract.
4. Another skill or Copilot must be able to invoke it independently.
5. Removing it would scatter substantial complexity across existing skills.

Otherwise it becomes an enhancement to the current owner, a shared contract/reference, or platform infrastructure.

## Recommended suite shape

Keep the existing Teacher Copilot and 11 specialists. Add four model-invoked specialists in the first architecture target:

1. `zamery-understand-learners`
2. `zamery-monitor-english-learning`
3. `zamery-plan-english-reteaching`
4. `zamery-design-english-learning-sequences`

Add one later-phase specialist only after longitudinal classroom evidence exists:

5. `zamery-improve-english-teaching`

Do not create standalone skills for accessibility, privacy, AI safety, learning science, curriculum mapping, family communication, listening, speaking, or assessment validity. They belong in the shared kernel or current owners as described below.

## 1. `zamery-understand-learners`

**Leading word:** learner discovery  
**Invocation:** teacher asks to understand a learner/class, create or update a StudentCard, run an intake or baseline learner study, collect student voice, understand engagement conditions, or prepare learner context before planning.  
**Why standalone:** this is a governed multi-source discovery and evidence-resolution workflow, not a static profile document.

### Owns

- Learner Discovery Pack.
- Consent/purpose check before collection.
- Structured academic baseline orchestration.
- Student voice, structured teacher observation, optional parent input, and authorised accommodation intake.
- StudentCard creation, review, correction, dispute, expiry, and deletion requests.
- ClassProfile and Learner Context Snapshot generation.
- Safeguarding hold and human-only escalation.
- When a LearningTrajectory already exists, consume its approved summaries instead of independently re-ingesting raw longitudinal assessment evidence.

### Does not own

- Longitudinal mastery aggregation or progress reporting.
- Ongoing ingestion of assessment/student-work results for time-series analysis; that belongs to `zamery-monitor-english-learning`.
- Diagnosis, personality testing, emotion recognition, risk prediction, placement, or accommodation decisions.
- Student-work marking or item generation.
- Final lesson, practice, assessment, or material generation.

### Inputs

- Approved purpose and consent scopes.
- Teacher context and structured observations.
- Student self-report and co-authored goals.
- Parent/caregiver input when authorised.
- Academic diagnostic evidence from assessment or student-work analysis.

### Outputs

- `StudentCard`.
- `ClassProfile`.
- `LearnerContextSnapshot`.
- Missing/conflicting/stale evidence report.
- Optional teacher-action hypotheses for immediate low-stakes use.

### Copilot route

Runs before design when longitudinal learner context is requested or available. Whole-class work receives ClassProfile; individual practice/reteaching receives an approved snapshot. Full cards never reach downstream generation skills.

## 2. `zamery-monitor-english-learning`

**Leading word:** learning trajectory  
**Invocation:** teacher asks how a learner/class is progressing, which objectives are secure, where growth has stalled, what evidence changed, or requests a progress summary/dashboard.  
**Why standalone:** it owns longitudinal aggregation, not learner discovery; its core problem is time-series evidence over stable objectives.

### Owns

- Objective-evidence ledger across lessons, practice, assessments, and student-work analysis.
- Dated mastery/evidence trajectory without predictive ranking.
- Spacing/review due-state and prerequisite dependency visibility.
- Class-level coverage and evidence summaries.
- Teacher-reviewed plateau, regression, or missing-evidence indicators.
- Progress summary data for student/family communication.

### Does not own

- Initial learner profiling or consent collection.
- Psychological, behavioural, future-outcome, placement, or intervention risk scores.
- Causal claims that a strategy worked without teacher review.
- Document layout or family communication prose.

### Inputs

- Objective IDs and curriculum references.
- Results from `zamery-compose-english-assessments`.
- Evidence from `zamery-analyze-student-work`.
- Strategy-result records from reteaching and lesson enactment.
- StudentCard ID only for linking inside the protected store, never as downstream content.

### Outputs

- `LearningTrajectory`.
- `ObjectiveEvidenceSummary`.
- `ClassProgressProfile`.
- Review-due and evidence-gap indicators.
- Approved progress facts for materials/report generation.

### Copilot route

Runs after learning evidence is created, or before design/reteaching when the teacher asks for current state or trajectory. It feeds facts to learner understanding, reteaching, lesson design, and materials; it does not directly change those artifacts.

## 3. `zamery-plan-english-reteaching`

**Leading word:** reteaching loop  
**Invocation:** teacher says students still do not understand, asks how to fix a misconception, close an objective gap, intervene after assessment, or reteach a concept differently.  
**Why standalone:** this is a deep corrective-instruction workflow with multiple decision branches and an explicit reassessment loop.

### Owns

- Confirmation of the target gap and evidence sufficiency.
- Alternative explanations and misconception discrimination.
- Selection of the smallest corrective teaching move.
- Reteaching sequence: reconnect prerequisite → re-represent/contrast → guided discrimination → corrective rehearsal → transfer → reassessment.
- Teacher Action Plan with trial window and success signal.
- Reassessment prescription and review of whether the move helped.

### Does not own

- Original diagnosis of student work.
- Finished explanation, worksheet, or assessment rendering.
- Long-term progress aggregation.
- Automatic intervention assignment.

### Inputs

- Evidence ledger and misconception confidence from `zamery-analyze-student-work`.
- Current objective trajectory from `zamery-monitor-english-learning`.
- Approved Learner Context Snapshot or ClassProfile.
- Original blueprint and relevant artifacts.

### Outputs

- `ReteachingPlan`.
- `TeacherActionPlan`.
- Requests to `zamery-teach-english-concepts` and `zamery-build-english-practice`.
- Reassessment specification for assessment composition or student-work analysis.

### Copilot route

Runs after student-work analysis or progress monitoring confirms an unmet objective. Its internal route is concept teaching → targeted practice → reassessment → analysis/monitoring.

## 4. `zamery-design-english-learning-sequences`

**Leading word:** learning journey  
**Invocation:** teacher asks for a multi-week scheme of work, semester plan, spiral curriculum, spaced review plan, syllabus pacing, curriculum map, or coordinated sequence of lessons and assessments.  
**Why standalone:** the existing design skill owns one lesson or unit blueprint. Long-horizon curriculum sequencing introduces distinct constraints: standards coverage, prerequisite graph, spacing, interleaving, assessment windows, revision cycles, and artifact dependencies.

### Owns

- Multi-week/term objective and prerequisite map.
- Curriculum/standard coverage ledger with governed source authority.
- Spacing, retrieval, interleaving, cumulative review, and near-to-far transfer schedule.
- Lesson/unit slots and assessment windows.
- Resource and artifact roadmap.
- Sequence revision impact across downstream lessons and assessments.

### Does not own

- Detailed lesson blueprint, concept explanation, worksheet, item bank, or exam generation.
- Curriculum certification without a governed reference pack.
- Individual learner profiling.

### Inputs

- Curriculum/standard source pack.
- Time horizon, sessions, constraints, and assessment calendar.
- ClassProfile and ClassProgressProfile when authorised.
- Existing lesson/unit blueprints and artifacts.

### Outputs

- `LearningSequenceMap`.
- Objective/prerequisite graph.
- Coverage and review schedule.
- Briefs for `zamery-design-english-learning` and assessment/item-bank specialists.

### Copilot route

Runs before lesson/unit design for term, course, semester, syllabus, or spiral-planning requests. Individual lessons remain owned by `zamery-design-english-learning`.

## 5. Later phase: `zamery-improve-english-teaching`

**Leading word:** instructional inquiry  
**Invocation:** teacher supplies enacted-lesson evidence and asks to reflect, compare teaching moves, improve classroom practice, or run a small action-research cycle.  
**Status:** do not build in the first wave. It becomes legitimate only after StudentCard/action-plan, progress, and reteaching flows produce structured enactment evidence.

### Future ownership

- Lesson intention-versus-enactment review.
- Teacher reflection tied to student evidence.
- Strategy-result comparison without teacher ranking.
- Small inquiry cycle: question → evidence → change → trial → review.
- Coaching questions and next teaching experiment.

### Non-overlap

It never evaluates teacher performance or conducts employment appraisal. Without real enactment evidence, it must not provide generic opinion-based coaching.

## Enhancements to existing skills

### `zamery-teacher-copilot`

- Add four new route intents and dependency order.
- Route learner discovery before learner-sensitive design.
- Route monitoring before reteaching or progress communication.
- Route sequence design before lesson/unit design for long horizons.
- Keep full StudentCards outside downstream context.
- Add an explicit insufficient-evidence and human-handoff path.
- Add an error-recovery and partial-delivery path that states what remains valid, what is blocked, and what can be retried when a downstream skill fails.
- Assert Teaching Brief and dependency-version currency before every downstream generation; reject or explicitly re-approve stale inputs.

### `zamery-design-english-learning`

- Consume ClassProfile and approved snapshots.
- Add prior-knowledge activation, worked examples, near/far transfer, and spacing hooks.
- Validate each lesson/unit against its parent LearningSequenceMap when present.
- Keep curriculum mapping for a single unit inside this skill; course/term sequencing belongs to `zamery-design-english-learning-sequences`.

### `zamery-teach-english-concepts`

- Expand oral-language playbooks for listening and speaking.
- Add misconception-triggered contrast, prediction, counterexample, self-explanation, and teach-back patterns.
- Consume a minimum ClassProfile/snapshot, never a full StudentCard.

### `zamery-build-english-practice`

- Apply shared retrieval, spacing, interleaving, worked-example fading, and transfer contracts.
- Accept targeted requests from reteaching.
- Add listening and speaking practice families rather than creating separate listening/speaking skills.

### `zamery-build-english-item-banks`

- Add validity, bias/DIF review metadata, misconception coverage, exposure/security, and shared oral-language item families.
- Never encode an individual learner profile into a reusable bank.

### `zamery-compose-english-assessments`

- Add validity argument, construct-preserving accommodation review, reliability/decision-consistency, form-equivalence, and rater-calibration contracts.
- Export objective evidence to monitoring only after teacher-approved scoring.

### `zamery-create-ielts-practice`

- Add rater-calibration exemplars and longitudinal criterion evidence exports.
- Keep official task-family constraints unchanged by learner context.

### `zamery-build-video-learning`

- Apply multimedia-learning, listening strategy, connected-speech, accessibility, and learner-control references.
- Consume ClassProfile only for chunking/access/context decisions.

### `zamery-design-teaching-materials`

- Add `learner_progress_report`, `family_update_letter`, `student_goal_review`, and curriculum-overview document types.
- Consume only approved progress facts and communication directives.
- Add accessible DOCX/PDF/PPTX semantics, not only visual QA.

### `zamery-create-english-presentations`

- Add accessibility, cognitive-load, classroom participation, and CJK rendering gates.
- Never place named learner cues or protected profile data on projected surfaces.

### `zamery-analyze-student-work`

- Export structured objective evidence and misconception records to monitoring.
- Offer a handoff to reteaching when evidence is sufficient, especially after the teacher reports that the smallest first reteaching move did not resolve the gap.
- Keep feedback ownership; remove responsibility for the full reteaching sequence.
- Apply feedback literacy: help the learner understand, judge, manage the response, and act on feedback rather than delivering feedback as a one-way message.

### `zamery-review-publish-pack`

- Add accessibility, source-grounding, AI-safety/bias, privacy, and StudentCard-leakage gates.
- Verify progress/family communications against approved facts and audience rules.
- Verify descriptor-level CEFR alignment whenever an artifact claims a CEFR level; otherwise require a non-certified alignment label.

## Shared education kernel

Create shared contracts and references under `skills/education/_shared/`; these are mandatory dependencies, not skills.

### Contracts

- `learner-evidence-contract`: observation/inference separation, provenance, confidence, counterevidence, expiry, dispute.
- `student-card-contract`: consent, access, retention, pseudonym, safeguarding hold, no-leakage.
- `objective-evidence-contract`: stable objectives, evidence type, authority, scoring status, trajectory export.
- `learning-sequence-contract`: prerequisite graph, coverage, spacing, review, transfer, assessment windows.
- `teacher-action-contract`: evidence-linked reversible hypothesis, teacher approval, success signal, result.
- `accessibility-contract`: WCAG/UDL/non-web document accessibility and accommodations-versus-construct rules.
- `assessment-quality-contract`: validity, reliability, fairness, DIF/bias, rater calibration, security.
- `ai-safety-contract`: grounding, source authority, prohibited inference, human oversight, auditability.
- `communication-contract`: student/family audience, positive factual framing, consent, no sensitive leakage.
- `error-recovery-contract`: valid partial state, retry boundary, failure disclosure, and dependency/version recovery.
- `brief-version-contract`: immutable brief identity, current approved version, downstream dependency assertion, and stale-input rejection.

### References

- learning-science protocols: retrieval, spacing, interleaving, worked examples, cognitive load, transfer, metacognition.
- English oral-language playbook: listening, connected speech, speaking, interaction, pronunciation.
- curriculum authority registry format; actual standards are governed source packs.
- safeguarding, privacy, consent, and jurisdiction matrix.
- structured observation and prohibited-label vocabulary.
- feedback literacy and student voice.

## Platform infrastructure, not skills

- School-controlled StudentCard and evidence persistence.
- Tenant isolation, encryption, audit logs, access control, export, correction, deletion, and legal hold.
- Identity-to-pseudonym mapping.
- Consent registry and withdrawal cascade.
- Objective-evidence/event store.
- Optional teacher dashboard UI.
- Jurisdiction/configuration policy engine.

Skills consume these interfaces; they must not simulate persistence with Markdown files inside installed skill folders.

## Anti-skills

Do not create these as standalone skills:

| Anti-skill | Correct home |
|---|---|
| `zamery-ensure-accessibility` | shared accessibility contract + every artifact owner + review/publish gate |
| `zamery-protect-student-privacy` | shared StudentCard/AI safety contracts + platform policy and access control |
| `zamery-apply-learning-science` | shared learning-science reference consumed by design/practice/sequence/reteaching |
| `zamery-map-english-curriculum` | long-horizon sequence skill; single-unit validation stays in design |
| `zamery-communicate-learning-progress` | monitoring owns facts; material design owns approved communication artifacts |
| `zamery-teach-listening` | expand concept/practice/video/assessment oral-language branches |
| `zamery-teach-speaking` | expand concept/practice/presentation/IELTS oral-language branches |
| `zamery-check-assessment-validity` | assessment composer and shared assessment-quality contract |
| `zamery-create-student-card` | one branch of `zamery-understand-learners`, not a separate workflow |
| `zamery-dashboard` | platform/UI surface, not pedagogical workflow |

## Copilot route order

Recommended conceptual order:

```text
understand_learners
  -> monitor_learning (when prior evidence exists)
  -> sequence_design (term/course requests)
  -> design
  -> concept_teaching
  -> practice / video_learning
  -> item_bank
  -> assessment_composition / ielts_practice
  -> student_work_analysis
  -> monitor_learning
  -> reteach (when a gap is confirmed)
  -> material_design / presentation
  -> review_publish
```

Routes are selected by intent, not all executed every time.

## Phased implementation

### Phase 0 — shared safety and evidence kernel

- Legal/profiling determination and consent/persistence architecture.
- Shared contracts for learner evidence, accessibility, assessment quality, AI safety, and objective evidence.
- Extend review/publish gates.

### Phase 1 — close the learner feedback loop

- Build `zamery-understand-learners` with synthetic data first.
- Build `zamery-monitor-english-learning` once the protected evidence store exists.
- Extend student-work analysis and assessment exports.
- Build `zamery-plan-english-reteaching` and route through concept/practice/reassessment.

### Phase 2 — deepen current teaching artifacts

- Learning-science and oral-language references.
- Enhance lesson, concept, practice, video, item bank, assessment, IELTS, materials, presentations, and publishing.
- Add progress and family communication document types.

### Phase 3 — long-horizon planning

- Build `zamery-design-english-learning-sequences`.
- Connect sequence coverage, spacing, assessments, and lesson briefs.

### Phase 4 — instructional inquiry

- Build `zamery-improve-english-teaching` only after sufficient structured enactment evidence exists.

## Resulting suite

The first target moves the suite from 12 to 16 skills: one user-invoked Teacher Copilot plus 15 model-invoked specialists. The architecture adds only four independently valuable workflows while placing pervasive quality requirements in the shared kernel, where they cannot be skipped by choosing the wrong skill.
