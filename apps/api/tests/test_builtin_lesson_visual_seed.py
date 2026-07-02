import unittest

from scripts.seed_builtin_lesson_visuals_to_s3 import (
    course_placement_sources,
    seed,
    seed_targets,
)


class BuiltinLessonVisualSeedTest(unittest.TestCase):
    def test_every_english_lesson_has_four_assignments(self):
        targets = seed_targets()
        assignment_keys = {(item["slug"], item["slot"]) for item in targets}

        self.assertEqual(len(targets), 800)
        self.assertEqual(len(assignment_keys), 800)

    def test_dry_run_includes_every_builtin_asset(self):
        result = seed(execute=False)

        self.assertTrue(result["dry_run"])
        self.assertEqual(result["assignment_count"], 800)
        self.assertEqual(result["unique_asset_count"], 124)
        self.assertEqual(result["placement_count"], 280)
        self.assertEqual(result["failed"], [])

    def test_every_seeded_course_placement_has_a_source_lesson_slot(self):
        placements = course_placement_sources()

        self.assertEqual(len(placements), 280)
        self.assertTrue(all(item["source_lesson_slug"] for item in placements))
        self.assertTrue(
            all(item["source_slot"] in {"hero", "card-1", "card-2", "card-3"} for item in placements)
        )


if __name__ == "__main__":
    unittest.main()
