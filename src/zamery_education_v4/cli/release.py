from __future__ import annotations
import json
from pathlib import Path
import typer
from ..application.release import verify_release
app=typer.Typer(help="Verify release and cutover criteria.")
@app.command("verify")
def verify(profile: str="production", evidence: Path | None=None, commit: str="working-tree") -> None:
    payload=json.loads(evidence.read_text()) if evidence else {}
    report=verify_release(commit,payload)
    typer.echo(report.model_dump_json(indent=2))
    if not report.passed: raise typer.Exit(7)
