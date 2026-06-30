import base64
from io import BytesIO
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from app.services.lesson_visual_regeneration import (
    LessonVisualRegenerationError,
    PNG_SIGNATURE,
    extract_visual_prompt,
    image_bytes_from_response,
    image_generation_dimensions,
    lesson_prompt_index,
    optimize_png,
    regenerate_lesson_visual,
)


class FakeImageClient:
    def __init__(self, image_bytes: bytes) -> None:
        self.image_bytes = image_bytes
        self.prompts = []

    async def generate_png(self, *, prompt: str, slot: str) -> bytes:
        self.prompts.append((prompt, slot))
        return self.image_bytes


class LessonVisualRegenerationTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        lesson_prompt_index.cache_clear()
        image = Image.new("RGB", (32, 18), (36, 99, 235))
        output = BytesIO()
        image.save(output, format="PNG")
        self.png = output.getvalue()

    async def test_regenerates_hero_from_lesson_prompt_into_unique_override(self):
        client = FakeImageClient(self.png)
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            result = await regenerate_lesson_visual(
                slug="saying-hello-and-goodbye",
                slot="hero",
                image_client=client,
                overrides_dir=root,
            )
            output = root / "saying-hello-and-goodbye" / "hero.png"

            self.assertTrue(output.read_bytes().startswith(PNG_SIGNATURE))
            self.assertEqual(result.byte_count, output.stat().st_size)
            self.assertEqual(result.slug, "saying-hello-and-goodbye")
            self.assertEqual(result.slot, "hero")
            self.assertEqual(client.prompts[0][1], "hero")
            self.assertIn("Lesson: Saying Hello", client.prompts[0][0])

    async def test_regenerates_only_requested_card(self):
        client = FakeImageClient(self.png)
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            await regenerate_lesson_visual(
                slug="saying-hello-and-goodbye",
                slot="card-2",
                image_client=client,
                overrides_dir=root,
            )

            self.assertTrue((root / "saying-hello-and-goodbye" / "card-2.png").exists())
            self.assertFalse((root / "saying-hello-and-goodbye" / "hero.png").exists())
            self.assertIn("card 2", client.prompts[0][0].lower())

    async def test_invalid_slot_is_rejected_before_generation(self):
        client = FakeImageClient(self.png)
        with self.assertRaises(LessonVisualRegenerationError) as context:
            await regenerate_lesson_visual(
                slug="saying-hello-and-goodbye",
                slot="card-4",
                image_client=client,
            )
        self.assertEqual(context.exception.code, "invalid_visual_slot")
        self.assertEqual(client.prompts, [])

    def test_all_actual_prompt_sections_are_extractable(self):
        prompt_index = lesson_prompt_index()
        self.assertEqual(len(prompt_index), 200)
        for prompt_path in prompt_index.values():
            for slot in ("hero", "card-1", "card-2", "card-3"):
                prompt = extract_visual_prompt(prompt_path, slot)
                self.assertGreater(len(prompt), 100)

    def test_dimensions_preserve_required_shapes(self):
        hero_width, hero_height = image_generation_dimensions("hero")
        card_width, card_height = image_generation_dimensions("card-1")
        self.assertEqual((hero_width, hero_height), (1024, 576))
        self.assertEqual((card_width, card_height), (1024, 1024))
        self.assertAlmostEqual(hero_width / hero_height, 16 / 9, places=2)
        self.assertEqual(card_width, card_height)
        self.assertEqual(hero_width % 16, 0)
        self.assertEqual(hero_height % 16, 0)

    def test_png_optimization_reduces_size_without_resizing(self):
        image = Image.effect_noise((640, 360), 80).convert("RGB")
        source = BytesIO()
        image.save(source, format="PNG")

        optimized = optimize_png(source.getvalue())

        self.assertLess(len(optimized), len(source.getvalue()))
        with Image.open(BytesIO(optimized)) as result:
            self.assertEqual(result.size, (640, 360))

    async def test_base64_together_response_is_decoded(self):
        body = {"data": [{"b64_json": base64.b64encode(self.png).decode("ascii")}]}
        decoded = await image_bytes_from_response(body, client=None)
        self.assertEqual(decoded, self.png)


if __name__ == "__main__":
    unittest.main()
