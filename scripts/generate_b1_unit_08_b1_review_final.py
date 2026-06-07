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
            "- Tone: friendly, clear, supportive",
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

        Read it again and underline the review words (story, progress, problem, option, agree, next step).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B1"
    b1_root = Path("content/curriculum/english/B1")
    units_root = b1_root / "units"
    unit_key = "unit-08-b1-review-final"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-08-b1-review-final
            level_code: B1
            title: B1 Review & Final Conversation
            main_conversation_outcome: Use B1 speaking skills in a connected conversation.
            status: in_production
            lessons:
              - lesson-01-review-stories-and-work
              - lesson-02-review-problems-and-travel
              - lesson-03-review-goals-and-preferences
              - lesson-04-b1-final-test-practice
              - lesson-05-b1-final-conversation
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
            "lesson_key": "lesson-01-review-stories-and-work",
            "slug": "review-stories-and-work",
            "title": "Review Stories and Work",
            "conversation_situation": "review_story_and_work_update",
            "conversation_goal": "Tell a short story and give a clear work update with one next step.",
            "grammar_summary": "Combine story sequencing (then/after that) with work update phrases (I'm working on..., next...).",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Review: kamu cerita kejadian singkat (personal story), lalu kasih update kerja singkat (progress + next step).",
            "dialogue": [
                ("Alex", "How was your weekend?"),
                ("Mina", "It was great. I visited my cousin, and we went to a small concert."),
                ("Alex", "Nice. What happened after that?"),
                ("Mina", "Then we grabbed street food and talked until late."),
                ("Alex", "Sounds fun. How's work going today?"),
                ("Mina", "I'm working on the release checklist. I'm making good progress."),
                ("Alex", "Great. What's the next step?"),
                ("Mina", "Next, I'll review the risks and share an update with the team."),
            ],
            "translations": [
                ("Alex", "How was your weekend?", "Weekend kamu gimana?"),
                ("Mina", "It was great. I visited my cousin, and we went to a small concert.", "Seru. Aku ke rumah sepupuku, terus kita nonton konser kecil."),
                ("Alex", "Nice. What happened after that?", "Oke. Habis itu ngapain?"),
                ("Mina", "Then we grabbed street food and talked until late.", "Terus kita beli street food dan ngobrol sampai malam."),
                ("Alex", "Sounds fun. How's work going today?", "Kedengarannya seru. Kerja hari ini gimana?"),
                ("Mina", "I'm working on the release checklist. I'm making good progress.", "Aku lagi ngerjain release checklist. Progressnya bagus."),
                ("Alex", "Great. What's the next step?", "Oke. Next step-nya apa?"),
                ("Mina", "Next, I'll review the risks and share an update with the team.", "Berikutnya aku review risiko dan kasih update ke tim."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Then we grabbed street food.",
                    "meaning_id": "Terus kita beli street food.",
                    "usage_note": "Then helps sequence a story.",
                    "common_mistake": 'Do not say "After that then" together; use one connector.',
                },
                {
                    "phrase": "What happened after that?",
                    "meaning_id": "Habis itu apa yang terjadi?",
                    "usage_note": "A natural follow-up question for stories.",
                    "common_mistake": 'Do not say "What happen after that" without -ed for past.',
                },
                {
                    "phrase": "I'm working on the release checklist.",
                    "meaning_id": "Aku lagi ngerjain release checklist.",
                    "usage_note": "A clear work status sentence.",
                    "common_mistake": 'Do not say "I working on"; use I\'m working on.',
                },
                {
                    "phrase": "I'm making good progress.",
                    "meaning_id": "Progressnya bagus.",
                    "usage_note": "A short progress update.",
                    "common_mistake": 'Do not say "I\'m progress".',
                },
                {
                    "phrase": "Next, I'll review the risks.",
                    "meaning_id": "Berikutnya, aku review risiko.",
                    "usage_note": "Next sets the next step clearly.",
                    "common_mistake": 'Do not say "Next, I will reviewing".',
                },
            ],
            "grammar_md": [
                ("Story sequencing", ["Then we grabbed street food.", "After that, we went home."]),
                ("Work update", ["I'm working on the release checklist.", "Next, I'll review the risks."]),
            ],
            "pronunciation": [
                ("after that", "AF-ter that."),
                ("checklist", "CHECK-list."),
                ("progress", "PRAH-gres."),
            ],
            "response_prompts": [
                {
                    "prompt": "Continue a story with then.",
                    "target_response": "Then we grabbed street food.",
                    "acceptable_variations": ["Then we grabbed street food.", "Then we went home."],
                },
                {
                    "prompt": "Give a work update (working on...).",
                    "target_response": "I'm working on the release checklist.",
                    "acceptable_variations": ["I'm working on the release checklist.", "I'm working on a report."],
                },
                {
                    "prompt": "Say the next step (Next, I'll...).",
                    "target_response": "Next, I'll review the risks.",
                    "acceptable_variations": ["Next, I'll review the risks.", "Next, I'll share an update."],
                },
            ],
            "quiz": [
                {
                    "key": "story_connector",
                    "type": "multiple_choice",
                    "prompt": "Which word helps sequence a story?",
                    "options": ["then", "because", "maybe"],
                    "correct_answer": "then",
                },
                {
                    "key": "work_update",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a work status update?",
                    "options": ["I'm working on the release checklist.", "I was hungry.", "It was sunny."],
                    "correct_answer": "I'm working on the release checklist.",
                },
                {
                    "key": "next_step_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces the next action?",
                    "options": ["Next, I'll ...", "Yesterday, I ...", "Never mind."],
                    "correct_answer": "Next, I'll ...",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_review_stories_work",
                "opening_line": "Tell me what you did, then give me a work update.",
                "learner_goal": "Tell a short story, then give a work update with a next step.",
                "turns": [
                    {
                        "coach": "Tell me about your weekend.",
                        "hint": "Ceritain 2 kalimat (visited/went...).",
                        "sample_answer": "It was great. I visited my cousin and we went to a small concert.",
                        "focus": "Tell a short story",
                        "expected_keywords": ["visited", "went"],
                    },
                    {
                        "coach": "What happened after that?",
                        "hint": "Jawab pakai then.",
                        "sample_answer": "Then we grabbed street food and talked until late.",
                        "focus": "Continue the story",
                        "expected_keywords": ["then"],
                    },
                    {
                        "coach": "Now give a work update and next step.",
                        "hint": "I'm working on... Next, I'll...",
                        "sample_answer": "I'm working on the release checklist. Next, I'll review the risks.",
                        "focus": "Work update + next step",
                        "expected_keywords": ["working on", "next"],
                    },
                ],
                "target_phrases": ["Then ...", "I'm working on ...", "Next, I'll ..."],
            },
            "reading_support": "This review lesson mixes two B1 skills: telling a short story with sequence words, and giving a clear work update with a next step.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. My weekend was ...",
                "2. I visited ...",
                "3. Then we ...",
                "4. I'm working on ...",
                "5. I'm making progress.",
                "6. Next, I'll ...",
            ],
            "goal_examples": ["Then ...", "I'm working on ...", "Next, I'll ..."],
        },
        {
            "lesson_key": "lesson-02-review-problems-and-travel",
            "slug": "review-problems-and-travel",
            "title": "Review Problems and Travel",
            "conversation_situation": "review_problem_and_travel_delay",
            "conversation_goal": "Explain a problem, describe the impact, and give a travel-style delay update with an estimate.",
            "grammar_summary": "Combine: There's a problem with... / so ... and I'm running late... / I'll be there in about ...",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Review: kamu jelasin masalah (impact), lalu kasih update telat (delay + estimasi).",
            "dialogue": [
                ("Jordan", "Quick check: what's the issue?"),
                ("Mina", "There's a problem with the meeting link."),
                ("Jordan", "What's the impact?"),
                ("Mina", "People can't join, so we need a new link."),
                ("Jordan", "Okay. Are you on your way?"),
                ("Mina", "Yes, but I'm running a bit late. My train is delayed."),
                ("Jordan", "When will you arrive?"),
                ("Mina", "I'll be there in about 15 minutes."),
            ],
            "translations": [
                ("Jordan", "Quick check: what's the issue?", "Cek cepat: masalahnya apa?"),
                ("Mina", "There's a problem with the meeting link.", "Ada masalah dengan link meeting."),
                ("Jordan", "What's the impact?", "Dampaknya apa?"),
                ("Mina", "People can't join, so we need a new link.", "Orang nggak bisa join, jadi kita butuh link baru."),
                ("Jordan", "Okay. Are you on your way?", "Oke. Kamu lagi di jalan?"),
                ("Mina", "Yes, but I'm running a bit late. My train is delayed.", "Iya, tapi aku agak telat. Kereta aku delay."),
                ("Jordan", "When will you arrive?", "Kapan kamu sampai?"),
                ("Mina", "I'll be there in about 15 minutes.", "Aku sampai kira-kira 15 menit lagi."),
            ],
            "useful_phrases": [
                {
                    "phrase": "There's a problem with the meeting link.",
                    "meaning_id": "Ada masalah dengan link meeting.",
                    "usage_note": "A clear problem statement.",
                    "common_mistake": 'Do not say "Have problem"; use There\'s a problem with...',
                },
                {
                    "phrase": "People can't join, so we need a new link.",
                    "meaning_id": "Orang nggak bisa join, jadi kita butuh link baru.",
                    "usage_note": "So shows impact/result.",
                    "common_mistake": 'Do not use because if it is a result; use so.',
                },
                {
                    "phrase": "I'm running a bit late.",
                    "meaning_id": "Aku agak telat.",
                    "usage_note": "A natural delay phrase.",
                    "common_mistake": 'Do not say "I am late running"; use running late.',
                },
                {
                    "phrase": "My train is delayed.",
                    "meaning_id": "Kereta aku delay.",
                    "usage_note": "A clear reason for delay.",
                    "common_mistake": 'Do not say "My train delay"; include is.',
                },
                {
                    "phrase": "I'll be there in about 15 minutes.",
                    "meaning_id": "Aku sampai kira-kira 15 menit lagi.",
                    "usage_note": "In about + time gives an estimate.",
                    "common_mistake": 'Do not say "in 15 minutes more"; just in 15 minutes.',
                },
            ],
            "grammar_md": [
                ("Problem + impact", ["There's a problem with the meeting link.", "People can't join, so we need a new link."]),
                ("Delay + estimate", ["I'm running a bit late.", "I'll be there in about 15 minutes."]),
            ],
            "pronunciation": [
                ("issue", "ISH-yoo."),
                ("delayed", "di-LAYD."),
                ("minutes", "MIN-its."),
            ],
            "response_prompts": [
                {
                    "prompt": "State the problem.",
                    "target_response": "There's a problem with the meeting link.",
                    "acceptable_variations": ["There's a problem with the meeting link.", "There's a problem with the login page."],
                },
                {
                    "prompt": "State the impact with so.",
                    "target_response": "People can't join, so we need a new link.",
                    "acceptable_variations": ["People can't join, so we need a new link.", "Users can't sign in, so it's urgent."],
                },
                {
                    "prompt": "Give a delay estimate.",
                    "target_response": "I'm running a bit late. I'll be there in about 15 minutes.",
                    "acceptable_variations": [
                        "I'm running a bit late. I'll be there in about 15 minutes.",
                        "I'm running a bit late. I'll be there in about 20 minutes.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "problem_starter_review",
                    "type": "multiple_choice",
                    "prompt": "Which sentence starts a problem description?",
                    "options": ["There's a problem with the meeting link.", "I like meetings.", "Let's go home."],
                    "correct_answer": "There's a problem with the meeting link.",
                },
                {
                    "key": "so_result_review",
                    "type": "multiple_choice",
                    "prompt": "Which word shows a result?",
                    "options": ["so", "because", "and"],
                    "correct_answer": "so",
                },
                {
                    "key": "running_late_review",
                    "type": "multiple_choice",
                    "prompt": 'What does "running late" mean?',
                    "options": ["telat", "lebih cepat", "tidur"],
                    "correct_answer": "telat",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_review_problem_travel",
                "opening_line": "What's the issue, and are you on your way?",
                "learner_goal": "Describe a problem with impact, then give a delay update with an estimate.",
                "turns": [
                    {
                        "coach": "What's the issue?",
                        "hint": "Mulai dengan There's a problem with...",
                        "sample_answer": "There's a problem with the meeting link.",
                        "focus": "State problem",
                        "expected_keywords": ["problem", "with"],
                    },
                    {
                        "coach": "What's the impact?",
                        "hint": "Gunakan so untuk dampak.",
                        "sample_answer": "People can't join, so we need a new link.",
                        "focus": "Explain impact",
                        "expected_keywords": ["can't", "so"],
                    },
                    {
                        "coach": "Now say you're late and give an estimate.",
                        "hint": "I'm running late... I'll be there in about...",
                        "sample_answer": "I'm running a bit late. I'll be there in about 15 minutes.",
                        "focus": "Delay + estimate",
                        "expected_keywords": ["running", "in about"],
                    },
                ],
                "target_phrases": ["There's a problem with ...", "..., so ...", "I'll be there in about ..."],
            },
            "reading_support": "This review lesson connects two real-life skills: explaining problems clearly (with impact) and giving a travel-style delay update with an estimate.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. There's a problem with ...",
                "2. People can't ..., so ...",
                "3. I'm running a bit late.",
                "4. My train/flight is delayed.",
                "5. I'll be there in about ... minutes.",
                "6. Thank you for waiting.",
            ],
            "goal_examples": ["There's a problem with ...", "..., so ...", "I'll be there in about ..."],
        },
        {
            "lesson_key": "lesson-03-review-goals-and-preferences",
            "slug": "review-goals-and-preferences",
            "title": "Review Goals and Preferences",
            "conversation_situation": "review_goals_and_preferences",
            "conversation_goal": "State a goal, share progress, and explain a preference with a clear reason.",
            "grammar_summary": "Combine: My goal is to... / I've been... / I prefer... because...",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Review: kamu cerita goal + progress, lalu jelasin preferensi kamu dengan alasan.",
            "dialogue": [
                ("Leo", "What's your goal right now?"),
                ("Mina", "My goal is to speak more confidently by the end of this month."),
                ("Leo", "How's it going?"),
                ("Mina", "I'm making progress. I've been practicing every morning."),
                ("Leo", "Nice. What do you prefer for practice: coach or shadowing?"),
                ("Mina", "I prefer Conversation Coach because it gives me feedback."),
                ("Leo", "That makes sense."),
                ("Mina", "Yeah, it helps me stay consistent."),
            ],
            "translations": [
                ("Leo", "What's your goal right now?", "Goal kamu sekarang apa?"),
                ("Mina", "My goal is to speak more confidently by the end of this month.", "Goal aku adalah ngomong lebih pede paling lambat akhir bulan ini."),
                ("Leo", "How's it going?", "Gimana progressnya?"),
                ("Mina", "I'm making progress. I've been practicing every morning.", "Aku ada progress. Aku latihan tiap pagi."),
                ("Leo", "Nice. What do you prefer for practice: coach or shadowing?", "Oke. Kamu prefer latihan yang mana: coach atau shadowing?"),
                ("Mina", "I prefer Conversation Coach because it gives me feedback.", "Aku prefer Conversation Coach karena itu kasih aku feedback."),
                ("Leo", "That makes sense.", "Masuk akal."),
                ("Mina", "Yeah, it helps me stay consistent.", "Iya, itu bantu aku tetap konsisten."),
            ],
            "useful_phrases": [
                {
                    "phrase": "My goal is to speak more confidently by the end of this month.",
                    "meaning_id": "Goal aku adalah ngomong lebih pede paling lambat akhir bulan ini.",
                    "usage_note": "Goal + deadline in one sentence.",
                    "common_mistake": 'Do not forget by + time for deadlines.',
                },
                {
                    "phrase": "I've been practicing every morning.",
                    "meaning_id": "Aku latihan tiap pagi.",
                    "usage_note": "Shows an ongoing habit up to now.",
                    "common_mistake": 'Do not say "I am practicing since"; use I\'ve been practicing.',
                },
                {
                    "phrase": "I prefer Conversation Coach because it gives me feedback.",
                    "meaning_id": "Aku prefer Conversation Coach karena itu kasih aku feedback.",
                    "usage_note": "Preference + reason.",
                    "common_mistake": 'Do not say "I prefer because"; include what you prefer.',
                },
                {
                    "phrase": "That makes sense.",
                    "meaning_id": "Masuk akal.",
                    "usage_note": "A polite reaction to reasons.",
                    "common_mistake": 'Do not say "That make sense"; add -s.',
                },
                {
                    "phrase": "It helps me stay consistent.",
                    "meaning_id": "Itu bantu aku tetap konsisten.",
                    "usage_note": "A simple benefit sentence.",
                    "common_mistake": 'Do not say "help me to stay" every time; help me stay is natural.',
                },
            ],
            "grammar_md": [
                ("Goal + deadline", ["My goal is to ... by the end of this month.", "My goal is to ... by Friday."]),
                ("Preference + reason", ["I prefer Conversation Coach because it gives me feedback.", "I prefer option B because it's simpler."]),
            ],
            "pronunciation": [
                ("confidently", "KON-fi-dent-lee."),
                ("feedback", "FEED-bak."),
                ("consistent", "kun-SIS-tent."),
            ],
            "response_prompts": [
                {
                    "prompt": "State goal + deadline.",
                    "target_response": "My goal is to speak more confidently by the end of this month.",
                    "acceptable_variations": [
                        "My goal is to speak more confidently by the end of this month.",
                        "My goal is to speak more confidently by next month.",
                    ],
                },
                {
                    "prompt": "Share progress with I've been practicing.",
                    "target_response": "I've been practicing every morning.",
                    "acceptable_variations": ["I've been practicing every morning.", "I've been practicing every day."],
                },
                {
                    "prompt": "State preference with because.",
                    "target_response": "I prefer Conversation Coach because it gives me feedback.",
                    "acceptable_variations": [
                        "I prefer Conversation Coach because it gives me feedback.",
                        "I prefer shadowing because it's simple.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "goal_deadline_review",
                    "type": "multiple_choice",
                    "prompt": "Which sentence includes a goal and a deadline?",
                    "options": [
                        "My goal is to speak more confidently by the end of this month.",
                        "My goal to speak more confidently.",
                        "I spoke yesterday.",
                    ],
                    "correct_answer": "My goal is to speak more confidently by the end of this month.",
                },
                {
                    "key": "been_practicing_review",
                    "type": "multiple_choice",
                    "prompt": "Which sentence shows an ongoing habit up to now?",
                    "options": ["I've been practicing every morning.", "I practice tomorrow.", "I practiced tomorrow."],
                    "correct_answer": "I've been practicing every morning.",
                },
                {
                    "key": "prefer_because_review",
                    "type": "multiple_choice",
                    "prompt": "Which sentence explains a preference with a reason?",
                    "options": [
                        "I prefer Conversation Coach because it gives me feedback.",
                        "I prefer because feedback.",
                        "Prefer Conversation Coach.",
                    ],
                    "correct_answer": "I prefer Conversation Coach because it gives me feedback.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_review_goals_preferences",
                "opening_line": "Tell me your goal, progress, and preference.",
                "learner_goal": "State a goal, share progress, and explain a preference with a reason.",
                "turns": [
                    {
                        "coach": "What's your goal right now?",
                        "hint": "Goal + by ...",
                        "sample_answer": "My goal is to speak more confidently by the end of this month.",
                        "focus": "Goal with deadline",
                        "expected_keywords": ["goal", "by"],
                    },
                    {
                        "coach": "How's it going?",
                        "hint": "I've been practicing ...",
                        "sample_answer": "I'm making progress. I've been practicing every morning.",
                        "focus": "Progress update",
                        "expected_keywords": ["progress", "been"],
                    },
                    {
                        "coach": "Which practice method do you prefer, and why?",
                        "hint": "I prefer ... because ...",
                        "sample_answer": "I prefer Conversation Coach because it gives me feedback.",
                        "focus": "Preference with reason",
                        "expected_keywords": ["prefer", "because"],
                    },
                ],
                "target_phrases": ["My goal is to ... by ...", "I've been practicing ...", "I prefer ... because ..."],
            },
            "reading_support": "This review lesson combines goal language and preference language. Keep your sentences clear: goal + deadline, progress habit, and preference + reason.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. My goal is to ... by ...",
                "2. I'm making progress.",
                "3. I've been practicing ...",
                "4. I prefer ... because ...",
                "5. The main reason is ...",
                "6. It helps me ...",
            ],
            "goal_examples": ["My goal is to ...", "I've been practicing ...", "I prefer ... because ..."],
        },
        {
            "lesson_key": "lesson-04-b1-final-test-practice",
            "slug": "b1-final-test-practice",
            "title": "B1 Final Test Practice",
            "conversation_situation": "b1_final_test_practice",
            "conversation_goal": "Practice a short mixed conversation with clear, accurate sentences across B1 topics.",
            "grammar_summary": "Review connectors (because/so/but/then) and key patterns (goal, progress, preference, problems).",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Latihan test: kamu jawab beberapa prompt cepat (goal, progress, problem, preference) dengan kalimat jelas.",
            "dialogue": [
                ("Alex", "Let's do a quick B1 practice round."),
                ("Mina", "Okay, I'm ready."),
                ("Alex", "What's your goal this month?"),
                ("Mina", "My goal is to speak more confidently by the end of this month."),
                ("Alex", "Any challenges?"),
                ("Mina", "The biggest challenge is staying consistent after work, so I'm keeping sessions short."),
                ("Alex", "Which do you prefer for dinner, option A or B?"),
                ("Mina", "I prefer option B because it's cheaper, but it might be crowded."),
            ],
            "translations": [
                ("Alex", "Let's do a quick B1 practice round.", "Yuk latihan B1 cepat."),
                ("Mina", "Okay, I'm ready.", "Oke, aku siap."),
                ("Alex", "What's your goal this month?", "Goal kamu bulan ini apa?"),
                ("Mina", "My goal is to speak more confidently by the end of this month.", "Goal aku adalah ngomong lebih pede paling lambat akhir bulan ini."),
                ("Alex", "Any challenges?", "Ada tantangan?"),
                ("Mina", "The biggest challenge is staying consistent after work, so I'm keeping sessions short.", "Tantangan terbesarnya tetap konsisten setelah kerja, jadi aku bikin sesi pendek."),
                ("Alex", "Which do you prefer for dinner, option A or B?", "Kamu prefer yang mana buat makan malam, opsi A atau B?"),
                ("Mina", "I prefer option B because it's cheaper, but it might be crowded.", "Aku prefer opsi B karena lebih murah, tapi mungkin rame."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let's do a quick practice round.",
                    "meaning_id": "Yuk latihan cepat.",
                    "usage_note": "A simple test starter.",
                    "common_mistake": 'Do not say "Let\'s to do"; use let\'s do.',
                },
                {
                    "phrase": "The biggest challenge is staying consistent.",
                    "meaning_id": "Tantangan terbesarnya tetap konsisten.",
                    "usage_note": "A clear challenge sentence.",
                    "common_mistake": 'Do not drop is; keep the structure.',
                },
                {
                    "phrase": "So I'm keeping sessions short.",
                    "meaning_id": "Jadi aku bikin sesi pendek.",
                    "usage_note": "So shows a solution/decision.",
                    "common_mistake": 'Do not use because if it is a result; use so.',
                },
                {
                    "phrase": "I prefer option B because it's cheaper.",
                    "meaning_id": "Aku prefer opsi B karena lebih murah.",
                    "usage_note": "Preference + reason.",
                    "common_mistake": 'Do not say "more cheap"; use cheaper.',
                },
                {
                    "phrase": "But it might be crowded.",
                    "meaning_id": "Tapi mungkin rame.",
                    "usage_note": "But + might expresses a concern.",
                    "common_mistake": 'Do not say "might crowded"; add be.',
                },
            ],
            "grammar_md": [
                ("Key connectors", ["because (reason)", "so (result/decision)", "but (contrast)", "then (sequence)"]),
                ("Mixed sentence patterns", ["My goal is to ... by ...", "I prefer ... because ...", "..., so ..."]),
            ],
            "pronunciation": [
                ("consistent", "kun-SIS-tent."),
                ("sessions", "SESH-unz."),
                ("crowded", "KROW-did."),
            ],
            "response_prompts": [
                {
                    "prompt": "Goal + deadline.",
                    "target_response": "My goal is to speak more confidently by the end of this month.",
                    "acceptable_variations": ["My goal is to speak more confidently by the end of this month.", "My goal is to improve my speaking by next month."],
                },
                {
                    "prompt": "Challenge + so (solution).",
                    "target_response": "The biggest challenge is staying consistent, so I'm keeping sessions short.",
                    "acceptable_variations": [
                        "The biggest challenge is staying consistent, so I'm keeping sessions short.",
                        "The biggest challenge is finding time, so I practice in the morning.",
                    ],
                },
                {
                    "prompt": "Preference + because + but (concern).",
                    "target_response": "I prefer option B because it's cheaper, but it might be crowded.",
                    "acceptable_variations": [
                        "I prefer option B because it's cheaper, but it might be crowded.",
                        "I prefer option A because it's nicer, but it's more expensive.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "so_connector",
                    "type": "multiple_choice",
                    "prompt": "Which word shows a result or decision?",
                    "options": ["so", "because", "then"],
                    "correct_answer": "so",
                },
                {
                    "key": "might_usage",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["It might be crowded.", "It might crowded.", "It might to be crowded."],
                    "correct_answer": "It might be crowded.",
                },
                {
                    "key": "because_usage",
                    "type": "multiple_choice",
                    "prompt": "Which sentence uses because correctly?",
                    "options": ["I prefer option B because it's cheaper.", "I prefer because it's cheaper.", "I because prefer option B."],
                    "correct_answer": "I prefer option B because it's cheaper.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_final_test_practice",
                "opening_line": "Quick test: answer my prompts.",
                "learner_goal": "Answer short prompts across B1 topics with clear sentences.",
                "turns": [
                    {
                        "coach": "What's your goal this month?",
                        "hint": "Goal + by ...",
                        "sample_answer": "My goal is to speak more confidently by the end of this month.",
                        "focus": "Goal with deadline",
                        "expected_keywords": ["goal", "by"],
                    },
                    {
                        "coach": "What's your biggest challenge, and what will you do?",
                        "hint": "Challenge + so ...",
                        "sample_answer": "The biggest challenge is staying consistent, so I'm keeping sessions short.",
                        "focus": "Challenge + solution",
                        "expected_keywords": ["challenge", "so"],
                    },
                    {
                        "coach": "Compare and choose: option A or B?",
                        "hint": "I prefer ... because ... but ...",
                        "sample_answer": "I prefer option B because it's cheaper, but it might be crowded.",
                        "focus": "Preference with reason + concern",
                        "expected_keywords": ["prefer", "because", "might"],
                    },
                ],
                "target_phrases": ["My goal is to ... by ...", "..., so ...", "I prefer ... because ..., but ..."],
            },
            "reading_support": "Final test practice is about clarity and accuracy. Keep answers short: one sentence per idea, using the right connector.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. My goal is to ... by ...",
                "2. I've been practicing ...",
                "3. The biggest challenge is ...",
                "4. ..., so I ...",
                "5. I prefer ... because ...",
                "6. ..., but it might ...",
            ],
            "goal_examples": ["My goal is to ...", "The biggest challenge is ...", "I prefer ... because ..."],
        },
        {
            "lesson_key": "lesson-05-b1-final-conversation",
            "slug": "b1-final-conversation",
            "title": "B1 Final Conversation",
            "conversation_situation": "b1_final_connected_conversation",
            "conversation_goal": "Hold a connected conversation that includes a story, a plan, a problem, a preference, and a next step.",
            "grammar_summary": "Use connectors naturally (then/because/so/but) to keep the conversation connected and clear.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Final conversation: kamu ngobrol panjang (tetap sederhana) mencakup cerita, goal, problem, preferensi, dan kesepakatan next step.",
            "dialogue": [
                ("Jordan", "How have you been lately?"),
                ("Mina", "Pretty good. Last week I tried a new speaking routine."),
                ("Jordan", "Nice. What happened?"),
                ("Mina", "At first it was hard, but then it got easier because I kept sessions short."),
                ("Jordan", "Great progress. What's your goal now?"),
                ("Mina", "My goal is to speak more confidently by next month."),
                ("Jordan", "Any problems right now?"),
                ("Mina", "Sometimes I get distracted, so I leave my phone in another room."),
                ("Jordan", "Good idea. Which practice method do you prefer?"),
                ("Mina", "I prefer Conversation Coach because it gives feedback. So my next step is to practice three times this week."),
            ],
            "translations": [
                ("Jordan", "How have you been lately?", "Akhir-akhir ini gimana?"),
                ("Mina", "Pretty good. Last week I tried a new speaking routine.", "Lumayan baik. Minggu lalu aku coba rutinitas speaking baru."),
                ("Jordan", "Nice. What happened?", "Oke. Terus gimana?"),
                ("Mina", "At first it was hard, but then it got easier because I kept sessions short.", "Awalnya susah, tapi kemudian jadi lebih mudah karena aku bikin sesi pendek."),
                ("Jordan", "Great progress. What's your goal now?", "Progress bagus. Goal kamu sekarang apa?"),
                ("Mina", "My goal is to speak more confidently by next month.", "Goal aku adalah ngomong lebih pede paling lambat bulan depan."),
                ("Jordan", "Any problems right now?", "Ada masalah sekarang?"),
                ("Mina", "Sometimes I get distracted, so I leave my phone in another room.", "Kadang aku terdistraksi, jadi aku taruh HP di ruangan lain."),
                ("Jordan", "Good idea. Which practice method do you prefer?", "Ide bagus. Kamu prefer metode latihan yang mana?"),
                ("Mina", "I prefer Conversation Coach because it gives feedback. So my next step is to practice three times this week.", "Aku prefer Conversation Coach karena itu kasih feedback. Jadi next step aku latihan tiga kali minggu ini."),
            ],
            "useful_phrases": [
                {
                    "phrase": "At first it was hard, but then it got easier.",
                    "meaning_id": "Awalnya susah, tapi kemudian jadi lebih mudah.",
                    "usage_note": "A natural story + progress sentence.",
                    "common_mistake": 'Do not say "In first"; use at first.',
                },
                {
                    "phrase": "Because I kept sessions short.",
                    "meaning_id": "Karena aku bikin sesi pendek.",
                    "usage_note": "A clear reason sentence.",
                    "common_mistake": 'Do not say "Because kept"; include I.',
                },
                {
                    "phrase": "Sometimes I get distracted, so I leave my phone in another room.",
                    "meaning_id": "Kadang aku terdistraksi, jadi aku taruh HP di ruangan lain.",
                    "usage_note": "Problem + solution in one sentence.",
                    "common_mistake": 'Do not use because if it is a solution/result; use so.',
                },
                {
                    "phrase": "I prefer Conversation Coach because it gives feedback.",
                    "meaning_id": "Aku prefer Conversation Coach karena itu kasih feedback.",
                    "usage_note": "Preference + reason.",
                    "common_mistake": 'Do not say "because give"; include it gives.',
                },
                {
                    "phrase": "So my next step is to practice three times this week.",
                    "meaning_id": "Jadi next step aku latihan tiga kali minggu ini.",
                    "usage_note": "A clear next step plan.",
                    "common_mistake": 'Do not say "three time"; add -s.',
                },
            ],
            "grammar_md": [
                ("Connected conversation connectors", ["at first / then", "because (reason)", "so (result/decision)", "but (contrast)"]),
                ("Goal + preference + next step", ["My goal is to ... by ...", "I prefer ... because ...", "So my next step is to ..."]),
            ],
            "pronunciation": [
                ("at first", "at FIRST."),
                ("distracted", "di-STRAK-tid."),
                ("another", "uh-NUH-ther."),
            ],
            "response_prompts": [
                {
                    "prompt": "Tell a progress story (at first... but then...).",
                    "target_response": "At first it was hard, but then it got easier.",
                    "acceptable_variations": ["At first it was hard, but then it got easier.", "At first I was nervous, but then I felt better."],
                },
                {
                    "prompt": "Share a problem + solution with so.",
                    "target_response": "Sometimes I get distracted, so I leave my phone in another room.",
                    "acceptable_variations": [
                        "Sometimes I get distracted, so I leave my phone in another room.",
                        "Sometimes I'm tired, so I practice in the morning.",
                    ],
                },
                {
                    "prompt": "Preference + reason + next step.",
                    "target_response": "I prefer Conversation Coach because it gives feedback. So my next step is to practice three times this week.",
                    "acceptable_variations": [
                        "I prefer Conversation Coach because it gives feedback. So my next step is to practice three times this week.",
                        "I prefer shadowing because it's simple. So my next step is to practice twice this week.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "at_first_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "at first" mean?',
                    "options": ["awalnya", "akhirnya", "sekarang"],
                    "correct_answer": "awalnya",
                },
                {
                    "key": "connected_connector",
                    "type": "multiple_choice",
                    "prompt": "Which set connects ideas in B1 conversations?",
                    "options": ["then / because / so / but", "red / blue / green", "one / two / three"],
                    "correct_answer": "then / because / so / but",
                },
                {
                    "key": "next_step_structure",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct next step sentence.",
                    "options": ["So my next step is to practice three times this week.", "So my next step practice three times.", "So next step is practice three time."],
                    "correct_answer": "So my next step is to practice three times this week.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_final_conversation",
                "opening_line": "Let's have a final conversation. Start with a short story and your goal.",
                "learner_goal": "Hold a connected conversation: story, goal, problem, preference, and next step.",
                "turns": [
                    {
                        "coach": "Start with a short story about your practice last week.",
                        "hint": "At first..., but then... because...",
                        "sample_answer": "At first it was hard, but then it got easier because I kept sessions short.",
                        "focus": "Story + reason",
                        "expected_keywords": ["at first", "but", "because"],
                    },
                    {
                        "coach": "Now state your goal with a deadline.",
                        "hint": "My goal is to... by ...",
                        "sample_answer": "My goal is to speak more confidently by next month.",
                        "focus": "Goal with deadline",
                        "expected_keywords": ["goal", "by"],
                    },
                    {
                        "coach": "Share one problem and your solution, then preference + next step.",
                        "hint": "Sometimes..., so... I prefer... because... So my next step is...",
                        "sample_answer": "Sometimes I get distracted, so I leave my phone in another room. I prefer Conversation Coach because it gives feedback. So my next step is to practice three times this week.",
                        "focus": "Problem + preference + next step",
                        "expected_keywords": ["so", "prefer", "because", "next step"],
                    },
                ],
                "target_phrases": ["At first..., but then...", "My goal is to ... by ...", "So my next step is to ..."],
            },
            "reading_support": "A final B1 conversation should feel connected. Use simple connectors to link your story, goal, problem, preference, and next step.",
            "writing_support_lines": [
                "Write your final conversation (8 lines):",
                "1. Last week I ...",
                "2. At first it was ..., but then ...",
                "3. Because ...",
                "4. My goal is to ... by ...",
                "5. Sometimes I ..., so I ...",
                "6. I prefer ... because ...",
                "7. So my next step is to ...",
                "8. Thanks for the chat.",
            ],
            "goal_examples": ["At first..., but then...", "I prefer ... because ...", "So my next step is to ..."],
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

