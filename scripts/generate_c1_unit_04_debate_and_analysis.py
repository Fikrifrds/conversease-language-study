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
            "- Tone: analytical, calm, assertive",
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

        Read it again and underline the debate tools (assumption, premise, evidence, counterexample, inference, bias).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "C1"
    root = Path("content/curriculum/english/C1")
    units_root = root / "units"
    unit_key = "unit-04-debate-and-analysis"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-04-debate-and-analysis
            level_code: C1
            title: Debate & Analysis
            main_conversation_outcome: Analyze arguments and respond persuasively in debate-style conversations.
            status: in_production
            lessons:
              - lesson-01-identifying-assumptions
              - lesson-02-challenging-an-argument
              - lesson-03-presenting-evidence
              - lesson-04-responding-under-pressure
              - lesson-05-debate-analysis-mission
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
            "lesson_key": "lesson-01-identifying-assumptions",
            "slug": "identifying-assumptions",
            "title": "Identifying Assumptions",
            "conversation_situation": "debate_identify_assumptions",
            "conversation_goal": "Identify assumptions behind an argument and ask clarifying questions about the premise.",
            "grammar_summary": "Use It seems you're assuming... / What are we assuming about... / If that's true, then... to identify assumptions.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu lagi debat ringan di kerja. Kamu ingin menguji argumen dengan cara mengangkat asumsi yang tersembunyi, tanpa menyerang orangnya.",
            "dialogue": [
                ("Alex", "We should cut the onboarding steps to increase conversion."),
                ("Mina", "It seems you're assuming fewer steps automatically mean better conversion."),
                ("Alex", "Isn't that obvious?"),
                ("Mina", "Not necessarily. What are we assuming about user trust and clarity?"),
                ("Alex", "That users just want speed."),
                ("Mina", "If that's true, then we should see drop-offs mainly on longer forms."),
                ("Alex", "So how do we test it?"),
                ("Mina", "Let's separate essential steps from redundant ones and measure impact."),
            ],
            "translations": [
                ("Alex", "We should cut the onboarding steps to increase conversion.", "Kita harus potong step onboarding supaya conversion naik."),
                ("Mina", "It seems you're assuming fewer steps automatically mean better conversion.", "Sepertinya kamu berasumsi step lebih sedikit otomatis bikin conversion lebih bagus."),
                ("Alex", "Isn't that obvious?", "Bukannya itu jelas?"),
                ("Mina", "Not necessarily. What are we assuming about user trust and clarity?", "Belum tentu. Kita berasumsi apa tentang trust dan kejelasan bagi user?"),
                ("Alex", "That users just want speed.", "Bahwa user cuma mau cepat."),
                ("Mina", "If that's true, then we should see drop-offs mainly on longer forms.", "Kalau itu benar, drop-off harusnya terjadi terutama di form yang panjang."),
                ("Alex", "So how do we test it?", "Jadi kita test gimana?"),
                ("Mina", "Let's separate essential steps from redundant ones and measure impact.", "Kita pisahkan step yang essential dari yang redundant lalu ukur dampaknya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "It seems you're assuming fewer steps automatically mean better conversion.",
                    "meaning_id": "Sepertinya kamu berasumsi step lebih sedikit otomatis bikin conversion lebih bagus.",
                    "usage_note": "Surface an assumption without sounding accusatory.",
                    "common_mistake": "Do not say you're wrong; say it seems you're assuming.",
                },
                {
                    "phrase": "What are we assuming about user trust and clarity?",
                    "meaning_id": "Kita berasumsi apa tentang trust dan kejelasan bagi user?",
                    "usage_note": "Ask about the underlying premise.",
                    "common_mistake": "Do not stay abstract; name a specific dimension (trust, clarity).",
                },
                {
                    "phrase": "If that's true, then we should see drop-offs mainly on longer forms.",
                    "meaning_id": "Kalau itu benar, drop-off harusnya terutama di form panjang.",
                    "usage_note": "Draw a testable implication from an assumption.",
                    "common_mistake": "Do not argue in circles; make it testable.",
                },
                {
                    "phrase": "Let's separate essential steps from redundant ones and measure impact.",
                    "meaning_id": "Kita pisahkan step essential dari yang redundant lalu ukur dampaknya.",
                    "usage_note": "Turn debate into an experiment plan.",
                    "common_mistake": "Do not stop at criticism; propose a test.",
                },
                {
                    "phrase": "Not necessarily.",
                    "meaning_id": "Belum tentu.",
                    "usage_note": "A concise disagreement marker.",
                    "common_mistake": "Do not sound dismissive; follow up with a question.",
                },
            ],
            "grammar_md": [
                ("Assumption language", ["It seems you're assuming ...", "What are we assuming about ...?"]),
                ("Implications", ["If that's true, then ...", "If we accept that premise, ..."]),
            ],
            "pronunciation": [
                ("assumption", "uh-SUMP-shun."),
                ("premise", "PREM-iss."),
                ("redundant", "ri-DUN-dent."),
            ],
            "response_prompts": [
                {
                    "prompt": "Surface an assumption politely.",
                    "target_response": "It seems you're assuming fewer steps automatically mean better conversion.",
                    "acceptable_variations": [
                        "It seems you're assuming fewer steps automatically mean better conversion.",
                        "It seems you're assuming speed is the main driver of conversion.",
                    ],
                },
                {
                    "prompt": "Ask about the underlying premise.",
                    "target_response": "What are we assuming about user trust and clarity?",
                    "acceptable_variations": [
                        "What are we assuming about user trust and clarity?",
                        "What are we assuming about user intent here?",
                    ],
                },
                {
                    "prompt": "State a testable implication.",
                    "target_response": "If that's true, then we should see drop-offs mainly on longer forms.",
                    "acceptable_variations": [
                        "If that's true, then we should see drop-offs mainly on longer forms.",
                        "If that's true, then the data should show drop-offs on step three and four.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "assuming_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase surfaces an assumption politely?",
                    "options": ["It seems you're assuming ...", "You're wrong.", "No."],
                    "correct_answer": "It seems you're assuming ...",
                },
                {
                    "key": "premise_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "premise" mean?',
                    "options": ["dasar argumen/asumsi awal", "kesimpulan", "judul"],
                    "correct_answer": "dasar argumen/asumsi awal",
                },
                {
                    "key": "if_true",
                    "type": "multiple_choice",
                    "prompt": "Which phrase draws an implication?",
                    "options": ["If that's true, then ...", "Whatever.", "Stop."],
                    "correct_answer": "If that's true, then ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_identifying_assumptions",
                "opening_line": "We should cut steps to increase conversion.",
                "learner_goal": "Identify assumptions and turn them into testable implications.",
                "turns": [
                    {
                        "coach": "We should cut steps to increase conversion.",
                        "hint": "Surface an assumption politely.",
                        "sample_answer": "It seems you're assuming fewer steps automatically mean better conversion.",
                        "focus": "Assumption",
                        "expected_keywords": ["assuming", "steps", "conversion"],
                    },
                    {
                        "coach": "Ask a clarifying question about the premise.",
                        "hint": "What are we assuming about...?",
                        "sample_answer": "What are we assuming about user trust and clarity?",
                        "focus": "Premise",
                        "expected_keywords": ["assuming", "trust", "clarity"],
                    },
                    {
                        "coach": "Make it testable and propose a next step.",
                        "hint": "If that's true, then... Let's...",
                        "sample_answer": "If that's true, then we should see drop-offs mainly on longer forms. Let's separate essential steps from redundant ones and measure impact.",
                        "focus": "Test",
                        "expected_keywords": ["if that's true", "measure"],
                    },
                ],
                "target_phrases": ["It seems you're assuming ...", "What are we assuming about ...?", "If that's true, then ..."],
            },
            "reading_support": "In debate and analysis, identifying assumptions is powerful. Surface the hidden premise, ask clarifying questions, then make the argument testable by stating what the data should show.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. It seems you're assuming ...",
                "2. What are we assuming about ...?",
                "3. Not necessarily.",
                "4. If that's true, then ...",
                "5. The data should show ...",
                "6. One alternative explanation is ...",
                "7. How would we test that?",
                "8. Let's separate ... from ...",
                "9. And measure ...",
                "10. Then we can decide.",
            ],
            "goal_examples": ["It seems you're assuming ...", "What are we assuming about ...?", "If that's true, then ..."],
        },
        {
            "lesson_key": "lesson-02-challenging-an-argument",
            "slug": "challenging-an-argument",
            "title": "Challenging an Argument",
            "conversation_situation": "challenge_argument",
            "conversation_goal": "Challenge an argument constructively using counterexamples, alternative explanations, and precise questions.",
            "grammar_summary": "Use I'm not sure that follows... / What's the evidence for... / Could there be another explanation? / For example... to challenge arguments.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu menantang argumen orang lain secara konstruktif. Kamu fokus ke logika dan evidence, bukan menyerang personal.",
            "dialogue": [
                ("Alex", "Fewer steps always increases conversion."),
                ("Mina", "I'm not sure that follows. What's the evidence for that claim?"),
                ("Alex", "It's common sense."),
                ("Mina", "Could there be another explanation, like unclear copy or missing reassurance?"),
                ("Alex", "Maybe."),
                ("Mina", "For example, we reduced steps last quarter, but conversion didn't change."),
                ("Alex", "So what do you propose?"),
                ("Mina", "Let's test messaging changes alongside step reduction."),
            ],
            "translations": [
                ("Alex", "Fewer steps always increases conversion.", "Step lebih sedikit selalu bikin conversion naik."),
                ("Mina", "I'm not sure that follows. What's the evidence for that claim?", "Aku nggak yakin itu nyambung. Evidence-nya apa untuk claim itu?"),
                ("Alex", "It's common sense.", "Itu common sense."),
                ("Mina", "Could there be another explanation, like unclear copy or missing reassurance?", "Bisa nggak ada penjelasan lain, misalnya copy yang nggak jelas atau reassurance yang kurang?"),
                ("Alex", "Maybe.", "Mungkin."),
                ("Mina", "For example, we reduced steps last quarter, but conversion didn't change.", "Contohnya, kita kurangi step kuartal lalu, tapi conversion nggak berubah."),
                ("Alex", "So what do you propose?", "Jadi kamu usul apa?"),
                ("Mina", "Let's test messaging changes alongside step reduction.", "Kita test perubahan messaging bareng pengurangan step."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'm not sure that follows.",
                    "meaning_id": "Aku nggak yakin itu nyambung.",
                    "usage_note": "Challenge logic without being rude.",
                    "common_mistake": "Do not say that's nonsense; keep it neutral.",
                },
                {
                    "phrase": "What's the evidence for that claim?",
                    "meaning_id": "Evidence-nya apa untuk claim itu?",
                    "usage_note": "Ask for evidence directly.",
                    "common_mistake": "Do not say prove it; ask for evidence.",
                },
                {
                    "phrase": "Could there be another explanation?",
                    "meaning_id": "Bisa nggak ada penjelasan lain?",
                    "usage_note": "Introduce alternative hypotheses.",
                    "common_mistake": "Do not dismiss; explore alternatives.",
                },
                {
                    "phrase": "For example, we reduced steps last quarter, but conversion didn't change.",
                    "meaning_id": "Contohnya, kita kurangi step kuartal lalu, tapi conversion nggak berubah.",
                    "usage_note": "Use counterexample to challenge.",
                    "common_mistake": "Do not generalize from one example; use it as evidence to test.",
                },
                {
                    "phrase": "Let's test messaging changes alongside step reduction.",
                    "meaning_id": "Kita test perubahan messaging bareng pengurangan step.",
                    "usage_note": "Turn challenge into actionable test.",
                    "common_mistake": "Do not only criticize; propose a next step.",
                },
            ],
            "grammar_md": [
                ("Challenging logic", ["I'm not sure that follows.", "What's the evidence for ...?"]),
                ("Alternatives + examples", ["Could there be another explanation?", "For example, ..."]),
            ],
            "pronunciation": [
                ("evidence", "EV-uh-dens."),
                ("counterexample", "KOWN-ter-ig-ZAM-puhl."),
                ("reassurance", "ree-uh-SHUR-ens."),
            ],
            "response_prompts": [
                {
                    "prompt": "Challenge logic politely.",
                    "target_response": "I'm not sure that follows.",
                    "acceptable_variations": ["I'm not sure that follows.", "I'm not sure the conclusion follows from that."],
                },
                {
                    "prompt": "Ask for evidence.",
                    "target_response": "What's the evidence for that claim?",
                    "acceptable_variations": [
                        "What's the evidence for that claim?",
                        "What evidence do we have for that?",
                    ],
                },
                {
                    "prompt": "Offer an alternative explanation.",
                    "target_response": "Could there be another explanation, like unclear copy or missing reassurance?",
                    "acceptable_variations": [
                        "Could there be another explanation, like unclear copy or missing reassurance?",
                        "Could there be another explanation, like trust issues?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "follows_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase challenges logic politely?",
                    "options": ["I'm not sure that follows.", "You're stupid.", "No."],
                    "correct_answer": "I'm not sure that follows.",
                },
                {
                    "key": "ask_evidence",
                    "type": "multiple_choice",
                    "prompt": "Which phrase asks for evidence?",
                    "options": ["What's the evidence for that claim?", "Prove it now.", "Stop."],
                    "correct_answer": "What's the evidence for that claim?",
                },
                {
                    "key": "another_explanation",
                    "type": "multiple_choice",
                    "prompt": "Which phrase suggests alternative explanations?",
                    "options": ["Could there be another explanation?", "No alternatives.", "Anyway."],
                    "correct_answer": "Could there be another explanation?",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_challenging_argument",
                "opening_line": "Fewer steps always increases conversion.",
                "learner_goal": "Challenge an argument constructively using evidence questions and alternatives.",
                "turns": [
                    {
                        "coach": "Fewer steps always increases conversion.",
                        "hint": "Challenge logic politely.",
                        "sample_answer": "I'm not sure that follows. What's the evidence for that claim?",
                        "focus": "Logic + evidence",
                        "expected_keywords": ["not sure", "evidence"],
                    },
                    {
                        "coach": "I think it's common sense. What's your response?",
                        "hint": "Introduce another explanation + example.",
                        "sample_answer": "Could there be another explanation, like unclear copy or missing reassurance? For example, we reduced steps last quarter, but conversion didn't change.",
                        "focus": "Alternatives",
                        "expected_keywords": ["another explanation", "for example"],
                    },
                    {
                        "coach": "Close with a constructive next step.",
                        "hint": "Let's test...",
                        "sample_answer": "Let's test messaging changes alongside step reduction and compare results.",
                        "focus": "Next step",
                        "expected_keywords": ["test", "compare"],
                    },
                ],
                "target_phrases": ["I'm not sure that follows.", "What's the evidence for ...?", "Could there be another explanation?"],
            },
            "reading_support": "Challenging an argument is about logic and evidence. Question whether the conclusion follows, ask for evidence, propose alternative explanations, and end with a testable next step.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. I'm not sure that follows.",
                "2. What's the evidence for ...?",
                "3. Could there be another explanation?",
                "4. For example, ...",
                "5. That suggests ...",
                "6. Another possibility is ...",
                "7. How would we test that?",
                "8. Let's test ...",
                "9. And compare ...",
                "10. Then decide based on results.",
            ],
            "goal_examples": ["I'm not sure that follows.", "What's the evidence for ...?", "Could there be another explanation?"],
        },
        {
            "lesson_key": "lesson-03-presenting-evidence",
            "slug": "presenting-evidence",
            "title": "Presenting Evidence",
            "conversation_situation": "presenting_evidence_in_debate",
            "conversation_goal": "Present evidence clearly, distinguish facts from interpretations, and reference sources confidently.",
            "grammar_summary": "Use According to... / The data indicates... / This suggests... / To be precise... to present evidence.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu mendukung argumen dengan evidence. Kamu bisa membedakan fakta, interpretasi, dan menyebut sumbernya.",
            "dialogue": [
                ("Alex", "Do we have any data to support this?"),
                ("Mina", "According to the support dashboard, drop-offs increased after the redesign."),
                ("Alex", "So the redesign caused it?"),
                ("Mina", "To be precise, the data indicates correlation, not necessarily causation."),
                ("Alex", "What does it suggest, then?"),
                ("Mina", "This suggests we should investigate the checkout experience before changing other variables."),
                ("Alex", "Any other sources?"),
                ("Mina", "Yes—session recordings show confusion on the verification step."),
            ],
            "translations": [
                ("Alex", "Do we have any data to support this?", "Kita punya data untuk mendukung ini nggak?"),
                ("Mina", "According to the support dashboard, drop-offs increased after the redesign.", "Menurut dashboard support, drop-off naik setelah redesign."),
                ("Alex", "So the redesign caused it?", "Berarti redesign yang nyebabin?"),
                ("Mina", "To be precise, the data indicates correlation, not necessarily causation.", "Biar presisi, data menunjukkan korelasi, belum tentu kausalitas."),
                ("Alex", "What does it suggest, then?", "Jadi itu menyarankan apa?"),
                ("Mina", "This suggests we should investigate the checkout experience before changing other variables.", "Ini menyarankan kita investigasi checkout dulu sebelum mengubah variabel lain."),
                ("Alex", "Any other sources?", "Ada sumber lain?"),
                ("Mina", "Yes—session recordings show confusion on the verification step.", "Ada—rekaman sesi menunjukkan kebingungan di step verifikasi."),
            ],
            "useful_phrases": [
                {
                    "phrase": "According to the support dashboard, drop-offs increased after the redesign.",
                    "meaning_id": "Menurut dashboard support, drop-off naik setelah redesign.",
                    "usage_note": "Reference a source explicitly.",
                    "common_mistake": "Do not state numbers without citing where they come from.",
                },
                {
                    "phrase": "To be precise, the data indicates correlation, not necessarily causation.",
                    "meaning_id": "Biar presisi, data menunjukkan korelasi, belum tentu kausalitas.",
                    "usage_note": "Distinguish correlation vs causation.",
                    "common_mistake": "Do not claim causation from correlation.",
                },
                {
                    "phrase": "This suggests we should investigate the checkout experience.",
                    "meaning_id": "Ini menyarankan kita investigasi pengalaman checkout.",
                    "usage_note": "Move from evidence to implication.",
                    "common_mistake": "Do not jump to a solution; suggest investigation first.",
                },
                {
                    "phrase": "Session recordings show confusion on the verification step.",
                    "meaning_id": "Rekaman sesi menunjukkan kebingungan di step verifikasi.",
                    "usage_note": "Use multiple sources to strengthen argument.",
                    "common_mistake": "Do not rely on one source only; triangulate.",
                },
                {
                    "phrase": "The data indicates ...",
                    "meaning_id": "Data menunjukkan ...",
                    "usage_note": "Neutral evidence phrasing.",
                    "common_mistake": "Do not say data proves for complex issues; use indicates.",
                },
            ],
            "grammar_md": [
                ("Sources", ["According to ...", "Based on ..."]),
                ("Precision", ["To be precise, ...", "The data indicates ..."]),
            ],
            "pronunciation": [
                ("correlation", "kor-uh-LAY-shun."),
                ("causation", "kaw-ZAY-shun."),
                ("triangulate", "try-ANG-gyuh-layt."),
            ],
            "response_prompts": [
                {
                    "prompt": "Cite a source with according to.",
                    "target_response": "According to the support dashboard, drop-offs increased after the redesign.",
                    "acceptable_variations": [
                        "According to the support dashboard, drop-offs increased after the redesign.",
                        "According to the logs, errors increased after the release.",
                    ],
                },
                {
                    "prompt": "Clarify correlation vs causation.",
                    "target_response": "To be precise, the data indicates correlation, not necessarily causation.",
                    "acceptable_variations": [
                        "To be precise, the data indicates correlation, not necessarily causation.",
                        "To be precise, the trend suggests correlation, not causation.",
                    ],
                },
                {
                    "prompt": "State an implication carefully.",
                    "target_response": "This suggests we should investigate the checkout experience before changing other variables.",
                    "acceptable_variations": [
                        "This suggests we should investigate the checkout experience before changing other variables.",
                        "This suggests we should validate the hypothesis before making changes.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "according_to",
                    "type": "multiple_choice",
                    "prompt": "Which phrase cites a source?",
                    "options": ["According to ...", "Because I said so.", "No source."],
                    "correct_answer": "According to ...",
                },
                {
                    "key": "correlation_causation",
                    "type": "multiple_choice",
                    "prompt": "Which sentence distinguishes correlation from causation?",
                    "options": [
                        "The data indicates correlation, not necessarily causation.",
                        "Correlation is causation.",
                        "No difference.",
                    ],
                    "correct_answer": "The data indicates correlation, not necessarily causation.",
                },
                {
                    "key": "to_be_precise",
                    "type": "multiple_choice",
                    "prompt": 'What does "to be precise" mean?',
                    "options": ["agar lebih tepat/presisi", "agar cepat", "agar lucu"],
                    "correct_answer": "agar lebih tepat/presisi",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_presenting_evidence",
                "opening_line": "Do we have data to support this?",
                "learner_goal": "Present evidence with sources and precision, then state implications carefully.",
                "turns": [
                    {
                        "coach": "Do we have data to support this?",
                        "hint": "Use According to...",
                        "sample_answer": "According to the support dashboard, drop-offs increased after the redesign.",
                        "focus": "Source",
                        "expected_keywords": ["according to", "dashboard"],
                    },
                    {
                        "coach": "So the redesign caused it?",
                        "hint": "Clarify correlation vs causation.",
                        "sample_answer": "To be precise, the data indicates correlation, not necessarily causation.",
                        "focus": "Precision",
                        "expected_keywords": ["precise", "correlation", "causation"],
                    },
                    {
                        "coach": "Close with a careful implication and another source.",
                        "hint": "This suggests... Another source shows...",
                        "sample_answer": "This suggests we should investigate the checkout experience. Session recordings also show confusion on the verification step.",
                        "focus": "Implication + triangulation",
                        "expected_keywords": ["suggests", "recordings", "confusion"],
                    },
                ],
                "target_phrases": ["According to ...", "To be precise, ...", "The data indicates ..."],
            },
            "reading_support": "Presenting evidence in debate means citing sources and being precise about what the data shows. Avoid overclaiming causation, and strengthen your case with multiple sources.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. According to ...",
                "2. The data indicates ...",
                "3. To be precise, ...",
                "4. This suggests ...",
                "5. Another source shows ...",
                "6. For example, ...",
                "7. That supports ...",
                "8. However, ...",
                "9. So the next step is ...",
                "10. Any questions?",
            ],
            "goal_examples": ["According to ...", "To be precise, ...", "This suggests ..."],
        },
        {
            "lesson_key": "lesson-04-responding-under-pressure",
            "slug": "responding-under-pressure",
            "title": "Responding Under Pressure",
            "conversation_situation": "debate_under_pressure",
            "conversation_goal": "Respond under pressure by staying calm, addressing the core point, and tightening your argument.",
            "grammar_summary": "Use Let me be clear... / I understand the concern, however... / The key point is... / If you look at... to respond under pressure.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Debat mulai panas. Kamu perlu tetap calm, jawab poin inti, dan perjelas argumen kamu tanpa defensif.",
            "dialogue": [
                ("Alex", "This is just speculation. Do you have anything solid?"),
                ("Mina", "Let me be clear: we have indicators, not proof yet."),
                ("Alex", "So why should we act now?"),
                ("Mina", "I understand the concern. However, the key point is that waiting increases risk."),
                ("Alex", "Show me the numbers."),
                ("Mina", "If you look at the last four weeks, incident volume has doubled."),
                ("Alex", "Fine. What's your proposal?"),
                ("Mina", "We run a pilot this week and review results before scaling."),
            ],
            "translations": [
                ("Alex", "This is just speculation. Do you have anything solid?", "Ini cuma spekulasi. Kamu punya yang solid nggak?"),
                ("Mina", "Let me be clear: we have indicators, not proof yet.", "Biar jelas: kita punya indikator, belum bukti."),
                ("Alex", "So why should we act now?", "Jadi kenapa harus bertindak sekarang?"),
                ("Mina", "I understand the concern. However, the key point is that waiting increases risk.", "Aku paham concern-nya. Tapi poin kuncinya: menunggu meningkatkan risiko."),
                ("Alex", "Show me the numbers.", "Tunjukin angkanya."),
                ("Mina", "If you look at the last four weeks, incident volume has doubled.", "Kalau lihat 4 minggu terakhir, volume incident naik dua kali lipat."),
                ("Alex", "Fine. What's your proposal?", "Oke. Proposal kamu apa?"),
                ("Mina", "We run a pilot this week and review results before scaling.", "Kita jalankan pilot minggu ini dan review hasil sebelum scaling."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let me be clear: we have indicators, not proof yet.",
                    "meaning_id": "Biar jelas: kita punya indikator, belum bukti.",
                    "usage_note": "Calmly clarify what you know.",
                    "common_mistake": "Do not overclaim; be explicit about limits.",
                },
                {
                    "phrase": "I understand the concern. However, the key point is that waiting increases risk.",
                    "meaning_id": "Aku paham concern-nya. Tapi poin kuncinya: menunggu meningkatkan risiko.",
                    "usage_note": "Acknowledge then pivot to key point.",
                    "common_mistake": "Do not ignore concern; acknowledge first.",
                },
                {
                    "phrase": "If you look at the last four weeks, incident volume has doubled.",
                    "meaning_id": "Kalau lihat 4 minggu terakhir, volume incident naik dua kali lipat.",
                    "usage_note": "Use a precise reference window for evidence.",
                    "common_mistake": "Do not say it's worse; quantify it.",
                },
                {
                    "phrase": "The key point is ...",
                    "meaning_id": "Poin kuncinya adalah ...",
                    "usage_note": "Refocus under pressure.",
                    "common_mistake": "Do not add many points; focus on one.",
                },
                {
                    "phrase": "We run a pilot this week and review results before scaling.",
                    "meaning_id": "Kita pilot minggu ini dan review hasil sebelum scaling.",
                    "usage_note": "Offer a controlled next step.",
                    "common_mistake": "Do not propose a huge rollout immediately.",
                },
            ],
            "grammar_md": [
                ("Clarity under pressure", ["Let me be clear: ...", "The key point is ..."]),
                ("Acknowledge + pivot", ["I understand the concern. However, ...", "If you look at ..., ..."]),
            ],
            "pronunciation": [
                ("speculation", "spek-yuh-LAY-shun."),
                ("indicators", "IN-di-kay-terz."),
                ("doubled", "DUB-uhld."),
            ],
            "response_prompts": [
                {
                    "prompt": "Clarify calmly under pressure.",
                    "target_response": "Let me be clear: we have indicators, not proof yet.",
                    "acceptable_variations": [
                        "Let me be clear: we have indicators, not proof yet.",
                        "Let me be clear: we have signals, not proof yet.",
                    ],
                },
                {
                    "prompt": "Acknowledge concern and pivot.",
                    "target_response": "I understand the concern. However, the key point is that waiting increases risk.",
                    "acceptable_variations": [
                        "I understand the concern. However, the key point is that waiting increases risk.",
                        "I understand the concern. However, the key point is that delays increase risk.",
                    ],
                },
                {
                    "prompt": "Cite a time window with a metric.",
                    "target_response": "If you look at the last four weeks, incident volume has doubled.",
                    "acceptable_variations": [
                        "If you look at the last four weeks, incident volume has doubled.",
                        "If you look at the last month, incidents have doubled.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "let_me_be_clear",
                    "type": "multiple_choice",
                    "prompt": "Which phrase clarifies calmly under pressure?",
                    "options": ["Let me be clear: ...", "You're wrong.", "No."],
                    "correct_answer": "Let me be clear: ...",
                },
                {
                    "key": "key_point",
                    "type": "multiple_choice",
                    "prompt": "Which phrase refocuses on the main point?",
                    "options": ["The key point is ...", "Key points are many.", "Stop."],
                    "correct_answer": "The key point is ...",
                },
                {
                    "key": "doubled_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "doubled" mean?',
                    "options": ["naik dua kali lipat", "turun setengah", "tetap sama"],
                    "correct_answer": "naik dua kali lipat",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_under_pressure",
                "opening_line": "This is just speculation. Do you have anything solid?",
                "learner_goal": "Stay calm under pressure, clarify limits, cite evidence, and propose a controlled next step.",
                "turns": [
                    {
                        "coach": "This is just speculation. Do you have anything solid?",
                        "hint": "Clarify calmly: indicators, not proof.",
                        "sample_answer": "Let me be clear: we have indicators, not proof yet.",
                        "focus": "Clarity",
                        "expected_keywords": ["be clear", "indicators", "not proof"],
                    },
                    {
                        "coach": "So why should we act now?",
                        "hint": "Acknowledge + key point.",
                        "sample_answer": "I understand the concern. However, the key point is that waiting increases risk.",
                        "focus": "Key point",
                        "expected_keywords": ["understand", "however", "key point"],
                    },
                    {
                        "coach": "Show me the numbers and propose next step.",
                        "hint": "If you look at... doubled... pilot...",
                        "sample_answer": "If you look at the last four weeks, incident volume has doubled. We run a pilot this week and review results before scaling.",
                        "focus": "Evidence + proposal",
                        "expected_keywords": ["last four weeks", "doubled", "pilot"],
                    },
                ],
                "target_phrases": ["Let me be clear: ...", "I understand the concern. However, ...", "If you look at ..."],
            },
            "reading_support": "Under pressure, clarity and tone matter. Be explicit about what you know and what you don't, cite a concrete time window for evidence, then propose a controlled next step like a pilot.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. Let me be clear: ...",
                "2. We have indicators, not proof yet.",
                "3. I understand the concern.",
                "4. However, the key point is ...",
                "5. If you look at ...",
                "6. Over the last ... weeks, ...",
                "7. That suggests ...",
                "8. So I propose ...",
                "9. We'll run a pilot ...",
                "10. Then review results before scaling.",
            ],
            "goal_examples": ["Let me be clear: ...", "The key point is ...", "If you look at ..."],
        },
        {
            "lesson_key": "lesson-05-debate-analysis-mission",
            "slug": "debate-analysis-mission",
            "title": "Debate Analysis Mission",
            "conversation_situation": "mission_debate_analysis",
            "conversation_goal": "Lead a debate-style discussion: identify assumptions, challenge claims, present evidence, and respond under pressure.",
            "grammar_summary": "Combine assumption language, evidence framing, and pressure responses into one coherent mission conversation.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Misi: kamu memimpin diskusi debat yang realistis. Kamu angkat asumsi, uji logika, bawa evidence, dan tetap calm saat ditekan.",
            "dialogue": [
                ("Alex", "We should cut onboarding steps. Fewer steps always increase conversion."),
                ("Mina", "It seems you're assuming fewer steps automatically mean better conversion. What's the evidence for that claim?"),
                ("Alex", "It's common sense."),
                ("Mina", "I'm not sure that follows. Could there be another explanation, like unclear copy or missing reassurance?"),
                ("Alex", "Do we have data?"),
                ("Mina", "According to the support dashboard, drop-offs increased after the redesign. To be precise, the data indicates correlation, not necessarily causation."),
                ("Alex", "This is speculation. Why act now?"),
                ("Mina", "Let me be clear: we have indicators, not proof yet. However, the key point is waiting increases risk. We run a pilot this week and review results before scaling."),
            ],
            "translations": [
                ("Alex", "We should cut onboarding steps. Fewer steps always increase conversion.", "Kita harus potong step onboarding. Step lebih sedikit selalu bikin conversion naik."),
                ("Mina", "It seems you're assuming fewer steps automatically mean better conversion. What's the evidence for that claim?", "Sepertinya kamu berasumsi step lebih sedikit otomatis bikin conversion lebih bagus. Evidence-nya apa untuk claim itu?"),
                ("Alex", "It's common sense.", "Itu common sense."),
                ("Mina", "I'm not sure that follows. Could there be another explanation, like unclear copy or missing reassurance?", "Aku nggak yakin itu nyambung. Bisa nggak ada penjelasan lain, misalnya copy nggak jelas atau reassurance kurang?"),
                ("Alex", "Do we have data?", "Kita punya data nggak?"),
                ("Mina", "According to the support dashboard, drop-offs increased after the redesign. To be precise, the data indicates correlation, not necessarily causation.", "Menurut dashboard support, drop-off naik setelah redesign. Biar presisi, itu korelasi, belum tentu kausalitas."),
                ("Alex", "This is speculation. Why act now?", "Ini spekulasi. Kenapa harus bertindak sekarang?"),
                ("Mina", "Let me be clear: we have indicators, not proof yet. However, the key point is waiting increases risk. We run a pilot this week and review results before scaling.", "Biar jelas: kita punya indikator, belum bukti. Tapi poin kuncinya: menunggu meningkatkan risiko. Kita pilot minggu ini dan review sebelum scaling."),
            ],
            "useful_phrases": [
                {
                    "phrase": "It seems you're assuming ... What's the evidence for that claim?",
                    "meaning_id": "Sepertinya kamu berasumsi ... Evidence-nya apa untuk claim itu?",
                    "usage_note": "Assumption + evidence challenge.",
                    "common_mistake": "Don't attack the person; focus on claim and evidence.",
                },
                {
                    "phrase": "I'm not sure that follows. Could there be another explanation?",
                    "meaning_id": "Aku nggak yakin itu nyambung. Bisa nggak ada penjelasan lain?",
                    "usage_note": "Challenge logic + propose alternative.",
                    "common_mistake": "Don't be dismissive; explore alternatives.",
                },
                {
                    "phrase": "To be precise, the data indicates correlation, not necessarily causation.",
                    "meaning_id": "Biar presisi, data menunjukkan korelasi, belum tentu kausalitas.",
                    "usage_note": "Precision in evidence.",
                    "common_mistake": "Don't claim causation from correlation.",
                },
                {
                    "phrase": "Let me be clear: we have indicators, not proof yet.",
                    "meaning_id": "Biar jelas: kita punya indikator, belum bukti.",
                    "usage_note": "Stay calm under pressure.",
                    "common_mistake": "Don't overclaim; clarify limits.",
                },
                {
                    "phrase": "However, the key point is ...",
                    "meaning_id": "Tapi poin kuncinya adalah ...",
                    "usage_note": "Refocus to the core point.",
                    "common_mistake": "Don't add multiple points; keep one core point.",
                },
            ],
            "grammar_md": [
                (
                    "Debate analysis toolkit",
                    [
                        "It seems you're assuming ...",
                        "I'm not sure that follows. What's the evidence for ...?",
                        "Could there be another explanation?",
                        "According to ... To be precise, ...",
                        "Let me be clear: ... However, the key point is ...",
                    ],
                )
            ],
            "pronunciation": [
                ("analysis", "uh-NAL-uh-sis."),
                ("inference", "IN-fer-ens."),
                ("bias", "BY-us."),
            ],
            "response_prompts": [
                {
                    "prompt": "Challenge assumption and ask for evidence.",
                    "target_response": "It seems you're assuming fewer steps automatically mean better conversion. What's the evidence for that claim?",
                    "acceptable_variations": [
                        "It seems you're assuming fewer steps automatically mean better conversion. What's the evidence for that claim?",
                        "It seems you're assuming speed is the main driver. What's the evidence for that?",
                    ],
                },
                {
                    "prompt": "Present evidence with precision.",
                    "target_response": "According to the dashboard, drop-offs increased after the redesign. To be precise, the data indicates correlation, not necessarily causation.",
                    "acceptable_variations": [
                        "According to the dashboard, drop-offs increased after the redesign. To be precise, the data indicates correlation, not necessarily causation.",
                        "According to the logs, errors increased after the release. To be precise, that's correlation, not causation.",
                    ],
                },
                {
                    "prompt": "Respond under pressure with a controlled plan.",
                    "target_response": "Let me be clear: we have indicators, not proof yet. However, the key point is waiting increases risk. We run a pilot this week and review results before scaling.",
                    "acceptable_variations": [
                        "Let me be clear: we have indicators, not proof yet. However, the key point is waiting increases risk. We run a pilot this week and review results before scaling.",
                        "Let me be clear: we have signals, not proof. The key point is risk grows over time, so we should pilot now.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "debate_flow",
                    "type": "multiple_choice",
                    "prompt": "Which flow fits debate analysis?",
                    "options": [
                        "Assumptions -> evidence -> alternatives -> response under pressure",
                        "Greeting -> goodbye",
                        "Colors -> numbers",
                    ],
                    "correct_answer": "Assumptions -> evidence -> alternatives -> response under pressure",
                },
                {
                    "key": "correlation",
                    "type": "multiple_choice",
                    "prompt": "Which phrase shows precision about data?",
                    "options": [
                        "The data indicates correlation, not necessarily causation.",
                        "The data proves everything.",
                        "No data needed.",
                    ],
                    "correct_answer": "The data indicates correlation, not necessarily causation.",
                },
                {
                    "key": "under_pressure",
                    "type": "multiple_choice",
                    "prompt": "Which phrase stays calm under pressure?",
                    "options": ["Let me be clear: ...", "You're attacking me.", "Stop."],
                    "correct_answer": "Let me be clear: ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_debate_mission",
                "opening_line": "We should cut onboarding steps to increase conversion.",
                "learner_goal": "Lead a debate-style discussion with assumptions, evidence, and calm responses under pressure.",
                "turns": [
                    {
                        "coach": "Challenge the claim by surfacing an assumption and asking for evidence.",
                        "hint": "It seems you're assuming... What's the evidence for...?",
                        "sample_answer": "It seems you're assuming fewer steps automatically mean better conversion. What's the evidence for that claim?",
                        "focus": "Assumption + evidence",
                        "expected_keywords": ["assuming", "evidence"],
                    },
                    {
                        "coach": "Present evidence carefully and be precise about what it shows.",
                        "hint": "According to... To be precise...",
                        "sample_answer": "According to the support dashboard, drop-offs increased after the redesign. To be precise, the data indicates correlation, not necessarily causation.",
                        "focus": "Evidence + precision",
                        "expected_keywords": ["according to", "precise", "correlation"],
                    },
                    {
                        "coach": "Respond under pressure and propose a controlled next step.",
                        "hint": "Let me be clear... key point... pilot...",
                        "sample_answer": "Let me be clear: we have indicators, not proof yet. However, the key point is waiting increases risk. We run a pilot this week and review results before scaling.",
                        "focus": "Pressure response",
                        "expected_keywords": ["be clear", "key point", "pilot"],
                    },
                ],
                "target_phrases": ["It seems you're assuming ...", "According to ...", "Let me be clear: ..."],
            },
            "reading_support": "Debate analysis at C1 means you can challenge ideas without conflict: surface assumptions, ask for evidence, propose alternatives, present data precisely, and stay calm under pressure with a controlled plan.",
            "writing_support_lines": [
                "Write your mission (12 lines):",
                "1. It seems you're assuming ...",
                "2. What's the evidence for ...?",
                "3. I'm not sure that follows.",
                "4. Could there be another explanation?",
                "5. According to ...",
                "6. To be precise, ...",
                "7. The data indicates ...",
                "8. Let me be clear: ...",
                "9. However, the key point is ...",
                "10. If you look at ...",
                "11. So I propose ...",
                "12. We'll run a pilot and review results.",
            ],
            "goal_examples": ["It seems you're assuming ...", "According to ...", "Let me be clear: ..."],
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

