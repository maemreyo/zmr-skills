import unittest

from scripts.route_advisor import advise_route


class RouteAdvisorTests(unittest.TestCase):
    def test_bulk_reusable_count_routes_to_item_bank(self) -> None:
        self.assertEqual(advise_route("Create a reusable bank of 300 English questions"), "item_bank")

    def test_large_exam_routes_to_composer_not_item_bank(self) -> None:
        self.assertEqual(advise_route("Create a 100-question end-of-term exam with Form A and B"), "assessment_composition")

    def test_ielts_and_video_have_profile_routes(self) -> None:
        self.assertEqual(advise_route("Build an IELTS Academic Reading mock"), "ielts_practice")
        self.assertEqual(advise_route("Use this YouTube link and transcript for questions"), "video_learning")

    def test_small_ungraded_worksheet_stays_practice(self) -> None:
        self.assertEqual(advise_route("Make a 20-question ungraded worksheet"), "practice")

    def test_learner_discovery_routes_to_understand_learners(self) -> None:
        self.assertEqual(
            advise_route("Create a StudentCard from student voice and teacher observations"),
            "understand_learners",
        )

    def test_progress_request_routes_to_monitor_learning(self) -> None:
        self.assertEqual(
            advise_route("Show this learner's objective progress over the last six weeks"),
            "monitor_learning",
        )

    def test_confirmed_gap_routes_to_reteaching(self) -> None:
        self.assertEqual(
            advise_route("They still don't understand since and for; plan corrective reteaching"),
            "reteach",
        )

    def test_term_plan_routes_to_sequence_design(self) -> None:
        self.assertEqual(
            advise_route("Design a 16-week spiral curriculum with spaced review"),
            "sequence_design",
        )


if __name__ == "__main__":
    unittest.main()
