from __future__ import annotations

import argparse
import json
import re
import uuid
import zipfile
from html import escape
from pathlib import Path
from urllib.parse import parse_qs, urlparse

YOUTUBE_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
TRANSCRIPT_AUTHORITIES = {
    "teacher_supplied", "authorized_channel", "licensed", "public_link_only", "none"
}


def parse_youtube_url(url: str) -> str | None:
    try:
        parsed = urlparse(url)
    except ValueError:
        return None
    host = parsed.netloc.casefold().removeprefix("www.")
    candidate: str | None = None
    if host == "youtu.be":
        candidate = parsed.path.strip("/").split("/")[0]
    elif host in {"youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [None])[0]
        else:
            parts = parsed.path.strip("/").split("/")
            if len(parts) >= 2 and parts[0] in {"embed", "shorts", "live"}:
                candidate = parts[1]
    return candidate if candidate and YOUTUBE_ID.fullmatch(candidate) else None


def validate_media_manifest(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "zamery-media.v3":
        errors.append("schema_version must be zamery-media.v3")
    for field in ("media_id", "title", "url", "language"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be a non-empty string")
    source_type = data.get("source_type")
    if source_type not in {"youtube", "web_video", "teacher_file"}:
        errors.append("source_type is invalid")
    if source_type == "youtube" and isinstance(data.get("url"), str) and parse_youtube_url(data["url"]) is None:
        errors.append("url is not a recognized YouTube video URL")
    duration = data.get("duration_seconds")
    if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration <= 0:
        errors.append("duration_seconds must be positive")
    transcript = data.get("transcript")
    if not isinstance(transcript, dict):
        errors.append("transcript must be an object")
    else:
        authority = transcript.get("authority")
        status = transcript.get("grounding_status")
        if authority not in TRANSCRIPT_AUTHORITIES:
            errors.append("transcript authority is invalid")
        if status not in {"verified", "grounded", "ungrounded", "unavailable"}:
            errors.append("transcript grounding_status is invalid")
        if authority == "public_link_only" and status in {"grounded", "verified"}:
            errors.append("public_link_only cannot be marked grounded or verified")
        if authority == "public_link_only" and transcript.get("teacher_verification_required") is not True:
            errors.append("public_link_only requires teacher verification")
        segments = transcript.get("segments")
        if not isinstance(segments, list):
            errors.append("transcript segments must be a list")
        else:
            ids: list[object] = []
            previous_end = 0.0
            for index, segment in enumerate(segments):
                if not isinstance(segment, dict):
                    errors.append(f"transcript segment {index} must be an object")
                    continue
                ids.append(segment.get("segment_id"))
                start, end = segment.get("start_seconds"), segment.get("end_seconds")
                if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in (start, end)) or not 0 <= start < end:
                    errors.append(f"transcript segment {index} has invalid bounds")
                else:
                    if isinstance(duration, (int, float)) and end > duration:
                        errors.append(f"transcript segment {index} exceeds media duration")
                    if start < previous_end:
                        errors.append(f"transcript segment {index} overlaps the prior segment")
                    previous_end = end
                if not isinstance(segment.get("text"), str) or not segment["text"].strip():
                    errors.append(f"transcript segment {index} requires text")
            if len(ids) != len(set(ids)) or any(not isinstance(value, str) or not value for value in ids):
                errors.append("transcript segment IDs must be non-empty and unique")
            if status in {"grounded", "verified"} and not segments:
                errors.append("grounded or verified transcripts require segments")
    accessibility = data.get("accessibility")
    if not isinstance(accessibility, dict):
        errors.append("accessibility must be an object")
    else:
        for field in ("captions_available", "alternative_text"):
            if not isinstance(accessibility.get(field), bool):
                errors.append(f"accessibility {field} must be boolean")
    return errors


def validate_timed_items(media: dict[str, object], items: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    media_errors = validate_media_manifest(media)
    if media_errors:
        return [f"media: {error}" for error in media_errors]
    duration = float(media["duration_seconds"])
    segments = media["transcript"]["segments"]
    known_segments = {segment["segment_id"] for segment in segments}
    item_ids: list[object] = []
    for index, item in enumerate(items):
        item_id = item.get("item_id")
        item_ids.append(item_id)
        label = item_id if isinstance(item_id, str) and item_id else str(index)
        if item.get("phase") not in {"before", "during", "after"}:
            errors.append(f"item {label} phase is invalid")
        timestamp = item.get("at_seconds")
        if isinstance(timestamp, bool) or not isinstance(timestamp, (int, float)) or not 0 <= timestamp <= duration:
            errors.append(f"item {label} timestamp is outside media duration")
        interaction = item.get("interaction")
        if interaction not in {"single_choice", "true_false", "text_prompt"}:
            errors.append(f"item {label} interaction is not H5P-exportable")
        if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
            errors.append(f"item {label} requires prompt")
        anchor = item.get("source_anchor")
        if not isinstance(anchor, dict):
            errors.append(f"item {label} requires source_anchor")
        else:
            start, end = anchor.get("start_seconds"), anchor.get("end_seconds")
            if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in (start, end)) or not 0 <= start < end <= duration:
                errors.append(f"item {label} source anchor bounds are invalid")
            cited = anchor.get("segment_ids")
            if not isinstance(cited, list) or not cited:
                errors.append(f"item {label} requires transcript segment IDs")
            else:
                for segment_id in cited:
                    if segment_id not in known_segments:
                        errors.append(f"item {label} cites unknown transcript segment {segment_id}")
        if interaction == "single_choice":
            options = item.get("options")
            option_ids = {option.get("option_id") for option in options or [] if isinstance(option, dict)} if isinstance(options, list) else set()
            correct = item.get("answer", {}).get("correct_option_ids") if isinstance(item.get("answer"), dict) else None
            if not isinstance(options, list) or len(options) < 2 or len(option_ids) != len(options):
                errors.append(f"item {label} requires unique options")
            if not isinstance(correct, list) or not correct or not set(correct) <= option_ids:
                errors.append(f"item {label} correct options are invalid")
        if interaction == "true_false" and not isinstance(item.get("answer", {}).get("correct") if isinstance(item.get("answer"), dict) else None, bool):
            errors.append(f"item {label} true_false answer must be boolean")
    if len(item_ids) != len(set(item_ids)) or any(not isinstance(value, str) or not value for value in item_ids):
        errors.append("timed item IDs must be non-empty and unique")
    return errors


def _action(item: dict[str, object]) -> dict[str, object]:
    sub_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"zamery:{item['item_id']}"))
    if item["interaction"] == "single_choice":
        correct = set(item["answer"]["correct_option_ids"])
        return {
            "library": "H5P.MultiChoice 1.16",
            "params": {
                "question": escape(str(item["prompt"]), quote=False),
                "answers": [
                    {
                        "text": escape(str(option["text"]), quote=False),
                        "correct": option["option_id"] in correct,
                    }
                    for option in item["options"]
                ],
                "behaviour": {"enableRetry": True, "enableSolutionsButton": True, "singlePoint": True},
            },
            "subContentId": sub_id,
            "metadata": {"contentType": "Multiple Choice", "license": "U", "title": item["item_id"]},
        }
    if item["interaction"] == "true_false":
        return {
            "library": "H5P.TrueFalse 1.8",
            "params": {
                "question": escape(str(item["prompt"]), quote=False),
                "correct": "true" if item["answer"]["correct"] else "false",
            },
            "subContentId": sub_id,
            "metadata": {"contentType": "True/False Question", "license": "U", "title": item["item_id"]},
        }
    return {
        "library": "H5P.Text 1.1",
        "params": {"text": f"<p>{escape(str(item['prompt']), quote=False)}</p>"},
        "subContentId": sub_id,
        "metadata": {"contentType": "Text", "license": "U", "title": item["item_id"]},
    }


def _zip_write(archive: zipfile.ZipFile, name: str, value: object) -> None:
    content = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, content)


def export_h5p(media: dict[str, object], items: list[dict[str, object]], destination: Path) -> None:
    errors = validate_timed_items(media, items)
    if errors:
        raise ValueError("; ".join(errors))
    libraries = {"H5P.InteractiveVideo": (1, 28), "H5P.Video": (1, 6), "H5P.Summary": (1, 10)}
    for item in items:
        machine_name, version = {
            "single_choice": ("H5P.MultiChoice", (1, 16)),
            "true_false": ("H5P.TrueFalse", (1, 8)),
            "text_prompt": ("H5P.Text", (1, 1)),
        }[item["interaction"]]
        libraries[machine_name] = version
    definition = {
        "title": media["title"],
        "mainLibrary": "H5P.InteractiveVideo",
        "language": media.get("language", "en"),
        "embedTypes": ["div"],
        "preloadedDependencies": [
            {"machineName": name, "majorVersion": version[0], "minorVersion": version[1]}
            for name, version in sorted(libraries.items())
        ],
        "source": media["url"],
        "license": "U",
        "authorComments": "Host-resolved content package: the target H5P platform must already provide the declared libraries.",
    }
    interactions = []
    for index, item in enumerate(items):
        start = float(item["at_seconds"])
        interactions.append({
            "duration": {"from": start, "to": min(start + 10, float(media["duration_seconds"]))},
            "pause": item["interaction"] != "text_prompt",
            "displayType": "poster",
            "buttonOnMobile": False,
            "label": f"<p>{escape(str(item['item_id']), quote=False)}</p>",
            "x": 10 + (index % 3) * 28,
            "y": 15 + (index % 2) * 35,
            "width": 35,
            "height": 30,
            "action": _action(item),
        })
    content = {
        "video": {
            "files": [{"path": media["url"], "mime": "video/YouTube" if media["source_type"] == "youtube" else "video/mp4"}],
            "startScreenOptions": {"title": media["title"], "hideStartTitle": False},
        },
        "assets": {"interactions": interactions, "bookmarks": [], "endscreens": []},
        "summary": {"task": {"library": "H5P.Summary 1.10", "params": {"summaries": []}}, "displayAt": 3},
        "override": {"autoplay": False, "loop": False, "hasNoAutoPause": False, "showRewind10": True, "preventSkippingMode": "none"},
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w") as archive:
        _zip_write(archive, "h5p.json", definition)
        _zip_write(archive, "content/content.json", content)


def validate_h5p_package(path: Path) -> dict[str, object]:
    errors: list[str] = []
    interaction_count = 0
    dependency_mode = "unknown"
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            bad_crc = archive.testzip()
            if bad_crc:
                errors.append(f"CRC failure in {bad_crc}")
            for required in ("h5p.json", "content/content.json"):
                if required not in names:
                    errors.append(f"missing {required}")
            if not errors:
                try:
                    definition = json.loads(archive.read("h5p.json"))
                    content = json.loads(archive.read("content/content.json"))
                except (json.JSONDecodeError, UnicodeDecodeError) as error:
                    errors.append(f"invalid JSON: {error}")
                else:
                    for field in ("title", "mainLibrary", "language", "preloadedDependencies", "embedTypes"):
                        if not definition.get(field):
                            errors.append(f"h5p.json missing {field}")
                    if definition.get("mainLibrary") != "H5P.InteractiveVideo":
                        errors.append("mainLibrary must be H5P.InteractiveVideo")
                    dependencies = {entry.get("machineName") for entry in definition.get("preloadedDependencies", [])}
                    if "H5P.InteractiveVideo" not in dependencies:
                        errors.append("main library dependency is missing")
                    interactions = content.get("assets", {}).get("interactions")
                    if not isinstance(interactions, list):
                        errors.append("content interactions must be a list")
                    else:
                        interaction_count = len(interactions)
                        for index, interaction in enumerate(interactions):
                            action = interaction.get("action", {})
                            library = str(action.get("library", "")).rsplit(" ", 1)[0]
                            if library not in dependencies:
                                errors.append(f"interaction {index} dependency {library} is undeclared")
                    bundled = any(name.endswith("/library.json") for name in names)
                    dependency_mode = "bundled" if bundled else "host_resolved"
    except (OSError, zipfile.BadZipFile) as error:
        errors.append(f"invalid package: {error}")
    return {
        "valid": not errors,
        "interaction_count": interaction_count,
        "dependency_mode": dependency_mode,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate video lessons or export host-resolved H5P Interactive Video packages.")
    parser.add_argument("media", type=Path)
    parser.add_argument("items", type=Path)
    parser.add_argument("--h5p", type=Path)
    args = parser.parse_args()
    media = json.loads(args.media.read_text(encoding="utf-8"))
    items = json.loads(args.items.read_text(encoding="utf-8"))
    errors = validate_timed_items(media, items)
    if args.h5p and not errors:
        export_h5p(media, items, args.h5p)
        report = validate_h5p_package(args.h5p)
        errors.extend(report["errors"])
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
