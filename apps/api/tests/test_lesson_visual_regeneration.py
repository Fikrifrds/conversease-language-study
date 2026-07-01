import base64
from io import BytesIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, patch

import httpx
from PIL import Image
import yaml

from app.core.config import settings
from app.services.lesson_visual_regeneration import (
    LessonVisualRegenerationError,
    PNG_SIGNATURE,
    extract_visual_prompt,
    download_remote_image,
    image_bytes_from_response,
    image_generation_dimensions,
    import_lesson_visual_from_url,
    create_visual_thumbnail,
    get_active_lesson_visual,
    lesson_prompt_index,
    list_lesson_visual_library,
    optimize_png,
    regenerate_lesson_visual,
    select_lesson_visual_asset,
    upload_lesson_visual,
    validate_remote_image_url,
)


class FakeS3Missing(Exception):
    response = {"Error": {"Code": "NoSuchKey"}}


class FakeVisualS3:
    def __init__(self) -> None:
        self.objects = {}

    def put_object(self, *, Bucket, Key, Body, ContentType, CacheControl):
        self.objects[Key] = {
            "Body": bytes(Body),
            "ContentType": ContentType,
            "CacheControl": CacheControl,
        }

    def get_object(self, *, Bucket, Key):
        if Key not in self.objects:
            raise FakeS3Missing()
        return {"Body": BytesIO(self.objects[Key]["Body"])}


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
            self.assertEqual(
                output.with_suffix(".library-asset-id").read_text(),
                result.library_asset_id,
            )
            self.assertEqual(result.byte_count, output.stat().st_size)
            self.assertEqual(result.slug, "saying-hello-and-goodbye")
            self.assertEqual(result.slot, "hero")
            self.assertEqual(client.prompts[0][1], "hero")
            self.assertIn("Lesson: Saying Hello", client.prompts[0][0])
            self.assertIn("1024×576 pixels", client.prompts[0][0])
            self.assertNotIn("1672×941 pixels", client.prompts[0][0])

            library_entry = root / "_library" / result.library_relative_path
            self.assertTrue((library_entry / "image.png").exists())
            self.assertEqual(library_entry.name, result.library_asset_id)
            metadata = yaml.safe_load((library_entry / "metadata.yaml").read_text())
            self.assertEqual(metadata["description"]["setting"], "a bright open English classroom beside the classroom entrance.")
            self.assertEqual(
                [person["name"] for person in metadata["description"]["people"]],
                ["Dimas", "Ben"],
            )
            readme = (library_entry / "README.md").read_text()
            self.assertIn("## Tentang gambar", readme)
            self.assertIn("## Siapa saja di dalam gambar", readme)

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

    async def test_each_regeneration_is_preserved_as_a_separate_library_asset(self):
        client = FakeImageClient(self.png)
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            first = await regenerate_lesson_visual(
                slug="saying-hello-and-goodbye",
                slot="hero",
                image_client=client,
                overrides_dir=root,
            )
            second = await regenerate_lesson_visual(
                slug="saying-hello-and-goodbye",
                slot="hero",
                image_client=client,
                overrides_dir=root,
            )

            self.assertNotEqual(first.library_asset_id, second.library_asset_id)
            entries = list((root / "_library" / "saying-hello-and-goodbye" / "hero").iterdir())
            self.assertEqual(len(entries), 2)

    async def test_existing_untracked_override_is_archived_before_replacement(self):
        client = FakeImageClient(self.png)
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            existing = root / "saying-hello-and-goodbye" / "hero.png"
            existing.parent.mkdir(parents=True)
            existing.write_bytes(self.png)

            await regenerate_lesson_visual(
                slug="saying-hello-and-goodbye",
                slot="hero",
                image_client=client,
                overrides_dir=root,
            )

            entries = list((root / "_library" / "saying-hello-and-goodbye" / "hero").iterdir())
            self.assertEqual(len(entries), 2)
            reasons = {
                yaml.safe_load((entry / "metadata.yaml").read_text())["archive_reason"]
                for entry in entries
            }
            self.assertEqual(reasons, {"preserved_existing_override", "new_generation"})

    def test_manual_jpeg_upload_is_normalized_and_archived(self):
        source = BytesIO()
        Image.new("RGB", (1600, 900), (245, 158, 11)).save(source, format="JPEG")
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            result = upload_lesson_visual(
                slug="saying-hello-and-goodbye",
                slot="hero",
                image_bytes=source.getvalue(),
                overrides_dir=root,
            )

            self.assertEqual(result.model, "manual-upload")
            output = root / "saying-hello-and-goodbye" / "hero.png"
            with Image.open(output) as image:
                self.assertEqual(image.size, (1024, 576))
            metadata = yaml.safe_load(
                (root / "_library" / result.library_relative_path / "metadata.yaml").read_text()
            )
            self.assertEqual(metadata["archive_reason"], "manual_upload")

    def test_manual_upload_rejects_wrong_aspect_ratio(self):
        source = BytesIO()
        Image.new("RGB", (600, 600), (245, 158, 11)).save(source, format="PNG")
        with self.assertRaises(LessonVisualRegenerationError) as context:
            upload_lesson_visual(
                slug="saying-hello-and-goodbye",
                slot="hero",
                image_bytes=source.getvalue(),
            )
        self.assertEqual(context.exception.code, "uploaded_image_aspect_ratio_invalid")

    def test_s3_library_keeps_assets_and_active_pointer_without_local_files(self):
        source = BytesIO()
        Image.new("RGB", (1600, 900), (245, 158, 11)).save(source, format="JPEG")
        fake_s3 = FakeVisualS3()
        patches = [
            patch.object(settings, "s3_bucket", "visual-bucket"),
            patch.object(settings, "aws_access_key_id", "key"),
            patch.object(settings, "aws_secret_access_key", "secret"),
            patch.object(settings, "aws_region", "ap-southeast-1"),
            patch.object(settings, "s3_public_base_url", "https://cdn.example.com"),
            patch(
                "app.services.lesson_visual_regeneration.visual_s3_client",
                return_value=fake_s3,
            ),
        ]
        for active_patch in patches:
            active_patch.start()
            self.addCleanup(active_patch.stop)

        first = upload_lesson_visual(
            slug="saying-hello-and-goodbye",
            slot="hero",
            image_bytes=source.getvalue(),
        )
        second = upload_lesson_visual(
            slug="saying-hello-and-goodbye",
            slot="hero",
            image_bytes=source.getvalue(),
        )

        library = list_lesson_visual_library(slug="saying-hello-and-goodbye", slot="hero")
        self.assertEqual(len(library["assets"]), 2)
        self.assertEqual(library["active_asset_id"], second.library_asset_id)
        self.assertTrue(all(item["url"].startswith("s3://visual-bucket/") for item in library["assets"]))
        select_lesson_visual_asset(
            slug="saying-hello-and-goodbye",
            slot="hero",
            asset_id=first.library_asset_id,
        )
        active = get_active_lesson_visual(slug="saying-hello-and-goodbye", slot="hero")
        self.assertEqual(active["version"], first.library_asset_id)
        self.assertTrue(active["asset_url"].startswith("https://cdn.example.com/"))
        first_image_key = library["assets"][1]["storage_key"]
        first_thumbnail_key = library["assets"][1]["preview_storage_key"]
        self.assertEqual(
            fake_s3.objects[first_image_key]["CacheControl"],
            "public, max-age=31536000, immutable",
        )
        self.assertEqual(fake_s3.objects[first_thumbnail_key]["ContentType"], "image/webp")
        self.assertEqual(
            fake_s3.objects[first_thumbnail_key]["CacheControl"],
            "public, max-age=31536000, immutable",
        )

    async def test_remote_image_is_downloaded_as_bytes(self):
        transport = httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                headers={"content-type": "image/png"},
                content=self.png,
                request=request,
            )
        )
        async with httpx.AsyncClient(transport=transport) as client:
            with patch(
                "app.services.lesson_visual_regeneration.validate_remote_image_url",
                return_value="https://example.com/image.png",
            ):
                downloaded = await download_remote_image(
                    "https://example.com/image.png",
                    client=client,
                )
        self.assertEqual(downloaded, self.png)

    async def test_remote_image_reports_when_browser_session_is_required(self):
        transport = httpx.MockTransport(
            lambda request: httpx.Response(403, json={"detail": "File stream access denied."}, request=request)
        )
        async with httpx.AsyncClient(transport=transport) as client:
            with patch(
                "app.services.lesson_visual_regeneration.validate_remote_image_url",
                return_value="https://chatgpt.com/backend-api/estuary/content?sig=secret",
            ):
                with self.assertRaises(LessonVisualRegenerationError) as context:
                    await download_remote_image(
                        "https://chatgpt.com/backend-api/estuary/content?sig=secret",
                        client=client,
                    )
        self.assertEqual(context.exception.code, "remote_image_auth_required")

    async def test_url_import_stores_image_but_not_expiring_source_url(self):
        expiring_url = "https://chatgpt.com/backend-api/estuary/content?sig=secret-value"
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            with patch(
                "app.services.lesson_visual_regeneration.download_remote_image",
                new=AsyncMock(return_value=self.png),
            ):
                result = await import_lesson_visual_from_url(
                    slug="saying-hello-and-goodbye",
                    slot="hero",
                    url=expiring_url,
                    overrides_dir=root,
                )

            metadata_text = (
                root / "_library" / result.library_relative_path / "metadata.yaml"
            ).read_text()
            self.assertNotIn(expiring_url, metadata_text)
            self.assertNotIn("secret-value", metadata_text)
            self.assertIn("archive_reason: url_import", metadata_text)

    def test_remote_image_url_rejects_private_addresses(self):
        with patch(
            "app.services.lesson_visual_regeneration.socket.getaddrinfo",
            return_value=[(2, 1, 6, "", ("127.0.0.1", 443))],
        ):
            with self.assertRaises(LessonVisualRegenerationError) as context:
                validate_remote_image_url("https://example.com/image.png")
        self.assertEqual(context.exception.code, "remote_image_url_forbidden")

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

    def test_library_thumbnail_is_small_webp(self):
        image = Image.effect_noise((1024, 576), 80).convert("RGB")
        source = BytesIO()
        image.save(source, format="PNG")

        thumbnail = create_visual_thumbnail(source.getvalue())

        self.assertLess(len(thumbnail), len(source.getvalue()))
        with Image.open(BytesIO(thumbnail)) as result:
            self.assertEqual(result.format, "WEBP")
            self.assertLessEqual(result.width, 384)
            self.assertLessEqual(result.height, 384)

    async def test_base64_together_response_is_decoded(self):
        body = {"data": [{"b64_json": base64.b64encode(self.png).decode("ascii")}]}
        decoded = await image_bytes_from_response(body, client=None)
        self.assertEqual(decoded, self.png)


if __name__ == "__main__":
    unittest.main()
