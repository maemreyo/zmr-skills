# StudentCard Contract

The contract is deliberately evidence-heavy and interpretation-light.

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

## Required metadata for every evidence item

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

## Prohibited fields

- Personality type or trait score.
- Clinical diagnosis, disability category, psychological score, mental-health risk, or emotion-recognition result.
- Predicted dropout, misconduct, future attainment, or other future-outcome score.
- Race, religion, family income, socioeconomic rank, or demographic comparison.
- Comparative class ranking or labels such as `low`, `weak`, `lazy`, `naughty`, `unmotivated`, `addicted`, or `problem student`.
- Unstructured teacher notes.
- Raw PII in evidence copied into downstream artifacts.
- Any automatic placement, track, intervention, accommodation, parent notification, or change to assessment construct.

## Review cadence

- student interests/confidence: 4–6 weeks;
- structured teacher observations: 2–4 weeks;
- academic evidence: per completed unit or diagnostic event;
- behavioural pattern: at least three observations, reviewed monthly;
- accommodations: when the authorised plan changes and at least annually;
- parent input/consent: re-confirm each term;
- data older than two terms: hidden by default;
- data older than one academic year: delete unless an authorised retention requirement applies.
