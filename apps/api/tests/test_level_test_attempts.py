import unittest

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.models import LevelTestAttemptModel
from app.repositories.level_test_attempts import (
    InvalidLevelTestAttemptStateError,
    LevelTestAttemptRepository,
)


class LevelTestAttemptRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def test_create_and_submit_attempt_persists_report(self):
        with self.SessionLocal() as db:
            repository = LevelTestAttemptRepository(db)

            attempt = repository.create_attempt(user_id="user-123", level_code="A1")
            initial_status = attempt.status
            submitted = repository.submit_attempt(
                user_id="user-123",
                attempt_id=attempt.id,
                lesson_completion_percent=85,
                scores={
                    "listening": 70,
                    "speaking_conversation": 70,
                    "pronunciation_fluency": 70,
                    "useful_phrases": 70,
                    "grammar": 70,
                    "reading": 70,
                    "writing": 70,
                },
                responses={"note": "beta self-check"},
            )

            stored = db.execute(select(LevelTestAttemptModel)).scalar_one()

            self.assertEqual(initial_status, "in_progress")
            self.assertEqual(submitted.status, "submitted")
            self.assertEqual(stored.overall_score, 70)
            self.assertTrue(stored.passed)
            self.assertEqual(stored.evaluation_snapshot_json["level_code"], "A1")
            self.assertEqual(stored.responses_json["note"], "beta self-check")

    def test_create_attempt_reuses_existing_in_progress_attempt(self):
        with self.SessionLocal() as db:
            repository = LevelTestAttemptRepository(db)

            first_attempt = repository.create_attempt(user_id="user-123", level_code="A1")
            second_attempt = repository.create_attempt(user_id="user-123", level_code="A1")

            self.assertEqual(first_attempt.id, second_attempt.id)

    def test_language_scoped_attempts_do_not_collide(self):
        with self.SessionLocal() as db:
            repository = LevelTestAttemptRepository(db)

            english_attempt = repository.create_attempt(user_id="user-123", level_code="A1")
            arabic_attempt = repository.create_attempt(user_id="user-123", level_code="AR-A1")

            self.assertNotEqual(english_attempt.id, arabic_attempt.id)
            self.assertEqual(english_attempt.level_code, "A1")
            self.assertEqual(arabic_attempt.level_code, "AR-A1")
            self.assertEqual(arabic_attempt.evaluation_snapshot_json["language"], "arabic")

    def test_can_save_draft_for_higher_level_attempt(self):
        with self.SessionLocal() as db:
            repository = LevelTestAttemptRepository(db)

            attempt = repository.create_attempt(user_id="user-123", level_code="A2")
            updated = repository.save_draft_attempt(
                user_id="user-123",
                attempt_id=attempt.id,
                lesson_completion_percent=82,
                scores={
                    "listening": 70,
                    "speaking_conversation": 72,
                    "pronunciation_fluency": 68,
                    "useful_phrases": 71,
                    "grammar": 69,
                    "reading": 70,
                    "writing": 67,
                },
                responses={
                    "listening": {"answer": "The speakers are planning to meet on Saturday."},
                    "writing": {"answer": "Hi, I can join on Saturday because I am free then."},
                },
            )

            self.assertEqual(updated.level_code, "A2")
            self.assertEqual(updated.status, "in_progress")
            self.assertEqual(updated.lesson_completion_percent, 82)
            self.assertEqual(updated.responses_json["writing"]["answer"], "Hi, I can join on Saturday because I am free then.")
            self.assertIsNotNone(updated.overall_score)

    def test_submitted_attempt_cannot_be_submitted_twice(self):
        with self.SessionLocal() as db:
            repository = LevelTestAttemptRepository(db)
            attempt = repository.create_attempt(user_id="user-123", level_code="A1")
            scores = {
                "listening": 70,
                "speaking_conversation": 70,
                "pronunciation_fluency": 70,
                "useful_phrases": 70,
                "grammar": 70,
                "reading": 70,
                "writing": 70,
            }

            repository.submit_attempt(
                user_id="user-123",
                attempt_id=attempt.id,
                lesson_completion_percent=85,
                scores=scores,
            )

            with self.assertRaises(InvalidLevelTestAttemptStateError):
                repository.submit_attempt(
                    user_id="user-123",
                    attempt_id=attempt.id,
                    lesson_completion_percent=85,
                    scores=scores,
                )

    def test_admin_can_review_submitted_attempt(self):
        with self.SessionLocal() as db:
            repository = LevelTestAttemptRepository(db)
            attempt = repository.create_attempt(user_id="user-123", level_code="A1")
            repository.submit_attempt(
                user_id="user-123",
                attempt_id=attempt.id,
                lesson_completion_percent=85,
                scores={
                    "listening": 70,
                    "speaking_conversation": 70,
                    "pronunciation_fluency": 70,
                    "useful_phrases": 70,
                    "grammar": 70,
                    "reading": 70,
                    "writing": 70,
                },
            )

            reviewed = repository.admin_score_attempt(
                attempt_id=attempt.id,
                reviewed_by="Admin QA",
                lesson_completion_percent=90,
                scores={
                    "listening": 80,
                    "speaking_conversation": 80,
                    "pronunciation_fluency": 75,
                    "useful_phrases": 80,
                    "grammar": 80,
                    "reading": 75,
                    "writing": 75,
                },
                notes="Manual beta review",
            )

            self.assertEqual(reviewed.status, "reviewed")
            self.assertEqual(reviewed.reviewed_by, "Admin QA")
            self.assertEqual(reviewed.admin_notes, "Manual beta review")
            self.assertEqual(reviewed.lesson_completion_percent, 90)
            self.assertTrue(reviewed.passed)

    def test_admin_cannot_review_in_progress_attempt(self):
        with self.SessionLocal() as db:
            repository = LevelTestAttemptRepository(db)
            attempt = repository.create_attempt(user_id="user-123", level_code="A1")

            with self.assertRaises(InvalidLevelTestAttemptStateError):
                repository.admin_score_attempt(
                    attempt_id=attempt.id,
                    reviewed_by="Admin QA",
                    scores={
                        "listening": 80,
                        "speaking_conversation": 80,
                        "pronunciation_fluency": 75,
                        "useful_phrases": 80,
                        "grammar": 80,
                        "reading": 75,
                        "writing": 75,
                    },
                )


if __name__ == "__main__":
    unittest.main()
