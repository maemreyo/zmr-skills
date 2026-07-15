from __future__ import annotations
import typer
app=typer.Typer(help="Evaluate and explain gates.")
@app.command("explain")
def explain(gate: str) -> None: typer.echo(f"gate: {gate}")
