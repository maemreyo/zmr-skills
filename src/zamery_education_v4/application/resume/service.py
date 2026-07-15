from __future__ import annotations

from ...kernel.records.execution import ExecutionPlan


class ResumeRejected(ValueError):
    pass


def build_resume_plan(
    previous_plan: ExecutionPlan,
    successful_node_ids: tuple[str, ...],
    current_graph_hash: str,
    *,
    valid_cache_keys: set[str] | None = None,
) -> ExecutionPlan:
    if previous_plan.input_graph_hash != current_graph_hash:
        raise ResumeRejected("input graph hash changed")
    reusable = set(successful_node_ids)
    if valid_cache_keys is not None:
        reusable = {node.node_id for node in previous_plan.nodes if node.node_id in reusable and node.cache_key in valid_cache_keys}
    nodes = tuple(node for node in previous_plan.nodes if node.node_id not in reusable)
    return previous_plan.model_copy(update={"record_id": previous_plan.record_id + ":resume", "nodes": nodes})
