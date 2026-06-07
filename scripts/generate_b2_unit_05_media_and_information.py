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
            "- Tone: professional, thoughtful, clear",
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

        Read it again and underline the information words (source, claim, evidence, reliable, viewpoint).
        """
    )


def render_writing_support_md(lines_: list[str]) -> str:
    return "# Writing Support\n\n" + "\n".join(lines_)


def main() -> None:
    level_code = "B2"
    b2_root = Path("content/curriculum/english/B2")
    units_root = b2_root / "units"
    unit_key = "unit-05-media-and-information"
    unit_dir = units_root / unit_key

    units_root.mkdir(parents=True, exist_ok=True)
    if unit_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing: {unit_dir}")

    unit_dir.mkdir(parents=True, exist_ok=False)

    write_text(
        unit_dir / "unit.yaml",
        dedent(
            """\
            unit_key: unit-05-media-and-information
            level_code: B2
            title: Media & Information
            main_conversation_outcome: Discuss information, sources, and viewpoints critically.
            status: in_production
            lessons:
              - lesson-01-summarizing-an-article
              - lesson-02-discussing-reliable-sources
              - lesson-03-explaining-a-viewpoint
              - lesson-04-responding-to-new-information
              - lesson-05-information-discussion-mission
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
            "lesson_key": "lesson-01-summarizing-an-article",
            "slug": "summarizing-an-article",
            "title": "Summarizing an Article",
            "conversation_situation": "summarizing_article",
            "conversation_goal": "Summarize an article in 2–3 sentences: main topic, key point, and conclusion.",
            "grammar_summary": "Use The article is about... / The main point is... / It concludes that... to summarize clearly.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu habis baca artikel. Kamu jelasin topiknya, poin utama, dan kesimpulan singkat ke teman kerja.",
            "dialogue": [
                ("Alex", "Did you read that article about remote work?"),
                ("Mina", "Yes. The article is about how remote work affects productivity."),
                ("Alex", "What's the main point?"),
                ("Mina", "The main point is productivity improves when teams set clear communication rules."),
                ("Alex", "Interesting. Does it mention any downsides?"),
                ("Mina", "Yes, it mentions isolation, especially for new hires."),
                ("Alex", "How does it conclude?"),
                ("Mina", "It concludes that hybrid setups work best for many teams."),
            ],
            "translations": [
                ("Alex", "Did you read that article about remote work?", "Kamu baca artikel tentang kerja remote itu?"),
                ("Mina", "Yes. The article is about how remote work affects productivity.", "Iya. Artikelnya tentang dampak kerja remote ke produktivitas."),
                ("Alex", "What's the main point?", "Poin utamanya apa?"),
                ("Mina", "The main point is productivity improves when teams set clear communication rules.", "Poin utamanya produktivitas naik kalau tim punya aturan komunikasi yang jelas."),
                ("Alex", "Interesting. Does it mention any downsides?", "Menarik. Ada kekurangannya?"),
                ("Mina", "Yes, it mentions isolation, especially for new hires.", "Ada, disebutkan rasa terisolasi, terutama buat orang baru."),
                ("Alex", "How does it conclude?", "Kesimpulannya apa?"),
                ("Mina", "It concludes that hybrid setups work best for many teams.", "Kesimpulannya model hybrid paling cocok untuk banyak tim."),
            ],
            "useful_phrases": [
                {
                    "phrase": "The article is about how remote work affects productivity.",
                    "meaning_id": "Artikelnya tentang dampak kerja remote ke produktivitas.",
                    "usage_note": "A clear topic sentence.",
                    "common_mistake": 'Do not say "The article about"; include is.',
                },
                {
                    "phrase": "The main point is productivity improves with clear rules.",
                    "meaning_id": "Poin utamanya produktivitas naik kalau ada aturan yang jelas.",
                    "usage_note": "A clear main point sentence.",
                    "common_mistake": 'Do not say "main point are"; use is.',
                },
                {
                    "phrase": "It mentions isolation as a downside.",
                    "meaning_id": "Disebutkan rasa terisolasi sebagai kekurangan.",
                    "usage_note": "Mention a downside briefly.",
                    "common_mistake": 'Do not say "It mention"; add -s.',
                },
                {
                    "phrase": "It concludes that hybrid setups work best.",
                    "meaning_id": "Kesimpulannya model hybrid paling cocok.",
                    "usage_note": "A clear conclusion sentence.",
                    "common_mistake": 'Do not say "It conclude"; add -s.',
                },
                {
                    "phrase": "In short, the key takeaway is clear rules help.",
                    "meaning_id": "Singkatnya, inti pesannya: aturan yang jelas itu membantu.",
                    "usage_note": "A concise summary closing.",
                    "common_mistake": 'Do not add too many details after in short.',
                },
            ],
            "grammar_md": [
                ("Summary structure", ["The article is about ...", "The main point is ...", "It concludes that ..."]),
            ],
            "pronunciation": [
                ("productivity", "pro-duk-TIV-i-tee."),
                ("concludes", "kun-KLOODZ."),
                ("hybrid", "HY-brid."),
            ],
            "response_prompts": [
                {
                    "prompt": "State the topic.",
                    "target_response": "The article is about how remote work affects productivity.",
                    "acceptable_variations": [
                        "The article is about how remote work affects productivity.",
                        "The article is about media bias.",
                    ],
                },
                {
                    "prompt": "State the main point.",
                    "target_response": "The main point is productivity improves with clear communication rules.",
                    "acceptable_variations": [
                        "The main point is productivity improves with clear communication rules.",
                        "The main point is reliable sources matter.",
                    ],
                },
                {
                    "prompt": "State the conclusion.",
                    "target_response": "It concludes that hybrid setups work best for many teams.",
                    "acceptable_variations": [
                        "It concludes that hybrid setups work best for many teams.",
                        "It concludes that we need clearer guidelines.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "summary_topic",
                    "type": "multiple_choice",
                    "prompt": "Which sentence states the topic of an article?",
                    "options": ["The article is about ...", "I am article ...", "About article ..."],
                    "correct_answer": "The article is about ...",
                },
                {
                    "key": "main_point",
                    "type": "multiple_choice",
                    "prompt": "Which sentence states the main point?",
                    "options": ["The main point is ...", "Main point are ...", "Point main ..."],
                    "correct_answer": "The main point is ...",
                },
                {
                    "key": "conclusion",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a conclusion?",
                    "options": ["It concludes that ...", "It concluded to ...", "It conclude ..."],
                    "correct_answer": "It concludes that ...",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_info_summarize_article",
                "opening_line": "Can you summarize the article you read?",
                "learner_goal": "Summarize an article with topic, main point, and conclusion.",
                "turns": [
                    {
                        "coach": "What's the article about?",
                        "hint": "The article is about ...",
                        "sample_answer": "The article is about how remote work affects productivity.",
                        "focus": "Topic",
                        "expected_keywords": ["article is about"],
                    },
                    {
                        "coach": "What's the main point?",
                        "hint": "The main point is ...",
                        "sample_answer": "The main point is productivity improves with clear communication rules.",
                        "focus": "Main point",
                        "expected_keywords": ["main point"],
                    },
                    {
                        "coach": "How does it conclude?",
                        "hint": "It concludes that ...",
                        "sample_answer": "It concludes that hybrid setups work best for many teams.",
                        "focus": "Conclusion",
                        "expected_keywords": ["concludes"],
                    },
                ],
                "target_phrases": ["The article is about ...", "The main point is ...", "It concludes that ..."],
            },
            "reading_support": "A strong summary is short and structured: topic, main point, and conclusion. Avoid extra details unless asked.",
            "writing_support_lines": [
                "Write 5 lines:",
                "1. The article is about ...",
                "2. The main point is ...",
                "3. It mentions ... as a downside.",
                "4. It concludes that ...",
                "5. In short, the key takeaway is ...",
            ],
            "goal_examples": ["The article is about ...", "The main point is ...", "It concludes that ..."],
        },
        {
            "lesson_key": "lesson-02-discussing-reliable-sources",
            "slug": "discussing-reliable-sources",
            "title": "Discussing Reliable Sources",
            "conversation_situation": "discussing_reliable_sources",
            "conversation_goal": "Discuss whether a source is reliable, explain why, and suggest a better source.",
            "grammar_summary": "Use I trust this source because... / I'm not sure it's reliable / I'd check... to evaluate sources.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu bahas berita. Kamu nilai sumbernya reliable atau tidak, jelasin alasannya, lalu saranin sumber yang lebih baik.",
            "dialogue": [
                ("Jordan", "I saw a claim on social media. Is it true?"),
                ("Mina", "I'm not sure that source is reliable."),
                ("Jordan", "Why not?"),
                ("Mina", "Because it doesn't cite data or mention who wrote it."),
                ("Jordan", "So what would you check?"),
                ("Mina", "I'd check official reports or reputable news outlets."),
                ("Jordan", "How do you decide what's reputable?"),
                ("Mina", "I trust sources that show evidence and correct mistakes publicly."),
            ],
            "translations": [
                ("Jordan", "I saw a claim on social media. Is it true?", "Aku lihat klaim di social media. Itu bener nggak?"),
                ("Mina", "I'm not sure that source is reliable.", "Aku nggak yakin sumber itu reliable."),
                ("Jordan", "Why not?", "Kenapa?"),
                ("Mina", "Because it doesn't cite data or mention who wrote it.", "Karena nggak nyantumin data atau siapa penulisnya."),
                ("Jordan", "So what would you check?", "Jadi kamu cek apa?"),
                ("Mina", "I'd check official reports or reputable news outlets.", "Aku bakal cek laporan resmi atau media berita yang reputasinya bagus."),
                ("Jordan", "How do you decide what's reputable?", "Gimana kamu nentuin yang reputasinya bagus?"),
                ("Mina", "I trust sources that show evidence and correct mistakes publicly.", "Aku percaya sumber yang nunjukin bukti dan mengoreksi kesalahan secara terbuka."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I'm not sure that source is reliable.",
                    "meaning_id": "Aku nggak yakin sumber itu reliable.",
                    "usage_note": "A polite skepticism phrase.",
                    "common_mistake": 'Do not say "I not sure"; use I\'m not sure.',
                },
                {
                    "phrase": "Because it doesn't cite data or mention the author.",
                    "meaning_id": "Karena nggak nyantumin data atau penulisnya.",
                    "usage_note": "Give a concrete reason.",
                    "common_mistake": 'Do not say "doesn\'t cites"; keep doesn\'t + base verb.',
                },
                {
                    "phrase": "I'd check official reports.",
                    "meaning_id": "Aku bakal cek laporan resmi.",
                    "usage_note": "Suggest a better verification step.",
                    "common_mistake": 'Do not say "I will check" every time; I\'d check is natural.',
                },
                {
                    "phrase": "I trust sources that show evidence.",
                    "meaning_id": "Aku percaya sumber yang nunjukin bukti.",
                    "usage_note": "Explain your criteria.",
                    "common_mistake": 'Do not say "trust to"; use trust + object.',
                },
                {
                    "phrase": "Let's verify it before sharing.",
                    "meaning_id": "Yuk verifikasi dulu sebelum share.",
                    "usage_note": "A practical closing suggestion.",
                    "common_mistake": 'Do not blame; suggest a shared action.',
                },
            ],
            "grammar_md": [
                ("Reliability language", ["I'm not sure it's reliable.", "I trust this source because it cites evidence."]),
                ("Verification", ["I'd check official reports.", "I'd cross-check with two sources."]),
            ],
            "pronunciation": [
                ("reliable", "ri-LYE-uh-bul."),
                ("evidence", "EV-i-dens."),
                ("official", "uh-FISH-ul."),
            ],
            "response_prompts": [
                {
                    "prompt": "Express polite doubt.",
                    "target_response": "I'm not sure that source is reliable.",
                    "acceptable_variations": ["I'm not sure that source is reliable.", "I'm not sure it's reliable."],
                },
                {
                    "prompt": "Give a reason.",
                    "target_response": "Because it doesn't cite data or mention the author.",
                    "acceptable_variations": [
                        "Because it doesn't cite data or mention the author.",
                        "Because it has no evidence.",
                    ],
                },
                {
                    "prompt": "Suggest a better check.",
                    "target_response": "I'd check official reports or reputable news outlets.",
                    "acceptable_variations": [
                        "I'd check official reports or reputable news outlets.",
                        "I'd cross-check with two reputable sources.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "reliable_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "reliable" mean?',
                    "options": ["dapat dipercaya", "terlambat", "ramai"],
                    "correct_answer": "dapat dipercaya",
                },
                {
                    "key": "cite_data",
                    "type": "multiple_choice",
                    "prompt": 'What does "cite data" mean?',
                    "options": ["menyantumkan data", "membuat data", "menghapus data"],
                    "correct_answer": "menyantumkan data",
                },
                {
                    "key": "verification",
                    "type": "multiple_choice",
                    "prompt": "Which sentence suggests verification?",
                    "options": ["I'd check official reports.", "I believe anything.", "Share it now."],
                    "correct_answer": "I'd check official reports.",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_info_reliable_sources",
                "opening_line": "I saw a claim online. Is it reliable?",
                "learner_goal": "Discuss reliability: express doubt, give reasons, and suggest verification.",
                "turns": [
                    {
                        "coach": "Is this source reliable?",
                        "hint": "I'm not sure it's reliable.",
                        "sample_answer": "I'm not sure that source is reliable.",
                        "focus": "Express doubt",
                        "expected_keywords": ["not sure", "reliable"],
                    },
                    {
                        "coach": "Why not?",
                        "hint": "Because it doesn't cite... / mention...",
                        "sample_answer": "Because it doesn't cite data or mention the author.",
                        "focus": "Give criteria",
                        "expected_keywords": ["doesn't", "cite"],
                    },
                    {
                        "coach": "What would you do next?",
                        "hint": "I'd check ...",
                        "sample_answer": "I'd check official reports or reputable news outlets before sharing.",
                        "focus": "Suggest verification",
                        "expected_keywords": ["I'd check", "official"],
                    },
                ],
                "target_phrases": ["I'm not sure it's reliable.", "Because it doesn't ...", "I'd check ..."],
            },
            "reading_support": "Reliable sources usually show evidence, cite data, and are transparent about authorship. If you're unsure, verify before sharing.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. I'm not sure this source is reliable.",
                "2. Because ...",
                "3. I'd check ...",
                "4. I trust sources that ...",
                "5. Let's verify it before sharing.",
                "6. Then we can decide.",
            ],
            "goal_examples": ["I'm not sure it's reliable.", "I'd check ...", "I trust sources that ..."],
        },
        {
            "lesson_key": "lesson-03-explaining-a-viewpoint",
            "slug": "explaining-a-viewpoint",
            "title": "Explaining a Viewpoint",
            "conversation_situation": "explaining_viewpoint",
            "conversation_goal": "Explain a viewpoint clearly, support it with one reason, and acknowledge another perspective.",
            "grammar_summary": "Use From my perspective... / The reason is... / I see the other side, but... to discuss viewpoints respectfully.",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Kamu diskusi isu publik. Kamu jelasin viewpoint kamu, kasih alasan, dan akui perspektif lain dengan sopan.",
            "dialogue": [
                ("Alex", "What's your take on regulating AI tools?"),
                ("Mina", "From my perspective, some regulation is necessary."),
                ("Alex", "Why?"),
                ("Mina", "The reason is it protects users from misuse and misinformation."),
                ("Alex", "But regulation could slow innovation."),
                ("Mina", "I see the other side, but basic safety rules can still support innovation."),
                ("Alex", "That's fair."),
                ("Mina", "We need balance."),
            ],
            "translations": [
                ("Alex", "What's your take on regulating AI tools?", "Menurut kamu soal regulasi AI gimana?"),
                ("Mina", "From my perspective, some regulation is necessary.", "Dari perspektifku, beberapa regulasi itu perlu."),
                ("Alex", "Why?", "Kenapa?"),
                ("Mina", "The reason is it protects users from misuse and misinformation.", "Alasannya itu melindungi user dari penyalahgunaan dan misinformasi."),
                ("Alex", "But regulation could slow innovation.", "Tapi regulasi bisa memperlambat inovasi."),
                ("Mina", "I see the other side, but basic safety rules can still support innovation.", "Aku paham sisi satunya, tapi aturan keamanan dasar tetap bisa mendukung inovasi."),
                ("Alex", "That's fair.", "Masuk akal."),
                ("Mina", "We need balance.", "Kita butuh keseimbangan."),
            ],
            "useful_phrases": [
                {
                    "phrase": "From my perspective, some regulation is necessary.",
                    "meaning_id": "Dari perspektifku, beberapa regulasi itu perlu.",
                    "usage_note": "A respectful viewpoint opener.",
                    "common_mistake": 'Do not say "From my perspective is"; use comma + sentence.',
                },
                {
                    "phrase": "The reason is it protects users from misinformation.",
                    "meaning_id": "Alasannya itu melindungi user dari misinformasi.",
                    "usage_note": "A clear reason structure.",
                    "common_mistake": 'Do not say "The reason it protects"; include is.',
                },
                {
                    "phrase": "I see the other side, but...",
                    "meaning_id": "Aku paham sisi satunya, tapi...",
                    "usage_note": "Acknowledge another perspective.",
                    "common_mistake": 'Do not dismiss the other side; acknowledge first.',
                },
                {
                    "phrase": "We need balance.",
                    "meaning_id": "Kita butuh keseimbangan.",
                    "usage_note": "A concise wrap-up sentence.",
                    "common_mistake": 'Do not over-explain; keep it short.',
                },
                {
                    "phrase": "That's fair.",
                    "meaning_id": "Itu masuk akal.",
                    "usage_note": "A polite response.",
                    "common_mistake": 'Do not say "That fair"; add is.',
                },
            ],
            "grammar_md": [
                ("Viewpoint language", ["From my perspective, ...", "The reason is ...", "I see the other side, but ..."]),
            ],
            "pronunciation": [
                ("perspective", "per-SPEK-tiv."),
                ("misinformation", "mis-in-fer-MAY-shun."),
                ("necessary", "NES-uh-ser-ee."),
            ],
            "response_prompts": [
                {
                    "prompt": "State your viewpoint.",
                    "target_response": "From my perspective, some regulation is necessary.",
                    "acceptable_variations": [
                        "From my perspective, some regulation is necessary.",
                        "From my perspective, transparency is important.",
                    ],
                },
                {
                    "prompt": "Support with a reason.",
                    "target_response": "The reason is it protects users from misinformation.",
                    "acceptable_variations": [
                        "The reason is it protects users from misinformation.",
                        "The reason is it reduces harm.",
                    ],
                },
                {
                    "prompt": "Acknowledge the other side politely.",
                    "target_response": "I see the other side, but we still need basic rules.",
                    "acceptable_variations": [
                        "I see the other side, but we still need basic rules.",
                        "I see your point, but I think balance is possible.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "perspective_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase introduces a viewpoint respectfully?",
                    "options": ["From my perspective, ...", "You're wrong.", "Obviously ..."],
                    "correct_answer": "From my perspective, ...",
                },
                {
                    "key": "acknowledge_other_side",
                    "type": "multiple_choice",
                    "prompt": "Which phrase acknowledges another perspective?",
                    "options": ["I see the other side, but...", "No.", "Stop."],
                    "correct_answer": "I see the other side, but...",
                },
                {
                    "key": "balance_meaning",
                    "type": "multiple_choice",
                    "prompt": 'What does "balance" mean?',
                    "options": ["keseimbangan", "kebisingan", "kekacauan"],
                    "correct_answer": "keseimbangan",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_info_viewpoint",
                "opening_line": "What's your viewpoint on this topic?",
                "learner_goal": "Explain a viewpoint with a reason and acknowledge another perspective.",
                "turns": [
                    {
                        "coach": "What's your take on this?",
                        "hint": "From my perspective, ...",
                        "sample_answer": "From my perspective, some regulation is necessary.",
                        "focus": "Viewpoint",
                        "expected_keywords": ["from my perspective"],
                    },
                    {
                        "coach": "Why?",
                        "hint": "The reason is ...",
                        "sample_answer": "The reason is it protects users from misuse and misinformation.",
                        "focus": "Reason",
                        "expected_keywords": ["the reason is"],
                    },
                    {
                        "coach": "I disagree. It could slow innovation.",
                        "hint": "Acknowledge: I see the other side, but...",
                        "sample_answer": "I see the other side, but basic safety rules can still support innovation.",
                        "focus": "Acknowledge + respond",
                        "expected_keywords": ["other side", "but"],
                    },
                ],
                "target_phrases": ["From my perspective, ...", "The reason is ...", "I see the other side, but ..."],
            },
            "reading_support": "When discussing viewpoints, be respectful: state your perspective, support it with a reason, and acknowledge the other side before responding.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. From my perspective, ...",
                "2. The reason is ...",
                "3. I see the other side, but ...",
                "4. We need balance.",
                "5. In my view, ...",
                "6. That's fair.",
            ],
            "goal_examples": ["From my perspective, ...", "The reason is ...", "I see the other side, but ..."],
        },
        {
            "lesson_key": "lesson-04-responding-to-new-information",
            "slug": "responding-to-new-information",
            "title": "Responding to New Information",
            "conversation_situation": "responding_to_new_information",
            "conversation_goal": "Respond to new information, update your opinion, and ask a follow-up question.",
            "grammar_summary": "Use I wasn't aware of that / That changes things / I'd like to understand... to respond thoughtfully.",
            "speakers": ("Mina", "Jordan"),
            "situation_id": "Kamu dapat info baru. Kamu respon dengan terbuka, update pendapat kamu, dan tanya pertanyaan follow-up.",
            "dialogue": [
                ("Jordan", "I found a report that contradicts the article we read."),
                ("Mina", "Oh, I wasn't aware of that."),
                ("Jordan", "It says the data sample was very small."),
                ("Mina", "That changes things. I'd like to understand the methodology."),
                ("Jordan", "We should check the full report."),
                ("Mina", "Agreed. Can you share the link?"),
                ("Jordan", "Sure, I'll send it after this."),
                ("Mina", "Thanks. Then we can revise our conclusion."),
            ],
            "translations": [
                ("Jordan", "I found a report that contradicts the article we read.", "Aku nemu laporan yang bertentangan sama artikel yang kita baca."),
                ("Mina", "Oh, I wasn't aware of that.", "Oh, aku belum tahu itu."),
                ("Jordan", "It says the data sample was very small.", "Katanya sampel datanya sangat kecil."),
                ("Mina", "That changes things. I'd like to understand the methodology.", "Itu mengubah situasinya. Aku pengen paham metodologinya."),
                ("Jordan", "We should check the full report.", "Kita harus cek laporan lengkapnya."),
                ("Mina", "Agreed. Can you share the link?", "Setuju. Bisa share link-nya?"),
                ("Jordan", "Sure, I'll send it after this.", "Bisa, aku kirim setelah ini."),
                ("Mina", "Thanks. Then we can revise our conclusion.", "Makasih. Habis itu kita bisa revisi kesimpulannya."),
            ],
            "useful_phrases": [
                {
                    "phrase": "I wasn't aware of that.",
                    "meaning_id": "Aku belum tahu itu.",
                    "usage_note": "A polite way to acknowledge new information.",
                    "common_mistake": 'Do not say "I wasn\'t know"; use wasn\'t aware.',
                },
                {
                    "phrase": "That changes things.",
                    "meaning_id": "Itu mengubah situasinya.",
                    "usage_note": "A natural reaction phrase.",
                    "common_mistake": 'Do not say "That change things"; add -s.',
                },
                {
                    "phrase": "I'd like to understand the methodology.",
                    "meaning_id": "Aku pengen paham metodologinya.",
                    "usage_note": "A thoughtful follow-up request.",
                    "common_mistake": 'Do not say "I want understand"; use I\'d like to.',
                },
                {
                    "phrase": "We should check the full report.",
                    "meaning_id": "Kita harus cek laporan lengkapnya.",
                    "usage_note": "A practical action step.",
                    "common_mistake": 'Do not say "should to check"; should + base verb.',
                },
                {
                    "phrase": "Then we can revise our conclusion.",
                    "meaning_id": "Lalu kita bisa revisi kesimpulannya.",
                    "usage_note": "A collaborative closing.",
                    "common_mistake": 'Do not say "revise to our conclusion"; revise our conclusion.',
                },
            ],
            "grammar_md": [
                ("New information phrases", ["I wasn't aware of that.", "That changes things.", "I'd like to understand ..."]),
            ],
            "pronunciation": [
                ("aware", "uh-WAIR."),
                ("methodology", "meth-uh-DOL-uh-jee."),
                ("contradicts", "kon-truh-DIKTS."),
            ],
            "response_prompts": [
                {
                    "prompt": "Acknowledge new info.",
                    "target_response": "I wasn't aware of that.",
                    "acceptable_variations": ["I wasn't aware of that.", "I didn't know that."],
                },
                {
                    "prompt": "Say it changes your view.",
                    "target_response": "That changes things.",
                    "acceptable_variations": ["That changes things.", "That changes my view."],
                },
                {
                    "prompt": "Ask to understand more.",
                    "target_response": "I'd like to understand the methodology.",
                    "acceptable_variations": [
                        "I'd like to understand the methodology.",
                        "I'd like to understand where the data came from.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "aware_phrase",
                    "type": "multiple_choice",
                    "prompt": "Which phrase acknowledges new information politely?",
                    "options": ["I wasn't aware of that.", "No way.", "You're lying."],
                    "correct_answer": "I wasn't aware of that.",
                },
                {
                    "key": "changes_things",
                    "type": "multiple_choice",
                    "prompt": "Choose the correct sentence.",
                    "options": ["That changes things.", "That change things.", "That changing things."],
                    "correct_answer": "That changes things.",
                },
                {
                    "key": "follow_up",
                    "type": "multiple_choice",
                    "prompt": "Which sentence asks for deeper understanding?",
                    "options": ["I'd like to understand the methodology.", "Stop.", "Whatever."],
                    "correct_answer": "I'd like to understand the methodology.",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_info_new_information",
                "opening_line": "I found new information about this topic.",
                "learner_goal": "Respond to new information, update your view, and ask a follow-up question.",
                "turns": [
                    {
                        "coach": "I found a report that contradicts what we read.",
                        "hint": "I wasn't aware of that.",
                        "sample_answer": "Oh, I wasn't aware of that.",
                        "focus": "Acknowledge",
                        "expected_keywords": ["aware"],
                    },
                    {
                        "coach": "It says the sample size was very small.",
                        "hint": "That changes things + request understanding.",
                        "sample_answer": "That changes things. I'd like to understand the methodology.",
                        "focus": "Update view + ask",
                        "expected_keywords": ["changes", "understand"],
                    },
                    {
                        "coach": "Agree on next steps.",
                        "hint": "We should check... Can you share... Then we can revise...",
                        "sample_answer": "We should check the full report. Can you share the link? Then we can revise our conclusion.",
                        "focus": "Next steps",
                        "expected_keywords": ["check", "share", "revise"],
                    },
                ],
                "target_phrases": ["I wasn't aware of that.", "That changes things.", "I'd like to understand ..."],
            },
            "reading_support": "When you get new information, respond openly. Acknowledge it, adjust your view, and ask a follow-up question to understand the details.",
            "writing_support_lines": [
                "Write 6 lines:",
                "1. I wasn't aware of that.",
                "2. That changes things.",
                "3. I'd like to understand ...",
                "4. We should check ...",
                "5. Can you share ...?",
                "6. Then we can revise ...",
            ],
            "goal_examples": ["I wasn't aware of that.", "That changes things.", "I'd like to understand ..."],
        },
        {
            "lesson_key": "lesson-05-information-discussion-mission",
            "slug": "information-discussion-mission",
            "title": "Information Discussion Mission",
            "conversation_situation": "mission_media_information_discussion",
            "conversation_goal": "Complete a discussion: summarize an article, evaluate source reliability, explain a viewpoint, and respond to new information with next steps.",
            "grammar_summary": "Combine: The article is about... / I'm not sure it's reliable / From my perspective... / That changes things / I'd like to understand...",
            "speakers": ("Mina", "Alex"),
            "situation_id": "Misi: kamu diskusi informasi. Kamu ringkas artikel, nilai sumber, jelasin viewpoint, lalu respon info baru dan tentuin langkah lanjut.",
            "dialogue": [
                ("Alex", "Can you summarize the article you read?"),
                ("Mina", "Sure. The article is about remote work and productivity. The main point is clear rules improve focus."),
                ("Alex", "Is the source reliable?"),
                ("Mina", "I'm not sure it's reliable because it doesn't cite data. I'd check official reports."),
                ("Alex", "What's your viewpoint overall?"),
                ("Mina", "From my perspective, hybrid work is a good balance. The reason is it supports focus and connection."),
                ("Alex", "I found a report that contradicts it. The sample size was small."),
                ("Mina", "I wasn't aware of that. That changes things. I'd like to understand the methodology. Can you share the link so we can revise our conclusion?"),
            ],
            "translations": [
                ("Alex", "Can you summarize the article you read?", "Bisa ringkas artikel yang kamu baca?"),
                ("Mina", "Sure. The article is about remote work and productivity. The main point is clear rules improve focus.", "Bisa. Artikelnya tentang kerja remote dan produktivitas. Poin utamanya aturan yang jelas bikin fokus lebih baik."),
                ("Alex", "Is the source reliable?", "Sumbernya reliable?"),
                ("Mina", "I'm not sure it's reliable because it doesn't cite data. I'd check official reports.", "Aku nggak yakin reliable karena nggak nyantumin data. Aku bakal cek laporan resmi."),
                ("Alex", "What's your viewpoint overall?", "Secara umum viewpoint kamu apa?"),
                ("Mina", "From my perspective, hybrid work is a good balance. The reason is it supports focus and connection.", "Dari perspektifku, kerja hybrid itu balance yang bagus. Alasannya itu mendukung fokus dan koneksi."),
                ("Alex", "I found a report that contradicts it. The sample size was small.", "Aku nemu laporan yang bertentangan. Sampel datanya kecil."),
                ("Mina", "I wasn't aware of that. That changes things. I'd like to understand the methodology. Can you share the link so we can revise our conclusion?", "Aku belum tahu itu. Itu mengubah situasinya. Aku pengen paham metodologinya. Bisa share link-nya supaya kita bisa revisi kesimpulannya?"),
            ],
            "useful_phrases": [
                {
                    "phrase": "The article is about ... The main point is ...",
                    "meaning_id": "Artikelnya tentang ... Poin utamanya ...",
                    "usage_note": "A compact summary structure.",
                    "common_mistake": "Do not over-explain; keep it to 2 sentences.",
                },
                {
                    "phrase": "I'm not sure it's reliable because it doesn't cite data.",
                    "meaning_id": "Aku nggak yakin reliable karena nggak nyantumin data.",
                    "usage_note": "Reliability + reason.",
                    "common_mistake": "Avoid personal attacks; focus on evidence.",
                },
                {
                    "phrase": "From my perspective, ... The reason is ...",
                    "meaning_id": "Dari perspektifku, ... Alasannya ...",
                    "usage_note": "Viewpoint + reason.",
                    "common_mistake": "Acknowledge another view if needed.",
                },
                {
                    "phrase": "I wasn't aware of that. That changes things.",
                    "meaning_id": "Aku belum tahu itu. Itu mengubah situasinya.",
                    "usage_note": "Open reaction to new info.",
                    "common_mistake": "Don't dismiss new info; accept it calmly.",
                },
                {
                    "phrase": "Can you share the link so we can revise our conclusion?",
                    "meaning_id": "Bisa share link-nya supaya kita bisa revisi kesimpulan?",
                    "usage_note": "A clear next step request.",
                    "common_mistake": "Ask for a concrete next step.",
                },
            ],
            "grammar_md": [
                (
                    "Information discussion flow",
                    [
                        "The article is about ... The main point is ...",
                        "I'm not sure it's reliable because ... I'd check ...",
                        "From my perspective, ... The reason is ...",
                        "That changes things. I'd like to understand ...",
                    ],
                ),
            ],
            "pronunciation": [
                ("reliable", "ri-LYE-uh-bul."),
                ("methodology", "meth-uh-DOL-uh-jee."),
                ("conclusion", "kun-KLOO-zhun."),
            ],
            "response_prompts": [
                {
                    "prompt": "Summarize the article in two sentences.",
                    "target_response": "The article is about remote work and productivity. The main point is clear rules improve focus.",
                    "acceptable_variations": [
                        "The article is about remote work and productivity. The main point is clear rules improve focus.",
                        "The article is about AI regulation. The main point is safety matters.",
                    ],
                },
                {
                    "prompt": "Evaluate reliability and suggest verification.",
                    "target_response": "I'm not sure it's reliable because it doesn't cite data. I'd check official reports.",
                    "acceptable_variations": [
                        "I'm not sure it's reliable because it doesn't cite data. I'd check official reports.",
                        "I trust it because it cites sources. I'd still cross-check with another report.",
                    ],
                },
                {
                    "prompt": "Respond to new information with next steps.",
                    "target_response": "I wasn't aware of that. That changes things. Can you share the link so we can revise our conclusion?",
                    "acceptable_variations": [
                        "I wasn't aware of that. That changes things. Can you share the link so we can revise our conclusion?",
                        "I wasn't aware of that. That changes my view. Let's check the report and update our summary.",
                    ],
                },
            ],
            "quiz": [
                {
                    "key": "mission_info_flow",
                    "type": "multiple_choice",
                    "prompt": "Which flow fits an information discussion?",
                    "options": [
                        "Summary -> reliability -> viewpoint -> new information response",
                        "Greeting -> goodbye",
                        "Numbers -> colors",
                    ],
                    "correct_answer": "Summary -> reliability -> viewpoint -> new information response",
                },
                {
                    "key": "not_sure_reliable",
                    "type": "multiple_choice",
                    "prompt": "Which sentence expresses doubt about a source?",
                    "options": ["I'm not sure it's reliable.", "It's always true.", "Share it now."],
                    "correct_answer": "I'm not sure it's reliable.",
                },
                {
                    "key": "changes_things_mission",
                    "type": "multiple_choice",
                    "prompt": "Which phrase reacts to new information?",
                    "options": ["That changes things.", "That's irrelevant.", "Stop."],
                    "correct_answer": "That changes things.",
                },
            ],
            "roleplay": {
                "scenario_key": "b2_info_mission",
                "opening_line": "Let's discuss an article and evaluate the information.",
                "learner_goal": "Discuss information critically: summary, reliability, viewpoint, and response to new info.",
                "turns": [
                    {
                        "coach": "Summarize the article briefly.",
                        "hint": "The article is about... The main point is...",
                        "sample_answer": "The article is about remote work and productivity. The main point is clear rules improve focus.",
                        "focus": "Summary",
                        "expected_keywords": ["article is about", "main point"],
                    },
                    {
                        "coach": "Is the source reliable? Explain why and what you'd check.",
                        "hint": "I'm not sure it's reliable because... I'd check...",
                        "sample_answer": "I'm not sure it's reliable because it doesn't cite data. I'd check official reports or reputable outlets.",
                        "focus": "Reliability",
                        "expected_keywords": ["reliable", "because", "I'd check"],
                    },
                    {
                        "coach": "Now respond to new contradictory information and propose next steps.",
                        "hint": "I wasn't aware... That changes things... I'd like to understand... Can you share...?",
                        "sample_answer": "I wasn't aware of that. That changes things. I'd like to understand the methodology. Can you share the link so we can revise our conclusion?",
                        "focus": "New info + next steps",
                        "expected_keywords": ["aware", "changes", "understand", "share"],
                    },
                ],
                "target_phrases": ["The article is about ...", "I'm not sure it's reliable ...", "That changes things."],
            },
            "reading_support": "In information discussions, focus on structure and evidence. Summarize clearly, evaluate source reliability, explain viewpoints respectfully, and update your view when new information appears.",
            "writing_support_lines": [
                "Write your mission (10 lines):",
                "1. The article is about ...",
                "2. The main point is ...",
                "3. I'm not sure it's reliable because ...",
                "4. I'd check ...",
                "5. From my perspective, ...",
                "6. The reason is ...",
                "7. I wasn't aware of that.",
                "8. That changes things.",
                "9. I'd like to understand ...",
                "10. Can you share the link so we can revise ...?",
            ],
            "goal_examples": ["The article is about ...", "I'm not sure it's reliable ...", "From my perspective, ..."],
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

