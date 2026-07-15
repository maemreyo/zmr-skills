from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from ..types import RecordHash
from .base import CanonicalRecord


class RetryPolicy(CanonicalRecord):
    record_type = "retry_policy"
    max_attempts: int = 1
    retryable_codes: tuple[str, ...] = ()


class ExecutionNode(CanonicalRecord):
    record_type = "execution_node"
    node_id: str
    capability_id: str
    capability_version: str
    runtime_digest: RecordHash
    input_hashes: tuple[RecordHash, ...]
    dependencies: tuple[str, ...] = ()
    expected_outputs: tuple[str, ...]
    configuration: dict[str, object] = Field(default_factory=dict)
    cache_key: RecordHash
    retry_max_attempts: int = 1
    retryable_codes: tuple[str, ...] = ()
    required_approval_scopes: tuple[str, ...] = ()

    @field_validator("input_hashes", "dependencies", "expected_outputs", "retryable_codes", "required_approval_scopes")
    @classmethod
    def sorted_unique(cls, values: tuple) -> tuple:
        return tuple(sorted(set(values)))


class ExecutionPlan(CanonicalRecord):
    record_type = "execution_plan"
    input_graph_hash: RecordHash
    policy_version: str
    nodes: tuple[ExecutionNode, ...]

    @field_validator("nodes")
    @classmethod
    def stable_nodes(cls, values: tuple[ExecutionNode, ...]) -> tuple[ExecutionNode, ...]:
        ids = [node.node_id for node in values]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate execution node id")
        return tuple(values)
