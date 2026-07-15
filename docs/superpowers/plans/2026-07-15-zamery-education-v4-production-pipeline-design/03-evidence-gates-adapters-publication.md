# Education V4 Evidence, Gates, Adapters, Repair, and Publication Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce independent evidence for content and binary quality, evaluate seven ordered gates, repair only affected graph regions, and publish bundles only after clean extraction and revalidation.

**Architecture:** Evidence producers create immutable receipts for exact subject hashes. Gate policies aggregate receipts, approvals, and structured human reviews. Format adapters generate binaries; separate inspectors reopen and render them. Publication assembles exact graph membership and fails closed on unknown or stale files.

**Tech Stack:** Python 3.12, Pydantic v2, python-docx, python-pptx, pypdf, Pillow, lxml, LibreOffice headless, pytest.

## Global Constraints

- Depends on Parts 1 and 2.
- Gate order is Brief, Pedagogy, Content, Safety, Accessibility, Presentation, Pack.
- A gate policy cannot trust a boolean declared by a generator.
- Evidence targets exact record, binary, render, or graph hashes.
- Human review uses versioned rubrics and structured `ReviewRecord` records.
- Binary generation and inspection use distinct capabilities.
- Bundle assembly uses exact `DeliveryBundleSpec` membership, never globbing.
- Production publication requires clean extraction, hash parity, reopen, rerender, and final gate aggregation.

---

### Task 17: Define evidence, review, and gate-decision records

**Files:**
- Create: `src/zamery_education_v4/kernel/records/evidence.py`
- Create: `src/zamery_education_v4/kernel/evidence/findings.py`
- Create: `src/zamery_education_v4/kernel/evidence/freshness.py`
- Create: `src/zamery_education_v4/kernel/evidence/registry.py`
- Create: `tests/v4/evidence/test_evidence_records.py`
- Create: `tests/v4/evidence/test_freshness.py`

**Interfaces:**
- Produces `Finding`, `EvidenceReceipt`, `ReviewRecord`, `GateDecision`, and `EvidenceFreshnessPolicy`.

- [ ] **Step 1: Write wrong-subject and stale-policy tests**

```python
def test_receipt_does_not_apply_to_a_different_binary() -> None:
    receipt = EvidenceReceipt(
        record_id="receipt:notes",
        receipt_type="speaker_notes",
        subject_hash="sha256:" + "a" * 64,
        checker_id="pptx-notes-inspector",
        checker_version="4.0.0",
        policy_version="presentation-policy@4.0.0",
        result="pass",
        findings=(),
    )
    assert not receipt_applies(
        receipt,
        subject_hash="sha256:" + "b" * 64,
        policy_version="presentation-policy@4.0.0",
    )
```

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/evidence -q
```

- [ ] **Step 3: Implement record models**

`EvidenceReceipt` includes subject hash, checker identity/version/runtime digest, policy version, result, findings, execution receipt hash, and optional expiry. `ReviewRecord` includes rubric version, reviewer role, exact subject hashes, ratings, and findings. `GateDecision` includes gate, policy, subject graph hash, consumed evidence hashes, decision, severity, findings, and invalidation conditions.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/evidence -q
git add src/zamery_education_v4/kernel/records/evidence.py src/zamery_education_v4/kernel/evidence tests/v4/evidence
git commit -m "feat(education-v4): add immutable evidence records"
```

### Task 18: Implement ordered evidence-driven gate policies

**Files:**
- Create: `src/zamery_education_v4/kernel/gates/policy.py`
- Create: `src/zamery_education_v4/kernel/gates/engine.py`
- Create: `src/zamery_education_v4/kernel/gates/order.py`
- Create: `src/zamery_education_v4/kernel/gates/explain.py`
- Create: `policies/v4/gates/brief.yaml`
- Create: `policies/v4/gates/pedagogy.yaml`
- Create: `policies/v4/gates/content.yaml`
- Create: `policies/v4/gates/safety.yaml`
- Create: `policies/v4/gates/accessibility.yaml`
- Create: `policies/v4/gates/presentation.yaml`
- Create: `policies/v4/gates/pack.yaml`
- Create: `tests/v4/gates/`

**Interfaces:**
- Produces `GatePolicy`, `GateEngine.evaluate`, and `explain_gate`.

- [ ] **Step 1: Write self-attestation rejection test**

```python
def test_pack_boolean_does_not_replace_reopen_receipt(context) -> None:
    context.manifest_payload["reopened_after_export"] = True
    decision = context.engine.evaluate("pack", context.graph_hash)
    assert decision.decision == "fail"
    assert "REOPEN_RECEIPT_MISSING" in {f.code for f in decision.findings}
```

Add stale evidence, prior hard block, missing human review, and policy-version invalidation tests.

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/gates -q
```

- [ ] **Step 3: Implement evaluation order**

```text
resolve exact subject graph
verify prior ordered gates
resolve required receipt types
validate subject hash and freshness
validate required review rubric and hashes
apply hard-block codes
sort findings deterministically
commit a new immutable decision
```

- [ ] **Step 4: Implement explanation output**

Include policy version, subject graph, evidence hashes, missing evidence, finding codes, affected IDs, required repair, and preserved nodes.

- [ ] **Step 5: Run and commit**

```bash
uv run pytest tests/v4/gates -q
git add src/zamery_education_v4/kernel/gates policies/v4/gates tests/v4/gates
git commit -m "feat(education-v4): evaluate seven ordered gates"
```

### Task 19: Implement content-governance inspectors

**Files:**
- Create: `capabilities/verification/source_lineage/`
- Create: `capabilities/verification/objective_coverage/`
- Create: `capabilities/verification/answer_authority/`
- Create: `capabilities/verification/decision_rule/`
- Create: `tests/v4/evidence/test_content_inspectors.py`
- Create: `tests/v4/fixtures/content/`

**Interfaces:**
- Produces source-lineage, objective-coverage, answer-authority, and decision-rule receipts.

- [ ] **Step 1: Write known-failure tests**

```python
def test_denominator_mismatch_is_detected(run_capability) -> None:
    receipt = run_capability(
        "decision_rule",
        "tests/v4/fixtures/content/denominator-mismatch.json",
    )
    assert receipt.result == "fail"
    assert receipt.findings[0].code == "DECISION_RULE_DENOMINATOR_MISMATCH"
```

Fixtures cover missing lineage, missing source answers, generated transfer replacing core source work, and cross-surface threshold mismatch.

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/evidence/test_content_inspectors.py -q
```

- [ ] **Step 3: Implement deterministic inspectors**

All manifests set network denied and deterministic true. Findings carry stable codes and affected record IDs. The answer inspector verifies every active scored item has current answer authority.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/evidence/test_content_inspectors.py -q
git add capabilities/verification tests/v4/evidence tests/v4/fixtures/content
git commit -m "feat(education-v4): verify lineage and answer authority"
```

### Task 20: Implement DOCX generation and independent inspection

**Files:**
- Create: `adapters/docx/generate/`
- Create: `adapters/docx/inspect/`
- Create: `adapters/docx/shared/relationships.py`
- Create: `tests/v4/adapters/docx/`
- Create: `tests/v4/fixtures/docx/`

**Interfaces:**
- Consumes approved document artifact specs.
- Produces DOCX blobs, `BinaryInspectionReceipt`, `DocxSemanticReceipt`, and `MetadataReceipt`.

- [ ] **Step 1: Write generator/inspector independence test**

The generator result contains no inspection or gate fields. The inspector runs in a separate invocation against the committed binary hash.

- [ ] **Step 2: Write hidden-data tests**

Cover comments, tracked changes, macros, external relationships, author metadata, document language, title, heading hierarchy, table headers, alt text, and visible-text fingerprint.

- [ ] **Step 3: Verify failure**

```bash
uv run pytest tests/v4/adapters/docx -q
```

- [ ] **Step 4: Implement generation and package inspection**

Generation receives only a spec and mounted assets. Inspection checks ZIP relationships/XML and then reopens through `python-docx`. Every receipt targets the independently calculated binary hash.

- [ ] **Step 5: Run and commit**

```bash
uv run pytest tests/v4/adapters/docx -q
git add adapters/docx tests/v4/adapters/docx tests/v4/fixtures/docx
git commit -m "feat(education-v4): generate and inspect DOCX"
```

### Task 21: Implement PPTX generation, notes, and geometry inspection

**Files:**
- Create: `adapters/pptx/generate/`
- Create: `adapters/pptx/inspect/main.py`
- Create: `adapters/pptx/inspect/notes.py`
- Create: `adapters/pptx/inspect/geometry.py`
- Create: `tests/v4/adapters/pptx/`
- Create: `tests/v4/fixtures/pptx/empty-notes.pptx`
- Create: `tests/v4/fixtures/pptx/off-canvas-shape.pptx`

**Interfaces:**
- Produces PPTX blob, `SpeakerNotesReceipt`, `BinaryInspectionReceipt`, and geometry findings.

- [ ] **Step 1: Write empty-notes regression test**

```python
def test_present_but_empty_notes_fail(inspect_pptx) -> None:
    receipt = inspect_pptx("tests/v4/fixtures/pptx/empty-notes.pptx")
    assert receipt.result == "fail"
    assert "EMPTY_SPEAKER_NOTES" in {f.code for f in receipt.findings}
```

- [ ] **Step 2: Add hidden-slide, orphan-note, off-canvas, font-floor, and external-relationship tests**

- [ ] **Step 3: Verify failure**

```bash
uv run pytest tests/v4/adapters/pptx -q
```

- [ ] **Step 4: Implement inspection**

Verify semantic slide title, non-whitespace notes, one-to-one note relationships, no orphan note parts, no unauthorized hidden content, shape bounds, projected font floor, and no unauthorized embedded/external relationships.

- [ ] **Step 5: Run and commit**

```bash
uv run pytest tests/v4/adapters/pptx -q
git add adapters/pptx tests/v4/adapters/pptx tests/v4/fixtures/pptx
git commit -m "feat(education-v4): inspect PPTX notes and geometry"
```

### Task 22: Implement rendering, PDF inspection, and page-role visual QA

**Files:**
- Create: `adapters/libreoffice/render/`
- Create: `adapters/pdf/inspect/`
- Create: `adapters/rendered_pages/analyze/main.py`
- Create: `adapters/rendered_pages/analyze/geometry.py`
- Create: `policies/v4/presentation/page-roles.yaml`
- Create: `tests/v4/adapters/pdf/`
- Create: `tests/v4/adapters/rendered_pages/`

**Interfaces:**
- Produces rendered PDF/page blobs, render receipts, accessibility receipts, and semantic fingerprints.

- [ ] **Step 1: Write Pillow API regression test**

```python
def test_analyzer_does_not_use_nonexistent_pillow_api() -> None:
    source = Path("adapters/rendered_pages/analyze/geometry.py").read_text()
    assert "get_flattened_data" not in source
```

- [ ] **Step 2: Write page-role tests**

Cover cover page, student practice with intentional response space, accidental blank page, teacher command center, answer key, clipping, overlap, grayscale, and projection legibility.

- [ ] **Step 3: Verify failure**

```bash
uv run pytest tests/v4/adapters/pdf tests/v4/adapters/rendered_pages -q
```

- [ ] **Step 4: Implement render and inspection**

LibreOffice runs with pinned version metadata. PDF checks title, language, page count, text extraction, raster-only pages, annotations, attachments, tags, and metadata. Geometry uses supported Pillow `getdata()` or NumPy arrays. Occupancy thresholds depend on page role and never alone determine a pass.

- [ ] **Step 5: Run and commit**

```bash
uv run pytest tests/v4/adapters/pdf tests/v4/adapters/rendered_pages -q
git add adapters/libreoffice adapters/pdf adapters/rendered_pages policies/v4/presentation tests/v4/adapters
git commit -m "feat(education-v4): render and inspect pages by role"
```

### Task 23: Implement safety, privacy, accessibility, and answer separation

**Files:**
- Create: `capabilities/verification/safety/`
- Create: `capabilities/verification/privacy_homework/`
- Create: `capabilities/verification/accessibility/`
- Create: `capabilities/verification/answer_separation/`
- Create: `tests/v4/evidence/test_safety_accessibility.py`
- Create: `tests/v4/fixtures/homework/unsafe-video-mission.json`
- Create: `tests/v4/fixtures/artifacts/student-answer-leak.json`

**Interfaces:**
- Produces safety, privacy, accessibility, accommodation, and answer-separation receipts.

- [ ] **Step 1: Write unsafe-media test**

A mission requiring a learner face, room, or family member without a neutral alternative, consent, private submission, retention policy, and deletion policy hard fails.

- [ ] **Step 2: Write construct-preservation test**

A word bank added to unaided-recall diagnostic emits `ACCOMMODATION_CHANGES_CONSTRUCT`.

- [ ] **Step 3: Verify failure**

```bash
uv run pytest tests/v4/evidence/test_safety_accessibility.py -q
```

- [ ] **Step 4: Implement and run**

```bash
uv run pytest tests/v4/evidence/test_safety_accessibility.py -q
git add capabilities/verification tests/v4/evidence tests/v4/fixtures/homework tests/v4/fixtures/artifacts
git commit -m "feat(education-v4): enforce safety and accessibility"
```

### Task 24: Implement materiality-aware repair planning

**Files:**
- Create: `src/zamery_education_v4/application/repair_planning/models.py`
- Create: `src/zamery_education_v4/application/repair_planning/materiality.py`
- Create: `src/zamery_education_v4/application/repair_planning/service.py`
- Create: `tests/v4/application/repair_planning/test_repair_plan.py`

**Interfaces:**
- Produces `Materiality`, `RepairPlan`, `classify_materiality`, and `build_repair_plan`.

- [ ] **Step 1: Write materiality tests**

Metadata, spacing, and response-box geometry are non-material when meaning is unchanged. Objective, source substitution, scoring membership, grammar scope, and privacy-model changes are material.

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/application/repair_planning -q
```

- [ ] **Step 3: Implement repair plan**

Include affected IDs, invalidated nodes, preserved nodes, required reruns, required approval scopes, expected receipt types, and original finding hashes.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/application/repair_planning -q
git add src/zamery_education_v4/application/repair_planning tests/v4/application/repair_planning
git commit -m "feat(education-v4): plan selective repairs"
```

### Task 25: Implement exact bundle assembly and publication

**Files:**
- Create: `src/zamery_education_v4/application/publication/assemble.py`
- Create: `src/zamery_education_v4/application/publication/verify.py`
- Create: `src/zamery_education_v4/application/publication/publish.py`
- Create: `adapters/archive/create/`
- Create: `adapters/archive/inspect/`
- Create: `tests/v4/publication/`
- Create: `tests/v4/fixtures/archives/zip-slip.zip`
- Create: `tests/v4/fixtures/archives/case-collision.zip`

**Interfaces:**
- Produces candidate archives, archive receipts, and `PublishedBundleRecord`.

- [ ] **Step 1: Write exact-membership tests**

Assembly fails on any unknown file, missing declared file, duplicate normalized path, or file hash mismatch.

- [ ] **Step 2: Write archive security tests**

Reject absolute paths, `..`, symlinks, duplicate paths, case collisions, CRC failure, and extracted hash mismatch.

- [ ] **Step 3: Write re-extract/rerender test**

After extraction, reopen DOCX/PPTX/PDF, rerender classroom formats, compare semantic fingerprints, and then evaluate Pack Gate.

- [ ] **Step 4: Verify failure**

```bash
uv run pytest tests/v4/publication -q
```

- [ ] **Step 5: Implement publication chain**

Require seven current gate decisions and exact publication approval. Create `PublishedBundleRecord` only after fresh verification passes.

- [ ] **Step 6: Run Part 3 gate and commit**

```bash
uv run pytest tests/v4/evidence tests/v4/gates tests/v4/adapters tests/v4/publication tests/v4/application/repair_planning -q
git add src/zamery_education_v4/application/publication adapters/archive tests/v4/publication
git commit -m "feat(education-v4): publish verified bundles"
```
