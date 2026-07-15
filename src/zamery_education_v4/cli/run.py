from __future__ import annotations

from pathlib import Path

import typer

from ..kernel.records.execution import ExecutionPlan
from .output import emit

app = typer.Typer(help="Validate, inspect, and execute governed plans.")


@app.command("start")
def start(
    plan: Path,
    dry_run: bool = typer.Option(True, "--dry-run/--execute"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    try:
        execution_plan = ExecutionPlan.model_validate_json(
            plan.read_text(encoding="utf-8")
        )
    except (OSError, ValueError) as error:
        typer.echo(emit({"code": "INVALID_EXECUTION_PLAN", "message": str(error)}, as_json=True))
        raise typer.Exit(2) from error
    payload = {
        "plan_hash": execution_plan.calculated_hash,
        "input_graph_hash": execution_plan.input_graph_hash,
        "nodes": [node.node_id for node in execution_plan.nodes],
        "dry_run": dry_run,
    }
    if not dry_run:
        payload["code"] = "CAPABILITY_BINDINGS_REQUIRED"
        typer.echo(emit(payload, as_json=True))
        raise typer.Exit(5)
    typer.echo(emit(payload, as_json=as_json))


@app.command("explain")
def explain(
    plan: Path,
    node_id: str | None = None,
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    try:
        execution_plan = ExecutionPlan.model_validate_json(
            plan.read_text(encoding="utf-8")
        )
    except (OSError, ValueError) as error:
        typer.echo(emit({"code": "INVALID_EXECUTION_PLAN", "message": str(error)}, as_json=True))
        raise typer.Exit(2) from error
    nodes = execution_plan.nodes
    if node_id is not None:
        nodes = tuple(node for node in nodes if node.node_id == node_id)
        if not nodes:
            typer.echo(emit({"code": "NODE_NOT_FOUND", "node_id": node_id}, as_json=True))
            raise typer.Exit(2)
    typer.echo(
        emit(
            {
                "plan_hash": execution_plan.calculated_hash,
                "nodes": [node.model_dump(mode="json") for node in nodes],
            },
            as_json=as_json,
        )
    )
