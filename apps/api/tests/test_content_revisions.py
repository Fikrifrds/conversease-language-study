import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import models  # noqa: F401
from app.db.base import Base
from app.repositories.content_revisions import ContentRevisionRepository


class ContentRevisionRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def test_record_revision_versions_are_scoped_to_resource(self):
        with self.SessionLocal() as db:
            repository = ContentRevisionRepository(db)

            first = repository.record_revision(
                resource_type="curriculum_lesson",
                resource_key="saying-your-name",
                action="update",
                changed_by="Fikri",
                before_payload={"title": "Old title"},
                after_payload={"title": "New title"},
            )
            second = repository.record_revision(
                resource_type="curriculum_lesson",
                resource_key="saying-your-name",
                action="update",
                changed_by="Fikri",
                before_payload={"title": "New title"},
                after_payload={"title": "Newer title"},
            )
            other = repository.record_revision(
                resource_type="email_template",
                resource_key="auth_verify_email",
                action="update",
                changed_by="Admin",
                after_payload={"subject": "Verify"},
            )

            lesson_revisions = repository.list_revisions(
                resource_type="curriculum_lesson",
                resource_key="saying-your-name",
            )

            self.assertEqual(first.version, 1)
            self.assertEqual(second.version, 2)
            self.assertEqual(other.version, 1)
            self.assertEqual([revision.version for revision in lesson_revisions], [2, 1])
            self.assertEqual(repository.latest_revision(
                resource_type="curriculum_lesson",
                resource_key="saying-your-name",
            ).id, second.id)


if __name__ == "__main__":
    unittest.main()
