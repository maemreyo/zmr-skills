import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.video_learning import (
    export_h5p,
    parse_youtube_url,
    validate_h5p_package,
    validate_media_manifest,
    validate_timed_items,
)


MEDIA = {
    "schema_version": "zamery-media.v3",
    "media_id": "yt-lesson-01",
    "title": "City transport interview",
    "source_type": "youtube",
    "url": "https://www.youtube.com/watch?v=abcdefghijk",
    "duration_seconds": 420,
    "language": "en",
    "transcript": {
        "authority": "teacher_supplied",
        "grounding_status": "verified",
        "teacher_verification_required": False,
        "segments": [
            {"segment_id": "s1", "start_seconds": 0, "end_seconds": 30, "text": "Today we discuss city transport."},
            {"segment_id": "s2", "start_seconds": 30, "end_seconds": 75, "text": "The speaker compares buses and trains."},
        ],
    },
    "accessibility": {"captions_available": True, "alternative_text": True},
}

TIMED_ITEMS = [
    {
        "item_id": "video-q1",
        "phase": "during",
        "at_seconds": 32,
        "interaction": "single_choice",
        "prompt": "Which two types of transport are compared?",
        "options": [
            {"option_id": "A", "text": "Buses and trains"},
            {"option_id": "B", "text": "Cars and bicycles"},
        ],
        "answer": {"correct_option_ids": ["A"]},
        "source_anchor": {"start_seconds": 30, "end_seconds": 75, "segment_ids": ["s2"]},
    },
    {
        "item_id": "video-q2",
        "phase": "after",
        "at_seconds": 76,
        "interaction": "true_false",
        "prompt": "The clip compares buses and trains.",
        "answer": {"correct": True},
        "source_anchor": {"start_seconds": 30, "end_seconds": 75, "segment_ids": ["s2"]},
    },
]


class VideoLearningTests(unittest.TestCase):
    def test_parses_common_youtube_urls(self) -> None:
        urls = [
            "https://www.youtube.com/watch?v=abcdefghijk&t=30s",
            "https://youtu.be/abcdefghijk",
            "https://www.youtube.com/embed/abcdefghijk",
            "https://www.youtube.com/shorts/abcdefghijk",
        ]
        self.assertEqual([parse_youtube_url(url) for url in urls], ["abcdefghijk"] * 4)
        self.assertIsNone(parse_youtube_url("https://example.com/watch?v=abcdefghijk"))

    def test_verified_teacher_transcript_manifest_passes(self) -> None:
        self.assertEqual(validate_media_manifest(MEDIA), [])

    def test_public_link_alone_cannot_claim_a_verified_transcript(self) -> None:
        changed = {
            **MEDIA,
            "transcript": {
                "authority": "public_link_only",
                "grounding_status": "verified",
                "teacher_verification_required": False,
                "segments": [],
            },
        }
        errors = validate_media_manifest(changed)
        self.assertIn("public_link_only cannot be marked grounded or verified", errors)
        self.assertIn("public_link_only requires teacher verification", errors)

    def test_timed_items_require_in_bounds_grounding(self) -> None:
        self.assertEqual(validate_timed_items(MEDIA, TIMED_ITEMS), [])
        changed = [{**TIMED_ITEMS[0], "at_seconds": 500}]
        self.assertIn("item video-q1 timestamp is outside media duration", validate_timed_items(MEDIA, changed))
        changed = [{**TIMED_ITEMS[0], "source_anchor": {"start_seconds": 30, "end_seconds": 75, "segment_ids": ["missing"]}}]
        self.assertIn("item video-q1 cites unknown transcript segment missing", validate_timed_items(MEDIA, changed))

    def test_h5p_export_is_a_structurally_valid_host_resolved_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "video-lesson.h5p"
            export_h5p(MEDIA, TIMED_ITEMS, package)
            report = validate_h5p_package(package)
            self.assertTrue(report["valid"])
            self.assertEqual(report["interaction_count"], 2)
            self.assertEqual(report["dependency_mode"], "host_resolved")
            with zipfile.ZipFile(package) as archive:
                self.assertEqual(set(archive.namelist()), {"h5p.json", "content/content.json"})
                definition = json.loads(archive.read("h5p.json"))
                self.assertEqual(definition["mainLibrary"], "H5P.InteractiveVideo")

    def test_h5p_export_escapes_teacher_supplied_html(self) -> None:
        unsafe = {
            "item_id": "unsafe</p><script>alert(1)</script>",
            "phase": "after",
            "at_seconds": 20,
            "interaction": "text_prompt",
            "prompt": "Compare A < B. <script>alert(1)</script>",
            "source_anchor": {"start_seconds": 0, "end_seconds": 30, "segment_ids": ["s1"]},
        }
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "escaped-video-lesson.h5p"
            export_h5p(MEDIA, [unsafe], package)
            with zipfile.ZipFile(package) as archive:
                content = json.loads(archive.read("content/content.json"))
            interaction = content["assets"]["interactions"][0]
            self.assertNotIn("<script>", interaction["label"])
            self.assertNotIn("<script>", interaction["action"]["params"]["text"])
            self.assertIn("&lt;script&gt;", interaction["action"]["params"]["text"])


if __name__ == "__main__":
    unittest.main()
