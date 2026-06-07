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
            "- Tone: friendly, clear, helpful",
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

        Read it again and underline the problem, solution, and decision words.
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B1"
    b1_root = Path("content/curriculum/english/B1")
    units_root = b1_root / "units"
    unit_key = "unit-03-problems-and-solutions"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-03-problems-and-solutions
            level_code: B1
            title: Problems & Solutions
            main_conversation_outcome: Explain a problem, suggest a solution, and respond to advice.
            status: in_production
            lessons:
              - lesson-01-describing-a-problem
              - lesson-02-suggesting-a-solution
              - lesson-03-responding-to-advice
              - lesson-04-making-a-simple-decision
              - lesson-05-problem-solving-mission
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
            "lesson_key": "lesson-01-describing-a-problem",
            "slug": "describing-a-problem",
            "title": "Describing a Problem",
            "conversation_situation": "describing_a_problem_at_work",
            "conversation_goal": "Describe a problem clearly and explain what happened and why it matters.",
            "grammar_summary": "Use There's a problem with... / It happened when... / Because... to explain a problem clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu ngobrol sama manager. Kamu jelaskan masalah yang terjadi dan dampaknya.",
            "dialogue": [
                ("Alex", "Hey Mina. You look concerned. What's going on?"),
                ("Mina", "There's a problem with the login page."),
                ("Alex", "What happened?"),
                ("Mina", "It started this morning when we deployed the update."),
                ("Alex", "How bad is it?"),
                ("Mina", "Users can't sign in, so they can't access their lessons."),
                ("Alex", "Okay. Let's fix it quickly."),
            ],
            "translations": [
                ("Alex", "Hey Mina. You look concerned. What's going on?", "Hai Mina. Kamu kelihatan khawatir. Ada apa?"),
                ("Mina", "There's a problem with the login page.", "Ada masalah di halaman login."),
                ("Alex", "What happened?", "Apa yang terjadi?"),
                ("Mina", "It started this morning when we deployed the update.", "Mulainya pagi ini waktu kita deploy update."),
                ("Alex", "How bad is it?", "Seberapa parah?"),
                ("Mina", "Users can't sign in, so they can't access their lessons.", "User nggak bisa login, jadi mereka nggak bisa akses lesson."),
                ("Alex", "Okay. Let's fix it quickly.", "Oke. Kita beresin cepat ya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "There's a problem with the login page.",
                    "meaning_id": "Ada masalah di halaman login.",
                    "usage_note": "A clear way to start describing a problem.",
                    "common_mistake": 'Do not say "Have problem"; use There\'s a problem with...',
                },
                {
                    "phrase": "It started this morning.",
                    "meaning_id": "Mulainya pagi ini.",
                    "usage_note": "Say when the problem started.",
                    "common_mistake": 'Do not say "It start" in past; use started.',
                },
                {
                    "phrase": "It happened when we deployed the update.",
                    "meaning_id": "Terjadi waktu kita deploy update.",
                    "usage_note": "Explain the trigger clearly.",
                    "common_mistake": 'Do not say "happened in deployed"; use when we deployed.',
                },
                {
                    "phrase": "Users can't sign in.",
                    "meaning_id": "User nggak bisa login.",
                    "usage_note": "State the impact in a simple sentence.",
                    "common_mistake": 'Do not say "Users can\'t to sign in".',
                },
                {
                    "phrase": "So they can't access their lessons.",
                    "meaning_id": "Jadi mereka nggak bisa akses lesson.",
                    "usage_note": "Use so to show impact/result.",
                    "common_mistake": 'Do not use because if you mean result; use so.',
                },
            ],
            "grammar_md": [
                ("There's a problem with...", ["There's a problem with the login page.", "There's a problem with the payment flow."]),
                ("Cause and result (because / so)", ["It happened because of the update.", "Users can't sign in, so they can't access lessons."]),
            ],
            "pronunciation": [
                ("problem", "PROB-lem."),
                ("deployed", "di-PLOYD."),
                ("sign in", "SIGN in."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start with: There's a problem with ...",
                    "target_response": "There's a problem with the login page.",
                    "acceptable_variations": ["There's a problem with the login page.", "There's a problem with the app."],
                },
                {
                    "prompt": "Say when it started.",
                    "target_response": "It started this morning.",
                    "acceptable_variations": ["It started this morning.", "It started yesterday afternoon."],
                },
                {
                    "prompt": "Say the impact with so.",
                    "target_response": "Users can't sign in, so they can't access their lessons.",
                    "acceptable_variations": ["Users can't sign in, so they can't access their lessons.", "Users can't sign in, so they can't use the app."],
                },
            ],
            "quiz": [
                {
                    "key": "problem_starter",
                    "type": "multiple_choice",
                    "prompt": "Which sentence starts a problem description?",
                    "options": ["There's a problem with the login page.", "I like the login page.", "Let's go home."],
                    "correct_answer": "There's a problem with the login page.",
                },
                {
                    "key": "so_result",
                    "type": "multiple_choice",
                    "prompt": 'Which word shows a result (impact)?',
                    "options": ["so", "because", "but"],
                    "correct_answer": "so",
                },
                {
                    "key": "past_started",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct past sentence.",
                    "options": ["It start this morning.", "It started this morning.", "It starting this morning."],
                    "correct_answer": "It started this morning.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_problem_describe",
                "opening_line": "What's going on?",
                "learner_goal": "Describe the problem, say when it started, and explain the impact.",
                "turns": [
                    {
                        "coach": "What's going on?",
                        "hint": "Mulai dengan: There's a problem with ...",
                        "sample_answer": "There's a problem with the login page.",
                        "focus": "State the problem",
                        "expected_keywords": ["problem", "with"],
                    },
                    {
                        "coach": "When did it start?",
                        "hint": "Jawab kapan mulai.",
                        "sample_answer": "It started this morning when we deployed the update.",
                        "focus": "State timing and trigger",
                        "expected_keywords": ["started", "when"],
                    },
                    {
                        "coach": "What is the impact?",
                        "hint": "Jelaskan dampak pakai so.",
                        "sample_answer": "Users can't sign in, so they can't access their lessons.",
                        "focus": "Explain impact",
                        "expected_keywords": ["can't", "so"],
                    },
                ],
                "target_phrases": ["There's a problem with ...", "It started when ...", "..., so ..."],
            },
            "reading_support": "A good problem description includes: what the problem is, when it started, what triggered it, and the impact on users.",
            "writing_support_lines": [
                "Write 4 sentences:",
                "1. There's a problem with ...",
                "2. It started ...",
                "3. It happened when ...",
                "4. Users can't ..., so ...",
            ],
            "goal_examples": ["There's a problem with ...", "It started ...", "Users can't ..., so ..."],
        },
        {
            "lesson_key": "lesson-02-suggesting-a-solution",
            "slug": "suggesting-a-solution",
            "title": "Suggesting a Solution",
            "conversation_situation": "suggesting_a_solution",
            "conversation_goal": "Suggest a solution politely and explain why it could help.",
            "grammar_summary": "Use We could... / We should... / I suggest... because... to propose solutions.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu diskusi solusi. Kamu kasih saran, jelaskan alasan, dan pilih langkah aman.",
            "dialogue": [
                ("Alex", "Any ideas to fix it?"),
                ("Mina", "We could roll back the update."),
                ("Alex", "Why do you think that's best?"),
                ("Mina", "Because the issue started after the deploy, and rollback is quick."),
                ("Alex", "That makes sense. Anything else?"),
                ("Mina", "We should also add a quick test so it doesn't happen again."),
                ("Alex", "Good plan."),
            ],
            "translations": [
                ("Alex", "Any ideas to fix it?", "Ada ide buat beresin?"),
                ("Mina", "We could roll back the update.", "Kita bisa rollback update-nya."),
                ("Alex", "Why do you think that's best?", "Kenapa kamu pikir itu paling bagus?"),
                ("Mina", "Because the issue started after the deploy, and rollback is quick.", "Karena masalahnya mulai setelah deploy, dan rollback itu cepat."),
                ("Alex", "That makes sense. Anything else?", "Masuk akal. Ada lagi?"),
                ("Mina", "We should also add a quick test so it doesn't happen again.", "Kita juga harus tambah quick test supaya nggak kejadian lagi."),
                ("Alex", "Good plan.", "Rencana bagus."),
            ],
            "useful_phrases": [
                {
                    "phrase": "We could roll back the update.",
                    "meaning_id": "Kita bisa rollback update-nya.",
                    "usage_note": "Could is a polite suggestion.",
                    "common_mistake": 'Do not say "We can rollback" if you want a softer suggestion; use could.',
                },
                {
                    "phrase": "I suggest we roll it back.",
                    "meaning_id": "Aku saranin kita rollback.",
                    "usage_note": "I suggest is common in meetings.",
                    "common_mistake": 'Do not say "I suggestion".',
                },
                {
                    "phrase": "Because rollback is quick.",
                    "meaning_id": "Karena rollback itu cepat.",
                    "usage_note": "Give one clear reason.",
                    "common_mistake": "Avoid too many reasons in one sentence; keep it simple.",
                },
                {
                    "phrase": "We should add a quick test.",
                    "meaning_id": "Kita harus tambah quick test.",
                    "usage_note": "Should suggests the best next action.",
                    "common_mistake": 'Do not say "We must" if you want polite suggestions; should is softer.',
                },
                {
                    "phrase": "So it doesn't happen again.",
                    "meaning_id": "Supaya nggak kejadian lagi.",
                    "usage_note": "So shows purpose/result.",
                    "common_mistake": 'Do not say "so not happen"; include it.',
                },
            ],
            "grammar_md": [
                ("We could... / We should...", ["We could roll back the update.", "We should add a quick test."]),
                ("Suggestion + reason", ["I suggest we roll it back because it's quick.", "We could do it now because it's low risk."]),
            ],
            "pronunciation": [
                ("could", "KUD (soft)."),
                ("should", "SHUD."),
                ("roll back", "ROLL back."),
            ],
            "response_prompts": [
                {
                    "prompt": "Suggest a solution with could.",
                    "target_response": "We could roll back the update.",
                    "acceptable_variations": ["We could roll back the update.", "We could restart the service."],
                },
                {
                    "prompt": "Give one reason with because.",
                    "target_response": "Because rollback is quick.",
                    "acceptable_variations": ["Because rollback is quick.", "Because it's low risk."],
                },
                {
                    "prompt": "Add a preventive step with should + so.",
                    "target_response": "We should add a quick test so it doesn't happen again.",
                    "acceptable_variations": ["We should add a quick test so it doesn't happen again.", "We should add monitoring so we catch it early."],
                },
            ],
            "quiz": [
                {
                    "key": "could_usage",
                    "type": "multiple_choice",
                    "prompt": "Which is a polite suggestion?",
                    "options": ["We could roll back the update.", "Roll back now!", "You do it."],
                    "correct_answer": "We could roll back the update.",
                },
                {
                    "key": "should_usage",
                    "type": "multiple_choice",
                    "prompt": "Which sentence suggests the best next step?",
                    "options": ["We should add a test.", "We like tests.", "We tested yesterday."],
                    "correct_answer": "We should add a test.",
                },
                {
                    "key": "reason_word",
                    "type": "multiple_choice",
                    "prompt": "Which word introduces a reason?",
                    "options": ["because", "so", "then"],
                    "correct_answer": "because",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_problem_suggest_solution",
                "opening_line": "Any ideas to fix it?",
                "learner_goal": "Suggest a solution with could/should and give a reason.",
                "turns": [
                    {
                        "coach": "Any ideas to fix it?",
                        "hint": "Kasih saran dengan could.",
                        "sample_answer": "We could roll back the update.",
                        "focus": "Suggest a solution",
                        "expected_keywords": ["could", "roll"],
                    },
                    {
                        "coach": "Why?",
                        "hint": "Jawab dengan because + reason.",
                        "sample_answer": "Because rollback is quick and low risk.",
                        "focus": "Give a reason",
                        "expected_keywords": ["because"],
                    },
                    {
                        "coach": "How can we prevent it next time?",
                        "hint": "Gunakan should + so.",
                        "sample_answer": "We should add a quick test so it doesn't happen again.",
                        "focus": "Preventive step",
                        "expected_keywords": ["should", "so"],
                    },
                ],
                "target_phrases": ["We could ...", "Because ...", "We should ... so ..."],
            },
            "reading_support": "A good solution suggestion includes: the action, one reason why it helps, and one step to prevent the same problem later.",
            "writing_support_lines": [
                "Write 4 sentences:",
                "1. We could ...",
                "2. Because ...",
                "3. We should ...",
                "4. ... so it doesn't happen again.",
            ],
            "goal_examples": ["We could ...", "Because ...", "We should ... so ..."],
        },
        {
            "lesson_key": "lesson-03-responding-to-advice",
            "slug": "responding-to-advice",
            "title": "Responding to Advice",
            "conversation_situation": "responding_to_advice",
            "conversation_goal": "Respond to advice politely and decide what you will do next.",
            "grammar_summary": "Use That sounds good / You're right / I'll try... to respond to advice and commit to an action.",
            "speakers": ("Leo", "Mina"),
            "situation_id": "Kamu cerita masalah kecil, teman kasih saran. Kamu respon dengan sopan dan bilang langkahmu.",
            "dialogue": [
                ("Mina", "I'm stressed because I keep missing my speaking practice."),
                ("Leo", "Maybe you should set a small daily goal."),
                ("Mina", "That sounds good. What do you suggest?"),
                ("Leo", "Try five minutes every morning."),
                ("Mina", "You're right. I'll try that starting tomorrow."),
                ("Leo", "And maybe track it in a checklist."),
                ("Mina", "Good idea. Thanks."),
            ],
            "translations": [
                ("Mina", "I'm stressed because I keep missing my speaking practice.", "Aku stres karena aku terus kelewat latihan speaking."),
                ("Leo", "Maybe you should set a small daily goal.", "Mungkin kamu harus bikin target kecil harian."),
                ("Mina", "That sounds good. What do you suggest?", "Kedengarannya bagus. Kamu saranin apa?"),
                ("Leo", "Try five minutes every morning.", "Coba lima menit tiap pagi."),
                ("Mina", "You're right. I'll try that starting tomorrow.", "Kamu bener. Aku akan coba mulai besok."),
                ("Leo", "And maybe track it in a checklist.", "Dan mungkin dicatat pakai checklist."),
                ("Mina", "Good idea. Thanks.", "Ide bagus. Makasih."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Maybe you should set a small daily goal.",
                    "meaning_id": "Mungkin kamu harus bikin target kecil harian.",
                    "usage_note": "A gentle advice sentence.",
                    "common_mistake": 'Do not say "You must"; should is softer.',
                },
                {
                    "phrase": "That sounds good.",
                    "meaning_id": "Kedengarannya bagus.",
                    "usage_note": "A polite way to accept advice.",
                    "common_mistake": 'Do not say "That sound good"; add -s.',
                },
                {
                    "phrase": "You're right.",
                    "meaning_id": "Kamu bener.",
                    "usage_note": "Agree and accept the point.",
                    "common_mistake": 'Do not say "You right".',
                },
                {
                    "phrase": "I'll try that starting tomorrow.",
                    "meaning_id": "Aku akan coba mulai besok.",
                    "usage_note": "Commit to an action plan.",
                    "common_mistake": "Don't overpromise; try is realistic.",
                },
                {
                    "phrase": "Good idea. Thanks.",
                    "meaning_id": "Ide bagus. Makasih.",
                    "usage_note": "Close politely after advice.",
                    "common_mistake": "Avoid just saying thanks; add good idea to show you listened.",
                },
            ],
            "grammar_md": [
                ("Advice with should", ["Maybe you should set a daily goal.", "You should try a shorter session."]),
                ("Responding to advice", ["That sounds good.", "You're right.", "I'll try that starting tomorrow."]),
            ],
            "pronunciation": [
                ("should", "SHUD."),
                ("sounds good", "SOWNDZ good."),
                ("starting tomorrow", "STAR-ting to-MOR-row."),
            ],
            "response_prompts": [
                {
                    "prompt": "Accept advice politely.",
                    "target_response": "That sounds good.",
                    "acceptable_variations": ["That sounds good.", "That sounds helpful."],
                },
                {
                    "prompt": "Agree: You're right.",
                    "target_response": "You're right.",
                    "acceptable_variations": ["You're right.", "Yeah, you're right."],
                },
                {
                    "prompt": "Commit to a small action.",
                    "target_response": "I'll try that starting tomorrow.",
                    "acceptable_variations": ["I'll try that starting tomorrow.", "I'll try that this week."],
                },
            ],
            "quiz": [
                {
                    "key": "sounds_good",
                    "type": "multiple_choice",
                    "prompt": 'Which response accepts advice politely?',
                    "options": ["That sounds good.", "No.", "Whatever."],
                    "correct_answer": "That sounds good.",
                },
                {
                    "key": "youre_right",
                    "type": "multiple_choice",
                    "prompt": 'Which sentence is correct?',
                    "options": ["You right.", "You're right.", "Your right."],
                    "correct_answer": "You're right.",
                },
                {
                    "key": "should_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "should" usually express?',
                    "options": ["saran", "masa lalu", "jumlah"],
                    "correct_answer": "saran",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_problem_respond_advice",
                "opening_line": "Maybe you should try a small daily goal.",
                "learner_goal": "Accept advice politely and say what you will do next.",
                "turns": [
                    {
                        "coach": "Maybe you should try a small daily goal.",
                        "hint": "Terima saran dengan sopan.",
                        "sample_answer": "That sounds good.",
                        "focus": "Accept advice",
                        "expected_keywords": ["sounds"],
                    },
                    {
                        "coach": "When will you start?",
                        "hint": "Jawab dengan rencana singkat.",
                        "sample_answer": "I'll try that starting tomorrow.",
                        "focus": "Commit to action",
                        "expected_keywords": ["try", "tomorrow"],
                    },
                    {
                        "coach": "How will you keep it consistent?",
                        "hint": "Sebutkan satu cara (checklist/alarm).",
                        "sample_answer": "I'll set a reminder and track it in a checklist.",
                        "focus": "Plan for consistency",
                        "expected_keywords": ["reminder", "checklist"],
                    },
                ],
                "target_phrases": ["That sounds good.", "You're right.", "I'll try that starting ..."],
            },
            "reading_support": "When someone gives advice, a good response is: accept politely, agree if appropriate, and say a clear next step you will try.",
            "writing_support_lines": [
                "Write 4 sentences:",
                "1. That sounds good.",
                "2. You're right.",
                "3. I'll try ... starting ...",
                "4. I'll also ... (reminder/checklist)",
            ],
            "goal_examples": ["That sounds good.", "You're right.", "I'll try that starting ..."],
        },
        {
            "lesson_key": "lesson-04-making-a-simple-decision",
            "slug": "making-a-simple-decision",
            "title": "Making a Simple Decision",
            "conversation_situation": "making_a_simple_decision",
            "conversation_goal": "Compare two options and make a simple decision with a clear reason.",
            "grammar_summary": "Use We could... but... / I'd rather... / Let's... because... to make decisions politely.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu pilih antara dua opsi. Kamu jelaskan alasan singkat dan putuskan bareng.",
            "dialogue": [
                ("Leo", "We have two options: fix it now or wait until tomorrow."),
                ("Mina", "I'd rather fix it now because users are blocked."),
                ("Leo", "True. But it's late."),
                ("Mina", "We could do a quick rollback and then sleep."),
                ("Leo", "That sounds reasonable."),
                ("Mina", "Okay, let's roll back now and do a full review tomorrow."),
                ("Leo", "Deal."),
            ],
            "translations": [
                ("Leo", "We have two options: fix it now or wait until tomorrow.", "Kita punya dua opsi: beresin sekarang atau tunggu besok."),
                ("Mina", "I'd rather fix it now because users are blocked.", "Aku lebih pilih beresin sekarang karena user ke-block."),
                ("Leo", "True. But it's late.", "Bener. Tapi udah malam."),
                ("Mina", "We could do a quick rollback and then sleep.", "Kita bisa rollback cepat lalu tidur."),
                ("Leo", "That sounds reasonable.", "Kedengarannya masuk akal."),
                ("Mina", "Okay, let's roll back now and do a full review tomorrow.", "Oke, kita rollback sekarang dan review penuh besok."),
                ("Leo", "Deal.", "Deal."),
            ],
            "useful_phrases": [
                {
                    "phrase": "We have two options.",
                    "meaning_id": "Kita punya dua opsi.",
                    "usage_note": "Start a decision discussion.",
                    "common_mistake": 'Do not say "We have two option" without -s.',
                },
                {
                    "phrase": "I'd rather fix it now.",
                    "meaning_id": "Aku lebih pilih beresin sekarang.",
                    "usage_note": "A clear preference statement.",
                    "common_mistake": 'Do not say "I rather". Use I\'d rather.',
                },
                {
                    "phrase": "We could do a quick rollback.",
                    "meaning_id": "Kita bisa rollback cepat.",
                    "usage_note": "A practical compromise option.",
                    "common_mistake": "Keep it simple; avoid long technical details.",
                },
                {
                    "phrase": "That sounds reasonable.",
                    "meaning_id": "Kedengarannya masuk akal.",
                    "usage_note": "Agree to a plan politely.",
                    "common_mistake": 'Do not say "That sound reasonable"; add -s.',
                },
                {
                    "phrase": "Let's do a full review tomorrow.",
                    "meaning_id": "Besok kita review penuh.",
                    "usage_note": "Make a clear next step plan.",
                    "common_mistake": 'Do not say "Let\'s to do".',
                },
            ],
            "grammar_md": [
                ("Preference with I'd rather", ["I'd rather fix it now.", "I'd rather wait until tomorrow."]),
                ("Decision with let's + because", ["Let's roll back now because users are blocked.", "Let's decide after we check the logs."]),
            ],
            "pronunciation": [
                ("I'd rather", "I'd RATH-er."),
                ("reasonable", "REE-zuh-nuh-bul."),
                ("deal", "DEEL."),
            ],
            "response_prompts": [
                {
                    "prompt": "State a preference with I'd rather.",
                    "target_response": "I'd rather fix it now because users are blocked.",
                    "acceptable_variations": ["I'd rather fix it now because users are blocked.", "I'd rather fix it now because it's urgent."],
                },
                {
                    "prompt": "Suggest a compromise with could.",
                    "target_response": "We could do a quick rollback and review tomorrow.",
                    "acceptable_variations": ["We could do a quick rollback and review tomorrow.", "We could do a quick fix and check tomorrow."],
                },
                {
                    "prompt": "Make a decision with let's.",
                    "target_response": "Okay, let's roll back now.",
                    "acceptable_variations": ["Okay, let's roll back now.", "Let's do it now."],
                },
            ],
            "quiz": [
                {
                    "key": "rather_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "I\'d rather" mean?',
                    "options": ["saya lebih memilih", "saya tidak tahu", "saya sudah selesai"],
                    "correct_answer": "saya lebih memilih",
                },
                {
                    "key": "two_options",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["We have two options.", "We have two option.", "We has two options."],
                    "correct_answer": "We have two options.",
                },
                {
                    "key": "reasonable_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "reasonable" mean?',
                    "options": ["masuk akal", "berbahaya", "lambat"],
                    "correct_answer": "masuk akal",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_problem_make_decision",
                "opening_line": "We have two options. What do you prefer?",
                "learner_goal": "State a preference, suggest a compromise, and make a simple decision.",
                "turns": [
                    {
                        "coach": "We have two options. What do you prefer?",
                        "hint": "Gunakan I'd rather + because.",
                        "sample_answer": "I'd rather fix it now because users are blocked.",
                        "focus": "State preference with reason",
                        "expected_keywords": ["rather", "because"],
                    },
                    {
                        "coach": "But it's late. Any compromise?",
                        "hint": "Gunakan We could ...",
                        "sample_answer": "We could do a quick rollback and review tomorrow.",
                        "focus": "Suggest compromise",
                        "expected_keywords": ["could", "rollback"],
                    },
                    {
                        "coach": "Okay. What's the decision?",
                        "hint": "Gunakan Let's ...",
                        "sample_answer": "Okay, let's roll back now.",
                        "focus": "Make decision",
                        "expected_keywords": ["let's"],
                    },
                ],
                "target_phrases": ["I'd rather ...", "We could ...", "Let's ..."],
            },
            "reading_support": "A simple decision includes: options, preference, a reason, and a clear next step (decision).",
            "writing_support_lines": [
                "Write 4 sentences:",
                "1. We have two options: ... or ...",
                "2. I'd rather ... because ...",
                "3. We could ...",
                "4. Let's ...",
            ],
            "goal_examples": ["I'd rather ... because ...", "We could ...", "Let's ..."],
        },
        {
            "lesson_key": "lesson-05-problem-solving-mission",
            "slug": "problem-solving-mission",
            "title": "Problem Solving Mission",
            "conversation_situation": "mission_problem_solution_decision",
            "conversation_goal": "Complete a mini problem-solving conversation: describe a problem, suggest a solution, respond to a concern, and decide next steps.",
            "grammar_summary": "Combine: There's a problem with..., We could/should..., Because/so..., Let's... to complete a short problem-solving flow.",
            "speakers": ("Alex", "Mina"),
            "situation_id": "Misi: kamu jelaskan problem, kasih solusi, tanggapi concern, lalu putuskan next step.",
            "dialogue": [
                ("Alex", "Quick check: what's the issue?"),
                ("Mina", "There's a problem with the login page. Users can't sign in."),
                ("Alex", "When did it start?"),
                ("Mina", "It started this morning after the deploy, so it's urgent."),
                ("Alex", "What should we do?"),
                ("Mina", "We could roll back now because it's quick."),
                ("Alex", "But will it affect other features?"),
                ("Mina", "It might, so let's roll back and then test the key flows."),
            ],
            "translations": [
                ("Alex", "Quick check: what's the issue?", "Cek cepat: masalahnya apa?"),
                ("Mina", "There's a problem with the login page. Users can't sign in.", "Ada masalah di halaman login. User nggak bisa login."),
                ("Alex", "When did it start?", "Mulai kapan?"),
                ("Mina", "It started this morning after the deploy, so it's urgent.", "Mulainya pagi ini setelah deploy, jadi ini urgent."),
                ("Alex", "What should we do?", "Kita harus ngapain?"),
                ("Mina", "We could roll back now because it's quick.", "Kita bisa rollback sekarang karena cepat."),
                ("Alex", "But will it affect other features?", "Tapi bakal ngaruh ke fitur lain nggak?"),
                ("Mina", "It might, so let's roll back and then test the key flows.", "Mungkin, jadi kita rollback lalu tes alur penting."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Quick check: what's the issue?",
                    "meaning_id": "Cek cepat: masalahnya apa?",
                    "usage_note": "A common workplace opener.",
                    "common_mistake": 'Do not say "What is issue?" without the.',
                },
                {
                    "phrase": "There's a problem with the login page.",
                    "meaning_id": "Ada masalah di halaman login.",
                    "usage_note": "Clear problem statement.",
                    "common_mistake": "Start with the problem before details.",
                },
                {
                    "phrase": "We could roll back now because it's quick.",
                    "meaning_id": "Kita bisa rollback sekarang karena cepat.",
                    "usage_note": "Solution + reason.",
                    "common_mistake": "Avoid too many reasons; one is enough.",
                },
                {
                    "phrase": "But will it affect other features?",
                    "meaning_id": "Tapi bakal ngaruh ke fitur lain nggak?",
                    "usage_note": "A realistic concern question.",
                    "common_mistake": 'Do not drop will in this future question.',
                },
                {
                    "phrase": "It might, so let's roll back and then test the key flows.",
                    "meaning_id": "Mungkin, jadi kita rollback lalu tes alur penting.",
                    "usage_note": "Respond to concern and propose next steps.",
                    "common_mistake": "Keep next steps short and clear.",
                },
            ],
            "grammar_md": [
                ("Problem -> solution -> decision", ["There's a problem with ...", "We could ... because ...", "But will it ...?", "It might, so let's ..."]),
            ],
            "pronunciation": [
                ("issue", "ISH-yoo."),
                ("urgent", "UR-jent."),
                ("affect", "uh-FEKT."),
            ],
            "response_prompts": [
                {
                    "prompt": "Describe the problem.",
                    "target_response": "There's a problem with the login page. Users can't sign in.",
                    "acceptable_variations": ["There's a problem with the login page. Users can't sign in.", "There's a problem with the app. Users can't sign in."],
                },
                {
                    "prompt": "Suggest a solution with because.",
                    "target_response": "We could roll back now because it's quick.",
                    "acceptable_variations": ["We could roll back now because it's quick.", "We could roll back now because it's low risk."],
                },
                {
                    "prompt": "Respond to a concern and decide next steps.",
                    "target_response": "It might, so let's roll back and then test the key flows.",
                    "acceptable_variations": ["It might, so let's roll back and then test the key flows.", "It might, so let's roll back and test quickly."],
                },
            ],
            "quiz": [
                {
                    "key": "mission_order",
                    "type": "multiple_choice",
                    "prompt": "Which order is correct for problem solving?",
                    "options": ["Problem -> impact -> solution -> next steps", "Greeting -> goodbye", "Price -> size -> color"],
                    "correct_answer": "Problem -> impact -> solution -> next steps",
                },
                {
                    "key": "might_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "might" express?',
                    "options": ["kemungkinan", "kepastian", "masa lalu"],
                    "correct_answer": "kemungkinan",
                },
                {
                    "key": "affect_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "affect" mean?',
                    "options": ["mempengaruhi", "membatalkan", "mengulang"],
                    "correct_answer": "mempengaruhi",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_problem_mission",
                "opening_line": "Quick check: what's the issue?",
                "learner_goal": "Describe the issue, propose a solution with a reason, respond to a concern, and decide next steps.",
                "turns": [
                    {
                        "coach": "Quick check: what's the issue?",
                        "hint": "Jelaskan problem + impact singkat.",
                        "sample_answer": "There's a problem with the login page. Users can't sign in.",
                        "focus": "Describe problem and impact",
                        "expected_keywords": ["problem", "can't"],
                    },
                    {
                        "coach": "What should we do?",
                        "hint": "Kasih solusi dengan could/should + because.",
                        "sample_answer": "We could roll back now because it's quick.",
                        "focus": "Suggest solution with reason",
                        "expected_keywords": ["could", "because"],
                    },
                    {
                        "coach": "But will it affect other features?",
                        "hint": "Jawab dengan might + next steps (so let's...).",
                        "sample_answer": "It might, so let's roll back and then test the key flows.",
                        "focus": "Respond to concern and decide next steps",
                        "expected_keywords": ["might", "so", "let's"],
                    },
                ],
                "target_phrases": ["There's a problem with ...", "We could ... because ...", "It might, so let's ..."],
            },
            "reading_support": "A problem-solving mission includes: issue, impact, timeline, solution, a concern, and a clear decision for next steps.",
            "writing_support_lines": [
                "Write your mission (5 lines):",
                "1. There's a problem with ...",
                "2. It started ... so ...",
                "3. We could ... because ...",
                "4. It might ...",
                "5. So let's ...",
            ],
            "goal_examples": ["There's a problem with ...", "We could ... because ...", "It might, so let's ..."],
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
                "speaking": {"minimum_score": 70},
                "relevance": {"minimum_score": 70},
                "grammar": {"minimum_score": 65},
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

