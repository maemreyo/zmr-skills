# Claim Graph

## Verified claims

Pending convergence and counter-search.

- **C-006:** StudentCard is valuable only when it uses dated evidence and student voice to support reversible teacher decisions, while excluding personality, diagnosis, emotion recognition, prediction, and fixed labels. Supported by repository audit and independent child-safety/regulatory research.

| claim_id | Statement | Type | Risk | Scope | Intent ids | Supporting observations | Contradicting observations | Independent groups | Convergence | Counter-search | Primary source | Dependencies | Status | Synthesis location |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | Skill responsibilities and boundaries are complete and unambiguous. | codebase/system | high | all skills | I-01 | pending | pending | pending | open | pending | repository corpus | none | unresolved | pending |
| C-002 | Skill contracts reliably produce effective learning and transfer. | pedagogical | high | all skills | I-02 | pending | pending | pending | open | pending | learning-science primary sources | C-001 | unresolved | pending |
| C-003 | The suite implements a closed instructional improvement loop. | system | high | suite | I-03 | pending | pending | pending | open | pending | repository + formative assessment evidence | C-001,C-002 | unresolved | pending |
| C-004 | Cross-cutting quality and learner-protection requirements are consistently enforced. | governance | high | suite | I-04 | pending | pending | pending | open | pending | standards + repository | C-001 | unresolved | pending |
| C-005 | Handoffs preserve semantic intent and evidence. | system | high | routing/contracts | I-05 | pending | pending | pending | open | pending | repository contracts | C-001 | unresolved | pending |
| C-006 | A bounded learner-evidence layer can improve responsive teaching, while personality/psychological profiling and fixed labels create unacceptable validity, privacy, regulatory, and self-fulfilling-prophecy risks. | pedagogical/governance | high | StudentCard and all downstream skills | I-06 | O-002,O-003 | none stronger than safeguards | repo-audit, external-primary-sources | converged with constraints | Active counter-search examined claimed personalisation benefits and current ed-tech practice | COPPA, FERPA/PPRA, UK GDPR/ICO, EU AI Act, UNCRC, Council of Europe, UNESCO/UNICEF | C-003,C-004,C-005 | supported | `STUDENT-CARD-DESIGN-NOTE.md` |
