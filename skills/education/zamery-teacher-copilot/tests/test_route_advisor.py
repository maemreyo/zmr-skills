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


if __name__ == "__main__":
    unittest.main()
