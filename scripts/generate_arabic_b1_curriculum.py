#!/usr/bin/env python3
"""Generate Arabic B1 curriculum content.

Arabic A1/A2 are the style baseline. B1 keeps the same file layout, but moves
from short exchanges into connected explanations: stories, work updates,
problems, travel situations, goals, preferences, community, and final review.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

import yaml

from generate_arabic_vocabulary import vocabulary_for_lesson


REPO_ROOT = Path(__file__).resolve().parents[1]
B1_ROOT = REPO_ROOT / "content" / "curriculum" / "arabic" / "B1"
UNITS_ROOT = B1_ROOT / "units"
TRACKER_PATH = REPO_ROOT / "content" / "production_tracker.csv"
CONTENT_PLAN_PATH = B1_ROOT / "content_plan.yaml"

REQUIRED_SECTIONS = [
    "conversation_goal",
    "situation_setup",
    "listening",
    "comprehension_check",
    "useful_phrases",
    "vocabulary",
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


def lesson(
    key: str,
    slug: str,
    title: str,
    situation: str,
    goal: str,
    grammar: str,
    patterns: list[str],
    phrases: list[dict[str, str]],
    speakers: tuple[str, str],
    opening: tuple[str, str],
) -> dict[str, Any]:
    speaker_a, speaker_b = speakers
    opening_ar, opening_id = opening
    dialogue = [
        line(speaker_a, opening_ar, opening_id),
        line(speaker_b, phrases[0]["phrase"], phrases[0]["meaning"]),
        line(speaker_a, "هَلْ يُمْكِنُ أَنْ تُوَضِّحَ أَكْثَرَ؟", "Bisakah kamu menjelaskan lebih banyak?"),
        line(speaker_b, f"{phrases[1]['phrase']} {phrases[2]['phrase']}", f"{phrases[1]['meaning']} {phrases[2]['meaning']}"),
        line(speaker_a, phrases[3]["phrase"], phrases[3]["meaning"]),
        line(speaker_b, phrases[4]["phrase"], phrases[4]["meaning"]),
    ]
    return {
        "lesson_key": key,
        "slug": slug,
        "title": title,
        "status": "published",
        "situation": situation,
        "goal": goal,
        "grammar": grammar,
        "patterns": patterns,
        "phrases": phrases,
        "dialogue": dialogue,
    }


UNITS: list[dict[str, Any]] = [
    {
        "unit_key": "unit-01-personal-stories",
        "title": "Personal Stories",
        "main_conversation_outcome": "Tell connected personal stories with time, place, sequence, feeling, and follow-up details.",
        "speakers": ("Ahmad", "Karim"),
        "lessons": [
            lesson(
                "lesson-01-setting-the-scene",
                "arabic-b1-setting-the-scene",
                "Setting the Scene",
                "Kamu membuka cerita pendek dengan waktu, tempat, dan orang yang terlibat sebelum masuk ke kejadian utama.",
                "Set the scene for a connected personal story.",
                "Gunakan frasa waktu/tempat dan كَانَ untuk memberi konteks sebelum cerita utama.",
                ["فِي الْأُسْبُوعِ الْمَاضِي، ...", "كُنْتُ فِي ...", "كَانَ الْمَكَانُ ..."],
                [
                    phrase("فِي الْأُسْبُوعِ الْمَاضِي، كُنْتُ فِي الْمَكْتَبَةِ.", "Minggu lalu, saya berada di perpustakaan.", "Membuka cerita dengan waktu dan tempat."),
                    phrase("كُنْتُ مَعَ صَدِيقِي فِي ذَلِكَ الْوَقْتِ.", "Saya bersama teman saya pada waktu itu.", "Menyebut siapa yang ikut."),
                    phrase("كَانَ الْمَكَانُ هَادِئًا وَمُنَاسِبًا.", "Tempatnya tenang dan cocok.", "Memberi suasana cerita."),
                    phrase("هَذَا يُسَاعِدُ عَلَى فَهْمِ الْقِصَّةِ.", "Ini membantu memahami ceritanya.", "Menjelaskan fungsi konteks."),
                    phrase("بَعْدَ ذَلِكَ، بَدَأَ الْحَدَثُ الْأَسَاسِيُّ.", "Setelah itu, kejadian utamanya dimulai.", "Masuk ke urutan cerita."),
                ],
                ("Ahmad", "Karim"),
                ("كَيْفَ تَبْدَأُ قِصَّةً شَخْصِيَّةً؟", "Bagaimana kamu memulai cerita pribadi?"),
            ),
            lesson(
                "lesson-02-telling-events-in-order",
                "arabic-b1-telling-events-in-order",
                "Telling Events in Order",
                "Kamu menceritakan kejadian secara berurutan agar lawan bicara mudah mengikuti alurnya.",
                "Tell events in a clear sequence.",
                "Gunakan أَوَّلًا، ثُمَّ، بَعْدَ ذَلِكَ، وَأَخِيرًا untuk menyusun cerita.",
                ["أَوَّلًا، ...", "ثُمَّ ...", "بَعْدَ ذَلِكَ ...", "وَأَخِيرًا ..."],
                [
                    phrase("أَوَّلًا، وَصَلْتُ إِلَى الْمَكَانِ مُبَكِّرًا.", "Pertama, saya tiba di tempat itu lebih awal.", "Memulai urutan kejadian."),
                    phrase("ثُمَّ انْتَظَرْتُ صَدِيقِي قَلِيلًا.", "Lalu saya menunggu teman saya sebentar.", "Menyebut kejadian berikutnya."),
                    phrase("بَعْدَ ذَلِكَ، تَحَدَّثْنَا عَنِ الْخُطَّةِ.", "Setelah itu, kami berbicara tentang rencana.", "Menyambung urutan."),
                    phrase("وَأَخِيرًا، اتَّفَقْنَا عَلَى الْخُطْوَةِ التَّالِيَةِ.", "Akhirnya, kami sepakat pada langkah berikutnya.", "Menutup urutan."),
                    phrase("هَكَذَا صَارَتِ الْقِصَّةُ وَاضِحَةً.", "Dengan begitu ceritanya menjadi jelas.", "Menjelaskan hasil cerita."),
                ],
                ("Ahmad", "Karim"),
                ("مَاذَا حَدَثَ بَعْدَ ذَلِكَ؟", "Apa yang terjadi setelah itu?"),
            ),
            lesson(
                "lesson-03-describing-feelings",
                "arabic-b1-describing-feelings",
                "Describing Feelings",
                "Kamu menjelaskan perasaan dalam cerita dan memberi alasan singkat mengapa merasa begitu.",
                "Describe feelings with a short reason.",
                "Gunakan شَعَرْتُ بِـ dan لِأَنَّ untuk menghubungkan perasaan dengan alasan.",
                ["شَعَرْتُ بِـ ...", "كُنْتُ ...", "لِأَنَّ ..."],
                [
                    phrase("شَعَرْتُ بِالْقَلَقِ فِي الْبِدَايَةِ.", "Saya merasa khawatir di awal.", "Menyebut perasaan awal."),
                    phrase("لِأَنَّ الْمَوْقِفَ كَانَ جَدِيدًا عَلَيَّ.", "Karena situasinya baru bagi saya.", "Memberi alasan perasaan."),
                    phrase("بَعْدَ قَلِيلٍ، شَعَرْتُ بِالرَّاحَةِ.", "Setelah sebentar, saya merasa nyaman.", "Menunjukkan perubahan perasaan."),
                    phrase("هَذَا التَّغْيِيرُ كَانَ مُهِمًّا فِي الْقِصَّةِ.", "Perubahan ini penting dalam cerita.", "Menjelaskan makna perasaan."),
                    phrase("فِي النِّهَايَةِ، كُنْتُ سَعِيدًا بِالنَّتِيجَةِ.", "Pada akhirnya, saya senang dengan hasilnya.", "Menutup cerita dengan perasaan akhir."),
                ],
                ("Ahmad", "Karim"),
                ("كَيْفَ شَعَرْتَ فِي ذَلِكَ الْمَوْقِفِ؟", "Bagaimana perasaanmu dalam situasi itu?"),
            ),
            lesson(
                "lesson-04-asking-about-someones-story",
                "arabic-b1-asking-about-someones-story",
                "Asking About Someone's Story",
                "Kamu bertanya lanjutan tentang cerita seseorang tanpa memotong alur pembicaraan.",
                "Ask natural follow-up questions about a story.",
                "Gunakan مَاذَا حَدَثَ، كَيْفَ شَعَرْتَ، dan لِمَاذَا untuk memperdalam cerita.",
                ["مَاذَا حَدَثَ؟", "كَيْفَ شَعَرْتَ؟", "لِمَاذَا كَانَ ذَلِكَ مُهِمًّا؟"],
                [
                    phrase("مَاذَا حَدَثَ بَعْدَ ذَلِكَ؟", "Apa yang terjadi setelah itu?", "Meminta lanjutan cerita."),
                    phrase("كَيْفَ شَعَرْتَ فِي تِلْكَ اللَّحْظَةِ؟", "Bagaimana perasaanmu pada saat itu?", "Menanyakan perasaan."),
                    phrase("لِمَاذَا كَانَ ذَلِكَ مُهِمًّا لَكَ؟", "Mengapa itu penting bagimu?", "Menanyakan makna cerita."),
                    phrase("أُرِيدُ أَنْ أَفْهَمَ السِّبَاقَ أَكْثَرَ.", "Saya ingin memahami konteksnya lebih banyak.", "Meminta konteks dengan sopan."),
                    phrase("شُكْرًا، أَصْبَحَتِ الْقِصَّةُ أَوْضَحَ.", "Terima kasih, ceritanya menjadi lebih jelas.", "Merespons setelah penjelasan."),
                ],
                ("Ahmad", "Karim"),
                ("كَيْفَ تَسْأَلُ عَنْ قِصَّةِ شَخْصٍ آخَرَ؟", "Bagaimana kamu bertanya tentang cerita orang lain?"),
            ),
            lesson(
                "lesson-05-personal-story-mission",
                "arabic-b1-personal-story-mission",
                "Personal Story Mission",
                "Kamu menggabungkan konteks, urutan kejadian, perasaan, dan pertanyaan lanjutan dalam satu cerita.",
                "Tell a connected personal story and answer follow-up questions.",
                "Gabungkan frasa konteks, sequence markers, feeling, dan follow-up response.",
                ["فِي الْبِدَايَةِ ...", "ثُمَّ ...", "شَعَرْتُ بِـ ...", "فِي النِّهَايَةِ ..."],
                [
                    phrase("فِي الْبِدَايَةِ، كَانَ الْمَوْقِفُ غَيْرَ وَاضِحٍ.", "Di awal, situasinya belum jelas.", "Membuka cerita dengan masalah ringan."),
                    phrase("ثُمَّ سَأَلْتُ صَدِيقِي عَنْ التَّفَاصِيلِ.", "Lalu saya bertanya kepada teman saya tentang detailnya.", "Menyebut tindakan."),
                    phrase("بَعْدَ ذَلِكَ، فَهِمْتُ السَّبَبَ.", "Setelah itu, saya memahami alasannya.", "Menunjukkan perkembangan cerita."),
                    phrase("شَعَرْتُ بِالرَّاحَةِ لِأَنَّ الْأَمْرَ صَارَ وَاضِحًا.", "Saya merasa nyaman karena masalahnya menjadi jelas.", "Menghubungkan perasaan dan alasan."),
                    phrase("فِي النِّهَايَةِ، تَعَلَّمْتُ دَرْسًا مُفِيدًا.", "Pada akhirnya, saya belajar pelajaran yang bermanfaat.", "Menutup cerita."),
                ],
                ("Ahmad", "Karim"),
                ("احْكِ لِي قِصَّةً قَصِيرَةً عَنْ تَجْرِبَتِكَ.", "Ceritakan cerita singkat tentang pengalamanmu."),
            ),
        ],
    },
    {
        "unit_key": "unit-02-workplace-conversations",
        "title": "Workplace Conversations",
        "main_conversation_outcome": "Explain tasks, clarify requests, give updates, join simple meetings, and close with action points.",
        "speakers": ("Maryam", "Noura"),
        "lessons": [
            lesson(
                "lesson-01-explaining-your-task",
                "arabic-b1-explaining-your-task",
                "Explaining Your Task",
                "Kamu menjelaskan tugas kerja atau belajar secara jelas: tujuan, langkah, dan hasil yang diharapkan.",
                "Explain a task with purpose and next steps.",
                "Gunakan أَعْمَلُ عَلَى، الْهَدَفُ، وَالْخُطْوَةُ التَّالِيَةُ untuk menjelaskan tugas.",
                ["أَعْمَلُ عَلَى ...", "الْهَدَفُ هُوَ ...", "الْخُطْوَةُ التَّالِيَةُ ..."],
                [
                    phrase("أَعْمَلُ عَلَى مَهَمَّةٍ جَدِيدَةٍ هَذَا الْأُسْبُوعَ.", "Saya mengerjakan tugas baru minggu ini.", "Menjelaskan tugas utama."),
                    phrase("الْهَدَفُ هُوَ تَحْسِينُ التَّنْظِيمِ.", "Tujuannya adalah memperbaiki pengaturan.", "Menjelaskan tujuan."),
                    phrase("أَحْتَاجُ إِلَى مَرَاجَعَةِ التَّفَاصِيلِ أَوَّلًا.", "Saya perlu meninjau detailnya dulu.", "Menjelaskan langkah awal."),
                    phrase("الْخُطْوَةُ التَّالِيَةُ هِيَ إِرْسَالُ مُلَخَّصٍ.", "Langkah berikutnya adalah mengirim ringkasan.", "Menyebut tindakan berikutnya."),
                    phrase("سَأُكْمِلُ ذَلِكَ قَبْلَ نِهَايَةِ الْيَوْمِ.", "Saya akan menyelesaikan itu sebelum akhir hari.", "Memberi batas waktu."),
                ],
                ("Maryam", "Noura"),
                ("مَا الْمَهَمَّةُ الَّتِي تَعْمَلِينَ عَلَيْهَا؟", "Tugas apa yang sedang kamu kerjakan?"),
            ),
            lesson(
                "lesson-02-asking-for-clarification",
                "arabic-b1-asking-for-clarification",
                "Asking for Clarification",
                "Kamu meminta klarifikasi ketika instruksi belum cukup jelas.",
                "Ask for clarification politely.",
                "Gunakan هَلْ تَقْصِدُ، مَا الْمَقْصُودُ، dan لِكَيْ أَتَأَكَّدَ.",
                ["هَلْ تَقْصِدُ ...؟", "مَا الْمَقْصُودُ بِـ ...؟", "لِكَيْ أَتَأَكَّدَ ..."],
                [
                    phrase("هَلْ تَقْصِدِينَ أَنَّ الْمَوْعِدَ تَغَيَّرَ؟", "Apakah maksudmu jadwalnya berubah?", "Mengecek maksud."),
                    phrase("مَا الْمَقْصُودُ بِهَذِهِ النُّقْطَةِ؟", "Apa maksud poin ini?", "Meminta penjelasan detail."),
                    phrase("أَسْأَلُ لِكَيْ أَتَأَكَّدَ فَقَطْ.", "Saya bertanya hanya untuk memastikan.", "Melembutkan klarifikasi."),
                    phrase("هَلْ يُمْكِنُ أَنْ تُعِيدِي الشَّرْحَ بِاخْتِصَارٍ؟", "Bisakah kamu mengulang penjelasan dengan singkat?", "Meminta pengulangan."),
                    phrase("الْآنَ فَهِمْتُ الْمَطْلُوبَ.", "Sekarang saya memahami yang diminta.", "Menutup klarifikasi."),
                ],
                ("Maryam", "Noura"),
                ("هَلِ التَّعْلِيمَاتُ وَاضِحَةٌ؟", "Apakah instruksinya jelas?"),
            ),
            lesson(
                "lesson-03-giving-a-short-update",
                "arabic-b1-giving-a-short-update",
                "Giving a Short Update",
                "Kamu memberi update singkat tentang progress, kendala, dan langkah berikutnya.",
                "Give a concise progress update.",
                "Gunakan أَنْجَزْتُ، مَا زِلْتُ، وَسَأُكْمِلُ untuk update ringkas.",
                ["أَنْجَزْتُ ...", "مَا زِلْتُ أَعْمَلُ عَلَى ...", "سَأُكْمِلُ ..."],
                [
                    phrase("أَنْجَزْتُ الْجُزْءَ الْأَوَّلَ مِنَ الْمَهَمَّةِ.", "Saya sudah menyelesaikan bagian pertama tugas.", "Menyebut progress."),
                    phrase("مَا زِلْتُ أَعْمَلُ عَلَى التَّفَاصِيلِ.", "Saya masih mengerjakan detailnya.", "Menyebut yang belum selesai."),
                    phrase("لَا تُوجَدُ مُشْكِلَةٌ كَبِيرَةٌ حَتَّى الْآنَ.", "Belum ada masalah besar sampai sekarang.", "Memberi status kendala."),
                    phrase("سَأُرْسِلُ التَّحْدِيثَ بَعْدَ سَاعَةٍ.", "Saya akan mengirim update setelah satu jam.", "Memberi waktu update."),
                    phrase("هَذَا هُوَ الْوَضْعُ الْحَالِيُّ.", "Ini adalah kondisi saat ini.", "Menutup update."),
                ],
                ("Maryam", "Noura"),
                ("هَلْ عِنْدَكِ تَحْدِيثٌ قَصِيرٌ؟", "Apakah kamu punya update singkat?"),
            ),
            lesson(
                "lesson-04-joining-a-simple-meeting",
                "arabic-b1-joining-a-simple-meeting",
                "Joining a Simple Meeting",
                "Kamu masuk meeting sederhana, memberi pendapat, dan menanyakan langkah berikutnya.",
                "Join a simple meeting and contribute politely.",
                "Gunakan أُرِيدُ أَنْ أُضِيفَ، أَقْتَرِحُ، وَمَا الْخُطْوَةُ التَّالِيَةُ؟",
                ["أُرِيدُ أَنْ أُضِيفَ ...", "أَقْتَرِحُ أَنْ ...", "مَا الْخُطْوَةُ التَّالِيَةُ؟"],
                [
                    phrase("أُرِيدُ أَنْ أُضِيفَ نُقْطَةً صَغِيرَةً.", "Saya ingin menambahkan poin kecil.", "Masuk diskusi dengan sopan."),
                    phrase("أَقْتَرِحُ أَنْ نُرَاجِعَ الْخُطَّةَ أَوَّلًا.", "Saya menyarankan kita meninjau rencana dulu.", "Memberi saran."),
                    phrase("هَذَا يُمْكِنُ أَنْ يُقَلِّلَ الْخَطَأَ.", "Ini bisa mengurangi kesalahan.", "Memberi alasan saran."),
                    phrase("مَا الْخُطْوَةُ التَّالِيَةُ بَعْدَ ذَلِكَ؟", "Apa langkah berikutnya setelah itu?", "Menanyakan tindak lanjut."),
                    phrase("سَأَكْتُبُ النِّقَاطَ الْمُهِمَّةَ.", "Saya akan menulis poin-poin penting.", "Mengambil tanggung jawab."),
                ],
                ("Maryam", "Noura"),
                ("هَلْ تُرِيدِينَ أَنْ تُضِيفِي شَيْئًا؟", "Apakah kamu ingin menambahkan sesuatu?"),
            ),
            lesson(
                "lesson-05-workplace-mission",
                "arabic-b1-workplace-mission",
                "Workplace Mission",
                "Kamu menjelaskan tugas, meminta klarifikasi, memberi update, dan menutup dengan action point.",
                "Combine task explanation, clarification, update, and next action.",
                "Gabungkan أَعْمَلُ عَلَى، هَلْ تَقْصِدُ، أَنْجَزْتُ، وَسَأُرْسِلُ.",
                ["أَعْمَلُ عَلَى ...", "هَلْ تَقْصِدُ ...؟", "أَنْجَزْتُ ...", "سَأُرْسِلُ ..."],
                [
                    phrase("أَعْمَلُ عَلَى تَنْظِيمِ الْمَلَفَّاتِ.", "Saya mengerjakan pengaturan file.", "Menjelaskan tugas."),
                    phrase("هَلْ تَقْصِدِينَ الْمَلَفَّاتِ الْجَدِيدَةَ فَقَطْ؟", "Apakah maksudmu hanya file baru?", "Meminta klarifikasi."),
                    phrase("أَنْجَزْتُ نِصْفَ الْعَمَلِ حَتَّى الْآنَ.", "Saya sudah menyelesaikan setengah pekerjaan sampai sekarang.", "Memberi progress."),
                    phrase("سَأُرْسِلُ مُلَخَّصًا قَبْلَ الْمَسَاءِ.", "Saya akan mengirim ringkasan sebelum sore.", "Memberi komitmen."),
                    phrase("إِذَا ظَهَرَتْ مُشْكِلَةٌ، سَأُخْبِرُكِ.", "Jika muncul masalah, saya akan memberitahumu.", "Menutup dengan mitigasi."),
                ],
                ("Maryam", "Noura"),
                ("أَعْطِينِي تَحْدِيثًا عَنِ الْعَمَلِ.", "Berikan saya update tentang pekerjaan."),
            ),
        ],
    },
]


MORE_UNITS: list[dict[str, Any]] = [
    {
        "unit_key": "unit-03-problems-and-solutions",
        "title": "Problems & Solutions",
        "main_conversation_outcome": "Explain a problem, suggest solutions, respond to advice, and make a simple decision.",
        "speakers": ("Omar", "Raka"),
        "topics": [
            ("describing-a-problem", "Describing a Problem", "تُوجَدُ مُشْكِلَةٌ فِي الْخِدْمَةِ.", "Ada masalah pada layanan.", "الْمُشْكِلَةُ بَدَأَتْ مُنْذُ الصَّبَاحِ.", "Masalahnya mulai sejak pagi.", "أَثَّرَ ذَلِكَ عَلَى الْعَمَلِ.", "Itu memengaruhi pekerjaan.", "أَحْتَاجُ إِلَى حَلٍّ سَرِيعٍ.", "Saya butuh solusi cepat.", "سَأُرَاجِعُ السَّبَبَ أَوَّلًا.", "Saya akan meninjau penyebabnya dulu."),
            ("suggesting-a-solution", "Suggesting a Solution", "أَقْتَرِحُ أَنْ نُجَرِّبَ حَلًّا بَسِيطًا.", "Saya menyarankan kita mencoba solusi sederhana.", "يُمْكِنُنَا أَنْ نُغَيِّرَ الْخُطَّةَ قَلِيلًا.", "Kita bisa mengubah rencana sedikit.", "هَذَا الْحَلُّ أَسْرَعُ مِنَ الْخِيَارِ الْآخَرِ.", "Solusi ini lebih cepat dari pilihan lain.", "لَكِنَّهُ يَحْتَاجُ إِلَى مُرَاجَعَةٍ.", "Tetapi perlu tinjauan.", "إِذَا نَجَحَ، نَسْتَمِرُّ عَلَيْهِ.", "Jika berhasil, kita lanjutkan."),
            ("responding-to-advice", "Responding to Advice", "نَصِيحَتُكَ مُفِيدَةٌ.", "Nasihatmu bermanfaat.", "سَأُجَرِّبُ ذَلِكَ الْيَوْمَ.", "Saya akan mencoba itu hari ini.", "أَتَّفِقُ مَعَكَ فِي هَذِهِ النُّقْطَةِ.", "Saya setuju denganmu pada poin ini.", "لَكِنْ عِنْدِي سُؤَالٌ صَغِيرٌ.", "Tetapi saya punya pertanyaan kecil.", "شُكْرًا عَلَى التَّوْجِيهِ.", "Terima kasih atas arahannya."),
            ("making-a-simple-decision", "Making a Simple Decision", "لَدَيْنَا خِيَارَانِ مُنَاسِبَانِ.", "Kita punya dua pilihan yang cocok.", "الْخِيَارُ الْأَوَّلُ أَسْهَلُ.", "Pilihan pertama lebih mudah.", "الْخِيَارُ الثَّانِي أَفْضَلُ عَلَى الْمَدَى الطَّوِيلِ.", "Pilihan kedua lebih baik untuk jangka panjang.", "أُفَضِّلُ الْخِيَارَ الثَّانِي لِهَذَا السَّبَبِ.", "Saya memilih pilihan kedua karena alasan ini.", "إِذَنْ، نَبْدَأُ بِهِ غَدًا.", "Kalau begitu, kita mulai besok."),
            ("problem-solving-mission", "Problem Solving Mission", "سَأَشْرَحُ الْمُشْكِلَةَ بِاخْتِصَارٍ.", "Saya akan menjelaskan masalahnya dengan singkat.", "السَّبَبُ غَيْرُ وَاضِحٍ حَتَّى الْآنَ.", "Penyebabnya belum jelas sampai sekarang.", "أَقْتَرِحُ أَنْ نُجَرِّبَ حَلًّا مُؤَقَّتًا.", "Saya menyarankan kita mencoba solusi sementara.", "إِذَا نَجَحَ، نُثَبِّتُهُ.", "Jika berhasil, kita tetapkan.", "وَإِذَا لَمْ يَنْجَحْ، نَبْحَثُ عَنْ خِيَارٍ آخَرَ.", "Jika tidak berhasil, kita cari pilihan lain."),
        ],
    },
    {
        "unit_key": "unit-04-travel-situations",
        "title": "Travel Situations",
        "main_conversation_outcome": "Handle travel check-in, delays, recommendations, complaints, and practical travel requests.",
        "speakers": ("Ahmad", "Karim"),
        "topics": [
            ("checking-in", "Checking In", "لَدَيَّ حَجْزٌ بِاسْمِ أَحْمَدَ.", "Saya punya reservasi atas nama Ahmad.", "أُرِيدُ أَنْ أُؤَكِّدَ التَّفَاصِيلَ.", "Saya ingin mengonfirmasi detailnya.", "هَلِ الْغُرْفَةُ جَاهِزَةٌ الآنَ؟", "Apakah kamarnya sudah siap sekarang?", "أَحْتَاجُ إِلَى بُطَاقَةِ الدُّخُولِ.", "Saya perlu kartu masuk.", "شُكْرًا عَلَى الْمُسَاعَدَةِ.", "Terima kasih atas bantuannya."),
            ("explaining-a-delay", "Explaining a Delay", "تَأَخَّرَتِ الرِّحْلَةُ قَلِيلًا.", "Perjalanannya sedikit terlambat.", "السَّبَبُ هُوَ الِازْدِحَامُ فِي الطَّرِيقِ.", "Alasannya adalah kemacetan di jalan.", "سَأَصِلُ بَعْدَ ثَلَاثِينَ دَقِيقَةً.", "Saya akan tiba setelah tiga puluh menit.", "آسِفٌ عَلَى التَّأْخِيرِ.", "Maaf atas keterlambatannya.", "سَأُخْبِرُكَ إِذَا تَغَيَّرَ الْوَقْتُ.", "Saya akan memberitahumu jika waktunya berubah."),
            ("asking-for-recommendations", "Asking for Recommendations", "هَلْ تُوصِي بِمَطْعَمٍ قَرِيبٍ؟", "Apakah kamu merekomendasikan restoran dekat?", "أُفَضِّلُ مَكَانًا هَادِئًا.", "Saya lebih suka tempat yang tenang.", "يَهُمُّنِي أَنْ يَكُونَ السِّعْرُ مُنَاسِبًا.", "Penting bagi saya agar harganya cocok.", "مَا أَفْضَلُ خِيَارٍ فِي رَأْيِكَ؟", "Apa pilihan terbaik menurutmu?", "شُكْرًا، سَأُجَرِّبُ هَذَا الْمَكَانَ.", "Terima kasih, saya akan mencoba tempat ini."),
            ("handling-a-simple-complaint", "Handling a Simple Complaint", "أُرِيدُ أَنْ أُوَضِّحَ مُشْكِلَةً صَغِيرَةً.", "Saya ingin menjelaskan masalah kecil.", "الْغُرْفَةُ غَيْرُ نَظِيفَةٍ تَمَامًا.", "Kamarnya tidak sepenuhnya bersih.", "هَلْ يُمْكِنُ أَنْ تُرْسِلُوا أَحَدًا؟", "Bisakah kalian mengirim seseorang?", "أُقَدِّرُ مُسَاعَدَتَكُمْ.", "Saya menghargai bantuan kalian.", "إِذَا أَمْكَنَ، أُرِيدُ حَلًّا الْيَوْمَ.", "Jika memungkinkan, saya ingin solusi hari ini."),
            ("travel-situation-mission", "Travel Situation Mission", "عِنْدِي حَجْزٌ وَلَكِنَّنِي تَأَخَّرْتُ.", "Saya punya reservasi tetapi terlambat.", "أُرِيدُ أَنْ أُؤَكِّدَ الْوُصُولَ.", "Saya ingin mengonfirmasi kedatangan.", "هَلْ تُوصِي بِمَكَانٍ قَرِيبٍ لِلطَّعَامِ؟", "Apakah kamu merekomendasikan tempat makan dekat?", "لَدَيَّ مُشْكِلَةٌ صَغِيرَةٌ فِي الْغُرْفَةِ.", "Saya punya masalah kecil di kamar.", "شُكْرًا عَلَى سُرْعَةِ الْمُسَاعَدَةِ.", "Terima kasih atas cepatnya bantuan."),
        ],
    },
    {
        "unit_key": "unit-05-goals-and-progress",
        "title": "Goals & Progress",
        "main_conversation_outcome": "Talk about goals, progress, challenges, and next steps with connected reasons.",
        "speakers": ("Sara", "Layla"),
        "topics": [
            ("talking-about-goals", "Talking About Goals", "هَدَفِي هُوَ تَحْسِينُ الْمُحَادَثَةِ.", "Tujuan saya adalah memperbaiki percakapan.", "أُرِيدُ أَنْ أَتَكَلَّمَ بِثِقَةٍ أَكْبَرَ.", "Saya ingin berbicara dengan lebih percaya diri.", "لِذَلِكَ أَتَدَرَّبُ كُلَّ يَوْمٍ.", "Karena itu saya berlatih setiap hari.", "أَقِيسُ التَّقَدُّمَ بِالْمُرَاجَعَةِ.", "Saya mengukur progress dengan review.", "هَذَا الْهَدَفُ مُهِمٌّ لِي.", "Tujuan ini penting bagi saya."),
            ("explaining-progress", "Explaining Progress", "تَقَدَّمْتُ قَلِيلًا هَذَا الشَّهْرَ.", "Saya sedikit maju bulan ini.", "أَصْبَحْتُ أَفْهَمُ الْحِوَارَ أَسْرَعَ.", "Saya menjadi lebih cepat memahami dialog.", "مَا زِلْتُ أُخْطِئُ فِي بَعْضِ الْجُمَلِ.", "Saya masih salah pada beberapa kalimat.", "لَكِنَّ التَّحَسُّنَ وَاضِحٌ.", "Tetapi perbaikannya jelas.", "سَأُوَاصِلُ التَّدْرِيبَ.", "Saya akan terus berlatih."),
            ("discussing-challenges", "Discussing Challenges", "أَكْبَرُ تَحَدٍّ هُوَ السُّرْعَةُ.", "Tantangan terbesar adalah kecepatan.", "أَحْتَاجُ إِلَى وَقْتٍ لِلتَّفْكِيرِ.", "Saya butuh waktu untuk berpikir.", "أَحْيَانًا أَنْسَى الْكَلِمَاتِ الْمُنَاسِبَةَ.", "Kadang saya lupa kata yang cocok.", "سَأُقَلِّلُ الْجُمَلَ الطَّوِيلَةَ.", "Saya akan mengurangi kalimat panjang.", "هَذَا يُسَاعِدُنِي عَلَى الطَّلَاقَةِ.", "Ini membantu saya pada kelancaran."),
            ("making-next-step-plans", "Making Next-step Plans", "الْخُطْوَةُ التَّالِيَةُ هِيَ التَّدْرِيبُ الْيَوْمِيُّ.", "Langkah berikutnya adalah latihan harian.", "سَأُرَاجِعُ خَمْسَ عِبَارَاتٍ كُلَّ يَوْمٍ.", "Saya akan meninjau lima frasa setiap hari.", "سَأُسَجِّلُ صَوْتِي مَرَّةً وَاحِدَةً.", "Saya akan merekam suara saya satu kali.", "بَعْدَ أُسْبُوعٍ، سَأُقَيِّمُ النَّتِيجَةَ.", "Setelah seminggu, saya akan menilai hasilnya.", "إِذَا احْتَجْتُ، سَأُغَيِّرُ الْخُطَّةَ.", "Jika perlu, saya akan mengubah rencana."),
            ("goals-progress-mission", "Goals Progress Mission", "هَدَفِي وَاضِحٌ لِهَذَا الشَّهْرِ.", "Tujuan saya jelas untuk bulan ini.", "تَقَدَّمْتُ فِي الِاسْتِمَاعِ، وَلَكِنَّ الْكَلَامَ أَصْعَبُ.", "Saya maju dalam listening, tetapi speaking lebih sulit.", "أَكْبَرُ تَحَدٍّ هُوَ التَّرَدُّدُ.", "Tantangan terbesar adalah keraguan.", "سَأَتَدَرَّبُ عَلَى إِجَابَاتٍ قَصِيرَةٍ.", "Saya akan berlatih jawaban pendek.", "سَأُرَاجِعُ النَّتِيجَةَ بَعْدَ أُسْبُوعٍ.", "Saya akan meninjau hasilnya setelah seminggu."),
        ],
    },
    {
        "unit_key": "unit-06-explaining-preferences",
        "title": "Explaining Preferences",
        "main_conversation_outcome": "Compare options, explain preferences, ask about pros and cons, and reach agreement.",
        "speakers": ("Fatimah", "Noura"),
        "topics": [
            ("comparing-two-options", "Comparing Two Options", "عِنْدَنَا خِيَارَانِ مُخْتَلِفَانِ.", "Kita punya dua pilihan berbeda.", "الْخِيَارُ الْأَوَّلُ أَسْرَعُ.", "Pilihan pertama lebih cepat.", "الْخِيَارُ الثَّانِي أَرْخَصُ.", "Pilihan kedua lebih murah.", "لَكِنَّ الْجَوْدَةَ مُهِمَّةٌ أَيْضًا.", "Tetapi kualitas juga penting.", "نَحْتَاجُ إِلَى مُقَارَنَةٍ هَادِئَةٍ.", "Kita perlu perbandingan yang tenang."),
            ("explaining-why-you-prefer-something", "Explaining Why You Prefer Something", "أُفَضِّلُ هَذَا الْخِيَارَ لِأَنَّهُ أَوْضَحُ.", "Saya lebih memilih pilihan ini karena lebih jelas.", "يُنَاسِبُ هَدَفَنَا أَكْثَرَ.", "Ini lebih cocok dengan tujuan kita.", "رَغْمَ أَنَّهُ أَغْلَى قَلِيلًا.", "Meskipun sedikit lebih mahal.", "لَكِنَّهُ يُوَفِّرُ وَقْتًا.", "Tetapi ini menghemat waktu.", "لِذَلِكَ أَرَاهُ أَفْضَلَ.", "Karena itu saya melihatnya lebih baik."),
            ("asking-about-pros-and-cons", "Asking About Pros and Cons", "مَا إِيجَابِيَّاتُ هَذَا الْخِيَارِ؟", "Apa kelebihan pilihan ini?", "وَمَا السَّلْبِيَّاتُ الْمُمْكِنَةُ؟", "Dan apa kemungkinan kekurangannya?", "هَلِ الْمَزَايَا أَكْثَرُ مِنَ الْمَشَاكِلِ؟", "Apakah kelebihannya lebih banyak dari masalahnya?", "أُرِيدُ أَنْ أَفْهَمَ الصُّورَةَ كَامِلَةً.", "Saya ingin memahami gambaran lengkap.", "بَعْدَ ذَلِكَ، نَقْرِّرُ.", "Setelah itu, kita putuskan."),
            ("reaching-agreement", "Reaching Agreement", "أَتَّفِقُ مَعَكِ فِي النُّقْطَةِ الْأُولَى.", "Saya setuju denganmu pada poin pertama.", "لَكِنَّنِي أَرَى خِيَارًا آخَرَ.", "Tetapi saya melihat pilihan lain.", "مُمْكِنٌ أَنْ نَجْمَعَ بَيْنَ الْفِكْرَتَيْنِ.", "Mungkin kita bisa menggabungkan dua ide.", "هَذَا حَلٌّ مُتَوَازِنٌ.", "Ini solusi yang seimbang.", "إِذَنْ، نَتَّفِقُ عَلَى هَذِهِ الْخُطَّةِ.", "Kalau begitu, kita sepakat pada rencana ini."),
            ("preference-discussion-mission", "Preference Discussion Mission", "سَأُقَارِنُ بَيْنَ خِيَارَيْنِ.", "Saya akan membandingkan dua pilihan.", "أُفَضِّلُ الْخِيَارَ الْأَوَّلَ لِأَنَّهُ أَسْهَلُ.", "Saya lebih memilih pilihan pertama karena lebih mudah.", "لَكِنَّ الْخِيَارَ الثَّانِي أَقْوَى.", "Tetapi pilihan kedua lebih kuat.", "نَحْتَاجُ إِلَى تَوَازُنٍ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", "Kita perlu keseimbangan antara kecepatan dan kualitas.", "إِذَنْ، نَخْتَارُ الْحَلَّ الْمُتَوَازِنَ.", "Kalau begitu, kita pilih solusi yang seimbang."),
        ],
    },
    {
        "unit_key": "unit-07-community-and-culture",
        "title": "Community & Culture",
        "main_conversation_outcome": "Discuss community, habits, differences, and polite cultural questions in clear formal Arabic.",
        "speakers": ("Khalid", "Zayd"),
        "topics": [
            ("describing-your-community", "Describing Your Community", "أَعِيشُ فِي مُجْتَمَعٍ هَادِئٍ.", "Saya tinggal di komunitas yang tenang.", "النَّاسُ يَتَعَاوَنُونَ فِي الْأَعْمَالِ الْيَوْمِيَّةِ.", "Orang-orang saling membantu dalam pekerjaan harian.", "تُوجَدُ عَادَاتٌ جَمِيلَةٌ فِي الْحَيِّ.", "Ada kebiasaan indah di lingkungan.", "أَشْعُرُ بِالِانْتِمَاءِ إِلَى هَذَا الْمَكَانِ.", "Saya merasa memiliki tempat ini.", "هَذَا يُؤَثِّرُ عَلَى حَيَاتِي.", "Ini memengaruhi hidup saya."),
            ("talking-about-local-habits", "Talking About Local Habits", "مِنَ الْعَادَةِ أَنْ نُحَيِّيَ الْجِيرَانَ.", "Biasanya kami menyapa tetangga.", "فِي الصَّبَاحِ، يَكُونُ الشَّارِعُ نَشِيطًا.", "Pada pagi hari, jalan menjadi aktif.", "بَعْضُ النَّاسِ يَفْضِّلُونَ الْهُدُوءَ.", "Sebagian orang lebih suka ketenangan.", "هَذِهِ الْعَادَةُ تُسَاعِدُ عَلَى الِاحْتِرَامِ.", "Kebiasaan ini membantu penghormatan.", "أَحْتَرِمُ هَذِهِ الطَّرِيقَةَ.", "Saya menghormati cara ini."),
            ("asking-about-culture", "Asking About Culture", "هَلْ يُمْكِنُ أَنْ أَسْأَلَ عَنْ هَذِهِ الْعَادَةِ؟", "Bolehkah saya bertanya tentang kebiasaan ini?", "أُرِيدُ أَنْ أَفْهَمَ السِّبَاقَ الثَّقَافِيَّ.", "Saya ingin memahami konteks budaya.", "هَلْ هَذَا أَمْرٌ رَسْمِيٌّ أَمْ عَادِيٌّ؟", "Apakah ini hal resmi atau biasa?", "شُكْرًا عَلَى التَّوْضِيحِ.", "Terima kasih atas penjelasannya.", "سَأَتَصَرَّفُ بِاحْتِرَامٍ.", "Saya akan bersikap dengan hormat."),
            ("being-polite-with-differences", "Being Polite With Differences", "أَفْهَمُ أَنَّ الْعَادَاتِ تَخْتَلِفُ.", "Saya paham bahwa kebiasaan berbeda-beda.", "لَا أُرِيدُ أَنْ أُسِيءَ الْفَهْمَ.", "Saya tidak ingin salah paham.", "مِنَ الْأَفْضَلِ أَنْ نَسْأَلَ بِأَدَبٍ.", "Lebih baik bertanya dengan sopan.", "أَحْتَرِمُ اخْتِلَافَ الطُّرُقِ.", "Saya menghormati perbedaan cara.", "هَذَا يَجْعَلُ الْحِوَارَ أَسْهَلَ.", "Ini membuat dialog lebih mudah."),
            ("community-culture-mission", "Community Culture Mission", "سَأَصِفُ مُجْتَمَعِي بِاخْتِصَارٍ.", "Saya akan menjelaskan komunitas saya dengan singkat.", "تُوجَدُ عَادَةٌ مُهِمَّةٌ عِنْدَنَا.", "Ada kebiasaan penting di tempat kami.", "أُرِيدُ أَنْ أَفْهَمَ عَادَتَكُمْ أَيْضًا.", "Saya ingin memahami kebiasaan kalian juga.", "إِذَا اخْتَلَفْنَا، نَسْأَلُ بِاحْتِرَامٍ.", "Jika kita berbeda, kita bertanya dengan hormat.", "هَكَذَا يَصِيرُ التَّوَاصُلُ أَفْضَلَ.", "Dengan begitu komunikasi menjadi lebih baik."),
        ],
    },
    {
        "unit_key": "unit-08-b1-review-final",
        "title": "B1 Review & Final Conversation",
        "main_conversation_outcome": "Use B1 Arabic skills in connected conversations across stories, work, problems, travel, goals, and culture.",
        "speakers": ("Ahmad", "Karim"),
        "topics": [
            ("review-stories-and-work", "Review Stories and Work", "سَأَبْدَأُ بِقِصَّةٍ قَصِيرَةٍ.", "Saya akan mulai dengan cerita singkat.", "بَعْدَ ذَلِكَ، أُعْطِي تَحْدِيثًا عَنِ الْعَمَلِ.", "Setelah itu, saya memberi update tentang pekerjaan.", "أَحْتَاجُ إِلَى تَوْضِيحٍ فِي نُقْطَةٍ وَاحِدَةٍ.", "Saya butuh klarifikasi pada satu poin.", "سَأُرْسِلُ مُلَخَّصًا فِي النِّهَايَةِ.", "Saya akan mengirim ringkasan di akhir.", "هَذَا يُظْهِرُ التَّرَابُطَ فِي الْحِوَارِ.", "Ini menunjukkan keterhubungan dalam dialog."),
            ("review-problems-and-travel", "Review Problems and Travel", "سَأَشْرَحُ مُشْكِلَةً ثُمَّ أَقْتَرِحُ حَلًّا.", "Saya akan menjelaskan masalah lalu menyarankan solusi.", "فِي السَّفَرِ، أَحْتَاجُ إِلَى تَفَاصِيلَ وَاضِحَةٍ.", "Dalam perjalanan, saya butuh detail jelas.", "إِذَا حَدَثَ تَأْخِيرٌ، سَأُخْبِرُ الطَّرَفَ الْآخَرَ.", "Jika terjadi keterlambatan, saya akan memberi tahu pihak lain.", "أُفَضِّلُ حَلًّا سَرِيعًا وَمُهَذَّبًا.", "Saya lebih memilih solusi cepat dan sopan.", "فِي النِّهَايَةِ، أُؤَكِّدُ الْخُطْوَةَ التَّالِيَةَ.", "Pada akhir, saya memastikan langkah berikutnya."),
            ("review-goals-and-preferences", "Review Goals and Preferences", "هَدَفِي وَاضِحٌ وَلَكِنَّ التَّحَدِّي مَوْجُودٌ.", "Tujuan saya jelas tetapi tantangannya ada.", "أُفَضِّلُ خُطَّةً بَسِيطَةً وَمُسْتَمِرَّةً.", "Saya lebih memilih rencana sederhana dan berkelanjutan.", "سَأُقَارِنُ بَيْنَ خِيَارَيْنِ.", "Saya akan membandingkan dua pilihan.", "السَّبَبُ الرَّئِيسِيُّ هُوَ الْجَوْدَةُ.", "Alasan utamanya adalah kualitas.", "بَعْدَ ذَلِكَ، أَتَّخِذُ قَرَارًا.", "Setelah itu, saya mengambil keputusan."),
            ("b1-final-test-practice", "B1 Final Test Practice", "سَأُجِيبُ بِجُمَلٍ مُتَرَابِطَةٍ.", "Saya akan menjawab dengan kalimat yang terhubung.", "أَذْكُرُ السِّبَاقَ وَالسَّبَبَ وَالنَّتِيجَةَ.", "Saya menyebut konteks, alasan, dan hasil.", "إِذَا لَمْ أَفْهَمْ، أَطْلُبُ تَوْضِيحًا.", "Jika saya tidak paham, saya meminta klarifikasi.", "أُحَافِظُ عَلَى الْهُدُوءِ وَالسُّرْعَةِ الْمُنَاسِبَةِ.", "Saya menjaga ketenangan dan kecepatan yang sesuai.", "هَذَا يُسَاعِدُنِي فِي الِاخْتِبَارِ.", "Ini membantu saya dalam tes."),
            ("b1-final-conversation", "B1 Final Conversation", "سَأَتَحَدَّثُ عَنْ تَجْرِبَةٍ شَخْصِيَّةٍ.", "Saya akan berbicara tentang pengalaman pribadi.", "ثُمَّ أَشْرَحُ مُشْكِلَةً وَحَلًّا.", "Lalu saya menjelaskan masalah dan solusi.", "بَعْدَ ذَلِكَ، أُبَيِّنُ رَأْيِي بِسَبَبٍ.", "Setelah itu, saya menjelaskan pendapat saya dengan alasan.", "أَسْأَلُ سُؤَالًا لِأُبْقِيَ الْحِوَارَ حَيًّا.", "Saya bertanya agar dialog tetap hidup.", "فِي النِّهَايَةِ، أُلَخِّصُ النُّقَاطَ الْمُهِمَّةَ.", "Pada akhir, saya merangkum poin penting."),
        ],
    },
]


def topic_lesson(unit: dict[str, Any], index: int, topic: tuple[str, ...]) -> dict[str, Any]:
    slug_tail, title, *phrase_parts = topic
    phrase_items = [
        phrase(phrase_parts[i], phrase_parts[i + 1], "Gunakan untuk percakapan B1 yang lebih terhubung.")
        for i in range(0, len(phrase_parts), 2)
    ]
    key = f"lesson-{index:02d}-{slug_tail}"
    return lesson(
        key,
        f"arabic-b1-{slug_tail}",
        title,
        f"Kamu berlatih topik B1: {title.lower()}, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
        f"Handle B1 conversation for: {title}.",
        "Gunakan kalimat terhubung dengan konteks, alasan, hasil, dan langkah berikutnya.",
        [item["phrase"] for item in phrase_items[:4]],
        phrase_items,
        unit["speakers"],
        ("مَا النُّقْطَةُ الْأَسَاسِيَّةُ فِي هَذَا الْمَوْضُوعِ؟", "Apa poin utama dalam topik ini?"),
    )


def expand_units() -> list[dict[str, Any]]:
    units = list(UNITS)
    for unit in MORE_UNITS:
        units.append(
            {
                "unit_key": unit["unit_key"],
                "title": unit["title"],
                "main_conversation_outcome": unit["main_conversation_outcome"],
                "speakers": unit["speakers"],
                "lessons": [
                    topic_lesson(unit, index, topic)
                    for index, topic in enumerate(unit["topics"], 1)
                ],
            }
        )
    return units


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def write_level_files(units: list[dict[str, Any]]) -> None:
    B1_ROOT.mkdir(parents=True, exist_ok=True)
    (B1_ROOT / "LEVEL_SPEC.md").write_text(
        "# Arabic B1 - Connected Conversations\n\n"
        "## Level Outcome\n\n"
        "Learners can tell connected personal stories, handle work and travel situations, "
        "explain problems and solutions, compare options, discuss goals, and ask polite "
        "cultural questions in clear formal Arabic.\n\n"
        "## Scope\n\n"
        "- Formal Arabic / Modern Standard Arabic, not dialect.\n"
        "- Indonesian explanations for adult learners.\n"
        "- Arabic script with harakat for learner-facing examples and listening scripts.\n"
        "- Conversation-first lessons with reading and writing support.\n"
        "- Connected answers with context, reason, result, and next step.\n"
        "- No religious source text or devotional TTS content.\n\n"
        "## B1 Upgrade From A2\n\n"
        "- Dialogue length: 6-10 connected turns.\n"
        "- Learner responses may combine context, action, reason, and result.\n"
        "- Introduce story sequencing, clarification, updates, recommendations, "
        "comparison, agreement, and polite cultural questions.\n"
        "- Keep vocabulary practical and concrete even when answers are longer.\n\n"
        "## Passing Threshold\n\n"
        "- Overall score: 75\n"
        "- Speaking / Conversation: 70\n"
        "- Listening: 68\n"
        "- Pronunciation: 62\n"
        "- Vocabulary / Useful Phrases: 68\n"
        "- Grammar: 68\n"
        "- Reading: 60\n"
        "- Writing: 60\n"
        "- Lesson completion: 80%\n",
        encoding="utf-8",
    )

    write_yaml(
        CONTENT_PLAN_PATH,
        {
            "language": "arabic",
            "language_code": "ar",
            "level_code": "B1",
            "course_slug": "arabic-b1-connected-conversations",
            "course_title": "Arabic Connected Conversations",
            "access_tier": "pro",
            "target_lesson_count": 40,
            "quality_reference": "docs/arabic_content_standard.md",
            "units": [
                {
                    "unit_key": unit["unit_key"],
                    "title": unit["title"],
                    "status": "published",
                    "main_conversation_outcome": unit["main_conversation_outcome"],
                    "lessons": [
                        {
                            "lesson_key": item["lesson_key"],
                            "slug": item["slug"],
                            "title": item["title"],
                            "status": item["status"],
                        }
                        for item in unit["lessons"]
                    ],
                }
                for unit in units
            ],
        },
    )


def learner_goal(item: dict[str, Any]) -> str:
    return f"Latih percakapan Arab B1 untuk situasi ini: {item['situation']}"


def roleplay_payload(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "scenario_key": item["slug"].replace("-", "_"),
        "mode": "lesson_practice_coach",
        "level_code": "B1",
        "opening_line": item["dialogue"][0][1],
        "learner_goal": learner_goal(item),
        "max_turns": 6,
        "feedback_level": {"free": "basic", "pro": "detailed"},
        "turns": [
            {
                "coach": item["dialogue"][0][1] if index == 1 else f"استخدم الفكرة: {entry['phrase']}",
                "hint": f"Jawab dengan kalimat terhubung memakai: {entry['phrase']}",
                "sample_answer": entry["phrase"],
                "focus": entry["usage"],
                "expected_keywords": entry["phrase"].replace("؟", "").replace(".", "").split()[:4],
                "indonesian_explanation": entry["meaning"],
            }
            for index, entry in enumerate(item["phrases"][:3], 1)
        ],
        "target_phrases": [entry["phrase"] for entry in item["phrases"][:5]],
        "rubric": {
            "speaking": {"minimum_score": 70},
            "relevance": {"minimum_score": 70},
            "grammar": {"minimum_score": 68},
        },
    }


def phrase_options(phrases: list[dict[str, str]], correct_index: int) -> list[str]:
    correct = phrases[correct_index]["phrase"]
    options = [correct]
    for entry in phrases:
        if entry["phrase"] not in options:
            options.append(entry["phrase"])
        if len(options) == 3:
            break
    return options


def write_unit_and_lessons(unit: dict[str, Any]) -> None:
    unit_dir = UNITS_ROOT / unit["unit_key"]
    write_yaml(
        unit_dir / "unit.yaml",
        {
            "unit_key": unit["unit_key"],
            "level_code": "B1",
            "title": unit["title"],
            "main_conversation_outcome": unit["main_conversation_outcome"],
            "status": "published",
            "lessons": [item["lesson_key"] for item in unit["lessons"]],
        },
    )

    for item in unit["lessons"]:
        lesson_dir = unit_dir / item["lesson_key"]
        lesson_dir.mkdir(parents=True, exist_ok=True)

        write_yaml(
            lesson_dir / "lesson.yaml",
            {
                "lesson_key": item["lesson_key"],
                "slug": item["slug"],
                "title": item["title"],
                "status": item["status"],
                "estimated_minutes": 14,
                "conversation_situation": item["slug"].replace("arabic-b1-", "").replace("-", "_"),
                "conversation_goal": learner_goal(item),
                "grammar_summary": item["grammar"],
                "required_sections": REQUIRED_SECTIONS,
                "completion_rules": {
                    "listening_completed": True,
                    "quiz_required": True,
                    "speaking_attempt_required": True,
                    "minimum_score": 70,
                },
            },
        )

        (lesson_dir / "lesson.md").write_text(
            f"# {item['title']}\n\n"
            "Setelah lesson ini, kamu bisa memakai bahasa Arab formal untuk jawaban "
            "yang lebih terhubung, dengan konteks, alasan, dan langkah berikutnya.\n\n"
            "## Situation\n\n"
            f"{item['situation']}\n\n"
            "## Catatan Belajar\n\n"
            "Di B1, jangan hanya menjawab satu frasa. Bangun jawaban pendek yang saling "
            "terhubung: konteks, detail utama, alasan, dan penutup.\n",
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
            "Use distinct voices according to speaker names.\n",
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
                        "usage_note": entry["usage"],
                    }
                    for entry in item["phrases"]
                ]
            },
        )

        write_yaml(lesson_dir / "vocabulary.yaml", {"vocabulary": vocabulary_for_lesson(item["phrases"], item["dialogue"])})

        (lesson_dir / "grammar_for_conversation.md").write_text(
            "# Pola Percakapan\n\n"
            f"{item['grammar']}\n\n"
            "```txt\n"
            + "\n".join(item["patterns"])
            + "\n```\n\n"
            "Gunakan pola ini untuk membuat jawaban yang tetap pendek tetapi terhubung. "
            "Jika kalimat terasa panjang, pecah menjadi dua kalimat sederhana.\n",
            encoding="utf-8",
        )

        (lesson_dir / "pronunciation_drill.md").write_text(
            "# Latihan Pengucapan\n\n## Ulangi\n\n"
            + "\n".join(f"{index}. {entry['phrase']}" for index, entry in enumerate(item["phrases"][:5], 1))
            + "\n\n## Fokus\n\n"
            "- Jaga harakat akhir tetap terdengar cukup jelas.\n"
            "- Beri jeda kecil setelah frasa penghubung seperti ثُمَّ dan بَعْدَ ذَلِكَ.\n"
            "- Jangan mempercepat kalimat yang berisi alasan atau hasil.\n",
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
            "Baca kalimat dari kanan ke kiri. Cari dulu frasa penghubung, lalu pahami "
            "fungsi kalimat: konteks, alasan, hasil, atau langkah berikutnya.\n\n"
            + "\n".join(f"- {entry['phrase']} -> {entry['meaning']}" for entry in item["phrases"][:5])
            + "\n",
            encoding="utf-8",
        )

        (lesson_dir / "writing_support.md").write_text(
            "# Bantuan Menulis\n\n"
            "Tulis jawaban B1 pendek dengan empat bagian: konteks, detail utama, alasan, "
            "dan penutup. Gunakan frasa berikut sebagai kerangka.\n\n"
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


def update_tracker(units: list[dict[str, Any]]) -> None:
    raw_tracker = TRACKER_PATH.read_bytes()
    reader = csv.DictReader(io.StringIO(raw_tracker.decode("utf-8")))
    fieldnames = reader.fieldnames or []
    rows = list(reader)
    rows_by_key = {(row["level"], row["unit"], row["lesson"]): row for row in rows}

    for unit in units:
        for item in unit["lessons"]:
            key = ("arabic/B1", unit["unit_key"], item["lesson_key"])
            row = rows_by_key.get(key)
            if row is None:
                row = {name: "" for name in fieldnames}
                row["level"], row["unit"], row["lesson"] = key
                rows.append(row)
                rows_by_key[key] = row
            for column in TEXT_TRACKER_COLUMNS:
                row[column] = "done"
            row["audio_generated"] = "not_generated"
            row["review_status"] = "ready"
            row["publish_status"] = "published"

    with TRACKER_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    units = expand_units()
    write_level_files(units)
    for unit in units:
        write_unit_and_lessons(unit)
    update_tracker(units)
    print("Generated Arabic B1 curriculum content.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
