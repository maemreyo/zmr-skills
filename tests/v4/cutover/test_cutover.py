import pytest
from zamery_education_v4.application.cutover import CutoverRejected, PipelineConfig, switch_pipeline

def test_full_v4_requires_accepted_canary() -> None:
    current=PipelineConfig(mode="v3",final_v3_tag="education-v3-final")
    with pytest.raises(CutoverRejected, match="accepted canary"):
        switch_pipeline(current,mode="v4",commit="abc",verification_report_hash="sha256:"+"a"*64,actor="operator",reason="cutover")

def test_rollback_preserves_final_v3_tag() -> None:
    current=PipelineConfig(mode="v4",final_v3_tag="education-v3-final",canary_accepted=True)
    result=switch_pipeline(current,mode="v3",commit="abc",verification_report_hash=None,actor="operator",reason="rollback")
    assert result.final_v3_tag == "education-v3-final"
