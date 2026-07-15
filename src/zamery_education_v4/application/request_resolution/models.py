from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator


class WorkflowStage(StrEnum):
    RESOLVE_SOURCE_AUTHORITY = "resolve_source_authority"
    BUILD_TEACHING_BRIEF = "build_teaching_brief"
    DESIGN_LEARNING_BLUEPRINT = "design_learning_blueprint"
    AUTHOR_PRACTICE_CONTENT = "author_practice_content"
    COMPOSE_STUDENT_MATERIALS = "compose_student_materials"
    COMPOSE_TEACHER_MATERIALS = "compose_teacher_materials"
    COMPOSE_PRESENTATION = "compose_presentation"
    REVIEW_PUBLISH = "review_publish"
    AUTHOR_ITEM_BANK = "author_item_bank"
    ASSEMBLE_ASSESSMENT = "assemble_assessment"
    BUILD_VIDEO_ACTIVITY = "build_video_activity"
    BUILD_RETEACHING_LOOP = "build_reteaching_loop"


class DomainProfile(StrEnum):
    IELTS_FOUNDATION_COURSEBOOK = "ielts_foundation_coursebook"
    IELTS_PRACTICE = "ielts_practice"
    GENERAL_ENGLISH = "general_english"
    ASSESSMENT = "assessment"
    MEDIA_LEARNING = "media_learning"


class TeachingRequestRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    record_id: str
    lifecycle_goal: str | None = None
    requested_deliverables: tuple[str, ...] = ()
    source_kinds: tuple[str, ...] = ()
    domain_terms: tuple[str, ...] = ()
    quantity: int | None = None
    current_stage: str | None = None
    graded: bool = False
    output_formats: tuple[str, ...] = ()

    @field_validator("requested_deliverables", "source_kinds", "domain_terms", "output_formats")
    @classmethod
    def sorted_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted(set(values)))


class WorkflowPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    primary_goal: str
    stages: tuple[WorkflowStage, ...]
    domain_profiles: tuple[DomainProfile, ...]
    reasons: tuple[str, ...]
