from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, Literal

from ..records.execution import ExecutionNode, ExecutionPlan
from .cache import CacheStore
from .retry import should_retry


NodeStatus = Literal["success", "failure", "cache_hit", "blocked"]


@dataclass(frozen=True)
class NodeExecutionResult:
    node_id: str
    status: NodeStatus
    output_hashes: tuple[str, ...] = ()
    failure_code: str | None = None
    attempts: int = 1

    @property
    def dependency_satisfied(self) -> bool:
        return self.status in {"success", "cache_hit"}


class ExecutionSummary:
    def __init__(self, results: dict[str, NodeExecutionResult]) -> None:
        self.results = dict(results)

    def node(self, node_id: str) -> NodeExecutionResult:
        return self.results[node_id]

    @property
    def successful(self) -> bool:
        return all(
            result.status in {"success", "cache_hit"}
            for result in self.results.values()
        )


class DagExecutor:
    def __init__(
        self,
        execute_node: Callable[[ExecutionNode], Awaitable[NodeExecutionResult]],
        *,
        cache: CacheStore | None = None,
        max_concurrency: int = 4,
    ) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be positive")
        self.execute_node = execute_node
        self.cache = cache or CacheStore()
        self.max_concurrency = max_concurrency

    async def _run_node(
        self,
        node: ExecutionNode,
        semaphore: asyncio.Semaphore,
    ) -> NodeExecutionResult:
        cached = self.cache.get(node.cache_key)
        if isinstance(cached, NodeExecutionResult):
            return NodeExecutionResult(
                node_id=node.node_id,
                status="cache_hit",
                output_hashes=cached.output_hashes,
                attempts=0,
            )

        attempt = 0
        while True:
            attempt += 1
            async with semaphore:
                result = await self.execute_node(node)
            result = NodeExecutionResult(
                node_id=node.node_id,
                status=result.status,
                output_hashes=tuple(sorted(set(result.output_hashes))),
                failure_code=result.failure_code,
                attempts=attempt,
            )
            if result.status in {"success", "cache_hit"}:
                self.cache.put(node.cache_key, result)
                return result
            if result.status != "failure" or result.failure_code is None:
                return result
            if not should_retry(
                attempt=attempt,
                max_attempts=node.retry_max_attempts,
                failure_code=result.failure_code,
                retryable_codes=node.retryable_codes,
            ):
                return result

    async def execute(self, plan: ExecutionPlan) -> ExecutionSummary:
        nodes = {node.node_id: node for node in plan.nodes}
        unknown_dependencies = {
            dependency
            for node in plan.nodes
            for dependency in node.dependencies
            if dependency not in nodes
        }
        if unknown_dependencies:
            raise ValueError(
                f"unknown execution dependencies: {sorted(unknown_dependencies)}"
            )

        results: dict[str, NodeExecutionResult] = {}
        pending = set(nodes)
        semaphore = asyncio.Semaphore(self.max_concurrency)

        while pending:
            progress = False
            ready: list[ExecutionNode] = []
            for node_id in sorted(tuple(pending)):
                node = nodes[node_id]
                dependencies = [results.get(dep) for dep in node.dependencies]
                if any(
                    dependency is not None
                    and dependency.status in {"failure", "blocked"}
                    for dependency in dependencies
                ):
                    results[node_id] = NodeExecutionResult(
                        node_id=node_id,
                        status="blocked",
                        failure_code="DEPENDENCY_FAILED",
                        attempts=0,
                    )
                    pending.remove(node_id)
                    progress = True
                    continue
                if all(
                    dependency in results
                    and results[dependency].dependency_satisfied
                    for dependency in node.dependencies
                ):
                    ready.append(node)
            if ready:
                completed = await asyncio.gather(
                    *(self._run_node(node, semaphore) for node in ready)
                )
                for result in completed:
                    results[result.node_id] = result
                    pending.remove(result.node_id)
                progress = True
            if not progress:
                raise RuntimeError("execution plan cannot make progress")
        return ExecutionSummary(results)
