# Education V4 Migration, Goldens, CI, Security, and Cutover Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate only authoritative V3 information with explicit loss reporting, prove V4 across six production workflows, continuously verify determinism and security, and perform a guarded canary and hard cutover.

**Architecture:** Versioned migrators convert individual record families and emit immutable migration receipts. Golden workflows exercise the real production pipeline. GitHub Actions runs layered verification from kernel through clean extraction/rerender. Release verification aggregates technical, security, migration, and teacher-acceptance evidence.

**Tech Stack:** Python 3.12, Pydantic v2, pytest, Hypothesis, GitHub Actions, Node 22, pinned LibreOffice container, JSON/JSONL/CSV, QTI/H5P fixture tooling.

## Global Constraints

- Depends on Parts 1–3.
- V3 binaries may be comparison evidence but are not automatically V4 production artifacts.
- Migration never converts V3 trust booleans into receipts.
- Every input field is classified as preserved, transformed, discarded, review-required, or rejected.
- Golden tests assert semantics and findings rather than exact model prose.
- Copyright-sensitive fixtures use references, short attributed fragments, or original synthetic substitutes.
- CI begins from clean workspaces and rebuilds SQLite.
- Production document-tool jobs use pinned runtime digests.
- Logs exclude learner PII, secrets, hidden reasoning, and raw copyrighted passages.
- Rollback switches entry point to the final V3 tag; it does not add V3 compatibility to V4.

---

### Task 26: Build loss-explicit migration infrastructure

**Files:**
- Create: `src/zamery_education_v4/kernel/records/migration.py`
- Create: `src/zamery_education_v4/kernel/migrations/registry.py`
- Create: `src/zamery_education_v4/kernel/migrations/runner.py`
- Create: `src/zamery_education_v4/kernel/migrations/errors.py`
- Create: `tests/v4/migrations/test_registry.py`
- Create: `tests/v4/migrations/test_loss_explicit.py`

**Interfaces:**
- Produces `MigrationDefinition`, `MigrationOutcome`, `MigrationReceipt`, and `MigrationRegistry.migrate`.

- [ ] **Step 1: Write silent-loss rejection test**

```python
def test_every_input_field_is_classified(registry, v3_payload) -> None:
    v3_payload["visual_qa_passed"] = True
    result = registry.migrate(v3_payload, "teaching-brief.v3", "teaching-brief.v4")
    assert "visual_qa_passed" in result.receipt.discarded_fields
    assert result.receipt.discard_reasons["visual_qa_passed"] == "self_attested_quality"
```

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/migrations/test_registry.py tests/v4/migrations/test_loss_explicit.py -q
```

- [ ] **Step 3: Implement coverage assertion**

For every migration:

```text
input field paths
= preserved paths
+ transformed paths
+ discarded paths
+ review-required paths
+ rejected paths
```

Raise `UnreportedMigrationLoss` when any path is unclassified.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/migrations/test_registry.py tests/v4/migrations/test_loss_explicit.py -q
git add src/zamery_education_v4/kernel/records/migration.py src/zamery_education_v4/kernel/migrations tests/v4/migrations
git commit -m "feat(education-v4): add loss-explicit migration"
```

### Task 27: Implement V3 record-family migrators

**Files:**
- Create: `migrations/v4/teaching_brief_v3_to_v4.py`
- Create: `migrations/v4/learning_blueprint_v3_to_v4.py`
- Create: `migrations/v4/practice_content_v3_to_v4.py`
- Create: `migrations/v4/deck_manifest_v3_to_v4.py`
- Create: `migrations/v4/layout_manifest_v3_to_v4.py`
- Create: `migrations/v4/pack_manifest_v3_to_v4.py`
- Create: `tests/v4/migrations/test_v3_migrators.py`
- Create: `tests/v4/fixtures/migrations/v3/`

**Interfaces:**
- Each module exports `migrate(payload, context) -> MigrationResult`.

- [ ] **Step 1: Add representative V3 fixtures**

Include explicit duration/source, inferred CEFR, `ielts_practice` route, empty speaker notes mapping, `reopened_after_export: true`, visual/CRC booleans, and progression labels without item membership.

- [ ] **Step 2: Write outcome tests**

Expected classifications:

```text
explicit duration -> migrated
explicit source identity -> migrated
inferred CEFR -> requires_teacher_review
empty note mapping -> requires_reauthoring
reopened boolean -> discarded
visual pass boolean -> discarded
missing item membership -> requires_reauthoring
unsupported source claim -> rejected
```

- [ ] **Step 3: Verify failure**

```bash
uv run pytest tests/v4/migrations/test_v3_migrators.py -q
```

- [ ] **Step 4: Implement without importing V3 validators**

V3 schema names are input contracts only. Existing binaries become `CandidateReferenceRecord` records unless separately governed and regenerated.

- [ ] **Step 5: Run and commit**

```bash
uv run pytest tests/v4/migrations/test_v3_migrators.py -q
git add migrations/v4 tests/v4/migrations tests/v4/fixtures/migrations
git commit -m "feat(education-v4): migrate authoritative V3 data"
```

### Task 28: Encode Unit 1 audit failures as negative goldens

**Files:**
- Create: `goldens/v4/unit1-lesson1/README.md`
- Create: `goldens/v4/unit1-lesson1/source-map.json`
- Create: `goldens/v4/unit1-lesson1/negative/`
- Create: `src/zamery_education_v4/testing/golden_runner.py`
- Create: `tests/v4/goldens/test_unit1_negative.py`

**Interfaces:**
- Produces `GoldenRunner` and regression assertions for every confirmed audit failure.

- [ ] **Step 1: Create negative fixtures**

```text
route-misclassification.json
missing-lineage.json
threshold-denominator.json
preexposed-diagnostic.json
missing-source-answers.json
empty-speaker-notes.json
self-attested-pack-qa.json
render-analyzer-crash.json
unsafe-media-homework.json
```

- [ ] **Step 2: Write parameterized regression test**

```python
@pytest.mark.parametrize(
    ("fixture", "code"),
    [
        ("route-misclassification", "WORKFLOW_GOAL_MISMATCH"),
        ("missing-lineage", "MISSING_SOURCE_LINEAGE"),
        ("threshold-denominator", "DECISION_RULE_DENOMINATOR_MISMATCH"),
        ("preexposed-diagnostic", "DIAGNOSTIC_PREEXPOSED_CUES"),
        ("missing-source-answers", "MISSING_SOURCE_ANSWER_AUTHORITY"),
        ("empty-speaker-notes", "EMPTY_SPEAKER_NOTES"),
        ("self-attested-pack-qa", "REOPEN_RECEIPT_MISSING"),
        ("render-analyzer-crash", "INSPECTOR_EXECUTION_FAILED"),
        ("unsafe-media-homework", "MEDIA_PRIVACY_ALTERNATIVE_MISSING"),
    ],
)
def test_negative_fixture_fails_closed(fixture, code, golden_runner) -> None:
    result = golden_runner.run_negative("unit1-lesson1", fixture)
    assert code in result.finding_codes
    assert not result.published
```

- [ ] **Step 3: Run and commit**

```bash
uv run pytest tests/v4/goldens/test_unit1_negative.py -q
git add goldens/v4/unit1-lesson1 src/zamery_education_v4/testing tests/v4/goldens
git commit -m "test(education-v4): encode Unit 1 audit regressions"
```

### Task 29: Build the Unit 1 production tracer bullet

**Files:**
- Create: `goldens/v4/unit1-lesson1/production/request.json`
- Create: `goldens/v4/unit1-lesson1/production/brief.json`
- Create: `goldens/v4/unit1-lesson1/production/source-records.jsonl`
- Create: `goldens/v4/unit1-lesson1/production/blueprint.json`
- Create: `goldens/v4/unit1-lesson1/production/content-units.jsonl`
- Create: `goldens/v4/unit1-lesson1/production/artifact-specs.jsonl`
- Create: `goldens/v4/unit1-lesson1/production/reviews.jsonl`
- Create: `goldens/v4/unit1-lesson1/production/approvals.jsonl`
- Create: `tests/v4/goldens/test_unit1_production.py`

**Interfaces:**
- Produces a distribution-safe workbook, teacher guide, answer key, presentation, homework, governance report, and verified bundle.

- [ ] **Step 1: Write production assertions**

Assert lifecycle goal, source/core/transfer distinction, objective evidence, exact decision-rule membership, source-answer authority, answer separation, meaningful slide notes, privacy-safe homework alternatives, seven ordered gate passes, clean extraction, reopen/rerender, and graph-hash parity.

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/goldens/test_unit1_production.py -q
```

- [ ] **Step 3: Author distribution-safe fixture**

Reference source pages/exercises and authority metadata without copying complete copyrighted passages. Use original supplementary practice.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/goldens/test_unit1_production.py -q
uv run zamery-v4 golden run --fixture unit1-lesson1 --profile production
git add goldens/v4/unit1-lesson1/production tests/v4/goldens/test_unit1_production.py
git commit -m "test(education-v4): add Unit 1 production tracer"
```

### Task 30: Add five additional production goldens

**Files:**
- Create: `goldens/v4/worksheet-basic/`
- Create: `goldens/v4/item-bank-300/`
- Create: `goldens/v4/assessment-100/`
- Create: `goldens/v4/video-learning/`
- Create: `goldens/v4/reteaching-loop/`
- Create: `tests/v4/goldens/test_worksheet.py`
- Create: `tests/v4/goldens/test_item_bank.py`
- Create: `tests/v4/goldens/test_assessment.py`
- Create: `tests/v4/goldens/test_video_learning.py`
- Create: `tests/v4/goldens/test_reteaching_loop.py`
- Create: `capabilities/composition/qti_export/`
- Create: `capabilities/composition/h5p_export/`

**Interfaces:**
- Produces acceptance evidence for worksheet, large item bank, exam, media activity, and reteaching loop workflows.

- [ ] **Step 1: Write worksheet assertions**

Guided, independent, and retrieval memberships are distinct; response space is semantic; answer separation and print profile pass.

- [ ] **Step 2: Write item-bank assertions**

Exactly 300 stable IDs, no duplicate normalized prompts, deterministic batching, resumability, JSONL authority, rebuildable SQLite, and CSV interoperability.

- [ ] **Step 3: Write assessment assertions**

Exact blueprint coverage, 100 active items, form membership, no answer leakage, answer-key parity, administration guide, QTI IDs, archive security, and graded publication approval.

- [ ] **Step 4: Write video and reteaching assertions**

Video checks source allowlist, transcript provenance, timestamps, caption/fallback, H5P validity, and privacy. Reteaching checks StudentCard boundaries, monitoring evidence, human decision boundary, and reassessment linkage.

- [ ] **Step 5: Run and commit**

```bash
uv run pytest tests/v4/goldens -q
git add goldens/v4 capabilities/composition/qti_export capabilities/composition/h5p_export tests/v4/goldens
git commit -m "test(education-v4): add five production goldens"
```

### Task 31: Build V3/V4 comparison reports

**Files:**
- Create: `src/zamery_education_v4/application/comparison/models.py`
- Create: `src/zamery_education_v4/application/comparison/service.py`
- Create: `src/zamery_education_v4/cli/comparison.py`
- Create: `tests/v4/application/comparison/test_comparison.py`
- Create: `docs/architecture/v4/comparison-metrics.md`

**Interfaces:**
- Produces `ComparisonReport`.

- [ ] **Step 1: Write comparison tests**

Metrics include deliverables, source lineage, objective and answer coverage, binary reopen, notes coverage, gate states, teacher findings, file counts, and severe regressions.

- [ ] **Step 2: Implement severe-regression rules**

A severe regression is a lost supported deliverable, new answer leakage, lost core source activity, failed reopen, missing teacher command surface, or new hard safety finding.

- [ ] **Step 3: Run and commit**

```bash
uv run pytest tests/v4/application/comparison -q
git add src/zamery_education_v4/application/comparison src/zamery_education_v4/cli/comparison tests/v4/application/comparison docs/architecture/v4/comparison-metrics.md
git commit -m "feat(education-v4): compare V3 and V4 outcomes"
```

### Task 32: Add structured observability and explanation commands

**Files:**
- Create: `src/zamery_education_v4/kernel/observability/events.py`
- Create: `src/zamery_education_v4/kernel/observability/sink.py`
- Create: `src/zamery_education_v4/kernel/observability/redaction.py`
- Create: `src/zamery_education_v4/application/explain/`
- Create: `src/zamery_education_v4/cli/explain.py`
- Create: `src/zamery_education_v4/cli/gate.py`
- Create: `src/zamery_education_v4/cli/repair.py`
- Create: `src/zamery_education_v4/cli/golden.py`
- Create: `src/zamery_education_v4/cli/release.py`
- Create: `tests/v4/observability/`
- Create: `tests/v4/application/explain/`
- Create: `tests/v4/cli/test_explain_commands.py`

**Interfaces:**
- Produces redacted run events and `run explain`, `graph trace`, `artifact provenance`, `gate explain`, `repair explain`, `golden run`, and `release verify`.

- [ ] **Step 1: Write redaction test**

```python
def test_redaction_removes_pii_and_secrets() -> None:
    event = make_event(data={"student_name": "Protected", "api_key": "secret", "record_hash": "sha256:" + "a" * 64})
    redacted = redact_event(event).model_dump_json()
    assert "Protected" not in redacted
    assert "secret" not in redacted
    assert "sha256:" in redacted
```

- [ ] **Step 2: Implement event types**

```text
RUN_PLANNED NODE_READY CACHE_HIT CAPABILITY_STARTED CAPABILITY_COMPLETED
OUTPUT_REJECTED REVIEW_REQUIRED GATE_DECIDED REPAIR_PLANNED BUNDLE_PUBLISHED
```

- [ ] **Step 3: Implement stable CLI exit codes**

```text
0 success
2 invalid input
3 approval required
4 gate hard block
5 capability/tool failure
6 security failure
7 incomplete release criteria
```

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/observability tests/v4/application/explain tests/v4/cli/test_explain_commands.py -q
git add src/zamery_education_v4/kernel/observability src/zamery_education_v4/application/explain src/zamery_education_v4/cli tests/v4
git commit -m "feat(education-v4): add explainable observability"
```

### Task 33: Add security and supply-chain verification

**Files:**
- Create: `security/v4/network-allowlist.yaml`
- Create: `security/v4/runtime-digests.yaml`
- Create: `security/v4/archive-policy.yaml`
- Create: `scripts/v4/verify_runtime_digests.py`
- Create: `scripts/v4/generate_sbom.py`
- Create: `tests/v4/security/`

**Interfaces:**
- Produces runtime-verification report and SBOM.

- [ ] **Step 1: Write policy tests**

Reject wildcard production network, missing digest, unlocked Node adapter, unregistered runtime command, archive traversal, secret fixture in logs, and production `development_unisolated` runs.

- [ ] **Step 2: Implement verification scripts**

Parse every capability manifest, verify runtime digest and lockfile hash, and generate Python/Node/container component inventory.

- [ ] **Step 3: Run and commit**

```bash
uv run pytest tests/v4/security -q
uv run python scripts/v4/verify_runtime_digests.py
uv run python scripts/v4/generate_sbom.py --output build/v4-sbom.json
git add security/v4 scripts/v4 tests/v4/security
git commit -m "security(education-v4): verify runtime boundaries"
```

### Task 34: Add layered GitHub Actions workflows

**Files:**
- Create: `.github/workflows/education-v4-kernel.yml`
- Create: `.github/workflows/education-v4-adapters.yml`
- Create: `.github/workflows/education-v4-goldens.yml`
- Create: `.github/workflows/education-v4-release.yml`
- Create: `.github/actions/setup-education-v4/action.yml`
- Create: `containers/education-v4-doc-tools/Dockerfile`
- Create: `containers/education-v4-doc-tools/versions.env`
- Create: `tests/v4/ci/test_workflow_contracts.py`

**Interfaces:**
- Produces jobs `v4-kernel`, `v4-capability-contracts`, `v4-docx-adapter`, `v4-pptx-adapter`, `v4-pdf-adapter`, `v4-pack-security`, `v4-golden-unit1`, `v4-golden-bank`, `v4-golden-assessment`, `v4-determinism`, and `v4-migration`.

- [ ] **Step 1: Write workflow contract tests**

Assert Python 3.12, Node 22, lockfile cache keys, pinned document-tool container, no reused SQLite authority, verification-report artifacts, and release dependencies.

- [ ] **Step 2: Implement reusable setup and workflows**

Setup installs uv, syncs dependencies, verifies runtime digests, and prints tool versions. Adapter jobs run on relevant paths, nightly schedule, and release triggers.

- [ ] **Step 3: Run and commit**

```bash
uv run pytest tests/v4/ci/test_workflow_contracts.py -q
git add .github/workflows .github/actions containers tests/v4/ci
git commit -m "ci(education-v4): add layered verification"
```

### Task 35: Add clean determinism replay and index rebuild

**Files:**
- Create: `scripts/v4/run_determinism_replay.py`
- Create: `scripts/v4/compare_semantic_fingerprints.py`
- Create: `scripts/v4/verify_clean_index_rebuild.py`
- Create: `tests/v4/release/test_determinism_replay.py`
- Create: `tests/v4/release/test_clean_index.py`
- Modify: `.github/workflows/education-v4-release.yml`

**Interfaces:**
- Produces determinism and index-rebuild reports.

- [ ] **Step 1: Write replay assertions**

Two empty workspaces must match canonical record hashes, graph hash, plan hash, cache keys, gate subjects, semantic fingerprints, and normalized archive order.

- [ ] **Step 2: Implement clean runs**

Use distinct temporary roots and empty caches. Delete `graph.sqlite`, rebuild, and compare `IndexFingerprint`.

- [ ] **Step 3: Run and commit**

```bash
uv run pytest tests/v4/release/test_determinism_replay.py tests/v4/release/test_clean_index.py -q
git add scripts/v4 tests/v4/release .github/workflows/education-v4-release.yml
git commit -m "test(education-v4): verify clean determinism"
```

### Task 36: Add operator, migration, review, and incident documentation

**Files:**
- Create: `docs/architecture/v4/README.md`
- Create: `docs/architecture/v4/record-model.md`
- Create: `docs/architecture/v4/capability-protocol.md`
- Create: `docs/architecture/v4/gate-policies.md`
- Create: `docs/architecture/v4/security-model.md`
- Create: `docs/operations/education-v4/operator-guide.md`
- Create: `docs/operations/education-v4/teacher-review-guide.md`
- Create: `docs/operations/education-v4/migration-guide.md`
- Create: `docs/operations/education-v4/incident-runbook.md`
- Create: `tests/v4/docs/test_documented_commands.py`

**Interfaces:**
- Produces executable maintainer and teacher documentation.

- [ ] **Step 1: Write documentation command tests**

Extract fenced commands marked `testable` and run their `--help` or dry-run form. Fail on nonexistent subcommands.

- [ ] **Step 2: Write documentation**

Operator guide covers plan, run, resume, impact, repair, gate explain, publication, and rollback. Incident runbook covers tool outage, corrupt store, hash mismatch, leaked data, compromised runtime digest, and failed canary.

- [ ] **Step 3: Run and commit**

```bash
uv run pytest tests/v4/docs/test_documented_commands.py -q
git add docs/architecture/v4 docs/operations/education-v4 tests/v4/docs
git commit -m "docs(education-v4): add architecture and operations guides"
```

### Task 37: Implement guarded canary, release criteria, and rollback

**Files:**
- Create: `config/education-pipeline.yaml`
- Create: `src/zamery_education_v4/application/cutover/config.py`
- Create: `src/zamery_education_v4/application/cutover/service.py`
- Create: `scripts/v4/switch_pipeline.py`
- Create: `policies/v4/release/criteria.yaml`
- Create: `docs/operations/education-v4/teacher-acceptance-protocol.md`
- Create: `goldens/v4/unit1-lesson1/acceptance/teacher-review-template.json`
- Create: `tests/v4/cutover/`
- Create: `tests/v4/release/test_release_criteria.py`

**Interfaces:**
- Produces `v3`, `v4-canary`, and `v4` pipeline states plus `ReleaseVerificationReport`.

- [ ] **Step 1: Encode twelve cutover criteria**

```text
kernel/graph pass
cross-language protocol pass
Unit 1 seven-gate pass
five additional goldens pass
clean index rebuild
semantic determinism
re-extract/reopen/rerender pass
all known audit failures detected
no severe V3 regression
no silent migration loss
sandbox/archive security pass
teacher classroom-usability approval
```

- [ ] **Step 2: Write switch guards**

V4 canary requires a report for the exact commit. Full V4 requires accepted canary. Rollback requires recorded final V3 tag.

- [ ] **Step 3: Implement atomic selector update**

Record commit, actor, reason, verification-report hash, and timestamp. Do not copy V3 schema into V4.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/cutover tests/v4/release/test_release_criteria.py -q
git add config/education-pipeline.yaml src/zamery_education_v4/application/cutover scripts/v4/switch_pipeline.py policies/v4/release docs/operations/education-v4/teacher-acceptance-protocol.md goldens/v4/unit1-lesson1/acceptance tests/v4
git commit -m "feat(education-v4): guard canary and hard cutover"
```

### Task 38: Execute hard cutover and separate V3 removal

**Files:**
- Create: `docs/releases/education-v3-final.md`
- Create: `docs/releases/education-v4-canary.md`
- Create: `docs/releases/education-v4-cutover.md`
- Create: `scripts/v4/archive_v3_inventory.py`
- Modify: `config/education-pipeline.yaml`

**Interfaces:**
- Consumes passing release report.
- Produces final V3 tag, canary record, V4 default, and separate V3-removal change.

- [ ] **Step 1: Tag final V3 state**

```bash
git tag -a education-v3-final -m "Final frozen Education V3 runtime"
git push origin education-v3-final
```

- [ ] **Step 2: Generate V3 inventory**

```bash
uv run python scripts/v4/archive_v3_inventory.py --tag education-v3-final --output docs/releases/education-v3-final.md
```

- [ ] **Step 3: Switch to canary**

```bash
uv run python scripts/v4/switch_pipeline.py --mode v4-canary --verification build/release-verification.json --reason "Education V4 production canary"
```

Run production canary fixtures and teacher acceptance; record incidents and repairs.

- [ ] **Step 4: Switch default to V4 after acceptance**

```bash
uv run python scripts/v4/switch_pipeline.py --mode v4 --verification build/release-verification.json --reason "Education V4 hard cutover"
```

- [ ] **Step 5: Remove V3 runtime in a separate reviewed change**

Preserve the tag and archived documentation. Confirm no V4 imports reference V3.

- [ ] **Step 6: Run final clean-clone verification**

```bash
uv sync --extra dev
uv run ruff check src tests capabilities adapters scripts
uv run mypy src/zamery_education_v4
uv run pytest tests/v4 -q
uv run python scripts/v4/verify_runtime_digests.py
uv run python scripts/v4/run_determinism_replay.py --fixture unit1-lesson1
uv run python scripts/v4/verify_clean_index_rebuild.py --fixture unit1-lesson1
uv run zamery-v4 release verify --profile production
```

Expected: all commands exit `0`; release report references exact receipt, approval, graph, and bundle hashes.

- [ ] **Step 7: Commit cutover**

```bash
git add config/education-pipeline.yaml docs/releases scripts/v4/archive_v3_inventory.py
git commit -m "release(education-v4): complete governed hard cutover"
```
