# Intent vs Reality

| intent_id | Expected truth | Observed reality | Diff | Violated invariant | Intent source | Supporting observations | Status | Claim ids |
|---|---|---|---|---|---|---|---|---|
| I-01 | Every education skill has a distinct, teachable responsibility and explicit boundaries. | Pending audit. | Unknown. | Clear ownership and routing. | User request; `skills/education/README.md` | O-001 | unknown | C-001 |
| I-02 | Outputs are pedagogically sound, communicable, usable by teachers, and capable of producing durable understanding and transfer. | Pending audit. | Unknown. | Learning quality. | User request | O-001 | unknown | C-002 |
| I-03 | The suite closes the loop from learner needs to design, instruction, practice, assessment, feedback, reteaching, and revision. | Pending audit. | Unknown. | Closed-loop instruction. | User request; suite README | O-001 | unknown | C-003 |
| I-04 | Quality, safety, accessibility, inclusion, evidence, and source authority are enforced consistently across artifacts. | Pending audit. | Unknown. | Cross-suite quality floor. | User request | O-001 | unknown | C-004 |
| I-05 | Cross-skill handoffs preserve intent and evidence without contradictory contracts or silent information loss. | Pending audit. | Unknown. | Contract integrity. | User request; copilot routing | O-001 | unknown | C-005 |
| I-06 | Teachers can understand learners well enough to adapt lessons, teaching, assignments, materials, and study methods without diagnostic or deterministic child profiling. | Current suite has only an unstructured `confidence/profile` field and no longitudinal learner-evidence loop. | A bounded StudentCard, ClassProfile, snapshot, and teacher-action layer are missing. | Responsive, child-safe personalisation. | User follow-up; research baseline | O-002, O-003 | violated | C-006 |
