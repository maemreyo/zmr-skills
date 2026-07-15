from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from ..hashing import content_hash


@dataclass(frozen=True)
class IndexFingerprint:
    records: str
    graphs: str
    edges: str

class GraphIndex:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def fingerprint(self) -> IndexFingerprint:
        db = self.connect()
        try:
            records = [
                tuple(row)
                for row in db.execute("SELECT * FROM records ORDER BY record_id")
            ]
            graphs = [
                tuple(row)
                for row in db.execute("SELECT * FROM graphs ORDER BY graph_id")
            ]
            edges = [
                tuple(row)
                for row in db.execute(
                    "SELECT * FROM edges "
                    "ORDER BY graph_id, source_id, target_id, edge_type"
                )
            ]
        finally:
            db.close()
        return IndexFingerprint(
            content_hash(records),
            content_hash(graphs),
            content_hash(edges),
        )

    def record_hash(self, record_id: str) -> str | None:
        db = self.connect()
        try:
            row = db.execute(
                "SELECT record_hash FROM records WHERE record_id=?",
                (record_id,),
            ).fetchone()
        finally:
            db.close()
        return None if row is None else str(row[0])
