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
            "- Tone: confident, professional, friendly",
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

        Read it again and underline the review connectors (to summarize, in short, on the other hand, given that, next steps).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B2"
    b2_root = Path("content/curriculum/english/B2")
    units_root = b2_root / "units"
    unit_key = "unit-08-b2-review-final"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-08-b2-review-final
            level_code: B2
            title: B2 Review & Final Discussion
            main_conversation_outcome: Use B2 discussion skills in professional and social contexts.
            status: in_production
            lessons:
              - lesson-01-review-arguments-and-meetings
              - lesson-02-review-negotiation-and-presenting
              - lesson-03-review-information-and-clients
              - lesson-04-b2-final-test-practice
              - lesson-05-b2-final-discussion
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
            "lesson_key": "lesson-01-review-arguments-and-meetings",
            "slug": "review-arguments-and-meetings",
            "title": "Review Arguments and Meetings",
            "conversation_situation": "review_argument_meeting",
            "conversation_goal": "Summarize your position clearly, support it with reasons, and close with clear next steps.",
            "grammar_summary": "Use My position is... / The main reason is... / To summarize... / Next steps are... to sound clear in meetings.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Review: kamu rangkum posisi kamu di meeting, kasih alasan, lalu tutup dengan next steps yang jelas.",
            "dialogue": [
                ("Alex", "Can you summarize your position for the meeting?"),
                ("Mina", "Sure. My position is that we should prioritize fixing the billing flow."),
                ("Alex", "What's your main reason?"),
                ("Mina", "The main reason is it affects revenue and support workload."),
                ("Alex", "Any counterpoints?"),
                ("Mina", "Some teams prefer new features, but the risk is higher if billing stays broken."),
                ("Alex", "Okay. How do we close this?"),
                ("Mina", "To summarize, we focus on billing first. Next steps are: I'll share a plan today, and you'll review it by Friday."),
            ],
            "translations": [
                ("Alex", "Can you summarize your position for the meeting?", "Bisa rangkum posisi kamu untuk meeting?"),
                ("Mina", "Sure. My position is that we should prioritize fixing the billing flow.", "Oke. Posisi aku: kita harus prioritasin beresin alur billing."),
                ("Alex", "What's your main reason?", "Alasan utamanya apa?"),
                ("Mina", "The main reason is it affects revenue and support workload.", "Alasan utamanya: itu berdampak ke revenue dan beban tim support."),
                ("Alex", "Any counterpoints?", "Ada counterpoint?"),
                ("Mina", "Some teams prefer new features, but the risk is higher if billing stays broken.", "Ada tim yang pengen fitur baru, tapi risikonya lebih tinggi kalau billing tetap bermasalah."),
                ("Alex", "Okay. How do we close this?", "Oke. Gimana kita tutup?"),
                ("Mina", "To summarize, we focus on billing first. Next steps are: I'll share a plan today, and you'll review it by Friday.", "Singkatnya, kita fokus billing dulu. Next steps-nya: aku share plan hari ini, dan kamu review sebelum Jumat."),
            ],
            "useful_phrases": [
                {
                    "phrase": "My position is that we should prioritize fixing the billing flow.",
                    "meaning_id": "Posisi aku: kita harus prioritasin beresin alur billing.",
                    "usage_note": "A clear meeting position statement.",
                    "common_mistake": 'Do not say "my position is prioritize"; use my position is that we should.',
                },
                {
                    "phrase": "The main reason is it affects revenue and support workload.",
                    "meaning_id": "Alasan utamanya: itu berdampak ke revenue dan beban tim support.",
                    "usage_note": "A concise reason statement.",
                    "common_mistake": 'Do not list too many reasons; start with the main one.',
                },
                {
                    "phrase": "To summarize, we focus on billing first.",
                    "meaning_id": "Singkatnya, kita fokus billing dulu.",
                    "usage_note": "Closing summary language.",
                    "common_mistake": 'Do not introduce new points in the summary.',
                },
                {
                    "phrase": "Next steps are: I'll share a plan today, and you'll review it by Friday.",
                    "meaning_id": "Next steps-nya: aku share plan hari ini, dan kamu review sebelum Jumat.",
                    "usage_note": "Clear owners and deadlines.",
                    "common_mistake": 'Do not forget owners; say who does what by when.',
                },
                {
                    "phrase": "Some teams prefer new features, but the risk is higher if billing stays broken.",
                    "meaning_id": "Ada tim yang pengen fitur baru, tapi risikonya lebih tinggi kalau billing tetap bermasalah.",
                    "usage_note": "A calm counterpoint response.",
                    "common_mistake": "Do not dismiss the counterpoint; acknowledge then explain risk.",
                },
            ],
            "grammar_md": [
                ("Position + reason", ["My position is that we should ...", "The main reason is ..."]),
                ("Closing", ["To summarize, ...", "Next steps are: I'll ..., and you'll ... by ..."]),
            ],
            "pronunciation": [
                ("prioritize", "pry-OR-uh-tize."),
                ("revenue", "REV-uh-noo."),
                ("workload", "WERK-lohd."),
            ],
            "response_prompts": [
                {
                    "prompt": "State your position clearly.",
                    "target_response": "My position is that we should prioritize fixing the billing flow.",
                    "acceptable_variations": [
                        "My position is that we should prioritize fixing the billing flow.",
                        "My position is that we should fix billing before new features.",
                    ],
                },
                {
                    "prompt": "Give one main reason.",
                    "target_response": "The main reason is it affects revenue and support workload.",
                    "acceptable_variations": [
                        "The main reason is it affects revenue and support workload.",
                        "The main reason is it reduces risk and saves time.",
                    ],
                },
                {
                    "prompt": "Close with summary and next steps.",
                    "target_response": "To summarize, we focus on billing first. Next steps are: I'll share a plan today, and you'll review it by Friday.",
                    "acceptable_variations": [
                        "To summarize, we focus on billing first. Next steps are: I'll share a plan today, and you'll review it by Friday.",
                        "To summarize, we agree on option B. Next steps are: I'll draft the doc today, and you'll review it tomorrow.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "position_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase states your position in a meeting?",
                    "options": ["My position is that ...", "Position I ...", "No position."],
                    "correct_answer": "My position is that ...",
                },
                {
                    "key": "next_steps_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces next steps clearly?",
                    "options": ["Next steps are ...", "Next is whatever.", "No need."],
                    "correct_answer": "Next steps are ...",
                },
                {
                    "key": "summarize_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "to summarize" mean?',
                    "options": ["untuk merangkum", "untuk menolak", "untuk membeli"],
                    "correct_answer": "untuk merangkum",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_review_meeting",
                "opening_line": "Can you summarize your position?",
                "learner_goal": "State a position, support it, then close with summary and next steps.",
                "turns": [
                    {
                        "coach": "Can you summarize your position?",
                        "hint": "My position is that...",
                        "sample_answer": "My position is that we should prioritize fixing the billing flow.",
                        "focus": "Position",
                        "expected_keywords": ["position", "prioritize"],
                    },
                    {
                        "coach": "What's your main reason?",
                        "hint": "The main reason is...",
                        "sample_answer": "The main reason is it affects revenue and support workload.",
                        "focus": "Reason",
                        "expected_keywords": ["main reason", "affects"],
                    },
                    {
                        "coach": "Close with a summary and next steps.",
                        "hint": "To summarize... Next steps are...",
                        "sample_answer": "To summarize, we focus on billing first. Next steps are: I'll share a plan today, and you'll review it by Friday.",
                        "focus": "Close",
                        "expected_keywords": ["to summarize", "next steps", "by"],
                    },
                ],
                "target_phrases": ["My position is that ...", "The main reason is ...", "Next steps are ..."],
            },
            "reading_support": "A good meeting summary has three parts: your position, one strong reason, and a close with next steps (owner + deadline).",
            "writing_support_lines": [
                "Write 8 lines:",
                "1. My position is that ...",
                "2. The main reason is ...",
                "3. One example is ...",
                "4. A counterpoint is ...",
                "5. But the risk is ...",
                "6. To summarize, ...",
                "7. Next steps are: I'll ..., you'll ... by ...",
                "8. Does that work for everyone?",
            ],
            "goal_examples": ["My position is that ...", "The main reason is ...", "Next steps are ..."],
        },
        {
            "lesson_key": "lesson-02-review-negotiation-and-presenting",
            "slug": "review-negotiation-and-presenting",
            "title": "Review Negotiation and Presenting",
            "conversation_situation": "review_negotiation_presentation",
            "conversation_goal": "Propose a compromise, explain trade-offs, and present a recommendation with clear signposting.",
            "grammar_summary": "Use Here's my proposal... / The trade-off is... / On the other hand... / I'd recommend... to review negotiation language.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Review: kamu negosiasi timeline dan scope, jelasin trade-off, dan present rekomendasi singkat dengan signposting.",
            "dialogue": [
                ("Jordan", "We need this delivered next week."),
                ("Mina", "Here's my proposal: we deliver a smaller scope next week, then the full version two weeks later."),
                ("Jordan", "What's the trade-off?"),
                ("Mina", "The trade-off is speed versus completeness."),
                ("Jordan", "Can we meet in the middle?"),
                ("Mina", "Yes. On the other hand, we can include the top two features now and postpone the rest."),
                ("Jordan", "So what do you recommend?"),
                ("Mina", "I'd recommend that compromise. To summarize: top two features next week, the rest in two weeks."),
            ],
            "translations": [
                ("Jordan", "We need this delivered next week.", "Kita butuh ini selesai minggu depan."),
                ("Mina", "Here's my proposal: we deliver a smaller scope next week, then the full version two weeks later.", "Ini proposal aku: kita deliver scope yang lebih kecil minggu depan, lalu versi full dua minggu setelahnya."),
                ("Jordan", "What's the trade-off?", "Trade-off-nya apa?"),
                ("Mina", "The trade-off is speed versus completeness.", "Trade-off-nya kecepatan versus kelengkapan."),
                ("Jordan", "Can we meet in the middle?", "Bisa ketemu di tengah nggak?"),
                ("Mina", "Yes. On the other hand, we can include the top two features now and postpone the rest.", "Bisa. Di sisi lain, kita bisa masukin dua fitur paling penting sekarang dan tunda sisanya."),
                ("Jordan", "So what do you recommend?", "Jadi kamu rekomend apa?"),
                ("Mina", "I'd recommend that compromise. To summarize: top two features next week, the rest in two weeks.", "Aku rekomend kompromi itu. Singkatnya: dua fitur teratas minggu depan, sisanya dua minggu lagi."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Here's my proposal: we deliver a smaller scope next week.",
                    "meaning_id": "Ini proposal aku: kita deliver scope yang lebih kecil minggu depan.",
                    "usage_note": "A clear negotiation proposal.",
                    "common_mistake": "Do not propose without scope; specify what is included.",
                },
                {
                    "phrase": "The trade-off is speed versus completeness.",
                    "meaning_id": "Trade-off-nya kecepatan versus kelengkapan.",
                    "usage_note": "Explain trade-offs quickly.",
                    "common_mistake": "Do not over-explain; one trade-off first.",
                },
                {
                    "phrase": "Can we meet in the middle?",
                    "meaning_id": "Bisa ketemu di tengah nggak?",
                    "usage_note": "Invite compromise politely.",
                    "common_mistake": "Do not sound aggressive; keep it neutral.",
                },
                {
                    "phrase": "I'd recommend that compromise.",
                    "meaning_id": "Aku rekomend kompromi itu.",
                    "usage_note": "Recommendation language.",
                    "common_mistake": 'Do not say "I recommend you"; recommend the plan.',
                },
                {
                    "phrase": "To summarize: top two features next week, the rest in two weeks.",
                    "meaning_id": "Singkatnya: dua fitur teratas minggu depan, sisanya dua minggu lagi.",
                    "usage_note": "Signposted close.",
                    "common_mistake": "Do not add new scope in the summary.",
                },
            ],
            "grammar_md": [
                ("Negotiation proposals", ["Here's my proposal: ...", "Can we meet in the middle?"]),
                ("Trade-offs + summary", ["The trade-off is X versus Y.", "To summarize: ..."]),
            ],
            "pronunciation": [
                ("proposal", "pruh-POH-zuhl."),
                ("compromise", "KOM-pruh-mize."),
                ("completeness", "kuhm-PLEET-nis."),
            ],
            "response_prompts": [
                {
                    "prompt": "Make a proposal.",
                    "target_response": "Here's my proposal: we deliver a smaller scope next week, then the full version two weeks later.",
                    "acceptable_variations": [
                        "Here's my proposal: we deliver a smaller scope next week, then the full version two weeks later.",
                        "Here's my proposal: we deliver a pilot next week, then expand later.",
                    ],
                },
                {
                    "prompt": "Explain a trade-off.",
                    "target_response": "The trade-off is speed versus completeness.",
                    "acceptable_variations": [
                        "The trade-off is speed versus completeness.",
                        "The trade-off is speed versus reliability.",
                    ],
                },
                {
                    "prompt": "Close with a recommendation and summary.",
                    "target_response": "I'd recommend that compromise. To summarize: top two features next week, the rest in two weeks.",
                    "acceptable_variations": [
                        "I'd recommend that compromise. To summarize: top two features next week, the rest in two weeks.",
                        "I'd recommend the middle-ground option. To summarize: small scope first, then full scope.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "proposal_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a proposal?",
                    "options": ["Here's my proposal: ...", "Proposal is ...", "No plan."],
                    "correct_answer": "Here's my proposal: ...",
                },
                {
                    "key": "meet_middle",
                    "type": "multiple_choice",
                    "prompt": "Which phrase invites compromise?",
                    "options": ["Can we meet in the middle?", "Meet middle now.", "Stop."],
                    "correct_answer": "Can we meet in the middle?",
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
                "scenario_key": "b2_review_negotiation",
                "opening_line": "We need this delivered next week.",
                "learner_goal": "Propose a compromise, explain trade-offs, and recommend an option.",
                "turns": [
                    {
                        "coach": "We need this delivered next week.",
                        "hint": "Mulai dengan Here's my proposal...",
                        "sample_answer": "Here's my proposal: we deliver a smaller scope next week, then the full version two weeks later.",
                        "focus": "Proposal",
                        "expected_keywords": ["proposal", "scope"],
                    },
                    {
                        "coach": "What's the trade-off?",
                        "hint": "The trade-off is...",
                        "sample_answer": "The trade-off is speed versus completeness.",
                        "focus": "Trade-off",
                        "expected_keywords": ["trade-off"],
                    },
                    {
                        "coach": "Close with a recommendation and summary.",
                        "hint": "I'd recommend... To summarize...",
                        "sample_answer": "I'd recommend that compromise. To summarize: top two features next week, the rest in two weeks.",
                        "focus": "Close",
                        "expected_keywords": ["recommend", "to summarize"],
                    },
                ],
                "target_phrases": ["Here's my proposal: ...", "The trade-off is ...", "I'd recommend ..."],
            },
            "reading_support": "In negotiation, keep it structured: proposal, trade-off, compromise, recommendation, and a short summary with dates.",
            "writing_support_lines": [
                "Write 8 lines:",
                "1. Here's my proposal: ...",
                "2. The trade-off is ...",
                "3. Can we meet in the middle?",
                "4. On the other hand, ...",
                "5. I'd recommend ...",
                "6. To summarize: ...",
                "7. Next week we deliver ...",
                "8. Two weeks later we deliver ...",
            ],
            "goal_examples": ["Here's my proposal: ...", "The trade-off is ...", "I'd recommend ..."],
        },
        {
            "lesson_key": "lesson-03-review-information-and-clients",
            "slug": "review-information-and-clients",
            "title": "Review Information and Clients",
            "conversation_situation": "review_information_client_call",
            "conversation_goal": "Discuss information sources carefully and handle a client call with clarity, empathy, and next steps.",
            "grammar_summary": "Use Based on the source... / We should verify... / I understand the concern... / Next steps are... to review information and client communication.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Review: kamu bahas sumber informasi (reliability) dan jalankan mini client call: clarify, handle concerns, confirm next steps.",
            "dialogue": [
                ("Jordan", "We saw a report saying complaints are up. Is it reliable?"),
                ("Mina", "Based on the source, it's a partial snapshot. We should verify it with our support data."),
                ("Jordan", "Clients are worried about delays."),
                ("Mina", "I understand the concern. Just to clarify, what timeline did we promise?"),
                ("Jordan", "Two weeks."),
                ("Mina", "Got it. Next steps are: I'll share an update today, and we'll confirm a revised timeline by Friday."),
                ("Jordan", "Sounds good."),
                ("Mina", "Great. We'll keep you posted with weekly summaries."),
            ],
            "translations": [
                ("Jordan", "We saw a report saying complaints are up. Is it reliable?", "Kita lihat report bilang komplain naik. Itu reliable nggak?"),
                ("Mina", "Based on the source, it's a partial snapshot. We should verify it with our support data.", "Berdasarkan sumbernya, itu cuma snapshot sebagian. Kita harus verifikasi pakai data support kita."),
                ("Jordan", "Clients are worried about delays.", "Klien khawatir soal keterlambatan."),
                ("Mina", "I understand the concern. Just to clarify, what timeline did we promise?", "Aku paham kekhawatirannya. Biar jelas, timeline apa yang kita janjikan?"),
                ("Jordan", "Two weeks.", "Dua minggu."),
                ("Mina", "Got it. Next steps are: I'll share an update today, and we'll confirm a revised timeline by Friday.", "Oke. Next steps-nya: aku share update hari ini, dan kita konfirmasi timeline revisi sebelum Jumat."),
                ("Jordan", "Sounds good.", "Oke."),
                ("Mina", "Great. We'll keep you posted with weekly summaries.", "Oke. Kita akan update kamu lewat ringkasan mingguan."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Based on the source, it's a partial snapshot.",
                    "meaning_id": "Berdasarkan sumbernya, itu cuma snapshot sebagian.",
                    "usage_note": "Discuss source limitations carefully.",
                    "common_mistake": "Do not treat one report as the full truth; mention limits.",
                },
                {
                    "phrase": "We should verify it with our support data.",
                    "meaning_id": "Kita harus verifikasi pakai data support kita.",
                    "usage_note": "Verification language.",
                    "common_mistake": 'Do not say "verify with data are"; use verify it with.',
                },
                {
                    "phrase": "I understand the concern.",
                    "meaning_id": "Aku paham kekhawatirannya.",
                    "usage_note": "Empathetic opener for clients.",
                    "common_mistake": "Do not dismiss concerns; acknowledge first.",
                },
                {
                    "phrase": "Just to clarify, what timeline did we promise?",
                    "meaning_id": "Biar jelas, timeline apa yang kita janjikan?",
                    "usage_note": "Clarify commitments.",
                    "common_mistake": "Do not blame; just clarify.",
                },
                {
                    "phrase": "Next steps are: I'll share an update today, and we'll confirm a revised timeline by Friday.",
                    "meaning_id": "Next steps-nya: aku share update hari ini, dan kita konfirmasi timeline revisi sebelum Jumat.",
                    "usage_note": "Close with next steps.",
                    "common_mistake": "Do not give next steps without deadlines.",
                },
            ],
            "grammar_md": [
                ("Source reliability", ["Based on the source, ...", "We should verify it with ..."]),
                ("Client clarity", ["I understand the concern.", "Just to clarify, ...", "Next steps are ..."]),
            ],
            "pronunciation": [
                ("reliable", "ri-LYE-uh-buhl."),
                ("verify", "VER-uh-fy."),
                ("snapshot", "SNAP-shot."),
            ],
            "response_prompts": [
                {
                    "prompt": "Comment on reliability carefully.",
                    "target_response": "Based on the source, it's a partial snapshot. We should verify it with our support data.",
                    "acceptable_variations": [
                        "Based on the source, it's a partial snapshot. We should verify it with our support data.",
                        "Based on the source, it may be incomplete. We should verify it with our logs.",
                    ],
                },
                {
                    "prompt": "Acknowledge concern and clarify timeline.",
                    "target_response": "I understand the concern. Just to clarify, what timeline did we promise?",
                    "acceptable_variations": [
                        "I understand the concern. Just to clarify, what timeline did we promise?",
                        "I understand the concern. Just to clarify, what deadline did we commit to?",
                    ],
                },
                {
                    "prompt": "Close with next steps.",
                    "target_response": "Next steps are: I'll share an update today, and we'll confirm a revised timeline by Friday.",
                    "acceptable_variations": [
                        "Next steps are: I'll share an update today, and we'll confirm a revised timeline by Friday.",
                        "Next steps are: I'll send a summary today, and we'll confirm the plan tomorrow.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "verify_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase suggests verification?",
                    "options": ["We should verify it with our data.", "It's always true.", "No need to check."],
                    "correct_answer": "We should verify it with our data.",
                },
                {
                    "key": "timeline_clarify",
                    "type": "multiple_choice",
                    "prompt": "Which phrase clarifies a timeline politely?",
                    "options": ["Just to clarify, what timeline did we promise?", "You promised wrong.", "Why did you lie?"],
                    "correct_answer": "Just to clarify, what timeline did we promise?",
                },
                {
                    "key": "reliable_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "reliable" mean?',
                    "options": ["bisa dipercaya", "terlambat", "murah"],
                    "correct_answer": "bisa dipercaya",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_review_clients",
                "opening_line": "Is this report reliable? Clients are worried.",
                "learner_goal": "Discuss reliability, acknowledge concerns, clarify commitments, and close with next steps.",
                "turns": [
                    {
                        "coach": "Is this report reliable?",
                        "hint": "Based on the source... verify...",
                        "sample_answer": "Based on the source, it's a partial snapshot. We should verify it with our support data.",
                        "focus": "Reliability",
                        "expected_keywords": ["source", "verify"],
                    },
                    {
                        "coach": "Clients are worried about delays. What do you say?",
                        "hint": "I understand the concern... Just to clarify...",
                        "sample_answer": "I understand the concern. Just to clarify, what timeline did we promise?",
                        "focus": "Concern + clarify",
                        "expected_keywords": ["understand", "clarify", "timeline"],
                    },
                    {
                        "coach": "Close with next steps and a deadline.",
                        "hint": "Next steps are... today... by Friday.",
                        "sample_answer": "Next steps are: I'll share an update today, and we'll confirm a revised timeline by Friday.",
                        "focus": "Next steps",
                        "expected_keywords": ["next steps", "today", "by"],
                    },
                ],
                "target_phrases": ["We should verify it with ...", "I understand the concern.", "Next steps are ..."],
            },
            "reading_support": "When discussing information, separate what you know from what you suspect. For client communication, acknowledge concerns, clarify commitments, and confirm next steps with deadlines.",
            "writing_support_lines": [
                "Write 9 lines:",
                "1. Based on the source, ...",
                "2. We should verify it with ...",
                "3. I understand the concern.",
                "4. Just to clarify, ...",
                "5. What timeline did we promise?",
                "6. Next steps are: ...",
                "7. I'll share an update today.",
                "8. We'll confirm a revised timeline by Friday.",
                "9. We'll keep you posted weekly.",
            ],
            "goal_examples": ["We should verify it with ...", "I understand the concern.", "Next steps are ..."],
        },
        {
            "lesson_key": "lesson-04-b2-final-test-practice",
            "slug": "b2-final-test-practice",
            "title": "B2 Final Test Practice",
            "conversation_situation": "final_test_practice",
            "conversation_goal": "Answer a set of B2-style prompts: position, evidence, trade-offs, recommendation, and next steps.",
            "grammar_summary": "Use signposting: My position is... / Based on the data... / The trade-off is... / I'd recommend... / Next steps are...",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Latihan final: kamu jawab prompt satu per satu dengan struktur B2 yang rapi dan natural.",
            "dialogue": [
                ("Alex", "Final practice: what's your position?"),
                ("Mina", "My position is that we should run a two-week pilot before a full rollout."),
                ("Alex", "What's your evidence?"),
                ("Mina", "Based on the data, drop-offs increased after the redesign."),
                ("Alex", "Explain the trade-off."),
                ("Mina", "The trade-off is speed versus long-term reliability."),
                ("Alex", "Make a recommendation and next steps."),
                ("Mina", "I'd recommend the pilot. Next steps are: I'll draft the plan today, and you'll review it by Friday."),
            ],
            "translations": [
                ("Alex", "Final practice: what's your position?", "Latihan final: posisi kamu apa?"),
                ("Mina", "My position is that we should run a two-week pilot before a full rollout.", "Posisi aku: kita harus jalankan pilot dua minggu sebelum rollout penuh."),
                ("Alex", "What's your evidence?", "Buktinya apa?"),
                ("Mina", "Based on the data, drop-offs increased after the redesign.", "Berdasarkan data, drop-off naik setelah redesign."),
                ("Alex", "Explain the trade-off.", "Jelasin trade-off-nya."),
                ("Mina", "The trade-off is speed versus long-term reliability.", "Trade-off-nya kecepatan versus reliability jangka panjang."),
                ("Alex", "Make a recommendation and next steps.", "Kasih rekomendasi dan next steps."),
                ("Mina", "I'd recommend the pilot. Next steps are: I'll draft the plan today, and you'll review it by Friday.", "Aku rekomend pilot. Next steps-nya: aku draft plan hari ini, dan kamu review sebelum Jumat."),
            ],
            "useful_phrases": [
                {
                    "phrase": "My position is that we should run a two-week pilot before a full rollout.",
                    "meaning_id": "Posisi aku: kita harus jalankan pilot dua minggu sebelum rollout penuh.",
                    "usage_note": "Position statement for a test response.",
                    "common_mistake": "Do not start with unrelated context; state position first.",
                },
                {
                    "phrase": "Based on the data, drop-offs increased after the redesign.",
                    "meaning_id": "Berdasarkan data, drop-off naik setelah redesign.",
                    "usage_note": "Evidence language.",
                    "common_mistake": "Do not say datas; data is uncountable.",
                },
                {
                    "phrase": "The trade-off is speed versus long-term reliability.",
                    "meaning_id": "Trade-off-nya kecepatan versus reliability jangka panjang.",
                    "usage_note": "Trade-off explanation.",
                    "common_mistake": "Do not list too many trade-offs at once.",
                },
                {
                    "phrase": "I'd recommend the pilot.",
                    "meaning_id": "Aku rekomend pilot.",
                    "usage_note": "Recommendation phrase.",
                    "common_mistake": 'Do not say "I recommend you"; recommend the plan.',
                },
                {
                    "phrase": "Next steps are: I'll draft the plan today, and you'll review it by Friday.",
                    "meaning_id": "Next steps-nya: aku draft plan hari ini, dan kamu review sebelum Jumat.",
                    "usage_note": "Next steps with owners and deadlines.",
                    "common_mistake": "Do not forget the deadline (by Friday).",
                },
            ],
            "grammar_md": [
                (
                    "Signposting (test answers)",
                    [
                        "My position is that ...",
                        "Based on the data, ...",
                        "The trade-off is X versus Y.",
                        "I'd recommend ...",
                        "Next steps are ...",
                    ],
                )
            ],
            "pronunciation": [
                ("pilot", "PY-lut."),
                ("rollout", "ROHL-out."),
                ("signposting", "SYNE-post-ing."),
            ],
            "response_prompts": [
                {
                    "prompt": "State a position.",
                    "target_response": "My position is that we should run a two-week pilot before a full rollout.",
                    "acceptable_variations": [
                        "My position is that we should run a two-week pilot before a full rollout.",
                        "My position is that we should start with a small pilot first.",
                    ],
                },
                {
                    "prompt": "State evidence.",
                    "target_response": "Based on the data, drop-offs increased after the redesign.",
                    "acceptable_variations": [
                        "Based on the data, drop-offs increased after the redesign.",
                        "Based on the data, complaints increased after the change.",
                    ],
                },
                {
                    "prompt": "Close with recommendation and next steps.",
                    "target_response": "I'd recommend the pilot. Next steps are: I'll draft the plan today, and you'll review it by Friday.",
                    "acceptable_variations": [
                        "I'd recommend the pilot. Next steps are: I'll draft the plan today, and you'll review it by Friday.",
                        "I'd recommend a pilot first. Next steps are: I'll send a draft today, and you'll review it tomorrow.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "signposting_order",
                    "type": "multiple_choice",
                    "prompt": "Which order is best for a structured answer?",
                    "options": [
                        "Position -> evidence -> trade-off -> recommendation -> next steps",
                        "Jokes -> evidence -> goodbye",
                        "Trade-off -> colors -> position",
                    ],
                    "correct_answer": "Position -> evidence -> trade-off -> recommendation -> next steps",
                },
                {
                    "key": "rollout_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "rollout" mean?',
                    "options": ["peluncuran/penerapan", "istirahat", "harga"],
                    "correct_answer": "peluncuran/penerapan",
                },
                {
                    "key": "pilot_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "pilot" mean in projects?',
                    "options": ["uji coba kecil", "pilot pesawat", "warna"],
                    "correct_answer": "uji coba kecil",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_final_practice",
                "opening_line": "Final practice: answer my prompts.",
                "learner_goal": "Answer B2 prompts with clear signposting.",
                "turns": [
                    {
                        "coach": "What's your position?",
                        "hint": "My position is that...",
                        "sample_answer": "My position is that we should run a two-week pilot before a full rollout.",
                        "focus": "Position",
                        "expected_keywords": ["position", "pilot"],
                    },
                    {
                        "coach": "What's your evidence and trade-off?",
                        "hint": "Based on the data... The trade-off is...",
                        "sample_answer": "Based on the data, drop-offs increased after the redesign. The trade-off is speed versus long-term reliability.",
                        "focus": "Evidence + trade-off",
                        "expected_keywords": ["based on", "data", "trade-off"],
                    },
                    {
                        "coach": "Recommend a next step and timeline.",
                        "hint": "I'd recommend... Next steps are... by Friday.",
                        "sample_answer": "I'd recommend the pilot. Next steps are: I'll draft the plan today, and you'll review it by Friday.",
                        "focus": "Recommendation + next steps",
                        "expected_keywords": ["recommend", "next steps", "by"],
                    },
                ],
                "target_phrases": ["My position is that ...", "Based on the data, ...", "Next steps are ..."],
            },
            "reading_support": "For test-style prompts, keep answers short and signposted. One sentence per prompt is enough: position, evidence, trade-off, recommendation, next steps.",
            "writing_support_lines": [
                "Write 10 lines (one per prompt):",
                "1. My position is that ...",
                "2. The main reason is ...",
                "3. Based on the data, ...",
                "4. One possible cause is ...",
                "5. The trade-off is ...",
                "6. On the other hand, ...",
                "7. I'd recommend ...",
                "8. The main risk is ...",
                "9. We can mitigate it by ...",
                "10. Next steps are ...",
            ],
            "goal_examples": ["My position is that ...", "Based on the data, ...", "Next steps are ..."],
        },
        {
            "lesson_key": "lesson-05-b2-final-discussion",
            "slug": "b2-final-discussion",
            "title": "B2 Final Discussion",
            "conversation_situation": "final_discussion_scenario",
            "conversation_goal": "Hold a final B2 discussion: frame the issue, compare options, address concerns, and align on a decision.",
            "grammar_summary": "Use Let's define the scope... / Based on the data... / The trade-off is... / Given these constraints... / Next steps are...",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Final: kamu pimpin diskusi profesional yang utuh dan natural (problem framing, trade-off, rekomendasi, next steps).",
            "dialogue": [
                ("Jordan", "We need to decide our approach for the next quarter."),
                ("Mina", "Great. Let's define the scope and what success looks like."),
                ("Jordan", "We want fewer complaints and faster completion."),
                ("Mina", "Based on the data, the billing redesign increased drop-offs, so we should address that first."),
                ("Jordan", "But leadership wants new features too."),
                ("Mina", "I understand the concern. The trade-off is speed versus reliability. Given these constraints, I'd recommend a time-boxed pilot."),
                ("Jordan", "Okay. What are the next steps?"),
                ("Mina", "Next steps are: I'll share a plan today, and you'll review it by Friday. Then we finalize on Monday."),
            ],
            "translations": [
                ("Jordan", "We need to decide our approach for the next quarter.", "Kita harus putuskan pendekatan untuk kuartal depan."),
                ("Mina", "Great. Let's define the scope and what success looks like.", "Oke. Kita definisikan scope dan seperti apa suksesnya."),
                ("Jordan", "We want fewer complaints and faster completion.", "Kita mau komplain berkurang dan completion lebih cepat."),
                ("Mina", "Based on the data, the billing redesign increased drop-offs, so we should address that first.", "Berdasarkan data, redesign billing bikin drop-off naik, jadi kita harus beresin itu dulu."),
                ("Jordan", "But leadership wants new features too.", "Tapi leadership juga mau fitur baru."),
                ("Mina", "I understand the concern. The trade-off is speed versus reliability. Given these constraints, I'd recommend a time-boxed pilot.", "Aku paham kekhawatirannya. Trade-off-nya kecepatan versus reliability. Dengan constraint ini, aku rekomend pilot yang time-boxed."),
                ("Jordan", "Okay. What are the next steps?", "Oke. Next steps-nya apa?"),
                ("Mina", "Next steps are: I'll share a plan today, and you'll review it by Friday. Then we finalize on Monday.", "Next steps-nya: aku share plan hari ini, dan kamu review sebelum Jumat. Lalu kita finalize Senin."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let's define the scope and what success looks like.",
                    "meaning_id": "Kita definisikan scope dan seperti apa suksesnya.",
                    "usage_note": "Frame a discussion at the start.",
                    "common_mistake": "Do not start with details; frame first.",
                },
                {
                    "phrase": "Based on the data, we should address billing first.",
                    "meaning_id": "Berdasarkan data, kita harus beresin billing dulu.",
                    "usage_note": "Evidence-driven recommendation.",
                    "common_mistake": "Do not present opinions as facts; cite data.",
                },
                {
                    "phrase": "I understand the concern.",
                    "meaning_id": "Aku paham kekhawatirannya.",
                    "usage_note": "Acknowledge concerns before trade-offs.",
                    "common_mistake": "Do not dismiss; acknowledge first.",
                },
                {
                    "phrase": "Given these constraints, I'd recommend a time-boxed pilot.",
                    "meaning_id": "Dengan constraint ini, aku rekomend pilot yang time-boxed.",
                    "usage_note": "Recommendation with constraints.",
                    "common_mistake": 'Do not say "recommend to do"; use recommend a pilot.',
                },
                {
                    "phrase": "Next steps are: I'll share a plan today, and you'll review it by Friday.",
                    "meaning_id": "Next steps-nya: aku share plan hari ini, dan kamu review sebelum Jumat.",
                    "usage_note": "Close with owners and deadlines.",
                    "common_mistake": "Do not skip the deadline; use by Friday.",
                },
            ],
            "grammar_md": [
                ("Discussion framing", ["Let's define the scope.", "What does success look like?"]),
                ("Decision language", ["Given these constraints, I'd recommend ...", "Next steps are ..."]),
            ],
            "pronunciation": [
                ("quarter", "KWOR-ter."),
                ("time-boxed", "TIME-bokst."),
                ("finalize", "FYE-nuh-lize."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start by framing the discussion.",
                    "target_response": "Let's define the scope and what success looks like.",
                    "acceptable_variations": [
                        "Let's define the scope and what success looks like.",
                        "Let's define the scope and success criteria.",
                    ],
                },
                {
                    "prompt": "Recommend an approach based on constraints.",
                    "target_response": "Given these constraints, I'd recommend a time-boxed pilot.",
                    "acceptable_variations": [
                        "Given these constraints, I'd recommend a time-boxed pilot.",
                        "Given these constraints, I'd recommend starting with a pilot.",
                    ],
                },
                {
                    "prompt": "Close with next steps and timeline.",
                    "target_response": "Next steps are: I'll share a plan today, and you'll review it by Friday.",
                    "acceptable_variations": [
                        "Next steps are: I'll share a plan today, and you'll review it by Friday.",
                        "Next steps are: I'll send a draft today, and you'll review it tomorrow.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "timeboxed_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "time-boxed" mean?',
                    "options": ["dibatasi waktu", "tanpa batas", "lebih mahal"],
                    "correct_answer": "dibatasi waktu",
                },
                {
                    "key": "frame_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase frames a discussion at the start?",
                    "options": ["Let's define the scope.", "Whatever.", "Stop."],
                    "correct_answer": "Let's define the scope.",
                },
                {
                    "key": "constraints_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase links a recommendation to constraints?",
                    "options": ["Given these constraints, I'd recommend ...", "I recommend because yes.", "No constraints."],
                    "correct_answer": "Given these constraints, I'd recommend ...",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_final_discussion",
                "opening_line": "We need to decide our approach for next quarter.",
                "learner_goal": "Lead a final discussion from framing to decision and next steps.",
                "turns": [
                    {
                        "coach": "Start by framing the scope and success criteria.",
                        "hint": "Let's define the scope... what does success look like?",
                        "sample_answer": "Great. Let's define the scope and what success looks like.",
                        "focus": "Frame",
                        "expected_keywords": ["scope", "success"],
                    },
                    {
                        "coach": "Leadership wants new features too. Handle concerns and trade-offs.",
                        "hint": "I understand the concern... The trade-off is...",
                        "sample_answer": "I understand the concern. The trade-off is speed versus reliability, so we should keep scope tight.",
                        "focus": "Concerns + trade-offs",
                        "expected_keywords": ["understand", "trade-off"],
                    },
                    {
                        "coach": "Make a recommendation and confirm next steps with timeline.",
                        "hint": "Given these constraints... Next steps are... today... by Friday.",
                        "sample_answer": "Given these constraints, I'd recommend a time-boxed pilot. Next steps are: I'll share a plan today, and you'll review it by Friday.",
                        "focus": "Decision + next steps",
                        "expected_keywords": ["recommend", "next steps", "by"],
                    },
                ],
                "target_phrases": ["Let's define the scope.", "The trade-off is ...", "Next steps are ..."],
            },
            "reading_support": "A strong final discussion is structured: frame the scope and success criteria, present evidence, acknowledge concerns, explain trade-offs, recommend a plan, then confirm next steps with deadlines.",
            "writing_support_lines": [
                "Write your final discussion (10 lines):",
                "1. Let's define the scope ...",
                "2. What does success look like?",
                "3. Based on the data, ...",
                "4. I understand the concern ...",
                "5. The trade-off is ...",
                "6. Given these constraints, I'd recommend ...",
                "7. The main risk is ...",
                "8. We can mitigate it by ...",
                "9. Next steps are: I'll ..., you'll ... by ...",
                "10. Great, let's finalize on ...",
            ],
            "goal_examples": ["Let's define the scope.", "The trade-off is ...", "Next steps are ..."],
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

