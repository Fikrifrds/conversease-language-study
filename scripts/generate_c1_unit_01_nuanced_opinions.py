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
            "- Tone: thoughtful, confident, precise",
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

        Read it again and underline the nuance markers (to some extent, broadly speaking, that said, on balance, in principle).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "C1"
    root = Path("content/curriculum/english/C1")
    units_root = root / "units"
    unit_key = "unit-01-nuanced-opinions"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-01-nuanced-opinions
            level_code: C1
            title: Nuanced Opinions
            main_conversation_outcome: Express nuanced opinions with precision and flexibility.
            status: in_production
            lessons:
              - lesson-01-qualifying-your-opinion
              - lesson-02-expressing-certainty-and-doubt
              - lesson-03-balancing-two-viewpoints
              - lesson-04-softening-disagreement
              - lesson-05-nuanced-opinion-mission
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
            "lesson_key": "lesson-01-qualifying-your-opinion",
            "slug": "qualifying-your-opinion",
            "title": "Qualifying Your Opinion",
            "conversation_situation": "qualifying_opinions_in_discussion",
            "conversation_goal": "Qualify your opinion with nuance by signaling scope, conditions, and limits.",
            "grammar_summary": "Use To some extent... / Broadly speaking... / In principle..., but... / That said... to qualify opinions.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu lagi diskusi kerja. Kamu setuju sebagian, tapi kamu kasih batasan dan kondisi biar opini kamu lebih presisi.",
            "dialogue": [
                ("Jordan", "Do you think we should adopt the new policy immediately?"),
                ("Mina", "To some extent, yes—especially for new projects."),
                ("Jordan", "So you're fully in favor?"),
                ("Mina", "Broadly speaking, I support it. That said, we need a clear exception for legacy systems."),
                ("Jordan", "What's the main concern?"),
                ("Mina", "In principle it's a good move, but the rollout timeline is too aggressive."),
                ("Jordan", "So what would you suggest?"),
                ("Mina", "I'd phase it in over two quarters and review adoption data along the way."),
            ],
            "translations": [
                ("Jordan", "Do you think we should adopt the new policy immediately?", "Menurut kamu kita harus adopsi kebijakan baru ini langsung nggak?"),
                ("Mina", "To some extent, yes—especially for new projects.", "Sampai batas tertentu, iya—terutama untuk project baru."),
                ("Jordan", "So you're fully in favor?", "Jadi kamu 100% setuju?"),
                ("Mina", "Broadly speaking, I support it. That said, we need a clear exception for legacy systems.", "Secara umum, aku dukung. Tapi, kita butuh pengecualian yang jelas untuk sistem lama."),
                ("Jordan", "What's the main concern?", "Concern utamanya apa?"),
                ("Mina", "In principle it's a good move, but the rollout timeline is too aggressive.", "Secara prinsip itu langkah bagus, tapi timeline rollout-nya terlalu agresif."),
                ("Jordan", "So what would you suggest?", "Jadi kamu saranin apa?"),
                ("Mina", "I'd phase it in over two quarters and review adoption data along the way.", "Aku akan implement bertahap selama dua kuartal dan review data adoption sambil jalan."),
            ],
            "useful_phrases": [
                {
                    "phrase": "To some extent, yes—especially for new projects.",
                    "meaning_id": "Sampai batas tertentu, iya—terutama untuk project baru.",
                    "usage_note": "Agree partially and specify scope.",
                    "common_mistake": "Do not say yes/no only; add scope or condition.",
                },
                {
                    "phrase": "Broadly speaking, I support it.",
                    "meaning_id": "Secara umum, aku dukung.",
                    "usage_note": "Give a general stance without overcommitting.",
                    "common_mistake": 'Do not say "in general speaking"; use broadly speaking.',
                },
                {
                    "phrase": "That said, we need a clear exception for legacy systems.",
                    "meaning_id": "Tapi, kita butuh pengecualian yang jelas untuk sistem lama.",
                    "usage_note": "Add an important limitation after agreement.",
                    "common_mistake": "Do not contradict without linking; use that said.",
                },
                {
                    "phrase": "In principle it's a good move, but the timeline is too aggressive.",
                    "meaning_id": "Secara prinsip itu langkah bagus, tapi timeline-nya terlalu agresif.",
                    "usage_note": "Support the idea but challenge execution.",
                    "common_mistake": "Do not criticize harshly; focus on timeline/constraints.",
                },
                {
                    "phrase": "I'd phase it in over two quarters.",
                    "meaning_id": "Aku akan implement bertahap selama dua kuartal.",
                    "usage_note": "Suggest a measured approach.",
                    "common_mistake": 'Do not say "phase in it"; use phase it in.',
                },
            ],
            "grammar_md": [
                ("Partial agreement", ["To some extent, ...", "Broadly speaking, ..."]),
                ("Limitations", ["That said, ...", "In principle ..., but ..."]),
            ],
            "pronunciation": [
                ("extent", "ik-STENT."),
                ("broadly", "BROAD-lee."),
                ("legacy", "LEG-uh-see."),
            ],
            "response_prompts": [
                {
                    "prompt": "Agree partially and set scope.",
                    "target_response": "To some extent, yes—especially for new projects.",
                    "acceptable_variations": [
                        "To some extent, yes—especially for new projects.",
                        "To some extent, yes—if we start with a pilot.",
                    ],
                },
                {
                    "prompt": "Add a limitation with that said.",
                    "target_response": "That said, we need a clear exception for legacy systems.",
                    "acceptable_variations": [
                        "That said, we need a clear exception for legacy systems.",
                        "That said, we should define guardrails first.",
                    ],
                },
                {
                    "prompt": "Suggest a phased approach.",
                    "target_response": "I'd phase it in over two quarters and review adoption data along the way.",
                    "acceptable_variations": [
                        "I'd phase it in over two quarters and review adoption data along the way.",
                        "I'd phase it in gradually and review results monthly.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "to_some_extent",
                    "type": "multiple_choice",
                    "prompt": "Which phrase signals partial agreement?",
                    "options": ["To some extent, ...", "Absolutely not.", "No comment."],
                    "correct_answer": "To some extent, ...",
                },
                {
                    "key": "that_said_usage",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a limitation politely?",
                    "options": ["That said, ...", "You're wrong.", "Whatever."],
                    "correct_answer": "That said, ...",
                },
                {
                    "key": "in_principle_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "in principle" mean?',
                    "options": ["secara prinsip (ide dasarnya)", "secara rahasia", "secara kebetulan"],
                    "correct_answer": "secara prinsip (ide dasarnya)",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_qualifying_opinion",
                "opening_line": "Should we adopt the new policy immediately?",
                "learner_goal": "State a nuanced opinion with scope, limitation, and a measured suggestion.",
                "turns": [
                    {
                        "coach": "Should we adopt the new policy immediately?",
                        "hint": "Jawab dengan partial agreement + scope.",
                        "sample_answer": "To some extent, yes—especially for new projects.",
                        "focus": "Scope",
                        "expected_keywords": ["to some extent", "especially"],
                    },
                    {
                        "coach": "So you're fully in favor?",
                        "hint": "Broadly speaking... That said...",
                        "sample_answer": "Broadly speaking, I support it. That said, we need a clear exception for legacy systems.",
                        "focus": "Limitation",
                        "expected_keywords": ["broadly", "that said", "exception"],
                    },
                    {
                        "coach": "What would you suggest instead?",
                        "hint": "Propose a phased approach.",
                        "sample_answer": "I'd phase it in over two quarters and review adoption data along the way.",
                        "focus": "Suggestion",
                        "expected_keywords": ["phase", "review"],
                    },
                ],
                "target_phrases": ["To some extent, ...", "That said, ...", "In principle ..., but ..."],
            },
            "reading_support": "Nuance comes from signaling scope and limits. Use partial agreement, then add a constraint (that said) and a measured alternative rather than a blunt yes/no.",
            "writing_support_lines": [
                "Write 8 lines:",
                "1. To some extent, ...",
                "2. Broadly speaking, ...",
                "3. That said, ...",
                "4. In principle ..., but ...",
                "5. The main concern is ...",
                "6. I'd phase it in over ...",
                "7. We'll review ... along the way.",
                "8. On balance, I think ...",
            ],
            "goal_examples": ["To some extent, ...", "That said, ...", "In principle ..., but ..."],
        },
        {
            "lesson_key": "lesson-02-expressing-certainty-and-doubt",
            "slug": "expressing-certainty-and-doubt",
            "title": "Expressing Certainty and Doubt",
            "conversation_situation": "certainty_and_doubt",
            "conversation_goal": "Express degrees of certainty and doubt using precise language and evidence framing.",
            "grammar_summary": "Use I'm fairly confident... / I'm not entirely convinced... / There's a strong chance... / It's unlikely that... to calibrate certainty.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu diskusi strategi. Kamu harus bilang mana yang kamu yakin, mana yang kamu ragu, tanpa terdengar ragu-ragu atau terlalu absolut.",
            "dialogue": [
                ("Jordan", "Will this change reduce complaints?"),
                ("Mina", "I'm fairly confident it will, given the support trends."),
                ("Jordan", "So we're safe to roll it out broadly?"),
                ("Mina", "I'm not entirely convinced. There's a strong chance we'll see edge cases."),
                ("Jordan", "Is it risky, then?"),
                ("Mina", "It's unlikely that we'll break core flows, but we should monitor closely."),
                ("Jordan", "What do you propose?"),
                ("Mina", "Let's start with a limited rollout and define clear success metrics."),
            ],
            "translations": [
                ("Jordan", "Will this change reduce complaints?", "Apakah perubahan ini bakal ngurangin komplain?"),
                ("Mina", "I'm fairly confident it will, given the support trends.", "Aku cukup yakin iya, melihat tren di support."),
                ("Jordan", "So we're safe to roll it out broadly?", "Jadi aman untuk rollout luas?"),
                ("Mina", "I'm not entirely convinced. There's a strong chance we'll see edge cases.", "Aku belum sepenuhnya yakin. Ada kemungkinan besar kita ketemu edge case."),
                ("Jordan", "Is it risky, then?", "Berarti ini risky?"),
                ("Mina", "It's unlikely that we'll break core flows, but we should monitor closely.", "Kemungkinan kecil kita merusak alur inti, tapi kita harus monitor ketat."),
                ("Jordan", "What do you propose?", "Kamu usul apa?"),
                ("Mina", "Let's start with a limited rollout and define clear success metrics.", "Kita mulai rollout terbatas dan definisikan metrik sukses yang jelas."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'm fairly confident it will, given the support trends.",
                    "meaning_id": "Aku cukup yakin iya, melihat tren di support.",
                    "usage_note": "High confidence with evidence framing.",
                    "common_mistake": "Do not claim certainty without evidence; add given the data/trends.",
                },
                {
                    "phrase": "I'm not entirely convinced.",
                    "meaning_id": "Aku belum sepenuhnya yakin.",
                    "usage_note": "Polite doubt without sounding dismissive.",
                    "common_mistake": 'Do not say "I am not convinced at all" unless you mean it.',
                },
                {
                    "phrase": "There's a strong chance we'll see edge cases.",
                    "meaning_id": "Ada kemungkinan besar kita ketemu edge case.",
                    "usage_note": "Strong probability language.",
                    "common_mistake": "Do not say maybe many; be specific (strong chance).",
                },
                {
                    "phrase": "It's unlikely that we'll break core flows, but we should monitor closely.",
                    "meaning_id": "Kemungkinan kecil kita merusak alur inti, tapi kita harus monitor ketat.",
                    "usage_note": "Low probability + mitigation.",
                    "common_mistake": "Do not stop at unlikely; add monitoring.",
                },
                {
                    "phrase": "Let's start with a limited rollout.",
                    "meaning_id": "Kita mulai rollout terbatas.",
                    "usage_note": "A safe next step when uncertain.",
                    "common_mistake": "Do not jump to full rollout when doubt exists.",
                },
            ],
            "grammar_md": [
                ("Degrees of certainty", ["I'm fairly confident ...", "I'm not entirely convinced ..."]),
                ("Probability + mitigation", ["There's a strong chance ...", "It's unlikely that ..., but ..."]),
            ],
            "pronunciation": [
                ("confident", "KON-fi-dent."),
                ("entirely", "en-TY-er-lee."),
                ("unlikely", "un-LYKE-lee."),
            ],
            "response_prompts": [
                {
                    "prompt": "Express high confidence with evidence.",
                    "target_response": "I'm fairly confident it will, given the support trends.",
                    "acceptable_variations": [
                        "I'm fairly confident it will, given the support trends.",
                        "I'm fairly confident it will, based on the data we have.",
                    ],
                },
                {
                    "prompt": "Express polite doubt.",
                    "target_response": "I'm not entirely convinced.",
                    "acceptable_variations": ["I'm not entirely convinced.", "I'm not fully convinced yet."],
                },
                {
                    "prompt": "Express low probability with mitigation.",
                    "target_response": "It's unlikely that we'll break core flows, but we should monitor closely.",
                    "acceptable_variations": [
                        "It's unlikely that we'll break core flows, but we should monitor closely.",
                        "It's unlikely that it will fail, but we should monitor it closely.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "fairly_confident",
                    "type": "multiple_choice",
                    "prompt": "Which phrase shows high confidence but not absolute certainty?",
                    "options": ["I'm fairly confident ...", "I'm 100% sure.", "No idea."],
                    "correct_answer": "I'm fairly confident ...",
                },
                {
                    "key": "not_entirely_convinced",
                    "type": "multiple_choice",
                    "prompt": "Which phrase expresses polite doubt?",
                    "options": ["I'm not entirely convinced.", "You are wrong.", "It's impossible."],
                    "correct_answer": "I'm not entirely convinced.",
                },
                {
                    "key": "unlikely_usage",
                    "type": "multiple_choice",
                    "prompt": "Which sentence uses unlikely correctly?",
                    "options": [
                        "It's unlikely that we'll break core flows.",
                        "It's unlikely we breaked core flows.",
                        "Unlikely is break.",
                    ],
                    "correct_answer": "It's unlikely that we'll break core flows.",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_certainty_doubt",
                "opening_line": "Will this change work as expected?",
                "learner_goal": "Express calibrated certainty and propose a safe next step.",
                "turns": [
                    {
                        "coach": "Will this change work as expected?",
                        "hint": "Jawab dengan I'm fairly confident... given...",
                        "sample_answer": "I'm fairly confident it will, given the support trends.",
                        "focus": "Confidence",
                        "expected_keywords": ["fairly confident", "given"],
                    },
                    {
                        "coach": "So we can roll it out broadly?",
                        "hint": "I'm not entirely convinced... strong chance...",
                        "sample_answer": "I'm not entirely convinced. There's a strong chance we'll see edge cases.",
                        "focus": "Doubt",
                        "expected_keywords": ["not entirely convinced", "strong chance"],
                    },
                    {
                        "coach": "Close with a safe plan.",
                        "hint": "Limited rollout + metrics.",
                        "sample_answer": "Let's start with a limited rollout and define clear success metrics.",
                        "focus": "Plan",
                        "expected_keywords": ["limited rollout", "metrics"],
                    },
                ],
                "target_phrases": ["I'm fairly confident ...", "I'm not entirely convinced ...", "It's unlikely that ..., but ..."],
            },
            "reading_support": "At C1 level, sounding confident means calibrating certainty. Use fairly confident for strong belief, not entirely convinced for polite doubt, and unlikely for low probability—then add a mitigation plan.",
            "writing_support_lines": [
                "Write 8 lines:",
                "1. I'm fairly confident ...",
                "2. Given the data, ...",
                "3. I'm not entirely convinced ...",
                "4. There's a strong chance ...",
                "5. It's unlikely that ...",
                "6. But we should monitor ...",
                "7. Let's start with a limited rollout ...",
                "8. And define clear success metrics.",
            ],
            "goal_examples": ["I'm fairly confident ...", "I'm not entirely convinced ...", "It's unlikely that ..., but ..."],
        },
        {
            "lesson_key": "lesson-03-balancing-two-viewpoints",
            "slug": "balancing-two-viewpoints",
            "title": "Balancing Two Viewpoints",
            "conversation_situation": "balancing_viewpoints",
            "conversation_goal": "Balance two viewpoints fairly and reach a nuanced conclusion.",
            "grammar_summary": "Use On the one hand... / On the other hand... / While it's true that... / On balance... to weigh perspectives.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu diminta menilai dua sisi. Kamu harus adil, jelasin pro-kontra, lalu kasih kesimpulan yang seimbang.",
            "dialogue": [
                ("Jordan", "Should we invest in growth or stability this quarter?"),
                ("Mina", "On the one hand, growth initiatives could unlock new revenue."),
                ("Jordan", "And on the other hand?"),
                ("Mina", "On the other hand, stability work reduces long-term risk."),
                ("Jordan", "So what's your take?"),
                ("Mina", "While it's true that growth matters, the current incident rate is concerning."),
                ("Jordan", "So you lean toward stability?"),
                ("Mina", "On balance, yes—but I'd ring-fence a small budget for growth experiments."),
            ],
            "translations": [
                ("Jordan", "Should we invest in growth or stability this quarter?", "Kuartal ini kita invest ke growth atau stability?"),
                ("Mina", "On the one hand, growth initiatives could unlock new revenue.", "Di satu sisi, inisiatif growth bisa buka revenue baru."),
                ("Jordan", "And on the other hand?", "Kalau sisi lainnya?"),
                ("Mina", "On the other hand, stability work reduces long-term risk.", "Di sisi lain, kerja stability ngurangin risiko jangka panjang."),
                ("Jordan", "So what's your take?", "Jadi menurut kamu gimana?"),
                ("Mina", "While it's true that growth matters, the current incident rate is concerning.", "Walau benar growth itu penting, tingkat incident sekarang cukup mengkhawatirkan."),
                ("Jordan", "So you lean toward stability?", "Berarti kamu condong ke stability?"),
                ("Mina", "On balance, yes—but I'd ring-fence a small budget for growth experiments.", "Secara keseluruhan, iya—tapi aku sisihkan budget kecil buat eksperimen growth."),
            ],
            "useful_phrases": [
                {
                    "phrase": "On the one hand, growth initiatives could unlock new revenue.",
                    "meaning_id": "Di satu sisi, inisiatif growth bisa buka revenue baru.",
                    "usage_note": "Introduce one viewpoint fairly.",
                    "common_mistake": "Do not argue only one side; present both.",
                },
                {
                    "phrase": "On the other hand, stability work reduces long-term risk.",
                    "meaning_id": "Di sisi lain, kerja stability ngurangin risiko jangka panjang.",
                    "usage_note": "Contrast the second viewpoint.",
                    "common_mistake": "Do not repeat the same point; show a real contrast.",
                },
                {
                    "phrase": "While it's true that growth matters, the incident rate is concerning.",
                    "meaning_id": "Walau benar growth itu penting, tingkat incident mengkhawatirkan.",
                    "usage_note": "Acknowledge a point then pivot.",
                    "common_mistake": "Do not dismiss; acknowledge first with while it's true.",
                },
                {
                    "phrase": "On balance, I'd prioritize stability.",
                    "meaning_id": "Secara keseluruhan, aku prioritasin stability.",
                    "usage_note": "Give a nuanced conclusion after weighing.",
                    "common_mistake": "Do not conclude without weighing both sides first.",
                },
                {
                    "phrase": "I'd ring-fence a small budget for experiments.",
                    "meaning_id": "Aku sisihkan budget kecil untuk eksperimen.",
                    "usage_note": "Practical compromise language.",
                    "common_mistake": "Do not promise too much; specify small budget.",
                },
            ],
            "grammar_md": [
                ("Balancing viewpoints", ["On the one hand, ...", "On the other hand, ..."]),
                ("Nuanced conclusion", ["While it's true that ..., ...", "On balance, ..."]),
            ],
            "pronunciation": [
                ("initiative", "ih-NISH-uh-tiv."),
                ("concerning", "kun-SER-ning."),
                ("ring-fence", "RING-fens."),
            ],
            "response_prompts": [
                {
                    "prompt": "Present both viewpoints.",
                    "target_response": "On the one hand, growth could unlock new revenue. On the other hand, stability reduces long-term risk.",
                    "acceptable_variations": [
                        "On the one hand, growth could unlock new revenue. On the other hand, stability reduces long-term risk.",
                        "On the one hand, speed matters. On the other hand, reliability matters.",
                    ],
                },
                {
                    "prompt": "Acknowledge then pivot.",
                    "target_response": "While it's true that growth matters, the current incident rate is concerning.",
                    "acceptable_variations": [
                        "While it's true that growth matters, the current incident rate is concerning.",
                        "While it's true that speed matters, quality issues are concerning.",
                    ],
                },
                {
                    "prompt": "Conclude with a balanced plan.",
                    "target_response": "On balance, I'd prioritize stability—but ring-fence a small budget for growth experiments.",
                    "acceptable_variations": [
                        "On balance, I'd prioritize stability—but ring-fence a small budget for growth experiments.",
                        "On balance, I'd prioritize reliability, with a small pilot for new features.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "on_balance",
                    "type": "multiple_choice",
                    "prompt": 'What does "on balance" mean?',
                    "options": ["secara keseluruhan setelah menimbang", "tanpa alasan", "secara acak"],
                    "correct_answer": "secara keseluruhan setelah menimbang",
                },
                {
                    "key": "both_sides",
                    "type": "multiple_choice",
                    "prompt": "Which pair correctly balances viewpoints?",
                    "options": ["On the one hand... On the other hand...", "Because... because...", "No."],
                    "correct_answer": "On the one hand... On the other hand...",
                },
                {
                    "key": "while_true",
                    "type": "multiple_choice",
                    "prompt": "Which phrase acknowledges a point then pivots?",
                    "options": ["While it's true that ..., ...", "You are wrong.", "Stop."],
                    "correct_answer": "While it's true that ..., ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_balancing_viewpoints",
                "opening_line": "We need to choose between growth and stability.",
                "learner_goal": "Balance two viewpoints and give a nuanced conclusion.",
                "turns": [
                    {
                        "coach": "We need to choose between growth and stability.",
                        "hint": "Mulai dengan on the one hand... on the other hand...",
                        "sample_answer": "On the one hand, growth could unlock new revenue. On the other hand, stability reduces long-term risk.",
                        "focus": "Balance",
                        "expected_keywords": ["on the one hand", "on the other hand"],
                    },
                    {
                        "coach": "Give a nuanced conclusion.",
                        "hint": "While it's true... On balance...",
                        "sample_answer": "While it's true that growth matters, the incident rate is concerning. On balance, I'd prioritize stability.",
                        "focus": "Conclusion",
                        "expected_keywords": ["while it's true", "on balance"],
                    },
                    {
                        "coach": "Offer a compromise plan.",
                        "hint": "Ring-fence a small budget...",
                        "sample_answer": "I'd ring-fence a small budget for growth experiments while we focus on stability.",
                        "focus": "Compromise",
                        "expected_keywords": ["ring-fence", "budget"],
                    },
                ],
                "target_phrases": ["On the one hand, ...", "While it's true that ..., ...", "On balance, ..."],
            },
            "reading_support": "A balanced viewpoint sounds fair and strategic. Present both sides, acknowledge the strongest point from each, then conclude with a compromise plan when possible.",
            "writing_support_lines": [
                "Write 9 lines:",
                "1. On the one hand, ...",
                "2. This could ...",
                "3. On the other hand, ...",
                "4. This reduces ...",
                "5. While it's true that ..., ...",
                "6. That said, ...",
                "7. On balance, I would ...",
                "8. I'd ring-fence ...",
                "9. Does that sound reasonable?",
            ],
            "goal_examples": ["On the one hand, ...", "While it's true that ..., ...", "On balance, ..."],
        },
        {
            "lesson_key": "lesson-04-softening-disagreement",
            "slug": "softening-disagreement",
            "title": "Softening Disagreement",
            "conversation_situation": "softened_disagreement",
            "conversation_goal": "Disagree tactfully while staying precise and constructive.",
            "grammar_summary": "Use I see your point, but... / I'm not sure I'd go that far... / With respect, ... / I might frame it differently... to disagree softly.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu nggak setuju di meeting, tapi kamu harus tetap sopan, jelas, dan konstruktif.",
            "dialogue": [
                ("Jordan", "I think we should launch next week, no matter what."),
                ("Mina", "I see your point, but I'm not sure I'd go that far."),
                ("Jordan", "Why not?"),
                ("Mina", "With respect, the current error rate suggests we're not ready."),
                ("Jordan", "So you want to delay?"),
                ("Mina", "I might frame it differently: we launch a limited version next week and keep the rest behind a feature flag."),
                ("Jordan", "That could work."),
                ("Mina", "Great—this way we protect reliability without losing momentum."),
            ],
            "translations": [
                ("Jordan", "I think we should launch next week, no matter what.", "Aku pikir kita harus launch minggu depan, apapun yang terjadi."),
                ("Mina", "I see your point, but I'm not sure I'd go that far.", "Aku paham poin kamu, tapi aku nggak yakin aku akan sejauh itu."),
                ("Jordan", "Why not?", "Kenapa?"),
                ("Mina", "With respect, the current error rate suggests we're not ready.", "Dengan hormat, error rate sekarang menunjukkan kita belum siap."),
                ("Jordan", "So you want to delay?", "Jadi kamu mau delay?"),
                ("Mina", "I might frame it differently: we launch a limited version next week and keep the rest behind a feature flag.", "Aku akan framing beda: kita launch versi terbatas minggu depan dan sisanya pakai feature flag."),
                ("Jordan", "That could work.", "Bisa juga."),
                ("Mina", "Great—this way we protect reliability without losing momentum.", "Oke—dengan begitu kita jaga reliability tanpa kehilangan momentum."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I see your point, but I'm not sure I'd go that far.",
                    "meaning_id": "Aku paham poin kamu, tapi aku nggak yakin aku akan sejauh itu.",
                    "usage_note": "Acknowledge then disagree softly.",
                    "common_mistake": "Do not say you're wrong; acknowledge first.",
                },
                {
                    "phrase": "With respect, the current error rate suggests we're not ready.",
                    "meaning_id": "Dengan hormat, error rate sekarang menunjukkan kita belum siap.",
                    "usage_note": "Polite disagreement with evidence.",
                    "common_mistake": "Do not sound emotional; use evidence language.",
                },
                {
                    "phrase": "I might frame it differently: ...",
                    "meaning_id": "Aku akan framing beda: ...",
                    "usage_note": "Offer an alternative without confrontation.",
                    "common_mistake": "Do not reject without proposing an alternative.",
                },
                {
                    "phrase": "That could work.",
                    "meaning_id": "Bisa juga.",
                    "usage_note": "A flexible response to align.",
                    "common_mistake": "Do not be rigid; show openness.",
                },
                {
                    "phrase": "This way we protect reliability without losing momentum.",
                    "meaning_id": "Dengan begitu kita jaga reliability tanpa kehilangan momentum.",
                    "usage_note": "Summarize benefits of the compromise.",
                    "common_mistake": "Do not oversell; keep it practical.",
                },
            ],
            "grammar_md": [
                ("Soft disagreement", ["I see your point, but ...", "I'm not sure I'd go that far."]),
                ("Alternatives", ["I might frame it differently: ...", "What if we ... instead?"]),
            ],
            "pronunciation": [
                ("respect", "ri-SPEKT."),
                ("suggests", "suh-JESTS."),
                ("momentum", "moh-MEN-tum."),
            ],
            "response_prompts": [
                {
                    "prompt": "Disagree tactfully.",
                    "target_response": "I see your point, but I'm not sure I'd go that far.",
                    "acceptable_variations": [
                        "I see your point, but I'm not sure I'd go that far.",
                        "I see your point, but I'm not sure we should do it that way.",
                    ],
                },
                {
                    "prompt": "Use respectful evidence language.",
                    "target_response": "With respect, the current error rate suggests we're not ready.",
                    "acceptable_variations": [
                        "With respect, the current error rate suggests we're not ready.",
                        "With respect, the current data suggests we should wait.",
                    ],
                },
                {
                    "prompt": "Offer an alternative.",
                    "target_response": "I might frame it differently: we launch a limited version next week and keep the rest behind a feature flag.",
                    "acceptable_variations": [
                        "I might frame it differently: we launch a limited version next week and keep the rest behind a feature flag.",
                        "I might frame it differently: we do a limited rollout first, then expand.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "soft_disagree",
                    "type": "multiple_choice",
                    "prompt": "Which phrase softens disagreement?",
                    "options": ["I see your point, but ...", "You're wrong.", "No."],
                    "correct_answer": "I see your point, but ...",
                },
                {
                    "key": "go_that_far",
                    "type": "multiple_choice",
                    "prompt": 'What does "I wouldn\'t go that far" mean?',
                    "options": ["aku tidak setuju sepenuhnya", "aku setuju total", "aku tidak mengerti"],
                    "correct_answer": "aku tidak setuju sepenuhnya",
                },
                {
                    "key": "frame_it",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces an alternative framing?",
                    "options": ["I might frame it differently: ...", "Stop.", "Whatever."],
                    "correct_answer": "I might frame it differently: ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_soft_disagreement",
                "opening_line": "We should launch next week, no matter what.",
                "learner_goal": "Disagree tactfully and offer a constructive alternative.",
                "turns": [
                    {
                        "coach": "We should launch next week, no matter what.",
                        "hint": "Acknowledge + soften.",
                        "sample_answer": "I see your point, but I'm not sure I'd go that far.",
                        "focus": "Soften",
                        "expected_keywords": ["see your point", "not sure"],
                    },
                    {
                        "coach": "Explain your concern respectfully.",
                        "hint": "With respect... suggests...",
                        "sample_answer": "With respect, the current error rate suggests we're not ready.",
                        "focus": "Evidence",
                        "expected_keywords": ["with respect", "suggests"],
                    },
                    {
                        "coach": "Offer an alternative plan.",
                        "hint": "I might frame it differently...",
                        "sample_answer": "I might frame it differently: we launch a limited version next week and keep the rest behind a feature flag.",
                        "focus": "Alternative",
                        "expected_keywords": ["frame", "limited", "feature flag"],
                    },
                ],
                "target_phrases": ["I see your point, but ...", "With respect, ...", "I might frame it differently: ..."],
            },
            "reading_support": "Softening disagreement is about tone and structure: acknowledge the point, state your concern with evidence, then propose an alternative that preserves the shared goal.",
            "writing_support_lines": [
                "Write 9 lines:",
                "1. I see your point, but ...",
                "2. I'm not sure I'd go that far ...",
                "3. With respect, ... suggests ...",
                "4. The main risk is ...",
                "5. That said, ...",
                "6. I might frame it differently: ...",
                "7. This way, we ...",
                "8. Without losing ...",
                "9. Does that work for you?",
            ],
            "goal_examples": ["I see your point, but ...", "With respect, ...", "I might frame it differently: ..."],
        },
        {
            "lesson_key": "lesson-05-nuanced-opinion-mission",
            "slug": "nuanced-opinion-mission",
            "title": "Nuanced Opinion Mission",
            "conversation_situation": "mission_nuanced_opinion",
            "conversation_goal": "Hold a nuanced discussion: qualify your stance, calibrate certainty, balance viewpoints, and disagree tactfully.",
            "grammar_summary": "Combine: to some extent / that said / fairly confident / not entirely convinced / on balance / I see your point, but ...",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Misi: kamu ikut diskusi yang menuntut opini yang nuanced. Kamu harus presisi, sopan, dan tetap decisive.",
            "dialogue": [
                ("Jordan", "Should we adopt the new policy right away?"),
                ("Mina", "To some extent, yes—especially for new projects. That said, we need exceptions for legacy systems."),
                ("Jordan", "Are you confident it will help?"),
                ("Mina", "I'm fairly confident it will, but I'm not entirely convinced we won't see edge cases."),
                ("Jordan", "So do we prioritize speed or stability?"),
                ("Mina", "On the one hand, speed matters. On the other hand, stability reduces risk. On balance, I'd prioritize stability with a limited rollout."),
                ("Jordan", "I still think we should launch next week no matter what."),
                ("Mina", "I see your point, but I'm not sure I'd go that far. I might frame it differently: limited launch next week, full rollout after we review the data."),
            ],
            "translations": [
                ("Jordan", "Should we adopt the new policy right away?", "Kita adopsi kebijakan baru ini langsung nggak?"),
                ("Mina", "To some extent, yes—especially for new projects. That said, we need exceptions for legacy systems.", "Sampai batas tertentu, iya—terutama untuk project baru. Tapi, kita butuh pengecualian untuk sistem lama."),
                ("Jordan", "Are you confident it will help?", "Kamu yakin itu bakal membantu?"),
                ("Mina", "I'm fairly confident it will, but I'm not entirely convinced we won't see edge cases.", "Aku cukup yakin iya, tapi aku belum sepenuhnya yakin kita nggak akan ketemu edge case."),
                ("Jordan", "So do we prioritize speed or stability?", "Jadi kita prioritasin speed atau stability?"),
                ("Mina", "On the one hand, speed matters. On the other hand, stability reduces risk. On balance, I'd prioritize stability with a limited rollout.", "Di satu sisi, speed itu penting. Di sisi lain, stability ngurangin risiko. Secara keseluruhan, aku prioritasin stability dengan rollout terbatas."),
                ("Jordan", "I still think we should launch next week no matter what.", "Aku tetap pikir kita harus launch minggu depan apapun yang terjadi."),
                ("Mina", "I see your point, but I'm not sure I'd go that far. I might frame it differently: limited launch next week, full rollout after we review the data.", "Aku paham poin kamu, tapi aku nggak yakin aku akan sejauh itu. Aku akan framing beda: launch terbatas minggu depan, rollout penuh setelah kita review data."),
            ],
            "useful_phrases": [
                {
                    "phrase": "To some extent, yes—especially for new projects.",
                    "meaning_id": "Sampai batas tertentu, iya—terutama untuk project baru.",
                    "usage_note": "Partial agreement + scope.",
                    "common_mistake": "Don't answer with only yes/no.",
                },
                {
                    "phrase": "I'm fairly confident it will, but I'm not entirely convinced.",
                    "meaning_id": "Aku cukup yakin, tapi belum sepenuhnya yakin.",
                    "usage_note": "Calibrate certainty.",
                    "common_mistake": "Don't sound absolute when evidence is limited.",
                },
                {
                    "phrase": "On balance, I'd prioritize stability with a limited rollout.",
                    "meaning_id": "Secara keseluruhan, aku prioritasin stability dengan rollout terbatas.",
                    "usage_note": "Balanced conclusion.",
                    "common_mistake": "Don't conclude without weighing both sides.",
                },
                {
                    "phrase": "I see your point, but I'm not sure I'd go that far.",
                    "meaning_id": "Aku paham poin kamu, tapi aku nggak yakin aku akan sejauh itu.",
                    "usage_note": "Soft disagreement.",
                    "common_mistake": "Don't be confrontational; acknowledge first.",
                },
                {
                    "phrase": "I might frame it differently: limited launch first, then review the data.",
                    "meaning_id": "Aku akan framing beda: launch terbatas dulu, lalu review data.",
                    "usage_note": "Alternative proposal.",
                    "common_mistake": "Don't reject without suggesting an alternative.",
                },
            ],
            "grammar_md": [
                (
                    "Nuanced discussion toolkit",
                    [
                        "To some extent, ... That said, ...",
                        "I'm fairly confident ..., but I'm not entirely convinced ...",
                        "On the one hand ... On the other hand ... On balance ...",
                        "I see your point, but ... I might frame it differently: ...",
                    ],
                )
            ],
            "pronunciation": [
                ("nuanced", "NOO-ahnst."),
                ("calibrate", "KAL-uh-brayt."),
                ("decisive", "di-SY-siv."),
            ],
            "response_prompts": [
                {
                    "prompt": "Qualify your stance with a limitation.",
                    "target_response": "To some extent, yes—especially for new projects. That said, we need exceptions for legacy systems.",
                    "acceptable_variations": [
                        "To some extent, yes—especially for new projects. That said, we need exceptions for legacy systems.",
                        "To some extent, yes. That said, we should define guardrails first.",
                    ],
                },
                {
                    "prompt": "Balance two viewpoints and conclude.",
                    "target_response": "On the one hand, speed matters. On the other hand, stability reduces risk. On balance, I'd prioritize stability with a limited rollout.",
                    "acceptable_variations": [
                        "On the one hand, speed matters. On the other hand, stability reduces risk. On balance, I'd prioritize stability with a limited rollout.",
                        "On the one hand, cost matters. On the other hand, quality matters. On balance, I'd prioritize quality.",
                    ],
                },
                {
                    "prompt": "Disagree softly and propose an alternative.",
                    "target_response": "I see your point, but I'm not sure I'd go that far. I might frame it differently: limited launch next week, full rollout after we review the data.",
                    "acceptable_variations": [
                        "I see your point, but I'm not sure I'd go that far. I might frame it differently: limited launch next week, full rollout after we review the data.",
                        "I see your point, but I'm not sure I'd go that far. I might frame it differently: pilot first, then expand.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "nuance_marker",
                    "type": "multiple_choice",
                    "prompt": "Which phrase signals a nuanced stance?",
                    "options": ["To some extent, ...", "Always.", "Never."],
                    "correct_answer": "To some extent, ...",
                },
                {
                    "key": "soft_disagree_marker",
                    "type": "multiple_choice",
                    "prompt": "Which phrase softens disagreement?",
                    "options": ["I see your point, but ...", "You're wrong.", "No."],
                    "correct_answer": "I see your point, but ...",
                },
                {
                    "key": "on_balance_marker",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a balanced conclusion?",
                    "options": ["On balance, ...", "Anyway, ...", "Randomly, ..."],
                    "correct_answer": "On balance, ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_nuance_mission",
                "opening_line": "We need a nuanced view before we decide.",
                "learner_goal": "Show nuance, balance, calibrated certainty, and soft disagreement in one discussion.",
                "turns": [
                    {
                        "coach": "Start with a nuanced stance and a limitation.",
                        "hint": "To some extent... That said...",
                        "sample_answer": "To some extent, yes—especially for new projects. That said, we need exceptions for legacy systems.",
                        "focus": "Nuanced stance",
                        "expected_keywords": ["to some extent", "that said"],
                    },
                    {
                        "coach": "Balance two viewpoints and conclude.",
                        "hint": "On the one hand... On the other hand... On balance...",
                        "sample_answer": "On the one hand, speed matters. On the other hand, stability reduces risk. On balance, I'd prioritize stability with a limited rollout.",
                        "focus": "Balance",
                        "expected_keywords": ["on the one hand", "on the other hand", "on balance"],
                    },
                    {
                        "coach": "Disagree softly and propose an alternative plan.",
                        "hint": "I see your point, but... I might frame it differently...",
                        "sample_answer": "I see your point, but I'm not sure I'd go that far. I might frame it differently: limited launch first, then full rollout after we review the data.",
                        "focus": "Soft disagreement",
                        "expected_keywords": ["see your point", "frame", "limited"],
                    },
                ],
                "target_phrases": ["To some extent, ...", "On balance, ...", "I see your point, but ..."],
            },
            "reading_support": "In a mission-level discussion, you sound C1 when you are precise and flexible: qualify your stance, calibrate certainty, balance viewpoints, and disagree tactfully while offering alternatives.",
            "writing_support_lines": [
                "Write your mission (12 lines):",
                "1. To some extent, ...",
                "2. Broadly speaking, ...",
                "3. That said, ...",
                "4. I'm fairly confident ..., but ...",
                "5. I'm not entirely convinced ...",
                "6. On the one hand, ...",
                "7. On the other hand, ...",
                "8. On balance, ...",
                "9. I see your point, but ...",
                "10. With respect, ... suggests ...",
                "11. I might frame it differently: ...",
                "12. Next steps are ...",
            ],
            "goal_examples": ["To some extent, ...", "I'm fairly confident ...", "On balance, ..."],
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

