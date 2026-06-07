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
            "- Tone: professional, confident, clear",
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

        Read it again and underline the presenting words (today I'll, first, next, benefit, risk, question).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B2"
    b2_root = Path("content/curriculum/english/B2")
    units_root = b2_root / "units"
    unit_key = "unit-04-presenting-ideas"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-04-presenting-ideas
            level_code: B2
            title: Presenting Ideas
            main_conversation_outcome: Present an idea and answer questions naturally.
            status: in_production
            lessons:
              - lesson-01-structuring-a-short-presentation
              - lesson-02-signposting-clearly
              - lesson-03-explaining-benefits-and-risks
              - lesson-04-answering-questions
              - lesson-05-idea-presentation-mission
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
            "lesson_key": "lesson-01-structuring-a-short-presentation",
            "slug": "structuring-a-short-presentation",
            "title": "Structuring a Short Presentation",
            "conversation_situation": "structuring_short_presentation",
            "conversation_goal": "Present an idea with a clear structure: context, proposal, and next steps.",
            "grammar_summary": "Use Today I'd like to... / The problem is... / My proposal is... / Next steps are... to keep a short presentation clear.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu presentasi ide di meeting singkat. Kamu kasih konteks, jelasin proposal, dan tutup dengan next steps.",
            "dialogue": [
                ("Mina", "Today I'd like to share an idea to improve our onboarding."),
                ("Alex", "Great. What's the context?"),
                ("Mina", "The problem is new hires often feel lost in the first week."),
                ("Alex", "Okay. What's your proposal?"),
                ("Mina", "My proposal is a simple onboarding checklist and a buddy for the first two weeks."),
                ("Alex", "Sounds practical. What are the next steps?"),
                ("Mina", "Next steps are: draft the checklist today, then pilot it with the next hire."),
                ("Alex", "Nice. Let's do it."),
            ],
            "translations": [
                ("Mina", "Today I'd like to share an idea to improve our onboarding.", "Hari ini aku mau share ide untuk improve onboarding kita."),
                ("Alex", "Great. What's the context?", "Oke. Konteksnya apa?"),
                ("Mina", "The problem is new hires often feel lost in the first week.", "Masalahnya orang baru sering bingung di minggu pertama."),
                ("Alex", "Okay. What's your proposal?", "Oke. Proposal kamu apa?"),
                ("Mina", "My proposal is a simple onboarding checklist and a buddy for the first two weeks.", "Proposal aku: checklist onboarding sederhana dan buddy selama dua minggu pertama."),
                ("Alex", "Sounds practical. What are the next steps?", "Kedengarannya praktis. Next steps-nya apa?"),
                ("Mina", "Next steps are: draft the checklist today, then pilot it with the next hire.", "Next steps-nya: bikin draft checklist hari ini, lalu pilot dengan orang baru berikutnya."),
                ("Alex", "Nice. Let's do it.", "Oke. Gas."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Today I'd like to share an idea to improve our onboarding.",
                    "meaning_id": "Hari ini aku mau share ide untuk improve onboarding kita.",
                    "usage_note": "A clear presentation opening.",
                    "common_mistake": 'Do not start with too much detail; open with today I\'d like to.',
                },
                {
                    "phrase": "The problem is new hires often feel lost.",
                    "meaning_id": "Masalahnya orang baru sering bingung.",
                    "usage_note": "A clear problem statement.",
                    "common_mistake": 'Do not say "The problem are"; use is.',
                },
                {
                    "phrase": "My proposal is a simple checklist and a buddy system.",
                    "meaning_id": "Proposal aku: checklist sederhana dan buddy system.",
                    "usage_note": "A concise proposal sentence.",
                    "common_mistake": 'Do not say "My proposal are"; use is.',
                },
                {
                    "phrase": "Next steps are: draft it today, then pilot it.",
                    "meaning_id": "Next steps-nya: bikin draft hari ini, lalu pilot.",
                    "usage_note": "A strong, actionable close.",
                    "common_mistake": 'Do not end without next steps; include 1-2 actions.',
                },
                {
                    "phrase": "What's the context?",
                    "meaning_id": "Konteksnya apa?",
                    "usage_note": "A common audience question.",
                    "common_mistake": 'Do not answer without context; give one sentence.',
                },
            ],
            "grammar_md": [
                ("Presentation structure", ["Today I'd like to ...", "The problem is ...", "My proposal is ...", "Next steps are ..."]),
            ],
            "pronunciation": [
                ("proposal", "pruh-POH-zul."),
                ("onboarding", "ON-bor-ding."),
                ("checklist", "CHECK-list."),
            ],
            "response_prompts": [
                {
                    "prompt": "Open a short presentation.",
                    "target_response": "Today I'd like to share an idea to improve our onboarding.",
                    "acceptable_variations": [
                        "Today I'd like to share an idea to improve our onboarding.",
                        "Today I'd like to share an idea to improve our meetings.",
                    ],
                },
                {
                    "prompt": "State the problem.",
                    "target_response": "The problem is new hires often feel lost in the first week.",
                    "acceptable_variations": [
                        "The problem is new hires often feel lost in the first week.",
                        "The problem is we spend too much time in meetings.",
                    ],
                },
                {
                    "prompt": "Close with next steps.",
                    "target_response": "Next steps are: draft the checklist today, then pilot it with the next hire.",
                    "acceptable_variations": [
                        "Next steps are: draft the checklist today, then pilot it with the next hire.",
                        "Next steps are: write a draft today, then review it tomorrow.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "presentation_opening",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a clear presentation opening?",
                    "options": ["Today I'd like to share an idea.", "Idea. Listen.", "Now."],
                    "correct_answer": "Today I'd like to share an idea.",
                },
                {
                    "key": "proposal_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which sentence introduces a proposal?",
                    "options": ["My proposal is ...", "My proposing ...", "Proposal I ..."],
                    "correct_answer": "My proposal is ...",
                },
                {
                    "key": "next_steps",
                    "type": "multiple_choice",
                    "prompt": "Which phrase closes with action items?",
                    "options": ["Next steps are ...", "By the way ...", "Anyway ..."],
                    "correct_answer": "Next steps are ...",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_present_structure",
                "opening_line": "Please present your idea briefly.",
                "learner_goal": "Present an idea with context, proposal, and next steps.",
                "turns": [
                    {
                        "coach": "Open your presentation.",
                        "hint": "Today I'd like to...",
                        "sample_answer": "Today I'd like to share an idea to improve our onboarding.",
                        "focus": "Opening",
                        "expected_keywords": ["today", "idea"],
                    },
                    {
                        "coach": "State the problem and proposal.",
                        "hint": "The problem is... My proposal is...",
                        "sample_answer": "The problem is new hires feel lost. My proposal is a simple checklist and a buddy system.",
                        "focus": "Problem + proposal",
                        "expected_keywords": ["problem", "proposal"],
                    },
                    {
                        "coach": "Close with next steps.",
                        "hint": "Next steps are...",
                        "sample_answer": "Next steps are: draft the checklist today, then pilot it with the next hire.",
                        "focus": "Next steps",
                        "expected_keywords": ["next steps", "draft", "pilot"],
                    },
                ],
                "target_phrases": ["Today I'd like to ...", "The problem is ...", "Next steps are ..."],
            },
            "reading_support": "A strong short presentation is structured: open with the topic, explain the problem, propose a solution, then end with next steps.",
            "writing_support_lines": [
                "Write 7 lines:",
                "1. Today I'd like to ...",
                "2. The context is ...",
                "3. The problem is ...",
                "4. My proposal is ...",
                "5. The benefit is ...",
                "6. The risk is ...",
                "7. Next steps are ...",
            ],
            "goal_examples": ["Today I'd like to ...", "My proposal is ...", "Next steps are ..."],
        },
        {
            "lesson_key": "lesson-02-signposting-clearly",
            "slug": "signposting-clearly",
            "title": "Signposting Clearly",
            "conversation_situation": "signposting_in_presentation",
            "conversation_goal": "Use clear signposting to guide listeners through your presentation.",
            "grammar_summary": "Use First... / Next... / Finally... / Let me summarize... to make your presentation easy to follow.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu presentasi ide. Kamu pakai signposting supaya alurnya mudah diikutin.",
            "dialogue": [
                ("Mina", "Let me quickly walk you through the plan."),
                ("Jordan", "Sure."),
                ("Mina", "First, I'll explain the problem. Next, I'll share the proposal. Finally, I'll outline next steps."),
                ("Jordan", "Great. Go ahead."),
                ("Mina", "First, the problem is that onboarding is inconsistent across teams."),
                ("Jordan", "Okay."),
                ("Mina", "Next, the proposal is a shared checklist and a short orientation call."),
                ("Jordan", "And finally?"),
                ("Mina", "Finally, we can pilot it next week and collect feedback."),
            ],
            "translations": [
                ("Mina", "Let me quickly walk you through the plan.", "Biar aku jelasin rencana ini secara singkat ya."),
                ("Jordan", "Sure.", "Oke."),
                ("Mina", "First, I'll explain the problem. Next, I'll share the proposal. Finally, I'll outline next steps.", "Pertama, aku jelasin masalahnya. Berikutnya, aku share proposal. Terakhir, aku jelasin next steps."),
                ("Jordan", "Great. Go ahead.", "Oke. Silakan."),
                ("Mina", "First, the problem is that onboarding is inconsistent across teams.", "Pertama, masalahnya onboarding itu nggak konsisten antar tim."),
                ("Jordan", "Okay.", "Oke."),
                ("Mina", "Next, the proposal is a shared checklist and a short orientation call.", "Berikutnya, proposalnya checklist bersama dan call orientasi singkat."),
                ("Jordan", "And finally?", "Terus terakhir?"),
                ("Mina", "Finally, we can pilot it next week and collect feedback.", "Terakhir, kita bisa pilot minggu depan dan kumpulin feedback."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let me quickly walk you through the plan.",
                    "meaning_id": "Biar aku jelasin rencana ini secara singkat ya.",
                    "usage_note": "A natural signposting opener.",
                    "common_mistake": 'Do not say "Let me explain quickly you"; use walk you through.',
                },
                {
                    "phrase": "First, I'll explain the problem.",
                    "meaning_id": "Pertama, aku jelasin masalahnya.",
                    "usage_note": "Clear structure signpost.",
                    "common_mistake": 'Do not say "First I explaining"; use I\'ll explain.',
                },
                {
                    "phrase": "Next, I'll share the proposal.",
                    "meaning_id": "Berikutnya, aku share proposalnya.",
                    "usage_note": "Moves to the next section.",
                    "common_mistake": 'Do not forget the comma pause; keep it clear.',
                },
                {
                    "phrase": "Finally, I'll outline next steps.",
                    "meaning_id": "Terakhir, aku jelasin next steps.",
                    "usage_note": "Signals the closing part.",
                    "common_mistake": 'Do not say "Finally I will outlining"; use I\'ll outline.',
                },
                {
                    "phrase": "Let me summarize.",
                    "meaning_id": "Biar aku rangkum.",
                    "usage_note": "A quick wrap-up phrase.",
                    "common_mistake": 'Do not say "Let me summary"; summarize is the verb.',
                },
            ],
            "grammar_md": [
                ("Signposting", ["First, ...", "Next, ...", "Finally, ...", "Let me summarize ..."]),
            ],
            "pronunciation": [
                ("walk you through", "WAWK-yuh through."),
                ("outline", "OUT-line."),
                ("finally", "FYE-nuh-lee."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start with signposting opener.",
                    "target_response": "Let me quickly walk you through the plan.",
                    "acceptable_variations": ["Let me quickly walk you through the plan.", "Let me walk you through the plan."],
                },
                {
                    "prompt": "Use first/next/finally.",
                    "target_response": "First, I'll explain the problem. Next, I'll share the proposal. Finally, I'll outline next steps.",
                    "acceptable_variations": [
                        "First, I'll explain the problem. Next, I'll share the proposal. Finally, I'll outline next steps.",
                        "First, I'll share context. Next, I'll explain benefits. Finally, I'll summarize.",
                    ],
                },
                {
                    "prompt": "Use let me summarize.",
                    "target_response": "Let me summarize the key points.",
                    "acceptable_variations": ["Let me summarize the key points.", "Let me summarize our decision."],
                },
            ],
            "quiz": [
                {
                    "key": "signposting_words",
                    "type": "multiple_choice",
                    "prompt": "Which set are signposting words?",
                    "options": ["First / Next / Finally", "Blue / Green / Red", "Yesterday / Tomorrow / Never"],
                    "correct_answer": "First / Next / Finally",
                },
                {
                    "key": "walk_you_through",
                    "type": "multiple_choice",
                    "prompt": 'What does "walk you through" mean?',
                    "options": ["menjelaskan langkah demi langkah", "jalan-jalan", "menolak ide"],
                    "correct_answer": "menjelaskan langkah demi langkah",
                },
                {
                    "key": "summarize_verb",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["Let me summarize.", "Let me summary.", "Let me summarizing."],
                    "correct_answer": "Let me summarize.",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_present_signposting",
                "opening_line": "Can you guide us through your presentation?",
                "learner_goal": "Use signposting to structure your presentation clearly.",
                "turns": [
                    {
                        "coach": "Start with a signposting opener.",
                        "hint": "Let me walk you through...",
                        "sample_answer": "Let me quickly walk you through the plan.",
                        "focus": "Opener",
                        "expected_keywords": ["walk you through"],
                    },
                    {
                        "coach": "Use first, next, finally to outline your structure.",
                        "hint": "First... Next... Finally...",
                        "sample_answer": "First, I'll explain the problem. Next, I'll share the proposal. Finally, I'll outline next steps.",
                        "focus": "Structure",
                        "expected_keywords": ["first", "next", "finally"],
                    },
                    {
                        "coach": "Wrap up with a short summary phrase.",
                        "hint": "Let me summarize...",
                        "sample_answer": "Let me summarize the key points in one sentence.",
                        "focus": "Summary",
                        "expected_keywords": ["summarize"],
                    },
                ],
                "target_phrases": ["Let me walk you through ...", "First, ... Next, ... Finally, ...", "Let me summarize ..."],
            },
            "reading_support": "Signposting makes presentations easy to follow. Use first/next/finally and a short summary to guide your listeners.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. Let me walk you through ...",
                "2. First, ...",
                "3. Next, ...",
                "4. Finally, ...",
                "5. Let me summarize ...",
                "6. Any questions?",
            ],
            "goal_examples": ["First, ...", "Next, ...", "Finally, ..."],
        },
        {
            "lesson_key": "lesson-03-explaining-benefits-and-risks",
            "slug": "explaining-benefits-and-risks",
            "title": "Explaining Benefits and Risks",
            "conversation_situation": "explaining_benefits_risks",
            "conversation_goal": "Explain two benefits, mention one risk, and propose a mitigation plan.",
            "grammar_summary": "Use The main benefit is... / Another benefit is... / A key risk is... / To reduce the risk, we can... to present trade-offs clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu jelasin ide dan trade-off-nya. Kamu sebut manfaat, risikonya, lalu mitigasinya.",
            "dialogue": [
                ("Alex", "What are the benefits of your idea?"),
                ("Mina", "The main benefit is faster onboarding for new hires."),
                ("Alex", "Anything else?"),
                ("Mina", "Another benefit is fewer repeated questions for the team."),
                ("Alex", "Okay. Any risks?"),
                ("Mina", "A key risk is that the checklist becomes outdated."),
                ("Alex", "How can we reduce that risk?"),
                ("Mina", "To reduce the risk, we can review it monthly and assign an owner."),
            ],
            "translations": [
                ("Alex", "What are the benefits of your idea?", "Apa manfaat dari ide kamu?"),
                ("Mina", "The main benefit is faster onboarding for new hires.", "Manfaat utamanya onboarding lebih cepat untuk orang baru."),
                ("Alex", "Anything else?", "Ada lagi?"),
                ("Mina", "Another benefit is fewer repeated questions for the team.", "Manfaat lainnya pertanyaan berulang jadi lebih sedikit untuk tim."),
                ("Alex", "Okay. Any risks?", "Oke. Ada risiko?"),
                ("Mina", "A key risk is that the checklist becomes outdated.", "Risiko utamanya checklist jadi nggak update."),
                ("Alex", "How can we reduce that risk?", "Gimana cara ngurangin risikonya?"),
                ("Mina", "To reduce the risk, we can review it monthly and assign an owner.", "Untuk ngurangin risiko, kita bisa review tiap bulan dan tentuin owner."),
            ],
            "useful_phrases": [
                {
                    "phrase": "The main benefit is faster onboarding for new hires.",
                    "meaning_id": "Manfaat utamanya onboarding lebih cepat untuk orang baru.",
                    "usage_note": "A clear benefit sentence.",
                    "common_mistake": 'Do not say "main benefit are"; use is.',
                },
                {
                    "phrase": "Another benefit is fewer repeated questions.",
                    "meaning_id": "Manfaat lainnya pertanyaan berulang jadi lebih sedikit.",
                    "usage_note": "Add a second benefit clearly.",
                    "common_mistake": 'Do not say "another benefit are"; use is.',
                },
                {
                    "phrase": "A key risk is that the checklist becomes outdated.",
                    "meaning_id": "Risiko utamanya checklist jadi nggak update.",
                    "usage_note": "A clear risk statement.",
                    "common_mistake": 'Do not say "risk is the checklist outdated" without that-clause; keep it clear.',
                },
                {
                    "phrase": "To reduce the risk, we can review it monthly.",
                    "meaning_id": "Untuk ngurangin risiko, kita bisa review tiap bulan.",
                    "usage_note": "A mitigation plan sentence.",
                    "common_mistake": 'Do not say "reduce risk we can" without to; keep the structure.',
                },
                {
                    "phrase": "We should assign an owner.",
                    "meaning_id": "Kita perlu tentuin owner.",
                    "usage_note": "A practical governance step.",
                    "common_mistake": 'Do not say "assign owner" without an/the in a full sentence.',
                },
            ],
            "grammar_md": [
                ("Benefits and risks", ["The main benefit is ...", "Another benefit is ...", "A key risk is ..."]),
                ("Mitigation", ["To reduce the risk, we can ...", "To mitigate this, we can ..."]),
            ],
            "pronunciation": [
                ("benefit", "BEN-uh-fit."),
                ("risk", "RISK."),
                ("outdated", "out-DAY-tid."),
            ],
            "response_prompts": [
                {
                    "prompt": "State the main benefit.",
                    "target_response": "The main benefit is faster onboarding for new hires.",
                    "acceptable_variations": [
                        "The main benefit is faster onboarding for new hires.",
                        "The main benefit is better clarity.",
                    ],
                },
                {
                    "prompt": "State a key risk.",
                    "target_response": "A key risk is that the checklist becomes outdated.",
                    "acceptable_variations": [
                        "A key risk is that the checklist becomes outdated.",
                        "A key risk is that it adds extra work.",
                    ],
                },
                {
                    "prompt": "Propose mitigation.",
                    "target_response": "To reduce the risk, we can review it monthly and assign an owner.",
                    "acceptable_variations": [
                        "To reduce the risk, we can review it monthly and assign an owner.",
                        "To reduce the risk, we can start with a small pilot.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "benefit_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a benefit?",
                    "options": ["The main benefit is ...", "The main because ...", "The main point was ..."],
                    "correct_answer": "The main benefit is ...",
                },
                {
                    "key": "risk_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a risk?",
                    "options": ["A key risk is ...", "A key reason is ...", "A key step is ..."],
                    "correct_answer": "A key risk is ...",
                },
                {
                    "key": "mitigation_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces mitigation?",
                    "options": ["To reduce the risk, we can ...", "To angry, we can ...", "To random, we can ..."],
                    "correct_answer": "To reduce the risk, we can ...",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_present_benefits_risks",
                "opening_line": "Explain benefits and risks of your idea.",
                "learner_goal": "Explain benefits, a risk, and mitigation clearly.",
                "turns": [
                    {
                        "coach": "What is the main benefit?",
                        "hint": "The main benefit is ...",
                        "sample_answer": "The main benefit is faster onboarding for new hires.",
                        "focus": "Benefit 1",
                        "expected_keywords": ["main benefit"],
                    },
                    {
                        "coach": "Give another benefit.",
                        "hint": "Another benefit is ...",
                        "sample_answer": "Another benefit is fewer repeated questions for the team.",
                        "focus": "Benefit 2",
                        "expected_keywords": ["another benefit"],
                    },
                    {
                        "coach": "Now mention a key risk and mitigation.",
                        "hint": "A key risk is... To reduce the risk, we can...",
                        "sample_answer": "A key risk is that it becomes outdated. To reduce the risk, we can review it monthly and assign an owner.",
                        "focus": "Risk + mitigation",
                        "expected_keywords": ["risk", "reduce"],
                    },
                ],
                "target_phrases": ["The main benefit is ...", "A key risk is ...", "To reduce the risk, we can ..."],
            },
            "reading_support": "Presenting ideas professionally means discussing trade-offs: benefits, risks, and how you will reduce the risks.",
            "writing_support_lines": [
                "Write 7 lines:",
                "1. The main benefit is ...",
                "2. Another benefit is ...",
                "3. A key risk is ...",
                "4. To reduce the risk, we can ...",
                "5. We'll measure ...",
                "6. We'll review ...",
                "7. Next steps are ...",
            ],
            "goal_examples": ["The main benefit is ...", "A key risk is ...", "To reduce the risk, we can ..."],
        },
        {
            "lesson_key": "lesson-04-answering-questions",
            "slug": "answering-questions",
            "title": "Answering Questions",
            "conversation_situation": "answering_questions_after_presentation",
            "conversation_goal": "Answer a question clearly, admit uncertainty when needed, and offer to follow up.",
            "grammar_summary": "Use That's a good question / As far as I know... / I'm not sure, but I can follow up to answer questions professionally.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Setelah presentasi, kamu jawab pertanyaan dengan jelas. Kalau belum yakin, kamu bilang jujur dan janji follow up.",
            "dialogue": [
                ("Jordan", "How much effort will this take?"),
                ("Mina", "That's a good question. As far as I know, the first version takes about one day."),
                ("Jordan", "What about maintenance?"),
                ("Mina", "I'm not sure yet, but I can follow up with a monthly estimate by tomorrow."),
                ("Jordan", "Okay. Who will own it?"),
                ("Mina", "I suggest we assign one owner per quarter to keep it updated."),
                ("Jordan", "Makes sense."),
                ("Mina", "Any other questions?"),
            ],
            "translations": [
                ("Jordan", "How much effort will this take?", "Ini butuh effort berapa besar?"),
                ("Mina", "That's a good question. As far as I know, the first version takes about one day.", "Pertanyaan bagus. Sejauh yang aku tahu, versi pertama butuh sekitar satu hari."),
                ("Jordan", "What about maintenance?", "Kalau maintenance gimana?"),
                ("Mina", "I'm not sure yet, but I can follow up with a monthly estimate by tomorrow.", "Aku belum yakin, tapi aku bisa follow up dengan estimasi bulanan besok."),
                ("Jordan", "Okay. Who will own it?", "Oke. Siapa yang jadi owner?"),
                ("Mina", "I suggest we assign one owner per quarter to keep it updated.", "Aku saranin kita assign satu owner per kuartal supaya tetap update."),
                ("Jordan", "Makes sense.", "Masuk akal."),
                ("Mina", "Any other questions?", "Ada pertanyaan lain?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "That's a good question.",
                    "meaning_id": "Pertanyaan bagus.",
                    "usage_note": "A polite opener when answering.",
                    "common_mistake": 'Do not respond defensively; start with a good question.',
                },
                {
                    "phrase": "As far as I know, it takes about one day.",
                    "meaning_id": "Sejauh yang aku tahu, butuh sekitar satu hari.",
                    "usage_note": "Answer with confidence level.",
                    "common_mistake": 'Do not say "As far I know"; include as far as.',
                },
                {
                    "phrase": "I'm not sure yet, but I can follow up by tomorrow.",
                    "meaning_id": "Aku belum yakin, tapi aku bisa follow up besok.",
                    "usage_note": "Admit uncertainty professionally.",
                    "common_mistake": 'Do not say "I don\'t know" without follow-up; offer a follow-up.',
                },
                {
                    "phrase": "I suggest we assign an owner.",
                    "meaning_id": "Aku saranin kita assign owner.",
                    "usage_note": "A practical answer to governance questions.",
                    "common_mistake": 'Do not say "I suggest assign"; include we.',
                },
                {
                    "phrase": "Any other questions?",
                    "meaning_id": "Ada pertanyaan lain?",
                    "usage_note": "A polite closing invitation.",
                    "common_mistake": 'Do not rush; pause before asking this.',
                },
            ],
            "grammar_md": [
                ("Answering questions", ["That's a good question.", "As far as I know, ...", "I'm not sure yet, but I can follow up ..."]),
            ],
            "pronunciation": [
                ("effort", "EF-ert."),
                ("estimate", "ES-ti-mit (noun) / ES-ti-mayt (verb)."),
                ("follow up", "FAH-loh up."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start an answer politely.",
                    "target_response": "That's a good question.",
                    "acceptable_variations": ["That's a good question.", "Good question."],
                },
                {
                    "prompt": "Answer with confidence level.",
                    "target_response": "As far as I know, it takes about one day.",
                    "acceptable_variations": ["As far as I know, it takes about one day.", "As far as I know, it takes about a week."],
                },
                {
                    "prompt": "Admit uncertainty and offer follow-up.",
                    "target_response": "I'm not sure yet, but I can follow up by tomorrow.",
                    "acceptable_variations": [
                        "I'm not sure yet, but I can follow up by tomorrow.",
                        "I'm not sure yet, but I can check and get back to you.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "good_question",
                    "type": "multiple_choice",
                    "prompt": "Which phrase is a polite opener?",
                    "options": ["That's a good question.", "That's a bad question.", "Stop asking."],
                    "correct_answer": "That's a good question.",
                },
                {
                    "key": "follow_up_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "follow up" mean?',
                    "options": ["menindaklanjuti", "menolak", "melupakan"],
                    "correct_answer": "menindaklanjuti",
                },
                {
                    "key": "not_sure_structure",
                    "type": "multiple_choice",
                    "prompt": "Choose the best professional response.",
                    "options": [
                        "I'm not sure yet, but I can follow up by tomorrow.",
                        "I don't know.",
                        "No idea.",
                    ],
                    "correct_answer": "I'm not sure yet, but I can follow up by tomorrow.",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_present_answer_questions",
                "opening_line": "I have some questions about your idea.",
                "learner_goal": "Answer questions clearly and professionally, including uncertainty and follow-up.",
                "turns": [
                    {
                        "coach": "How much effort will this take?",
                        "hint": "That's a good question. As far as I know...",
                        "sample_answer": "That's a good question. As far as I know, the first version takes about one day.",
                        "focus": "Answer with confidence level",
                        "expected_keywords": ["good question", "as far as I know"],
                    },
                    {
                        "coach": "What about maintenance?",
                        "hint": "I'm not sure yet, but I can follow up...",
                        "sample_answer": "I'm not sure yet, but I can follow up with an estimate by tomorrow.",
                        "focus": "Uncertainty + follow up",
                        "expected_keywords": ["not sure", "follow up"],
                    },
                    {
                        "coach": "Who will own it?",
                        "hint": "I suggest we assign...",
                        "sample_answer": "I suggest we assign one owner per quarter to keep it updated.",
                        "focus": "Ownership answer",
                        "expected_keywords": ["suggest", "assign", "owner"],
                    },
                ],
                "target_phrases": ["That's a good question.", "I'm not sure yet, but ...", "I suggest we ..."],
            },
            "reading_support": "Good Q&A feels professional: acknowledge the question, answer clearly, and if you're unsure, offer a specific follow-up time.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. That's a good question.",
                "2. As far as I know, ...",
                "3. I'm not sure yet, but ...",
                "4. I can follow up by ...",
                "5. I suggest we ...",
                "6. Any other questions?",
            ],
            "goal_examples": ["That's a good question.", "As far as I know, ...", "I'm not sure yet, but ..."],
        },
        {
            "lesson_key": "lesson-05-idea-presentation-mission",
            "slug": "idea-presentation-mission",
            "title": "Idea Presentation Mission",
            "conversation_situation": "mission_present_idea_and_qa",
            "conversation_goal": "Complete a mini presentation: structure the idea, signpost clearly, explain benefits and risks, and answer questions professionally.",
            "grammar_summary": "Combine: Today I'd like to... / First... Next... Finally... / The main benefit is... / A key risk is... / That's a good question...",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Misi: kamu presentasi ide singkat lalu Q&A. Kamu pakai struktur, signposting, trade-offs, dan jawaban profesional.",
            "dialogue": [
                ("Alex", "You have two minutes. Present your idea."),
                ("Mina", "Today I'd like to propose a shared onboarding checklist."),
                ("Mina", "First, the problem is onboarding is inconsistent. Next, the proposal is a checklist plus a buddy. Finally, we'll pilot it next week."),
                ("Alex", "What are the benefits?"),
                ("Mina", "The main benefit is faster onboarding. Another benefit is fewer repeated questions."),
                ("Alex", "Any risks?"),
                ("Mina", "A key risk is it becomes outdated. To reduce the risk, we'll review it monthly and assign an owner."),
                ("Alex", "How much effort will it take?"),
                ("Mina", "That's a good question. As far as I know, the first version takes about one day. I'm not sure about maintenance yet, but I can follow up by tomorrow."),
            ],
            "translations": [
                ("Alex", "You have two minutes. Present your idea.", "Kamu punya dua menit. Presentasiin idemu."),
                ("Mina", "Today I'd like to propose a shared onboarding checklist.", "Hari ini aku mau usul checklist onboarding bersama."),
                ("Mina", "First, the problem is onboarding is inconsistent. Next, the proposal is a checklist plus a buddy. Finally, we'll pilot it next week.", "Pertama, masalahnya onboarding nggak konsisten. Berikutnya, proposalnya checklist plus buddy. Terakhir, kita pilot minggu depan."),
                ("Alex", "What are the benefits?", "Apa manfaatnya?"),
                ("Mina", "The main benefit is faster onboarding. Another benefit is fewer repeated questions.", "Manfaat utamanya onboarding lebih cepat. Manfaat lainnya pertanyaan berulang berkurang."),
                ("Alex", "Any risks?", "Ada risiko?"),
                ("Mina", "A key risk is it becomes outdated. To reduce the risk, we'll review it monthly and assign an owner.", "Risiko utamanya jadi nggak update. Untuk ngurangin risiko, kita review tiap bulan dan tentuin owner."),
                ("Alex", "How much effort will it take?", "Butuh effort berapa?"),
                ("Mina", "That's a good question. As far as I know, the first version takes about one day. I'm not sure about maintenance yet, but I can follow up by tomorrow.", "Pertanyaan bagus. Sejauh yang aku tahu, versi pertama butuh sekitar satu hari. Aku belum yakin maintenance-nya, tapi aku bisa follow up besok."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Today I'd like to propose a shared onboarding checklist.",
                    "meaning_id": "Hari ini aku mau usul checklist onboarding bersama.",
                    "usage_note": "A concise mission opening.",
                    "common_mistake": "Keep it short; don't add extra details in the first sentence.",
                },
                {
                    "phrase": "First... Next... Finally...",
                    "meaning_id": "Pertama... Berikutnya... Terakhir...",
                    "usage_note": "Signposting for structure.",
                    "common_mistake": "Don't overuse signposts; 3 is enough.",
                },
                {
                    "phrase": "The main benefit is ... Another benefit is ...",
                    "meaning_id": "Manfaat utama ... Manfaat lain ...",
                    "usage_note": "Clear benefits structure.",
                    "common_mistake": "Don't list too many benefits; two is enough.",
                },
                {
                    "phrase": "A key risk is ... To reduce the risk, we can ...",
                    "meaning_id": "Risiko utama ... Untuk ngurangin risiko, kita bisa ...",
                    "usage_note": "Risk + mitigation.",
                    "common_mistake": "Always add mitigation after a risk.",
                },
                {
                    "phrase": "I'm not sure yet, but I can follow up by tomorrow.",
                    "meaning_id": "Aku belum yakin, tapi aku bisa follow up besok.",
                    "usage_note": "Professional uncertainty.",
                    "common_mistake": "Always include a follow-up time.",
                },
            ],
            "grammar_md": [
                (
                    "Presentation + Q&A flow",
                    [
                        "Today I'd like to ...",
                        "First ... Next ... Finally ...",
                        "The main benefit is ... Another benefit is ...",
                        "A key risk is ... To reduce the risk, ...",
                        "That's a good question. As far as I know, ...",
                    ],
                ),
            ],
            "pronunciation": [
                ("inconsistent", "in-kun-SIS-tent."),
                ("benefit", "BEN-uh-fit."),
                ("maintenance", "MAYN-tuh-nens."),
            ],
            "response_prompts": [
                {
                    "prompt": "Present your idea opening.",
                    "target_response": "Today I'd like to propose a shared onboarding checklist.",
                    "acceptable_variations": [
                        "Today I'd like to propose a shared onboarding checklist.",
                        "Today I'd like to propose a change to our meeting format.",
                    ],
                },
                {
                    "prompt": "Explain benefits and risk.",
                    "target_response": "The main benefit is faster onboarding. A key risk is it becomes outdated. To reduce the risk, we'll review it monthly.",
                    "acceptable_variations": [
                        "The main benefit is faster onboarding. A key risk is it becomes outdated. To reduce the risk, we'll review it monthly.",
                        "The main benefit is better clarity. A key risk is extra work. To reduce the risk, we'll start small.",
                    ],
                },
                {
                    "prompt": "Answer a question with follow-up.",
                    "target_response": "That's a good question. I'm not sure yet, but I can follow up by tomorrow.",
                    "acceptable_variations": [
                        "That's a good question. I'm not sure yet, but I can follow up by tomorrow.",
                        "That's a good question. I'm not sure yet, but I can check and get back to you.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "mission_flow_present",
                    "type": "multiple_choice",
                    "prompt": "Which flow fits an idea presentation?",
                    "options": [
                        "Structure -> signposting -> benefits/risks -> Q&A",
                        "Greeting -> goodbye",
                        "Numbers -> spelling",
                    ],
                    "correct_answer": "Structure -> signposting -> benefits/risks -> Q&A",
                },
                {
                    "key": "signpost_count",
                    "type": "multiple_choice",
                    "prompt": "Which set is a clear 3-part signpost?",
                    "options": ["First / Next / Finally", "First / Because / However", "Maybe / Anyway / Never mind"],
                    "correct_answer": "First / Next / Finally",
                },
                {
                    "key": "follow_up_best",
                    "type": "multiple_choice",
                    "prompt": "Which is the best professional response when unsure?",
                    "options": [
                        "I'm not sure yet, but I can follow up by tomorrow.",
                        "I don't know.",
                        "No idea.",
                    ],
                    "correct_answer": "I'm not sure yet, but I can follow up by tomorrow.",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_present_mission",
                "opening_line": "You have two minutes. Present your idea, then answer my questions.",
                "learner_goal": "Present an idea clearly and handle Q&A professionally.",
                "turns": [
                    {
                        "coach": "Present your idea in 2-3 sentences with signposting.",
                        "hint": "Today I'd like to... First... Next... Finally...",
                        "sample_answer": "Today I'd like to propose a shared onboarding checklist. First, the problem is inconsistency. Next, the proposal is a checklist plus a buddy. Finally, we'll pilot it next week.",
                        "focus": "Presentation with signposting",
                        "expected_keywords": ["today", "first", "next", "finally"],
                    },
                    {
                        "coach": "Explain benefits and one risk with mitigation.",
                        "hint": "The main benefit is... Another benefit is... A key risk is... To reduce the risk...",
                        "sample_answer": "The main benefit is faster onboarding. Another benefit is fewer repeated questions. A key risk is it becomes outdated. To reduce the risk, we'll review it monthly and assign an owner.",
                        "focus": "Benefits + risk + mitigation",
                        "expected_keywords": ["benefit", "risk", "reduce"],
                    },
                    {
                        "coach": "Answer a question and offer follow-up if needed.",
                        "hint": "That's a good question... I'm not sure yet, but I can follow up by...",
                        "sample_answer": "That's a good question. As far as I know, it takes about one day. I'm not sure about maintenance yet, but I can follow up by tomorrow.",
                        "focus": "Q&A",
                        "expected_keywords": ["good question", "as far as I know", "follow up"],
                    },
                ],
                "target_phrases": ["First, ... Next, ... Finally, ...", "The main benefit is ...", "I'm not sure yet, but I can follow up ..."],
            },
            "reading_support": "This mission combines full presentation skills: structure, signposting, trade-offs, and professional Q&A.",
            "writing_support_lines": [
                "Write your mission (10 lines):",
                "1. Today I'd like to ...",
                "2. First, ...",
                "3. Next, ...",
                "4. Finally, ...",
                "5. The main benefit is ...",
                "6. Another benefit is ...",
                "7. A key risk is ...",
                "8. To reduce the risk, ...",
                "9. That's a good question. As far as I know, ...",
                "10. I'm not sure yet, but I can follow up by ...",
            ],
            "goal_examples": ["Today I'd like to ...", "The main benefit is ...", "That's a good question."],
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
