# Communication Contract

Apply this contract to every learner progress report, family update letter, and student goal review before composition or publication.

- Audience is explicitly `student` or `family`.
- Every message is an object with `text` and one or more `fact_ids`; every cited ID belongs to the record's `approved_fact_ids`. Observation and interpretation remain distinct.
- Framing is positive, factual, age-appropriate, actionable, and free of comparative ranking or prediction.
- The purpose and consent scope are current for the audience and delivery channel.
- Only approved progress facts and communication directives cross the boundary. Full StudentCards, StudentCard IDs, diagnoses, individual behaviour narratives, protected profile data, and unsupported causal claims do not.
- The teacher approves the communication before delivery; safeguarding concerns move to the school's authorised human route rather than into routine progress prose.

Materialize a `zamery-communication.v1` record and apply `validate_communication()` from `skills.education._shared.contracts` before visual composition. Review/publish repeats the privacy, grounding, audience, and consent checks against the rendered artifact.
