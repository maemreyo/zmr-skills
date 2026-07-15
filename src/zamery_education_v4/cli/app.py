from __future__ import annotations

from pathlib import Path

import typer

from ..application.impact_analysis import analyze_impact
from ..application.request_resolution import TeachingRequestRecord, resolve_workflow
from ..application.resume import build_resume_plan
from ..kernel.graph import PackGraph
from ..kernel.records.execution import ExecutionPlan
from . import cache, comparison, explain, gate, golden, graph, index, release, repair, run
from .output import emit

app = typer.Typer(
    help="Zamery Education V4 governed production pipeline.",
    no_args_is_help=True,
)
app.add_typer(graph.app, name="graph")
app.add_typer(run.app, name="run")
app.add_typer(index.app, name="index")
app.add_typer(cache.app, name="cache")
app.add_typer(comparison.app, name="comparison")
app.add_typer(explain.app, name="explain")
app.add_typer(gate.app, name="gate")
app.add_typer(repair.app, name="repair")
app.add_typer(golden.app, name="golden")
app.add_typer(release.app, name="release")


@app.command("plan")
def plan(
    request: Path,
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    try:
        teaching_request = TeachingRequestRecord.model_validate_json(
            request.read_text(encoding="utf-8")
        )
        workflow = resolve_workflow(teaching_request)
    except (OSError, ValueError) as error:
        typer.echo(emit({"code": "INVALID_REQUEST", "message": str(error)}, as_json=True))
        raise typer.Exit(2) from error
    typer.echo(emit(workflow.model_dump(mode="json"), as_json=as_json))


@app.command("resume")
def resume(
    plan_path: Path,
    current_graph_hash: str,
    successful_node: list[str] | None = typer.Option(None, "--successful-node"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    try:
        previous = ExecutionPlan.model_validate_json(
            plan_path.read_text(encoding="utf-8")
        )
        resumed = build_resume_plan(
            previous,
            tuple(successful_node or []),
            current_graph_hash,
        )
    except (OSError, ValueError) as error:
        typer.echo(emit({"code": "RESUME_REJECTED", "message": str(error)}, as_json=True))
        raise typer.Exit(2) from error
    typer.echo(emit(resumed.canonical_payload(), as_json=as_json))


@app.command("impact")
def impact(
    graph_path: Path,
    changed_id: list[str] = typer.Option(..., "--changed-id"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    try:
        pack_graph = PackGraph.model_validate_json(
            graph_path.read_text(encoding="utf-8")
        )
        report = analyze_impact(
            graph=pack_graph,
            changed_ids=tuple(changed_id),
        )
    except (OSError, ValueError) as error:
        typer.echo(emit({"code": "IMPACT_ANALYSIS_FAILED", "message": str(error)}, as_json=True))
        raise typer.Exit(2) from error
    typer.echo(emit(report.model_dump(mode="json"), as_json=as_json))


def main() -> None:
    app()
