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
            self.assertIn("Scene and background:", actual)
            self.assertIn("Actual conversation location:", actual)
            self.assertIn("Required background cues:", actual)
            self.assertIn("Context guardrail:", actual)

            background = self.prompts.background_spec_for(lesson_dir)
            for detail in background:
                self.assertGreaterEqual(len(detail), 25, f"Background detail too short: {lesson_dir}")
                self.assertIn(detail, actual)

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

    def test_background_catalog_explicitly_covers_every_unit_and_override(self):
        unit_keys = {
            (self.prompts.lesson_identity(lesson_dir)[1], self.prompts.lesson_identity(lesson_dir)[2])
            for lesson_dir in self.lesson_dirs
        }
        lesson_keys = {
            self.prompts.lesson_identity(lesson_dir)[1:]
            for lesson_dir in self.lesson_dirs
        }
        self.assertEqual(unit_keys, set(self.prompts.UNIT_BACKGROUND_SPECS))
        self.assertTrue(set(self.prompts.LESSON_BACKGROUND_OVERRIDES).issubset(lesson_keys))
        self.assertFalse(hasattr(self.prompts, "SETTING_RULES"))

        for lesson_dir in self.lesson_dirs:
            background = " ".join(self.prompts.background_spec_for(lesson_dir)).lower()
            self.assertNotIn("whose props clearly match", background)
            self.assertNotIn("topic-relevant", background)

            lesson = self.prompts.read_yaml(lesson_dir / "lesson.yaml")
            mode = self.prompts.communication_mode(lesson)
            location = self.prompts.background_spec_for(lesson_dir)[0].lower()
            if "separate appropriate locations" in mode:
                self.assertIn("split", location, f"Remote scene is not visually split: {lesson_dir}")
            if "split" in location:
                self.assertIn(
                    "separate appropriate locations",
                    mode,
                    f"Split background conflicts with in-person mode: {lesson_dir}",
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
        self.assertIn("No women, girls, children, or additional people", prompt)
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
        self.assertIn("No women, girls, children, or additional people", prompt)
        self.assertIn("MEN-ONLY SCENE", prompt)
        self.assertNotIn("long khimar", prompt)
        self.assertIn("hotel guest-information desk", prompt)
        self.assertIn("object-only local-food photo cards", prompt)
        self.assertIn("Do not place them inside any restaurant", prompt)
        self.assertIn("Do not draw buildings, monuments, labels, flags, or religious icons on the map", prompt)
        self.assertNotIn("where a personal story is being shared", prompt)

    def test_b1_travel_delay_is_a_split_phone_call_not_face_to_face(self):
        lesson_dir = (
            CURRICULUM_ROOT
            / "english"
            / "B1"
            / "units"
            / "unit-04-travel-situations"
            / "lesson-02-explaining-a-delay"
        )
        prompt = self.prompts.build_prompt(lesson_dir)
        self.assertIn("a split phone-call scene", prompt)
        self.assertIn("They are physically separate during the delay call", prompt)
        self.assertIn("speakers are in separate appropriate locations connected by phone", prompt)
        self.assertNotIn("The speakers are physically present in the same appropriate scene", prompt)

    def test_mixed_gender_phone_call_has_only_remote_named_speakers(self):
        lesson_dir = (
            CURRICULUM_ROOT
            / "english"
            / "A2"
            / "units"
            / "unit-05-health-and-appointments"
            / "lesson-03-making-an-appointment"
        )
        prompt = self.prompts.build_prompt(lesson_dir)
        self.assertIn("REMOTE MIXED-GENDER SCENE", prompt)
        self.assertIn("They are physically separate and are the only human figures", prompt)
        self.assertNotIn("Include exactly two additional modestly dressed adult men", prompt)
        self.assertIn("The mixed-gender speakers are never together physically", prompt)

if __name__ == "__main__":
    unittest.main()
