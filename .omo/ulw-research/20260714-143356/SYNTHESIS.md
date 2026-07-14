# Education Skills Suite — Saturation Audit Synthesis

**Workers:** 7 (3 corpus + 3 evidence + 1 red-team)  
**Waves:** 1 primary + EXPAND  
**Sources:** 200+ (150+ research + 30+ regulatory + 40+ codebase references)  
**Date:** 2026-07-14

---

## Executive Summary

The Zamery education skill suite (`skills/education/`) is **structurally comprehensive**: it covers the entire teaching cycle from lesson design → concept teaching → practice → item banking → assessment → IELTS → video learning → materials design → presentations → student-work analysis → review/publish. The Copilot router (`zamery-teacher-copilot`) handles entry; shared contracts enforce field disciplines; six quality gates gate output.

The audit found that the suite is **strong in pedagogical depth** (concept teaching references 4 methodologies with board-plan contracts; error taxonomy is granular; feedback protocol is structured) but **exhibits systemic gaps in learner-protection infrastructure, accessibility, AI safety, teacher workflow enablers, and closed-loop evidence**.

The most critical finding: **the suite has no learner-protection framework** — no WCAG/UDL baseline, no AI hallucination/bias mitigation, no accommodations-vs-construct-validity framework, no feedback literacy protocol, no COPPA/FERPA/GDPR compliance matrix, no EU AI Act classification. These are regulatory requirements in most target markets (Vietnam, UK, EU), not nice-to-haves.

The second major gap: **teacher workflow is under-designed**. The suite focuses on *artifact generation* but not on *classroom enactment* — there is no progress tracking, no curriculum mapping, no intervention/MTSS support, no student/family communication, no post-lesson reflection, no adaptive/sequential release, no portfolio, no lesson observation framework.

---

## Findings by Domain

### 1. Core Learning Design (design → concept → practice)

**Strengths:**
- `zamery-design-english-learning`: Solid blueprint contract; grade/CEFR mapping; objective decomposition; methodology selection; 5-stage lesson template (Launch→Notice→Test→Build→Transfer)
- `zamery-teach-english-concepts`: Deep methodology registry (PPP, TBLT, GRR, CI); board-plan contract; inverse-thinking protocol; domain playbooks for grammar/vocab/pronunciation/reading/writing/listening/speaking
- `zamery-build-english-practice`: Exercise catalog with 15+ distinct types; practice progression model; differentiation support/challenge axis; U-shaped learning emphasis

**Gaps:**
- No misconception library / common-error catalog
- No explicit schema-building / prior-knowledge activation phase in any design
- No spacing/review/revision schedule support
- Differentiation is *designed* (support/challenge axis) but not *scaffolded* — no graduated prompts, no tiered exit tickets, no flexible grouping guidance
- Aha moments are hoped for, not *engineered* — no insight-triggering patterns (contrast pairs, critical incidents, prediction-errors)
- Transfer design is present but untested — no near→far transfer progression contracts

### 2. Assessment & Feedback (item-banks → assessments → IELTS → student-work)

**Strengths:**
- `zamery-build-english-item-banks`: Solid canonical item model, 7-axis question taxonomy, batch generation with seed dedup, storage policies
- `zamery-compose-english-assessments`: Blueprint contracts, form A/B/C design, answer-set contracts, rubric design with criteria/levels
- `zamery-create-ielts-practice`: Official task-family constraints, labeling/disclaimers, authority-reference, writing/speaking feedback rubric
- `zamery-analyze-student-work`: PII redaction, error taxonomy (10+ categories), probing-question protocol, feedback structure (success→next→retry)

**Gaps:**
- **No validity framework**: Item-bank quality references item-writing heuristics but not AERA/APA/NCME Standards validity argumentation
- **No reliability/precision evidence**: No SEM reporting, no decision-consistency for mastery decisions, no subgroup confidence intervals
- **No DIF / bias detection**: Items have no bias review (gender, culture, SES); no differential-item-functioning analysis
- **No psychometric linking**: No equating, no vertical scaling for growth, no form-equivalence beyond "same blueprint"
- **Feedback is structured but not feedback-literate**: No Carless&Boud model, no Molloy 7-group framework; feedback as "message" rather than "process"
- **Reteaching is single-shot**: Analyze-student-work suggests probes then reteaching, but no protocol exists for *how* to reteach based on diagnosis
- **IELTS rubrics lack inter-rater calibration**: Teachers get rubrics but no calibration exercise, no benchmarked exemplars, no moderation

### 3. Media & Publishing (video → materials → presentations → review-publish)

**Strengths:**
- `zamery-build-video-learning`: Media-source authority contract; transcript policy; learning-sequence design; H5P export
- `zamery-design-teaching-materials`: Branded DOCX/PDF templates; teacher-guide/worksheet/workbook/answer-key contracts; data-format policy with per-format validation
- `zamery-create-english-presentations`: Deck contract; slide-pedagogy principles; teacher-notes-and-safety contract
- `zamery-review-publish-pack`: Six quality gates (Brief→Pedagogy→Content→Safety→Presentation→Pack); pack-manifest contract

**Gaps:**
- **No accessibility gate**: Six quality gates do not include WCAG, UDL, color-contrast, font-size, or alt-text verification
- **No screen-reader / assistive-tech QA**: Outputs are DOCX/PDF/PPTX — none include aria, alt-text, heading-structure, or semantic-reading-order verification
- **Video accessibility is thin**: Captions/transcripts present but no audio-description, no sign-language, no interactive-transcript for neurodivergent learners
- **Print-to-digital translation missing**: No guidance for how worksheet/worksheet designs survive translation to mobile/web platforms
- **Teacher guide is template-heavy, coaching-light**: The guide includes "watch-for" callouts but no actual teaching-move recommendations based on evidence

### 4. System Architecture & Routing (Copilot → shared contracts → orchestration)

**Strengths:**
- `zamery-teacher-copilot`: Robust routing with ROUTE_ORDER, impact_diff for field-level change detection, CONTENT_INTENTS, semantic revision, teaching-brief as boundary object
- Shared contracts: brand, contracts.py data models, fixtures, tests for route_advisor
- Impact_diff properly surfaces cross-skill blast radius

**Gaps:**
- **Unrouted artifacts**: `workbook`, `exam_pack` routed to `material_design` but no corresponding intent/quality gate — they reach publishing without pedagogical sign-off
- **No error-recovery path**: If a skill fails mid-generation, there's no protocol for rollback, partial delivery, or degradation
- **No retry/iterate loop**: Assessment feedback from student-work analysis does not feed back into item-bank or lesson design
- **Teacher-copilot has no "I don't know" path**: For ambiguous/unhandled requests, copilot has no graceful handoff to human
- **Teaching brief is not signed**: No version-lock between design and downstream consumers — downstream skills may use stale briefs
- **No observability**: No instrumentation to measure which routes are failing, which handoffs lose fidelity, which skills are never invoked
- **Tests exist but are incomplete**: route_advisor has tests; impact_diff has none; shared contract tests are thin

### 5. Learning Science & Workflow — External Evidence Baseline

**Key Evidence Anchors:**
- Retrieval practice: g=0.40-0.80 (Roediger & Karpicke; Agarwal et al. 2021 K-12)
- Spacing effect: g=0.46-0.71 (Cepeda et al. 2006); no spacing support in suite
- Interleaving: g=0.42 (Foster et al., Butler); no interleaving in practice or assessment
- Worked examples: d=0.57 (Renkl); no worked-example phase in any design skill
- Transfer: g=0.40-0.75 near, g=0.15-0.30 far; no far-transfer contract
- Dual coding / multimedia learning: g=0.38-0.72 (Mayer); present in design but not enforced in materials

**Missing Capabilities (ranked by impact):**
| Rank | Capability | Evidence | Current State |
|------|-----------|----------|---------------|
| 1 | Spaced/repetition schedule | g=0.46-0.71 | Absent |
| 2 | Retrieval-practice integration | g=0.40-0.80 | Not systematic |
| 3 | Progress tracking / analytics | High teacher demand | Absent |
| 4 | Lesson observations / coaching | High impact | Absent |
| 5 | Family communication (homework) | Equity requirement | Absent |
| 6 | Adaptive / sequential release | g=0.30-0.50 (Cognitively-based) | Absent |
| 7 | Intervention / MTSS | Tiered instruction evidence | Absent |
| 8 | Student portfolios | Formative assessment best practice | Absent |
| 9 | Curriculum mapping / alignment | Teacher workload reduction | Absent |
| 10 | Post-lesson reflection / revision loop | Reflective practice evidence | Not systematic |
| 11 | AI as Socratic tutor | 14 studies 2018-2024 | Not addressed |
| 12 | Automated item generation psychometrics | IAG research frontier | Not addressed |

### 6. English Pedagogy — Evidence vs Current Practice

**Strong alignment:** Vocabulary, grammar, pronunciation, reading, writing instruction domains — current skill contracts align well with high/moderate-high evidence domains.

**Critical mismatches:**
- **Listening instruction** (d=0.25): Suite has no dedicated listening skill. Video-learning partially covers it but listening as a *standalone skill* is absent.
- **Speaking instruction**: No dedicated speaking skill. IELTS covers some speaking but general K-12 speaking practice is absent.
- **Translanguaging** (low evidence, high risk of bias): Not addressed, which is *correct* — but no guidance for multilingual contexts.
- **Culturally Responsive Teaching** (zero causal evidence): Not addressed; suite is language-agnostic.
- **CEFR alignment**: Present in design but no ongoing verification that output actually maps to CEFR descriptors.

### 7. Assessment, Access, Safety — Regulatory & Standards Baseline

**Immediate Regulatory Pressure:**
- **EU AI Act (Reg 2024/1689)**: Art.14 human oversight, Annex III high-risk classification for learning-outcome evaluation → `compose-assessments` and `analyze-student-work` likely high-risk
- **COPPA 2026** (Apr 22 deadline): Biometric identifier expansion includes voiceprints → `analyze-student-work` with speech assessment needs new consent flows
- **FERPA**: Student inputs = education records; `analyze-student-work` must guarantee data deletion at contract termination
- **WCAG 2.2**: US DOJ Title II enforcement Apr 2026/2027 → all digital materials must meet WCAG 2.1 AA

**Learner Protection Gap (Current Suite Level 0-1 out of 3):**
- WCAG conformance: **Level 0** — no baseline, no VPAT
- UDL integration: **Level 0** — no CAST 3.0 framework reference
- Neurodiversity guidance: **Level 0** — no specific ADHD/dyslexia/autism guidance
- AI hallucination: **Level 0** — no RAG, no confidence scoring, no fact-check protocol
- AI bias mitigation: **Level 0** — no fairness audit, no stratified evaluation
- Teacher-in-the-loop: **Level 1** — six quality gates serve as human review but no blind-mode protocol
- Privacy/PII: **Level 2** — strong redaction but no FERPA/COPPA/GDPR compliance matrix
- Accommodations framework: **Level 0** — no interaction hypothesis, no construct-vs-accommodation mapping
- Feedback literacy: **Level 1** — feedback structured correctly but not framed as a literacy
- Rubric quality: **Level 2** — analytic rubrics exist but no inter-rater reliability protocol

---

## Cross-Skill System Seams

| Seam | Gap | Contradiction | Enhancement |
|------|-----|---------------|-------------|
| Design → Concept Teaching | Design produces objectives; concept teaching receives them but no dependency-hint | Concept teaching may teach different thing than designed | Teaching brief should carry more than objectives (examples, contrasts, known misconceptions) |
| Concept → Practice | Practice independently selects exercise types | No guarantee practice exercises align with taught concept depth | Practice should receive concept-did-not-stick signal and adjust |
| Practice → Item Bank | Different taxonomies (exercise-catalog vs question-taxonomy) | Cognitive levels/evaluation dimensions may diverge | Practice exercises and item banks share 7-axis taxonomy |
| Item Bank → Assessment | Assessment composes from bank but can skip items | No "blueprint coverage" assertion — assessment may miss construct dimensions | Assert form coverage against blueprint before generation |
| Assessment → Student Work | Different feedback models (rubric vs error-taxonomy) | Two feedback sources with no reconciliation | Gradebook unified feedback model |
| Student Work → Reteach | Student work analysis generates reteaching suggestions | No skill exists to *execute* reteach | Reteach-loop skill |
| Copilot → Downstream | Brief carries intent, not evidence | Assessment outcomes don't feed back to design brief | Brief-synesis protocol |
| Materials → Review-Publish | Materials designed independently of review gates | Six gates not conditioned on material type | Gate-per-artifact-type configuration |

---

## Prioritized Enhancements

### P0 — Regulatory & Safety (Imminent Risk)

1. **AI hallucination/bias mitigation**: RAG grounding + source confidence scoring + human-in-the-loop verification protocol. Must precede any production release.
2. **WCAG/UDL/Neurodiversity baseline**: Audit all 11 skills against WCAG 2.2, CAST UDL 3.0, neurodiversity guidance; document conformance gaps per skill.
3. **COPPA 2026 compliance**: Protect child audio and other personal information, separate consent for model-training disclosure, and establish purpose-limited retention and deletion contracts.
4. **EU AI Act classification**: Classify each skill per Annex III; implement Art.14 human oversight for high-risk routes; document FRIA.
5. **Privacy/Data compliance matrix**: FERPA school-official exception, COPPA verifiable parental consent, GDPR 72-hour breach notification per skill.

### P1 — Learning Science Integration

6. **Spacing/review schedule contract**: Add retrieval-practice schedule as optional cross-skill contract; practice sets and assessments should be sequenced per spacing principles.
7. **Transfer design contract**: Differentiate near, medium, far transfer in lesson design; practice and assessment must sample all transfer levels.
8. **Worked-example phase**: Add worked-example with self-explanation prompts to concept-teaching and practice skills.
9. **Listening instruction skill**: New specialist skill — listening currently under-designed given d=0.25 evidence.
10. **Speaking instruction skill**: New specialist skill — speaking practice absent except IELTS.

### Cross-Cutting Learner Understanding Layer — Direction with Hard Gates

Add a teacher-governed **StudentCard** system, implemented as four bounded objects: a longitudinal StudentCard, a privacy-safe ClassProfile, a minimal Learner Context Snapshot for one teaching purpose, and a reversible Teacher Action Plan. The discovery process collects academic evidence, student voice, structured teacher observations, optional parent input, and authorised accommodations. It does not administer personality tests, psychological screening, emotion recognition, or predictive risk scoring. Implementation and real-student pilots are blocked until jurisdiction/profiling review, field-level consent, school-controlled persistence, safeguarding, and age-specific policies are approved.

StudentCard is intended to close the current loop from student-work evidence back into lesson design, teaching, practice, and materials. Copilot should derive two or three evidence-linked teaching hypotheses, require teacher approval, define an observable success signal, and later record whether the teaching move helped. Full design, field boundaries, lifecycle, per-skill effects, and future acceptance criteria are recorded in [`STUDENT-CARD-DESIGN-NOTE.md`](./STUDENT-CARD-DESIGN-NOTE.md). The child-safety and regulatory evidence baseline is in [`docs/research/student-card-boundaries.md`](../../../docs/research/student-card-boundaries.md).

The suite-level conversion plan is recorded in [`SKILL-ARCHITECTURE-PROPOSAL.md`](./SKILL-ARCHITECTURE-PROPOSAL.md). It recommends four first-target specialist skills (`zamery-understand-learners`, `zamery-monitor-english-learning`, `zamery-plan-english-reteaching`, and `zamery-design-english-learning-sequences`), a later evidence-dependent instructional-inquiry skill, targeted enhancements to all current specialists, and a mandatory shared education kernel for learning science, accessibility, assessment quality, learner evidence, privacy, consent, AI safety, and communication.

### P2 — Workflow & Teacher Enablement

11. **Progress tracking + student dashboard**: Teacher-facing evidence of student performance across items, skills, CEFR levels over time.
12. **Reteach-loop skill**: New skill that receives student-work analysis, identifies patterns, and regenerates differentiated instruction.
13. **Curriculum mapping / syllabus alignment**: Teacher-facing view of which skills cover which standards over the term.
14. **Family communication templates**: Automated home-support letters in instruction language + languages spoken at home.
15. **Classroom discourse / interactive decision-making guidance**: Add "teacher moves" playbook to lesson design, not just board plan.
16. **Differentiation execution engine**: From "support/challenge" design to actual scaffolded tiered materials with graduated prompts.

### P3 — Assessment & Psychometric Rigor

17. **Validity argument framework**: Integrate AERA/APA/NCME Standards validity evidence structure into assessment contracts.
18. **DIF / bias detection protocol**: Add gender/culture/SES bias review protocol to item-bank QA gates.
19. **Reliability estimation**: Add SEM reporting, decision-consistency for mastery/classification decisions.
20. **Inter-rater reliability protocol**: Add teacher calibration exercises; benchmarked writing/speaking exemplars with scored commentary.
21. **Form-equivalence beyond blueprint**: Add parallel-form equating design (not just same blueprint).

### P4 — System & Infrastructure

22. **Observability instrumentation**: Measure route failure rates, handoff fidelity, skill-utilization frequency.
23. **Error recovery / partial delivery protocol**: When a downstream skill fails, what does the system promise?
24. **Teaching brief version-lock**: Downstream skills assert "brief version X is current" before generation.
25. **Copilot "I don't know" path**: Graceful human-handoff for ambiguous/unhandled requests.
26. **Unrouted artifact governance**: `workbook` and `exam_pack` need pedagogical QA before `material_design` route.
27. **Impact_diff test coverage**: No tests exist for the only cross-skill change-impact tool.

### P5 — Evidence Baselines That Exist But Deserve Attention

28. **Pronunciation AI tools**: MALL/CAPT rapidly evolving — AI-generated speech as pedagogical input is uncharted.
29. **AI as scaffold for writing**: 14 studies show cognitive/creative benefits but dependency risk — should inform practice design.
30. **Multilingual Science of Reading**: SOR for MLs must include L1 transfer, cross-linguistic decoding, balanced literacy + SOR.
31. **CEFR descriptor verification**: Output alignment to CEFR should be verifiable, not just asserted per skill.
32. **CRP/CRT evidence gap documentation**: Document the zero-causal-evidence finding in equity design decisions.

---

## Contradictions & Open Questions

| Issue | Finding | Unresolved? |
|-------|---------|-------------|
| **Translanguaging effectiveness** | 4/5 positive studies high risk of bias | Yes — use as pedagogical principle, not evidence-based technique |
| **Pronunciation instruction effect** | d=0.89 but most studies lack delayed post-test | Partially — immediate effects are robust |
| **Listening instruction effect** | d=0.25 — concerningly low | Yes — major gap needing new skill |
| **Culturally Responsive Teaching evidence** | Zero studies meeting WWC standards | Yes — ethical principle, not evidence-based pedagogy |
| **UDL achievement evidence** | g=0.43 but only 20 eligible studies | Yes — moderate confidence |
| **Hattie's d=0.79 feedback effect** | EPPI 2021 revision estimates d=0.17-0.48 | Yes — sue with caution, not as fixed benchmark |
| **Marks+comments impact** | Butler (1988): negative; contested by newer studies | Partially — comments-without-marks recommended |

---

## Expansion Trace

| Wave | Axis | Workers | Leads Gained | Leads Closed |
|------|------|---------|-------------|-------------|
| 1 | Corpus — design/learning | 1 | 2 | 2 |
| 1 | Corpus — assessment/feedback | 1 | 4 | 4 |
| 1 | Corpus — media/publishing | 1 | 3 | 3 |
| 1 | Red-team — routing/system | 1 | 5 | 5 |
| 1 | Evidence — learning science/workflow | 1 | 8 | 8 |
| 1 | Evidence — language pedagogy | 1 | 5 | 5 |
| 1 | Evidence — assessment/access/safety | 1 | 10 | 10 |

**Convergence Reason:** All leads either investigated to closure (incorporated into synthesis findings) or explicitly deferred to implementation phase. Zero unchecked leads remain.

---

## Methodology

- **Corpus workers**: Exhaustive file read + structural search + git history + test audit for each assigned skill group
- **Evidence workers**: 10-15+ distinct websearch + Context7 queries per domain; cross-referencing against systematic reviews, meta-analyses, government/regulatory sources; active counter-search for contested claims
- **Red-team worker**: Adversarial analysis seeking contradictions, blind spots, and optimistic-bias failures across all findings
- **Epistemic control**: intent-diff.md (5 intentions tracked), claim-graph.md (5 claims, all supported), observation-manifest.md, verification-economics.md, cause-disappearance.md in session journal

---

## Key Sources

See individual worker reports for complete 200+ citation list. Representative pillars:

- AERA/APA/NCME Standards for Educational and Psychological Testing (2014)
- WCAG 2.2 (W3C, Oct 2023) https://www.w3.org/TR/WCAG22/
- CAST UDL Guidelines 3.0 (July 2024) https://udlguidelines.cast.org/
- EU AI Act (Regulation 2024/1689) https://eur-lex.europa.eu/eli/reg/2024/1689
- COPPA (2025 amendments, compliance Apr 2026)
- Feedback Literacy (Carless & Boud, 2018) doi:10.1080/02602938.2018.1463354
- Norris & Ortega (2000) FFI meta-analysis
- Graham et al. (2023) writing meta-analysis
- Ludwig et al. (2019) ELL reading meta-analysis
- Agarwal et al. (2021) retrieval practice K-12 meta-analysis
- Cepeda et al. (2006) spacing meta-analysis
- Black & Wiliam (1998) formative assessment review
- Yao et al. (2024) K-12 FA meta-analysis
