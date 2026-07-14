Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-review-publish-pack
```

```bash
npx skills update zamery-review-publish-pack
```

[Source](https://github.com/mattpocock/skills/tree/main/skills/education/zamery-review-publish-pack)

## What it does

`zamery-review-publish-pack` gates, finalises, packages, and exports complete English K-12 teaching packs through six quality gates before delivery.

A pack does not ship until every gate passes. Brief, Pedagogy, Content, Safety, Presentation, and Pack gates run in sequence; a hard failure at any gate blocks rendering. The skill records evidence for each gate — which artifacts passed, which failed, and on what grounds — so a teacher never receives materials that haven't been checked against the original brief, for pedagogical soundness, for content accuracy, for PII or answer leakage, for visual quality, or for structural integrity.

## When to reach for it

Type `/zamery-review-publish-pack`, or the agent reaches for it automatically when a task fits — any time a teacher asks to check, finalise, package, or export a teaching pack.

Reach for it when the individual artifacts exist and need a final pass before delivery. If the artifacts themselves still need composing or creating, finish those first — [zamery-design-teaching-materials](https://aihero.dev/skills-zamery-design-teaching-materials) for page layouts, [zamery-create-english-presentations](https://aihero.dev/skills-zamery-create-english-presentations) for slide decks, [zamery-build-video-learning](https://aihero.dev/skills-zamery-build-video-learning) for video sequences.

## Gate, don't guess

The six quality gates are the skill's structure. Each has a clear pass-fail criterion.

**Brief gate.** The pack is checked against the original teaching brief. Every required artifact is present, every objective is addressed, and no artifact exceeds its defined scope.

**Pedagogy gate.** The teaching approach in each artifact matches the methodology specified in the brief. A practice worksheet designed for guided release is not checked against inquiry-based criteria.

**Content gate.** Objectives, questions, answers, rubrics, and source references are accurate. Content authority is verified — no question was silently reworded, no objective was dropped.

**Safety gate.** PII and student answer leakage are checked across every artifact. The safety findings from each individual artifact's build are pooled and rechecked at the pack level, because a single artifact may be clean but two artifacts combined may reveal an answer.

**Presentation gate.** Visual QA runs on every rendered document and slide: DOCX pages are inspected, PPTX slides are reopened, PDFs are checked for correct output. Repairs target only the affected artifact; the gate does not pass until every rendered file is clean.

**Pack gate.** The final ZIP is built, its CRC is verified, nested OOXML files inside it are decompressed and checked for corruption, classroom files are reopened and re-rendered from the extracted bundle, and structured exports (JSONL, SQLite, QTI, H5P) are re-validated. Only then does the skill deliver separate student and teacher file sets.

## It's working if

- Every gate result includes evidence — a name, a finding, a pass/fail — not just a green check.
- A hard failure at any gate stops rendering before a single file is written.
- The delivered ZIP survives a re-extract and re-render without errors.
- Student and teacher files are delivered as separate, independently usable sets.

## Where it fits

`zamery-review-publish-pack` is the terminal step in the Zamery materials flow. Every content skill feeds into it:

```txt
zamery-build-english-practice / zamery-design-teaching-materials / 
zamery-create-english-presentations / zamery-build-video-learning →
  zamery-review-publish-pack
```

Its upstream neighbours are [zamery-design-teaching-materials](https://aihero.dev/skills-zamery-design-teaching-materials) (composes the documents it gates), [zamery-create-english-presentations](https://aihero.dev/skills-zamery-create-english-presentations) (creates the decks it gates), and [zamery-build-video-learning](https://aihero.dev/skills-zamery-build-video-learning) (creates the video sequences it gates). When you're unsure which skill fits, [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) routes you.
