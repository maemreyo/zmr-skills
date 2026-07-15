from __future__ import annotations
from datetime import datetime, timezone
from .config import PipelineConfig
class CutoverRejected(ValueError): pass

def switch_pipeline(current: PipelineConfig, *, mode: str, commit: str, verification_report_hash: str | None, actor: str, reason: str, canary_accepted: bool=False) -> PipelineConfig:
    if mode not in {"v3","v4-canary","v4"}: raise CutoverRejected("unsupported pipeline mode")
    if mode in {"v4-canary","v4"} and not verification_report_hash: raise CutoverRejected("verification report required")
    if mode == "v4" and not (canary_accepted or current.canary_accepted): raise CutoverRejected("accepted canary required")
    if mode == "v3" and not current.final_v3_tag: raise CutoverRejected("final V3 tag required for rollback")
    return PipelineConfig(mode=mode,final_v3_tag=current.final_v3_tag,commit=commit,verification_report_hash=verification_report_hash,canary_accepted=canary_accepted or current.canary_accepted,actor=actor,reason=reason,changed_at=datetime.now(timezone.utc).isoformat())
