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
        # PRD attempt policy: 3 attempts, then a 30-day cooldown before retake.
        metadata_json={"max_attempts": 3, "cooldown_days": 30},
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
        {
            "item_type": "mcq",
            "sequence_order": 4,
            "prompt_text": "Listen to the conversation. What is Ben's phone number?",
            "stimulus_text": "Mina: Can I have your phone number, Ben?\nBen: Sure. It's oh eight one two, three four five six.\nMina: Oh eight one two, three four five six. Thank you.\nBen: You're welcome.",
            "options_json": [
                {"id": "A", "text": "0812 3456"},
                {"id": "B", "text": "0821 3456"},
                {"id": "C", "text": "0812 6543"},
            ],
            "correct_answer": {"option_id": "A"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 5,
            "prompt_text": "Listen to the dialogue. Where is Arif from?",
            "stimulus_text": "Alya: Nice to meet you. Where are you from?\nArif: I'm from Indonesia. And you?\nAlya: I'm from Malaysia.\nArif: Nice. Welcome to the class.",
            "options_json": [
                {"id": "A", "text": "Malaysia"},
                {"id": "B", "text": "Indonesia"},
                {"id": "C", "text": "Singapore"},
            ],
            "correct_answer": {"option_id": "B"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 6,
            "prompt_text": "Listen to the conversation. Where is the bank?",
            "stimulus_text": "Man: Excuse me, where is the bank?\nWoman: Go straight, then turn left. It's next to the post office.\nMan: Next to the post office. Thank you.\nWoman: You're welcome.",
            "options_json": [
                {"id": "A", "text": "Next to the post office"},
                {"id": "B", "text": "Across from the school"},
                {"id": "C", "text": "Behind the station"},
            ],
            "correct_answer": {"option_id": "A"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 7,
            "prompt_text": "Listen to the conversation. What does the customer order?",
            "stimulus_text": "Staff: Good morning. What would you like?\nLina: One hot tea, please.\nStaff: Anything else?\nLina: No, thank you. That's all.",
            "options_json": [
                {"id": "A", "text": "A hot tea"},
                {"id": "B", "text": "An iced coffee"},
                {"id": "C", "text": "An orange juice"},
            ],
            "correct_answer": {"option_id": "A"},
            "score_points": 1,
        },
        {
            "item_type": "fill_blank",
            "sequence_order": 8,
            "prompt_text": "Listen and fill in the blank. What time does John get up?",
            "stimulus_text": "Lina: What time do you get up?\nJohn: I get up at [BLANK] o'clock every morning.",
            "options_json": None,
            "correct_answer": {
                "blanks": ["seven"],
                "acceptable_variants": {"0": ["7", "seven o'clock"]},
            },
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 9,
            "prompt_text": "Listen to the end of the conversation. What does Sara say to close it?",
            "stimulus_text": "Sara: I have to go now. It was nice talking to you.\nBen: Nice talking to you too.\nSara: See you later. Bye!\nBen: Bye, Sara.",
            "options_json": [
                {"id": "A", "text": "Good morning"},
                {"id": "B", "text": "See you later"},
                {"id": "C", "text": "How are you?"},
            ],
            "correct_answer": {"option_id": "B"},
            "score_points": 1,
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
            "stimulus_text": "Hi! My name is Anna. I am from [BLANK]. I live in London now. I am a [BLANK]. I work in a hospital. I like my job!\n\nWord bank: Italy, nurse, teacher, Japan",
            "options_json": None,
            "correct_answer": {"blanks": ["Italy", "nurse"], "acceptable_variants": {"0": ["italy", "ITALY"], "1": ["Nurse", "NURSE"]}},
            "score_points": 2,
        },
        {
            "item_type": "mcq",
            "sequence_order": 3,
            "prompt_text": "Read the message. Where do they meet?",
            "stimulus_text": "Hi Ben! Are you free this Saturday? Let's meet at the station at four o'clock. We can walk to the park together. See you! - Mina",
            "options_json": [
                {"id": "A", "text": "At the park"},
                {"id": "B", "text": "At the station"},
                {"id": "C", "text": "At Mina's house"},
            ],
            "correct_answer": {"option_id": "B"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 4,
            "prompt_text": "Read the menu. How much is one tea and one cake together?",
            "stimulus_text": "**Corner Café Menu**\n\nTea ......... $2\nCoffee ....... $3\nCake ......... $4\nSandwich ..... $5",
            "options_json": [
                {"id": "A", "text": "$5"},
                {"id": "B", "text": "$6"},
                {"id": "C", "text": "$7"},
            ],
            "correct_answer": {"option_id": "B"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 5,
            "prompt_text": "Read Tomo's profile. What is his job?",
            "stimulus_text": "**Class Profile**\n\nName: Tomo\nCountry: Japan\nCity: Osaka\nJob: Taxi driver\nHobby: Cooking",
            "options_json": [
                {"id": "A", "text": "Cook"},
                {"id": "B", "text": "Teacher"},
                {"id": "C", "text": "Taxi driver"},
            ],
            "correct_answer": {"option_id": "C"},
            "score_points": 1,
        },
        {
            "item_type": "matching",
            "sequence_order": 6,
            "prompt_text": "Match each sign with its meaning.",
            "options_json": {
                "left_items": [
                    {"id": "1", "text": "OPEN"},
                    {"id": "2", "text": "EXIT"},
                    {"id": "3", "text": "PUSH"},
                ],
                "right_items": [
                    {"id": "A", "text": "The way out"},
                    {"id": "B", "text": "The shop is ready for you"},
                    {"id": "C", "text": "Move the door away from you"},
                ],
            },
            "correct_answer": {"pairs": {"1": "B", "2": "A", "3": "C"}},
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
        {
            "item_type": "mcq",
            "sequence_order": 4,
            "prompt_text": "Choose the correct answer: They _____ from Japan.",
            "options_json": [
                {"id": "A", "text": "is"},
                {"id": "B", "text": "are"},
                {"id": "C", "text": "am"},
            ],
            "correct_answer": {"option_id": "B"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 5,
            "prompt_text": "Choose the correct question word: _____ are you from?",
            "options_json": [
                {"id": "A", "text": "Where"},
                {"id": "B", "text": "When"},
                {"id": "C", "text": "Who"},
            ],
            "correct_answer": {"option_id": "A"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 6,
            "prompt_text": "Choose the correct answer: She is _____ engineer.",
            "options_json": [
                {"id": "A", "text": "a"},
                {"id": "B", "text": "an"},
                {"id": "C", "text": "the"},
            ],
            "correct_answer": {"option_id": "B"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 7,
            "prompt_text": "Choose the correct answer: This is _____ book. It is not your book.",
            "options_json": [
                {"id": "A", "text": "my"},
                {"id": "B", "text": "me"},
                {"id": "C", "text": "I"},
            ],
            "correct_answer": {"option_id": "A"},
            "score_points": 1,
        },
        {
            "item_type": "fill_blank",
            "sequence_order": 8,
            "prompt_text": "Complete the sentence with one word.",
            "stimulus_text": "I [BLANK] a student at this school.",
            "options_json": None,
            "correct_answer": {"blanks": ["am"], "acceptable_variants": {"0": ["'m"]}},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 9,
            "prompt_text": "Choose the opposite of \"cheap\".",
            "options_json": [
                {"id": "A", "text": "Expensive"},
                {"id": "B", "text": "Small"},
                {"id": "C", "text": "Easy"},
            ],
            "correct_answer": {"option_id": "A"},
            "score_points": 1,
        },
        {
            "item_type": "mcq",
            "sequence_order": 10,
            "prompt_text": "Choose the correct answer: The class is _____ Monday.",
            "options_json": [
                {"id": "A", "text": "in"},
                {"id": "B", "text": "at"},
                {"id": "C", "text": "on"},
            ],
            "correct_answer": {"option_id": "C"},
            "score_points": 1,
        },
        {
            "item_type": "matching",
            "sequence_order": 11,
            "prompt_text": "Match each question with the best answer.",
            "options_json": {
                "left_items": [
                    {"id": "1", "text": "How are you?"},
                    {"id": "2", "text": "What's your name?"},
                    {"id": "3", "text": "Where are you from?"},
                ],
                "right_items": [
                    {"id": "A", "text": "I'm from Brazil."},
                    {"id": "B", "text": "I'm fine, thank you."},
                    {"id": "C", "text": "My name is Tom."},
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
            "prompt_text": "Introduce yourself. Say your name, your country, and your job or study. (Speak for 20-40 seconds)",
            "rubric_criteria": {
                "content": {"weight": 0.4, "criteria": "Says name, origin, and job or study"},
                "pronunciation": {"weight": 0.3, "criteria": "Clear enough to understand"},
                "fluency": {"weight": 0.3, "criteria": "Steady pacing without long pauses"},
            },
            "score_points": 10,
        },
        {
            "item_type": "audio_response",
            "sequence_order": 3,
            "prompt_text": "Answer the question: What food do you like? Say one or two sentences.",
            "rubric_criteria": {
                "content": {"weight": 0.4, "criteria": "Answers the question with a relevant food"},
                "vocabulary": {"weight": 0.3, "criteria": "Uses simple food and like/don't like words"},
                "grammar": {"weight": 0.3, "criteria": "Uses I like / I don't like correctly"},
            },
            "score_points": 10,
        },
        {
            "item_type": "audio_response",
            "sequence_order": 4,
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
        {
            "item_type": "text_response",
            "sequence_order": 2,
            "prompt_text": "You have a new online classmate. Write a short reply (20-40 words). Include:\n- Your name\n- Your country or city\n- One polite closing phrase",
            "rubric_criteria": {
                "task_achievement": {"weight": 0.4, "criteria": "Includes name, origin, and a closing phrase"},
                "vocabulary": {"weight": 0.3, "criteria": "Uses simple introduction phrases"},
                "grammar": {"weight": 0.3, "criteria": "Uses I am / I'm from correctly"},
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
        from sqlalchemy import select

        existing = db.execute(
            select(ExamTemplateModel).where(ExamTemplateModel.code == "CEFR-A1-EXAM-v1")
        ).scalar_one_or_none()
        if existing:
            print("⚠️  Exam template CEFR-A1-EXAM-v1 already exists. Delete it first to reseed.")
            return

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
