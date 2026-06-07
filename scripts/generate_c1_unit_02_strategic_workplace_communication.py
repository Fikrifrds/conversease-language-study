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
            "- Tone: strategic, calm, professional",
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

        Read it again and underline the strategy words (stakeholder, alignment, expectation, constraint, risk, timeline).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "C1"
    root = Path("content/curriculum/english/C1")
    units_root = root / "units"
    unit_key = "unit-02-strategic-workplace-communication"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-02-strategic-workplace-communication
            level_code: C1
            title: Strategic Workplace Communication
            main_conversation_outcome: Communicate strategically in complex professional situations.
            status: in_production
            lessons:
              - lesson-01-aligning-stakeholders
              - lesson-02-managing-expectations
              - lesson-03-handling-sensitive-feedback
              - lesson-04-communicating-risk
              - lesson-05-strategic-workplace-mission
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
            "lesson_key": "lesson-01-aligning-stakeholders",
            "slug": "aligning-stakeholders",
            "title": "Aligning Stakeholders",
            "conversation_situation": "stakeholder_alignment_meeting",
            "conversation_goal": "Align stakeholders by clarifying priorities, surfacing constraints, and confirming a shared decision.",
            "grammar_summary": "Use To make sure we're aligned... / From your perspective... / The key constraint is... / Can we agree that... to align stakeholders.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu fasilitasi alignment meeting lintas tim. Kamu klarifikasi prioritas tiap pihak, highlight constraint, lalu sepakati keputusan.",
            "dialogue": [
                ("Jordan", "We have conflicting priorities across teams."),
                ("Mina", "To make sure we're aligned, can you share your top priority?"),
                ("Jordan", "Speed. We need impact this quarter."),
                ("Mina", "Got it. From your perspective, what's the biggest constraint?"),
                ("Jordan", "We can't add headcount."),
                ("Mina", "Understood. The key constraint is capacity. Can we agree that we ship a smaller scope first?"),
                ("Jordan", "That sounds reasonable."),
                ("Mina", "Great. I'll capture the decision and circulate it today."),
            ],
            "translations": [
                ("Jordan", "We have conflicting priorities across teams.", "Prioritas antar tim bentrok."),
                ("Mina", "To make sure we're aligned, can you share your top priority?", "Biar kita aligned, bisa share prioritas utama kamu?"),
                ("Jordan", "Speed. We need impact this quarter.", "Kecepatan. Kita butuh impact kuartal ini."),
                ("Mina", "Got it. From your perspective, what's the biggest constraint?", "Oke. Dari perspektif kamu, constraint terbesarnya apa?"),
                ("Jordan", "We can't add headcount.", "Kita nggak bisa nambah orang."),
                ("Mina", "Understood. The key constraint is capacity. Can we agree that we ship a smaller scope first?", "Oke. Constraint utamanya kapasitas. Kita sepakat nggak kalau kita ship scope kecil dulu?"),
                ("Jordan", "That sounds reasonable.", "Masuk akal."),
                ("Mina", "Great. I'll capture the decision and circulate it today.", "Oke. Aku rangkum keputusannya dan share hari ini."),
            ],
            "useful_phrases": [
                {
                    "phrase": "To make sure we're aligned, can you share your top priority?",
                    "meaning_id": "Biar kita aligned, bisa share prioritas utama kamu?",
                    "usage_note": "A strategic opener to align goals.",
                    "common_mistake": "Do not assume priorities; ask explicitly.",
                },
                {
                    "phrase": "From your perspective, what's the biggest constraint?",
                    "meaning_id": "Dari perspektif kamu, constraint terbesarnya apa?",
                    "usage_note": "Invite constraints without blame.",
                    "common_mistake": "Do not sound accusatory; keep it neutral.",
                },
                {
                    "phrase": "The key constraint is capacity.",
                    "meaning_id": "Constraint utamanya kapasitas.",
                    "usage_note": "Name a constraint clearly.",
                    "common_mistake": "Do not list many constraints; name the key one first.",
                },
                {
                    "phrase": "Can we agree that we ship a smaller scope first?",
                    "meaning_id": "Kita sepakat nggak kalau kita ship scope kecil dulu?",
                    "usage_note": "Move toward a decision.",
                    "common_mistake": "Do not end with open discussion; confirm agreement.",
                },
                {
                    "phrase": "I'll capture the decision and circulate it today.",
                    "meaning_id": "Aku rangkum keputusannya dan share hari ini.",
                    "usage_note": "Close with clear next step.",
                    "common_mistake": 'Do not say "I will capturing"; use I\'ll capture.',
                },
            ],
            "grammar_md": [
                ("Alignment questions", ["To make sure we're aligned, ...", "From your perspective, ..."]),
                ("Decision confirmation", ["Can we agree that ...?", "The key constraint is ..."]),
            ],
            "pronunciation": [
                ("stakeholders", "STAYK-hohl-derz."),
                ("aligned", "uh-LYND."),
                ("constraint", "kun-STRAYNT."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask for top priority to align.",
                    "target_response": "To make sure we're aligned, can you share your top priority?",
                    "acceptable_variations": [
                        "To make sure we're aligned, can you share your top priority?",
                        "To make sure we're aligned, what's your top priority?",
                    ],
                },
                {
                    "prompt": "Ask for key constraint.",
                    "target_response": "From your perspective, what's the biggest constraint?",
                    "acceptable_variations": [
                        "From your perspective, what's the biggest constraint?",
                        "From your perspective, what's the main constraint we should consider?",
                    ],
                },
                {
                    "prompt": "Confirm agreement on a decision.",
                    "target_response": "Can we agree that we ship a smaller scope first?",
                    "acceptable_variations": [
                        "Can we agree that we ship a smaller scope first?",
                        "Can we agree that we start with a smaller scope first?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "aligned_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase checks alignment?",
                    "options": ["To make sure we're aligned, ...", "Stop talking.", "Whatever."],
                    "correct_answer": "To make sure we're aligned, ...",
                },
                {
                    "key": "constraint_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "constraint" mean?',
                    "options": ["batasan/keterbatasan", "hadiah", "pilihan bebas"],
                    "correct_answer": "batasan/keterbatasan",
                },
                {
                    "key": "agree_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase confirms agreement?",
                    "options": ["Can we agree that ...?", "You must agree.", "No."],
                    "correct_answer": "Can we agree that ...?",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_aligning_stakeholders",
                "opening_line": "We have conflicting priorities across teams.",
                "learner_goal": "Align stakeholders by clarifying priorities, constraints, and confirming a shared decision.",
                "turns": [
                    {
                        "coach": "We have conflicting priorities across teams.",
                        "hint": "Mulai dengan alignment question.",
                        "sample_answer": "To make sure we're aligned, can you share your top priority?",
                        "focus": "Priorities",
                        "expected_keywords": ["aligned", "priority"],
                    },
                    {
                        "coach": "Our top priority is speed. What do you ask next?",
                        "hint": "Tanya constraint.",
                        "sample_answer": "Got it. From your perspective, what's the biggest constraint?",
                        "focus": "Constraints",
                        "expected_keywords": ["perspective", "constraint"],
                    },
                    {
                        "coach": "We can't add headcount. Close with a decision.",
                        "hint": "Can we agree that ...",
                        "sample_answer": "Understood. The key constraint is capacity. Can we agree that we ship a smaller scope first?",
                        "focus": "Decision",
                        "expected_keywords": ["key constraint", "agree", "scope"],
                    },
                ],
                "target_phrases": ["To make sure we're aligned, ...", "From your perspective, ...", "Can we agree that ...?"],
            },
            "reading_support": "Stakeholder alignment means turning opinions into decisions. Ask for priorities, surface constraints, propose a trade-off, and confirm agreement with a clear next step.",
            "writing_support_lines": [
                "Write 9 lines:",
                "1. To make sure we're aligned, ...",
                "2. What's your top priority?",
                "3. From your perspective, ...",
                "4. What's the biggest constraint?",
                "5. The key constraint is ...",
                "6. Can we agree that ...?",
                "7. Next steps are ...",
                "8. I'll capture the decision ...",
                "9. And circulate it by ...",
            ],
            "goal_examples": ["To make sure we're aligned, ...", "From your perspective, ...", "Can we agree that ...?"],
        },
        {
            "lesson_key": "lesson-02-managing-expectations",
            "slug": "managing-expectations",
            "title": "Managing Expectations",
            "conversation_situation": "managing_expectations",
            "conversation_goal": "Manage expectations by setting clear boundaries, timelines, and what success looks like.",
            "grammar_summary": "Use What we can commit to is... / The earliest we can deliver is... / To avoid surprises... / I'd rather under-promise... to manage expectations.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Ada permintaan besar. Kamu harus set ekspektasi yang realistis, jelas, dan tetap menjaga hubungan baik.",
            "dialogue": [
                ("Jordan", "Can we deliver the full scope by next week?"),
                ("Mina", "What we can commit to is a smaller release by next week."),
                ("Jordan", "Why not the full scope?"),
                ("Mina", "To avoid surprises, I'd rather under-promise and deliver reliably."),
                ("Jordan", "So when can we deliver everything?"),
                ("Mina", "The earliest we can deliver the full scope is two weeks later, assuming no new blockers."),
                ("Jordan", "Okay. What does success look like?"),
                ("Mina", "Success means fewer incidents and a stable rollout with clear monitoring."),
            ],
            "translations": [
                ("Jordan", "Can we deliver the full scope by next week?", "Kita bisa deliver scope penuh minggu depan nggak?"),
                ("Mina", "What we can commit to is a smaller release by next week.", "Yang bisa kita commit adalah rilis kecil minggu depan."),
                ("Jordan", "Why not the full scope?", "Kenapa nggak scope penuh?"),
                ("Mina", "To avoid surprises, I'd rather under-promise and deliver reliably.", "Biar nggak ada kejutan, aku lebih pilih under-promise dan deliver dengan reliable."),
                ("Jordan", "So when can we deliver everything?", "Jadi kapan bisa deliver semua?"),
                ("Mina", "The earliest we can deliver the full scope is two weeks later, assuming no new blockers.", "Paling cepat kita bisa deliver scope penuh dua minggu setelahnya, asumsi nggak ada blocker baru."),
                ("Jordan", "Okay. What does success look like?", "Oke. Suksesnya seperti apa?"),
                ("Mina", "Success means fewer incidents and a stable rollout with clear monitoring.", "Sukses artinya incident berkurang dan rollout stabil dengan monitoring yang jelas."),
            ],
            "useful_phrases": [
                {
                    "phrase": "What we can commit to is a smaller release by next week.",
                    "meaning_id": "Yang bisa kita commit adalah rilis kecil minggu depan.",
                    "usage_note": "Set a realistic commitment.",
                    "common_mistake": "Do not commit to full scope when it's unrealistic.",
                },
                {
                    "phrase": "To avoid surprises, I'd rather under-promise and deliver reliably.",
                    "meaning_id": "Biar nggak ada kejutan, aku lebih pilih under-promise dan deliver dengan reliable.",
                    "usage_note": "Explain boundary with a principle.",
                    "common_mistake": "Do not blame; focus on reliability.",
                },
                {
                    "phrase": "The earliest we can deliver the full scope is two weeks later.",
                    "meaning_id": "Paling cepat scope penuh dua minggu setelahnya.",
                    "usage_note": "State earliest timeline.",
                    "common_mistake": "Do not say maybe; give a clear earliest date.",
                },
                {
                    "phrase": "Assuming no new blockers.",
                    "meaning_id": "Asumsi nggak ada blocker baru.",
                    "usage_note": "Add a condition politely.",
                    "common_mistake": "Do not hide assumptions; state them.",
                },
                {
                    "phrase": "Success means fewer incidents and a stable rollout.",
                    "meaning_id": "Sukses artinya incident berkurang dan rollout stabil.",
                    "usage_note": "Define success criteria.",
                    "common_mistake": "Do not keep success vague; name metrics.",
                },
            ],
            "grammar_md": [
                ("Commitments", ["What we can commit to is ...", "The earliest we can deliver is ..."]),
                ("Principles + conditions", ["To avoid surprises, ...", "Assuming no new blockers, ..."]),
            ],
            "pronunciation": [
                ("commit", "kuh-MIT."),
                ("reliably", "ri-LYE-uh-blee."),
                ("blocker", "BLOK-er."),
            ],
            "response_prompts": [
                {
                    "prompt": "Set a realistic commitment.",
                    "target_response": "What we can commit to is a smaller release by next week.",
                    "acceptable_variations": [
                        "What we can commit to is a smaller release by next week.",
                        "What we can commit to is a pilot by next week.",
                    ],
                },
                {
                    "prompt": "State earliest timeline with condition.",
                    "target_response": "The earliest we can deliver the full scope is two weeks later, assuming no new blockers.",
                    "acceptable_variations": [
                        "The earliest we can deliver the full scope is two weeks later, assuming no new blockers.",
                        "The earliest we can deliver the full scope is in two weeks, assuming no surprises.",
                    ],
                },
                {
                    "prompt": "Define success criteria.",
                    "target_response": "Success means fewer incidents and a stable rollout with clear monitoring.",
                    "acceptable_variations": [
                        "Success means fewer incidents and a stable rollout with clear monitoring.",
                        "Success means fewer tickets and a stable release.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "commit_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase sets a realistic commitment?",
                    "options": ["What we can commit to is ...", "We promise everything.", "No plan."],
                    "correct_answer": "What we can commit to is ...",
                },
                {
                    "key": "under_promise",
                    "type": "multiple_choice",
                    "prompt": 'What does "under-promise" mean?',
                    "options": ["janji lebih kecil agar pasti deliver", "berbohong", "menolak semua"],
                    "correct_answer": "janji lebih kecil agar pasti deliver",
                },
                {
                    "key": "earliest",
                    "type": "multiple_choice",
                    "prompt": "Which phrase states the earliest timeline?",
                    "options": ["The earliest we can deliver is ...", "Maybe soon.", "Whenever."],
                    "correct_answer": "The earliest we can deliver is ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_managing_expectations",
                "opening_line": "Can we deliver the full scope by next week?",
                "learner_goal": "Set realistic expectations with commitments, conditions, and success criteria.",
                "turns": [
                    {
                        "coach": "Can we deliver the full scope by next week?",
                        "hint": "Start with what you can commit to.",
                        "sample_answer": "What we can commit to is a smaller release by next week.",
                        "focus": "Commitment",
                        "expected_keywords": ["commit", "smaller"],
                    },
                    {
                        "coach": "When can we deliver everything?",
                        "hint": "The earliest we can deliver... assuming...",
                        "sample_answer": "The earliest we can deliver the full scope is two weeks later, assuming no new blockers.",
                        "focus": "Timeline + condition",
                        "expected_keywords": ["earliest", "assuming", "blockers"],
                    },
                    {
                        "coach": "Define success criteria.",
                        "hint": "Success means...",
                        "sample_answer": "Success means fewer incidents and a stable rollout with clear monitoring.",
                        "focus": "Success",
                        "expected_keywords": ["success means", "stable"],
                    },
                ],
                "target_phrases": ["What we can commit to is ...", "The earliest we can deliver is ...", "To avoid surprises, ..."],
            },
            "reading_support": "Managing expectations is about clarity: what you can commit to, what you cannot, the earliest realistic timeline, the assumptions, and what success means in measurable terms.",
            "writing_support_lines": [
                "Write 9 lines:",
                "1. What we can commit to is ...",
                "2. What we can't commit to is ...",
                "3. To avoid surprises, ...",
                "4. The earliest we can deliver is ...",
                "5. Assuming no new blockers, ...",
                "6. Success means ...",
                "7. We'll monitor ...",
                "8. Next steps are ...",
                "9. Does that work for you?",
            ],
            "goal_examples": ["What we can commit to is ...", "The earliest we can deliver is ...", "Success means ..."],
        },
        {
            "lesson_key": "lesson-03-handling-sensitive-feedback",
            "slug": "handling-sensitive-feedback",
            "title": "Handling Sensitive Feedback",
            "conversation_situation": "sensitive_feedback",
            "conversation_goal": "Give sensitive feedback tactfully, focusing on impact and concrete next steps.",
            "grammar_summary": "Use I wanted to flag... / The impact is... / I appreciate..., and... / Would you be open to... to give sensitive feedback.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu perlu kasih feedback sensitif ke stakeholder. Kamu tetap sopan, fokus ke impact, dan tawarkan next step yang konkret.",
            "dialogue": [
                ("Jordan", "How did the last review go?"),
                ("Mina", "I wanted to flag one point about the messaging."),
                ("Jordan", "Sure—what is it?"),
                ("Mina", "The impact is that some teams interpreted it as a hard deadline."),
                ("Jordan", "That's not what I meant."),
                ("Mina", "I appreciate the intent, and I think we can make it clearer with one sentence."),
                ("Jordan", "What would you suggest?"),
                ("Mina", "Would you be open to adding an explicit 'earliest possible' line?"),
            ],
            "translations": [
                ("Jordan", "How did the last review go?", "Gimana hasil review terakhir?"),
                ("Mina", "I wanted to flag one point about the messaging.", "Aku mau highlight satu poin soal messaging-nya."),
                ("Jordan", "Sure—what is it?", "Oke—apa?"),
                ("Mina", "The impact is that some teams interpreted it as a hard deadline.", "Impact-nya: beberapa tim nangkepnya sebagai deadline fix."),
                ("Jordan", "That's not what I meant.", "Bukan itu maksudku."),
                ("Mina", "I appreciate the intent, and I think we can make it clearer with one sentence.", "Aku apresiasi niatnya, dan menurutku kita bisa bikin lebih jelas dengan satu kalimat."),
                ("Jordan", "What would you suggest?", "Kamu saranin apa?"),
                ("Mina", "Would you be open to adding an explicit 'earliest possible' line?", "Kamu open nggak kalau kita tambahin kalimat 'earliest possible' yang eksplisit?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "I wanted to flag one point about the messaging.",
                    "meaning_id": "Aku mau highlight satu poin soal messaging-nya.",
                    "usage_note": "A gentle opener for feedback.",
                    "common_mistake": "Do not start with blame; start with flagging a point.",
                },
                {
                    "phrase": "The impact is that some teams interpreted it as a hard deadline.",
                    "meaning_id": "Impact-nya: beberapa tim nangkepnya sebagai deadline fix.",
                    "usage_note": "Focus on impact, not intent.",
                    "common_mistake": "Do not accuse; describe impact objectively.",
                },
                {
                    "phrase": "I appreciate the intent, and I think we can make it clearer.",
                    "meaning_id": "Aku apresiasi niatnya, dan menurutku kita bisa bikin lebih jelas.",
                    "usage_note": "Acknowledge positives before a suggestion.",
                    "common_mistake": "Do not sound sarcastic; keep it sincere.",
                },
                {
                    "phrase": "Would you be open to adding an explicit line?",
                    "meaning_id": "Kamu open nggak kalau kita tambahin kalimat yang eksplisit?",
                    "usage_note": "Invite change collaboratively.",
                    "common_mistake": "Do not command; ask if they are open to it.",
                },
                {
                    "phrase": "We can make it clearer with one sentence.",
                    "meaning_id": "Kita bisa bikin lebih jelas dengan satu kalimat.",
                    "usage_note": "Make the fix feel small and doable.",
                    "common_mistake": "Do not propose a huge rewrite; keep it scoped.",
                },
            ],
            "grammar_md": [
                ("Feedback openers", ["I wanted to flag ...", "I wanted to raise one point ..."]),
                ("Impact + suggestion", ["The impact is ...", "Would you be open to ...?"]),
            ],
            "pronunciation": [
                ("messaging", "MES-ij-ing."),
                ("interpreted", "in-TER-prih-tid."),
                ("explicit", "ik-SPLIS-it."),
            ],
            "response_prompts": [
                {
                    "prompt": "Open feedback gently.",
                    "target_response": "I wanted to flag one point about the messaging.",
                    "acceptable_variations": [
                        "I wanted to flag one point about the messaging.",
                        "I wanted to raise one point about the wording.",
                    ],
                },
                {
                    "prompt": "Describe impact objectively.",
                    "target_response": "The impact is that some teams interpreted it as a hard deadline.",
                    "acceptable_variations": [
                        "The impact is that some teams interpreted it as a hard deadline.",
                        "The impact is that it sounded like a hard deadline to some teams.",
                    ],
                },
                {
                    "prompt": "Invite a change collaboratively.",
                    "target_response": "Would you be open to adding an explicit 'earliest possible' line?",
                    "acceptable_variations": [
                        "Would you be open to adding an explicit 'earliest possible' line?",
                        "Would you be open to adding a clarifying line about the timeline?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "flag_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase opens sensitive feedback gently?",
                    "options": ["I wanted to flag ...", "You did it wrong.", "No."],
                    "correct_answer": "I wanted to flag ...",
                },
                {
                    "key": "impact_focus",
                    "type": "multiple_choice",
                    "prompt": "Which sentence focuses on impact?",
                    "options": ["The impact is that ...", "You always ...", "You should know."],
                    "correct_answer": "The impact is that ...",
                },
                {
                    "key": "open_to",
                    "type": "multiple_choice",
                    "prompt": "Which phrase invites change politely?",
                    "options": ["Would you be open to ...?", "Do it now.", "Stop."],
                    "correct_answer": "Would you be open to ...?",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_sensitive_feedback",
                "opening_line": "How did the last review go?",
                "learner_goal": "Give sensitive feedback tactfully and propose a small, concrete improvement.",
                "turns": [
                    {
                        "coach": "How did the last review go?",
                        "hint": "Mulai dengan I wanted to flag...",
                        "sample_answer": "It went well overall. I wanted to flag one point about the messaging.",
                        "focus": "Opener",
                        "expected_keywords": ["flag", "messaging"],
                    },
                    {
                        "coach": "What was the issue?",
                        "hint": "Fokus ke impact.",
                        "sample_answer": "The impact is that some teams interpreted it as a hard deadline.",
                        "focus": "Impact",
                        "expected_keywords": ["impact", "interpreted", "deadline"],
                    },
                    {
                        "coach": "Suggest a fix politely.",
                        "hint": "Would you be open to...?",
                        "sample_answer": "Would you be open to adding an explicit 'earliest possible' line to clarify the timeline?",
                        "focus": "Suggestion",
                        "expected_keywords": ["open to", "explicit", "clarify"],
                    },
                ],
                "target_phrases": ["I wanted to flag ...", "The impact is that ...", "Would you be open to ...?"],
            },
            "reading_support": "Sensitive feedback lands better when you focus on impact rather than blame. Start gently, name the impact, acknowledge intent, and propose a small, concrete improvement.",
            "writing_support_lines": [
                "Write 9 lines:",
                "1. I wanted to flag ...",
                "2. Overall, ...",
                "3. The impact is that ...",
                "4. Some teams ...",
                "5. I appreciate ...",
                "6. That said, ...",
                "7. Would you be open to ...?",
                "8. This would make ... clearer.",
                "9. Thanks for considering it.",
            ],
            "goal_examples": ["I wanted to flag ...", "The impact is that ...", "Would you be open to ...?"],
        },
        {
            "lesson_key": "lesson-04-communicating-risk",
            "slug": "communicating-risk",
            "title": "Communicating Risk",
            "conversation_situation": "communicating_risk",
            "conversation_goal": "Communicate risk clearly by describing likelihood, impact, and mitigation options.",
            "grammar_summary": "Use The main risk is... / There's a reasonable chance... / The impact would be... / We can mitigate it by... to communicate risk.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu harus komunikasi risiko ke stakeholder. Kamu jelasin probabilitas, dampak, dan mitigasi dengan bahasa yang jelas.",
            "dialogue": [
                ("Jordan", "What risks should we highlight to leadership?"),
                ("Mina", "The main risk is a spike in incidents during rollout."),
                ("Jordan", "How likely is that?"),
                ("Mina", "There's a reasonable chance, given recent instability."),
                ("Jordan", "What's the impact?"),
                ("Mina", "The impact would be delayed revenue and higher support load."),
                ("Jordan", "How do we reduce it?"),
                ("Mina", "We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan."),
            ],
            "translations": [
                ("Jordan", "What risks should we highlight to leadership?", "Risiko apa yang harus kita highlight ke leadership?"),
                ("Mina", "The main risk is a spike in incidents during rollout.", "Risiko utamanya lonjakan incident saat rollout."),
                ("Jordan", "How likely is that?", "Seberapa mungkin itu terjadi?"),
                ("Mina", "There's a reasonable chance, given recent instability.", "Ada kemungkinan yang cukup besar, melihat instabilitas belakangan."),
                ("Jordan", "What's the impact?", "Dampaknya apa?"),
                ("Mina", "The impact would be delayed revenue and higher support load.", "Dampaknya revenue terlambat dan beban support naik."),
                ("Jordan", "How do we reduce it?", "Gimana cara nguranginnya?"),
                ("Mina", "We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan.", "Kita bisa mitigasi dengan time-box rollout, tambah monitoring, dan siapin rollback plan."),
            ],
            "useful_phrases": [
                {
                    "phrase": "The main risk is a spike in incidents during rollout.",
                    "meaning_id": "Risiko utamanya lonjakan incident saat rollout.",
                    "usage_note": "Name a main risk clearly.",
                    "common_mistake": "Do not list many risks immediately; start with the main one.",
                },
                {
                    "phrase": "There's a reasonable chance, given recent instability.",
                    "meaning_id": "Ada kemungkinan yang cukup besar, melihat instabilitas belakangan.",
                    "usage_note": "Likelihood with rationale.",
                    "common_mistake": "Do not say maybe; calibrate (reasonable chance).",
                },
                {
                    "phrase": "The impact would be delayed revenue and higher support load.",
                    "meaning_id": "Dampaknya revenue terlambat dan beban support naik.",
                    "usage_note": "Describe impact in concrete terms.",
                    "common_mistake": "Do not keep impact vague; name business impact.",
                },
                {
                    "phrase": "We can mitigate it by time-boxing the rollout.",
                    "meaning_id": "Kita mitigasi dengan time-box rollout.",
                    "usage_note": "Introduce mitigation with by + -ing.",
                    "common_mistake": "Do not say mitigate with do; use mitigate by doing.",
                },
                {
                    "phrase": "Let's include a rollback plan.",
                    "meaning_id": "Kita masukin rollback plan.",
                    "usage_note": "Operational mitigation.",
                    "common_mistake": "Do not discuss risk without a rollback option.",
                },
            ],
            "grammar_md": [
                ("Risk framing", ["The main risk is ...", "There's a reasonable chance ..."]),
                ("Impact + mitigation", ["The impact would be ...", "We can mitigate it by ..."]),
            ],
            "pronunciation": [
                ("likelihood", "LYKE-lee-hood."),
                ("mitigate", "MIT-i-gayt."),
                ("rollback", "ROHL-bak."),
            ],
            "response_prompts": [
                {
                    "prompt": "Name a main risk.",
                    "target_response": "The main risk is a spike in incidents during rollout.",
                    "acceptable_variations": [
                        "The main risk is a spike in incidents during rollout.",
                        "The main risk is instability during release.",
                    ],
                },
                {
                    "prompt": "Describe likelihood with rationale.",
                    "target_response": "There's a reasonable chance, given recent instability.",
                    "acceptable_variations": [
                        "There's a reasonable chance, given recent instability.",
                        "There's a reasonable chance, based on the data.",
                    ],
                },
                {
                    "prompt": "Propose mitigation.",
                    "target_response": "We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan.",
                    "acceptable_variations": [
                        "We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan.",
                        "We can mitigate it by rolling out gradually and preparing a rollback plan.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "main_risk",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a main risk?",
                    "options": ["The main risk is ...", "Main risky is ...", "No risk."],
                    "correct_answer": "The main risk is ...",
                },
                {
                    "key": "reasonable_chance",
                    "type": "multiple_choice",
                    "prompt": 'What does "a reasonable chance" mean?',
                    "options": ["kemungkinan yang cukup besar", "tidak mungkin", "pasti terjadi"],
                    "correct_answer": "kemungkinan yang cukup besar",
                },
                {
                    "key": "mitigate_by",
                    "type": "multiple_choice",
                    "prompt": "Which sentence uses mitigate by correctly?",
                    "options": ["We can mitigate it by adding monitoring.", "We mitigate with add monitoring.", "Mitigate is monitoring."],
                    "correct_answer": "We can mitigate it by adding monitoring.",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_communicating_risk",
                "opening_line": "What risks should we highlight to leadership?",
                "learner_goal": "Communicate risk with likelihood, impact, and mitigation.",
                "turns": [
                    {
                        "coach": "What risks should we highlight to leadership?",
                        "hint": "Start with The main risk is...",
                        "sample_answer": "The main risk is a spike in incidents during rollout.",
                        "focus": "Risk",
                        "expected_keywords": ["main risk", "incidents"],
                    },
                    {
                        "coach": "How likely is that?",
                        "hint": "There's a reasonable chance... given...",
                        "sample_answer": "There's a reasonable chance, given recent instability.",
                        "focus": "Likelihood",
                        "expected_keywords": ["reasonable chance", "given"],
                    },
                    {
                        "coach": "Close with mitigation steps.",
                        "hint": "We can mitigate it by... monitoring... rollback...",
                        "sample_answer": "We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan.",
                        "focus": "Mitigation",
                        "expected_keywords": ["mitigate", "monitoring", "rollback"],
                    },
                ],
                "target_phrases": ["The main risk is ...", "There's a reasonable chance ...", "We can mitigate it by ..."],
            },
            "reading_support": "Risk communication is clearer when it's structured: risk, likelihood, impact, and mitigation. Avoid vague language and propose concrete controls like monitoring and rollback plans.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. The main risk is ...",
                "2. There's a reasonable chance ...",
                "3. Given ...",
                "4. The impact would be ...",
                "5. If that happens, ...",
                "6. We can mitigate it by ...",
                "7. We'll add monitoring ...",
                "8. We'll time-box ...",
                "9. We'll prepare a rollback plan ...",
                "10. Next steps are ...",
            ],
            "goal_examples": ["The main risk is ...", "There's a reasonable chance ...", "We can mitigate it by ..."],
        },
        {
            "lesson_key": "lesson-05-strategic-workplace-mission",
            "slug": "strategic-workplace-mission",
            "title": "Strategic Workplace Mission",
            "conversation_situation": "mission_strategic_workplace",
            "conversation_goal": "Lead a strategic workplace conversation: align stakeholders, manage expectations, give sensitive feedback, and communicate risk.",
            "grammar_summary": "Combine alignment questions, realistic commitments, impact-based feedback, and risk framing into one coherent discussion.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Misi: kamu memimpin diskusi lintas tim. Kamu selaraskan stakeholder, set ekspektasi, kasih feedback sensitif, dan jelasin risk + mitigasi.",
            "dialogue": [
                ("Jordan", "We need to align on priorities and deliver next week."),
                ("Mina", "To make sure we're aligned, what's your top priority and biggest constraint?"),
                ("Jordan", "Speed, and we can't add headcount."),
                ("Mina", "Understood. What we can commit to is a smaller release by next week, assuming no new blockers."),
                ("Jordan", "Some teams think it's a hard deadline."),
                ("Mina", "I wanted to flag the impact: it was interpreted as a hard deadline. Would you be open to adding an explicit 'earliest possible' line?"),
                ("Jordan", "Yes. What risks should we mention?"),
                ("Mina", "The main risk is incidents during rollout. We can mitigate it by time-boxing, adding monitoring, and having a rollback plan."),
            ],
            "translations": [
                ("Jordan", "We need to align on priorities and deliver next week.", "Kita harus align prioritas dan deliver minggu depan."),
                ("Mina", "To make sure we're aligned, what's your top priority and biggest constraint?", "Biar aligned, apa prioritas utama kamu dan constraint terbesarnya?"),
                ("Jordan", "Speed, and we can't add headcount.", "Kecepatan, dan kita nggak bisa nambah orang."),
                ("Mina", "Understood. What we can commit to is a smaller release by next week, assuming no new blockers.", "Oke. Yang bisa kita commit adalah rilis kecil minggu depan, asumsi nggak ada blocker baru."),
                ("Jordan", "Some teams think it's a hard deadline.", "Beberapa tim nangkepnya sebagai deadline fix."),
                ("Mina", "I wanted to flag the impact: it was interpreted as a hard deadline. Would you be open to adding an explicit 'earliest possible' line?", "Aku mau highlight impact-nya: itu ditangkap sebagai deadline fix. Kamu open nggak kalau kita tambahin kalimat 'earliest possible' yang eksplisit?"),
                ("Jordan", "Yes. What risks should we mention?", "Oke. Risiko apa yang harus kita sebut?"),
                ("Mina", "The main risk is incidents during rollout. We can mitigate it by time-boxing, adding monitoring, and having a rollback plan.", "Risiko utamanya incident saat rollout. Kita mitigasi dengan time-box, tambah monitoring, dan siapin rollback plan."),
            ],
            "useful_phrases": [
                {
                    "phrase": "To make sure we're aligned, what's your top priority and biggest constraint?",
                    "meaning_id": "Biar aligned, apa prioritas utama kamu dan constraint terbesarnya?",
                    "usage_note": "Alignment question.",
                    "common_mistake": "Don't assume priorities or constraints.",
                },
                {
                    "phrase": "What we can commit to is a smaller release by next week, assuming no new blockers.",
                    "meaning_id": "Yang bisa kita commit adalah rilis kecil minggu depan, asumsi nggak ada blocker baru.",
                    "usage_note": "Expectation management.",
                    "common_mistake": "Don't commit without stating assumptions.",
                },
                {
                    "phrase": "I wanted to flag the impact: it was interpreted as a hard deadline.",
                    "meaning_id": "Aku mau highlight impact-nya: itu ditangkap sebagai deadline fix.",
                    "usage_note": "Sensitive feedback focused on impact.",
                    "common_mistake": "Don't blame; describe impact.",
                },
                {
                    "phrase": "The main risk is incidents during rollout. We can mitigate it by time-boxing and monitoring.",
                    "meaning_id": "Risiko utamanya incident saat rollout. Kita mitigasi dengan time-box dan monitoring.",
                    "usage_note": "Risk framing + mitigation.",
                    "common_mistake": "Don't discuss risk without mitigation.",
                },
                {
                    "phrase": "I'll capture the decision and circulate it today.",
                    "meaning_id": "Aku rangkum keputusannya dan share hari ini.",
                    "usage_note": "Close with a clear follow-up action.",
                    "common_mistake": 'Don\'t leave decisions undocumented.',
                },
            ],
            "grammar_md": [
                (
                    "Strategic workplace flow",
                    [
                        "To make sure we're aligned, ...",
                        "What we can commit to is ... assuming ...",
                        "The impact is that ... Would you be open to ...?",
                        "The main risk is ... We can mitigate it by ...",
                    ],
                )
            ],
            "pronunciation": [
                ("alignment", "uh-LYNT-ment."),
                ("expectations", "eks-pek-TAY-shunz."),
                ("mitigation", "mit-ih-GAY-shun."),
            ],
            "response_prompts": [
                {
                    "prompt": "Align priorities and constraints.",
                    "target_response": "To make sure we're aligned, what's your top priority and biggest constraint?",
                    "acceptable_variations": [
                        "To make sure we're aligned, what's your top priority and biggest constraint?",
                        "To make sure we're aligned, can you share your top priority and constraint?",
                    ],
                },
                {
                    "prompt": "Set expectations with assumptions.",
                    "target_response": "What we can commit to is a smaller release by next week, assuming no new blockers.",
                    "acceptable_variations": [
                        "What we can commit to is a smaller release by next week, assuming no new blockers.",
                        "What we can commit to is a pilot by next week, assuming no surprises.",
                    ],
                },
                {
                    "prompt": "State main risk and mitigation.",
                    "target_response": "The main risk is incidents during rollout. We can mitigate it by time-boxing, adding monitoring, and having a rollback plan.",
                    "acceptable_variations": [
                        "The main risk is incidents during rollout. We can mitigate it by time-boxing, adding monitoring, and having a rollback plan.",
                        "The main risk is instability. We can mitigate it by rolling out gradually and monitoring closely.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "strategic_flow",
                    "type": "multiple_choice",
                    "prompt": "Which flow fits a strategic workplace conversation?",
                    "options": [
                        "Align -> commit -> feedback -> risk",
                        "Greeting -> goodbye",
                        "Colors -> numbers",
                    ],
                    "correct_answer": "Align -> commit -> feedback -> risk",
                },
                {
                    "key": "open_to_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase invites a change politely?",
                    "options": ["Would you be open to ...?", "Do it.", "Stop."],
                    "correct_answer": "Would you be open to ...?",
                },
                {
                    "key": "mitigate_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces mitigation?",
                    "options": ["We can mitigate it by ...", "Mitigate with do.", "No risk."],
                    "correct_answer": "We can mitigate it by ...",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_strategic_workplace_mission",
                "opening_line": "We need to align priorities and deliver soon.",
                "learner_goal": "Lead a strategic workplace conversation end-to-end with alignment, expectations, feedback, and risk management.",
                "turns": [
                    {
                        "coach": "Start by aligning priorities and constraints.",
                        "hint": "To make sure we're aligned... top priority... biggest constraint...",
                        "sample_answer": "To make sure we're aligned, what's your top priority and biggest constraint?",
                        "focus": "Align",
                        "expected_keywords": ["aligned", "priority", "constraint"],
                    },
                    {
                        "coach": "Set realistic expectations and timeline with assumptions.",
                        "hint": "What we can commit to is... assuming...",
                        "sample_answer": "What we can commit to is a smaller release by next week, assuming no new blockers.",
                        "focus": "Expectations",
                        "expected_keywords": ["commit", "assuming"],
                    },
                    {
                        "coach": "Communicate the main risk and mitigation steps.",
                        "hint": "The main risk is... We can mitigate it by...",
                        "sample_answer": "The main risk is incidents during rollout. We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan.",
                        "focus": "Risk",
                        "expected_keywords": ["main risk", "mitigate", "rollback"],
                    },
                ],
                "target_phrases": ["To make sure we're aligned, ...", "What we can commit to is ...", "The main risk is ..."],
            },
            "reading_support": "Strategic communication means you manage the conversation: align stakeholders, set realistic commitments, give feedback focused on impact, and communicate risks with mitigation. Close by documenting decisions.",
            "writing_support_lines": [
                "Write your mission (12 lines):",
                "1. To make sure we're aligned, ...",
                "2. What's your top priority?",
                "3. What's the biggest constraint?",
                "4. What we can commit to is ...",
                "5. The earliest we can deliver is ...",
                "6. Assuming no new blockers, ...",
                "7. I wanted to flag ...",
                "8. The impact is that ...",
                "9. Would you be open to ...?",
                "10. The main risk is ...",
                "11. We can mitigate it by ...",
                "12. Next steps are ...",
            ],
            "goal_examples": ["To make sure we're aligned, ...", "What we can commit to is ...", "The main risk is ..."],
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

