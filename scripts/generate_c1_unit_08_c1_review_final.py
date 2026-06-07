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
            "- Speed: natural, confident, slightly fast",
            "- Tone: professional, thoughtful, collaborative",
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

        Read it again and underline the review signposting (to be precise, on balance, in other words, given that, next steps).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "C1"
    root = Path("content/curriculum/english/C1")
    units_root = root / "units"
    unit_key = "unit-08-c1-review-final"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-08-c1-review-final
            level_code: C1
            title: C1 Review & Final Conversation
            main_conversation_outcome: Use C1 skills in complex professional and social conversations.
            status: in_production
            lessons:
              - lesson-01-review-nuance-and-strategy
              - lesson-02-review-presenting-and-debate
              - lesson-03-review-leadership-and-listening
              - lesson-04-c1-final-test-practice
              - lesson-05-c1-final-conversation
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
            "lesson_key": "lesson-01-review-nuance-and-strategy",
            "slug": "review-nuance-and-strategy",
            "title": "Review Nuance and Strategy",
            "conversation_situation": "review_nuance_and_strategy",
            "conversation_goal": "Express a nuanced position, manage expectations, and align stakeholders on a careful plan.",
            "grammar_summary": "Use On balance... / To be precise... / What I can commit to is... / The key trade-off is... / Next steps are... to sound strategic.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Review: kamu perlu menyampaikan opini yang bernuansa, ngatur ekspektasi, dan align stakeholder tanpa overpromise.",
            "dialogue": [
                ("Jordan", "So do you support the plan or not?"),
                ("Mina", "On balance, I support it, but I'd adjust the scope to reduce risk."),
                ("Jordan", "What exactly would you change?"),
                ("Mina", "To be precise, I'd keep the core workflow and postpone optional add-ons."),
                ("Jordan", "Can you commit to next week?"),
                ("Mina", "What I can commit to is a pilot next week, and a full rollout after we validate the metrics."),
                ("Jordan", "How do we align everyone?"),
                ("Mina", "Next steps are: I'll share a one-page summary today, and we'll align in a 30-minute call tomorrow."),
            ],
            "translations": [
                ("Jordan", "So do you support the plan or not?", "Jadi kamu dukung plan ini atau nggak?"),
                ("Mina", "On balance, I support it, but I'd adjust the scope to reduce risk.", "Secara keseluruhan aku dukung, tapi scope-nya perlu disesuaikan biar risikonya turun."),
                ("Jordan", "What exactly would you change?", "Tepatnya apa yang kamu ubah?"),
                ("Mina", "To be precise, I'd keep the core workflow and postpone optional add-ons.", "Biar spesifik, aku pertahankan workflow inti dan tunda add-on opsional."),
                ("Jordan", "Can you commit to next week?", "Bisa commit minggu depan?"),
                ("Mina", "What I can commit to is a pilot next week, and a full rollout after we validate the metrics.", "Yang bisa aku commit: pilot minggu depan, dan rollout penuh setelah metriknya tervalidasi."),
                ("Jordan", "How do we align everyone?", "Gimana cara align semua orang?"),
                ("Mina", "Next steps are: I'll share a one-page summary today, and we'll align in a 30-minute call tomorrow.", "Next steps-nya: aku share ringkasan satu halaman hari ini, lalu kita align lewat call 30 menit besok."),
            ],
            "useful_phrases": [
                {
                    "phrase": "On balance, I support it, but I'd adjust the scope to reduce risk.",
                    "meaning_id": "Secara keseluruhan aku dukung, tapi scope-nya perlu disesuaikan biar risikonya turun.",
                    "usage_note": "A nuanced position statement that includes a condition.",
                    "common_mistake": "Do not sound absolute; keep it balanced and specific.",
                },
                {
                    "phrase": "To be precise, I'd keep the core workflow and postpone optional add-ons.",
                    "meaning_id": "Biar spesifik, aku pertahankan workflow inti dan tunda add-on opsional.",
                    "usage_note": "Precision language for scope decisions.",
                    "common_mistake": "Do not stay vague; specify what stays and what moves.",
                },
                {
                    "phrase": "What I can commit to is a pilot next week.",
                    "meaning_id": "Yang bisa aku commit: pilot minggu depan.",
                    "usage_note": "Expectation management without overpromising.",
                    "common_mistake": "Do not promise a full delivery if it is uncertain.",
                },
                {
                    "phrase": "Next steps are: I'll share a one-page summary today, and we'll align tomorrow.",
                    "meaning_id": "Next steps-nya: aku share ringkasan satu halaman hari ini, lalu kita align besok.",
                    "usage_note": "Clear next steps with time anchors.",
                    "common_mistake": "Do not skip ownership; say who does what by when.",
                },
                {
                    "phrase": "The key trade-off is speed versus confidence in the metrics.",
                    "meaning_id": "Trade-off utamanya: cepat versus yakin dengan metrik.",
                    "usage_note": "Name trade-offs explicitly and calmly.",
                    "common_mistake": "Do not list too many trade-offs; start with the key one.",
                },
            ],
            "grammar_md": [
                (
                    "Nuance + precision",
                    [
                        "On balance, I support it, but ...",
                        "To be precise, ...",
                    ],
                ),
                (
                    "Strategic commitments",
                    [
                        "What I can commit to is ...",
                        "Next steps are: I'll ..., and we'll ...",
                    ],
                ),
            ],
            "pronunciation": [
                ("on balance", "on BAL-uhns."),
                ("precise", "pri-SICE."),
                ("commit", "kuh-MIT."),
            ],
            "response_prompts": [
                {
                    "prompt": "Give a nuanced position with a condition.",
                    "target_response": "On balance, I support it, but I'd adjust the scope to reduce risk.",
                    "acceptable_variations": [
                        "On balance, I support it, but I'd adjust the scope to reduce risk.",
                        "On balance, I agree, but I'd keep the scope smaller to reduce risk.",
                    ],
                },
                {
                    "prompt": "Manage expectations with a clear commitment.",
                    "target_response": "What I can commit to is a pilot next week, and a full rollout after we validate the metrics.",
                    "acceptable_variations": [
                        "What I can commit to is a pilot next week, and a full rollout after we validate the metrics.",
                        "What I can commit to is a pilot next week, then we decide after reviewing the data.",
                    ],
                },
                {
                    "prompt": "Close with next steps and timing.",
                    "target_response": "Next steps are: I'll share a one-page summary today, and we'll align in a 30-minute call tomorrow.",
                    "acceptable_variations": [
                        "Next steps are: I'll share a one-page summary today, and we'll align in a 30-minute call tomorrow.",
                        "Next steps are: I'll send a summary today, and we'll align tomorrow morning.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "on_balance_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "on balance" mean?',
                    "options": ["secara keseluruhan", "tanpa bukti", "terlalu cepat"],
                    "correct_answer": "secara keseluruhan",
                },
                {
                    "key": "commit_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase manages expectations without overpromising?",
                    "options": ["What I can commit to is ...", "I guarantee ...", "No risk."],
                    "correct_answer": "What I can commit to is ...",
                },
                {
                    "key": "precision_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase signals precision?",
                    "options": ["To be precise, ...", "Maybe ...", "Whatever."],
                    "correct_answer": "To be precise, ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_review_nuance_strategy",
                "opening_line": "Do you support the plan or not?",
                "learner_goal": "Give a nuanced position, manage expectations, and align on next steps.",
                "turns": [
                    {
                        "coach": "Give a nuanced position with a condition.",
                        "hint": "On balance... but I'd...",
                        "sample_answer": "On balance, I support it, but I'd adjust the scope to reduce risk.",
                        "focus": "Nuance",
                        "expected_keywords": ["on balance", "scope", "risk"],
                    },
                    {
                        "coach": "Be precise about what changes.",
                        "hint": "To be precise...",
                        "sample_answer": "To be precise, I'd keep the core workflow and postpone optional add-ons.",
                        "focus": "Precision",
                        "expected_keywords": ["to be precise", "core", "postpone"],
                    },
                    {
                        "coach": "Manage expectations and close with next steps.",
                        "hint": "What I can commit to is... Next steps are...",
                        "sample_answer": "What I can commit to is a pilot next week. Next steps are: I'll share a one-page summary today, and we'll align tomorrow.",
                        "focus": "Commitment + next steps",
                        "expected_keywords": ["commit", "next steps", "today"],
                    },
                ],
                "target_phrases": [
                    "On balance, ...",
                    "To be precise, ...",
                    "What I can commit to is ...",
                    "Next steps are ...",
                ],
            },
            "reading_support": "C1 conversations often require nuance. State your position, qualify it with conditions, be precise about scope, and manage expectations by committing to what is realistic and verifiable.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. On balance, I ...",
                "2. However, ...",
                "3. To be precise, ...",
                "4. The key trade-off is ...",
                "5. What I can commit to is ...",
                "6. What I can't commit to is ...",
                "7. Given that, ...",
                "8. Next steps are: ...",
                "9. I'll ... today.",
                "10. We'll align ... tomorrow.",
            ],
            "goal_examples": [
                "On balance, ...",
                "To be precise, ...",
                "What I can commit to is ...",
            ],
        },
        {
            "lesson_key": "lesson-02-review-presenting-and-debate",
            "slug": "review-presenting-and-debate",
            "title": "Review Presenting and Debate",
            "conversation_situation": "review_presenting_and_debate",
            "conversation_goal": "Present a structured argument, challenge assumptions respectfully, and respond under pressure with clarity.",
            "grammar_summary": "Use Let me frame this... / The core assumption is... / If we accept that, then... / On the other hand... / In short... to debate clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Review: kamu present argumen singkat, lalu kamu ditantang. Kamu harus jawab dengan struktur dan tetap sopan.",
            "dialogue": [
                ("Alex", "Give me the short version of your argument."),
                ("Mina", "Let me frame this: the goal is reliability, not just speed."),
                ("Alex", "You're assuming reliability is the main driver."),
                ("Mina", "That's fair. The core assumption is that incidents cost more than delay."),
                ("Alex", "What if leadership rejects that?"),
                ("Mina", "If we accept speed as the priority, then we should time-box a pilot and limit scope."),
                ("Alex", "Any counterpoint?"),
                ("Mina", "On the other hand, we can keep one feature in scope if the metrics stay stable."),
                ("Alex", "Summarize."),
                ("Mina", "In short: protect reliability, validate with metrics, then expand safely."),
            ],
            "translations": [
                ("Alex", "Give me the short version of your argument.", "Kasih versi singkat argumen kamu."),
                ("Mina", "Let me frame this: the goal is reliability, not just speed.", "Biar aku frame: targetnya reliability, bukan cuma cepat."),
                ("Alex", "You're assuming reliability is the main driver.", "Kamu mengasumsikan reliability itu driver utama."),
                ("Mina", "That's fair. The core assumption is that incidents cost more than delay.", "Masuk akal. Asumsi intinya: incident biayanya lebih mahal daripada delay."),
                ("Alex", "What if leadership rejects that?", "Kalau leadership nolak asumsi itu?"),
                ("Mina", "If we accept speed as the priority, then we should time-box a pilot and limit scope.", "Kalau prioritasnya speed, maka kita time-box pilot dan batasi scope."),
                ("Alex", "Any counterpoint?", "Ada counterpoint?"),
                ("Mina", "On the other hand, we can keep one feature in scope if the metrics stay stable.", "Di sisi lain, kita bisa tetap masukin satu fitur kalau metriknya stabil."),
                ("Alex", "Summarize.", "Rangkum."),
                ("Mina", "In short: protect reliability, validate with metrics, then expand safely.", "Singkatnya: lindungi reliability, validasi pakai metrik, lalu ekspansi dengan aman."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let me frame this: the goal is reliability, not just speed.",
                    "meaning_id": "Biar aku frame: targetnya reliability, bukan cuma cepat.",
                    "usage_note": "A strong, structured opening for presentations.",
                    "common_mistake": "Do not start with details; frame the goal first.",
                },
                {
                    "phrase": "The core assumption is that incidents cost more than delay.",
                    "meaning_id": "Asumsi intinya: incident biayanya lebih mahal daripada delay.",
                    "usage_note": "Surface assumptions explicitly to debate honestly.",
                    "common_mistake": "Do not hide assumptions; name them clearly.",
                },
                {
                    "phrase": "If we accept speed as the priority, then we should time-box a pilot and limit scope.",
                    "meaning_id": "Kalau prioritasnya speed, maka kita time-box pilot dan batasi scope.",
                    "usage_note": "Conditional reasoning under pressure.",
                    "common_mistake": "Do not argue emotionally; use if/then logic.",
                },
                {
                    "phrase": "On the other hand, we can keep one feature in scope if the metrics stay stable.",
                    "meaning_id": "Di sisi lain, kita bisa tetap masukin satu fitur kalau metriknya stabil.",
                    "usage_note": "Balanced counterpoint language.",
                    "common_mistake": "Do not dismiss the other view; acknowledge it.",
                },
                {
                    "phrase": "In short: protect reliability, validate with metrics, then expand safely.",
                    "meaning_id": "Singkatnya: lindungi reliability, validasi pakai metrik, lalu ekspansi dengan aman.",
                    "usage_note": "A crisp closing summary.",
                    "common_mistake": "Do not introduce new points in the summary.",
                },
            ],
            "grammar_md": [
                (
                    "Framing + assumptions",
                    [
                        "Let me frame this: ...",
                        "The core assumption is that ...",
                    ],
                ),
                (
                    "Conditional reasoning",
                    [
                        "If we accept X, then we should Y.",
                        "On the other hand, ...",
                        "In short: ...",
                    ],
                ),
            ],
            "pronunciation": [
                ("assumption", "uh-SUMP-shun."),
                ("time-box", "TIME-boks."),
                ("validate", "VAL-ih-date."),
            ],
            "response_prompts": [
                {
                    "prompt": "Frame your argument in one sentence.",
                    "target_response": "Let me frame this: the goal is reliability, not just speed.",
                    "acceptable_variations": [
                        "Let me frame this: the goal is reliability, not just speed.",
                        "Let me frame this: the goal is long-term stability, not just quick wins.",
                    ],
                },
                {
                    "prompt": "Respond with conditional reasoning.",
                    "target_response": "If we accept speed as the priority, then we should time-box a pilot and limit scope.",
                    "acceptable_variations": [
                        "If we accept speed as the priority, then we should time-box a pilot and limit scope.",
                        "If speed is the priority, then we should reduce scope and validate quickly.",
                    ],
                },
                {
                    "prompt": "Close with a short summary.",
                    "target_response": "In short: protect reliability, validate with metrics, then expand safely.",
                    "acceptable_variations": [
                        "In short: protect reliability, validate with metrics, then expand safely.",
                        "In short: validate first, then scale.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "frame_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase frames a presentation clearly?",
                    "options": ["Let me frame this: ...", "No frame.", "Stop."],
                    "correct_answer": "Let me frame this: ...",
                },
                {
                    "key": "conditional_logic",
                    "type": "multiple_choice",
                    "prompt": "Which phrase shows conditional reasoning?",
                    "options": ["If we accept X, then we should Y.", "X is bad.", "Whatever."],
                    "correct_answer": "If we accept X, then we should Y.",
                },
                {
                    "key": "in_short",
                    "type": "multiple_choice",
                    "prompt": 'What does "in short" mean?',
                    "options": ["singkatnya", "berlawanan", "berat"],
                    "correct_answer": "singkatnya",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_review_presenting_debate",
                "opening_line": "Give me the short version of your argument.",
                "learner_goal": "Present a structured argument and respond to challenges calmly.",
                "turns": [
                    {
                        "coach": "Frame your argument in one sentence.",
                        "hint": "Let me frame this...",
                        "sample_answer": "Let me frame this: the goal is reliability, not just speed.",
                        "focus": "Frame",
                        "expected_keywords": ["frame", "goal"],
                    },
                    {
                        "coach": "Name your core assumption.",
                        "hint": "The core assumption is that...",
                        "sample_answer": "The core assumption is that incidents cost more than delay.",
                        "focus": "Assumption",
                        "expected_keywords": ["assumption", "incidents"],
                    },
                    {
                        "coach": "Respond under pressure with if/then logic and summarize.",
                        "hint": "If we accept..., then... In short...",
                        "sample_answer": "If we accept speed as the priority, then we should time-box a pilot and limit scope. In short: validate with metrics, then expand safely.",
                        "focus": "Pressure response",
                        "expected_keywords": ["if", "then", "in short"],
                    },
                ],
                "target_phrases": ["Let me frame this: ...", "The core assumption is ...", "If we accept X, then ...", "In short: ..."],
            },
            "reading_support": "In debate-style conversations, clarity beats volume. Frame the goal, surface assumptions, use conditional reasoning, acknowledge counterpoints, and close with a short summary.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. Let me frame this: ...",
                "2. The goal is ...",
                "3. The core assumption is ...",
                "4. If we accept X, then ...",
                "5. On the other hand, ...",
                "6. The key risk is ...",
                "7. We can mitigate it by ...",
                "8. Therefore, ...",
                "9. In short: ...",
                "10. Does that sound reasonable?",
            ],
            "goal_examples": ["Let me frame this: ...", "The core assumption is ...", "In short: ..."],
        },
        {
            "lesson_key": "lesson-03-review-leadership-and-listening",
            "slug": "review-leadership-and-listening",
            "title": "Review Leadership and Listening",
            "conversation_situation": "review_leadership_and_listening",
            "conversation_goal": "Coach someone with questions, catch implied meaning, and align on a decision with clear next steps.",
            "grammar_summary": "Use What I'm hearing is... / When you say X, do you mean Y or Z? / What would success look like? / What I can commit to is... to lead with listening.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Review: kamu memimpin percakapan coaching. Kamu nangkep maksud tersirat, tanya pertanyaan bagus, dan tutup dengan keputusan + next steps.",
            "dialogue": [
                ("Jordan", "I feel like the team is hesitant, but they won't say it directly."),
                ("Mina", "What I'm hearing is there's some concern under the surface."),
                ("Jordan", "Yeah, maybe they're worried about blame."),
                ("Mina", "When you say 'worried about blame', do you mean fear of mistakes or fear of visibility?"),
                ("Jordan", "Mostly fear of visibility."),
                ("Mina", "What would success look like in the next two weeks?"),
                ("Jordan", "A small pilot with stable metrics."),
                ("Mina", "Great. Next steps are: you'll propose the pilot plan, and I'll help you align stakeholders tomorrow."),
            ],
            "translations": [
                ("Jordan", "I feel like the team is hesitant, but they won't say it directly.", "Aku merasa tim ragu-ragu, tapi mereka nggak ngomong langsung."),
                ("Mina", "What I'm hearing is there's some concern under the surface.", "Yang aku tangkap: ada concern tersirat."),
                ("Jordan", "Yeah, maybe they're worried about blame.", "Iya, mungkin mereka takut disalahin."),
                ("Mina", "When you say 'worried about blame', do you mean fear of mistakes or fear of visibility?", "Kalau bilang 'takut disalahin', maksudnya takut bikin salah atau takut jadi terlihat/ter-spotlight?"),
                ("Jordan", "Mostly fear of visibility.", "Lebih ke takut visibility."),
                ("Mina", "What would success look like in the next two weeks?", "Suksesnya seperti apa dalam dua minggu ke depan?"),
                ("Jordan", "A small pilot with stable metrics.", "Pilot kecil dengan metrik stabil."),
                ("Mina", "Great. Next steps are: you'll propose the pilot plan, and I'll help you align stakeholders tomorrow.", "Oke. Next steps: kamu usulkan plan pilot, dan aku bantu align stakeholder besok."),
            ],
            "useful_phrases": [
                {
                    "phrase": "What I'm hearing is there's some concern under the surface.",
                    "meaning_id": "Yang aku tangkap: ada concern tersirat.",
                    "usage_note": "A listening mirror that invites clarity.",
                    "common_mistake": "Do not assume details; mirror the pattern and ask.",
                },
                {
                    "phrase": "When you say X, do you mean Y or Z?",
                    "meaning_id": "Kalau bilang X, maksudnya Y atau Z?",
                    "usage_note": "Clarify ambiguous concerns with two options.",
                    "common_mistake": "Do not offer too many options; keep it to two.",
                },
                {
                    "phrase": "What would success look like in the next two weeks?",
                    "meaning_id": "Suksesnya seperti apa dalam dua minggu ke depan?",
                    "usage_note": "A coaching question that defines outcomes.",
                    "common_mistake": "Do not ask vague questions; specify timeframe.",
                },
                {
                    "phrase": "Next steps are: you'll propose the pilot plan, and I'll help align stakeholders.",
                    "meaning_id": "Next steps: kamu usulkan plan pilot, dan aku bantu align stakeholder.",
                    "usage_note": "Leadership language with clear ownership.",
                    "common_mistake": "Do not leave next steps unclear; name owners.",
                },
                {
                    "phrase": "What would change your mind?",
                    "meaning_id": "Apa yang bisa mengubah pikiran kamu?",
                    "usage_note": "Find decision criteria and reduce conflict.",
                    "common_mistake": "Do not argue first; ask criteria.",
                },
            ],
            "grammar_md": [
                ("Listening mirrors", ["What I'm hearing is ...", "It sounds like ..."]),
                ("Coaching questions", ["What would success look like ...?", "When you say X, do you mean Y or Z?"]),
                ("Leadership close", ["Next steps are: you'll ..., and I'll ..."]),
            ],
            "pronunciation": [
                ("hesitant", "HEZ-ih-tunt."),
                ("visibility", "viz-uh-BIL-ih-tee."),
                ("stakeholders", "STAKE-hohl-derz."),
            ],
            "response_prompts": [
                {
                    "prompt": "Mirror a concern without assuming details.",
                    "target_response": "What I'm hearing is there's some concern under the surface.",
                    "acceptable_variations": [
                        "What I'm hearing is there's some concern under the surface.",
                        "What I'm hearing is there may be hesitation under the surface.",
                    ],
                },
                {
                    "prompt": "Clarify an ambiguous concern with two options.",
                    "target_response": "When you say 'worried about blame', do you mean fear of mistakes or fear of visibility?",
                    "acceptable_variations": [
                        "When you say 'worried about blame', do you mean fear of mistakes or fear of visibility?",
                        "When you say 'concerned', do you mean scope or timing?",
                    ],
                },
                {
                    "prompt": "Close with next steps and ownership.",
                    "target_response": "Next steps are: you'll propose the pilot plan, and I'll help you align stakeholders tomorrow.",
                    "acceptable_variations": [
                        "Next steps are: you'll propose the pilot plan, and I'll help you align stakeholders tomorrow.",
                        "Next steps are: you'll draft the plan today, and I'll help you align stakeholders tomorrow.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "mirror_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase mirrors what someone said without assuming?",
                    "options": ["What I'm hearing is ...", "You're wrong.", "No concerns."],
                    "correct_answer": "What I'm hearing is ...",
                },
                {
                    "key": "coaching_question",
                    "type": "multiple_choice",
                    "prompt": "Which question defines outcomes clearly?",
                    "options": ["What would success look like in the next two weeks?", "Why are you like that?", "No question."],
                    "correct_answer": "What would success look like in the next two weeks?",
                },
                {
                    "key": "ownership",
                    "type": "multiple_choice",
                    "prompt": "Which phrase clearly assigns ownership?",
                    "options": ["Next steps are: you'll ..., and I'll ...", "Someone will do it.", "Maybe later."],
                    "correct_answer": "Next steps are: you'll ..., and I'll ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_review_leadership_listening",
                "opening_line": "The team seems hesitant, but they won't say it directly.",
                "learner_goal": "Lead with listening and coaching questions, then align on next steps.",
                "turns": [
                    {
                        "coach": "Mirror the concern.",
                        "hint": "What I'm hearing is...",
                        "sample_answer": "What I'm hearing is there's some concern under the surface.",
                        "focus": "Mirror",
                        "expected_keywords": ["hearing", "concern"],
                    },
                    {
                        "coach": "Clarify what the concern means with two options.",
                        "hint": "When you say X, do you mean Y or Z?",
                        "sample_answer": "When you say 'worried about blame', do you mean fear of mistakes or fear of visibility?",
                        "focus": "Clarify",
                        "expected_keywords": ["do you mean", "fear"],
                    },
                    {
                        "coach": "Ask for success criteria and close with next steps.",
                        "hint": "What would success look like...? Next steps are...",
                        "sample_answer": "What would success look like in the next two weeks? Next steps are: you'll propose the pilot plan, and I'll help align stakeholders tomorrow.",
                        "focus": "Criteria + next steps",
                        "expected_keywords": ["success", "next steps", "tomorrow"],
                    },
                ],
                "target_phrases": ["What I'm hearing is ...", "When you say X, do you mean Y or Z?", "Next steps are ..."],
            },
            "reading_support": "Leadership conversations are often listening conversations. Mirror what you hear, clarify ambiguous language, define success criteria, and close with owners and next steps to create alignment.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. What I'm hearing is ...",
                "2. Just to check, ...",
                "3. When you say X, do you mean Y or Z?",
                "4. What's your assumption about ...?",
                "5. What would success look like in the next two weeks?",
                "6. What would change your mind?",
                "7. Given that, ...",
                "8. Next steps are: you'll ..., and I'll ...",
                "9. Let's check in on ...",
                "10. Does that work for you?",
            ],
            "goal_examples": ["What I'm hearing is ...", "What would success look like ...?", "Next steps are ..."],
        },
        {
            "lesson_key": "lesson-04-c1-final-test-practice",
            "slug": "c1-final-test-practice",
            "title": "C1 Final Test Practice",
            "conversation_situation": "c1_final_test_practice",
            "conversation_goal": "Answer C1-style prompts with nuance, structure, and precise language under time pressure.",
            "grammar_summary": "Use Let me frame this... / On balance... / To be precise... / The decision is... / The open questions are... / Next steps are... to stay structured.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Latihan final: kamu jawab prompt C1 dengan cepat tapi tetap bernuansa (frame, asumsi, trade-off, keputusan, next steps).",
            "dialogue": [
                ("Alex", "Final practice. Frame the issue in one line."),
                ("Mina", "Let me frame this: we need reliability and stakeholder confidence before scaling."),
                ("Alex", "Give your nuanced position."),
                ("Mina", "On balance, I support the rollout, but only after we validate pilot metrics."),
                ("Alex", "Be precise about next steps."),
                ("Mina", "Next steps are: I'll send a one-page summary today, and we'll align on scope tomorrow."),
                ("Alex", "State decisions and open questions."),
                ("Mina", "The decision is to run a two-week pilot. The open questions are resourcing and change management."),
            ],
            "translations": [
                ("Alex", "Final practice. Frame the issue in one line.", "Latihan final. Frame isu-nya dalam satu kalimat."),
                ("Mina", "Let me frame this: we need reliability and stakeholder confidence before scaling.", "Biar aku frame: kita butuh reliability dan kepercayaan stakeholder sebelum scale."),
                ("Alex", "Give your nuanced position.", "Kasih posisi bernuansa kamu."),
                ("Mina", "On balance, I support the rollout, but only after we validate pilot metrics.", "Secara keseluruhan aku dukung rollout, tapi hanya setelah metrik pilot tervalidasi."),
                ("Alex", "Be precise about next steps.", "Spesifik soal next steps."),
                ("Mina", "Next steps are: I'll send a one-page summary today, and we'll align on scope tomorrow.", "Next steps: aku kirim ringkasan satu halaman hari ini, lalu kita align scope besok."),
                ("Alex", "State decisions and open questions.", "Sebutkan keputusan dan pertanyaan terbuka."),
                ("Mina", "The decision is to run a two-week pilot. The open questions are resourcing and change management.", "Keputusannya: jalankan pilot dua minggu. Pertanyaan terbukanya: resourcing dan change management."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let me frame this: we need reliability and stakeholder confidence before scaling.",
                    "meaning_id": "Biar aku frame: kita butuh reliability dan kepercayaan stakeholder sebelum scale.",
                    "usage_note": "A strong C1 framing sentence.",
                    "common_mistake": "Do not over-explain; keep the frame to one line.",
                },
                {
                    "phrase": "On balance, I support the rollout, but only after we validate pilot metrics.",
                    "meaning_id": "Secara keseluruhan aku dukung rollout, tapi hanya setelah metrik pilot tervalidasi.",
                    "usage_note": "A nuanced position with a clear condition.",
                    "common_mistake": "Do not remove the condition; it's the nuance.",
                },
                {
                    "phrase": "The decision is to run a two-week pilot.",
                    "meaning_id": "Keputusannya: jalankan pilot dua minggu.",
                    "usage_note": "Decision labeling for clarity.",
                    "common_mistake": "Do not mix decisions and open questions.",
                },
                {
                    "phrase": "The open questions are resourcing and change management.",
                    "meaning_id": "Pertanyaan terbukanya: resourcing dan change management.",
                    "usage_note": "Label open questions explicitly.",
                    "common_mistake": "Do not hide uncertainty; name it.",
                },
                {
                    "phrase": "Next steps are: I'll send a one-page summary today, and we'll align tomorrow.",
                    "meaning_id": "Next steps: aku kirim ringkasan satu halaman hari ini, lalu kita align besok.",
                    "usage_note": "Time-boxed next steps.",
                    "common_mistake": "Do not omit timing; add today/tomorrow/by Friday.",
                },
            ],
            "grammar_md": [
                (
                    "Test-style structure",
                    [
                        "Let me frame this: ...",
                        "On balance, ... but ...",
                        "To be precise, ...",
                        "The decision is ...",
                        "The open questions are ...",
                        "Next steps are ...",
                    ],
                )
            ],
            "pronunciation": [
                ("confidence", "KON-fih-dens."),
                ("scaling", "SKAY-ling."),
                ("resourcing", "ree-SOR-sing."),
            ],
            "response_prompts": [
                {
                    "prompt": "Frame the issue in one line.",
                    "target_response": "Let me frame this: we need reliability and stakeholder confidence before scaling.",
                    "acceptable_variations": [
                        "Let me frame this: we need reliability and stakeholder confidence before scaling.",
                        "Let me frame this: we need stable metrics and confidence before scaling.",
                    ],
                },
                {
                    "prompt": "Give a nuanced position with a clear condition.",
                    "target_response": "On balance, I support the rollout, but only after we validate pilot metrics.",
                    "acceptable_variations": [
                        "On balance, I support the rollout, but only after we validate pilot metrics.",
                        "On balance, I support it, but only after we validate the data.",
                    ],
                },
                {
                    "prompt": "Label decisions and open questions, then close with next steps.",
                    "target_response": "The decision is to run a two-week pilot. The open questions are resourcing and change management. Next steps are: I'll send a summary today, and we'll align tomorrow.",
                    "acceptable_variations": [
                        "The decision is to run a two-week pilot. The open questions are resourcing and change management. Next steps are: I'll send a summary today, and we'll align tomorrow.",
                        "The decision is to start with a pilot. The open questions are staffing and scope. Next steps are: I'll send a summary today, and we'll align tomorrow.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "decision_label",
                    "type": "multiple_choice",
                    "prompt": "Which phrase labels a decision clearly?",
                    "options": ["The decision is ...", "I guess ...", "No decision."],
                    "correct_answer": "The decision is ...",
                },
                {
                    "key": "open_questions_label",
                    "type": "multiple_choice",
                    "prompt": "Which phrase labels uncertainty as open questions?",
                    "options": ["The open questions are ...", "Everything is solved.", "No questions."],
                    "correct_answer": "The open questions are ...",
                },
                {
                    "key": "nuance_marker",
                    "type": "multiple_choice",
                    "prompt": "Which phrase marks a nuanced position?",
                    "options": ["On balance, ... but ...", "Always ...", "Never ..."],
                    "correct_answer": "On balance, ... but ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_final_test_practice",
                "opening_line": "Final test practice: answer my prompts.",
                "learner_goal": "Answer C1 prompts with nuance, structure, and precision under pressure.",
                "turns": [
                    {
                        "coach": "Frame the issue in one line.",
                        "hint": "Let me frame this...",
                        "sample_answer": "Let me frame this: we need reliability and stakeholder confidence before scaling.",
                        "focus": "Frame",
                        "expected_keywords": ["frame", "reliability"],
                    },
                    {
                        "coach": "Give a nuanced position with a condition.",
                        "hint": "On balance... but only after...",
                        "sample_answer": "On balance, I support the rollout, but only after we validate pilot metrics.",
                        "focus": "Nuance",
                        "expected_keywords": ["on balance", "only after", "validate"],
                    },
                    {
                        "coach": "Label decisions and open questions, then close with next steps.",
                        "hint": "The decision is... The open questions are... Next steps are...",
                        "sample_answer": "The decision is to run a two-week pilot. The open questions are resourcing and change management. Next steps are: I'll send a summary today, and we'll align tomorrow.",
                        "focus": "Structure",
                        "expected_keywords": ["decision", "open questions", "next steps"],
                    },
                ],
                "target_phrases": ["Let me frame this: ...", "On balance, ...", "The decision is ...", "The open questions are ...", "Next steps are ..."],
            },
            "reading_support": "In C1 test-style prompts, structure is your advantage. Keep answers short but precise: frame the issue, state a nuanced position, label decisions and open questions, then close with next steps.",
            "writing_support_lines": [
                "Write 10 lines (one per prompt):",
                "1. Let me frame this: ...",
                "2. On balance, I ... but ...",
                "3. To be precise, ...",
                "4. The core assumption is ...",
                "5. If we accept X, then ...",
                "6. The key trade-off is ...",
                "7. The decision is ...",
                "8. The open questions are ...",
                "9. Next steps are: ...",
                "10. I'll share ... by ...",
            ],
            "goal_examples": ["Let me frame this: ...", "On balance, ...", "The decision is ..."],
        },
        {
            "lesson_key": "lesson-05-c1-final-conversation",
            "slug": "c1-final-conversation",
            "title": "C1 Final Conversation",
            "conversation_situation": "c1_final_conversation",
            "conversation_goal": "Lead a complex conversation from framing to decision: nuance, debate, leadership listening, and clear next steps.",
            "grammar_summary": "Use Let me frame this... / On balance... / What I'm hearing is... / The decision is... / The open questions are... / Next steps are... to lead end-to-end.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Final: kamu memimpin percakapan kompleks yang realistis. Kamu harus frame, jawab tantangan, nangkep maksud, dan tutup dengan keputusan + next steps.",
            "dialogue": [
                ("Jordan", "We need a final decision for next quarter."),
                ("Mina", "Let me frame this: we need reliable outcomes and stakeholder confidence before scaling."),
                ("Jordan", "Leadership wants speed."),
                ("Mina", "On balance, we can move fast, but only if we limit scope and validate metrics."),
                ("Jordan", "The team seems hesitant."),
                ("Mina", "What I'm hearing is some fear of visibility. When you say 'hesitant', do you mean scope concerns or accountability concerns?"),
                ("Jordan", "Accountability concerns."),
                ("Mina", "Got it. The decision is to run a two-week pilot with clear success criteria. Next steps are: I'll send a one-page plan today, and we'll align stakeholders tomorrow."),
            ],
            "translations": [
                ("Jordan", "We need a final decision for next quarter.", "Kita butuh keputusan final untuk kuartal depan."),
                ("Mina", "Let me frame this: we need reliable outcomes and stakeholder confidence before scaling.", "Biar aku frame: kita butuh outcome yang reliable dan kepercayaan stakeholder sebelum scale."),
                ("Jordan", "Leadership wants speed.", "Leadership maunya cepat."),
                ("Mina", "On balance, we can move fast, but only if we limit scope and validate metrics.", "Secara keseluruhan kita bisa cepat, tapi hanya kalau scope dibatasi dan metrik tervalidasi."),
                ("Jordan", "The team seems hesitant.", "Tim kelihatan ragu-ragu."),
                ("Mina", "What I'm hearing is some fear of visibility. When you say 'hesitant', do you mean scope concerns or accountability concerns?", "Yang aku tangkap: ada rasa takut terlihat/ter-spotlight. Kalau bilang 'ragu', maksudnya concern scope atau concern soal akuntabilitas?"),
                ("Jordan", "Accountability concerns.", "Concern akuntabilitas."),
                ("Mina", "Got it. The decision is to run a two-week pilot with clear success criteria. Next steps are: I'll send a one-page plan today, and we'll align stakeholders tomorrow.", "Oke. Keputusannya: jalankan pilot dua minggu dengan kriteria sukses yang jelas. Next steps: aku kirim plan satu halaman hari ini, lalu kita align stakeholder besok."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let me frame this: we need reliable outcomes and stakeholder confidence before scaling.",
                    "meaning_id": "Biar aku frame: kita butuh outcome yang reliable dan kepercayaan stakeholder sebelum scale.",
                    "usage_note": "Frame complex conversations with the true goal.",
                    "common_mistake": "Do not jump to tactics before framing goals.",
                },
                {
                    "phrase": "On balance, we can move fast, but only if we limit scope and validate metrics.",
                    "meaning_id": "Secara keseluruhan kita bisa cepat, tapi hanya kalau scope dibatasi dan metrik tervalidasi.",
                    "usage_note": "Nuanced compromise with conditions.",
                    "common_mistake": "Do not agree without conditions; state them clearly.",
                },
                {
                    "phrase": "What I'm hearing is some fear of visibility.",
                    "meaning_id": "Yang aku tangkap: ada rasa takut terlihat/ter-spotlight.",
                    "usage_note": "Catch implied meaning and name it carefully.",
                    "common_mistake": "Do not accuse; keep it as what I'm hearing.",
                },
                {
                    "phrase": "The decision is to run a two-week pilot with clear success criteria.",
                    "meaning_id": "Keputusannya: jalankan pilot dua minggu dengan kriteria sukses yang jelas.",
                    "usage_note": "Decision language with criteria.",
                    "common_mistake": "Do not end without a decision statement.",
                },
                {
                    "phrase": "Next steps are: I'll send a one-page plan today, and we'll align stakeholders tomorrow.",
                    "meaning_id": "Next steps: aku kirim plan satu halaman hari ini, lalu kita align stakeholder besok.",
                    "usage_note": "Close with owners and timing.",
                    "common_mistake": "Do not omit timing; add today/tomorrow/by Friday.",
                },
            ],
            "grammar_md": [
                (
                    "Final conversation toolkit",
                    [
                        "Let me frame this: ...",
                        "On balance, ... but only if ...",
                        "What I'm hearing is ...",
                        "When you say X, do you mean Y or Z?",
                        "The decision is ...",
                        "Next steps are ...",
                    ],
                )
            ],
            "pronunciation": [
                ("accountability", "uh-kown-tuh-BIL-ih-tee."),
                ("criteria", "kry-TEER-ee-uh."),
                ("stakeholder", "STAKE-hohl-der."),
            ],
            "response_prompts": [
                {
                    "prompt": "Frame the conversation goal.",
                    "target_response": "Let me frame this: we need reliable outcomes and stakeholder confidence before scaling.",
                    "acceptable_variations": [
                        "Let me frame this: we need reliable outcomes and stakeholder confidence before scaling.",
                        "Let me frame this: we need stable metrics and confidence before scaling.",
                    ],
                },
                {
                    "prompt": "Offer a nuanced compromise with conditions.",
                    "target_response": "On balance, we can move fast, but only if we limit scope and validate metrics.",
                    "acceptable_variations": [
                        "On balance, we can move fast, but only if we limit scope and validate metrics.",
                        "On balance, we can move quickly, but only if we keep scope tight and validate the data.",
                    ],
                },
                {
                    "prompt": "Close with a decision and next steps.",
                    "target_response": "The decision is to run a two-week pilot with clear success criteria. Next steps are: I'll send a one-page plan today, and we'll align stakeholders tomorrow.",
                    "acceptable_variations": [
                        "The decision is to run a two-week pilot with clear success criteria. Next steps are: I'll send a one-page plan today, and we'll align stakeholders tomorrow.",
                        "The decision is to run a pilot first. Next steps are: I'll send a plan today, and we'll align tomorrow.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "frame_goal",
                    "type": "multiple_choice",
                    "prompt": "Which phrase frames the goal of a complex conversation?",
                    "options": ["Let me frame this: ...", "No goal.", "Stop."],
                    "correct_answer": "Let me frame this: ...",
                },
                {
                    "key": "hearing_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase catches implied meaning carefully?",
                    "options": ["What I'm hearing is ...", "You're afraid.", "No feelings."],
                    "correct_answer": "What I'm hearing is ...",
                },
                {
                    "key": "decision_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase states the decision explicitly?",
                    "options": ["The decision is ...", "Maybe we ...", "Not sure."],
                    "correct_answer": "The decision is ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_final_conversation",
                "opening_line": "We need a final decision for next quarter.",
                "learner_goal": "Lead a complex conversation from framing to decision and next steps.",
                "turns": [
                    {
                        "coach": "Frame the conversation goal.",
                        "hint": "Let me frame this...",
                        "sample_answer": "Let me frame this: we need reliable outcomes and stakeholder confidence before scaling.",
                        "focus": "Frame",
                        "expected_keywords": ["frame", "confidence"],
                    },
                    {
                        "coach": "Respond with nuance and catch implied concerns.",
                        "hint": "On balance... What I'm hearing is... do you mean X or Y?",
                        "sample_answer": "On balance, we can move fast, but only if we limit scope and validate metrics. What I'm hearing is some fear of visibility. Do you mean scope concerns or accountability concerns?",
                        "focus": "Nuance + listening",
                        "expected_keywords": ["on balance", "only if", "hearing"],
                    },
                    {
                        "coach": "Close with a decision and next steps.",
                        "hint": "The decision is... Next steps are... today... tomorrow...",
                        "sample_answer": "The decision is to run a two-week pilot with clear success criteria. Next steps are: I'll send a one-page plan today, and we'll align stakeholders tomorrow.",
                        "focus": "Decision + next steps",
                        "expected_keywords": ["decision", "next steps", "today"],
                    },
                ],
                "target_phrases": ["Let me frame this: ...", "On balance, ...", "What I'm hearing is ...", "The decision is ...", "Next steps are ..."],
            },
            "reading_support": "A C1 final conversation is end-to-end leadership: frame the goal, handle pushback with nuance, listen for implied meaning, clarify ambiguity, then state the decision and next steps with ownership and timing.",
            "writing_support_lines": [
                "Write your final conversation (12 lines):",
                "1. Let me frame this: ...",
                "2. On balance, I ... but ...",
                "3. To be precise, ...",
                "4. What I'm hearing is ...",
                "5. When you say X, do you mean Y or Z?",
                "6. The core assumption is ...",
                "7. If we accept X, then ...",
                "8. The key trade-off is ...",
                "9. The decision is ...",
                "10. The open questions are ...",
                "11. Next steps are: I'll ..., and we'll ...",
                "12. Does that capture it accurately?",
            ],
            "goal_examples": ["Let me frame this: ...", "On balance, ...", "The decision is ..."],
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

