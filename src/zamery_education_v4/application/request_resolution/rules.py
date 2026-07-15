from __future__ import annotations

from .models import WorkflowStage

PACK_STAGES = (
    WorkflowStage.RESOLVE_SOURCE_AUTHORITY,
    WorkflowStage.BUILD_TEACHING_BRIEF,
    WorkflowStage.DESIGN_LEARNING_BLUEPRINT,
    WorkflowStage.AUTHOR_PRACTICE_CONTENT,
    WorkflowStage.COMPOSE_STUDENT_MATERIALS,
    WorkflowStage.COMPOSE_TEACHER_MATERIALS,
    WorkflowStage.COMPOSE_PRESENTATION,
    WorkflowStage.REVIEW_PUBLISH,
)

WORKSHEET_STAGES = (
    WorkflowStage.BUILD_TEACHING_BRIEF,
    WorkflowStage.DESIGN_LEARNING_BLUEPRINT,
    WorkflowStage.AUTHOR_PRACTICE_CONTENT,
    WorkflowStage.COMPOSE_STUDENT_MATERIALS,
    WorkflowStage.REVIEW_PUBLISH,
)
