import unittest

from scripts.validate_blueprint import validate_blueprint


VALID = {
    "blueprint_id": "bp-1",
    "grade_band": "grades_6_8",
    "cefr": None,
    "target_language": "en",
    "instruction_language": "vi",
    "duration_minutes": 45,
    "methodology": "contrastive_pairs",
    "objectives": [{"objective_id": "obj-1", "statement": "Distinguish past simple from present perfect."}],
    "phases": [
        {"phase_id": "engage", "minutes": 5, "objective_ids": ["obj-1"]},
        {"phase_id": "teach", "minutes": 15, "objective_ids": ["obj-1"]},
        {"phase_id": "practice", "minutes": 20, "objective_ids": ["obj-1"]},
        {"phase_id": "close", "minutes": 5, "objective_ids": ["obj-1"]},
    ],
    "provenance": {"grade_band": "explicit", "cefr": "not_supplied", "methodology": "explicit"},
}


class BlueprintValidatorTests(unittest.TestCase):
    def test_valid_blueprint_passes(self) -> None:
        self.assertEqual(validate_blueprint(VALID), [])

    def test_phase_minutes_must_equal_duration(self) -> None:
        changed = {**VALID, "phases": VALID["phases"][:-1]}
        self.assertIn("phase minutes must equal duration_minutes", validate_blueprint(changed))

    def test_objective_ids_must_be_unique(self) -> None:
        changed = {**VALID, "objectives": [VALID["objectives"][0], VALID["objectives"][0]]}
        self.assertIn("objective IDs must be unique", validate_blueprint(changed))

    def test_cefr_cannot_be_derived_from_grade(self) -> None:
        changed = {**VALID, "cefr": "B1", "provenance": {**VALID["provenance"], "cefr": "derived_from_grade"}}
        self.assertIn("cefr provenance may not be derived_from_grade", validate_blueprint(changed))

    def test_every_objective_must_appear_in_a_phase(self) -> None:
        changed = {
            **VALID,
            "objectives": [
                VALID["objectives"][0],
                {"objective_id": "obj-2", "statement": "Use both forms in a new context."},
            ],
        }
        self.assertIn("objective obj-2 is not covered by any phase", validate_blueprint(changed))

    def test_grade_band_must_be_inside_k12(self) -> None:
        changed = {**VALID, "grade_band": "college"}
        self.assertIn("grade_band must be a supported K–12 band", validate_blueprint(changed))


if __name__ == "__main__":
    unittest.main()
