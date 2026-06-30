import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CURRICULUM_ROOT = REPO_ROOT / "content" / "curriculum"
PROMPT_ROOT = (
    REPO_ROOT
    / "content"
    / "visual-prompts"
    / "english"
)


def load_script(name: str):
    path = REPO_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EnglishVisualPromptsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompts = load_script("generate_english_visual_prompts")
        cls.lesson_dirs = cls.prompts.lesson_dirs()

    def test_every_english_lesson_has_current_prompt_pack(self):
        self.assertEqual(len(self.lesson_dirs), 200)
        prompt_paths = sorted(PROMPT_ROOT.glob("*/unit-*/*/PROMPT.md"))
        self.assertEqual(len(prompt_paths), 200)

        for lesson_dir in self.lesson_dirs:
            prompt_path = self.prompts.output_dir(lesson_dir) / "PROMPT.md"
            actual = prompt_path.read_text(encoding="utf-8")
            self.assertEqual(actual, self.prompts.build_prompt(lesson_dir))
            self.assertIn("## Hero prompt", actual)
            self.assertEqual(actual.count("## Card "), 3)
            self.assertIn("hero.png` | 1672×941", actual)
            self.assertIn("card-3.png` | 1254×1254", actual)
            self.assertIn("trousers whose hems clearly end above the ankle bones", actual)

            dialogue = self.prompts.dialogue_turns(lesson_dir / "listening_script.md")
            for speaker in self.prompts.unique_speakers(dialogue):
                self.assertIn(speaker, actual)

            lesson = self.prompts.read_yaml(lesson_dir / "lesson.yaml")
            unit = self.prompts.read_yaml(lesson_dir.parent / "unit.yaml")
            self.assertNotIn(
                "whose props clearly match",
                self.prompts.setting_for(lesson, unit),
                f"Generic setting remains for {lesson_dir}",
            )

    def test_a1_unit_1_lesson_1_uses_two_men_in_a_classroom(self):
        lesson_dir = (
            CURRICULUM_ROOT
            / "english"
            / "A1"
            / "units"
            / "unit-01-greeting-introducing-yourself"
            / "lesson-01-saying-hello"
        )
        prompt = self.prompts.build_prompt(lesson_dir)
        self.assertIn("Dialogue speakers: **Dimas, Ben**", prompt)
        self.assertIn("Show exactly 2 adult men in the foreground", prompt)
        self.assertIn("a bright open English classroom", prompt)
        self.assertNotIn("Show exactly 2 adult women", prompt)

if __name__ == "__main__":
    unittest.main()
