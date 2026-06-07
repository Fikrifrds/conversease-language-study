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
            "- Tone: professional, calm, collaborative",
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

        Read it again and underline the negotiation words (priority, trade-off, proposal, concern, compromise).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B2"
    b2_root = Path("content/curriculum/english/B2")
    units_root = b2_root / "units"
    unit_key = "unit-03-negotiation-and-compromise"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-03-negotiation-and-compromise
            level_code: B2
            title: Negotiation & Compromise
            main_conversation_outcome: Negotiate simple professional outcomes and find compromise.
            status: in_production
            lessons:
              - lesson-01-expressing-priorities
              - lesson-02-making-a-proposal
              - lesson-03-handling-objections
              - lesson-04-finding-middle-ground
              - lesson-05-negotiation-mission
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
            "lesson_key": "lesson-01-expressing-priorities",
            "slug": "expressing-priorities",
            "title": "Expressing Priorities",
            "conversation_situation": "expressing_priorities",
            "conversation_goal": "State your priorities clearly, explain what matters most, and ask about the other person's priorities.",
            "grammar_summary": "Use My top priority is... / What matters most is... / What's your priority? to align on priorities.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu lagi diskusi rencana kerja. Kamu jelasin prioritas utama kamu, jelasin alasannya singkat, lalu tanya prioritas lawan bicara.",
            "dialogue": [
                ("Alex", "We have limited time. What should we focus on first?"),
                ("Mina", "My top priority is shipping the core feature safely."),
                ("Alex", "Why that first?"),
                ("Mina", "Because it's the main value for users, and the deadline is close."),
                ("Alex", "Okay. Anything else?"),
                ("Mina", "The second priority is improving monitoring, so we can catch issues early."),
                ("Alex", "Makes sense. What's your priority?"),
                ("Mina", "What about you? What's your top priority?"),
            ],
            "translations": [
                ("Alex", "We have limited time. What should we focus on first?", "Waktu kita terbatas. Kita fokus apa dulu?"),
                ("Mina", "My top priority is shipping the core feature safely.", "Prioritas utamaku adalah rilis fitur utama dengan aman."),
                ("Alex", "Why that first?", "Kenapa itu dulu?"),
                ("Mina", "Because it's the main value for users, and the deadline is close.", "Karena itu nilai utama buat user, dan deadline-nya dekat."),
                ("Alex", "Okay. Anything else?", "Oke. Ada yang lain?"),
                ("Mina", "The second priority is improving monitoring, so we can catch issues early.", "Prioritas kedua adalah ningkatin monitoring, jadi kita bisa nangkep masalah lebih cepat."),
                ("Alex", "Makes sense. What's your priority?", "Masuk akal. Prioritasmu apa?"),
                ("Mina", "What about you? What's your top priority?", "Kalau kamu gimana? Prioritas utamamu apa?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "My top priority is shipping the core feature safely.",
                    "meaning_id": "Prioritas utamaku adalah rilis fitur utama dengan aman.",
                    "usage_note": "A clear priority statement.",
                    "common_mistake": 'Do not say "My top priority shipping"; include is.',
                },
                {
                    "phrase": "What matters most is shipping safely.",
                    "meaning_id": "Yang paling penting adalah rilis dengan aman.",
                    "usage_note": "A natural way to emphasize importance.",
                    "common_mistake": 'Do not say "What matter most"; add -s.',
                },
                {
                    "phrase": "Because the deadline is close.",
                    "meaning_id": "Karena deadline-nya dekat.",
                    "usage_note": "A short reason sentence.",
                    "common_mistake": 'Do not say "Because deadline close" without the.',
                },
                {
                    "phrase": "The second priority is improving monitoring.",
                    "meaning_id": "Prioritas kedua adalah ningkatin monitoring.",
                    "usage_note": "Add a second priority clearly.",
                    "common_mistake": 'Do not say "second priority are"; use is.',
                },
                {
                    "phrase": "What about you? What's your top priority?",
                    "meaning_id": "Kalau kamu gimana? Prioritas utamamu apa?",
                    "usage_note": "Ask for the other person's priorities.",
                    "common_mistake": 'Do not ask vaguely; use top priority for clarity.',
                },
            ],
            "grammar_md": [
                ("Priority statements", ["My top priority is shipping safely.", "The second priority is improving monitoring."]),
                ("What matters most", ["What matters most is meeting the deadline.", "What matters most is quality."]),
            ],
            "pronunciation": [
                ("priority", "pry-OR-i-tee."),
                ("deadline", "DED-line."),
                ("monitoring", "MON-i-ter-ing."),
            ],
            "response_prompts": [
                {
                    "prompt": "State your top priority.",
                    "target_response": "My top priority is shipping the core feature safely.",
                    "acceptable_variations": [
                        "My top priority is shipping the core feature safely.",
                        "My top priority is meeting the deadline.",
                    ],
                },
                {
                    "prompt": "Explain what matters most.",
                    "target_response": "What matters most is quality.",
                    "acceptable_variations": ["What matters most is quality.", "What matters most is speed."],
                },
                {
                    "prompt": "Ask about the other person's priorities.",
                    "target_response": "What about you? What's your top priority?",
                    "acceptable_variations": ["What about you? What's your top priority?", "What's your priority for this sprint?"],
                },
            ],
            "quiz": [
                {
                    "key": "priority_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which sentence states a top priority?",
                    "options": ["My top priority is ...", "My top priority ...", "Top priority I ..."],
                    "correct_answer": "My top priority is ...",
                },
                {
                    "key": "matters_most",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["What matters most is quality.", "What matter most is quality.", "What matters most quality."],
                    "correct_answer": "What matters most is quality.",
                },
                {
                    "key": "deadline_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "deadline" mean?',
                    "options": ["batas waktu", "libur", "alasan"],
                    "correct_answer": "batas waktu",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_negotiation_priorities",
                "opening_line": "We have limited time. What's your top priority?",
                "learner_goal": "State your priorities clearly and ask about the other person's priorities.",
                "turns": [
                    {
                        "coach": "What's your top priority?",
                        "hint": "Mulai dengan My top priority is...",
                        "sample_answer": "My top priority is shipping the core feature safely.",
                        "focus": "State top priority",
                        "expected_keywords": ["top priority", "is"],
                    },
                    {
                        "coach": "Why is that important?",
                        "hint": "Jawab dengan because + reason.",
                        "sample_answer": "Because it's the main value for users and the deadline is close.",
                        "focus": "Give reason",
                        "expected_keywords": ["because", "deadline"],
                    },
                    {
                        "coach": "Ask about my priorities.",
                        "hint": "Gunakan What about you? What's your top priority?",
                        "sample_answer": "What about you? What's your top priority?",
                        "focus": "Ask other priorities",
                        "expected_keywords": ["what about you", "top priority"],
                    },
                ],
                "target_phrases": ["My top priority is ...", "What matters most is ...", "What's your top priority?"],
            },
            "reading_support": "In negotiations, align on priorities first. State your top priority, explain why it matters, and ask the other person what matters most for them.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. My top priority is ...",
                "2. Because ...",
                "3. The second priority is ...",
                "4. What matters most is ...",
                "5. What about you?",
                "6. What's your top priority?",
            ],
            "goal_examples": ["My top priority is ...", "What matters most is ...", "What's your top priority?"],
        },
        {
            "lesson_key": "lesson-02-making-a-proposal",
            "slug": "making-a-proposal",
            "title": "Making a Proposal",
            "conversation_situation": "making_a_proposal",
            "conversation_goal": "Make a clear proposal, suggest a timeline, and ask if it works.",
            "grammar_summary": "Use I propose we... / How about we... / Would that work? to make proposals politely and clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu negosiasi rencana. Kamu ajukan proposal, sebut timeline, lalu tanya apakah itu works buat tim.",
            "dialogue": [
                ("Alex", "How should we handle the launch plan?"),
                ("Mina", "I propose we do a small pilot first."),
                ("Alex", "What timeline are you thinking?"),
                ("Mina", "How about we run it for two weeks and review the results?"),
                ("Alex", "Would that delay the full launch?"),
                ("Mina", "Not necessarily. We can prepare in parallel."),
                ("Alex", "Okay. Would that work for you?"),
                ("Mina", "Yes, that works for me."),
            ],
            "translations": [
                ("Alex", "How should we handle the launch plan?", "Kita handle launch plan gimana?"),
                ("Mina", "I propose we do a small pilot first.", "Aku usul kita coba pilot kecil dulu."),
                ("Alex", "What timeline are you thinking?", "Timeline yang kamu bayangin gimana?"),
                ("Mina", "How about we run it for two weeks and review the results?", "Gimana kalau kita jalanin dua minggu lalu review hasilnya?"),
                ("Alex", "Would that delay the full launch?", "Itu bakal nunda full launch nggak?"),
                ("Mina", "Not necessarily. We can prepare in parallel.", "Belum tentu. Kita bisa siapin paralel."),
                ("Alex", "Okay. Would that work for you?", "Oke. Itu works buat kamu?"),
                ("Mina", "Yes, that works for me.", "Iya, itu works buat aku."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I propose we do a small pilot first.",
                    "meaning_id": "Aku usul kita coba pilot kecil dulu.",
                    "usage_note": "A clear, formal proposal phrase.",
                    "common_mistake": 'Do not say "I propose to do"; use I propose we do.',
                },
                {
                    "phrase": "How about we run it for two weeks?",
                    "meaning_id": "Gimana kalau kita jalanin dua minggu?",
                    "usage_note": "A friendly proposal.",
                    "common_mistake": 'Do not say "How about we runs"; use run.',
                },
                {
                    "phrase": "Would that work for you?",
                    "meaning_id": "Itu works buat kamu?",
                    "usage_note": "Check agreement.",
                    "common_mistake": 'Do not say "Will that work" if you want a softer tone; would is softer.',
                },
                {
                    "phrase": "Not necessarily.",
                    "meaning_id": "Belum tentu.",
                    "usage_note": "A professional way to disagree softly.",
                    "common_mistake": 'Do not say "No" too fast; use not necessarily if uncertain.',
                },
                {
                    "phrase": "We can prepare in parallel.",
                    "meaning_id": "Kita bisa siapin paralel.",
                    "usage_note": "Offer a solution to reduce risk.",
                    "common_mistake": 'Do not say "prepare parallel"; use in parallel.',
                },
            ],
            "grammar_md": [
                ("I propose we...", ["I propose we do a small pilot first.", "I propose we meet with the client tomorrow."]),
                ("Would that work?", ["Would that work for you?", "Would that work for the team?"]),
            ],
            "pronunciation": [
                ("propose", "pruh-POHZ."),
                ("pilot", "PY-lut."),
                ("parallel", "PAIR-uh-lel."),
            ],
            "response_prompts": [
                {
                    "prompt": "Make a proposal with I propose we...",
                    "target_response": "I propose we do a small pilot first.",
                    "acceptable_variations": ["I propose we do a small pilot first.", "I propose we start next week."],
                },
                {
                    "prompt": "Suggest a timeline.",
                    "target_response": "How about we run it for two weeks and review the results?",
                    "acceptable_variations": [
                        "How about we run it for two weeks and review the results?",
                        "How about we try it for one week?",
                    ],
                },
                {
                    "prompt": "Check agreement.",
                    "target_response": "Would that work for you?",
                    "acceptable_variations": ["Would that work for you?", "Would that work for the team?"],
                },
            ],
            "quiz": [
                {
                    "key": "propose_structure",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["I propose we do a small pilot.", "I propose to do a small pilot.", "I propose doing a small pilot we."],
                    "correct_answer": "I propose we do a small pilot.",
                },
                {
                    "key": "would_that_work",
                    "type": "multiple_choice",
                    "prompt": "Which question checks agreement politely?",
                    "options": ["Would that work for you?", "You do it now?", "Why you not?"],
                    "correct_answer": "Would that work for you?",
                },
                {
                    "key": "not_necessarily",
                    "type": "multiple_choice",
                    "prompt": 'What does "Not necessarily" mean?',
                    "options": ["belum tentu", "pasti", "tidak pernah"],
                    "correct_answer": "belum tentu",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_negotiation_proposal",
                "opening_line": "We need a plan. What do you propose?",
                "learner_goal": "Make a proposal, suggest a timeline, and check agreement.",
                "turns": [
                    {
                        "coach": "What do you propose?",
                        "hint": "Gunakan I propose we...",
                        "sample_answer": "I propose we do a small pilot first.",
                        "focus": "Make proposal",
                        "expected_keywords": ["propose"],
                    },
                    {
                        "coach": "What's the timeline?",
                        "hint": "How about we run it for ... weeks?",
                        "sample_answer": "How about we run it for two weeks and review the results?",
                        "focus": "Suggest timeline",
                        "expected_keywords": ["how about", "weeks"],
                    },
                    {
                        "coach": "Check if it works for me.",
                        "hint": "Would that work for you?",
                        "sample_answer": "Would that work for you?",
                        "focus": "Check agreement",
                        "expected_keywords": ["would", "work"],
                    },
                ],
                "target_phrases": ["I propose we ...", "How about we ...?", "Would that work for you?"],
            },
            "reading_support": "A good proposal is specific: what to do, timeline, and a question to confirm agreement.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. I propose we ...",
                "2. How about we ... for ... weeks?",
                "3. Then we can review ...",
                "4. Would that work for you?",
                "5. Not necessarily, because ...",
                "6. We can ... in parallel.",
            ],
            "goal_examples": ["I propose we ...", "How about we ...?", "Would that work for you?"],
        },
        {
            "lesson_key": "lesson-03-handling-objections",
            "slug": "handling-objections",
            "title": "Handling Objections",
            "conversation_situation": "handling_objections",
            "conversation_goal": "Respond to an objection politely, ask a clarifying question, and offer a revised proposal.",
            "grammar_summary": "Use I understand the concern / What if we... / Would it help if... to handle objections calmly.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Lawan bicara keberatan. Kamu respon sopan, tanya klarifikasi, lalu revisi proposal biar lebih bisa diterima.",
            "dialogue": [
                ("Jordan", "I'm concerned this plan will slow us down."),
                ("Mina", "I understand the concern. What part feels risky to you?"),
                ("Jordan", "The extra review steps."),
                ("Mina", "Would it help if we limit reviews to high-risk changes only?"),
                ("Jordan", "Maybe, but who decides what's high-risk?"),
                ("Mina", "Good question. What if we define simple criteria and review them together?"),
                ("Jordan", "That sounds reasonable."),
                ("Mina", "Great. Let's draft criteria today."),
            ],
            "translations": [
                ("Jordan", "I'm concerned this plan will slow us down.", "Aku khawatir plan ini bakal bikin kita lambat."),
                ("Mina", "I understand the concern. What part feels risky to you?", "Aku paham kekhawatirannya. Bagian mana yang terasa berisiko buat kamu?"),
                ("Jordan", "The extra review steps.", "Step review tambahannya."),
                ("Mina", "Would it help if we limit reviews to high-risk changes only?", "Gimana kalau review-nya dibatasi cuma untuk perubahan berisiko tinggi?"),
                ("Jordan", "Maybe, but who decides what's high-risk?", "Mungkin, tapi siapa yang nentuin mana yang high-risk?"),
                ("Mina", "Good question. What if we define simple criteria and review them together?", "Pertanyaan bagus. Gimana kalau kita bikin kriteria sederhana dan review bareng?"),
                ("Jordan", "That sounds reasonable.", "Kedengarannya masuk akal."),
                ("Mina", "Great. Let's draft criteria today.", "Oke. Yuk bikin draft kriterianya hari ini."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I understand the concern.",
                    "meaning_id": "Aku paham kekhawatirannya.",
                    "usage_note": "Start calmly and show empathy.",
                    "common_mistake": 'Do not argue immediately; acknowledge first.',
                },
                {
                    "phrase": "What part feels risky to you?",
                    "meaning_id": "Bagian mana yang terasa berisiko buat kamu?",
                    "usage_note": "Ask a clarifying question.",
                    "common_mistake": 'Do not ask "Why are you worried?" too directly; ask what part feels risky.',
                },
                {
                    "phrase": "Would it help if we limit reviews to high-risk changes only?",
                    "meaning_id": "Gimana kalau review dibatasi cuma untuk perubahan high-risk?",
                    "usage_note": "Offer a revised proposal.",
                    "common_mistake": 'Do not say "Would it help if limit"; include we.',
                },
                {
                    "phrase": "What if we define simple criteria?",
                    "meaning_id": "Gimana kalau kita bikin kriteria sederhana?",
                    "usage_note": "A friendly revision option.",
                    "common_mistake": 'Do not say "What if define"; include we.',
                },
                {
                    "phrase": "That sounds reasonable.",
                    "meaning_id": "Kedengarannya masuk akal.",
                    "usage_note": "A polite acceptance.",
                    "common_mistake": 'Do not say "That sound"; add -s.',
                },
            ],
            "grammar_md": [
                ("I understand the concern", ["I understand the concern.", "I understand the concern about the timeline."]),
                ("Would it help if... / What if we...", ["Would it help if we limit reviews?", "What if we define simple criteria?"]),
            ],
            "pronunciation": [
                ("concern", "kun-SURN."),
                ("criteria", "kry-TEER-ee-uh."),
                ("reasonable", "REE-zuh-nuh-bul."),
            ],
            "response_prompts": [
                {
                    "prompt": "Acknowledge the objection.",
                    "target_response": "I understand the concern.",
                    "acceptable_variations": ["I understand the concern.", "I understand your concern."],
                },
                {
                    "prompt": "Ask a clarifying question.",
                    "target_response": "What part feels risky to you?",
                    "acceptable_variations": ["What part feels risky to you?", "Which part worries you the most?"],
                },
                {
                    "prompt": "Offer a revised proposal.",
                    "target_response": "Would it help if we limit reviews to high-risk changes only?",
                    "acceptable_variations": [
                        "Would it help if we limit reviews to high-risk changes only?",
                        "What if we start with a small pilot?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "empathy_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase shows empathy in a negotiation?",
                    "options": ["I understand the concern.", "You're wrong.", "No."],
                    "correct_answer": "I understand the concern.",
                },
                {
                    "key": "what_if_we",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["What if we define simple criteria?", "What if define criteria?", "What if we defined criteria? (not a suggestion)"],
                    "correct_answer": "What if we define simple criteria?",
                },
                {
                    "key": "would_it_help_if",
                    "type": "multiple_choice",
                    "prompt": "Which phrase offers a soft revision?",
                    "options": ["Would it help if we ...?", "Do it now.", "Stop complaining."],
                    "correct_answer": "Would it help if we ...?",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_negotiation_objections",
                "opening_line": "I have a concern about your proposal.",
                "learner_goal": "Handle an objection: acknowledge, clarify, and revise the proposal.",
                "turns": [
                    {
                        "coach": "I'm concerned this plan will slow us down.",
                        "hint": "Mulai dengan I understand the concern.",
                        "sample_answer": "I understand the concern.",
                        "focus": "Acknowledge",
                        "expected_keywords": ["understand", "concern"],
                    },
                    {
                        "coach": "Ask me what part feels risky.",
                        "hint": "Gunakan What part feels risky to you?",
                        "sample_answer": "What part feels risky to you?",
                        "focus": "Clarify",
                        "expected_keywords": ["risky"],
                    },
                    {
                        "coach": "Offer a revised proposal.",
                        "hint": "Would it help if... / What if we...",
                        "sample_answer": "Would it help if we limit reviews to high-risk changes only? What if we define simple criteria together?",
                        "focus": "Revise proposal",
                        "expected_keywords": ["would it help", "what if"],
                    },
                ],
                "target_phrases": ["I understand the concern.", "What part feels risky to you?", "Would it help if ...?"],
            },
            "reading_support": "Handling objections well means: acknowledge the concern, ask a clarifying question, and adjust the proposal to reduce risk.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. I understand the concern.",
                "2. What part feels risky to you?",
                "3. Would it help if we ...?",
                "4. What if we ...?",
                "5. That sounds reasonable.",
                "6. Let's ... today.",
            ],
            "goal_examples": ["I understand the concern.", "Would it help if we ...?", "What if we ...?"],
        },
        {
            "lesson_key": "lesson-04-finding-middle-ground",
            "slug": "finding-middle-ground",
            "title": "Finding Middle Ground",
            "conversation_situation": "finding_middle_ground",
            "conversation_goal": "Find a compromise, propose a middle-ground option, and confirm agreement.",
            "grammar_summary": "Use Maybe we can... / A compromise could be... / If we do X, can we agree on Y? to find middle ground.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kalian beda pendapat. Kamu usul opsi tengah, jelasin trade-off singkat, lalu konfirmasi kesepakatan.",
            "dialogue": [
                ("Alex", "I want to launch next week, but you want more testing."),
                ("Mina", "Maybe we can find a compromise."),
                ("Alex", "Like what?"),
                ("Mina", "A compromise could be launching to 10% of users first."),
                ("Alex", "That could work. What about testing?"),
                ("Mina", "If we do a small rollout, can we agree on one extra day for testing?"),
                ("Alex", "Yes, that feels fair."),
                ("Mina", "Great. I'll update the rollout plan."),
            ],
            "translations": [
                ("Alex", "I want to launch next week, but you want more testing.", "Aku mau launch minggu depan, tapi kamu mau testing lebih banyak."),
                ("Mina", "Maybe we can find a compromise.", "Mungkin kita bisa cari kompromi."),
                ("Alex", "Like what?", "Kayak apa?"),
                ("Mina", "A compromise could be launching to 10% of users first.", "Komprominya bisa launch dulu ke 10% user."),
                ("Alex", "That could work. What about testing?", "Itu bisa. Kalau testing gimana?"),
                ("Mina", "If we do a small rollout, can we agree on one extra day for testing?", "Kalau kita rollout kecil, bisa sepakat tambah satu hari buat testing?"),
                ("Alex", "Yes, that feels fair.", "Iya, itu adil."),
                ("Mina", "Great. I'll update the rollout plan.", "Oke. Aku update rollout plan-nya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Maybe we can find a compromise.",
                    "meaning_id": "Mungkin kita bisa cari kompromi.",
                    "usage_note": "A neutral way to move toward agreement.",
                    "common_mistake": 'Do not sound like an ultimatum; use maybe we can.',
                },
                {
                    "phrase": "A compromise could be launching to 10% of users first.",
                    "meaning_id": "Komprominya bisa launch dulu ke 10% user.",
                    "usage_note": "A clear middle-ground proposal.",
                    "common_mistake": 'Do not say "compromise can be"; use could be.',
                },
                {
                    "phrase": "If we do a small rollout, can we agree on one extra day?",
                    "meaning_id": "Kalau kita rollout kecil, bisa sepakat tambah satu hari?",
                    "usage_note": "A conditional agreement question.",
                    "common_mistake": 'Do not say "can we agree one extra day" without on.',
                },
                {
                    "phrase": "That feels fair.",
                    "meaning_id": "Itu terasa adil.",
                    "usage_note": "A professional acceptance.",
                    "common_mistake": 'Do not say "That feel fair"; add -s.',
                },
                {
                    "phrase": "I'll update the rollout plan.",
                    "meaning_id": "Aku update rollout plan.",
                    "usage_note": "A clear next step.",
                    "common_mistake": 'Do not say "I will updating"; use I\'ll update.',
                },
            ],
            "grammar_md": [
                ("Maybe we can...", ["Maybe we can find a compromise.", "Maybe we can try a smaller scope."]),
                ("A compromise could be...", ["A compromise could be a pilot.", "A compromise could be a phased rollout."]),
            ],
            "pronunciation": [
                ("compromise", "KOM-pruh-mize."),
                ("rollout", "ROHL-out."),
                ("percentage", "per-SEN-tij."),
            ],
            "response_prompts": [
                {
                    "prompt": "Suggest finding a compromise.",
                    "target_response": "Maybe we can find a compromise.",
                    "acceptable_variations": ["Maybe we can find a compromise.", "Maybe we can meet in the middle."],
                },
                {
                    "prompt": "Propose a compromise.",
                    "target_response": "A compromise could be a small rollout first.",
                    "acceptable_variations": ["A compromise could be a small rollout first.", "A compromise could be a two-week pilot."],
                },
                {
                    "prompt": "Confirm agreement with a condition.",
                    "target_response": "If we do a small rollout, can we agree on one extra day for testing?",
                    "acceptable_variations": [
                        "If we do a small rollout, can we agree on one extra day for testing?",
                        "If we reduce scope, can we agree to launch next week?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "maybe_we_can",
                    "type": "multiple_choice",
                    "prompt": "Which phrase sounds neutral and collaborative?",
                    "options": ["Maybe we can find a compromise.", "You must accept.", "No discussion."],
                    "correct_answer": "Maybe we can find a compromise.",
                },
                {
                    "key": "compromise_could_be",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["A compromise could be a small rollout.", "A compromise could to be a rollout.", "A compromise be rollout."],
                    "correct_answer": "A compromise could be a small rollout.",
                },
                {
                    "key": "fair_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "That feels fair" mean?',
                    "options": ["itu terasa adil", "itu terasa mahal", "itu terasa sulit"],
                    "correct_answer": "itu terasa adil",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_negotiation_middle_ground",
                "opening_line": "We disagree. Can we find a compromise?",
                "learner_goal": "Propose a compromise and confirm agreement.",
                "turns": [
                    {
                        "coach": "We disagree. How can we move forward?",
                        "hint": "Mulai dengan Maybe we can find a compromise.",
                        "sample_answer": "Maybe we can find a compromise.",
                        "focus": "Suggest compromise",
                        "expected_keywords": ["compromise"],
                    },
                    {
                        "coach": "Propose a middle-ground option.",
                        "hint": "A compromise could be...",
                        "sample_answer": "A compromise could be launching to 10% of users first.",
                        "focus": "Propose middle ground",
                        "expected_keywords": ["could be", "users"],
                    },
                    {
                        "coach": "Ask for agreement with a condition.",
                        "hint": "If we do X, can we agree on Y?",
                        "sample_answer": "If we do a small rollout, can we agree on one extra day for testing?",
                        "focus": "Confirm agreement",
                        "expected_keywords": ["if", "agree"],
                    },
                ],
                "target_phrases": ["Maybe we can...", "A compromise could be...", "Can we agree on ...?"],
            },
            "reading_support": "Finding middle ground means offering a compromise that respects both priorities. Propose a practical option and confirm agreement clearly.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. Maybe we can find a compromise.",
                "2. A compromise could be ...",
                "3. The trade-off is ...",
                "4. If we do X, can we agree on Y?",
                "5. That feels fair.",
                "6. I'll update the plan.",
            ],
            "goal_examples": ["Maybe we can ...", "A compromise could be ...", "Can we agree on ...?"],
        },
        {
            "lesson_key": "lesson-05-negotiation-mission",
            "slug": "negotiation-mission",
            "title": "Negotiation Mission",
            "conversation_situation": "mission_negotiation_compromise",
            "conversation_goal": "Complete a negotiation: align priorities, make a proposal, handle objections, find middle ground, and agree on next steps.",
            "grammar_summary": "Combine: My top priority is... / I propose we... / I understand the concern... / Would it help if... / A compromise could be...",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Misi: kamu negosiasi rencana launch. Kamu align prioritas, usul proposal, handle keberatan, cari kompromi, lalu sepakat next step.",
            "dialogue": [
                ("Alex", "We need to decide our launch plan."),
                ("Mina", "My top priority is quality. What matters most to you?"),
                ("Alex", "My top priority is speed."),
                ("Mina", "I understand. I propose we run a small pilot for two weeks."),
                ("Alex", "I'm concerned it will delay the launch."),
                ("Mina", "I understand the concern. Would it help if we prepare in parallel?"),
                ("Alex", "Maybe. What's the compromise?"),
                ("Mina", "A compromise could be launching to 10% first, then expanding if results look good."),
            ],
            "translations": [
                ("Alex", "We need to decide our launch plan.", "Kita perlu putusin launch plan."),
                ("Mina", "My top priority is quality. What matters most to you?", "Prioritas utamaku kualitas. Yang paling penting buat kamu apa?"),
                ("Alex", "My top priority is speed.", "Prioritas utamaku kecepatan."),
                ("Mina", "I understand. I propose we run a small pilot for two weeks.", "Aku paham. Aku usul kita jalanin pilot kecil dua minggu."),
                ("Alex", "I'm concerned it will delay the launch.", "Aku khawatir itu bakal nunda launch."),
                ("Mina", "I understand the concern. Would it help if we prepare in parallel?", "Aku paham kekhawatirannya. Gimana kalau kita siapin paralel?"),
                ("Alex", "Maybe. What's the compromise?", "Mungkin. Komprominya apa?"),
                ("Mina", "A compromise could be launching to 10% first, then expanding if results look good.", "Komprominya bisa launch dulu ke 10%, lalu diperluas kalau hasilnya bagus."),
            ],
            "useful_phrases": [
                {
                    "phrase": "My top priority is quality. What matters most to you?",
                    "meaning_id": "Prioritas utamaku kualitas. Yang paling penting buat kamu apa?",
                    "usage_note": "Align priorities first.",
                    "common_mistake": "Don't assume priorities; ask directly.",
                },
                {
                    "phrase": "I propose we run a small pilot for two weeks.",
                    "meaning_id": "Aku usul kita jalanin pilot kecil dua minggu.",
                    "usage_note": "Proposal + timeline.",
                    "common_mistake": 'Do not say "I propose to run"; use I propose we run.',
                },
                {
                    "phrase": "I understand the concern. Would it help if we prepare in parallel?",
                    "meaning_id": "Aku paham kekhawatirannya. Gimana kalau kita siapin paralel?",
                    "usage_note": "Handle objection with empathy + mitigation.",
                    "common_mistake": "Don't dismiss concerns; acknowledge first.",
                },
                {
                    "phrase": "A compromise could be launching to 10% first.",
                    "meaning_id": "Komprominya bisa launch dulu ke 10%.",
                    "usage_note": "Middle-ground option.",
                    "common_mistake": "Offer a concrete compromise, not a vague promise.",
                },
                {
                    "phrase": "Then expanding if results look good.",
                    "meaning_id": "Lalu diperluas kalau hasilnya bagus.",
                    "usage_note": "Conditional next step.",
                    "common_mistake": 'Do not say "if results looks"; use look.',
                },
            ],
            "grammar_md": [
                (
                    "Negotiation structure",
                    [
                        "My top priority is ...",
                        "I propose we ...",
                        "I understand the concern. Would it help if ...?",
                        "A compromise could be ...",
                    ],
                ),
            ],
            "pronunciation": [
                ("trade-off", "TRAYD-off."),
                ("expand", "ik-SPAND."),
                ("results", "ri-ZULTS."),
            ],
            "response_prompts": [
                {
                    "prompt": "Align priorities.",
                    "target_response": "My top priority is quality. What matters most to you?",
                    "acceptable_variations": [
                        "My top priority is quality. What matters most to you?",
                        "My top priority is speed. What matters most to you?",
                    ],
                },
                {
                    "prompt": "Make a proposal with timeline.",
                    "target_response": "I propose we run a small pilot for two weeks.",
                    "acceptable_variations": ["I propose we run a small pilot for two weeks.", "I propose we start with a small rollout."],
                },
                {
                    "prompt": "Offer compromise.",
                    "target_response": "A compromise could be launching to 10% first, then expanding if results look good.",
                    "acceptable_variations": [
                        "A compromise could be launching to 10% first, then expanding if results look good.",
                        "A compromise could be a one-week pilot, then a full launch.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "negotiation_flow",
                    "type": "multiple_choice",
                    "prompt": "Which flow fits a negotiation?",
                    "options": [
                        "Priorities -> proposal -> objection -> compromise",
                        "Greeting -> goodbye",
                        "Weather -> food",
                    ],
                    "correct_answer": "Priorities -> proposal -> objection -> compromise",
                },
                {
                    "key": "prepare_in_parallel",
                    "type": "multiple_choice",
                    "prompt": 'What does "in parallel" mean?',
                    "options": ["secara paralel/bersamaan", "sendirian", "setelah selesai"],
                    "correct_answer": "secara paralel/bersamaan",
                },
                {
                    "key": "results_look_good",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["If results look good, we can expand.", "If results looks good, we can expand.", "If results looking good, expand."],
                    "correct_answer": "If results look good, we can expand.",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_negotiation_mission",
                "opening_line": "We need to decide a launch plan. Let's negotiate.",
                "learner_goal": "Negotiate: align priorities, propose a plan, handle an objection, and suggest a compromise.",
                "turns": [
                    {
                        "coach": "What's your top priority?",
                        "hint": "My top priority is ... + ask mine.",
                        "sample_answer": "My top priority is quality. What matters most to you?",
                        "focus": "Priorities",
                        "expected_keywords": ["top priority", "matters most"],
                    },
                    {
                        "coach": "Make a proposal with a timeline.",
                        "hint": "I propose we ... for ... weeks.",
                        "sample_answer": "I propose we run a small pilot for two weeks.",
                        "focus": "Proposal",
                        "expected_keywords": ["propose", "weeks"],
                    },
                    {
                        "coach": "I’m concerned it will delay the launch. Respond and offer a compromise.",
                        "hint": "I understand the concern. Would it help if... A compromise could be...",
                        "sample_answer": "I understand the concern. Would it help if we prepare in parallel? A compromise could be launching to 10% first, then expanding if results look good.",
                        "focus": "Objection + compromise",
                        "expected_keywords": ["understand", "help", "compromise"],
                    },
                ],
                "target_phrases": ["My top priority is ...", "I propose we ...", "A compromise could be ..."],
            },
            "reading_support": "Negotiation is collaborative. Start with priorities, propose a plan, address concerns, and suggest a concrete compromise with next steps.",
            "writing_support_lines": [
                "Write your mission (8 lines):",
                "1. My top priority is ...",
                "2. What matters most to you?",
                "3. I propose we ...",
                "4. How about we ...?",
                "5. I understand the concern.",
                "6. Would it help if ...?",
                "7. A compromise could be ...",
                "8. If results look good, we can ...",
            ],
            "goal_examples": ["My top priority is ...", "I propose we ...", "A compromise could be ..."],
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

