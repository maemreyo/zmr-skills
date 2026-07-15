from __future__ import annotations

from ...kernel.hashing import content_hash
from ...kernel.records.evidence import Finding
from ..impact_analysis.models import ImpactReport
from .materiality import Materiality, classify_materiality
from .models import RepairPlan


def build_repair_plan(
    *,
    findings: tuple[Finding, ...],
    impact: ImpactReport,
    change_kinds: tuple[str, ...],
    rerun_map: dict[str, tuple[str, ...]] | None = None,
) -> RepairPlan:
    material = classify_materiality(change_kinds) == Materiality.MATERIAL
    affected = tuple(sorted({record_id for finding in findings for record_id in finding.affected_ids}))
    codes = {finding.code for finding in findings}
    default_reruns = tuple(sorted({run for code in codes for run in (rerun_map or {}).get(code, ("affected_inspector", "gate_aggregation"))}))
    approvals = ("content", "publication") if material else ()
    return RepairPlan(
        affected_ids=affected, invalidated_ids=impact.invalidated_ids, preserved_ids=impact.preserved_ids,
        required_reruns=default_reruns, required_approval_scopes=approvals,
        expected_receipt_types=tuple(sorted({finding.code.casefold() for finding in findings})),
        original_finding_hashes=tuple(sorted({content_hash(finding.model_dump(mode="json")) for finding in findings})),
        material=material,
    )
