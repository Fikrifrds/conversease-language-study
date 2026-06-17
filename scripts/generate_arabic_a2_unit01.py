#!/usr/bin/env python3
"""Generate Arabic A2 Unit 1 pilot content.

Arabic A1 is the quality baseline. This script intentionally creates only the
first A2 unit so the team can review quality before scaling the rest of A2.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
A2_ROOT = REPO_ROOT / "content" / "curriculum" / "arabic" / "A2"
UNITS_ROOT = A2_ROOT / "units"
TRACKER_PATH = REPO_ROOT / "content" / "production_tracker.csv"
CONTENT_PLAN_PATH = A2_ROOT / "content_plan.yaml"

REQUIRED_SECTIONS = [
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

TEXT_TRACKER_COLUMNS = [
    "lesson_md",
    "listening_script",
    "phrases",
    "grammar",
    "pronunciation",
    "response_prompts",
    "conversation_coach",
    "quiz",
    "reading",
    "writing",
]


def phrase(text: str, meaning: str, usage: str) -> dict[str, str]:
    return {"phrase": text, "meaning": meaning, "usage": usage}


def line(speaker: str, text: str, translation: str) -> tuple[str, str, str]:
    return (speaker, text, translation)


UNIT = {
    "unit_key": "unit-01-social-follow-up",
    "title": "Social Follow-up",
    "status": "beta",
    "main_conversation_outcome": (
        "Keep a short Fusha conversation going with follow-up questions, reactions, "
        "and simple personal details."
    ),
    "lessons": [
        {
            "lesson_key": "lesson-01-reconnecting-after-class",
            "slug": "arabic-reconnecting-after-class",
            "title": "Reconnecting After Class",
            "status": "beta",
            "situation": (
                "Kamu bertemu teman setelah kelas bahasa Arab dan membuka percakapan "
                "singkat dengan kabar, kelas, dan rencana belajar."
            ),
            "goal": (
                "Start a short follow-up conversation after class and answer with one "
                "simple detail."
            ),
            "grammar": (
                "Gunakan pertanyaan kabar, jawaban pendek, dan satu detail tambahan "
                "dengan pola: أَنَا بِخَيْرٍ، وَ..."
            ),
            "patterns": [
                "كَيْفَ حَالُكَ؟",
                "أَنَا بِخَيْرٍ، وَأَنْتَ؟",
                "كَانَ الدَّرْسُ جَيِّدًا.",
                "سَأُرَاجِعُ الْكَلِمَاتِ.",
            ],
            "phrases": [
                phrase("كَيْفَ حَالُكَ؟", "Apa kabarmu?", "Membuka percakapan setelah bertemu lagi."),
                phrase("أَنَا بِخَيْرٍ، وَأَنْتَ؟", "Saya baik, dan kamu?", "Menjawab kabar lalu bertanya balik."),
                phrase("كَانَ الدَّرْسُ جَيِّدًا.", "Pelajarannya bagus.", "Memberi komentar pendek tentang kelas."),
                phrase("سَأُرَاجِعُ الْكَلِمَاتِ.", "Saya akan mengulang kosakata.", "Menyebut rencana belajar dekat."),
                phrase("إِلَى اللِّقَاءِ غَدًا.", "Sampai bertemu besok.", "Menutup percakapan dengan sopan."),
            ],
            "dialogue": [
                line("Khalid", "السَّلَامُ عَلَيْكِ يَا مَرْيَمُ.", "Assalamu'alaikum, Maryam."),
                line("Maryam", "وَعَلَيْكُمُ السَّلَامُ يَا خَالِدُ. كَيْفَ حَالُكَ؟", "Wa'alaikumussalam, Khalid. Apa kabarmu?"),
                line("Khalid", "أَنَا بِخَيْرٍ، وَأَنْتِ؟", "Saya baik, dan kamu?"),
                line("Maryam", "أَنَا بِخَيْرٍ. كَانَ الدَّرْسُ جَيِّدًا.", "Saya baik. Pelajarannya bagus."),
                line("Khalid", "نَعَمْ، وَسَأُرَاجِعُ الْكَلِمَاتِ الْيَوْمَ.", "Ya, dan saya akan mengulang kosakata hari ini."),
                line("Maryam", "جَيِّدٌ. إِلَى اللِّقَاءِ غَدًا.", "Bagus. Sampai bertemu besok."),
            ],
        },
        {
            "lesson_key": "lesson-02-asking-follow-up-questions",
            "slug": "arabic-asking-follow-up-questions",
            "title": "Asking Follow-up Questions",
            "status": "beta",
            "situation": (
                "Kamu berbicara dengan teman kelas dan menjaga percakapan tetap berjalan "
                "dengan pertanyaan lanjutan yang sederhana."
            ),
            "goal": "Ask one follow-up question and respond with a short reason.",
            "grammar": (
                "Gunakan pertanyaan lanjutan dengan مَاذَا dan لِمَاذَا, lalu jawab "
                "dengan alasan pendek memakai لِأَنَّ."
            ),
            "patterns": [
                "مَاذَا تَفْعَلُ بَعْدَ الدَّرْسِ؟",
                "لِمَاذَا؟",
                "لِأَنَّنِي أُرِيدُ أَنْ أَتَدَرَّبَ.",
                "هَذَا جَيِّدٌ.",
            ],
            "phrases": [
                phrase("مَاذَا تَفْعَلُ بَعْدَ الدَّرْسِ؟", "Apa yang kamu lakukan setelah pelajaran?", "Membuka pertanyaan lanjutan."),
                phrase("لِمَاذَا؟", "Mengapa?", "Meminta alasan secara singkat."),
                phrase("لِأَنَّنِي أُرِيدُ أَنْ أَتَدَرَّبَ.", "Karena saya ingin berlatih.", "Memberi alasan pendek."),
                phrase("هَذَا جَيِّدٌ.", "Itu bagus.", "Memberi reaksi sederhana."),
                phrase("وَأَنْتَ؟", "Dan kamu?", "Mengembalikan pertanyaan."),
            ],
            "dialogue": [
                line("Layla", "مَاذَا تَفْعَلُ بَعْدَ الدَّرْسِ؟", "Apa yang kamu lakukan setelah pelajaran?"),
                line("Zayd", "سَأَذْهَبُ إِلَى الْمَكْتَبَةِ.", "Saya akan pergi ke perpustakaan."),
                line("Layla", "لِمَاذَا؟", "Mengapa?"),
                line("Zayd", "لِأَنَّنِي أُرِيدُ أَنْ أَتَدَرَّبَ عَلَى الْقِرَاءَةِ.", "Karena saya ingin berlatih membaca."),
                line("Layla", "هَذَا جَيِّدٌ. أَنَا سَأَكْتُبُ الْوَاجِبَ.", "Itu bagus. Saya akan menulis tugas."),
                line("Zayd", "جَمِيلٌ. وَهَلْ تَحْتَاجِينَ إِلَى مُسَاعَدَةٍ؟", "Bagus. Apakah kamu butuh bantuan?"),
                line("Layla", "لَا، شُكْرًا. الْوَاجِبُ سَهْلٌ.", "Tidak, terima kasih. Tugasnya mudah."),
            ],
        },
        {
            "lesson_key": "lesson-03-talking-about-the-weekend",
            "slug": "arabic-talking-about-the-weekend",
            "title": "Talking About the Weekend",
            "status": "beta",
            "situation": (
                "Kamu menceritakan kegiatan akhir pekan secara pendek: ke mana pergi, "
                "dengan siapa, dan bagaimana rasanya."
            ),
            "goal": "Talk about a simple weekend activity using short past-tense phrases.",
            "grammar": (
                "Gunakan bentuk lampau sederhana seperti ذَهَبْتُ dan كَانَ untuk "
                "menceritakan pengalaman pendek."
            ),
            "patterns": [
                "مَاذَا فَعَلْتَ فِي نِهَايَةِ الْأُسْبُوعِ؟",
                "ذَهَبْتُ إِلَى ...",
                "كَانَ الْمَكَانُ جَمِيلًا.",
                "مَعَ أُسْرَتِي.",
            ],
            "phrases": [
                phrase("مَاذَا فَعَلْتَ فِي نِهَايَةِ الْأُسْبُوعِ؟", "Apa yang kamu lakukan pada akhir pekan?", "Menanyakan pengalaman akhir pekan."),
                phrase("ذَهَبْتُ إِلَى الْحَدِيقَةِ.", "Saya pergi ke taman.", "Menceritakan tempat yang dikunjungi."),
                phrase("مَعَ أُسْرَتِي.", "Bersama keluarga saya.", "Menjawab dengan siapa."),
                phrase("كَانَ الْمَكَانُ جَمِيلًا.", "Tempatnya indah.", "Memberi komentar sederhana."),
                phrase("وَمَاذَا فَعَلْتِ أَنْتِ؟", "Dan apa yang kamu lakukan?", "Mengembalikan topik."),
            ],
            "dialogue": [
                line("Omar", "مَاذَا فَعَلْتِ فِي نِهَايَةِ الْأُسْبُوعِ؟", "Apa yang kamu lakukan pada akhir pekan?"),
                line("Noura", "ذَهَبْتُ إِلَى الْحَدِيقَةِ مَعَ أُسْرَتِي.", "Saya pergi ke taman bersama keluarga saya."),
                line("Omar", "هَلْ كَانَ الْمَكَانُ جَمِيلًا؟", "Apakah tempatnya indah?"),
                line("Noura", "نَعَمْ، كَانَ الْمَكَانُ جَمِيلًا وَهَادِئًا.", "Ya, tempatnya indah dan tenang."),
                line("Omar", "جَيِّدٌ. أَنَا ذَهَبْتُ إِلَى السُّوقِ.", "Bagus. Saya pergi ke pasar."),
                line("Noura", "وَمَاذَا اشْتَرَيْتَ؟", "Dan apa yang kamu beli?"),
                line("Omar", "اشْتَرَيْتُ كِتَابًا صَغِيرًا.", "Saya membeli buku kecil."),
            ],
        },
        {
            "lesson_key": "lesson-04-reacting-with-interest",
            "slug": "arabic-reacting-with-interest",
            "title": "Reacting With Interest",
            "status": "beta",
            "situation": (
                "Kamu merespons cerita teman dengan ekspresi pendek yang sopan, lalu "
                "bertanya satu pertanyaan lanjutan."
            ),
            "goal": "React politely and ask one short question to show interest.",
            "grammar": (
                "Gunakan reaksi pendek seperti حَقًّا؟ dan مُمْتَازٌ, lalu lanjutkan "
                "dengan pertanyaan sederhana."
            ),
            "patterns": [
                "حَقًّا؟",
                "هَذَا مُمْتَازٌ.",
                "كَيْفَ كَانَ ...؟",
                "أُرِيدُ أَنْ أَزُورَ ذَلِكَ الْمَكَانَ.",
            ],
            "phrases": [
                phrase("حَقًّا؟", "Benarkah?", "Menunjukkan tertarik pada cerita."),
                phrase("هَذَا مُمْتَازٌ.", "Itu luar biasa.", "Memberi reaksi positif."),
                phrase("كَيْفَ كَانَ الْمَكَانُ؟", "Bagaimana tempatnya?", "Bertanya lanjutan."),
                phrase("كَانَ نَظِيفًا وَهَادِئًا.", "Tempatnya bersih dan tenang.", "Menjawab dengan dua sifat."),
                phrase("أُرِيدُ أَنْ أَزُورَ ذَلِكَ الْمَكَانَ.", "Saya ingin mengunjungi tempat itu.", "Menunjukkan minat."),
            ],
            "dialogue": [
                line("Sara", "ذَهَبْتُ إِلَى مَكْتَبَةٍ جَدِيدَةٍ أَمْسِ.", "Saya pergi ke perpustakaan baru kemarin."),
                line("Adi", "حَقًّا؟ كَيْفَ كَانَ الْمَكَانُ؟", "Benarkah? Bagaimana tempatnya?"),
                line("Sara", "كَانَ نَظِيفًا وَهَادِئًا.", "Tempatnya bersih dan tenang."),
                line("Adi", "هَذَا مُمْتَازٌ. هَلْ هِيَ قَرِيبَةٌ؟", "Itu luar biasa. Apakah dekat?"),
                line("Sara", "نَعَمْ، هِيَ قَرِيبَةٌ مِنَ الْمَرْكَزِ.", "Ya, dekat dari pusat."),
                line("Adi", "أُرِيدُ أَنْ أَزُورَ ذَلِكَ الْمَكَانَ.", "Saya ingin mengunjungi tempat itu."),
            ],
        },
        {
            "lesson_key": "lesson-05-social-follow-up-mission",
            "slug": "arabic-social-follow-up-mission",
            "title": "Social Follow-up Mission",
            "status": "beta",
            "situation": (
                "Kamu menjaga percakapan singkat dengan teman: membuka kabar, menanyakan "
                "kegiatan, memberi reaksi, dan menutup dengan rencana sederhana."
            ),
            "goal": "Combine greeting, follow-up questions, reactions, and one simple future plan.",
            "grammar": (
                "Gabungkan salam, pertanyaan lanjutan, alasan pendek, dan rencana dekat "
                "dengan سَـ."
            ),
            "patterns": [
                "كَيْفَ حَالُكَ؟",
                "مَاذَا فَعَلْتَ أَمْسِ؟",
                "هَذَا جَيِّدٌ.",
                "سَنَتَحَدَّثُ غَدًا.",
            ],
            "phrases": [
                phrase("كَيْفَ حَالُكَ؟", "Apa kabarmu?", "Membuka percakapan."),
                phrase("مَاذَا فَعَلْتَ أَمْسِ؟", "Apa yang kamu lakukan kemarin?", "Menanyakan pengalaman lampau."),
                phrase("هَذَا جَيِّدٌ.", "Itu bagus.", "Memberi reaksi."),
                phrase("لِأَنَّنِي أُرِيدُ أَنْ أَتَعَلَّمَ.", "Karena saya ingin belajar.", "Memberi alasan pendek."),
                phrase("سَنَتَحَدَّثُ غَدًا.", "Kita akan berbicara besok.", "Menutup dengan rencana."),
            ],
            "dialogue": [
                line("Maryam", "السَّلَامُ عَلَيْكَ يَا أَحْمَدُ. كَيْفَ حَالُكَ؟", "Assalamu'alaikum, Ahmad. Apa kabarmu?"),
                line("Ahmad", "وَعَلَيْكُمُ السَّلَامُ. أَنَا بِخَيْرٍ، وَأَنْتِ؟", "Wa'alaikumussalam. Saya baik, dan kamu?"),
                line("Maryam", "أَنَا بِخَيْرٍ. مَاذَا فَعَلْتَ أَمْسِ؟", "Saya baik. Apa yang kamu lakukan kemarin?"),
                line("Ahmad", "ذَهَبْتُ إِلَى الْمَكْتَبَةِ وَقَرَأْتُ كِتَابًا.", "Saya pergi ke perpustakaan dan membaca buku."),
                line("Maryam", "هَذَا جَيِّدٌ. لِمَاذَا قَرَأْتَ الْكِتَابَ؟", "Itu bagus. Mengapa kamu membaca buku itu?"),
                line("Ahmad", "لِأَنَّنِي أُرِيدُ أَنْ أَتَعَلَّمَ كَلِمَاتٍ جَدِيدَةً.", "Karena saya ingin belajar kata-kata baru."),
                line("Maryam", "جَمِيلٌ. سَنَتَحَدَّثُ غَدًا عَنِ الْكِتَابِ.", "Bagus. Kita akan berbicara besok tentang buku itu."),
                line("Ahmad", "نَعَمْ، إِلَى اللِّقَاءِ غَدًا.", "Ya, sampai bertemu besok."),
            ],
        },
    ],
}


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def lesson_plan_entries() -> list[dict[str, str]]:
    return [
        {
            "lesson_key": item["lesson_key"],
            "slug": item["slug"],
            "title": item["title"],
            "status": item["status"],
        }
        for item in UNIT["lessons"]
    ]


def update_content_plan() -> None:
    plan = yaml.safe_load(CONTENT_PLAN_PATH.read_text(encoding="utf-8"))
    for unit in plan.get("units", []):
        if unit.get("unit_key") != UNIT["unit_key"]:
            continue
        unit["status"] = UNIT["status"]
        unit["main_conversation_outcome"] = UNIT["main_conversation_outcome"]
        unit["lessons"] = lesson_plan_entries()
    write_yaml(CONTENT_PLAN_PATH, plan)


def write_unit() -> None:
    unit_dir = UNITS_ROOT / UNIT["unit_key"]
    unit_dir.mkdir(parents=True, exist_ok=True)
    write_yaml(
        unit_dir / "unit.yaml",
        {
            "unit_key": UNIT["unit_key"],
            "level_code": "A2",
            "title": UNIT["title"],
            "main_conversation_outcome": UNIT["main_conversation_outcome"],
            "status": UNIT["status"],
            "lessons": [item["lesson_key"] for item in UNIT["lessons"]],
        },
    )


def learner_goal(item: dict[str, Any]) -> str:
    return f"Latih percakapan Arab A2 untuk situasi ini: {item['situation']}"


def usage_note(entry: dict[str, str]) -> str:
    return f"Gunakan saat ingin mengatakan: {entry['meaning']}"


def focus_note(entry: dict[str, str]) -> str:
    return f"Latihan frasa: {entry['meaning']}"


def phrase_options(phrases: list[dict[str, str]], correct_index: int) -> list[str]:
    correct = phrases[correct_index]["phrase"]
    options = [correct]
    for entry in phrases:
        candidate = entry["phrase"]
        if candidate not in options:
            options.append(candidate)
        if len(options) == 3:
            break
    return options


def roleplay_payload(item: dict[str, Any]) -> dict[str, Any]:
    turns = []
    for index, entry in enumerate(item["phrases"][:3], 1):
        turns.append(
            {
                "coach": item["dialogue"][0][1] if index == 1 else f"استخدم: {entry['phrase']}",
                "hint": f"Jawab dengan pola: {entry['phrase']}",
                "sample_answer": entry["phrase"],
                "focus": focus_note(entry),
                "expected_keywords": entry["phrase"].replace("؟", "").replace(".", "").split()[:3],
                "indonesian_explanation": entry["meaning"],
            }
        )
    return {
        "scenario_key": item["slug"].replace("arabic-", "arabic_").replace("-", "_"),
        "mode": "lesson_practice_coach",
        "level_code": "A2",
        "opening_line": item["dialogue"][0][1],
        "learner_goal": learner_goal(item),
        "max_turns": 5,
        "feedback_level": {"free": "basic", "pro": "detailed"},
        "turns": turns,
        "target_phrases": [entry["phrase"] for entry in item["phrases"][:4]],
        "rubric": {
            "speaking": {"minimum_score": 65},
            "relevance": {"minimum_score": 65},
            "grammar": {"minimum_score": 60},
        },
    }


def write_lesson_files(item: dict[str, Any]) -> None:
    lesson_dir = UNITS_ROOT / UNIT["unit_key"] / item["lesson_key"]
    lesson_dir.mkdir(parents=True, exist_ok=True)

    write_yaml(
        lesson_dir / "lesson.yaml",
        {
            "lesson_key": item["lesson_key"],
            "slug": item["slug"],
            "title": item["title"],
            "status": item["status"],
            "estimated_minutes": 12,
            "conversation_situation": item["slug"].replace("arabic-", "").replace("-", "_"),
            "conversation_goal": learner_goal(item),
            "grammar_summary": item["grammar"],
            "required_sections": REQUIRED_SECTIONS,
            "completion_rules": {
                "listening_completed": True,
                "quiz_required": True,
                "speaking_attempt_required": True,
                "minimum_score": 65,
            },
        },
    )

    (lesson_dir / "lesson.md").write_text(
        f"# {item['title']}\n\n"
        "Setelah lesson ini, kamu bisa menjaga percakapan Fusha pendek dengan lebih alami.\n\n"
        "## Situation\n\n"
        f"{item['situation']}\n\n"
        "## Catatan Belajar\n\n"
        "A2 tetap memakai kalimat pendek, tetapi kamu mulai menambahkan alasan, reaksi, "
        "atau satu detail tambahan. Jaga ucapan tetap pelan dan jelas.\n",
        encoding="utf-8",
    )

    (lesson_dir / "conversation_goal.md").write_text(
        f"# Target Percakapan\n\n{learner_goal(item)}\n\n"
        "Kamu akan berlatih mengatakan:\n\n"
        + "\n".join(f"- {entry['phrase']}" for entry in item["phrases"][:5])
        + "\n",
        encoding="utf-8",
    )

    (lesson_dir / "listening_script.md").write_text(
        "# Listening Script\n\n"
        + "\n".join(f"**{speaker}:** {text}" for speaker, text, _ in item["dialogue"])
        + "\n\n## Audio Direction\n\n"
        "Use Arabic only. Speaker labels are metadata and must not be spoken. "
        "Keep a calm pace with a short natural pause between speakers. "
        "Use distinct male/female voices according to speaker names.\n",
        encoding="utf-8",
    )

    (lesson_dir / "transcript_translation.md").write_text(
        "# Transcript Translation\n\n"
        + "\n".join(
            f"- **{speaker}:** {text} -> {translation}"
            for speaker, text, translation in item["dialogue"]
        )
        + "\n",
        encoding="utf-8",
    )

    write_yaml(
        lesson_dir / "useful_phrases.yaml",
        {
            "phrases": [
                {
                    "phrase": entry["phrase"],
                    "meaning_id": entry["meaning"],
                    "usage_note": usage_note(entry),
                }
                for entry in item["phrases"]
            ]
        },
    )

    (lesson_dir / "grammar_for_conversation.md").write_text(
        "# Pola Percakapan\n\n"
        f"{item['grammar']}\n\n"
        "```txt\n"
        + "\n".join(item["patterns"])
        + "\n```\n\n"
        "Di A2, cukup tambahkan satu alasan, satu reaksi, atau satu detail. Jangan membuat "
        "jawaban terlalu panjang sebelum pola inti terasa stabil.\n",
        encoding="utf-8",
    )

    (lesson_dir / "pronunciation_drill.md").write_text(
        "# Latihan Pengucapan\n\n## Ulangi\n\n"
        + "\n".join(f"{index}. {entry['phrase']}" for index, entry in enumerate(item["phrases"][:5], 1))
        + "\n\n## Fokus\n\n"
        "- Jaga panjang pendek vokal Arab.\n"
        "- Ucapkan akhir kata yang diberi harakat dengan jelas.\n"
        "- Beri jeda pendek setelah pertanyaan lanjutan.\n",
        encoding="utf-8",
    )

    write_yaml(
        lesson_dir / "response_prompts.yaml",
        {
            "prompts": [
                {
                    "prompt": f"Ucapkan dalam bahasa Arab: {entry['meaning']}",
                    "target_response": entry["phrase"],
                    "acceptable_responses": [entry["phrase"]],
                }
                for entry in item["phrases"][:3]
            ]
        },
    )

    write_yaml(
        lesson_dir / "quiz.yaml",
        {
            "questions": [
                {
                    "key": f"phrase_{index}",
                    "prompt": f"Frasa mana yang berarti \"{entry['meaning']}\"?",
                    "options": phrase_options(item["phrases"], index - 1),
                    "correct_answer": entry["phrase"],
                }
                for index, entry in enumerate(item["phrases"][:2], 1)
            ]
        },
    )

    write_yaml(lesson_dir / "conversation_coach_roleplay.yaml", roleplay_payload(item))

    (lesson_dir / "reading_support.md").write_text(
        "# Bantuan Membaca\n\n"
        "Baca frasa Arab dari kanan ke kiri. Kenali pola utuhnya dulu, lalu perhatikan "
        "kata tanya, alasan, atau kata kerja lampau/dekat.\n\n"
        + "\n".join(f"- {entry['phrase']} -> {entry['meaning']}" for entry in item["phrases"][:5])
        + "\n",
        encoding="utf-8",
    )

    (lesson_dir / "writing_support.md").write_text(
        "# Bantuan Menulis\n\n"
        "Salin frasa berikut. Setelah itu, ganti satu bagian saja, misalnya tempat, waktu, "
        "atau aktivitas.\n\n"
        + "\n".join(f"- {entry['phrase']}" for entry in item["phrases"][:4])
        + "\n",
        encoding="utf-8",
    )

    write_yaml(
        lesson_dir / "audio_manifest.yaml",
        {
            "lesson_key": item["lesson_key"],
            "status": "not_generated",
            "provider": "elevenlabs",
            "model": "eleven_v3",
            "default_voice_id": "multi_speaker",
            "assets": [],
        },
    )


def update_tracker() -> None:
    with TRACKER_PATH.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    rows_by_key = {(row["level"], row["unit"], row["lesson"]): row for row in rows}
    for item in UNIT["lessons"]:
        key = ("arabic/A2", UNIT["unit_key"], item["lesson_key"])
        row = rows_by_key.get(key)
        if row is None:
            row = {name: "" for name in fieldnames}
            row["level"], row["unit"], row["lesson"] = key
            rows.append(row)
            rows_by_key[key] = row
        for column in TEXT_TRACKER_COLUMNS:
            row[column] = "done"
        row["audio_generated"] = "not_generated"
        row["review_status"] = ""
        row["publish_status"] = "beta"

    with TRACKER_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    update_content_plan()
    write_unit()
    for item in UNIT["lessons"]:
        write_lesson_files(item)
    update_tracker()
    print("Generated Arabic A2 Unit 1 pilot content.")


if __name__ == "__main__":
    main()
