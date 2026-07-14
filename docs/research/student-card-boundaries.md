# StudentCard Boundaries: Evidence-Based and Child-Safe Design

> Research synthesis for the English K-12 teaching copilot StudentCard.
> **Date**: 14 July 2026
> **Purpose**: Establish boundaries so the card supports teachers without diagnosing, stereotyping, or creating self-fulfilling labels.

---

## Table of Contents

1. [Regulatory Foundations](#1-regulatory-foundations)
2. [Learner Profiles & Labeling Effects](#2-learner-profiles--labeling-effects)
3. [SEL Screening vs. Diagnosis](#3-sel-screening-vs-diagnosis)
4. [Personality Testing in Minors](#4-personality-testing-in-minors)
5. [Motivation & Interest Inventories](#5-motivation--interest-inventories)
6. [Teacher Observations](#6-teacher-observations)
7. [Student Voice & Participation](#7-student-voice--participation)
8. [Dynamic Profiling & Self-Fulfilling Prophecies](#8-dynamic-profiling--self-fulfilling-prophecies)
9. [Accommodations & Differentiation](#9-accommodations--differentiation)
10. [Algorithmic Profiling Risks](#10-algorithmic-profiling-risks)
11. [SAFE/UNSAFE Field Table](#11-safeunsafe-field-table)
12. [Recommended Wording](#12-recommended-wording)
13. [Update Cadence Recommendations](#13-update-cadence-recommendations)
14. [Human-Review Rules](#14-human-review-rules)
15. [Counterarguments](#15-counterarguments)
16. [EXPAND](#16-expand)
17. [Source Index](#17-source-index)

---

## 1. Regulatory Foundations

### 1.1 COPPA (Children's Online Privacy Protection Act) — US Federal

**Current status**: The FTC's 2025 COPPA Final Rule compliance deadline was **April 22, 2026**. There is no grace period.

**Key provisions relevant to a StudentCard**:

- **Data minimization** (amended 16 CFR § 312.7): Collection must not exceed what is reasonably necessary to fulfill the specific purpose for which parental consent was given. You **cannot** condition a child's participation on collecting more than that baseline. [Source](https://www.govinfo.gov/content/pkg/FR-2025-04-22/html/2025-05904.htm)

- **Written retention policy** (amended 16 CFR § 312.10): Every category of data must have a documented business necessity, a defined retention period, and a deletion timeframe. The policy must appear in the operator's online notice. [Source](https://blog.promise.legal/coppa-april-2026-amendments-edtech/)

- **Biometric identifiers** now covered: fingerprints, handprints, retina/iris patterns, genetic data. Notably, voice-derived and facial-derived data were **excluded** from the biometric definition after public comment — but audio files containing a child's voice were already covered as personal information. [Source](https://www.govinfo.gov/content/pkg/FR-2025-04-22/html/2025-05904.htm)

- **AI training data** (amended 16 CFR § 312.5(a)(2)): Disclosing children's personal information to third parties to "train or otherwise develop artificial intelligence technologies" is **not integral** to the service and requires **separate verifiable parental consent**. [Source](https://blog.promise.legal/coppa-april-2026-amendments-edtech/)

- **Separate consent mechanisms**: Bundling consent to third-party data disclosure into the same mechanism as consent to collection is now **prohibited**. [Source](https://blog.promise.legal/coppa-april-2026-amendments-edtech/)

- **COPPA 2.0** (House draft, June 2026): Proposes a two-tier age threshold (children under 14, teens 14–17) and a constructive "knows or should have known" knowledge standard. [Source](https://fpf.org/resource/june-2026-redline-comparison-of-the-children-and-teens-online-privacy-protection-act-coppa-2-0/)

### 1.2 FERPA (Family Educational Rights and Privacy Act) — US Federal

FERPA protects the privacy of student education records at any school receiving US Department of Education funds.

- **Directory information** can be disclosed without consent: name, address, telephone number, date/place of birth, honors/awards, dates of attendance. Parents must be notified annually and given a reasonable time to opt out. [Source](https://studentprivacy.ed.gov/ferpa)

- **Non-directory information** requires written parental consent before disclosure — this includes grades, test scores, disability status, disciplinary records, and any psychological/medical information. [Source](https://ies.ed.gov/sites/default/files/national-forum-education-statistics-nfes/document/2025/11/family-educational-rights_0.pdf)

- **School official exception**: Records may be disclosed without consent to school officials with "legitimate educational interest." Third-party ed-tech tools operating under a school contract typically fall under this exception, but FERPA requires the school to define "school official" and "legitimate educational interest" in its annual notification. [Source](https://studentprivacy.ed.gov/sites/default/files/resource_document/file/Superintendents_AnnualNotice_March2025_Final508_0.pdf)

### 1.3 PPRA (Protection of Pupil Rights Amendment) — US Federal

PPRA governs the administration of surveys touching **eight protected areas**. No student shall be required to submit to a survey revealing information concerning:

1. Political affiliations or beliefs (student or parent)
2. **Mental or psychological problems** (student or family)
3. Sex behavior or attitudes
4. Illegal, anti-social, self-incriminating, or demeaning behavior
5. Critical appraisals of close family relationships
6. Legally recognized privileged relationships
7. Religious practices, affiliations, or beliefs
8. Income (except for program eligibility)

→ **Requires prior written parental consent** for surveys in these areas. The StudentCard **must never collect, store, or surface PPRA-protected information** without both (a) explicit school-authorization and (b) individual parental consent. [Source](https://studentprivacy.ed.gov/topic/protection-pupil-rights-amendment-ppra)

### 1.4 UK GDPR / ICO Children's Code — UK

The UK GDPR gives children **specific protection**:

- Recital 38: Children merit "specific protection" regarding personal data, "in particular" for "creating personality or user profiles." [Source](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/what-should-our-general-approach-be-to-handling-children-s-personal-information/)

- **Data minimisation principle** (Article 5(1)(c)): Personal data must be "adequate, relevant and limited to what is necessary" for the stated purpose. [Source](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/)

- **Children's higher protection matters** duty (Article 25, as amended by the Data (Use and Access) Act 2025): When providing an ISS likely to be accessed by children, you must take into account that children "merit specific protection" and "have different needs at different ages and at different stages of development." [Source](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-by-design-and-by-default/)

- Standard 8 (Data minimisation) of the Children's Code: "Collect the minimum amount of personal data needed to deliver an individual element of your service." [Source](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/8-data-minimisation/)

### 1.5 EU AI Act — European Union

The EU AI Act classifies AI in education under **Annex III Area 3** (High-Risk), enforceable **August 2, 2026**:

| Use Case | High-Risk? | Enforceable |
|---|---|---|
| AI determining access/admission to educational institutions | YES | 2 Aug 2026 |
| AI evaluating learning outcomes (grading, essay scoring) | YES | 2 Aug 2026 |
| AI assessing appropriate level of education (placement, course recommendations based on ability) | YES | 2 Aug 2026 |
| AI monitoring prohibited behaviour during exams (proctoring) | YES | 2 Aug 2026 |
| AI tutoring chatbot (no grading, no placement decisions) | LIKELY NOT | Transparency obligations apply |
| Administrative AI (scheduling, not student-facing) | NOT HIGH-RISK | — |

**Prohibited since 2 Feb 2025**: Article 5(1)(f) — emotion recognition systems in education settings.

**Implications for a StudentCard**:
- A StudentCard that surfaces proficiency data to inform placement or course recommendations **likely triggers high-risk classification** under Annex III Area 3(c).
- A StudentCard that passes judgements about "engagement," "wellbeing," or "readiness" risks being treated as evaluating learning outcomes (Area 3(b)).
- **Filter mechanism** (Article 6(3)): Systems performing only "narrow procedural tasks" or that "improve the result of a previously completed human activity" may be exempt — but *profiling* disqualifies the exemption.
- **Human oversight** is mandatory (Article 14).

[Source](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3) | [Source](https://euaicompass.com/eu-ai-act-for-education.html) | [Source](https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-high-risk-systems)

### 1.6 UNESCO — AI in Education

UNESCO's 2021 **Recommendation on the Ethics of Artificial Intelligence** (adopted by all 193 member states) provides the global normative framework:

- **Human-centred approach**: AI should serve the development of human capabilities, guided by human rights principles and protection of human dignity. [Source](https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence)

- **2023 Guidance for GenAI in Education**: Calls for age limits, data privacy mandates, transparency, and human validation of AI systems. Educational institutions must "validate GenAI systems on their ethical and pedagogical appropriateness." [Source](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)

- **Beijing Consensus on AI and Education (2019)**: Affirms AI should "enhance human capacities" and ensure equitable access, supporting marginalised people. [Source](https://unesco.org.uk/site/assets/files/10375/guidance_for_generative_ai_in_education_and_research.pdf)

---

## 2. Learner Profiles & Labeling Effects

### 2.1 The Harm of Labels

A 2023 **multilevel meta-analysis** (60 experiments, 8,295 participants) published in *Educational Psychology Review* found:

- **Moderately negative overall label effect**: Hedges' g = −0.42, robust across evaluation types, diagnostic categories, samples.
- **Label-only condition**: When participants received only a label with no other information, the effect was g = −1.26 — **very large negative effect**.
- Diagnostic labels negatively affected academic evaluations, behavioural evaluations, personality evaluations, and overall assessments.
- **Expertise did not protect against labeling bias**: Trained professionals were as susceptible as non-experts.

**Key interpretation for StudentCard**: Even benevolently-intended labels ("struggling reader," "disengaged," "low motivation") can trigger the same negative cascade of expectations documented for clinical labels.

[Source](https://link.springer.com/article/10.1007/s10648-023-09716-6)

### 2.2 Self-Fulfilling Prophecies (Pygmalion & Golem Effects)

The classic **Rosenthal & Jacobson (1968)** Pygmalion experiment demonstrated that teacher expectations, experimentally induced, produced actual IQ gains in randomly selected "bloomer" students. [Source](https://gwern.net/doc/statistics/bias/1968-rosenthal-pygmalionintheclassroom.pdf)

**Jussim's (2005)** comprehensive review concluded:
- Self-fulfilling prophecies in classrooms do occur, but **effects are typically small**.
- **Powerful self-fulfilling prophecies may selectively occur among students from stigmatized social groups**.
- Teacher expectations predict student outcomes more because they are *accurate* than because they are self-fulfilling — but accuracy and bias can coexist.

[Source](https://journals.sagepub.com/doi/abs/10.1207/s15327957pspr0902_3)

### 2.3 Growth Mindset Interventions

A **national experiment** in the US (Yeager et al., *Nature*, 2019) with a nationally representative sample found:
- A one-hour online growth mindset intervention improved grades among lower-achieving students.
- Effects were sustained in schools where peer norms supported challenge-seeking.
- The intervention did **not** rely on profiling or labeling students — it changed beliefs about the nature of intelligence.

[Source](https://www.nature.com/articles/s41586-019-1466-y)

### 2.4 Stereotype Threat

Research on stereotype threat shows that when students are reminded of negative stereotypes about their group before a task, performance declines. This has been documented across racial/ethnic groups and domains. [Source](https://www.sciencedirect.com/science/article/abs/pii/S0883035521001853)

> **Design implication**: A StudentCard that surfaces group-level attributes or makes comparisons salient (e.g., "behind grade level" or "below average for demographic group") could **trigger stereotype threat**.

---

## 3. SEL Screening vs. Diagnosis

### 3.1 The Distinction

The Wisconsin Department of Public Instruction provides the clearest framework:

| Type | Purpose | Who Interprets | Scope |
|---|---|---|---|
| **SEL Competency Assessment** | Measure student strengths in SEL competencies (e.g., self-management, relationship skills) | Teachers, with training | Not diagnostic, not for grades |
| **Universal SEB Screening** | Identify students at risk for social, emotional, behavioural problems early | School mental health staff | Population-level, early warning |
| **Targeted SEB Assessment** | Determine individual level of risk/resilience, aid diagnosis | Licensed school psychologist, clinical professional | Individual diagnosis |

**Critical rules from DPI**:
- SEL competence assessment scores are **not designed to be used as a grade or score**.
- SEL assessments are **not validated** to identify students for Tier 2/3 intervention.
- **Do not recommend screening for Adverse Childhood Experiences (ACE)** in schools — knowing a student's ACE score does not tell you how the trauma impacts them.
- Using SEL assessment tools to evaluate teacher performance is **not supported**.

[Source](https://dpi.wi.gov/sites/default/files/imce/sspw/pdf/SEL_Competence_Assessment_and_Social_Emotional_and_Behavioral_SEB_Assessment.pdf)

### 3.2 Universal SEB Screening

Best practices from the National Center for School Mental Health and PBIS:
- Universal screeners are intended for **detection of early warning signs**, NOT for diagnosis.
- Screeners have **not been validated** to predict violence or suicide.
- Research has **not supported** the use of screeners to predict violence or suicide.
- Parental consent is **not required** when the respondent is a teacher (PPRA exception).
- Schools must have clear policies on parental notification and opt-out procedures.

[Source](https://smhcollaborative.org/wp-content/uploads/2019/11/universalscreening.pdf)

### 3.3 Validated Instruments

| Instrument | Age Range | Format | What It Measures | Not For |
|---|---|---|---|---|
| **DESSA** (Devereux Student Strengths Assessment) | K–8 | 72-item teacher/parent rating | 8 social-emotional competencies (strength-based) | Diagnosis, grade assignment |
| **BASC-3 BESS** | 3–18 | Brief teacher/parent/student forms | Behavioural and emotional risk index (Externalizing, Internalizing, Adaptive Skills) | Comprehensive diagnosis — flags risk for further assessment |
| **SSIS** (Social Skills Improvement System) | 3–18 | Rating scales | Social skills, problem behaviours, academic competence | Clinical diagnosis alone |

**Implication**: Any validated instrument requires **trained administration and interpretation** by a qualified professional (school psychologist, counsellor). A StudentCard should **never** run or interpret clinical screeners — it should surface *teacher-reported observations* within safe bounds and only if a trained professional has already performed the interpretation.

[Source DESSA](https://measuringsel.casel.org/wp-content/uploads/2018/10/DESSA-User-Manual.pdf) | [Source BASC-3](https://www.pearsonassessments.com/content/dam/school/global/clinical/us/assets/basc-3/basc3-bess-overview.pdf)

---

## 4. Personality Testing in Minors

### 4.1 APA Ethical Standards

The **APA Ethical Principles of Psychologists and Code of Conduct** (Standard 9: Assessment) requires:
- **9.01 Bases for Assessments**: Psychologists base opinions on "information and techniques sufficient to substantiate their findings."
- **9.02 Use of Assessments**: Psychologists use assessment instruments whose validity and reliability have been established for use with members of the population tested.
- **9.03 Informed Consent**: Informed consent must be obtained, including "the nature and purpose of the assessment."

**Key constraint for minors**: Most personality inventories (Big Five, MBTI, NEO-PI-R, MMPI-A) were **standardised on adult or clinical adolescent populations**. Their use in general K-12 classroom settings for non-clinical purposes has **no validity evidence** and violates APA Standard 9.02. [Source](https://www.apa.org/ethics/code)

### 4.2 Why Personality Tests Are Inappropriate for K-12 Classrooms

1. **Lack of age-appropriate norms**: Even adolescent versions expect 14+ reading levels and developmental maturity.
2. **Trait stability is low**: Children's personalities are still developing; labelling a 9-year-old as "introverted" or "high in neuroticism" is developmentally unsound.
3. **No classroom utility evidence**: No peer-reviewed study shows that administering a Big Five inventory to a general K-6 classroom improves instruction, outcomes, or student wellbeing.
4. **Self-fulfilling risk**: A personality label on a StudentCard could shape teacher expectations and student self-concept for years.
5. **Stigmatisation**: Personality labels are sticky and may follow a child across teachers, grades, and schools.

### 4.3 MBTI-Specific Concerns

The Myers-Briggs Type Indicator is **particularly unsuitable**:
- Has poor test-retest reliability (up to 50% of people get a different type on retest).
- Has essentially zero predictive validity for academic outcomes.
- Places individuals into discrete, supposedly fixed categories — maximally dangerous for labeling effects.
- The APA does not endorse its use in educational settings.

---

## 5. Motivation & Interest Inventories

### 5.1 Validated Instruments That Are Safe

#### MUSIC® Model of Academic Motivation Inventory

- **What**: Measures five perceptions about learning: eMpowerment, Usefulness, Success, Interest, Caring.
- **Ages**: Validated with 1st–5th graders (elementary version), middle/high school, and college.
- **Format**: 15 items (elementary version), 4-point Likert scale (No / Maybe / Yes / Definitely Yes).
- **Validity**: Strong CFI (.97–.99), acceptable internal consistency (α = .62–.77 for elementary).
- **Origin**: Developed by Brett D. Jones, based on self-determination theory, social cognitive theory, and interest theory.

**Why it's safe**: The MUSIC Inventory assesses **student perceptions of the learning environment**, not fixed student traits. If a student scores low on "Interest," it tells you the *instruction* needs adjusting, not that the student has a motivation deficit.

[Source](https://doi.org/10.14204/ejrep.38.15081) | [Source](https://www.themusicmodel.com/wp-content/uploads/2024/10/User-Guide-Oct-2024.pdf) | [Source](https://www.themusicmodel.com/questionnaires/)

#### Intrinsic Motivation Inventory (IMI)

- **What**: Measures interest/enjoyment, perceived competence, effort, value/usefulness, felt pressure, perceived choice.
- **Theoretical basis**: Self-Determination Theory (Ryan & Deci).
- **Format**: Varies by study — adaptable subscales.
- **Ages**: Primarily validated with older adolescents and adults; some K-12 use requires adaptation.

[Source](https://selfdeterminationtheory.org/intrinsic-motivation-inventory/)

### 5.2 Safe vs. Unsafe Motivation Constructs

| Safe (Instructional Perceptions) | Unsafe (Fixed Student Traits) |
|---|---|
| "I could do it my way" (empowerment) | "This student is lazy" |
| "What I did was interesting" (interest) | "This student is unmotivated" |
| "My teacher cared about how well I did" (caring) | "This student has a fixed mindset" |
| "I can use what I learned" (usefulness) | "This student has low self-efficacy" |

> **Rule**: Frame all motivational data as **perceptions of the instructional context**, not as attributes of the student.

---

## 6. Teacher Observations

### 6.1 Teacher Judgment Accuracy

Teacher judgments of student ability are **moderately accurate** for academic achievement but are subject to systematic biases:

- **Socioeconomic bias**: Teachers tend to underestimate the abilities of students from low-SES backgrounds.
- **Racial/ethnic bias**: Observed in both academic expectation and behavioural ratings (Gill et al., MET study).
- **Gender bias**: Observed in classroom observation ratings (Vanderbilt/Tennessee study: female teachers score 0.32 SD higher; white teachers score 0.15 SD higher than Black teachers, controlling for value-added measures).

[Source](https://cdn.vanderbilt.edu/vu-my/wp-content/uploads/sites/2824/2021/02/28183837/Teacher_Evaluation_Bias-unblinded.pdf)

### 6.2 Structured Observation Protocols

Structured protocols (CLASS, FFT, PLATO) improve reliability over unstructured judgment but still show:
- **Classroom composition effects**: Teachers with higher percentages of racial/ethnic minority students receive lower CLASS and FFT scores in ELA classes, even when controlling for teaching quality.
- **Cross-context bias**: Protocols developed in one cultural/educational context may produce systematically biased scores when applied in another.

[Source](https://files.eric.ed.gov/fulltext/ED569941.pdf) | [Source](https://link.springer.com/article/10.1007/s11092-022-09394-y)

### 6.3 Design Implication for StudentCard

- **Never hard-code teacher observations as facts** about the student. Instead present them as *teacher-reported perceptions on a specific date in a specific context*.
- **Require structured prompts** for teacher input, not open "notes" fields that invite unchecked bias.
- Include **bias-awareness prompts** before teacher observation entries (e.g., "Consider whether your observation might be influenced by unconscious assumptions about the student's background").

---

## 7. Student Voice & Participation

### 7.1 UNCRC Article 12

Article 12 of the UN Convention on the Rights of the Child gives every child "the right to express their views freely in all matters affecting the child" and for those views to be "given due weight in accordance with the age and maturity of the child."

This is a **legal obligation**, not a pedagogical option. The StudentCard affects the child — therefore **the child has a right to be heard** about what goes on it.

### 7.2 The Lundy Model

Professor Laura Lundy's model operationalises Article 12 into four elements:

| Element | What It Means for the StudentCard |
|---|---|
| **SPACE** | The child must be given a safe, inclusive opportunity to express views about the card. |
| **VOICE** | The child must be facilitated to express their views (e.g., age-appropriate explanation of the card, choice of whether to contribute). |
| **AUDIENCE** | The child's views must be listened to. The teacher must see the child's self-report alongside their own observations. |
| **INFLUENCE** | The child's views must be acted upon, as appropriate. The child should know what was decided and why. |

[Source](https://commission.europa.eu/system/files/2022-12/lundy_model_of_participation_0.pdf) | [Source](https://www.gov.ie/en/department-of-education/publications/student-participation-in-primary-and-post-primary-schools-a-rights-respecting-approach-2024/)

### 7.3 Design Requirements

- **Student self-report must be a first-class field**, not an afterthought. The card should display student voice alongside teacher observations, with clear labelling.
- **Students below age 12 should have an "assent" process** (informed agreement to participate), not just passive consent from parents.
- **Students 12+ should have active participation in any decisions** based on card data that affect their learning pathway.
- **Student-facing explanations must use age-appropriate language** (see ICO Children's Code Standard 2).

---

## 8. Dynamic Profiling & Self-Fulfilling Prophecies

### 8.1 The Empirical Picture

Core findings:
1. **Labels create negative cascades** (meta-analysis: g = −0.42). The less other information available, the more powerful the label (g = −1.26 for label-only). [Source](https://link.springer.com/article/10.1007/s10648-023-09716-6)
2. **Teacher expectations can become self-fulfilling**, especially for stigmatized groups. [Source](https://journals.sagepub.com/doi/abs/10.1207/s15327957pspr0902_3)
3. **Stereotype threat degrades performance** when group identity is made salient in evaluative contexts. [Source](https://www.sciencedirect.com/science/article/abs/pii/S0883035521001853)
4. **Dynamic profiles can entrench disadvantage** through feedback loops: low profile → reduced opportunity → lower performance → reinforced profile.

### 8.2 Council of Europe: Profiling Should Be Prohibited for Children

The Council of Europe **Recommendation CM/Rec(2021)8** on profiling states:

> "Profiling of children should be prohibited by law. In exceptional circumstances, States may lift this restriction when it is in the best interests of the child or if there is an overriding public interest, on the condition that appropriate safeguards are provided for by law."

The Council of Europe's **guidelines on data processing in education** (Convention 108+) reiterate:
> "Profiling of children should be prohibited by law."

[Source](https://rm.coe.int/0900001680a46147) | [Source](https://rm.coe.int/t-pd-2019-6bisrev5-eng-guidelines-education-setting-plenary-clean-2790/1680a07f2b)

### 8.3 Design Countermeasures

| Risk | Countermeasure |
|---|---|
| Fixed labeling | **Temporal framing**: All fields include "as of [date]" — no data exists without time context |
| Self-fulfilling prophecy | **Growth framing**: Surface trajectory not status ("showing improvement in decoding" not "below grade level") |
| Stereotype threat | **No group comparisons**: Never compare a student to demographic, racial, or socioeconomic reference groups |
| Feedback loops | **Staleness detection**: If card data hasn't been updated in >X days, show a warning, not the stale value |
| Single source bias | **Multi-source display**: Teacher observation, student self-report, and assessment data must all be shown side by side |
| Profile inertia | **Decay functions**: Old observations fade; recent data weighted more heavily |

---

## 9. Accommodations & Differentiation

### 9.1 Legal Framework

- **IDEA (Individuals with Disabilities Education Act)**: Students with disabilities are entitled to a Free Appropriate Public Education (FAPE) through an IEP. The IEP team — not an algorithm — determines accommodations.
- **Section 504 (Rehabilitation Act)**: Students with disabilities affecting major life activities are entitled to reasonable accommodations. A 504 plan specifies these.
- **ESSA (Every Student Succeeds Act)**: Requires accommodations for assessments to ensure valid measurement.

### 9.2 What a StudentCard Can and Cannot Do

| Safe | Unsafe |
|---|---|
| Surface that a student has a documented 504/IEP accommodation (with permission from the school/director) | Display the specific diagnosis or disability category |
| Remind teachers of the accommodation (e.g., "extended time on assessments") | Recommend accommodations based on card data (only the IEP/504 team may do this) |
| Allow the teacher to log what accommodations were provided and when | Gate content or assessments based on card data (decision must remain with teacher) |
| Track whether accommodations were delivered (with opt-in from school) | Assign categories of disability severity or risk scores |

### 9.3 Differentiation

The UDL (Universal Design for Learning) framework provides the best model:
- Multiple means of **engagement** (the "why" of learning)
- Multiple means of **representation** (the "what" of learning)
- Multiple means of **action and expression** (the "how" of learning)

A StudentCard should recommend *instructional strategies* aligned to observed needs, **not** place the student in a fixed tier or track.

---

## 10. Algorithmic Profiling Risks

### 10.1 EU AI Act: High-Risk Classification

As noted (§1.5), ANY AI system that:
- Determines access/admission to education → High-risk
- Evaluates learning outcomes (including when used to steer learning) → High-risk
- Assesses appropriate level of education (placement, course recommendations) → High-risk

**A StudentCard that algorithmically suggests placements, tracks, or interventions based on profiling likely triggers all three.**

### 10.2 The Council of Europe's Position

The Council of Europe's preparatory study on regulating AI in education warns:
> "Current regulations do not take the protection of the child and its future self adequately into consideration."

Key risks identified:
- **Automation bias**: Teachers and administrators deferring to algorithmically-generated profiles over their own professional judgment.
- **Black-box profiling**: Systems whose logic cannot be inspected or challenged by teachers, students, or parents.
- **Right to freedom of thought**: AI used to nudge opinions, beliefs, and behaviour in educational settings, including tools that infer attentiveness from brain activity.
- **Permanent record**: A profile created in childhood following the individual into adulthood.

[Source](https://rm.coe.int/regulating-the-use-of-ertificial-intelligence-systems-education-prepar/1680b29928)

### 10.3 UNESCO: Human Oversight Required

UNESCO's guidance requires:
- **Transparency and explainability** — children need to know how AI impacts them.
- **Human oversight** — AI should augment, not replace, teacher judgment.
- **Regular validation** — systems must be tested for bias, fairness, and appropriateness.

[Source](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)

### 10.4 UNICEF: Child-Centred AI

UNICEF's Policy Guidance on AI for Children (v3.0, 2025) outlines nine requirements:
1. Support development and well-being
2. Ensure inclusion
3. Prioritize equity and non-discrimination
4. Protect data and privacy
5. Ensure safety
6. Provide transparency, explainability, accountability
7. Provide governments and businesses with knowledge
8. Prepare children for AI developments
9. Create an enabling environment

[Source](https://www.unicef.org/innocenti/reports/policy-guidance-ai-children) | [Source](https://www.unicef.org/innocenti/media/1341/file/UNICEF-Global-Insight-policy-guidance-AI-children-2.0-2021.pdf)

---

## 11. SAFE/UNSAFE Field Table

### 11.1 Safe Fields — May Be Included (with safeguards)

| Field Name | Data Type | Example | Risk Level | Justification |
|---|---|---|---|---|
| `student_name` | String | "Alex Chen" | SAFE | Directory info per FERPA; opt-out available |
| `grade_level` | Enum | "3" | SAFE | Directory info; necessary for contextualising observations |
| `teacher_name` | String | "Ms. Rodriguez" | SAFE | Professional record |
| `teacher_observed_strengths` | Text (structured, from checklist) | "Actively participates in group discussions" | SAFE | Positive, contextualised, from structured prompt |
| `student_self_reported_interest` | Likert (1-4) | "3" (Yes) | SAFE | Student perception of instruction, not student trait; from validated instrument (MUSIC) |
| `student_self_reported_efficacy` | Likert (1-4) | "2" (Maybe) | SAFE | Same as above; instructional perception |
| `instructional_strategies_used` | Tags | "visual_aids, kinesthetic, collaborative_learning" | SAFE | Describes what teacher did, not student deficit |
| `accommodations_documented` | Bool + Enum | true, "extended_time" | SAFE | Only if school-authorised; shows flag, not diagnosis |
| `date_of_entry` | ISO 8601 | "2026-09-15" | SAFE | Temporal context for all entries |
| `lesson_engagement_pattern` | Structured tags from validated teacher menu | "focused_during_independent_work" | SAFE | Behavioural observation, not trait inference |
| `goal_set_by_teacher_and_student` | Text (co-authored) | "Student will increase reading stamina by 5 minutes over 4 weeks" | SAFE | Co-constructed, student-involved, growth-oriented |

### 11.2 Caution Fields — Include Only with Explicit Safeguards

| Field Name | Data Type | Example | Risk Level | Safeguard |
|---|---|---|---|---|
| `teacher_observed_concern` | Text (structured menu, no free text) | "Difficulty sustaining attention during 15+ min independent tasks" | CAUTION | Must use structured prompt; paired with strength; dated; must have human review before surfacing |
| `seb_screener_result_summary` | Enum (from licensed screener) | "Within normal range" | CAUTION | Only if administered by school psychologist; only summary score, never raw item responses |
| `iep_504_flag` | Bool | true | CAUTION | Only with school authorisation; must not reveal diagnosis category |
| `attendance_pattern` | Structured tags | "late_arrival_3_times_this_month" | CAUTION | Must be factual, not inferential ("disengaged" vs. "arrived late to 3 sessions") |
| `student_self_reported_wellbeing` | Likert (1-4) | "2" (Sometimes) | CAUTION | PPRA-protected area; requires prior written parental consent; must be voluntary for student |
| `parent_reported_insight` | Text (structured) | "Parent notes student feels anxious about tests" | CAUTION | Parent-provided; require explicit consent; no clinical interpretation |

### 11.3 UNSAFE Fields — Must NEVER Be Included

| Field Name | Reason for Prohibition | Regulatory/Research Basis |
|---|---|---|
| `personality_type` (e.g., "INTJ", "high in neuroticism") | No validity for K-12 classroom use; high labeling risk | APA Standard 9.02; labeling meta-analysis (g=-0.42) |
| `clinical_diagnosis` (e.g., "ADHD", "dyslexia") | Violates FERPA; requires clinical training to interpret; creates labels | FERPA non-directory; IEP team only; labeling meta-analysis |
| `mental_health_score` (e.g., "depression screener: 8/27") | PPRA-protected area; requires licensed clinician; cannot be processed by AI | PPRA §1232h(b)(2); APA Standard 9 |
| `predicted_future_outcome` (e.g., "at risk of dropout") | No validated predictive model for individual K-12 students; algorithmic profiling risk | EU AI Act Annex III; Council of Europe CM/Rec(2021)8 |
| `family_income` or `socioeconomic_status` | PPRA-protected; stereotype threat risk; data minimisation violation | PPRA §1232h(b)(8); GDPR Article 5(1)(c) |
| `race_or_ethnicity` | High discrimination risk; stereotype threat trigger; not necessary for teaching | EU AI Act non-discrimination; UNESCO human-centred AI |
| `religion` | PPRA-protected; not relevant to English instruction | PPRA §1232h(b)(7) |
| `biometric_data` (facial recognition, fingerprint, voiceprint) | COPPA-regulated; not necessary for StudentCard function | COPPA amended 16 CFR §312.2 |
| `emotion_recognition_data` | Prohibited in education by EU AI Act Article 5(1)(f); no evidence of pedagogical utility | EU AI Act Art. 5(1)(f), enforceable since Feb 2025 |
| `label_terms` (e.g., "struggling reader", "low motivation", "disengaged") | Creates self-fulfilling prophecy; label effects even with rich context | Labeling meta-analysis (g=-1.26 for label-only); Jussim review |
| `comparative_ranking` (e.g., "bottom quartile", "below average for demographic") | Stereotype threat; no pedagogical value; demoralising | Stereotype threat research; growth mindset research |
| `teacher_free_text_notes` (unstructured) | Invites unchecked bias; cannot be audited for fairness | Teacher bias research (Vanderbilt study; Gill et al.) |

---

## 12. Recommended Wording

### 12.1 Do's and Don'ts

| Instead of This (UNSAFE) | Use This (SAFE) |
|---|---|
| "Struggling reader — below grade level" | "Currently reading at Level L. Working on inferencing strategies. Showing 2-level improvement since September." |
| "Unmotivated / disengaged" | "During 15+ min independent reading, student redirected to task 3 times. Engaged well in 1:1 setting." |
| "ADHD" | Has documented [accommodation type] per school-authorised plan." |
| "Low self-efficacy" | "Student self-report: 'Maybe I can do well' on MUSIC Success scale." |
| "At risk" | "3 unexcused absences this month. Teacher observation: needs support with [specific skill]." |
| "Introverted personality" | "Prefers written response over oral presentation. Participates actively in small groups of 2-3." |
| "Behaviour problem" | "Interrupted instruction 4 times during 30-min lesson on [date]. Teacher used [strategy] with [effect]." |
| "Behind peers" | Current level: [specific objective]. Target for next 4 weeks: [specific objective]." |

### 12.2 Wording Rules

1. **Observable behaviours only**: Describe what the student *did* ("arrived late 3 times"), not what they *are* ("tardy").
2. **Context-attached**: Every observation tied to a specific task, setting, and date.
3. **Counterexample included**: "Struggled with inference during whole-group reading (but identified main idea correctly in 1:1 setting)."
4. **Strengths first**: Any concerning observation must be preceded or accompanied by an observed strength.
5. **Student-authored content**: Student self-report must be shown verbatim, not paraphrased or interpreted by the system.
6. **No labels**: The system must have a **blocklist** of prohibited label terms that cannot be stored or displayed.
7. **Temporal framing**: Every data point formatted as "As of [date]: [observation]" — never as a permanent descriptor.

---

## 13. Update Cadence Recommendations

| Data Category | Update Cadence | Rationale | Safety Mechanism |
|---|---|---|---|
| **Student self-report (interest/efficacy)** | Every 4-6 weeks | Motivational climate changes with instruction | Automated re-administration; never re-use stale data |
| **Teacher observation (structured)** | Every 2-4 weeks | Frequent enough to see change, slow enough to avoid surveillance | Old observations archived but not displayed by default after 1 term |
| **Assessment/skill level** | Per completed assessment unit (typically 2-6 weeks) | Aligned to curriculum units | Must include date and assessment type |
| **Accommodation/504/IEP** | Per school/academic year or when document updated | Legal document; not a dynamic attribute | Requires school admin re-verify annually |
| **Attendance data** | Real-time (per session) | Operational necessity | Only factual (present/late/absent); no inference |
| **SEB screener summary** | Per school screening cycle (typically 1-2x/year) | Clinical instruments require trained administration | Must be discarded after one cycle; never accumulate |
| **Behavioural observation** | Per incident, aggregated monthly | Pattern detection requires sufficient data points | Never fewer than 3 observations before a pattern is noted |
| **Student goals** | Set termly; reviewed mid-term | Growth-oriented; co-constructed | Auto-archive at end of term; must be re-set |
| **Parent-provided insight** | Per parent opt-in cycle | Consent can be withdrawn at any time | Re-verify consent termly; delete immediately on withdrawal |

**Retention policy (COPPA-mandated)**: All data must have a defined deletion date. Default recommendation:
- Current and previous term: retained and accessible
- Older than 2 terms: archived, not visible by default
- Older than 1 academic year: permanently deleted unless required for legal/regulatory hold (documented separately)

---

## 14. Human-Review Rules

### 14.1 Decisions That REQUIRE a Trained Human (No Automation)

| Decision | Who Must Review | Basis |
|---|---|---|
| Interpreting SEB screener results | Licensed school psychologist or counsellor | APA Standard 9; Wisconsin DPI guidance |
| Determining placement or track change | Teacher + parent + school administrator (IEP team if applicable) | EU AI Act Annex III Area 3(c); IDEA |
| Flagging a student for mental health concern | School counsellor or psychologist (not the system) | PPRA; suicide/violence screening limitations |
| Modifying an accommodation or IEP | IEP team (including parent) | IDEA; Section 504 |
| Assigning a clinical or diagnostic label | Licensed clinical professional; never the AI system | APA Standard 9.02; labeling meta-analysis |
| Overriding a student's self-reported data | Teacher + student (with student present) | Lundy model — student voice & influence |
| Making a consequential decision based on card data | Teacher + parent + student (age-appropriate) | UNCRC Article 12; EU AI Act Art. 14 |

### 14.2 Decisions Where a Teacher May Act Alone (With System Support)

| Decision | Why OK | Safeguard |
|---|---|---|
| Adjusting next lesson's instructional strategy | Within professional scope; low stakes | Recommendation is a suggestion, not a directive |
| Logging a structured observation | Teacher is the source of the observation | Must use structured menu, not free text; bias prompt shown |
| Setting a short-term learning goal (with student) | Co-constructed; reversible | Must involve student; documented |
| Flagging concerning attendance pattern for follow-up | Factual; reversible | Must be based on ≥3 instances |
| Selecting a different UDL modality for a lesson | Instructional decision; reversible | Track what was tried and what happened |

### 14.3 Automated Actions — Extremely Limited

| Automated Action | Condition | Why Safe |
|---|---|---|
| Archiving stale data | >2 terms old | Non-destructive; reversible by teacher |
| Reminding teacher of accommodation | Only if documented in school-authorised plan | Factual; teacher acts on reminder or ignores |
| Showing trajectory ("improving", "stable", "needs attention") | Based on ≥3 data points over ≥6 weeks | Descriptive of trend, not predictive; always teacher-interpreted |
| Decay weighting older observations | Algorithmic, but visible and overridable | Transparency; teacher can see and override weight |

**What must never be fully automated**:
- Flagging a student for any intervention
- Altering content difficulty or pacing without teacher approval
- Generating any comparative ranking
- Sending any notification to parents about student behaviour or wellbeing
- Locking/changing a student's learning pathway

---

## 15. Counterarguments

### "Other ed-tech apps already do this."

| Counterargument | Response |
|---|---|
| "Other apps profile students with personality tests and behavior scores." | Those apps are **not compliant** with the evolving regulatory landscape. The 2025/2026 COPPA amendments, the EU AI Act (enforcing Aug 2026), and the Council of Europe's prohibition on child profiling represent a **step change** in regulatory enforcement. Compliance by comparison to current market practice is not a legal defence. |
| "ClassDojo/X app already tracks behavior points." | Behaviorist point systems have been **widely criticised** by child development researchers for public shaming, fixed-mindset reinforcement, and lack of evidence. The UK Children's Commissioner called for their regulation in 2022. The StudentCard should learn from these failures, not replicate them. |
| "This is standard practice in personalised learning platforms." | Most "personalised learning" platforms operate in a regulatory grey area. The StudentCard should be designed for the regulatory environment of 2027+, where algorithmic profiling of children is increasingly prohibited or tightly constrained. |

### "Teachers already know this information. We're just digitising it."

| Counterargument | Response |
|---|---|
| "A structured card is the same as what teachers already hold in their heads." | Research on **teacher expectation bias** shows that unstructured teacher impressions are **not neutral** — they are shaped by race, class, and gender biases (Vanderbilt study; Gill et al.). Digitising and systemising those impressions **amplifies** their power by making them persistent, shareable, and seemingly objective. |
| "Digital records are more accurate than memory." | Accuracy is not the same as fairness. A more accurate record of biased observations is not an improvement — it is bias at scale. |
| "Every good teacher has mental profiles of their students." | The difference between a mental model and a digital profile: the mental model is updated continuously, forgotten over time, and not shared wholesale. The digital profile is persistent, transmissible, and carries institutional authority. |

### "It's just for personalisation — adapting content to their level."

| Counterargument | Response |
|---|---|
| "We need profiling to deliver personalised instruction." | **Effective** personalised instruction does **not require** fixed profiling. It requires *responsive teaching* — moment-by-moment adjustments based on observable performance. The EU AI Act distinguishes between "evaluating learning outcomes to steer learning" (high-risk) and adaptive tutoring that adjusts to immediate responses (likely not high-risk if no profiling). |
| "Netflix-style recommendations for learning." | Education is not content consumption. Algorithmic recommendations based on profiling can create filter bubbles in learning, narrowing rather than expanding a student's exposure. The right to a broad, balanced curriculum is undermined by narrowcasting based on a profile. |
| "Without profiles, the AI can't personalise." | A StudentCard can support personalisation through **current, observable performance data** (what they've mastered and what's next), without needing personality traits, motivation scores, or behaviour profiles. This is how good teachers have always done it. |

### "We need this data for the AI to work well."

| Counterargument | Response |
|---|---|
| "Better data means better AI recommendations." | This is **data maximisation** — the opposite of COPPA's data minimisation duty (amended 16 CFR §312.7) and GDPR Article 5(1)(c). More data does not mean better outcomes; it often means noisier, more biased, and more harmful outcomes. |
| "We're building a model of the student." | The Council of Europe recommends **prohibiting** the profiling of children. Building a model of a child is precisely what this means. Your model will be wrong (models are simplifications), and the consequences of that wrongness fall on the child. |
| "The AI needs historical data to predict." | Then your AI may not be appropriate for children. Predictive models of individual children have **no validated accuracy** for academic outcomes, and the harm of false positives/negatives is borne by the child. Consider whether the feature truly requires prediction. |

### "But parents/caregivers would want to know about wellbeing concerns."

| Counterargument | Response |
|---|---|
| "Parents need to be informed about their child's mental health." | Yes — but through **appropriate channels** (teacher call, counsellor referral, parent-teacher conference), not through an automated system. The PPRA lists mental/psychological problems as a protected area requiring prior written consent. Automated wellbeing flagging bypasses this. |
| "Early warning systems save lives." | There is **no evidence** that algorithmic early warning systems prevent suicide or self-harm in K-12 populations (Best Practices in Universal SEB Screening, 2021). Screeners are not validated for this purpose. The most effective suicide prevention remains direct human relationship — teacher noticing, counsellor checking in. |
| "If we see signs of distress, we should act." | Yes — the teacher should act. But the system should **not** independently detect, classify, or flag distress. The system can provide a *structured channel* for a teacher to log a concern they've already identified, which then goes to the appropriate human (counsellor, not another system). |

---

## 16. EXPAND

The following questions and edge cases deserve further investigation before implementation:

### 16.1 The "Dashboard-Nudging" Problem

If the StudentCard's UI is designed to draw teacher attention to certain students (e.g., colour-coded indicators, sorting by "needs attention"), does this constitute algorithmic profiling or steering of teacher behaviour even if no explicit profile is created? The EU AI Act's definition of "AI system" under Article 3(1) is broad enough that a dashboard that prioritises teacher attention algorithmically may itself be a high-risk AI system. **Needs**: legal analysis of whether UI prioritisation falls within the AI Act's scope.

### 16.2 Age-Differentiated Tiers

The available evidence suggests very different implications for:
- **K–2**: Near-universal unsuitability of formal profiling; reliance on teacher observation; developing self-report capacity.
- **Grades 3–5**: Self-report becomes more reliable (MUSIC validated); minimal abstraction ability for personality constructs.
- **Grades 6–8**: Increased self-awareness; but also increased stereotype threat vulnerability and labelling sensitivity.
- **Grades 9–12**: Approaching adult capacity; greater autonomy rights (FERPA transfers at 18).

**Needs**: Systematic review of age-graded recommendations for each StudentCard data type. Current research does not provide per-age granularity.

### 16.3 The "Opt-In / Opt-Out Cascade"

Under COPPA (2025 amendments), consent mechanisms must be:
- Separate for different purposes
- Individually revocable
- Reconcilable with school-authorisation exceptions

Under the EU AI Act, deployers must conduct a Fundamental Rights Impact Assessment (FRIA). For a StudentCard, a "cascade" emerges:
1. School authorises the tool (FERPA school-official exception)
2. Parent consents to data collection (COPPA)
3. Student assents to participation (UNCRC Article 12)
4. Student consents to specific uses of self-report data at a certain age

**Needs**: A consent architecture that satisfies all four layers without creating unworkable complexity. This is an unsolved design problem.

### 16.4 Transferability Across Jurisdictions

The StudentCard must work across:
- US federal law (COPPA, FERPA, PPRA, IDEA)
- State-level student privacy laws (CA, NY, IL, TX increasingly regulate ed-tech)
- UK GDPR / ICO Children's Code
- EU AI Act (if deployed to EU users or if student data originates in EU)
- Council of Europe Framework Convention on AI (if ratified)

A field that is "safe" under US law may be "unsafe" under the UK GDPR or EU AI Act. **Needs**: Cross-jurisdictional compliance mapping before field specification.

### 16.5 Longitudinal Effects of Student Self-Monitoring

Does the act of having a StudentCard — even a safe one — change how students see themselves? Research on the **reflexive effects of measurement** (Hacking's "looping effects") suggests that when people are classified, they change their behaviour in response to the classification. A StudentCard that asks a 7-year-old to rate their own "interest" or "success" weekly may inadvertently teach them to see themselves through a fixed lens of performance metrics.

**Needs**: Pre/post research design to measure whether a StudentCard implementation changes student self-concept, academic identity, or metacognitive awareness — and in what direction.

---

## 17. Source Index

| # | Source | URL |
|---|---|---|
| 1 | COPPA Final Rule (FTC, Apr 2025, effective Jun 2025, compliance Apr 2026) | https://www.govinfo.gov/content/pkg/FR-2025-04-22/html/2025-05904.htm |
| 2 | COPPA April 2026 Amendments — EdTech Analysis | https://blog.promise.legal/coppa-april-2026-amendments-edtech/ |
| 3 | COPPA 2.0 Redline Comparison (FPF, Jun 2026) | https://fpf.org/resource/june-2026-redline-comparison-of-the-children-and-teens-online-privacy-protection-act-coppa-2-0/ |
| 4 | FERPA Statute and Regulations (US DOE) | https://studentprivacy.ed.gov/ferpa |
| 5 | FERPA Annual Notice Template (US DOE, Mar 2025) | https://studentprivacy.ed.gov/sites/default/files/resource_document/file/Superintendents_AnnualNotice_March2025_Final508_0.pdf |
| 6 | PPRA Overview (US DOE) | https://studentprivacy.ed.gov/topic/protection-pupil-rights-amendment-ppra |
| 7 | 20 USC §1232h — Protection of Pupil Rights | https://www.law.cornell.edu/uscode/text/20/1232h |
| 8 | UK GDPR Data Minimisation Principle (ICO) | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/ |
| 9 | UK GDPR — Children's Higher Protection Matters (ICO, Feb 2026) | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-by-design-and-by-default/ |
| 10 | UK GDPR — Specific Protection for Children (ICO) | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/what-should-our-general-approach-be-to-handling-children-s-personal-information/ |
| 11 | ICO Children's Code Standard 8 — Data Minimisation | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/8-data-minimisation/ |
| 12 | EU AI Act — Annex III (High-Risk Systems) | https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3 |
| 13 | EU AI Act — Education AI Classification Guide | https://euaicompass.com/eu-ai-act-for-education.html |
| 14 | EU AI Act — Draft High-Risk Classification Guidelines (2026) | https://table.media/assets/documents/draft_guidelines_on_the_classification_of_high_risk_ai_annex_iii_7mxr3yiz2gw3uppjpwvvndd8ioi_128561.pdf |
| 15 | UNESCO Recommendation on Ethics of AI (2021) | https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence |
| 16 | UNESCO Guidance for GenAI in Education (2023) | https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research |
| 17 | UNESCO AI in Education — Policy Guidance | https://www.unesco.org/en/articles/ai-and-education-guidance-policy-makers |
| 18 | APA Ethical Principles of Psychologists and Code of Conduct | https://www.apa.org/ethics/code |
| 19 | APA Guidelines for Psychological Assessment and Evaluation | https://mindremakeproject.org/wp-content/uploads/2023/08/APA-Guidelines-for-Psychological-Assessment-Evaluation.pdf |
| 20 | APA — Standardized Assessment in PreK-12 Education | https://www.apa.org/science/programs/testing/standardized-assessment-testing-education.pdf |
| 21 | Labeling Effects Meta-Analysis (Educ Psych Review, 2023) | https://link.springer.com/article/10.1007/s10648-023-09716-6 |
| 22 | Teacher Expectations & Self-Fulfilling Prophecies (Jussim, 2005) | https://journals.sagepub.com/doi/abs/10.1207/s15327957pspr0902_3 |
| 23 | Pygmalion in the Classroom (Rosenthal & Jacobson, 1968) | https://gwern.net/doc/statistics/bias/1968-rosenthal-pygmalionintheclassroom.pdf |
| 24 | Growth Mindset National Experiment (Yeager et al., Nature 2019) | https://www.nature.com/articles/s41586-019-1466-y |
| 25 | Stereotype Threat & English Learners (ScienceDirect, 2022) | https://www.sciencedirect.com/science/article/abs/pii/S0883035521001853 |
| 26 | SEL Competence Assessment vs SEB Screening (Wisconsin DPI) | https://dpi.wi.gov/sites/default/files/imce/sspw/pdf/SEL_Competence_Assessment_and_Social_Emotional_and_Behavioral_SEB_Assessment.pdf |
| 27 | Best Practices in Universal SEB Screening (2021) | https://smhcollaborative.org/wp-content/uploads/2019/11/universalscreening.pdf |
| 28 | DESSA Manual (CASEL) | https://measuringsel.casel.org/wp-content/uploads/2018/10/DESSA-User-Manual.pdf |
| 29 | BASC-3 BESS Overview (Pearson) | https://www.pearsonassessments.com/content/dam/school/global/clinical/us/assets/basc-3/basc3-bess-overview.pdf |
| 30 | MUSIC Motivation Inventory — Validation (Jones & Sigmon, 2016) | https://doi.org/10.14204/ejrep.38.15081 |
| 31 | MUSIC Inventory User Guide (Jones, 2024) | https://www.themusicmodel.com/wp-content/uploads/2024/10/User-Guide-Oct-2024.pdf |
| 32 | MUSIC Model — Questionnaires | https://www.themusicmodel.com/questionnaires/ |
| 33 | Intrinsic Motivation Inventory (SDT) | https://selfdeterminationtheory.org/intrinsic-motivation-inventory/ |
| 34 | Teacher Observation Bias — MET Study (Gill et al., IES) | https://files.eric.ed.gov/fulltext/ED569941.pdf |
| 35 | Teacher Observation Bias — Race/Gender (Vanderbilt, 2021) | https://cdn.vanderbilt.edu/vu-my/wp-content/uploads/sites/2824/2021/02/28183837/Teacher_Evaluation_Bias-unblinded.pdf |
| 36 | Observation Bias Across Contexts (Educ Assessment, 2022) | https://link.springer.com/article/10.1007/s11092-022-09394-y |
| 37 | Lundy Model of Participation (UNCRC Article 12) | https://commission.europa.eu/system/files/2022-12/lundy_model_of_participation_0.pdf |
| 38 | Student Participation — Rights-Based Approach (Gov.ie, 2024) | https://www.gov.ie/en/department-of-education/publications/student-participation-in-primary-and-post-primary-schools-a-rights-respecting-approach-2024/ |
| 39 | Council of Europe — Profiling Recommendation CM/Rec(2021)8 | https://rm.coe.int/0900001680a46147 |
| 40 | Council of Europe — Data Processing in Education (Convention 108+) | https://rm.coe.int/t-pd-2019-6bisrev5-eng-guidelines-education-setting-plenary-clean-2790/1680a07f2b |
| 41 | Council of Europe — AI in Education Preparatory Study (2024) | https://rm.coe.int/regulating-the-use-of-ertificial-intelligence-systems-education-prepar/1680b29928 |
| 42 | Council of Europe — Children & AI Mapping Study (2024) | https://rm.coe.int/cdenf-2024-04-mapping-study-children-and-artificial-intelligence-/1680b212f8 |
| 43 | UNICEF Policy Guidance on AI for Children (v3.0, 2025) | https://www.unicef.org/innocenti/reports/policy-guidance-ai-children |
| 44 | UNICEF AI for Children — Policy Guidance v2.0 (2021) | https://www.unicef.org/innocenti/media/1341/file/UNICEF-Global-Insight-policy-guidance-AI-children-2.0-2021.pdf |
