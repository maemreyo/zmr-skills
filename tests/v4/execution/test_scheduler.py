import pytest

from zamery_education_v4.kernel.execution.scheduler import DagExecutor, NodeExecutionResult
from zamery_education_v4.kernel.records.execution import ExecutionNode, ExecutionPlan


def node(name: str, deps=()) -> ExecutionNode:
    return ExecutionNode(record_id=f"n:{name}", node_id=name, capability_id=name, capability_version="1", runtime_digest="sha256:"+"a"*64, input_hashes=(), dependencies=deps, expected_outputs=(), cache_key="sha256:"+"a"*64)


@pytest.mark.asyncio
async def test_peer_branch_can_finish_when_render_branch_fails() -> None:
    async def execute(item):
        if item.node_id == "presentation-render":
            return NodeExecutionResult(item.node_id, "failure", failure_code="RENDER")
        return NodeExecutionResult(item.node_id, "success")
    plan = ExecutionPlan(record_id="plan:1", input_graph_hash="sha256:"+"b"*64, policy_version="p", nodes=(node("student-workbook"), node("presentation-render"), node("pack-publication", ("student-workbook", "presentation-render"))))
    summary = await DagExecutor(execute).execute(plan)
    assert summary.node("student-workbook").status == "success"
    assert summary.node("presentation-render").status == "failure"
    assert summary.node("pack-publication").status == "blocked"


@pytest.mark.asyncio
async def test_retry_is_limited_to_declared_failure_codes() -> None:
    attempts = 0

    async def execute(item):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return NodeExecutionResult(item.node_id, "failure", failure_code="TRANSIENT")
        return NodeExecutionResult(item.node_id, "success", output_hashes=("sha256:" + "c" * 64,))

    retrying = ExecutionNode(
        record_id="n:retry",
        node_id="retry",
        capability_id="retry",
        capability_version="1",
        runtime_digest="sha256:" + "a" * 64,
        input_hashes=(),
        expected_outputs=(),
        cache_key="sha256:" + "d" * 64,
        retry_max_attempts=2,
        retryable_codes=("TRANSIENT",),
    )
    plan = ExecutionPlan(
        record_id="plan:retry",
        input_graph_hash="sha256:" + "b" * 64,
        policy_version="p",
        nodes=(retrying,),
    )
    result = (await DagExecutor(execute).execute(plan)).node("retry")
    assert result.status == "success"
    assert result.attempts == 2
