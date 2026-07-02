from datetime import datetime, timezone
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.repositories.lesson_visual_library import (
    activate_visual_asset,
    assign_visual_placement,
    get_active_visual_asset,
    list_visual_placements,
    list_visual_assets,
    register_visual_asset,
)


class LessonVisualLibraryRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine)

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def register(self, *, asset_id: str, content_hash: str, slot: str):
        return register_visual_asset(
            self.db,
            asset_id=asset_id,
            content_hash=content_hash,
            storage_key=f"lesson-visuals/assets/{asset_id}/image.png",
            preview_storage_key=f"lesson-visuals/assets/{asset_id}/thumbnail.webp",
            source_lesson_slug="source-lesson",
            source_slot=slot,
            model="builtin-static",
            archive_reason="builtin_asset_seed",
            width=1024,
            height=576 if slot == "hero" else 1024,
            byte_count=123,
            description={"subject": asset_id},
            prompt_text=None,
            created_at=datetime.now(timezone.utc),
        )

    def test_assets_are_global_and_active_selection_is_per_lesson(self):
        hero = self.register(asset_id="hero-asset", content_hash="a" * 64, slot="hero")
        card = self.register(asset_id="card-asset", content_hash="b" * 64, slot="card-2")
        activate_visual_asset(
            self.db,
            lesson_slug="target-lesson",
            slot="hero",
            asset_id=hero.id,
        )
        self.db.commit()

        self.assertEqual([item.id for item in list_visual_assets(self.db, slot="hero")], [hero.id])
        self.assertEqual(
            [item.id for item in list_visual_assets(self.db, slot="card-1")],
            [card.id],
        )
        active = get_active_visual_asset(
            self.db, lesson_slug="target-lesson", slot="hero"
        )
        self.assertEqual(active.id, hero.id)

    def test_registration_deduplicates_by_content_hash(self):
        first = self.register(asset_id="first", content_hash="c" * 64, slot="hero")
        second = self.register(asset_id="second", content_hash="c" * 64, slot="hero")

        self.assertEqual(second.id, first.id)
        self.assertEqual(len(list_visual_assets(self.db, slot="hero")), 1)

    def test_visual_placements_reuse_assets_without_copying_binary(self):
        asset = self.register(asset_id="shared", content_hash="d" * 64, slot="hero")
        assign_visual_placement(
            self.db,
            owner_type="course",
            owner_key="english-a1",
            slot="detail-hero",
            asset_id=asset.id,
            source_lesson_slug="source-lesson",
            source_slot="hero",
        )
        assign_visual_placement(
            self.db,
            owner_type="unit",
            owner_key="english-a1:unit-01",
            slot="thumbnail-1",
            asset_id=asset.id,
            source_lesson_slug="source-lesson",
            source_slot="hero",
        )
        self.db.commit()

        placements = list_visual_placements(self.db)
        self.assertEqual(len(placements), 2)
        self.assertEqual({item[1].id for item in placements}, {asset.id})

        replacement = self.register(
            asset_id="replacement", content_hash="e" * 64, slot="hero"
        )
        activate_visual_asset(
            self.db,
            lesson_slug="source-lesson",
            slot="hero",
            asset_id=replacement.id,
        )
        self.db.commit()
        self.assertEqual(
            {item[0].asset_id for item in list_visual_placements(self.db)},
            {replacement.id},
        )

    def test_pinned_placement_does_not_follow_lesson_changes(self):
        pinned = self.register(asset_id="pinned", content_hash="f" * 64, slot="hero")
        replacement = self.register(
            asset_id="next", content_hash="1" * 64, slot="hero"
        )
        assign_visual_placement(
            self.db,
            owner_type="course",
            owner_key="english-a1",
            slot="detail-hero",
            asset_id=pinned.id,
            mode="pinned",
            source_lesson_slug="source-lesson",
            source_slot="hero",
        )
        activate_visual_asset(
            self.db,
            lesson_slug="source-lesson",
            slot="hero",
            asset_id=replacement.id,
        )
        self.db.commit()

        placement, _ = list_visual_placements(self.db)[0]
        self.assertEqual(placement.asset_id, pinned.id)
        self.assertEqual(placement.mode, "pinned")

    def test_seed_style_activation_preserves_existing_lesson_choice(self):
        selected = self.register(
            asset_id="selected", content_hash="2" * 64, slot="hero"
        )
        builtin = self.register(
            asset_id="builtin", content_hash="3" * 64, slot="hero"
        )
        activate_visual_asset(
            self.db,
            lesson_slug="source-lesson",
            slot="hero",
            asset_id=selected.id,
        )
        self.db.flush()
        activate_visual_asset(
            self.db,
            lesson_slug="source-lesson",
            slot="hero",
            asset_id=builtin.id,
            only_if_missing=True,
        )
        self.db.commit()

        active = get_active_visual_asset(
            self.db, lesson_slug="source-lesson", slot="hero"
        )
        self.assertEqual(active.id, selected.id)
