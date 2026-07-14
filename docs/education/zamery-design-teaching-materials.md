Quickstart:

```bash
npx skills add mattpocock/skills --skill=zamery-design-teaching-materials
```

```bash
npx skills update zamery-design-teaching-materials
```

[Source](https://github.com/mattpocock/skills/tree/main/skills/education/zamery-design-teaching-materials)

## What it does

`zamery-design-teaching-materials` composes approved English K-12 content into branded, print-ready classroom documents — worksheets, workbooks, exam papers, answer keys, and administration guides.

It never changes what students are asked to learn or how the teacher teaches it. Pedagogy arrives approved; this skill only controls how that content lands on the page. It validates every layout against a template registry before rendering, so a worksheet template is never stretched to hold an exam, and an exam template is never used for a workbook. Internal metadata (prompts, route plans, manifests, QA ledgers) is hard-blocked from leaking into classroom-facing files.

## When to reach for it

Type `/zamery-design-teaching-materials`, or the agent reaches for it automatically when a task fits — any time approved content needs composing into a branded classroom document.

Reach for it when the content is settled and what remains is visual composition: which template, which components, how much response space per item. If the content itself still needs writing, use [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice) first.

## Composition, not creation

The skill owns three registries that together make composition predictable.

The **template registry** maps artifact type to a document template — worksheets, workbooks, exam papers (forms A/B/C), answer keys, admin guides, and data exports. Each template knows its page size, margins, brand chrome, and structural sections. The skill always picks the closest match; it never re-creates a generic layout when a dedicated template exists.

The **component registry** maps every content unit (objective, question, instruction, rubric, worked example) to a deliberate visual component — a two-column grid for side-by-side question-and-response, a tabular layout for marking rubrics, a full-width callout for worked examples. No content unit gets a default container; each is assigned deliberately.

The **response-space registry** allocates writing room per item. Short-answer items get a ruled line; extended responses get a half-page box; diagram tasks get a labelled grid. The registry prevents the default of identical answer areas for every item in a document.

Before rendering, the skill produces a `zamery-layout.v2` manifest that captures every page's purpose, brand application, grid, item placement, and occupancy. A script validates the manifest against the registries, so a mismatch between intended layout and available template is caught before any DOCX or PDF is written.

## It's working if

- The output uses the correct template, brand tokens, and component per content unit — not a generic document.
- Response space varies by item type, not by a one-size-fits-all default.
- The layout manifest is validated before rendering, not after.
- No prompt text, snake-case brief fields, or generation commentary appears in the classroom file.

## Where it fits

`zamery-design-teaching-materials` is a chain step in the Zamery materials flow, sitting between content creation and final publishing:

```txt
zamery-build-english-practice → zamery-design-teaching-materials → zamery-review-publish-pack
```

Its neighbour [zamery-build-english-practice](https://aihero.dev/skills-zamery-build-english-practice) produces the content it composes; [zamery-review-publish-pack](https://aihero.dev/skills-zamery-review-publish-pack) gates and ships what it renders. For slide decks instead of page layouts, use [zamery-create-english-presentations](https://aihero.dev/skills-zamery-create-english-presentations). When you're unsure which skill fits, [zamery-teacher-copilot](https://aihero.dev/skills-zamery-teacher-copilot) routes you.
