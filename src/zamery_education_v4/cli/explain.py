from __future__ import annotations

from pathlib import Path

import typer

from ..application.explain import explain_record
from ..kernel.graph import PackGraph
from .output import emit

app = typer.Typer(help="Explain provenance and governed decisions.")


@app.command("record")
def record(record_id: str) -> None:
    typer.echo(emit(explain_record(record_id)))


@app.command("artifact")
def artifact(
    graph_path: Path,
    artifact_id: str,
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    try:
        graph = PackGraph.model_validate_json(graph_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        typer.echo(emit({"code": "INVALID_GRAPH", "message": str(error)}, as_json=True))
        raise typer.Exit(2) from error
    incoming = tuple(
        f"{edge.source_id}:{edge.edge_type}"
        for edge in graph.edges
        if edge.target_id == artifact_id
    )
    outgoing = tuple(
        f"{edge.edge_type}:{edge.target_id}"
        for edge in graph.edges
        if edge.source_id == artifact_id
    )
    typer.echo(
        emit(
            explain_record(
                artifact_id,
                incoming=incoming,
                outgoing=outgoing,
            ),
            as_json=as_json,
        )
    )
