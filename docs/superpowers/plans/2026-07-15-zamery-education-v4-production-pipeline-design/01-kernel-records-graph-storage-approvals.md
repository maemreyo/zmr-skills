# Education V4 Kernel Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the authoritative V4 kernel for canonical records, content hashes, typed graph invariants, content-addressed storage, a disposable SQLite index, and immutable approvals.

**Architecture:** Pydantic v2 models serialize through one canonical encoder before hashing and committing. A typed directed graph stores record identities and allowed relationships; an approval service resolves authority for exact hashes. SQLite is populated only from canonical files.

**Tech Stack:** Python 3.12, Pydantic v2, pytest, Hypothesis, SQLite, Ruff, mypy, uv.

## Global Constraints

- V4 code lives under `src/zamery_education_v4/` and does not import V3 runtime.
- Canonical records are immutable and reject unknown fields.
- Content hashes use SHA-256 over canonical UTF-8 JSON bytes.
- Canonical records exclude host paths, run timestamps, PIDs, secrets, hidden reasoning, and mutable build status.
- SQLite can be deleted without losing authority.
- Approval is a separate immutable record tied to exact hashes.
- Each task starts with a failing test and ends with a commit.

---

### Task 1: Bootstrap the typed Python package

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Create: `src/zamery_education_v4/__init__.py`
- Create: `src/zamery_education_v4/py.typed`
- Create: `tests/v4/test_package_contract.py`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: none.
- Produces: importable package `zamery_education_v4`, Python floor `3.12`, and shared test configuration.

- [ ] **Step 1: Write the failing package test**

```python
from importlib.metadata import version

import zamery_education_v4


def test_package_exposes_v4_identity() -> None:
    assert zamery_education_v4.__version__ == "4.0.0"
    assert version("zamery-education-v4") == "4.0.0"
```

- [ ] **Step 2: Verify failure**

```bash
python3.12 -m pytest tests/v4/test_package_contract.py -q
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Add package configuration**

```toml
[build-system]
requires = ["hatchling>=1.27,<2"]
build-backend = "hatchling.build"

[project]
name = "zamery-education-v4"
version = "4.0.0"
requires-python = ">=3.12,<3.14"
dependencies = [
  "pydantic>=2.10,<3",
  "typer>=0.15,<1",
]

[project.optional-dependencies]
dev = [
  "hypothesis>=6.120,<7",
  "mypy>=1.14,<2",
  "pytest>=8.3,<9",
  "pytest-cov>=6,<7",
  "ruff>=0.9,<1",
]

[tool.hatch.build.targets.wheel]
packages = ["src/zamery_education_v4"]

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = ["integration: requires external document tooling"]

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "RUF"]

[tool.mypy]
python_version = "3.12"
strict = true
packages = ["zamery_education_v4"]
```

```python
# src/zamery_education_v4/__init__.py
__version__ = "4.0.0"
```

- [ ] **Step 4: Run baseline checks**

```bash
uv sync --extra dev
uv run pytest tests/v4/test_package_contract.py -q
uv run ruff check src tests
uv run mypy src/zamery_education_v4
```

Expected: all commands exit `0`.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml .python-version .gitignore src/zamery_education_v4 tests/v4
git commit -m "build(education-v4): bootstrap typed runtime"
```

### Task 2: Implement canonical JSON and hashing

**Files:**
- Create: `src/zamery_education_v4/kernel/canonical_json.py`
- Create: `src/zamery_education_v4/kernel/hashing.py`
- Create: `src/zamery_education_v4/kernel/__init__.py`
- Create: `tests/v4/kernel/test_canonical_json.py`
- Create: `tests/v4/kernel/test_hashing_properties.py`

**Interfaces:**
- Produces:
  - `canonical_json_bytes(value: object) -> bytes`
  - `sha256_bytes(payload: bytes) -> str`
  - `content_hash(value: object) -> str`

- [ ] **Step 1: Write deterministic tests**

```python
from zamery_education_v4.kernel.canonical_json import canonical_json_bytes


def test_key_order_and_unicode_do_not_change_bytes() -> None:
    left = {"b": "e\u0301", "a": [2, 1]}
    right = {"a": [2, 1], "b": "é"}
    assert canonical_json_bytes(left) == canonical_json_bytes(right)
```

```python
from hypothesis import given, strategies as st
from zamery_education_v4.kernel.hashing import content_hash


@given(st.dictionaries(st.text(min_size=1), st.integers(), max_size=10))
def test_hash_ignores_mapping_insertion_order(data: dict[str, int]) -> None:
    assert content_hash(data) == content_hash(dict(reversed(list(data.items()))))
```

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/kernel/test_canonical_json.py tests/v4/kernel/test_hashing_properties.py -q
```

- [ ] **Step 3: Implement canonicalization**

```python
from __future__ import annotations

import json
import math
import unicodedata
from collections.abc import Mapping, Sequence


def _normalize(value: object) -> object:
    if value is None or isinstance(value, bool | int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite numbers are not canonical")
        return 0 if value == 0 else value
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, Mapping):
        normalized: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("object keys must be strings")
            normalized[unicodedata.normalize("NFC", key)] = _normalize(item)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, bytes | bytearray):
        return [_normalize(item) for item in value]
    raise TypeError(f"unsupported canonical value: {type(value).__name__}")


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        _normalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
```

```python
from hashlib import sha256
from .canonical_json import canonical_json_bytes


def sha256_bytes(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def content_hash(value: object) -> str:
    return sha256_bytes(canonical_json_bytes(value))
```

- [ ] **Step 4: Run tests and static checks**

```bash
uv run pytest tests/v4/kernel/test_canonical_json.py tests/v4/kernel/test_hashing_properties.py -q
uv run ruff check src/zamery_education_v4/kernel tests/v4/kernel
uv run mypy src/zamery_education_v4/kernel
```

- [ ] **Step 5: Commit**

```bash
git add src/zamery_education_v4/kernel tests/v4/kernel
git commit -m "feat(education-v4): add canonical hashing"
```

### Task 3: Define immutable record models and registry

**Files:**
- Create: `src/zamery_education_v4/kernel/records/base.py`
- Create: `src/zamery_education_v4/kernel/records/identity.py`
- Create: `src/zamery_education_v4/kernel/records/context.py`
- Create: `src/zamery_education_v4/kernel/records/planning.py`
- Create: `src/zamery_education_v4/kernel/records/content.py`
- Create: `src/zamery_education_v4/kernel/records/artifacts.py`
- Create: `src/zamery_education_v4/kernel/records/registry.py`
- Create: `tests/v4/kernel/records/`
- Create: `schemas/v4/records/`

**Interfaces:**
- Produces `CanonicalRecord`, `RecordId`, `RecordHash`, `RecordRegistry`, and initial context/planning/content/artifact record families.

- [ ] **Step 1: Write immutability and forbidden-field tests**

```python
import pytest
from pydantic import ValidationError
from zamery_education_v4.kernel.records.context import TeachingBrief


def test_record_is_frozen() -> None:
    brief = TeachingBrief(
        record_id="brief:unit1",
        duration_minutes=90,
        learner_level="A2",
        source_ids=("source:mindset-unit1",),
    )
    with pytest.raises(ValidationError):
        brief.duration_minutes = 105  # type: ignore[misc]


@pytest.mark.parametrize("field", ["approved", "build_status", "absolute_path", "process_id"])
def test_unknown_mutable_fields_are_rejected(field: str) -> None:
    payload = {
        "record_id": "brief:unit1",
        "duration_minutes": 90,
        "learner_level": "A2",
        "source_ids": ["source:mindset-unit1"],
        field: True,
    }
    with pytest.raises(ValidationError):
        TeachingBrief.model_validate(payload)
```

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/kernel/records -q
```

- [ ] **Step 3: Implement record base**

```python
from functools import cached_property
from typing import ClassVar
from pydantic import BaseModel, ConfigDict
from ..hashing import content_hash


class CanonicalRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    record_type: ClassVar[str]
    schema_version: str = "4.0.0"
    record_id: str

    def canonical_payload(self) -> dict[str, object]:
        payload = self.model_dump(mode="json", exclude_none=True)
        payload["record_type"] = self.record_type
        return payload

    @cached_property
    def calculated_hash(self) -> str:
        return content_hash(self.canonical_payload())
```

Create initial models for `SourceRecord`, `TeachingBrief`, `ObjectiveRecord`, `AssessmentDecisionRule`, `ItemRecord`, `AnswerRecord`, `ArtifactSpec`, and `GeneratedArtifact`. Use tuples for canonical collections and validators for sorted uniqueness where order is not semantic.

- [ ] **Step 4: Implement registry and schema export**

```python
class RecordRegistry:
    def __init__(self) -> None:
        self._models: dict[str, type[CanonicalRecord]] = {}

    def register(self, model: type[CanonicalRecord]) -> None:
        if model.record_type in self._models:
            raise ValueError(f"duplicate record type: {model.record_type}")
        self._models[model.record_type] = model

    def parse(self, payload: dict[str, object]) -> CanonicalRecord:
        record_type = payload.get("record_type")
        if not isinstance(record_type, str) or record_type not in self._models:
            raise ValueError(f"unknown record type: {record_type!r}")
        clean = dict(payload)
        clean.pop("record_type")
        return self._models[record_type].model_validate(clean)
```

- [ ] **Step 5: Run and commit**

```bash
uv run pytest tests/v4/kernel/records -q
uv run python scripts/v4/export_schemas.py --group records
uv run mypy src/zamery_education_v4/kernel/records
git add src/zamery_education_v4/kernel/records tests/v4/kernel/records schemas/v4 scripts/v4/export_schemas.py
git commit -m "feat(education-v4): define immutable records"
```

### Task 4: Implement typed graph and mandatory invariants

**Files:**
- Create: `src/zamery_education_v4/kernel/graph/edges.py`
- Create: `src/zamery_education_v4/kernel/graph/model.py`
- Create: `src/zamery_education_v4/kernel/graph/invariants.py`
- Create: `src/zamery_education_v4/kernel/graph/errors.py`
- Create: `tests/v4/kernel/graph/`
- Create: `tests/v4/fixtures/graphs/`

**Interfaces:**
- Produces `EdgeType`, `GraphEdge`, `PackGraph`, `GraphFinding`, and `validate_graph`.

- [ ] **Step 1: Write failing tests for cycles, missing targets, answer leakage, denominator mismatch, wrong receipt subject, and untracked bundle files**

```python
def test_threshold_cannot_exceed_unique_membership(graph_with_two_items) -> None:
    findings = validate_graph(graph_with_two_items)
    assert "DECISION_THRESHOLD_EXCEEDS_MEMBERSHIP" in {item.code for item in findings}
```

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/kernel/graph -q
```

- [ ] **Step 3: Implement edge types and immutable graph**

Required edge types:

```text
DERIVED_FROM REFERENCES IMPLEMENTS_OBJECTIVE USES_AUTHORITY USES_DURATION
PROJECTS_TO GENERATED_FROM RENDERED_FROM VERIFIED_BY APPROVED_BY
SUPERSEDES REVOKES INVALIDATES PACKAGES
```

`PackGraph.graph_hash` contains sorted record ID/hash pairs and sorted typed edges.

- [ ] **Step 4: Implement invariant codes**

```text
GRAPH_CYCLE
MISSING_EDGE_SOURCE
MISSING_EDGE_TARGET
INVALID_EDGE_SHAPE
STUDENT_ANSWER_LEAKAGE
ANSWER_AUTHORITY_MISSING
DECISION_THRESHOLD_EXCEEDS_MEMBERSHIP
GENERATED_ARTIFACT_SPEC_MISSING
RECEIPT_SUBJECT_HASH_MISMATCH
APPROVAL_TARGET_MISSING
BUNDLE_UNTRACKED_FILE
CORE_SOURCE_REPLACED_WITHOUT_APPROVAL
CROSS_SURFACE_DECISION_RULE_MISMATCH
```

- [ ] **Step 5: Run and commit**

```bash
uv run pytest tests/v4/kernel/graph -q
uv run ruff check src/zamery_education_v4/kernel/graph tests/v4/kernel/graph
git add src/zamery_education_v4/kernel/graph tests/v4/kernel/graph tests/v4/fixtures/graphs
git commit -m "feat(education-v4): enforce artifact graph invariants"
```

### Task 5: Implement content-addressed records and blobs

**Files:**
- Create: `src/zamery_education_v4/kernel/storage/layout.py`
- Create: `src/zamery_education_v4/kernel/storage/record_store.py`
- Create: `src/zamery_education_v4/kernel/storage/blob_store.py`
- Create: `src/zamery_education_v4/kernel/storage/errors.py`
- Create: `tests/v4/kernel/storage/test_record_store.py`
- Create: `tests/v4/kernel/storage/test_blob_store.py`

**Interfaces:**
- Produces `StoreLayout`, `RecordStore.commit/load`, and `BlobStore.commit_file/open`.

- [ ] **Step 1: Write tamper and atomicity tests**

```python
def test_tampered_record_is_rejected(tmp_path, store, brief) -> None:
    digest = store.commit(brief)
    store.path_for(digest).write_text('{"record_type":"teaching_brief"}')
    with pytest.raises(ContentHashMismatch):
        store.load(digest)
```

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/kernel/storage/test_record_store.py tests/v4/kernel/storage/test_blob_store.py -q
```

- [ ] **Step 3: Implement atomic commit**

Write into a temporary file in the target directory, flush and `fsync`, atomically replace, then reread and verify SHA-256 before returning. Store paths:

```text
.zamery/records/<record_type>/<digest>.json
.zamery/blobs/<digest>
```

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/kernel/storage/test_record_store.py tests/v4/kernel/storage/test_blob_store.py -q
git add src/zamery_education_v4/kernel/storage tests/v4/kernel/storage
git commit -m "feat(education-v4): add canonical content store"
```

### Task 6: Implement disposable SQLite indexing and rebuild

**Files:**
- Create: `src/zamery_education_v4/kernel/storage/index_schema.py`
- Create: `src/zamery_education_v4/kernel/storage/index.py`
- Create: `src/zamery_education_v4/kernel/storage/rebuild.py`
- Create: `tests/v4/kernel/storage/test_index_rebuild.py`
- Create: `tests/v4/kernel/storage/test_index_queries.py`

**Interfaces:**
- Produces `GraphIndex`, `IndexFingerprint`, and `rebuild_index`.

- [ ] **Step 1: Write delete-and-rebuild test**

```python
def test_rebuild_is_deterministic(index_path, store, graph_paths) -> None:
    first = rebuild_index(index_path, store, graph_paths)
    index_path.unlink()
    second = rebuild_index(index_path, store, graph_paths)
    assert second == first
```

- [ ] **Step 2: Implement schema**

```sql
CREATE TABLE records(record_id TEXT PRIMARY KEY, record_type TEXT NOT NULL, record_hash TEXT NOT NULL UNIQUE);
CREATE TABLE edges(graph_id TEXT NOT NULL, source_id TEXT NOT NULL, target_id TEXT NOT NULL, edge_type TEXT NOT NULL, PRIMARY KEY(graph_id, source_id, target_id, edge_type));
CREATE TABLE graphs(graph_id TEXT PRIMARY KEY, graph_hash TEXT NOT NULL);
```

Build into `graph.sqlite.new`, run `PRAGMA integrity_check`, and atomically replace the prior index.

- [ ] **Step 3: Run and commit**

```bash
uv run pytest tests/v4/kernel/storage/test_index_rebuild.py tests/v4/kernel/storage/test_index_queries.py -q
git add src/zamery_education_v4/kernel/storage tests/v4/kernel/storage
git commit -m "feat(education-v4): add rebuildable graph index"
```

### Task 7: Implement immutable approval authority

**Files:**
- Create: `src/zamery_education_v4/kernel/records/approvals.py`
- Create: `src/zamery_education_v4/kernel/approvals/service.py`
- Create: `src/zamery_education_v4/kernel/approvals/policy.py`
- Create: `tests/v4/kernel/approvals/`

**Interfaces:**
- Produces `ApprovalScope`, `ApprovalRecord`, `ApprovalResolution`, and `ApprovalAuthority.require`.

- [ ] **Step 1: Write stale-hash, wrong-scope, revocation, and supersession tests**

```python
def test_approval_is_stale_after_subject_change(authority) -> None:
    authority.add(approval_for("sha256:" + "a" * 64, scope="teaching_brief"))
    result = authority.resolve("teaching_brief", ("sha256:" + "b" * 64,))
    assert not result.approved
    assert result.reason == "APPROVAL_STALE"
```

- [ ] **Step 2: Implement approval model**

Fields:

```text
scope
approved_hashes
approver_role
approved_at
accepted_assumptions
accepted_limitations
supersedes
revokes
```

Applicability requires exact scope and exact subject-hash set. Graph adjacency never implies approval.

- [ ] **Step 3: Run full Part 1 gate**

```bash
uv run pytest tests/v4/kernel -q
uv run pytest tests/v4/kernel --cov=zamery_education_v4.kernel --cov-branch --cov-report=term-missing
uv run ruff check src tests
uv run mypy src/zamery_education_v4
```

- [ ] **Step 4: Commit**

```bash
git add src/zamery_education_v4/kernel/records/approvals.py src/zamery_education_v4/kernel/approvals tests/v4/kernel/approvals
git commit -m "feat(education-v4): enforce hash-bound approvals"
```
