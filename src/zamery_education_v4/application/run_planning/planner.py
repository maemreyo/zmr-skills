from __future__ import annotations

from collections.abc import Iterable

from ...kernel.execution.cache import calculate_cache_key
from ...kernel.records.execution import ExecutionNode, ExecutionPlan
from ...protocol.manifest import CapabilityManifest
from .dependencies import topological_order


def build_execution_plan(
    *,
    record_id: str,
    input_graph_hash: str,
    policy_version: str,
    node_specs: Iterable[dict[str, object]],
    manifests: dict[str, CapabilityManifest],
) -> ExecutionPlan:
    specs = {str(spec["node_id"]): dict(spec) for spec in node_specs}
    order = topological_order({node_id: tuple(spec.get("dependencies", ())) for node_id, spec in specs.items()})
    nodes: list[ExecutionNode] = []
    for node_id in order:
        spec = specs[node_id]
        capability_id = str(spec["capability_id"])
        manifest = manifests[capability_id]
        inputs = tuple(sorted(spec.get("input_hashes", ())))
        configuration = dict(spec.get("configuration", {}))
        cache_key = calculate_cache_key(
            capability_id=manifest.capability_id,
            capability_version=manifest.capability_version,
            runtime_digest=manifest.runtime_digest,
            input_hashes=inputs,
            configuration=configuration,
            protocol_version=manifest.protocol_version,
            policy_version=policy_version,
        )
        nodes.append(ExecutionNode(
            record_id=f"execution-node:{node_id}", node_id=node_id,
            capability_id=capability_id, capability_version=manifest.capability_version,
            runtime_digest=manifest.runtime_digest, input_hashes=inputs,
            dependencies=tuple(spec.get("dependencies", ())),
            expected_outputs=tuple(spec.get("expected_outputs", manifest.outputs)),
            configuration=configuration, cache_key=cache_key,
            retry_max_attempts=int(spec.get("retry_max_attempts", 1)),
            retryable_codes=tuple(spec.get("retryable_codes", ())),
            required_approval_scopes=tuple(spec.get("required_approval_scopes", ())),
        ))
    return ExecutionPlan(record_id=record_id, input_graph_hash=input_graph_hash, policy_version=policy_version, nodes=tuple(nodes))
