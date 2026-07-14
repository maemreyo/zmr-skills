# Student Artifact Contract

Required envelope fields are `artifact_id`, `artifact_type`, `audience: student`, positive `version`, `brief_id`, `grade_band`, optional `cefr`, `target_language`, `instruction_language`, non-empty `objective_ids`, `methodology_lineage`, `source_references`, `authority`, `accessibility`, `brand`, and versioned `dependencies`. Practice fields add `progression` and `items`. Every item has a stable `item_id`, non-empty `objective_ids`, and a student prompt. Item IDs remain stable during copy edits. Every item objective exists at artifact level.

V3 practice uses independent `interaction`, `response_mode`, and `cognitive_operation` fields. Every item also declares the renderer projection `response_type`, integer `expected_response_lines`, and non-empty `layout_intent`. Minimum response space is 1 line for `selected_response`, 2 for `short_answer`, 4 for `explanation`, and 5 for `two_sentence_transfer`. The projection controls classroom layout and does not replace the canonical taxonomy.

Optional accessibility metadata includes reading order, plain-language instructions, image `alt_text`, and non-color cues. Print instructions specify page size, grayscale need, cut lines, and teacher setup without embedding answers.

Prohibited anywhere in a student artifact: `answer`, `answer_key`, `accepted_answers`, `correct_answer`, `correct_option_ids`, `explanation`, `rubric`, and `wrong_reasons`. Hidden metadata counts as leakage. A teacher answer document must be derived separately by the assessment workflow.
