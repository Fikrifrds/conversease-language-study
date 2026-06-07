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

        Read it again and underline the linking words and past verbs.
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B1"
    b1_root = Path("content/curriculum/english/B1")
    units_root = b1_root / "units"
    unit_key = "unit-01-personal-stories"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-01-personal-stories
            level_code: B1
            title: Personal Stories
            main_conversation_outcome: Tell simple connected stories about personal experiences.
            status: in_production
            lessons:
              - lesson-01-setting-the-scene
              - lesson-02-telling-events-in-order
              - lesson-03-describing-feelings
              - lesson-04-asking-about-someones-story
              - lesson-05-personal-story-mission
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
            "lesson_key": "lesson-01-setting-the-scene",
            "slug": "setting-the-scene",
            "title": "Setting the Scene",
            "conversation_situation": "telling_a_short_story_setting",
            "conversation_goal": "Set the scene for a short story (when, where, who) before telling what happened.",
            "grammar_summary": 'Use time and place phrases (last weekend, at the beach) and past \"be\" (I was, we were) to set the scene.',
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu cerita pengalaman singkat. Kamu jelaskan kapan, di mana, dan sama siapa dulu sebelum cerita inti.",
            "dialogue": [
                ("Mina", "You look happy today. What happened?"),
                ("Leo", "Last weekend, I was in Bandung with my cousin."),
                ("Mina", "Oh nice. What were you doing there?"),
                ("Leo", "We were visiting my aunt and exploring the city."),
                ("Mina", "How was the place?"),
                ("Leo", "It was cooler than Jakarta, and the food was great."),
                ("Mina", "Sounds like a good trip."),
            ],
            "translations": [
                ("Mina", "You look happy today. What happened?", "Kamu kelihatan senang hari ini. Ada apa?"),
                ("Leo", "Last weekend, I was in Bandung with my cousin.", "Weekend kemarin aku ada di Bandung sama sepupuku."),
                ("Mina", "Oh nice. What were you doing there?", "Wah asik. Kamu ngapain di sana?"),
                ("Leo", "We were visiting my aunt and exploring the city.", "Kami nengok tanteku dan jalan-jalan di kota."),
                ("Mina", "How was the place?", "Gimana tempatnya?"),
                ("Leo", "It was cooler than Jakarta, and the food was great.", "Lebih sejuk dari Jakarta, dan makanannya enak banget."),
                ("Mina", "Sounds like a good trip.", "Kedengarannya trip-nya enak."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Last weekend, I was in Bandung.",
                    "meaning_id": "Weekend kemarin aku ada di Bandung.",
                    "usage_note": "A clear way to set time and place.",
                    "common_mistake": 'Do not say "In last weekend".',
                },
                {
                    "phrase": "I was there with my cousin.",
                    "meaning_id": "Aku di sana sama sepupuku.",
                    "usage_note": "Add who you were with.",
                    "common_mistake": "Keep it simple and clear.",
                },
                {
                    "phrase": "We were visiting my aunt.",
                    "meaning_id": "Kami nengok tanteku.",
                    "usage_note": "Past continuous for background activities.",
                    "common_mistake": 'Do not say "We was visiting"; use were.',
                },
                {
                    "phrase": "How was the place?",
                    "meaning_id": "Gimana tempatnya?",
                    "usage_note": "A natural follow-up question.",
                    "common_mistake": 'Do not say "How the place was?".',
                },
                {
                    "phrase": "It was cooler than Jakarta.",
                    "meaning_id": "Lebih sejuk dari Jakarta.",
                    "usage_note": "Use comparative adjective + than.",
                    "common_mistake": 'Do not say "more cool" here.',
                },
            ],
            "grammar_md": [
                ("Setting time and place", ["Last weekend, I was in Bandung.", "Yesterday afternoon, we were at the station."]),
                ("Past be (was / were)", ["I was with my cousin.", "We were visiting my aunt."]),
            ],
            "pronunciation": [
                ("last weekend", "Link it: last-WEEK-end."),
                ("were visiting", "wer-VI-zi-ting."),
                ("cooler than", "KOO-ler than."),
            ],
            "response_prompts": [
                {
                    "prompt": "Set the scene: last weekend + Bandung.",
                    "target_response": "Last weekend, I was in Bandung.",
                    "acceptable_variations": ["Last weekend, I was in Bandung.", "I was in Bandung last weekend."],
                },
                {
                    "prompt": "Add who you were with.",
                    "target_response": "I was there with my cousin.",
                    "acceptable_variations": ["I was there with my cousin.", "I went with my cousin."],
                },
                {
                    "prompt": "Describe the place with a comparison.",
                    "target_response": "It was cooler than Jakarta.",
                    "acceptable_variations": ["It was cooler than Jakarta.", "It was quieter than Jakarta."],
                },
            ],
            "quiz": [
                {
                    "key": "past_be",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["We was in Bandung.", "We were in Bandung.", "We are in Bandung yesterday."],
                    "correct_answer": "We were in Bandung.",
                },
                {
                    "key": "meaning_scene",
                    "type": "multiple_choice",
                    "prompt": 'What does "set the scene" mean in a story?',
                    "options": ["jelaskan kapan/di mana", "beri hadiah", "tanya harga"],
                    "correct_answer": "jelaskan kapan/di mana",
                },
                {
                    "key": "comparative",
                    "type": "multiple_choice",
                    "prompt": "Which is a comparative sentence?",
                    "options": ["It was cooler than Jakarta.", "It is cool.", "It was the coolest."],
                    "correct_answer": "It was cooler than Jakarta.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_story_setting_scene",
                "opening_line": "You look happy today. What happened?",
                "learner_goal": "Set the scene with time, place, and who you were with, then add one background activity.",
                "turns": [
                    {
                        "coach": "You look happy today. What happened?",
                        "hint": "Mulai dengan kapan + di mana.",
                        "sample_answer": "Last weekend, I was in Bandung.",
                        "focus": "Set time and place",
                        "expected_keywords": ["last", "was", "in"],
                    },
                    {
                        "coach": "Oh nice. Who were you with?",
                        "hint": "Jawab dengan with + person.",
                        "sample_answer": "I was there with my cousin.",
                        "focus": "Say who you were with",
                        "expected_keywords": ["with", "cousin"],
                    },
                    {
                        "coach": "What were you doing there?",
                        "hint": "Tambah 1 aktivitas background.",
                        "sample_answer": "We were visiting my aunt and exploring the city.",
                        "focus": "Add background activity",
                        "expected_keywords": ["were", "visiting"],
                    },
                ],
                "target_phrases": ["Last weekend, I was...", "I was there with...", "We were ...ing"],
            },
            "reading_support": "Leo sets the scene for his story: last weekend in Bandung with his cousin. He describes the place and what they were doing.",
            "writing_support_lines": [
                "Write 4 connected sentences:",
                "1. Time: Last weekend, ...",
                "2. Place: I was in ...",
                "3. Who: I was with ...",
                "4. Background: We were ...ing",
            ],
            "goal_examples": [
                "Last weekend, I was in Bandung with my cousin.",
                "We were visiting my aunt.",
                "It was cooler than Jakarta.",
            ],
        },
        {
            "lesson_key": "lesson-02-telling-events-in-order",
            "slug": "telling-events-in-order",
            "title": "Telling Events in Order",
            "conversation_situation": "telling_events_in_order",
            "conversation_goal": "Tell story events in order using simple linking words (first, then, after that, finally).",
            "grammar_summary": "Use linking words (first, then, after that, finally) to connect past events clearly.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu cerita kejadian berurutan. Kamu pakai first/then/after that/finally supaya jelas.",
            "dialogue": [
                ("Mina", "So what did you do on your trip?"),
                ("Leo", "First, we checked in at the hotel."),
                ("Mina", "Okay. Then what?"),
                ("Leo", "Then we walked around and tried street food."),
                ("Mina", "Nice. What happened after that?"),
                ("Leo", "After that, we met my aunt for dinner."),
                ("Mina", "And finally?"),
                ("Leo", "Finally, we went back early because we were tired."),
            ],
            "translations": [
                ("Mina", "So what did you do on your trip?", "Terus kamu ngapain pas trip?"),
                ("Leo", "First, we checked in at the hotel.", "Pertama, kami check-in di hotel."),
                ("Mina", "Okay. Then what?", "Oke. Terus?"),
                ("Leo", "Then we walked around and tried street food.", "Lalu kami jalan-jalan dan coba street food."),
                ("Mina", "Nice. What happened after that?", "Asik. Setelah itu apa yang terjadi?"),
                ("Leo", "After that, we met my aunt for dinner.", "Setelah itu, kami ketemu tanteku buat makan malam."),
                ("Mina", "And finally?", "Terus terakhir?"),
                ("Leo", "Finally, we went back early because we were tired.", "Terakhir, kami pulang lebih cepat karena capek."),
            ],
            "useful_phrases": [
                {
                    "phrase": "First, we checked in at the hotel.",
                    "meaning_id": "Pertama, kami check-in di hotel.",
                    "usage_note": "Start a sequence clearly.",
                    "common_mistake": "Do not skip the subject; say who did it.",
                },
                {
                    "phrase": "Then we walked around.",
                    "meaning_id": "Lalu kami jalan-jalan.",
                    "usage_note": "Then continues the sequence.",
                    "common_mistake": "Do not overuse then; mix with after that.",
                },
                {
                    "phrase": "What happened after that?",
                    "meaning_id": "Setelah itu apa yang terjadi?",
                    "usage_note": "Ask for the next event.",
                    "common_mistake": 'Do not say "What happen"; use happened.',
                },
                {
                    "phrase": "After that, we met my aunt for dinner.",
                    "meaning_id": "Setelah itu, kami ketemu tanteku buat makan malam.",
                    "usage_note": "After that is natural for stories.",
                    "common_mistake": 'Do not say "After that we meet"; use met.',
                },
                {
                    "phrase": "Finally, we went back early.",
                    "meaning_id": "Terakhir, kami pulang lebih cepat.",
                    "usage_note": "Finally ends the story sequence.",
                    "common_mistake": "Do not use finally for the middle of the story.",
                },
            ],
            "grammar_md": [
                ("Linking words for sequence", ["First, ...", "Then, ...", "After that, ...", "Finally, ..."]),
                ("Past verbs in stories", ["We checked in.", "We walked around.", "We met my aunt.", "We went back."]),
            ],
            "pronunciation": [
                ("after that", "AF-ter that."),
                ("finally", "FINE-uh-lee."),
                ("checked in", "CHECKT in."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start with first (check in).",
                    "target_response": "First, we checked in at the hotel.",
                    "acceptable_variations": ["First, we checked in at the hotel.", "First, we checked in."],
                },
                {
                    "prompt": "Ask: What happened after that?",
                    "target_response": "What happened after that?",
                    "acceptable_variations": ["What happened after that?", "What happened next?"],
                },
                {
                    "prompt": "End with finally (went back).",
                    "target_response": "Finally, we went back early.",
                    "acceptable_variations": ["Finally, we went back early.", "Finally, we went home early."],
                },
            ],
            "quiz": [
                {
                    "key": "sequence_word",
                    "type": "multiple_choice",
                    "prompt": "Which word usually ends a sequence?",
                    "options": ["first", "finally", "then"],
                    "correct_answer": "finally",
                },
                {
                    "key": "past_met",
                    "type": "multiple_choice",
                    "prompt": 'What is the past of "meet"?',
                    "options": ["meeted", "met", "meet"],
                    "correct_answer": "met",
                },
                {
                    "key": "meaning_after_that",
                    "type": "multiple_choice",
                    "prompt": 'What does "after that" mean?',
                    "options": ["setelah itu", "sebelum itu", "hari ini"],
                    "correct_answer": "setelah itu",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_story_events_in_order",
                "opening_line": "So what did you do on your trip?",
                "learner_goal": "Tell 3 events in order using first/then/after that/finally.",
                "turns": [
                    {
                        "coach": "So what did you do on your trip?",
                        "hint": "Mulai dengan first.",
                        "sample_answer": "First, we checked in at the hotel.",
                        "focus": "Start the sequence",
                        "expected_keywords": ["first"],
                    },
                    {
                        "coach": "Nice. What did you do next?",
                        "hint": "Gunakan then atau after that.",
                        "sample_answer": "Then we walked around and tried street food.",
                        "focus": "Continue the sequence",
                        "expected_keywords": ["then"],
                    },
                    {
                        "coach": "And finally?",
                        "hint": "Tutup dengan finally + reason singkat.",
                        "sample_answer": "Finally, we went back early because we were tired.",
                        "focus": "End the sequence",
                        "expected_keywords": ["finally", "because"],
                    },
                ],
                "target_phrases": ["First, ...", "After that, ...", "Finally, ..."],
            },
            "reading_support": "Leo tells his trip in order using linking words: first, then, after that, and finally.",
            "writing_support_lines": [
                "Write a short sequence (4 sentences):",
                "1. First, ...",
                "2. Then, ...",
                "3. After that, ...",
                "4. Finally, ...",
            ],
            "goal_examples": [
                "First, we checked in at the hotel.",
                "What happened after that?",
                "Finally, we went back early.",
            ],
        },
        {
            "lesson_key": "lesson-03-describing-feelings",
            "slug": "describing-feelings",
            "title": "Describing Feelings",
            "conversation_situation": "describing_feelings_in_a_story",
            "conversation_goal": "Describe how you felt during a story using feeling adjectives.",
            "grammar_summary": "Use I felt + adjective and I was + adjective to describe feelings in past situations.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu cerita pengalaman dan jelaskan perasaan kamu (nervous, excited, relieved).",
            "dialogue": [
                ("Mina", "How did you feel during the trip?"),
                ("Leo", "At first, I felt nervous because we got lost."),
                ("Mina", "Oh no. What did you do?"),
                ("Leo", "We asked for directions, and I felt relieved."),
                ("Mina", "Good. Were you excited too?"),
                ("Leo", "Yes. I was excited when we found a great food place."),
                ("Mina", "That sounds fun."),
            ],
            "translations": [
                ("Mina", "How did you feel during the trip?", "Gimana perasaanmu selama trip itu?"),
                ("Leo", "At first, I felt nervous because we got lost.", "Awalnya aku gugup karena kami tersesat."),
                ("Mina", "Oh no. What did you do?", "Aduh. Kamu ngapain?"),
                ("Leo", "We asked for directions, and I felt relieved.", "Kami tanya arah, dan aku lega."),
                ("Mina", "Good. Were you excited too?", "Oke. Kamu juga excited?"),
                ("Leo", "Yes. I was excited when we found a great food place.", "Iya. Aku excited waktu nemu tempat makan enak."),
                ("Mina", "That sounds fun.", "Kedengarannya seru."),
            ],
            "useful_phrases": [
                {
                    "phrase": "How did you feel?",
                    "meaning_id": "Gimana perasaanmu?",
                    "usage_note": "Ask about feelings in the past.",
                    "common_mistake": 'Do not say "How you feel" for past.',
                },
                {
                    "phrase": "I felt nervous.",
                    "meaning_id": "Aku gugup.",
                    "usage_note": "Use felt for past feelings.",
                    "common_mistake": 'Do not say "I feel nervous" for yesterday.',
                },
                {
                    "phrase": "I felt relieved.",
                    "meaning_id": "Aku lega.",
                    "usage_note": "Relieved is common after a problem ends.",
                    "common_mistake": 'Do not say "I am relieved" if you want past story.',
                },
                {
                    "phrase": "I was excited when...",
                    "meaning_id": "Aku excited waktu...",
                    "usage_note": "Use was excited + when for story moments.",
                    "common_mistake": 'Do not say "I excited" without was.',
                },
                {
                    "phrase": "We got lost.",
                    "meaning_id": "Kami tersesat.",
                    "usage_note": "A common travel problem phrase.",
                    "common_mistake": 'Do not say "We lost" for getting lost.',
                },
            ],
            "grammar_md": [
                ("I felt + adjective", ["I felt nervous.", "I felt relieved."]),
                ("I was + adjective", ["I was excited.", "I was worried."]),
            ],
            "pronunciation": [
                ("nervous", "NER-vus."),
                ("relieved", "ri-LEEVd."),
                ("excited", "ik-SAI-ted."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask about feelings in the past.",
                    "target_response": "How did you feel?",
                    "acceptable_variations": ["How did you feel?", "How did you feel during the trip?"],
                },
                {
                    "prompt": "Say you felt nervous because you got lost.",
                    "target_response": "I felt nervous because we got lost.",
                    "acceptable_variations": ["I felt nervous because we got lost.", "I felt nervous because I got lost."],
                },
                {
                    "prompt": "Say you felt relieved after asking for directions.",
                    "target_response": "I felt relieved after we asked for directions.",
                    "acceptable_variations": ["I felt relieved after we asked for directions.", "I felt relieved after that."],
                },
            ],
            "quiz": [
                {
                    "key": "felt_past",
                    "type": "multiple_choice",
                    "prompt": "Choose the best past sentence.",
                    "options": ["I feel nervous yesterday.", "I felt nervous yesterday.", "I am feel nervous yesterday."],
                    "correct_answer": "I felt nervous yesterday.",
                },
                {
                    "key": "meaning_relieved",
                    "type": "multiple_choice",
                    "prompt": 'What does "relieved" mean?',
                    "options": ["lega", "marah", "bosan"],
                    "correct_answer": "lega",
                },
                {
                    "key": "ask_feeling",
                    "type": "multiple_choice",
                    "prompt": "Which question asks about feelings in the past?",
                    "options": ["How do you feel?", "How did you feel?", "How you feel?"],
                    "correct_answer": "How did you feel?",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_story_feelings",
                "opening_line": "How did you feel when that happened?",
                "learner_goal": "Describe a negative feeling, then a positive feeling after solving the problem.",
                "turns": [
                    {
                        "coach": "How did you feel when that happened?",
                        "hint": "Sebutkan perasaan + sebab singkat.",
                        "sample_answer": "I felt nervous because we got lost.",
                        "focus": "Describe feeling with reason",
                        "expected_keywords": ["felt", "because"],
                    },
                    {
                        "coach": "What did you do next?",
                        "hint": "Sebutkan solusi singkat.",
                        "sample_answer": "We asked for directions.",
                        "focus": "Describe an action",
                        "expected_keywords": ["asked"],
                    },
                    {
                        "coach": "And how did you feel after that?",
                        "hint": "Sebutkan perasaan setelahnya.",
                        "sample_answer": "I felt relieved after that.",
                        "focus": "Describe feeling after",
                        "expected_keywords": ["relieved"],
                    },
                ],
                "target_phrases": ["I felt nervous because...", "We asked for directions.", "I felt relieved."],
            },
            "reading_support": "Leo describes his feelings in the story. He felt nervous when they got lost, and relieved after they asked for directions.",
            "writing_support_lines": [
                "Write 4 connected sentences:",
                "1. At first, I felt ... because ...",
                "2. Then we ...",
                "3. After that, I felt ...",
                "4. Finally, I was ...",
            ],
            "goal_examples": ["How did you feel?", "I felt nervous because we got lost.", "I felt relieved after that."],
        },
        {
            "lesson_key": "lesson-04-asking-about-someones-story",
            "slug": "asking-about-someones-story",
            "title": "Asking About Someone's Story",
            "conversation_situation": "asking_follow_up_questions_about_a_story",
            "conversation_goal": "Ask follow-up questions to keep someone's story going (next event, reason, feelings).",
            "grammar_summary": "Use follow-up questions in the past: What happened next? Why did you...? How did you feel?",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu dengar cerita teman. Kamu tanya follow-up: next, alasan, dan perasaan.",
            "dialogue": [
                ("Mina", "So you got lost. What happened next?"),
                ("Leo", "We asked a local person for help."),
                ("Mina", "Why did you choose that route?"),
                ("Leo", "Because my cousin thought it was faster."),
                ("Mina", "How did you feel at that moment?"),
                ("Leo", "I felt worried, but then I felt relieved."),
                ("Mina", "I'm glad it worked out."),
            ],
            "translations": [
                ("Mina", "So you got lost. What happened next?", "Jadi kamu tersesat. Terus apa yang terjadi?"),
                ("Leo", "We asked a local person for help.", "Kami tanya orang lokal buat bantuan."),
                ("Mina", "Why did you choose that route?", "Kenapa kamu pilih jalan itu?"),
                ("Leo", "Because my cousin thought it was faster.", "Karena sepupuku pikir itu lebih cepat."),
                ("Mina", "How did you feel at that moment?", "Gimana perasaanmu saat itu?"),
                ("Leo", "I felt worried, but then I felt relieved.", "Aku khawatir, tapi lalu lega."),
                ("Mina", "I'm glad it worked out.", "Syukurlah akhirnya beres."),
            ],
            "useful_phrases": [
                {
                    "phrase": "What happened next?",
                    "meaning_id": "Terus apa yang terjadi?",
                    "usage_note": "A strong follow-up question.",
                    "common_mistake": "Use next/after that for clarity.",
                },
                {
                    "phrase": "Why did you choose that route?",
                    "meaning_id": "Kenapa kamu pilih jalan itu?",
                    "usage_note": "Ask for the reason in the past.",
                    "common_mistake": 'Do not say "Why you chose" in a simple question; use did.',
                },
                {
                    "phrase": "How did you feel at that moment?",
                    "meaning_id": "Gimana perasaanmu saat itu?",
                    "usage_note": "Ask about feelings in the story.",
                    "common_mistake": 'Do not say "How you felt"; use did you feel.',
                },
                {
                    "phrase": "We asked a local person for help.",
                    "meaning_id": "Kami tanya orang lokal buat bantuan.",
                    "usage_note": "A simple action in the past.",
                    "common_mistake": 'Do not say "We ask" in a past story.',
                },
                {
                    "phrase": "I'm glad it worked out.",
                    "meaning_id": "Syukurlah akhirnya beres.",
                    "usage_note": "A natural supportive reaction.",
                    "common_mistake": 'Do not say "I am happy it finish".',
                },
            ],
            "grammar_md": [
                ("Follow-up questions", ["What happened next?", "Why did you do that?", "How did you feel?"]),
                ("Past question with did", ["Why did you choose that route?", "Why did you go there?"]),
            ],
            "pronunciation": [
                ("happened", "HAP-end."),
                ("route", "ROOT."),
                ("worked out", "WORKT out."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask: What happened next?",
                    "target_response": "What happened next?",
                    "acceptable_variations": ["What happened next?", "What happened after that?"],
                },
                {
                    "prompt": "Ask: Why did you choose that route?",
                    "target_response": "Why did you choose that route?",
                    "acceptable_variations": ["Why did you choose that route?", "Why did you choose that one?"],
                },
                {
                    "prompt": "Ask about feelings: How did you feel?",
                    "target_response": "How did you feel?",
                    "acceptable_variations": ["How did you feel?", "How did you feel at that moment?"],
                },
            ],
            "quiz": [
                {
                    "key": "follow_up_next",
                    "type": "multiple_choice",
                    "prompt": "Which question asks about the next event?",
                    "options": ["What happened next?", "How was it?", "Do you like it?"],
                    "correct_answer": "What happened next?",
                },
                {
                    "key": "why_did",
                    "type": "multiple_choice",
                    "prompt": "Which question is correct?",
                    "options": ["Why you did that?", "Why did you do that?", "Why did you did that?"],
                    "correct_answer": "Why did you do that?",
                },
                {
                    "key": "meaning_worked_out",
                    "type": "multiple_choice",
                    "prompt": 'What does "It worked out" mean?',
                    "options": ["akhirnya beres", "mulai lagi", "hilang"],
                    "correct_answer": "akhirnya beres",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_story_ask_followups",
                "opening_line": "So you got lost. What happened next?",
                "learner_goal": "Ask 3 follow-up questions to keep a story going: next event, reason, and feeling.",
                "turns": [
                    {
                        "coach": "So you got lost. What happened next?",
                        "hint": "Jawab dengan 1 aksi di masa lalu.",
                        "sample_answer": "We asked a local person for help.",
                        "focus": "Continue the story",
                        "expected_keywords": ["asked", "help"],
                    },
                    {
                        "coach": "Why did you do that?",
                        "hint": "Jawab dengan because + reason.",
                        "sample_answer": "Because we did not want to waste time.",
                        "focus": "Give a reason",
                        "expected_keywords": ["because"],
                    },
                    {
                        "coach": "How did you feel at that moment?",
                        "hint": "Sebutkan perasaan (felt...).",
                        "sample_answer": "I felt worried, but then I felt relieved.",
                        "focus": "Describe feelings",
                        "expected_keywords": ["felt", "but"],
                    },
                ],
                "target_phrases": ["What happened next?", "Why did you...?", "How did you feel?"],
            },
            "reading_support": "Mina keeps Leo's story going with follow-up questions: what happened next, why he chose something, and how he felt.",
            "writing_support_lines": [
                "Write 4 follow-up questions:",
                "1. What happened next?",
                "2. Why did you ...?",
                "3. How did you feel?",
                "4. What did you do after that?",
            ],
            "goal_examples": ["What happened next?", "Why did you choose that route?", "How did you feel at that moment?"],
        },
        {
            "lesson_key": "lesson-05-personal-story-mission",
            "slug": "personal-story-mission",
            "title": "Personal Story Mission",
            "conversation_situation": "mission_tell_a_connected_personal_story",
            "conversation_goal": "Tell a connected personal story with a clear scene, ordered events, and feelings, then answer a follow-up question.",
            "grammar_summary": "Combine scene setting + sequence words + feelings to tell a connected story (4 to 6 sentences).",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Misi: kamu cerita pengalaman kemarin. Kamu set the scene, urutkan kejadian, jelaskan perasaan, lalu jawab follow-up.",
            "dialogue": [
                ("Mina", "Tell me about something interesting that happened recently."),
                ("Leo", "Last weekend, I was in Bandung with my cousin."),
                ("Mina", "Okay. What happened?"),
                ("Leo", "First, we explored the city. Then we got lost for a while."),
                ("Mina", "Oh no. How did you feel?"),
                ("Leo", "I felt nervous, but after we asked for directions, I felt relieved."),
                ("Mina", "What happened next?"),
                ("Leo", "Finally, we found a great place to eat and ended the day happily."),
            ],
            "translations": [
                ("Mina", "Tell me about something interesting that happened recently.", "Ceritain sesuatu yang menarik yang baru terjadi akhir-akhir ini."),
                ("Leo", "Last weekend, I was in Bandung with my cousin.", "Weekend kemarin aku ada di Bandung sama sepupuku."),
                ("Mina", "Okay. What happened?", "Oke. Terus apa yang terjadi?"),
                ("Leo", "First, we explored the city. Then we got lost for a while.", "Pertama, kami jalan-jalan di kota. Lalu kami sempat tersesat."),
                ("Mina", "Oh no. How did you feel?", "Aduh. Gimana perasaanmu?"),
                ("Leo", "I felt nervous, but after we asked for directions, I felt relieved.", "Aku gugup, tapi setelah tanya arah, aku lega."),
                ("Mina", "What happened next?", "Terus apa yang terjadi?"),
                ("Leo", "Finally, we found a great place to eat and ended the day happily.", "Terakhir, kami nemu tempat makan enak dan menutup hari dengan senang."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Tell me about something interesting that happened recently.",
                    "meaning_id": "Ceritain sesuatu yang menarik yang baru terjadi.",
                    "usage_note": "A natural mission starter request.",
                    "common_mistake": "Keep it short and clear.",
                },
                {
                    "phrase": "First, we explored the city.",
                    "meaning_id": "Pertama, kami jalan-jalan di kota.",
                    "usage_note": "A clear first event.",
                    "common_mistake": "Do not forget the subject (we/I).",
                },
                {
                    "phrase": "Then we got lost for a while.",
                    "meaning_id": "Lalu kami sempat tersesat.",
                    "usage_note": "A simple problem event.",
                    "common_mistake": 'Do not say "Then we lost".',
                },
                {
                    "phrase": "I felt nervous, but then I felt relieved.",
                    "meaning_id": "Aku gugup, tapi lalu lega.",
                    "usage_note": "Contrast feelings with but.",
                    "common_mistake": "Do not mix present and past in one story.",
                },
                {
                    "phrase": "What happened next?",
                    "meaning_id": "Terus apa yang terjadi?",
                    "usage_note": "A follow-up question.",
                    "common_mistake": 'Do not say "What happen next".',
                },
            ],
            "grammar_md": [
                (
                    "Connected story pattern",
                    [
                        "Last weekend, I was in ...",
                        "First, ... Then ... After that ... Finally, ...",
                        "I felt ... because ...",
                    ],
                )
            ],
            "pronunciation": [
                ("interesting", "IN-tres-ting."),
                ("explored", "ik-SPLORD."),
                ("ended", "EN-did."),
            ],
            "response_prompts": [
                {
                    "prompt": "Start a connected story with time and place.",
                    "target_response": "Last weekend, I was in Bandung with my cousin.",
                    "acceptable_variations": ["Last weekend, I was in Bandung with my cousin.", "Last weekend, I was in Bandung."],
                },
                {
                    "prompt": "Tell two events with first/then.",
                    "target_response": "First, we explored the city. Then we got lost for a while.",
                    "acceptable_variations": [
                        "First, we explored the city. Then we got lost for a while.",
                        "First, we explored the city. Then we went to a cafe.",
                    ],
                },
                {
                    "prompt": "Describe feelings with contrast.",
                    "target_response": "I felt nervous, but after that I felt relieved.",
                    "acceptable_variations": ["I felt nervous, but after that I felt relieved.", "I felt worried, but then I felt relieved."],
                },
            ],
            "quiz": [
                {
                    "key": "connected_story",
                    "type": "multiple_choice",
                    "prompt": "Which option is a connected story?",
                    "options": [
                        "Last weekend, I was in Bandung. First, we explored the city. Then we got lost.",
                        "Bandung. Explore. Lost.",
                        "I am in Bandung now.",
                    ],
                    "correct_answer": "Last weekend, I was in Bandung. First, we explored the city. Then we got lost.",
                },
                {
                    "key": "follow_up_q",
                    "type": "multiple_choice",
                    "prompt": "Which is a follow-up question?",
                    "options": ["What happened next?", "I felt nervous.", "It was great."],
                    "correct_answer": "What happened next?",
                },
                {
                    "key": "felt_vs_feel",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct past sentence.",
                    "options": ["I feel relieved after that.", "I felt relieved after that.", "I am felt relieved."],
                    "correct_answer": "I felt relieved after that.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_story_mission",
                "opening_line": "Tell me about something interesting that happened recently.",
                "learner_goal": "Tell a connected story (4 to 6 sentences) and answer one follow-up question.",
                "turns": [
                    {
                        "coach": "Tell me about something interesting that happened recently.",
                        "hint": "Mulai dengan scene: time + place + who.",
                        "sample_answer": "Last weekend, I was in Bandung with my cousin.",
                        "focus": "Start with scene",
                        "expected_keywords": ["last", "was", "with"],
                    },
                    {
                        "coach": "What happened?",
                        "hint": "Ceritakan 2 event pakai first/then.",
                        "sample_answer": "First, we explored the city. Then we got lost for a while.",
                        "focus": "Tell events in order",
                        "expected_keywords": ["first", "then"],
                    },
                    {
                        "coach": "How did you feel?",
                        "hint": "Sebutkan feeling + contrast (but).",
                        "sample_answer": "I felt nervous, but after we asked for directions, I felt relieved.",
                        "focus": "Describe feelings",
                        "expected_keywords": ["felt", "but", "relieved"],
                    },
                ],
                "target_phrases": ["Last weekend, I was...", "First..., then...", "I felt... but..."],
            },
            "reading_support": "A connected personal story has a clear scene, ordered events, and feelings. It also includes one follow-up question and answer.",
            "writing_support_lines": [
                "Write your mission (5 sentences):",
                "1. Time + place",
                "2. Who you were with",
                "3. First, ...",
                "4. Then, ...",
                "5. I felt ... but ...",
            ],
            "goal_examples": ["Last weekend, I was in ...", "First..., then...", "I felt ... but ..."],
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

