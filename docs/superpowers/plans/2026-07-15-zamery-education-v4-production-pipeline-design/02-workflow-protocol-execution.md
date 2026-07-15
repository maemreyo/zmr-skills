# Education V4 Workflow, Capability Protocol, and Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert governed teaching requests into deterministic workflow and execution plans, run isolated capabilities through a typed protocol, cache valid outputs, calculate selective invalidation, resume failures, and expose operator CLI commands.

**Architecture:** Request resolution determines lifecycle goal before domain profile. The kernel compiles a typed DAG whose nodes invoke sandboxed subprocesses. Capability outputs cross a hostile boundary: schema, hash, graph-reference, and permission checks happen before canonical commit.

**Tech Stack:** Python 3.12, Pydantic v2, asyncio subprocesses, Typer, pytest, Hypothesis, Node 22 reference adapter.

## Global Constraints

- Depends on Part 1 interfaces.
- A route is a governed `WorkflowPlan`, not one intent string.
- `IELTS` constrains a workflow but cannot replace a full lesson-pack lifecycle goal.
- Stdout contains exactly one protocol JSON object; logs use stderr.
- Capabilities see only mounted inputs and one fresh output directory.
- Kernel recalculates every declared record and file hash.
- Retry applies only to declared retryable failures.
- Resume requires the same execution-plan input graph hash.

---

### Task 8: Implement governed request resolution

**Files:**
- Create: `src/zamery_education_v4/application/request_resolution/models.py`
- Create: `src/zamery_education_v4/application/request_resolution/rules.py`
- Create: `src/zamery_education_v4/application/request_resolution/resolver.py`
- Create: `tests/v4/application/request_resolution/test_resolver.py`
- Create: `tests/v4/fixtures/requests/`

**Interfaces:**
- Produces `TeachingRequestRecord`, `WorkflowStage`, `DomainProfile`, `WorkflowPlan`, and `resolve_workflow`.

- [ ] **Step 1: Write the IELTS route regression test**

```python
def test_coursebook_pack_is_not_reduced_to_ielts_practice() -> None:
    request = TeachingRequestRecord(
        record_id="request:unit1",
        lifecycle_goal="publish_teaching_pack",
        requested_deliverables=("student_workbook", "teacher_guide", "presentation"),
        source_kinds=("textbook",),
        domain_terms=("IELTS",),
        quantity=None,
    )
    plan = resolve_workflow(request)
    assert plan.primary_goal == "publish_teaching_pack"
    assert plan.stages == (
        "resolve_source_authority",
        "build_teaching_brief",
        "design_learning_blueprint",
        "author_practice_content",
        "compose_student_materials",
        "compose_teacher_materials",
        "compose_presentation",
        "review_publish",
    )
    assert plan.domain_profiles == ("ielts_foundation_coursebook",)
```

- [ ] **Step 2: Add route fixtures**

Include full teaching pack, IELTS-only practice, 300-item bank, 100-item exam, standalone worksheet, and video-learning request.

- [ ] **Step 3: Verify failure**

```bash
uv run pytest tests/v4/application/request_resolution -q
```

- [ ] **Step 4: Implement precedence**

Resolve in this order:

```text
explicit lifecycle goal
requested deliverables
current lifecycle stage
source sensitivity
graded status
quantity/reuse
output formats
domain profiles
```

`IELTS` is read only in the final profile step.

- [ ] **Step 5: Run and commit**

```bash
uv run pytest tests/v4/application/request_resolution -q
git add src/zamery_education_v4/application/request_resolution tests/v4/application/request_resolution tests/v4/fixtures/requests
git commit -m "feat(education-v4): add governed workflow resolution"
```

### Task 9: Define capability manifests and protocol messages

**Files:**
- Create: `src/zamery_education_v4/protocol/manifest.py`
- Create: `src/zamery_education_v4/protocol/invocation.py`
- Create: `src/zamery_education_v4/protocol/result.py`
- Create: `src/zamery_education_v4/protocol/failure.py`
- Create: `src/zamery_education_v4/protocol/codec.py`
- Create: `schemas/v4/protocol/`
- Create: `tests/v4/protocol/test_models.py`
- Create: `tests/v4/protocol/test_codec.py`

**Interfaces:**
- Produces `CapabilityManifest`, `CapabilityInvocation`, `CapabilityResult`, `CapabilityFailure`, and `decode_result`.

- [ ] **Step 1: Write strict protocol tests**

```python
def test_decoder_rejects_logs_mixed_with_json() -> None:
    payload = b'loading model\n{"protocol_version":"zamery-capability.v1"}'
    with pytest.raises(ProtocolViolation, match="exactly one JSON object"):
        decode_result(payload)
```

Add wrong invocation ID, unknown field, undeclared output type, malformed hash, duplicate output path, and missing runtime digest tests.

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/protocol -q
```

- [ ] **Step 3: Implement manifest model**

```python
class CapabilityManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    capability_id: str
    capability_version: str
    protocol_version: Literal["zamery-capability.v1"]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    deterministic: bool
    side_effects: Literal["none", "model", "binary", "network", "human"]
    timeout_seconds: int
    memory_mb: int
    runtime_kind: Literal["python", "node", "native"]
    runtime_version: str
    runtime_digest: RecordHash
    lockfile_hash: RecordHash
    filesystem_read: Literal["input_mount_only"]
    filesystem_write: Literal["output_mount_only"]
    network_domains: tuple[str, ...] = ()
    cache_enabled: bool
    failure_codes: tuple[str, ...]
```

- [ ] **Step 4: Implement strict decoding**

Use `json.JSONDecoder.raw_decode`; reject leading or trailing non-whitespace and validate one discriminated success/failure object.

- [ ] **Step 5: Export schemas and commit**

```bash
uv run python scripts/v4/export_schemas.py --group protocol
uv run pytest tests/v4/protocol -q
git add src/zamery_education_v4/protocol schemas/v4/protocol tests/v4/protocol
git commit -m "feat(education-v4): define capability protocol"
```

### Task 10: Implement the sandboxed subprocess runner

**Files:**
- Create: `src/zamery_education_v4/kernel/execution/sandbox.py`
- Create: `src/zamery_education_v4/kernel/execution/runner.py`
- Create: `src/zamery_education_v4/kernel/execution/resources.py`
- Create: `src/zamery_education_v4/kernel/execution/errors.py`
- Create: `tests/v4/execution/test_runner.py`
- Create: `tests/v4/execution/fixtures/capabilities/`

**Interfaces:**
- Produces `SandboxPolicy`, `CapabilityRunner`, and `RawInvocationResult`.

- [ ] **Step 1: Write boundary tests**

```python
@pytest.mark.asyncio
async def test_output_cannot_escape_mount(runner, manifest, invocation) -> None:
    with pytest.raises(SandboxViolation, match="escapes output mount"):
        await runner.run(
            manifest,
            invocation,
            [sys.executable, "tests/v4/execution/fixtures/capabilities/write_outside.py"],
        )
```

Add timeout, stdout limit, symlink, excessive file count, excessive output bytes, stderr capture, and undeclared-network tests.

- [ ] **Step 2: Verify failure**

```bash
uv run pytest tests/v4/execution/test_runner.py -q
```

- [ ] **Step 3: Implement process execution**

Use `asyncio.create_subprocess_exec` with:

- no shell;
- allowlisted environment;
- fresh working directory;
- read-only input mount and empty output mount;
- invocation JSON on stdin;
- bounded stdout/stderr reads;
- process-group termination on timeout;
- output-tree validation after exit.

Production Linux runs through a pinned container or bubblewrap policy. Unsupported local isolation is labeled `development_unisolated` and cannot publish.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/execution/test_runner.py -q
git add src/zamery_education_v4/kernel/execution tests/v4/execution
git commit -m "feat(education-v4): isolate capability subprocesses"
```

### Task 11: Validate outputs before canonical commit

**Files:**
- Create: `src/zamery_education_v4/kernel/execution/output_validation.py`
- Create: `src/zamery_education_v4/kernel/execution/commit.py`
- Create: `tests/v4/execution/test_output_validation.py`
- Create: `tests/v4/execution/fixtures/capabilities/wrong_declared_hash.py`
- Create: `tests/v4/execution/fixtures/capabilities/unknown_reference.py`

**Interfaces:**
- Produces `ValidatedCapabilityOutputs`, `CommittedOutputs`, `validate_outputs`, and `commit_outputs`.

- [ ] **Step 1: Write hostile-output tests**

```python
def test_kernel_recalculates_declared_hash(context) -> None:
    result = success_result(
        record_type="teaching_brief",
        path="outputs/brief.json",
        declared_hash="sha256:" + "0" * 64,
    )
    with pytest.raises(OutputHashMismatch):
        validate_outputs(result, context)
```

- [ ] **Step 2: Implement fixed validation order**

```text
protocol and invocation ID
path containment
manifest output permission
record registry parsing
canonicalization and hash recalculation
declared hash comparison
record-reference validation
candidate graph invariants
produced-file hashing
atomic records-and-blobs commit
```

No partial canonical commit is allowed.

- [ ] **Step 3: Run and commit**

```bash
uv run pytest tests/v4/execution/test_output_validation.py -q
git add src/zamery_education_v4/kernel/execution tests/v4/execution
git commit -m "feat(education-v4): validate capability trust boundary"
```

### Task 12: Compile immutable execution plans

**Files:**
- Create: `src/zamery_education_v4/kernel/records/execution.py`
- Create: `src/zamery_education_v4/application/run_planning/catalog.py`
- Create: `src/zamery_education_v4/application/run_planning/dependencies.py`
- Create: `src/zamery_education_v4/application/run_planning/planner.py`
- Create: `tests/v4/application/run_planning/`

**Interfaces:**
- Produces `ExecutionNode`, `ExecutionPlan`, `CapabilityCatalog`, and `build_execution_plan`.

- [ ] **Step 1: Write deterministic-plan test**

```python
def test_same_inputs_produce_same_plan_hash(context) -> None:
    first = build_execution_plan(**context)
    second = build_execution_plan(**context)
    assert first.calculated_hash == second.calculated_hash
    assert [node.node_id for node in first.nodes] == sorted(node.node_id for node in first.nodes)
```

Add missing approval, unsupported target, missing manifest, stale graph hash, and capability-cycle tests.

- [ ] **Step 2: Implement execution records**

Each node contains stable node ID, capability ID/version/runtime digest, sorted input hashes, expected outputs, normalized configuration, cache key, retry policy, and required approval scopes.

- [ ] **Step 3: Implement deterministic topological order**

Use Kahn sorting and `node_id` as the ready-queue tie breaker. Refuse capability cycles.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/application/run_planning -q
git add src/zamery_education_v4/kernel/records/execution.py src/zamery_education_v4/application/run_planning tests/v4/application/run_planning
git commit -m "feat(education-v4): compile deterministic execution plans"
```

### Task 13: Implement cache identity and DAG scheduling

**Files:**
- Create: `src/zamery_education_v4/kernel/execution/cache.py`
- Create: `src/zamery_education_v4/kernel/execution/scheduler.py`
- Create: `src/zamery_education_v4/kernel/execution/receipts.py`
- Create: `src/zamery_education_v4/kernel/execution/retry.py`
- Create: `tests/v4/execution/test_cache.py`
- Create: `tests/v4/execution/test_scheduler.py`
- Create: `tests/v4/execution/test_retry.py`

**Interfaces:**
- Produces `CacheKey`, `ExecutionReceipt`, `DagExecutor`, and `ExecutionSummary`.

- [ ] **Step 1: Write cache identity tests**

```python
def test_machine_local_values_do_not_change_cache_key(context) -> None:
    left = calculate_cache_key(**context, temp_dir="/tmp/a", hostname="one")
    right = calculate_cache_key(**context, temp_dir="/tmp/b", hostname="two")
    assert left == right
```

Version, runtime digest, input hash, normalized configuration, protocol version, and relevant policy version must change the key.

- [ ] **Step 2: Write scheduler failure-boundary test**

```python
@pytest.mark.asyncio
async def test_peer_branch_can_finish_when_render_branch_fails(executor, plan) -> None:
    summary = await executor.execute(plan)
    assert summary.node("student-workbook").status == "success"
    assert summary.node("presentation-render").status == "failure"
    assert summary.node("pack-publication").status == "blocked"
```

- [ ] **Step 3: Implement scheduling**

Launch only dependency-ready nodes, deduplicate equal cache keys, commit valid outputs before unblocking dependents, emit receipts for cache hits and executions, cap retries, and block downstream nodes on non-retryable failure.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/execution/test_cache.py tests/v4/execution/test_scheduler.py tests/v4/execution/test_retry.py -q
git add src/zamery_education_v4/kernel/execution tests/v4/execution
git commit -m "feat(education-v4): execute cached deterministic DAGs"
```

### Task 14: Add impact analysis and deterministic resume

**Files:**
- Create: `src/zamery_education_v4/application/impact_analysis/models.py`
- Create: `src/zamery_education_v4/application/impact_analysis/service.py`
- Create: `src/zamery_education_v4/application/resume/service.py`
- Create: `tests/v4/application/impact_analysis/`
- Create: `tests/v4/application/resume/`

**Interfaces:**
- Produces `ImpactReport`, `analyze_impact`, and `build_resume_plan`.

- [ ] **Step 1: Write duration-change impact test**

```python
def test_duration_change_preserves_unrelated_content(fixture) -> None:
    report = analyze_impact(**fixture)
    assert "content-unit:vocabulary" in report.preserved_ids
    assert "artifact-spec:teacher-guide" in report.invalidated_ids
    assert "artifact-spec:presentation" in report.invalidated_ids
```

- [ ] **Step 2: Write resume rejection test**

```python
def test_resume_rejects_changed_input_graph(previous_plan, current_graph) -> None:
    with pytest.raises(ResumeRejected, match="input graph hash changed"):
        build_resume_plan(previous_plan, (), current_graph)
```

- [ ] **Step 3: Implement dependency-reason traversal**

Impact includes changed records, invalidated IDs, preserved IDs, edge reasons, and materiality. Resume reuses only successful nodes whose cache, approvals, outputs, and policies remain valid.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/application/impact_analysis tests/v4/application/resume -q
git add src/zamery_education_v4/application/impact_analysis src/zamery_education_v4/application/resume tests/v4/application
git commit -m "feat(education-v4): add selective invalidation and resume"
```

### Task 15: Add Python and Node reference capabilities

**Files:**
- Create: `capabilities/reference/python_echo/`
- Create: `capabilities/reference/node_echo/`
- Create: `tests/v4/protocol/test_reference_capabilities.py`

**Interfaces:**
- Produces two locked reference implementations used by capability conformance tests.

- [ ] **Step 1: Write cross-language hash parity test**

Launch both capabilities with the same invocation and assert identical canonical record hashes.

- [ ] **Step 2: Implement Python reference**

Read one invocation from stdin, write one declared record under output mount, calculate canonical hash, and emit one result object.

- [ ] **Step 3: Implement Node reference**

Use Node 22, a committed `package-lock.json`, and the same canonical serialization fixture corpus.

- [ ] **Step 4: Run and commit**

```bash
uv run pytest tests/v4/protocol/test_reference_capabilities.py -q
git add capabilities/reference tests/v4/protocol/test_reference_capabilities.py
git commit -m "test(education-v4): add cross-language protocol references"
```

### Task 16: Expose the operator CLI

**Files:**
- Create: `src/zamery_education_v4/cli/app.py`
- Create: `src/zamery_education_v4/cli/graph.py`
- Create: `src/zamery_education_v4/cli/run.py`
- Create: `src/zamery_education_v4/cli/index.py`
- Create: `src/zamery_education_v4/cli/cache.py`
- Create: `src/zamery_education_v4/cli/output.py`
- Create: `tests/v4/cli/test_cli.py`
- Modify: `pyproject.toml`

**Interfaces:**
- Produces `zamery-v4` with `graph`, `plan`, `run`, `resume`, `impact`, `index`, and `cache` groups.

- [ ] **Step 1: Write CLI contract test**

```python
def test_help_lists_required_groups(runner) -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("graph", "plan", "run", "resume", "impact", "index", "cache"):
        assert command in result.stdout
```

- [ ] **Step 2: Register entry point**

```toml
[project.scripts]
zamery-v4 = "zamery_education_v4.cli.app:main"
```

Commands support `--json`; failures include stable code, affected IDs, and next allowed action.

- [ ] **Step 3: Run Part 2 exit gate**

```bash
uv sync --extra dev
uv run pytest tests/v4/protocol tests/v4/execution tests/v4/application tests/v4/cli -q
uv run zamery-v4 --help
uv run ruff check src tests capabilities/reference
uv run mypy src/zamery_education_v4
```

- [ ] **Step 4: Commit**

```bash
git add src/zamery_education_v4/cli tests/v4/cli pyproject.toml
git commit -m "feat(education-v4): expose governed execution CLI"
```
