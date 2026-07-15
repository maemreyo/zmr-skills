from __future__ import annotations

from pydantic import Field, field_validator

from ..types import RecordHash
from .base import CanonicalRecord


class ArtifactSpec(CanonicalRecord):
    record_type = "artifact_spec"
    artifact_kind: str
    audience: str
    content_record_ids: tuple[str, ...]
    format: str
    configuration: dict[str, object] = Field(default_factory=dict)

    @field_validator("content_record_ids")
    @classmethod
    def sorted_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted(set(values)))


class GeneratedArtifact(CanonicalRecord):
    record_type = "generated_artifact"
    spec_id: str
    blob_hash: RecordHash
    media_type: str
    semantic_fingerprint: RecordHash | None = None


class DeliveryBundleSpec(CanonicalRecord):
    record_type = "delivery_bundle_spec"
    members: dict[str, RecordHash]


class PublishedBundleRecord(CanonicalRecord):
    record_type = "published_bundle"
    bundle_spec_id: str
    archive_hash: RecordHash
    graph_hash: RecordHash
    gate_decision_hashes: tuple[RecordHash, ...]
    publication_approval_hash: RecordHash

    @field_validator("gate_decision_hashes")
    @classmethod
    def sorted_unique(cls, values: tuple[RecordHash, ...]) -> tuple[RecordHash, ...]:
        return tuple(sorted(set(values)))
