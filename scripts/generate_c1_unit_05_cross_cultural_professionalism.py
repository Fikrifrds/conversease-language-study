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
            "- Tone: respectful, warm, professional",
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

        Read it again and underline the tact phrases (would you mind, if it's okay, I don't mean to..., just to make sure...).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "C1"
    root = Path("content/curriculum/english/C1")
    units_root = root / "units"
    unit_key = "unit-05-cross-cultural-professionalism"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-05-cross-cultural-professionalism
            level_code: C1
            title: Cross-cultural Professionalism
            main_conversation_outcome: Communicate across cultures with tact, clarity, and professionalism.
            status: in_production
            lessons:
              - lesson-01-reading-context
              - lesson-02-asking-tactful-questions
              - lesson-03-explaining-local-norms
              - lesson-04-repairing-misunderstanding
              - lesson-05-cross-cultural-mission
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
            "lesson_key": "lesson-01-reading-context",
            "slug": "reading-context",
            "title": "Reading Context",
            "conversation_situation": "reading_cross_cultural_context",
            "conversation_goal": "Read context carefully by noticing tone, hierarchy, and implied expectations before responding.",
            "grammar_summary": "Use It may be worth considering... / My sense is that... / Before we decide, can we clarify... to read context.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu dapat pesan yang agak indirect dari stakeholder lintas budaya. Kamu perlu baca konteksnya dulu sebelum jawab.",
            "dialogue": [
                ("Jordan", "The client said the timeline is 'ambitious'. What do you think that means?"),
                ("Mina", "My sense is that they're signaling concern without saying no directly."),
                ("Jordan", "So how should we respond?"),
                ("Mina", "Before we decide, can we clarify what their priority is—speed or risk reduction?"),
                ("Jordan", "Good point."),
                ("Mina", "It may be worth considering a phased plan to show flexibility."),
                ("Jordan", "And tone-wise?"),
                ("Mina", "We should stay respectful and avoid sounding defensive."),
            ],
            "translations": [
                ("Jordan", "The client said the timeline is 'ambitious'. What do you think that means?", "Klien bilang timeline-nya 'ambitious'. Menurut kamu maksudnya apa?"),
                ("Mina", "My sense is that they're signaling concern without saying no directly.", "Feeling aku, mereka ngasih sinyal concern tanpa bilang tidak secara langsung."),
                ("Jordan", "So how should we respond?", "Jadi harus jawab gimana?"),
                ("Mina", "Before we decide, can we clarify what their priority is—speed or risk reduction?", "Sebelum putuskan, bisa kita klarifikasi prioritasnya apa—cepat atau mengurangi risiko?"),
                ("Jordan", "Good point.", "Oke."),
                ("Mina", "It may be worth considering a phased plan to show flexibility.", "Mungkin perlu dipertimbangkan rencana bertahap supaya terlihat fleksibel."),
                ("Jordan", "And tone-wise?", "Kalau soal tone?"),
                ("Mina", "We should stay respectful and avoid sounding defensive.", "Kita harus tetap respectful dan jangan terdengar defensif."),
            ],
            "useful_phrases": [
                {
                    "phrase": "My sense is that they're signaling concern without saying no directly.",
                    "meaning_id": "Feeling aku, mereka ngasih sinyal concern tanpa bilang tidak langsung.",
                    "usage_note": "Interpret implied meaning carefully.",
                    "common_mistake": "Do not assume hostility; interpret cautiously.",
                },
                {
                    "phrase": "Before we decide, can we clarify what their priority is—speed or risk reduction?",
                    "meaning_id": "Sebelum putuskan, bisa kita klarifikasi prioritasnya apa—cepat atau mengurangi risiko?",
                    "usage_note": "Clarify priorities before replying.",
                    "common_mistake": "Do not reply immediately; clarify intent first.",
                },
                {
                    "phrase": "It may be worth considering a phased plan.",
                    "meaning_id": "Mungkin perlu dipertimbangkan rencana bertahap.",
                    "usage_note": "A tactful suggestion.",
                    "common_mistake": "Do not sound absolute; use may be worth considering.",
                },
                {
                    "phrase": "We should stay respectful and avoid sounding defensive.",
                    "meaning_id": "Kita harus tetap respectful dan jangan terdengar defensif.",
                    "usage_note": "Tone management across cultures.",
                    "common_mistake": "Do not over-explain; keep it calm.",
                },
                {
                    "phrase": "What do you think that means in context?",
                    "meaning_id": "Menurut kamu maksudnya apa dalam konteksnya?",
                    "usage_note": "Invite interpretation explicitly.",
                    "common_mistake": "Do not treat words literally only; ask about context.",
                },
            ],
            "grammar_md": [
                ("Context reading", ["My sense is that ...", "It may be worth considering ..."]),
                ("Clarifying", ["Before we decide, can we clarify ...?", "What is their priority: X or Y?"]),
            ],
            "pronunciation": [
                ("ambitious", "am-BISH-us."),
                ("hierarchy", "HY-uh-rar-kee."),
                ("defensive", "di-FEN-siv."),
            ],
            "response_prompts": [
                {
                    "prompt": "Interpret indirect feedback cautiously.",
                    "target_response": "My sense is that they're signaling concern without saying no directly.",
                    "acceptable_variations": [
                        "My sense is that they're signaling concern without saying no directly.",
                        "My sense is that they want us to slow down without rejecting it.",
                    ],
                },
                {
                    "prompt": "Ask to clarify priority before responding.",
                    "target_response": "Before we decide, can we clarify what their priority is—speed or risk reduction?",
                    "acceptable_variations": [
                        "Before we decide, can we clarify what their priority is—speed or risk reduction?",
                        "Before we decide, can we clarify what matters most to them?",
                    ],
                },
                {
                    "prompt": "Suggest a phased plan tactfully.",
                    "target_response": "It may be worth considering a phased plan to show flexibility.",
                    "acceptable_variations": [
                        "It may be worth considering a phased plan to show flexibility.",
                        "It may be worth considering a phased approach to reduce risk.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "my_sense",
                    "type": "multiple_choice",
                    "prompt": "Which phrase is useful for interpreting implied meaning cautiously?",
                    "options": ["My sense is that ...", "They are angry.", "No context needed."],
                    "correct_answer": "My sense is that ...",
                },
                {
                    "key": "clarify_priority",
                    "type": "multiple_choice",
                    "prompt": "Which phrase clarifies priorities before responding?",
                    "options": ["Before we decide, can we clarify ...?", "Reply now.", "Ignore them."],
                    "correct_answer": "Before we decide, can we clarify ...?",
                },
                {
                    "key": "phased_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "phased plan" mean?',
                    "options": ["rencana bertahap", "rencana dadakan", "rencana rahasia"],
                    "correct_answer": "rencana bertahap",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_reading_context",
                "opening_line": "The client says the timeline is 'ambitious'.",
                "learner_goal": "Interpret implied meaning, manage tone, and clarify priorities before replying.",
                "turns": [
                    {
                        "coach": "The client says the timeline is 'ambitious'. What does that mean?",
                        "hint": "Interpret cautiously: My sense is that...",
                        "sample_answer": "My sense is that they're signaling concern without saying no directly.",
                        "focus": "Interpretation",
                        "expected_keywords": ["my sense", "signaling", "concern"],
                    },
                    {
                        "coach": "What should we do before replying?",
                        "hint": "Ask to clarify priority.",
                        "sample_answer": "Before we decide, can we clarify what their priority is—speed or risk reduction?",
                        "focus": "Clarify",
                        "expected_keywords": ["before we decide", "clarify", "priority"],
                    },
                    {
                        "coach": "Offer a tactful option and set the right tone.",
                        "hint": "May be worth considering... stay respectful...",
                        "sample_answer": "It may be worth considering a phased plan to show flexibility. We should stay respectful and avoid sounding defensive.",
                        "focus": "Option + tone",
                        "expected_keywords": ["worth considering", "phased", "respectful"],
                    },
                ],
                "target_phrases": ["My sense is that ...", "Before we decide, can we clarify ...?", "It may be worth considering ..."],
            },
            "reading_support": "Cross-cultural context often shows up as indirect language. Read tone, implied meaning, and priorities before replying. Clarify what matters most, then respond with flexible options and a respectful tone.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. My sense is that ...",
                "2. They may be signaling ...",
                "3. Before we decide, can we clarify ...?",
                "4. What is the priority: ... or ...?",
                "5. It may be worth considering ...",
                "6. A phased plan could ...",
                "7. We should stay respectful ...",
                "8. And avoid sounding ...",
                "9. Next steps are ...",
                "10. Does that sound reasonable?",
            ],
            "goal_examples": ["My sense is that ...", "Before we decide, can we clarify ...?", "It may be worth considering ..."],
        },
        {
            "lesson_key": "lesson-02-asking-tactful-questions",
            "slug": "asking-tactful-questions",
            "title": "Asking Tactful Questions",
            "conversation_situation": "tactful_questions",
            "conversation_goal": "Ask tactful questions to clarify expectations, boundaries, and sensitive topics without causing discomfort.",
            "grammar_summary": "Use Would you mind if I ask... / If it's okay, could you clarify... / Just to make sure I understand... to ask tactfully.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu perlu tanya hal sensitif ke klien/stakeholder. Kamu harus menjaga sopan santun dan tetap jelas.",
            "dialogue": [
                ("Jordan", "The client seems uncomfortable with direct feedback."),
                ("Mina", "Would you mind if I ask how they prefer to receive feedback?"),
                ("Jordan", "That's a good question."),
                ("Mina", "If it's okay, could you clarify whether they want feedback in writing or in a call?"),
                ("Jordan", "Probably in a call."),
                ("Mina", "Just to make sure I understand, should we share concerns privately first?"),
                ("Jordan", "Yes, that would be better."),
                ("Mina", "Great. We'll adjust our approach accordingly."),
            ],
            "translations": [
                ("Jordan", "The client seems uncomfortable with direct feedback.", "Klien kelihatan nggak nyaman dengan feedback yang langsung."),
                ("Mina", "Would you mind if I ask how they prefer to receive feedback?", "Boleh aku tanya mereka lebih nyaman menerima feedback seperti apa?"),
                ("Jordan", "That's a good question.", "Pertanyaan bagus."),
                ("Mina", "If it's okay, could you clarify whether they want feedback in writing or in a call?", "Kalau boleh, bisa klarifikasi mereka maunya feedback tertulis atau via call?"),
                ("Jordan", "Probably in a call.", "Mungkin via call."),
                ("Mina", "Just to make sure I understand, should we share concerns privately first?", "Biar aku paham, sebaiknya kita share concern dulu secara private?"),
                ("Jordan", "Yes, that would be better.", "Iya, lebih baik."),
                ("Mina", "Great. We'll adjust our approach accordingly.", "Oke. Kita sesuaikan approach-nya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Would you mind if I ask how you prefer to receive feedback?",
                    "meaning_id": "Boleh aku tanya kamu lebih nyaman menerima feedback seperti apa?",
                    "usage_note": "A tactful opener for sensitive questions.",
                    "common_mistake": "Do not ask bluntly; soften with would you mind.",
                },
                {
                    "phrase": "If it's okay, could you clarify whether you want feedback in writing or in a call?",
                    "meaning_id": "Kalau boleh, bisa klarifikasi maunya feedback tertulis atau via call?",
                    "usage_note": "A polite clarification question.",
                    "common_mistake": "Do not assume; offer options.",
                },
                {
                    "phrase": "Just to make sure I understand, should we share concerns privately first?",
                    "meaning_id": "Biar aku paham, sebaiknya kita share concern dulu secara private?",
                    "usage_note": "A respectful check for expectations.",
                    "common_mistake": "Do not imply blame; keep it as understanding check.",
                },
                {
                    "phrase": "We'll adjust our approach accordingly.",
                    "meaning_id": "Kita sesuaikan approach-nya.",
                    "usage_note": "Signal respect for preferences.",
                    "common_mistake": "Do not argue with preferences; adapt.",
                },
                {
                    "phrase": "How do you prefer to ...?",
                    "meaning_id": "Kamu lebih nyaman ... seperti apa?",
                    "usage_note": "A general preference question pattern.",
                    "common_mistake": "Do not ask why they are uncomfortable; ask preferences.",
                },
            ],
            "grammar_md": [
                ("Tactful openers", ["Would you mind if I ask ...?", "If it's okay, could you clarify ...?"]),
                ("Understanding checks", ["Just to make sure I understand, ...", "Just to confirm, ..."]),
            ],
            "pronunciation": [
                ("tactful", "TAKT-ful."),
                ("privately", "PRY-vit-lee."),
                ("accordingly", "uh-KOR-ding-lee."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask a tactful preference question.",
                    "target_response": "Would you mind if I ask how you prefer to receive feedback?",
                    "acceptable_variations": [
                        "Would you mind if I ask how you prefer to receive feedback?",
                        "Would you mind if I ask how you prefer to communicate updates?",
                    ],
                },
                {
                    "prompt": "Clarify with if it's okay.",
                    "target_response": "If it's okay, could you clarify whether you want feedback in writing or in a call?",
                    "acceptable_variations": [
                        "If it's okay, could you clarify whether you want feedback in writing or in a call?",
                        "If it's okay, could you clarify whether you prefer email or a quick call?",
                    ],
                },
                {
                    "prompt": "Check understanding politely.",
                    "target_response": "Just to make sure I understand, should we share concerns privately first?",
                    "acceptable_variations": [
                        "Just to make sure I understand, should we share concerns privately first?",
                        "Just to make sure I understand, should we align one-on-one first?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "would_you_mind",
                    "type": "multiple_choice",
                    "prompt": "Which phrase is tactful for a sensitive question?",
                    "options": ["Would you mind if I ask ...?", "Tell me now.", "Why are you sensitive?"],
                    "correct_answer": "Would you mind if I ask ...?",
                },
                {
                    "key": "if_its_okay",
                    "type": "multiple_choice",
                    "prompt": "Which phrase softens a clarification request?",
                    "options": ["If it's okay, could you clarify ...?", "Clarify now.", "No need."],
                    "correct_answer": "If it's okay, could you clarify ...?",
                },
                {
                    "key": "make_sure_understand",
                    "type": "multiple_choice",
                    "prompt": "Which phrase checks understanding politely?",
                    "options": ["Just to make sure I understand, ...", "You don't understand.", "Stop."],
                    "correct_answer": "Just to make sure I understand, ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_tactful_questions",
                "opening_line": "We need to ask about a sensitive preference.",
                "learner_goal": "Ask tactful questions and confirm preferences without causing discomfort.",
                "turns": [
                    {
                        "coach": "Ask how they prefer to receive feedback.",
                        "hint": "Would you mind if I ask...?",
                        "sample_answer": "Would you mind if I ask how you prefer to receive feedback?",
                        "focus": "Preference",
                        "expected_keywords": ["would you mind", "prefer"],
                    },
                    {
                        "coach": "Clarify the format politely.",
                        "hint": "If it's okay, could you clarify whether...?",
                        "sample_answer": "If it's okay, could you clarify whether you'd prefer feedback in writing or in a call?",
                        "focus": "Clarify",
                        "expected_keywords": ["if it's okay", "clarify", "whether"],
                    },
                    {
                        "coach": "Check understanding about privacy.",
                        "hint": "Just to make sure I understand...",
                        "sample_answer": "Just to make sure I understand, should we share concerns privately first?",
                        "focus": "Confirm",
                        "expected_keywords": ["make sure", "privately"],
                    },
                ],
                "target_phrases": ["Would you mind if I ask ...?", "If it's okay, could you clarify ...?", "Just to make sure I understand, ..."],
            },
            "reading_support": "Tactful questions reduce friction across cultures. Use softeners (would you mind, if it's okay) and understanding checks to clarify preferences, boundaries, and sensitive topics respectfully.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. Would you mind if I ask ...?",
                "2. How do you prefer to ...?",
                "3. If it's okay, could you clarify ...?",
                "4. Would you prefer ... or ...?",
                "5. Just to make sure I understand, ...",
                "6. Should we ... privately first?",
                "7. Thanks for clarifying.",
                "8. We'll adjust accordingly.",
                "9. Next steps are ...",
                "10. Does that work for you?",
            ],
            "goal_examples": ["Would you mind if I ask ...?", "If it's okay, could you clarify ...?", "Just to make sure I understand, ..."],
        },
        {
            "lesson_key": "lesson-03-explaining-local-norms",
            "slug": "explaining-local-norms",
            "title": "Explaining Local Norms",
            "conversation_situation": "explaining_local_norms",
            "conversation_goal": "Explain local work norms tactfully and help others adapt without sounding judgmental.",
            "grammar_summary": "Use In our context... / It's generally expected that... / People tend to... / It might help to... to explain norms.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Ada rekan baru dari budaya berbeda. Kamu jelasin kebiasaan kerja lokal dengan cara yang sopan dan membantu.",
            "dialogue": [
                ("Jordan", "I'm not sure how direct I should be with the team."),
                ("Mina", "In our context, people tend to be indirect when disagreeing in group settings."),
                ("Jordan", "So I shouldn't disagree openly?"),
                ("Mina", "It's generally expected that you raise concerns one-on-one first."),
                ("Jordan", "Interesting. Any tips?"),
                ("Mina", "It might help to start with appreciation, then ask a question instead of stating a critique."),
                ("Jordan", "Got it."),
                ("Mina", "That usually lands better and keeps relationships smooth."),
            ],
            "translations": [
                ("Jordan", "I'm not sure how direct I should be with the team.", "Aku nggak yakin harus se-direct apa ke tim."),
                ("Mina", "In our context, people tend to be indirect when disagreeing in group settings.", "Dalam konteks kita, orang cenderung indirect saat tidak setuju di forum grup."),
                ("Jordan", "So I shouldn't disagree openly?", "Jadi aku nggak boleh disagree secara terbuka?"),
                ("Mina", "It's generally expected that you raise concerns one-on-one first.", "Umumnya diharapkan kamu raise concern dulu one-on-one."),
                ("Jordan", "Interesting. Any tips?", "Menarik. Ada tips?"),
                ("Mina", "It might help to start with appreciation, then ask a question instead of stating a critique.", "Mungkin membantu kalau mulai dengan apresiasi, lalu tanya pertanyaan daripada langsung kritik."),
                ("Jordan", "Got it.", "Oke."),
                ("Mina", "That usually lands better and keeps relationships smooth.", "Biasanya itu lebih enak diterima dan menjaga relasi tetap smooth."),
            ],
            "useful_phrases": [
                {
                    "phrase": "In our context, people tend to be indirect when disagreeing in group settings.",
                    "meaning_id": "Dalam konteks kita, orang cenderung indirect saat tidak setuju di forum grup.",
                    "usage_note": "Explain norms without judging.",
                    "common_mistake": "Do not say people are wrong; describe tendencies.",
                },
                {
                    "phrase": "It's generally expected that you raise concerns one-on-one first.",
                    "meaning_id": "Umumnya diharapkan kamu raise concern dulu one-on-one.",
                    "usage_note": "Explain expectations.",
                    "common_mistake": "Do not present as a strict rule; use generally expected.",
                },
                {
                    "phrase": "It might help to start with appreciation, then ask a question.",
                    "meaning_id": "Mungkin membantu mulai dengan apresiasi, lalu tanya pertanyaan.",
                    "usage_note": "Offer a practical adaptation tip.",
                    "common_mistake": "Do not lecture; offer help.",
                },
                {
                    "phrase": "That usually lands better.",
                    "meaning_id": "Biasanya itu lebih enak diterima.",
                    "usage_note": "Explain the benefit of the norm.",
                    "common_mistake": "Do not overclaim; say usually.",
                },
                {
                    "phrase": "People tend to ...",
                    "meaning_id": "Orang cenderung ...",
                    "usage_note": "A neutral phrasing for cultural tendencies.",
                    "common_mistake": "Do not generalize harshly; keep it neutral.",
                },
            ],
            "grammar_md": [
                ("Norms", ["In our context, ...", "People tend to ...", "It's generally expected that ..."]),
                ("Suggestions", ["It might help to ...", "You might find it useful to ..."]),
            ],
            "pronunciation": [
                ("context", "KON-tekst."),
                ("expected", "ik-SPEK-tid."),
                ("appreciation", "uh-pree-shee-AY-shun."),
            ],
            "response_prompts": [
                {
                    "prompt": "Explain a norm neutrally.",
                    "target_response": "In our context, people tend to be indirect when disagreeing in group settings.",
                    "acceptable_variations": [
                        "In our context, people tend to be indirect when disagreeing in group settings.",
                        "In our context, people tend to soften disagreement in groups.",
                    ],
                },
                {
                    "prompt": "Explain a general expectation.",
                    "target_response": "It's generally expected that you raise concerns one-on-one first.",
                    "acceptable_variations": [
                        "It's generally expected that you raise concerns one-on-one first.",
                        "It's generally expected that sensitive feedback happens privately first.",
                    ],
                },
                {
                    "prompt": "Offer an adaptation tip tactfully.",
                    "target_response": "It might help to start with appreciation, then ask a question instead of stating a critique.",
                    "acceptable_variations": [
                        "It might help to start with appreciation, then ask a question instead of stating a critique.",
                        "It might help to ask a clarifying question first, then share your view.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "tend_to",
                    "type": "multiple_choice",
                    "prompt": "Which phrase describes a cultural tendency neutrally?",
                    "options": ["People tend to ...", "People are wrong.", "Always do this."],
                    "correct_answer": "People tend to ...",
                },
                {
                    "key": "generally_expected",
                    "type": "multiple_choice",
                    "prompt": "Which phrase explains an expectation without sounding strict?",
                    "options": ["It's generally expected that ...", "You must ...", "Never ..."],
                    "correct_answer": "It's generally expected that ...",
                },
                {
                    "key": "might_help",
                    "type": "multiple_choice",
                    "prompt": "Which phrase offers a suggestion tactfully?",
                    "options": ["It might help to ...", "Do it.", "Stop."],
                    "correct_answer": "It might help to ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_explaining_norms",
                "opening_line": "I'm not sure how direct I should be with the team.",
                "learner_goal": "Explain local norms tactfully and offer practical adaptation tips.",
                "turns": [
                    {
                        "coach": "Explain a local norm about disagreement.",
                        "hint": "In our context... people tend to...",
                        "sample_answer": "In our context, people tend to be indirect when disagreeing in group settings.",
                        "focus": "Norm",
                        "expected_keywords": ["context", "tend to", "indirect"],
                    },
                    {
                        "coach": "Explain what's generally expected.",
                        "hint": "It's generally expected that...",
                        "sample_answer": "It's generally expected that you raise concerns one-on-one first.",
                        "focus": "Expectation",
                        "expected_keywords": ["generally expected", "one-on-one"],
                    },
                    {
                        "coach": "Offer a practical tip.",
                        "hint": "It might help to...",
                        "sample_answer": "It might help to start with appreciation, then ask a question instead of stating a critique.",
                        "focus": "Tip",
                        "expected_keywords": ["might help", "appreciation", "question"],
                    },
                ],
                "target_phrases": ["In our context, ...", "It's generally expected that ...", "It might help to ..."],
            },
            "reading_support": "Explaining norms works best when it's neutral and helpful: describe tendencies, explain what's generally expected, and offer practical tips. Avoid judging and focus on what helps relationships.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. In our context, ...",
                "2. People tend to ...",
                "3. It's generally expected that ...",
                "4. In group settings, ...",
                "5. One-on-one, ...",
                "6. It might help to ...",
                "7. Start with appreciation ...",
                "8. Then ask a question ...",
                "9. That usually lands better ...",
                "10. Let me know if you'd like examples.",
            ],
            "goal_examples": ["In our context, ...", "It's generally expected that ...", "It might help to ..."],
        },
        {
            "lesson_key": "lesson-04-repairing-misunderstanding",
            "slug": "repairing-misunderstanding",
            "title": "Repairing Misunderstanding",
            "conversation_situation": "repairing_misunderstanding",
            "conversation_goal": "Repair a misunderstanding by acknowledging it, clarifying intent, and proposing a constructive next step.",
            "grammar_summary": "Use I may have misunderstood... / I didn't mean to... / Just to clarify... / How about we... to repair misunderstandings.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Terjadi miskomunikasi lintas budaya. Kamu perlu memperbaiki situasi dengan cepat, sopan, dan jelas.",
            "dialogue": [
                ("Jordan", "The client seemed upset after your message."),
                ("Mina", "I may have misunderstood their tone. I didn't mean to come across as dismissive."),
                ("Jordan", "What should we do now?"),
                ("Mina", "Just to clarify, my intent was to confirm the constraints, not reject the request."),
                ("Jordan", "Should we apologize?"),
                ("Mina", "Yes. How about we send a short note acknowledging the misunderstanding and offer a quick call?"),
                ("Jordan", "That sounds good."),
                ("Mina", "Great. I'll draft it and share it in ten minutes."),
            ],
            "translations": [
                ("Jordan", "The client seemed upset after your message.", "Klien kelihatan upset setelah pesan kamu."),
                ("Mina", "I may have misunderstood their tone. I didn't mean to come across as dismissive.", "Mungkin aku salah baca tone-nya. Aku nggak bermaksud terdengar dismissive."),
                ("Jordan", "What should we do now?", "Sekarang kita harus gimana?"),
                ("Mina", "Just to clarify, my intent was to confirm the constraints, not reject the request.", "Biar jelas, niatku untuk konfirmasi constraint, bukan menolak request."),
                ("Jordan", "Should we apologize?", "Perlu minta maaf?"),
                ("Mina", "Yes. How about we send a short note acknowledging the misunderstanding and offer a quick call?", "Iya. Gimana kalau kita kirim note singkat mengakui miskomunikasinya dan tawarkan call cepat?"),
                ("Jordan", "That sounds good.", "Oke."),
                ("Mina", "Great. I'll draft it and share it in ten minutes.", "Oke. Aku draft dan share dalam 10 menit."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I may have misunderstood their tone.",
                    "meaning_id": "Mungkin aku salah baca tone-nya.",
                    "usage_note": "Take responsibility without over-apologizing.",
                    "common_mistake": "Do not blame them; focus on your understanding.",
                },
                {
                    "phrase": "I didn't mean to come across as dismissive.",
                    "meaning_id": "Aku nggak bermaksud terdengar dismissive.",
                    "usage_note": "Clarify intent politely.",
                    "common_mistake": "Do not say you're too sensitive; clarify your intent.",
                },
                {
                    "phrase": "Just to clarify, my intent was to confirm the constraints, not reject the request.",
                    "meaning_id": "Biar jelas, niatku untuk konfirmasi constraint, bukan menolak request.",
                    "usage_note": "Clarify the purpose of your message.",
                    "common_mistake": "Do not get defensive; clarify calmly.",
                },
                {
                    "phrase": "How about we send a short note acknowledging the misunderstanding and offer a quick call?",
                    "meaning_id": "Gimana kalau kita kirim note singkat mengakui miskomunikasinya dan tawarkan call cepat?",
                    "usage_note": "Propose a constructive repair step.",
                    "common_mistake": "Do not over-explain; propose a next step.",
                },
                {
                    "phrase": "I'll draft it and share it in ten minutes.",
                    "meaning_id": "Aku draft dan share dalam 10 menit.",
                    "usage_note": "Immediate action to repair quickly.",
                    "common_mistake": 'Do not say "I will drafting"; use I\'ll draft.',
                },
            ],
            "grammar_md": [
                ("Acknowledging misunderstanding", ["I may have misunderstood ...", "I didn't mean to ..."]),
                ("Repair plan", ["Just to clarify, ...", "How about we ...?"]),
            ],
            "pronunciation": [
                ("misunderstood", "mis-un-DER-stood."),
                ("dismissive", "dis-MIS-iv."),
                ("acknowledging", "ak-NOL-ij-ing."),
            ],
            "response_prompts": [
                {
                    "prompt": "Acknowledge misunderstanding.",
                    "target_response": "I may have misunderstood their tone. I didn't mean to come across as dismissive.",
                    "acceptable_variations": [
                        "I may have misunderstood their tone. I didn't mean to come across as dismissive.",
                        "I may have misunderstood the context. I didn't mean to sound dismissive.",
                    ],
                },
                {
                    "prompt": "Clarify intent calmly.",
                    "target_response": "Just to clarify, my intent was to confirm the constraints, not reject the request.",
                    "acceptable_variations": [
                        "Just to clarify, my intent was to confirm the constraints, not reject the request.",
                        "Just to clarify, I was trying to confirm details, not say no.",
                    ],
                },
                {
                    "prompt": "Propose a repair step.",
                    "target_response": "How about we send a short note acknowledging the misunderstanding and offer a quick call?",
                    "acceptable_variations": [
                        "How about we send a short note acknowledging the misunderstanding and offer a quick call?",
                        "How about we apologize briefly and offer a short call to align?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "may_have_misunderstood",
                    "type": "multiple_choice",
                    "prompt": "Which phrase acknowledges misunderstanding responsibly?",
                    "options": ["I may have misunderstood ...", "You misunderstood.", "Not my problem."],
                    "correct_answer": "I may have misunderstood ...",
                },
                {
                    "key": "didnt_mean",
                    "type": "multiple_choice",
                    "prompt": "Which phrase clarifies intent politely?",
                    "options": ["I didn't mean to ...", "You are too sensitive.", "Stop."],
                    "correct_answer": "I didn't mean to ...",
                },
                {
                    "key": "how_about",
                    "type": "multiple_choice",
                    "prompt": "Which phrase proposes a constructive next step?",
                    "options": ["How about we ...?", "Whatever.", "No."],
                    "correct_answer": "How about we ...?",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_repairing_misunderstanding",
                "opening_line": "The client seemed upset after your message.",
                "learner_goal": "Repair a misunderstanding with acknowledgement, clarification, and next steps.",
                "turns": [
                    {
                        "coach": "Acknowledge the misunderstanding and clarify intent.",
                        "hint": "I may have misunderstood... I didn't mean to...",
                        "sample_answer": "I may have misunderstood their tone. I didn't mean to come across as dismissive.",
                        "focus": "Acknowledge",
                        "expected_keywords": ["misunderstood", "didn't mean", "dismissive"],
                    },
                    {
                        "coach": "Clarify what you meant.",
                        "hint": "Just to clarify, my intent was ...",
                        "sample_answer": "Just to clarify, my intent was to confirm the constraints, not reject the request.",
                        "focus": "Clarify intent",
                        "expected_keywords": ["just to clarify", "intent", "not reject"],
                    },
                    {
                        "coach": "Propose a repair plan and timeline.",
                        "hint": "How about we... I'll draft it...",
                        "sample_answer": "How about we send a short note acknowledging the misunderstanding and offer a quick call? I'll draft it and share it in ten minutes.",
                        "focus": "Repair plan",
                        "expected_keywords": ["how about", "acknowledging", "call", "draft"],
                    },
                ],
                "target_phrases": ["I may have misunderstood ...", "Just to clarify, ...", "How about we ...?"],
            },
            "reading_support": "Repairing misunderstandings across cultures works best when you acknowledge the issue, clarify your intent calmly, and propose a concrete next step (short note + call). Move quickly and keep the tone respectful.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. I may have misunderstood ...",
                "2. I didn't mean to ...",
                "3. Just to clarify, ...",
                "4. My intent was to ...",
                "5. Not to ...",
                "6. How about we ...?",
                "7. We'll send a short note ...",
                "8. And offer a quick call ...",
                "9. I'll draft it by ...",
                "10. Thanks for raising this.",
            ],
            "goal_examples": ["I may have misunderstood ...", "Just to clarify, ...", "How about we ...?"],
        },
        {
            "lesson_key": "lesson-05-cross-cultural-mission",
            "slug": "cross-cultural-mission",
            "title": "Cross-cultural Mission",
            "conversation_situation": "mission_cross_cultural",
            "conversation_goal": "Handle a cross-cultural situation: read context, ask tactful questions, explain norms, and repair misunderstandings.",
            "grammar_summary": "Combine context reading, tactful questions, norms explanation, and repair language into one end-to-end conversation.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Misi: kamu handle situasi lintas budaya dari interpretasi pesan sampai repair miskomunikasi, dengan tone yang profesional.",
            "dialogue": [
                ("Jordan", "The client says the timeline is 'ambitious'."),
                ("Mina", "My sense is that they're signaling concern indirectly. Before we decide, can we clarify whether they prioritize speed or risk reduction?"),
                ("Jordan", "They also dislike direct criticism."),
                ("Mina", "Would you mind if I ask how they prefer to receive feedback—writing or a call?"),
                ("Jordan", "In our culture, they prefer private feedback first."),
                ("Mina", "In our context, it's generally expected that we raise concerns one-on-one first. It might help to start with appreciation."),
                ("Jordan", "They seemed upset after the last message."),
                ("Mina", "I may have misunderstood their tone. Just to clarify, my intent was to confirm constraints, not reject the request. How about we send a short note and offer a quick call?"),
            ],
            "translations": [
                ("Jordan", "The client says the timeline is 'ambitious'.", "Klien bilang timeline-nya 'ambitious'."),
                ("Mina", "My sense is that they're signaling concern indirectly. Before we decide, can we clarify whether they prioritize speed or risk reduction?", "Feeling aku, mereka ngasih sinyal concern secara indirect. Sebelum putuskan, bisa kita klarifikasi mereka prioritasin speed atau risk reduction?"),
                ("Jordan", "They also dislike direct criticism.", "Mereka juga nggak suka kritik yang direct."),
                ("Mina", "Would you mind if I ask how they prefer to receive feedback—writing or a call?", "Boleh aku tanya mereka lebih nyaman feedback lewat tulisan atau call?"),
                ("Jordan", "In our culture, they prefer private feedback first.", "Dalam budaya mereka, lebih suka feedback private dulu."),
                ("Mina", "In our context, it's generally expected that we raise concerns one-on-one first. It might help to start with appreciation.", "Dalam konteks kita, umumnya diharapkan concern diangkat one-on-one dulu. Mungkin membantu mulai dengan apresiasi."),
                ("Jordan", "They seemed upset after the last message.", "Mereka kelihatan upset setelah pesan terakhir."),
                ("Mina", "I may have misunderstood their tone. Just to clarify, my intent was to confirm constraints, not reject the request. How about we send a short note and offer a quick call?", "Mungkin aku salah baca tone-nya. Biar jelas, niatku konfirmasi constraint, bukan menolak request. Gimana kalau kita kirim note singkat dan tawarkan call cepat?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "My sense is that they're signaling concern indirectly.",
                    "meaning_id": "Feeling aku, mereka ngasih sinyal concern secara indirect.",
                    "usage_note": "Context reading.",
                    "common_mistake": "Don't assume they're angry; read context first.",
                },
                {
                    "phrase": "Would you mind if I ask how you prefer to receive feedback?",
                    "meaning_id": "Boleh aku tanya kamu lebih nyaman menerima feedback seperti apa?",
                    "usage_note": "Tactful question.",
                    "common_mistake": "Don't ask bluntly; soften it.",
                },
                {
                    "phrase": "In our context, it's generally expected that we raise concerns one-on-one first.",
                    "meaning_id": "Dalam konteks kita, umumnya concern diangkat one-on-one dulu.",
                    "usage_note": "Explain norms neutrally.",
                    "common_mistake": "Don't present it as a strict rule.",
                },
                {
                    "phrase": "I may have misunderstood their tone. Just to clarify, my intent was to confirm constraints, not reject the request.",
                    "meaning_id": "Mungkin aku salah baca tone-nya. Biar jelas, niatku konfirmasi constraint, bukan menolak request.",
                    "usage_note": "Repair misunderstanding.",
                    "common_mistake": "Don't get defensive; clarify calmly.",
                },
                {
                    "phrase": "How about we send a short note and offer a quick call?",
                    "meaning_id": "Gimana kalau kita kirim note singkat dan tawarkan call cepat?",
                    "usage_note": "Constructive next step.",
                    "common_mistake": "Don't over-apologize; propose action.",
                },
            ],
            "grammar_md": [
                (
                    "Cross-cultural toolkit",
                    [
                        "My sense is that ... Before we decide, can we clarify ...?",
                        "Would you mind if I ask ...?",
                        "In our context, people tend to ... It's generally expected that ...",
                        "I may have misunderstood ... Just to clarify, ... How about we ...?",
                    ],
                )
            ],
            "pronunciation": [
                ("tact", "TAKT."),
                ("misunderstanding", "mis-un-der-STAN-ding."),
                ("cultural", "KUL-cher-uhl."),
            ],
            "response_prompts": [
                {
                    "prompt": "Read context and clarify priorities.",
                    "target_response": "My sense is that they're signaling concern indirectly. Before we decide, can we clarify whether they prioritize speed or risk reduction?",
                    "acceptable_variations": [
                        "My sense is that they're signaling concern indirectly. Before we decide, can we clarify whether they prioritize speed or risk reduction?",
                        "My sense is that they're hesitant. Before we decide, can we clarify what matters most to them?",
                    ],
                },
                {
                    "prompt": "Ask a tactful question about preferences.",
                    "target_response": "Would you mind if I ask how you prefer to receive feedback—writing or a call?",
                    "acceptable_variations": [
                        "Would you mind if I ask how you prefer to receive feedback—writing or a call?",
                        "Would you mind if I ask what format you prefer for feedback?",
                    ],
                },
                {
                    "prompt": "Repair misunderstanding and propose next step.",
                    "target_response": "I may have misunderstood their tone. Just to clarify, my intent was to confirm constraints, not reject the request. How about we send a short note and offer a quick call?",
                    "acceptable_variations": [
                        "I may have misunderstood their tone. Just to clarify, my intent was to confirm constraints, not reject the request. How about we send a short note and offer a quick call?",
                        "I may have misunderstood the context. Just to clarify, I was trying to confirm details. How about we offer a quick call?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "context_first",
                    "type": "multiple_choice",
                    "prompt": "Which phrase helps you interpret indirect feedback?",
                    "options": ["My sense is that ...", "They hate us.", "No context."],
                    "correct_answer": "My sense is that ...",
                },
                {
                    "key": "tactful_question",
                    "type": "multiple_choice",
                    "prompt": "Which phrase is tactful for sensitive preferences?",
                    "options": ["Would you mind if I ask ...?", "Answer now.", "Stop."],
                    "correct_answer": "Would you mind if I ask ...?",
                },
                {
                    "key": "repair_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase repairs misunderstanding responsibly?",
                    "options": ["I may have misunderstood ...", "You misunderstood.", "Not my issue."],
                    "correct_answer": "I may have misunderstood ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_cross_cultural_mission",
                "opening_line": "The client seems indirect and uncomfortable with direct feedback.",
                "learner_goal": "Handle cross-cultural communication end-to-end with tact, clarity, and repair.",
                "turns": [
                    {
                        "coach": "Interpret the client's indirect message and clarify priorities.",
                        "hint": "My sense is that... Before we decide, can we clarify...?",
                        "sample_answer": "My sense is that they're signaling concern indirectly. Before we decide, can we clarify whether they prioritize speed or risk reduction?",
                        "focus": "Context",
                        "expected_keywords": ["my sense", "clarify", "priority"],
                    },
                    {
                        "coach": "Ask a tactful question about feedback preferences.",
                        "hint": "Would you mind if I ask...?",
                        "sample_answer": "Would you mind if I ask how you prefer to receive feedback—writing or a call?",
                        "focus": "Tactful question",
                        "expected_keywords": ["would you mind", "prefer"],
                    },
                    {
                        "coach": "Repair a misunderstanding and propose a next step.",
                        "hint": "I may have misunderstood... Just to clarify... How about we...?",
                        "sample_answer": "I may have misunderstood their tone. Just to clarify, my intent was to confirm constraints, not reject the request. How about we send a short note and offer a quick call?",
                        "focus": "Repair",
                        "expected_keywords": ["misunderstood", "intent", "how about"],
                    },
                ],
                "target_phrases": ["My sense is that ...", "Would you mind if I ask ...?", "I may have misunderstood ..."],
            },
            "reading_support": "Cross-cultural professionalism means you read context, ask tactful questions, explain norms neutrally, and repair misunderstandings quickly. Focus on respect, clarity, and concrete next steps.",
            "writing_support_lines": [
                "Write your mission (12 lines):",
                "1. My sense is that ...",
                "2. They may be signaling ...",
                "3. Before we decide, can we clarify ...?",
                "4. Would you mind if I ask ...?",
                "5. If it's okay, could you clarify ...?",
                "6. In our context, people tend to ...",
                "7. It's generally expected that ...",
                "8. It might help to ...",
                "9. I may have misunderstood ...",
                "10. Just to clarify, my intent was ...",
                "11. How about we ...?",
                "12. Next steps are ...",
            ],
            "goal_examples": ["My sense is that ...", "Would you mind if I ask ...?", "I may have misunderstood ..."],
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

