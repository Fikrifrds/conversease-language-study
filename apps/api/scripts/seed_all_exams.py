"""Seed exam data for all CEFR levels (A2, B1, B2, C1).

Usage:
    PYTHONPATH=apps/api apps/api/.venv/bin/python apps/api/scripts/seed_all_exams.py
"""
import hashlib
import secrets
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.exam_models import ExamTemplateModel, ExamSectionModel, ExamItemModel
from app.db.session import get_sessionmaker


def generate_id() -> str:
    return hashlib.sha256(secrets.token_bytes(32)).hexdigest()[:64]


SECTIONS_TEMPLATE = [
    {"code": "LISTENING", "title": "Listening Comprehension", "seq": 1, "minutes": 10, "weight": 25, "types": ["mcq", "fill_blank", "matching"]},
    {"code": "READING", "title": "Reading Comprehension", "seq": 2, "minutes": 8, "weight": 20, "types": ["mcq", "fill_blank", "matching"]},
    {"code": "GRAMMAR_VOCABULARY", "title": "Grammar and Vocabulary", "seq": 3, "minutes": 10, "weight": 20, "types": ["mcq", "fill_blank", "matching"]},
    {"code": "SPEAKING", "title": "Speaking", "seq": 4, "minutes": 5, "weight": 25, "types": ["audio_response"]},
    {"code": "WRITING", "title": "Writing", "seq": 5, "minutes": 2, "weight": 10, "types": ["text_response"]},
]


EXAM_CONFIGS = {
    "A2": {
        "code": "CEFR-A2-EXAM-v1",
        "title": "A2 Elementary English Exam",
        "description": "CEFR A2 level examination. Tests ability to handle everyday conversations and simple past experiences.",
        "duration": 45,
        "passing": 60,
    },
    "B1": {
        "code": "CEFR-B1-EXAM-v1",
        "title": "B1 Intermediate English Exam",
        "description": "CEFR B1 level examination. Tests ability to express opinions, tell stories, and handle workplace conversations.",
        "duration": 50,
        "passing": 65,
    },
    "B2": {
        "code": "CEFR-B2-EXAM-v1",
        "title": "B2 Upper Intermediate English Exam",
        "description": "CEFR B2 level examination. Tests ability to discuss professional topics, present ideas, and negotiate.",
        "duration": 55,
        "passing": 70,
    },
    "C1": {
        "code": "CEFR-C1-EXAM-v1",
        "title": "C1 Advanced English Exam",
        "description": "CEFR C1 level examination. Tests ability to handle nuanced discussions, presentations, and complex professional communication.",
        "duration": 60,
        "passing": 75,
    },
}


# ── A2 Items ──────────────────────────────────────────────────────────────

A2_LISTENING = [
    {"item_type": "mcq", "seq": 1, "prompt": "Listen to the conversation. What are the friends planning to do this weekend?",
     "stimulus": "Mina: Hi Riko! Do you want to do something this weekend?\nRiko: Sure! How about going to the cinema?\nMina: Great idea. What time?\nRiko: How about three o'clock on Saturday?\nMina: Perfect. See you then!",
     "options": [{"id": "A", "text": "Go to the cinema"}, {"id": "B", "text": "Go shopping"}, {"id": "C", "text": "Study together"}],
     "answer": {"option_id": "A"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Listen to the dialogue. Where did Rina go yesterday?",
     "stimulus": "Ben: Hey Rina, how was your weekend?\nRina: It was great! I went to the beach with my family.\nBen: Nice! Was the weather good?\nRina: Yes, it was sunny and warm.",
     "options": [{"id": "A", "text": "To the mountains"}, {"id": "B", "text": "To the beach"}, {"id": "C", "text": "To the park"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 3, "prompt": "Listen to the conversation. What time does the train leave?",
     "stimulus": "Man: Excuse me, what time does the next train to Jakarta leave?\nWoman: The next train leaves at 2:30 PM.\nMan: How much is a ticket?\nWoman: It's 150,000 rupiah.",
     "options": [{"id": "A", "text": "At 2:00 PM"}, {"id": "B", "text": "At 2:30 PM"}, {"id": "C", "text": "At 3:00 PM"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 4, "prompt": "Listen and fill in the blank.",
     "stimulus": "Woman: How do you feel today?\nMan: I feel a bit [BLANK]. I think I have a cold.",
     "answer": {"blanks": ["sick"], "acceptable_variants": {"0": ["ill", "unwell"]}}, "points": 1},
    {"item_type": "mcq", "seq": 5, "prompt": "Listen to the dialogue. What size does the customer want?",
     "stimulus": "Staff: Can I help you?\nWoman: Yes, I'd like this T-shirt, please.\nStaff: What size? Small, medium, or large?\nWoman: Medium, please. And do you have it in blue?",
     "options": [{"id": "A", "text": "Small"}, {"id": "B", "text": "Medium"}, {"id": "C", "text": "Large"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 6, "prompt": "Listen to the conversation. What did Andi do yesterday?",
     "stimulus": "Sari: What did you do yesterday, Andi?\nAndi: I watched a movie with my friends.\nSari: What movie?\nAndi: It was an action movie. It was exciting!",
     "options": [{"id": "A", "text": "He went shopping"}, {"id": "B", "text": "He watched a movie"}, {"id": "C", "text": "He studied at home"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 7, "prompt": "Listen and fill in the blank.",
     "stimulus": "Doctor: How long have you had this headache?\nPatient: Since [BLANK]. Two days ago it started.",
     "answer": {"blanks": ["Monday"], "acceptable_variants": {"0": ["yesterday", "last week"]}}, "points": 1},
]

A2_READING = [
    {"item_type": "mcq", "seq": 1, "prompt": "Read the message. What time will they meet?",
     "stimulus": "Hi Dina! Let's meet at the café near the station at 4 PM. I want to show you the photos from my trip. See you! - Rina",
     "options": [{"id": "A", "text": "At 3 PM"}, {"id": "B", "text": "At 4 PM"}, {"id": "C", "text": "At 5 PM"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Read the email. Why is Budi writing?",
     "stimulus": "Hi Sari,\nI'm writing to invite you to my birthday party this Saturday. It's at my house at 7 PM. I hope you can come!\nBest, Budi",
     "options": [{"id": "A", "text": "To ask for help"}, {"id": "B", "text": "To invite Sari to a party"}, {"id": "C", "text": "To say thank you"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 3, "prompt": "Read the note. Fill in the blanks.",
     "stimulus": "Dear Roommate,\nI went to the [BLANK] to buy some groceries. I'll be back in one [BLANK]. Please cook the rice.\n- Adi",
     "answer": {"blanks": ["supermarket", "hour"], "acceptable_variants": {"0": ["store", "market"], "1": ["hour"]}}, "points": 2},
    {"item_type": "mcq", "seq": 4, "prompt": "Read the sign. When is the library closed?",
     "stimulus": "**City Library**\nOpen: Monday - Friday, 9 AM - 8 PM\nSaturday: 9 AM - 5 PM\nSunday: CLOSED",
     "options": [{"id": "A", "text": "On Monday"}, {"id": "B", "text": "On Saturday"}, {"id": "C", "text": "On Sunday"}],
     "answer": {"option_id": "C"}, "points": 1},
    {"item_type": "matching", "seq": 5, "prompt": "Match each situation with the best response.",
     "options": {"left_items": [{"id": "1", "text": "How was your weekend?"}, {"id": "2", "text": "Do you want to come?"}, {"id": "3", "text": "I'm sorry I'm late."}],
                 "right_items": [{"id": "A", "text": "No worries. We just started."}, {"id": "B", "text": "It was great, thanks!"}, {"id": "C", "text": "Yes, I'd love to!"}]},
     "answer": {"pairs": {"1": "B", "2": "C", "3": "A"}}, "points": 3},
]

A2_GRAMMAR = [
    {"item_type": "mcq", "seq": 1, "prompt": "Choose the correct answer: She _____ to the store yesterday.",
     "options": [{"id": "A", "text": "go"}, {"id": "B", "text": "goes"}, {"id": "C", "text": "went"}],
     "answer": {"option_id": "C"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Choose the correct answer: I _____ a headache since this morning.",
     "options": [{"id": "A", "text": "have"}, {"id": "B", "text": "has"}, {"id": "C", "text": "having"}],
     "answer": {"option_id": "A"}, "points": 1},
    {"item_type": "mcq", "seq": 3, "prompt": "Which sentence uses 'going to' correctly for a plan?",
     "options": [{"id": "A", "text": "I going to visit my friend."}, {"id": "B", "text": "I'm going to visit my friend."}, {"id": "C", "text": "I'm go to visit my friend."}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 4, "prompt": "Complete with one word.",
     "stimulus": "We _____ at the restaurant last night. The food was delicious.",
     "answer": {"blanks": ["ate"], "acceptable_variants": {"0": ["had", "dined"]}}, "points": 1},
    {"item_type": "mcq", "seq": 5, "prompt": "Choose the correct question: _____ did you go on holiday?",
     "options": [{"id": "A", "text": "Where"}, {"id": "B", "text": "When"}, {"id": "C", "text": "What"}],
     "answer": {"option_id": "A"}, "points": 1},
    {"item_type": "matching", "seq": 6, "prompt": "Match each word with its opposite.",
     "options": {"left_items": [{"id": "1", "text": "expensive"}, {"id": "2", "text": "difficult"}, {"id": "3", "text": "boring"}],
                 "right_items": [{"id": "A", "text": "cheap"}, {"id": "B", "text": "exciting"}, {"id": "C", "text": "easy"}]},
     "answer": {"pairs": {"1": "A", "2": "C", "3": "B"}}, "points": 3},
]

A2_SPEAKING = [
    {"item_type": "audio_response", "seq": 1, "prompt": "Read this sentence aloud: 'Yesterday I went to the supermarket and bought some vegetables.'",
     "stimulus": "Yesterday I went to the supermarket and bought some vegetables.",
     "rubric": {"pronunciation": {"weight": 0.4}, "fluency": {"weight": 0.3}, "accuracy": {"weight": 0.3}}, "points": 10},
    {"item_type": "audio_response", "seq": 2, "prompt": "Talk about what you did last weekend. Where did you go? What did you do? (Speak for 20-40 seconds)",
     "rubric": {"content": {"weight": 0.4}, "grammar": {"weight": 0.3}, "fluency": {"weight": 0.3}}, "points": 10},
    {"item_type": "audio_response", "seq": 3, "prompt": "You are at a café. Order a drink and ask about the price. (Speak for 15-30 seconds)",
     "rubric": {"content": {"weight": 0.4}, "vocabulary": {"weight": 0.3}, "pronunciation": {"weight": 0.3}}, "points": 10},
]

A2_WRITING = [
    {"item_type": "text_response", "seq": 1, "prompt": "Write a short message to your friend about your weekend plans (30-50 words). Include:\n- What you plan to do\n- When\n- Invite your friend",
     "rubric": {"task_achievement": {"weight": 0.3}, "vocabulary": {"weight": 0.3}, "grammar": {"weight": 0.2}, "organization": {"weight": 0.2}}, "points": 10},
    {"item_type": "text_response", "seq": 2, "prompt": "Write about what you did yesterday (30-50 words). Include:\n- Where you went\n- What you did\n- How you felt",
     "rubric": {"task_achievement": {"weight": 0.3}, "vocabulary": {"weight": 0.3}, "grammar": {"weight": 0.2}, "organization": {"weight": 0.2}}, "points": 10},
]


# ── B1 Items ──────────────────────────────────────────────────────────────

B1_LISTENING = [
    {"item_type": "mcq", "seq": 1, "prompt": "Listen to the conversation. What problem does the speaker describe?",
     "stimulus": "Woman: I've been having trouble with my laptop. It keeps freezing every time I open more than two programs.\nMan: Have you tried restarting it?\nWoman: Yes, several times. It didn't help.\nMan: You might need more memory. I can take a look if you want.",
     "options": [{"id": "A", "text": "The laptop is too old"}, {"id": "B", "text": "The laptop freezes with multiple programs"}, {"id": "C", "text": "The laptop won't turn on"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Listen to the discussion. What does the team decide?",
     "stimulus": "Manager: So, should we launch the product next week or wait until the feedback is ready?\nDev: I think we should wait. The feedback could change our approach.\nMarketing: I agree. Let's aim for the end of the month.\nManager: OK, let's postpone to the 28th.",
     "options": [{"id": "A", "text": "Launch next week"}, {"id": "B", "text": "Postpone to the end of the month"}, {"id": "C", "text": "Cancel the launch"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 3, "prompt": "Listen and fill in the blank.",
     "stimulus": "I've been living in this city for three [BLANK]. I moved here because of my job.",
     "answer": {"blanks": ["years"], "acceptable_variants": {"0": ["years"]}}, "points": 1},
    {"item_type": "mcq", "seq": 4, "prompt": "Listen to the conversation. Why is the woman upset?",
     "stimulus": "Woman: I'm really frustrated. I ordered a book two weeks ago and it still hasn't arrived.\nMan: Did you check the tracking number?\nWoman: Yes, it says it's still in transit. I needed it for my class.\nMan: You should contact customer service.",
     "options": [{"id": "A", "text": "The book is damaged"}, {"id": "B", "text": "The book hasn't arrived yet"}, {"id": "C", "text": "The book is the wrong one"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 5, "prompt": "Listen to the speaker. What is the main recommendation?",
     "stimulus": "If you want to improve your English, I recommend watching English movies with subtitles. Start with subtitles in your language, then switch to English subtitles. It helps with listening and vocabulary at the same time.",
     "options": [{"id": "A", "text": "Read English books"}, {"id": "B", "text": "Watch English movies with subtitles"}, {"id": "C", "text": "Take an English class"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 6, "prompt": "Listen to the conversation. What suggestion does the man make?",
     "stimulus": "Woman: I'm stressed about my presentation tomorrow.\nMan: Why don't you practice it in front of a mirror? It really helps with confidence.\nWoman: That's a good idea. I'll try it tonight.\nMan: Good luck! You'll do great.",
     "options": [{"id": "A", "text": "Cancel the presentation"}, {"id": "B", "text": "Practice in front of a mirror"}, {"id": "C", "text": "Ask someone else to present"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 7, "prompt": "Listen and fill in the blank.",
     "stimulus": "Woman: What are your plans for the holiday?\nMan: I'm thinking of visiting my [BLANK] in Surabaya. I haven't seen them in a while.",
     "answer": {"blanks": ["parents"], "acceptable_variants": {"0": ["family", "grandparents", "relatives"]}}, "points": 1},
]

B1_READING = [
    {"item_type": "mcq", "seq": 1, "prompt": "Read the email. What is the main purpose?",
     "stimulus": "Hi Team,\nJust a quick update: the meeting has been moved from Wednesday to Friday at 2 PM. The room is the same. Please let me know if Friday doesn't work for you.\nThanks, Sarah",
     "options": [{"id": "A", "text": "To cancel the meeting"}, {"id": "B", "text": "To reschedule the meeting"}, {"id": "C", "text": "To invite new people"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Read the review. What does the reviewer think?",
     "stimulus": "I tried the new restaurant downtown. The food was excellent, especially the pasta. However, the service was quite slow - we waited 30 minutes for our main course. I'd give it 3 out of 5 stars.",
     "options": [{"id": "A", "text": "The food and service were both great"}, {"id": "B", "text": "The food was good but the service was slow"}, {"id": "C", "text": "The reviewer hated the restaurant"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 3, "prompt": "Read the message and fill in the blanks.",
     "stimulus": "Hi! I wanted to tell you that I got the [BLANK]! I start next Monday. I'm really [BLANK] about it. Let's celebrate this weekend!",
     "answer": {"blanks": ["job", "excited"], "acceptable_variants": {"0": ["position", "promotion"], "1": ["happy", "thrilled"]}}, "points": 2},
    {"item_type": "matching", "seq": 4, "prompt": "Match each phrase with its purpose.",
     "options": {"left_items": [{"id": "1", "text": "I'm writing to let you know"}, {"id": "2", "text": "I was wondering if"}, {"id": "3", "text": "I'd appreciate it if"}],
                 "right_items": [{"id": "A", "text": "Making a polite request"}, {"id": "B", "text": "Giving information"}, {"id": "C", "text": "Asking a polite question"}]},
     "answer": {"pairs": {"1": "B", "2": "C", "3": "A"}}, "points": 3},
    {"item_type": "mcq", "seq": 5, "prompt": "Read the announcement. What is being announced?",
     "stimulus": "Important: Starting next month, all employees must submit their weekly reports by Friday at 5 PM instead of Monday morning. This change aims to improve our planning process for the following week.",
     "options": [{"id": "A", "text": "A new vacation policy"}, {"id": "B", "text": "A change in report deadline"}, {"id": "C", "text": "A new meeting schedule"}],
     "answer": {"option_id": "B"}, "points": 1},
]

B1_GRAMMAR = [
    {"item_type": "mcq", "seq": 1, "prompt": "Choose the correct answer: I _____ in London for three years before I moved to Jakarta.",
     "options": [{"id": "A", "text": "lived"}, {"id": "B", "text": "have lived"}, {"id": "C", "text": "had lived"}],
     "answer": {"option_id": "C"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Choose the correct answer: _____ it rains, we'll stay inside.",
     "options": [{"id": "A", "text": "Although"}, {"id": "B", "text": "If"}, {"id": "C", "text": "Because"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 3, "prompt": "Which sentence uses a linking word correctly?",
     "options": [{"id": "A", "text": "I was tired, so I went to bed early."}, {"id": "B", "text": "I was tired, because I went to bed early."}, {"id": "C", "text": "I was tired, but I went to bed early."}],
     "answer": {"option_id": "A"}, "points": 1},
    {"item_type": "fill_blank", "seq": 4, "prompt": "Complete with one word.",
     "stimulus": "You [BLANK] see a doctor if the pain continues.",
     "answer": {"blanks": ["should"], "acceptable_variants": {"0": ["must", "ought to"]}}, "points": 1},
    {"item_type": "mcq", "seq": 5, "prompt": "Choose the correct passive form: The report _____ by the team last week.",
     "options": [{"id": "A", "text": "was written"}, {"id": "B", "text": "wrote"}, {"id": "C", "text": "is written"}],
     "answer": {"option_id": "A"}, "points": 1},
]

B1_SPEAKING = [
    {"item_type": "audio_response", "seq": 1, "prompt": "Read this sentence aloud: 'Although the project was challenging, the team managed to finish it on time.'",
     "stimulus": "Although the project was challenging, the team managed to finish it on time.",
     "rubric": {"pronunciation": {"weight": 0.4}, "fluency": {"weight": 0.3}, "accuracy": {"weight": 0.3}}, "points": 10},
    {"item_type": "audio_response", "seq": 2, "prompt": "Describe a problem you had at work or school and how you solved it. (Speak for 30-60 seconds)",
     "rubric": {"content": {"weight": 0.4}, "grammar": {"weight": 0.3}, "fluency": {"weight": 0.3}}, "points": 15},
    {"item_type": "audio_response", "seq": 3, "prompt": "Give your opinion about learning English online. Do you think it's effective? Why or why not? (Speak for 20-40 seconds)",
     "rubric": {"content": {"weight": 0.4}, "vocabulary": {"weight": 0.3}, "pronunciation": {"weight": 0.3}}, "points": 10},
]

B1_WRITING = [
    {"item_type": "text_response", "seq": 1, "prompt": "Write a reply to this message (40-60 words):\n\n'Hi! I'm planning to change jobs. What do you think I should consider before making the decision?'\n\nInclude your opinion, one reason, and a polite closing.",
     "rubric": {"task_achievement": {"weight": 0.3}, "vocabulary": {"weight": 0.3}, "grammar": {"weight": 0.2}, "organization": {"weight": 0.2}}, "points": 10},
    {"item_type": "text_response", "seq": 2, "prompt": "Write about a problem you had and how you solved it (40-60 words). Include:\n- What the problem was\n- What you did to solve it\n- How you felt after",
     "rubric": {"task_achievement": {"weight": 0.3}, "vocabulary": {"weight": 0.3}, "grammar": {"weight": 0.2}, "organization": {"weight": 0.2}}, "points": 10},
]


# ── B2 Items ──────────────────────────────────────────────────────────────

B2_LISTENING = [
    {"item_type": "mcq", "seq": 1, "prompt": "Listen to the meeting discussion. What is the main concern raised?",
     "stimulus": "Manager: We need to discuss the Q3 targets. Sales are down 15% compared to last quarter.\nSales Lead: I think the main issue is that our competitors launched similar products at lower prices.\nManager: That's a fair point. What do you suggest?\nSales Lead: We should focus on our unique features and consider a promotional campaign.",
     "options": [{"id": "A", "text": "The team is understaffed"}, {"id": "B", "text": "Sales are down due to competitor pricing"}, {"id": "C", "text": "The product needs redesign"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Listen to the speaker. What is the speaker's position?",
     "stimulus": "While remote work has clear benefits - flexibility, no commute, better work-life balance - I believe hybrid work is the best approach. It gives employees the freedom to choose while maintaining team collaboration. The key is to be intentional about which days are in-office.",
     "options": [{"id": "A", "text": "Fully remote work is best"}, {"id": "B", "text": "Hybrid work is the best approach"}, {"id": "C", "text": "Everyone should work in the office"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 3, "prompt": "Listen and fill in the blank.",
     "stimulus": "The proposal was rejected because the budget was too [BLANK]. We need to find a more cost-effective solution.",
     "answer": {"blanks": ["high"], "acceptable_variants": {"0": ["expensive", "large"]}}, "points": 1},
    {"item_type": "mcq", "seq": 4, "prompt": "Listen to the negotiation. What compromise is reached?",
     "stimulus": "Client: We'd like the delivery by March 1st.\nSupplier: That's tight. We can do March 15th without extra cost.\nClient: How about March 10th? We could accept a small premium.\nSupplier: That works. March 10th with a 5% rush fee.\nClient: Agreed.",
     "options": [{"id": "A", "text": "March 1st with no extra cost"}, {"id": "B", "text": "March 10th with a 5% rush fee"}, {"id": "C", "text": "March 15th with no extra cost"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 5, "prompt": "Listen to the presentation. What evidence does the speaker use?",
     "stimulus": "Our customer satisfaction scores have improved by 20% since we introduced the new support system. The average response time dropped from 24 hours to 4 hours. These numbers show that investing in infrastructure directly impacts customer experience.",
     "options": [{"id": "A", "text": "Personal opinions"}, {"id": "B", "text": "Statistics and data"}, {"id": "C", "text": "Expert testimonials"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 6, "prompt": "Listen and fill in the blank.",
     "stimulus": "We need to [BLANK] the risks before making a final decision. Rushing could cost us more in the long run.",
     "answer": {"blanks": ["assess"], "acceptable_variants": {"0": ["evaluate", "consider", "analyze"]}}, "points": 1},
]

B2_READING = [
    {"item_type": "mcq", "seq": 1, "prompt": "Read the email. What action is requested?",
     "stimulus": "Hi Team,\nFollowing our discussion, I'd like to propose we restructure the onboarding process. Specifically, I suggest we split the technical and cultural orientation into separate sessions. This would allow new hires to absorb information more effectively.\nCould you share your thoughts by Friday?\nBest, David",
     "options": [{"id": "A", "text": "To approve a budget increase"}, {"id": "B", "text": "To get feedback on a proposed change"}, {"id": "C", "text": "To announce a new hire"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Read the article excerpt. What is the author's main argument?",
     "stimulus": "Many companies claim to value innovation, yet their internal processes discourage creative thinking. Employees are rewarded for following established procedures rather than challenging them. If organizations truly want innovation, they need to create safe spaces for experimentation and accept that failure is part of the process.",
     "options": [{"id": "A", "text": "Companies should follow established procedures"}, {"id": "B", "text": "Companies need to create safe spaces for experimentation"}, {"id": "C", "text": "Innovation is not important for companies"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "matching", "seq": 3, "prompt": "Match each discourse marker with its function.",
     "options": {"left_items": [{"id": "1", "text": "However"}, {"id": "2", "text": "Furthermore"}, {"id": "3", "text": "In conclusion"}],
                 "right_items": [{"id": "A", "text": "Adding information"}, {"id": "B", "text": "Contrasting"}, {"id": "C", "text": "Summarizing"}]},
     "answer": {"pairs": {"1": "B", "2": "A", "3": "C"}}, "points": 3},
    {"item_type": "mcq", "seq": 4, "prompt": "Read the policy update. What is the main change?",
     "stimulus": "Effective immediately, all expense reports must include receipts for any purchase over $25, down from the previous threshold of $50. Additionally, reports submitted more than 30 days after the expense will not be reimbursed. This change aligns with our updated compliance requirements.",
     "options": [{"id": "A", "text": "The receipt threshold is now lower"}, {"id": "B", "text": "Expenses no longer need receipts"}, {"id": "C", "text": "The deadline for reports is now 60 days"}],
     "answer": {"option_id": "A"}, "points": 1},
    {"item_type": "mcq", "seq": 5, "prompt": "Read the email. What tone does the writer use?",
     "stimulus": "I appreciate the effort your team has put into this project. However, I must express concern about the timeline. The current deadline seems unrealistic given the scope changes we discussed last week. I'd like to schedule a call to discuss potential adjustments.",
     "options": [{"id": "A", "text": "Angry and confrontational"}, {"id": "B", "text": "Professional but firm"}, {"id": "C", "text": "Casual and relaxed"}],
     "answer": {"option_id": "B"}, "points": 1},
]

B2_GRAMMAR = [
    {"item_type": "mcq", "seq": 1, "prompt": "Choose the correct answer: If I _____ more time, I would learn another language.",
     "options": [{"id": "A", "text": "have"}, {"id": "B", "text": "had"}, {"id": "C", "text": "would have"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Choose the correct answer: The report, _____ was submitted yesterday, needs revision.",
     "options": [{"id": "A", "text": "that"}, {"id": "B", "text": "which"}, {"id": "C", "text": "who"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 3, "prompt": "Choose the sentence with correct reported speech.",
     "options": [{"id": "A", "text": "He said that he will come tomorrow."}, {"id": "B", "text": "He said that he would come the next day."}, {"id": "C", "text": "He said that he would come tomorrow."}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 4, "prompt": "Complete with one word.",
     "stimulus": "Despite [BLANK] the deadline, the team delivered high-quality work.",
     "answer": {"blanks": ["missing"], "acceptable_variants": {"0": ["losing", "facing"]}}, "points": 1},
    {"item_type": "mcq", "seq": 5, "prompt": "Choose the correct answer: Neither the manager nor the team _____ available for the meeting.",
     "options": [{"id": "A", "text": "is"}, {"id": "B", "text": "are"}, {"id": "C", "text": "were"}],
     "answer": {"option_id": "A"}, "points": 1},
    {"item_type": "mcq", "seq": 6, "prompt": "Choose the sentence that uses 'although' correctly.",
     "options": [{"id": "A", "text": "Although the weather was bad, but we went out."}, {"id": "B", "text": "Although the weather was bad, we went out."}, {"id": "C", "text": "Although the weather was bad, however we went out."}],
     "answer": {"option_id": "B"}, "points": 1},
]

B2_SPEAKING = [
    {"item_type": "audio_response", "seq": 1, "prompt": "Read this sentence aloud: 'Although the initial results were promising, further research is needed to confirm the findings.'",
     "stimulus": "Although the initial results were promising, further research is needed to confirm the findings.",
     "rubric": {"pronunciation": {"weight": 0.4}, "fluency": {"weight": 0.3}, "accuracy": {"weight": 0.3}}, "points": 10},
    {"item_type": "audio_response", "seq": 2, "prompt": "You are in a meeting. State your position on this topic: 'Should our company adopt a 4-day work week?' Give reasons and an example. (Speak for 45-90 seconds)",
     "rubric": {"content": {"weight": 0.4}, "grammar": {"weight": 0.3}, "fluency": {"weight": 0.3}}, "points": 20},
    {"item_type": "audio_response", "seq": 3, "prompt": "You disagree with a colleague's proposal in a meeting. Express your disagreement politely, give a reason, and suggest an alternative. (Speak for 30-60 seconds)",
     "rubric": {"content": {"weight": 0.4}, "vocabulary": {"weight": 0.3}, "pronunciation": {"weight": 0.3}}, "points": 15},
]

B2_WRITING = [
    {"item_type": "text_response", "seq": 1, "prompt": "Write a professional email reply (50-80 words) to this message:\n\n'We are considering switching to a new software platform. Could you provide your recommendation and reasons?'\n\nState your position, give one reason, and propose a next step.",
     "rubric": {"task_achievement": {"weight": 0.3}, "vocabulary": {"weight": 0.3}, "grammar": {"weight": 0.2}, "organization": {"weight": 0.2}}, "points": 15},
    {"item_type": "text_response", "seq": 2, "prompt": "Write a short summary of a meeting (50-80 words) that covers:\n- The main topic discussed\n- One decision made\n- The next steps",
     "rubric": {"task_achievement": {"weight": 0.3}, "vocabulary": {"weight": 0.3}, "grammar": {"weight": 0.2}, "organization": {"weight": 0.2}}, "points": 15},
]


# ── C1 Items ──────────────────────────────────────────────────────────────

C1_LISTENING = [
    {"item_type": "mcq", "seq": 1, "prompt": "Listen to the discussion. What is the speaker's implied attitude?",
     "stimulus": "Look, I understand the board's concern about short-term profitability. But if we keep prioritizing quarterly numbers over R&D investment, we're essentially mortgaging our future. The competitors who are investing now will dominate the market in three years. We need to think strategically, not just tactically.",
     "options": [{"id": "A", "text": "The speaker supports the board's approach"}, {"id": "B", "text": "The speaker believes the board is being short-sighted"}, {"id": "C", "text": "The speaker is neutral about the decision"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Listen to the presentation. What rhetorical strategy is the speaker using?",
     "stimulus": "When we launched this product three years ago, skeptics said it would never work. Today, it's our fastest-growing revenue stream. Now, I'm not here to say 'I told you so' - I'm here to say: let's double down on what works and apply the same bold thinking to our next challenge.",
     "options": [{"id": "A", "text": "Appealing to authority"}, {"id": "B", "text": "Using past success to build credibility for a new proposal"}, {"id": "C", "text": "Criticizing competitors"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 3, "prompt": "Listen and fill in the blank.",
     "stimulus": "The key takeaway is that we need to [BLANK] between short-term gains and long-term sustainability.",
     "answer": {"blanks": ["balance"], "acceptable_variants": {"0": ["strike a balance", "find a balance"]}}, "points": 1},
    {"item_type": "mcq", "seq": 4, "prompt": "Listen to the interview. What nuance does the speaker express?",
     "stimulus": "I wouldn't say AI will replace developers entirely. What it will do is change the nature of the work. The developers who thrive will be those who can think architecturally and communicate effectively with stakeholders. The coding itself will increasingly be automated, but the problem-solving and design thinking won't be.",
     "options": [{"id": "A", "text": "AI will completely replace developers"}, {"id": "B", "text": "AI will change the nature of development work"}, {"id": "C", "text": "AI will have no impact on developers"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 5, "prompt": "Listen to the debate. How does the second speaker respond to the first speaker's argument?",
     "stimulus": "Speaker 1: Universal basic income is the only way to address automation-driven job losses.\nSpeaker 2: That's an interesting perspective, but I think it oversimplifies the issue. UBI addresses the symptom, not the root cause. What we really need is massive investment in education and reskilling programs to prepare workers for the jobs of tomorrow.",
     "options": [{"id": "A", "text": "By fully agreeing with the first speaker"}, {"id": "B", "text": "By acknowledging the point but offering an alternative view"}, {"id": "C", "text": "By dismissing the argument entirely"}],
     "answer": {"option_id": "B"}, "points": 1},
]

C1_READING = [
    {"item_type": "mcq", "seq": 1, "prompt": "Read the passage. What is the author's tone?",
     "stimulus": "The notion that artificial intelligence will replace all human jobs is, to put it charitably, an oversimplification. While AI will undoubtedly transform the labor market, history shows that technological revolutions tend to create as many opportunities as they eliminate - though the transition can be painful for those caught in the middle.",
     "options": [{"id": "A", "text": "Alarmist and pessimistic"}, {"id": "B", "text": "Cautiously optimistic with nuance"}, {"id": "C", "text": "Enthusiastic and uncritical"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Read the opinion piece. What is the writer's main thesis?",
     "stimulus": "Remote work is not merely a perk - it's a fundamental shift in how we think about productivity. The companies that thrive will be those that redesign their processes around outcomes rather than hours spent at a desk. Measuring presence is easy; measuring impact requires better leadership.",
     "options": [{"id": "A", "text": "Remote work is just a temporary trend"}, {"id": "B", "text": "Companies need to measure outcomes, not presence"}, {"id": "C", "text": "Leadership doesn't matter for remote work"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 3, "prompt": "Read the analysis. What is the author's implied criticism?",
     "stimulus": "The quarterly earnings cycle has created a perverse incentive structure. Executives optimize for short-term stock price at the expense of long-term value creation. Shareholders who think in decades are systematically disadvantaged against those who think in quarters.",
     "options": [{"id": "A", "text": "Executives are generally incompetent"}, {"id": "B", "text": "Short-term thinking undermines long-term value"}, {"id": "C", "text": "Shareholders should not have a voice"}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 4, "prompt": "Read the passage and fill in the blank.",
     "stimulus": "The [BLANK] of this argument is that we must choose between economic growth and environmental protection. In reality, sustainable practices can drive innovation and create new markets.",
     "answer": {"blanks": ["premise"], "acceptable_variants": {"0": ["assumption", "fallacy"]}}, "points": 1},
    {"item_type": "mcq", "seq": 5, "prompt": "Read the essay. What literary device does the author use?",
     "stimulus": "We are told that data is the new oil. But oil, once extracted, is consumed. Data, by contrast, can be used infinitely without depletion. If anything, data is the new sunlight - abundant, renewable, and increasingly central to how we power our world.",
     "options": [{"id": "A", "text": "Hyperbole"}, {"id": "B", "text": "Extended metaphor and analogy"}, {"id": "C", "text": "Irony"}],
     "answer": {"option_id": "B"}, "points": 1},
]

C1_GRAMMAR = [
    {"item_type": "mcq", "seq": 1, "prompt": "Choose the sentence that uses a cleft structure for emphasis.",
     "options": [{"id": "A", "text": "The strategy was what changed the outcome."}, {"id": "B", "text": "It was the strategy that changed the outcome."}, {"id": "C", "text": "The outcome changed because of the strategy."}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 2, "prompt": "Choose the correct inversion: _____ had we started when the problems began.",
     "options": [{"id": "A", "text": "Hardly"}, {"id": "B", "text": "Although"}, {"id": "C", "text": "Despite"}],
     "answer": {"option_id": "A"}, "points": 1},
    {"item_type": "mcq", "seq": 3, "prompt": "Choose the sentence with the most appropriate hedging.",
     "options": [{"id": "A", "text": "This approach will definitely solve all our problems."}, {"id": "B", "text": "This approach could potentially address some of our challenges."}, {"id": "C", "text": "This approach might maybe help a little bit."}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "mcq", "seq": 4, "prompt": "Choose the sentence with correct subjunctive mood.",
     "options": [{"id": "A", "text": "I suggest that he takes the meeting."}, {"id": "B", "text": "I suggest that he take the meeting."}, {"id": "C", "text": "I suggest that he took the meeting."}],
     "answer": {"option_id": "B"}, "points": 1},
    {"item_type": "fill_blank", "seq": 5, "prompt": "Complete with one word.",
     "stimulus": "Not only _____ the project on time, but it also came in under budget.",
     "answer": {"blanks": ["did"], "acceptable_variants": {"0": ["did"]}}, "points": 1},
]

C1_SPEAKING = [
    {"item_type": "audio_response", "seq": 1, "prompt": "Read this sentence aloud: 'It was precisely this misalignment between strategy and execution that ultimately led to the project's failure.'",
     "stimulus": "It was precisely this misalignment between strategy and execution that ultimately led to the project's failure.",
     "rubric": {"pronunciation": {"weight": 0.4}, "fluency": {"weight": 0.3}, "accuracy": {"weight": 0.3}}, "points": 10},
    {"item_type": "audio_response", "seq": 2, "prompt": "You are leading a discussion on this topic: 'Should companies prioritize social responsibility over profit maximization?' Frame the issue, present a balanced view, and steer toward a conclusion. (Speak for 60-120 seconds)",
     "rubric": {"content": {"weight": 0.4}, "grammar": {"weight": 0.3}, "fluency": {"weight": 0.3}}, "points": 25},
    {"item_type": "audio_response", "seq": 3, "prompt": "A client is unhappy with a delayed deliverable. Acknowledge their frustration, explain the situation diplomatically, and propose a concrete solution. (Speak for 45-90 seconds)",
     "rubric": {"content": {"weight": 0.4}, "vocabulary": {"weight": 0.3}, "pronunciation": {"weight": 0.3}}, "points": 15},
]

C1_WRITING = [
    {"item_type": "text_response", "seq": 1, "prompt": "Write a concise, persuasive reply (60-100 words) to this scenario:\n\n'A client wants to cancel a project mid-way due to budget concerns. Write a response that acknowledges their concern, frames the value of continuing, and proposes a strategic compromise.'",
     "rubric": {"task_achievement": {"weight": 0.3}, "vocabulary": {"weight": 0.3}, "grammar": {"weight": 0.2}, "organization": {"weight": 0.2}}, "points": 20},
    {"item_type": "text_response", "seq": 2, "prompt": "Write a strategic recommendation (60-100 words) for your company's leadership team:\n\nTopic: Whether to expand into a new market\nInclude: Your position, one key risk, and a recommended next step.",
     "rubric": {"task_achievement": {"weight": 0.3}, "vocabulary": {"weight": 0.3}, "grammar": {"weight": 0.2}, "organization": {"weight": 0.2}}, "points": 20},
]


LEVEL_ITEMS = {
    "A2": {"LISTENING": A2_LISTENING, "READING": A2_READING, "GRAMMAR_VOCABULARY": A2_GRAMMAR, "SPEAKING": A2_SPEAKING, "WRITING": A2_WRITING},
    "B1": {"LISTENING": B1_LISTENING, "READING": B1_READING, "GRAMMAR_VOCABULARY": B1_GRAMMAR, "SPEAKING": B1_SPEAKING, "WRITING": B1_WRITING},
    "B2": {"LISTENING": B2_LISTENING, "READING": B2_READING, "GRAMMAR_VOCABULARY": B2_GRAMMAR, "SPEAKING": B2_SPEAKING, "WRITING": B2_WRITING},
    "C1": {"LISTENING": C1_LISTENING, "READING": C1_READING, "GRAMMAR_VOCABULARY": C1_GRAMMAR, "SPEAKING": C1_SPEAKING, "WRITING": C1_WRITING},
}


def seed_exam(db: Session, level_code: str) -> ExamTemplateModel:
    config = EXAM_CONFIGS[level_code]
    items_by_section = LEVEL_ITEMS[level_code]

    template = ExamTemplateModel(
        id=generate_id(),
        code=config["code"],
        level_code=level_code,
        title=config["title"],
        description=config["description"],
        duration_minutes=config["duration"],
        passing_score_percent=config["passing"],
        status="active",
        version=1,
        metadata_json={"max_attempts": 3, "cooldown_days": 30},
        created_by="system",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(template)
    print(f"  Template: {template.title}")

    sections = {}
    for sec_data in SECTIONS_TEMPLATE:
        section = ExamSectionModel(
            id=generate_id(),
            exam_template_id=template.id,
            code=sec_data["code"],
            title=sec_data["title"],
            description=f"{sec_data['title']} for {level_code} level",
            sequence_order=sec_data["seq"],
            duration_minutes=sec_data["minutes"],
            score_weight_percent=sec_data["weight"],
            item_types_allowed=sec_data["types"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(section)
        sections[sec_data["code"]] = section

    total_items = 0
    for section_code, section in sections.items():
        items_data = items_by_section.get(section_code, [])
        for item_data in items_data:
            item = ExamItemModel(
                id=generate_id(),
                exam_template_id=template.id,
                section_id=section.id,
                item_type=item_data["item_type"],
                sequence_order=item_data["seq"],
                prompt_text=item_data["prompt"],
                stimulus_text=item_data.get("stimulus"),
                options_json=item_data.get("options"),
                correct_answer=item_data.get("answer"),
                rubric_criteria=item_data.get("rubric"),
                score_points=item_data.get("points", 1),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(item)
            total_items += 1

    print(f"  Sections: {len(sections)}, Items: {total_items}")
    return template


def seed_all():
    print("=" * 60)
    print("Seeding Real Exam Data (A2, B1, B2, C1)")
    print("=" * 60)

    db = get_sessionmaker()()
    try:
        for level_code in ("A2", "B1", "B2", "C1"):
            existing = db.execute(
                select(ExamTemplateModel).where(ExamTemplateModel.code == EXAM_CONFIGS[level_code]["code"])
            ).scalar_one_or_none()
            if existing:
                print(f"\n⚠️  {level_code} exam already exists ({existing.code}). Skipping.")
                continue

            print(f"\n{level_code}:")
            template = seed_exam(db, level_code)
            print(f"  ✅ {level_code} seeded (ID: {template.id[:8]}...)")

        db.commit()
        print("\n" + "=" * 60)
        print("✅ All exams seeded successfully!")
        print("=" * 60)
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
