from __future__ import annotations

from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict, field_validator

from ..hashing import content_hash
from ..records.base import CanonicalRecord
from ..records.identity import RecordRef
from .edges import GraphEdge


class PackGraph(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    graph_id: str
    records: tuple[RecordRef, ...]
    edges: tuple[GraphEdge, ...] = ()

    @field_validator("records")
    @classmethod
    def records_sorted_unique(cls, values: tuple[RecordRef, ...]) -> tuple[RecordRef, ...]:
        by_id = {value.record_id: value for value in values}
        if len(by_id) != len(values):
            raise ValueError("duplicate graph record id")
        return tuple(sorted(values, key=lambda value: value.record_id))

    @field_validator("edges")
    @classmethod
    def edges_sorted_unique(cls, values: tuple[GraphEdge, ...]) -> tuple[GraphEdge, ...]:
        unique = {(v.source_id, v.target_id, v.edge_type): v for v in values}
        return tuple(sorted(unique.values(), key=lambda v: (v.source_id, v.target_id, v.edge_type)))

    @classmethod
    def from_records(
        cls, graph_id: str, records: Iterable[CanonicalRecord], edges: Iterable[GraphEdge] = ()
    ) -> "PackGraph":
        refs = tuple(
            RecordRef(record_id=r.record_id, record_type=r.record_type, record_hash=r.calculated_hash)
            for r in records
        )
        return cls(graph_id=graph_id, records=refs, edges=tuple(edges))

    @property
    def graph_hash(self) -> str:
        return content_hash({
            "graph_id": self.graph_id,
            "records": [record.model_dump(mode="json") for record in self.records],
            "edges": [edge.model_dump(mode="json") for edge in self.edges],
        })
