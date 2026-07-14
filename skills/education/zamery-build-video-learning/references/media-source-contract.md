# Media source contract

`zamery-media.v3` stores media identity, source type, URL, duration, language, transcript evidence, and accessibility.

Transcript authority values:

- `teacher_supplied` — the teacher supplied or approved the text;
- `authorized_channel` — captions were accessed with channel/content-owner authorization;
- `licensed` — a licensed transcript is in scope;
- `public_link_only` — the URL is public but transcript evidence is not authorized;
- `none` — no transcript exists.

Grounding values are `verified`, `grounded`, `ungrounded`, and `unavailable`. Verified/grounded states require timed segments with unique IDs. `public_link_only` can only be ungrounded/unavailable and always requires teacher verification.

Every source-dependent item points to `start_seconds`, `end_seconds`, and one or more transcript segment IDs. Store source evidence separately from the user-facing prompt.
