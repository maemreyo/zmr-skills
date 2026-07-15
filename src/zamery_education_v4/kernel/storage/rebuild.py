from __future__ import annotations

import json
import os
import sqlite3
from contextlib import closing
from collections.abc import Iterable
from pathlib import Path

from ..graph.model import PackGraph
from ..hashing import sha256_bytes
from .index import GraphIndex, IndexFingerprint
from .index_schema import SCHEMA
from .record_store import RecordStore


def rebuild_index(index_path: str | Path, store: RecordStore, graph_paths: Iterable[str | Path]) -> IndexFingerprint:
    index_path = Path(index_path)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    new_path = index_path.with_suffix(index_path.suffix + ".new")
    new_path.unlink(missing_ok=True)
    with closing(sqlite3.connect(new_path)) as db:
        db.executescript(SCHEMA)
        for path in store.iter_paths():
            payload = path.read_bytes()
            digest = sha256_bytes(payload)
            decoded = json.loads(payload)
            db.execute(
                "INSERT INTO records(record_id, record_type, record_hash) VALUES(?,?,?)",
                (decoded["record_id"], decoded["record_type"], digest),
            )
        for graph_path in sorted(map(Path, graph_paths)):
            graph = PackGraph.model_validate_json(graph_path.read_text(encoding="utf-8"))
            db.execute("INSERT INTO graphs(graph_id, graph_hash) VALUES(?,?)", (graph.graph_id, graph.graph_hash))
            for edge in graph.edges:
                db.execute(
                    "INSERT INTO edges(graph_id, source_id, target_id, edge_type) VALUES(?,?,?,?)",
                    (graph.graph_id, edge.source_id, edge.target_id, edge.edge_type),
                )
        result = db.execute("PRAGMA integrity_check").fetchone()
        if not result or result[0] != "ok":
            raise RuntimeError(f"index integrity check failed: {result}")
        db.commit()
    os.replace(new_path, index_path)
    return GraphIndex(index_path).fingerprint()
