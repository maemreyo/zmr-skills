from __future__ import annotations
from pydantic import BaseModel, ConfigDict
CRITERIA=("kernel_graph","cross_language_protocol","unit1_seven_gates","five_additional_goldens","clean_index_rebuild","semantic_determinism","reextract_reopen_rerender","known_audit_failures","no_severe_v3_regression","no_silent_migration_loss","sandbox_archive_security","teacher_classroom_usability")
class ReleaseVerificationReport(BaseModel):
    model_config=ConfigDict(extra="forbid", frozen=True, strict=True)
    commit: str
    criteria: dict[str,bool]
    passed: bool
    missing: tuple[str,...]
def verify_release(commit: str, evidence: dict[str,bool]) -> ReleaseVerificationReport:
    missing=tuple(name for name in CRITERIA if not evidence.get(name,False))
    return ReleaseVerificationReport(commit=commit,criteria={name:bool(evidence.get(name,False)) for name in CRITERIA},passed=not missing,missing=missing)
