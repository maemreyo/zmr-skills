from __future__ import annotations

from dataclasses import dataclass

from ..storage import BlobStore, RecordStore
from .output_validation import ValidatedCapabilityOutputs


@dataclass(frozen=True)
class CommittedOutputs:
    record_hashes: tuple[str, ...]
    blob_hashes: tuple[str, ...]


def commit_outputs(outputs: ValidatedCapabilityOutputs, record_store: RecordStore, blob_store: BlobStore) -> CommittedOutputs:
    # Validation must happen before this function; commits are content-addressed and idempotent.
    records = tuple(sorted(record_store.commit(record) for record in outputs.records))
    blobs = tuple(sorted(blob_store.commit_file(path) for path in outputs.files))
    return CommittedOutputs(records, blobs)
