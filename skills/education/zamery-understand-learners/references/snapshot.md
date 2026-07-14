# Learner Context Snapshot

For individual practice, tutoring, or reteaching, Copilot may create a time-bounded snapshot containing only:

- current objective and success evidence;
- demonstrated prerequisite evidence;
- relevant strengths and misconceptions;
- authorised accommodations;
- recently effective or ineffective teaching strategies;
- one or two current interests if useful;
- current learner goal;
- evidence dates and expiry.

The teacher approves the snapshot before it is used. The full StudentCard is never passed to content-generation or publishing skills.

## Boundaries

- Snapshot fields are a minimum subset of the StudentCard, selected for one teaching purpose.
- Every field carries its original evidence date and expiry.
- Snapshot has its own `snapshot_id` and `expires_at` — it is invalid after the teacher-approved window.
- When the snapshot expires, the skill must request a new snapshot or regenerate it from the current StudentCard.
