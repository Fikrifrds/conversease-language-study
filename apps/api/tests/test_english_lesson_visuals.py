import importlib.util
import struct
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
CURRICULUM_ROOT = REPO_ROOT / "content" / "curriculum"
ENGLISH_ROOT = CURRICULUM_ROOT / "english"
ASSET_ROOT = REPO_ROOT / "apps" / "web" / "public" / "images" / "lesson-visual-library"
GENERATOR_PATH = REPO_ROOT / "scripts" / "generate_lesson_visuals.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_lesson_visuals", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"Not a PNG asset: {path}")
    return struct.unpack(">II", header[16:24])


class EnglishLessonVisualsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()
        cls.visual_paths = sorted(ENGLISH_ROOT.glob("*/units/*/*/visuals.yaml"))

    def test_all_english_lessons_use_curated_scenes(self):
        self.assertEqual(len(self.visual_paths), 200)

        used_scenes = set()
        for visual_path in self.visual_paths:
            visual = yaml.safe_load(visual_path.read_text(encoding="utf-8"))
            lesson_dir = visual_path.parent
            parts = lesson_dir.relative_to(CURRICULUM_ROOT).parts
            _, level, _, unit_key, lesson_key = parts
            expected_scene = self.generator.ENGLISH_LESSON_SCENE_OVERRIDES.get(
                (level, unit_key, lesson_key)
            ) or self.generator.ENGLISH_UNIT_SCENES.get((level, unit_key))

            self.assertIsNotNone(expected_scene, f"Missing curated scene for {lesson_dir}")
            used_scenes.add(expected_scene)
            self.assertEqual(
                visual["hero"]["src"],
                f"/images/lesson-visual-library/{expected_scene}/hero.png",
            )
            self.assertEqual(len(visual["cards"]), 3)
            for index, card in enumerate(visual["cards"], start=1):
                self.assertEqual(
                    card["src"],
                    f"/images/lesson-visual-library/{expected_scene}/card-{index}.png",
                )

        self.assertEqual(used_scenes, set(self.generator.ENGLISH_SCENE_DESCRIPTIONS))

    def test_curated_scene_assets_exist_at_production_dimensions(self):
        for scene in self.generator.ENGLISH_SCENE_DESCRIPTIONS:
            hero = ASSET_ROOT / scene / "hero.png"
            self.assertTrue(hero.is_file(), f"Missing hero asset: {hero}")
            self.assertEqual(png_size(hero), (1672, 941))

            for index in range(1, 4):
                card = ASSET_ROOT / scene / f"card-{index}.png"
                self.assertTrue(card.is_file(), f"Missing card asset: {card}")
                self.assertEqual(png_size(card), (1254, 1254))


if __name__ == "__main__":
    unittest.main()
