from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import yaml


def dump_yaml(data: object) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        width=1000,
        default_flow_style=False,
    )


def write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def render_listening_script(*, level_code: str, speakers: tuple[str, str], dialogue: list[tuple[str, str]]) -> str:
    lines = ["# Dialogue Script", ""]
    for speaker, line in dialogue:
        lines.append(f"**{speaker}:** {line}  ")
    lines.extend(
        [
            "",
            "## Audio Direction",
            "",
            f"- Level: {level_code}",
            "- Speed: slow and natural",
            "- Tone: friendly, clear, helpful",
            f"- Voices: {speakers[0]} and {speakers[1]}",
        ]
    )
    return "\n".join(lines)


def render_translation_md(translations: list[tuple[str, str, str]]) -> str:
    lines = ["# Transcript Translation", ""]
    for speaker, en, idn in translations:
        lines.append(f"- **{speaker}:** {en} -> {idn}")
    return "\n".join(lines)


def render_lesson_md(*, title: str, conversation_goal: str, situation_id: str) -> str:
    return dedent(
        f"""\
        # {title}

        ## Conversation Outcome

        After this lesson, learners can {conversation_goal[0].lower() + conversation_goal[1:]}

        ## Situation

        {situation_id}

        ## Lesson Flow

        1. Listen to a short dialogue.
        2. Understand the conversation with Indonesian support.
        3. Practice useful phrases.
        4. Repeat key phrases clearly.
        5. Respond to short prompts.
        6. Practice the same situation with Conversation Coach.
        7. Review conversation feedback.
        """
    )


def render_conversation_goal_md(*, conversation_goal: str, examples: list[str]) -> str:
    lines = [conversation_goal, "", "Learners should be able to say:", ""]
    for ex in examples:
        lines.append(f"- {ex}")
    return "\n".join(lines)


def render_grammar_md(grammar_md: list[tuple[str, list[str]]]) -> str:
    lines = ["# Grammar for Conversation", ""]
    for title, examples in grammar_md:
        lines.append(f"Use **{title}**.")
        lines.append("")
        lines.append("Examples:")
        lines.append("")
        for ex in examples:
            lines.append(f"- {ex}")
        lines.append("")
    return "\n".join(lines).rstrip()


def render_pronunciation_md(pronunciation: list[tuple[str, str]]) -> str:
    lines = ["# Pronunciation Drill", "", "Repeat slowly, then say it in a short answer.", ""]
    for item, note in pronunciation:
        lines.append(f"- **{item}** - {note}")
    return "\n".join(lines)


def render_reading_support_md(text: str) -> str:
    return dedent(
        f"""\
        # Reading Support

        {text}

        ## Check

        Read it again and underline the travel request words (check in, delayed, recommend, problem).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B1"
    b1_root = Path("content/curriculum/english/B1")
    units_root = b1_root / "units"
    unit_key = "unit-04-travel-situations"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-04-travel-situations
            level_code: B1
            title: Travel Situations
            main_conversation_outcome: Handle travel issues, requests, and explanations.
            status: in_production
            lessons:
              - lesson-01-checking-in
              - lesson-02-explaining-a-delay
              - lesson-03-asking-for-recommendations
              - lesson-04-handling-a-simple-complaint
              - lesson-05-travel-situation-mission
            """
        ),
    )

    required_sections = [
        "conversation_goal",
        "situation_setup",
        "listening",
        "comprehension_check",
        "useful_phrases",
        "grammar_for_conversation",
        "speak_clearly",
        "response_practice",
        "conversation_coach_roleplay",
        "conversation_feedback",
        "conversation_check",
    ]

    lessons: list[dict[str, object]] = [
        {
            "lesson_key": "lesson-01-checking-in",
            "slug": "checking-in",
            "title": "Checking In",
            "conversation_situation": "checking_in_at_hotel",
            "conversation_goal": "Check in at a hotel, confirm your reservation, and ask one practical question.",
            "grammar_summary": "Use I'd like to... and I have a reservation under... to check in politely and confirm details.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu baru sampai hotel. Kamu check-in, konfirmasi reservasi, lalu tanya info penting (sarapan / check-out).",
            "dialogue": [
                ("Jordan", "Welcome. How can I help you?"),
                ("Mina", "Hi. I'd like to check in."),
                ("Jordan", "Sure. Do you have a reservation?"),
                ("Mina", "Yes. I have a reservation under Mina Kim."),
                ("Jordan", "Great. Could I see your ID, please?"),
                ("Mina", "Of course. Here you go."),
                ("Jordan", "Thank you. Breakfast is included. Check-out is at 11 a.m."),
                ("Mina", "Perfect. Thanks for your help."),
            ],
            "translations": [
                ("Jordan", "Welcome. How can I help you?", "Selamat datang. Ada yang bisa saya bantu?"),
                ("Mina", "Hi. I'd like to check in.", "Hai. Saya mau check-in."),
                ("Jordan", "Sure. Do you have a reservation?", "Baik. Ada reservasi?"),
                ("Mina", "Yes. I have a reservation under Mina Kim.", "Iya. Saya ada reservasi atas nama Mina Kim."),
                ("Jordan", "Great. Could I see your ID, please?", "Baik. Boleh saya lihat ID-nya?"),
                ("Mina", "Of course. Here you go.", "Tentu. Ini."),
                ("Jordan", "Thank you. Breakfast is included. Check-out is at 11 a.m.", "Makasih. Sarapan sudah termasuk. Check-out jam 11 pagi."),
                ("Mina", "Perfect. Thanks for your help.", "Oke. Makasih ya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'd like to check in.",
                    "meaning_id": "Saya mau check-in.",
                    "usage_note": "A polite way to start at a hotel front desk.",
                    "common_mistake": 'Do not say "I want check in" in a formal situation; use I\'d like to.',
                },
                {
                    "phrase": "Do you have a reservation?",
                    "meaning_id": "Ada reservasi?",
                    "usage_note": "A standard check-in question.",
                    "common_mistake": 'Do not say "You have reservation?" without do.',
                },
                {
                    "phrase": "I have a reservation under Mina Kim.",
                    "meaning_id": "Saya ada reservasi atas nama Mina Kim.",
                    "usage_note": "Under + name means the booking name.",
                    "common_mistake": 'Do not say "in the name"; use under + name.',
                },
                {
                    "phrase": "Could I see your ID, please?",
                    "meaning_id": "Boleh saya lihat ID-nya?",
                    "usage_note": "A polite request from staff.",
                    "common_mistake": 'Do not drop please in formal service situations.',
                },
                {
                    "phrase": "Breakfast is included.",
                    "meaning_id": "Sarapan sudah termasuk.",
                    "usage_note": "Included means it is part of the price.",
                    "common_mistake": 'Do not say "Breakfast include"; add -d.',
                },
            ],
            "grammar_md": [
                ("I'd like to + verb", ["I'd like to check in.", "I'd like to ask a question."]),
                ("Reservation under + name", ["I have a reservation under Mina Kim.", "It's under Alex Chen."]),
            ],
            "pronunciation": [
                ("reservation", "rez-er-VAY-shun."),
                ("check in", "CHECK in."),
                ("included", "in-KLOO-did."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start check-in politely.",
                    "target_response": "I'd like to check in.",
                    "acceptable_variations": ["I'd like to check in.", "Hi, I'd like to check in."],
                },
                {
                    "prompt": "Say you have a reservation under your name.",
                    "target_response": "I have a reservation under Mina Kim.",
                    "acceptable_variations": ["I have a reservation under Mina Kim.", "I have a reservation under Alex Chen."],
                },
                {
                    "prompt": "Ask one practical question (check-out time).",
                    "target_response": "What time is check-out?",
                    "acceptable_variations": ["What time is check-out?", "Is breakfast included?"],
                },
            ],
            "quiz": [
                {
                    "key": "check_in_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a polite check-in starter?",
                    "options": ["I'd like to check in.", "I check in now.", "Check in me."],
                    "correct_answer": "I'd like to check in.",
                },
                {
                    "key": "under_name",
                    "type": "multiple_choice",
                    "prompt": 'What does "under Mina Kim" mean?',
                    "options": ["atas nama Mina Kim", "di bawah meja", "di dalam tas"],
                    "correct_answer": "atas nama Mina Kim",
                },
                {
                    "key": "included_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "included" mean?',
                    "options": ["sudah termasuk", "ditunda", "dilarang"],
                    "correct_answer": "sudah termasuk",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_travel_check_in",
                "opening_line": "Welcome. How can I help you?",
                "learner_goal": "Check in, give the reservation name, and ask one practical question.",
                "turns": [
                    {
                        "coach": "Welcome. How can I help you?",
                        "hint": "Mulai dengan: I'd like to check in.",
                        "sample_answer": "Hi. I'd like to check in.",
                        "focus": "Start check-in",
                        "expected_keywords": ["check in"],
                    },
                    {
                        "coach": "Sure. Do you have a reservation?",
                        "hint": "Jawab dengan under + name.",
                        "sample_answer": "Yes. I have a reservation under Mina Kim.",
                        "focus": "Confirm reservation name",
                        "expected_keywords": ["reservation", "under"],
                    },
                    {
                        "coach": "Great. Any questions about your stay?",
                        "hint": "Tanya 1 hal (check-out / breakfast).",
                        "sample_answer": "Yes. What time is check-out?",
                        "focus": "Ask a practical question",
                        "expected_keywords": ["what time", "check-out"],
                    },
                ],
                "target_phrases": ["I'd like to check in.", "I have a reservation under ...", "What time is check-out?"],
            },
            "reading_support": "In hotel check-in conversations, keep it simple: greet, say you'd like to check in, give the reservation name, and ask one practical question.",
            "writing_support_lines": [
                "Write 4 sentences:",
                "1. Hi. I'd like to check in.",
                "2. I have a reservation under ...",
                "3. Could I ask a question?",
                "4. What time is check-out?",
            ],
            "goal_examples": ["I'd like to check in.", "I have a reservation under ...", "What time is check-out?"],
        },
        {
            "lesson_key": "lesson-02-explaining-a-delay",
            "slug": "explaining-a-delay",
            "title": "Explaining a Delay",
            "conversation_situation": "explaining_travel_delay",
            "conversation_goal": "Explain that you are delayed, give an updated arrival time, and ask to adjust the plan.",
            "grammar_summary": "Use I'm running a bit late / ... is delayed / I'll be there in ... to explain delays clearly.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu telat karena transport delay. Kamu kasih kabar, sebut estimasi, dan minta mulai sedikit lebih lambat.",
            "dialogue": [
                ("Jordan", "Hi Mina. Are you on your way?"),
                ("Mina", "Yes, but I'm running a bit late."),
                ("Jordan", "Oh no. What happened?"),
                ("Mina", "My train is delayed because of a signal problem."),
                ("Jordan", "Okay. When will you arrive?"),
                ("Mina", "I'll be there in about 20 minutes."),
                ("Jordan", "No problem. We can start a little later."),
                ("Mina", "Thank you for waiting."),
            ],
            "translations": [
                ("Jordan", "Hi Mina. Are you on your way?", "Hai Mina. Kamu lagi di jalan?"),
                ("Mina", "Yes, but I'm running a bit late.", "Iya, tapi aku agak telat."),
                ("Jordan", "Oh no. What happened?", "Waduh. Kenapa?"),
                ("Mina", "My train is delayed because of a signal problem.", "Kereta aku delay karena masalah sinyal."),
                ("Jordan", "Okay. When will you arrive?", "Oke. Kamu sampai jam berapa?"),
                ("Mina", "I'll be there in about 20 minutes.", "Aku sampai kira-kira 20 menit lagi."),
                ("Jordan", "No problem. We can start a little later.", "Nggak apa-apa. Kita bisa mulai agak telat sedikit."),
                ("Mina", "Thank you for waiting.", "Makasih sudah nungguin ya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'm running a bit late.",
                    "meaning_id": "Aku agak telat.",
                    "usage_note": "A natural way to say you're late.",
                    "common_mistake": 'Do not say "I am late running"; use I\'m running late.',
                },
                {
                    "phrase": "My train is delayed.",
                    "meaning_id": "Kereta aku delay.",
                    "usage_note": "A clear reason for delay.",
                    "common_mistake": 'Do not say "My train delay" without is.',
                },
                {
                    "phrase": "I'll be there in about 20 minutes.",
                    "meaning_id": "Aku sampai kira-kira 20 menit lagi.",
                    "usage_note": "In about + time gives an estimate.",
                    "common_mistake": 'Do not say "in 20 minutes more"; just in 20 minutes.',
                },
                {
                    "phrase": "Can we start a little later?",
                    "meaning_id": "Bisa mulai agak telat sedikit?",
                    "usage_note": "A polite request to adjust timing.",
                    "common_mistake": 'Do not say "Can start later?" without we.',
                },
                {
                    "phrase": "Thank you for waiting.",
                    "meaning_id": "Makasih sudah nungguin ya.",
                    "usage_note": "A polite closing after being late.",
                    "common_mistake": 'Do not say "Thanks for wait".',
                },
            ],
            "grammar_md": [
                ("Running late", ["I'm running a bit late.", "Sorry, I'm running late."]),
                ("In about + time", ["I'll be there in about 20 minutes.", "I'll arrive in about an hour."]),
            ],
            "pronunciation": [
                ("delayed", "di-LAYD."),
                ("running late", "RUN-ning late."),
                ("about", "uh-BOUT."),
            ],
            "response_prompts": [
                {
                    "prompt": "Say you're running a bit late.",
                    "target_response": "I'm running a bit late.",
                    "acceptable_variations": ["I'm running a bit late.", "Sorry, I'm running late."],
                },
                {
                    "prompt": "Give the reason (train delayed).",
                    "target_response": "My train is delayed.",
                    "acceptable_variations": ["My train is delayed.", "My flight is delayed."],
                },
                {
                    "prompt": "Give an estimate (about 20 minutes).",
                    "target_response": "I'll be there in about 20 minutes.",
                    "acceptable_variations": ["I'll be there in about 20 minutes.", "I'll be there in about 10 minutes."],
                },
            ],
            "quiz": [
                {
                    "key": "running_late_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "running late" mean?',
                    "options": ["telat", "lebih cepat", "sedang liburan"],
                    "correct_answer": "telat",
                },
                {
                    "key": "delayed_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "delayed" mean?',
                    "options": ["tertunda", "termasuk", "terkunci"],
                    "correct_answer": "tertunda",
                },
                {
                    "key": "in_about_usage",
                    "type": "multiple_choice",
                    "prompt": "Which sentence gives an estimate?",
                    "options": ["I'll be there in about 20 minutes.", "I'm there now.", "I was there yesterday."],
                    "correct_answer": "I'll be there in about 20 minutes.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_travel_delay",
                "opening_line": "Hi. Are you on your way?",
                "learner_goal": "Explain you're late, give a reason, and share an estimated arrival time.",
                "turns": [
                    {
                        "coach": "Hi. Are you on your way?",
                        "hint": "Jawab + bilang kamu telat.",
                        "sample_answer": "Yes, but I'm running a bit late.",
                        "focus": "State you are late",
                        "expected_keywords": ["running", "late"],
                    },
                    {
                        "coach": "What happened?",
                        "hint": "Sebutkan transport kamu delayed.",
                        "sample_answer": "My train is delayed because of a signal problem.",
                        "focus": "Give a reason",
                        "expected_keywords": ["delayed", "because"],
                    },
                    {
                        "coach": "When will you arrive?",
                        "hint": "Kasih estimasi in about + time.",
                        "sample_answer": "I'll be there in about 20 minutes.",
                        "focus": "Give an estimate",
                        "expected_keywords": ["in about", "minutes"],
                    },
                ],
                "target_phrases": ["I'm running a bit late.", "My ... is delayed.", "I'll be there in about ... minutes."],
            },
            "reading_support": "When you are delayed while traveling, keep the message short: say you're running late, give one reason, and share an estimated arrival time.",
            "writing_support_lines": [
                "Write 4 lines:",
                "1. Hi, I'm running a bit late.",
                "2. My train/flight is delayed.",
                "3. I'll be there in about ... minutes.",
                "4. Thank you for waiting.",
            ],
            "goal_examples": ["I'm running a bit late.", "My train is delayed.", "I'll be there in about ... minutes."],
        },
        {
            "lesson_key": "lesson-03-asking-for-recommendations",
            "slug": "asking-for-recommendations",
            "title": "Asking for Recommendations",
            "conversation_situation": "asking_for_travel_recommendations",
            "conversation_goal": "Ask for recommendations, describe what you want, and ask one follow-up question.",
            "grammar_summary": "Use Do you have any recommendations for...? and I'm looking for... to ask politely and clearly.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu tanya rekomendasi tempat makan. Kamu jelaskan yang kamu cari, lalu tanya jarak atau cara pergi.",
            "dialogue": [
                ("Mina", "Hi. Do you have any recommendations for dinner?"),
                ("Jordan", "Sure. Are you looking for something local?"),
                ("Mina", "Yes. Something local would be great."),
                ("Jordan", "I recommend Sate House. It's nearby and popular."),
                ("Mina", "Sounds good. Is it far from here?"),
                ("Jordan", "Not at all. It's a 10-minute walk."),
                ("Mina", "Great. How do I get there?"),
                ("Jordan", "Go straight and turn left at the second corner."),
            ],
            "translations": [
                ("Mina", "Hi. Do you have any recommendations for dinner?", "Hai. Ada rekomendasi buat makan malam?"),
                ("Jordan", "Sure. Are you looking for something local?", "Ada. Kamu cari yang lokal?"),
                ("Mina", "Yes. Something local would be great.", "Iya. Yang lokal bakal bagus."),
                ("Jordan", "I recommend Sate House. It's nearby and popular.", "Aku rekomendasiin Sate House. Dekat dan populer."),
                ("Mina", "Sounds good. Is it far from here?", "Oke. Jauh nggak dari sini?"),
                ("Jordan", "Not at all. It's a 10-minute walk.", "Nggak jauh. Jalan kaki 10 menit."),
                ("Mina", "Great. How do I get there?", "Oke. Cara ke sana gimana?"),
                ("Jordan", "Go straight and turn left at the second corner.", "Jalan terus lalu belok kiri di tikungan kedua."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Do you have any recommendations for dinner?",
                    "meaning_id": "Ada rekomendasi buat makan malam?",
                    "usage_note": "A polite way to ask for ideas.",
                    "common_mistake": 'Do not say "Give me recommendation"; ask Do you have any recommendations...?',
                },
                {
                    "phrase": "I'm looking for something local.",
                    "meaning_id": "Aku lagi cari yang lokal.",
                    "usage_note": "Looking for explains what you want.",
                    "common_mistake": 'Do not say "I search" for this meaning; use I\'m looking for.',
                },
                {
                    "phrase": "Something local would be great.",
                    "meaning_id": "Yang lokal bakal bagus.",
                    "usage_note": "Would be great sounds friendly and polite.",
                    "common_mistake": 'Do not say "will be great" if you want softer tone; use would.',
                },
                {
                    "phrase": "Is it far from here?",
                    "meaning_id": "Jauh nggak dari sini?",
                    "usage_note": "A simple follow-up question about distance.",
                    "common_mistake": 'Do not say "Is far?" without it.',
                },
                {
                    "phrase": "How do I get there?",
                    "meaning_id": "Cara ke sana gimana?",
                    "usage_note": "Ask for directions after a recommendation.",
                    "common_mistake": 'Do not say "How to go there?" in a full question; use How do I get there?',
                },
            ],
            "grammar_md": [
                ("Do you have any recommendations for...?", ["Do you have any recommendations for dinner?", "Do you have any recommendations for a museum?"]),
                ("I'm looking for...", ["I'm looking for something local.", "I'm looking for a quiet cafe."]),
            ],
            "pronunciation": [
                ("recommendations", "rek-uh-men-DAY-shunz."),
                ("local", "LOH-kul."),
                ("nearby", "NEER-bye."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask for recommendations (dinner).",
                    "target_response": "Do you have any recommendations for dinner?",
                    "acceptable_variations": [
                        "Do you have any recommendations for dinner?",
                        "Do you have any recommendations for lunch?",
                    ],
                },
                {
                    "prompt": "Say you're looking for something local.",
                    "target_response": "I'm looking for something local.",
                    "acceptable_variations": ["I'm looking for something local.", "I'm looking for a local restaurant."],
                },
                {
                    "prompt": "Ask one follow-up question (distance).",
                    "target_response": "Is it far from here?",
                    "acceptable_variations": ["Is it far from here?", "How do I get there?"],
                },
            ],
            "quiz": [
                {
                    "key": "recommendations_usage",
                    "type": "multiple_choice",
                    "prompt": "Which sentence asks for recommendations politely?",
                    "options": [
                        "Do you have any recommendations for dinner?",
                        "Recommendation dinner now.",
                        "Give me restaurant.",
                    ],
                    "correct_answer": "Do you have any recommendations for dinner?",
                },
                {
                    "key": "looking_for_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "I\'m looking for" mean?',
                    "options": ["aku lagi cari", "aku sudah punya", "aku tidak suka"],
                    "correct_answer": "aku lagi cari",
                },
                {
                    "key": "far_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "far" mean?',
                    "options": ["jauh", "dekat", "mahal"],
                    "correct_answer": "jauh",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_travel_recommendations",
                "opening_line": "Hi. How can I help you today?",
                "learner_goal": "Ask for a recommendation, say what you want, and ask one follow-up question.",
                "turns": [
                    {
                        "coach": "Hi. How can I help you today?",
                        "hint": "Tanya rekomendasi buat dinner.",
                        "sample_answer": "Do you have any recommendations for dinner?",
                        "focus": "Ask for recommendations",
                        "expected_keywords": ["recommendations"],
                    },
                    {
                        "coach": "Sure. What kind of place are you looking for?",
                        "hint": "Jelaskan yang kamu cari (local / quiet / cheap).",
                        "sample_answer": "I'm looking for something local. Something local would be great.",
                        "focus": "Describe what you want",
                        "expected_keywords": ["looking for", "local"],
                    },
                    {
                        "coach": "I recommend a place nearby. Any questions?",
                        "hint": "Tanya jarak atau cara pergi.",
                        "sample_answer": "Great. Is it far from here?",
                        "focus": "Ask a follow-up question",
                        "expected_keywords": ["far", "here"],
                    },
                ],
                "target_phrases": ["Do you have any recommendations for ...?", "I'm looking for ...", "Is it far from here?"],
            },
            "reading_support": "When asking for recommendations, start with a polite question, describe what you want, and then ask a short follow-up (distance or directions).",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. Hi. Do you have any recommendations for ...?",
                "2. I'm looking for ...",
                "3. Something ... would be great.",
                "4. Is it far from here?",
                "5. Thanks!",
            ],
            "goal_examples": ["Do you have any recommendations for ...?", "I'm looking for ...", "How do I get there?"],
        },
        {
            "lesson_key": "lesson-04-handling-a-simple-complaint",
            "slug": "handling-a-simple-complaint",
            "title": "Handling a Simple Complaint",
            "conversation_situation": "handling_hotel_complaint",
            "conversation_goal": "Explain a simple problem politely and ask for help or an alternative.",
            "grammar_summary": "Use There's a problem with... and Could you... / Could I... to complain politely and request help.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu punya masalah kecil di hotel. Kamu jelaskan masalahnya, lalu minta bantuan atau ganti kamar.",
            "dialogue": [
                ("Mina", "Hi. There's a problem with my room."),
                ("Jordan", "I'm sorry to hear that. What's wrong?"),
                ("Mina", "The air conditioning isn't working."),
                ("Jordan", "Okay. Could you tell me your room number?"),
                ("Mina", "It's room 508."),
                ("Jordan", "Thanks. We can send someone to take a look."),
                ("Mina", "Could I change rooms if it can't be fixed?"),
                ("Jordan", "Yes, of course. We'll help you."),
            ],
            "translations": [
                ("Mina", "Hi. There's a problem with my room.", "Hai. Ada masalah dengan kamar saya."),
                ("Jordan", "I'm sorry to hear that. What's wrong?", "Maaf ya. Masalahnya apa?"),
                ("Mina", "The air conditioning isn't working.", "AC-nya nggak berfungsi."),
                ("Jordan", "Okay. Could you tell me your room number?", "Oke. Boleh sebutin nomor kamarnya?"),
                ("Mina", "It's room 508.", "Kamar 508."),
                ("Jordan", "Thanks. We can send someone to take a look.", "Makasih. Kami bisa kirim orang untuk cek."),
                ("Mina", "Could I change rooms if it can't be fixed?", "Bisa ganti kamar kalau nggak bisa diperbaiki?"),
                ("Jordan", "Yes, of course. We'll help you.", "Bisa. Tentu. Kami bantu."),
            ],
            "useful_phrases": [
                {
                    "phrase": "There's a problem with my room.",
                    "meaning_id": "Ada masalah dengan kamar saya.",
                    "usage_note": "A polite way to start a complaint.",
                    "common_mistake": 'Do not say "I have problem"; use There\'s a problem with...',
                },
                {
                    "phrase": "The air conditioning isn't working.",
                    "meaning_id": "AC-nya nggak berfungsi.",
                    "usage_note": "Explain the problem clearly.",
                    "common_mistake": 'Do not say "isn\'t work"; use isn\'t working.',
                },
                {
                    "phrase": "Could you send someone to take a look?",
                    "meaning_id": "Bisa kirim orang untuk cek?",
                    "usage_note": "A polite request for help.",
                    "common_mistake": 'Do not say "Send person" without someone.',
                },
                {
                    "phrase": "Could I change rooms?",
                    "meaning_id": "Bisa ganti kamar?",
                    "usage_note": "Ask for an alternative option.",
                    "common_mistake": 'Do not say "Can change room?" without I/we.',
                },
                {
                    "phrase": "Thank you for your help.",
                    "meaning_id": "Terima kasih bantuannya.",
                    "usage_note": "Close politely after the request.",
                    "common_mistake": 'Do not say "Thanks for help you".',
                },
            ],
            "grammar_md": [
                ("There's a problem with...", ["There's a problem with my room.", "There's a problem with the key card."]),
                ("Could you... / Could I...?", ["Could you send someone to take a look?", "Could I change rooms?"]),
            ],
            "pronunciation": [
                ("air conditioning", "AIR kun-DISH-uh-ning."),
                ("isn't working", "IZ-nt WUR-king."),
                ("change rooms", "CHAYNJ rooms."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start a polite complaint.",
                    "target_response": "There's a problem with my room.",
                    "acceptable_variations": ["There's a problem with my room.", "There's a problem with the key card."],
                },
                {
                    "prompt": "Explain what's wrong (AC isn't working).",
                    "target_response": "The air conditioning isn't working.",
                    "acceptable_variations": ["The air conditioning isn't working.", "The hot water isn't working."],
                },
                {
                    "prompt": "Ask for help politely (send someone).",
                    "target_response": "Could you send someone to take a look?",
                    "acceptable_variations": [
                        "Could you send someone to take a look?",
                        "Could you help me with it?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "complaint_starter",
                    "type": "multiple_choice",
                    "prompt": "Which sentence starts a polite complaint?",
                    "options": ["There's a problem with my room.", "My room bad!", "Problem room!"],
                    "correct_answer": "There's a problem with my room.",
                },
                {
                    "key": "isnt_working",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["It isn't working.", "It isn't work.", "It not working."],
                    "correct_answer": "It isn't working.",
                },
                {
                    "key": "could_request",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a polite request?",
                    "options": ["Could you send someone to take a look?", "Send someone now.", "Look it."],
                    "correct_answer": "Could you send someone to take a look?",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_travel_complaint",
                "opening_line": "Hi. How can I help you?",
                "learner_goal": "Describe the problem in your room and ask for help or a room change politely.",
                "turns": [
                    {
                        "coach": "Hi. How can I help you?",
                        "hint": "Mulai dengan: There's a problem with ...",
                        "sample_answer": "Hi. There's a problem with my room.",
                        "focus": "Start complaint politely",
                        "expected_keywords": ["problem", "room"],
                    },
                    {
                        "coach": "I'm sorry to hear that. What's wrong?",
                        "hint": "Jelaskan masalahnya (isn't working).",
                        "sample_answer": "The air conditioning isn't working.",
                        "focus": "Explain the issue",
                        "expected_keywords": ["isn't working"],
                    },
                    {
                        "coach": "Okay. What would you like us to do?",
                        "hint": "Minta bantuan (Could you...) atau opsi (Could I...).",
                        "sample_answer": "Could you send someone to take a look? Could I change rooms if it can't be fixed?",
                        "focus": "Request help or alternative",
                        "expected_keywords": ["could", "send", "change"],
                    },
                ],
                "target_phrases": ["There's a problem with ...", "The ... isn't working.", "Could you... / Could I...?"],
            },
            "reading_support": "When complaining while traveling, be polite and clear. Say the problem, ask for help, and ask about alternatives if needed.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. Hi. There's a problem with my room.",
                "2. The ... isn't working.",
                "3. Could you send someone to take a look?",
                "4. Could I change rooms if needed?",
                "5. Thank you for your help.",
            ],
            "goal_examples": ["There's a problem with ...", "The ... isn't working.", "Could you send someone to take a look?"],
        },
        {
            "lesson_key": "lesson-05-travel-situation-mission",
            "slug": "travel-situation-mission",
            "title": "Travel Situation Mission",
            "conversation_situation": "mission_travel_delay_check_in_and_help",
            "conversation_goal": "Complete a travel mini-conversation: explain a delay, check in, ask for a recommendation, and request help with a small issue.",
            "grammar_summary": "Combine travel patterns: I'm running late..., I'd like to check in..., Do you have any recommendations...?, Could you...?",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Misi: kamu telat sampai hotel, check-in, minta rekomendasi makan, lalu minta bantuan untuk masalah kecil di kamar.",
            "dialogue": [
                ("Jordan", "Hi Mina. Are you on your way to the hotel?"),
                ("Mina", "Yes, but I'm running a bit late. My train is delayed."),
                ("Jordan", "No worries. When will you arrive?"),
                ("Mina", "I'll be there in about 20 minutes."),
                ("Jordan", "Okay. When you arrive, we'll check you in."),
                ("Mina", "Thanks. I have a reservation under Mina Kim."),
                ("Jordan", "Great. Also, do you need anything else?"),
                ("Mina", "Yes. Do you have any recommendations for dinner? And if there's a problem with my room, could you help me?"),
            ],
            "translations": [
                ("Jordan", "Hi Mina. Are you on your way to the hotel?", "Hai Mina. Kamu lagi di jalan ke hotel?"),
                ("Mina", "Yes, but I'm running a bit late. My train is delayed.", "Iya, tapi aku agak telat. Kereta aku delay."),
                ("Jordan", "No worries. When will you arrive?", "Nggak apa-apa. Kamu sampai kapan?"),
                ("Mina", "I'll be there in about 20 minutes.", "Aku sampai kira-kira 20 menit lagi."),
                ("Jordan", "Okay. When you arrive, we'll check you in.", "Oke. Kalau sudah sampai, kita check-in-kan kamu."),
                ("Mina", "Thanks. I have a reservation under Mina Kim.", "Makasih. Aku ada reservasi atas nama Mina Kim."),
                ("Jordan", "Great. Also, do you need anything else?", "Oke. Ada yang kamu butuh lagi?"),
                ("Mina", "Yes. Do you have any recommendations for dinner? And if there's a problem with my room, could you help me?", "Iya. Ada rekomendasi makan malam? Dan kalau ada masalah di kamar, bisa dibantu?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'm running a bit late. My train is delayed.",
                    "meaning_id": "Aku agak telat. Kereta aku delay.",
                    "usage_note": "A short delay explanation.",
                    "common_mistake": "Do not over-explain; keep it short and clear.",
                },
                {
                    "phrase": "I'll be there in about 20 minutes.",
                    "meaning_id": "Aku sampai kira-kira 20 menit lagi.",
                    "usage_note": "A simple estimate.",
                    "common_mistake": 'Do not say "I will there"; use I\'ll be there.',
                },
                {
                    "phrase": "I have a reservation under Mina Kim.",
                    "meaning_id": "Aku ada reservasi atas nama Mina Kim.",
                    "usage_note": "Confirm your booking name.",
                    "common_mistake": 'Do not say "reservation name Mina"; use under + name.',
                },
                {
                    "phrase": "Do you have any recommendations for dinner?",
                    "meaning_id": "Ada rekomendasi buat makan malam?",
                    "usage_note": "Ask for ideas politely.",
                    "common_mistake": "Do not demand; ask politely with do you have any.",
                },
                {
                    "phrase": "If there's a problem with my room, could you help me?",
                    "meaning_id": "Kalau ada masalah di kamar, bisa dibantu?",
                    "usage_note": "A polite conditional request.",
                    "common_mistake": 'Do not say "If have problem"; use If there\'s a problem...',
                },
            ],
            "grammar_md": [
                ("Combine delay + check-in + request", ["I'm running a bit late. My train is delayed.", "I have a reservation under ...", "Do you have any recommendations for ...?", "Could you help me?"]),
            ],
            "pronunciation": [
                ("no worries", "no WUR-reez."),
                ("recommendations", "rek-uh-men-DAY-shunz."),
                ("could you", "KUD-yuh (link it)."),
            ],
            "response_prompts": [
                {
                    "prompt": "Explain delay + estimate.",
                    "target_response": "I'm running a bit late. My train is delayed. I'll be there in about 20 minutes.",
                    "acceptable_variations": [
                        "I'm running a bit late. My train is delayed. I'll be there in about 20 minutes.",
                        "I'm running a bit late. My flight is delayed. I'll be there in about 30 minutes.",
                    ],
                },
                {
                    "prompt": "Confirm reservation name.",
                    "target_response": "I have a reservation under Mina Kim.",
                    "acceptable_variations": ["I have a reservation under Mina Kim.", "I have a reservation under Alex Chen."],
                },
                {
                    "prompt": "Ask for recommendation + request help politely.",
                    "target_response": "Do you have any recommendations for dinner? If there's a problem with my room, could you help me?",
                    "acceptable_variations": [
                        "Do you have any recommendations for dinner? If there's a problem with my room, could you help me?",
                        "Do you have any recommendations for lunch? If there's a problem with my room, could you help me?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "mission_skills",
                    "type": "multiple_choice",
                    "prompt": "Which skills are combined in this mission?",
                    "options": [
                        "Delay explanation + check-in + recommendation + help request",
                        "Weather report + math",
                        "Job interview only",
                    ],
                    "correct_answer": "Delay explanation + check-in + recommendation + help request",
                },
                {
                    "key": "no_worries_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "No worries" mean?',
                    "options": ["nggak apa-apa", "hati-hati", "jangan lupa"],
                    "correct_answer": "nggak apa-apa",
                },
                {
                    "key": "conditional_if",
                    "type": "multiple_choice",
                    "prompt": 'What does "If there\'s a problem" express?',
                    "options": ["kondisi/kalau", "masa lalu", "perintah"],
                    "correct_answer": "kondisi/kalau",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_travel_mission",
                "opening_line": "Hi. Are you on your way to the hotel?",
                "learner_goal": "Explain the delay, confirm reservation, ask for a recommendation, and request help politely.",
                "turns": [
                    {
                        "coach": "Hi. Are you on your way to the hotel?",
                        "hint": "Jelaskan kamu telat + alasan + estimasi.",
                        "sample_answer": "Yes, but I'm running a bit late. My train is delayed. I'll be there in about 20 minutes.",
                        "focus": "Delay explanation with estimate",
                        "expected_keywords": ["running", "delayed", "in about"],
                    },
                    {
                        "coach": "Okay. Do you have a reservation?",
                        "hint": "Jawab dengan under + name.",
                        "sample_answer": "Yes. I have a reservation under Mina Kim.",
                        "focus": "Confirm reservation",
                        "expected_keywords": ["reservation", "under"],
                    },
                    {
                        "coach": "Great. Anything else you need?",
                        "hint": "Tanya rekomendasi + minta bantuan dengan could you.",
                        "sample_answer": "Do you have any recommendations for dinner? If there's a problem with my room, could you help me?",
                        "focus": "Ask recommendations and request help",
                        "expected_keywords": ["recommendations", "could you", "problem"],
                    },
                ],
                "target_phrases": ["I'm running a bit late.", "I have a reservation under ...", "Do you have any recommendations for ...?"],
            },
            "reading_support": "This mission practices real travel communication: delay messages, hotel check-in phrases, asking for recommendations, and polite requests for help.",
            "writing_support_lines": [
                "Write your mission (6 lines):",
                "1. I'm running a bit late. My ... is delayed.",
                "2. I'll be there in about ... minutes.",
                "3. I'd like to check in.",
                "4. I have a reservation under ...",
                "5. Do you have any recommendations for ...?",
                "6. If there's a problem with my room, could you help me?",
            ],
            "goal_examples": ["I'm running a bit late.", "I have a reservation under ...", "Could you help me?"],
        },
    ]

    for lesson in lessons:
        lesson_dir = unit_dir / str(lesson["lesson_key"])
        lesson_dir.mkdir(parents=True, exist_ok=False)

        lesson_yaml = {
            "lesson_key": lesson["lesson_key"],
            "slug": lesson["slug"],
            "title": lesson["title"],
            "status": "published",
            "estimated_minutes": 12,
            "conversation_situation": lesson["conversation_situation"],
            "conversation_goal": lesson["conversation_goal"],
            "grammar_summary": lesson["grammar_summary"],
            "required_sections": required_sections,
            "completion_rules": {
                "listening_completed": True,
                "quiz_required": True,
                "speaking_attempt_required": True,
                "minimum_score": 70,
            },
        }
        (lesson_dir / "lesson.yaml").write_text(dump_yaml(lesson_yaml), encoding="utf-8")

        write_text(
            lesson_dir / "lesson.md",
            render_lesson_md(
                title=str(lesson["title"]),
                conversation_goal=str(lesson["conversation_goal"]),
                situation_id=str(lesson["situation_id"]),
            ),
        )
        write_text(
            lesson_dir / "conversation_goal.md",
            render_conversation_goal_md(
                conversation_goal=str(lesson["conversation_goal"]),
                examples=list(lesson["goal_examples"]),
            ),
        )

        speakers = tuple(lesson["speakers"])
        write_text(
            lesson_dir / "listening_script.md",
            render_listening_script(level_code=level_code, speakers=speakers, dialogue=list(lesson["dialogue"])),
        )
        write_text(lesson_dir / "transcript_translation.md", render_translation_md(list(lesson["translations"])))

        (lesson_dir / "useful_phrases.yaml").write_text(dump_yaml({"phrases": list(lesson["useful_phrases"])}), encoding="utf-8")
        write_text(lesson_dir / "grammar_for_conversation.md", render_grammar_md(list(lesson["grammar_md"])))
        write_text(lesson_dir / "pronunciation_drill.md", render_pronunciation_md(list(lesson["pronunciation"])))
        (lesson_dir / "response_prompts.yaml").write_text(dump_yaml({"prompts": list(lesson["response_prompts"])}), encoding="utf-8")
        (lesson_dir / "quiz.yaml").write_text(dump_yaml({"questions": list(lesson["quiz"])}), encoding="utf-8")
        write_text(lesson_dir / "reading_support.md", render_reading_support_md(str(lesson["reading_support"])))
        write_text(lesson_dir / "writing_support.md", render_writing_support_md(list(lesson["writing_support_lines"])))

        roleplay = dict(lesson["roleplay"])
        roleplay_payload = {
            "scenario_key": roleplay["scenario_key"],
            "mode": "lesson_practice_coach",
            "level_code": level_code,
            "opening_line": roleplay["opening_line"],
            "learner_goal": roleplay["learner_goal"],
            "max_turns": 12,
            "feedback_level": {"free": "basic", "pro": "detailed"},
            "turns": roleplay["turns"],
            "target_phrases": roleplay["target_phrases"],
            "rubric": {
                "speaking": {"minimum_score": 70},
                "relevance": {"minimum_score": 70},
                "grammar": {"minimum_score": 65},
            },
        }
        (lesson_dir / "conversation_coach_roleplay.yaml").write_text(dump_yaml(roleplay_payload), encoding="utf-8")

        audio_manifest = {
            "lesson_key": lesson["lesson_key"],
            "status": "not_generated",
            "provider": "minimax",
            "model": "speech-2.8-hd",
            "default_voice_id": "multi_speaker",
            "assets": [
                {
                    "key": "dialogue_main",
                    "type": "dialogue",
                    "script_file": "listening_script.md",
                    "audio_url": None,
                    "duration_seconds": None,
                    "provider": "minimax",
                    "model": "speech-2.8-hd",
                    "voice_id": "multi_speaker",
                    "speaker_voices": {speakers[0]: "English_Upbeat_Woman", speakers[1]: "English_Upbeat_Woman"},
                },
                {
                    "key": "phrases",
                    "type": "phrase_pronunciation",
                    "source_file": "useful_phrases.yaml",
                    "audio_url": None,
                    "duration_seconds": None,
                },
            ],
        }
        (lesson_dir / "audio_manifest.yaml").write_text(dump_yaml(audio_manifest), encoding="utf-8")

    print("Created:", unit_dir)
    print("Lessons:", ", ".join([str(l["lesson_key"]) for l in lessons]))


if __name__ == "__main__":
    main()

