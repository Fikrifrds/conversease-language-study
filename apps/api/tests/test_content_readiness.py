import hashlib
import tempfile
import unittest
from pathlib import Path

from app.data.content_readiness import (
    all_content_readiness_summary,
    audio_manifest_ready,
    content_readiness_summary,
)


class ContentReadinessTest(unittest.TestCase):
    def test_a1_plan_tracks_implemented_and_missing_lessons(self):
        readiness = content_readiness_summary()

        # English A1 is fully generated.
        self.assertEqual(readiness["summary"]["planned_lesson_count"], 40)
        self.assertEqual(readiness["summary"]["implemented_lesson_count"], 40)
        self.assertEqual(readiness["summary"]["text_ready_count"], 40)
        self.assertEqual(readiness["summary"]["audio_ready_count"], 40)
        self.assertEqual(readiness["summary"]["beta_ready_count"], 40)
        self.assertEqual(readiness["summary"]["production_ready_count"], 40)

    def test_first_unit_is_text_ready_with_audio(self):
        readiness = content_readiness_summary()
        first_unit = readiness["units"][0]
        first_lesson = first_unit["lessons"][0]

        self.assertEqual(first_unit["unit_key"], "unit-01-greeting-introducing-yourself")
        self.assertTrue(first_lesson["implemented"])
        self.assertTrue(first_lesson["text_ready"])
        self.assertTrue(first_lesson["audio_ready"])
        self.assertEqual(first_lesson["status"], "production_ready")

    def test_a1_is_text_complete_and_mostly_audio_ready(self):
        readiness = content_readiness_summary()

        self.assertEqual(readiness["summary"]["missing_content_count"], 0)
        self.assertEqual(readiness["summary"]["missing_audio_count"], 0)
        self.assertTrue(
            all(
                lesson["implemented"] and lesson["text_ready"]
                for unit in readiness["units"]
                for lesson in unit["lessons"]
            )
        )
        self.assertTrue(
            all(
                lesson["status"] in {"production_ready", "beta_ready_needs_audio"}
                for unit in readiness["units"]
                for lesson in unit["lessons"]
            )
        )

    def test_all_supported_english_levels_are_tracked(self):
        readiness = all_content_readiness_summary(language="english")

        self.assertEqual(readiness["level_count"], 5)
        self.assertEqual(
            [level["course"]["level_code"] for level in readiness["levels"]],
            ["A1", "A2", "B1", "B2", "C1"],
        )
        self.assertEqual(readiness["summary"]["planned_lesson_count"], 200)
        self.assertEqual(readiness["summary"]["implemented_lesson_count"], 200)
        self.assertEqual(readiness["summary"]["text_ready_count"], 200)
        self.assertEqual(readiness["summary"]["audio_ready_count"], 200)
        self.assertEqual(readiness["summary"]["missing_content_count"], 0)
        self.assertEqual(readiness["summary"]["missing_audio_count"], 0)

    def test_audio_manifest_ready_requires_dialogue_main_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "audio_manifest.yaml"
            manifest.write_text(
                "lesson_key: sample\n"
                "status: generated\n"
                "assets:\n"
                "  - key: dialogue_main\n"
                "    type: dialogue\n"
                "    audio_url: https://cdn.example.com/dialogue.wav\n"
                "    duration_seconds: 12\n"
                "  - key: phrases\n"
                "    type: phrase_pronunciation\n"
                "    audio_url:\n"
                "    duration_seconds:\n",
                encoding="utf-8",
            )

            self.assertTrue(audio_manifest_ready(manifest))

    def test_audio_manifest_ready_rejects_stale_script_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "listening_script.md"
            script.write_text("old script", encoding="utf-8")
            original_hash = hashlib.sha256(script.read_bytes()).hexdigest()
            script.write_text("new script", encoding="utf-8")

            manifest = Path(directory) / "audio_manifest.yaml"
            manifest.write_text(
                "lesson_key: sample\n"
                "status: generated\n"
                "assets:\n"
                "  - key: dialogue_main\n"
                "    type: dialogue\n"
                "    script_file: listening_script.md\n"
                "    script_content_hash: " + original_hash + "\n"
                "    audio_url: https://cdn.example.com/dialogue.wav\n"
                "    duration_seconds: 12\n",
                encoding="utf-8",
            )

            self.assertFalse(audio_manifest_ready(manifest))

    def test_audio_manifest_not_ready_when_tracker_would_be_done_but_manifest_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "audio_manifest.yaml"
            manifest.write_text(
                "lesson_key: sample\n"
                "status: generated\n"
                "assets:\n"
                "  - key: dialogue_main\n"
                "    type: dialogue\n"
                "    audio_url:\n"
                "    duration_seconds:\n",
                encoding="utf-8",
            )

            self.assertFalse(audio_manifest_ready(manifest))


if __name__ == "__main__":
    unittest.main()
