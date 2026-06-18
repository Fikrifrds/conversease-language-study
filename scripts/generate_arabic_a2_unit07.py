#!/usr/bin/env python3
"""Generate Arabic A2 Unit 7 content."""
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
    "unit_key": "unit-07-opinions-reasons",
    "title": "Opinions & Reasons",
    "status": "published",
    "main_conversation_outcome": (
        "Give simple opinions, short reasons, agreement, disagreement, and preference "
        "in Arabic."
    ),
    "lessons": [
        {
            "lesson_key": "lesson-01-saying-what-you-think",
            "slug": "arabic-saying-what-you-think",
            "title": "Saying What You Think",
            "status": "published",
            "situation": (
                "Kamu berdiskusi santai setelah kelas dan ingin menyampaikan pendapat "
                "tentang pelajaran, tempat belajar, atau aktivitas."
            ),
            "goal": "Say what you think using simple opinion phrases.",
            "grammar": (
                "Gunakan أَعْتَقِدُ أَنَّ untuk 'saya pikir bahwa', فِي رَأْيِي "
                "untuk 'menurut saya', dan هَذَا untuk merujuk hal yang sedang dibahas."
            ),
            "patterns": [
                "أَعْتَقِدُ أَنَّ الدَّرْسَ مُفِيدٌ.",
                "فِي رَأْيِي، هَذَا جَيِّدٌ.",
                "أَرَى أَنَّ الْمَكَانَ مُنَاسِبٌ.",
                "هَذَا أَفْضَلُ لِي.",
            ],
            "phrases": [
                phrase("أَعْتَقِدُ أَنَّ الدَّرْسَ مُفِيدٌ.", "Saya pikir pelajarannya bermanfaat.", "Menyampaikan pendapat dengan أَعْتَقِدُ."),
                phrase("فِي رَأْيِي، هَذَا جَيِّدٌ.", "Menurut saya, ini baik.", "Memberi pendapat pendek."),
                phrase("أَرَى أَنَّ الْمَكَانَ مُنَاسِبٌ.", "Saya melihat bahwa tempatnya cocok.", "Menyampaikan penilaian."),
                phrase("هَذَا أَفْضَلُ لِي.", "Ini lebih baik untuk saya.", "Menyatakan pilihan pribadi."),
                phrase("مَا رَأْيُكَ؟", "Apa pendapatmu?", "Meminta pendapat lawan bicara."),
            ],
            "dialogue": [
                line("Khalid", "مَا رَأْيُكِ فِي الدَّرْسِ الْيَوْمَ يَا نُورَةُ؟", "Apa pendapatmu tentang pelajaran hari ini, Noura?"),
                line("Noura", "أَعْتَقِدُ أَنَّ الدَّرْسَ مُفِيدٌ.", "Saya pikir pelajarannya bermanfaat."),
                line("Khalid", "لِمَاذَا؟", "Mengapa?"),
                line("Noura", "لِأَنَّ الْحِوَارَ كَانَ وَاضِحًا وَسَهْلًا.", "Karena dialognya jelas dan mudah."),
                line("Khalid", "فِي رَأْيِي، التَّدْرِيبُ بَعْدَ الدَّرْسِ مُهِمٌّ أَيْضًا.", "Menurut saya, latihan setelah pelajaran juga penting."),
                line("Noura", "نَعَمْ، أُوَافِقُكَ.", "Ya, saya setuju denganmu."),
            ],
        },
        {
            "lesson_key": "lesson-02-giving-simple-reasons",
            "slug": "arabic-giving-simple-reasons",
            "title": "Giving Simple Reasons",
            "status": "published",
            "situation": (
                "Kamu menjelaskan alasan pendek untuk pendapatmu: karena mudah, dekat, "
                "murah, jelas, atau cocok untuk jadwalmu."
            ),
            "goal": "Give simple reasons using because and short supporting details.",
            "grammar": (
                "Gunakan لِأَنَّ untuk 'karena', dan sambungkan alasan dengan وَ atau "
                "وَلَكِنَّ ketika ada kontras sederhana."
            ),
            "patterns": [
                "أُحِبُّ هَذَا لِأَنَّهُ سَهْلٌ.",
                "أُفَضِّلُ هَذَا لِأَنَّهُ قَرِيبٌ.",
                "هُوَ جَيِّدٌ، وَلَكِنَّهُ غَالٍ.",
                "السَّبَبُ بَسِيطٌ.",
            ],
            "phrases": [
                phrase("أُحِبُّ هَذَا لِأَنَّهُ سَهْلٌ.", "Saya suka ini karena mudah.", "Memberi alasan sederhana."),
                phrase("أُفَضِّلُ هَذَا لِأَنَّهُ قَرِيبٌ.", "Saya lebih memilih ini karena dekat.", "Memberi alasan pilihan."),
                phrase("هُوَ جَيِّدٌ، وَلَكِنَّهُ غَالٍ.", "Itu bagus, tetapi mahal.", "Memberi alasan dengan kontras."),
                phrase("السَّبَبُ بَسِيطٌ.", "Alasannya sederhana.", "Membuka penjelasan alasan."),
                phrase("لِأَنَّ الْوَقْتَ مُنَاسِبٌ.", "Karena waktunya cocok.", "Memberi alasan waktu."),
            ],
            "dialogue": [
                line("Layla", "أَيُّ مَكَانٍ تُفَضِّلُ لِلدِّرَاسَةِ يَا رَامِي؟", "Tempat mana yang kamu pilih untuk belajar, Rami?"),
                line("Rami", "أُفَضِّلُ الْمَكْتَبَةَ.", "Saya lebih memilih perpustakaan."),
                line("Layla", "لِمَاذَا؟", "Mengapa?"),
                line("Rami", "السَّبَبُ بَسِيطٌ. أُفَضِّلُهَا لِأَنَّهَا هَادِئَةٌ وَقَرِيبَةٌ.", "Alasannya sederhana. Saya memilihnya karena tenang dan dekat."),
                line("Layla", "وَالْمَقْهَى؟", "Dan kafe?"),
                line("Rami", "الْمَقْهَى جَيِّدٌ، وَلَكِنَّهُ مُزْدَحِمٌ.", "Kafe bagus, tetapi ramai."),
                line("Layla", "فَهِمْتُ. الْمَكْتَبَةُ أَفْضَلُ لَكَ.", "Saya mengerti. Perpustakaan lebih baik untukmu."),
            ],
        },
        {
            "lesson_key": "lesson-03-agreeing-and-disagreeing-politely",
            "slug": "arabic-agreeing-and-disagreeing-politely",
            "title": "Agreeing and Disagreeing Politely",
            "status": "published",
            "situation": (
                "Kamu berdiskusi dengan teman dan perlu setuju, kurang setuju, atau "
                "memberi pendapat berbeda tanpa terdengar kasar."
            ),
            "goal": "Agree and disagree politely with short reasons.",
            "grammar": (
                "Gunakan أُوَافِقُكَ untuk setuju kepada laki-laki, أُوَافِقُكِ "
                "kepada perempuan, dan لَا أُوَافِقُ تَمَامًا untuk kurang setuju."
            ),
            "patterns": [
                "أُوَافِقُكَ.",
                "أُوَافِقُكِ فِي هَذَا.",
                "لَا أُوَافِقُ تَمَامًا.",
                "فِي رَأْيِي، هُنَاكَ خِيَارٌ أَفْضَلُ.",
            ],
            "phrases": [
                phrase("أُوَافِقُكَ.", "Saya setuju denganmu.", "Setuju kepada laki-laki."),
                phrase("أُوَافِقُكِ فِي هَذَا.", "Saya setuju denganmu dalam hal ini.", "Setuju kepada perempuan."),
                phrase("لَا أُوَافِقُ تَمَامًا.", "Saya tidak sepenuhnya setuju.", "Tidak setuju dengan sopan."),
                phrase("فِي رَأْيِي، هُنَاكَ خِيَارٌ أَفْضَلُ.", "Menurut saya, ada pilihan yang lebih baik.", "Memberi alternatif sopan."),
                phrase("أَفْهَمُ رَأْيَكَ.", "Saya memahami pendapatmu.", "Menghargai pendapat orang lain."),
            ],
            "dialogue": [
                line("Ahmad", "أَعْتَقِدُ أَنَّ الدِّرَاسَةَ فِي الْبَيْتِ أَفْضَلُ.", "Saya pikir belajar di rumah lebih baik."),
                line("Sara", "أَفْهَمُ رَأْيَكَ، وَلَكِنْ لَا أُوَافِقُ تَمَامًا.", "Saya memahami pendapatmu, tetapi saya tidak sepenuhnya setuju."),
                line("Ahmad", "لِمَاذَا؟", "Mengapa?"),
                line("Sara", "فِي رَأْيِي، الدِّرَاسَةُ مَعَ صَدِيقَةٍ أَفْضَلُ لِأَنَّهَا تُسَاعِدُنِي.", "Menurut saya, belajar dengan teman lebih baik karena ia membantu saya."),
                line("Ahmad", "هَذَا صَحِيحٌ أَيْضًا.", "Itu juga benar."),
                line("Sara", "إِذًا نَدْرُسُ مَعًا فِي الْمَكْتَبَةِ؟", "Jadi kita belajar bersama di perpustakaan?"),
                line("Ahmad", "نَعَمْ، أُوَافِقُكِ فِي هَذَا.", "Ya, saya setuju denganmu dalam hal ini."),
            ],
        },
        {
            "lesson_key": "lesson-04-asking-for-opinions",
            "slug": "arabic-asking-for-opinions",
            "title": "Asking for Opinions",
            "status": "published",
            "situation": (
                "Kamu meminta pendapat teman sebelum memilih tempat, waktu, aktivitas, "
                "atau opsi sederhana."
            ),
            "goal": "Ask for opinions and respond with a short follow-up question.",
            "grammar": (
                "Gunakan مَا رَأْيُكَ؟ untuk bertanya kepada laki-laki, مَا رَأْيُكِ؟ "
                "kepada perempuan, dan أَيُّهُمَا untuk dua pilihan."
            ),
            "patterns": [
                "مَا رَأْيُكَ فِي هَذَا؟",
                "مَا رَأْيُكِ فِي الْخِيَارِ الثَّانِي؟",
                "أَيُّهُمَا أَفْضَلُ؟",
                "هَلْ تَعْتَقِدُ أَنَّ هَذَا مُنَاسِبٌ؟",
            ],
            "phrases": [
                phrase("مَا رَأْيُكَ فِي هَذَا؟", "Apa pendapatmu tentang ini?", "Meminta pendapat laki-laki."),
                phrase("مَا رَأْيُكِ فِي الْخِيَارِ الثَّانِي؟", "Apa pendapatmu tentang pilihan kedua?", "Meminta pendapat perempuan."),
                phrase("أَيُّهُمَا أَفْضَلُ؟", "Mana dari keduanya yang lebih baik?", "Meminta perbandingan."),
                phrase("هَلْ تَعْتَقِدُ أَنَّ هَذَا مُنَاسِبٌ؟", "Apakah kamu pikir ini cocok?", "Meminta evaluasi."),
                phrase("أُرِيدُ رَأْيًا وَاضِحًا.", "Saya ingin pendapat yang jelas.", "Meminta kejelasan."),
            ],
            "dialogue": [
                line("Maryam", "مَا رَأْيُكَ فِي هَذَا الْجَدْوَلِ يَا دِيمَاسُ؟", "Apa pendapatmu tentang jadwal ini, Dimas?"),
                line("Dimas", "أَعْتَقِدُ أَنَّهُ جَيِّدٌ، وَلَكِنَّهُ طَوِيلٌ قَلِيلًا.", "Saya pikir itu baik, tetapi sedikit panjang."),
                line("Maryam", "أَيُّهُمَا أَفْضَلُ: الصَّبَاحُ أَمِ الْمَسَاءُ؟", "Mana yang lebih baik: pagi atau sore?"),
                line("Dimas", "فِي رَأْيِي، الصَّبَاحُ أَفْضَلُ لِأَنَّنَا نَكُونُ نَشِيطِينَ.", "Menurut saya, pagi lebih baik karena kita aktif."),
                line("Maryam", "هَلْ تَعْتَقِدُ أَنَّ السَّاعَةَ التَّاسِعَةَ مُنَاسِبَةٌ؟", "Apakah kamu pikir jam sembilan cocok?"),
                line("Dimas", "نَعَمْ، السَّاعَةُ التَّاسِعَةُ مُنَاسِبَةٌ.", "Ya, jam sembilan cocok."),
            ],
        },
        {
            "lesson_key": "lesson-05-opinion-conversation-mission",
            "slug": "arabic-opinion-conversation-mission",
            "title": "Opinion Conversation Mission",
            "status": "published",
            "situation": (
                "Kamu memilih rencana belajar bersama teman: meminta pendapat, memberi "
                "alasan, setuju/kurang setuju, lalu mengambil keputusan."
            ),
            "goal": "Combine opinions, reasons, agreement, disagreement, and preference.",
            "grammar": (
                "Gabungkan مَا رَأْيُكَ, أَعْتَقِدُ أَنَّ, لِأَنَّ, أُوَافِقُ, "
                "لَا أُوَافِقُ تَمَامًا, dan أُفَضِّلُ."
            ),
            "patterns": [
                "مَا رَأْيُكَ فِي ...؟",
                "أَعْتَقِدُ أَنَّ ...",
                "أُفَضِّلُ ... لِأَنَّ ...",
                "لَا أُوَافِقُ تَمَامًا.",
            ],
            "phrases": [
                phrase("مَا رَأْيُكَ فِي هَذِهِ الْخُطَّةِ؟", "Apa pendapatmu tentang rencana ini?", "Membuka diskusi rencana."),
                phrase("أَعْتَقِدُ أَنَّهَا جَيِّدَةٌ.", "Saya pikir itu baik.", "Memberi pendapat positif."),
                phrase("أُفَضِّلُ الصَّبَاحَ لِأَنَّهُ أَهْدَأُ.", "Saya lebih memilih pagi karena lebih tenang.", "Memberi pilihan dan alasan."),
                phrase("لَا أُوَافِقُ تَمَامًا.", "Saya tidak sepenuhnya setuju.", "Kurang setuju dengan sopan."),
                phrase("إِذًا نَخْتَارُ هَذَا.", "Jadi kita memilih ini.", "Menutup dengan keputusan."),
            ],
            "dialogue": [
                line("Khalid", "مَا رَأْيُكِ فِي هَذِهِ الْخُطَّةِ يَا لَيْلَى؟", "Apa pendapatmu tentang rencana ini, Layla?"),
                line("Layla", "أَعْتَقِدُ أَنَّهَا جَيِّدَةٌ، وَلَكِنَّ الْوَقْتَ غَيْرُ مُنَاسِبٍ.", "Saya pikir itu baik, tetapi waktunya tidak cocok."),
                line("Khalid", "أَيُّ وَقْتٍ تُفَضِّلِينَ؟", "Waktu apa yang kamu pilih?"),
                line("Layla", "أُفَضِّلُ الصَّبَاحَ لِأَنَّهُ أَهْدَأُ.", "Saya lebih memilih pagi karena lebih tenang."),
                line("Khalid", "لَا أُوَافِقُ تَمَامًا. الصَّبَاحُ صَعْبٌ لِي.", "Saya tidak sepenuhnya setuju. Pagi sulit untuk saya."),
                line("Layla", "أَفْهَمُ رَأْيَكَ. مَاذَا عَنِ السَّاعَةِ الْعَاشِرَةِ؟", "Saya memahami pendapatmu. Bagaimana dengan jam sepuluh?"),
                line("Khalid", "السَّاعَةُ الْعَاشِرَةُ مُنَاسِبَةٌ.", "Jam sepuluh cocok."),
                line("Layla", "إِذًا نَخْتَارُ هَذَا.", "Jadi kita memilih ini."),
            ],
        },
    ],
}


def main() -> None:
    generator.UNIT = UNIT
    generator.main()


if __name__ == "__main__":
    main()
