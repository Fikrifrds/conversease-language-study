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
            "- Tone: friendly, clear, respectful",
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

        Read it again and underline the community/culture words (neighborhood, tradition, usually, in my country).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B1"
    b1_root = Path("content/curriculum/english/B1")
    units_root = b1_root / "units"
    unit_key = "unit-07-community-and-culture"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-07-community-and-culture
            level_code: B1
            title: Community & Culture
            main_conversation_outcome: Discuss community, habits, and cultural differences politely.
            status: in_production
            lessons:
              - lesson-01-describing-your-community
              - lesson-02-talking-about-local-habits
              - lesson-03-asking-about-culture
              - lesson-04-being-polite-with-differences
              - lesson-05-community-culture-mission
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
            "lesson_key": "lesson-01-describing-your-community",
            "slug": "describing-your-community",
            "title": "Describing Your Community",
            "conversation_situation": "describing_neighborhood",
            "conversation_goal": "Describe your neighborhood, mention what you like, and invite a follow-up question.",
            "grammar_summary": "Use It's a... neighborhood / It's known for... / I like it because... to describe your community clearly.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu ngobrol sama teman baru. Kamu jelasin lingkungan tempat kamu tinggal, apa yang kamu suka, dan tanya balik.",
            "dialogue": [
                ("Leo", "So, where do you live?"),
                ("Mina", "I live in a quiet neighborhood near the city center."),
                ("Leo", "Nice. What's it like?"),
                ("Mina", "It's known for its food stalls and small parks."),
                ("Leo", "Sounds great. What do you like about it?"),
                ("Mina", "I like it because it's convenient but still peaceful."),
                ("Leo", "Do you know your neighbors?"),
                ("Mina", "Yeah, we say hi and help each other sometimes."),
            ],
            "translations": [
                ("Leo", "So, where do you live?", "Jadi, kamu tinggal di mana?"),
                ("Mina", "I live in a quiet neighborhood near the city center.", "Aku tinggal di lingkungan yang tenang dekat pusat kota."),
                ("Leo", "Nice. What's it like?", "Oke. Suasananya gimana?"),
                ("Mina", "It's known for its food stalls and small parks.", "Terkenal dengan warung makan dan taman kecil."),
                ("Leo", "Sounds great. What do you like about it?", "Kedengarannya enak. Kamu suka apa dari sana?"),
                ("Mina", "I like it because it's convenient but still peaceful.", "Aku suka karena praktis tapi tetap tenang."),
                ("Leo", "Do you know your neighbors?", "Kamu kenal tetangga kamu?"),
                ("Mina", "Yeah, we say hi and help each other sometimes.", "Iya, kita saling sapa dan kadang saling bantu."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I live in a quiet neighborhood.",
                    "meaning_id": "Aku tinggal di lingkungan yang tenang.",
                    "usage_note": "A simple neighborhood description.",
                    "common_mistake": 'Do not say "I live at neighborhood"; use in a neighborhood.',
                },
                {
                    "phrase": "It's known for its food stalls.",
                    "meaning_id": "Terkenal dengan warung makan.",
                    "usage_note": "Known for describes what a place is famous for.",
                    "common_mistake": 'Do not say "known about" for this meaning; use known for.',
                },
                {
                    "phrase": "I like it because it's convenient.",
                    "meaning_id": "Aku suka karena praktis.",
                    "usage_note": "A clear reason sentence.",
                    "common_mistake": 'Do not say "because convenient" without it\'s.',
                },
                {
                    "phrase": "It's convenient but still peaceful.",
                    "meaning_id": "Praktis tapi tetap tenang.",
                    "usage_note": "A nice contrast sentence.",
                    "common_mistake": 'Do not drop still if you want the contrast; keep it.',
                },
                {
                    "phrase": "We help each other sometimes.",
                    "meaning_id": "Kita kadang saling bantu.",
                    "usage_note": "A simple community habit sentence.",
                    "common_mistake": 'Do not say "we helping"; use help.',
                },
            ],
            "grammar_md": [
                ("Known for", ["It's known for its food stalls.", "It's known for its beaches."]),
                ("Because + reason", ["I like it because it's convenient.", "I like it because it's quiet."]),
            ],
            "pronunciation": [
                ("neighborhood", "NAY-bur-hood."),
                ("convenient", "kun-VEE-nee-ent."),
                ("peaceful", "PEES-ful."),
            ],
            "response_prompts": [
                {
                    "prompt": "Describe your neighborhood.",
                    "target_response": "I live in a quiet neighborhood.",
                    "acceptable_variations": ["I live in a quiet neighborhood.", "I live in a busy neighborhood."],
                },
                {
                    "prompt": "Say what it's known for.",
                    "target_response": "It's known for its food stalls.",
                    "acceptable_variations": ["It's known for its food stalls.", "It's known for its parks."],
                },
                {
                    "prompt": "Say what you like and why.",
                    "target_response": "I like it because it's convenient but still peaceful.",
                    "acceptable_variations": [
                        "I like it because it's convenient but still peaceful.",
                        "I like it because it's quiet and friendly.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "known_for",
                    "type": "multiple_choice",
                    "prompt": 'Which phrase means "terkenal dengan"?',
                    "options": ["known for", "known from", "known about"],
                    "correct_answer": "known for",
                },
                {
                    "key": "neighborhood_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "neighborhood" mean?',
                    "options": ["lingkungan", "tiket", "kantor"],
                    "correct_answer": "lingkungan",
                },
                {
                    "key": "because_usage",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["I like it because it's convenient.", "I like it because convenient.", "I like because it's convenient."],
                    "correct_answer": "I like it because it's convenient.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_culture_describe_community",
                "opening_line": "What's your neighborhood like?",
                "learner_goal": "Describe your neighborhood and say what you like about it with a reason.",
                "turns": [
                    {
                        "coach": "What's your neighborhood like?",
                        "hint": "Mulai dengan I live in ... neighborhood.",
                        "sample_answer": "I live in a quiet neighborhood near the city center.",
                        "focus": "Describe neighborhood",
                        "expected_keywords": ["neighborhood"],
                    },
                    {
                        "coach": "What is it known for?",
                        "hint": "Jawab dengan It's known for ...",
                        "sample_answer": "It's known for its food stalls and small parks.",
                        "focus": "Say what it's known for",
                        "expected_keywords": ["known for"],
                    },
                    {
                        "coach": "What do you like about it?",
                        "hint": "Jawab dengan because + reason.",
                        "sample_answer": "I like it because it's convenient but still peaceful.",
                        "focus": "Give a reason",
                        "expected_keywords": ["because", "convenient"],
                    },
                ],
                "target_phrases": ["I live in ...", "It's known for ...", "I like it because ..."],
            },
            "reading_support": "To describe your community, talk about the neighborhood, what it's known for, and one thing you like with a reason.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. I live in a ... neighborhood.",
                "2. It's known for ...",
                "3. I like it because ...",
                "4. It's ... but still ...",
                "5. People here ...",
            ],
            "goal_examples": ["I live in a ... neighborhood.", "It's known for ...", "I like it because ..."],
        },
        {
            "lesson_key": "lesson-02-talking-about-local-habits",
            "slug": "talking-about-local-habits",
            "title": "Talking About Local Habits",
            "conversation_situation": "talking_about_local_habits",
            "conversation_goal": "Describe a local habit, say how often it happens, and give a simple example.",
            "grammar_summary": "Use People usually... / In my area, people often... to describe local habits naturally.",
            "speakers": ("Mina", "Leo"),
            "situation_id": "Kamu cerita kebiasaan di daerah kamu. Kamu jelaskan biasanya orang ngapain dan kasih contoh singkat.",
            "dialogue": [
                ("Leo", "Are there any local habits in your area?"),
                ("Mina", "Yeah. People usually eat outside in the evening."),
                ("Leo", "Interesting. Like street food?"),
                ("Mina", "Exactly. In my area, people often grab noodles or satay after work."),
                ("Leo", "Do families do that too?"),
                ("Mina", "Yes, especially on weekends."),
                ("Leo", "That sounds fun."),
                ("Mina", "It is. It's a social thing."),
            ],
            "translations": [
                ("Leo", "Are there any local habits in your area?", "Ada kebiasaan lokal di daerah kamu?"),
                ("Mina", "Yeah. People usually eat outside in the evening.", "Ada. Orang biasanya makan di luar sore/malam."),
                ("Leo", "Interesting. Like street food?", "Menarik. Kayak street food?"),
                ("Mina", "Exactly. In my area, people often grab noodles or satay after work.", "Iya. Di daerahku orang sering beli mi atau sate setelah kerja."),
                ("Leo", "Do families do that too?", "Keluarga juga gitu?"),
                ("Mina", "Yes, especially on weekends.", "Iya, apalagi pas weekend."),
                ("Leo", "That sounds fun.", "Kedengarannya seru."),
                ("Mina", "It is. It's a social thing.", "Seru. Itu kegiatan sosial."),
            ],
            "useful_phrases": [
                {
                    "phrase": "People usually eat outside in the evening.",
                    "meaning_id": "Orang biasanya makan di luar sore/malam.",
                    "usage_note": "Usually shows a common habit.",
                    "common_mistake": 'Do not say "People usual eat"; use usually.',
                },
                {
                    "phrase": "In my area, people often grab street food.",
                    "meaning_id": "Di daerahku, orang sering beli street food.",
                    "usage_note": "In my area is a natural starter.",
                    "common_mistake": 'Do not say "In my area people often" without comma if you want a pause; keep it clear.',
                },
                {
                    "phrase": "Especially on weekends.",
                    "meaning_id": "Apalagi pas weekend.",
                    "usage_note": "Add detail about frequency.",
                    "common_mistake": 'Do not say "special" for this meaning; use especially.',
                },
                {
                    "phrase": "It's a social thing.",
                    "meaning_id": "Itu kegiatan sosial.",
                    "usage_note": "A natural explanation phrase.",
                    "common_mistake": 'Do not say "It social"; use it\'s.',
                },
                {
                    "phrase": "People often do it after work.",
                    "meaning_id": "Orang sering ngelakuin itu setelah kerja.",
                    "usage_note": "Often is a simple frequency word.",
                    "common_mistake": 'Do not say "People often does"; use do.',
                },
            ],
            "grammar_md": [
                ("People usually...", ["People usually eat outside in the evening.", "People usually go home before 10."]),
                ("People often...", ["People often grab street food after work.", "People often meet friends on weekends."]),
            ],
            "pronunciation": [
                ("usually", "YOO-zhoo-uh-lee."),
                ("especially", "es-PESH-uh-lee."),
                ("street food", "STREET food."),
            ],
            "response_prompts": [
                {
                    "prompt": "Describe a local habit with usually.",
                    "target_response": "People usually eat outside in the evening.",
                    "acceptable_variations": ["People usually eat outside in the evening.", "People usually go out at night."],
                },
                {
                    "prompt": "Describe another habit with in my area + often.",
                    "target_response": "In my area, people often grab street food after work.",
                    "acceptable_variations": [
                        "In my area, people often grab street food after work.",
                        "In my area, people often meet friends on weekends.",
                    ],
                },
                {
                    "prompt": "Add a frequency detail (especially on weekends).",
                    "target_response": "Especially on weekends.",
                    "acceptable_variations": ["Especially on weekends.", "Especially on Friday nights."],
                },
            ],
            "quiz": [
                {
                    "key": "usually_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "usually" mean?',
                    "options": ["biasanya", "jarang", "tiba-tiba"],
                    "correct_answer": "biasanya",
                },
                {
                    "key": "often_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "often" mean?',
                    "options": ["sering", "tidak pernah", "sekali"],
                    "correct_answer": "sering",
                },
                {
                    "key": "especially_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "especially" mean?',
                    "options": ["terutama", "mungkin", "hampir"],
                    "correct_answer": "terutama",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_culture_local_habits",
                "opening_line": "Tell me a local habit in your area.",
                "learner_goal": "Describe a local habit using usually/often and add one example.",
                "turns": [
                    {
                        "coach": "Tell me a local habit in your area.",
                        "hint": "Mulai dengan People usually...",
                        "sample_answer": "People usually eat outside in the evening.",
                        "focus": "Describe habit",
                        "expected_keywords": ["usually"],
                    },
                    {
                        "coach": "Can you give an example?",
                        "hint": "Gunakan In my area, people often...",
                        "sample_answer": "In my area, people often grab noodles or satay after work.",
                        "focus": "Give example",
                        "expected_keywords": ["often", "in my area"],
                    },
                    {
                        "coach": "How often does it happen?",
                        "hint": "Tambahkan detail: especially on weekends.",
                        "sample_answer": "Especially on weekends.",
                        "focus": "Add frequency detail",
                        "expected_keywords": ["especially", "weekends"],
                    },
                ],
                "target_phrases": ["People usually ...", "In my area, people often ...", "Especially on weekends."],
            },
            "reading_support": "Local habits are easy to describe with frequency words like usually and often. Add one simple example and one frequency detail.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. In my area, people usually ...",
                "2. People often ... after work.",
                "3. Especially on weekends.",
                "4. It's a social thing.",
                "5. I like it because ...",
            ],
            "goal_examples": ["People usually ...", "In my area, people often ...", "Especially on weekends."],
        },
        {
            "lesson_key": "lesson-03-asking-about-culture",
            "slug": "asking-about-culture",
            "title": "Asking About Culture",
            "conversation_situation": "asking_about_culture_politely",
            "conversation_goal": "Ask about cultural traditions politely and respond with a short explanation.",
            "grammar_summary": "Use What is it like in your country? / Do people usually...? to ask about culture respectfully.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu ngobrol sama orang baru. Kamu tanya tradisi atau kebiasaan di negaranya dengan sopan, lalu jawab singkat tentang negaramu juga.",
            "dialogue": [
                ("Jordan", "Do you have any big holidays in your country?"),
                ("Mina", "Yes. We celebrate Eid, and many people travel to visit family."),
                ("Jordan", "What is it like during that time?"),
                ("Mina", "It's busy, but it's also warm and meaningful."),
                ("Jordan", "Do people usually give gifts?"),
                ("Mina", "Sometimes. Mostly we share food and spend time together."),
                ("Jordan", "That sounds lovely."),
                ("Mina", "How about in your country?"),
            ],
            "translations": [
                ("Jordan", "Do you have any big holidays in your country?", "Ada hari libur besar di negara kamu?"),
                ("Mina", "Yes. We celebrate Eid, and many people travel to visit family.", "Iya. Kita merayakan Idul Fitri, dan banyak orang mudik."),
                ("Jordan", "What is it like during that time?", "Suasananya gimana waktu itu?"),
                ("Mina", "It's busy, but it's also warm and meaningful.", "Ramai, tapi juga hangat dan bermakna."),
                ("Jordan", "Do people usually give gifts?", "Orang biasanya kasih hadiah?"),
                ("Mina", "Sometimes. Mostly we share food and spend time together.", "Kadang. Kebanyakan kita berbagi makanan dan kumpul."),
                ("Jordan", "That sounds lovely.", "Kedengarannya bagus."),
                ("Mina", "How about in your country?", "Kalau di negara kamu gimana?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "What is it like in your country?",
                    "meaning_id": "Gimana di negara kamu?",
                    "usage_note": "A respectful culture question.",
                    "common_mistake": 'Do not say "What like your country?" Use What is it like...?',
                },
                {
                    "phrase": "Do people usually travel to visit family?",
                    "meaning_id": "Orang biasanya mudik/berkunjung ke keluarga?",
                    "usage_note": "A polite habit question.",
                    "common_mistake": 'Do not say "People usually travel?" without do in a question.',
                },
                {
                    "phrase": "It's busy, but it's also meaningful.",
                    "meaning_id": "Ramai, tapi juga bermakna.",
                    "usage_note": "A balanced description.",
                    "common_mistake": 'Do not drop the second it\'s; keep the structure clear.',
                },
                {
                    "phrase": "Mostly we share food and spend time together.",
                    "meaning_id": "Kebanyakan kita berbagi makanan dan kumpul.",
                    "usage_note": "Mostly is a natural frequency word.",
                    "common_mistake": 'Do not say "Mostly we sharing"; use share.',
                },
                {
                    "phrase": "How about in your country?",
                    "meaning_id": "Kalau di negara kamu gimana?",
                    "usage_note": "A polite way to ask back.",
                    "common_mistake": 'Do not say "How about your country?" without in if you mean the place.',
                },
            ],
            "grammar_md": [
                ("Culture questions", ["What is it like in your country?", "Do people usually travel during holidays?"]),
                ("Mostly / sometimes", ["Mostly we share food.", "Sometimes people give gifts."]),
            ],
            "pronunciation": [
                ("meaningful", "MEE-ning-ful."),
                ("mostly", "MOHST-lee."),
                ("holiday", "HOL-uh-day."),
            ],
            "response_prompts": [
                {
                    "prompt": "Ask a culture question.",
                    "target_response": "What is it like in your country?",
                    "acceptable_variations": ["What is it like in your country?", "Do people usually travel during holidays?"],
                },
                {
                    "prompt": "Describe it (busy but meaningful).",
                    "target_response": "It's busy, but it's also meaningful.",
                    "acceptable_variations": ["It's busy, but it's also meaningful.", "It's busy, but it's also fun."],
                },
                {
                    "prompt": "Ask back politely.",
                    "target_response": "How about in your country?",
                    "acceptable_variations": ["How about in your country?", "How about you?"],
                },
            ],
            "quiz": [
                {
                    "key": "culture_question",
                    "type": "multiple_choice",
                    "prompt": "Which sentence is a respectful culture question?",
                    "options": ["What is it like in your country?", "Your country weird?", "Tell me now."],
                    "correct_answer": "What is it like in your country?",
                },
                {
                    "key": "mostly_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "mostly" mean?',
                    "options": ["kebanyakan", "selalu", "tidak pernah"],
                    "correct_answer": "kebanyakan",
                },
                {
                    "key": "meaningful_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "meaningful" mean?',
                    "options": ["bermakna", "berbahaya", "membosankan"],
                    "correct_answer": "bermakna",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_culture_asking_about_culture",
                "opening_line": "Ask me about a tradition in my country.",
                "learner_goal": "Ask politely about culture and respond with a short explanation.",
                "turns": [
                    {
                        "coach": "Ask me about a tradition in my country.",
                        "hint": "Gunakan What is it like...?",
                        "sample_answer": "What is it like in your country during big holidays?",
                        "focus": "Ask culture question",
                        "expected_keywords": ["what is it like", "country"],
                    },
                    {
                        "coach": "Answer about your country in 1-2 sentences.",
                        "hint": "Jawab: It's ... but ... Mostly ...",
                        "sample_answer": "It's busy, but it's also meaningful. Mostly we share food and spend time together.",
                        "focus": "Explain briefly",
                        "expected_keywords": ["busy", "mostly"],
                    },
                    {
                        "coach": "Ask back politely.",
                        "hint": "Gunakan How about in your country?",
                        "sample_answer": "How about in your country?",
                        "focus": "Ask back",
                        "expected_keywords": ["how about"],
                    },
                ],
                "target_phrases": ["What is it like in your country?", "It's ..., but ...", "How about in your country?"],
            },
            "reading_support": "When asking about culture, be respectful: ask general questions, listen, and ask back. Keep your explanation short and positive.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. What is it like in your country during ...?",
                "2. In my country, we usually ...",
                "3. It's ..., but it's also ...",
                "4. Mostly we ...",
                "5. How about in your country?",
            ],
            "goal_examples": ["What is it like in your country?", "Do people usually...?", "How about in your country?"],
        },
        {
            "lesson_key": "lesson-04-being-polite-with-differences",
            "slug": "being-polite-with-differences",
            "title": "Being Polite With Differences",
            "conversation_situation": "being_polite_about_differences",
            "conversation_goal": "Talk about cultural differences politely and show respect even if you do things differently.",
            "grammar_summary": "Use In my country,... / That's interesting / I'm not used to... / That sounds nice to be polite about differences.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu diskusi perbedaan kebiasaan. Kamu jelasin kebiasaanmu, respon dengan sopan, dan tunjukkan respek.",
            "dialogue": [
                ("Jordan", "In my country, people usually eat dinner early, around 6 p.m."),
                ("Mina", "Oh, that's interesting. In my country, we often eat later."),
                ("Jordan", "Really? Around what time?"),
                ("Mina", "Around 8 or 9 p.m. I'm not used to eating that early."),
                ("Jordan", "That makes sense."),
                ("Mina", "But eating early sounds nice, especially if you sleep early."),
                ("Jordan", "Yeah, it works well for families."),
                ("Mina", "Cool. Thanks for sharing."),
            ],
            "translations": [
                ("Jordan", "In my country, people usually eat dinner early, around 6 p.m.", "Di negara aku, orang biasanya makan malam lebih awal, sekitar jam 6."),
                ("Mina", "Oh, that's interesting. In my country, we often eat later.", "Oh menarik. Di negara aku, kita sering makan lebih malam."),
                ("Jordan", "Really? Around what time?", "Serius? Jam berapa?"),
                ("Mina", "Around 8 or 9 p.m. I'm not used to eating that early.", "Sekitar jam 8 atau 9 malam. Aku nggak terbiasa makan secepat itu."),
                ("Jordan", "That makes sense.", "Masuk akal."),
                ("Mina", "But eating early sounds nice, especially if you sleep early.", "Tapi makan lebih awal kedengarannya enak, apalagi kalau tidurnya cepat."),
                ("Jordan", "Yeah, it works well for families.", "Iya, itu cocok buat keluarga."),
                ("Mina", "Cool. Thanks for sharing.", "Oke. Makasih sudah cerita."),
            ],
            "useful_phrases": [
                {
                    "phrase": "Oh, that's interesting.",
                    "meaning_id": "Oh menarik.",
                    "usage_note": "A polite reaction to differences.",
                    "common_mistake": 'Do not sound judgmental; keep a neutral tone.',
                },
                {
                    "phrase": "In my country, we often eat later.",
                    "meaning_id": "Di negara aku, kita sering makan lebih malam.",
                    "usage_note": "A polite way to explain your habit.",
                    "common_mistake": 'Do not say "In my country we eats"; use eat.',
                },
                {
                    "phrase": "I'm not used to eating that early.",
                    "meaning_id": "Aku nggak terbiasa makan secepat itu.",
                    "usage_note": "A polite way to say it's unfamiliar.",
                    "common_mistake": 'Do not say "I not used"; use I\'m not used to.',
                },
                {
                    "phrase": "That sounds nice.",
                    "meaning_id": "Kedengarannya enak/bagus.",
                    "usage_note": "Show respect even if different.",
                    "common_mistake": 'Do not say "That sound nice"; add -s.',
                },
                {
                    "phrase": "Thanks for sharing.",
                    "meaning_id": "Makasih sudah cerita.",
                    "usage_note": "A polite closing for culture talk.",
                    "common_mistake": 'Do not say only thanks; add for sharing to show you listened.',
                },
            ],
            "grammar_md": [
                ("I'm not used to + noun/verb-ing", ["I'm not used to eating that early.", "I'm not used to spicy food."]),
                ("Polite reactions", ["That's interesting.", "That sounds nice.", "That makes sense."]),
            ],
            "pronunciation": [
                ("interesting", "IN-ter-es-ting."),
                ("used to", "YOOS-to (link it)."),
                ("early", "ER-lee."),
            ],
            "response_prompts": [
                {
                    "prompt": "React politely.",
                    "target_response": "Oh, that's interesting.",
                    "acceptable_variations": ["Oh, that's interesting.", "That's interesting."],
                },
                {
                    "prompt": "Explain your habit (eat later).",
                    "target_response": "In my country, we often eat later.",
                    "acceptable_variations": ["In my country, we often eat later.", "In my country, we usually eat later."],
                },
                {
                    "prompt": "Say you're not used to it.",
                    "target_response": "I'm not used to eating that early.",
                    "acceptable_variations": ["I'm not used to eating that early.", "I'm not used to that."],
                },
            ],
            "quiz": [
                {
                    "key": "not_used_to",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["I'm not used to eating that early.", "I not used to eating that early.", "I'm not use to eating early."],
                    "correct_answer": "I'm not used to eating that early.",
                },
                {
                    "key": "judgment_tone",
                    "type": "multiple_choice",
                    "prompt": "Which reaction is polite?",
                    "options": ["That's interesting.", "That's weird.", "That's wrong."],
                    "correct_answer": "That's interesting.",
                },
                {
                    "key": "thanks_sharing",
                    "type": "multiple_choice",
                    "prompt": "Which sentence closes politely?",
                    "options": ["Thanks for sharing.", "Whatever.", "Stop."],
                    "correct_answer": "Thanks for sharing.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_culture_polite_differences",
                "opening_line": "In my country, people usually do it differently.",
                "learner_goal": "React politely, explain your habit, and show respect.",
                "turns": [
                    {
                        "coach": "In my country, people usually eat dinner early, around 6 p.m.",
                        "hint": "Reaksi sopan + jelaskan kebiasaanmu.",
                        "sample_answer": "Oh, that's interesting. In my country, we often eat later.",
                        "focus": "Polite reaction + difference",
                        "expected_keywords": ["interesting", "in my country"],
                    },
                    {
                        "coach": "Really? Are you used to eating early?",
                        "hint": "Jawab dengan I'm not used to...",
                        "sample_answer": "I'm not used to eating that early.",
                        "focus": "Say unfamiliar politely",
                        "expected_keywords": ["not used to"],
                    },
                    {
                        "coach": "Say something respectful about my habit.",
                        "hint": "Gunakan That sounds nice.",
                        "sample_answer": "That sounds nice, especially if you sleep early.",
                        "focus": "Show respect",
                        "expected_keywords": ["sounds nice"],
                    },
                ],
                "target_phrases": ["That's interesting.", "I'm not used to ...", "That sounds nice."],
            },
            "reading_support": "Cultural differences are normal. Use polite reactions, explain your habit, and show respect even if it's different from yours.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. Oh, that's interesting.",
                "2. In my country, we usually ...",
                "3. I'm not used to ...",
                "4. But that sounds nice.",
                "5. Thanks for sharing.",
            ],
            "goal_examples": ["Oh, that's interesting.", "I'm not used to ...", "That sounds nice."],
        },
        {
            "lesson_key": "lesson-05-community-culture-mission",
            "slug": "community-culture-mission",
            "title": "Community Culture Mission",
            "conversation_situation": "mission_community_culture_difference",
            "conversation_goal": "Complete a mini conversation: describe your community, share a local habit, ask about culture, and respond politely to differences.",
            "grammar_summary": "Combine: It's known for... / People usually... / What is it like in your country? / I'm not used to... / That sounds nice.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Misi: kamu kenalan sama orang baru. Kamu ceritain komunitas kamu, kebiasaan lokal, tanya budaya negaranya, lalu respon sopan soal perbedaan.",
            "dialogue": [
                ("Jordan", "So, what's your neighborhood like?"),
                ("Mina", "I live in a quiet neighborhood. It's known for food stalls."),
                ("Jordan", "Nice. Any local habits?"),
                ("Mina", "People usually eat outside in the evening, especially on weekends."),
                ("Jordan", "Interesting. What is it like in your country during big holidays?"),
                ("Mina", "It's busy, but it's also meaningful. Mostly we spend time with family."),
                ("Jordan", "In my country, people eat dinner early, around 6 p.m."),
                ("Mina", "Oh, that's interesting. I'm not used to that, but it sounds nice."),
            ],
            "translations": [
                ("Jordan", "So, what's your neighborhood like?", "Jadi, lingkungan kamu gimana?"),
                ("Mina", "I live in a quiet neighborhood. It's known for food stalls.", "Aku tinggal di lingkungan yang tenang. Terkenal dengan warung makan."),
                ("Jordan", "Nice. Any local habits?", "Oke. Ada kebiasaan lokal?"),
                ("Mina", "People usually eat outside in the evening, especially on weekends.", "Orang biasanya makan di luar sore/malam, apalagi weekend."),
                ("Jordan", "Interesting. What is it like in your country during big holidays?", "Menarik. Suasananya gimana di negara kamu waktu libur besar?"),
                ("Mina", "It's busy, but it's also meaningful. Mostly we spend time with family.", "Ramai, tapi juga bermakna. Kebanyakan kita kumpul sama keluarga."),
                ("Jordan", "In my country, people eat dinner early, around 6 p.m.", "Di negara aku, orang makan malam lebih awal, sekitar jam 6."),
                ("Mina", "Oh, that's interesting. I'm not used to that, but it sounds nice.", "Oh menarik. Aku nggak terbiasa, tapi kedengarannya bagus."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I live in a quiet neighborhood. It's known for food stalls.",
                    "meaning_id": "Aku tinggal di lingkungan yang tenang. Terkenal dengan warung makan.",
                    "usage_note": "Short community description.",
                    "common_mistake": "Avoid long details; keep it to 1-2 sentences.",
                },
                {
                    "phrase": "People usually eat outside in the evening, especially on weekends.",
                    "meaning_id": "Orang biasanya makan di luar sore/malam, apalagi weekend.",
                    "usage_note": "Habit + frequency detail.",
                    "common_mistake": "Don't list too many habits; one is enough.",
                },
                {
                    "phrase": "What is it like in your country during big holidays?",
                    "meaning_id": "Suasananya gimana di negara kamu waktu libur besar?",
                    "usage_note": "A respectful culture question.",
                    "common_mistake": 'Do not shorten it to "What like"; keep the full question.',
                },
                {
                    "phrase": "It's busy, but it's also meaningful.",
                    "meaning_id": "Ramai, tapi juga bermakna.",
                    "usage_note": "Balanced description.",
                    "common_mistake": "Keep a positive tone.",
                },
                {
                    "phrase": "I'm not used to that, but it sounds nice.",
                    "meaning_id": "Aku nggak terbiasa, tapi kedengarannya bagus.",
                    "usage_note": "Polite difference response.",
                    "common_mistake": 'Do not say "That\'s wrong"; be polite.',
                },
            ],
            "grammar_md": [
                (
                    "Community + habit + culture + difference",
                    [
                        "It's known for ...",
                        "People usually ...",
                        "What is it like in your country ...?",
                        "I'm not used to ..., but it sounds nice.",
                    ],
                ),
            ],
            "pronunciation": [
                ("known for", "KNOWN-for (link it)."),
                ("meaningful", "MEE-ning-ful."),
                ("not used to", "not-YOOS-to (link it)."),
            ],
            "response_prompts": [
                {
                    "prompt": "Describe your community (known for).",
                    "target_response": "I live in a quiet neighborhood. It's known for food stalls.",
                    "acceptable_variations": [
                        "I live in a quiet neighborhood. It's known for food stalls.",
                        "I live in a busy neighborhood. It's known for cafes.",
                    ],
                },
                {
                    "prompt": "Share a local habit (usually + especially).",
                    "target_response": "People usually eat outside in the evening, especially on weekends.",
                    "acceptable_variations": [
                        "People usually eat outside in the evening, especially on weekends.",
                        "People usually meet friends at night, especially on weekends.",
                    ],
                },
                {
                    "prompt": "Respond politely to a difference.",
                    "target_response": "I'm not used to that, but it sounds nice.",
                    "acceptable_variations": [
                        "I'm not used to that, but it sounds nice.",
                        "I'm not used to it, but that's interesting.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "mission_culture_flow",
                    "type": "multiple_choice",
                    "prompt": "Which skills are combined in this mission?",
                    "options": [
                        "Community description + local habit + culture question + polite differences",
                        "Numbers only",
                        "Ordering food only",
                    ],
                    "correct_answer": "Community description + local habit + culture question + polite differences",
                },
                {
                    "key": "used_to_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "I\'m not used to that" mean?',
                    "options": ["aku nggak terbiasa", "aku setuju", "aku lupa"],
                    "correct_answer": "aku nggak terbiasa",
                },
                {
                    "key": "respectful_reaction",
                    "type": "multiple_choice",
                    "prompt": "Which reaction is respectful?",
                    "options": ["That sounds nice.", "That's wrong.", "That's stupid."],
                    "correct_answer": "That sounds nice.",
                },
            ],
            "roleplay": {
                "scenario_key": "b1_culture_mission",
                "opening_line": "Tell me about your community and culture.",
                "learner_goal": "Describe your community, share a habit, ask about culture, and respond politely to differences.",
                "turns": [
                    {
                        "coach": "Tell me about your neighborhood.",
                        "hint": "I live in... It's known for...",
                        "sample_answer": "I live in a quiet neighborhood. It's known for food stalls and small parks.",
                        "focus": "Describe community",
                        "expected_keywords": ["neighborhood", "known for"],
                    },
                    {
                        "coach": "Share one local habit.",
                        "hint": "People usually... especially on weekends.",
                        "sample_answer": "People usually eat outside in the evening, especially on weekends.",
                        "focus": "Share local habit",
                        "expected_keywords": ["usually", "especially"],
                    },
                    {
                        "coach": "Now respond politely to a cultural difference.",
                        "hint": "That's interesting. I'm not used to..., but it sounds nice.",
                        "sample_answer": "Oh, that's interesting. I'm not used to that, but it sounds nice.",
                        "focus": "Polite differences",
                        "expected_keywords": ["interesting", "not used to", "sounds nice"],
                    },
                ],
                "target_phrases": ["It's known for ...", "People usually ...", "I'm not used to ..., but it sounds nice."],
            },
            "reading_support": "This mission combines community and culture skills: describing your neighborhood, sharing a local habit, asking polite culture questions, and responding respectfully to differences.",
            "writing_support_lines": [
                "Write your mission (6 lines):",
                "1. I live in a ... neighborhood.",
                "2. It's known for ...",
                "3. People usually ...",
                "4. Especially on weekends.",
                "5. Oh, that's interesting. I'm not used to ...",
                "6. But it sounds nice.",
            ],
            "goal_examples": ["It's known for ...", "People usually ...", "Oh, that's interesting."],
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

