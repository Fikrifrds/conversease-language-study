#!/usr/bin/env python3
"""Generate Arabic A2 Unit 6 content."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve().with_name("generate_arabic_a2_unit01.py")
spec = importlib.util.spec_from_file_location("generate_arabic_a2_unit01", SCRIPT_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load Arabic A2 generator helpers.")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)

phrase = generator.phrase
line = generator.line


UNIT: dict[str, Any] = {
    "unit_key": "unit-06-past-experiences",
    "title": "Past Experiences",
    "status": "published",
    "main_conversation_outcome": (
        "Talk about recent activities, where you went, what happened, and how it felt."
    ),
    "lessons": [
        {
            "lesson_key": "lesson-01-talking-about-yesterday",
            "slug": "arabic-talking-about-yesterday",
            "title": "Talking About Yesterday",
            "status": "published",
            "situation": (
                "Kamu bertemu teman setelah kelas dan menceritakan kegiatan kemarin "
                "dengan kalimat pendek."
            ),
            "goal": "Say what you did yesterday using short past-tense sentences.",
            "grammar": (
                "Gunakan أَمْسِ untuk kemarin, ذَهَبْتُ untuk saya pergi, dan "
                "دَرَسْتُ untuk saya belajar."
            ),
            "patterns": [
                "مَاذَا فَعَلْتَ أَمْسِ؟",
                "ذَهَبْتُ إِلَى ...",
                "دَرَسْتُ فِي ...",
                "كَانَ الْيَوْمُ جَيِّدًا.",
            ],
            "phrases": [
                phrase("مَاذَا فَعَلْتَ أَمْسِ؟", "Apa yang kamu lakukan kemarin?", "Menanyakan aktivitas kemarin kepada laki-laki."),
                phrase("ذَهَبْتُ إِلَى الْمَكْتَبَةِ.", "Saya pergi ke perpustakaan.", "Menceritakan tempat yang dikunjungi."),
                phrase("دَرَسْتُ بَعْضَ الْعَرَبِيَّةِ.", "Saya belajar sedikit bahasa Arab.", "Menyebut aktivitas belajar."),
                phrase("بَعْدَ ذَلِكَ، رَجَعْتُ إِلَى الْبَيْتِ.", "Setelah itu, saya kembali ke rumah.", "Mengurutkan kegiatan."),
                phrase("كَانَ الْيَوْمُ جَيِّدًا.", "Harinya baik.", "Memberi penilaian singkat."),
            ],
            "dialogue": [
                line("Khalid", "مَاذَا فَعَلْتِ أَمْسِ يَا لَيْلَى؟", "Apa yang kamu lakukan kemarin, Layla?"),
                line("Layla", "ذَهَبْتُ إِلَى الْمَكْتَبَةِ بَعْدَ الظُّهْرِ.", "Saya pergi ke perpustakaan setelah Zuhur."),
                line("Khalid", "مَاذَا دَرَسْتِ هُنَاكَ؟", "Apa yang kamu pelajari di sana?"),
                line("Layla", "دَرَسْتُ بَعْضَ الْعَرَبِيَّةِ، وَقَرَأْتُ نَصًّا قَصِيرًا.", "Saya belajar sedikit bahasa Arab, dan membaca teks pendek."),
                line("Khalid", "وَبَعْدَ ذَلِكَ؟", "Dan setelah itu?"),
                line("Layla", "بَعْدَ ذَلِكَ، رَجَعْتُ إِلَى الْبَيْتِ.", "Setelah itu, saya kembali ke rumah."),
                line("Khalid", "جَيِّدٌ. كَانَ يَوْمُكِ مُفِيدًا.", "Bagus. Harimu bermanfaat."),
            ],
        },
        {
            "lesson_key": "lesson-02-saying-where-you-went",
            "slug": "arabic-saying-where-you-went",
            "title": "Saying Where You Went",
            "status": "published",
            "situation": (
                "Kamu menceritakan tempat yang kamu datangi akhir pekan lalu: pasar, "
                "taman, rumah teman, atau pusat kota."
            ),
            "goal": "Say where you went and who you went with.",
            "grammar": (
                "Gunakan ذَهَبْتُ إِلَى untuk tempat, مَعَ untuk bersama siapa, dan "
                "فِي الصَّبَاحِ atau فِي الْمَسَاءِ untuk waktu."
            ),
            "patterns": [
                "أَيْنَ ذَهَبْتَ؟",
                "ذَهَبْتُ إِلَى السُّوقِ.",
                "ذَهَبْتُ مَعَ صَدِيقِي.",
                "فِي الْمَسَاءِ رَجَعْتُ.",
            ],
            "phrases": [
                phrase("أَيْنَ ذَهَبْتَ؟", "Ke mana kamu pergi?", "Menanyakan tempat kepada laki-laki."),
                phrase("ذَهَبْتُ إِلَى السُّوقِ.", "Saya pergi ke pasar.", "Menyebut tujuan."),
                phrase("ذَهَبْتُ مَعَ صَدِيقِي.", "Saya pergi bersama teman saya.", "Menyebut teman perjalanan."),
                phrase("فِي الصَّبَاحِ.", "Pada pagi hari.", "Menyebut waktu."),
                phrase("رَجَعْتُ فِي الْمَسَاءِ.", "Saya kembali pada sore hari.", "Menutup cerita perjalanan."),
            ],
            "dialogue": [
                line("Noura", "أَيْنَ ذَهَبْتَ فِي نِهَايَةِ الْأُسْبُوعِ يَا عُمَرُ؟", "Ke mana kamu pergi pada akhir pekan, Omar?"),
                line("Omar", "ذَهَبْتُ إِلَى السُّوقِ فِي الصَّبَاحِ.", "Saya pergi ke pasar pada pagi hari."),
                line("Noura", "هَلْ ذَهَبْتَ وَحْدَكَ؟", "Apakah kamu pergi sendiri?"),
                line("Omar", "لَا، ذَهَبْتُ مَعَ صَدِيقِي أَحْمَدَ.", "Tidak, saya pergi bersama teman saya Ahmad."),
                line("Noura", "مَاذَا اشْتَرَيْتَ؟", "Apa yang kamu beli?"),
                line("Omar", "اشْتَرَيْتُ كِتَابًا صَغِيرًا وَقَلَمًا.", "Saya membeli buku kecil dan pulpen."),
                line("Noura", "جَمِيلٌ. رَجَعْتَ فِي الْمَسَاءِ؟", "Bagus. Kamu kembali pada sore hari?"),
                line("Omar", "نَعَمْ، رَجَعْتُ فِي الْمَسَاءِ.", "Ya, saya kembali pada sore hari."),
            ],
        },
        {
            "lesson_key": "lesson-03-describing-a-simple-experience",
            "slug": "arabic-describing-a-simple-experience",
            "title": "Describing a Simple Experience",
            "status": "published",
            "situation": (
                "Kamu menceritakan pengalaman sederhana di tempat umum: apa yang kamu "
                "lihat, apa yang kamu lakukan, dan bagaimana rasanya."
            ),
            "goal": "Describe a simple past experience with a short feeling or opinion.",
            "grammar": (
                "Gunakan كَانَ atau كَانَتْ untuk menggambarkan pengalaman, رَأَيْتُ "
                "untuk saya melihat, dan أَعْجَبَنِي untuk saya suka."
            ),
            "patterns": [
                "كَانَتِ التَّجْرِبَةُ جَيِّدَةً.",
                "رَأَيْتُ مَكَانًا جَمِيلًا.",
                "أَعْجَبَنِي الطَّعَامُ.",
                "لَكِنَّ الْمَكَانَ كَانَ مُزْدَحِمًا.",
            ],
            "phrases": [
                phrase("كَانَتِ التَّجْرِبَةُ جَيِّدَةً.", "Pengalamannya baik.", "Menilai pengalaman."),
                phrase("رَأَيْتُ مَكَانًا جَمِيلًا.", "Saya melihat tempat yang indah.", "Menyebut hal yang dilihat."),
                phrase("أَعْجَبَنِي الطَّعَامُ.", "Saya suka makanannya.", "Mengatakan kesan positif."),
                phrase("كَانَ الْمَكَانُ مُزْدَحِمًا.", "Tempatnya ramai.", "Menggambarkan suasana."),
                phrase("أُرِيدُ أَنْ أَذْهَبَ مَرَّةً أُخْرَى.", "Saya ingin pergi sekali lagi.", "Menutup dengan rencana ringan."),
            ],
            "dialogue": [
                line("Sara", "كَيْفَ كَانَتْ رِحْلَتُكَ إِلَى الْحَدِيقَةِ؟", "Bagaimana perjalananmu ke taman?"),
                line("Rami", "كَانَتِ التَّجْرِبَةُ جَيِّدَةً.", "Pengalamannya baik."),
                line("Sara", "مَاذَا رَأَيْتَ هُنَاكَ؟", "Apa yang kamu lihat di sana?"),
                line("Rami", "رَأَيْتُ مَكَانًا جَمِيلًا وَبُحَيْرَةً صَغِيرَةً.", "Saya melihat tempat indah dan danau kecil."),
                line("Sara", "هَلْ أَعْجَبَكَ الطَّعَامُ؟", "Apakah kamu suka makanannya?"),
                line("Rami", "نَعَمْ، أَعْجَبَنِي الطَّعَامُ، وَلَكِنَّ الْمَكَانَ كَانَ مُزْدَحِمًا.", "Ya, saya suka makanannya, tetapi tempatnya ramai."),
                line("Sara", "هَلْ تُرِيدُ أَنْ تَذْهَبَ مَرَّةً أُخْرَى؟", "Apakah kamu ingin pergi sekali lagi?"),
                line("Rami", "نَعَمْ، أُرِيدُ ذَلِكَ.", "Ya, saya ingin itu."),
            ],
        },
        {
            "lesson_key": "lesson-04-asking-about-past-activities",
            "slug": "arabic-asking-about-past-activities",
            "title": "Asking About Past Activities",
            "status": "published",
            "situation": (
                "Kamu ingin menjaga percakapan tetap berjalan dengan bertanya tentang "
                "aktivitas masa lalu teman secara sopan dan natural."
            ),
            "goal": "Ask follow-up questions about someone's past activities.",
            "grammar": (
                "Gunakan مَاذَا فَعَلْتَ, مَعَ مَنْ, أَيْنَ, dan كَيْفَ كَانَ untuk "
                "pertanyaan lanjutan masa lalu."
            ),
            "patterns": [
                "مَاذَا فَعَلْتَ؟",
                "مَعَ مَنْ ذَهَبْتَ؟",
                "كَيْفَ كَانَ الْمَكَانُ؟",
                "هَلْ أَعْجَبَكَ؟",
            ],
            "phrases": [
                phrase("مَاذَا فَعَلْتَ بَعْدَ الدَّرْسِ؟", "Apa yang kamu lakukan setelah pelajaran?", "Membuka pertanyaan masa lalu."),
                phrase("مَعَ مَنْ ذَهَبْتَ؟", "Dengan siapa kamu pergi?", "Menanyakan teman aktivitas."),
                phrase("كَيْفَ كَانَ الْمَكَانُ؟", "Bagaimana tempatnya?", "Menanyakan kesan."),
                phrase("هَلْ أَعْجَبَكَ؟", "Apakah kamu menyukainya?", "Menanyakan pendapat."),
                phrase("مَاذَا فَعَلْتَ بَعْدَ ذَلِكَ؟", "Apa yang kamu lakukan setelah itu?", "Melanjutkan percakapan."),
            ],
            "dialogue": [
                line("Ahmad", "مَاذَا فَعَلْتِ بَعْدَ الدَّرْسِ يَا مَرْيَمُ؟", "Apa yang kamu lakukan setelah pelajaran, Maryam?"),
                line("Maryam", "ذَهَبْتُ إِلَى مَقْهًى قَرِيبٍ.", "Saya pergi ke kafe dekat sini."),
                line("Ahmad", "مَعَ مَنْ ذَهَبْتِ؟", "Dengan siapa kamu pergi?"),
                line("Maryam", "ذَهَبْتُ مَعَ نُورَةَ.", "Saya pergi bersama Noura."),
                line("Ahmad", "كَيْفَ كَانَ الْمَكَانُ؟", "Bagaimana tempatnya?"),
                line("Maryam", "كَانَ هَادِئًا، وَأَعْجَبَنِي الشَّايُ.", "Tempatnya tenang, dan saya suka tehnya."),
                line("Ahmad", "مَاذَا فَعَلْتِ بَعْدَ ذَلِكَ؟", "Apa yang kamu lakukan setelah itu?"),
                line("Maryam", "رَجَعْتُ إِلَى الْبَيْتِ وَكَتَبْتُ وَاجِبِي.", "Saya kembali ke rumah dan menulis tugas saya."),
            ],
        },
        {
            "lesson_key": "lesson-05-past-experience-mission",
            "slug": "arabic-past-experience-mission",
            "title": "Past Experience Mission",
            "status": "published",
            "situation": (
                "Kamu menceritakan pengalaman akhir pekan dan menjawab pertanyaan "
                "lanjutan tentang tempat, teman, kegiatan, dan kesan."
            ),
            "goal": "Combine past activities, places, sequence, and simple reactions.",
            "grammar": (
                "Gabungkan ذَهَبْتُ, رَأَيْتُ, اشْتَرَيْتُ, كَانَ, dan بَعْدَ ذَلِكَ "
                "untuk cerita pendek yang runtut."
            ),
            "patterns": [
                "فِي نِهَايَةِ الْأُسْبُوعِ، ذَهَبْتُ إِلَى ...",
                "رَأَيْتُ ...",
                "بَعْدَ ذَلِكَ، ...",
                "كَانَتِ التَّجْرِبَةُ ...",
            ],
            "phrases": [
                phrase("فِي نِهَايَةِ الْأُسْبُوعِ، ذَهَبْتُ إِلَى الْمَدِينَةِ.", "Pada akhir pekan, saya pergi ke kota.", "Membuka cerita akhir pekan."),
                phrase("رَأَيْتُ مَكَانًا جَدِيدًا.", "Saya melihat tempat baru.", "Menyebut pengalaman baru."),
                phrase("اشْتَرَيْتُ شَيْئًا صَغِيرًا.", "Saya membeli sesuatu yang kecil.", "Menyebut aktivitas belanja ringan."),
                phrase("بَعْدَ ذَلِكَ، رَجَعْتُ إِلَى الْبَيْتِ.", "Setelah itu, saya kembali ke rumah.", "Mengurutkan kejadian."),
                phrase("كَانَتِ التَّجْرِبَةُ مُفِيدَةً.", "Pengalamannya bermanfaat.", "Menutup dengan kesan."),
            ],
            "dialogue": [
                line("Dimas", "مَاذَا فَعَلْتِ فِي نِهَايَةِ الْأُسْبُوعِ يَا سَارَةُ؟", "Apa yang kamu lakukan pada akhir pekan, Sara?"),
                line("Sara", "ذَهَبْتُ إِلَى الْمَدِينَةِ مَعَ أُخْتِي.", "Saya pergi ke kota bersama saudari saya."),
                line("Dimas", "مَاذَا رَأَيْتِ هُنَاكَ؟", "Apa yang kamu lihat di sana?"),
                line("Sara", "رَأَيْتُ مَكَانًا جَدِيدًا وَمَتْجَرًا صَغِيرًا.", "Saya melihat tempat baru dan toko kecil."),
                line("Dimas", "هَلِ اشْتَرَيْتِ شَيْئًا؟", "Apakah kamu membeli sesuatu?"),
                line("Sara", "نَعَمْ، اشْتَرَيْتُ دَفْتَرًا وَقَلَمًا.", "Ya, saya membeli buku catatan dan pulpen."),
                line("Dimas", "كَيْفَ كَانَتِ التَّجْرِبَةُ؟", "Bagaimana pengalamannya?"),
                line("Sara", "كَانَتِ التَّجْرِبَةُ مُفِيدَةً، وَلَكِنَّ الْمَكَانَ كَانَ مُزْدَحِمًا.", "Pengalamannya bermanfaat, tetapi tempatnya ramai."),
                line("Dimas", "وَبَعْدَ ذَلِكَ؟", "Dan setelah itu?"),
                line("Sara", "بَعْدَ ذَلِكَ، رَجَعْتُ إِلَى الْبَيْتِ.", "Setelah itu, saya kembali ke rumah."),
            ],
        },
    ],
}


def main() -> None:
    generator.UNIT = UNIT
    generator.main()


if __name__ == "__main__":
    main()
