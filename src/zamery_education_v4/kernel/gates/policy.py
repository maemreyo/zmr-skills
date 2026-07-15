from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator


class GatePolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    gate: str
    version: str
    required_receipt_types: tuple[str, ...]
    hard_block_codes: tuple[str, ...] = ()
    required_review_rubric: str | None = None
    allow_warning: bool = True

    @field_validator("required_receipt_types", "hard_block_codes")
    @classmethod
    def stable_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted(set(values)))


DEFAULT_POLICIES = {
    "brief": GatePolicy(gate="brief", version="brief-policy@4.0.0", required_receipt_types=("source_lineage",), required_review_rubric="brief-rubric@4.0.0"),
    "pedagogy": GatePolicy(gate="pedagogy", version="pedagogy-policy@4.0.0", required_receipt_types=("objective_coverage",), required_review_rubric="pedagogy-rubric@4.0.0"),
    "content": GatePolicy(gate="content", version="content-policy@4.0.0", required_receipt_types=("answer_authority", "decision_rule"), hard_block_codes=("MISSING_SOURCE_ANSWER_AUTHORITY", "DECISION_RULE_DENOMINATOR_MISMATCH")),
    "safety": GatePolicy(gate="safety", version="safety-policy@4.0.0", required_receipt_types=("safety", "privacy"), hard_block_codes=("MEDIA_PRIVACY_ALTERNATIVE_MISSING",)),
    "accessibility": GatePolicy(gate="accessibility", version="accessibility-policy@4.0.0", required_receipt_types=("accessibility", "answer_separation")),
    "presentation": GatePolicy(gate="presentation", version="presentation-policy@4.0.0", required_receipt_types=("binary_inspection", "render", "speaker_notes"), hard_block_codes=("EMPTY_SPEAKER_NOTES", "RENDER_FAILED")),
    "pack": GatePolicy(gate="pack", version="pack-policy@4.0.0", required_receipt_types=("archive_security", "reopen", "rerender"), required_review_rubric="teacher-usability@4.0.0", hard_block_codes=("REOPEN_RECEIPT_MISSING", "ARCHIVE_SECURITY_FAILED")),
}
