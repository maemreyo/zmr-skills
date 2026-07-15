# Zamery Education V4 Implementation Plan — Master Index

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a breaking, production-ready Education V4 pipeline whose records, approvals, artifacts, receipts, gates, repairs, and published bundles are content-addressed, independently verifiable, and reproducible.

**Architecture:** A Python 3.12 shared kernel owns immutable records, the typed artifact graph, approvals, deterministic DAG execution, canonical storage, evidence, and gate policies. Pedagogy, composition, inspection, rendering, and publication run as isolated capabilities through a language-neutral JSON subprocess protocol.

**Tech Stack:** Python 3.12, Pydantic v2, pytest, Hypothesis, SQLite, JSON Schema, Typer, Python/Node capability adapters, DOCX/PPTX/PDF/LibreOffice tooling, GitHub Actions.

## Global Constraints

- V4 is a breaking release; production runtime must not import V3 schemas or validators.
- V3 remains frozen except for critical safety fixes until hard cutover.
- Canonical JSON records and content-addressed blobs are authoritative; SQLite is rebuildable.
- No mutable `approved`, `reopened`, `rerendered`, `visually_checked`, or equivalent trust booleans.
- Approvals apply to exact record or subgraph hashes and become inapplicable after material changes.
- A generator cannot verify or grant a gate pass for its own output.
- Every capability runs through the declared JSON protocol and an isolated input/output boundary.
- Network access is denied unless a capability manifest contains an explicit allowlist.
- Model-assisted work may author candidate records but cannot issue teacher approval.
- Published bundles must be re-extracted, rehashed, reopened, rerendered where applicable, and revalidated.
- StudentCard and protected learner data must not enter canonical downstream artifacts.
- Unit 1 Lesson 1 is the first production tracer bullet, not a hard-coded domain special case.
- Tests follow red-green-refactor and each task ends at a reviewable commit boundary.

---

## Approved design source

Place the approved design at:

```text
docs/superpowers/specs/2026-07-15-zamery-education-v4-production-pipeline-design.md
```

## Plan files and dependency order

### Part 1 — Kernel foundation

File: `01-kernel-records-graph-storage-approvals.md`

Produces immutable records, canonical hashing, graph invariants, content-addressed storage, disposable SQLite indexing, and hash-bound approval authority.

Exit gate:

```bash
uv run pytest tests/v4/kernel -q
uv run ruff check src tests
uv run mypy src/zamery_education_v4
```

### Part 2 — Workflow, protocol, execution, cache, and CLI

File: `02-workflow-protocol-execution.md`

Consumes Part 1 and produces governed request resolution, the capability protocol, sandbox runner, deterministic execution plans, DAG scheduling, cache, impact analysis, resume, and operator CLI.

Exit gate:

```bash
uv run pytest tests/v4/protocol tests/v4/execution tests/v4/application tests/v4/cli -q
uv run zamery-v4 --help
```

### Part 3 — Evidence, gates, adapters, repair, and publication

File: `03-evidence-gates-adapters-publication.md`

Consumes Parts 1–2 and produces independent evidence, seven ordered gates, document adapters, binary/render inspection, safety/accessibility checks, selective repair, and verified publication.

Exit gate:

```bash
uv run pytest tests/v4/evidence tests/v4/gates tests/v4/adapters tests/v4/publication -q
```

### Part 4 — Migration and golden workflows

File: `04-migration-goldens-ci-cutover.md`

Consumes Parts 1–3 and produces loss-explicit V3 migration, Unit 1 negative and production goldens, five additional workflow goldens, CI, determinism replay, observability, security checks, canary, and hard cutover.

Exit gate:

```bash
uv run pytest tests/v4 -q
uv run zamery-v4 release verify --profile production
```

## Review boundaries

Each numbered task is a reviewer boundary. Do not combine adjacent tasks merely to reduce commit count. Every task follows:

1. write the failing test;
2. run it and confirm the intended failure;
3. implement the smallest coherent behavior;
4. run focused and neighboring tests;
5. commit exact files;
6. record commands, exit codes, and evidence.

## Recommended branch structure

```bash
git switch zmr-dev
git pull --ff-only
git switch -c feature/education-v4
```

Use short-lived task branches such as:

```text
feature/education-v4-kernel-records
feature/education-v4-graph
feature/education-v4-protocol
feature/education-v4-gates
feature/education-v4-unit1-golden
```

## Required execution journal

Create:

```text
docs/superpowers/execution/education-v4/
```

For each task, save `task-<number>-verification.md` containing:

- commit SHA;
- commands and exit codes;
- failing-test evidence before implementation;
- passing-test evidence after implementation;
- deviations and rationale;
- newly discovered risks.

Do not place secrets, learner PII, hidden model reasoning, or raw copyrighted source passages in the journal.

## Program-level acceptance

The program is complete only when:

1. all plan parts are implemented;
2. V4 detects every confirmed Unit 1 audit failure;
3. Unit 1 production passes all seven gates;
4. five additional golden workflows pass;
5. two clean runs produce identical canonical graph and semantic fingerprints;
6. deleting and rebuilding SQLite preserves graph and decision resolution;
7. a freshly extracted bundle reopens and rerenders successfully;
8. migration reports contain no silent data loss;
9. sandbox and archive security tests pass;
10. teacher classroom-usability review passes;
11. canary rollback returns to the final V3 tag without introducing V3 compatibility into V4.
