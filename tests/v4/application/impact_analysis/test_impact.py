from zamery_education_v4.application.impact_analysis import analyze_impact
from zamery_education_v4.kernel.graph import EdgeType, GraphEdge, PackGraph
from zamery_education_v4.kernel.records.context import TeachingBrief
from zamery_education_v4.kernel.records.artifacts import ArtifactSpec


def test_duration_change_invalidates_dependents() -> None:
    brief = TeachingBrief(record_id="brief:1", duration_minutes=90, learner_level="A2", source_ids=())
    teacher = ArtifactSpec(record_id="artifact-spec:teacher-guide", artifact_kind="guide", audience="teacher", content_record_ids=(), format="docx")
    graph = PackGraph.from_records("g", (brief, teacher), (GraphEdge(source_id=brief.record_id, target_id=teacher.record_id, edge_type=EdgeType.USES_DURATION),))
    report = analyze_impact(graph=graph, changed_ids=(brief.record_id,))
    assert teacher.record_id in report.invalidated_ids
