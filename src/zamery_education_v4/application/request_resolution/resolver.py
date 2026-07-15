from __future__ import annotations

from .models import DomainProfile, TeachingRequestRecord, WorkflowPlan, WorkflowStage
from .rules import PACK_STAGES, WORKSHEET_STAGES


def resolve_workflow(request: TeachingRequestRecord) -> WorkflowPlan:
    deliverables = set(request.requested_deliverables)
    goal = request.lifecycle_goal
    reasons: list[str] = []

    if goal:
        reasons.append("explicit_lifecycle_goal")
    elif {"student_workbook", "teacher_guide", "presentation"} & deliverables:
        goal = "publish_teaching_pack"
        reasons.append("requested_deliverables")
    elif request.quantity and request.quantity >= 200:
        goal = "build_item_bank"
        reasons.append("quantity_reuse")
    elif request.graded or request.quantity == 100:
        goal = "publish_assessment"
        reasons.append("graded_status")
    elif "video_activity" in deliverables or "video" in request.source_kinds:
        goal = "publish_video_learning"
        reasons.append("source_sensitivity")
    else:
        goal = "publish_worksheet"
        reasons.append("default_worksheet")

    if goal == "publish_teaching_pack":
        stages = PACK_STAGES
    elif goal == "build_item_bank":
        stages = (WorkflowStage.BUILD_TEACHING_BRIEF, WorkflowStage.DESIGN_LEARNING_BLUEPRINT, WorkflowStage.AUTHOR_ITEM_BANK, WorkflowStage.REVIEW_PUBLISH)
    elif goal == "publish_assessment":
        stages = (WorkflowStage.BUILD_TEACHING_BRIEF, WorkflowStage.DESIGN_LEARNING_BLUEPRINT, WorkflowStage.AUTHOR_ITEM_BANK, WorkflowStage.ASSEMBLE_ASSESSMENT, WorkflowStage.REVIEW_PUBLISH)
    elif goal == "publish_video_learning":
        stages = (WorkflowStage.RESOLVE_SOURCE_AUTHORITY, WorkflowStage.BUILD_TEACHING_BRIEF, WorkflowStage.BUILD_VIDEO_ACTIVITY, WorkflowStage.REVIEW_PUBLISH)
    elif goal == "build_reteaching_loop":
        stages = (WorkflowStage.BUILD_TEACHING_BRIEF, WorkflowStage.BUILD_RETEACHING_LOOP, WorkflowStage.REVIEW_PUBLISH)
    else:
        stages = WORKSHEET_STAGES

    terms = {term.casefold() for term in request.domain_terms}
    if "ielts" in terms:
        if goal == "publish_teaching_pack" and "textbook" in request.source_kinds:
            profiles = (DomainProfile.IELTS_FOUNDATION_COURSEBOOK,)
        else:
            profiles = (DomainProfile.IELTS_PRACTICE,)
    elif goal == "publish_assessment":
        profiles = (DomainProfile.ASSESSMENT,)
    elif goal == "publish_video_learning":
        profiles = (DomainProfile.MEDIA_LEARNING,)
    else:
        profiles = (DomainProfile.GENERAL_ENGLISH,)
    return WorkflowPlan(primary_goal=goal, stages=stages, domain_profiles=profiles, reasons=tuple(reasons))
