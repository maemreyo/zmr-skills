# Teaching Brief

Field groups: learner (`grade_band`, age band, optional independent `cefr`, class size, confidence/profile, accessibility needs); intent (topic, English domain, desired outcome, objective IDs/statements, success evidence, prerequisites, misconceptions, duration, delivery context); language (`target_language`, `instruction_language`, bilingual balance); pedagogy (methodology, rationale, pinned status, curriculum/exam alignment, differentiation); scope (lesson/unit, sessions, artifact types, student/teacher audiences, item count, batch size, form IDs, seed, length constraints); authority (teacher sources marked required/preferred/reference, answer/rubric authority, media/transcript authority); constraints (must include/avoid, prohibited assumptions, privacy, difficulty, accessibility, print, technology); delivery (DOCX/PDF/PPTX/HTML/TSV/CSV/JSONL/SQLite/QTI/H5P, color/grayscale, print, student/teacher surfaces); identity (`zamery`, `rooted in strength`, supplied assets only).

Each value uses `explicit`, `inferred`, `defaulted`, or `unresolved`; optional absent CEFR uses `not_supplied`. Material fields are objectives, grade band, CEFR when independently supplied, methodology, assessment scope, target/instruction language, answer authority, required sources, duration, and artifact scope.

Authority precedence is: (1) safety, privacy, legal, and answer-separation hard blocks; (2) the teacher's current explicit instruction; (3) teacher sources marked required, including required answer keys or rubrics; (4) the approved Teaching Brief and blueprint; (5) teacher sources marked preferred or reference; (6) inferred values and defaults. Surface conflicts at levels 1–3; level 1 cannot be overridden, and other material conflicts require a teacher decision.

When confirmation helps, show only:

- `Known`: explicit values and approved constraints.
- `Inferred`: labelled assumptions that can proceed.
- `Needs your decision`: exactly one material question.
