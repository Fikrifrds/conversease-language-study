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
            "- Speed: natural, slightly fast",
            "- Tone: conversational, precise, professional",
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

        Read it again and underline the listening tools (implied, hinting, to be honest, what I'm getting at, in other words).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "C1"
    root = Path("content/curriculum/english/C1")
    units_root = root / "units"
    unit_key = "unit-07-advanced-listening-response"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-07-advanced-listening-response
            level_code: C1
            title: Advanced Listening & Response
            main_conversation_outcome: Respond accurately to dense, fast, or indirect speech.
            status: in_production
            lessons:
              - lesson-01-catching-implied-meaning
              - lesson-02-responding-to-long-turns
              - lesson-03-summarizing-what-you-heard
              - lesson-04-asking-high-quality-follow-ups
              - lesson-05-advanced-listening-mission
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
            "lesson_key": "lesson-01-catching-implied-meaning",
            "slug": "catching-implied-meaning",
            "title": "Catching Implied Meaning",
            "conversation_situation": "catching_implied_meaning",
            "conversation_goal": "Catch implied meaning by listening for hints, hedges, and what is not said explicitly.",
            "grammar_summary": "Use What I'm hearing is... / Are you implying that...? / It sounds like... / Just to check... to catch implied meaning.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu ngobrol dengan stakeholder yang ngomongnya halus/indirect. Kamu perlu nangkep maksud tersirat dan cek pemahaman.",
            "dialogue": [
                ("Jordan", "The proposal is interesting. It's just... not sure it's the right time."),
                ("Mina", "It sounds like timing is the main concern."),
                ("Jordan", "Well, there are a few moving parts."),
                ("Mina", "Just to check, are you implying that we should delay the rollout?"),
                ("Jordan", "Possibly, yes."),
                ("Mina", "What I'm hearing is we need a phased plan to reduce risk."),
                ("Jordan", "That would make it easier to align internally."),
                ("Mina", "Got it. I'll draft a phased option and share it today."),
            ],
            "translations": [
                ("Jordan", "The proposal is interesting. It's just... not sure it's the right time.", "Proposalnya menarik. Cuma... aku nggak yakin ini timing yang tepat."),
                ("Mina", "It sounds like timing is the main concern.", "Kedengarannya concern utamanya timing."),
                ("Jordan", "Well, there are a few moving parts.", "Soalnya ada beberapa hal yang lagi bergerak/berubah."),
                ("Mina", "Just to check, are you implying that we should delay the rollout?", "Biar aku cek, kamu menyiratkan kita sebaiknya delay rollout?"),
                ("Jordan", "Possibly, yes.", "Mungkin, iya."),
                ("Mina", "What I'm hearing is we need a phased plan to reduce risk.", "Yang aku tangkap: kita butuh rencana bertahap untuk ngurangin risiko."),
                ("Jordan", "That would make it easier to align internally.", "Itu bikin lebih gampang align internal."),
                ("Mina", "Got it. I'll draft a phased option and share it today.", "Oke. Aku draft opsi bertahap dan share hari ini."),
            ],
            "useful_phrases": [
                {
                    "phrase": "It sounds like timing is the main concern.",
                    "meaning_id": "Kedengarannya concern utamanya timing.",
                    "usage_note": "A neutral interpretation.",
                    "common_mistake": "Do not assume intent; phrase it as sounds like.",
                },
                {
                    "phrase": "Just to check, are you implying that we should delay the rollout?",
                    "meaning_id": "Biar aku cek, kamu menyiratkan kita sebaiknya delay rollout?",
                    "usage_note": "Confirm implied meaning explicitly and politely.",
                    "common_mistake": "Do not accuse; use just to check.",
                },
                {
                    "phrase": "What I'm hearing is we need a phased plan to reduce risk.",
                    "meaning_id": "Yang aku tangkap: kita butuh rencana bertahap untuk ngurangin risiko.",
                    "usage_note": "Summarize implied meaning as a next step.",
                    "common_mistake": "Do not summarize too broadly; keep it concrete.",
                },
                {
                    "phrase": "Are you implying that ...?",
                    "meaning_id": "Kamu menyiratkan bahwa ...?",
                    "usage_note": "A direct but polite check.",
                    "common_mistake": "Do not sound confrontational; pair with just to check.",
                },
                {
                    "phrase": "What I'm hearing is ...",
                    "meaning_id": "Yang aku tangkap adalah ...",
                    "usage_note": "A useful listening mirror.",
                    "common_mistake": "Do not paraphrase incorrectly; keep it accurate.",
                },
            ],
            "grammar_md": [
                ("Implied meaning checks", ["It sounds like ...", "Are you implying that ...?", "Just to check, ..."]),
                ("Listening mirrors", ["What I'm hearing is ...", "So you're saying ..."]),
            ],
            "pronunciation": [
                ("implying", "im-PLY-ing."),
                ("phased", "FAYZD."),
                ("moving parts", "MOO-ving parts."),
            ],
            "response_prompts": [
                {
                    "prompt": "Interpret a concern neutrally.",
                    "target_response": "It sounds like timing is the main concern.",
                    "acceptable_variations": [
                        "It sounds like timing is the main concern.",
                        "It sounds like alignment is the main concern.",
                    ],
                },
                {
                    "prompt": "Check implied meaning politely.",
                    "target_response": "Just to check, are you implying that we should delay the rollout?",
                    "acceptable_variations": [
                        "Just to check, are you implying that we should delay the rollout?",
                        "Just to check, are you suggesting we delay this?",
                    ],
                },
                {
                    "prompt": "Summarize what you heard as a next step.",
                    "target_response": "What I'm hearing is we need a phased plan to reduce risk.",
                    "acceptable_variations": [
                        "What I'm hearing is we need a phased plan to reduce risk.",
                        "What I'm hearing is we should propose a phased rollout.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "sounds_like",
                    "type": "multiple_choice",
                    "prompt": "Which phrase gives a neutral interpretation?",
                    "options": ["It sounds like ...", "You mean ...", "You're wrong."],
                    "correct_answer": "It sounds like ...",
                },
                {
                    "key": "implying",
                    "type": "multiple_choice",
                    "prompt": "Which phrase checks implied meaning?",
                    "options": ["Are you implying that ...?", "I'm sure that ...", "No need."],
                    "correct_answer": "Are you implying that ...?",
                },
                {
                    "key": "mirror_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase mirrors what you heard?",
                    "options": ["What I'm hearing is ...", "Stop.", "Whatever."],
                    "correct_answer": "What I'm hearing is ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_implied_meaning",
                "opening_line": "The proposal is interesting, but I'm not sure it's the right time.",
                "learner_goal": "Catch implied meaning and confirm it politely, then propose a clear next step.",
                "turns": [
                    {
                        "coach": "Interpret the concern neutrally.",
                        "hint": "Use It sounds like...",
                        "sample_answer": "It sounds like timing is the main concern.",
                        "focus": "Interpretation",
                        "expected_keywords": ["sounds like", "concern"],
                    },
                    {
                        "coach": "Confirm implied meaning politely.",
                        "hint": "Just to check... are you implying...?",
                        "sample_answer": "Just to check, are you implying that we should delay the rollout?",
                        "focus": "Check",
                        "expected_keywords": ["just to check", "implying", "delay"],
                    },
                    {
                        "coach": "Summarize and propose a next step.",
                        "hint": "What I'm hearing is... I'll...",
                        "sample_answer": "What I'm hearing is we need a phased plan to reduce risk. I'll draft a phased option and share it today.",
                        "focus": "Next step",
                        "expected_keywords": ["hearing", "phased", "share"],
                    },
                ],
                "target_phrases": ["It sounds like ...", "Just to check, are you implying ...?", "What I'm hearing is ..."],
            },
            "reading_support": "Implied meaning often appears as hedges and vague language. Listen for what is not said directly, then check your understanding politely and summarize the implication into a concrete next step.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. It sounds like ...",
                "2. My sense is that ...",
                "3. Just to check, ...",
                "4. Are you implying that ...?",
                "5. What I'm hearing is ...",
                "6. In other words, ...",
                "7. If that's the case, ...",
                "8. Then the next step is ...",
                "9. I'll draft ...",
                "10. And share it by ...",
            ],
            "goal_examples": ["It sounds like ...", "Just to check, are you implying ...?", "What I'm hearing is ..."],
        },
        {
            "lesson_key": "lesson-02-responding-to-long-turns",
            "slug": "responding-to-long-turns",
            "title": "Responding to Long Turns",
            "conversation_situation": "responding_to_long_turns",
            "conversation_goal": "Respond to long turns by extracting key points, acknowledging emotions, and replying in a structured way.",
            "grammar_summary": "Use Let me make sure I got this... / The key points are... / If I understand correctly... / Here's how I'd respond... to respond to long turns.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu dengar penjelasan panjang. Kamu harus merespons dengan rapi: rangkum poin, konfirmasi, lalu jawab.",
            "dialogue": [
                ("Jordan", "So the issue is: multiple teams depend on this, the timeline is tight, and leadership wants visibility. Also, clients are sensitive to changes."),
                ("Mina", "Let me make sure I got this: we need to manage dependencies, time pressure, and stakeholder visibility."),
                ("Jordan", "Exactly."),
                ("Mina", "The key points are: keep changes small, communicate clearly, and monitor risk."),
                ("Jordan", "So what do you suggest?"),
                ("Mina", "If I understand correctly, a phased rollout is the safest move."),
                ("Jordan", "How would you communicate it?"),
                ("Mina", "Here's how I'd respond: propose phases, share metrics, and set weekly check-ins."),
            ],
            "translations": [
                ("Jordan", "So the issue is: multiple teams depend on this, the timeline is tight, and leadership wants visibility. Also, clients are sensitive to changes.", "Jadi isu-nya: banyak tim bergantung, timeline ketat, leadership mau visibility. Dan klien sensitif terhadap perubahan."),
                ("Mina", "Let me make sure I got this: we need to manage dependencies, time pressure, and stakeholder visibility.", "Biar aku pastikan: kita perlu manage dependency, tekanan waktu, dan visibility stakeholder."),
                ("Jordan", "Exactly.", "Iya."),
                ("Mina", "The key points are: keep changes small, communicate clearly, and monitor risk.", "Poin kuncinya: perubahan kecil, komunikasi jelas, dan monitor risiko."),
                ("Jordan", "So what do you suggest?", "Jadi kamu saran apa?"),
                ("Mina", "If I understand correctly, a phased rollout is the safest move.", "Kalau aku paham, rollout bertahap paling aman."),
                ("Jordan", "How would you communicate it?", "Gimana kamu komunikasikan?"),
                ("Mina", "Here's how I'd respond: propose phases, share metrics, and set weekly check-ins.", "Aku akan jawab begini: usulkan fase, share metrik, dan set check-in mingguan."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let me make sure I got this: ...",
                    "meaning_id": "Biar aku pastikan: ...",
                    "usage_note": "Summarize a long turn before responding.",
                    "common_mistake": "Do not respond immediately; summarize first.",
                },
                {
                    "phrase": "The key points are: ...",
                    "meaning_id": "Poin kuncinya: ...",
                    "usage_note": "Extract key points clearly.",
                    "common_mistake": "Do not list too many points; pick 2-3.",
                },
                {
                    "phrase": "If I understand correctly, ...",
                    "meaning_id": "Kalau aku paham dengan benar, ...",
                    "usage_note": "Confirm understanding before proposing.",
                    "common_mistake": "Do not assume; confirm.",
                },
                {
                    "phrase": "Here's how I'd respond: ...",
                    "meaning_id": "Aku akan jawab begini: ...",
                    "usage_note": "Structure your response explicitly.",
                    "common_mistake": "Do not ramble; use a clear structure.",
                },
                {
                    "phrase": "Thanks, that's helpful context.",
                    "meaning_id": "Makasih, itu konteks yang membantu.",
                    "usage_note": "Acknowledge a long explanation politely.",
                    "common_mistake": "Do not ignore the effort; acknowledge it.",
                },
            ],
            "grammar_md": [
                ("Summarizing long turns", ["Let me make sure I got this: ...", "The key points are: ..."]),
                ("Structured response", ["If I understand correctly, ...", "Here's how I'd respond: ..."]),
            ],
            "pronunciation": [
                ("dependencies", "di-PEN-den-seez."),
                ("visibility", "viz-uh-BIL-ih-tee."),
                ("check-ins", "CHEK-inz."),
            ],
            "response_prompts": [
                {
                    "prompt": "Summarize a long explanation.",
                    "target_response": "Let me make sure I got this: we need to manage dependencies, time pressure, and stakeholder visibility.",
                    "acceptable_variations": [
                        "Let me make sure I got this: we need to manage dependencies, time pressure, and stakeholder visibility.",
                        "Let me make sure I got this: timeline is tight, and stakeholders need visibility.",
                    ],
                },
                {
                    "prompt": "Extract key points.",
                    "target_response": "The key points are: keep changes small, communicate clearly, and monitor risk.",
                    "acceptable_variations": [
                        "The key points are: keep changes small, communicate clearly, and monitor risk.",
                        "The key points are: reduce scope, communicate, and monitor.",
                    ],
                },
                {
                    "prompt": "Propose a structured response.",
                    "target_response": "Here's how I'd respond: propose phases, share metrics, and set weekly check-ins.",
                    "acceptable_variations": [
                        "Here's how I'd respond: propose phases, share metrics, and set weekly check-ins.",
                        "Here's how I'd respond: suggest a pilot, share metrics, and set a weekly cadence.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "make_sure_got_this",
                    "type": "multiple_choice",
                    "prompt": "Which phrase summarizes a long turn before responding?",
                    "options": ["Let me make sure I got this: ...", "No summary.", "Stop."],
                    "correct_answer": "Let me make sure I got this: ...",
                },
                {
                    "key": "key_points",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces key points?",
                    "options": ["The key points are: ...", "Key point is none.", "Whatever."],
                    "correct_answer": "The key points are: ...",
                },
                {
                    "key": "respond_structure",
                    "type": "multiple_choice",
                    "prompt": "Which phrase signals a structured response?",
                    "options": ["Here's how I'd respond: ...", "I respond now.", "No response."],
                    "correct_answer": "Here's how I'd respond: ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_long_turns",
                "opening_line": "Let me explain the situation in detail...",
                "learner_goal": "Respond to long turns by summarizing key points and replying in a structured way.",
                "turns": [
                    {
                        "coach": "Summarize what you heard.",
                        "hint": "Let me make sure I got this...",
                        "sample_answer": "Let me make sure I got this: we need to manage dependencies, time pressure, and stakeholder visibility.",
                        "focus": "Summary",
                        "expected_keywords": ["make sure", "got this"],
                    },
                    {
                        "coach": "Extract the key points.",
                        "hint": "The key points are...",
                        "sample_answer": "The key points are: keep changes small, communicate clearly, and monitor risk.",
                        "focus": "Key points",
                        "expected_keywords": ["key points"],
                    },
                    {
                        "coach": "Give a structured response.",
                        "hint": "Here's how I'd respond...",
                        "sample_answer": "Here's how I'd respond: propose phases, share metrics, and set weekly check-ins.",
                        "focus": "Response",
                        "expected_keywords": ["here's how", "phases", "weekly"],
                    },
                ],
                "target_phrases": ["Let me make sure I got this: ...", "The key points are: ...", "Here's how I'd respond: ..."],
            },
            "reading_support": "When someone speaks for a long time, strong listeners summarize before responding. Extract the core points, confirm understanding, then reply with a clear structure to avoid misunderstandings.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. Thanks, that's helpful context.",
                "2. Let me make sure I got this: ...",
                "3. The key points are: ...",
                "4. If I understand correctly, ...",
                "5. Here's how I'd respond: ...",
                "6. First, ...",
                "7. Next, ...",
                "8. Finally, ...",
                "9. Does that capture it?",
                "10. Any missing details?",
            ],
            "goal_examples": ["Let me make sure I got this: ...", "The key points are: ...", "Here's how I'd respond: ..."],
        },
        {
            "lesson_key": "lesson-03-summarizing-what-you-heard",
            "slug": "summarizing-what-you-heard",
            "title": "Summarizing What You Heard",
            "conversation_situation": "summarizing_what_you_heard",
            "conversation_goal": "Summarize accurately by separating facts, concerns, and decisions, then confirm with the speaker.",
            "grammar_summary": "Use So, to summarize... / Just to confirm... / The decision is... / The open questions are... to summarize.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu habis meeting. Kamu rangkum dengan rapi (fakta, concern, keputusan) dan cek konfirmasi.",
            "dialogue": [
                ("Jordan", "Can you summarize the meeting?"),
                ("Mina", "Sure. So, to summarize: the timeline is tight and clients are sensitive to change."),
                ("Jordan", "Any decisions?"),
                ("Mina", "The decision is to propose a phased rollout with clear metrics."),
                ("Jordan", "What concerns remain?"),
                ("Mina", "The open questions are around resourcing and internal alignment."),
                ("Jordan", "Can you confirm with the team?"),
                ("Mina", "Just to confirm, I'll send the summary and ask if anything is missing."),
            ],
            "translations": [
                ("Jordan", "Can you summarize the meeting?", "Bisa rangkum meeting-nya?"),
                ("Mina", "Sure. So, to summarize: the timeline is tight and clients are sensitive to change.", "Oke. Singkatnya: timeline ketat dan klien sensitif terhadap perubahan."),
                ("Jordan", "Any decisions?", "Ada keputusan?"),
                ("Mina", "The decision is to propose a phased rollout with clear metrics.", "Keputusannya: usulkan rollout bertahap dengan metrik yang jelas."),
                ("Jordan", "What concerns remain?", "Concern yang tersisa apa?"),
                ("Mina", "The open questions are around resourcing and internal alignment.", "Pertanyaan terbuka: resourcing dan alignment internal."),
                ("Jordan", "Can you confirm with the team?", "Bisa konfirmasi ke tim?"),
                ("Mina", "Just to confirm, I'll send the summary and ask if anything is missing.", "Biar pasti, aku kirim rangkuman dan tanya apakah ada yang kurang."),
            ],
            "useful_phrases": [
                {
                    "phrase": "So, to summarize: ...",
                    "meaning_id": "Singkatnya: ...",
                    "usage_note": "Start a structured summary.",
                    "common_mistake": "Do not ramble; start with summarize.",
                },
                {
                    "phrase": "The decision is to propose a phased rollout with clear metrics.",
                    "meaning_id": "Keputusannya: usulkan rollout bertahap dengan metrik jelas.",
                    "usage_note": "State the decision explicitly.",
                    "common_mistake": "Do not mix decisions with opinions; label it as decision.",
                },
                {
                    "phrase": "The open questions are around resourcing and internal alignment.",
                    "meaning_id": "Pertanyaan terbuka: resourcing dan alignment internal.",
                    "usage_note": "Separate open questions from decisions.",
                    "common_mistake": "Do not hide uncertainty; name open questions.",
                },
                {
                    "phrase": "Just to confirm, I'll send the summary and ask if anything is missing.",
                    "meaning_id": "Biar pasti, aku kirim rangkuman dan tanya apakah ada yang kurang.",
                    "usage_note": "Confirm understanding with the group.",
                    "common_mistake": "Do not assume completeness; ask.",
                },
                {
                    "phrase": "Does that capture it accurately?",
                    "meaning_id": "Itu sudah menangkapnya dengan akurat?",
                    "usage_note": "A helpful confirmation question.",
                    "common_mistake": "Do not avoid confirmation; ask directly.",
                },
            ],
            "grammar_md": [
                ("Structured summary", ["So, to summarize: ...", "The decision is ...", "The open questions are ..."]),
                ("Confirmation", ["Just to confirm, ...", "Does that capture it accurately?"]),
            ],
            "pronunciation": [
                ("resourcing", "ree-SOR-sing."),
                ("alignment", "uh-LYNT-ment."),
                ("capture", "KAP-cher."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start a summary clearly.",
                    "target_response": "So, to summarize: the timeline is tight and clients are sensitive to change.",
                    "acceptable_variations": [
                        "So, to summarize: the timeline is tight and clients are sensitive to change.",
                        "So, to summarize: we need a phased rollout and clear communication.",
                    ],
                },
                {
                    "prompt": "State the decision explicitly.",
                    "target_response": "The decision is to propose a phased rollout with clear metrics.",
                    "acceptable_variations": [
                        "The decision is to propose a phased rollout with clear metrics.",
                        "The decision is to start with a pilot and track metrics.",
                    ],
                },
                {
                    "prompt": "Name open questions and confirm.",
                    "target_response": "The open questions are around resourcing and internal alignment. Just to confirm, I'll send the summary and ask if anything is missing.",
                    "acceptable_variations": [
                        "The open questions are around resourcing and internal alignment. Just to confirm, I'll send the summary and ask if anything is missing.",
                        "The open questions are staffing and timeline. Just to confirm, I'll send the notes for review.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "decision_label",
                    "type": "multiple_choice",
                    "prompt": "Which phrase labels a decision clearly?",
                    "options": ["The decision is ...", "I think ...", "Maybe ..."],
                    "correct_answer": "The decision is ...",
                },
                {
                    "key": "open_questions",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces open questions?",
                    "options": ["The open questions are ...", "No questions.", "Stop."],
                    "correct_answer": "The open questions are ...",
                },
                {
                    "key": "to_summarize",
                    "type": "multiple_choice",
                    "prompt": 'What does "to summarize" mean?',
                    "options": ["untuk merangkum", "untuk menolak", "untuk membeli"],
                    "correct_answer": "untuk merangkum",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_summarizing",
                "opening_line": "Can you summarize what we discussed?",
                "learner_goal": "Give a structured summary with decisions and open questions, then confirm.",
                "turns": [
                    {
                        "coach": "Start with a summary of the facts and concerns.",
                        "hint": "So, to summarize...",
                        "sample_answer": "So, to summarize: the timeline is tight and clients are sensitive to change.",
                        "focus": "Summary",
                        "expected_keywords": ["to summarize", "timeline"],
                    },
                    {
                        "coach": "State the decision and open questions.",
                        "hint": "The decision is... The open questions are...",
                        "sample_answer": "The decision is to propose a phased rollout with clear metrics. The open questions are around resourcing and internal alignment.",
                        "focus": "Decision + open questions",
                        "expected_keywords": ["decision", "open questions"],
                    },
                    {
                        "coach": "Confirm your summary with the group.",
                        "hint": "Just to confirm... Does that capture it...?",
                        "sample_answer": "Just to confirm, I'll send the summary and ask if anything is missing. Does that capture it accurately?",
                        "focus": "Confirm",
                        "expected_keywords": ["confirm", "capture"],
                    },
                ],
                "target_phrases": ["So, to summarize: ...", "The decision is ...", "The open questions are ..."],
            },
            "reading_support": "Strong summaries separate facts, concerns, decisions, and open questions. Label each part explicitly, then confirm with the team to avoid misunderstandings and ensure alignment.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. So, to summarize: ...",
                "2. The key facts are ...",
                "3. The main concern is ...",
                "4. The decision is ...",
                "5. The open questions are ...",
                "6. Next steps are ...",
                "7. I'll send the summary ...",
                "8. Just to confirm, ...",
                "9. Does that capture it accurately?",
                "10. Anything missing?",
            ],
            "goal_examples": ["So, to summarize: ...", "The decision is ...", "The open questions are ..."],
        },
        {
            "lesson_key": "lesson-04-asking-high-quality-follow-ups",
            "slug": "asking-high-quality-follow-ups",
            "title": "Asking High-quality Follow-ups",
            "conversation_situation": "high_quality_followups",
            "conversation_goal": "Ask high-quality follow-up questions that clarify scope, assumptions, and next steps.",
            "grammar_summary": "Use When you say X, do you mean...? / What's your assumption about...? / What would change your mind? / What's the next step? to follow up.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu ingin memastikan pemahaman dan menggali detail dengan follow-up yang tajam tapi sopan.",
            "dialogue": [
                ("Jordan", "We should be more cautious with the rollout."),
                ("Mina", "When you say 'more cautious', do you mean smaller scope or slower timing?"),
                ("Jordan", "Mostly smaller scope."),
                ("Mina", "What's your assumption about the main risk?"),
                ("Jordan", "That incidents will spike."),
                ("Mina", "What would change your mind about the timeline?"),
                ("Jordan", "If we see stable metrics in a pilot."),
                ("Mina", "Got it. What's the next step we should take today?"),
            ],
            "translations": [
                ("Jordan", "We should be more cautious with the rollout.", "Kita harus lebih hati-hati dengan rollout."),
                ("Mina", "When you say 'more cautious', do you mean smaller scope or slower timing?", "Waktu kamu bilang 'lebih hati-hati', maksudnya scope lebih kecil atau timing lebih lambat?"),
                ("Jordan", "Mostly smaller scope.", "Lebih ke scope kecil."),
                ("Mina", "What's your assumption about the main risk?", "Asumsi kamu tentang risiko utama apa?"),
                ("Jordan", "That incidents will spike.", "Bahwa incident bakal naik."),
                ("Mina", "What would change your mind about the timeline?", "Apa yang bisa mengubah pikiran kamu soal timeline?"),
                ("Jordan", "If we see stable metrics in a pilot.", "Kalau kita lihat metrik stabil di pilot."),
                ("Mina", "Got it. What's the next step we should take today?", "Oke. Next step apa yang harus kita ambil hari ini?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "When you say 'more cautious', do you mean smaller scope or slower timing?",
                    "meaning_id": "Kalau bilang 'lebih hati-hati', maksudnya scope kecil atau timing lambat?",
                    "usage_note": "Clarify ambiguous language.",
                    "common_mistake": "Do not accept vague words; clarify meaning.",
                },
                {
                    "phrase": "What's your assumption about the main risk?",
                    "meaning_id": "Asumsi kamu tentang risiko utama apa?",
                    "usage_note": "Surface assumptions in a neutral way.",
                    "common_mistake": "Do not argue first; ask assumption.",
                },
                {
                    "phrase": "What would change your mind about the timeline?",
                    "meaning_id": "Apa yang bisa mengubah pikiran kamu soal timeline?",
                    "usage_note": "Find decision criteria and conditions.",
                    "common_mistake": "Do not debate endlessly; ask what would change mind.",
                },
                {
                    "phrase": "What's the next step we should take today?",
                    "meaning_id": "Next step apa yang harus kita ambil hari ini?",
                    "usage_note": "Move to action.",
                    "common_mistake": "Do not leave it abstract; ask next step.",
                },
                {
                    "phrase": "Do you mean X or Y?",
                    "meaning_id": "Maksudnya X atau Y?",
                    "usage_note": "A useful clarification pattern.",
                    "common_mistake": "Do not offer too many options; keep to two.",
                },
            ],
            "grammar_md": [
                ("Clarifying meaning", ["When you say X, do you mean ...?", "Do you mean X or Y?"]),
                ("Assumptions + criteria", ["What's your assumption about ...?", "What would change your mind about ...?"]),
            ],
            "pronunciation": [
                ("cautious", "KAW-shus."),
                ("ambiguous", "am-BIG-yoo-us."),
                ("criteria", "kry-TEER-ee-uh."),
            ],
            "response_prompts": [
                {
                    "prompt": "Clarify a vague word with two options.",
                    "target_response": "When you say 'more cautious', do you mean smaller scope or slower timing?",
                    "acceptable_variations": [
                        "When you say 'more cautious', do you mean smaller scope or slower timing?",
                        "When you say 'faster', do you mean fewer steps or shorter timeline?",
                    ],
                },
                {
                    "prompt": "Ask for assumption about risk.",
                    "target_response": "What's your assumption about the main risk?",
                    "acceptable_variations": ["What's your assumption about the main risk?", "What's your assumption about what could go wrong?"],
                },
                {
                    "prompt": "Ask what would change their mind and move to action.",
                    "target_response": "What would change your mind about the timeline? Got it. What's the next step we should take today?",
                    "acceptable_variations": [
                        "What would change your mind about the timeline? Got it. What's the next step we should take today?",
                        "What would change your mind? Great. What's the next step?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "clarify_two_options",
                    "type": "multiple_choice",
                    "prompt": "Which phrase clarifies ambiguous language?",
                    "options": ["When you say X, do you mean Y or Z?", "You are unclear.", "Stop."],
                    "correct_answer": "When you say X, do you mean Y or Z?",
                },
                {
                    "key": "change_mind",
                    "type": "multiple_choice",
                    "prompt": "Which question finds decision criteria?",
                    "options": ["What would change your mind?", "Why are you wrong?", "No criteria."],
                    "correct_answer": "What would change your mind?",
                },
                {
                    "key": "next_step",
                    "type": "multiple_choice",
                    "prompt": "Which question moves toward action?",
                    "options": ["What's the next step?", "Maybe later.", "No action."],
                    "correct_answer": "What's the next step?",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_followups",
                "opening_line": "We should be more cautious with the rollout.",
                "learner_goal": "Ask high-quality follow-up questions and move the conversation toward action.",
                "turns": [
                    {
                        "coach": "Clarify what 'more cautious' means.",
                        "hint": "When you say..., do you mean X or Y?",
                        "sample_answer": "When you say 'more cautious', do you mean smaller scope or slower timing?",
                        "focus": "Clarify",
                        "expected_keywords": ["when you say", "do you mean"],
                    },
                    {
                        "coach": "Ask about assumptions and decision criteria.",
                        "hint": "What's your assumption... What would change your mind...?",
                        "sample_answer": "What's your assumption about the main risk? And what would change your mind about the timeline?",
                        "focus": "Assumptions + criteria",
                        "expected_keywords": ["assumption", "change your mind"],
                    },
                    {
                        "coach": "Move to action.",
                        "hint": "What's the next step today?",
                        "sample_answer": "Got it. What's the next step we should take today?",
                        "focus": "Action",
                        "expected_keywords": ["next step", "today"],
                    },
                ],
                "target_phrases": ["When you say X, do you mean ...?", "What's your assumption about ...?", "What's the next step ...?"],
            },
            "reading_support": "High-quality follow-ups turn vague language into clarity. Ask what someone means, surface assumptions, find the criteria that would change their mind, and end by agreeing on a concrete next step.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. When you say X, do you mean Y or Z?",
                "2. Just to clarify, ...",
                "3. What's your assumption about ...?",
                "4. What's the main risk?",
                "5. What would change your mind?",
                "6. What data would you need?",
                "7. What does success look like?",
                "8. What's the next step today?",
                "9. Who owns it?",
                "10. When do we check in?",
            ],
            "goal_examples": ["When you say X, do you mean ...?", "What would change your mind?", "What's the next step?"],
        },
        {
            "lesson_key": "lesson-05-advanced-listening-mission",
            "slug": "advanced-listening-mission",
            "title": "Advanced Listening Mission",
            "conversation_situation": "mission_advanced_listening",
            "conversation_goal": "Handle advanced listening: implied meaning, long turns, accurate summary, and high-quality follow-ups.",
            "grammar_summary": "Combine implied meaning checks, structured summaries, and follow-up questions into one mission conversation.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Misi: kamu harus menangkap maksud tersirat, merespons penjelasan panjang, merangkum akurat, dan tanya follow-up berkualitas.",
            "dialogue": [
                ("Jordan", "The client says the plan is 'ambitious', and leadership wants visibility. Also, a few teams are nervous about changes."),
                ("Mina", "It sounds like timing and risk are the main concerns. Just to check, are you implying we should slow down?"),
                ("Jordan", "Possibly."),
                ("Mina", "Let me make sure I got this: dependencies, time pressure, and visibility. The decision is to propose a phased rollout with clear metrics."),
                ("Jordan", "Yes, but we need more caution."),
                ("Mina", "When you say 'more cautious', do you mean smaller scope or slower timing? What would change your mind about the timeline?"),
                ("Jordan", "Stable pilot metrics."),
                ("Mina", "Got it. Next steps are: I'll send the summary, draft phased options, and propose a weekly check-in."),
            ],
            "translations": [
                ("Jordan", "The client says the plan is 'ambitious', and leadership wants visibility. Also, a few teams are nervous about changes.", "Klien bilang plan-nya 'ambitious', leadership mau visibility, dan beberapa tim nervous soal perubahan."),
                ("Mina", "It sounds like timing and risk are the main concerns. Just to check, are you implying we should slow down?", "Kedengarannya concern utama timing dan risiko. Biar aku cek, kamu menyiratkan kita harus pelan-pelan?"),
                ("Jordan", "Possibly.", "Mungkin."),
                ("Mina", "Let me make sure I got this: dependencies, time pressure, and visibility. The decision is to propose a phased rollout with clear metrics.", "Biar aku pastikan: dependency, tekanan waktu, dan visibility. Keputusannya: usulkan rollout bertahap dengan metrik yang jelas."),
                ("Jordan", "Yes, but we need more caution.", "Iya, tapi kita perlu lebih hati-hati."),
                ("Mina", "When you say 'more cautious', do you mean smaller scope or slower timing? What would change your mind about the timeline?", "Kalau bilang 'lebih hati-hati', maksudnya scope kecil atau timing lambat? Apa yang bisa mengubah pikiran kamu soal timeline?"),
                ("Jordan", "Stable pilot metrics.", "Metrik pilot yang stabil."),
                ("Mina", "Got it. Next steps are: I'll send the summary, draft phased options, and propose a weekly check-in.", "Oke. Next steps: aku kirim rangkuman, draft opsi bertahap, dan usulkan check-in mingguan."),
            ],
            "useful_phrases": [
                {
                    "phrase": "It sounds like timing and risk are the main concerns.",
                    "meaning_id": "Kedengarannya concern utama timing dan risiko.",
                    "usage_note": "Interpretation + focus.",
                    "common_mistake": "Don't jump to solutions; interpret first.",
                },
                {
                    "phrase": "Let me make sure I got this: ...",
                    "meaning_id": "Biar aku pastikan: ...",
                    "usage_note": "Summarize long turns.",
                    "common_mistake": "Don't paraphrase incorrectly; keep it accurate.",
                },
                {
                    "phrase": "The decision is to propose a phased rollout with clear metrics.",
                    "meaning_id": "Keputusannya: usulkan rollout bertahap dengan metrik jelas.",
                    "usage_note": "Decision statement.",
                    "common_mistake": "Don't mix decision and open questions.",
                },
                {
                    "phrase": "When you say X, do you mean Y or Z?",
                    "meaning_id": "Kalau bilang X, maksudnya Y atau Z?",
                    "usage_note": "High-quality follow-up pattern.",
                    "common_mistake": "Don't ask vague follow-ups; give two options.",
                },
                {
                    "phrase": "Next steps are: ...",
                    "meaning_id": "Next steps adalah: ...",
                    "usage_note": "Close with concrete actions.",
                    "common_mistake": "Don't end without next steps.",
                },
            ],
            "grammar_md": [
                (
                    "Advanced listening toolkit",
                    [
                        "It sounds like ... Just to check, are you implying ...?",
                        "Let me make sure I got this: ... The key points are ...",
                        "So, to summarize: ... The decision is ... The open questions are ...",
                        "When you say X, do you mean Y or Z? What would change your mind ...?",
                        "Next steps are ...",
                    ],
                )
            ],
            "pronunciation": [
                ("implied", "im-PLYD."),
                ("summarize", "SUM-uh-rise."),
                ("follow-up", "FAH-loh-up."),
            ],
            "response_prompts": [
                {
                    "prompt": "Check implied meaning, then summarize.",
                    "target_response": "It sounds like timing and risk are the main concerns. Just to check, are you implying we should slow down? Let me make sure I got this: dependencies, time pressure, and visibility.",
                    "acceptable_variations": [
                        "It sounds like timing and risk are the main concerns. Just to check, are you implying we should slow down? Let me make sure I got this: dependencies, time pressure, and visibility.",
                        "It sounds like risk is the main concern. Just to check, are you suggesting we delay? Let me make sure I got this: tight timeline and stakeholder pressure.",
                    ],
                },
                {
                    "prompt": "Ask a high-quality follow-up and propose next steps.",
                    "target_response": "When you say 'more cautious', do you mean smaller scope or slower timing? What would change your mind about the timeline? Next steps are: I'll send the summary and draft phased options.",
                    "acceptable_variations": [
                        "When you say 'more cautious', do you mean smaller scope or slower timing? What would change your mind about the timeline? Next steps are: I'll send the summary and draft phased options.",
                        "When you say 'more cautious', do you mean smaller scope? What would change your mind? Next steps are: I'll draft a pilot plan.",
                    ],
                },
                {
                    "prompt": "State decision and open questions clearly.",
                    "target_response": "The decision is to propose a phased rollout with clear metrics. The open questions are around resourcing and alignment.",
                    "acceptable_variations": [
                        "The decision is to propose a phased rollout with clear metrics. The open questions are around resourcing and alignment.",
                        "The decision is to do a pilot first. The open questions are staffing and timeline.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "implied_check",
                    "type": "multiple_choice",
                    "prompt": "Which phrase checks implied meaning politely?",
                    "options": ["Just to check, are you implying ...?", "You're implying ...", "No need."],
                    "correct_answer": "Just to check, are you implying ...?",
                },
                {
                    "key": "two_options",
                    "type": "multiple_choice",
                    "prompt": "Which follow-up clarifies meaning with two options?",
                    "options": [
                        "When you say X, do you mean Y or Z?",
                        "What do you mean?",
                        "Stop.",
                    ],
                    "correct_answer": "When you say X, do you mean Y or Z?",
                },
                {
                    "key": "close_next_steps",
                    "type": "multiple_choice",
                    "prompt": "Which phrase closes with action?",
                    "options": ["Next steps are: ...", "No steps.", "Maybe later."],
                    "correct_answer": "Next steps are: ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_advanced_listening_mission",
                "opening_line": "Mission: listen carefully and respond accurately.",
                "learner_goal": "Handle implied meaning, long turns, accurate summaries, and high-quality follow-ups in one conversation.",
                "turns": [
                    {
                        "coach": "Interpret implied meaning and check it politely.",
                        "hint": "It sounds like... Just to check, are you implying...?",
                        "sample_answer": "It sounds like timing and risk are the main concerns. Just to check, are you implying we should slow down?",
                        "focus": "Implied meaning",
                        "expected_keywords": ["sounds like", "just to check", "implying"],
                    },
                    {
                        "coach": "Summarize and label the decision.",
                        "hint": "Let me make sure I got this... The decision is...",
                        "sample_answer": "Let me make sure I got this: dependencies, time pressure, and visibility. The decision is to propose a phased rollout with clear metrics.",
                        "focus": "Summary + decision",
                        "expected_keywords": ["make sure", "decision"],
                    },
                    {
                        "coach": "Ask a high-quality follow-up and close with next steps.",
                        "hint": "When you say... do you mean... or...? Next steps are...",
                        "sample_answer": "When you say 'more cautious', do you mean smaller scope or slower timing? Next steps are: I'll send the summary and draft phased options.",
                        "focus": "Follow-up + next steps",
                        "expected_keywords": ["do you mean", "next steps"],
                    },
                ],
                "target_phrases": ["Just to check, are you implying ...?", "Let me make sure I got this: ...", "When you say X, do you mean Y or Z?"],
            },
            "reading_support": "Advanced listening is about accuracy and control: check implied meaning, summarize long turns, label decisions and open questions, then ask follow-ups that clarify ambiguity and move to concrete next steps.",
            "writing_support_lines": [
                "Write your mission (12 lines):",
                "1. It sounds like ...",
                "2. Just to check, are you implying ...?",
                "3. Let me make sure I got this: ...",
                "4. The key points are: ...",
                "5. So, to summarize: ...",
                "6. The decision is ...",
                "7. The open questions are ...",
                "8. When you say X, do you mean Y or Z?",
                "9. What would change your mind?",
                "10. What's the next step today?",
                "11. Next steps are: ...",
                "12. Does that capture it accurately?",
            ],
            "goal_examples": ["It sounds like ...", "Let me make sure I got this: ...", "When you say X, do you mean Y or Z?"],
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
                "minimum_score": 78,
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
            "max_turns": 14,
            "feedback_level": {"free": "basic", "pro": "detailed"},
            "turns": roleplay["turns"],
            "target_phrases": roleplay["target_phrases"],
            "rubric": {
                "speaking": {"minimum_score": 78},
                "relevance": {"minimum_score": 76},
                "grammar": {"minimum_score": 74},
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

