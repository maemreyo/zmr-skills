# Brief Version Contract

Before any specialist generates or revises an artifact, assert the approved `brief_id`, positive `brief_version`, teacher approval, stable objective IDs, and every dependency artifact's approved and current versions.

Apply `validate_brief_version_assertion()` from `skills.education._shared.contracts`. A dependency is current only when its `approved_version` equals its `current_version`. This includes ClassProfile, Learner Context Snapshot, LearningSequenceMap, blueprint, authority pack, source artifact, bank snapshot, form, and prior analysis versions when used.

Reject stale or unapproved input. Show the mismatched artifact and versions, preserve the last approved state, and ask the teacher to re-approve the affected path. Never silently substitute a newer dependency when it could change objectives, evidence, pedagogy, assessment, learner context, authority, or scope.
