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
            "- Tone: confident, precise, professional",
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

        Read it again and underline the presentation signposts (today I'd like to..., first..., next..., that brings me to..., in short..., I'd like to end by...).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "C1"
    root = Path("content/curriculum/english/C1")
    units_root = root / "units"
    unit_key = "unit-03-advanced-presentations"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-03-advanced-presentations
            level_code: C1
            title: Advanced Presentations
            main_conversation_outcome: Present complex ideas and handle challenging questions.
            status: in_production
            lessons:
              - lesson-01-framing-a-complex-topic
              - lesson-02-building-a-persuasive-flow
              - lesson-03-using-precise-transitions
              - lesson-04-handling-challenging-questions
              - lesson-05-advanced-presentation-mission
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
            "lesson_key": "lesson-01-framing-a-complex-topic",
            "slug": "framing-a-complex-topic",
            "title": "Framing a Complex Topic",
            "conversation_situation": "framing_complex_topic",
            "conversation_goal": "Frame a complex topic by setting context, defining terms, and stating the purpose clearly.",
            "grammar_summary": "Use Today I'd like to... / By X, I mean... / The purpose of this is... to frame complex topics.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu presentasi topik kompleks. Kamu mulai dengan konteks, definisi istilah, dan tujuan supaya audiens nggak kehilangan arah.",
            "dialogue": [
                ("Alex", "Can you present the new architecture proposal?"),
                ("Mina", "Sure. Today I'd like to walk you through the proposal and why it matters."),
                ("Alex", "What's the key concept?"),
                ("Mina", "By 'modular architecture', I mean we separate features into independent components."),
                ("Alex", "And the purpose?"),
                ("Mina", "The purpose of this is to reduce coupling and speed up delivery."),
                ("Alex", "What should we focus on first?"),
                ("Mina", "First, I'll outline the problem we're solving, then the proposed approach."),
            ],
            "translations": [
                ("Alex", "Can you present the new architecture proposal?", "Bisa present proposal arsitektur yang baru?"),
                ("Mina", "Sure. Today I'd like to walk you through the proposal and why it matters.", "Oke. Hari ini aku mau jelasin proposalnya dan kenapa ini penting."),
                ("Alex", "What's the key concept?", "Konsep kuncinya apa?"),
                ("Mina", "By 'modular architecture', I mean we separate features into independent components.", "Dengan 'arsitektur modular', maksudku kita pisahin fitur jadi komponen yang independen."),
                ("Alex", "And the purpose?", "Tujuannya apa?"),
                ("Mina", "The purpose of this is to reduce coupling and speed up delivery.", "Tujuannya untuk ngurangin coupling dan mempercepat delivery."),
                ("Alex", "What should we focus on first?", "Pertama fokus ke apa?"),
                ("Mina", "First, I'll outline the problem we're solving, then the proposed approach.", "Pertama aku jelasin problemnya, lalu approach yang diusulkan."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Today I'd like to walk you through the proposal and why it matters.",
                    "meaning_id": "Hari ini aku mau jelasin proposalnya dan kenapa ini penting.",
                    "usage_note": "A clear opener that sets purpose.",
                    "common_mistake": "Do not start without context; state what you will cover.",
                },
                {
                    "phrase": "By 'modular architecture', I mean we separate features into independent components.",
                    "meaning_id": "Dengan 'arsitektur modular', maksudku kita pisahin fitur jadi komponen independen.",
                    "usage_note": "Define terms precisely.",
                    "common_mistake": "Do not assume everyone knows the term; define it.",
                },
                {
                    "phrase": "The purpose of this is to reduce coupling and speed up delivery.",
                    "meaning_id": "Tujuannya untuk ngurangin coupling dan mempercepat delivery.",
                    "usage_note": "State purpose in one sentence.",
                    "common_mistake": "Do not list too many purposes; keep it focused.",
                },
                {
                    "phrase": "First, I'll outline the problem we're solving, then the proposed approach.",
                    "meaning_id": "Pertama aku jelasin problemnya, lalu approach yang diusulkan.",
                    "usage_note": "Preview structure with signposting.",
                    "common_mistake": "Do not jump around; preview the structure.",
                },
                {
                    "phrase": "Let me define what I mean by ...",
                    "meaning_id": "Biar jelas, aku definisikan dulu maksudku dengan ...",
                    "usage_note": "A softer definition starter.",
                    "common_mistake": "Do not over-apologize; just define.",
                },
            ],
            "grammar_md": [
                ("Presentation framing", ["Today I'd like to ...", "The purpose of this is to ..."]),
                ("Definitions", ["By X, I mean ...", "Let me define what I mean by ..."]),
            ],
            "pronunciation": [
                ("architecture", "ARK-ih-tek-cher."),
                ("modular", "MOD-yuh-ler."),
                ("coupling", "KUP-ling."),
            ],
            "response_prompts": [
                {
                    "prompt": "Open your presentation clearly.",
                    "target_response": "Today I'd like to walk you through the proposal and why it matters.",
                    "acceptable_variations": [
                        "Today I'd like to walk you through the proposal and why it matters.",
                        "Today I'd like to outline the proposal and why it matters.",
                    ],
                },
                {
                    "prompt": "Define a key term precisely.",
                    "target_response": "By 'modular architecture', I mean we separate features into independent components.",
                    "acceptable_variations": [
                        "By 'modular architecture', I mean we separate features into independent components.",
                        "By 'modular design', I mean we break the system into independent parts.",
                    ],
                },
                {
                    "prompt": "Preview the structure with signposting.",
                    "target_response": "First, I'll outline the problem we're solving, then the proposed approach.",
                    "acceptable_variations": [
                        "First, I'll outline the problem we're solving, then the proposed approach.",
                        "First, I'll give context, then I'll explain the approach.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "walk_through",
                    "type": "multiple_choice",
                    "prompt": "Which phrase is a good presentation opener?",
                    "options": ["Today I'd like to walk you through ...", "Stop.", "No idea."],
                    "correct_answer": "Today I'd like to walk you through ...",
                },
                {
                    "key": "define_term",
                    "type": "multiple_choice",
                    "prompt": "Which phrase defines a term precisely?",
                    "options": ["By X, I mean ...", "X is cool.", "Whatever."],
                    "correct_answer": "By X, I mean ...",
                },
                {
                    "key": "purpose_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase states purpose clearly?",
                    "options": ["The purpose of this is to ...", "Purpose is ...ing.", "No purpose."],
                    "correct_answer": "The purpose of this is to ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_presentation_framing",
                "opening_line": "Can you present the proposal?",
                "learner_goal": "Frame a complex topic with context, definition, and purpose.",
                "turns": [
                    {
                        "coach": "Can you present the proposal?",
                        "hint": "Start with Today I'd like to...",
                        "sample_answer": "Sure. Today I'd like to walk you through the proposal and why it matters.",
                        "focus": "Opener",
                        "expected_keywords": ["today", "walk you through", "matters"],
                    },
                    {
                        "coach": "Define the key term clearly.",
                        "hint": "By X, I mean...",
                        "sample_answer": "By 'modular architecture', I mean we separate features into independent components.",
                        "focus": "Definition",
                        "expected_keywords": ["by", "i mean", "independent"],
                    },
                    {
                        "coach": "State the purpose and preview the structure.",
                        "hint": "The purpose of this is... First, I'll...",
                        "sample_answer": "The purpose of this is to reduce coupling and speed up delivery. First, I'll outline the problem, then the proposed approach.",
                        "focus": "Purpose + structure",
                        "expected_keywords": ["purpose", "first", "then"],
                    },
                ],
                "target_phrases": ["Today I'd like to ...", "By X, I mean ...", "The purpose of this is to ..."],
            },
            "reading_support": "When presenting a complex topic, start by framing: state what you will cover, define key terms, and explain why it matters. A clear structure reduces confusion and increases trust.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. Today I'd like to ...",
                "2. The purpose of this is to ...",
                "3. By X, I mean ...",
                "4. In short, ...",
                "5. First, ...",
                "6. Next, ...",
                "7. That brings me to ...",
                "8. Finally, ...",
                "9. I'd like to end by ...",
                "10. Any questions?",
            ],
            "goal_examples": ["Today I'd like to ...", "By X, I mean ...", "The purpose of this is to ..."],
        },
        {
            "lesson_key": "lesson-02-building-a-persuasive-flow",
            "slug": "building-a-persuasive-flow",
            "title": "Building a Persuasive Flow",
            "conversation_situation": "persuasive_presentation_flow",
            "conversation_goal": "Build a persuasive flow by stating a claim, supporting it with evidence, and addressing counterarguments.",
            "grammar_summary": "Use The core claim is... / The evidence suggests... / A common concern is... / That said... to build persuasion.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu presentasi dengan tujuan meyakinkan. Kamu harus runtut: claim, evidence, counterpoint, lalu conclusion.",
            "dialogue": [
                ("Alex", "What's the main argument for the proposal?"),
                ("Mina", "The core claim is that modularization will improve delivery speed."),
                ("Alex", "What's the evidence?"),
                ("Mina", "The evidence suggests teams ship faster when ownership is clear."),
                ("Alex", "What about the risk of fragmentation?"),
                ("Mina", "A common concern is fragmentation. That said, shared standards can mitigate it."),
                ("Alex", "How do you conclude?"),
                ("Mina", "In short, the benefits outweigh the risks if we set guardrails early."),
            ],
            "translations": [
                ("Alex", "What's the main argument for the proposal?", "Argumen utama proposal ini apa?"),
                ("Mina", "The core claim is that modularization will improve delivery speed.", "Claim utamanya: modularisasi akan mempercepat delivery."),
                ("Alex", "What's the evidence?", "Buktinya apa?"),
                ("Mina", "The evidence suggests teams ship faster when ownership is clear.", "Evidence-nya menunjukkan tim ship lebih cepat saat ownership jelas."),
                ("Alex", "What about the risk of fragmentation?", "Gimana dengan risiko fragmentasi?"),
                ("Mina", "A common concern is fragmentation. That said, shared standards can mitigate it.", "Concern umum adalah fragmentasi. Tapi, standard bersama bisa mitigasi itu."),
                ("Alex", "How do you conclude?", "Kesimpulannya gimana?"),
                ("Mina", "In short, the benefits outweigh the risks if we set guardrails early.", "Singkatnya, benefit lebih besar dari risiko kalau kita set guardrails dari awal."),
            ],
            "useful_phrases": [
                {
                    "phrase": "The core claim is that modularization will improve delivery speed.",
                    "meaning_id": "Claim utamanya: modularisasi akan mempercepat delivery.",
                    "usage_note": "State your main claim clearly.",
                    "common_mistake": "Do not bury the claim; say it upfront.",
                },
                {
                    "phrase": "The evidence suggests teams ship faster when ownership is clear.",
                    "meaning_id": "Evidence menunjukkan tim ship lebih cepat saat ownership jelas.",
                    "usage_note": "Evidence language without overclaiming.",
                    "common_mistake": "Do not say evidence prove; use suggests.",
                },
                {
                    "phrase": "A common concern is fragmentation.",
                    "meaning_id": "Concern umum adalah fragmentasi.",
                    "usage_note": "Introduce counterargument respectfully.",
                    "common_mistake": "Do not dismiss concerns; name them.",
                },
                {
                    "phrase": "That said, shared standards can mitigate it.",
                    "meaning_id": "Tapi, standard bersama bisa mitigasi itu.",
                    "usage_note": "Respond to concern with mitigation.",
                    "common_mistake": "Do not hand-wave; mention a concrete mitigation.",
                },
                {
                    "phrase": "In short, the benefits outweigh the risks.",
                    "meaning_id": "Singkatnya, benefit lebih besar dari risiko.",
                    "usage_note": "Concise conclusion.",
                    "common_mistake": "Do not conclude without connecting to evidence.",
                },
            ],
            "grammar_md": [
                ("Claims + evidence", ["The core claim is that ...", "The evidence suggests ..."]),
                ("Counterarguments", ["A common concern is ...", "That said, ..."]),
            ],
            "pronunciation": [
                ("persuasive", "per-SWAY-siv."),
                ("evidence", "EV-uh-dens."),
                ("fragmentation", "frag-men-TAY-shun."),
            ],
            "response_prompts": [
                {
                    "prompt": "State your core claim.",
                    "target_response": "The core claim is that modularization will improve delivery speed.",
                    "acceptable_variations": [
                        "The core claim is that modularization will improve delivery speed.",
                        "The core claim is that this approach will reduce cycle time.",
                    ],
                },
                {
                    "prompt": "Use evidence language with suggests.",
                    "target_response": "The evidence suggests teams ship faster when ownership is clear.",
                    "acceptable_variations": [
                        "The evidence suggests teams ship faster when ownership is clear.",
                        "The evidence suggests this reduces coordination overhead.",
                    ],
                },
                {
                    "prompt": "Address a concern with mitigation.",
                    "target_response": "A common concern is fragmentation. That said, shared standards can mitigate it.",
                    "acceptable_variations": [
                        "A common concern is fragmentation. That said, shared standards can mitigate it.",
                        "A common concern is complexity. That said, clear documentation can mitigate it.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "core_claim",
                    "type": "multiple_choice",
                    "prompt": "Which phrase states a main claim?",
                    "options": ["The core claim is that ...", "Core claim I ...", "No claim."],
                    "correct_answer": "The core claim is that ...",
                },
                {
                    "key": "evidence_suggests",
                    "type": "multiple_choice",
                    "prompt": "Which phrase expresses evidence carefully?",
                    "options": ["The evidence suggests ...", "The evidence proves ... always.", "No evidence."],
                    "correct_answer": "The evidence suggests ...",
                },
                {
                    "key": "outweigh_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "outweigh" mean?',
                    "options": ["lebih besar/lebih kuat daripada", "lebih kecil", "tidak relevan"],
                    "correct_answer": "lebih besar/lebih kuat daripada",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_persuasive_flow",
                "opening_line": "What's the main argument for this proposal?",
                "learner_goal": "Deliver a persuasive flow: claim, evidence, concern, mitigation, conclusion.",
                "turns": [
                    {
                        "coach": "What's the main argument for this proposal?",
                        "hint": "Start with The core claim is...",
                        "sample_answer": "The core claim is that modularization will improve delivery speed.",
                        "focus": "Claim",
                        "expected_keywords": ["core claim"],
                    },
                    {
                        "coach": "What's the evidence?",
                        "hint": "Use The evidence suggests...",
                        "sample_answer": "The evidence suggests teams ship faster when ownership is clear.",
                        "focus": "Evidence",
                        "expected_keywords": ["evidence suggests"],
                    },
                    {
                        "coach": "Address a concern and conclude.",
                        "hint": "A common concern is... That said... In short...",
                        "sample_answer": "A common concern is fragmentation. That said, shared standards can mitigate it. In short, the benefits outweigh the risks if we set guardrails early.",
                        "focus": "Concern + conclusion",
                        "expected_keywords": ["concern", "that said", "in short"],
                    },
                ],
                "target_phrases": ["The core claim is that ...", "The evidence suggests ...", "A common concern is ..."],
            },
            "reading_support": "A persuasive flow is structured: state your claim, give evidence, acknowledge a concern, explain mitigation, then conclude. This helps you sound confident without sounding biased.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. The core claim is that ...",
                "2. The evidence suggests ...",
                "3. For example, ...",
                "4. A common concern is ...",
                "5. That said, ...",
                "6. We can mitigate it by ...",
                "7. In short, ...",
                "8. The benefits outweigh the risks ...",
                "9. If we ...",
                "10. Any questions?",
            ],
            "goal_examples": ["The core claim is that ...", "The evidence suggests ...", "A common concern is ..."],
        },
        {
            "lesson_key": "lesson-03-using-precise-transitions",
            "slug": "using-precise-transitions",
            "title": "Using Precise Transitions",
            "conversation_situation": "precise_transitions",
            "conversation_goal": "Use precise transitions to guide listeners through complex ideas smoothly.",
            "grammar_summary": "Use That brings me to... / What's crucial here is... / To put it differently... / With that in mind... to transition clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu menjelaskan ide yang panjang. Kamu perlu transisi yang rapi supaya audiens bisa ngikutin alurnya.",
            "dialogue": [
                ("Alex", "Your explanation is clear so far. What's next?"),
                ("Mina", "That brings me to the key trade-off: speed versus reliability."),
                ("Alex", "What's crucial here?"),
                ("Mina", "What's crucial here is that we set clear standards early."),
                ("Alex", "Can you restate it?"),
                ("Mina", "To put it differently, standards let teams move fast without breaking consistency."),
                ("Alex", "So what should we do?"),
                ("Mina", "With that in mind, I'd propose a pilot with strict guardrails."),
            ],
            "translations": [
                ("Alex", "Your explanation is clear so far. What's next?", "Penjelasan kamu sejauh ini jelas. Next apa?"),
                ("Mina", "That brings me to the key trade-off: speed versus reliability.", "Itu membawa kita ke trade-off utama: speed versus reliability."),
                ("Alex", "What's crucial here?", "Yang krusial di sini apa?"),
                ("Mina", "What's crucial here is that we set clear standards early.", "Yang krusial adalah kita set standar yang jelas dari awal."),
                ("Alex", "Can you restate it?", "Bisa ulang dengan cara lain?"),
                ("Mina", "To put it differently, standards let teams move fast without breaking consistency.", "Dengan kata lain, standar bikin tim bisa cepat tanpa merusak konsistensi."),
                ("Alex", "So what should we do?", "Jadi kita harus ngapain?"),
                ("Mina", "With that in mind, I'd propose a pilot with strict guardrails.", "Dengan itu, aku usul pilot dengan guardrails yang ketat."),
            ],
            "useful_phrases": [
                {
                    "phrase": "That brings me to the key trade-off: speed versus reliability.",
                    "meaning_id": "Itu membawa kita ke trade-off utama: speed versus reliability.",
                    "usage_note": "Transition to a new section.",
                    "common_mistake": "Do not jump abruptly; use a transition phrase.",
                },
                {
                    "phrase": "What's crucial here is that we set clear standards early.",
                    "meaning_id": "Yang krusial adalah kita set standar yang jelas dari awal.",
                    "usage_note": "Highlight the key point.",
                    "common_mistake": "Do not bury the key point; signal it as crucial.",
                },
                {
                    "phrase": "To put it differently, ...",
                    "meaning_id": "Dengan kata lain, ...",
                    "usage_note": "Restate a point for clarity.",
                    "common_mistake": "Do not repeat the same words; rephrase.",
                },
                {
                    "phrase": "With that in mind, I'd propose ...",
                    "meaning_id": "Dengan itu, aku usul ...",
                    "usage_note": "Link reasoning to a proposal.",
                    "common_mistake": "Do not propose without linking; use with that in mind.",
                },
                {
                    "phrase": "Let me connect this to ...",
                    "meaning_id": "Biar aku hubungkan ini ke ...",
                    "usage_note": "Another transition option.",
                    "common_mistake": "Do not overuse; pick one transition per move.",
                },
            ],
            "grammar_md": [
                ("Transitions", ["That brings me to ...", "With that in mind, ..."]),
                ("Clarification", ["What's crucial here is ...", "To put it differently, ..."]),
            ],
            "pronunciation": [
                ("crucial", "KROO-shuhl."),
                ("consistency", "kun-SIS-ten-see."),
                ("guardrails", "GARD-raylz."),
            ],
            "response_prompts": [
                {
                    "prompt": "Transition to a trade-off.",
                    "target_response": "That brings me to the key trade-off: speed versus reliability.",
                    "acceptable_variations": [
                        "That brings me to the key trade-off: speed versus reliability.",
                        "That brings me to the next point: the trade-off between speed and reliability.",
                    ],
                },
                {
                    "prompt": "Highlight a key point as crucial.",
                    "target_response": "What's crucial here is that we set clear standards early.",
                    "acceptable_variations": [
                        "What's crucial here is that we set clear standards early.",
                        "What's crucial here is that we define guardrails up front.",
                    ],
                },
                {
                    "prompt": "Restate with to put it differently.",
                    "target_response": "To put it differently, standards let teams move fast without breaking consistency.",
                    "acceptable_variations": [
                        "To put it differently, standards let teams move fast without breaking consistency.",
                        "To put it differently, guardrails prevent chaos while we move fast.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "transition_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase transitions to a new point?",
                    "options": ["That brings me to ...", "Because.", "No."],
                    "correct_answer": "That brings me to ...",
                },
                {
                    "key": "restate_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase restates an idea?",
                    "options": ["To put it differently, ...", "Anyway.", "Stop."],
                    "correct_answer": "To put it differently, ...",
                },
                {
                    "key": "crucial_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "crucial" mean?',
                    "options": ["sangat penting", "opsional", "tidak relevan"],
                    "correct_answer": "sangat penting",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_precise_transitions",
                "opening_line": "Your explanation is clear so far. What's next?",
                "learner_goal": "Use transitions to guide listeners through complex ideas smoothly.",
                "turns": [
                    {
                        "coach": "Your explanation is clear so far. What's next?",
                        "hint": "Use That brings me to...",
                        "sample_answer": "That brings me to the key trade-off: speed versus reliability.",
                        "focus": "Transition",
                        "expected_keywords": ["brings me to", "trade-off"],
                    },
                    {
                        "coach": "Highlight the key point.",
                        "hint": "What's crucial here is...",
                        "sample_answer": "What's crucial here is that we set clear standards early.",
                        "focus": "Key point",
                        "expected_keywords": ["crucial", "standards"],
                    },
                    {
                        "coach": "Restate it and propose a next step.",
                        "hint": "To put it differently... With that in mind...",
                        "sample_answer": "To put it differently, standards let teams move fast without breaking consistency. With that in mind, I'd propose a pilot with strict guardrails.",
                        "focus": "Restate + propose",
                        "expected_keywords": ["differently", "with that in mind", "pilot"],
                    },
                ],
                "target_phrases": ["That brings me to ...", "What's crucial here is ...", "To put it differently, ..."],
            },
            "reading_support": "Transitions are a C1-level tool for clarity. Use them to connect points, highlight what's crucial, and restate ideas in simpler terms before moving to a proposal.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. That brings me to ...",
                "2. What's crucial here is ...",
                "3. To put it differently, ...",
                "4. In other words, ...",
                "5. With that in mind, ...",
                "6. Let me connect this to ...",
                "7. That leads to ...",
                "8. As a result, ...",
                "9. Finally, ...",
                "10. Any questions?",
            ],
            "goal_examples": ["That brings me to ...", "What's crucial here is ...", "With that in mind, ..."],
        },
        {
            "lesson_key": "lesson-04-handling-challenging-questions",
            "slug": "handling-challenging-questions",
            "title": "Handling Challenging Questions",
            "conversation_situation": "challenging_questions",
            "conversation_goal": "Handle challenging questions by acknowledging concerns, answering precisely, and reframing when needed.",
            "grammar_summary": "Use That's a fair question... / Let me clarify... / The short answer is... / What I'd emphasize is... to handle questions.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Saat Q&A, kamu dapat pertanyaan menantang. Kamu harus tetap tenang, jawab presisi, dan bisa reframe kalau perlu.",
            "dialogue": [
                ("Alex", "Isn't this approach too risky?"),
                ("Mina", "That's a fair question. Let me clarify what risk we're accepting."),
                ("Alex", "Okay."),
                ("Mina", "The short answer is: it's manageable if we pilot first and monitor closely."),
                ("Alex", "What if teams ignore standards?"),
                ("Mina", "What I'd emphasize is that standards need ownership and enforcement."),
                ("Alex", "So what's the fallback?"),
                ("Mina", "If adoption stalls, we pause expansion and revisit the design."),
            ],
            "translations": [
                ("Alex", "Isn't this approach too risky?", "Bukannya approach ini terlalu risky?"),
                ("Mina", "That's a fair question. Let me clarify what risk we're accepting.", "Pertanyaan yang fair. Biar aku jelasin risiko apa yang kita terima."),
                ("Alex", "Okay.", "Oke."),
                ("Mina", "The short answer is: it's manageable if we pilot first and monitor closely.", "Jawaban singkatnya: ini bisa di-manage kalau kita pilot dulu dan monitor ketat."),
                ("Alex", "What if teams ignore standards?", "Kalau tim mengabaikan standar gimana?"),
                ("Mina", "What I'd emphasize is that standards need ownership and enforcement.", "Yang perlu aku tekankan: standar butuh ownership dan enforcement."),
                ("Alex", "So what's the fallback?", "Jadi fallback-nya apa?"),
                ("Mina", "If adoption stalls, we pause expansion and revisit the design.", "Kalau adoption mandek, kita stop ekspansi dan evaluasi desainnya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "That's a fair question.",
                    "meaning_id": "Pertanyaan yang fair.",
                    "usage_note": "A calm acknowledgement before answering.",
                    "common_mistake": "Do not get defensive; acknowledge first.",
                },
                {
                    "phrase": "Let me clarify what risk we're accepting.",
                    "meaning_id": "Biar aku jelasin risiko apa yang kita terima.",
                    "usage_note": "Clarify the scope of the question.",
                    "common_mistake": "Do not answer vaguely; clarify the risk.",
                },
                {
                    "phrase": "The short answer is: it's manageable if we pilot first and monitor closely.",
                    "meaning_id": "Jawaban singkatnya: bisa di-manage kalau pilot dulu dan monitor ketat.",
                    "usage_note": "Concise answer with condition.",
                    "common_mistake": "Do not give a long answer; start with short answer.",
                },
                {
                    "phrase": "What I'd emphasize is that standards need ownership and enforcement.",
                    "meaning_id": "Yang aku tekankan: standar butuh ownership dan enforcement.",
                    "usage_note": "Reframe to the key point.",
                    "common_mistake": "Do not dodge; answer then emphasize the key point.",
                },
                {
                    "phrase": "If adoption stalls, we pause expansion and revisit the design.",
                    "meaning_id": "Kalau adoption mandek, kita stop ekspansi dan evaluasi desainnya.",
                    "usage_note": "A clear fallback plan.",
                    "common_mistake": "Do not avoid risk; show fallback.",
                },
            ],
            "grammar_md": [
                ("Acknowledgement + clarity", ["That's a fair question.", "Let me clarify ..."]),
                ("Concise answers", ["The short answer is: ...", "What I'd emphasize is ..."]),
            ],
            "pronunciation": [
                ("manageable", "MAN-ih-juh-buhl."),
                ("enforcement", "en-FORS-ment."),
                ("fallback", "FAWL-bak."),
            ],
            "response_prompts": [
                {
                    "prompt": "Acknowledge a challenging question.",
                    "target_response": "That's a fair question. Let me clarify what risk we're accepting.",
                    "acceptable_variations": [
                        "That's a fair question. Let me clarify what risk we're accepting.",
                        "That's a fair question. Let me clarify what we mean by risk here.",
                    ],
                },
                {
                    "prompt": "Give a short answer with a condition.",
                    "target_response": "The short answer is: it's manageable if we pilot first and monitor closely.",
                    "acceptable_variations": [
                        "The short answer is: it's manageable if we pilot first and monitor closely.",
                        "The short answer is: yes, if we start with a pilot.",
                    ],
                },
                {
                    "prompt": "Reframe to the key point.",
                    "target_response": "What I'd emphasize is that standards need ownership and enforcement.",
                    "acceptable_variations": [
                        "What I'd emphasize is that standards need ownership and enforcement.",
                        "What I'd emphasize is that we need clear accountability.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "fair_question",
                    "type": "multiple_choice",
                    "prompt": "Which phrase acknowledges a tough question calmly?",
                    "options": ["That's a fair question.", "That's stupid.", "No."],
                    "correct_answer": "That's a fair question.",
                },
                {
                    "key": "short_answer",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a concise answer?",
                    "options": ["The short answer is: ...", "Long answer is: ...", "Whatever."],
                    "correct_answer": "The short answer is: ...",
                },
                {
                    "key": "clarify_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase clarifies before answering?",
                    "options": ["Let me clarify ...", "Stop.", "No idea."],
                    "correct_answer": "Let me clarify ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_challenging_questions",
                "opening_line": "Isn't this approach too risky?",
                "learner_goal": "Handle challenging questions with acknowledgement, concise answers, and reframing.",
                "turns": [
                    {
                        "coach": "Isn't this approach too risky?",
                        "hint": "That's a fair question... Let me clarify...",
                        "sample_answer": "That's a fair question. Let me clarify what risk we're accepting.",
                        "focus": "Acknowledge",
                        "expected_keywords": ["fair question", "clarify"],
                    },
                    {
                        "coach": "Give the short answer and condition.",
                        "hint": "The short answer is...",
                        "sample_answer": "The short answer is: it's manageable if we pilot first and monitor closely.",
                        "focus": "Short answer",
                        "expected_keywords": ["short answer", "manageable", "pilot"],
                    },
                    {
                        "coach": "Close with emphasis and a fallback plan.",
                        "hint": "What I'd emphasize... If adoption stalls...",
                        "sample_answer": "What I'd emphasize is that standards need ownership and enforcement. If adoption stalls, we pause expansion and revisit the design.",
                        "focus": "Emphasis + fallback",
                        "expected_keywords": ["emphasize", "ownership", "pause"],
                    },
                ],
                "target_phrases": ["That's a fair question.", "The short answer is: ...", "What I'd emphasize is ..."],
            },
            "reading_support": "Challenging questions test your calm and clarity. Acknowledge the question, clarify what is being asked, give a short answer, then add conditions, emphasis, and a fallback plan.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. That's a fair question.",
                "2. Let me clarify ...",
                "3. The short answer is: ...",
                "4. If we ..., then ...",
                "5. What I'd emphasize is ...",
                "6. The main risk is ...",
                "7. We can mitigate it by ...",
                "8. If adoption stalls, ...",
                "9. We'll revisit ...",
                "10. Does that address your concern?",
            ],
            "goal_examples": ["That's a fair question.", "The short answer is: ...", "What I'd emphasize is ..."],
        },
        {
            "lesson_key": "lesson-05-advanced-presentation-mission",
            "slug": "advanced-presentation-mission",
            "title": "Advanced Presentation Mission",
            "conversation_situation": "mission_advanced_presentation",
            "conversation_goal": "Deliver an advanced presentation and handle challenging questions with clear signposting and strategic answers.",
            "grammar_summary": "Combine framing, persuasive flow, transitions, and Q&A language into one smooth mission.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Misi: kamu presentasi topik kompleks dengan alur yang meyakinkan, transisi rapi, dan Q&A yang tenang.",
            "dialogue": [
                ("Alex", "Mission: present the proposal and handle questions."),
                ("Mina", "Today I'd like to walk you through the proposal and why it matters. By 'modular architecture', I mean independent components."),
                ("Alex", "What's your main claim?"),
                ("Mina", "The core claim is that this will improve delivery speed. The evidence suggests teams move faster with clear ownership."),
                ("Alex", "Isn't it too risky?"),
                ("Mina", "That's a fair question. The short answer is: it's manageable if we pilot first and monitor closely."),
                ("Alex", "So what's crucial?"),
                ("Mina", "What's crucial here is shared standards. With that in mind, I'd propose a time-boxed pilot with guardrails."),
                ("Alex", "Sounds good. Any final summary?"),
                ("Mina", "In short, the benefits outweigh the risks if we set guardrails early. Next steps are: I'll share the plan today, and you'll review it by Friday."),
            ],
            "translations": [
                ("Alex", "Mission: present the proposal and handle questions.", "Misi: present proposal dan handle pertanyaan."),
                ("Mina", "Today I'd like to walk you through the proposal and why it matters. By 'modular architecture', I mean independent components.", "Hari ini aku mau jelasin proposalnya dan kenapa ini penting. Dengan 'arsitektur modular', maksudku komponen yang independen."),
                ("Alex", "What's your main claim?", "Claim utamanya apa?"),
                ("Mina", "The core claim is that this will improve delivery speed. The evidence suggests teams move faster with clear ownership.", "Claim utamanya: ini mempercepat delivery. Evidence menunjukkan tim lebih cepat dengan ownership yang jelas."),
                ("Alex", "Isn't it too risky?", "Bukannya ini terlalu risky?"),
                ("Mina", "That's a fair question. The short answer is: it's manageable if we pilot first and monitor closely.", "Pertanyaan yang fair. Jawaban singkatnya: bisa di-manage kalau kita pilot dulu dan monitor ketat."),
                ("Alex", "So what's crucial?", "Yang krusial apa?"),
                ("Mina", "What's crucial here is shared standards. With that in mind, I'd propose a time-boxed pilot with guardrails.", "Yang krusial adalah standard bersama. Dengan itu, aku usul pilot time-boxed dengan guardrails."),
                ("Alex", "Sounds good. Any final summary?", "Oke. Ada rangkuman akhir?"),
                ("Mina", "In short, the benefits outweigh the risks if we set guardrails early. Next steps are: I'll share the plan today, and you'll review it by Friday.", "Singkatnya, benefit lebih besar dari risiko kalau kita set guardrails dari awal. Next steps: aku share plan hari ini, dan kamu review sebelum Jumat."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Today I'd like to walk you through the proposal and why it matters.",
                    "meaning_id": "Hari ini aku mau jelasin proposalnya dan kenapa ini penting.",
                    "usage_note": "Clear framing opener.",
                    "common_mistake": "Do not start without telling what you'll cover.",
                },
                {
                    "phrase": "The core claim is that this will improve delivery speed.",
                    "meaning_id": "Claim utamanya: ini akan mempercepat delivery.",
                    "usage_note": "Main claim.",
                    "common_mistake": "Do not hide the claim; state it clearly.",
                },
                {
                    "phrase": "That brings me to the key trade-off: speed versus reliability.",
                    "meaning_id": "Itu membawa kita ke trade-off utama: speed versus reliability.",
                    "usage_note": "Transition in a mission.",
                    "common_mistake": "Do not jump; use signposting.",
                },
                {
                    "phrase": "That's a fair question. The short answer is: it's manageable if we pilot first.",
                    "meaning_id": "Pertanyaan yang fair. Jawaban singkatnya: manageable kalau pilot dulu.",
                    "usage_note": "Q&A handling.",
                    "common_mistake": "Do not get defensive; keep it calm and structured.",
                },
                {
                    "phrase": "In short, the benefits outweigh the risks. Next steps are ...",
                    "meaning_id": "Singkatnya, benefit lebih besar dari risiko. Next steps adalah ...",
                    "usage_note": "Strong close: summary + next steps.",
                    "common_mistake": "Do not end without next steps.",
                },
            ],
            "grammar_md": [
                (
                    "Advanced presentation toolkit",
                    [
                        "Today I'd like to ...",
                        "By X, I mean ...",
                        "The core claim is that ... The evidence suggests ...",
                        "That brings me to ... What's crucial here is ...",
                        "That's a fair question. The short answer is: ...",
                        "In short, ... Next steps are ...",
                    ],
                )
            ],
            "pronunciation": [
                ("signposting", "SYNE-post-ing."),
                ("guardrails", "GARD-raylz."),
                ("outweigh", "out-WAY."),
            ],
            "response_prompts": [
                {
                    "prompt": "Frame the presentation and define the term.",
                    "target_response": "Today I'd like to walk you through the proposal and why it matters. By 'modular architecture', I mean independent components.",
                    "acceptable_variations": [
                        "Today I'd like to walk you through the proposal and why it matters. By 'modular architecture', I mean independent components.",
                        "Today I'd like to outline the proposal and why it matters. By 'modular design', I mean independent components.",
                    ],
                },
                {
                    "prompt": "Answer a challenging question calmly.",
                    "target_response": "That's a fair question. The short answer is: it's manageable if we pilot first and monitor closely.",
                    "acceptable_variations": [
                        "That's a fair question. The short answer is: it's manageable if we pilot first and monitor closely.",
                        "That's a fair question. The short answer is: yes, with a pilot and monitoring.",
                    ],
                },
                {
                    "prompt": "Close with summary and next steps.",
                    "target_response": "In short, the benefits outweigh the risks if we set guardrails early. Next steps are: I'll share the plan today, and you'll review it by Friday.",
                    "acceptable_variations": [
                        "In short, the benefits outweigh the risks if we set guardrails early. Next steps are: I'll share the plan today, and you'll review it by Friday.",
                        "In short, the benefits outweigh the risks if we do a pilot. Next steps are: I'll send the plan today, and you'll review it tomorrow.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "fair_question_mission",
                    "type": "multiple_choice",
                    "prompt": "Which phrase acknowledges a tough question calmly?",
                    "options": ["That's a fair question.", "That's wrong.", "Stop."],
                    "correct_answer": "That's a fair question.",
                },
                {
                    "key": "signpost_transition",
                    "type": "multiple_choice",
                    "prompt": "Which phrase is a transition signpost?",
                    "options": ["That brings me to ...", "Anyway.", "No."],
                    "correct_answer": "That brings me to ...",
                },
                {
                    "key": "next_steps_close",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces next steps?",
                    "options": ["Next steps are ...", "Maybe later.", "No need."],
                    "correct_answer": "Next steps are ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_advanced_presentation_mission",
                "opening_line": "Mission: present the proposal and handle questions.",
                "learner_goal": "Deliver an advanced presentation with signposting and handle challenging questions.",
                "turns": [
                    {
                        "coach": "Open and frame the topic, then define a key term.",
                        "hint": "Today I'd like to... By X, I mean...",
                        "sample_answer": "Today I'd like to walk you through the proposal and why it matters. By 'modular architecture', I mean independent components.",
                        "focus": "Framing",
                        "expected_keywords": ["today", "by", "i mean"],
                    },
                    {
                        "coach": "State your claim and evidence, then transition to a key trade-off.",
                        "hint": "The core claim is... The evidence suggests... That brings me to...",
                        "sample_answer": "The core claim is that this will improve delivery speed. The evidence suggests teams move faster with clear ownership. That brings me to the key trade-off: speed versus reliability.",
                        "focus": "Persuasion + transition",
                        "expected_keywords": ["core claim", "evidence suggests", "trade-off"],
                    },
                    {
                        "coach": "Handle a tough question and close with summary + next steps.",
                        "hint": "That's a fair question... The short answer is... In short... Next steps are...",
                        "sample_answer": "That's a fair question. The short answer is: it's manageable if we pilot first and monitor closely. In short, the benefits outweigh the risks if we set guardrails early. Next steps are: I'll share the plan today, and you'll review it by Friday.",
                        "focus": "Q&A + close",
                        "expected_keywords": ["fair question", "short answer", "next steps", "by"],
                    },
                ],
                "target_phrases": ["Today I'd like to ...", "The core claim is that ...", "That's a fair question."],
            },
            "reading_support": "Advanced presentations sound C1 when they are structured and calm: frame the topic, define terms, persuade with claim + evidence, guide with transitions, handle tough questions, then close with a concise summary and next steps.",
            "writing_support_lines": [
                "Write your mission (12 lines):",
                "1. Today I'd like to ...",
                "2. The purpose of this is to ...",
                "3. By X, I mean ...",
                "4. The core claim is that ...",
                "5. The evidence suggests ...",
                "6. A common concern is ...",
                "7. That said, ...",
                "8. That brings me to ...",
                "9. That's a fair question. The short answer is: ...",
                "10. What I'd emphasize is ...",
                "11. In short, ...",
                "12. Next steps are ...",
            ],
            "goal_examples": ["Today I'd like to ...", "The evidence suggests ...", "The short answer is: ..."],
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

