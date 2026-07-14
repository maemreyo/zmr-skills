# Six Quality Gates

| Gate | Evidence | Pass | Hard block |
|---|---|---|---|
| Brief | approved brief plus provenance | explicit constraints preserved; assumptions labelled | unresolved material conflict |
| Pedagogy | objective, method, phase, learner fit | method and sequence support observable objective | silent material redesign or age-inappropriate demand |
| Content | source, examples, item lineage | accurate, internally consistent, objective-aligned; current, niche, and source-sensitive claims use primary sources | unsupported factual claim, unresolved source conflict, or contradictory answer authority |
| Safety | student and teacher surfaces plus visible and hidden metadata | no PII; no student answer leakage | any PII or answer-bearing student field |
| Presentation | render images and accessibility checks | readable, unclipped, ordered, non-color-dependent | content is unusable or teacher data is exposed |
| Pack | manifest, versions, dependencies, formats | IDs unique; dependencies current; formats supported | unknown objective, stale dependency, invalid AnswerSet source, unsupported requested format |

Run gates in order and stop before rendering on a hard block. Record evidence and affected artifact IDs, not only pass/fail labels.
