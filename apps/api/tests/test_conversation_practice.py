import unittest

from app.domain.conversation_practice import (
    ConversationPracticeStore,
    evaluate_answer,
    session_payload,
    session_summary,
)


class ConversationPracticeTest(unittest.TestCase):
    def test_feedback_rewards_relevant_greeting(self):
        feedback = evaluate_answer("Good morning. I'm good, thank you.", turn_index=0)

        self.assertEqual(feedback.better_version, "Good morning. I'm good, thank you. How are you?")
        self.assertGreaterEqual(feedback.scores["speaking"], 80)
        self.assertIn("pertanyaan balik", feedback.indonesian_explanation)

    def test_session_completes_after_three_turns(self):
        store = ConversationPracticeStore()
        session = store.create_session(demo_user_id="demo-user")

        store.add_turn(session.id, "Good morning. I'm good, thank you.")
        store.add_turn(session.id, "My name is Fikri. Nice to meet you.")
        store.add_turn(session.id, "I'm from Indonesia. How about you?")

        summary = session_summary(session)

        self.assertTrue(summary["completed"])
        self.assertEqual(summary["completed_turns"], 3)
        self.assertEqual(summary["total_turns"], 3)
        self.assertGreaterEqual(summary["last_score"], 70)

    def test_session_uses_lesson_specific_roleplay_script(self):
        store = ConversationPracticeStore()
        session = store.create_session(
            demo_user_id="demo-user",
            lesson_slug="saying-your-name",
        )

        payload = session_payload(session)
        turn = store.add_turn(session.id, "My name is Fikri. Nice to meet you.")

        self.assertEqual(payload["first_coach_message"], "Hi, my name is Sara. What is your name?")
        self.assertEqual(turn.coach_reply, "Nice to meet you. What should I call you?")
        self.assertEqual(turn.feedback.better_version, "My name is Fikri. Nice to meet you.")

    def test_latest_session_is_scoped_by_demo_user(self):
        store = ConversationPracticeStore()
        user_session = store.create_session(demo_user_id="demo-user")
        other_session = store.create_session(demo_user_id="other-user")

        store.add_turn(user_session.id, "Good morning. I'm good, thank you.")
        store.add_turn(other_session.id, "Good morning. I'm good, thank you.")

        latest = store.latest_session_for_user("demo-user")

        self.assertIsNotNone(latest)
        self.assertEqual(latest.id, user_session.id)


if __name__ == "__main__":
    unittest.main()
