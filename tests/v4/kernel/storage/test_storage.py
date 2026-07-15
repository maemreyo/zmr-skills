from pathlib import Path

import pytest

from zamery_education_v4.kernel.graph import PackGraph
from zamery_education_v4.kernel.records.context import TeachingBrief
from zamery_education_v4.kernel.storage import BlobStore, RecordStore, rebuild_index
from zamery_education_v4.kernel.storage.errors import ContentHashMismatch


def test_tampered_record_is_rejected(tmp_path: Path) -> None:
    store = RecordStore(tmp_path)
    brief = TeachingBrief(record_id="brief:1", duration_minutes=90, learner_level="A2", source_ids=())
    digest = store.commit(brief)
    store.path_for(digest).write_text('{"record_type":"teaching_brief"}')
    with pytest.raises(ContentHashMismatch):
        store.load(digest)


def test_blob_round_trip(tmp_path: Path) -> None:
    store = BlobStore(tmp_path)
    digest = store.commit_bytes(b"hello")
    with store.open(digest) as stream:
        assert stream.read() == b"hello"


def test_rebuild_is_deterministic(tmp_path: Path) -> None:
    store = RecordStore(tmp_path)
    brief = TeachingBrief(record_id="brief:1", duration_minutes=90, learner_level="A2", source_ids=())
    store.commit(brief)
    graph = PackGraph.from_records("graph:1", (brief,))
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(graph.model_dump_json())
    index_path = tmp_path / "graph.sqlite"
    first = rebuild_index(index_path, store, (graph_path,))
    index_path.unlink()
    second = rebuild_index(index_path, store, (graph_path,))
    assert first == second
