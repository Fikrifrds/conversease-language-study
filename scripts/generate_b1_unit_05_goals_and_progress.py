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

        Read it again and underline the goal, progress, challenge, and next step words.
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B1"
    b1_root = Path("content/curriculum/english/B1")
    units_root = b1_root / "units"
    unit_key = "unit-05-goals-and-progress"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-05-goals-and-progress
            level_code: B1
            title: Goals & Progress
            main_conversation_outcome: Talk about goals, plans, progress, and challenges.
            status: in_production
            lessons:
              - lesson-01-talking-about-goals
              - lesson-02-explaining-progress
              - lesson-03-discussing-challenges
              - lesson-04-making-next-step-plans
              - lesson-05-goals-progress-mission
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
            "lesson_key": "lesson-01-talking-about-goals",
            "slug": "talking-about-goals",
            "title": "Talking About Goals",
            "conversation_situation": "talking_about_learning_goals",
            "conversation_goal": "Talk about a personal goal, give a time frame, and explain why it matters.",
            "grammar_summary": "Use My goal is to... / I'd like to... and by + time to describe goals clearly.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu ngobrol sama teman. Kamu cerita goal kamu, kapan targetnya, dan kenapa penting buat kamu.",
            "dialogue": [
                ("Leo", "So, what's your goal this month?"),
                ("Mina", "My goal is to speak more confidently."),
                ("Leo", "Nice. By when?"),
                ("Mina", "By the end of this month."),
                ("Leo", "Why is that important to you?"),
                ("Mina", "Because I want to join meetings without feeling nervous."),
                ("Leo", "That sounds great. How will you practice?"),
                ("Mina", "I'll practice five minutes every day."),
            ],
            "translations": [
                ("Leo", "So, what's your goal this month?", "Jadi, apa goal kamu bulan ini?"),
                ("Mina", "My goal is to speak more confidently.", "Goal aku adalah ngomong lebih pede."),
                ("Leo", "Nice. By when?", "Oke. Targetnya kapan?"),
                ("Mina", "By the end of this month.", "Akhir bulan ini."),
                ("Leo", "Why is that important to you?", "Kenapa itu penting buat kamu?"),
                ("Mina", "Because I want to join meetings without feeling nervous.", "Karena aku mau ikut meeting tanpa merasa grogi."),
                ("Leo", "That sounds great. How will you practice?", "Kedengarannya bagus. Kamu latihan gimana?"),
                ("Mina", "I'll practice five minutes every day.", "Aku latihan lima menit tiap hari."),
            ],
            "useful_phrases": [
                {
                    "phrase": "My goal is to speak more confidently.",
                    "meaning_id": "Goal aku adalah ngomong lebih pede.",
                    "usage_note": "A clear way to state a goal.",
                    "common_mistake": 'Do not say "My goal to speak"; use is to.',
                },
                {
                    "phrase": "By the end of this month.",
                    "meaning_id": "Akhir bulan ini.",
                    "usage_note": "By + time shows a deadline.",
                    "common_mistake": 'Do not say "until end"; use by for deadlines.',
                },
                {
                    "phrase": "Because I want to join meetings without feeling nervous.",
                    "meaning_id": "Karena aku mau ikut meeting tanpa merasa grogi.",
                    "usage_note": "Give one simple reason.",
                    "common_mistake": "Avoid too many reasons; keep it short.",
                },
                {
                    "phrase": "I'd like to improve my speaking.",
                    "meaning_id": "Aku pengen improve speaking-ku.",
                    "usage_note": "A polite, friendly goal phrase.",
                    "common_mistake": 'Do not say "I like to improve" for goals; use I\'d like to.',
                },
                {
                    "phrase": "I'll practice five minutes every day.",
                    "meaning_id": "Aku latihan lima menit tiap hari.",
                    "usage_note": "A simple plan connected to a goal.",
                    "common_mistake": 'Do not say "I will practicing"; use I\'ll practice.',
                },
            ],
            "grammar_md": [
                ("My goal is to + verb", ["My goal is to speak more confidently.", "My goal is to learn 50 new words."]),
                ("By + time (deadline)", ["By the end of this month.", "By Friday morning."]),
            ],
            "pronunciation": [
                ("confidently", "KON-fi-dent-lee."),
                ("goal", "GOHL."),
                ("by the end", "by-the-END (link it)."),
            ],
            "response_prompts": [
                {
                    "prompt": "State your goal (speaking confidently).",
                    "target_response": "My goal is to speak more confidently.",
                    "acceptable_variations": ["My goal is to speak more confidently.", "My goal is to speak English more confidently."],
                },
                {
                    "prompt": "Give a deadline (end of this month).",
                    "target_response": "By the end of this month.",
                    "acceptable_variations": ["By the end of this month.", "By next month."],
                },
                {
                    "prompt": "Give one reason (meetings).",
                    "target_response": "Because I want to join meetings without feeling nervous.",
                    "acceptable_variations": [
                        "Because I want to join meetings without feeling nervous.",
                        "Because I want to speak more comfortably at work.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "goal_sentence",
                    "type": "multiple_choice",
                    "prompt": "Which sentence states a goal?",
                    "options": ["My goal is to speak more confidently.", "I spoke yesterday.", "I am a goal."],
                    "correct_answer": "My goal is to speak more confidently.",
                },
                {
                    "key": "by_deadline",
                    "type": "multiple_choice",
                    "prompt": 'What does "by the end of this month" mean?',
                    "options": ["paling lambat akhir bulan ini", "mulai akhir bulan ini", "setiap akhir bulan"],
                    "correct_answer": "paling lambat akhir bulan ini",
                },
                {
                    "key": "because_reason",
                    "type": "multiple_choice",
                    "prompt": "Which word introduces a reason?",
                    "options": ["because", "so", "but"],
                    "correct_answer": "because",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_goals_talk_about_goal",
                "opening_line": "What's your goal this month?",
                "learner_goal": "State a goal, give a deadline, and explain why it matters.",
                "turns": [
                    {
                        "coach": "What's your goal this month?",
                        "hint": "Jawab dengan: My goal is to ...",
                        "sample_answer": "My goal is to speak more confidently.",
                        "focus": "State the goal",
                        "expected_keywords": ["goal", "to"],
                    },
                    {
                        "coach": "By when?",
                        "hint": "Gunakan by + waktu.",
                        "sample_answer": "By the end of this month.",
                        "focus": "State the deadline",
                        "expected_keywords": ["by", "end"],
                    },
                    {
                        "coach": "Why does it matter to you?",
                        "hint": "Jawab dengan because + reason.",
                        "sample_answer": "Because I want to join meetings without feeling nervous.",
                        "focus": "Give a reason",
                        "expected_keywords": ["because", "meetings"],
                    },
                ],
                "target_phrases": ["My goal is to ...", "By the end of ...", "Because I want to ..."],
            },
            "reading_support": "A clear goal conversation includes: the goal, the time frame, and one reason why the goal matters.",
            "writing_support_lines": [
                "Write 4 lines:",
                "1. My goal is to ...",
                "2. By the end of ...",
                "3. Because I want to ...",
                "4. I'll practice ... every day.",
            ],
            "goal_examples": ["My goal is to ...", "By the end of ...", "Because I want to ..."],
        },
        {
            "lesson_key": "lesson-02-explaining-progress",
            "slug": "explaining-progress",
            "title": "Explaining Progress",
            "conversation_situation": "explaining_learning_progress",
            "conversation_goal": "Explain your progress clearly, mention what improved, and say what you still need to work on.",
            "grammar_summary": "Use I'm making progress... / I've been practicing... / I still need to... to give a clear progress update.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu kasih update progress ke teman. Kamu bilang progressnya gimana, apa yang membaik, dan apa yang masih perlu dilatih.",
            "dialogue": [
                ("Leo", "How's your speaking goal going?"),
                ("Mina", "I'm making good progress."),
                ("Leo", "Nice. What have you been doing?"),
                ("Mina", "I've been practicing every morning for five minutes."),
                ("Leo", "How far are you now?"),
                ("Mina", "I'm about halfway. I can speak for two minutes without stopping."),
                ("Leo", "That's great. What still needs work?"),
                ("Mina", "I still need to improve my pronunciation."),
            ],
            "translations": [
                ("Leo", "How's your speaking goal going?", "Gimana progress goal speaking kamu?"),
                ("Mina", "I'm making good progress.", "Progressnya bagus."),
                ("Leo", "Nice. What have you been doing?", "Oke. Kamu ngapain aja?"),
                ("Mina", "I've been practicing every morning for five minutes.", "Aku latihan tiap pagi lima menit."),
                ("Leo", "How far are you now?", "Sekarang sudah sejauh apa?"),
                ("Mina", "I'm about halfway. I can speak for two minutes without stopping.", "Kira-kira setengah jalan. Aku bisa ngomong dua menit tanpa berhenti."),
                ("Leo", "That's great. What still needs work?", "Bagus. Apa yang masih perlu dilatih?"),
                ("Mina", "I still need to improve my pronunciation.", "Aku masih perlu improve pronunciation."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'm making good progress.",
                    "meaning_id": "Progressnya bagus.",
                    "usage_note": "A natural progress update phrase.",
                    "common_mistake": 'Do not say "I\'m progress".',
                },
                {
                    "phrase": "I've been practicing every morning.",
                    "meaning_id": "Aku latihan tiap pagi.",
                    "usage_note": "Present perfect shows a habit up to now.",
                    "common_mistake": 'Do not say "I am practicing since"; use I\'ve been practicing.',
                },
                {
                    "phrase": "I'm about halfway.",
                    "meaning_id": "Kira-kira setengah jalan.",
                    "usage_note": "A simple way to describe progress level.",
                    "common_mistake": 'Do not say "I am half way" without about if it is approximate.',
                },
                {
                    "phrase": "I can speak for two minutes without stopping.",
                    "meaning_id": "Aku bisa ngomong dua menit tanpa berhenti.",
                    "usage_note": "A clear progress metric.",
                    "common_mistake": 'Do not say "without stop"; use without stopping.',
                },
                {
                    "phrase": "I still need to improve my pronunciation.",
                    "meaning_id": "Aku masih perlu improve pronunciation.",
                    "usage_note": "Still need shows what remains.",
                    "common_mistake": 'Do not say "I still must"; still need is more natural.',
                },
            ],
            "grammar_md": [
                ("I've been + verb-ing (habit up to now)", ["I've been practicing every morning.", "I've been studying for 10 minutes a day."]),
                ("Still need to + verb", ["I still need to improve my pronunciation.", "I still need to review the grammar."]),
            ],
            "pronunciation": [
                ("progress", "PRAH-gres."),
                ("halfway", "HAF-way."),
                ("pronunciation", "pro-nun-see-AY-shun."),
            ],
            "response_prompts": [
                {
                    "prompt": "Say you're making good progress.",
                    "target_response": "I'm making good progress.",
                    "acceptable_variations": ["I'm making good progress.", "I'm making progress."],
                },
                {
                    "prompt": "Say what you've been doing (practice every morning).",
                    "target_response": "I've been practicing every morning.",
                    "acceptable_variations": ["I've been practicing every morning.", "I've been practicing every day."],
                },
                {
                    "prompt": "Say what you still need to work on (pronunciation).",
                    "target_response": "I still need to improve my pronunciation.",
                    "acceptable_variations": ["I still need to improve my pronunciation.", "I still need to improve my listening."],
                },
            ],
            "quiz": [
                {
                    "key": "been_practicing",
                    "type": "multiple_choice",
                    "prompt": "Which sentence shows a habit up to now?",
                    "options": ["I've been practicing every morning.", "I practiced tomorrow.", "I am practice yesterday."],
                    "correct_answer": "I've been practicing every morning.",
                },
                {
                    "key": "halfway_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "halfway" mean?',
                    "options": ["setengah jalan", "langsung selesai", "tidak mulai"],
                    "correct_answer": "setengah jalan",
                },
                {
                    "key": "still_need",
                    "type": "multiple_choice",
                    "prompt": 'What does "still need to" express?',
                    "options": ["masih perlu", "sudah selesai", "tidak boleh"],
                    "correct_answer": "masih perlu",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_goals_explain_progress",
                "opening_line": "How's your goal going?",
                "learner_goal": "Explain your progress, say what you've been doing, and mention what you still need to work on.",
                "turns": [
                    {
                        "coach": "How's your goal going?",
                        "hint": "Mulai dengan: I'm making good progress.",
                        "sample_answer": "I'm making good progress.",
                        "focus": "Share progress",
                        "expected_keywords": ["progress"],
                    },
                    {
                        "coach": "What have you been doing?",
                        "hint": "Jawab dengan I've been practicing ...",
                        "sample_answer": "I've been practicing every morning for five minutes.",
                        "focus": "Explain practice habit",
                        "expected_keywords": ["been", "practicing"],
                    },
                    {
                        "coach": "What still needs work?",
                        "hint": "Jawab dengan I still need to ...",
                        "sample_answer": "I still need to improve my pronunciation.",
                        "focus": "State what's next to improve",
                        "expected_keywords": ["still", "improve"],
                    },
                ],
                "target_phrases": ["I'm making progress.", "I've been practicing ...", "I still need to ..."],
            },
            "reading_support": "A clear progress update includes: your current progress, what actions you have been doing, and what you still need to work on.",
            "writing_support_lines": [
                "Write 4 lines:",
                "1. I'm making good progress.",
                "2. I've been practicing ...",
                "3. I'm about ... (halfway / almost done).",
                "4. I still need to improve ...",
            ],
            "goal_examples": ["I'm making progress.", "I've been practicing ...", "I still need to ..."],
        },
        {
            "lesson_key": "lesson-03-discussing-challenges",
            "slug": "discussing-challenges",
            "title": "Discussing Challenges",
            "conversation_situation": "discussing_learning_challenges",
            "conversation_goal": "Describe a challenge, explain why it is difficult, and ask for a simple suggestion.",
            "grammar_summary": "Use The biggest challenge is... / I'm struggling with... / It's hard to... to talk about challenges clearly.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu cerita tantangan belajar. Kamu jelaskan kendalanya, kenapa susah, lalu minta saran sederhana.",
            "dialogue": [
                ("Leo", "How is your practice going this week?"),
                ("Mina", "Honestly, it's been challenging."),
                ("Leo", "What's the biggest challenge?"),
                ("Mina", "The biggest challenge is staying consistent after work."),
                ("Leo", "Why is it hard?"),
                ("Mina", "I get distracted by my phone, and I feel tired."),
                ("Leo", "I see. Do you want a quick tip?"),
                ("Mina", "Yes, please. Do you have any tips?"),
            ],
            "translations": [
                ("Leo", "How is your practice going this week?", "Gimana latihan kamu minggu ini?"),
                ("Mina", "Honestly, it's been challenging.", "Jujur, lumayan menantang."),
                ("Leo", "What's the biggest challenge?", "Tantangan terbesarnya apa?"),
                ("Mina", "The biggest challenge is staying consistent after work.", "Tantangan terbesarnya tetap konsisten setelah kerja."),
                ("Leo", "Why is it hard?", "Kenapa susah?"),
                ("Mina", "I get distracted by my phone, and I feel tired.", "Aku gampang terdistraksi sama HP, dan aku capek."),
                ("Leo", "I see. Do you want a quick tip?", "Oke. Mau tips singkat?"),
                ("Mina", "Yes, please. Do you have any tips?", "Iya. Ada tips nggak?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "The biggest challenge is staying consistent.",
                    "meaning_id": "Tantangan terbesarnya tetap konsisten.",
                    "usage_note": "A clear way to name the main challenge.",
                    "common_mistake": 'Do not say "My biggest challenge staying"; use is + verb-ing.',
                },
                {
                    "phrase": "I'm struggling with motivation.",
                    "meaning_id": "Aku lagi struggling sama motivasi.",
                    "usage_note": "Struggling with is common for difficulties.",
                    "common_mistake": 'Do not say "I struggle about"; use with.',
                },
                {
                    "phrase": "It's hard to stay consistent after work.",
                    "meaning_id": "Susah untuk tetap konsisten setelah kerja.",
                    "usage_note": "Hard to + verb explains difficulty.",
                    "common_mistake": 'Do not say "It hard"; add is.',
                },
                {
                    "phrase": "I get distracted by my phone.",
                    "meaning_id": "Aku gampang terdistraksi sama HP.",
                    "usage_note": "A clear reason for the challenge.",
                    "common_mistake": 'Do not say "I distracted"; use get distracted.',
                },
                {
                    "phrase": "Do you have any tips?",
                    "meaning_id": "Ada tips nggak?",
                    "usage_note": "A simple way to ask for advice.",
                    "common_mistake": 'Do not say "Give me tips" in a rude way; ask do you have any tips?',
                },
            ],
            "grammar_md": [
                ("The biggest challenge is + noun/verb-ing", ["The biggest challenge is staying consistent.", "The biggest challenge is finding time."]),
                ("It's hard to + verb", ["It's hard to stay consistent after work.", "It's hard to focus when I'm tired."]),
            ],
            "pronunciation": [
                ("challenge", "CHAL-inj."),
                ("consistent", "kun-SIS-tent."),
                ("distracted", "di-STRAK-tid."),
            ],
            "response_prompts": [
                {
                    "prompt": "Name your biggest challenge.",
                    "target_response": "The biggest challenge is staying consistent.",
                    "acceptable_variations": ["The biggest challenge is staying consistent.", "The biggest challenge is finding time."],
                },
                {
                    "prompt": "Give one reason (distracted by phone).",
                    "target_response": "I get distracted by my phone.",
                    "acceptable_variations": ["I get distracted by my phone.", "I feel tired after work."],
                },
                {
                    "prompt": "Ask for a tip.",
                    "target_response": "Do you have any tips?",
                    "acceptable_variations": ["Do you have any tips?", "Any tips?"],
                },
            ],
            "quiz": [
                {
                    "key": "biggest_challenge",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["The biggest challenge is staying consistent.", "The biggest challenge staying consistent.", "Biggest challenge is consistent."],
                    "correct_answer": "The biggest challenge is staying consistent.",
                },
                {
                    "key": "hard_to",
                    "type": "multiple_choice",
                    "prompt": "What does \"It's hard to...\" mean?",
                    "options": ["susah untuk...", "mudah untuk...", "wajib untuk..."],
                    "correct_answer": "susah untuk...",
                },
                {
                    "key": "distracted_meaning",
                    "type": "multiple_choice",
                    "prompt": "What does \"distracted\" mean?",
                    "options": ["teralihkan", "termasuk", "terkunci"],
                    "correct_answer": "teralihkan",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_goals_discuss_challenges",
                "opening_line": "What's the biggest challenge?",
                "learner_goal": "Describe your challenge, give a reason, and ask for a tip.",
                "turns": [
                    {
                        "coach": "What's the biggest challenge?",
                        "hint": "Jawab dengan The biggest challenge is ...",
                        "sample_answer": "The biggest challenge is staying consistent after work.",
                        "focus": "Name the challenge",
                        "expected_keywords": ["challenge", "consistent"],
                    },
                    {
                        "coach": "Why is it hard?",
                        "hint": "Sebutkan satu alasan (distracted/tired).",
                        "sample_answer": "I get distracted by my phone, and I feel tired.",
                        "focus": "Explain the reason",
                        "expected_keywords": ["distracted", "tired"],
                    },
                    {
                        "coach": "Okay. What do you want to ask me?",
                        "hint": "Minta saran singkat.",
                        "sample_answer": "Do you have any tips?",
                        "focus": "Ask for a suggestion",
                        "expected_keywords": ["tips"],
                    },
                ],
                "target_phrases": ["The biggest challenge is ...", "It's hard to ...", "Do you have any tips?"],
            },
            "reading_support": "When discussing challenges, be clear: name the biggest challenge, give one reason, and ask for a simple suggestion.",
            "writing_support_lines": [
                "Write 4 lines:",
                "1. Honestly, it's been challenging.",
                "2. The biggest challenge is ...",
                "3. It's hard to ... because ...",
                "4. Do you have any tips?",
            ],
            "goal_examples": ["The biggest challenge is ...", "It's hard to ...", "Do you have any tips?"],
        },
        {
            "lesson_key": "lesson-04-making-next-step-plans",
            "slug": "making-next-step-plans",
            "title": "Making Next-step Plans",
            "conversation_situation": "making_next_step_learning_plan",
            "conversation_goal": "State your next step, set a simple schedule, and confirm the plan clearly.",
            "grammar_summary": "Use My next step is to... / I'm going to... / I'll do it ... times this week to plan next steps.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu bikin rencana langkah berikutnya. Kamu sebut next step, jadwal sederhana, dan konfirmasi plan-nya.",
            "dialogue": [
                ("Leo", "So what's your next step?"),
                ("Mina", "My next step is to practice with Conversation Coach."),
                ("Leo", "Nice. When will you do it?"),
                ("Mina", "I'll do it three times this week."),
                ("Leo", "Great. Which days?"),
                ("Mina", "Monday, Wednesday, and Friday."),
                ("Leo", "Sounds realistic."),
                ("Mina", "Yeah. I'm going to keep it simple."),
            ],
            "translations": [
                ("Leo", "So what's your next step?", "Jadi, next step kamu apa?"),
                ("Mina", "My next step is to practice with Conversation Coach.", "Next step aku adalah latihan pakai Conversation Coach."),
                ("Leo", "Nice. When will you do it?", "Oke. Kapan kamu lakukan?"),
                ("Mina", "I'll do it three times this week.", "Aku lakukan tiga kali minggu ini."),
                ("Leo", "Great. Which days?", "Oke. Hari apa aja?"),
                ("Mina", "Monday, Wednesday, and Friday.", "Senin, Rabu, dan Jumat."),
                ("Leo", "Sounds realistic.", "Kedengarannya realistis."),
                ("Mina", "Yeah. I'm going to keep it simple.", "Iya. Aku mau bikin simpel."),
            ],
            "useful_phrases": [
                {
                    "phrase": "My next step is to practice with Conversation Coach.",
                    "meaning_id": "Next step aku adalah latihan pakai Conversation Coach.",
                    "usage_note": "A clear next-step sentence.",
                    "common_mistake": 'Do not say "My next step to practice"; use is to.',
                },
                {
                    "phrase": "I'll do it three times this week.",
                    "meaning_id": "Aku lakukan tiga kali minggu ini.",
                    "usage_note": "A simple schedule commitment.",
                    "common_mistake": 'Do not say "three time"; add -s.',
                },
                {
                    "phrase": "I'm going to keep it simple.",
                    "meaning_id": "Aku mau bikin simpel.",
                    "usage_note": "A realistic planning phrase.",
                    "common_mistake": 'Do not say "I go to keep"; use I\'m going to.',
                },
                {
                    "phrase": "Let's set a simple plan.",
                    "meaning_id": "Yuk bikin rencana sederhana.",
                    "usage_note": "A friendly suggestion to plan together.",
                    "common_mistake": 'Do not say "Let\'s to set".',
                },
                {
                    "phrase": "That sounds realistic.",
                    "meaning_id": "Kedengarannya realistis.",
                    "usage_note": "Agree to a plan politely.",
                    "common_mistake": 'Do not say "That sound realistic"; add -s.',
                },
            ],
            "grammar_md": [
                ("My next step is to + verb", ["My next step is to practice with Conversation Coach.", "My next step is to review vocabulary."]),
                ("Times per week", ["I'll do it three times this week.", "I'll practice twice a week."]),
            ],
            "pronunciation": [
                ("next step", "NEKST step."),
                ("three times", "three TIMEZ."),
                ("realistic", "ree-uh-LIS-tik."),
            ],
            "response_prompts": [
                {
                    "prompt": "State your next step.",
                    "target_response": "My next step is to practice with Conversation Coach.",
                    "acceptable_variations": ["My next step is to practice with Conversation Coach.", "My next step is to practice speaking."],
                },
                {
                    "prompt": "Set a schedule (three times this week).",
                    "target_response": "I'll do it three times this week.",
                    "acceptable_variations": ["I'll do it three times this week.", "I'll do it twice this week."],
                },
                {
                    "prompt": "Confirm plan tone (keep it simple).",
                    "target_response": "I'm going to keep it simple.",
                    "acceptable_variations": ["I'm going to keep it simple.", "I'll keep it simple."],
                },
            ],
            "quiz": [
                {
                    "key": "next_step_sentence",
                    "type": "multiple_choice",
                    "prompt": "Which sentence states a next step?",
                    "options": ["My next step is to practice speaking.", "My next step practice speaking.", "Next step I practicing."],
                    "correct_answer": "My next step is to practice speaking.",
                },
                {
                    "key": "times_this_week",
                    "type": "multiple_choice",
                    "prompt": "What does \"three times this week\" mean?",
                    "options": ["tiga kali minggu ini", "tiga minggu", "tiga kali tiap bulan"],
                    "correct_answer": "tiga kali minggu ini",
                },
                {
                    "key": "going_to_usage",
                    "type": "multiple_choice",
                    "prompt": "Which sentence uses going to correctly?",
                    "options": ["I'm going to keep it simple.", "I going to keep it simple.", "I'm go to keep it simple."],
                    "correct_answer": "I'm going to keep it simple.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_goals_next_step_plan",
                "opening_line": "What's your next step?",
                "learner_goal": "State a next step and set a simple schedule.",
                "turns": [
                    {
                        "coach": "What's your next step?",
                        "hint": "Jawab dengan My next step is to ...",
                        "sample_answer": "My next step is to practice with Conversation Coach.",
                        "focus": "State next step",
                        "expected_keywords": ["next step", "to"],
                    },
                    {
                        "coach": "How often will you do it this week?",
                        "hint": "Jawab dengan ... times this week.",
                        "sample_answer": "I'll do it three times this week.",
                        "focus": "Set schedule",
                        "expected_keywords": ["times", "week"],
                    },
                    {
                        "coach": "Great. How will you keep it realistic?",
                        "hint": "Gunakan keep it simple.",
                        "sample_answer": "I'm going to keep it simple and do short sessions.",
                        "focus": "Keep the plan realistic",
                        "expected_keywords": ["keep", "simple"],
                    },
                ],
                "target_phrases": ["My next step is to ...", "I'll do it ... times this week.", "I'll keep it simple."],
            },
            "reading_support": "A good next-step plan is simple: state your next step, choose how often you will do it, and keep it realistic.",
            "writing_support_lines": [
                "Write 4 lines:",
                "1. My next step is to ...",
                "2. I'll do it ... times this week.",
                "3. Monday / Wednesday / Friday.",
                "4. I'll keep it simple.",
            ],
            "goal_examples": ["My next step is to ...", "I'll do it ... times this week.", "I'll keep it simple."],
        },
        {
            "lesson_key": "lesson-05-goals-progress-mission",
            "slug": "goals-progress-mission",
            "title": "Goals Progress Mission",
            "conversation_situation": "mission_goal_progress_challenge_next_step",
            "conversation_goal": "Complete a mini conversation: state a goal, share progress, describe a challenge, and set a next-step plan.",
            "grammar_summary": "Combine: My goal is to... / I've been... / The biggest challenge is... / My next step is to... to complete a goal update.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Misi: kamu cerita goal kamu, update progress, sebut tantangan, lalu bikin next step plan yang realistis.",
            "dialogue": [
                ("Leo", "What's your goal right now?"),
                ("Mina", "My goal is to speak more confidently by the end of this month."),
                ("Leo", "Nice. How's it going?"),
                ("Mina", "I'm making progress. I've been practicing every morning."),
                ("Leo", "Any challenges?"),
                ("Mina", "The biggest challenge is staying consistent after work. I get distracted by my phone."),
                ("Leo", "Got it. What's your next step?"),
                ("Mina", "My next step is to practice with Conversation Coach three times this week."),
            ],
            "translations": [
                ("Leo", "What's your goal right now?", "Goal kamu sekarang apa?"),
                ("Mina", "My goal is to speak more confidently by the end of this month.", "Goal aku adalah ngomong lebih pede paling lambat akhir bulan ini."),
                ("Leo", "Nice. How's it going?", "Oke. Gimana progressnya?"),
                ("Mina", "I'm making progress. I've been practicing every morning.", "Aku ada progress. Aku latihan tiap pagi."),
                ("Leo", "Any challenges?", "Ada tantangan?"),
                ("Mina", "The biggest challenge is staying consistent after work. I get distracted by my phone.", "Tantangan terbesarnya tetap konsisten setelah kerja. Aku gampang terdistraksi sama HP."),
                ("Leo", "Got it. What's your next step?", "Oke. Next step kamu apa?"),
                ("Mina", "My next step is to practice with Conversation Coach three times this week.", "Next step aku adalah latihan pakai Conversation Coach tiga kali minggu ini."),
            ],
            "useful_phrases": [
                {
                    "phrase": "My goal is to speak more confidently by the end of this month.",
                    "meaning_id": "Goal aku adalah ngomong lebih pede paling lambat akhir bulan ini.",
                    "usage_note": "Goal + deadline in one sentence.",
                    "common_mistake": "Do not skip the deadline; include by + time.",
                },
                {
                    "phrase": "I'm making progress. I've been practicing every morning.",
                    "meaning_id": "Aku ada progress. Aku latihan tiap pagi.",
                    "usage_note": "A short progress update.",
                    "common_mistake": "Avoid long explanations; keep it short.",
                },
                {
                    "phrase": "The biggest challenge is staying consistent after work.",
                    "meaning_id": "Tantangan terbesarnya tetap konsisten setelah kerja.",
                    "usage_note": "Name the challenge clearly.",
                    "common_mistake": 'Do not say "biggest challenge staying"; use is + verb-ing.',
                },
                {
                    "phrase": "I get distracted by my phone.",
                    "meaning_id": "Aku gampang terdistraksi sama HP.",
                    "usage_note": "Give one clear reason.",
                    "common_mistake": "Don't add too many reasons; one is enough.",
                },
                {
                    "phrase": "My next step is to practice three times this week.",
                    "meaning_id": "Next step aku adalah latihan tiga kali minggu ini.",
                    "usage_note": "Next step + schedule.",
                    "common_mistake": 'Do not say "three time"; add -s.',
                },
            ],
            "grammar_md": [
                ("Goal -> progress -> challenge -> next step", ["My goal is to ... by the end of ...", "I've been practicing ...", "The biggest challenge is ...", "My next step is to ..."]),
            ],
            "pronunciation": [
                ("by the end of", "by-the-END-of (link it)."),
                ("challenge", "CHAL-inj."),
                ("next step", "NEKST step."),
            ],
            "response_prompts": [
                {
                    "prompt": "State goal + deadline.",
                    "target_response": "My goal is to speak more confidently by the end of this month.",
                    "acceptable_variations": ["My goal is to speak more confidently by the end of this month.", "My goal is to speak more confidently by next month."],
                },
                {
                    "prompt": "Share progress with I've been practicing.",
                    "target_response": "I'm making progress. I've been practicing every morning.",
                    "acceptable_variations": ["I'm making progress. I've been practicing every morning.", "I'm making progress. I've been practicing every day."],
                },
                {
                    "prompt": "Name challenge + next step plan.",
                    "target_response": "The biggest challenge is staying consistent after work. My next step is to practice three times this week.",
                    "acceptable_variations": ["The biggest challenge is staying consistent after work. My next step is to practice three times this week.", "The biggest challenge is finding time. My next step is to practice twice this week."],
                },
            ],
            "quiz": [
                {
                    "key": "mission_order_goals",
                    "type": "multiple_choice",
                    "prompt": "Which order fits a goal update?",
                    "options": ["Goal -> progress -> challenge -> next step", "Greeting -> goodbye", "Food -> price -> color"],
                    "correct_answer": "Goal -> progress -> challenge -> next step",
                },
                {
                    "key": "consistent_meaning",
                    "type": "multiple_choice",
                    "prompt": "What does \"consistent\" mean?",
                    "options": ["konsisten", "terlambat", "acak"],
                    "correct_answer": "konsisten",
                },
                {
                    "key": "next_step_meaning",
                    "type": "multiple_choice",
                    "prompt": "What does \"next step\" mean?",
                    "options": ["langkah berikutnya", "langkah pertama", "langkah terakhir"],
                    "correct_answer": "langkah berikutnya",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_goals_mission",
                "opening_line": "What's your goal right now?",
                "learner_goal": "State your goal, share progress, describe a challenge, and set a next step.",
                "turns": [
                    {
                        "coach": "What's your goal right now?",
                        "hint": "Goal + deadline (by ...).",
                        "sample_answer": "My goal is to speak more confidently by the end of this month.",
                        "focus": "Goal with deadline",
                        "expected_keywords": ["goal", "by"],
                    },
                    {
                        "coach": "How's it going?",
                        "hint": "Progress + I've been practicing ...",
                        "sample_answer": "I'm making progress. I've been practicing every morning.",
                        "focus": "Progress update",
                        "expected_keywords": ["progress", "been"],
                    },
                    {
                        "coach": "Any challenges and next steps?",
                        "hint": "Challenge + next step plan.",
                        "sample_answer": "The biggest challenge is staying consistent after work. My next step is to practice three times this week.",
                        "focus": "Challenge and next step",
                        "expected_keywords": ["challenge", "next step", "times"],
                    },
                ],
                "target_phrases": ["My goal is to ...", "I've been practicing ...", "My next step is to ..."],
            },
            "reading_support": "This mission combines goal language, progress updates, challenges, and next-step planning in one short conversation.",
            "writing_support_lines": [
                "Write your mission (6 lines):",
                "1. My goal is to ... by the end of ...",
                "2. I'm making progress.",
                "3. I've been practicing ...",
                "4. The biggest challenge is ...",
                "5. I get distracted by ...",
                "6. My next step is to ... times this week.",
            ],
            "goal_examples": ["My goal is to ...", "I'm making progress.", "My next step is to ..."],
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
