Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-create-ielts-practice
```

```bash
npx skills update zamery-create-ielts-practice
```

[Source](https://github.com/mattpocock/skills/tree/main/skills/education/zamery-create-ielts-practice)

## What it does

Generate IELTS Academic or General Training aligned practice materials for Listening, Reading, Writing, and Speaking. The defining constraint is that every output is labelled as practice or mock, never "official IELTS" or a definitive band score. Official format distinctions -- Academic versus General Training Reading and Writing profiles, Speaking Part 1/2/3 structure -- are preserved exactly, while all generated material explicitly disclaims equivalence to a live test.

## When to reach for it

- **Invocation mode.** Type `/zamery-create-ielts-practice`, or the agent reaches for it automatically when a task fits.
- **Trigger boundary.** Reach for this when you need IELTS-aligned practice with official task-family constraints, completion word and number rules, and criterion-based Writing or Speaking feedback. For ordinary K-12 English work that does not need the IELTS profile, use the other Zamery skills instead.

## Prerequisites

You need `scripts/ielts_profile.py` in your environment. For Writing and Speaking feedback, the skill gathers observable evidence under all four criteria before estimating a range.

## Task-family discipline

Each IELTS section has distinct task families and rules that the skill enforces. Listening and Reading award one mark per correct answer -- the skill reports a raw score but never applies a hard-coded raw-to-band table, because that conversion varies across test versions and between Academic and General Training Reading. For completion items, `max_words`, `max_numbers`, accepted alternatives, case sensitivity, and spelling policy are stored as machine-readable data fields, not hidden only in instructions.

Writing and Speaking feedback follows all four criteria (Task Achievement or Task Response, Coherence and Cohesion, Lexical Resource, Grammatical Range and Accuracy) and remains explicitly provisional. The skill estimates a range from observable evidence and never guarantees a band.

The non-negotiable labelling rules are simple: you can say "IELTS-aligned practice", "IELTS-aligned mock", "estimated practice feedback", and "practice raw score". You cannot say "official IELTS", "official band", "equivalent to a live test", or any guaranteed score prediction.

## It's working if

- Full Listening and Reading each have 40 questions; partial practice declares `full_test: false`.
- Academic Writing Task 1 is visual description; General Training Task 1 is a letter; Task 2 is a 250-word discursive essay weighted twice Task 1.
- Speaking includes Parts 1, 2, and 3 with correct long-turn and timing expectations.
- Generated materials cite their source and stay within supplied or authorised content.
- Completion answer policies are machine-readable and declared in data fields.

## Where it fits

- **Role.** A standalone profile skill that applies IELTS structure to content. It can hand off upstream to item-bank building for large reusable item sets, or downstream to assessment composition for mock exam forms.
- **Neighbours.** `zamery-build-english-item-banks` at https://aihero.dev/skills-zamery-build-english-item-banks for large reusable IELTS item sets. `zamery-compose-english-assessments` at https://aihero.dev/skills-zamery-compose-english-assessments for assembling mock exam forms from approved IELTS items.
- **The map.** Point to https://aihero.dev/skills-zamery-teacher-copilot.
