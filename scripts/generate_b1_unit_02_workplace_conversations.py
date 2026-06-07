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

        Read it again and underline the polite workplace phrases.
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B1"
    b1_root = Path("content/curriculum/english/B1")
    units_root = b1_root / "units"
    unit_key = "unit-02-workplace-conversations"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-02-workplace-conversations
            level_code: B1
            title: Workplace Conversations
            main_conversation_outcome: Handle common workplace conversations with clear, polite language.
            status: in_production
            lessons:
              - lesson-01-explaining-your-task
              - lesson-02-asking-for-clarification
              - lesson-03-giving-a-short-update
              - lesson-04-joining-a-simple-meeting
              - lesson-05-workplace-mission
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
            "lesson_key": "lesson-01-explaining-your-task",
            "slug": "explaining-your-task",
            "title": "Explaining Your Task",
            "conversation_situation": "explaining_work_task_to_manager",
            "conversation_goal": "Explain what you are working on and what the next step is in a short, clear way.",
            "grammar_summary": "Use I am working on... / I am planning to... to explain your task and next step politely.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu ngobrol sama manager. Kamu jelaskan kamu lagi ngerjain apa dan langkah berikutnya.",
            "dialogue": [
                ("Alex", "Hi Mina. What are you working on today?"),
                ("Mina", "I'm working on the onboarding email flow."),
                ("Alex", "Great. What's the next step?"),
                ("Mina", "Next, I'll review the copy and update the templates."),
                ("Alex", "Sounds good. Any blockers?"),
                ("Mina", "Not right now, but I may need feedback later."),
                ("Alex", "Okay. Keep me posted."),
            ],
            "translations": [
                ("Alex", "Hi Mina. What are you working on today?", "Hai Mina. Kamu lagi ngerjain apa hari ini?"),
                ("Mina", "I'm working on the onboarding email flow.", "Aku lagi ngerjain alur email onboarding."),
                ("Alex", "Great. What's the next step?", "Oke. Langkah berikutnya apa?"),
                ("Mina", "Next, I'll review the copy and update the templates.", "Berikutnya, aku review teksnya dan update templatenya."),
                ("Alex", "Sounds good. Any blockers?", "Oke. Ada hambatan?"),
                ("Mina", "Not right now, but I may need feedback later.", "Belum ada sekarang, tapi nanti mungkin aku butuh feedback."),
                ("Alex", "Okay. Keep me posted.", "Oke. Kabari aku ya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'm working on the onboarding email flow.",
                    "meaning_id": "Aku lagi ngerjain alur email onboarding.",
                    "usage_note": "A clear status sentence for work.",
                    "common_mistake": 'Do not say "I working on"; use I\'m working on.',
                },
                {
                    "phrase": "What's the next step?",
                    "meaning_id": "Langkah berikutnya apa?",
                    "usage_note": "A common manager question.",
                    "common_mistake": 'Do not say "What is next step?" without the.',
                },
                {
                    "phrase": "Next, I'll review the copy.",
                    "meaning_id": "Berikutnya, aku review teksnya.",
                    "usage_note": "Use Next to structure your update.",
                    "common_mistake": 'Do not say "Next, I will reviewing".',
                },
                {
                    "phrase": "Any blockers?",
                    "meaning_id": "Ada hambatan?",
                    "usage_note": "A short workplace check question.",
                    "common_mistake": "Do not answer with a long story; just name one blocker or say none.",
                },
                {
                    "phrase": "Keep me posted.",
                    "meaning_id": "Kabari aku ya.",
                    "usage_note": "A polite closing at work.",
                    "common_mistake": 'Do not say "Keep me post".',
                },
            ],
            "grammar_md": [
                ("I am working on + noun", ["I'm working on the onboarding email flow.", "I'm working on the bug fix."]),
                ("Next, I will / I'll + verb", ["Next, I'll review the copy.", "Next, I'll update the template."]),
            ],
            "pronunciation": [
                ("working on", "WORK-ing on (link it)."),
                ("next step", "NEXT step."),
                ("keep me posted", "KEEP me POS-ted."),
            ],
            "response_prompts": [
                {
                    "prompt": "Say what you are working on.",
                    "target_response": "I'm working on the onboarding email flow.",
                    "acceptable_variations": ["I'm working on the onboarding email flow.", "I'm working on a bug fix."],
                },
                {
                    "prompt": "Say the next step (review copy).",
                    "target_response": "Next, I'll review the copy.",
                    "acceptable_variations": ["Next, I'll review the copy.", "Next, I'll update the templates."],
                },
                {
                    "prompt": "Answer: Any blockers?",
                    "target_response": "Not right now.",
                    "acceptable_variations": ["Not right now.", "No blockers right now."],
                },
            ],
            "quiz": [
                {
                    "key": "work_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a work status update?",
                    "options": ["I'm working on the onboarding email flow.", "I like emails.", "I'm sleep now."],
                    "correct_answer": "I'm working on the onboarding email flow.",
                },
                {
                    "key": "meaning_blocker",
                    "type": "multiple_choice",
                    "prompt": 'What does "blocker" mean at work?',
                    "options": ["hambatan", "liburan", "rapat"],
                    "correct_answer": "hambatan",
                },
                {
                    "key": "next_step",
                    "type": "multiple_choice",
                    "prompt": "Which phrase asks about the next action?",
                    "options": ["What's the next step?", "How was it?", "Where is it?"],
                    "correct_answer": "What's the next step?",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_work_explain_task",
                "opening_line": "Hi. What are you working on today?",
                "learner_goal": "Explain what you're working on, share the next step, and mention a blocker or say none.",
                "turns": [
                    {
                        "coach": "Hi. What are you working on today?",
                        "hint": "Jelaskan task kamu: I'm working on ...",
                        "sample_answer": "I'm working on the onboarding email flow.",
                        "focus": "State current task",
                        "expected_keywords": ["working on"],
                    },
                    {
                        "coach": "Great. What's the next step?",
                        "hint": "Gunakan Next, I'll ...",
                        "sample_answer": "Next, I'll review the copy and update the templates.",
                        "focus": "State next step",
                        "expected_keywords": ["next", "review"],
                    },
                    {
                        "coach": "Any blockers?",
                        "hint": "Jawab singkat (none / one blocker).",
                        "sample_answer": "Not right now, but I may need feedback later.",
                        "focus": "Mention blockers",
                        "expected_keywords": ["not", "feedback"],
                    },
                ],
                "target_phrases": ["I'm working on ...", "What's the next step?", "Any blockers?"],
            },
            "reading_support": "In workplace updates, it helps to say what you are working on, what the next step is, and whether you have any blockers.",
            "writing_support_lines": [
                "Write 4 connected sentences:",
                "1. I'm working on ...",
                "2. Next, I'll ...",
                "3. I don't have blockers right now.",
                "4. I'll keep you posted.",
            ],
            "goal_examples": ["I'm working on ...", "Next, I'll ...", "Any blockers?"],
        },
        {
            "lesson_key": "lesson-02-asking-for-clarification",
            "slug": "asking-for-clarification",
            "title": "Asking for Clarification",
            "conversation_situation": "asking_for_clarification_at_work",
            "conversation_goal": "Ask for clarification politely when you are not sure about a task.",
            "grammar_summary": "Use Could you clarify...?, Do you mean...?, and Just to confirm... to avoid mistakes.",
            "speakers": ("Alex", "Mina"),
            "situation_id": "Kamu dapat instruksi kerja. Kamu belum yakin, jadi kamu minta klarifikasi dengan sopan.",
            "dialogue": [
                ("Alex", "Can you update the report for Friday?"),
                ("Mina", "Sure. Could you clarify which sections you need?"),
                ("Alex", "Focus on the summary and the risks."),
                ("Mina", "Got it. Just to confirm, you want the latest numbers too, right?"),
                ("Alex", "Yes, please include the latest numbers."),
                ("Mina", "Okay. I'll send it by Thursday afternoon."),
                ("Alex", "Perfect. Thanks."),
            ],
            "translations": [
                ("Alex", "Can you update the report for Friday?", "Bisa update report untuk Jumat?"),
                ("Mina", "Sure. Could you clarify which sections you need?", "Bisa. Boleh jelasin bagian mana yang kamu butuh?"),
                ("Alex", "Focus on the summary and the risks.", "Fokus di ringkasan dan risiko."),
                ("Mina", "Got it. Just to confirm, you want the latest numbers too, right?", "Oke. Sekadar memastikan, kamu juga mau angka terbaru, ya?"),
                ("Alex", "Yes, please include the latest numbers.", "Iya, tolong masukin angka terbaru."),
                ("Mina", "Okay. I'll send it by Thursday afternoon.", "Oke. Aku kirim paling lambat Kamis sore."),
                ("Alex", "Perfect. Thanks.", "Sip. Makasih."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Could you clarify which sections you need?",
                    "meaning_id": "Boleh jelasin bagian mana yang kamu butuh?",
                    "usage_note": "A polite clarification question.",
                    "common_mistake": 'Do not say "Can you explain me".',
                },
                {
                    "phrase": "Just to confirm, you want the latest numbers too, right?",
                    "meaning_id": "Sekadar memastikan, kamu juga mau angka terbaru, ya?",
                    "usage_note": "Confirm details to avoid mistakes.",
                    "common_mistake": "Do not add too many confirmations; keep it short.",
                },
                {
                    "phrase": "Do you mean the summary or the full report?",
                    "meaning_id": "Maksudnya ringkasan atau report lengkap?",
                    "usage_note": "Do you mean helps clarify meaning.",
                    "common_mistake": 'Do not say "You mean?" without context.',
                },
                {
                    "phrase": "Got it.",
                    "meaning_id": "Oke, paham.",
                    "usage_note": "A natural confirmation of understanding.",
                    "common_mistake": 'Do not overuse it for every sentence.',
                },
                {
                    "phrase": "I'll send it by Thursday afternoon.",
                    "meaning_id": "Aku kirim paling lambat Kamis sore.",
                    "usage_note": "By + time means deadline.",
                    "common_mistake": 'Do not say "until Thursday"; use by for deadlines.',
                },
            ],
            "grammar_md": [
                ("Could you clarify...?", ["Could you clarify which sections you need?", "Could you clarify the deadline?"]),
                ("Just to confirm...", ["Just to confirm, you want the latest numbers, right?", "Just to confirm, this is for Friday, right?"]),
            ],
            "pronunciation": [
                ("clarify", "KLA-ri-fai."),
                ("just to confirm", "jus-ta con-FIRM (link it)."),
                ("by Thursday", "by THURS-day."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask for clarification about sections.",
                    "target_response": "Could you clarify which sections you need?",
                    "acceptable_variations": ["Could you clarify which sections you need?", "Could you clarify which part you need?"],
                },
                {
                    "prompt": "Confirm the latest numbers.",
                    "target_response": "Just to confirm, you want the latest numbers too, right?",
                    "acceptable_variations": [
                        "Just to confirm, you want the latest numbers too, right?",
                        "Just to confirm, you need the latest numbers, right?",
                    ],
                },
                {
                    "prompt": "Say the deadline (Thursday afternoon).",
                    "target_response": "I'll send it by Thursday afternoon.",
                    "acceptable_variations": ["I'll send it by Thursday afternoon.", "I'll send it by Thursday."],
                },
            ],
            "quiz": [
                {
                    "key": "clarify_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "clarify" mean?',
                    "options": ["memperjelas", "membatalkan", "menunda"],
                    "correct_answer": "memperjelas",
                },
                {
                    "key": "confirm_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase is for confirmation?",
                    "options": ["Just to confirm, ...", "Nice to meet you.", "See you."],
                    "correct_answer": "Just to confirm, ...",
                },
                {
                    "key": "deadline_by",
                    "type": "multiple_choice",
                    "prompt": 'What does "by Thursday" mean?',
                    "options": ["paling lambat Kamis", "mulai Kamis", "setiap Kamis"],
                    "correct_answer": "paling lambat Kamis",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_work_clarification",
                "opening_line": "Can you update the report for Friday?",
                "learner_goal": "Ask for clarification and confirm key details politely.",
                "turns": [
                    {
                        "coach": "Can you update the report for Friday?",
                        "hint": "Terima dulu, lalu minta klarifikasi.",
                        "sample_answer": "Sure. Could you clarify which sections you need?",
                        "focus": "Ask for clarification",
                        "expected_keywords": ["clarify", "sections"],
                    },
                    {
                        "coach": "Focus on the summary and the risks.",
                        "hint": "Konfirmasi satu detail penting.",
                        "sample_answer": "Got it. Just to confirm, you want the latest numbers too, right?",
                        "focus": "Confirm details",
                        "expected_keywords": ["confirm", "latest"],
                    },
                    {
                        "coach": "Yes, please include the latest numbers.",
                        "hint": "Janji deadline singkat.",
                        "sample_answer": "Okay. I'll send it by Thursday afternoon.",
                        "focus": "Confirm deadline",
                        "expected_keywords": ["send", "by"],
                    },
                ],
                "target_phrases": ["Could you clarify...?", "Just to confirm, ...", "I'll send it by ..."],
            },
            "reading_support": "When you're not sure at work, ask for clarification and confirm details. This helps you avoid mistakes and set a clear deadline.",
            "writing_support_lines": [
                "Write 4 sentences:",
                "1. Sure. Could you clarify ...?",
                "2. Got it.",
                "3. Just to confirm, ... right?",
                "4. I'll send it by ...",
            ],
            "goal_examples": ["Could you clarify...?", "Just to confirm, ...", "I'll send it by ..."],
        },
        {
            "lesson_key": "lesson-03-giving-a-short-update",
            "slug": "giving-a-short-update",
            "title": "Giving a Short Update",
            "conversation_situation": "giving_a_short_work_update",
            "conversation_goal": "Give a short work update with progress, a plan, and one risk or blocker.",
            "grammar_summary": "Use I'm making progress... / I'm almost done... and I might need... to give a clear update.",
            "speakers": ("Alex", "Mina"),
            "situation_id": "Kamu kasih update singkat ke manager: progress, rencana berikutnya, dan risiko kecil.",
            "dialogue": [
                ("Alex", "Quick update: how is the report going?"),
                ("Mina", "I'm making good progress. I'm almost done with the summary."),
                ("Alex", "Great. What's left?"),
                ("Mina", "I still need to update the risk section and double-check the numbers."),
                ("Alex", "Any concerns?"),
                ("Mina", "One concern is time. I might need an extra hour to review everything."),
                ("Alex", "Okay, thanks for the heads-up."),
            ],
            "translations": [
                ("Alex", "Quick update: how is the report going?", "Update cepat: gimana progres report-nya?"),
                ("Mina", "I'm making good progress. I'm almost done with the summary.", "Progresnya bagus. Hampir selesai bagian ringkasannya."),
                ("Alex", "Great. What's left?", "Oke. Sisa apa?"),
                ("Mina", "I still need to update the risk section and double-check the numbers.", "Aku masih perlu update bagian risiko dan cek lagi angkanya."),
                ("Alex", "Any concerns?", "Ada kekhawatiran?"),
                ("Mina", "One concern is time. I might need an extra hour to review everything.", "Satu concern soal waktu. Mungkin aku butuh tambahan satu jam buat review semuanya."),
                ("Alex", "Okay, thanks for the heads-up.", "Oke, makasih sudah ngasih tahu."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'm making good progress.",
                    "meaning_id": "Progresnya bagus.",
                    "usage_note": "A natural update phrase.",
                    "common_mistake": 'Do not say "I\'m progress".',
                },
                {
                    "phrase": "I'm almost done with the summary.",
                    "meaning_id": "Hampir selesai bagian ringkasannya.",
                    "usage_note": "Almost done indicates near completion.",
                    "common_mistake": 'Do not say "I\'m finish".',
                },
                {
                    "phrase": "What's left?",
                    "meaning_id": "Sisa apa?",
                    "usage_note": "A short follow-up question.",
                    "common_mistake": 'Do not say "What remaining?".',
                },
                {
                    "phrase": "I still need to double-check the numbers.",
                    "meaning_id": "Aku masih perlu cek lagi angkanya.",
                    "usage_note": "Double-check is common at work.",
                    "common_mistake": 'Do not say "double check again again".',
                },
                {
                    "phrase": "Thanks for the heads-up.",
                    "meaning_id": "Makasih sudah ngasih tahu.",
                    "usage_note": "A polite reaction to a warning.",
                    "common_mistake": 'Do not say "Thanks for head up".',
                },
            ],
            "grammar_md": [
                ("Progress + almost done", ["I'm making good progress.", "I'm almost done with the summary."]),
                ("I might need...", ["I might need an extra hour.", "I might need feedback from you."]),
            ],
            "pronunciation": [
                ("progress", "PRAH-gres."),
                ("almost done", "AL-most done."),
                ("heads-up", "HEDZ-up."),
            ],
            "response_prompts": [
                {
                    "prompt": "Say you're making good progress.",
                    "target_response": "I'm making good progress.",
                    "acceptable_variations": ["I'm making good progress.", "I'm making progress."],
                },
                {
                    "prompt": "Say what's left (risk + numbers).",
                    "target_response": "I still need to update the risk section and double-check the numbers.",
                    "acceptable_variations": [
                        "I still need to update the risk section and double-check the numbers.",
                        "I still need to double-check the numbers.",
                    ],
                },
                {
                    "prompt": "Mention one concern (time).",
                    "target_response": "One concern is time. I might need an extra hour.",
                    "acceptable_variations": ["One concern is time. I might need an extra hour.", "I might need a bit more time."],
                },
            ],
            "quiz": [
                {
                    "key": "almost_done",
                    "type": "multiple_choice",
                    "prompt": 'What does "almost done" mean?',
                    "options": ["hampir selesai", "baru mulai", "sudah lupa"],
                    "correct_answer": "hampir selesai",
                },
                {
                    "key": "double_check",
                    "type": "multiple_choice",
                    "prompt": 'What does "double-check" mean?',
                    "options": ["cek lagi", "hapus", "tanya ulang"],
                    "correct_answer": "cek lagi",
                },
                {
                    "key": "might_need",
                    "type": "multiple_choice",
                    "prompt": 'What does "I might need" express?',
                    "options": ["kemungkinan", "kepastian", "penolakan"],
                    "correct_answer": "kemungkinan",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_work_short_update",
                "opening_line": "Quick update: how is it going?",
                "learner_goal": "Give a short update: progress, what's left, and one concern.",
                "turns": [
                    {
                        "coach": "Quick update: how is it going?",
                        "hint": "Jawab dengan progress.",
                        "sample_answer": "I'm making good progress. I'm almost done with the summary.",
                        "focus": "Share progress",
                        "expected_keywords": ["progress", "almost"],
                    },
                    {
                        "coach": "Great. What's left?",
                        "hint": "Sebutkan 1-2 item yang tersisa.",
                        "sample_answer": "I still need to update the risk section and double-check the numbers.",
                        "focus": "Say what's left",
                        "expected_keywords": ["still need", "double-check"],
                    },
                    {
                        "coach": "Any concerns?",
                        "hint": "Sebutkan 1 concern dengan might need.",
                        "sample_answer": "One concern is time. I might need an extra hour to review everything.",
                        "focus": "Mention a concern",
                        "expected_keywords": ["concern", "might"],
                    },
                ],
                "target_phrases": ["I'm making progress.", "What's left?", "One concern is ..."],
            },
            "reading_support": "A good short update includes progress, what is left, and one risk or concern. This makes your communication clear and helpful.",
            "writing_support_lines": [
                "Write 4 lines:",
                "1. I'm making good progress.",
                "2. I'm almost done with ...",
                "3. I still need to ...",
                "4. One concern is ... (I might need ...)",
            ],
            "goal_examples": ["I'm making good progress.", "What's left?", "One concern is ..."],
        },
        {
            "lesson_key": "lesson-04-joining-a-simple-meeting",
            "slug": "joining-a-simple-meeting",
            "title": "Joining a Simple Meeting",
            "conversation_situation": "joining_a_short_meeting",
            "conversation_goal": "Join a simple meeting, state your point briefly, and ask for the next step.",
            "grammar_summary": "Use I'd like to add... / I suggest... / What are the next steps? for short meeting contributions.",
            "speakers": ("Alex", "Mina"),
            "situation_id": "Kamu ikut meeting singkat. Kamu tambahkan satu poin, lalu tanya next step.",
            "dialogue": [
                ("Alex", "Any updates before we close?"),
                ("Mina", "I'd like to add one point about the schedule."),
                ("Alex", "Sure, go ahead."),
                ("Mina", "I suggest we move the deadline to Thursday to reduce risk."),
                ("Alex", "That makes sense. Anything else?"),
                ("Mina", "No. What are the next steps?"),
                ("Alex", "We'll confirm the plan and share it with the team."),
            ],
            "translations": [
                ("Alex", "Any updates before we close?", "Ada update sebelum kita selesai?"),
                ("Mina", "I'd like to add one point about the schedule.", "Aku mau nambah satu poin soal jadwal."),
                ("Alex", "Sure, go ahead.", "Silakan."),
                ("Mina", "I suggest we move the deadline to Thursday to reduce risk.", "Aku saranin deadline-nya dimajuin ke Kamis supaya risikonya berkurang."),
                ("Alex", "That makes sense. Anything else?", "Masuk akal. Ada lagi?"),
                ("Mina", "No. What are the next steps?", "Nggak. Next step-nya apa?"),
                ("Alex", "We'll confirm the plan and share it with the team.", "Kita konfirmasi rencananya dan share ke tim."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'd like to add one point.",
                    "meaning_id": "Aku mau nambah satu poin.",
                    "usage_note": "A polite way to speak up in a meeting.",
                    "common_mistake": 'Do not say "I want add"; use I\'d like to add.',
                },
                {
                    "phrase": "Go ahead.",
                    "meaning_id": "Silakan.",
                    "usage_note": "A common meeting response.",
                    "common_mistake": "Do not overuse it; one time is enough.",
                },
                {
                    "phrase": "I suggest we move the deadline to Thursday.",
                    "meaning_id": "Aku saranin deadline-nya dimajuin ke Kamis.",
                    "usage_note": "A clear suggestion in a meeting.",
                    "common_mistake": 'Do not say "I suggestion".',
                },
                {
                    "phrase": "That makes sense.",
                    "meaning_id": "Masuk akal.",
                    "usage_note": "Agree politely with a point.",
                    "common_mistake": 'Do not say "That makes sens".',
                },
                {
                    "phrase": "What are the next steps?",
                    "meaning_id": "Next step-nya apa?",
                    "usage_note": "Ask for action items after discussion.",
                    "common_mistake": 'Do not say "What is next steps?"',
                },
            ],
            "grammar_md": [
                ("I'd like to + verb", ["I'd like to add one point.", "I'd like to ask a question."]),
                ("I suggest + sentence", ["I suggest we move the deadline.", "I suggest we review the risks."]),
            ],
            "pronunciation": [
                ("I'd like to", "I'd (one sound) LIKE-to."),
                ("suggest", "sug-JEST."),
                ("next steps", "NEXT steps."),
            ],
            "response_prompts": [
                {
                    "prompt": "Say you would like to add one point.",
                    "target_response": "I'd like to add one point about the schedule.",
                    "acceptable_variations": ["I'd like to add one point.", "I'd like to add one point about the schedule."],
                },
                {
                    "prompt": "Make a suggestion (move deadline).",
                    "target_response": "I suggest we move the deadline to Thursday.",
                    "acceptable_variations": ["I suggest we move the deadline to Thursday.", "I suggest we move the deadline earlier."],
                },
                {
                    "prompt": "Ask for next steps.",
                    "target_response": "What are the next steps?",
                    "acceptable_variations": ["What are the next steps?", "What should we do next?"],
                },
            ],
            "quiz": [
                {
                    "key": "meeting_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase is polite in a meeting?",
                    "options": ["I'd like to add one point.", "Listen to me!", "Stop talking."],
                    "correct_answer": "I'd like to add one point.",
                },
                {
                    "key": "meaning_go_ahead",
                    "type": "multiple_choice",
                    "prompt": 'What does "Go ahead" mean?',
                    "options": ["silakan lanjut", "berhenti", "pulang"],
                    "correct_answer": "silakan lanjut",
                },
                {
                    "key": "next_steps",
                    "type": "multiple_choice",
                    "prompt": "Which question asks for action items?",
                    "options": ["What are the next steps?", "How are you?", "Where is the office?"],
                    "correct_answer": "What are the next steps?",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_work_meeting",
                "opening_line": "Any updates before we close?",
                "learner_goal": "Add one point in a meeting, make a suggestion, and ask for the next steps.",
                "turns": [
                    {
                        "coach": "Any updates before we close?",
                        "hint": "Minta kesempatan bicara dengan sopan.",
                        "sample_answer": "I'd like to add one point about the schedule.",
                        "focus": "Speak up politely",
                        "expected_keywords": ["like to", "point"],
                    },
                    {
                        "coach": "Sure, go ahead.",
                        "hint": "Sampaikan saran singkat.",
                        "sample_answer": "I suggest we move the deadline to Thursday to reduce risk.",
                        "focus": "Give a suggestion",
                        "expected_keywords": ["suggest", "deadline"],
                    },
                    {
                        "coach": "That makes sense. Anything else?",
                        "hint": "Tutup dan tanya next step.",
                        "sample_answer": "No. What are the next steps?",
                        "focus": "Ask for next steps",
                        "expected_keywords": ["next steps"],
                    },
                ],
                "target_phrases": ["I'd like to add...", "I suggest...", "What are the next steps?"],
            },
            "reading_support": "In a simple meeting, you can add a point politely, make a short suggestion, and ask about next steps to stay aligned.",
            "writing_support_lines": [
                "Write 4 sentences:",
                "1. I'd like to add one point.",
                "2. I suggest we ...",
                "3. That makes sense.",
                "4. What are the next steps?",
            ],
            "goal_examples": ["I'd like to add...", "I suggest we ...", "What are the next steps?"],
        },
        {
            "lesson_key": "lesson-05-workplace-mission",
            "slug": "workplace-mission",
            "title": "Workplace Mission",
            "conversation_situation": "mission_work_update_and_clarification",
            "conversation_goal": "Complete a workplace mini-conversation: give an update, ask for clarification, and confirm a deadline.",
            "grammar_summary": "Combine workplace patterns: I'm working on..., Could you clarify...?, Just to confirm..., I'll send it by...",
            "speakers": ("Alex", "Mina"),
            "situation_id": "Misi: kamu kasih update kerja, minta klarifikasi, lalu konfirmasi deadline dengan jelas.",
            "dialogue": [
                ("Alex", "Hi Mina. Quick update on the report?"),
                ("Mina", "I'm making good progress. I'm almost done with the summary."),
                ("Alex", "Great. Please update the risk section too."),
                ("Mina", "Sure. Could you clarify which risks you want me to focus on?"),
                ("Alex", "Focus on timeline and budget risks."),
                ("Mina", "Got it. Just to confirm, you need it by Friday morning, right?"),
                ("Alex", "Yes. Please send it by Thursday afternoon if possible."),
            ],
            "translations": [
                ("Alex", "Hi Mina. Quick update on the report?", "Hai Mina. Update cepat soal report?"),
                ("Mina", "I'm making good progress. I'm almost done with the summary.", "Progresnya bagus. Hampir selesai ringkasannya."),
                ("Alex", "Great. Please update the risk section too.", "Oke. Tolong update bagian risiko juga."),
                ("Mina", "Sure. Could you clarify which risks you want me to focus on?", "Bisa. Boleh jelasin risiko mana yang harus aku fokuskan?"),
                ("Alex", "Focus on timeline and budget risks.", "Fokus di risiko timeline dan budget."),
                ("Mina", "Got it. Just to confirm, you need it by Friday morning, right?", "Oke. Sekadar memastikan, kamu butuhnya paling lambat Jumat pagi, ya?"),
                ("Alex", "Yes. Please send it by Thursday afternoon if possible.", "Iya. Kalau bisa, kirim paling lambat Kamis sore."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'm making good progress.",
                    "meaning_id": "Progresnya bagus.",
                    "usage_note": "Start the mission with a clear update.",
                    "common_mistake": "Do not jump to details without stating progress.",
                },
                {
                    "phrase": "Could you clarify which risks you want me to focus on?",
                    "meaning_id": "Boleh jelasin risiko mana yang harus aku fokuskan?",
                    "usage_note": "Clarify scope politely.",
                    "common_mistake": 'Do not say "Explain me"; use Could you clarify.',
                },
                {
                    "phrase": "Just to confirm, you need it by Friday morning, right?",
                    "meaning_id": "Sekadar memastikan, kamu butuhnya paling lambat Jumat pagi, ya?",
                    "usage_note": "Confirm deadline details.",
                    "common_mistake": "Keep confirmation short and specific.",
                },
                {
                    "phrase": "Please send it by Thursday afternoon if possible.",
                    "meaning_id": "Kalau bisa, kirim paling lambat Kamis sore.",
                    "usage_note": "By indicates a deadline; if possible softens the request.",
                    "common_mistake": 'Do not say "until Thursday"; use by.',
                },
                {
                    "phrase": "Got it.",
                    "meaning_id": "Oke, paham.",
                    "usage_note": "A natural short acknowledgement.",
                    "common_mistake": "Do not overuse; one time is enough.",
                },
            ],
            "grammar_md": [
                ("Update + clarification + confirmation", ["I'm making good progress.", "Could you clarify...?", "Just to confirm..., right?", "I'll send it by ..."]),
            ],
            "pronunciation": [
                ("focus on", "FO-kus on."),
                ("by Friday", "by FRI-day."),
                ("if possible", "if POS-uh-bul."),
            ],
            "response_prompts": [
                {
                    "prompt": "Give a short update (progress + almost done).",
                    "target_response": "I'm making good progress. I'm almost done with the summary.",
                    "acceptable_variations": [
                        "I'm making good progress. I'm almost done with the summary.",
                        "I'm making good progress. I'm almost done.",
                    ],
                },
                {
                    "prompt": "Ask for clarification about risks.",
                    "target_response": "Could you clarify which risks you want me to focus on?",
                    "acceptable_variations": [
                        "Could you clarify which risks you want me to focus on?",
                        "Could you clarify which risks are most important?",
                    ],
                },
                {
                    "prompt": "Confirm deadline (Friday morning).",
                    "target_response": "Just to confirm, you need it by Friday morning, right?",
                    "acceptable_variations": [
                        "Just to confirm, you need it by Friday morning, right?",
                        "Just to confirm, the deadline is Friday morning, right?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "mission_pattern",
                    "type": "multiple_choice",
                    "prompt": "Which sequence fits a workplace mission?",
                    "options": [
                        "Update progress -> clarify scope -> confirm deadline",
                        "Order food -> pay -> leave",
                        "Say hi -> leave",
                    ],
                    "correct_answer": "Update progress -> clarify scope -> confirm deadline",
                },
                {
                    "key": "meaning_focus_on",
                    "type": "multiple_choice",
                    "prompt": 'What does "focus on" mean?',
                    "options": ["fokus pada", "lupakan", "tutup"],
                    "correct_answer": "fokus pada",
                },
                {
                    "key": "meaning_by",
                    "type": "multiple_choice",
                    "prompt": 'What does "by Thursday afternoon" mean?',
                    "options": ["paling lambat Kamis sore", "mulai Kamis sore", "setiap Kamis sore"],
                    "correct_answer": "paling lambat Kamis sore",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_work_mission",
                "opening_line": "Hi. Quick update on the report?",
                "learner_goal": "Give an update, ask for clarification, and confirm a deadline politely.",
                "turns": [
                    {
                        "coach": "Hi. Quick update on the report?",
                        "hint": "Mulai dengan progress singkat.",
                        "sample_answer": "I'm making good progress. I'm almost done with the summary.",
                        "focus": "Give update",
                        "expected_keywords": ["progress", "almost"],
                    },
                    {
                        "coach": "Great. Please update the risk section too.",
                        "hint": "Terima, lalu minta klarifikasi scope.",
                        "sample_answer": "Sure. Could you clarify which risks you want me to focus on?",
                        "focus": "Ask clarification",
                        "expected_keywords": ["clarify", "focus"],
                    },
                    {
                        "coach": "Focus on timeline and budget risks.",
                        "hint": "Konfirmasi deadline singkat.",
                        "sample_answer": "Got it. Just to confirm, you need it by Friday morning, right?",
                        "focus": "Confirm deadline",
                        "expected_keywords": ["confirm", "by"],
                    },
                ],
                "target_phrases": ["I'm making good progress.", "Could you clarify...?", "Just to confirm..."],
            },
            "reading_support": "This mission combines workplace skills: a short update, a clarification question, and a clear deadline confirmation.",
            "writing_support_lines": [
                "Write your mission (5 lines):",
                "1. I'm making good progress.",
                "2. I'm almost done with ...",
                "3. Could you clarify ...?",
                "4. Got it.",
                "5. Just to confirm, ... right?",
            ],
            "goal_examples": ["I'm making good progress.", "Could you clarify...?", "Just to confirm, ... right?"],
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
