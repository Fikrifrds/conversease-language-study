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
            "- Tone: professional, clear, confident",
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

        Read it again and underline the argument words (in my view, I believe, one reason, for example, however).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B2"
    b2_root = Path("content/curriculum/english/B2")
    units_root = b2_root / "units"
    unit_key = "unit-01-clear-arguments"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-01-clear-arguments
            level_code: B2
            title: Clear Arguments
            main_conversation_outcome: Present and support an argument clearly in conversation.
            status: in_production
            lessons:
              - lesson-01-stating-your-position
              - lesson-02-supporting-with-reasons
              - lesson-03-using-examples
              - lesson-04-responding-to-counterpoints
              - lesson-05-clear-argument-mission
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
            "lesson_key": "lesson-01-stating-your-position",
            "slug": "stating-your-position",
            "title": "Stating Your Position",
            "conversation_situation": "stating_position_in_meeting",
            "conversation_goal": "State your position clearly, acknowledge another view, and give one short reason.",
            "grammar_summary": "Use In my view... / I believe... and I see your point, but... to state a position clearly and politely.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu lagi diskusi di meeting. Kamu jelasin posisi kamu, akui pendapat orang lain, lalu kasih satu alasan utama.",
            "dialogue": [
                ("Alex", "Should we switch our weekly meeting to a written update?"),
                ("Mina", "In my view, a written update would be better for routine topics."),
                ("Alex", "Why do you think that?"),
                ("Mina", "Because it saves time and lets people focus on deep work."),
                ("Alex", "But some people like real-time discussion."),
                ("Mina", "I see your point, but we can keep one live meeting per month for open discussions."),
                ("Alex", "That sounds like a good compromise."),
                ("Mina", "Great. I'm happy to draft a proposal."),
            ],
            "translations": [
                ("Alex", "Should we switch our weekly meeting to a written update?", "Kita perlu ganti meeting mingguan jadi update tertulis nggak?"),
                ("Mina", "In my view, a written update would be better for routine topics.", "Menurutku, update tertulis lebih bagus untuk topik rutin."),
                ("Alex", "Why do you think that?", "Kenapa kamu pikir begitu?"),
                ("Mina", "Because it saves time and lets people focus on deep work.", "Karena itu hemat waktu dan bikin orang bisa fokus kerja yang butuh konsentrasi."),
                ("Alex", "But some people like real-time discussion.", "Tapi ada yang suka diskusi langsung."),
                ("Mina", "I see your point, but we can keep one live meeting per month for open discussions.", "Aku paham poin kamu, tapi kita bisa tetap adain satu meeting live per bulan untuk diskusi bebas."),
                ("Alex", "That sounds like a good compromise.", "Kedengarannya kompromi yang bagus."),
                ("Mina", "Great. I'm happy to draft a proposal.", "Oke. Aku siap bikin draft proposal-nya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "In my view, a written update would be better.",
                    "meaning_id": "Menurutku, update tertulis lebih bagus.",
                    "usage_note": "A clear and polite way to state your position.",
                    "common_mistake": 'Do not say "In my opinion is"; use In my view, ...',
                },
                {
                    "phrase": "Because it saves time.",
                    "meaning_id": "Karena itu hemat waktu.",
                    "usage_note": "Give one short reason.",
                    "common_mistake": 'Do not say "Because saves time"; include it.',
                },
                {
                    "phrase": "I see your point, but...",
                    "meaning_id": "Aku paham poin kamu, tapi...",
                    "usage_note": "Acknowledge and disagree politely.",
                    "common_mistake": 'Do not jump to disagreement without acknowledging; use I see your point.',
                },
                {
                    "phrase": "That sounds like a good compromise.",
                    "meaning_id": "Kedengarannya kompromi yang bagus.",
                    "usage_note": "A positive reaction to a balanced solution.",
                    "common_mistake": 'Do not say "That sound"; add -s.',
                },
                {
                    "phrase": "I'm happy to draft a proposal.",
                    "meaning_id": "Aku siap bikin draft proposal.",
                    "usage_note": "Offer a clear next step.",
                    "common_mistake": 'Do not say "I am happy draft"; use happy to + verb.',
                },
            ],
            "grammar_md": [
                ("In my view / I believe", ["In my view, a written update would be better.", "I believe this approach is more efficient."]),
                ("Acknowledge + but", ["I see your point, but we need to consider the timeline.", "I see your point, but I have a different view."]),
            ],
            "pronunciation": [
                ("compromise", "KOM-pruh-mize."),
                ("proposal", "pruh-POH-zul."),
                ("efficient", "ih-FISH-unt."),
            ],
            "response_prompts": [
                {
                    "prompt": "State your position (In my view...).",
                    "target_response": "In my view, a written update would be better.",
                    "acceptable_variations": [
                        "In my view, a written update would be better.",
                        "In my view, option B would be better.",
                    ],
                },
                {
                    "prompt": "Give one reason (Because...).",
                    "target_response": "Because it saves time.",
                    "acceptable_variations": ["Because it saves time.", "Because it's more efficient."],
                },
                {
                    "prompt": "Acknowledge and disagree politely.",
                    "target_response": "I see your point, but I prefer a different approach.",
                    "acceptable_variations": [
                        "I see your point, but I prefer a different approach.",
                        "I see your point, but we should consider the risks.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "position_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase politely states your position?",
                    "options": ["In my view, ...", "You are wrong.", "No, stop."],
                    "correct_answer": "In my view, ...",
                },
                {
                    "key": "acknowledge_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase acknowledges another view politely?",
                    "options": ["I see your point, but...", "That's stupid.", "Whatever."],
                    "correct_answer": "I see your point, but...",
                },
                {
                    "key": "compromise_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "compromise" mean?',
                    "options": ["kompromi", "penolakan", "janji"],
                    "correct_answer": "kompromi",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_argument_position",
                "opening_line": "What's your position on this?",
                "learner_goal": "State your position, give one reason, and respond politely to a counterpoint.",
                "turns": [
                    {
                        "coach": "What's your position on switching to written updates?",
                        "hint": "Mulai dengan In my view / I believe.",
                        "sample_answer": "In my view, a written update would be better for routine topics.",
                        "focus": "State position",
                        "expected_keywords": ["in my view", "better"],
                    },
                    {
                        "coach": "Why?",
                        "hint": "Jawab dengan because + satu alasan.",
                        "sample_answer": "Because it saves time and helps people focus.",
                        "focus": "Give reason",
                        "expected_keywords": ["because", "time"],
                    },
                    {
                        "coach": "But some people want real-time discussion.",
                        "hint": "Acknowledge + but + solusi singkat.",
                        "sample_answer": "I see your point, but we can keep one live meeting per month.",
                        "focus": "Respond to counterpoint",
                        "expected_keywords": ["see your point", "but"],
                    },
                ],
                "target_phrases": ["In my view, ...", "Because ...", "I see your point, but ..."],
            },
            "reading_support": "A clear position includes: your stance, one key reason, and a polite response to another view.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. In my view, ...",
                "2. Because ...",
                "3. I see your point, but ...",
                "4. A possible compromise is ...",
                "5. I'm happy to ...",
            ],
            "goal_examples": ["In my view, ...", "I see your point, but ...", "Because ..."],
        },
        {
            "lesson_key": "lesson-02-supporting-with-reasons",
            "slug": "supporting-with-reasons",
            "title": "Supporting With Reasons",
            "conversation_situation": "supporting_argument_with_reasons",
            "conversation_goal": "Support your argument with two structured reasons and keep it concise.",
            "grammar_summary": "Use One reason is... / Another reason is... / Also... to support an argument clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu lagi meyakinkan tim. Kamu kasih dua alasan yang terstruktur dan tetap ringkas.",
            "dialogue": [
                ("Alex", "Do we really need to invest time in automated tests?"),
                ("Mina", "I think we should. One reason is it reduces bugs in production."),
                ("Alex", "Okay. What's another reason?"),
                ("Mina", "Another reason is it speeds up releases because we can deploy with more confidence."),
                ("Alex", "But writing tests takes time."),
                ("Mina", "That's true, but it saves time later when we avoid firefighting."),
                ("Alex", "Fair point."),
                ("Mina", "We can start small and focus on critical flows."),
            ],
            "translations": [
                ("Alex", "Do we really need to invest time in automated tests?", "Kita beneran perlu investasi waktu buat automated tests?"),
                ("Mina", "I think we should. One reason is it reduces bugs in production.", "Menurutku perlu. Salah satu alasannya itu mengurangi bug di production."),
                ("Alex", "Okay. What's another reason?", "Oke. Alasan lainnya apa?"),
                ("Mina", "Another reason is it speeds up releases because we can deploy with more confidence.", "Alasan lain, itu mempercepat release karena kita bisa deploy dengan lebih yakin."),
                ("Alex", "But writing tests takes time.", "Tapi nulis test itu makan waktu."),
                ("Mina", "That's true, but it saves time later when we avoid firefighting.", "Bener, tapi itu hemat waktu nanti karena kita nggak terus-terusan beresin kebakaran."),
                ("Alex", "Fair point.", "Masuk akal."),
                ("Mina", "We can start small and focus on critical flows.", "Kita bisa mulai kecil dan fokus ke alur yang paling penting."),
            ],
            "useful_phrases": [
                {
                    "phrase": "One reason is it reduces bugs in production.",
                    "meaning_id": "Salah satu alasannya itu mengurangi bug di production.",
                    "usage_note": "A clear structured reason sentence.",
                    "common_mistake": 'Do not say "One reason reduce"; use is + it reduces.',
                },
                {
                    "phrase": "Another reason is it speeds up releases.",
                    "meaning_id": "Alasan lain, itu mempercepat release.",
                    "usage_note": "Add a second reason clearly.",
                    "common_mistake": 'Do not say "Another reason are"; use is.',
                },
                {
                    "phrase": "That's true, but...",
                    "meaning_id": "Bener, tapi...",
                    "usage_note": "A polite way to acknowledge a concern.",
                    "common_mistake": 'Do not ignore the concern; acknowledge it first.',
                },
                {
                    "phrase": "It saves time later.",
                    "meaning_id": "Itu hemat waktu nanti.",
                    "usage_note": "A simple long-term benefit.",
                    "common_mistake": 'Do not say "save times"; time is uncountable.',
                },
                {
                    "phrase": "We can start small and focus on critical flows.",
                    "meaning_id": "Kita bisa mulai kecil dan fokus ke alur paling penting.",
                    "usage_note": "A practical next step.",
                    "common_mistake": 'Do not propose a huge plan at once; start small is realistic.',
                },
            ],
            "grammar_md": [
                ("Structured reasons", ["One reason is it reduces bugs.", "Another reason is it saves time."]),
                ("Acknowledge + but", ["That's true, but it helps in the long run.", "That's true, but we can start small."]),
            ],
            "pronunciation": [
                ("production", "pruh-DUK-shun."),
                ("confidence", "KON-fi-dens."),
                ("critical", "KRIT-i-kul."),
            ],
            "response_prompts": [
                {
                    "prompt": "Give a first reason.",
                    "target_response": "One reason is it reduces bugs in production.",
                    "acceptable_variations": [
                        "One reason is it reduces bugs in production.",
                        "One reason is it saves time later.",
                    ],
                },
                {
                    "prompt": "Give a second reason.",
                    "target_response": "Another reason is it speeds up releases.",
                    "acceptable_variations": ["Another reason is it speeds up releases.", "Another reason is it improves quality."],
                },
                {
                    "prompt": "Acknowledge a concern and respond.",
                    "target_response": "That's true, but it saves time later.",
                    "acceptable_variations": [
                        "That's true, but it saves time later.",
                        "That's true, but we can start small.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "one_reason_structure",
                    "type": "multiple_choice",
                    "prompt": "Which sentence has a correct reason structure?",
                    "options": ["One reason is it reduces bugs.", "One reason reduce bugs.", "One reason are reduce bugs."],
                    "correct_answer": "One reason is it reduces bugs.",
                },
                {
                    "key": "another_reason_structure",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["Another reason is it saves time.", "Another reason are it saves time.", "Another reason saving time."],
                    "correct_answer": "Another reason is it saves time.",
                },
                {
                    "key": "thats_true_usage",
                    "type": "multiple_choice",
                    "prompt": "Which phrase acknowledges a concern politely?",
                    "options": ["That's true, but...", "No, you're wrong.", "Stop."],
                    "correct_answer": "That's true, but...",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_argument_reasons",
                "opening_line": "Convince me with reasons.",
                "learner_goal": "Support your argument with two reasons and respond to a concern.",
                "turns": [
                    {
                        "coach": "Why should we invest in automated tests?",
                        "hint": "Mulai dengan One reason is...",
                        "sample_answer": "One reason is it reduces bugs in production.",
                        "focus": "Reason 1",
                        "expected_keywords": ["one reason", "reduces"],
                    },
                    {
                        "coach": "What's another reason?",
                        "hint": "Gunakan Another reason is...",
                        "sample_answer": "Another reason is it speeds up releases because we can deploy with more confidence.",
                        "focus": "Reason 2",
                        "expected_keywords": ["another reason", "because"],
                    },
                    {
                        "coach": "But writing tests takes time.",
                        "hint": "Acknowledge + but + solusi singkat.",
                        "sample_answer": "That's true, but we can start small and it saves time later.",
                        "focus": "Address concern",
                        "expected_keywords": ["that's true", "but"],
                    },
                ],
                "target_phrases": ["One reason is ...", "Another reason is ...", "That's true, but ..."],
            },
            "reading_support": "To support an argument, give structured reasons. Keep them short and clear: one reason, another reason, and a practical response to concerns.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. I think we should ...",
                "2. One reason is ...",
                "3. Another reason is ...",
                "4. That's true, but ...",
                "5. In the long run, ...",
                "6. We can start small by ...",
            ],
            "goal_examples": ["One reason is ...", "Another reason is ...", "That's true, but ..."],
        },
        {
            "lesson_key": "lesson-03-using-examples",
            "slug": "using-examples",
            "title": "Using Examples",
            "conversation_situation": "supporting_argument_with_examples",
            "conversation_goal": "Support your point with a clear example and connect it back to your argument.",
            "grammar_summary": "Use for example / for instance / such as to support an argument with evidence.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu lagi diskusi ide. Kamu kasih contoh yang jelas supaya argumen kamu lebih kuat.",
            "dialogue": [
                ("Jordan", "Why do you think onboarding should be more structured?"),
                ("Mina", "Because new hires need clarity. For example, last quarter we had three new joiners who felt lost in week one."),
                ("Jordan", "What happened exactly?"),
                ("Mina", "They didn't know which tools to use, so they kept asking in multiple channels."),
                ("Jordan", "Okay, that's a good point."),
                ("Mina", "For instance, a simple checklist would reduce repeated questions."),
                ("Jordan", "So your suggestion is a checklist plus a buddy system?"),
                ("Mina", "Yes, such as pairing each new hire with one mentor for two weeks."),
            ],
            "translations": [
                ("Jordan", "Why do you think onboarding should be more structured?", "Kenapa kamu pikir onboarding harus lebih terstruktur?"),
                ("Mina", "Because new hires need clarity. For example, last quarter we had three new joiners who felt lost in week one.", "Karena karyawan baru butuh kejelasan. Contohnya, kuartal lalu ada tiga orang baru yang merasa bingung di minggu pertama."),
                ("Jordan", "What happened exactly?", "Apa yang terjadi tepatnya?"),
                ("Mina", "They didn't know which tools to use, so they kept asking in multiple channels.", "Mereka nggak tahu tool mana yang dipakai, jadi mereka terus tanya di banyak channel."),
                ("Jordan", "Okay, that's a good point.", "Oke, itu poin yang bagus."),
                ("Mina", "For instance, a simple checklist would reduce repeated questions.", "Misalnya, checklist sederhana bisa mengurangi pertanyaan yang berulang."),
                ("Jordan", "So your suggestion is a checklist plus a buddy system?", "Jadi saran kamu checklist plus buddy system?"),
                ("Mina", "Yes, such as pairing each new hire with one mentor for two weeks.", "Iya, misalnya pasangkan setiap orang baru dengan satu mentor selama dua minggu."),
            ],
            "useful_phrases": [
                {
                    "phrase": "For example, last quarter we had three new joiners who felt lost.",
                    "meaning_id": "Contohnya, kuartal lalu ada tiga orang baru yang merasa bingung.",
                    "usage_note": "For example introduces a concrete case.",
                    "common_mistake": 'Do not say "for example is"; use for example, + sentence.',
                },
                {
                    "phrase": "They didn't know which tools to use.",
                    "meaning_id": "Mereka nggak tahu tool mana yang dipakai.",
                    "usage_note": "A clear description of the example.",
                    "common_mistake": 'Do not say "didn\'t knew"; use didn\'t know.',
                },
                {
                    "phrase": "So they kept asking in multiple channels.",
                    "meaning_id": "Jadi mereka terus tanya di banyak channel.",
                    "usage_note": "Connect the example to the impact.",
                    "common_mistake": 'Do not say "keep asking" for past; use kept.',
                },
                {
                    "phrase": "For instance, a simple checklist would help.",
                    "meaning_id": "Misalnya, checklist sederhana akan membantu.",
                    "usage_note": "For instance is similar to for example.",
                    "common_mistake": 'Do not mix for instance and for example in every sentence; use one at a time.',
                },
                {
                    "phrase": "Such as pairing each new hire with one mentor.",
                    "meaning_id": "Misalnya memasangkan setiap orang baru dengan satu mentor.",
                    "usage_note": "Such as introduces specific items.",
                    "common_mistake": 'Do not say "such like"; use such as.',
                },
            ],
            "grammar_md": [
                ("For example / for instance", ["For example, we had three new joiners last quarter.", "For instance, a checklist would reduce questions."]),
                ("Such as + noun/verb-ing", ["Such as pairing each new hire with a mentor.", "Such as adding a short training session."]),
            ],
            "pronunciation": [
                ("example", "ig-ZAM-pul."),
                ("instance", "IN-stens."),
                ("mentor", "MEN-tor."),
            ],
            "response_prompts": [
                {
                    "prompt": "Introduce an example.",
                    "target_response": "For example, last quarter we had three new joiners who felt lost.",
                    "acceptable_variations": [
                        "For example, last quarter we had three new joiners who felt lost.",
                        "For example, we saw the same issue last month.",
                    ],
                },
                {
                    "prompt": "Describe the impact with so.",
                    "target_response": "So they kept asking in multiple channels.",
                    "acceptable_variations": ["So they kept asking in multiple channels.", "So it slowed the team down."],
                },
                {
                    "prompt": "Give a specific suggestion with such as.",
                    "target_response": "Such as pairing each new hire with one mentor.",
                    "acceptable_variations": [
                        "Such as pairing each new hire with one mentor.",
                        "Such as creating a simple checklist.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "for_example_use",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces an example?",
                    "options": ["For example, ...", "However, ...", "Therefore, ..."],
                    "correct_answer": "For example, ...",
                },
                {
                    "key": "such_as_use",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces specific items?",
                    "options": ["such as", "because of", "even though"],
                    "correct_answer": "such as",
                },
                {
                    "key": "didnt_know",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct past sentence.",
                    "options": ["They didn't know.", "They didn't knew.", "They don't knew."],
                    "correct_answer": "They didn't know.",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_argument_examples",
                "opening_line": "Convince me with an example.",
                "learner_goal": "Use an example to support your point and connect it to a clear suggestion.",
                "turns": [
                    {
                        "coach": "Why should onboarding be more structured?",
                        "hint": "Because... + For example...",
                        "sample_answer": "Because new hires need clarity. For example, last quarter three new joiners felt lost in week one.",
                        "focus": "Use an example",
                        "expected_keywords": ["because", "for example"],
                    },
                    {
                        "coach": "What's the impact?",
                        "hint": "Gunakan so untuk dampak.",
                        "sample_answer": "So they kept asking in multiple channels and it slowed the team down.",
                        "focus": "Explain impact",
                        "expected_keywords": ["so", "kept"],
                    },
                    {
                        "coach": "Give a specific suggestion.",
                        "hint": "Gunakan such as...",
                        "sample_answer": "Such as pairing each new hire with one mentor for two weeks.",
                        "focus": "Give specific suggestion",
                        "expected_keywords": ["such as", "mentor"],
                    },
                ],
                "target_phrases": ["For example, ...", "..., so ...", "Such as ..."],
            },
            "reading_support": "Examples make arguments stronger. Give one concrete case, explain the impact, then connect it to a specific suggestion.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. I think we should ...",
                "2. Because ...",
                "3. For example, ...",
                "4. So ...",
                "5. For instance, ...",
                "6. Such as ...",
            ],
            "goal_examples": ["For example, ...", "For instance, ...", "Such as ..."],
        },
        {
            "lesson_key": "lesson-04-responding-to-counterpoints",
            "slug": "responding-to-counterpoints",
            "title": "Responding to Counterpoints",
            "conversation_situation": "responding_to_counterpoints",
            "conversation_goal": "Respond to a counterpoint politely, show you understand it, and reinforce your position.",
            "grammar_summary": "Use That's a fair point / I understand the concern / However... to respond professionally.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu debat sehat. Lawan bicara kasih counterpoint, kamu respon sopan dan tetap mempertahankan argumenmu.",
            "dialogue": [
                ("Alex", "I like your idea, but I'm worried it will increase costs."),
                ("Mina", "That's a fair point. However, the long-term savings could be significant."),
                ("Alex", "Can you explain why?"),
                ("Mina", "If we reduce rework, we save engineering time and customer support time."),
                ("Alex", "But the upfront investment is still high."),
                ("Mina", "I understand the concern, but we can phase it in and measure results after one month."),
                ("Alex", "Okay, that feels more manageable."),
                ("Mina", "Great. Let's define success metrics first."),
            ],
            "translations": [
                ("Alex", "I like your idea, but I'm worried it will increase costs.", "Aku suka idemu, tapi aku khawatir biayanya naik."),
                ("Mina", "That's a fair point. However, the long-term savings could be significant.", "Itu poin yang adil. Tapi, penghematan jangka panjang bisa besar."),
                ("Alex", "Can you explain why?", "Bisa jelasin kenapa?"),
                ("Mina", "If we reduce rework, we save engineering time and customer support time.", "Kalau kita mengurangi rework, kita hemat waktu engineering dan customer support."),
                ("Alex", "But the upfront investment is still high.", "Tapi investasi awalnya tetap tinggi."),
                ("Mina", "I understand the concern, but we can phase it in and measure results after one month.", "Aku paham kekhawatirannya, tapi kita bisa jalanin bertahap dan ukur hasilnya setelah satu bulan."),
                ("Alex", "Okay, that feels more manageable.", "Oke, itu terasa lebih masuk akal untuk dijalankan."),
                ("Mina", "Great. Let's define success metrics first.", "Oke. Yuk tentukan metrik sukses dulu."),
            ],
            "useful_phrases": [
                {
                    "phrase": "That's a fair point.",
                    "meaning_id": "Itu poin yang adil/masuk akal.",
                    "usage_note": "A respectful way to acknowledge a counterpoint.",
                    "common_mistake": 'Do not sound defensive; start with fair point.',
                },
                {
                    "phrase": "However, the long-term savings could be significant.",
                    "meaning_id": "Tapi, penghematan jangka panjang bisa besar.",
                    "usage_note": "However is a professional contrast word.",
                    "common_mistake": 'Do not use however without a full sentence; keep it clear.',
                },
                {
                    "phrase": "I understand the concern, but...",
                    "meaning_id": "Aku paham kekhawatirannya, tapi...",
                    "usage_note": "Show empathy before responding.",
                    "common_mistake": 'Do not say "I understand you" for this; say the concern.',
                },
                {
                    "phrase": "We can phase it in.",
                    "meaning_id": "Kita bisa jalanin bertahap.",
                    "usage_note": "A practical way to reduce risk.",
                    "common_mistake": 'Do not say "phase in it"; keep word order we can phase it in.',
                },
                {
                    "phrase": "Let's define success metrics first.",
                    "meaning_id": "Yuk tentukan metrik sukses dulu.",
                    "usage_note": "A strong next step after discussion.",
                    "common_mistake": 'Do not say "define metrics firstly"; use first.',
                },
            ],
            "grammar_md": [
                ("Acknowledge + however", ["That's a fair point. However, we can reduce risk.", "That's a fair point. However, the benefit is long-term."]),
                ("I understand the concern, but...", ["I understand the concern, but we can phase it in.", "I understand the concern, but we can start with a pilot."]),
            ],
            "pronunciation": [
                ("however", "how-EV-er."),
                ("significant", "sig-NIF-i-kunt."),
                ("metrics", "MET-riks."),
            ],
            "response_prompts": [
                {
                    "prompt": "Acknowledge a counterpoint politely.",
                    "target_response": "That's a fair point.",
                    "acceptable_variations": ["That's a fair point.", "That's a good point."],
                },
                {
                    "prompt": "Respond with however + benefit.",
                    "target_response": "However, the long-term savings could be significant.",
                    "acceptable_variations": [
                        "However, the long-term savings could be significant.",
                        "However, the long-term benefit is clear.",
                    ],
                },
                {
                    "prompt": "Offer a mitigation plan (phase it in).",
                    "target_response": "I understand the concern, but we can phase it in.",
                    "acceptable_variations": [
                        "I understand the concern, but we can phase it in.",
                        "I understand the concern, but we can start with a pilot.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "fair_point_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "That\'s a fair point" mean?',
                    "options": ["itu poin yang masuk akal", "itu poin yang salah", "itu poin yang lucu"],
                    "correct_answer": "itu poin yang masuk akal",
                },
                {
                    "key": "however_function",
                    "type": "multiple_choice",
                    "prompt": 'What does "however" usually signal?',
                    "options": ["kontras", "urutan", "pertanyaan"],
                    "correct_answer": "kontras",
                },
                {
                    "key": "phase_it_in_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "phase it in" mean?',
                    "options": ["jalankan bertahap", "batalkan total", "ulang dari awal"],
                    "correct_answer": "jalankan bertahap",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_argument_counterpoints",
                "opening_line": "I have a concern about your idea.",
                "learner_goal": "Acknowledge a counterpoint, respond professionally, and propose a mitigation plan.",
                "turns": [
                    {
                        "coach": "I like your idea, but I'm worried it will increase costs.",
                        "hint": "Mulai dengan That's a fair point / I understand the concern.",
                        "sample_answer": "That's a fair point. However, the long-term savings could be significant.",
                        "focus": "Acknowledge + respond",
                        "expected_keywords": ["fair point", "however"],
                    },
                    {
                        "coach": "The upfront investment is still high.",
                        "hint": "Tawarkan mitigasi: phase it in / pilot.",
                        "sample_answer": "I understand the concern, but we can phase it in and measure results.",
                        "focus": "Mitigation plan",
                        "expected_keywords": ["phase", "measure"],
                    },
                    {
                        "coach": "Great. What's the next step?",
                        "hint": "Usul langkah berikutnya.",
                        "sample_answer": "Let's define success metrics first and run a small pilot.",
                        "focus": "Next steps",
                        "expected_keywords": ["metrics", "pilot"],
                    },
                ],
                "target_phrases": ["That's a fair point.", "However, ...", "I understand the concern, but ..."],
            },
            "reading_support": "Counterpoints are normal in professional discussions. A good response acknowledges the concern, explains your reasoning, and offers a practical way to reduce risk.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. That's a fair point.",
                "2. However, ...",
                "3. I understand the concern, but ...",
                "4. We can phase it in.",
                "5. We'll measure results after ...",
                "6. Let's define success metrics first.",
            ],
            "goal_examples": ["That's a fair point.", "I understand the concern, but ...", "However, ..."],
        },
        {
            "lesson_key": "lesson-05-clear-argument-mission",
            "slug": "clear-argument-mission",
            "title": "Clear Argument Mission",
            "conversation_situation": "mission_clear_argument",
            "conversation_goal": "Complete a mini argument: state your position, give reasons and an example, respond to a counterpoint, and agree on next steps.",
            "grammar_summary": "Combine: In my view... / One reason is... / For example... / That's a fair point. However... / Let's...",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Misi: kamu usul perubahan proses kerja. Kamu jelasin posisi, dua alasan, satu contoh, respon counterpoint, lalu sepakat next step.",
            "dialogue": [
                ("Alex", "Should we change our weekly meeting format?"),
                ("Mina", "In my view, we should move routine updates to a written summary."),
                ("Alex", "Why?"),
                ("Mina", "One reason is it saves time. Another reason is it improves focus."),
                ("Alex", "Can you give an example?"),
                ("Mina", "For example, last month we spent 30 minutes repeating status updates."),
                ("Alex", "But we might lose real-time discussion."),
                ("Mina", "That's a fair point. However, we can keep one monthly live session for deeper discussion."),
            ],
            "translations": [
                ("Alex", "Should we change our weekly meeting format?", "Kita perlu ubah format meeting mingguan nggak?"),
                ("Mina", "In my view, we should move routine updates to a written summary.", "Menurutku, update rutin sebaiknya dipindah ke ringkasan tertulis."),
                ("Alex", "Why?", "Kenapa?"),
                ("Mina", "One reason is it saves time. Another reason is it improves focus.", "Salah satu alasannya hemat waktu. Alasan lain, itu bikin fokus lebih bagus."),
                ("Alex", "Can you give an example?", "Bisa kasih contoh?"),
                ("Mina", "For example, last month we spent 30 minutes repeating status updates.", "Contohnya, bulan lalu kita habis 30 menit cuma ngulang status update."),
                ("Alex", "But we might lose real-time discussion.", "Tapi kita mungkin kehilangan diskusi real-time."),
                ("Mina", "That's a fair point. However, we can keep one monthly live session for deeper discussion.", "Itu poin yang adil. Tapi, kita bisa tetap adain satu sesi live bulanan untuk diskusi lebih dalam."),
            ],
            "useful_phrases": [
                {
                    "phrase": "In my view, we should move routine updates to a written summary.",
                    "meaning_id": "Menurutku, update rutin sebaiknya dipindah ke ringkasan tertulis.",
                    "usage_note": "Clear position + suggestion.",
                    "common_mistake": 'Do not say "In my view we must"; should is softer.',
                },
                {
                    "phrase": "One reason is it saves time.",
                    "meaning_id": "Salah satu alasannya hemat waktu.",
                    "usage_note": "Reason structure.",
                    "common_mistake": 'Do not drop is.',
                },
                {
                    "phrase": "For example, last month we spent 30 minutes repeating updates.",
                    "meaning_id": "Contohnya, bulan lalu kita habis 30 menit ngulang update.",
                    "usage_note": "Example with simple data.",
                    "common_mistake": "Avoid too many numbers; one is enough.",
                },
                {
                    "phrase": "That's a fair point. However, ...",
                    "meaning_id": "Itu poin yang adil. Tapi, ...",
                    "usage_note": "Polite response to a counterpoint.",
                    "common_mistake": 'Do not respond emotionally; keep it calm and professional.',
                },
                {
                    "phrase": "Let's run a one-month trial and review the results.",
                    "meaning_id": "Yuk coba satu bulan lalu review hasilnya.",
                    "usage_note": "A concrete next step.",
                    "common_mistake": 'Do not say "trialing"; use run a trial.',
                },
            ],
            "grammar_md": [
                (
                    "Clear argument structure",
                    [
                        "In my view, ...",
                        "One reason is ... Another reason is ...",
                        "For example, ...",
                        "That's a fair point. However, ...",
                        "Let's ...",
                    ],
                ),
            ],
            "pronunciation": [
                ("routine", "roo-TEEN."),
                ("summary", "SUM-uh-ree."),
                ("trial", "TRY-ul."),
            ],
            "response_prompts": [
                {
                    "prompt": "State position (In my view...).",
                    "target_response": "In my view, we should move routine updates to a written summary.",
                    "acceptable_variations": [
                        "In my view, we should move routine updates to a written summary.",
                        "In my view, we should change the meeting format.",
                    ],
                },
                {
                    "prompt": "Give two reasons.",
                    "target_response": "One reason is it saves time. Another reason is it improves focus.",
                    "acceptable_variations": [
                        "One reason is it saves time. Another reason is it improves focus.",
                        "One reason is it reduces meetings. Another reason is it improves clarity.",
                    ],
                },
                {
                    "prompt": "Respond to counterpoint politely.",
                    "target_response": "That's a fair point. However, we can keep one monthly live session.",
                    "acceptable_variations": [
                        "That's a fair point. However, we can keep one monthly live session.",
                        "That's a fair point. However, we can schedule a weekly Q&A.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "argument_structure",
                    "type": "multiple_choice",
                    "prompt": "Which order is a clear argument?",
                    "options": [
                        "Position -> reasons -> example -> counterpoint response -> next steps",
                        "Greeting -> goodbye",
                        "Food -> color -> price",
                    ],
                    "correct_answer": "Position -> reasons -> example -> counterpoint response -> next steps",
                },
                {
                    "key": "for_example_role",
                    "type": "multiple_choice",
                    "prompt": 'What does "for example" do?',
                    "options": ["memberi contoh", "menolak ide", "mengganti topik"],
                    "correct_answer": "memberi contoh",
                },
                {
                    "key": "however_role",
                    "type": "multiple_choice",
                    "prompt": 'What does "however" signal?',
                    "options": ["kontras", "urutan waktu", "alasan"],
                    "correct_answer": "kontras",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_argument_mission",
                "opening_line": "Let's discuss changing our meeting format.",
                "learner_goal": "Make a clear argument with reasons and an example, respond to a counterpoint, and propose next steps.",
                "turns": [
                    {
                        "coach": "State your position.",
                        "hint": "Mulai dengan In my view...",
                        "sample_answer": "In my view, we should move routine updates to a written summary.",
                        "focus": "Position",
                        "expected_keywords": ["in my view", "should"],
                    },
                    {
                        "coach": "Support it with two reasons.",
                        "hint": "One reason is... Another reason is...",
                        "sample_answer": "One reason is it saves time. Another reason is it improves focus.",
                        "focus": "Reasons",
                        "expected_keywords": ["one reason", "another reason"],
                    },
                    {
                        "coach": "Give an example, then respond to my concern and propose next steps.",
                        "hint": "For example... That's a fair point. However... Let's...",
                        "sample_answer": "For example, last month we spent 30 minutes repeating updates. That's a fair point. However, we can keep one monthly live session. Let's run a one-month trial and review the results.",
                        "focus": "Example + counterpoint + next steps",
                        "expected_keywords": ["for example", "fair point", "however", "trial"],
                    },
                ],
                "target_phrases": ["In my view, ...", "One reason is ...", "That's a fair point. However, ..."],
            },
            "reading_support": "A strong argument is structured. Start with your position, add reasons, support with an example, respond to counterpoints politely, and end with clear next steps.",
            "writing_support_lines": [
                "Write your mission (8 lines):",
                "1. In my view, ...",
                "2. One reason is ...",
                "3. Another reason is ...",
                "4. For example, ...",
                "5. That's a fair point.",
                "6. However, ...",
                "7. Let's run a ... trial.",
                "8. We'll review the results after ...",
            ],
            "goal_examples": ["In my view, ...", "One reason is ...", "For example, ..."],
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

