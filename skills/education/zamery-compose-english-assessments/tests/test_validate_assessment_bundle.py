import unittest

from scripts.validate_assessment_bundle import validate_assessment_bundle


VALID = {
    "requested_item_count": 2,
    "requested_difficulty_distribution": {"core": 2},
    "student_artifact": {
        "artifact_id": "quiz-1",
        "audience": "student",
        "objective_ids": ["obj-1"],
        "questions": [
            {
                "question_id": "q1",
                "objective_ids": ["obj-1"],
                "response_type": "selected_response",
                "expected_response_lines": 1,
                "layout_intent": "options_below_prompt",
                "difficulty": "core",
                "prompt": "Choose the correct sentence.",
                "options": ["She went yesterday.", "She has gone yesterday."],
            },
            {
                "question_id": "q2",
                "objective_ids": ["obj-1"],
                "response_type": "explanation",
                "expected_response_lines": 4,
                "layout_intent": "full_width_ruled_response",
                "difficulty": "core",
                "prompt": "Explain why the second sentence is incorrect.",
            },
        ],
    },
    "answer_set": {
        "answer_set_id": "answers-quiz-1",
        "source_artifact_id": "quiz-1",
        "audience": "teacher",
        "answers": [
            {
                "question_id": "q1",
                "correct_option_index": 0,
                "explanation": "Finished past time takes past simple.",
                "wrong_reasons": {"1": "Present perfect conflicts with yesterday."},
            },
            {
                "question_id": "q2",
                "accepted_answers": ["Present perfect is not used with a finished past-time marker."],
                "rubric": "Award one point for identifying the time-marker conflict.",
            },
        ],
    },
}


class AssessmentBundleTests(unittest.TestCase):
    def test_valid_mixed_response_bundle_passes(self) -> None:
        self.assertEqual(validate_assessment_bundle(VALID), [])

    def test_student_answer_field_is_blocked(self) -> None:
        changed = {
            **VALID,
            "student_artifact": {
                **VALID["student_artifact"],
                "questions": [{**VALID["student_artifact"]["questions"][0], "correct_option_index": 0}],
            },
        }
        self.assertTrue(any(error.startswith("student answer leakage at") for error in validate_assessment_bundle(changed)))

    def test_answer_ids_must_match_question_ids(self) -> None:
        changed = {**VALID, "answer_set": {**VALID["answer_set"], "answers": VALID["answer_set"]["answers"][:-1]}}
        self.assertIn("AnswerSet question IDs must exactly match student question IDs", validate_assessment_bundle(changed))

    def test_selected_response_options_must_be_distinct(self) -> None:
        q1 = {**VALID["student_artifact"]["questions"][0], "options": ["She went.", " she went. "]}
        changed = {
            **VALID,
            "student_artifact": {
                **VALID["student_artifact"],
                "questions": [q1, VALID["student_artifact"]["questions"][1]],
            },
        }
        self.assertIn("question q1 has duplicate normalized options", validate_assessment_bundle(changed))

    def test_requested_item_count_is_exact(self) -> None:
        changed = {**VALID, "requested_item_count": 3}
        self.assertIn("requested_item_count does not match generated questions", validate_assessment_bundle(changed))

    def test_requested_difficulty_distribution_is_exact(self) -> None:
        changed = {**VALID, "requested_difficulty_distribution": {"core": 1, "challenge": 1}}
        self.assertIn("requested difficulty distribution does not match generated questions", validate_assessment_bundle(changed))

    def test_every_declared_objective_must_be_assessed(self) -> None:
        student = {**VALID["student_artifact"], "objective_ids": ["obj-1", "obj-2"]}
        changed = {**VALID, "student_artifact": student}
        self.assertIn("objective obj-2 is not covered by any question", validate_assessment_bundle(changed))

    def test_response_layout_metadata_is_required(self) -> None:
        q2 = {key: value for key, value in VALID["student_artifact"]["questions"][1].items() if key != "layout_intent"}
        changed = {**VALID, "student_artifact": {**VALID["student_artifact"], "questions": [VALID["student_artifact"]["questions"][0], q2]}}
        self.assertIn("question q2 requires layout_intent", validate_assessment_bundle(changed))

    def test_explanation_gets_four_response_lines(self) -> None:
        q2 = {**VALID["student_artifact"]["questions"][1], "expected_response_lines": 2}
        changed = {**VALID, "student_artifact": {**VALID["student_artifact"], "questions": [VALID["student_artifact"]["questions"][0], q2]}}
        self.assertIn("question q2 requires at least 4 response lines for explanation", validate_assessment_bundle(changed))


if __name__ == "__main__":
    unittest.main()
