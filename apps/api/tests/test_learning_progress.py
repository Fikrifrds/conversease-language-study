import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import models  # noqa: F401
from app.db.base import Base
from app.repositories.learning_progress import LearningProgressRepository


class LearningProgressRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def test_saves_onboarding_profile_and_summary(self):
        with self.SessionLocal() as db:
            repository = LearningProgressRepository(db)

            profile = repository.save_onboarding(
                user_id="user-123",
                primary_goal="Daily conversation",
                confidence_level="Saya malu bicara",
                daily_target_minutes=15,
            )
            summary = repository.summary("user-123")

            self.assertTrue(profile.completed)
            self.assertEqual(profile.daily_target_minutes, 15)
            self.assertEqual(summary["onboarding"].primary_goal, "Daily conversation")
            self.assertEqual(summary["course"]["completion_percent"], 0)
            self.assertEqual(summary["current_mission"]["slug"], "saying-hello-and-goodbye")

    def test_tracks_lesson_start_and_completion(self):
        with self.SessionLocal() as db:
            repository = LearningProgressRepository(db)

            started = repository.start_lesson("user-123", "saying-hello-and-goodbye")
            started_status = started.status
            completed = repository.complete_lesson("user-123", "saying-hello-and-goodbye")
            summary = repository.summary("user-123")

            self.assertEqual(started_status, "in_progress")
            self.assertEqual(completed.status, "completed")
            self.assertIsNotNone(completed.completed_at)
            self.assertEqual(summary["course"]["completed_lessons"], 1)
            # A1 has 40 published lessons, so 1 completed => 2% (round(1/40*100)).
            self.assertEqual(summary["course"]["completion_percent"], 2)
            self.assertEqual(summary["course"]["total_lessons"], 40)
            self.assertEqual(summary["lessons"][0]["progress_status"], "completed")

    def test_unknown_lesson_raises_key_error(self):
        with self.SessionLocal() as db:
            repository = LearningProgressRepository(db)

            with self.assertRaises(KeyError):
                repository.start_lesson("user-123", "missing-lesson")


if __name__ == "__main__":
    unittest.main()
