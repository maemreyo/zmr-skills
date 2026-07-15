import json
from pathlib import Path

from typer.testing import CliRunner

from zamery_education_v4.cli.app import app
from zamery_education_v4.kernel.graph import PackGraph
from zamery_education_v4.kernel.records.context import TeachingBrief

runner = CliRunner()


def test_plan_resolves_real_request_fixture() -> None:
    result = runner.invoke(
        app,
        [
            "plan",
            "tests/v4/fixtures/requests/full-teaching-pack.json",
            "--json",
        ],
    )
    assert result.exit_code == 0
    assert json.loads(result.stdout)["primary_goal"] == "publish_teaching_pack"


def test_graph_validate_and_trace(tmp_path: Path) -> None:
    brief = TeachingBrief(
        record_id="brief:cli",
        duration_minutes=90,
        learner_level="A2",
        source_ids=(),
    )
    graph = PackGraph.from_records("graph:cli", (brief,))
    path = tmp_path / "graph.json"
    path.write_text(graph.model_dump_json())
    validated = runner.invoke(app, ["graph", "validate", str(path), "--json"])
    assert validated.exit_code == 0
    traced = runner.invoke(
        app,
        ["graph", "trace", str(path), brief.record_id, "--json"],
    )
    assert traced.exit_code == 0
    assert json.loads(traced.stdout)["record_id"] == brief.record_id
