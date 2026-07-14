# StudentCard: Design Note for Implementation

**Status:** architecture direction accepted; implementation and real-student pilots blocked until the legal, consent, persistence, and safeguarding gates below are closed
**Purpose:** help teachers understand each learner well enough to choose better teaching moves, assignments, lesson structure, and learning materials without diagnosing, stereotyping, or fixing the learner into a permanent category.  
**Research basis:** [`docs/research/student-card-boundaries.md`](../../../docs/research/student-card-boundaries.md)

## Decision

Add a new learner-understanding layer to the Zamery suite with four distinct objects:

1. **StudentCard** — a longitudinal, teacher-governed record of dated learner evidence.
2. **ClassProfile** — a privacy-safe aggregate of the class, used for whole-class planning.
3. **Learner Context Snapshot** — the minimum current context copied into a Teaching Brief for one lesson, unit, or intervention.
4. **Teacher Action Plan** — Copilot recommendations framed as reversible teaching hypotheses, approved by the teacher and evaluated after use.

Do **not** put the full StudentCard inside the Teaching Brief. The brief is lesson/class scoped; the card is learner scoped and longitudinal. The brief receives only the minimum snapshot needed for the current purpose.

## Hard gates before implementation

No production schema, persistence, integration, or real-student pilot may begin until all of these are documented and approved:

1. **Jurisdiction and profiling determination** — qualified legal/privacy review determines whether the proposed records, aggregates, snapshots, recommendations, and dashboard behaviour constitute prohibited child profiling under applicable Council of Europe rules or high-risk education AI under the EU AI Act. If they do, the project either implements every required conformity, FRIA, logging, human-oversight, contestability, and monitoring obligation or removes the triggering behaviour. Engineering cannot self-exempt the system.
2. **Purpose and field-level consent architecture** — each field category has a named educational purpose, lawful/authorised basis, school authority, parent/guardian consent requirement, student assent/participation rule, permitted consumers, expiry, retention, and independently revocable consent status. Withdrawal blocks future snapshots and starts the documented deletion cascade.
3. **School-controlled persistence design** — cards live in a tenant-isolated, access-controlled, encrypted school store outside the installed skill package. The store separates the school's identity mapping from the pseudonymous card, records every access/change/export, and supports correction, legal hold, consent withdrawal, and verified deletion. No cloud or model-training use is allowed by default.
4. **Safeguarding protocol** — student or parent input that contains possible serious harm, abuse, or acute distress is held from StudentCard ingestion and shown only to an authorised human with the school's existing safeguarding instructions. The system does not score, diagnose, classify risk, or choose an intervention. Emergency and statutory reporting decisions remain entirely with trained humans under school policy.
5. **Age and deployment policy** — the school defines age-appropriate assent, explanation, self-report, observation, and challenge processes for each grade band before collection begins. Until validated age-specific thresholds exist, the system may not algorithmically infer a behavioural trend for K–2 and may only show dated observations for older learners after teacher review.

Synthetic data may be used to prototype schemas and validation while these gates are open. That prototype must not process or persist real student information.

## Why this belongs in the suite

The current Teaching Brief already mentions `confidence/profile` and support needs, but does not define their structure, provenance, validity, expiry, or effect on downstream skills. `zamery-analyze-student-work` produces strong evidence about errors and misconceptions, but that evidence does not persist into later teaching decisions. StudentCard closes this loop:

```text
learner evidence
  -> StudentCard
  -> ClassProfile / Learner Context Snapshot
  -> Teaching Brief
  -> lesson, explanation, practice, materials, assessment
  -> observed response and student work
  -> reviewed StudentCard update
```

## Canonical language

| Avoid | Canonical term | Meaning |
|---|---|---|
| personality profile | participation and communication patterns | What the learner currently does in specific settings, not who the learner permanently is. |
| psychological profile | authorised support context | Human-approved support or accommodation information; never an AI diagnosis. |
| naughty / disruptive | contextual behaviour observation | A dated description of what happened, where, and after which teacher move. |
| lazy / unmotivated | task-engagement evidence | Observable persistence, completion, help-seeking, and response to task design. |
| addicted to games | reported game-study conflict | A student/parent-reported or directly observed scheduling conflict; not a clinical label. |
| low ability | current objective evidence | What the learner can currently demonstrate against named objectives. |
| visual/auditory learner | effective conditions tried | Which representations or response modes helped in a specific learning episode. |
| intervention prescribed by AI | teaching hypothesis | A reversible strategy suggestion requiring teacher approval and later review. |

## The Learner Discovery Pack

The input should not be one omnibus personality test. It should be a short, multi-source discovery pack with separate purposes and consent boundaries.

### A. Academic diagnostic

- Current evidence against named English objectives.
- Grade and CEFR remain independent; CEFR is never inferred from school grade.
- Evidence may include a baseline assessment, recent work, oral performance, or teacher-authorised records.
- Results report demonstrated strengths, next objectives, error patterns, and uncertainty rather than an ability label.

### B. Student voice

- Interests and topics the learner wants to encounter.
- Goals the learner helps set.
- Confidence or perceived success for the current subject/context.
- Preferred participation modes as a choice, not a learning-style diagnosis.
- What the learner says helps or blocks learning.

Student voice is shown verbatim and separately from teacher interpretation. It is reviewed every 4–6 weeks because motivation and confidence change with instruction.

Each self-report field declares whether it is ordinary instructional feedback or a protected wellbeing/psychological survey item. Protected items are disabled by default and cannot be collected through StudentCard unless the school has approved the instrument, the required parent/guardian consent exists, the student can decline, and a qualified human owns interpretation.

### C. Structured teacher observation

Each observation records:

- date and learning context;
- task and objective;
- observable action;
- strength or successful condition;
- support or teacher move tried;
- immediate effect;
- counterexample, if one exists;
- observer and evidence source.

Free-form labels are not accepted. For grades 3–12, three relevant observations is only an operational minimum for a teacher-reviewed descriptive pattern, not a validated inference threshold. K–2 shows observations without algorithmic trend language. The pilot must evaluate and replace these conservative rules with age-appropriate evidence before wider use.

### D. Optional parent/caregiver input

- Interests and routines relevant to learning.
- Practical scheduling constraints.
- Strategies that have helped at home.
- Parent-authorised support context selected from approved instructional fields.

Parent input uses structured choices and purpose-limited short answers. Validation blocks health/diagnosis, psychological, family-conflict, income, religion, disciplinary, identity, and other sensitive content from entering StudentCard; such content is held for the appropriate authorised human process rather than copied into the card.

### E. Authorised accommodations

StudentCard may surface an approved action such as `extended_time` or `text_to_speech_allowed`. Every action records the authorising plan/team, source record reference, approved scope, effective date, expiry/review date, and verification status. It must not store or infer the underlying diagnosis. The relevant school team, not Copilot, owns accommodation decisions.

## Mapping the teacher's proposed factors

| Proposed factor | Keep? | Safe representation | Copilot may do | Copilot must not do |
|---|---:|---|---|---|
| Personality | Reframed | Contextual participation, communication, response and independence patterns | Suggest group size, response mode, wait time, rehearsal, or private-to-public progression | Store MBTI/Big Five type; call the learner introverted, stubborn, anxious, or difficult |
| English level | Yes | Objective-linked evidence, independently supplied CEFR, dated assessment evidence | Adjust scaffolding, entry point, vocabulary load, model complexity, and practice sequence | Derive CEFR from grade; lower the common objective without teacher approval; issue an official diagnosis/band |
| Psychology / wellbeing | Not as a profile | Human-authorised support context or a teacher concern routed to a qualified person | Remind the teacher to follow an authorised support process | Screen, diagnose, infer emotions, assign risk, or recommend treatment |
| Naughty / disruptive behaviour | Yes, reframed | Context + observable action + frequency + teacher move + effect | Suggest classroom routines, task chunking, movement, choice, pre-correction, reinforcement, or restorative conversation | Store a character label, rank behaviour, predict misconduct, or notify parents automatically |
| Playing too many games | Yes, reframed | Reported schedule conflict, missing-work pattern, game interests, and learner/parent goals | Use game themes or mechanics selectively; propose micro-tasks, implementation intentions, study routines, and a teacher-approved home plan | Diagnose addiction, use games as the only motivator, punish, manipulate, or infer home behaviour |
| Interests | Yes | Student-authored interest tags with review date | Select examples, texts, projects, contrasts, and authentic communicative purposes | Narrow the curriculum into an interest filter bubble |
| Confidence | Yes | Context-specific learner self-report plus performance evidence | Adjust rehearsal, success criteria, feedback timing, and public response demand | Treat confidence as a stable personality trait |
| Attention / persistence | Yes, carefully | Observable duration and context, support tried, and effect | Adjust task length, breaks, cues, modality, and monitoring | Infer ADHD or emotional state |

## StudentCard contract

The contract should be deliberately evidence-heavy and interpretation-light.

```yaml
student_card:
  schema_version: zamery-student-card.v1
  card_id: pseudonymous-local-id
  owner: teacher-or-school
  purpose: instructional-support
  consent:
    school_authority: documented
    field_scopes: purpose-authority-parent-status-student-status-consumers-expiry
  lifecycle:
    created_at: date
    reviewed_at: date
    next_review_at: date
    delete_at: date
  student_voice:
    interests: dated-verbatim-values
    goals: co-authored-goals
    perceived_success: context-specific-self-report
    participation_choices: dated-choices
  learning_evidence:
    objective_evidence: dated-evidence-references
    independently_supplied_cefr: optional
    strengths: dated-observations
    error_patterns: evidence-references-with-confidence
    misconceptions: evidence-references-with-competing-explanations
  learning_conditions:
    observations: context-action-support-effect-records
    strategies_tried: strategy-result-records
  interests_and_routines:
    interest_tags: student-or-parent-supplied
    reported_schedule_conflicts: factual-and-consented
  authorised_support:
    accommodations: action-source-authority-scope-effective-expiry-verification
  disputes:
    entries: evidence-id-student-response-status-reviewer-decision-reason-resolved-at
  provenance:
    each_field: source-authority-date-confidence-expiry
```

### Required metadata for every evidence item

- `source`: student, teacher, parent/caregiver, assessment, or authorised school record;
- `authority`: who is allowed to make the statement;
- `observed_at`;
- `context` and objective when applicable;
- `evidence_id`: a stable card-local identifier used by disputes, snapshots, and action plans;
- `evidence_reference`;
- `confidence`: low, medium, or high for interpretations;
- `counterevidence` or competing explanation;
- `expires_at`;
- `reviewed_by` and review status.
- `consent_scope_id` for every student/parent-supplied or protected field;
- `dispute_status`, preserving student and teacher views side by side until a human resolves the entry.

No statement may exist as an undated permanent learner trait.

## Prohibited fields and outputs

- Personality type or trait score.
- Clinical diagnosis, disability category, psychological score, mental-health risk, or emotion-recognition result.
- Predicted dropout, misconduct, future attainment, or other future-outcome score.
- Race, religion, family income, socioeconomic rank, or demographic comparison.
- Comparative class ranking or labels such as `low`, `weak`, `lazy`, `naughty`, `unmotivated`, `addicted`, or `problem student`.
- Unstructured teacher notes.
- Raw PII in evidence copied into downstream artifacts.
- Any automatic placement, track, intervention, accommodation, parent notification, or change to assessment construct.

Although a real name can be directory information in some US contexts, this contract deliberately excludes it. The school retains the identity-to-card mapping separately to minimise re-identification and cross-skill leakage.

## ClassProfile

Whole-class lesson design should not read every StudentCard directly. Copilot produces a minimum aggregate ClassProfile:

- distribution of current objective evidence;
- common demonstrated strengths;
- common misconceptions with evidence counts;
- approved accessibility and modality requirements;
- participation conditions that affect whole-class enactment;
- interest clusters only when large enough to avoid re-identification;
- outlier needs represented as teacher-only planning constraints, not public labels.

ClassProfile never includes names, card IDs, diagnoses, individual behaviour narratives, or sensitive parent/student reports. Small-group aggregates use a minimum group threshold defined before implementation.

ClassProfile does not resolve contradictory evidence into a single score. It displays source-specific counts, dates, uncertainty, and disagreement. Copilot must not create a weighted learner-confidence, engagement, behaviour, readiness, or risk score.

## Learner Context Snapshot

For individual practice, tutoring, or reteaching, Copilot may create a time-bounded snapshot containing only:

- current objective and success evidence;
- demonstrated prerequisite evidence;
- relevant strengths and misconceptions;
- authorised accommodations;
- recently effective or ineffective teaching strategies;
- one or two current interests if useful;
- current learner goal;
- evidence dates and expiry.

The teacher approves the snapshot before it is used. The full StudentCard is never passed to content-generation or publishing skills.

## Teacher Action Plan contract

Every Copilot recommendation is a testable hypothesis:

```yaml
teacher_action:
  action_id: stable-id
  based_on_snapshot_id: approved-snapshot-id
  snapshot_expires_at: date
  target: named-objective-or-observed-barrier
  evidence_ids: dated-source-references
  proposed_move: concrete-reversible-teaching-action
  rationale: why-this-might-help
  preserves:
    - shared-objective
    - assessment-construct
    - learner-dignity
  trial_window: one-to-three-sessions
  expected_signal: observable-success-evidence
  teacher_approval: required
  result: not-yet-tried | helped | mixed | did-not-help
  confounding_factors: teacher-reviewed-context
  teacher_interpretation: optional-attribution-not-fact
  review_date: date
```

This design stores not only “what the learner did,” but also “what teaching was tried and what happened.” That prevents the system from placing every failure inside the learner.

## Effect on each skill

| Skill | StudentCard-derived input | Allowed adaptation | Guardrail |
|---|---|---|---|
| `zamery-teacher-copilot` | ClassProfile or approved snapshot | Route learner discovery, prepare action options, preserve evidence across handoffs | Never expose full card to downstream skills; teacher approves recommendations |
| `zamery-design-english-learning` | ClassProfile | Entry point, prerequisite repair, grouping, pacing, UDL choices, differentiation | Shared objectives remain; avoid fixed tiers |
| `zamery-teach-english-concepts` | ClassProfile or individual snapshot | Examples, contrasts, explanation depth, response mode, misconception checks | Interests are hooks, not curriculum limits; no learning-style claims |
| `zamery-build-english-practice` | Approved snapshot | Chunk size, scaffolds, response framing, retrieval schedule, near-to-far transfer | Support preserves objective; challenge is not merely more work |
| `zamery-build-english-item-banks` | Curriculum/construct needs, not individual cards | Improve coverage of known misconception families | Reusable banks must not encode one learner's profile |
| `zamery-compose-english-assessments` | Authorised accommodations and construct evidence | Accessible administration and teacher-approved diagnostic selection | No personality/behaviour adaptation; construct and scoring remain valid |
| `zamery-create-ielts-practice` | Current objective evidence and approved snapshot | Target criterion practice and feedback focus | No official band inference; no altered IELTS task-family rules |
| `zamery-build-video-learning` | ClassProfile | Chunking, captions, transcript support, pause points, relevant topics | Media authority and learning objective remain primary |
| `zamery-design-teaching-materials` | ClassProfile accessibility constraints | Font, spacing, response space, modality and scaffold presentation | No StudentCard data appears in student-facing artifacts |
| `zamery-create-english-presentations` | ClassProfile | Pacing, participation prompts, visual density, teacher notes | No named learner cues on projected slides |
| `zamery-analyze-student-work` | Prior approved snapshot plus current work | Add objective evidence, error patterns, probes, smallest reteaching move | Observation remains separate from inference; no diagnosis |
| `zamery-review-publish-pack` | Usage manifest, not card contents | Verify purpose limitation, privacy, accessibility, and no label leakage | Block publication if card data or prohibited labels leak |

## Copilot behaviour

When StudentCard context exists, Copilot should:

1. Confirm the current purpose: class planning, individual teaching, practice, diagnostic assessment, or reteaching.
2. Select the minimum ClassProfile or snapshot fields needed for that purpose.
3. Show the teacher what evidence is current, stale, conflicting, or missing.
4. Produce two or three plausible teaching moves rather than one deterministic prescription.
5. Explain which evidence supports each move and what could disconfirm it.
6. Require teacher approval before generating dependent artifacts.
7. Define an observable signal and review window.
8. After teaching, ask what happened and update the strategy-result record only after human review.

Copilot must say “insufficient evidence” when appropriate. It must not fill gaps with psychological or motivational inference.

Before using an interest hook, Copilot verifies that objective and curriculum coverage are unchanged. Every multi-session sequence includes contexts beyond recorded interests, and the teacher can inspect how often each interest has been used. Interests diversify access to the curriculum; they never narrow it.

## Aha-moment design

StudentCard can improve genuine insight moments by helping Copilot choose:

- a familiar interest as the surface context;
- a contrast pair linked to a demonstrated misconception;
- a prediction before explanation;
- a counterexample that breaks the current rule;
- a representation that previously helped in a similar task;
- a student-authored explanation or teach-back;
- a near-transfer task followed by a contextually different far-transfer task.

The insight mechanism remains conceptual conflict plus reconstruction. Game themes, visuals, stories, or preferred response modes are delivery choices, not the source of learning by themselves.

## Lifecycle and governance

1. **Authorise purpose** — define why the card exists and which data categories are needed.
2. **Obtain school authority, parent consent where required, and age-appropriate student assent.**
3. **Collect minimally** through the Learner Discovery Pack.
4. **Redact, safeguard, and validate** all free-text evidence; hold sensitive or serious-concern content outside StudentCard for authorised human handling.
5. **Teacher and student review** the first card; preserve disagreements rather than overwriting one view.
6. **Generate ClassProfile or snapshot** for a specific teaching purpose.
7. **Teacher approves action plan and artifacts.**
8. **Record teaching strategy and result.**
9. **Review and expire** observations on their cadence.
10. **Delete** data when purpose, consent, or retention period ends.

Default review cadence follows the research baseline:

- student interests/confidence: 4–6 weeks;
- structured teacher observations: 2–4 weeks;
- academic evidence: per completed unit or diagnostic event;
- behavioural pattern: at least three observations, reviewed monthly;
- accommodations: when the authorised plan changes and at least annually;
- parent input/consent: re-confirm each term;
- data older than two terms: hidden by default;
- data older than one academic year: delete unless an authorised retention requirement applies.

The school's named data controller authorises any retention exception, records its legal/operational basis and end date, and reviews it before expiry. The card-level `next_review_at` is always the earliest required field review or consent expiry; expired fields are excluded from snapshots until renewed.

## Direction after hard-gate closure

Introduce a model-invoked specialist skill tentatively named **`zamery-understand-learners`**. It owns:

- Learner Discovery Pack orchestration;
- StudentCard validation and review;
- ClassProfile generation;
- Learner Context Snapshot generation;
- the teacher-action hypothesis contract;
- consent, provenance, expiry, and deletion checks.

It does not own academic assessment item generation or psychological screening. It delegates academic diagnostics to assessment composition, evidence analysis to student-work analysis, and finished artifacts to the existing specialist skills.

The Teacher Copilot routes through `zamery-understand-learners` before design when longitudinal learner context is available or explicitly requested.

## Implementation work to prepare

1. Specify JSON schemas for StudentCard, ClassProfile, snapshot, and Teacher Action Plan.
2. Implement the approved school-controlled persistence boundary and local pseudonym mapping; do not store cards inside the installed skill package.
3. Encode the approved cross-jurisdiction privacy, purpose, and field-level consent matrix.
4. Define field-level access control, audit history, correction, export, and deletion.
5. Add prohibited-label validation and structured-observation menus.
6. Extend Teaching Brief with references to ClassProfile/snapshot IDs and provenance, not full card content.
7. Update `impact_diff`: authorised accommodations and objective evidence may be material; interests and participation preferences remain advisory.
8. Add routing and regression tests for learner discovery, stale snapshots, consent withdrawal, conflicting evidence, and card-data leakage.
9. Extend review/publish with a StudentCard privacy gate.
10. Pilot with a small teacher cohort and explicitly measure false assumptions, teacher overrides, student corrections, workload, and learning impact before broader release.

Runtime validators must reject prohibited fields and labels, missing/expired authority or consent, stale snapshots, unresolved safeguarding holds, absent evidence IDs, and downstream artifacts containing StudentCard identifiers or protected content. Audit tests must prove the correction, consent-withdrawal, deletion, and no-leakage flows end to end.

## Acceptance criteria for the future implementation

- Every recommendation links to dated evidence and a teacher-approved purpose.
- Every interpretation is distinguishable from observation and includes confidence and counterevidence.
- No personality, diagnosis, emotion recognition, predicted outcome, comparative ranking, or prohibited label can be stored.
- Students can contribute, view age-appropriate explanations, challenge an entry, and have stale/wrong entries corrected.
- Consent withdrawal prevents future use and triggers the configured deletion process.
- Whole-class generation consumes ClassProfile, not individual cards.
- Individual generation consumes only an approved, time-bounded snapshot.
- Shared objectives and assessment constructs cannot be silently changed by a card.
- Card content cannot leak into student-facing or published artifacts.
- The system records whether a recommended teaching move helped, not only whether the learner complied.
- Serious-concern content is never stored as a card attribute or algorithmic risk result; it follows the school's human safeguarding route.
- No real-student use occurs without documented jurisdiction/profiling determination and approved persistence/consent architecture.

## Final assessment

The proposed idea is strategically important and should be implemented, but its value comes from **responsive teaching**, not from creating a digital personality dossier. The safest and most pedagogically useful design understands the learner through current evidence, student voice, context, and response to teaching; it then offers teacher-controlled experiments that can be revised when the evidence changes.
