# Semantic Revision

Create immutable before/after brief snapshots and compare them with `scripts/impact_diff.py`. Cosmetic copy, spacing, and non-authoritative wording changes may proceed within the active artifact. Objectives, grade/CEFR, language, methodology, duration, artifact scope, answer authority, and required sources are material and require confirmation.

Layout-only fields route to `material_design` without forcing pedagogical confirmation. After approval, invalidate only artifacts whose owner or dependency appears in `affected_intents`; preserve all previous approved versions. Regenerate in dependency order, increment affected artifact versions, update dependency versions and derived AnswerSets, then re-run review/publish. If the teacher declines, retain the current approved brief and artifacts unchanged.
