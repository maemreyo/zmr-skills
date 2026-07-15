from __future__ import annotations
import typer
from ..testing import GoldenRunner
app=typer.Typer(help="Run governed golden workflows.")
@app.command("run")
def run(fixture: str, profile: str="production") -> None:
    result=GoldenRunner().run_production(fixture)
    typer.echo(result.model_dump_json(indent=2))
    if not result.published: raise typer.Exit(7)
