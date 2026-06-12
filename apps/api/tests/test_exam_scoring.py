import unittest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import create_access_token
from app.db import models
from app.db import exam_models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.services.exam_service import ExamService, ExamServiceError


def build_session_local():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def add_user(db, user_id: str, role: str = "student") -> None:
    now = datetime.utcnow()
    db.add(
        models.UserModel(
            id=user_id,
            name=f"User {user_id}",
            email=f"{user_id}@example.local",
            password_hash="hashed",
            email_verified_at=now,
            role=role,
            created_at=now,
            updated_at=now,
        )
    )
    db.commit()


def seed_exam(service: ExamService) -> dict:
    template = service.create_exam_template(
        code="TEST-A1",
        level_code="A1",
        title="Test A1 Exam",
        description=None,
        duration_minutes=45,
        passing_score_percent=60,
        created_by="tests",
    )
    template.status = "active"
    service.db.commit()

    listening = service.create_exam_section(
        exam_template_id=template.id,
        code="LISTENING",
        title="Listening",
        description=None,
        sequence_order=1,
        duration_minutes=10,
        score_weight_percent=50,
        item_types_allowed=["mcq", "fill_blank", "matching"],
    )
    speaking = service.create_exam_section(
        exam_template_id=template.id,
        code="SPEAKING",
        title="Speaking",
        description=None,
        sequence_order=2,
        duration_minutes=5,
        score_weight_percent=50,
        item_types_allowed=["audio_response"],
    )

    mcq = service.create_exam_item(
        exam_template_id=template.id,
        section_id=listening.id,
        item_type="mcq",
        sequence_order=1,
        prompt_text="Pick B",
        score_points=1,
        options_json=[{"id": "A", "text": "a"}, {"id": "B", "text": "b"}],
        correct_answer={"option_id": "B"},
    )
    fill = service.create_exam_item(
        exam_template_id=template.id,
        section_id=listening.id,
        item_type="fill_blank",
        sequence_order=2,
        prompt_text="Fill blanks",
        score_points=2,
        correct_answer={
            "blanks": ["Monday", "nurse"],
            "acceptable_variants": {"1": ["a nurse"]},
        },
    )
    matching = service.create_exam_item(
        exam_template_id=template.id,
        section_id=listening.id,
        item_type="matching",
        sequence_order=3,
        prompt_text="Match",
        score_points=3,
        options_json={
            "left_items": [{"id": "1", "text": "Big"}, {"id": "2", "text": "Fast"}, {"id": "3", "text": "Happy"}],
            "right_items": [{"id": "A", "text": "Not small"}, {"id": "B", "text": "Not slow"}, {"id": "C", "text": "Not sad"}],
        },
        correct_answer={"pairs": {"1": "A", "2": "B", "3": "C"}},
    )
    audio = service.create_exam_item(
        exam_template_id=template.id,
        section_id=speaking.id,
        item_type="audio_response",
        sequence_order=1,
        prompt_text="Read aloud",
        score_points=10,
        rubric_criteria={"pronunciation": {"weight": 1.0, "criteria": "clear"}},
    )

    return {
        "template": template,
        "listening": listening,
        "speaking": speaking,
        "mcq": mcq,
        "fill": fill,
        "matching": matching,
        "audio": audio,
    }


def run_exam_to_submission(service: ExamService, exam: dict, user_id: str):
    session = service.create_exam_session(
        exam_template_id=exam["template"].id,
        user_id=user_id,
    )
    service.start_exam(session.id)
    service.save_item_response(
        session_id=session.id,
        item_id=exam["mcq"].id,
        section_id=exam["listening"].id,
        response_type="mcq",
        selected_option_ids=["B"],
    )
    service.save_item_response(
        session_id=session.id,
        item_id=exam["fill"].id,
        section_id=exam["listening"].id,
        response_type="fill_blank",
        text_response="monday\nA Nurse",
    )
    service.save_item_response(
        session_id=session.id,
        item_id=exam["matching"].id,
        section_id=exam["listening"].id,
        response_type="matching",
        matched_pairs={"1": "A", "2": "B", "3": "A"},
    )
    service.save_item_response(
        session_id=session.id,
        item_id=exam["audio"].id,
        section_id=exam["speaking"].id,
        response_type="audio_response",
        file_url="https://example.com/answer.webm",
        audio_duration_seconds=22.0,
    )
    service.submit_exam(session.id)
    return session


class ExamObjectiveGradingTest(unittest.TestCase):
    def setUp(self):
        self.session_local = build_session_local()
        self.db = self.session_local()
        add_user(self.db, "user-1")
        self.service = ExamService(self.db)
        self.exam = seed_exam(self.service)

    def tearDown(self):
        self.db.close()

    def test_finalize_grades_objective_items_and_queues_speaking(self):
        session = run_exam_to_submission(self.service, self.exam, "user-1")
        result = self.service.finalize_submission(session.id)

        responses = {
            r.item_id: r for r in self.service.get_session_responses(session.id)
        }
        self.assertEqual(responses[self.exam["mcq"].id].score_points_earned, 1)
        self.assertTrue(responses[self.exam["mcq"].id].is_correct)
        # Casefolded blank plus acceptable variant both count
        self.assertEqual(responses[self.exam["fill"].id].score_points_earned, 2)
        self.assertTrue(responses[self.exam["fill"].id].is_correct)
        # 2 of 3 pairs correct -> 2 of 3 points
        self.assertEqual(responses[self.exam["matching"].id].score_points_earned, 2)
        self.assertFalse(responses[self.exam["matching"].id].is_correct)

        # Speaking answer is queued, result held for review
        queue = self.service.list_review_queue()
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0].item_type, "audio_response")
        self.assertEqual(result.status, "pending_review")
        self.assertIsNone(result.published_at)
        self.assertEqual(result.metadata_json["pending_review_count"], 1)

        # Listening: 5/6 raw points. Speaking still 0 until reviewed.
        listening = result.section_scores_json["LISTENING"]
        self.assertEqual(listening["score"], 5)
        self.assertEqual(listening["max"], 6)

    def test_review_score_publishes_result_with_weighted_percent(self):
        session = run_exam_to_submission(self.service, self.exam, "user-1")
        self.service.finalize_submission(session.id)

        queue = self.service.list_review_queue()
        result = self.service.apply_review_score(
            queue_id=queue[0].id,
            score_points=8,
            reviewed_by="admin@example.local",
            notes="Clear pronunciation",
        )

        self.assertEqual(result.status, "published")
        self.assertIsNotNone(result.published_at)
        self.assertEqual(result.metadata_json["pending_review_count"], 0)
        # Weighted: listening 5/6 (50%) + speaking 8/10 (50%)
        expected = (5 / 6 * 100 * 50 + 8 / 10 * 100 * 50) / 100
        self.assertAlmostEqual(result.score_percent, expected, places=3)
        self.assertTrue(result.passed)

        self.assertEqual(self.service.list_review_queue(), [])
        completed = self.service.list_review_queue(status="completed")
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].human_score_points, 8)

    def test_review_score_above_item_maximum_is_rejected(self):
        session = run_exam_to_submission(self.service, self.exam, "user-1")
        self.service.finalize_submission(session.id)
        queue = self.service.list_review_queue()

        with self.assertRaises(ExamServiceError):
            self.service.apply_review_score(
                queue_id=queue[0].id,
                score_points=11,
                reviewed_by="admin@example.local",
            )

    def test_wrong_mcq_answer_earns_zero(self):
        session = self.service.create_exam_session(
            exam_template_id=self.exam["template"].id,
            user_id="user-1",
        )
        self.service.start_exam(session.id)
        self.service.save_item_response(
            session_id=session.id,
            item_id=self.exam["mcq"].id,
            section_id=self.exam["listening"].id,
            response_type="mcq",
            selected_option_ids=["A"],
        )
        self.service.submit_exam(session.id)
        result = self.service.finalize_submission(session.id)

        responses = {
            r.item_id: r for r in self.service.get_session_responses(session.id)
        }
        self.assertEqual(responses[self.exam["mcq"].id].score_points_earned, 0)
        self.assertFalse(responses[self.exam["mcq"].id].is_correct)
        # No speaking response submitted -> nothing queued, result publishes
        self.assertEqual(result.status, "published")
        self.assertFalse(result.passed)


class ExamRoutesScoringTest(unittest.TestCase):
    def setUp(self):
        self.session_local = build_session_local()

        def override_db():
            db = self.session_local()
            try:
                yield db
            finally:
                db.close()

        self.app = create_app()
        self.app.dependency_overrides[get_db] = override_db
        self.client = TestClient(self.app)

        with self.session_local() as db:
            add_user(db, "user-1")
            add_user(db, "admin-1", role="admin")

        self.db = self.session_local()
        self.service = ExamService(self.db)
        self.exam = seed_exam(self.service)

    def tearDown(self):
        self.db.close()
        self.app.dependency_overrides.clear()

    def auth(self, user_id: str) -> dict:
        return {"Authorization": f"Bearer {create_access_token(user_id)}"}

    def test_submit_endpoint_returns_result_and_admin_can_score_review(self):
        session = run_exam_to_submission_via_responses(self.service, self.exam, "user-1")

        submit = self.client.post(
            f"/api/exam-runner/submit/{session.id}",
            headers=self.auth("user-1"),
        )
        self.assertEqual(submit.status_code, 200)
        body = submit.json()
        self.assertEqual(body["result_status"], "pending_review")
        self.assertEqual(body["pending_review_count"], 1)

        forbidden = self.client.get(
            "/api/exams/admin/review-queue",
            headers=self.auth("user-1"),
        )
        self.assertEqual(forbidden.status_code, 403)

        queue = self.client.get(
            "/api/exams/admin/review-queue",
            headers=self.auth("admin-1"),
        )
        self.assertEqual(queue.status_code, 200)
        entries = queue.json()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["item_type"], "audio_response")
        self.assertEqual(entries[0]["score_points_max"], 10)

        scored = self.client.post(
            f"/api/exams/admin/review-queue/{entries[0]['id']}/score",
            headers=self.auth("admin-1"),
            json={"score_points": 8, "notes": "Good"},
        )
        self.assertEqual(scored.status_code, 200)
        self.assertEqual(scored.json()["status"], "published")

        result = self.client.get(
            f"/api/exams/sessions/{session.id}/result",
            headers=self.auth("user-1"),
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["status"], "published")
        self.assertTrue(result.json()["passed"])


def run_exam_to_submission_via_responses(service: ExamService, exam: dict, user_id: str):
    """Save responses and start the session, but leave submission to the route."""
    session = service.create_exam_session(
        exam_template_id=exam["template"].id,
        user_id=user_id,
    )
    service.start_exam(session.id)
    service.save_item_response(
        session_id=session.id,
        item_id=exam["mcq"].id,
        section_id=exam["listening"].id,
        response_type="mcq",
        selected_option_ids=["B"],
    )
    service.save_item_response(
        session_id=session.id,
        item_id=exam["fill"].id,
        section_id=exam["listening"].id,
        response_type="fill_blank",
        text_response="Monday\nnurse",
    )
    service.save_item_response(
        session_id=session.id,
        item_id=exam["matching"].id,
        section_id=exam["listening"].id,
        response_type="matching",
        matched_pairs={"1": "A", "2": "B", "3": "C"},
    )
    service.save_item_response(
        session_id=session.id,
        item_id=exam["audio"].id,
        section_id=exam["speaking"].id,
        response_type="audio_response",
        file_url="https://example.com/answer.webm",
        audio_duration_seconds=20.0,
    )
    return session


if __name__ == "__main__":
    unittest.main()
