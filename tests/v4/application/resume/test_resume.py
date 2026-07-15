import pytest

from zamery_education_v4.application.resume import ResumeRejected, build_resume_plan
from zamery_education_v4.kernel.records.execution import ExecutionPlan


def test_resume_rejects_changed_input_graph() -> None:
    plan = ExecutionPlan(record_id="p", input_graph_hash="sha256:"+"a"*64, policy_version="p", nodes=())
    with pytest.raises(ResumeRejected, match="input graph hash changed"):
        build_resume_plan(plan, (), "sha256:"+"b"*64)
