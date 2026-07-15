from zamery_education_v4.kernel.graph import EdgeType, GraphEdge, PackGraph, validate_graph
from zamery_education_v4.kernel.records.content import ItemRecord
from zamery_education_v4.kernel.records.context import TeachingBrief
from zamery_education_v4.kernel.records.planning import AssessmentDecisionRule


def test_threshold_cannot_exceed_unique_membership() -> None:
    brief = TeachingBrief(record_id="brief:1", duration_minutes=90, learner_level="A2", source_ids=())
    rule = AssessmentDecisionRule(record_id="rule:1", member_item_ids=("item:1", "item:2"), threshold=3, outcome="reteach")
    graph = PackGraph.from_records("graph:1", (brief, rule))
    findings = validate_graph(graph, {brief.record_id: brief, rule.record_id: rule})
    assert "DECISION_THRESHOLD_EXCEEDS_MEMBERSHIP" in {item.code for item in findings}


def test_cycles_are_rejected() -> None:
    a = TeachingBrief(record_id="brief:a", duration_minutes=30, learner_level="A1", source_ids=())
    b = ItemRecord(record_id="item:b", prompt="x", scored=False)
    graph = PackGraph.from_records("graph:cycle", (a, b), (
        GraphEdge(source_id=a.record_id, target_id=b.record_id, edge_type=EdgeType.DERIVED_FROM),
        GraphEdge(source_id=b.record_id, target_id=a.record_id, edge_type=EdgeType.DERIVED_FROM),
    ))
    assert "GRAPH_CYCLE" in {finding.code for finding in validate_graph(graph)}
