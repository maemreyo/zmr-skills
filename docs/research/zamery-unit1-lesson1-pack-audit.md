# Audit: Zamery Unit 1 Lesson 1 Pack

> **Scope:** every file under `docs/output/zamery-unit1-lesson1/`  
> **Teaching context:** *Mindset for IELTS Foundation*, Unit 1 (*Daily Life*)  
> **Audit date:** 15 July 2026  
> **Repository state:** commit `78f1b83`  
> **Verdict:** **Do not publish as a production teaching pack.** Preserve the PPTX visual system as a redesign seed; rebuild the instructional lineage and the student/teacher documents from an approved content map.

## Executive conclusion

The pack is technically intact but instructionally unauditable. All nine files open, every OOXML archive passes CRC/structure checks, every PDF contains extractable text, and the DOCX/PDF pairs preserve the same semantic content. The PPTX has no shapes outside the slide canvas and is the strongest artifact in visual structure and lesson flow.

The pack nevertheless fails the declared **Content** and **Pack** gates. There is no saved Teaching Brief, blueprint, source map, layout/deck/pack manifest, gate report, render report, README, or versioned dependency record. The teacher guide mixes thresholds from different surfaces without declaring their lineage; the answer pack omits the textbook-reading answer authority and contains a visible grammatical error; the deck has no functional speaker notes; and the practice workbook does not clearly distinguish core source work from teacher-generated transfer. These are orchestration and governance failures, not merely styling defects.

## Evidence and limits

This audit used four evidence layers:

1. **Direct artifact inspection:** DOCX/PPTX OOXML extraction, PDF text/layout extraction, metadata, table geometry, style hierarchy, slide bounds, notes, and font sizes.
2. **Rendered-surface evidence:** all 14 PDF pages were rendered; the teacher supplied a page-by-page visual/classroom-UX review. Pixel occupancy was independently measured using the intended algorithm of the repository's broken render analyzer.
3. **Source comparison:** Cambridge/public-preview research for Unit 1 outcomes and the first source sequence, recorded in `docs/research/mindset-for-ielts-foundation-unit-1.md`.
4. **Pipeline execution:** the exact request was passed to the route advisor; the render analyzer and relevant material tests were executed; the output directory was searched for all required governance artifacts.

The separate “Real-Life Homework” discussed by the teacher was not found in this workspace. Its appendix below is therefore a review of the teacher-supplied observations, not an independent file audit.

## File-by-file verdicts

| # | File | Technical result | Instructional result | Verdict |
|---|---|---|---|---|
| 1 | `student/zamery-unit1-lesson1-classroom-deck-v1-student.pptx` | Valid OOXML; 14 slides; 16:9; no out-of-bounds shapes; no hidden slides | Strong sequence, but empty notes, no title placeholders, weak metadata, small projected text, no saved deck lineage | **Keep as redesign seed; do not publish unchanged** |
| 2 | `student/zamery-unit1-lesson1-diagnostic-v1-student.docx` | Valid OOXML; semantic Heading 1 sections; correct 7.4/57.4/35.3 table ratio; repeated header rows | Word bank undermines unaided recall; pattern leakage across grammar items; missing name/date/session; pronunciation evidence is underspecified | **Redesign** |
| 3 | `student/zamery-unit1-lesson1-diagnostic-v1-student.pdf` | Valid tagged PDF; 2 pages; full semantic token parity with DOCX | Faithfully reproduces the diagnostic's content defects; teacher-observed excessive whitespace | **Redesign and rerender** |
| 4 | `student/zamery-unit1-lesson1-practice-homework-v1-student.docx` | Valid OOXML; semantic headings and table header rows; no answer leakage | Weak source/transfer labeling, shallow reading discrimination, narrow repeated grammar action, response columns outside the declared grid contract, competing generic homework | **Rewrite substantially** |
| 5 | `student/zamery-unit1-lesson1-practice-homework-v1-student.pdf` | Valid tagged PDF; 4 pages; full semantic token parity with DOCX | Faithfully reproduces workbook defects and sparse page economy | **Rewrite and rerender** |
| 6 | `teacher/zamery-unit1-lesson1-teacher-guide-v1-teacher.docx` | Valid OOXML; 105 minutes sum correctly; semantic headings/tables | Useful framework but no grade/context record, no stage→source→slide→item mapping, unresolved denominators, no source-answer authority | **Rebuild as an executable command center** |
| 7 | `teacher/zamery-unit1-lesson1-teacher-guide-v1-teacher.pdf` | Valid tagged PDF; 4 pages; semantic parity with DOCX | Same instructional defects; no independent publication evidence | **Rebuild and rerender** |
| 8 | `teacher/zamery-unit1-lesson1-answer-observation-v1-teacher.docx` | Valid OOXML; teacher/student separation is clean | Missing source Exercise 6 answer mapping; source authority is collapsed into one vague label; P03 contains “They takes the base form”; observation evidence fields are too weak for the intended decision process | **Rebuild** |
| 9 | `teacher/zamery-unit1-lesson1-answer-observation-v1-teacher.pdf` | Valid tagged PDF; 4 pages; semantic parity with DOCX | Same content/authority defects | **Rebuild and rerender** |

### Pair-level finding

For all four DOCX/PDF pairs, every normalized DOCX token appears in its corresponding PDF. PDF-only tokens are page furniture such as `zamery`, `rooted in strength`, audience labels, and page numbers. There is no evidence that export silently removed instructional content.

## Confirmed instructional defects

### 1. Source lineage is missing, not merely unclear

The source sequence is coherent: visual lead-in and personal expansion; Ping vocabulary in context; Ava/Michael/Nina multiple-text reading with seven discrimination items; present-simple rules; and a pair guessing activity. The pack draws from this sequence, but no artifact records a stable mapping such as:

`source page/exercise → objective → classroom action → slide/item → answer authority`.

This matters because two reading sets coexist:

- Slide 7 uses Ava/Michael/Nina and explicitly points to “Unit 1 pages 3–4”.
- Workbook P06–P10 uses Linh/Mateo/Sara as a teacher-generated text.

These sets are **not inherently incompatible**. The second can be legitimate near-transfer practice after the textbook reading. The production failure is that it is not labeled or mapped as transfer, while the answer pack covers only P06–P10 and omits the source seven-question answer authority. A teacher cannot reliably tell which evidence produces `5/7`, which surface owns it, or where to verify answers.

### 2. Threshold lineage is unresolved

The teacher guide and deck declare:

- `8/10` routine phrases;
- `5/7` reading details;
- `8/10` grammar choices.

The pack exposes eight diagnostic vocabulary gaps (D06–D13), six diagnostic corrections (D14–D19), five transfer-reading questions (P06–P10), and several possible combinations that could form ten grammar items. The `5/7` reading threshold plausibly belongs to the textbook's seven questions, but this mapping is not stored. Vocabulary `8/10` has no ten-item surface in the delivered pack. The problem is not that every denominator is certainly wrong; it is that the pack provides no deterministic calculation rule.

### 3. Diagnostic validity is weaker than the teacher guide claims

The diagnostic promises independent baseline evidence, yet D06–D13 supplies all answer components in a word bank. That measures cued recognition/completion rather than unaided recall. D14–D19 then repeats a narrow set of error patterns, allowing learners to infer the test pattern during the sequence. Pronunciation is observed through general speaking/final sounds, but there is no explicit pronunciation target, elicitation sequence, correction boundary, or exit evidence.

The diagnostic can still function as a low-stakes classroom check. It cannot support strong independent/with-cue/not-yet classifications unless the administration protocol explicitly elicits unaided responses before revealing cues.

### 4. Practice changes wording more often than learning action

The strongest sequence is `worked example → notice → choose and defend → correct and explain → speak/redo`. However:

- the distinction between guided and independent stages is not explicit;
- the reading profiles permit near one-keyword matching and lack the overlapping information of the source task;
- textbook evidence and generated transfer are not labeled as separate phases;
- homework is a generic paragraph-plus-audio task with limited process evidence;
- response grids for P06–P10 and P12–P15 use prompt/response ratios of roughly 50/42 and 49/43, outside the material contract's 52–58% prompt and 34–40% response bands.

The teacher's visual inspection additionally found weak page economy and inadequate response affordances. Those visual findings are consistent with the repository analyzer's intended occupancy metric: all 14 rendered pages fall below its 25% threshold. The analyzer itself is broken, so this calculation was reproduced independently rather than claimed as a validator pass/fail.

### 5. Teacher workflow is not executable without inference

The guide has useful elements: objective IDs, timed stages, hinge questions, support/fade decisions, a two-priority feedback loop, and spaced retrieval. It is not yet a real command center because stages say “use textbook profiles”, “set ten items”, and “three-item exit check” without stable references to source exercise, slide, student item ID, and answer row.

The front matter also omits the promised grade/learner context. The guide states `Online 1-to-1 · English–Vietnamese`, but no approved brief exists to establish grade 8–9, learner profile, edition/ISBN, or source version.

### 6. Answer authority contains both a gap and an error

The answer pack's source label—`Unit1 MS_F.pdf + teacher-generated aligned items`—does not distinguish direct source, adaptation, original generated transfer, or governing answer source. It lacks the source reading's seven answers. It also contains a visible grammar error:

> P03 · `They takes the base form.`

The correct rationale is “They **take** the base form” or “They **takes** is incorrect; use the base form after *they*.”

By contrast, D19 is not an omitted-preposition defect: its answer `Anna catches the bus` and clue `catch + noun` do address both the preposition and third-person form. That earlier criticism is not retained.

### 7. The deck violates its own specialist contract

The presentation skill requires student slides, a **separate teacher-note surface**, print fallbacks, exact note mapping, rendered inspection, and reopened delivery. The PPTX contains 14 notes-slide parts but all note text is empty. The deck-manifest validator would still accept a note object containing only a `slide_id`, because it validates mapping but not non-empty note content.

The deck also has no title placeholders on any slide and metadata is `Title: Presentation`, `Author: Walnut Exporter`, no language, revision 0. Its shape geometry fits the canvas, but many functional text elements are 9.75–13.5 pt and page furniture is 8.25 pt, which is weak for projection despite looking clean on a laptop.

## Accessibility and file hygiene

The direct OOXML evidence corrects several overstatements from the initial review:

- Section headings do use `Heading 1` in the DOCX files.
- The principal data tables use repeated semantic header rows.
- Diagnostic prompt tables are not equal-width; they closely match the required 8/56/36 geometry.
- No student answer metadata, StudentCard data, hidden notes answers, embedded objects, or macros were found.

Confirmed accessibility/hygiene defects remain:

- all four DOCX files have empty document title and language metadata;
- student files have no name/date/session fields;
- the deck uses no title placeholders, has no meaningful title/language metadata, and contains empty notes;
- minimum PDF text is 8 pt and teacher tables use extensive 8–8.5 pt text;
- no saved accessibility report, reading-order test, contrast result, grayscale result, or final reopen receipt exists.

## Why the skills allowed this output

### Routing misclassifies the request

Executing the current router with:

`Soạn bài cho Unit 1 Lesson 1 của Mindset for IELTS Foundation`

returns `ielts_practice`. `route_advisor.py` returns that intent for **any** request containing `ielts`, before it considers lesson design or multi-artifact orchestration. A coursebook lesson-design request is therefore liable to skip the blueprint-first flow.

### The blueprint validator checks structure, not instructional completeness

`validate_blueprint.py` checks identity strings, grade band, duration, objective IDs, phase coverage, total minutes, and one CEFR provenance error. It does not enforce the blueprint contract's source references, authority, methodology lineage, success evidence, misconception targets, teacher/learner actions, differentiation, assessment plan, or recommended artifact lineage.

### The practice validator permits shallow progression

`validate_practice.py` validates item IDs, objective references, supported interaction metadata, response line counts, layout intent, leakage, and only requires that the progression list contain `guided` and `independent`. It does not prove that guided/independent practice is substantively different, or enforce worked example, retrieval, interleaving, and transfer despite the skill prose requiring them.

### The presentation validator does not require useful notes

`validate_deck_manifest.py` ensures every slide ID has one teacher-note object, but it never validates note text. Empty note records can pass. It also validates a JSON manifest, not the actual PPTX.

### Render QA is currently broken

`analyze_rendered_pages.py` calls the nonexistent Pillow method `Image.get_flattened_data()`. Executing it crashes. The material test suite currently reports **22 passing, 2 failing**, both failures from this method. Therefore, the declared sparse-page check could not have passed as implemented.

### Pack verification is declarative and no evidence was saved

`validate_pack_manifest.py` requires booleans such as `crc_checked`, `reextracted`, and `rerendered_from_extracted`, but it does not perform those operations. The output directory contains no pack manifest or receipts. The seven hardest gates—pedagogy, content, accessibility, and presentation—remain predominantly model-judged prose gates.

## Seven-gate result

| Gate | Result | Evidence |
|---|---|---|
| Brief | **FAIL / hard block** | No approved brief or provenance artifact saved; source edition/version and learner context are not governed |
| Pedagogy | **PARTIAL** | Strong overall lesson arc and redo loop; diagnostic validity, transfer labeling, pronunciation plan, and learner-fit evidence remain incomplete |
| Content | **FAIL / hard block** | Missing item lineage and source reading answer authority; unresolved denominators; visible P03 rationale error |
| Safety | **PASS for the nine-file pack** | No PII or student answer leakage detected; teacher/student surfaces are separated |
| Accessibility | **PARTIAL / no pass evidence** | Basic semantic headings/table headers exist, but metadata, title placeholders, notes, small type, and missing QA receipts prevent a pass claim |
| Presentation | **PARTIAL / no pass evidence** | Valid, unclipped binaries and a strong deck; sparse document pages and broken analyzer; no completed visual QA record |
| Pack | **FAIL / hard block** | No manifest, dependency graph, gate report, render report, README, or saved re-extraction/rerender evidence |

## Real-Life Homework appendix (teacher-supplied evidence only)

The concept is stronger than the generic workbook homework because it asks for authentic evidence, oral defence, an error log, a random challenge, and revision evidence. It should replace, not compete with, the existing page-four homework after these blockers are addressed:

1. provide a face-free, room-free submission option and neutral-background guidance;
2. define consent, private upload, retention, deletion, and bystander rules;
3. replace clock-minute randomness with a teacher-issued nonce or live prompt;
4. separate allowed, declared, and prohibited AI/tool use;
5. remove unnecessary lexical/grammar scope creep and recalibrate time estimates;
6. add an oral follow-up that verifies ownership of the submitted language.

Because the file is absent from the repository, no independent claim is made about its pagination, metadata, wording, or exact visual quality.

## Recommended rebuild order

### P0 — restore authority and coherence

1. Create an approved Teaching Brief with the exact book edition/ISBN, learner context, lesson scope, source authority, and delivery constraints.
2. Create a Lesson 1 Content Map: `source → objective → action → evidence → artifact location → answer authority`.
3. Label textbook reading as core and Linh/Mateo/Sara as generated near-transfer, if retained.
4. Define every denominator and store item membership for vocabulary, grammar, and reading decisions.
5. Add source Exercise 6 answers or an explicit authorized answer dependency.
6. Correct the P03 rationale and audit every answer/rationale against its source item.

### P1 — rebuild learning and teacher surfaces

1. Redesign the diagnostic as unaided recall → recognition → production, preserving an unprompted baseline.
2. Rebuild practice as visual notice → guided → independent → textbook evidence → generated transfer → spaced retrieval.
3. Replace the generic homework with the privacy-safe Real-Life Mission.
4. Make every teacher stage cite source page/exercise, slide, item IDs, answer row, and observation target.
5. Record original response, cue, repaired response, and stage/time in the observation surface.
6. Add useful notes for every slide and a separate notes/print fallback.

### P2 — make publishing real

1. Save brief, blueprint, practice/deck/layout manifests, pack manifest, gate report, render report, and README beside the pack.
2. Run validators against structured inputs and inspect actual binaries rather than trusting booleans.
3. Fix the rendered-page analyzer and add actual binary/semantic tests for DOCX, PDF, and PPTX.
4. Add document title/language, slide title placeholders, production metadata, accessibility receipts, and version notes.
5. Re-extract, reopen, rerender, and publish a cleanly named archive only after all seven gates pass.

## Sources and verification artifacts

1. `docs/research/mindset-for-ielts-foundation-unit-1.md` — source hierarchy and Unit 1 sequence/outcomes.
2. `skills/education/zamery-review-publish-pack/references/seven-quality-gates.md` — declared gate policy.
3. `skills/education/zamery-review-publish-pack/references/visual-qa.md` — mandatory render/inspection policy.
4. `skills/education/zamery-teacher-copilot/scripts/route_advisor.py:7-33` — executable routing behavior.
5. `skills/education/zamery-design-english-learning/scripts/validate_blueprint.py:14-82` — actual blueprint enforcement.
6. `skills/education/zamery-build-english-practice/scripts/validate_practice.py:60-128` — actual practice enforcement.
7. `skills/education/zamery-create-english-presentations/scripts/validate_deck_manifest.py:32-116` — actual deck-manifest enforcement.
8. `skills/education/zamery-design-teaching-materials/scripts/validate_layout_manifest.py:27-137` — actual layout enforcement.
9. `skills/education/zamery-design-teaching-materials/scripts/analyze_rendered_pages.py:10-20` — broken page analyzer.
10. `skills/education/zamery-review-publish-pack/scripts/validate_pack_manifest.py:14-135` — declarative pack validation.
11. `.omo/ulw-research/20260715-064240/SYNTHESIS.md` — research ledger and convergence record.
12. `/var/folders/c_/91y1n1cd6rv5c9qxcxjnmr_w0000gn/T/opencode/zamery-audit/` — ephemeral extraction, render, parity, and geometry evidence for this session.
