from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

INTERACTIONS = {
    "single_choice", "multiple_choice", "true_false", "matching", "ordering",
    "categorization", "fill_blank", "cloze", "dropdown_cloze", "short_answer",
    "extended_response", "error_correction", "sentence_transformation",
    "sentence_combining", "word_formation", "table_completion", "note_completion",
    "summary_completion", "labeling", "hotspot", "drag_drop", "dictation", "essay",
    "oral_response", "audio_recording", "dialogue_completion",
    "timestamped_video_response", "portfolio_evidence",
}
GRADE_BANDS = {"k_2", "grades_3_5", "grades_6_8", "grades_9_12"}
STATUSES = {"draft", "review", "approved", "retired"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _content_hash(item: dict[str, object]) -> str:
    return hashlib.sha256(_canonical_json(item).encode("utf-8")).hexdigest()


def validate_item(item: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if item.get("schema_version") != "zamery-item.v3":
        errors.append("schema_version must be zamery-item.v3")
    for field in ("item_id", "language", "cefr", "domain", "skill", "stem", "rationale"):
        if not isinstance(item.get(field), str) or not str(item[field]).strip():
            errors.append(f"{field} must be a non-empty string")
    version = item.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version < 1:
        errors.append("version must be a positive integer")
    if item.get("status") not in STATUSES:
        errors.append("status is invalid")
    if item.get("grade_band") not in GRADE_BANDS:
        errors.append("grade_band is invalid")
    if item.get("interaction") not in INTERACTIONS:
        errors.append("interaction is invalid")
    if item.get("response_mode") not in {"selected", "constructed", "spoken", "performance", "mixed"}:
        errors.append("response_mode is invalid")
    if item.get("cognitive_operation") not in {"remember", "understand", "apply", "analyze", "evaluate", "create"}:
        errors.append("cognitive_operation is invalid")
    difficulty = item.get("difficulty")
    if isinstance(difficulty, bool) or not isinstance(difficulty, (int, float)) or not 0 <= difficulty <= 1:
        errors.append("difficulty must be between 0 and 1")
    if not isinstance(item.get("objective_ids"), list) or not item["objective_ids"]:
        errors.append("objective_ids must be a non-empty list")
    anchors = item.get("source_anchors")
    if not isinstance(anchors, list) or not anchors:
        errors.append("source_anchors must be a non-empty list")
    else:
        for anchor in anchors:
            if not isinstance(anchor, dict) or not all(
                isinstance(anchor.get(field), str) and anchor[field].strip()
                for field in ("source_id", "authority", "locator")
            ):
                errors.append("each source anchor requires source_id, authority, and locator")
                break
    if not isinstance(item.get("answer"), dict) or not item["answer"]:
        errors.append("answer must be a non-empty object")
    if not isinstance(item.get("tags"), list):
        errors.append("tags must be a list")
    if item.get("interaction") in {"single_choice", "multiple_choice"}:
        options = item.get("options")
        valid_option_fields = isinstance(options, list) and all(
            isinstance(option, dict)
            and isinstance(option.get("option_id"), str)
            and option["option_id"].strip()
            and isinstance(option.get("text"), str)
            and option["text"].strip()
            for option in options
        )
        if not valid_option_fields:
            errors.append("choice options require non-empty option_id and text")
        option_ids = {
            option.get("option_id") for option in options or [] if isinstance(option, dict)
        } if isinstance(options, list) else set()
        if not isinstance(options, list) or len(options) < 2 or len(option_ids) != len(options):
            errors.append("choice items require unique options")
        answer = item.get("answer")
        correct = answer.get("correct_option_ids") if isinstance(answer, dict) else None
        if not isinstance(correct, list) or not correct or not set(correct) <= option_ids:
            errors.append("correct option IDs must exist in options")
        elif item.get("interaction") == "single_choice" and len(correct) != 1:
            errors.append("single_choice answer must identify exactly one option")
    return errors


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS batches (
    batch_id TEXT PRIMARY KEY,
    requested_count INTEGER NOT NULL CHECK(requested_count > 0),
    chunk_size INTEGER NOT NULL CHECK(chunk_size > 0),
    seed INTEGER NOT NULL,
    status TEXT NOT NULL,
    completed_count INTEGER NOT NULL DEFAULT 0,
    manifest_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS items (
    item_id TEXT NOT NULL,
    version INTEGER NOT NULL CHECK(version > 0),
    status TEXT NOT NULL,
    interaction TEXT NOT NULL,
    domain TEXT NOT NULL,
    skill TEXT NOT NULL,
    grade_band TEXT NOT NULL,
    cefr TEXT NOT NULL,
    difficulty REAL NOT NULL,
    stem TEXT NOT NULL,
    content_json TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    batch_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(item_id, version),
    FOREIGN KEY(batch_id) REFERENCES batches(batch_id)
);
CREATE INDEX IF NOT EXISTS idx_items_status ON items(status);
CREATE INDEX IF NOT EXISTS idx_items_blueprint ON items(domain, skill, interaction, difficulty);
CREATE TABLE IF NOT EXISTS ingest_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id TEXT NOT NULL,
    item_id TEXT,
    version INTEGER,
    action TEXT NOT NULL,
    content_hash TEXT,
    detail TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS duplicate_pairs (
    item_id_a TEXT NOT NULL,
    version_a INTEGER NOT NULL,
    item_id_b TEXT NOT NULL,
    version_b INTEGER NOT NULL,
    method TEXT NOT NULL,
    score REAL NOT NULL,
    checked_at TEXT NOT NULL,
    PRIMARY KEY(item_id_a, version_a, item_id_b, version_b)
);
"""


def init_database(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.executescript(SCHEMA)


def _ensure_batch(
    connection: sqlite3.Connection,
    batch_id: str,
    requested_count: int,
    chunk_size: int,
    seed: int,
) -> None:
    if requested_count < 1 or not 1 <= chunk_size <= requested_count:
        raise ValueError("batch counts are invalid")
    row = connection.execute(
        "SELECT requested_count, chunk_size, seed FROM batches WHERE batch_id = ?", (batch_id,)
    ).fetchone()
    manifest = {
        "schema_version": "zamery-batch.v3",
        "batch_id": batch_id,
        "requested_count": requested_count,
        "chunk_size": chunk_size,
        "seed": seed,
    }
    if row and tuple(row) != (requested_count, chunk_size, seed):
        raise ValueError("resume parameters do not match the stored batch")
    if not row:
        connection.execute(
            "INSERT INTO batches VALUES (?, ?, ?, ?, 'in_progress', 0, ?, ?)",
            (batch_id, requested_count, chunk_size, seed, _canonical_json(manifest), _now()),
        )


def ingest_jsonl(
    database: Path,
    source: Path,
    *,
    batch_id: str,
    requested_count: int,
    chunk_size: int | None = None,
    seed: int = 0,
) -> dict[str, int]:
    init_database(database)
    if chunk_size is None:
        chunk_size = min(40, requested_count)
    result = {"inserted": 0, "unchanged": 0, "rejected": 0}
    rejections: list[dict[str, object]] = []
    with sqlite3.connect(database) as connection:
        _ensure_batch(connection, batch_id, requested_count, chunk_size, seed)
        for line_number, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                item = json.loads(raw)
            except json.JSONDecodeError as error:
                errors = [f"invalid JSON: {error.msg}"]
                item = None
            else:
                errors = validate_item(item) if isinstance(item, dict) else ["record must be an object"]
            if errors:
                result["rejected"] += 1
                rejections.append({"line": line_number, "errors": errors})
                connection.execute(
                    "INSERT INTO ingest_events(batch_id, action, detail, created_at) VALUES (?, 'rejected', ?, ?)",
                    (batch_id, _canonical_json({"line": line_number, "errors": errors}), _now()),
                )
                continue
            assert isinstance(item, dict)
            digest = _content_hash(item)
            key = (item["item_id"], item["version"])
            existing = connection.execute(
                "SELECT content_hash FROM items WHERE item_id = ? AND version = ?", key
            ).fetchone()
            if existing:
                if existing[0] == digest:
                    action = "unchanged"
                    result[action] += 1
                else:
                    action = "rejected"
                    result[action] += 1
                    rejections.append({
                        "line": line_number,
                        "item_id": item["item_id"],
                        "version": item["version"],
                        "errors": ["same item_id and version has different content"],
                    })
                connection.execute(
                    "INSERT INTO ingest_events(batch_id, item_id, version, action, content_hash, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (batch_id, item["item_id"], item["version"], action, digest, _now()),
                )
                continue
            connection.execute(
                """INSERT INTO items(
                    item_id, version, status, interaction, domain, skill, grade_band, cefr,
                    difficulty, stem, content_json, content_hash, batch_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    item["item_id"], item["version"], item["status"], item["interaction"],
                    item["domain"], item["skill"], item["grade_band"], item["cefr"],
                    item["difficulty"], item["stem"], _canonical_json(item), digest, batch_id, _now(),
                ),
            )
            connection.execute(
                "INSERT INTO ingest_events(batch_id, item_id, version, action, content_hash, created_at) VALUES (?, ?, ?, 'inserted', ?, ?)",
                (batch_id, item["item_id"], item["version"], digest, _now()),
            )
            result["inserted"] += 1
        completed = connection.execute(
            "SELECT COUNT(DISTINCT item_id) FROM ingest_events WHERE batch_id = ? AND action IN ('inserted', 'unchanged')",
            (batch_id,),
        ).fetchone()[0]
        status = "complete" if completed >= requested_count else "in_progress"
        connection.execute(
            "UPDATE batches SET completed_count = ?, status = ?, updated_at = ? WHERE batch_id = ?",
            (completed, status, _now(), batch_id),
        )
    rejection_path = source.with_suffix(".rejections.jsonl")
    if rejections:
        rejection_path.write_text(
            "".join(_canonical_json(record) + "\n" for record in rejections), encoding="utf-8"
        )
    elif rejection_path.exists():
        rejection_path.unlink()
    return result


def _latest_items(connection: sqlite3.Connection) -> list[dict[str, object]]:
    rows = connection.execute(
        """SELECT content_json FROM items i
        WHERE version = (SELECT MAX(version) FROM items WHERE item_id = i.item_id)
        ORDER BY item_id"""
    ).fetchall()
    return [json.loads(row[0]) for row in rows]


def export_jsonl(database: Path, destination: Path) -> int:
    with sqlite3.connect(database) as connection:
        items = _latest_items(connection)
    destination.write_text(
        "".join(_canonical_json(item) + "\n" for item in items), encoding="utf-8"
    )
    return len(items)


def export_review_csv(database: Path, destination: Path) -> int:
    with sqlite3.connect(database) as connection:
        items = _latest_items(connection)
    fields = [
        "item_id", "version", "status", "grade_band", "cefr", "domain", "skill",
        "interaction", "difficulty", "stem", "options_json", "answer_json",
        "objective_ids_json", "source_anchors_json", "tags_json",
    ]
    with destination.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in items:
            writer.writerow({
                **{field: item.get(field, "") for field in fields if not field.endswith("_json")},
                "options_json": _canonical_json(item.get("options", [])),
                "answer_json": _canonical_json(item.get("answer", {})),
                "objective_ids_json": _canonical_json(item.get("objective_ids", [])),
                "source_anchors_json": _canonical_json(item.get("source_anchors", [])),
                "tags_json": _canonical_json(item.get("tags", [])),
            })
    return len(items)


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[\w']+", text.casefold()))


def deduplicate_bank(database: Path, destination: Path, *, threshold: float = 0.86) -> int:
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    with sqlite3.connect(database) as connection:
        items = _latest_items(connection)
        connection.execute("DELETE FROM duplicate_pairs")
        rows: list[dict[str, object]] = []
        for left_index, left in enumerate(items):
            for right in items[left_index + 1:]:
                left_text = " ".join(str(left.get(field, "")) for field in ("stem", "rationale"))
                right_text = " ".join(str(right.get(field, "")) for field in ("stem", "rationale"))
                normalized_left = " ".join(left_text.casefold().split())
                normalized_right = " ".join(right_text.casefold().split())
                if normalized_left == normalized_right:
                    method, score = "exact", 1.0
                else:
                    a, b = _tokens(left_text), _tokens(right_text)
                    score = len(a & b) / len(a | b) if a | b else 1.0
                    if score < threshold:
                        continue
                    method = "near"
                record = {
                    "item_id_a": left["item_id"], "version_a": left["version"],
                    "item_id_b": right["item_id"], "version_b": right["version"],
                    "method": method, "score": round(score, 6),
                }
                rows.append(record)
                connection.execute(
                    "INSERT INTO duplicate_pairs VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (*record.values(), _now()),
                )
    with destination.open("w", encoding="utf-8-sig", newline="") as handle:
        fields = ["item_id_a", "version_a", "item_id_b", "version_b", "method", "score"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def validate_database(database: Path) -> dict[str, object]:
    with sqlite3.connect(database) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        versions = connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        approved = connection.execute(
            "SELECT COUNT(DISTINCT item_id) FROM items WHERE status = 'approved'"
        ).fetchone()[0]
        invalid_json = 0
        invalid_items = 0
        for (content,) in connection.execute("SELECT content_json FROM items"):
            try:
                item = json.loads(content)
            except json.JSONDecodeError:
                invalid_json += 1
            else:
                invalid_items += bool(validate_item(item))
    return {
        "integrity": integrity,
        "item_versions": versions,
        "approved_items": approved,
        "invalid_json": invalid_json,
        "invalid_items": invalid_items,
    }
