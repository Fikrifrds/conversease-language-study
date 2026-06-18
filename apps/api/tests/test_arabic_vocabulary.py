import importlib.util
import re
import unittest
from pathlib import Path

import yaml

from app.data.content_readiness import content_readiness_summary


REPO_ROOT = Path(__file__).resolve().parents[3]
ARABIC_ROOT = REPO_ROOT / "content" / "curriculum" / "arabic"
ENGLISH_ROOT = REPO_ROOT / "content" / "curriculum" / "english"
GENERATOR = REPO_ROOT / "scripts" / "generate_web_lesson_data.py"
ARABIC_TEXT_RE = re.compile(r"[\u0621-\u064A]")
ENGLISH_TEXT_RE = re.compile(r"[A-Za-z]")


def _load_web_generator():
    spec = importlib.util.spec_from_file_location("generate_web_lesson_data", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ArabicVocabularyTest(unittest.TestCase):
    def test_every_arabic_lesson_has_structured_vocabulary(self):
        lesson_dirs = sorted(path for path in ARABIC_ROOT.glob("*/units/*/lesson-*") if path.is_dir())

        self.assertGreater(len(lesson_dirs), 0)
        for lesson_dir in lesson_dirs:
            path = lesson_dir / "vocabulary.yaml"
            self.assertTrue(path.exists(), f"Missing vocabulary file: {path}")

            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            vocabulary = data.get("vocabulary")
            self.assertIsInstance(vocabulary, list, f"Vocabulary must be a list: {path}")
            self.assertGreater(len(vocabulary), 0, f"Vocabulary must not be empty: {path}")

            for item in vocabulary:
                word = str(item.get("word") or "")
                meaning = str(item.get("meaning_id") or "")
                usage = str(item.get("usage_note") or "")

                self.assertRegex(word, ARABIC_TEXT_RE, f"Vocabulary word must be Arabic: {path}")
                self.assertTrue(meaning, f"Vocabulary meaning is required: {path}")
                self.assertTrue(usage, f"Vocabulary usage note is required: {path}")
                self.assertLessEqual(
                    len(word.split()),
                    3,
                    f"Vocabulary should stay word-focused, not phrase-heavy: {path}",
                )

    def test_web_lesson_generator_includes_arabic_vocabulary(self):
        generator = _load_web_generator()
        arabic_lessons = [
            lesson
            for lesson in generator.collect_lessons()
            if lesson["language"] == "arabic"
        ]

        self.assertGreater(len(arabic_lessons), 0)
        self.assertTrue(
            all(lesson["vocabulary"] for lesson in arabic_lessons),
            "Every Arabic lesson should expose vocabulary to the web lesson page.",
        )

    def test_every_english_lesson_has_structured_vocabulary(self):
        lesson_dirs = sorted(path for path in ENGLISH_ROOT.glob("*/units/*/lesson-*") if path.is_dir())

        self.assertGreater(len(lesson_dirs), 0)
        for lesson_dir in lesson_dirs:
            path = lesson_dir / "vocabulary.yaml"
            self.assertTrue(path.exists(), f"Missing vocabulary file: {path}")

            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            vocabulary = data.get("vocabulary")
            self.assertIsInstance(vocabulary, list, f"Vocabulary must be a list: {path}")
            self.assertGreater(len(vocabulary), 0, f"Vocabulary must not be empty: {path}")

            for item in vocabulary:
                word = str(item.get("word") or "")
                meaning = str(item.get("meaning_id") or "")
                usage = str(item.get("usage_note") or "")

                self.assertRegex(word, ENGLISH_TEXT_RE, f"Vocabulary word must be English: {path}")
                self.assertTrue(meaning, f"Vocabulary meaning is required: {path}")
                self.assertTrue(usage, f"Vocabulary usage note is required: {path}")
                self.assertLessEqual(
                    len(word.split()),
                    4,
                    f"Vocabulary should stay word-focused, not phrase-heavy: {path}",
                )

    def test_web_lesson_generator_includes_english_vocabulary(self):
        generator = _load_web_generator()
        english_lessons = [
            lesson
            for lesson in generator.collect_lessons()
            if lesson["language"] == "english"
        ]

        self.assertGreater(len(english_lessons), 0)
        self.assertTrue(
            all(lesson["vocabulary"] for lesson in english_lessons),
            "Every English lesson should expose vocabulary to the web lesson page.",
        )

    def test_cms_readiness_tracks_vocabulary_for_supported_languages(self):
        arabic_readiness = content_readiness_summary(language="arabic", level_code="A1")
        english_readiness = content_readiness_summary(language="english", level_code="A1")

        self.assertIn(
            "vocabulary",
            {item["key"] for item in arabic_readiness["required_items"]},
        )
        self.assertIn(
            "vocabulary",
            {item["key"] for item in english_readiness["required_items"]},
        )
        self.assertEqual(arabic_readiness["summary"]["missing_content_count"], 0)
        self.assertEqual(english_readiness["summary"]["missing_content_count"], 0)


if __name__ == "__main__":
    unittest.main()
