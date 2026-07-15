from zamery_education_v4.application.impact_analysis.models import ImpactReport
from zamery_education_v4.application.repair_planning import build_repair_plan
from zamery_education_v4.kernel.records.evidence import Finding


def test_material_change_requires_approval() -> None:
    impact = ImpactReport(changed_ids=("item:1",), invalidated_ids=("item:1","artifact:1"), preserved_ids=("brief:1",), reasons={}, material=True)
    plan = build_repair_plan(findings=(Finding(code="X", message="x", affected_ids=("item:1",)),), impact=impact, change_kinds=("scoring_membership",))
    assert plan.material
    assert "content" in plan.required_approval_scopes
