from __future__ import annotations
import json
from pathlib import Path
import typer
from ..application.comparison import compare_outcomes
app=typer.Typer(help="Compare governed V3 and V4 outcome metrics.")
@app.command("run")
def run(v3: Path, v4: Path) -> None:
    report=compare_outcomes(json.loads(v3.read_text()), json.loads(v4.read_text()))
    typer.echo(report.model_dump_json(indent=2))
