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
            "- Tone: calm, encouraging, professional",
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

        Read it again and underline the coaching words (direction, ownership, trade-off, options, next step, accountability).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "C1"
    root = Path("content/curriculum/english/C1")
    units_root = root / "units"
    unit_key = "unit-06-leadership-and-coaching"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-06-leadership-and-coaching
            level_code: C1
            title: Leadership & Coaching
            main_conversation_outcome: Lead conversations, coach others, and guide decisions.
            status: in_production
            lessons:
              - lesson-01-setting-direction
              - lesson-02-coaching-with-questions
              - lesson-03-giving-actionable-feedback
              - lesson-04-guiding-a-decision
              - lesson-05-leadership-coaching-mission
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
            "lesson_key": "lesson-01-setting-direction",
            "slug": "setting-direction",
            "title": "Setting Direction",
            "conversation_situation": "setting_direction",
            "conversation_goal": "Set direction by clarifying priorities, success criteria, and ownership.",
            "grammar_summary": "Use The direction I'd like to set is... / Success looks like... / I'd like you to own... / Let's align on... to set direction.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu jadi lead. Kamu perlu set arah kerja: prioritas, definisi sukses, dan siapa yang owning apa.",
            "dialogue": [
                ("Jordan", "What should the team focus on this sprint?"),
                ("Mina", "The direction I'd like to set is stabilizing the billing flow first."),
                ("Jordan", "How do we define success?"),
                ("Mina", "Success looks like fewer incidents and faster completion rates."),
                ("Jordan", "Who owns what?"),
                ("Mina", "I'd like you to own the rollout plan, and I'll own stakeholder updates."),
                ("Jordan", "Any constraints?"),
                ("Mina", "Yes—let's align on scope and keep it time-boxed to two weeks."),
            ],
            "translations": [
                ("Jordan", "What should the team focus on this sprint?", "Tim harus fokus ke apa sprint ini?"),
                ("Mina", "The direction I'd like to set is stabilizing the billing flow first.", "Arah yang mau aku set: stabilisasi billing dulu."),
                ("Jordan", "How do we define success?", "Suksesnya kita definisikan gimana?"),
                ("Mina", "Success looks like fewer incidents and faster completion rates.", "Sukses artinya incident berkurang dan completion rate lebih cepat."),
                ("Jordan", "Who owns what?", "Siapa owning apa?"),
                ("Mina", "I'd like you to own the rollout plan, and I'll own stakeholder updates.", "Aku minta kamu own rollout plan, dan aku own update ke stakeholder."),
                ("Jordan", "Any constraints?", "Ada constraint?"),
                ("Mina", "Yes—let's align on scope and keep it time-boxed to two weeks.", "Ada—kita align scope dan time-box dua minggu."),
            ],
            "useful_phrases": [
                {
                    "phrase": "The direction I'd like to set is stabilizing the billing flow first.",
                    "meaning_id": "Arah yang mau aku set: stabilisasi billing dulu.",
                    "usage_note": "A direct leadership framing.",
                    "common_mistake": "Do not give many directions at once; pick one priority.",
                },
                {
                    "phrase": "Success looks like fewer incidents and faster completion rates.",
                    "meaning_id": "Sukses artinya incident berkurang dan completion rate lebih cepat.",
                    "usage_note": "Define success criteria.",
                    "common_mistake": "Do not keep success vague; name measurable outcomes.",
                },
                {
                    "phrase": "I'd like you to own the rollout plan.",
                    "meaning_id": "Aku minta kamu own rollout plan.",
                    "usage_note": "Assign ownership clearly.",
                    "common_mistake": "Do not assign ownership without clarity; say who owns what.",
                },
                {
                    "phrase": "Let's align on scope and keep it time-boxed to two weeks.",
                    "meaning_id": "Kita align scope dan time-box dua minggu.",
                    "usage_note": "Set boundaries and timeline.",
                    "common_mistake": "Do not let scope creep; time-box it.",
                },
                {
                    "phrase": "Does that direction make sense to you?",
                    "meaning_id": "Arah itu masuk akal buat kamu?",
                    "usage_note": "Check alignment after setting direction.",
                    "common_mistake": "Do not assume agreement; check it.",
                },
            ],
            "grammar_md": [
                ("Direction + ownership", ["The direction I'd like to set is ...", "I'd like you to own ..."]),
                ("Success criteria", ["Success looks like ...", "Let's align on scope ..."]),
            ],
            "pronunciation": [
                ("ownership", "OH-ner-ship."),
                ("criteria", "kry-TEER-ee-uh."),
                ("time-boxed", "TIME-bokst."),
            ],
            "response_prompts": [
                {
                    "prompt": "Set one clear direction.",
                    "target_response": "The direction I'd like to set is stabilizing the billing flow first.",
                    "acceptable_variations": [
                        "The direction I'd like to set is stabilizing the billing flow first.",
                        "The direction I'd like to set is reducing incidents first.",
                    ],
                },
                {
                    "prompt": "Define success criteria.",
                    "target_response": "Success looks like fewer incidents and faster completion rates.",
                    "acceptable_variations": [
                        "Success looks like fewer incidents and faster completion rates.",
                        "Success looks like fewer tickets and a stable rollout.",
                    ],
                },
                {
                    "prompt": "Assign ownership clearly.",
                    "target_response": "I'd like you to own the rollout plan, and I'll own stakeholder updates.",
                    "acceptable_variations": [
                        "I'd like you to own the rollout plan, and I'll own stakeholder updates.",
                        "I'd like you to own the plan, and I'll own the communication.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "direction_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase sets direction clearly?",
                    "options": ["The direction I'd like to set is ...", "Direction is good.", "No direction."],
                    "correct_answer": "The direction I'd like to set is ...",
                },
                {
                    "key": "own_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase assigns ownership?",
                    "options": ["I'd like you to own ...", "You do it.", "Whatever."],
                    "correct_answer": "I'd like you to own ...",
                },
                {
                    "key": "timeboxed_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "time-boxed" mean?',
                    "options": ["dibatasi waktu", "tanpa batas", "lebih mahal"],
                    "correct_answer": "dibatasi waktu",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_setting_direction",
                "opening_line": "What should the team focus on this sprint?",
                "learner_goal": "Set direction with priorities, success criteria, and ownership.",
                "turns": [
                    {
                        "coach": "What should the team focus on this sprint?",
                        "hint": "Set direction clearly.",
                        "sample_answer": "The direction I'd like to set is stabilizing the billing flow first.",
                        "focus": "Direction",
                        "expected_keywords": ["direction", "first"],
                    },
                    {
                        "coach": "How do we define success?",
                        "hint": "Success looks like...",
                        "sample_answer": "Success looks like fewer incidents and faster completion rates.",
                        "focus": "Success",
                        "expected_keywords": ["success", "incidents"],
                    },
                    {
                        "coach": "Assign ownership and boundaries.",
                        "hint": "I'd like you to own... Let's align on scope...",
                        "sample_answer": "I'd like you to own the rollout plan, and I'll own stakeholder updates. Let's align on scope and keep it time-boxed to two weeks.",
                        "focus": "Ownership + scope",
                        "expected_keywords": ["own", "scope", "time-boxed"],
                    },
                ],
                "target_phrases": ["The direction I'd like to set is ...", "Success looks like ...", "I'd like you to own ..."],
            },
            "reading_support": "Setting direction means you reduce ambiguity: state one priority, define success, assign ownership, and set scope boundaries. This helps teams move faster with confidence.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. The direction I'd like to set is ...",
                "2. The priority is ...",
                "3. Success looks like ...",
                "4. I'd like you to own ...",
                "5. I'll own ...",
                "6. Let's align on scope ...",
                "7. We'll keep it time-boxed to ...",
                "8. The main risk is ...",
                "9. Next steps are ...",
                "10. Does that make sense?",
            ],
            "goal_examples": ["The direction I'd like to set is ...", "Success looks like ...", "I'd like you to own ..."],
        },
        {
            "lesson_key": "lesson-02-coaching-with-questions",
            "slug": "coaching-with-questions",
            "title": "Coaching with Questions",
            "conversation_situation": "coaching_with_questions",
            "conversation_goal": "Coach others using questions that build ownership, clarify thinking, and unblock decisions.",
            "grammar_summary": "Use What options do you see? / What would success look like? / What's the smallest next step? / What support do you need? to coach.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu coaching teammate. Alih-alih kasih jawaban, kamu pakai pertanyaan yang membantu mereka berpikir dan ambil ownership.",
            "dialogue": [
                ("Jordan", "I'm stuck on how to handle the rollout."),
                ("Mina", "What options do you see right now?"),
                ("Jordan", "We can do a pilot or a full rollout."),
                ("Mina", "What would success look like for the pilot?"),
                ("Jordan", "Low incidents and clear data."),
                ("Mina", "What's the smallest next step you can take today?"),
                ("Jordan", "Draft the rollout checklist."),
                ("Mina", "Great. What support do you need from me?"),
            ],
            "translations": [
                ("Jordan", "I'm stuck on how to handle the rollout.", "Aku stuck gimana handle rollout."),
                ("Mina", "What options do you see right now?", "Opsi apa yang kamu lihat sekarang?"),
                ("Jordan", "We can do a pilot or a full rollout.", "Kita bisa pilot atau rollout penuh."),
                ("Mina", "What would success look like for the pilot?", "Suksesnya pilot seperti apa?"),
                ("Jordan", "Low incidents and clear data.", "Incident rendah dan data jelas."),
                ("Mina", "What's the smallest next step you can take today?", "Langkah kecil paling next yang bisa kamu lakukan hari ini apa?"),
                ("Jordan", "Draft the rollout checklist.", "Draft checklist rollout."),
                ("Mina", "Great. What support do you need from me?", "Oke. Support apa yang kamu butuh dari aku?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "What options do you see right now?",
                    "meaning_id": "Opsi apa yang kamu lihat sekarang?",
                    "usage_note": "Open up solution space without prescribing.",
                    "common_mistake": "Do not give the answer first; ask options.",
                },
                {
                    "phrase": "What would success look like for the pilot?",
                    "meaning_id": "Suksesnya pilot seperti apa?",
                    "usage_note": "Define success criteria collaboratively.",
                    "common_mistake": "Do not assume success criteria; ask.",
                },
                {
                    "phrase": "What's the smallest next step you can take today?",
                    "meaning_id": "Langkah kecil paling next yang bisa kamu lakukan hari ini apa?",
                    "usage_note": "Unblock with a concrete step.",
                    "common_mistake": "Do not ask for a huge plan; ask smallest next step.",
                },
                {
                    "phrase": "What support do you need from me?",
                    "meaning_id": "Support apa yang kamu butuh dari aku?",
                    "usage_note": "Offer support while keeping ownership with them.",
                    "common_mistake": "Do not take over; offer support.",
                },
                {
                    "phrase": "Walk me through your thinking.",
                    "meaning_id": "Coba jelasin cara pikir kamu.",
                    "usage_note": "Invite reasoning.",
                    "common_mistake": "Do not interrogate; keep tone curious.",
                },
            ],
            "grammar_md": [
                ("Coaching questions", ["What options do you see?", "What's the smallest next step?"]),
                ("Support + ownership", ["What support do you need?", "Walk me through your thinking."]),
            ],
            "pronunciation": [
                ("ownership", "OH-ner-ship."),
                ("unblock", "un-BLOK."),
                ("checklist", "CHEK-list."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask for options instead of giving answers.",
                    "target_response": "What options do you see right now?",
                    "acceptable_variations": ["What options do you see right now?", "What options do we have?"],
                },
                {
                    "prompt": "Ask for the smallest next step.",
                    "target_response": "What's the smallest next step you can take today?",
                    "acceptable_variations": [
                        "What's the smallest next step you can take today?",
                        "What's one small step you can do today?",
                    ],
                },
                {
                    "prompt": "Offer support without taking over.",
                    "target_response": "What support do you need from me?",
                    "acceptable_variations": ["What support do you need from me?", "How can I support you?"],
                },
            ],
            "quiz": [
                {
                    "key": "options_question",
                    "type": "multiple_choice",
                    "prompt": "Which question opens up options?",
                    "options": ["What options do you see?", "Do this now.", "No options."],
                    "correct_answer": "What options do you see?",
                },
                {
                    "key": "smallest_step",
                    "type": "multiple_choice",
                    "prompt": "Which question helps unblock someone with a concrete step?",
                    "options": ["What's the smallest next step?", "Think harder.", "Stop."],
                    "correct_answer": "What's the smallest next step?",
                },
                {
                    "key": "support_question",
                    "type": "multiple_choice",
                    "prompt": "Which question offers support while keeping ownership?",
                    "options": ["What support do you need from me?", "I'll do it.", "No support."],
                    "correct_answer": "What support do you need from me?",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_coaching_questions",
                "opening_line": "I'm stuck on how to handle this.",
                "learner_goal": "Coach with questions that build ownership and unblock progress.",
                "turns": [
                    {
                        "coach": "I'm stuck on how to handle this.",
                        "hint": "Start with options.",
                        "sample_answer": "Got it. What options do you see right now?",
                        "focus": "Options",
                        "expected_keywords": ["options"],
                    },
                    {
                        "coach": "Now help define success.",
                        "hint": "What would success look like...?",
                        "sample_answer": "What would success look like for the pilot?",
                        "focus": "Success",
                        "expected_keywords": ["success look like"],
                    },
                    {
                        "coach": "Unblock with a small next step and offer support.",
                        "hint": "Smallest next step... support...",
                        "sample_answer": "What's the smallest next step you can take today? And what support do you need from me?",
                        "focus": "Next step + support",
                        "expected_keywords": ["smallest", "next step", "support"],
                    },
                ],
                "target_phrases": ["What options do you see ...?", "What's the smallest next step ...?", "What support do you need ...?"],
            },
            "reading_support": "Coaching is often about asking better questions. Start with options, define success, identify the smallest next step, and ask what support is needed—so the other person keeps ownership.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. What options do you see?",
                "2. Walk me through your thinking.",
                "3. What would success look like?",
                "4. What's the smallest next step?",
                "5. What could you do today?",
                "6. What might you be missing?",
                "7. What's the trade-off?",
                "8. What support do you need?",
                "9. When can you share a draft?",
                "10. Great—let's check in tomorrow.",
            ],
            "goal_examples": ["What options do you see?", "What's the smallest next step?", "What support do you need?"],
        },
        {
            "lesson_key": "lesson-03-giving-actionable-feedback",
            "slug": "giving-actionable-feedback",
            "title": "Giving Actionable Feedback",
            "conversation_situation": "actionable_feedback",
            "conversation_goal": "Give actionable feedback by describing impact, being specific, and proposing a clear improvement.",
            "grammar_summary": "Use One thing I'd suggest is... / The impact is... / A concrete improvement would be... / Would you be open to... to give feedback.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu kasih feedback yang actionable: spesifik, fokus ke impact, dan ada improvement yang jelas.",
            "dialogue": [
                ("Jordan", "How was my update message?"),
                ("Mina", "Overall it's solid. One thing I'd suggest is leading with the decision."),
                ("Jordan", "Why?"),
                ("Mina", "The impact is that stakeholders scan quickly and might miss the point."),
                ("Jordan", "So what should I change?"),
                ("Mina", "A concrete improvement would be a one-line summary at the top."),
                ("Jordan", "Okay."),
                ("Mina", "Would you be open to revising it and sending a second draft?"),
            ],
            "translations": [
                ("Jordan", "How was my update message?", "Gimana pesan update aku?"),
                ("Mina", "Overall it's solid. One thing I'd suggest is leading with the decision.", "Secara overall bagus. Satu yang aku sarankan: mulai dengan keputusan."),
                ("Jordan", "Why?", "Kenapa?"),
                ("Mina", "The impact is that stakeholders scan quickly and might miss the point.", "Impact-nya: stakeholder baca cepat dan bisa miss poin utamanya."),
                ("Jordan", "So what should I change?", "Jadi apa yang harus aku ubah?"),
                ("Mina", "A concrete improvement would be a one-line summary at the top.", "Improvement konkretnya: tambahin ringkasan satu baris di atas."),
                ("Jordan", "Okay.", "Oke."),
                ("Mina", "Would you be open to revising it and sending a second draft?", "Kamu open nggak untuk revisi dan kirim draft kedua?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "One thing I'd suggest is leading with the decision.",
                    "meaning_id": "Satu yang aku sarankan: mulai dengan keputusan.",
                    "usage_note": "A clear, non-judgmental suggestion.",
                    "common_mistake": "Do not list many critiques; start with one thing.",
                },
                {
                    "phrase": "The impact is that stakeholders scan quickly and might miss the point.",
                    "meaning_id": "Impact-nya: stakeholder baca cepat dan bisa miss poin utamanya.",
                    "usage_note": "Explain impact, not personal fault.",
                    "common_mistake": "Do not say you wrote badly; explain impact.",
                },
                {
                    "phrase": "A concrete improvement would be a one-line summary at the top.",
                    "meaning_id": "Improvement konkretnya: ringkasan satu baris di atas.",
                    "usage_note": "Specific, actionable change.",
                    "common_mistake": "Do not stay vague; propose a concrete improvement.",
                },
                {
                    "phrase": "Would you be open to revising it and sending a second draft?",
                    "meaning_id": "Kamu open nggak untuk revisi dan kirim draft kedua?",
                    "usage_note": "Invite revision collaboratively.",
                    "common_mistake": "Do not command; ask if they're open.",
                },
                {
                    "phrase": "Overall it's solid.",
                    "meaning_id": "Secara overall bagus.",
                    "usage_note": "Positive framing before feedback.",
                    "common_mistake": "Do not skip positives; start with overall.",
                },
            ],
            "grammar_md": [
                ("Feedback framing", ["Overall it's ...", "One thing I'd suggest is ..."]),
                ("Impact + improvement", ["The impact is that ...", "A concrete improvement would be ..."]),
            ],
            "pronunciation": [
                ("actionable", "AK-shuh-nuh-buhl."),
                ("stakeholders", "STAYK-hohl-derz."),
                ("revise", "ri-VIZE."),
            ],
            "response_prompts": [
                {
                    "prompt": "Give one specific suggestion.",
                    "target_response": "One thing I'd suggest is leading with the decision.",
                    "acceptable_variations": [
                        "One thing I'd suggest is leading with the decision.",
                        "One thing I'd suggest is adding a one-line summary first.",
                    ],
                },
                {
                    "prompt": "Explain impact.",
                    "target_response": "The impact is that stakeholders scan quickly and might miss the point.",
                    "acceptable_variations": [
                        "The impact is that stakeholders scan quickly and might miss the point.",
                        "The impact is that people might miss the key message.",
                    ],
                },
                {
                    "prompt": "Propose a concrete improvement.",
                    "target_response": "A concrete improvement would be a one-line summary at the top.",
                    "acceptable_variations": [
                        "A concrete improvement would be a one-line summary at the top.",
                        "A concrete improvement would be a clear decision line first.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "one_thing",
                    "type": "multiple_choice",
                    "prompt": "Which phrase gives feedback gently?",
                    "options": ["One thing I'd suggest is ...", "This is terrible.", "No feedback."],
                    "correct_answer": "One thing I'd suggest is ...",
                },
                {
                    "key": "concrete_improvement",
                    "type": "multiple_choice",
                    "prompt": "Which phrase proposes an actionable fix?",
                    "options": ["A concrete improvement would be ...", "Just be better.", "No idea."],
                    "correct_answer": "A concrete improvement would be ...",
                },
                {
                    "key": "open_to",
                    "type": "multiple_choice",
                    "prompt": "Which phrase invites revision politely?",
                    "options": ["Would you be open to ...?", "Do it now.", "Stop."],
                    "correct_answer": "Would you be open to ...?",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_actionable_feedback",
                "opening_line": "Can you give feedback on my message?",
                "learner_goal": "Give actionable feedback: one suggestion, impact, and concrete improvement.",
                "turns": [
                    {
                        "coach": "Give one suggestion, starting with a positive frame.",
                        "hint": "Overall it's... One thing I'd suggest is...",
                        "sample_answer": "Overall it's solid. One thing I'd suggest is leading with the decision.",
                        "focus": "Suggestion",
                        "expected_keywords": ["overall", "one thing"],
                    },
                    {
                        "coach": "Explain the impact.",
                        "hint": "The impact is that...",
                        "sample_answer": "The impact is that stakeholders scan quickly and might miss the point.",
                        "focus": "Impact",
                        "expected_keywords": ["impact", "might miss"],
                    },
                    {
                        "coach": "Propose a concrete improvement and invite revision.",
                        "hint": "A concrete improvement would be... Would you be open to...?",
                        "sample_answer": "A concrete improvement would be a one-line summary at the top. Would you be open to revising it and sending a second draft?",
                        "focus": "Improve + invite",
                        "expected_keywords": ["concrete", "open to"],
                    },
                ],
                "target_phrases": ["One thing I'd suggest is ...", "The impact is that ...", "A concrete improvement would be ..."],
            },
            "reading_support": "Actionable feedback is specific and useful. Start with an overall positive frame, give one suggestion, describe the impact, propose a concrete improvement, and invite a revision collaboratively.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. Overall it's ...",
                "2. One thing I'd suggest is ...",
                "3. The impact is that ...",
                "4. People might ...",
                "5. A concrete improvement would be ...",
                "6. For example, ...",
                "7. Would you be open to ...?",
                "8. If you revise it, ...",
                "9. Then we can ...",
                "10. Thanks for the effort.",
            ],
            "goal_examples": ["One thing I'd suggest is ...", "The impact is that ...", "A concrete improvement would be ..."],
        },
        {
            "lesson_key": "lesson-04-guiding-a-decision",
            "slug": "guiding-a-decision",
            "title": "Guiding a Decision",
            "conversation_situation": "guiding_decision",
            "conversation_goal": "Guide a decision by structuring options, trade-offs, and a clear recommendation.",
            "grammar_summary": "Use We have three options... / The trade-off is... / Given our constraints... / I'd recommend... / Can we agree on... to guide decisions.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Tim buntu. Kamu bantu bikin keputusan dengan struktur: opsi, trade-off, constraint, rekomendasi, lalu alignment.",
            "dialogue": [
                ("Jordan", "We can't decide which approach to take."),
                ("Mina", "We have three options: pilot, phased rollout, or full rollout."),
                ("Jordan", "What's the trade-off?"),
                ("Mina", "The trade-off is speed versus risk and operational load."),
                ("Jordan", "Given our constraints, what do you recommend?"),
                ("Mina", "Given our constraints, I'd recommend a phased rollout with clear monitoring."),
                ("Jordan", "Okay. Can we align on next steps?"),
                ("Mina", "Yes—can we agree on the scope today and review metrics weekly?"),
            ],
            "translations": [
                ("Jordan", "We can't decide which approach to take.", "Kita nggak bisa putuskan approach mana."),
                ("Mina", "We have three options: pilot, phased rollout, or full rollout.", "Kita punya tiga opsi: pilot, rollout bertahap, atau rollout penuh."),
                ("Jordan", "What's the trade-off?", "Trade-off-nya apa?"),
                ("Mina", "The trade-off is speed versus risk and operational load.", "Trade-off-nya speed versus risiko dan beban operasional."),
                ("Jordan", "Given our constraints, what do you recommend?", "Dengan constraint kita, kamu rekomend apa?"),
                ("Mina", "Given our constraints, I'd recommend a phased rollout with clear monitoring.", "Dengan constraint kita, aku rekomend rollout bertahap dengan monitoring yang jelas."),
                ("Jordan", "Okay. Can we align on next steps?", "Oke. Bisa align next steps?"),
                ("Mina", "Yes—can we agree on the scope today and review metrics weekly?", "Bisa—kita sepakat scope hari ini dan review metrik tiap minggu?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "We have three options: pilot, phased rollout, or full rollout.",
                    "meaning_id": "Kita punya tiga opsi: pilot, rollout bertahap, atau rollout penuh.",
                    "usage_note": "Structure options clearly.",
                    "common_mistake": "Do not list too many options; keep it to 2-3.",
                },
                {
                    "phrase": "The trade-off is speed versus risk and operational load.",
                    "meaning_id": "Trade-off-nya speed versus risiko dan beban operasional.",
                    "usage_note": "State trade-offs concisely.",
                    "common_mistake": "Do not be vague; name risk and load.",
                },
                {
                    "phrase": "Given our constraints, I'd recommend a phased rollout with clear monitoring.",
                    "meaning_id": "Dengan constraint kita, aku rekomend rollout bertahap dengan monitoring yang jelas.",
                    "usage_note": "Recommendation tied to constraints.",
                    "common_mistake": "Do not recommend without referencing constraints.",
                },
                {
                    "phrase": "Can we agree on the scope today and review metrics weekly?",
                    "meaning_id": "Kita sepakat scope hari ini dan review metrik tiap minggu?",
                    "usage_note": "Confirm alignment and cadence.",
                    "common_mistake": "Do not end without agreement; confirm next steps.",
                },
                {
                    "phrase": "Let's align on the decision criteria.",
                    "meaning_id": "Kita align kriteria keputusan.",
                    "usage_note": "A useful meta move to unblock decisions.",
                    "common_mistake": "Do not argue details before aligning criteria.",
                },
            ],
            "grammar_md": [
                ("Decision structure", ["We have three options: ...", "The trade-off is ..."]),
                ("Recommendation + agreement", ["Given our constraints, I'd recommend ...", "Can we agree on ...?"]),
            ],
            "pronunciation": [
                ("cadence", "KAY-dens."),
                ("operational", "op-uh-RAY-shuh-nl."),
                ("metrics", "MET-riks."),
            ],
            "response_prompts": [
                {
                    "prompt": "List options clearly.",
                    "target_response": "We have three options: pilot, phased rollout, or full rollout.",
                    "acceptable_variations": [
                        "We have three options: pilot, phased rollout, or full rollout.",
                        "We have two options: a pilot or a phased rollout.",
                    ],
                },
                {
                    "prompt": "Recommend based on constraints.",
                    "target_response": "Given our constraints, I'd recommend a phased rollout with clear monitoring.",
                    "acceptable_variations": [
                        "Given our constraints, I'd recommend a phased rollout with clear monitoring.",
                        "Given our constraints, I'd recommend starting with a pilot.",
                    ],
                },
                {
                    "prompt": "Confirm agreement on next steps.",
                    "target_response": "Can we agree on the scope today and review metrics weekly?",
                    "acceptable_variations": [
                        "Can we agree on the scope today and review metrics weekly?",
                        "Can we agree on scope today and check in weekly?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "three_options",
                    "type": "multiple_choice",
                    "prompt": "Which phrase structures options clearly?",
                    "options": ["We have three options: ...", "Options are many.", "No options."],
                    "correct_answer": "We have three options: ...",
                },
                {
                    "key": "tradeoff",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces trade-offs?",
                    "options": ["The trade-off is ...", "Trade is off.", "No trade-offs."],
                    "correct_answer": "The trade-off is ...",
                },
                {
                    "key": "agree_scope",
                    "type": "multiple_choice",
                    "prompt": "Which phrase confirms agreement on next steps?",
                    "options": ["Can we agree on ...?", "You must agree.", "Stop."],
                    "correct_answer": "Can we agree on ...?",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_guiding_decision",
                "opening_line": "We can't decide which approach to take.",
                "learner_goal": "Guide a decision with options, trade-offs, recommendation, and agreement.",
                "turns": [
                    {
                        "coach": "Structure the options.",
                        "hint": "We have three options...",
                        "sample_answer": "We have three options: pilot, phased rollout, or full rollout.",
                        "focus": "Options",
                        "expected_keywords": ["options"],
                    },
                    {
                        "coach": "Explain the trade-off and recommend an option.",
                        "hint": "The trade-off is... Given our constraints, I'd recommend...",
                        "sample_answer": "The trade-off is speed versus risk and operational load. Given our constraints, I'd recommend a phased rollout with clear monitoring.",
                        "focus": "Trade-off + recommend",
                        "expected_keywords": ["trade-off", "constraints", "recommend"],
                    },
                    {
                        "coach": "Confirm agreement on next steps.",
                        "hint": "Can we agree on... review weekly...",
                        "sample_answer": "Can we agree on the scope today and review metrics weekly?",
                        "focus": "Agreement",
                        "expected_keywords": ["agree", "scope", "weekly"],
                    },
                ],
                "target_phrases": ["We have three options: ...", "Given our constraints, I'd recommend ...", "Can we agree on ...?"],
            },
            "reading_support": "Guiding decisions is about structure. List a small set of options, name the main trade-off, recommend one option based on constraints, then confirm agreement on scope and cadence.",
            "writing_support_lines": [
                "Write 10 lines:",
                "1. We have three options: ...",
                "2. Option A ...",
                "3. Option B ...",
                "4. Option C ...",
                "5. The trade-off is ...",
                "6. Given our constraints, I'd recommend ...",
                "7. The main risk is ...",
                "8. We can mitigate it by ...",
                "9. Can we agree on ...?",
                "10. Next steps are ...",
            ],
            "goal_examples": ["We have three options: ...", "The trade-off is ...", "Given our constraints, I'd recommend ..."],
        },
        {
            "lesson_key": "lesson-05-leadership-coaching-mission",
            "slug": "leadership-coaching-mission",
            "title": "Leadership Coaching Mission",
            "conversation_situation": "mission_leadership_coaching",
            "conversation_goal": "Lead a coaching conversation: set direction, ask coaching questions, give actionable feedback, and guide a decision.",
            "grammar_summary": "Combine direction setting, coaching questions, feedback framing, and decision structure into one mission conversation.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Misi: kamu memimpin percakapan coaching yang utuh, dari set direction sampai membuat keputusan dan next steps.",
            "dialogue": [
                ("Jordan", "I'm stuck and we need to decide fast."),
                ("Mina", "The direction I'd like to set is stabilizing billing first. What options do you see?"),
                ("Jordan", "Pilot or phased rollout."),
                ("Mina", "Great. What would success look like? And what's the smallest next step today?"),
                ("Jordan", "Draft the checklist and metrics."),
                ("Mina", "Overall your update is solid. One thing I'd suggest is leading with the decision—the impact is people might miss it."),
                ("Jordan", "Got it. What do you recommend?"),
                ("Mina", "Given our constraints, I'd recommend a phased rollout. Can we agree on scope today and review metrics weekly?"),
            ],
            "translations": [
                ("Jordan", "I'm stuck and we need to decide fast.", "Aku stuck dan kita harus putuskan cepat."),
                ("Mina", "The direction I'd like to set is stabilizing billing first. What options do you see?", "Arah yang mau aku set: stabilisasi billing dulu. Opsi apa yang kamu lihat?"),
                ("Jordan", "Pilot or phased rollout.", "Pilot atau rollout bertahap."),
                ("Mina", "Great. What would success look like? And what's the smallest next step today?", "Oke. Suksesnya seperti apa? Dan langkah kecil paling next hari ini apa?"),
                ("Jordan", "Draft the checklist and metrics.", "Draft checklist dan metrik."),
                ("Mina", "Overall your update is solid. One thing I'd suggest is leading with the decision—the impact is people might miss it.", "Update kamu overall bagus. Satu yang aku sarankan: mulai dengan keputusan—impact-nya orang bisa miss."),
                ("Jordan", "Got it. What do you recommend?", "Oke. Kamu rekomend apa?"),
                ("Mina", "Given our constraints, I'd recommend a phased rollout. Can we agree on scope today and review metrics weekly?", "Dengan constraint kita, aku rekomend rollout bertahap. Kita sepakat scope hari ini dan review metrik tiap minggu?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "The direction I'd like to set is ...",
                    "meaning_id": "Arah yang mau aku set adalah ...",
                    "usage_note": "Set direction.",
                    "common_mistake": "Don't set multiple priorities at once.",
                },
                {
                    "phrase": "What options do you see right now?",
                    "meaning_id": "Opsi apa yang kamu lihat sekarang?",
                    "usage_note": "Coach with questions.",
                    "common_mistake": "Don't take over; ask options.",
                },
                {
                    "phrase": "One thing I'd suggest is leading with the decision.",
                    "meaning_id": "Satu yang aku sarankan: mulai dengan keputusan.",
                    "usage_note": "Actionable feedback.",
                    "common_mistake": "Don't list many items; start with one.",
                },
                {
                    "phrase": "Given our constraints, I'd recommend a phased rollout.",
                    "meaning_id": "Dengan constraint kita, aku rekomend rollout bertahap.",
                    "usage_note": "Recommendation tied to constraints.",
                    "common_mistake": "Don't recommend without constraints.",
                },
                {
                    "phrase": "Can we agree on scope today and review metrics weekly?",
                    "meaning_id": "Kita sepakat scope hari ini dan review metrik tiap minggu?",
                    "usage_note": "Confirm agreement + cadence.",
                    "common_mistake": "Don't end without agreement.",
                },
            ],
            "grammar_md": [
                (
                    "Leadership & coaching toolkit",
                    [
                        "The direction I'd like to set is ... Success looks like ...",
                        "What options do you see? What's the smallest next step?",
                        "One thing I'd suggest is ... The impact is ... A concrete improvement would be ...",
                        "We have three options ... The trade-off is ... Given our constraints, I'd recommend ...",
                        "Can we agree on ...?",
                    ],
                )
            ],
            "pronunciation": [
                ("accountability", "uh-kown-tuh-BIL-ih-tee."),
                ("constraints", "kun-STRAYNTS."),
                ("recommend", "rek-uh-MEND."),
            ],
            "response_prompts": [
                {
                    "prompt": "Set direction and ask for options.",
                    "target_response": "The direction I'd like to set is stabilizing billing first. What options do you see right now?",
                    "acceptable_variations": [
                        "The direction I'd like to set is stabilizing billing first. What options do you see right now?",
                        "The direction I'd like to set is reducing incidents first. What options do you see?",
                    ],
                },
                {
                    "prompt": "Give feedback with impact and improvement.",
                    "target_response": "One thing I'd suggest is leading with the decision. The impact is that people might miss the point. A concrete improvement would be a one-line summary at the top.",
                    "acceptable_variations": [
                        "One thing I'd suggest is leading with the decision. The impact is that people might miss the point. A concrete improvement would be a one-line summary at the top.",
                        "One thing I'd suggest is adding a summary first. The impact is clarity. A concrete improvement would be a decision line at the top.",
                    ],
                },
                {
                    "prompt": "Recommend and confirm agreement.",
                    "target_response": "Given our constraints, I'd recommend a phased rollout. Can we agree on scope today and review metrics weekly?",
                    "acceptable_variations": [
                        "Given our constraints, I'd recommend a phased rollout. Can we agree on scope today and review metrics weekly?",
                        "Given our constraints, I'd recommend a pilot. Can we agree on scope and check in weekly?",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "coaching_flow",
                    "type": "multiple_choice",
                    "prompt": "Which flow fits leadership coaching?",
                    "options": ["Direction -> questions -> feedback -> decision", "Greeting -> goodbye", "Colors -> numbers"],
                    "correct_answer": "Direction -> questions -> feedback -> decision",
                },
                {
                    "key": "ownership_question",
                    "type": "multiple_choice",
                    "prompt": "Which question builds ownership?",
                    "options": ["What options do you see?", "I'll decide.", "No options."],
                    "correct_answer": "What options do you see?",
                },
                {
                    "key": "decision_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase confirms agreement?",
                    "options": ["Can we agree on ...?", "You must agree.", "Stop."],
                    "correct_answer": "Can we agree on ...?",
                },
            ],
            "roleplay": {
                "scenario_key": "c1_leadership_coaching_mission",
                "opening_line": "I'm stuck and we need to decide fast.",
                "learner_goal": "Lead a coaching conversation from direction to decision with clear next steps.",
                "turns": [
                    {
                        "coach": "Set direction and ask for options.",
                        "hint": "The direction I'd like to set is... What options do you see?",
                        "sample_answer": "The direction I'd like to set is stabilizing billing first. What options do you see right now?",
                        "focus": "Direction + options",
                        "expected_keywords": ["direction", "options"],
                    },
                    {
                        "coach": "Coach them toward a small next step and success criteria.",
                        "hint": "What would success look like? smallest next step?",
                        "sample_answer": "What would success look like for the pilot, and what's the smallest next step you can take today?",
                        "focus": "Coach",
                        "expected_keywords": ["success", "smallest next step"],
                    },
                    {
                        "coach": "Recommend an option and confirm agreement.",
                        "hint": "Given our constraints... Can we agree on...?",
                        "sample_answer": "Given our constraints, I'd recommend a phased rollout. Can we agree on scope today and review metrics weekly?",
                        "focus": "Decision",
                        "expected_keywords": ["constraints", "recommend", "agree"],
                    },
                ],
                "target_phrases": ["The direction I'd like to set is ...", "What options do you see ...?", "Can we agree on ...?"],
            },
            "reading_support": "Leadership coaching combines clarity and empathy. Set a direction, coach with questions that build ownership, give actionable feedback, then guide the decision with options and trade-offs.",
            "writing_support_lines": [
                "Write your mission (12 lines):",
                "1. The direction I'd like to set is ...",
                "2. Success looks like ...",
                "3. What options do you see?",
                "4. What would success look like?",
                "5. What's the smallest next step?",
                "6. What support do you need?",
                "7. One thing I'd suggest is ...",
                "8. The impact is ...",
                "9. A concrete improvement would be ...",
                "10. Given our constraints, I'd recommend ...",
                "11. Can we agree on ...?",
                "12. Next steps are ...",
            ],
            "goal_examples": ["The direction I'd like to set is ...", "What options do you see?", "Given our constraints, I'd recommend ..."],
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

