"""Seed A1 exam data."""
import hashlib
import secrets
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session

from app.db.exam_models import (
    ExamTemplateModel,
    ExamSectionModel,
    ExamItemModel,
)
from app.db.session import get_sessionmaker


def generate_id() -> str:
    """Generate a unique ID."""
    return hashlib.sha256(secrets.token_bytes(32)).hexdigest()[:64]


def create_a1_exam(db: Session) -> ExamTemplateModel:
    """Create the A1 exam template with all sections and items."""
    
    # 1. Create Exam Template
    template = ExamTemplateModel(
        id=generate_id(),
        code="CEFR-A1-EXAM-v1",
        level_code="A1",
        title="A1 Beginner English Exam",
        description="Official CEFR A1 level examination for English language proficiency. Tests basic communication skills in everyday situations.",
        duration_minutes=45,
        passing_score_percent=60,
        status="active",
        version=1,
        created_by="system",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(template)
    print(f"✓ Created exam template: {template.title} ({template.id[:8]}...)")
    
    # 2. Create Sections
    sections_data = [
        {
            "code": "LISTENING",
            "title": "Listening Comprehension",
            "description": "Understand simple spoken exchanges in everyday situations",
            "sequence_order": 1,
            "duration_minutes": 10,
            "score_weight_percent": 25,
            "item_types_allowed": ["mcq", "fill_blank", "matching"],
        },
        {
            "code": "READING",
            "title": "Reading Comprehension",
            "description": "Understand short, simple texts and common everyday signs",
            "sequence_order": 2,
            "duration_minutes": 8,
            "score_weight_percent": 20,
            "item_types_allowed": ["mcq", "fill_blank", "matching"],
        },
        {
            "code": "GRAMMAR_VOCABULARY",
            "title": "Grammar and Vocabulary",
            "description": "Demonstrate basic grammatical structures and vocabulary",
            "sequence_order": 3,
            "duration_minutes": 10,
            "score_weight_percent": 20,
            "item_types_allowed": ["mcq", "fill_blank", "matching"],
        },
        {
            "code": "SPEAKING",
            "title": "Speaking",
            "description": "Interact in simple conversations on familiar topics",
            "sequence_order": 4,
            "duration_minutes": 5,
            "score_weight_percent": 25,
            "item_types_allowed": ["audio_response"],
        },
        {
            "code": "WRITING",
            "title": "Writing",
            "description": "Write simple texts and fill in forms with personal details",
            "sequence_order": 5,
            "duration_minutes": 2,
            "score_weight_percent": 10,
            "item_types_allowed": ["text_response"],
        },
    ]
    
    sections = {}
    for data in sections_data:
        section = ExamSectionModel(
            id=generate_id(),
            exam_template_id=template.id,
            code=data["code"],
            title=data["title"],
            description=data["description"],
            sequence_order=data["sequence_order"],
            duration_minutes=data["duration_minutes"],
            score_weight_percent=data["score_weight_percent"],
            item_types_allowed=data["item_types_allowed"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(section)
        sections[data["code"]] = section
        print(f"  ✓ Created section: {section.title}")
    
    # 3. Create Items for each section
    create_listening_items(db, template.id, sections["LISTENING"].id)
    create_reading_items(db, template.id, sections["READING"].id)
    create_grammar_items(db, template.id, sections["GRAMMAR_VOCABULARY"].id)
    create_speaking_items(db, template.id, sections["SPEAKING"].id)
    create_writing_items(db, template.id, sections["WRITING"].id)
    
    return template


def create_listening_items(db: Session, template_id: str, section_id: str):
    """Create listening comprehension items."""
    items_data = [
        {
            "item_type": "mcq",
            "sequence_order": 1,
            "prompt_text": "Listen to the conversation. Where are the speakers?",
            "stimulus_text": "Man: Excuse me, how much is this coffee?\nWoman: It's three dollars.\nMan: And the sandwich?\nWoman: The sandwich is five dollars.",
            "options_json": [
                {"id": "A", "text": "In a restaurant"},
                {"id": "B", "text": "At a supermarket"},
                {"id": "C", "text": "In a café"},
            ],
            "correct_answer": {"option_id": "C"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 2,
            "prompt_text": "Listen to the dialogue. What time is the meeting?",
            "stimulus_text": "Woman: Hi John, are you coming to the meeting today?\nMan: Yes, what time is it?\nWoman: It's at three o'clock.\nMan: Okay, see you at three.",
            "options_json": [
                {"id": "A", "text": "At 2:00"},
                {"id": "B", "text": "At 3:00"},
                {"id": "C", "text": "At 4:00"},
            ],
            "correct_answer": {"option_id": "B"},
            "score_points": 1,
        },
        {
            "item_type": "fill_blank",
            "sequence_order": 3,
            "prompt_text": "Listen and fill in the blank. What day is it today?",
            "stimulus_text": "Today is [BLANK]. I go to work every [BLANK].",
            "options_json": None,
            "correct_answer": {"blanks": ["Monday", "Monday"]},
            "score_points": 2,
        },
    ]
    
    for data in items_data:
        item = ExamItemModel(
            id=generate_id(),
            exam_template_id=template_id,
            section_id=section_id,
            item_type=data["item_type"],
            sequence_order=data["sequence_order"],
            prompt_text=data["prompt_text"],
            stimulus_text=data.get("stimulus_text"),
            options_json=data.get("options_json"),
            correct_answer=data.get("correct_answer"),
            score_points=data["score_points"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(item)
    
    print(f"    ✓ Created {len(items_data)} listening items")


def create_reading_items(db: Session, template_id: str, section_id: str):
    """Create reading comprehension items."""
    items_data = [
        {
            "item_type": "mcq",
            "sequence_order": 1,
            "prompt_text": "Read the text. What time does the café open?",
            "stimulus_text": "**Sunshine Café**\n\nOpen: Monday - Saturday\nTime: 8:00 AM - 6:00 PM\n\nCome and enjoy our coffee and cakes!",
            "options_json": [
                {"id": "A", "text": "7:00 AM"},
                {"id": "B", "text": "8:00 AM"},
                {"id": "C", "text": "9:00 AM"},
            ],
            "correct_answer": {"option_id": "B"},
            "score_points": 1,
        },
        {
            "item_type": "fill_blank",
            "sequence_order": 2,
            "prompt_text": "Read Anna's message. Fill in the blanks.",
            "stimulus_text": "Hi! My name is Anna. I am from [BLANK]. I live in London now. I am a [BLANK]. I work in a hospital. I like my job!",
            "options_json": None,
            "correct_answer": {"blanks": ["Italy", "nurse"], "acceptable_variants": {"0": ["italy", "ITALY"], "1": ["Nurse", "NURSE"]}},
            "score_points": 2,
        },
    ]
    
    for data in items_data:
        item = ExamItemModel(
            id=generate_id(),
            exam_template_id=template_id,
            section_id=section_id,
            item_type=data["item_type"],
            sequence_order=data["sequence_order"],
            prompt_text=data["prompt_text"],
            stimulus_text=data.get("stimulus_text"),
            options_json=data.get("options_json"),
            correct_answer=data.get("correct_answer"),
            score_points=data["score_points"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(item)
    
    print(f"    ✓ Created {len(items_data)} reading items")


def create_grammar_items(db: Session, template_id: str, section_id: str):
    """Create grammar and vocabulary items."""
    items_data = [
        {
            "item_type": "mcq",
            "sequence_order": 1,
            "prompt_text": "Choose the correct answer: She _____ to work every day.",
            "options_json": [
                {"id": "A", "text": "go"},
                {"id": "B", "text": "goes"},
                {"id": "C", "text": "going"},
            ],
            "correct_answer": {"option_id": "B"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 2,
            "prompt_text": "Which word is a verb?",
            "options_json": [
                {"id": "A", "text": "Happy"},
                {"id": "B", "text": "Quickly"},
                {"id": "C", "text": "Eat"},
            ],
            "correct_answer": {"option_id": "C"},
            "score_points": 1,
        },
        {
            "item_type": "matching",
            "sequence_order": 3,
            "prompt_text": "Match the words with their meanings.",
            "options_json": {
                "left_items": [
                    {"id": "1", "text": "Big"},
                    {"id": "2", "text": "Happy"},
                    {"id": "3", "text": "Fast"},
                ],
                "right_items": [
                    {"id": "A", "text": "Not slow"},
                    {"id": "B", "text": "Not small"},
                    {"id": "C", "text": "Not sad"},
                ],
            },
            "correct_answer": {"pairs": {"1": "B", "2": "C", "3": "A"}},
            "score_points": 3,
        },
    ]
    
    for data in items_data:
        item = ExamItemModel(
            id=generate_id(),
            exam_template_id=template_id,
            section_id=section_id,
            item_type=data["item_type"],
            sequence_order=data["sequence_order"],
            prompt_text=data["prompt_text"],
            options_json=data.get("options_json"),
            correct_answer=data.get("correct_answer"),
            score_points=data["score_points"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(item)
    
    print(f"    ✓ Created {len(items_data)} grammar/vocabulary items")


def create_speaking_items(db: Session, template_id: str, section_id: str):
    """Create speaking items."""
    items_data = [
        {
            "item_type": "audio_response",
            "sequence_order": 1,
            "prompt_text": "Please read this sentence aloud: 'Hello, my name is Anna. I live in London.'",
            "stimulus_text": "Hello, my name is Anna. I live in London.",
            "rubric_criteria": {
                "pronunciation": {"weight": 0.4, "criteria": "Clear pronunciation of words"},
                "fluency": {"weight": 0.3, "criteria": "Natural flow and rhythm"},
                "accuracy": {"weight": 0.3, "criteria": "Correct stress and intonation"},
            },
            "score_points": 10,
        },
        {
            "item_type": "audio_response",
            "sequence_order": 2,
            "prompt_text": "Talk about your daily routine. What do you do every day? (Speak for 30-60 seconds)",
            "rubric_criteria": {
                "content": {"weight": 0.4, "criteria": "Relevance and completeness of response"},
                "vocabulary": {"weight": 0.3, "criteria": "Appropriate use of vocabulary"},
                "grammar": {"weight": 0.3, "criteria": "Correct use of simple structures"},
            },
            "score_points": 15,
        },
    ]
    
    for data in items_data:
        item = ExamItemModel(
            id=generate_id(),
            exam_template_id=template_id,
            section_id=section_id,
            item_type=data["item_type"],
            sequence_order=data["sequence_order"],
            prompt_text=data["prompt_text"],
            stimulus_text=data.get("stimulus_text"),
            rubric_criteria=data.get("rubric_criteria"),
            score_points=data["score_points"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(item)
    
    print(f"    ✓ Created {len(items_data)} speaking items")


def create_writing_items(db: Session, template_id: str, section_id: str):
    """Create writing items."""
    items_data = [
        {
            "item_type": "text_response",
            "sequence_order": 1,
            "prompt_text": "You are on holiday. Write a postcard to your friend (30-50 words). Include:\n- Where you are\n- The weather\n- What you are doing",
            "rubric_criteria": {
                "task_achievement": {"weight": 0.3, "criteria": "All points covered appropriately"},
                "vocabulary": {"weight": 0.3, "criteria": "Appropriate word choice"},
                "grammar": {"weight": 0.2, "criteria": "Simple structures mostly correct"},
                "organization": {"weight": 0.2, "criteria": "Logical flow"},
            },
            "score_points": 10,
        },
    ]
    
    for data in items_data:
        item = ExamItemModel(
            id=generate_id(),
            exam_template_id=template_id,
            section_id=section_id,
            item_type=data["item_type"],
            sequence_order=data["sequence_order"],
            prompt_text=data["prompt_text"],
            rubric_criteria=data.get("rubric_criteria"),
            score_points=data["score_points"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(item)
    
    print(f"    ✓ Created {len(items_data)} writing items")


def seed_a1_exam():
    """Main function to seed the A1 exam."""
    print("=" * 60)
    print("Seeding A1 Exam Data")
    print("=" * 60)
    
    db = get_sessionmaker()()
    try:
        template = create_a1_exam(db)
        db.commit()
        print("\n" + "=" * 60)
        print("✅ A1 Exam seeded successfully!")
        print(f"   Template ID: {template.id}")
        print(f"   Code: {template.code}")
        print(f"   Duration: {template.duration_minutes} minutes")
        print("=" * 60)
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding A1 exam: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_a1_exam()
