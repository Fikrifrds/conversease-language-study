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
            "- Tone: professional, calm, clear",
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

        Read it again and underline the meeting words (agenda, scope, clarify, feedback, summarize, action items).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B2"
    b2_root = Path("content/curriculum/english/B2")
    units_root = b2_root / "units"
    unit_key = "unit-02-professional-meetings"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-02-professional-meetings
            level_code: B2
            title: Professional Meetings
            main_conversation_outcome: Participate actively and professionally in meetings.
            status: in_production
            lessons:
              - lesson-01-opening-a-meeting-point
              - lesson-02-clarifying-scope
              - lesson-03-giving-constructive-feedback
              - lesson-04-summarizing-decisions
              - lesson-05-meeting-participation-mission
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
            "lesson_key": "lesson-01-opening-a-meeting-point",
            "slug": "opening-a-meeting-point",
            "title": "Opening a Meeting Point",
            "conversation_situation": "opening_meeting_point",
            "conversation_goal": "Open a discussion point clearly, explain why it matters, and invite input.",
            "grammar_summary": "Use I'd like to bring up... / The main point is... / I'd like to hear your thoughts to open a meeting point professionally.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu lagi meeting. Kamu buka satu poin diskusi, jelasin kenapa penting, lalu minta pendapat tim.",
            "dialogue": [
                ("Mina", "I'd like to bring up the timeline for the next release."),
                ("Alex", "Sure. What's the main point?"),
                ("Mina", "The main point is we need to confirm the scope today."),
                ("Alex", "Why today?"),
                ("Mina", "Because the design handoff depends on it, and we don't want to block the team."),
                ("Alex", "Makes sense. What do you propose?"),
                ("Mina", "I'd like to hear your thoughts first, then we can decide."),
                ("Alex", "Okay. Let's hear from everyone."),
            ],
            "translations": [
                ("Mina", "I'd like to bring up the timeline for the next release.", "Aku mau bahas timeline untuk release berikutnya."),
                ("Alex", "Sure. What's the main point?", "Oke. Poin utamanya apa?"),
                ("Mina", "The main point is we need to confirm the scope today.", "Poin utamanya kita perlu konfirmasi scope hari ini."),
                ("Alex", "Why today?", "Kenapa harus hari ini?"),
                ("Mina", "Because the design handoff depends on it, and we don't want to block the team.", "Karena handoff design tergantung itu, dan kita nggak mau nge-block tim."),
                ("Alex", "Makes sense. What do you propose?", "Masuk akal. Kamu usul apa?"),
                ("Mina", "I'd like to hear your thoughts first, then we can decide.", "Aku pengen denger pendapat kalian dulu, lalu kita putuskan."),
                ("Alex", "Okay. Let's hear from everyone.", "Oke. Kita denger dari semua dulu."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'd like to bring up the timeline for the next release.",
                    "meaning_id": "Aku mau bahas timeline untuk release berikutnya.",
                    "usage_note": "A professional way to open a topic.",
                    "common_mistake": 'Do not say "I want bring up" in a meeting; use I\'d like to.',
                },
                {
                    "phrase": "The main point is we need to confirm the scope today.",
                    "meaning_id": "Poin utamanya kita perlu konfirmasi scope hari ini.",
                    "usage_note": "A clear main point sentence.",
                    "common_mistake": 'Do not say "The main point we need"; include is.',
                },
                {
                    "phrase": "Because the design handoff depends on it.",
                    "meaning_id": "Karena handoff design tergantung itu.",
                    "usage_note": "A clear reason sentence.",
                    "common_mistake": 'Do not say "depends to"; use depends on.',
                },
                {
                    "phrase": "I'd like to hear your thoughts.",
                    "meaning_id": "Aku pengen denger pendapat kamu/kalian.",
                    "usage_note": "Invite input politely.",
                    "common_mistake": 'Do not say "I want your thought"; use thoughts (plural).',
                },
                {
                    "phrase": "Let's hear from everyone.",
                    "meaning_id": "Yuk denger dari semua dulu.",
                    "usage_note": "A neutral facilitator phrase.",
                    "common_mistake": 'Do not say "Let\'s to hear"; use let\'s hear.',
                },
            ],
            "grammar_md": [
                ("Open a topic", ["I'd like to bring up the timeline.", "I'd like to bring up one concern."]),
                ("Invite input", ["I'd like to hear your thoughts.", "What are your thoughts on this?"]),
            ],
            "pronunciation": [
                ("timeline", "TIME-line."),
                ("scope", "SKOH-p."),
                ("handoff", "HAND-off."),
            ],
            "response_prompts": [
                {
                    "prompt": "Open a topic politely.",
                    "target_response": "I'd like to bring up the timeline for the next release.",
                    "acceptable_variations": [
                        "I'd like to bring up the timeline for the next release.",
                        "I'd like to bring up one concern about the schedule.",
                    ],
                },
                {
                    "prompt": "State the main point.",
                    "target_response": "The main point is we need to confirm the scope today.",
                    "acceptable_variations": [
                        "The main point is we need to confirm the scope today.",
                        "The main point is we need to decide today.",
                    ],
                },
                {
                    "prompt": "Invite input.",
                    "target_response": "I'd like to hear your thoughts.",
                    "acceptable_variations": ["I'd like to hear your thoughts.", "What are your thoughts on this?"],
                },
            ],
            "quiz": [
                {
                    "key": "bring_up_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "bring up" mean in a meeting?',
                    "options": ["membahas/menyampaikan topik", "membawa barang", "menutup meeting"],
                    "correct_answer": "membahas/menyampaikan topik",
                },
                {
                    "key": "depends_on",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct phrase.",
                    "options": ["depends on", "depends to", "depends at"],
                    "correct_answer": "depends on",
                },
                {
                    "key": "invite_input",
                    "type": "multiple_choice",
                    "prompt": "Which sentence invites input politely?",
                    "options": ["I'd like to hear your thoughts.", "Be quiet.", "Stop talking."],
                    "correct_answer": "I'd like to hear your thoughts.",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_meeting_open_topic",
                "opening_line": "Let's start. What would you like to bring up?",
                "learner_goal": "Open a topic, explain the main point, and invite input.",
                "turns": [
                    {
                        "coach": "What would you like to bring up?",
                        "hint": "Mulai dengan I'd like to bring up...",
                        "sample_answer": "I'd like to bring up the timeline for the next release.",
                        "focus": "Open a topic",
                        "expected_keywords": ["bring up", "timeline"],
                    },
                    {
                        "coach": "What's the main point?",
                        "hint": "Gunakan The main point is...",
                        "sample_answer": "The main point is we need to confirm the scope today.",
                        "focus": "State main point",
                        "expected_keywords": ["main point", "scope"],
                    },
                    {
                        "coach": "Invite input from the team.",
                        "hint": "Gunakan I'd like to hear your thoughts.",
                        "sample_answer": "I'd like to hear your thoughts first, then we can decide.",
                        "focus": "Invite input",
                        "expected_keywords": ["hear", "thoughts"],
                    },
                ],
                "target_phrases": ["I'd like to bring up ...", "The main point is ...", "I'd like to hear your thoughts."],
            },
            "reading_support": "To open a meeting point, introduce the topic, state the main point, explain why it matters, and invite input.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. I'd like to bring up ...",
                "2. The main point is ...",
                "3. Because ...",
                "4. I'd like to hear your thoughts.",
                "5. Then we can decide.",
                "6. Next steps are ...",
            ],
            "goal_examples": ["I'd like to bring up ...", "The main point is ...", "I'd like to hear your thoughts."],
        },
        {
            "lesson_key": "lesson-02-clarifying-scope",
            "slug": "clarifying-scope",
            "title": "Clarifying Scope",
            "conversation_situation": "clarifying_scope",
            "conversation_goal": "Clarify scope, ask what is included, and confirm what is out of scope.",
            "grammar_summary": "Use Just to clarify... / Does this include...? / Is ... out of scope? to avoid confusion.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu ingin scope jelas. Kamu tanya apa yang termasuk, apa yang tidak, dan konfirmasi biar nggak salah paham.",
            "dialogue": [
                ("Mina", "Just to clarify, what exactly is in scope for this sprint?"),
                ("Alex", "The core feature and the basic UI updates."),
                ("Mina", "Does this include the admin dashboard changes?"),
                ("Alex", "Not this sprint. That's out of scope for now."),
                ("Mina", "Got it. So we focus on the core feature only?"),
                ("Alex", "Yes, plus the UI updates for the main flow."),
                ("Mina", "Okay, thanks. I'll update the ticket list."),
                ("Alex", "Perfect."),
            ],
            "translations": [
                ("Mina", "Just to clarify, what exactly is in scope for this sprint?", "Biar jelas, yang termasuk scope sprint ini apa saja?"),
                ("Alex", "The core feature and the basic UI updates.", "Fitur utama dan update UI dasar."),
                ("Mina", "Does this include the admin dashboard changes?", "Termasuk perubahan admin dashboard juga?"),
                ("Alex", "Not this sprint. That's out of scope for now.", "Nggak untuk sprint ini. Itu di luar scope dulu."),
                ("Mina", "Got it. So we focus on the core feature only?", "Oke. Jadi kita fokus fitur utamanya saja?"),
                ("Alex", "Yes, plus the UI updates for the main flow.", "Iya, plus update UI untuk alur utama."),
                ("Mina", "Okay, thanks. I'll update the ticket list.", "Oke, makasih. Aku update daftar ticket-nya."),
                ("Alex", "Perfect.", "Sip."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Just to clarify, what exactly is in scope?",
                    "meaning_id": "Biar jelas, yang termasuk scope itu apa?",
                    "usage_note": "A polite way to ask for clarity.",
                    "common_mistake": 'Do not sound accusatory; use just to clarify to keep it neutral.',
                },
                {
                    "phrase": "Does this include the admin dashboard changes?",
                    "meaning_id": "Termasuk perubahan admin dashboard juga?",
                    "usage_note": "A direct scope-inclusion question.",
                    "common_mistake": 'Do not drop does in a question.',
                },
                {
                    "phrase": "That's out of scope for now.",
                    "meaning_id": "Itu di luar scope dulu.",
                    "usage_note": "A clear out-of-scope statement.",
                    "common_mistake": 'Do not say "out from scope"; use out of scope.',
                },
                {
                    "phrase": "Got it. So we focus on the core feature only?",
                    "meaning_id": "Oke. Jadi kita fokus fitur utama saja?",
                    "usage_note": "A confirmation question.",
                    "common_mistake": 'Do not confirm vaguely; repeat the key scope clearly.',
                },
                {
                    "phrase": "I'll update the ticket list.",
                    "meaning_id": "Aku akan update daftar ticket.",
                    "usage_note": "A practical next step.",
                    "common_mistake": 'Do not say "I will updating"; use I\'ll update.',
                },
            ],
            "grammar_md": [
                ("Just to clarify", ["Just to clarify, what is in scope?", "Just to clarify, do we need QA sign-off?"]),
                ("Include / out of scope", ["Does this include the dashboard changes?", "Is the admin flow out of scope?"]),
            ],
            "pronunciation": [
                ("clarify", "KLAIR-uh-fy."),
                ("exactly", "ig-ZAKT-lee."),
                ("scope", "SKOH-p."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask to clarify scope.",
                    "target_response": "Just to clarify, what exactly is in scope?",
                    "acceptable_variations": [
                        "Just to clarify, what exactly is in scope?",
                        "Just to clarify, what's in scope for this sprint?",
                    ],
                },
                {
                    "prompt": "Ask if something is included.",
                    "target_response": "Does this include the admin dashboard changes?",
                    "acceptable_variations": [
                        "Does this include the admin dashboard changes?",
                        "Does this include the reporting page?",
                    ],
                },
                {
                    "prompt": "Confirm out of scope.",
                    "target_response": "So that's out of scope for now, right?",
                    "acceptable_variations": ["So that's out of scope for now, right?", "Okay, so it's out of scope."],
                },
            ],
            "quiz": [
                {
                    "key": "out_of_scope",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct phrase.",
                    "options": ["out of scope", "out from scope", "out scope"],
                    "correct_answer": "out of scope",
                },
                {
                    "key": "clarify_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase asks for clarity politely?",
                    "options": ["Just to clarify, ...", "You didn't explain.", "Whatever."],
                    "correct_answer": "Just to clarify, ...",
                },
                {
                    "key": "include_question",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a correct include question?",
                    "options": [
                        "Does this include the admin changes?",
                        "This include the admin changes?",
                        "Is include admin changes?",
                    ],
                    "correct_answer": "Does this include the admin changes?",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_meeting_clarify_scope",
                "opening_line": "Let's clarify scope for this sprint.",
                "learner_goal": "Ask what is in scope, check if a specific item is included, and confirm what is out of scope.",
                "turns": [
                    {
                        "coach": "Ask what is in scope for this sprint.",
                        "hint": "Gunakan Just to clarify...",
                        "sample_answer": "Just to clarify, what exactly is in scope for this sprint?",
                        "focus": "Ask scope",
                        "expected_keywords": ["clarify", "in scope"],
                    },
                    {
                        "coach": "Ask if the admin dashboard is included.",
                        "hint": "Gunakan Does this include...?",
                        "sample_answer": "Does this include the admin dashboard changes?",
                        "focus": "Ask inclusion",
                        "expected_keywords": ["include", "admin"],
                    },
                    {
                        "coach": "Confirm what is out of scope and next step.",
                        "hint": "Use out of scope + I'll update...",
                        "sample_answer": "Got it. So that's out of scope for now. I'll update the ticket list.",
                        "focus": "Confirm + next step",
                        "expected_keywords": ["out of scope", "update"],
                    },
                ],
                "target_phrases": ["Just to clarify, ...", "Does this include ...?", "That's out of scope."],
            },
            "reading_support": "Clarifying scope prevents rework. Ask what is in scope, confirm what is out of scope, and summarize your understanding.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. Just to clarify, what's in scope?",
                "2. Does this include ...?",
                "3. Is ... out of scope?",
                "4. Got it. So we focus on ...",
                "5. I'll update ...",
                "6. Thanks.",
            ],
            "goal_examples": ["Just to clarify, ...", "Does this include ...?", "That's out of scope."],
        },
        {
            "lesson_key": "lesson-03-giving-constructive-feedback",
            "slug": "giving-constructive-feedback",
            "title": "Giving Constructive Feedback",
            "conversation_situation": "giving_constructive_feedback",
            "conversation_goal": "Give constructive feedback politely, focus on impact, and suggest one improvement.",
            "grammar_summary": "Use One suggestion is... / It might help if... / I noticed that... to give feedback professionally.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu kasih feedback ke rekan kerja. Kamu tetap sopan, jelasin dampaknya, lalu kasih satu saran perbaikan.",
            "dialogue": [
                ("Jordan", "How did the demo go? Any feedback?"),
                ("Mina", "Overall it was clear. I noticed the introduction was a bit long."),
                ("Jordan", "Oh, okay. What was the impact?"),
                ("Mina", "Some people lost focus, so the key message came late."),
                ("Jordan", "What would you suggest?"),
                ("Mina", "One suggestion is to start with the main takeaway, then show details."),
                ("Jordan", "That makes sense."),
                ("Mina", "It might help if you keep the intro under one minute."),
            ],
            "translations": [
                ("Jordan", "How did the demo go? Any feedback?", "Demo tadi gimana? Ada feedback?"),
                ("Mina", "Overall it was clear. I noticed the introduction was a bit long.", "Secara umum jelas. Aku perhatiin pembukaannya agak panjang."),
                ("Jordan", "Oh, okay. What was the impact?", "Oke. Dampaknya apa?"),
                ("Mina", "Some people lost focus, so the key message came late.", "Ada yang jadi kehilangan fokus, jadi pesan utamanya telat muncul."),
                ("Jordan", "What would you suggest?", "Kamu saranin apa?"),
                ("Mina", "One suggestion is to start with the main takeaway, then show details.", "Satu saran: mulai dari inti/pesan utama, lalu detailnya."),
                ("Jordan", "That makes sense.", "Masuk akal."),
                ("Mina", "It might help if you keep the intro under one minute.", "Mungkin membantu kalau pembukaannya di bawah satu menit."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Overall it was clear.",
                    "meaning_id": "Secara umum jelas.",
                    "usage_note": "Start feedback with something positive.",
                    "common_mistake": 'Do not start harshly; soften with overall.',
                },
                {
                    "phrase": "I noticed the introduction was a bit long.",
                    "meaning_id": "Aku perhatiin pembukaannya agak panjang.",
                    "usage_note": "A polite observation.",
                    "common_mistake": 'Do not say "You did wrong"; use I noticed.',
                },
                {
                    "phrase": "Some people lost focus, so the key message came late.",
                    "meaning_id": "Ada yang kehilangan fokus, jadi pesan utamanya telat muncul.",
                    "usage_note": "Explain impact with so.",
                    "common_mistake": 'Do not use because if it is a result; use so.',
                },
                {
                    "phrase": "One suggestion is to start with the main takeaway.",
                    "meaning_id": "Satu saran: mulai dari pesan utama.",
                    "usage_note": "A clear suggestion structure.",
                    "common_mistake": 'Do not say "one suggestion to start"; include is.',
                },
                {
                    "phrase": "It might help if you keep the intro under one minute.",
                    "meaning_id": "Mungkin membantu kalau pembukaannya di bawah satu menit.",
                    "usage_note": "A soft, constructive suggestion.",
                    "common_mistake": 'Do not sound like an order; use might help if.',
                },
            ],
            "grammar_md": [
                ("I noticed that...", ["I noticed the introduction was a bit long.", "I noticed the slides were hard to read."]),
                ("It might help if...", ["It might help if you start with the takeaway.", "It might help if you keep it shorter."]),
            ],
            "pronunciation": [
                ("overall", "OH-ver-awl."),
                ("takeaway", "TAYK-uh-way."),
                ("suggestion", "suh-JES-chun."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start feedback positively.",
                    "target_response": "Overall it was clear.",
                    "acceptable_variations": ["Overall it was clear.", "Overall, it went well."],
                },
                {
                    "prompt": "Make an observation with I noticed.",
                    "target_response": "I noticed the introduction was a bit long.",
                    "acceptable_variations": ["I noticed the introduction was a bit long.", "I noticed the pace was fast."],
                },
                {
                    "prompt": "Give one suggestion softly.",
                    "target_response": "It might help if you start with the main takeaway.",
                    "acceptable_variations": [
                        "It might help if you start with the main takeaway.",
                        "It might help if you keep the intro shorter.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "noticed_usage",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a polite observation?",
                    "options": ["I noticed the intro was a bit long.", "Your intro is bad.", "Stop talking."],
                    "correct_answer": "I noticed the intro was a bit long.",
                },
                {
                    "key": "might_help_if",
                    "type": "multiple_choice",
                    "prompt": "Which phrase gives a soft suggestion?",
                    "options": ["It might help if...", "You must...", "Do it now."],
                    "correct_answer": "It might help if...",
                },
                {
                    "key": "takeaway_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "takeaway" mean here?',
                    "options": ["pesan utama", "makanan dibungkus", "jalan pintas"],
                    "correct_answer": "pesan utama",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_meeting_feedback",
                "opening_line": "Any feedback on my demo?",
                "learner_goal": "Give constructive feedback: positive opener, observation, impact, and one suggestion.",
                "turns": [
                    {
                        "coach": "Any feedback on my demo?",
                        "hint": "Mulai positif + I noticed...",
                        "sample_answer": "Overall it was clear. I noticed the introduction was a bit long.",
                        "focus": "Positive + observation",
                        "expected_keywords": ["overall", "noticed"],
                    },
                    {
                        "coach": "What was the impact?",
                        "hint": "Jelaskan impact dengan so.",
                        "sample_answer": "Some people lost focus, so the key message came late.",
                        "focus": "Explain impact",
                        "expected_keywords": ["so", "message"],
                    },
                    {
                        "coach": "What would you suggest?",
                        "hint": "Gunakan One suggestion is... / It might help if...",
                        "sample_answer": "One suggestion is to start with the main takeaway. It might help if you keep the intro under one minute.",
                        "focus": "Give a suggestion",
                        "expected_keywords": ["suggestion", "might help"],
                    },
                ],
                "target_phrases": ["I noticed ...", "It might help if ...", "One suggestion is ..."],
            },
            "reading_support": "Constructive feedback is clear and respectful: start positive, describe what you noticed, explain the impact, and suggest one improvement.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. Overall, ...",
                "2. I noticed ...",
                "3. The impact was ...",
                "4. One suggestion is to ...",
                "5. It might help if ...",
                "6. Thanks for sharing.",
            ],
            "goal_examples": ["I noticed ...", "One suggestion is ...", "It might help if ..."],
        },
        {
            "lesson_key": "lesson-04-summarizing-decisions",
            "slug": "summarizing-decisions",
            "title": "Summarizing Decisions",
            "conversation_situation": "summarizing_meeting_decisions",
            "conversation_goal": "Summarize decisions clearly, confirm action items, and assign owners.",
            "grammar_summary": "Use To summarize... / We agreed to... / Action items are... / I'll take... to close meetings professionally.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Di akhir meeting kamu rangkum keputusan, sebut action items, dan jelas siapa yang ngerjain.",
            "dialogue": [
                ("Alex", "We're almost out of time."),
                ("Mina", "To summarize, we agreed to keep scope limited to the core feature."),
                ("Alex", "Right."),
                ("Mina", "Action items are: I'll update the tickets, and you'll confirm the design handoff."),
                ("Alex", "Yes. And Jordan will review QA coverage."),
                ("Mina", "Great. We'll check progress on Thursday."),
                ("Alex", "Thanks for summarizing."),
                ("Mina", "No problem."),
            ],
            "translations": [
                ("Alex", "We're almost out of time.", "Waktu kita hampir habis."),
                ("Mina", "To summarize, we agreed to keep scope limited to the core feature.", "Kesimpulannya, kita sepakat scope dibatasi ke fitur utama."),
                ("Alex", "Right.", "Iya."),
                ("Mina", "Action items are: I'll update the tickets, and you'll confirm the design handoff.", "Action items-nya: aku update ticket, dan kamu konfirmasi handoff design."),
                ("Alex", "Yes. And Jordan will review QA coverage.", "Iya. Dan Jordan review QA coverage."),
                ("Mina", "Great. We'll check progress on Thursday.", "Oke. Kita cek progress hari Kamis."),
                ("Alex", "Thanks for summarizing.", "Makasih sudah rangkum."),
                ("Mina", "No problem.", "Sama-sama."),
            ],
            "useful_phrases": [
                {
                    "phrase": "To summarize, we agreed to keep scope limited to the core feature.",
                    "meaning_id": "Kesimpulannya, kita sepakat scope dibatasi ke fitur utama.",
                    "usage_note": "A clear meeting close sentence.",
                    "common_mistake": 'Do not summarize vaguely; mention the key decision.',
                },
                {
                    "phrase": "Action items are: I'll update the tickets, and you'll confirm the design handoff.",
                    "meaning_id": "Action items-nya: aku update ticket, dan kamu konfirmasi handoff design.",
                    "usage_note": "Clear action items + owners.",
                    "common_mistake": 'Do not list actions without owners; assign who does what.',
                },
                {
                    "phrase": "Jordan will review QA coverage.",
                    "meaning_id": "Jordan akan review QA coverage.",
                    "usage_note": "Assign another owner.",
                    "common_mistake": 'Do not say "Jordan reviewing"; use will review.',
                },
                {
                    "phrase": "We'll check progress on Thursday.",
                    "meaning_id": "Kita cek progress hari Kamis.",
                    "usage_note": "Set the next checkpoint.",
                    "common_mistake": 'Do not forget the next checkpoint; set a day/time.',
                },
                {
                    "phrase": "Thanks for summarizing.",
                    "meaning_id": "Makasih sudah rangkum.",
                    "usage_note": "A polite closing line.",
                    "common_mistake": 'No common mistake; keep it simple.',
                },
            ],
            "grammar_md": [
                ("To summarize", ["To summarize, we agreed to ...", "To summarize, the decision is ..."]),
                ("Action items", ["Action items are: I'll ..., and you'll ...", "I'll take the first item."]),
            ],
            "pronunciation": [
                ("summarize", "SUM-uh-rise."),
                ("action items", "AK-shun EYE-tumz."),
                ("coverage", "KUV-er-ij."),
            ],
            "response_prompts": [
                {
                    "prompt": "Summarize the decision.",
                    "target_response": "To summarize, we agreed to keep scope limited to the core feature.",
                    "acceptable_variations": [
                        "To summarize, we agreed to keep scope limited to the core feature.",
                        "To summarize, we agreed to move updates to a written summary.",
                    ],
                },
                {
                    "prompt": "State action items with owners.",
                    "target_response": "Action items are: I'll update the tickets, and you'll confirm the design handoff.",
                    "acceptable_variations": [
                        "Action items are: I'll update the tickets, and you'll confirm the design handoff.",
                        "Action items are: I'll draft the doc, and you'll review it.",
                    ],
                },
                {
                    "prompt": "Set the next checkpoint.",
                    "target_response": "We'll check progress on Thursday.",
                    "acceptable_variations": ["We'll check progress on Thursday.", "We'll check progress next week."],
                },
            ],
            "quiz": [
                {
                    "key": "to_summarize_use",
                    "type": "multiple_choice",
                    "prompt": "Which phrase starts a meeting summary?",
                    "options": ["To summarize, ...", "By the way, ...", "Anyway, ..."],
                    "correct_answer": "To summarize, ...",
                },
                {
                    "key": "action_items_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What are "action items"?',
                    "options": ["tugas/aksi yang harus dilakukan", "topik lucu", "alat tulis"],
                    "correct_answer": "tugas/aksi yang harus dilakukan",
                },
                {
                    "key": "owner_importance",
                    "type": "multiple_choice",
                    "prompt": "Why assign owners for action items?",
                    "options": ["So it's clear who does what", "To make it longer", "To confuse people"],
                    "correct_answer": "So it's clear who does what",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_meeting_summarize",
                "opening_line": "We're out of time. Can you summarize?",
                "learner_goal": "Summarize decisions and action items with owners and a next checkpoint.",
                "turns": [
                    {
                        "coach": "Summarize the key decision.",
                        "hint": "Gunakan To summarize...",
                        "sample_answer": "To summarize, we agreed to keep scope limited to the core feature.",
                        "focus": "Summarize decision",
                        "expected_keywords": ["to summarize", "agreed"],
                    },
                    {
                        "coach": "List action items with owners.",
                        "hint": "Action items are: I'll..., you'll...",
                        "sample_answer": "Action items are: I'll update the tickets, and you'll confirm the design handoff.",
                        "focus": "Action items",
                        "expected_keywords": ["action items", "I'll", "you'll"],
                    },
                    {
                        "coach": "Set a next checkpoint.",
                        "hint": "We'll check progress on ...",
                        "sample_answer": "We'll check progress on Thursday.",
                        "focus": "Next checkpoint",
                        "expected_keywords": ["check progress"],
                    },
                ],
                "target_phrases": ["To summarize, ...", "Action items are ...", "We'll check progress on ..."],
            },
            "reading_support": "A good meeting close includes: a short summary of the decision, clear action items with owners, and the next checkpoint.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. To summarize, ...",
                "2. We agreed to ...",
                "3. Action items are: I'll ..., you'll ...",
                "4. Jordan will ...",
                "5. We'll check progress on ...",
                "6. Thanks everyone.",
            ],
            "goal_examples": ["To summarize, ...", "Action items are ...", "We'll check progress on ..."],
        },
        {
            "lesson_key": "lesson-05-meeting-participation-mission",
            "slug": "meeting-participation-mission",
            "title": "Meeting Participation Mission",
            "conversation_situation": "mission_professional_meeting",
            "conversation_goal": "Complete a mini meeting: open a point, clarify scope, give constructive feedback, and summarize decisions with action items.",
            "grammar_summary": "Combine: I'd like to bring up... / Just to clarify... / I noticed... / It might help if... / To summarize...",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Misi: kamu aktif di meeting secara profesional dari awal sampai rangkuman akhir.",
            "dialogue": [
                ("Alex", "Any topics to discuss today?"),
                ("Mina", "I'd like to bring up the timeline for the next release."),
                ("Alex", "Okay. Any scope questions?"),
                ("Mina", "Just to clarify, does this include the admin dashboard changes?"),
                ("Alex", "No, that's out of scope for now."),
                ("Alex", "Any feedback on the demo?"),
                ("Mina", "Overall it was clear. I noticed the introduction was a bit long, so the key message came late."),
                ("Mina", "To summarize, we agreed on the scope. Action items are: I'll update the tickets, and you'll confirm the design handoff."),
            ],
            "translations": [
                ("Alex", "Any topics to discuss today?", "Ada topik yang mau dibahas hari ini?"),
                ("Mina", "I'd like to bring up the timeline for the next release.", "Aku mau bahas timeline untuk release berikutnya."),
                ("Alex", "Okay. Any scope questions?", "Oke. Ada pertanyaan soal scope?"),
                ("Mina", "Just to clarify, does this include the admin dashboard changes?", "Biar jelas, termasuk perubahan admin dashboard juga?"),
                ("Alex", "No, that's out of scope for now.", "Nggak, itu di luar scope dulu."),
                ("Alex", "Any feedback on the demo?", "Ada feedback soal demo?"),
                ("Mina", "Overall it was clear. I noticed the introduction was a bit long, so the key message came late.", "Secara umum jelas. Aku perhatiin pembukaannya agak panjang, jadi pesan utamanya telat."),
                ("Mina", "To summarize, we agreed on the scope. Action items are: I'll update the tickets, and you'll confirm the design handoff.", "Kesimpulannya, kita sepakat soal scope. Action items-nya: aku update ticket, dan kamu konfirmasi handoff design."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'd like to bring up the timeline for the next release.",
                    "meaning_id": "Aku mau bahas timeline untuk release berikutnya.",
                    "usage_note": "Open a topic professionally.",
                    "common_mistake": "Don't ramble; state the topic clearly.",
                },
                {
                    "phrase": "Just to clarify, does this include the admin dashboard changes?",
                    "meaning_id": "Biar jelas, termasuk perubahan admin dashboard juga?",
                    "usage_note": "Clarify inclusion.",
                    "common_mistake": 'Do not forget does in a question.',
                },
                {
                    "phrase": "Overall it was clear. I noticed the introduction was a bit long.",
                    "meaning_id": "Secara umum jelas. Aku perhatiin pembukaannya agak panjang.",
                    "usage_note": "Constructive feedback structure.",
                    "common_mistake": "Don't sound personal; focus on the content.",
                },
                {
                    "phrase": "So the key message came late.",
                    "meaning_id": "Jadi pesan utamanya telat muncul.",
                    "usage_note": "Explain impact with so.",
                    "common_mistake": "Don't blame; just describe the impact.",
                },
                {
                    "phrase": "To summarize, action items are: I'll..., you'll...",
                    "meaning_id": "Kesimpulannya, action items-nya: aku..., kamu...",
                    "usage_note": "Close the meeting clearly.",
                    "common_mistake": "Always assign owners for action items.",
                },
            ],
            "grammar_md": [
                (
                    "Meeting participation flow",
                    [
                        "I'd like to bring up ...",
                        "Just to clarify, does this include ...?",
                        "Overall ... I noticed ...",
                        "To summarize, we agreed ... Action items are ...",
                    ],
                ),
            ],
            "pronunciation": [
                ("agenda", "uh-JEN-duh."),
                ("clarify", "KLAIR-uh-fy."),
                ("summarize", "SUM-uh-rise."),
            ],
            "response_prompts": [
                {
                    "prompt": "Open a topic.",
                    "target_response": "I'd like to bring up the timeline for the next release.",
                    "acceptable_variations": [
                        "I'd like to bring up the timeline for the next release.",
                        "I'd like to bring up one concern about scope.",
                    ],
                },
                {
                    "prompt": "Clarify scope inclusion.",
                    "target_response": "Just to clarify, does this include the admin dashboard changes?",
                    "acceptable_variations": [
                        "Just to clarify, does this include the admin dashboard changes?",
                        "Just to clarify, is the dashboard out of scope?",
                    ],
                },
                {
                    "prompt": "Summarize with action items.",
                    "target_response": "To summarize, action items are: I'll update the tickets, and you'll confirm the design handoff.",
                    "acceptable_variations": [
                        "To summarize, action items are: I'll update the tickets, and you'll confirm the design handoff.",
                        "To summarize, action items are: I'll draft the doc, and you'll review it.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "meeting_flow",
                    "type": "multiple_choice",
                    "prompt": "Which flow fits active meeting participation?",
                    "options": [
                        "Open topic -> clarify scope -> feedback -> summarize",
                        "Greeting -> goodbye",
                        "Food -> weather",
                    ],
                    "correct_answer": "Open topic -> clarify scope -> feedback -> summarize",
                },
                {
                    "key": "action_items_owner",
                    "type": "multiple_choice",
                    "prompt": "Why mention owners for action items?",
                    "options": ["So it's clear who does what", "To make it longer", "To avoid decisions"],
                    "correct_answer": "So it's clear who does what",
                },
                {
                    "key": "clarify_goal",
                    "type": "multiple_choice",
                    "prompt": 'Why say "Just to clarify"?',
                    "options": ["to avoid confusion", "to argue", "to end the meeting"],
                    "correct_answer": "to avoid confusion",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_meeting_mission",
                "opening_line": "Let's run a short meeting. Take the lead.",
                "learner_goal": "Lead a short meeting: open a point, clarify scope, give feedback, and summarize action items.",
                "turns": [
                    {
                        "coach": "Open a topic for today's meeting.",
                        "hint": "I'd like to bring up...",
                        "sample_answer": "I'd like to bring up the timeline for the next release.",
                        "focus": "Open topic",
                        "expected_keywords": ["bring up", "timeline"],
                    },
                    {
                        "coach": "Clarify scope and confirm what is out of scope.",
                        "hint": "Just to clarify... Does this include...? out of scope...",
                        "sample_answer": "Just to clarify, does this include the admin dashboard changes? If not, that's out of scope for now.",
                        "focus": "Clarify scope",
                        "expected_keywords": ["clarify", "include", "out of scope"],
                    },
                    {
                        "coach": "Give one feedback point and then summarize action items.",
                        "hint": "Overall... I noticed... To summarize... Action items are...",
                        "sample_answer": "Overall it was clear, but I noticed the intro was long. To summarize, action items are: I'll update the tickets, and you'll confirm the design handoff.",
                        "focus": "Feedback + summary",
                        "expected_keywords": ["noticed", "to summarize", "action items"],
                    },
                ],
                "target_phrases": ["I'd like to bring up ...", "Just to clarify, ...", "To summarize, ..."],
            },
            "reading_support": "Active meeting participation includes: introducing topics, clarifying scope, giving constructive feedback, and closing with clear decisions and action items.",
            "writing_support_lines": [
                "Write your mission (8 lines):",
                "1. I'd like to bring up ...",
                "2. The main point is ...",
                "3. Just to clarify, does this include ...?",
                "4. That's out of scope for now.",
                "5. Overall ... I noticed ...",
                "6. The impact is ..., so ...",
                "7. To summarize, we agreed ...",
                "8. Action items are: I'll ..., you'll ...",
            ],
            "goal_examples": ["I'd like to bring up ...", "Just to clarify, ...", "To summarize, ..."],
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
                "minimum_score": 72,
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
                "speaking": {"minimum_score": 72},
                "relevance": {"minimum_score": 72},
                "grammar": {"minimum_score": 68},
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

