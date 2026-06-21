import unittest

from app.data.curriculum import (
    A1_COURSE,
    get_lesson_or_none,
    load_a1_final_evaluation,
    public_course_payload,
    published_lessons,
    validate_curriculum_content,
    validate_production_tracker,
)


class CurriculumContentTest(unittest.TestCase):
    def test_a1_course_is_loaded_from_content_files(self):
        self.assertEqual(A1_COURSE["course_slug"], "english-a1-start-simple-conversations")
        self.assertEqual(A1_COURSE["level_code"], "A1")
        self.assertEqual(len(A1_COURSE["units"]), 8)
        self.assertEqual(len(published_lessons("A1")), 40)
        self.assertEqual(len(published_lessons()), 200)

    def test_lesson_detail_includes_roleplay_config_from_yaml(self):
        lesson = get_lesson_or_none("saying-your-name")

        self.assertIsNotNone(lesson)
        self.assertEqual(lesson["roleplay"]["scenario_key"], "saying_your_name_class")
        self.assertEqual(
            lesson["roleplay"]["opening_line"],
            "Hi, my name is Omar. What is your name?",
        )
        self.assertIn("Conversation Coach Roleplay", lesson["sections"])

    def test_curriculum_files_are_complete_for_published_a1_lessons(self):
        self.assertEqual(validate_curriculum_content(), [])

    def test_production_tracker_matches_published_lessons(self):
        self.assertEqual(validate_production_tracker(), [])

    def test_a1_final_evaluation_is_release_ready(self):
        evaluation = load_a1_final_evaluation()
        weight_total = sum(section["weight"] for section in evaluation["sections"])

        self.assertEqual(evaluation["status"], "published")
        self.assertEqual(evaluation["overall_threshold"], 70)
        self.assertEqual(evaluation["lesson_completion_required_percent"], 80)
        self.assertEqual(weight_total, 100)
        self.assertEqual(
            {section["key"] for section in evaluation["sections"]},
            {
                "listening",
                "speaking_conversation",
                "pronunciation_fluency",
                "useful_phrases",
                "grammar",
                "reading",
                "writing",
            },
        )
        for section in evaluation["sections"]:
            self.assertTrue(section["task"]["prompt"])
            self.assertTrue(section["task"]["success_criteria"])

    def test_public_course_payload_does_not_expose_local_file_paths(self):
        payload = public_course_payload()
        first_lesson = payload["units"][0]["lessons"][0]

        self.assertNotIn("content_files", first_lesson)


if __name__ == "__main__":
    unittest.main()
