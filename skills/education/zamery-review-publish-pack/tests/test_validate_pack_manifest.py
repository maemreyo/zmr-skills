import unittest

from scripts.validate_pack_manifest import validate_pack_manifest


VALID = {
    "pack_id": "pack-1",
    "brief_id": "brief-1",
    "objective_ids": ["obj-1"],
    "requested_formats": ["docx", "pdf", "pptx"],
    "safety_findings": [],
    "brand": {"name": "zamery", "tagline": "rooted in strength", "design_system": "zamery-core.v2"},
    "delivery_verification": {"crc_checked": True, "reextracted": True, "nested_ooxml_checked": True, "rerendered_from_extracted": True},
    "artifacts": [
        {"artifact_id": "lesson-1", "artifact_type": "lesson", "audience": "teacher", "version": 1, "objective_ids": ["obj-1"], "dependencies": []},
        {"artifact_id": "quiz-1", "artifact_type": "quiz", "audience": "student", "version": 1, "objective_ids": ["obj-1"], "dependencies": []},
        {"artifact_id": "answers-quiz-1", "artifact_type": "answer_set", "audience": "teacher", "version": 1, "objective_ids": ["obj-1"], "source_artifact_id": "quiz-1", "source_version": 1, "dependencies": [{"artifact_id": "quiz-1", "version": 1}]},
        {"artifact_id": "deck-1", "artifact_type": "slide_deck", "audience": "student", "version": 1, "objective_ids": ["obj-1"], "dependencies": [{"artifact_id": "lesson-1", "version": 1}]},
    ],
}


class PackManifestTests(unittest.TestCase):
    def test_valid_pack_passes(self) -> None:
        self.assertEqual(validate_pack_manifest(VALID), [])

    def test_unknown_objective_blocks_pack(self) -> None:
        artifact = {**VALID["artifacts"][0], "objective_ids": ["obj-missing"]}
        changed = {**VALID, "artifacts": [artifact, *VALID["artifacts"][1:]]}
        self.assertIn("artifact lesson-1 cites unknown objective obj-missing", validate_pack_manifest(changed))

    def test_stale_dependency_blocks_pack(self) -> None:
        deck = {**VALID["artifacts"][3], "dependencies": [{"artifact_id": "lesson-1", "version": 0}]}
        changed = {**VALID, "artifacts": [*VALID["artifacts"][:3], deck]}
        self.assertIn("artifact deck-1 depends on stale lesson-1 version 0; current is 1", validate_pack_manifest(changed))

    def test_answer_set_must_be_teacher_only(self) -> None:
        answer_set = {**VALID["artifacts"][2], "audience": "student"}
        changed = {**VALID, "artifacts": [*VALID["artifacts"][:2], answer_set, VALID["artifacts"][3]]}
        self.assertIn("answer_set answers-quiz-1 must be teacher-only", validate_pack_manifest(changed))

    def test_v3_structured_exports_require_specific_verification(self) -> None:
        changed = {
            **VALID,
            "requested_formats": ["jsonl", "sqlite", "qti", "h5p"],
            "delivery_verification": {
                **VALID["delivery_verification"],
                "structured_exports_checked": False,
            },
        }
        self.assertIn(
            "delivery verification requires structured_exports_checked",
            validate_pack_manifest(changed),
        )
        changed["delivery_verification"]["structured_exports_checked"] = True
        self.assertEqual(validate_pack_manifest(changed), [])

    def test_unknown_format_is_explicit(self) -> None:
        changed = {**VALID, "requested_formats": ["docx", "apkg"]}
        self.assertIn("unsupported requested format apkg", validate_pack_manifest(changed))

    def test_delivery_verification_must_cover_final_archive(self) -> None:
        changed = {**VALID, "delivery_verification": {**VALID["delivery_verification"], "rerendered_from_extracted": False}}
        self.assertIn("delivery verification requires rerendered_from_extracted", validate_pack_manifest(changed))

    def test_pii_and_answer_leakage_are_hard_blocks(self) -> None:
        changed = {
            **VALID,
            "safety_findings": [
                {"kind": "pii", "artifact_id": "quiz-1", "detail": "student email"},
                {"kind": "answer_leakage", "artifact_id": "quiz-1", "detail": "hidden answer"},
            ],
        }
        errors = validate_pack_manifest(changed)
        self.assertIn("blocking safety finding pii in quiz-1: student email", errors)
        self.assertIn("blocking safety finding answer_leakage in quiz-1: hidden answer", errors)

    def test_every_pack_objective_must_be_covered(self) -> None:
        changed = {**VALID, "objective_ids": ["obj-1", "obj-2"]}
        self.assertIn("pack objective obj-2 is not covered by any artifact", validate_pack_manifest(changed))

    def test_student_card_data_leakage_is_a_hard_block(self) -> None:
        changed = {
            **VALID,
            "safety_findings": [
                {
                    "kind": "student_card_leakage",
                    "artifact_id": "deck-1",
                    "detail": "card_id and behaviour observation on projected slide",
                }
            ],
        }
        self.assertIn(
            "blocking safety finding student_card_leakage in deck-1: card_id and behaviour observation on projected slide",
            validate_pack_manifest(changed),
        )


if __name__ == "__main__":
    unittest.main()
