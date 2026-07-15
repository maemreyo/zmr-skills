from __future__ import annotations
from .models import ComparisonReport

def compare_outcomes(v3: dict[str, object], v4: dict[str, object]) -> ComparisonReport:
    old = tuple(sorted(str(x) for x in v3.get("deliverables", [])))
    new = tuple(sorted(str(x) for x in v4.get("deliverables", [])))
    severe: list[str] = []
    if set(old) - set(new): severe.append("LOST_SUPPORTED_DELIVERABLE")
    if not bool(v3.get("answer_leakage", False)) and bool(v4.get("answer_leakage", False)): severe.append("NEW_ANSWER_LEAKAGE")
    if bool(v3.get("core_source_preserved", True)) and not bool(v4.get("core_source_preserved", False)): severe.append("LOST_CORE_SOURCE_ACTIVITY")
    if bool(v3.get("binary_reopen", True)) and not bool(v4.get("binary_reopen", False)): severe.append("FAILED_BINARY_REOPEN")
    if bool(v3.get("teacher_command_surface", True)) and not bool(v4.get("teacher_command_surface", False)): severe.append("MISSING_TEACHER_COMMAND_SURFACE")
    if not bool(v3.get("hard_safety_finding", False)) and bool(v4.get("hard_safety_finding", False)): severe.append("NEW_HARD_SAFETY_FINDING")
    metrics = {
        "source_lineage": bool(v4.get("source_lineage", False)),
        "objective_coverage": int(v4.get("objective_coverage", 0)),
        "answer_coverage": int(v4.get("answer_coverage", 0)),
        "notes_coverage": int(v4.get("notes_coverage", 0)),
    }
    return ComparisonReport(v3_deliverables=old, v4_deliverables=new, metrics=metrics, severe_regressions=tuple(sorted(severe)), acceptable=not severe)
