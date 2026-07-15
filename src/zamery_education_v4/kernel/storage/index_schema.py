SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE records(record_id TEXT PRIMARY KEY, record_type TEXT NOT NULL, record_hash TEXT NOT NULL UNIQUE);
CREATE TABLE graphs(graph_id TEXT PRIMARY KEY, graph_hash TEXT NOT NULL);
CREATE TABLE edges(graph_id TEXT NOT NULL, source_id TEXT NOT NULL, target_id TEXT NOT NULL, edge_type TEXT NOT NULL,
  PRIMARY KEY(graph_id, source_id, target_id, edge_type));
"""
