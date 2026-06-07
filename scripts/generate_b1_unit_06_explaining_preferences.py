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

        Read it again and underline the preference and reason words (prefer, rather, because, advantage, downside).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B1"
    b1_root = Path("content/curriculum/english/B1")
    units_root = b1_root / "units"
    unit_key = "unit-06-explaining-preferences"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-06-explaining-preferences
            level_code: B1
            title: Explaining Preferences
            main_conversation_outcome: Compare options and explain preferences with reasons.
            status: in_production
            lessons:
              - lesson-01-comparing-two-options
              - lesson-02-explaining-why-you-prefer-something
              - lesson-03-asking-about-pros-and-cons
              - lesson-04-reaching-agreement
              - lesson-05-preference-discussion-mission
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
            "lesson_key": "lesson-01-comparing-two-options",
            "slug": "comparing-two-options",
            "title": "Comparing Two Options",
            "conversation_situation": "comparing_two_options",
            "conversation_goal": "Compare two options and ask what the other person prefers.",
            "grammar_summary": "Use Option A is... but Option B is... and Which do you prefer? to compare options clearly.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu pilih antara dua opsi (misalnya dua restoran). Kamu bandingin singkat, lalu tanya preferensi teman kamu.",
            "dialogue": [
                ("Mina", "We have two options for dinner: Sushi Place or Noodle House."),
                ("Leo", "Okay. What's the difference?"),
                ("Mina", "Sushi Place is nicer, but it's more expensive."),
                ("Leo", "And Noodle House?"),
                ("Mina", "It's cheaper and faster, but it's usually crowded."),
                ("Leo", "Hmm. Which do you prefer?"),
                ("Mina", "I think I prefer Noodle House tonight."),
                ("Leo", "Sounds good to me."),
            ],
            "translations": [
                ("Mina", "We have two options for dinner: Sushi Place or Noodle House.", "Kita punya dua opsi buat makan malam: Sushi Place atau Noodle House."),
                ("Leo", "Okay. What's the difference?", "Oke. Bedanya apa?"),
                ("Mina", "Sushi Place is nicer, but it's more expensive.", "Sushi Place lebih enak/nyaman, tapi lebih mahal."),
                ("Leo", "And Noodle House?", "Kalau Noodle House?"),
                ("Mina", "It's cheaper and faster, but it's usually crowded.", "Lebih murah dan cepat, tapi biasanya rame."),
                ("Leo", "Hmm. Which do you prefer?", "Hmm. Kamu lebih pilih yang mana?"),
                ("Mina", "I think I prefer Noodle House tonight.", "Kayaknya aku lebih pilih Noodle House malam ini."),
                ("Leo", "Sounds good to me.", "Oke buat aku."),
            ],
            "useful_phrases": [
                {
                    "phrase": "We have two options.",
                    "meaning_id": "Kita punya dua opsi.",
                    "usage_note": "Start a comparison clearly.",
                    "common_mistake": 'Do not say "two option"; add -s.',
                },
                {
                    "phrase": "Option A is nicer, but it's more expensive.",
                    "meaning_id": "Opsi A lebih nyaman, tapi lebih mahal.",
                    "usage_note": "Use but to show contrast.",
                    "common_mistake": 'Do not say "more expensive but nicer" without clear structure; keep it simple.',
                },
                {
                    "phrase": "It's cheaper and faster.",
                    "meaning_id": "Lebih murah dan lebih cepat.",
                    "usage_note": "Simple comparison with two adjectives.",
                    "common_mistake": 'Do not say "more cheap"; use cheaper.',
                },
                {
                    "phrase": "Which do you prefer?",
                    "meaning_id": "Kamu lebih pilih yang mana?",
                    "usage_note": "A natural preference question.",
                    "common_mistake": 'Do not say "Which you prefer?" without do.',
                },
                {
                    "phrase": "I think I prefer Noodle House.",
                    "meaning_id": "Kayaknya aku lebih pilih Noodle House.",
                    "usage_note": "I think softens your preference.",
                    "common_mistake": 'Do not say "I prefer it" without saying what it is.',
                },
            ],
            "grammar_md": [
                ("Compare with but", ["Sushi Place is nicer, but it's more expensive.", "It's closer, but it's noisier."]),
                ("Preference question", ["Which do you prefer?", "Which one do you prefer?"]),
            ],
            "pronunciation": [
                ("options", "OP-shunz."),
                ("prefer", "pri-FER."),
                ("expensive", "ik-SPEN-siv."),
            ],
            "response_prompts": [
                {
                    "prompt": "Compare two options with but.",
                    "target_response": "Option A is nicer, but it's more expensive.",
                    "acceptable_variations": [
                        "Option A is nicer, but it's more expensive.",
                        "Option A is closer, but it's noisier.",
                    ],
                },
                {
                    "prompt": "Ask for preference.",
                    "target_response": "Which do you prefer?",
                    "acceptable_variations": ["Which do you prefer?", "Which one do you prefer?"],
                },
                {
                    "prompt": "Say your preference.",
                    "target_response": "I think I prefer the cheaper one.",
                    "acceptable_variations": ["I think I prefer the cheaper one.", "I think I prefer option B."],
                },
            ],
            "quiz": [
                {
                    "key": "which_prefer",
                    "type": "multiple_choice",
                    "prompt": "Which sentence asks about preference?",
                    "options": ["Which do you prefer?", "Where do you go?", "What did you do?"],
                    "correct_answer": "Which do you prefer?",
                },
                {
                    "key": "cheaper_word",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct comparative form.",
                    "options": ["cheaper", "more cheap", "cheapest"],
                    "correct_answer": "cheaper",
                },
                {
                    "key": "but_usage",
                    "type": "multiple_choice",
                    "prompt": 'Which word shows contrast?',
                    "options": ["but", "because", "so"],
                    "correct_answer": "but",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_preference_compare_options",
                "opening_line": "We have two options. What's the difference?",
                "learner_goal": "Compare two options and ask what the other person prefers.",
                "turns": [
                    {
                        "coach": "We have two options. What's the difference?",
                        "hint": "Bandingin pakai but.",
                        "sample_answer": "Option A is nicer, but it's more expensive.",
                        "focus": "Compare options",
                        "expected_keywords": ["but", "more"],
                    },
                    {
                        "coach": "Okay. And option B?",
                        "hint": "Sebutkan 1-2 poin: cheaper/faster/crowded.",
                        "sample_answer": "It's cheaper and faster, but it's usually crowded.",
                        "focus": "Describe option B",
                        "expected_keywords": ["cheaper", "faster"],
                    },
                    {
                        "coach": "Got it. Ask me what I prefer.",
                        "hint": "Tanya: Which do you prefer?",
                        "sample_answer": "Which do you prefer?",
                        "focus": "Ask preference",
                        "expected_keywords": ["prefer"],
                    },
                ],
                "target_phrases": ["We have two options.", "..., but ...", "Which do you prefer?"],
            },
            "reading_support": "When comparing two options, mention one benefit and one drawback. Then ask the other person what they prefer.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. We have two options: A or B.",
                "2. Option A is ..., but ...",
                "3. Option B is ..., but ...",
                "4. Which do you prefer?",
                "5. I think I prefer ...",
            ],
            "goal_examples": ["Option A is ..., but ...", "Which do you prefer?", "I think I prefer ..."],
        },
        {
            "lesson_key": "lesson-02-explaining-why-you-prefer-something",
            "slug": "explaining-why-you-prefer-something",
            "title": "Explaining Why You Prefer Something",
            "conversation_situation": "explaining_preference_with_reason",
            "conversation_goal": "State a preference and explain the main reason clearly.",
            "grammar_summary": "Use I prefer... because... / The main reason is... to explain preferences politely and clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu jelasin kenapa kamu prefer satu opsi. Kamu sebut preferensinya dan alasan utamanya.",
            "dialogue": [
                ("Alex", "So which one do you prefer?"),
                ("Mina", "I prefer the earlier flight."),
                ("Alex", "Why?"),
                ("Mina", "Because it gives us more time in the afternoon."),
                ("Alex", "That makes sense. Any other reasons?"),
                ("Mina", "The main reason is I don't want to arrive too late."),
                ("Alex", "Okay, let's book it."),
                ("Mina", "Great."),
            ],
            "translations": [
                ("Alex", "So which one do you prefer?", "Jadi kamu prefer yang mana?"),
                ("Mina", "I prefer the earlier flight.", "Aku prefer penerbangan yang lebih pagi."),
                ("Alex", "Why?", "Kenapa?"),
                ("Mina", "Because it gives us more time in the afternoon.", "Karena itu kasih kita lebih banyak waktu di sore hari."),
                ("Alex", "That makes sense. Any other reasons?", "Masuk akal. Ada alasan lain?"),
                ("Mina", "The main reason is I don't want to arrive too late.", "Alasan utamanya aku nggak mau sampai terlalu malam."),
                ("Alex", "Okay, let's book it.", "Oke, ayo kita booking itu."),
                ("Mina", "Great.", "Oke."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I prefer the earlier flight.",
                    "meaning_id": "Aku prefer penerbangan yang lebih pagi.",
                    "usage_note": "A clear preference statement.",
                    "common_mistake": 'Do not say "more early"; use earlier.',
                },
                {
                    "phrase": "Because it gives us more time.",
                    "meaning_id": "Karena itu kasih kita lebih banyak waktu.",
                    "usage_note": "A simple reason sentence.",
                    "common_mistake": 'Do not say "Because gives"; include it.',
                },
                {
                    "phrase": "The main reason is I don't want to arrive too late.",
                    "meaning_id": "Alasan utamanya aku nggak mau sampai terlalu malam.",
                    "usage_note": "A clear main-reason structure.",
                    "common_mistake": 'Do not say "The main reason I don\'t want"; include is.',
                },
                {
                    "phrase": "It feels more convenient.",
                    "meaning_id": "Rasanya lebih praktis.",
                    "usage_note": "Convenient is common for preferences.",
                    "common_mistake": 'Do not say "more convenience"; use more convenient.',
                },
                {
                    "phrase": "That makes sense.",
                    "meaning_id": "Masuk akal.",
                    "usage_note": "A polite reaction to a reason.",
                    "common_mistake": 'Do not say "That make sense"; add -s.',
                },
            ],
            "grammar_md": [
                ("I prefer... because...", ["I prefer the earlier flight because it gives us more time.", "I prefer this option because it's simpler."]),
                ("The main reason is...", ["The main reason is I don't want to arrive too late.", "The main reason is it's more reliable."]),
            ],
            "pronunciation": [
                ("earlier", "ER-lee-er."),
                ("convenient", "kun-VEE-nee-ent."),
                ("reason", "REE-zun."),
            ],
            "response_prompts": [
                {
                    "prompt": "State a preference (earlier flight).",
                    "target_response": "I prefer the earlier flight.",
                    "acceptable_variations": ["I prefer the earlier flight.", "I prefer option A."],
                },
                {
                    "prompt": "Give a reason with because.",
                    "target_response": "Because it gives us more time in the afternoon.",
                    "acceptable_variations": ["Because it gives us more time.", "Because it's more convenient."],
                },
                {
                    "prompt": "Say the main reason.",
                    "target_response": "The main reason is I don't want to arrive too late.",
                    "acceptable_variations": ["The main reason is I don't want to arrive too late.", "The main reason is I want more time."],
                },
            ],
            "quiz": [
                {
                    "key": "earlier_word",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct comparative form.",
                    "options": ["earlier", "more early", "earlyer"],
                    "correct_answer": "earlier",
                },
                {
                    "key": "prefer_reason",
                    "type": "multiple_choice",
                    "prompt": "Which sentence explains a preference with a reason?",
                    "options": ["I prefer option A because it's simpler.", "I prefer because option A.", "I option A prefer."],
                    "correct_answer": "I prefer option A because it's simpler.",
                },
                {
                    "key": "main_reason",
                    "type": "multiple_choice",
                    "prompt": 'What does "The main reason is..." do?',
                    "options": ["menjelaskan alasan utama", "mengucapkan salam", "mengubah topik"],
                    "correct_answer": "menjelaskan alasan utama",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_preference_explain_reason",
                "opening_line": "Which one do you prefer?",
                "learner_goal": "State your preference and explain the main reason.",
                "turns": [
                    {
                        "coach": "Which one do you prefer?",
                        "hint": "Jawab dengan I prefer ...",
                        "sample_answer": "I prefer the earlier flight.",
                        "focus": "State preference",
                        "expected_keywords": ["prefer"],
                    },
                    {
                        "coach": "Why?",
                        "hint": "Jawab dengan because + reason.",
                        "sample_answer": "Because it gives us more time in the afternoon.",
                        "focus": "Explain reason",
                        "expected_keywords": ["because", "time"],
                    },
                    {
                        "coach": "What is the main reason?",
                        "hint": "Gunakan The main reason is ...",
                        "sample_answer": "The main reason is I don't want to arrive too late.",
                        "focus": "State main reason",
                        "expected_keywords": ["main reason", "don't want"],
                    },
                ],
                "target_phrases": ["I prefer ...", "Because ...", "The main reason is ..."],
            },
            "reading_support": "To explain a preference, state what you prefer and give one clear reason. If needed, add the main reason to make it stronger.",
            "writing_support_lines": [
                "Write 4 lines:",
                "1. I prefer ...",
                "2. Because ...",
                "3. The main reason is ...",
                "4. That makes sense.",
            ],
            "goal_examples": ["I prefer ... because ...", "The main reason is ...", "It feels more convenient."],
        },
        {
            "lesson_key": "lesson-03-asking-about-pros-and-cons",
            "slug": "asking-about-pros-and-cons",
            "title": "Asking About Pros and Cons",
            "conversation_situation": "asking_pros_cons",
            "conversation_goal": "Ask about pros and cons and respond with one advantage and one downside.",
            "grammar_summary": "Use What are the pros and cons? / The advantage is... / One downside is... to discuss trade-offs clearly.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu lagi diskusi pilihan (misalnya remote vs office). Kamu tanya pros and cons, lalu respon dengan satu kelebihan dan satu kekurangan.",
            "dialogue": [
                ("Mina", "What are the pros and cons of working remotely?"),
                ("Leo", "The advantage is you save commuting time."),
                ("Mina", "True. Any downsides?"),
                ("Leo", "One downside is you might feel isolated."),
                ("Mina", "Yeah, I get that."),
                ("Leo", "Overall, it depends on your work style."),
                ("Mina", "Makes sense."),
                ("Leo", "What's your preference?"),
            ],
            "translations": [
                ("Mina", "What are the pros and cons of working remotely?", "Apa pro dan kontra kerja remote?"),
                ("Leo", "The advantage is you save commuting time.", "Kelebihannya kamu hemat waktu perjalanan."),
                ("Mina", "True. Any downsides?", "Bener. Ada kekurangan?"),
                ("Leo", "One downside is you might feel isolated.", "Salah satu kekurangannya kamu mungkin merasa kesepian."),
                ("Mina", "Yeah, I get that.", "Iya, aku paham."),
                ("Leo", "Overall, it depends on your work style.", "Secara keseluruhan, tergantung gaya kerja kamu."),
                ("Mina", "Makes sense.", "Masuk akal."),
                ("Leo", "What's your preference?", "Kalau kamu prefer yang mana?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "What are the pros and cons?",
                    "meaning_id": "Apa pro dan kontranya?",
                    "usage_note": "A clear way to ask about trade-offs.",
                    "common_mistake": 'Do not say "What is the pros and cons?" Use are.',
                },
                {
                    "phrase": "The advantage is you save time.",
                    "meaning_id": "Kelebihannya kamu hemat waktu.",
                    "usage_note": "A simple advantage sentence.",
                    "common_mistake": 'Do not say "advantage are"; use is.',
                },
                {
                    "phrase": "One downside is you might feel isolated.",
                    "meaning_id": "Salah satu kekurangannya kamu mungkin merasa kesepian.",
                    "usage_note": "A clear downside sentence.",
                    "common_mistake": 'Do not say "One downside are"; use is.',
                },
                {
                    "phrase": "Overall, it depends.",
                    "meaning_id": "Secara keseluruhan, tergantung.",
                    "usage_note": "A natural summary phrase.",
                    "common_mistake": 'Do not say "Overall depends" without it.',
                },
                {
                    "phrase": "Any downsides?",
                    "meaning_id": "Ada kekurangan?",
                    "usage_note": "A short follow-up question.",
                    "common_mistake": 'Do not say "Any downside" without -s.',
                },
            ],
            "grammar_md": [
                ("Pros and cons question", ["What are the pros and cons?", "What are the pros and cons of this plan?"]),
                ("Advantage / downside", ["The advantage is you save time.", "One downside is it's more expensive."]),
            ],
            "pronunciation": [
                ("pros and cons", "PROHZ and KONZ."),
                ("advantage", "ad-VAN-tij."),
                ("downside", "DOWN-side."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask about pros and cons.",
                    "target_response": "What are the pros and cons?",
                    "acceptable_variations": ["What are the pros and cons?", "What are the pros and cons of this option?"],
                },
                {
                    "prompt": "Give one advantage (save time).",
                    "target_response": "The advantage is you save time.",
                    "acceptable_variations": ["The advantage is you save time.", "The advantage is it's more convenient."],
                },
                {
                    "prompt": "Give one downside (more expensive).",
                    "target_response": "One downside is it's more expensive.",
                    "acceptable_variations": ["One downside is it's more expensive.", "One downside is it's crowded."],
                },
            ],
            "quiz": [
                {
                    "key": "pros_cons_question",
                    "type": "multiple_choice",
                    "prompt": "Which sentence asks about trade-offs?",
                    "options": ["What are the pros and cons?", "What time is it?", "Where is it?"],
                    "correct_answer": "What are the pros and cons?",
                },
                {
                    "key": "advantage_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "advantage" mean?',
                    "options": ["kelebihan", "kekurangan", "jadwal"],
                    "correct_answer": "kelebihan",
                },
                {
                    "key": "downside_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "downside" mean?',
                    "options": ["kekurangan", "kelebihan", "harga"],
                    "correct_answer": "kekurangan",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_preference_pros_cons",
                "opening_line": "Ask me about pros and cons.",
                "learner_goal": "Ask about pros and cons and respond with one advantage and one downside.",
                "turns": [
                    {
                        "coach": "Ask me about pros and cons of this option.",
                        "hint": "Tanya: What are the pros and cons ...?",
                        "sample_answer": "What are the pros and cons of working remotely?",
                        "focus": "Ask about trade-offs",
                        "expected_keywords": ["pros", "cons"],
                    },
                    {
                        "coach": "Give one advantage.",
                        "hint": "Mulai dengan The advantage is ...",
                        "sample_answer": "The advantage is you save time.",
                        "focus": "State an advantage",
                        "expected_keywords": ["advantage"],
                    },
                    {
                        "coach": "Now give one downside.",
                        "hint": "Mulai dengan One downside is ...",
                        "sample_answer": "One downside is you might feel isolated.",
                        "focus": "State a downside",
                        "expected_keywords": ["downside", "might"],
                    },
                ],
                "target_phrases": ["What are the pros and cons...?", "The advantage is ...", "One downside is ..."],
            },
            "reading_support": "Pros and cons help you compare options. Ask about trade-offs, then share one advantage and one downside.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. What are the pros and cons of ...?",
                "2. The advantage is ...",
                "3. One downside is ...",
                "4. Overall, it depends.",
                "5. I think I prefer ...",
            ],
            "goal_examples": ["What are the pros and cons of ...?", "The advantage is ...", "One downside is ..."],
        },
        {
            "lesson_key": "lesson-04-reaching-agreement",
            "slug": "reaching-agreement",
            "title": "Reaching Agreement",
            "conversation_situation": "reaching_agreement_on_plan",
            "conversation_goal": "Suggest a plan, respond politely, and confirm an agreement.",
            "grammar_summary": "Use How about we... / I'm okay with... / Let's go with... to reach agreement politely.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu mau mencapai kesepakatan. Kamu usul rencana, dengar respons, lalu konfirmasi keputusan bareng.",
            "dialogue": [
                ("Alex", "So which restaurant should we choose?"),
                ("Mina", "How about we go with the cheaper one tonight?"),
                ("Alex", "I'm okay with that, but is it too crowded?"),
                ("Mina", "It might be, so let's go early."),
                ("Alex", "That works for me."),
                ("Mina", "Great. So we agree on Noodle House at 6:30?"),
                ("Alex", "Yes, let's do that."),
                ("Mina", "Perfect."),
            ],
            "translations": [
                ("Alex", "So which restaurant should we choose?", "Jadi kita pilih restoran yang mana?"),
                ("Mina", "How about we go with the cheaper one tonight?", "Gimana kalau malam ini kita pilih yang lebih murah?"),
                ("Alex", "I'm okay with that, but is it too crowded?", "Aku oke, tapi apa terlalu rame?"),
                ("Mina", "It might be, so let's go early.", "Bisa jadi, jadi kita berangkat lebih awal."),
                ("Alex", "That works for me.", "Oke buat aku."),
                ("Mina", "Great. So we agree on Noodle House at 6:30?", "Oke. Jadi kita sepakat Noodle House jam 6:30?"),
                ("Alex", "Yes, let's do that.", "Iya, ayo."),
                ("Mina", "Perfect.", "Sip."),
            ],
            "useful_phrases": [
                {
                    "phrase": "How about we go with the cheaper one?",
                    "meaning_id": "Gimana kalau kita pilih yang lebih murah?",
                    "usage_note": "A polite suggestion structure.",
                    "common_mistake": 'Do not say "How about we goes"; use go.',
                },
                {
                    "phrase": "I'm okay with that.",
                    "meaning_id": "Aku oke dengan itu.",
                    "usage_note": "A polite acceptance phrase.",
                    "common_mistake": 'Do not say "I okay"; include am.',
                },
                {
                    "phrase": "That works for me.",
                    "meaning_id": "Oke buat aku.",
                    "usage_note": "A natural agreement phrase.",
                    "common_mistake": 'Do not say "That work for me"; add -s.',
                },
                {
                    "phrase": "So we agree on Noodle House at 6:30?",
                    "meaning_id": "Jadi kita sepakat Noodle House jam 6:30?",
                    "usage_note": "Confirm agreement clearly.",
                    "common_mistake": 'Do not forget the time if it matters; confirm it clearly.',
                },
                {
                    "phrase": "Let's go early.",
                    "meaning_id": "Yuk berangkat lebih awal.",
                    "usage_note": "A simple solution to a concern.",
                    "common_mistake": 'Do not say "Let\'s to go".',
                },
            ],
            "grammar_md": [
                ("How about we...?", ["How about we go early?", "How about we choose the cheaper one?"]),
                ("Confirm agreement", ["So we agree on Noodle House at 6:30?", "So we agree to book the earlier flight?"]),
            ],
            "pronunciation": [
                ("how about", "how-a-BOUT (link it)."),
                ("agree", "uh-GREE."),
                ("works for me", "WURKS for me."),
            ],
            "response_prompts": [
                {
                    "prompt": "Suggest a plan with How about we...",
                    "target_response": "How about we go with the cheaper one?",
                    "acceptable_variations": ["How about we go with the cheaper one?", "How about we go early?"],
                },
                {
                    "prompt": "Accept politely.",
                    "target_response": "I'm okay with that.",
                    "acceptable_variations": ["I'm okay with that.", "That works for me."],
                },
                {
                    "prompt": "Confirm agreement.",
                    "target_response": "So we agree on Noodle House at 6:30?",
                    "acceptable_variations": ["So we agree on Noodle House at 6:30?", "So we agree on option B?"],
                },
            ],
            "quiz": [
                {
                    "key": "how_about_usage",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a polite suggestion?",
                    "options": ["How about we go early?", "Go early now!", "Early go."],
                    "correct_answer": "How about we go early?",
                },
                {
                    "key": "works_for_me",
                    "type": "multiple_choice",
                    "prompt": 'What does "That works for me" mean?',
                    "options": ["oke buat aku", "aku tidak setuju", "aku tidak tahu"],
                    "correct_answer": "oke buat aku",
                },
                {
                    "key": "agree_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "agree" mean?',
                    "options": ["sepakat", "berangkat", "membandingkan"],
                    "correct_answer": "sepakat",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_preference_reach_agreement",
                "opening_line": "We need to decide. What do you suggest?",
                "learner_goal": "Suggest a plan, respond to a concern, and confirm the agreement.",
                "turns": [
                    {
                        "coach": "We need to decide. What do you suggest?",
                        "hint": "Usul dengan How about we...",
                        "sample_answer": "How about we go with the cheaper one tonight?",
                        "focus": "Make a suggestion",
                        "expected_keywords": ["how about", "cheaper"],
                    },
                    {
                        "coach": "I'm okay with that, but I'm worried it's crowded.",
                        "hint": "Tanggapi concern pakai might + so let's...",
                        "sample_answer": "It might be, so let's go early.",
                        "focus": "Respond to concern",
                        "expected_keywords": ["might", "so", "let's"],
                    },
                    {
                        "coach": "Great. Confirm the agreement.",
                        "hint": "Konfirmasi: So we agree on ...?",
                        "sample_answer": "Great. So we agree on Noodle House at 6:30?",
                        "focus": "Confirm agreement",
                        "expected_keywords": ["agree", "at"],
                    },
                ],
                "target_phrases": ["How about we ...?", "That works for me.", "So we agree on ...?"],
            },
            "reading_support": "To reach agreement, suggest a plan politely, respond to concerns, and confirm the final decision clearly.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. How about we ...?",
                "2. I'm okay with that, but ...",
                "3. It might be, so let's ...",
                "4. That works for me.",
                "5. So we agree on ...?",
            ],
            "goal_examples": ["How about we ...?", "That works for me.", "So we agree on ...?"],
        },
        {
            "lesson_key": "lesson-05-preference-discussion-mission",
            "slug": "preference-discussion-mission",
            "title": "Preference Discussion Mission",
            "conversation_situation": "mission_compare_prefer_pros_cons_agree",
            "conversation_goal": "Complete a mini conversation: compare options, explain your preference with reasons, discuss pros and cons, and reach an agreement.",
            "grammar_summary": "Combine: ... but ... / I prefer... because... / The advantage is... / One downside is... / So we agree on...?",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Misi: kamu diskusi pilihan bareng teman. Kamu bandingin opsi, jelasin preferensi dan alasan, bahas pro/kontra, lalu sepakat.",
            "dialogue": [
                ("Leo", "We have two options: eat out or cook at home."),
                ("Mina", "Eating out is easier, but it's more expensive."),
                ("Leo", "So what do you prefer?"),
                ("Mina", "I prefer cooking at home because it's cheaper."),
                ("Leo", "What are the pros and cons of cooking?"),
                ("Mina", "The advantage is it's healthier. One downside is it takes time."),
                ("Leo", "Okay. How about we cook something simple?"),
                ("Mina", "That works for me. So we agree on cooking at home?"),
            ],
            "translations": [
                ("Leo", "We have two options: eat out or cook at home.", "Kita punya dua opsi: makan di luar atau masak di rumah."),
                ("Mina", "Eating out is easier, but it's more expensive.", "Makan di luar lebih gampang, tapi lebih mahal."),
                ("Leo", "So what do you prefer?", "Jadi kamu prefer yang mana?"),
                ("Mina", "I prefer cooking at home because it's cheaper.", "Aku prefer masak di rumah karena lebih murah."),
                ("Leo", "What are the pros and cons of cooking?", "Apa pro dan kontra masak?"),
                ("Mina", "The advantage is it's healthier. One downside is it takes time.", "Kelebihannya lebih sehat. Kekurangannya makan waktu."),
                ("Leo", "Okay. How about we cook something simple?", "Oke. Gimana kalau kita masak yang simpel?"),
                ("Mina", "That works for me. So we agree on cooking at home?", "Oke buat aku. Jadi kita sepakat masak di rumah?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "Eating out is easier, but it's more expensive.",
                    "meaning_id": "Makan di luar lebih gampang, tapi lebih mahal.",
                    "usage_note": "A clear compare sentence.",
                    "common_mistake": "Do not list too many points; one contrast is enough.",
                },
                {
                    "phrase": "I prefer cooking at home because it's cheaper.",
                    "meaning_id": "Aku prefer masak di rumah karena lebih murah.",
                    "usage_note": "Preference + reason in one sentence.",
                    "common_mistake": 'Do not say "I prefer because"; include what you prefer.',
                },
                {
                    "phrase": "What are the pros and cons?",
                    "meaning_id": "Apa pro dan kontranya?",
                    "usage_note": "Ask about trade-offs.",
                    "common_mistake": 'Do not use is; use are.',
                },
                {
                    "phrase": "The advantage is it's healthier. One downside is it takes time.",
                    "meaning_id": "Kelebihannya lebih sehat. Kekurangannya makan waktu.",
                    "usage_note": "Advantage + downside short answers.",
                    "common_mistake": "Don't mix advantage and downside in one long sentence; keep two short sentences.",
                },
                {
                    "phrase": "So we agree on cooking at home?",
                    "meaning_id": "Jadi kita sepakat masak di rumah?",
                    "usage_note": "Confirm agreement clearly.",
                    "common_mistake": 'Do not skip confirmation; say the final choice clearly.',
                },
            ],
            "grammar_md": [
                (
                    "Comparison -> preference -> pros/cons -> agreement",
                    [
                        "Option A is easier, but it's more expensive.",
                        "I prefer option B because it's cheaper.",
                        "The advantage is ... One downside is ...",
                        "So we agree on ...?",
                    ],
                ),
            ],
            "pronunciation": [
                ("eating out", "EE-ting out."),
                ("healthier", "HEL-thee-er."),
                ("takes time", "TAYKS time."),
            ],
            "response_prompts": [
                {
                    "prompt": "Compare options with but.",
                    "target_response": "Eating out is easier, but it's more expensive.",
                    "acceptable_variations": [
                        "Eating out is easier, but it's more expensive.",
                        "Option A is faster, but it's more expensive.",
                    ],
                },
                {
                    "prompt": "State preference with because.",
                    "target_response": "I prefer cooking at home because it's cheaper.",
                    "acceptable_variations": ["I prefer cooking at home because it's cheaper.", "I prefer option B because it's simpler."],
                },
                {
                    "prompt": "Give one advantage and one downside.",
                    "target_response": "The advantage is it's healthier. One downside is it takes time.",
                    "acceptable_variations": [
                        "The advantage is it's healthier. One downside is it takes time.",
                        "The advantage is it's cheaper. One downside is it takes time.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "mission_flow",
                    "type": "multiple_choice",
                    "prompt": "Which flow fits a preference discussion?",
                    "options": [
                        "Compare -> preference + reason -> pros/cons -> agreement",
                        "Greeting -> goodbye",
                        "Numbers -> spelling",
                    ],
                    "correct_answer": "Compare -> preference + reason -> pros/cons -> agreement",
                },
                {
                    "key": "downside_usage",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["One downside is it takes time.", "One downside are it takes time.", "Downside is it takes time."],
                    "correct_answer": "One downside is it takes time.",
                },
                {
                    "key": "agree_question",
                    "type": "multiple_choice",
                    "prompt": "Which sentence confirms agreement?",
                    "options": ["So we agree on cooking at home?", "What time is it?", "Where are you from?"],
                    "correct_answer": "So we agree on cooking at home?",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_preference_mission",
                "opening_line": "We have two options. What do you think?",
                "learner_goal": "Compare options, explain preference, discuss pros and cons, and confirm agreement.",
                "turns": [
                    {
                        "coach": "We have two options. Compare them.",
                        "hint": "Bandingin pakai but.",
                        "sample_answer": "Option A is easier, but it's more expensive.",
                        "focus": "Compare options",
                        "expected_keywords": ["but", "more"],
                    },
                    {
                        "coach": "Okay. Which do you prefer and why?",
                        "hint": "Jawab dengan I prefer ... because ...",
                        "sample_answer": "I prefer option B because it's cheaper.",
                        "focus": "Preference with reason",
                        "expected_keywords": ["prefer", "because"],
                    },
                    {
                        "coach": "Give one advantage and one downside, then confirm agreement.",
                        "hint": "The advantage is... One downside is... So we agree on...?",
                        "sample_answer": "The advantage is it's healthier. One downside is it takes time. So we agree on option B?",
                        "focus": "Pros/cons + agreement",
                        "expected_keywords": ["advantage", "downside", "agree"],
                    },
                ],
                "target_phrases": ["Which do you prefer?", "I prefer ... because ...", "So we agree on ...?"],
            },
            "reading_support": "A good preference discussion is structured: compare options, state your preference with a reason, discuss pros and cons, and confirm the agreement.",
            "writing_support_lines": [
                "Write your mission (6 lines):",
                "1. We have two options: A or B.",
                "2. Option A is ..., but ...",
                "3. I prefer ... because ...",
                "4. The advantage is ...",
                "5. One downside is ...",
                "6. So we agree on ...?",
            ],
            "goal_examples": ["I prefer ... because ...", "The advantage is ...", "So we agree on ...?"],
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

