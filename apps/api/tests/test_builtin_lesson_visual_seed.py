import unittest

from scripts.seed_builtin_lesson_visuals_to_s3 import seed, seed_targets


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


if __name__ == "__main__":
    unittest.main()
