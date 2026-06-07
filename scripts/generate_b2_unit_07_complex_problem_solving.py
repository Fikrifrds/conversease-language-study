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
            "- Tone: professional, analytical, calm",
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

        Read it again and underline the problem-solving words (scope, constraint, root cause, trade-off, recommendation, risk).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B2"
    b2_root = Path("content/curriculum/english/B2")
    units_root = b2_root / "units"
    unit_key = "unit-07-complex-problem-solving"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-07-complex-problem-solving
            level_code: B2
            title: Complex Problem Solving
            main_conversation_outcome: Analyze a complex problem and discuss tradeoffs.
            status: in_production
            lessons:
              - lesson-01-framing-the-problem
              - lesson-02-explaining-causes
              - lesson-03-discussing-tradeoffs
              - lesson-04-recommending-a-solution
              - lesson-05-problem-solving-discussion-mission
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
            "lesson_key": "lesson-01-framing-the-problem",
            "slug": "framing-the-problem",
            "title": "Framing the Problem",
            "conversation_situation": "problem_framing_session",
            "conversation_goal": "Frame a complex problem clearly by defining scope, success criteria, and constraints.",
            "grammar_summary": "Use Let's define... / What does success look like? / Can we agree on the scope? to frame a problem clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu lagi meeting internal. Kamu bantu tim ngerumuskan problem statement yang jelas sebelum loncat ke solusi.",
            "dialogue": [
                ("Alex", "Our customer complaints have increased this month."),
                ("Mina", "Okay. Let's define the problem statement first."),
                ("Alex", "Sure. Where should we start?"),
                ("Mina", "Can we agree on the scope? Which product area is affected?"),
                ("Alex", "Mostly the billing flow."),
                ("Mina", "Great. What does success look like for the next four weeks?"),
                ("Alex", "Fewer support tickets and faster payment completion."),
                ("Mina", "Got it. Any constraints we should keep in mind?"),
                ("Alex", "We can't change pricing this quarter."),
            ],
            "translations": [
                ("Alex", "Our customer complaints have increased this month.", "Komplain pelanggan naik bulan ini."),
                ("Mina", "Okay. Let's define the problem statement first.", "Oke. Kita definisikan problem statement dulu."),
                ("Alex", "Sure. Where should we start?", "Oke. Mulai dari mana?"),
                ("Mina", "Can we agree on the scope? Which product area is affected?", "Kita sepakat scope-nya dulu ya? Area produk mana yang terdampak?"),
                ("Alex", "Mostly the billing flow.", "Kebanyakan di alur billing."),
                ("Mina", "Great. What does success look like for the next four weeks?", "Oke. Suksesnya itu seperti apa untuk 4 minggu ke depan?"),
                ("Alex", "Fewer support tickets and faster payment completion.", "Tiket support berkurang dan pembayaran lebih cepat selesai."),
                ("Mina", "Got it. Any constraints we should keep in mind?", "Oke. Ada constraint yang harus kita ingat?"),
                ("Alex", "We can't change pricing this quarter.", "Kita nggak bisa ubah pricing kuartal ini."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let's define the problem statement first.",
                    "meaning_id": "Kita definisikan problem statement dulu.",
                    "usage_note": "A structured opener before proposing solutions.",
                    "common_mistake": "Do not jump to solutions immediately.",
                },
                {
                    "phrase": "Can we agree on the scope?",
                    "meaning_id": "Kita sepakat scope-nya dulu ya?",
                    "usage_note": "Align what is in scope and out of scope.",
                    "common_mistake": "Do not keep scope vague; name the area affected.",
                },
                {
                    "phrase": "What does success look like?",
                    "meaning_id": "Suksesnya itu seperti apa?",
                    "usage_note": "Ask for measurable success criteria.",
                    "common_mistake": "Do not accept a vague answer; ask for metrics.",
                },
                {
                    "phrase": "Any constraints we should keep in mind?",
                    "meaning_id": "Ada constraint yang harus kita ingat?",
                    "usage_note": "Surface limitations early.",
                    "common_mistake": "Do not ignore constraints like timeline or pricing rules.",
                },
                {
                    "phrase": "Got it. Understood.",
                    "meaning_id": "Oke. Paham.",
                    "usage_note": "Professional listening signals.",
                    "common_mistake": "Do not overuse; use once per section.",
                },
            ],
            "grammar_md": [
                ("Framing language", ["Let's define the problem statement first.", "Can we agree on the scope?"]),
                ("Success criteria", ["What does success look like in the next four weeks?", "How will we measure success?"]),
            ],
            "pronunciation": [
                ("scope", "SKOHP."),
                ("constraints", "kuhn-STRAYNTS."),
                ("criteria", "kry-TEER-ee-uh."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask to define the problem first.",
                    "target_response": "Let's define the problem statement first.",
                    "acceptable_variations": ["Let's define the problem statement first.", "Let's frame the problem first."],
                },
                {
                    "prompt": "Ask to agree on scope.",
                    "target_response": "Can we agree on the scope?",
                    "acceptable_variations": ["Can we agree on the scope?", "Can we align on the scope?"],
                },
                {
                    "prompt": "Ask for success criteria.",
                    "target_response": "What does success look like for the next four weeks?",
                    "acceptable_variations": [
                        "What does success look like for the next four weeks?",
                        "How will we measure success in four weeks?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "define_problem",
                    "type": "multiple_choice",
                    "prompt": "Which phrase helps frame a problem before proposing solutions?",
                    "options": ["Let's define the problem statement first.", "Do it now.", "No need to discuss."],
                    "correct_answer": "Let's define the problem statement first.",
                },
                {
                    "key": "scope_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "scope" mean in a project discussion?',
                    "options": ["batas/topik yang dibahas", "alat musik", "waktu makan"],
                    "correct_answer": "batas/topik yang dibahas",
                },
                {
                    "key": "success_question",
                    "type": "multiple_choice",
                    "prompt": "Which question asks for success criteria?",
                    "options": ["What does success look like?", "Why are you late?", "Stop talking."],
                    "correct_answer": "What does success look like?",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_problem_framing",
                "opening_line": "We have a complex issue to solve.",
                "learner_goal": "Define the problem by aligning scope, success criteria, and constraints.",
                "turns": [
                    {
                        "coach": "We have a complex issue to solve.",
                        "hint": "Mulai dengan ajak tim framing dulu.",
                        "sample_answer": "Got it. Let's define the problem statement first.",
                        "focus": "Frame first",
                        "expected_keywords": ["define", "problem"],
                    },
                    {
                        "coach": "Okay. What should we clarify first?",
                        "hint": "Tanya scope.",
                        "sample_answer": "Can we agree on the scope? Which area is affected?",
                        "focus": "Scope",
                        "expected_keywords": ["scope", "affected"],
                    },
                    {
                        "coach": "How do we know we succeeded?",
                        "hint": "Tanya success criteria.",
                        "sample_answer": "What does success look like for the next four weeks?",
                        "focus": "Success criteria",
                        "expected_keywords": ["success", "look like"],
                    },
                ],
                "target_phrases": ["Let's define the problem statement first.", "Can we agree on the scope?", "What does success look like?"],
            },
            "reading_support": "When framing a complex problem, be explicit about scope (where the problem happens), success criteria (how you measure improvement), and constraints (what you cannot change).",
            "writing_support_lines": [
                "Write 7 lines:",
                "1. Let's define the problem statement first.",
                "2. Can we agree on the scope?",
                "3. Which area is affected?",
                "4. What does success look like?",
                "5. How will we measure it?",
                "6. Any constraints we should keep in mind?",
                "7. Great, let's summarize the problem in one sentence.",
            ],
            "goal_examples": ["Let's define the problem statement first.", "Can we agree on the scope?", "What does success look like?"],
        },
        {
            "lesson_key": "lesson-02-explaining-causes",
            "slug": "explaining-causes",
            "title": "Explaining Causes",
            "conversation_situation": "root_cause_discussion",
            "conversation_goal": "Explain possible causes using evidence language and clarify what data supports each cause.",
            "grammar_summary": "Use One possible cause is... / Based on the data... / It might be due to... to discuss root causes calmly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu bahas akar masalah. Kamu jelasin kemungkinan penyebab dengan bahasa yang hati-hati dan berbasis data.",
            "dialogue": [
                ("Alex", "Why do you think billing complaints are up?"),
                ("Mina", "One possible cause is the new checkout design."),
                ("Alex", "What makes you think that?"),
                ("Mina", "Based on the data, drop-offs increased right after the redesign."),
                ("Alex", "Could it be something else?"),
                ("Mina", "It might be due to slower load times as well."),
                ("Alex", "How can we confirm?"),
                ("Mina", "Let's compare load times and run a small A/B test."),
            ],
            "translations": [
                ("Alex", "Why do you think billing complaints are up?", "Menurut kamu kenapa komplain billing naik?"),
                ("Mina", "One possible cause is the new checkout design.", "Salah satu kemungkinan penyebabnya adalah desain checkout yang baru."),
                ("Alex", "What makes you think that?", "Kenapa kamu mikir begitu?"),
                ("Mina", "Based on the data, drop-offs increased right after the redesign.", "Berdasarkan data, drop-off naik tepat setelah redesign."),
                ("Alex", "Could it be something else?", "Bisa jadi hal lain nggak?"),
                ("Mina", "It might be due to slower load times as well.", "Bisa juga karena load time yang lebih lambat."),
                ("Alex", "How can we confirm?", "Gimana cara kita konfirmasi?"),
                ("Mina", "Let's compare load times and run a small A/B test.", "Kita bandingin load time dan jalankan A/B test kecil."),
            ],
            "useful_phrases": [
                {
                    "phrase": "One possible cause is the new checkout design.",
                    "meaning_id": "Salah satu kemungkinan penyebabnya adalah desain checkout yang baru.",
                    "usage_note": "Use possible cause to sound careful, not absolute.",
                    "common_mistake": 'Do not say "the cause is"; use one possible cause is.',
                },
                {
                    "phrase": "Based on the data, drop-offs increased after the redesign.",
                    "meaning_id": "Berdasarkan data, drop-off naik setelah redesign.",
                    "usage_note": "Evidence language for reasoning.",
                    "common_mistake": "Do not say based on datas; data is uncountable.",
                },
                {
                    "phrase": "It might be due to slower load times.",
                    "meaning_id": "Bisa juga karena load time yang lebih lambat.",
                    "usage_note": "A second hypothesis with might be due to.",
                    "common_mistake": 'Do not say "due slow"; use due to.',
                },
                {
                    "phrase": "How can we confirm?",
                    "meaning_id": "Gimana cara kita konfirmasi?",
                    "usage_note": "Move from hypothesis to validation.",
                    "common_mistake": "Do not stop at opinions; propose a way to confirm.",
                },
                {
                    "phrase": "Let's run a small A/B test.",
                    "meaning_id": "Kita jalankan A/B test kecil.",
                    "usage_note": "A practical validation step.",
                    "common_mistake": "Do not propose a huge change without validation.",
                },
            ],
            "grammar_md": [
                ("Hypotheses", ["One possible cause is ...", "It might be due to ..."]),
                ("Evidence", ["Based on the data, ...", "We saw an increase right after ..."]),
            ],
            "pronunciation": [
                ("hypothesis", "hy-POTH-uh-sis."),
                ("redesign", "REE-dee-zine."),
                ("data", "DAY-tuh."),
            ],
            "response_prompts": [
                {
                    "prompt": "State a possible cause.",
                    "target_response": "One possible cause is the new checkout design.",
                    "acceptable_variations": [
                        "One possible cause is the new checkout design.",
                        "One possible cause is a confusing step in checkout.",
                    ],
                },
                {
                    "prompt": "Use evidence language.",
                    "target_response": "Based on the data, drop-offs increased right after the redesign.",
                    "acceptable_variations": [
                        "Based on the data, drop-offs increased right after the redesign.",
                        "Based on the data, complaints increased after the change.",
                    ],
                },
                {
                    "prompt": "Suggest a way to confirm.",
                    "target_response": "Let's compare load times and run a small A/B test.",
                    "acceptable_variations": [
                        "Let's compare load times and run a small A/B test.",
                        "Let's run a small experiment to confirm.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "possible_cause_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase sounds careful and professional when suggesting a cause?",
                    "options": ["One possible cause is ...", "This is the only cause.", "You are wrong."],
                    "correct_answer": "One possible cause is ...",
                },
                {
                    "key": "data_usage",
                    "type": "multiple_choice",
                    "prompt": "Which sentence uses data correctly?",
                    "options": ["Based on the data, ...", "Based on the datas, ...", "Based on data are ..."],
                    "correct_answer": "Based on the data, ...",
                },
                {
                    "key": "due_to_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "due to" mean?',
                    "options": ["karena/disebabkan oleh", "sebaliknya", "akhirnya"],
                    "correct_answer": "karena/disebabkan oleh",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_root_causes",
                "opening_line": "Why do you think this problem is happening?",
                "learner_goal": "Explain possible causes with evidence language and propose how to confirm.",
                "turns": [
                    {
                        "coach": "Why do you think this problem is happening?",
                        "hint": "Jawab dengan one possible cause is...",
                        "sample_answer": "One possible cause is the new checkout design.",
                        "focus": "Possible cause",
                        "expected_keywords": ["possible cause"],
                    },
                    {
                        "coach": "What evidence do we have?",
                        "hint": "Pakai based on the data.",
                        "sample_answer": "Based on the data, drop-offs increased right after the redesign.",
                        "focus": "Evidence",
                        "expected_keywords": ["based on", "data"],
                    },
                    {
                        "coach": "How can we confirm this?",
                        "hint": "Usulkan test/compare.",
                        "sample_answer": "Let's compare load times and run a small A/B test.",
                        "focus": "Confirm",
                        "expected_keywords": ["compare", "test"],
                    },
                ],
                "target_phrases": ["One possible cause is ...", "Based on the data, ...", "Let's run a small A/B test."],
            },
            "reading_support": "When explaining causes, separate hypotheses from evidence. Use careful language (might, possible), cite what data shows, and propose how to confirm with an experiment.",
            "writing_support_lines": [
                "Write 7 lines:",
                "1. One possible cause is ...",
                "2. Based on the data, ...",
                "3. It might be due to ...",
                "4. Another hypothesis is ...",
                "5. How can we confirm?",
                "6. Let's run a small test.",
                "7. Then we can decide the next step.",
            ],
            "goal_examples": ["One possible cause is ...", "Based on the data, ...", "It might be due to ..."],
        },
        {
            "lesson_key": "lesson-03-discussing-tradeoffs",
            "slug": "discussing-tradeoffs",
            "title": "Discussing Tradeoffs",
            "conversation_situation": "tradeoff_discussion",
            "conversation_goal": "Discuss trade-offs between options, highlighting impact on cost, time, and risk.",
            "grammar_summary": "Use The trade-off is... / If we optimize for..., we might... / On the other hand... to compare options clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu bandingin beberapa opsi. Kamu jelasin trade-off-nya dengan jelas: cepat vs kualitas, biaya vs risiko, dll.",
            "dialogue": [
                ("Alex", "We have two solutions. Which one should we pick?"),
                ("Mina", "The trade-off is speed versus long-term reliability."),
                ("Alex", "Can you explain that?"),
                ("Mina", "If we optimize for speed, we might introduce more bugs."),
                ("Alex", "And the slower option?"),
                ("Mina", "On the other hand, the slower option reduces risk but takes more effort."),
                ("Alex", "What do you suggest?"),
                ("Mina", "Let's choose based on our biggest constraint: time or risk."),
            ],
            "translations": [
                ("Alex", "We have two solutions. Which one should we pick?", "Kita punya dua solusi. Pilih yang mana?"),
                ("Mina", "The trade-off is speed versus long-term reliability.", "Trade-off-nya adalah kecepatan versus reliability jangka panjang."),
                ("Alex", "Can you explain that?", "Bisa jelasin maksudnya?"),
                ("Mina", "If we optimize for speed, we might introduce more bugs.", "Kalau kita fokus ke cepat, kita bisa nambah bug."),
                ("Alex", "And the slower option?", "Kalau opsi yang lebih lambat?"),
                ("Mina", "On the other hand, the slower option reduces risk but takes more effort.", "Di sisi lain, opsi yang lebih lambat mengurangi risiko tapi butuh effort lebih besar."),
                ("Alex", "What do you suggest?", "Kamu saranin apa?"),
                ("Mina", "Let's choose based on our biggest constraint: time or risk.", "Kita pilih berdasarkan constraint terbesar: waktu atau risiko."),
            ],
            "useful_phrases": [
                {
                    "phrase": "The trade-off is speed versus long-term reliability.",
                    "meaning_id": "Trade-off-nya adalah kecepatan versus reliability jangka panjang.",
                    "usage_note": "A clear trade-off statement.",
                    "common_mistake": "Do not list too many trade-offs at once; start with one.",
                },
                {
                    "phrase": "If we optimize for speed, we might introduce more bugs.",
                    "meaning_id": "Kalau kita fokus ke cepat, kita bisa nambah bug.",
                    "usage_note": "Explain downside with might.",
                    "common_mistake": "Do not sound absolute; use might or could.",
                },
                {
                    "phrase": "On the other hand, the slower option reduces risk.",
                    "meaning_id": "Di sisi lain, opsi yang lebih lambat mengurangi risiko.",
                    "usage_note": "Contrast a second option.",
                    "common_mistake": "Do not say on other hand without contrast; always compare.",
                },
                {
                    "phrase": "Let's choose based on our biggest constraint.",
                    "meaning_id": "Kita pilih berdasarkan constraint terbesar.",
                    "usage_note": "Decision principle tied to constraints.",
                    "common_mistake": "Do not ignore constraints; use them to decide.",
                },
                {
                    "phrase": "What do you suggest?",
                    "meaning_id": "Kamu saranin apa?",
                    "usage_note": "Invite recommendation.",
                    "common_mistake": "Do not demand; keep tone neutral.",
                },
            ],
            "grammar_md": [
                ("Trade-offs", ["The trade-off is X versus Y.", "The trade-off is speed versus reliability."]),
                ("Contrast + impact", ["If we optimize for X, we might Y.", "On the other hand, ..."]),
            ],
            "pronunciation": [
                ("reliability", "ri-LYE-uh-BIL-ih-tee."),
                ("optimize", "OP-tuh-mize."),
                ("effort", "EF-urt."),
            ],
            "response_prompts": [
                {
                    "prompt": "State a trade-off.",
                    "target_response": "The trade-off is speed versus long-term reliability.",
                    "acceptable_variations": [
                        "The trade-off is speed versus long-term reliability.",
                        "The trade-off is cost versus quality.",
                    ],
                },
                {
                    "prompt": "Explain impact with might.",
                    "target_response": "If we optimize for speed, we might introduce more bugs.",
                    "acceptable_variations": [
                        "If we optimize for speed, we might introduce more bugs.",
                        "If we optimize for cost, we might lose quality.",
                    ],
                },
                {
                    "prompt": "Use a contrast phrase.",
                    "target_response": "On the other hand, the slower option reduces risk but takes more effort.",
                    "acceptable_variations": [
                        "On the other hand, the slower option reduces risk but takes more effort.",
                        "On the other hand, it is more reliable but slower.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "tradeoff_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a trade-off?",
                    "options": ["The trade-off is ...", "Trade off is have.", "No trade."],
                    "correct_answer": "The trade-off is ...",
                },
                {
                    "key": "contrast_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase shows contrast between options?",
                    "options": ["On the other hand, ...", "Because, ...", "Maybe."],
                    "correct_answer": "On the other hand, ...",
                },
                {
                    "key": "optimize_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "optimize for speed" mean?',
                    "options": ["memprioritaskan kecepatan", "memperlambat", "menghapus fitur"],
                    "correct_answer": "memprioritaskan kecepatan",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_tradeoffs",
                "opening_line": "We have two options. Compare them.",
                "learner_goal": "Explain trade-offs and impact, then suggest a decision principle.",
                "turns": [
                    {
                        "coach": "We have two options. Compare them.",
                        "hint": "Mulai dengan trade-off.",
                        "sample_answer": "The trade-off is speed versus long-term reliability.",
                        "focus": "Trade-off",
                        "expected_keywords": ["trade-off"],
                    },
                    {
                        "coach": "Explain the downside of the fast option.",
                        "hint": "If we optimize for speed, we might...",
                        "sample_answer": "If we optimize for speed, we might introduce more bugs.",
                        "focus": "Impact",
                        "expected_keywords": ["optimize", "might"],
                    },
                    {
                        "coach": "Now contrast with the safer option.",
                        "hint": "On the other hand...",
                        "sample_answer": "On the other hand, the slower option reduces risk but takes more effort.",
                        "focus": "Contrast",
                        "expected_keywords": ["on the other hand", "risk"],
                    },
                ],
                "target_phrases": ["The trade-off is ...", "If we optimize for ..., we might ...", "On the other hand, ..."],
            },
            "reading_support": "Trade-offs are about priorities. Compare options using a consistent structure: trade-off, downside of option A, benefit of option B, and how constraints affect the decision.",
            "writing_support_lines": [
                "Write 8 lines:",
                "1. The trade-off is ... versus ...",
                "2. Option A is faster, but ...",
                "3. If we optimize for speed, we might ...",
                "4. Option B is slower, but ...",
                "5. On the other hand, ...",
                "6. The risk is ...",
                "7. Our biggest constraint is ...",
                "8. So I suggest we ...",
            ],
            "goal_examples": ["The trade-off is ...", "If we optimize for ..., we might ...", "On the other hand, ..."],
        },
        {
            "lesson_key": "lesson-04-recommending-a-solution",
            "slug": "recommending-a-solution",
            "title": "Recommending a Solution",
            "conversation_situation": "recommend_solution_meeting",
            "conversation_goal": "Recommend a solution clearly by summarizing reasoning, risks, and next steps.",
            "grammar_summary": "Use Given these constraints... / I'd recommend... / The main risk is... / We can mitigate it by... to recommend a solution.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu harus kasih rekomendasi. Kamu rangkum reasoning-nya, sebut risiko utama, dan next steps yang realistis.",
            "dialogue": [
                ("Alex", "So what should we do next?"),
                ("Mina", "Given these constraints, I'd recommend starting with a two-week pilot."),
                ("Alex", "Why a pilot?"),
                ("Mina", "It reduces risk and gives us data before a full rollout."),
                ("Alex", "What's the main risk?"),
                ("Mina", "The main risk is slower progress if we over-scope the pilot."),
                ("Alex", "How do we mitigate that?"),
                ("Mina", "We can mitigate it by setting clear success metrics and a strict timeline."),
            ],
            "translations": [
                ("Alex", "So what should we do next?", "Jadi next kita harus ngapain?"),
                ("Mina", "Given these constraints, I'd recommend starting with a two-week pilot.", "Dengan constraint ini, aku rekomend mulai dengan pilot dua minggu."),
                ("Alex", "Why a pilot?", "Kenapa pilot?"),
                ("Mina", "It reduces risk and gives us data before a full rollout.", "Itu ngurangin risiko dan ngasih data sebelum rollout penuh."),
                ("Alex", "What's the main risk?", "Risiko utamanya apa?"),
                ("Mina", "The main risk is slower progress if we over-scope the pilot.", "Risiko utamanya progress jadi lambat kalau pilot-nya kebesaran scope."),
                ("Alex", "How do we mitigate that?", "Gimana mitigasinya?"),
                ("Mina", "We can mitigate it by setting clear success metrics and a strict timeline.", "Kita mitigasi dengan set metrik sukses yang jelas dan timeline yang ketat."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Given these constraints, I'd recommend starting with a two-week pilot.",
                    "meaning_id": "Dengan constraint ini, aku rekomend mulai dengan pilot dua minggu.",
                    "usage_note": "Recommendation tied to constraints.",
                    "common_mistake": 'Do not say "I recommend start"; use I\'d recommend starting.',
                },
                {
                    "phrase": "It reduces risk and gives us data before a full rollout.",
                    "meaning_id": "Itu ngurangin risiko dan ngasih data sebelum rollout penuh.",
                    "usage_note": "Justify recommendation in one sentence.",
                    "common_mistake": "Do not over-explain; keep the justification clear.",
                },
                {
                    "phrase": "The main risk is slower progress if we over-scope the pilot.",
                    "meaning_id": "Risiko utamanya progress jadi lambat kalau pilot-nya kebesaran scope.",
                    "usage_note": "Name a risk with if-structure.",
                    "common_mistake": "Do not list many risks; start with the main one.",
                },
                {
                    "phrase": "We can mitigate it by setting clear success metrics.",
                    "meaning_id": "Kita mitigasi dengan set metrik sukses yang jelas.",
                    "usage_note": "Mitigation language.",
                    "common_mistake": "Do not say mitigate it with setting; use by + -ing.",
                },
                {
                    "phrase": "Does that approach work for you?",
                    "meaning_id": "Pendekatan itu works buat kamu?",
                    "usage_note": "Check alignment after recommending.",
                    "common_mistake": "Do not assume agreement; ask.",
                },
            ],
            "grammar_md": [
                ("Recommendation", ["Given these constraints, I'd recommend ...", "My recommendation is to start with ..."]),
                ("Risk + mitigation", ["The main risk is ... if ...", "We can mitigate it by ..."]),
            ],
            "pronunciation": [
                ("recommend", "rek-uh-MEND."),
                ("mitigate", "MIT-i-gayt."),
                ("metrics", "MET-riks."),
            ],
            "response_prompts": [
                {
                    "prompt": "Recommend a solution linked to constraints.",
                    "target_response": "Given these constraints, I'd recommend starting with a two-week pilot.",
                    "acceptable_variations": [
                        "Given these constraints, I'd recommend starting with a two-week pilot.",
                        "Given these constraints, I'd recommend a small rollout first.",
                    ],
                },
                {
                    "prompt": "Name a main risk.",
                    "target_response": "The main risk is slower progress if we over-scope the pilot.",
                    "acceptable_variations": [
                        "The main risk is slower progress if we over-scope the pilot.",
                        "The main risk is delays if the scope expands.",
                    ],
                },
                {
                    "prompt": "Propose mitigation.",
                    "target_response": "We can mitigate it by setting clear success metrics and a strict timeline.",
                    "acceptable_variations": [
                        "We can mitigate it by setting clear success metrics and a strict timeline.",
                        "We can mitigate it by keeping the scope small and time-boxed.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "recommend_structure",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a clear recommendation?",
                    "options": [
                        "Given these constraints, I'd recommend starting with a pilot.",
                        "Given constraints I recommending.",
                        "Recommend now.",
                    ],
                    "correct_answer": "Given these constraints, I'd recommend starting with a pilot.",
                },
                {
                    "key": "mitigate_structure",
                    "type": "multiple_choice",
                    "prompt": "Which sentence uses mitigation language correctly?",
                    "options": ["We can mitigate it by setting clear metrics.", "We can mitigate with set metrics.", "Mitigate is metrics."],
                    "correct_answer": "We can mitigate it by setting clear metrics.",
                },
                {
                    "key": "risk_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "risk" mean?',
                    "options": ["potensi masalah/kemungkinan buruk", "hadiah", "jawaban benar"],
                    "correct_answer": "potensi masalah/kemungkinan buruk",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_solution_recommendation",
                "opening_line": "We need a recommendation. What should we do?",
                "learner_goal": "Recommend a solution with reasoning, risk, and mitigation.",
                "turns": [
                    {
                        "coach": "We need a recommendation. What should we do?",
                        "hint": "Given these constraints, I'd recommend...",
                        "sample_answer": "Given these constraints, I'd recommend starting with a two-week pilot.",
                        "focus": "Recommend",
                        "expected_keywords": ["recommend", "pilot"],
                    },
                    {
                        "coach": "What's the main risk?",
                        "hint": "The main risk is... if...",
                        "sample_answer": "The main risk is slower progress if we over-scope the pilot.",
                        "focus": "Risk",
                        "expected_keywords": ["main risk", "if"],
                    },
                    {
                        "coach": "How do we mitigate it?",
                        "hint": "We can mitigate it by...",
                        "sample_answer": "We can mitigate it by setting clear success metrics and a strict timeline.",
                        "focus": "Mitigation",
                        "expected_keywords": ["mitigate", "metrics"],
                    },
                ],
                "target_phrases": ["Given these constraints, I'd recommend ...", "The main risk is ...", "We can mitigate it by ..."],
            },
            "reading_support": "A strong recommendation connects constraints to a clear action, then names the main risk and a mitigation plan. Keep it short: recommendation, why, risk, mitigation, next step.",
            "writing_support_lines": [
                "Write 8 lines:",
                "1. Given these constraints, I'd recommend ...",
                "2. Because ...",
                "3. The main risk is ...",
                "4. If ...",
                "5. We can mitigate it by ...",
                "6. Next steps are ...",
                "7. I'll share a draft plan by ...",
                "8. Does that approach work for you?",
            ],
            "goal_examples": ["Given these constraints, I'd recommend ...", "The main risk is ...", "We can mitigate it by ..."],
        },
        {
            "lesson_key": "lesson-05-problem-solving-discussion-mission",
            "slug": "problem-solving-discussion-mission",
            "title": "Problem Solving Discussion Mission",
            "conversation_situation": "mission_problem_solving_discussion",
            "conversation_goal": "Lead a problem-solving discussion: frame the problem, explain causes, discuss trade-offs, and recommend next steps.",
            "grammar_summary": "Combine framing + causes + trade-offs + recommendation into one structured discussion.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Misi: kamu pimpin diskusi problem solving dari framing sampai rekomendasi, lalu set next steps yang jelas.",
            "dialogue": [
                ("Alex", "We need to fix billing complaints. What should we do?"),
                ("Mina", "Let's define the problem statement first. Can we agree on the scope?"),
                ("Alex", "Scope is the billing flow."),
                ("Mina", "Based on the data, drop-offs increased after the redesign. One possible cause is confusion in checkout."),
                ("Alex", "What are our options?"),
                ("Mina", "The trade-off is speed versus reliability. Given these constraints, I'd recommend a two-week pilot."),
                ("Alex", "What's the main risk?"),
                ("Mina", "The main risk is slower progress if we over-scope. We can mitigate it by setting clear metrics and a strict timeline."),
            ],
            "translations": [
                ("Alex", "We need to fix billing complaints. What should we do?", "Kita harus beresin komplain billing. Kita harus ngapain?"),
                ("Mina", "Let's define the problem statement first. Can we agree on the scope?", "Kita definisikan problem statement dulu. Kita sepakat scope-nya dulu ya?"),
                ("Alex", "Scope is the billing flow.", "Scope-nya alur billing."),
                ("Mina", "Based on the data, drop-offs increased after the redesign. One possible cause is confusion in checkout.", "Berdasarkan data, drop-off naik setelah redesign. Salah satu kemungkinan penyebabnya adalah checkout yang membingungkan."),
                ("Alex", "What are our options?", "Opsi kita apa?"),
                ("Mina", "The trade-off is speed versus reliability. Given these constraints, I'd recommend a two-week pilot.", "Trade-off-nya kecepatan versus reliability. Dengan constraint ini, aku rekomend pilot dua minggu."),
                ("Alex", "What's the main risk?", "Risiko utamanya apa?"),
                ("Mina", "The main risk is slower progress if we over-scope. We can mitigate it by setting clear metrics and a strict timeline.", "Risiko utamanya progress jadi lambat kalau scope-nya kebesaran. Kita mitigasi dengan metrik yang jelas dan timeline yang ketat."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Let's define the problem statement first.",
                    "meaning_id": "Kita definisikan problem statement dulu.",
                    "usage_note": "Start structured problem solving.",
                    "common_mistake": "Don't jump to solutions.",
                },
                {
                    "phrase": "Based on the data, one possible cause is ...",
                    "meaning_id": "Berdasarkan data, salah satu kemungkinan penyebabnya adalah ...",
                    "usage_note": "Cause explanation with evidence language.",
                    "common_mistake": "Don't make it sound certain; keep it as possible cause.",
                },
                {
                    "phrase": "The trade-off is speed versus reliability.",
                    "meaning_id": "Trade-off-nya kecepatan versus reliability.",
                    "usage_note": "Compare options quickly.",
                    "common_mistake": "Don't talk in circles; state the trade-off clearly.",
                },
                {
                    "phrase": "Given these constraints, I'd recommend a two-week pilot.",
                    "meaning_id": "Dengan constraint ini, aku rekomend pilot dua minggu.",
                    "usage_note": "Recommendation.",
                    "common_mistake": 'Don\'t say "I recommend to pilot"; use I\'d recommend a pilot.',
                },
                {
                    "phrase": "We can mitigate it by setting clear metrics and a strict timeline.",
                    "meaning_id": "Kita mitigasi dengan metrik yang jelas dan timeline yang ketat.",
                    "usage_note": "Mitigation + next step.",
                    "common_mistake": "Don't stop at risk; propose mitigation.",
                },
            ],
            "grammar_md": [
                (
                    "Problem-solving flow",
                    [
                        "Let's define the problem statement first.",
                        "One possible cause is ... Based on the data, ...",
                        "The trade-off is X versus Y.",
                        "Given these constraints, I'd recommend ...",
                        "We can mitigate it by ...",
                    ],
                ),
            ],
            "pronunciation": [
                ("root cause", "ROOT kawz."),
                ("trade-off", "TRAYD-off."),
                ("recommendation", "rek-uh-men-DAY-shun."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start by framing the problem.",
                    "target_response": "Let's define the problem statement first. Can we agree on the scope?",
                    "acceptable_variations": [
                        "Let's define the problem statement first. Can we agree on the scope?",
                        "Let's frame the problem first. Can we align on scope?",
                    ],
                },
                {
                    "prompt": "Explain a cause using evidence language.",
                    "target_response": "Based on the data, one possible cause is confusion in checkout.",
                    "acceptable_variations": [
                        "Based on the data, one possible cause is confusion in checkout.",
                        "Based on the data, it might be due to slower load times.",
                    ],
                },
                {
                    "prompt": "Recommend next steps with mitigation.",
                    "target_response": "Given these constraints, I'd recommend a two-week pilot. We can mitigate risk by setting clear metrics and a strict timeline.",
                    "acceptable_variations": [
                        "Given these constraints, I'd recommend a two-week pilot. We can mitigate risk by setting clear metrics and a strict timeline.",
                        "Given these constraints, I'd recommend a small rollout first. We can mitigate risk with clear metrics.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "flow_order",
                    "type": "multiple_choice",
                    "prompt": "Which order fits a problem-solving discussion?",
                    "options": [
                        "Frame problem -> causes -> trade-offs -> recommendation",
                        "Recommendation -> frame problem -> greeting",
                        "Colors -> numbers -> days",
                    ],
                    "correct_answer": "Frame problem -> causes -> trade-offs -> recommendation",
                },
                {
                    "key": "possible_cause",
                    "type": "multiple_choice",
                    "prompt": "Which phrase suggests a cause carefully?",
                    "options": ["One possible cause is ...", "This is 100% the cause.", "No cause."],
                    "correct_answer": "One possible cause is ...",
                },
                {
                    "key": "mitigation_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces mitigation?",
                    "options": ["We can mitigate it by ...", "Mitigate with do.", "No risk."],
                    "correct_answer": "We can mitigate it by ...",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_problem_mission",
                "opening_line": "We have a complex issue. Lead the discussion.",
                "learner_goal": "Lead a structured problem-solving discussion from framing to recommendation.",
                "turns": [
                    {
                        "coach": "Start by framing the problem and scope.",
                        "hint": "Let's define... Can we agree on the scope?",
                        "sample_answer": "Let's define the problem statement first. Can we agree on the scope?",
                        "focus": "Framing",
                        "expected_keywords": ["define", "scope"],
                    },
                    {
                        "coach": "Now explain one possible cause with evidence language.",
                        "hint": "Based on the data... one possible cause is...",
                        "sample_answer": "Based on the data, one possible cause is confusion in checkout after the redesign.",
                        "focus": "Causes",
                        "expected_keywords": ["based on", "data", "possible"],
                    },
                    {
                        "coach": "Discuss trade-offs and recommend a next step with mitigation.",
                        "hint": "The trade-off is... Given these constraints... We can mitigate it by...",
                        "sample_answer": "The trade-off is speed versus reliability. Given these constraints, I'd recommend a two-week pilot. We can mitigate risk by setting clear metrics and a strict timeline.",
                        "focus": "Trade-offs + recommendation",
                        "expected_keywords": ["trade-off", "recommend", "mitigate"],
                    },
                ],
                "target_phrases": ["Let's define the problem statement first.", "One possible cause is ...", "Given these constraints, I'd recommend ..."],
            },
            "reading_support": "In a mission-style discussion, keep a clear structure: frame the problem, propose causes with evidence language, compare options with trade-offs, then recommend a time-boxed next step with mitigation.",
            "writing_support_lines": [
                "Write your mission (10 lines):",
                "1. Let's define the problem statement first.",
                "2. Can we agree on the scope?",
                "3. What does success look like?",
                "4. Based on the data, ...",
                "5. One possible cause is ...",
                "6. The trade-off is ... versus ...",
                "7. Given these constraints, I'd recommend ...",
                "8. The main risk is ...",
                "9. We can mitigate it by ...",
                "10. Next steps are ...",
            ],
            "goal_examples": ["Let's define the problem statement first.", "One possible cause is ...", "Given these constraints, I'd recommend ..."],
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

