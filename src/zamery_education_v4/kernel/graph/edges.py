from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class EdgeType(StrEnum):
    DERIVED_FROM = "DERIVED_FROM"
    REFERENCES = "REFERENCES"
    IMPLEMENTS_OBJECTIVE = "IMPLEMENTS_OBJECTIVE"
    USES_AUTHORITY = "USES_AUTHORITY"
    USES_DURATION = "USES_DURATION"
    PROJECTS_TO = "PROJECTS_TO"
    GENERATED_FROM = "GENERATED_FROM"
    RENDERED_FROM = "RENDERED_FROM"
    VERIFIED_BY = "VERIFIED_BY"
    APPROVED_BY = "APPROVED_BY"
    SUPERSEDES = "SUPERSEDES"
    REVOKES = "REVOKES"
    INVALIDATES = "INVALIDATES"
    PACKAGES = "PACKAGES"


class GraphEdge(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    source_id: str
    target_id: str
    edge_type: EdgeType
