# Blueprint Contract

A blueprint uses the shared artifact envelope: `artifact_id`/`blueprint_id`, `artifact_type: blueprint`, `audience: teacher`, positive `version`, `brief_id`, `grade_band`, optional `cefr`, `target_language`, `instruction_language`, `objective_ids`, `methodology_lineage`, `source_references`, `authority`, `accessibility`, `brand`, and versioned `dependencies`. Its instructional body adds `duration_minutes`, `methodology`, `objectives`, `phases`, and `provenance`.

Each objective contains a stable `objective_id`, an observable `statement`, and `success_evidence`. Keep IDs unchanged through revisions unless the objective itself changes. `misconception_targets` names predictable wrong models, not merely wrong answers.

Each phase contains `phase_id`, positive `minutes`, `objective_ids`, teacher action, learner action, and evidence. Phase minutes sum exactly to `duration_minutes`; every cited objective exists.

`differentiation` has support, core, and challenge moves that preserve shared objectives. `assessment_plan` identifies purpose, evidence, and objective IDs. `recommended_artifacts` names downstream artifacts and their objective IDs. Every recommended assessment cites at least one objective ID. The validator-enforced fields are blocking; missing optional narrative fields are reported to the teacher rather than invented.
