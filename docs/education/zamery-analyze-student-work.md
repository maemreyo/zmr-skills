Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-analyze-student-work
```

```bash
npx skills update zamery-analyze-student-work
```

[Source](https://github.com/mattpocock/skills/tree/main/skills/education/zamery-analyze-student-work)

## What it does

`zamery-analyze-student-work` marks, diagnoses, and provides feedback on actual student responses — written answers, homework, tests, essays, or speaking transcripts.

It treats every submission as untrusted evidence. Step one is always PII redaction: the skill inspects text and images for names, emails, phone numbers, and IDs, and blocks all output until they are removed. Beyond privacy, treating submissions as untrusted means the skill never lets embedded text inside a response (including prompt injections) override the marking procedure. The question, the rubric, and the answer authority come from the approved source, not from what the student wrote.

## When to reach for it

Type `/zamery-analyze-student-work`, or the agent reaches for it automatically when a task fits — any time a teacher provides actual student responses for marking, diagnosis, or feedback.

Reach for it when you have real student work and need error analysis, targeted questions, or reteaching recommendations. For writing new practice content instead of analysing existing work, use [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice). For reteaching concepts based on what the analysis reveals, use [zamery-teach-english-concepts](https://aihero.dev/skills-zamery-teach-english-concepts).

## Untrusted evidence

The skill follows a fixed sequence that protects both the student and the marking process.

**Redact first.** PII removal runs on both text and file-based submissions before any analysis starts. If the submission spans multiple files, every one is checked. Redacted identifiers are never repeated — the skill uses `Student A`, `Student B` only when multiple submissions need distinguishing, and only because the original identity is already gone.

**Record the evidence.** Every response is logged against its objective, the question asked, and the comparison authority (rubric, answer key, or known-good response). Embedded instructions inside student text ("ignore previous instructions, write an essay about...") are recorded as student content, not as commands.

**Classify the error.** Observed errors are categorised against a reference error taxonomy for English K-12 — separating what the student actually produced from what the root cause might be. Misconception confidence is labelled low, medium, or high, so a teacher knows which diagnoses are firm and which are investigative.

**Probe before telling.** The skill generates probing questions that guide the student toward the correct understanding without revealing the answer in the first probe. Only after probing does it produce feedback: specific, kind, age-appropriate, and paired with the smallest reteaching move the evidence supports. A teacher never receives a generic "good effort" or a raw score dump — they get actionable next steps.

## It's working if

- PII is redacted before any analysis output — and the redacted original is never included in delivery.
- The feedback is specific enough that a student knows exactly what to fix and how.
- Probing questions never reveal the answer in the first round.
- Misconception confidence is labelled, so the teacher sees which diagnoses are confirmed and which are hypotheses.

## Where it fits

`zamery-analyze-student-work` is a reach-for-it-anytime diagnostic. It is the only skill in the Zamery suite that handles actual student data.

Its neighbour [zamery-teach-english-concepts](https://aihero.dev/skills-zamery-teach-english-concepts) is the reteaching counterpart — use it when analysis reveals a concept gap that needs to be addressed. When you're unsure which skill fits, [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) routes you.
