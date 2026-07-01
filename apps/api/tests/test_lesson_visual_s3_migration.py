from pathlib import Path
import tempfile
import unittest

from scripts.migrate_lesson_visuals_to_s3 import migration_targets


class LessonVisualS3MigrationTest(unittest.TestCase):
    def test_library_assets_are_ordered_before_active_override(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            archived = root / "_library" / "saying-hello-and-goodbye" / "hero" / "old-asset"
            archived.mkdir(parents=True)
            (archived / "image.png").write_bytes(b"archived")
            active = root / "saying-hello-and-goodbye"
            active.mkdir(parents=True)
            (active / "hero.png").write_bytes(b"active")

            targets = migration_targets(root)

        self.assertEqual(len(targets), 2)
        self.assertFalse(targets[0]["active"])
        self.assertTrue(targets[1]["active"])
        self.assertEqual(targets[1]["slug"], "saying-hello-and-goodbye")


if __name__ == "__main__":
    unittest.main()
