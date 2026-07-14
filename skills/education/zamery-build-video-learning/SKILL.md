---
name: zamery-build-video-learning
description: Use when a teacher supplies a YouTube or other video link/file and wants English K–12 pre-viewing, while-viewing, post-viewing, listening, speaking, writing, timestamped questions, transcript-grounded activities, or an H5P Interactive Video export. Use explicit transcript authority and grounding states; a public YouTube link alone does not authorize caption download or prove a transcript.
---

# Zamery Build Video Learning

Turn authorized or teacher-verified media evidence into a timestamped English-learning sequence. Separate media access, transcript authority, grounding, pedagogy, and delivery format.

## Intake decision

Accept one of these source states:

1. teacher-supplied video and transcript;
2. teacher-supplied transcript for a public video link;
3. channel-authorized captions/transcript;
4. licensed transcript;
5. public link only, marked `ungrounded` with teacher verification required.

Never imply that a public YouTube link grants caption-download rights. Official caption download requires authorization. If no transcript is authorized, create observation prompts only or request teacher-supplied evidence; do not invent timestamped factual answers.

## Workflow

1. Parse and normalize the media URL. For YouTube, use `parse_youtube_url` in `scripts/video_learning.py`.
2. Create `zamery-media.v3` using `references/media-source-contract.md`. Record duration, language, transcript authority/grounding, segments, and accessibility.
3. Validate the media manifest before drafting source-dependent questions.
4. Build a pre/during/post sequence using `references/learning-sequence.md`.
5. Give each source-dependent item a stable ID, phase, timestamp, interaction, prompt, answer/rubric, and `source_anchor` with exact transcript segment IDs.
6. Validate timestamps, segment IDs, answer structures, and bounds with `validate_timed_items`.
7. Optionally export H5P with `export_h5p`. The exporter creates a standards-structured host-resolved content package; the target H5P platform must already have the declared libraries.
8. For summative assessment, hand approved items to `zamery-compose-english-assessments`; do not treat H5P activity completion as secure high-stakes testing.

## H5P scope

- Supported interactions: single choice, true/false, and text prompt.
- Package includes `h5p.json` and `content/content.json` for `H5P.InteractiveVideo 1.28`.
- Dependencies are declared but not bundled. Validate against the target LMS/content bank before classroom release.
- Run `validate_h5p_package` for CRC, required files, JSON, dependencies, and interaction counts.

## Quality gates

- Verified/grounded transcript states require non-empty, ordered, non-overlapping segments.
- Every timestamp and anchor stays within media duration.
- Every cited segment exists.
- Public-link-only media cannot be marked verified and must retain teacher verification.
- Captions and a non-audio alternative are recorded; unsupported accessibility is surfaced.
- During-viewing questions are sparse enough to preserve comprehension flow.
- Questions target listening evidence, inference, language noticing, or transfer—not trivia unrelated to objectives.
- IELTS-style use routes through `zamery-create-ielts-practice` for profile constraints.

Read `references/youtube-and-transcript-policy.md`, `references/media-source-contract.md`, `references/learning-sequence.md`, and `references/accessibility-and-publishing.md`.
