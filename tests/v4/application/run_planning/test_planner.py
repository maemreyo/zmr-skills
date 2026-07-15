from zamery_education_v4.application.run_planning.planner import build_execution_plan
from zamery_education_v4.protocol.manifest import CapabilityManifest


def test_same_inputs_produce_same_plan_hash() -> None:
    manifest = CapabilityManifest(capability_id="a", capability_version="1", outputs=("x",), deterministic=True, runtime_kind="python", runtime_version="3.12", runtime_digest="sha256:"+"a"*64, lockfile_hash="sha256:"+"b"*64)
    context = dict(record_id="plan:1", input_graph_hash="sha256:"+"c"*64, policy_version="p1", node_specs=({"node_id":"b","capability_id":"a","dependencies":("a",)}, {"node_id":"a","capability_id":"a"}), manifests={"a":manifest})
    first = build_execution_plan(**context)
    second = build_execution_plan(**context)
    assert first.calculated_hash == second.calculated_hash
    assert [node.node_id for node in first.nodes] == ["a", "b"]
