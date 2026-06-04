import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db import models  # noqa: F401
from app.repositories.conversation_practice import ConversationPracticeRepository


class ConversationPracticeRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def test_persists_session_turns_and_latest_progress(self):
        with self.SessionLocal() as db:
            repository = ConversationPracticeRepository(db)
            session = repository.create_session(demo_user_id="demo-user")

            session, first_turn = repository.add_turn(
                session_id=session.id,
                transcript="Good morning. I'm good, thank you.",
            )
            session, second_turn = repository.add_turn(
                session_id=session.id,
                transcript="My name is Arif. Nice to meet you.",
            )
            session, third_turn = repository.add_turn(
                session_id=session.id,
                transcript="I'm from Indonesia. How about you?",
            )

            latest = repository.latest_session_for_user("demo-user")

            self.assertIsNotNone(latest)
            self.assertEqual(latest.id, session.id)
            self.assertTrue(latest.completed)
            self.assertEqual(latest.completed_turns, 3)
            self.assertIsNotNone(first_turn.coach_reply)
            self.assertIsNotNone(second_turn.coach_reply)
            self.assertIsNone(third_turn.coach_reply)
            self.assertGreaterEqual(latest.last_score, 70)

    def test_reset_latest_deletes_progress_and_session(self):
        with self.SessionLocal() as db:
            repository = ConversationPracticeRepository(db)
            session = repository.create_session(demo_user_id="demo-user")
            repository.add_turn(session_id=session.id, transcript="Good morning, thank you.")

            reset = repository.reset_latest_for_user("demo-user")

            self.assertTrue(reset)
            self.assertIsNone(repository.latest_session_for_user("demo-user"))
            self.assertIsNone(repository.get_session(session.id))

    def test_persists_lesson_specific_roleplay_progress(self):
        with self.SessionLocal() as db:
            repository = ConversationPracticeRepository(db)
            session = repository.create_session(
                demo_user_id="demo-user",
                lesson_slug="saying-where-you-are-from",
            )

            session, first_turn = repository.add_turn(
                session_id=session.id,
                transcript="I'm from Indonesia.",
            )
            latest = repository.latest_session_for_user(
                "demo-user",
                lesson_slug="saying-where-you-are-from",
            )

            self.assertIsNotNone(latest)
            self.assertEqual(latest.id, session.id)
            self.assertFalse(latest.completed)
            self.assertEqual(latest.completed_turns, 1)
            self.assertEqual(first_turn.coach_reply, "Where do you live now?")


if __name__ == "__main__":
    unittest.main()
