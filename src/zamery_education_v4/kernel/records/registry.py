from __future__ import annotations

from collections.abc import Iterable

from ..canonical_json import canonical_json_bytes

from .approvals import ApprovalRecord
from .artifacts import ArtifactSpec, DeliveryBundleSpec, GeneratedArtifact, PublishedBundleRecord
from .base import CanonicalRecord
from .content import AnswerRecord, ItemRecord
from .context import SourceRecord, TeachingBrief
from .evidence import EvidenceReceipt, GateDecision, ReviewRecord
from .execution import ExecutionNode, ExecutionPlan, RetryPolicy
from .migration import MigrationReceipt
from .planning import AssessmentDecisionRule, ObjectiveRecord


class RecordRegistry:
    def __init__(self, models: Iterable[type[CanonicalRecord]] = ()) -> None:
        self._models: dict[str, type[CanonicalRecord]] = {}
        for model in models:
            self.register(model)

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
        return self._models[record_type].model_validate_json(canonical_json_bytes(clean))

    def export_schemas(self) -> dict[str, dict[str, object]]:
        return {name: model.model_json_schema() for name, model in sorted(self._models.items())}


def default_registry() -> RecordRegistry:
    return RecordRegistry((
        SourceRecord, TeachingBrief, ObjectiveRecord, AssessmentDecisionRule,
        ItemRecord, AnswerRecord, ArtifactSpec, GeneratedArtifact,
        DeliveryBundleSpec, PublishedBundleRecord, ApprovalRecord,
        RetryPolicy, ExecutionNode, ExecutionPlan, EvidenceReceipt, ReviewRecord,
        GateDecision, MigrationReceipt,
    ))
