Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-build-video-learning
```

```bash
npx skills update zamery-build-video-learning
```

[Source](https://github.com/mattpocock/skills/tree/main/skills/education/zamery-build-video-learning)

## What it does

Turn authorised or teacher-verified video media into a timestamped English-learning sequence with pre-viewing, while-viewing, and post-viewing activities. The defining constraint is that transcript authority and grounding are explicit -- a public YouTube URL alone does not authorise caption download or prove a transcript, so the skill separates media access, transcript authority, pedagogy, and delivery format into distinct concerns that each get their own state.

## When to reach for it

- **Invocation mode.** Type `/zamery-build-video-learning`, or the agent reaches for it automatically when a task fits.
- **Trigger boundary.** Reach for this when you have a video (YouTube link or uploaded file) and want English-learning activities grounded in its transcript. If you need IELTS-style practice based on video, route through `zamery-create-ielts-practice` first.

## Prerequisites

You need `scripts/video_learning.py` in your environment. For H5P export, the target H5P platform must already have the declared libraries (H5P.InteractiveVideo 1.28). The exporter creates a standards-structured content package but does not bundle the libraries themselves.

## Transcript authority decides what the skill can do

The skill accepts five source states, and the grounding state determines what it can produce:

1. Teacher-supplied video and transcript -- fully grounded.
2. Teacher-supplied transcript for a public video link -- grounded.
3. Channel-authorised captions or transcript -- grounded.
4. Licensed transcript -- grounded.
5. Public link only, marked `ungrounded` -- teacher verification required before factual questions are created.

If no transcript is authorised, the skill creates observation prompts only. It never invents timestamped factual answers from an unauthorised source. During-viewing questions are kept sparse to preserve comprehension flow -- the goal is listening evidence, inference, language noticing, and transfer, not trivia.

For summative assessment, approved items can be handed to `zamery-compose-english-assessments`. The H5P Interactive Video activity itself is not treated as secure high-stakes testing.

## It's working if

- Verified or grounded transcripts have non-empty, ordered, non-overlapping segments.
- Every timestamp and source anchor stays within the media duration.
- Public-link-only media retains the `ungrounded` marker and teacher verification requirement.
- During-viewing questions are sparse enough to preserve comprehension flow.
- Questions target listening evidence, inference, language noticing, or transfer -- not trivia unrelated to the learning objectives.

## Where it fits

- **Role.** A standalone media-to-pedagogy skill. It can hand approved items to assessment composition for summative use, or to material design for video-based worksheets.
- **Neighbours.** `zamery-compose-english-assessments` at https://aihero.dev/skills-zamery-compose-english-assessments for summative video-based assessment. `zamery-create-ielts-practice` at https://aihero.dev/skills-zamery-create-ielts-practice for IELTS-aligned video tasks.
- **The map.** Point to https://aihero.dev/skills-zamery-teacher-copilot.
