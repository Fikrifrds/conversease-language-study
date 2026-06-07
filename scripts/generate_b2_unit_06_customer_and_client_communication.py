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
            "- Tone: professional, empathetic, clear",
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

        Read it again and underline the client words (needs, requirements, options, concern, timeline, next steps).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B2"
    b2_root = Path("content/curriculum/english/B2")
    units_root = b2_root / "units"
    unit_key = "unit-06-customer-and-client-communication"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-06-customer-and-client-communication
            level_code: B2
            title: Customer & Client Communication
            main_conversation_outcome: Handle client conversations with clarity, empathy, and professionalism.
            status: in_production
            lessons:
              - lesson-01-understanding-client-needs
              - lesson-02-explaining-options
              - lesson-03-handling-concerns
              - lesson-04-confirming-next-steps
              - lesson-05-client-conversation-mission
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
            "lesson_key": "lesson-01-understanding-client-needs",
            "slug": "understanding-client-needs",
            "title": "Understanding Client Needs",
            "conversation_situation": "client_needs_discovery",
            "conversation_goal": "Ask clarifying questions to understand client needs, confirm requirements, and summarize what you heard.",
            "grammar_summary": "Use Just to clarify... / Could you share more about... / So what you need is... to understand clients clearly.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu ngobrol sama klien. Kamu gali kebutuhan, tanya detail, lalu rangkum supaya nggak salah paham.",
            "dialogue": [
                ("Jordan", "We want to improve our onboarding experience."),
                ("Mina", "Got it. Just to clarify, who is the main user group?"),
                ("Jordan", "Mostly new hires in engineering."),
                ("Mina", "Thanks. Could you share more about the biggest pain point today?"),
                ("Jordan", "They don't know where to find key docs."),
                ("Mina", "Understood. So what you need is a clear starting point and a simple checklist, right?"),
                ("Jordan", "Exactly."),
                ("Mina", "Great. I'll summarize the requirements and share a proposal."),
            ],
            "translations": [
                ("Jordan", "We want to improve our onboarding experience.", "Kami ingin improve pengalaman onboarding."),
                ("Mina", "Got it. Just to clarify, who is the main user group?", "Oke. Biar jelas, siapa user utama-nya?"),
                ("Jordan", "Mostly new hires in engineering.", "Kebanyakan orang baru di engineering."),
                ("Mina", "Thanks. Could you share more about the biggest pain point today?", "Makasih. Bisa share lebih detail pain point terbesarnya sekarang?"),
                ("Jordan", "They don't know where to find key docs.", "Mereka nggak tahu di mana cari dokumen penting."),
                ("Mina", "Understood. So what you need is a clear starting point and a simple checklist, right?", "Oke. Jadi yang dibutuhkan adalah starting point yang jelas dan checklist sederhana, bener?"),
                ("Jordan", "Exactly.", "Iya."),
                ("Mina", "Great. I'll summarize the requirements and share a proposal.", "Oke. Aku rangkum requirement-nya dan share proposal."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Just to clarify, who is the main user group?",
                    "meaning_id": "Biar jelas, siapa user utama-nya?",
                    "usage_note": "A professional clarification question.",
                    "common_mistake": 'Do not ask vaguely; ask about the user group.',
                },
                {
                    "phrase": "Could you share more about the biggest pain point?",
                    "meaning_id": "Bisa share lebih detail pain point terbesarnya?",
                    "usage_note": "A polite question to get specifics.",
                    "common_mistake": 'Do not say "Can you share me"; use share more about.',
                },
                {
                    "phrase": "So what you need is a clear starting point, right?",
                    "meaning_id": "Jadi yang kamu butuh adalah starting point yang jelas, bener?",
                    "usage_note": "A confirmation summary.",
                    "common_mistake": 'Do not confirm vaguely; repeat the key need.',
                },
                {
                    "phrase": "I'll summarize the requirements and share a proposal.",
                    "meaning_id": "Aku rangkum requirement-nya dan share proposal.",
                    "usage_note": "A clear next step.",
                    "common_mistake": 'Do not say "I will summarizing"; use I\'ll summarize.',
                },
                {
                    "phrase": "Got it. Understood.",
                    "meaning_id": "Oke. Paham.",
                    "usage_note": "Professional listening signals.",
                    "common_mistake": 'Do not overuse; use once per section.',
                },
            ],
            "grammar_md": [
                ("Clarifying questions", ["Just to clarify, ...", "Could you share more about ...?"]),
                ("Summary confirmation", ["So what you need is ..., right?", "So the key requirement is ..., correct?"]),
            ],
            "pronunciation": [
                ("requirements", "ri-KWYER-munts."),
                ("clarify", "KLAIR-uh-fy."),
                ("pain point", "PAYN point."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask a clarification question.",
                    "target_response": "Just to clarify, who is the main user group?",
                    "acceptable_variations": [
                        "Just to clarify, who is the main user group?",
                        "Just to clarify, what is in scope?",
                    ],
                },
                {
                    "prompt": "Ask for more detail.",
                    "target_response": "Could you share more about the biggest pain point?",
                    "acceptable_variations": [
                        "Could you share more about the biggest pain point?",
                        "Could you share more about your timeline?",
                    ],
                },
                {
                    "prompt": "Summarize the need and confirm.",
                    "target_response": "So what you need is a clear starting point and a checklist, right?",
                    "acceptable_variations": [
                        "So what you need is a clear starting point and a checklist, right?",
                        "So what you need is faster onboarding, right?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "clarify_client",
                    "type": "multiple_choice",
                    "prompt": "Which phrase asks to clarify professionally?",
                    "options": ["Just to clarify, ...", "You are unclear.", "Explain now."],
                    "correct_answer": "Just to clarify, ...",
                },
                {
                    "key": "share_more",
                    "type": "multiple_choice",
                    "prompt": "Which sentence asks for more detail politely?",
                    "options": [
                        "Could you share more about the biggest pain point?",
                        "Tell me everything.",
                        "Why are you complaining?",
                    ],
                    "correct_answer": "Could you share more about the biggest pain point?",
                },
                {
                    "key": "requirements_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "requirements" mean?',
                    "options": ["kebutuhan/requirement", "hadiah", "liburan"],
                    "correct_answer": "kebutuhan/requirement",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_client_needs",
                "opening_line": "We want to improve our product experience.",
                "learner_goal": "Ask clarifying questions and summarize the client needs.",
                "turns": [
                    {
                        "coach": "We want to improve our product experience.",
                        "hint": "Mulai dengan pertanyaan klarifikasi (Just to clarify...).",
                        "sample_answer": "Got it. Just to clarify, who is the main user group?",
                        "focus": "Clarify user group",
                        "expected_keywords": ["clarify", "user"],
                    },
                    {
                        "coach": "The main users are new hires. What's next?",
                        "hint": "Minta detail pain point.",
                        "sample_answer": "Thanks. Could you share more about the biggest pain point today?",
                        "focus": "Ask for pain point",
                        "expected_keywords": ["share more", "pain point"],
                    },
                    {
                        "coach": "They can't find key docs. Summarize and confirm.",
                        "hint": "So what you need is ... right?",
                        "sample_answer": "Understood. So what you need is a clear starting point and a simple checklist, right?",
                        "focus": "Summarize need",
                        "expected_keywords": ["need", "right"],
                    },
                ],
                "target_phrases": ["Just to clarify, ...", "Could you share more about ...?", "So what you need is ..."],
            },
            "reading_support": "Client discovery focuses on clarity. Ask who the users are, what the pain point is, then summarize the requirement in one sentence and confirm it.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. Just to clarify, ...",
                "2. Who is the main user group?",
                "3. Could you share more about ...?",
                "4. So what you need is ...",
                "5. Right?",
                "6. I'll summarize the requirements and share a proposal.",
            ],
            "goal_examples": ["Just to clarify, ...", "Could you share more about ...?", "So what you need is ..."],
        },
        {
            "lesson_key": "lesson-02-explaining-options",
            "slug": "explaining-options",
            "title": "Explaining Options",
            "conversation_situation": "explaining_options_to_client",
            "conversation_goal": "Explain two options clearly, compare trade-offs, and recommend one option.",
            "grammar_summary": "Use We have two options... / Option A would... / The trade-off is... / I'd recommend... to explain options clearly.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu jelasin dua opsi solusi ke klien. Kamu bandingin trade-off-nya dan kasih rekomendasi.",
            "dialogue": [
                ("Jordan", "What are our options?"),
                ("Mina", "We have two options. Option A is a quick fix we can deliver this week."),
                ("Jordan", "And option B?"),
                ("Mina", "Option B is a more robust solution, but it takes two more weeks."),
                ("Jordan", "What's the trade-off?"),
                ("Mina", "The trade-off is speed versus long-term stability."),
                ("Jordan", "What do you recommend?"),
                ("Mina", "I'd recommend option B if the timeline allows."),
            ],
            "translations": [
                ("Jordan", "What are our options?", "Opsi kita apa aja?"),
                ("Mina", "We have two options. Option A is a quick fix we can deliver this week.", "Kita punya dua opsi. Opsi A quick fix yang bisa kita deliver minggu ini."),
                ("Jordan", "And option B?", "Kalau opsi B?"),
                ("Mina", "Option B is a more robust solution, but it takes two more weeks.", "Opsi B solusi yang lebih robust, tapi butuh dua minggu lagi."),
                ("Jordan", "What's the trade-off?", "Trade-off-nya apa?"),
                ("Mina", "The trade-off is speed versus long-term stability.", "Trade-off-nya kecepatan versus stabilitas jangka panjang."),
                ("Jordan", "What do you recommend?", "Kamu rekomendasiin yang mana?"),
                ("Mina", "I'd recommend option B if the timeline allows.", "Aku rekomendasi opsi B kalau timeline memungkinkan."),
            ],
            "useful_phrases": [
                {
                    "phrase": "We have two options.",
                    "meaning_id": "Kita punya dua opsi.",
                    "usage_note": "A clear option opener.",
                    "common_mistake": 'Do not say "two option"; add -s.',
                },
                {
                    "phrase": "Option A is a quick fix we can deliver this week.",
                    "meaning_id": "Opsi A quick fix yang bisa kita deliver minggu ini.",
                    "usage_note": "A concise option description.",
                    "common_mistake": 'Do not over-explain; one sentence per option.',
                },
                {
                    "phrase": "Option B is more robust, but it takes two more weeks.",
                    "meaning_id": "Opsi B lebih robust, tapi butuh dua minggu lagi.",
                    "usage_note": "Option + contrast with but.",
                    "common_mistake": 'Do not say "more robust but takes"; include it.',
                },
                {
                    "phrase": "The trade-off is speed versus long-term stability.",
                    "meaning_id": "Trade-off-nya kecepatan versus stabilitas jangka panjang.",
                    "usage_note": "Explain trade-offs clearly.",
                    "common_mistake": 'Do not say "trade off"; keep it as trade-off as a concept.',
                },
                {
                    "phrase": "I'd recommend option B if the timeline allows.",
                    "meaning_id": "Aku rekomendasi opsi B kalau timeline memungkinkan.",
                    "usage_note": "A professional recommendation.",
                    "common_mistake": 'Do not force; use if the timeline allows.',
                },
            ],
            "grammar_md": [
                ("Option structure", ["We have two options: A or B.", "Option A is ..., but ..."]),
                ("Recommendation", ["I'd recommend option B if the timeline allows.", "I'd recommend starting with a pilot."]),
            ],
            "pronunciation": [
                ("trade-off", "TRAYD-off."),
                ("robust", "roh-BUST."),
                ("stability", "stuh-BIL-i-tee."),
            ],
            "response_prompts": [
                {
                    "prompt": "Introduce two options.",
                    "target_response": "We have two options.",
                    "acceptable_variations": ["We have two options.", "We have two main options."],
                },
                {
                    "prompt": "Explain the trade-off.",
                    "target_response": "The trade-off is speed versus long-term stability.",
                    "acceptable_variations": [
                        "The trade-off is speed versus long-term stability.",
                        "The trade-off is cost versus quality.",
                    ],
                },
                {
                    "prompt": "Make a recommendation politely.",
                    "target_response": "I'd recommend option B if the timeline allows.",
                    "acceptable_variations": [
                        "I'd recommend option B if the timeline allows.",
                        "I'd recommend option A if you need it this week.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "two_options",
                    "type": "multiple_choice",
                    "prompt": "Which sentence introduces options clearly?",
                    "options": ["We have two options.", "Two option we have.", "Have two option."],
                    "correct_answer": "We have two options.",
                },
                {
                    "key": "tradeoff_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "trade-off" mean?',
                    "options": ["kompromi antara dua hal", "janji", "target"],
                    "correct_answer": "kompromi antara dua hal",
                },
                {
                    "key": "recommend_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase gives a recommendation politely?",
                    "options": ["I'd recommend ...", "You must ...", "Do it now."],
                    "correct_answer": "I'd recommend ...",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_client_options",
                "opening_line": "Can you explain our options?",
                "learner_goal": "Explain options, trade-offs, and a recommendation.",
                "turns": [
                    {
                        "coach": "Can you explain our options?",
                        "hint": "Mulai dengan We have two options.",
                        "sample_answer": "We have two options. Option A is a quick fix we can deliver this week.",
                        "focus": "Option A",
                        "expected_keywords": ["two options", "option a"],
                    },
                    {
                        "coach": "And option B?",
                        "hint": "Option B is..., but it takes...",
                        "sample_answer": "Option B is a more robust solution, but it takes two more weeks.",
                        "focus": "Option B",
                        "expected_keywords": ["option b", "but"],
                    },
                    {
                        "coach": "Explain the trade-off and recommend one.",
                        "hint": "The trade-off is... I'd recommend...",
                        "sample_answer": "The trade-off is speed versus long-term stability. I'd recommend option B if the timeline allows.",
                        "focus": "Trade-off + recommendation",
                        "expected_keywords": ["trade-off", "recommend"],
                    },
                ],
                "target_phrases": ["We have two options.", "The trade-off is ...", "I'd recommend ..."],
            },
            "reading_support": "When explaining options to a client, keep it structured: option A, option B, trade-off, and a recommendation based on priorities.",
            "writing_support_lines": [
                "Write 7 lines:",
                "1. We have two options.",
                "2. Option A is ...",
                "3. Option B is ..., but ...",
                "4. The trade-off is ...",
                "5. If your priority is speed, ...",
                "6. I'd recommend ...",
                "7. Would that work for you?",
            ],
            "goal_examples": ["We have two options.", "The trade-off is ...", "I'd recommend ..."],
        },
        {
            "lesson_key": "lesson-03-handling-concerns",
            "slug": "handling-concerns",
            "title": "Handling Concerns",
            "conversation_situation": "handling_client_concerns",
            "conversation_goal": "Acknowledge a client concern, ask a clarifying question, and propose a mitigation plan.",
            "grammar_summary": "Use I understand the concern / Could you clarify... / To reduce the risk, we can... to respond professionally.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Klien punya kekhawatiran. Kamu respon dengan empati, tanya detail, lalu kasih mitigasi.",
            "dialogue": [
                ("Jordan", "I'm concerned this change will disrupt our team."),
                ("Mina", "I understand the concern. Could you clarify what disruption you expect?"),
                ("Jordan", "People might miss updates."),
                ("Mina", "That makes sense. To reduce the risk, we can send a weekly summary and keep a monthly live meeting."),
                ("Jordan", "Okay, that helps."),
                ("Mina", "We can also run a two-week trial and gather feedback."),
                ("Jordan", "Sounds reasonable."),
                ("Mina", "Great. I'll share a draft plan today."),
            ],
            "translations": [
                ("Jordan", "I'm concerned this change will disrupt our team.", "Aku khawatir perubahan ini bakal mengganggu tim kita."),
                ("Mina", "I understand the concern. Could you clarify what disruption you expect?", "Aku paham kekhawatirannya. Bisa jelasin gangguan seperti apa yang kamu bayangin?"),
                ("Jordan", "People might miss updates.", "Orang mungkin kelewatan update."),
                ("Mina", "That makes sense. To reduce the risk, we can send a weekly summary and keep a monthly live meeting.", "Masuk akal. Untuk ngurangin risiko, kita bisa kirim ringkasan mingguan dan tetap adain meeting live bulanan."),
                ("Jordan", "Okay, that helps.", "Oke, itu membantu."),
                ("Mina", "We can also run a two-week trial and gather feedback.", "Kita juga bisa coba dua minggu dan kumpulin feedback."),
                ("Jordan", "Sounds reasonable.", "Kedengarannya masuk akal."),
                ("Mina", "Great. I'll share a draft plan today.", "Oke. Aku share draft plan hari ini."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I understand the concern.",
                    "meaning_id": "Aku paham kekhawatirannya.",
                    "usage_note": "A respectful opener.",
                    "common_mistake": 'Do not dismiss the concern; acknowledge first.',
                },
                {
                    "phrase": "Could you clarify what disruption you expect?",
                    "meaning_id": "Bisa jelasin gangguan seperti apa yang kamu bayangin?",
                    "usage_note": "A calm clarifying question.",
                    "common_mistake": 'Do not ask aggressively; keep tone neutral.',
                },
                {
                    "phrase": "To reduce the risk, we can send a weekly summary.",
                    "meaning_id": "Untuk ngurangin risiko, kita bisa kirim ringkasan mingguan.",
                    "usage_note": "Mitigation language.",
                    "common_mistake": 'Do not say "reduce risk we can"; keep the structure.',
                },
                {
                    "phrase": "We can run a two-week trial and gather feedback.",
                    "meaning_id": "Kita bisa coba dua minggu dan kumpulin feedback.",
                    "usage_note": "A practical risk-reduction step.",
                    "common_mistake": 'Do not propose a huge rollout immediately; suggest a trial.',
                },
                {
                    "phrase": "I'll share a draft plan today.",
                    "meaning_id": "Aku share draft plan hari ini.",
                    "usage_note": "Clear next step.",
                    "common_mistake": 'Do not say "I will sharing"; use I\'ll share.',
                },
            ],
            "grammar_md": [
                ("Concern handling", ["I understand the concern.", "Could you clarify ...?"]),
                ("Mitigation", ["To reduce the risk, we can ...", "We can run a short trial and gather feedback."]),
            ],
            "pronunciation": [
                ("disrupt", "dis-RUPT."),
                ("mitigate", "MIT-i-gayt."),
                ("weekly", "WEEK-lee."),
            ],
            "response_prompts": [
                {
                    "prompt": "Acknowledge the concern.",
                    "target_response": "I understand the concern.",
                    "acceptable_variations": ["I understand the concern.", "I understand your concern."],
                },
                {
                    "prompt": "Ask a clarifying question.",
                    "target_response": "Could you clarify what disruption you expect?",
                    "acceptable_variations": [
                        "Could you clarify what disruption you expect?",
                        "Could you clarify what your main worry is?",
                    ],
                },
                {
                    "prompt": "Offer mitigation.",
                    "target_response": "To reduce the risk, we can run a short trial and gather feedback.",
                    "acceptable_variations": [
                        "To reduce the risk, we can run a short trial and gather feedback.",
                        "To reduce the risk, we can start with a small rollout.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "concern_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase acknowledges a concern politely?",
                    "options": ["I understand the concern.", "That's wrong.", "No."],
                    "correct_answer": "I understand the concern.",
                },
                {
                    "key": "clarify_phrase_client",
                    "type": "multiple_choice",
                    "prompt": "Which phrase asks for clarification politely?",
                    "options": ["Could you clarify ...?", "Explain now!", "Why are you scared?"],
                    "correct_answer": "Could you clarify ...?",
                },
                {
                    "key": "reduce_risk",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces mitigation?",
                    "options": ["To reduce the risk, we can ...", "To reduce, we angry ...", "To random, we ..."],
                    "correct_answer": "To reduce the risk, we can ...",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_client_concerns",
                "opening_line": "I'm concerned about this change.",
                "learner_goal": "Acknowledge concerns, clarify, and propose mitigation.",
                "turns": [
                    {
                        "coach": "I'm concerned this change will disrupt our team.",
                        "hint": "Mulai dengan I understand the concern.",
                        "sample_answer": "I understand the concern.",
                        "focus": "Acknowledge",
                        "expected_keywords": ["understand", "concern"],
                    },
                    {
                        "coach": "Ask me what I mean.",
                        "hint": "Could you clarify...?",
                        "sample_answer": "Could you clarify what disruption you expect?",
                        "focus": "Clarify",
                        "expected_keywords": ["clarify"],
                    },
                    {
                        "coach": "Offer a mitigation plan.",
                        "hint": "To reduce the risk, we can...",
                        "sample_answer": "To reduce the risk, we can run a two-week trial, send weekly summaries, and gather feedback.",
                        "focus": "Mitigation",
                        "expected_keywords": ["reduce", "trial", "feedback"],
                    },
                ],
                "target_phrases": ["I understand the concern.", "Could you clarify ...?", "To reduce the risk, we can ..."],
            },
            "reading_support": "Handling client concerns requires empathy and structure: acknowledge the concern, clarify the risk, then offer mitigation steps like a trial and clear updates.",
            "writing_support_lines": [
                "Write 7 lines:",
                "1. I understand the concern.",
                "2. Could you clarify ...?",
                "3. That makes sense.",
                "4. To reduce the risk, we can ...",
                "5. We can run a short trial.",
                "6. We'll gather feedback.",
                "7. I'll share a draft plan today.",
            ],
            "goal_examples": ["I understand the concern.", "Could you clarify ...?", "To reduce the risk, we can ..."],
        },
        {
            "lesson_key": "lesson-04-confirming-next-steps",
            "slug": "confirming-next-steps",
            "title": "Confirming Next Steps",
            "conversation_situation": "confirming_next_steps_with_client",
            "conversation_goal": "Confirm next steps, assign owners, and set a timeline clearly.",
            "grammar_summary": "Use To confirm... / Next steps are... / I'll ... by ... / Does that work? to align on follow-up.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu menutup call dengan klien. Kamu rangkum keputusan, sebut next steps, dan set timeline.",
            "dialogue": [
                ("Jordan", "This sounds good. What happens next?"),
                ("Mina", "To confirm, we'll start with a two-week pilot."),
                ("Jordan", "Okay."),
                ("Mina", "Next steps are: I'll send the draft plan today, and you'll review it by Friday."),
                ("Jordan", "That works."),
                ("Mina", "We'll meet next Monday to finalize the rollout."),
                ("Jordan", "Sounds good."),
                ("Mina", "Great. Does that timeline work for you?"),
            ],
            "translations": [
                ("Jordan", "This sounds good. What happens next?", "Kedengarannya bagus. Next-nya apa?"),
                ("Mina", "To confirm, we'll start with a two-week pilot.", "Buat konfirmasi, kita mulai dengan pilot dua minggu."),
                ("Jordan", "Okay.", "Oke."),
                ("Mina", "Next steps are: I'll send the draft plan today, and you'll review it by Friday.", "Next steps-nya: aku kirim draft plan hari ini, dan kamu review sebelum Jumat."),
                ("Jordan", "That works.", "Oke."),
                ("Mina", "We'll meet next Monday to finalize the rollout.", "Kita meeting Senin depan untuk finalize rollout."),
                ("Jordan", "Sounds good.", "Oke."),
                ("Mina", "Great. Does that timeline work for you?", "Oke. Timeline itu works buat kamu?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "To confirm, we'll start with a two-week pilot.",
                    "meaning_id": "Buat konfirmasi, kita mulai dengan pilot dua minggu.",
                    "usage_note": "Confirm the plan clearly.",
                    "common_mistake": 'Do not confirm vaguely; restate the decision.',
                },
                {
                    "phrase": "Next steps are: I'll send the draft plan today.",
                    "meaning_id": "Next steps-nya: aku kirim draft plan hari ini.",
                    "usage_note": "Clear action items.",
                    "common_mistake": 'Do not list actions without a time; add today/by Friday.',
                },
                {
                    "phrase": "You'll review it by Friday.",
                    "meaning_id": "Kamu review sebelum Jumat.",
                    "usage_note": "Assign an owner and deadline.",
                    "common_mistake": 'Do not say "review it until Friday" for deadline; use by.',
                },
                {
                    "phrase": "We'll meet next Monday to finalize.",
                    "meaning_id": "Kita meeting Senin depan untuk finalize.",
                    "usage_note": "Set the next checkpoint.",
                    "common_mistake": 'Do not skip the next checkpoint; set one clearly.',
                },
                {
                    "phrase": "Does that timeline work for you?",
                    "meaning_id": "Timeline itu works buat kamu?",
                    "usage_note": "Confirm agreement.",
                    "common_mistake": 'Do not assume; ask if it works.',
                },
            ],
            "grammar_md": [
                ("Confirm + next steps", ["To confirm, ...", "Next steps are: I'll ..., and you'll ..."]),
                ("Deadlines", ["I'll send it today.", "You'll review it by Friday."]),
            ],
            "pronunciation": [
                ("timeline", "TIME-line."),
                ("finalize", "FYE-nuh-lize."),
                ("pilot", "PY-lut."),
            ],
            "response_prompts": [
                {
                    "prompt": "Confirm the plan.",
                    "target_response": "To confirm, we'll start with a two-week pilot.",
                    "acceptable_variations": [
                        "To confirm, we'll start with a two-week pilot.",
                        "To confirm, we'll go with option B.",
                    ],
                },
                {
                    "prompt": "State next steps with owners.",
                    "target_response": "Next steps are: I'll send the draft plan today, and you'll review it by Friday.",
                    "acceptable_variations": [
                        "Next steps are: I'll send the draft plan today, and you'll review it by Friday.",
                        "Next steps are: I'll draft the doc, and you'll review it tomorrow.",
                    ],
                },
                {
                    "prompt": "Check if timeline works.",
                    "target_response": "Does that timeline work for you?",
                    "acceptable_variations": ["Does that timeline work for you?", "Would that timeline work for you?"],
                },
            ],
            "quiz": [
                {
                    "key": "to_confirm",
                    "type": "multiple_choice",
                    "prompt": "Which phrase confirms a decision?",
                    "options": ["To confirm, ...", "By the way, ...", "Anyway, ..."],
                    "correct_answer": "To confirm, ...",
                },
                {
                    "key": "by_deadline_client",
                    "type": "multiple_choice",
                    "prompt": "Which sentence uses by for a deadline correctly?",
                    "options": ["You'll review it by Friday.", "You'll review it until Friday.", "You'll by Friday review."],
                    "correct_answer": "You'll review it by Friday.",
                },
                {
                    "key": "timeline_question",
                    "type": "multiple_choice",
                    "prompt": "Which question checks agreement on timing?",
                    "options": ["Does that timeline work for you?", "Why are you late?", "Stop."],
                    "correct_answer": "Does that timeline work for you?",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_client_next_steps",
                "opening_line": "This sounds good. What happens next?",
                "learner_goal": "Confirm next steps with owners and timeline.",
                "turns": [
                    {
                        "coach": "Confirm the decision.",
                        "hint": "To confirm, ...",
                        "sample_answer": "To confirm, we'll start with a two-week pilot.",
                        "focus": "Confirm decision",
                        "expected_keywords": ["to confirm", "pilot"],
                    },
                    {
                        "coach": "List next steps with owners and deadlines.",
                        "hint": "Next steps are: I'll... today, and you'll... by Friday.",
                        "sample_answer": "Next steps are: I'll send the draft plan today, and you'll review it by Friday.",
                        "focus": "Next steps",
                        "expected_keywords": ["next steps", "by"],
                    },
                    {
                        "coach": "Check if the timeline works.",
                        "hint": "Does that timeline work for you?",
                        "sample_answer": "Great. Does that timeline work for you?",
                        "focus": "Confirm timeline",
                        "expected_keywords": ["timeline", "work"],
                    },
                ],
                "target_phrases": ["To confirm, ...", "Next steps are ...", "Does that timeline work for you?"],
            },
            "reading_support": "Ending a client call professionally means confirming decisions, assigning next steps with owners and deadlines, and checking that the timeline works.",
            "writing_support_lines": [
                "Write 7 lines:",
                "1. To confirm, ...",
                "2. Next steps are: I'll ...",
                "3. You'll ... by ...",
                "4. We'll meet on ...",
                "5. Does that timeline work for you?",
                "6. Great, thanks.",
                "7. I'll follow up by ...",
            ],
            "goal_examples": ["To confirm, ...", "Next steps are ...", "Does that timeline work for you?"],
        },
        {
            "lesson_key": "lesson-05-client-conversation-mission",
            "slug": "client-conversation-mission",
            "title": "Client Conversation Mission",
            "conversation_situation": "mission_client_conversation",
            "conversation_goal": "Complete a client conversation: understand needs, explain options, handle concerns, and confirm next steps.",
            "grammar_summary": "Combine: Just to clarify... / We have two options... / I understand the concern... / To reduce the risk... / Next steps are...",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Misi: kamu handle call klien dari discovery sampai follow-up yang jelas.",
            "dialogue": [
                ("Jordan", "We want to improve onboarding. What can you do?"),
                ("Mina", "Just to clarify, who is the main user group and what's the biggest pain point?"),
                ("Jordan", "New hires can't find key docs."),
                ("Mina", "Got it. We have two options: a quick fix this week, or a more robust solution in two weeks."),
                ("Jordan", "I'm concerned it will disrupt our team."),
                ("Mina", "I understand the concern. To reduce the risk, we can run a two-week pilot and send weekly summaries."),
                ("Jordan", "Okay. What happens next?"),
                ("Mina", "To confirm, next steps are: I'll send a draft plan today, and you'll review it by Friday. Does that timeline work for you?"),
            ],
            "translations": [
                ("Jordan", "We want to improve onboarding. What can you do?", "Kami mau improve onboarding. Kamu bisa bantu apa?"),
                ("Mina", "Just to clarify, who is the main user group and what's the biggest pain point?", "Biar jelas, siapa user utamanya dan pain point terbesarnya apa?"),
                ("Jordan", "New hires can't find key docs.", "Orang baru nggak bisa nemu dokumen penting."),
                ("Mina", "Got it. We have two options: a quick fix this week, or a more robust solution in two weeks.", "Oke. Kita punya dua opsi: quick fix minggu ini, atau solusi lebih robust dalam dua minggu."),
                ("Jordan", "I'm concerned it will disrupt our team.", "Aku khawatir itu bakal ganggu tim."),
                ("Mina", "I understand the concern. To reduce the risk, we can run a two-week pilot and send weekly summaries.", "Aku paham kekhawatirannya. Untuk ngurangin risiko, kita bisa pilot dua minggu dan kirim ringkasan mingguan."),
                ("Jordan", "Okay. What happens next?", "Oke. Next-nya apa?"),
                ("Mina", "To confirm, next steps are: I'll send a draft plan today, and you'll review it by Friday. Does that timeline work for you?", "Buat konfirmasi, next steps-nya: aku kirim draft plan hari ini, dan kamu review sebelum Jumat. Timeline itu works buat kamu?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "Just to clarify, who is the main user group?",
                    "meaning_id": "Biar jelas, siapa user utama-nya?",
                    "usage_note": "Discovery question.",
                    "common_mistake": "Don't assume; ask.",
                },
                {
                    "phrase": "We have two options: a quick fix or a robust solution.",
                    "meaning_id": "Kita punya dua opsi: quick fix atau solusi yang lebih robust.",
                    "usage_note": "Options structure.",
                    "common_mistake": "Keep each option to one sentence.",
                },
                {
                    "phrase": "I understand the concern. To reduce the risk, we can run a pilot.",
                    "meaning_id": "Aku paham kekhawatirannya. Untuk ngurangin risiko, kita bisa pilot.",
                    "usage_note": "Concern + mitigation.",
                    "common_mistake": "Acknowledge first, then mitigate.",
                },
                {
                    "phrase": "Next steps are: I'll send a draft plan today, and you'll review it by Friday.",
                    "meaning_id": "Next steps-nya: aku kirim draft plan hari ini, dan kamu review sebelum Jumat.",
                    "usage_note": "Clear follow-up.",
                    "common_mistake": "Always assign owners and deadlines.",
                },
                {
                    "phrase": "Does that timeline work for you?",
                    "meaning_id": "Timeline itu works buat kamu?",
                    "usage_note": "Confirm agreement.",
                    "common_mistake": "Do not assume the timeline works.",
                },
            ],
            "grammar_md": [
                (
                    "Client conversation flow",
                    [
                        "Just to clarify, ...",
                        "We have two options ...",
                        "I understand the concern. To reduce the risk, ...",
                        "Next steps are ... Does that timeline work for you?",
                    ],
                ),
            ],
            "pronunciation": [
                ("client", "KLY-ent."),
                ("disrupt", "dis-RUPT."),
                ("deadline", "DED-line."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask discovery questions.",
                    "target_response": "Just to clarify, who is the main user group and what's the biggest pain point?",
                    "acceptable_variations": [
                        "Just to clarify, who is the main user group and what's the biggest pain point?",
                        "Just to clarify, what is your timeline and success criteria?",
                    ],
                },
                {
                    "prompt": "Explain options and trade-off.",
                    "target_response": "We have two options: a quick fix this week, or a more robust solution in two weeks.",
                    "acceptable_variations": [
                        "We have two options: a quick fix this week, or a more robust solution in two weeks.",
                        "We have two options: a pilot first, or a full rollout later.",
                    ],
                },
                {
                    "prompt": "Confirm next steps and timeline.",
                    "target_response": "Next steps are: I'll send a draft plan today, and you'll review it by Friday. Does that timeline work for you?",
                    "acceptable_variations": [
                        "Next steps are: I'll send a draft plan today, and you'll review it by Friday. Does that timeline work for you?",
                        "Next steps are: I'll send the draft tomorrow, and you'll review it by next week. Would that work?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "client_flow",
                    "type": "multiple_choice",
                    "prompt": "Which flow fits a client call?",
                    "options": [
                        "Discovery -> options -> concerns -> next steps",
                        "Greeting -> goodbye",
                        "Numbers -> colors",
                    ],
                    "correct_answer": "Discovery -> options -> concerns -> next steps",
                },
                {
                    "key": "mitigation_phrase_client",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces mitigation?",
                    "options": ["To reduce the risk, we can ...", "To reduce, stop.", "No risk."],
                    "correct_answer": "To reduce the risk, we can ...",
                },
                {
                    "key": "next_steps_phrase_client",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces follow-up actions?",
                    "options": ["Next steps are ...", "Whatever.", "No need."],
                    "correct_answer": "Next steps are ...",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_client_mission",
                "opening_line": "We need help with onboarding. Can you walk us through options?",
                "learner_goal": "Handle a client conversation end-to-end: needs, options, concerns, and next steps.",
                "turns": [
                    {
                        "coach": "Start by understanding our needs.",
                        "hint": "Just to clarify... biggest pain point...",
                        "sample_answer": "Just to clarify, who is the main user group and what's the biggest pain point today?",
                        "focus": "Discovery",
                        "expected_keywords": ["clarify", "pain point"],
                    },
                    {
                        "coach": "Now explain two options and a trade-off, then recommend one.",
                        "hint": "We have two options... The trade-off is... I'd recommend...",
                        "sample_answer": "We have two options: a quick fix this week, or a more robust solution in two weeks. The trade-off is speed versus stability. I'd recommend the robust option if the timeline allows.",
                        "focus": "Options + recommendation",
                        "expected_keywords": ["two options", "trade-off", "recommend"],
                    },
                    {
                        "coach": "We are concerned about disruption. Handle it and confirm next steps.",
                        "hint": "I understand the concern... To reduce the risk... Next steps are... Does that timeline work...?",
                        "sample_answer": "I understand the concern. To reduce the risk, we can run a two-week pilot and send weekly summaries. Next steps are: I'll send a draft plan today, and you'll review it by Friday. Does that timeline work for you?",
                        "focus": "Concerns + next steps",
                        "expected_keywords": ["understand", "reduce", "next steps", "timeline"],
                    },
                ],
                "target_phrases": ["Just to clarify, ...", "We have two options ...", "Next steps are ..."],
            },
            "reading_support": "Strong client communication is structured and empathetic: understand needs, present options with trade-offs, handle concerns with mitigation, and confirm next steps with deadlines.",
            "writing_support_lines": [
                "Write your mission (10 lines):",
                "1. Just to clarify, ...",
                "2. Could you share more about ...?",
                "3. So what you need is ... right?",
                "4. We have two options: A or B.",
                "5. The trade-off is ...",
                "6. I understand the concern.",
                "7. To reduce the risk, we can ...",
                "8. To confirm, ...",
                "9. Next steps are: I'll ..., you'll ... by ...",
                "10. Does that timeline work for you?",
            ],
            "goal_examples": ["Just to clarify, ...", "We have two options ...", "Next steps are ..."],
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

