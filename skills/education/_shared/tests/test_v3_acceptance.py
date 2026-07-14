import unittest

from contracts import (
    RESPONSE_INTERACTIONS,
    ZAMERY_SKILL_NAMES,
    validate_batch_manifest,
    validate_canonical_item,
    validate_form_manifest,
    validate_media_manifest,
)


def canonical_item() -> dict[str, object]:
    return {
        "schema_version": "zamery-item.v3",
        "item_id": "grammar-g6-0001",
        "version": 1,
        "status": "approved",
        "language": "en",
        "grade_band": "grades_6_8",
        "cefr": "A2",
        "domain": "grammar",
        "skill": "language_use",
        "objective_ids": ["OBJ-SVA-01"],
        "interaction": "single_choice",
        "response_mode": "selected",
        "cognitive_operation": "apply",
        "difficulty": 0.45,
        "stem": "Choose the correct verb: Mina ___ to school every day.",
        "options": [
            {"option_id": "A", "text": "walk"},
            {"option_id": "B", "text": "walks"},
            {"option_id": "C", "text": "walking"},
        ],
        "answer": {"correct_option_ids": ["B"]},
        "rationale": "A singular third-person subject takes -s in the present simple.",
        "source_anchors": [
            {
                "source_id": "teacher-brief-01",
                "authority": "teacher_supplied",
                "locator": "objective-2",
            }
        ],
        "tags": ["present-simple", "subject-verb-agreement"],
    }


class V3FoundationAcceptanceTests(unittest.TestCase):
    def test_suite_declares_twelve_unique_v3_skills(self) -> None:
        self.assertEqual(len(ZAMERY_SKILL_NAMES), 12)
        self.assertEqual(len(set(ZAMERY_SKILL_NAMES)), 12)
        for name in (
            "zamery-build-english-item-banks",
            "zamery-compose-english-assessments",
            "zamery-create-ielts-practice",
            "zamery-build-video-learning",
        ):
            self.assertIn(name, ZAMERY_SKILL_NAMES)
        self.assertNotIn("zamery-assess-english-learning", ZAMERY_SKILL_NAMES)

    def test_interaction_taxonomy_supports_large_variety(self) -> None:
        self.assertGreaterEqual(len(RESPONSE_INTERACTIONS), 24)
        for interaction in (
            "single_choice",
            "matching",
            "ordering",
            "cloze",
            "error_correction",
            "essay",
            "oral_response",
            "timestamped_video_response",
        ):
            self.assertIn(interaction, RESPONSE_INTERACTIONS)

    def test_canonical_item_accepts_a_grounded_versioned_item(self) -> None:
        self.assertEqual(validate_canonical_item(canonical_item()), [])

    def test_canonical_item_rejects_missing_source_and_invalid_choice_key(self) -> None:
        item = canonical_item()
        item["source_anchors"] = []
        item["answer"] = {"correct_option_ids": ["Z"]}
        errors = validate_canonical_item(item)
        self.assertIn("source_anchors must be a non-empty list", errors)
        self.assertIn("correct option IDs must exist in options", errors)

    def test_batch_manifest_supports_resumable_400_item_runs(self) -> None:
        manifest = {
            "schema_version": "zamery-batch.v3",
            "batch_id": "bank-july-400",
            "requested_count": 400,
            "chunk_size": 40,
            "completed_item_ids": [f"item-{index:04d}" for index in range(280)],
            "seed": 20260714,
            "status": "in_progress",
        }
        self.assertEqual(validate_batch_manifest(manifest), [])

    def test_batch_manifest_rejects_duplicate_progress_and_bad_counts(self) -> None:
        manifest = {
            "schema_version": "zamery-batch.v3",
            "batch_id": "broken",
            "requested_count": 80,
            "chunk_size": 100,
            "completed_item_ids": ["item-1", "item-1"],
            "seed": 7,
            "status": "in_progress",
        }
        errors = validate_batch_manifest(manifest)
        self.assertIn("chunk_size must be between 1 and requested_count", errors)
        self.assertIn("completed_item_ids must be unique", errors)

    def test_form_manifest_requires_reproducibility_and_stable_versions(self) -> None:
        manifest = {
            "schema_version": "zamery-form.v3",
            "form_id": "midterm-a",
            "blueprint_id": "midterm-blueprint",
            "seed": 91,
            "items": [
                {"item_id": "item-0001", "version": 2, "section_id": "reading"},
                {"item_id": "item-0002", "version": 1, "section_id": "grammar"},
            ],
        }
        self.assertEqual(validate_form_manifest(manifest), [])
        manifest["items"].append(
            {"item_id": "item-0001", "version": 3, "section_id": "grammar"}
        )
        self.assertIn("form item IDs must be unique", validate_form_manifest(manifest))

    def test_media_manifest_distinguishes_link_from_authorized_transcript(self) -> None:
        manifest = {
            "schema_version": "zamery-media.v3",
            "media_id": "video-lesson-01",
            "url": "https://www.youtube.com/watch?v=abcdefghijk",
            "duration_seconds": 420,
            "transcript": {
                "authority": "public_link_only",
                "grounding_status": "ungrounded",
                "teacher_verification_required": True,
            },
            "accessibility": {"captions_available": False, "alternative_text": True},
        }
        self.assertEqual(validate_media_manifest(manifest), [])
        manifest["transcript"]["grounding_status"] = "verified"
        self.assertIn(
            "public_link_only transcripts cannot be marked verified",
            validate_media_manifest(manifest),
        )


if __name__ == "__main__":
    unittest.main()
