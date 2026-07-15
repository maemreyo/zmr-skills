from __future__ import annotations
import typer
app=typer.Typer(help="Plan and explain selective repairs.")
@app.command("explain")
def explain(finding: str) -> None: typer.echo(f"repair: {finding}")
