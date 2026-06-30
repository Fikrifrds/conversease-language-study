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
            self.assertIn("FACELESS MEANS COMPLETELY BLANK FACES", actual)
            self.assertIn("no eyes, pupils, eyelids, eyebrows, eyelashes", actual)
            self.assertIn("the total human count is exact", actual)

            dialogue = self.prompts.dialogue_turns(lesson_dir / "listening_script.md")
            speakers = self.prompts.unique_speakers(dialogue)
            voices = self.prompts.speaker_voices(lesson_dir / "audio_manifest.yaml")
            genders = [self.prompts.gender_for_voice(voices[speaker]) for speaker in speakers]
            if "male" in genders:
                self.assertIn("trousers whose hems clearly end above the ankle bones", actual)
            if "female" in genders:
                self.assertIn("long khimar fully covering the chest", actual)

            for speaker in speakers:
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
        self.assertIn("show exactly 2 adult men total in the entire image", prompt)
        self.assertIn("Dimas, Ben. They are the only human figures allowed anywhere", prompt)
        self.assertIn("No women, girls, children", prompt)
        self.assertIn("MEN-ONLY SCENE", prompt)
        self.assertNotIn("long khimar", prompt)
        self.assertIn("a bright open English classroom", prompt)
        self.assertNotIn("show exactly 2 adult women", prompt)

    def test_b1_travel_recommendation_uses_exactly_two_faceless_men(self):
        lesson_dir = (
            CURRICULUM_ROOT
            / "english"
            / "B1"
            / "units"
            / "unit-04-travel-situations"
            / "lesson-03-asking-for-recommendations"
        )
        prompt = self.prompts.build_prompt(lesson_dir)
        self.assertIn("Dialogue speakers: **Faris, Ilham**", prompt)
        self.assertIn("show exactly 2 adult men total in the entire image", prompt)
        self.assertIn("Faris, Ilham. They are the only human figures allowed anywhere", prompt)
        self.assertIn("No women, girls, children", prompt)
        self.assertIn("MEN-ONLY SCENE", prompt)
        self.assertNotIn("long khimar", prompt)
        self.assertIn("with local dining photo cards", prompt)
        self.assertNotIn("where a personal story is being shared", prompt)

if __name__ == "__main__":
    unittest.main()
