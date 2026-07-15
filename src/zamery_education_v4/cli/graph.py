from __future__ import annotations

import json
from pathlib import Path

import typer

from ..kernel.graph import PackGraph, validate_graph
from .output import emit

app = typer.Typer(help="Inspect and validate canonical graphs.")


@app.command("validate")
def validate(
    path: Path,
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    try:
        graph = PackGraph.model_validate_json(path.read_text(encoding="utf-8"))
        findings = validate_graph(graph)
    except (OSError, ValueError) as error:
        typer.echo(emit({"code": "INVALID_GRAPH", "message": str(error)}, as_json=True))
        raise typer.Exit(2) from error
    payload = {
        "graph_id": graph.graph_id,
        "graph_hash": graph.graph_hash,
        "valid": not findings,
        "findings": [finding.model_dump(mode="json") for finding in findings],
    }
    typer.echo(emit(payload, as_json=as_json))
    if findings:
        raise typer.Exit(4)


@app.command("trace")
def trace(
    graph_path: Path,
    record_id: str,
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    try:
        graph = PackGraph.model_validate_json(graph_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        typer.echo(emit({"code": "INVALID_GRAPH", "message": str(error)}, as_json=True))
        raise typer.Exit(2) from error
    ids = {record.record_id for record in graph.records}
    if record_id not in ids:
        typer.echo(emit({"code": "RECORD_NOT_FOUND", "record_id": record_id}, as_json=True))
        raise typer.Exit(2)
    payload = {
        "record_id": record_id,
        "incoming": [
            edge.model_dump(mode="json")
            for edge in graph.edges
            if edge.target_id == record_id
        ],
        "outgoing": [
            edge.model_dump(mode="json")
            for edge in graph.edges
            if edge.source_id == record_id
        ],
    }
    typer.echo(emit(payload, as_json=as_json))
