from __future__ import annotations

from pathlib import Path

import typer

from ..kernel.storage import RecordStore, StoreLayout, rebuild_index
from .output import emit

app = typer.Typer(help="Rebuild and inspect the disposable SQLite index.")


@app.command("rebuild")
def rebuild(
    root: Path = Path("."),
    graph: list[Path] | None = typer.Option(None, "--graph"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    try:
        layout = StoreLayout(root)
        fingerprint = rebuild_index(
            layout.index_path,
            RecordStore(root),
            graph or [],
        )
    except (OSError, ValueError, RuntimeError) as error:
        typer.echo(emit({"code": "INDEX_REBUILD_FAILED", "message": str(error)}, as_json=True))
        raise typer.Exit(5) from error
    typer.echo(
        emit(
            {
                "index_path": str(layout.index_path),
                "fingerprint": {
                    "records": fingerprint.records,
                    "graphs": fingerprint.graphs,
                    "edges": fingerprint.edges,
                },
            },
            as_json=as_json,
        )
    )
