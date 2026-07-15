from __future__ import annotations

import shutil
from pathlib import Path

import typer

from .output import emit

app = typer.Typer(help="Inspect and clear content-addressed execution cache.")


def _cache_root(root: Path) -> Path:
    return root / ".zamery" / "cache"


@app.command("inspect")
def inspect(
    key: str,
    root: Path = Path("."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    normalized = key.removeprefix("sha256:")
    path = _cache_root(root) / f"{normalized}.json"
    payload = {
        "key": key,
        "exists": path.is_file(),
        "path": str(path),
        "size_bytes": path.stat().st_size if path.is_file() else 0,
    }
    typer.echo(emit(payload, as_json=as_json))


@app.command("clear")
def clear(
    root: Path = Path("."),
    yes: bool = typer.Option(False, "--yes"),
) -> None:
    path = _cache_root(root)
    if not yes:
        typer.echo("Refusing to clear cache without --yes")
        raise typer.Exit(2)
    shutil.rmtree(path, ignore_errors=True)
    typer.echo(str(path))
