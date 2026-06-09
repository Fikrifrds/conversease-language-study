"""End-to-end test for the exam system."""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.db.models import UserModel
from app.db.session import get_sessionmaker
from app.services.exam_service import ExamService


def test_exam_e2e():
    """Run end-to-end test of exam system."""
    print("=" * 70)
    print("EXAM SYSTEM E2E TEST")
    print("=" * 70)
    
    db = get_sessionmaker()()
    try:
        service = ExamService(db)

        # Step 1: List available exams
        print("\n📋 Step 1: List available exams")
        templates = service.list_exam_templates(
            level_code="A1",
            status="active",
        )
        print(f"   Found {len(templates)} active A1 exam(s)")
        if not templates:
            print("   ❌ No exams found! Run seed_a1_exam.py first.")
            return
        
        template = templates[0]
        print(f"   ✓ Using exam: {template.title} (ID: {template.id[:8]}...)")

        # Step 2: Get exam structure
        print("\n📚 Step 2: Get exam structure")
        sections = service.get_exam_sections(template.id)
        print(f"   Exam has {len(sections)} section(s):")
        for section in sections:
            items = service.get_exam_items(section.id)
            print(f"   - {section.title}: {len(items)} item(s), {section.duration_minutes} min")

        # Step 3: Create and start exam session
        print("\n🚀 Step 3: Create and start exam session")
        user_row = db.execute(select(UserModel.id).order_by(UserModel.created_at.asc()).limit(1)).first()
        if user_row is None:
            print("   ❌ No users found in database. Create a user first.")
            return
        test_user_id = user_row[0]

        session = service.create_exam_session(
            exam_template_id=template.id,
            user_id=test_user_id,
        )
        print(f"   ✓ Created session: {session.id[:8]}...")

        # Start the exam
        first_section_id = sections[0].id if sections else None
        first_items = service.get_exam_items(first_section_id) if first_section_id else []
        first_item_id = first_items[0].id if first_items else None

        session = service.start_exam(
            session_id=session.id,
            current_section_id=first_section_id,
            current_item_id=first_item_id,
        )
        time_remaining = int((session.expires_at - datetime.utcnow()).total_seconds())
        print(f"   ✓ Exam started at: {session.started_at}")
        print(f"   ✓ Expires at: {session.expires_at}")
        print(f"   ✓ Time remaining: {time_remaining // 60} minutes")

        # Step 4: Submit responses for items
        print("\n✏️  Step 4: Submit responses")

        # Get first section items
        items = service.get_exam_items(first_section_id)
        for i, item in enumerate(items[:2]):  # Submit first 2 items
            print(f"   Submitting response for item {i+1}/{len(items)}: {item.id[:8]}...")

            # Prepare response based on item type
            if item.item_type == "mcq" and item.options_json:
                selected = [item.options_json[0]["id"]] if item.options_json else []
                response = service.save_item_response(
                    session_id=session.id,
                    item_id=item.id,
                    section_id=first_section_id,
                    response_type="mcq",
                    selected_option_ids=selected,
                    time_spent_seconds=30,
                )
            elif item.item_type == "fill_blank":
                response = service.save_item_response(
                    session_id=session.id,
                    item_id=item.id,
                    section_id=first_section_id,
                    response_type="fill_blank",
                    text_response="Sample answer",
                    time_spent_seconds=45,
                )
            else:
                response = service.save_item_response(
                    session_id=session.id,
                    item_id=item.id,
                    section_id=first_section_id,
                    response_type=item.item_type,
                    text_response="Test response",
                    time_spent_seconds=30,
                )

            print(f"   ✓ Response saved: {response.id[:8]}...")

        # Step 5: Check exam status
        print("\n📊 Step 5: Check exam status")
        responses = service.get_session_responses(session.id)
        print(f"   Total responses submitted: {len(responses)}")

        # Step 6: Submit exam
        print("\n📝 Step 6: Submit exam")
        session = service.submit_exam(session.id)
        print(f"   ✓ Exam submitted at: {session.submitted_at}")

        # Final summary
        print("\n" + "=" * 70)
        print("✅ E2E TEST COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\n📋 Summary:")
        print(f"   • Exam Template: {template.title}")
        print(f"   • Session ID: {session.id}")
        print(f"   • User ID: {test_user_id}")
        print(f"   • Responses Submitted: {len(responses)}")
        print(f"   • Exam Status: {session.status}")
        print("\n✨ All core exam flows working correctly!")
        print("=" * 70)
    finally:
        db.close()


if __name__ == "__main__":
    test_exam_e2e()
