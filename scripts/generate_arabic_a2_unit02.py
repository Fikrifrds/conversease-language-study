#!/usr/bin/env python3
"""Generate Arabic A2 Unit 2 content."""
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
    "unit_key": "unit-02-plans-invitations",
    "title": "Plans & Invitations",
    "status": "published",
    "main_conversation_outcome": (
        "Invite someone, accept or decline politely, reschedule, and confirm time "
        "and place in Arabic."
    ),
    "lessons": [
        {
            "lesson_key": "lesson-01-making-a-simple-plan",
            "slug": "arabic-making-a-simple-plan",
            "title": "Making a Simple Plan",
            "status": "published",
            "situation": (
                "Kamu membuat rencana sederhana dengan teman: menentukan kegiatan, "
                "hari, waktu, dan tempat bertemu."
            ),
            "goal": "Make a simple plan and confirm time and place.",
            "grammar": (
                "Gunakan سَـ untuk rencana dekat, مَتَى untuk waktu, dan أَيْنَ untuk "
                "tempat bertemu."
            ),
            "patterns": [
                "سَأَذْهَبُ إِلَى ...",
                "مَتَى نَلْتَقِي؟",
                "نَلْتَقِي السَّاعَةَ ...",
                "أَمَامَ الْمَكْتَبَةِ.",
            ],
            "phrases": [
                phrase("سَأَذْهَبُ إِلَى الْمَكْتَبَةِ.", "Saya akan pergi ke perpustakaan.", "Menyebut rencana dekat."),
                phrase("هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي؟", "Apakah kamu ingin pergi bersama saya?", "Mengajak secara sederhana."),
                phrase("مَتَى نَلْتَقِي؟", "Kapan kita bertemu?", "Menanyakan waktu rencana."),
                phrase("نَلْتَقِي السَّاعَةَ الرَّابِعَةَ.", "Kita bertemu jam empat.", "Mengonfirmasi waktu."),
                phrase("أَمَامَ الْمَكْتَبَةِ.", "Di depan perpustakaan.", "Mengonfirmasi tempat."),
            ],
            "dialogue": [
                line("Khalid", "سَأَذْهَبُ إِلَى الْمَكْتَبَةِ بَعْدَ الدَّرْسِ.", "Saya akan pergi ke perpustakaan setelah pelajaran."),
                line("Zayd", "هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي؟", "Apakah kamu ingin pergi bersama saya?"),
                line("Khalid", "نَعَمْ، أُرِيدُ ذَلِكَ. مَتَى نَلْتَقِي؟", "Ya, saya ingin itu. Kapan kita bertemu?"),
                line("Zayd", "نَلْتَقِي السَّاعَةَ الرَّابِعَةَ.", "Kita bertemu jam empat."),
                line("Khalid", "أَيْنَ نَلْتَقِي؟", "Di mana kita bertemu?"),
                line("Zayd", "أَمَامَ الْمَكْتَبَةِ.", "Di depan perpustakaan."),
                line("Khalid", "حَسَنًا، إِلَى اللِّقَاءِ.", "Baik, sampai bertemu."),
            ],
        },
        {
            "lesson_key": "lesson-02-inviting-someone",
            "slug": "arabic-inviting-someone",
            "title": "Inviting Someone",
            "status": "published",
            "situation": (
                "Kamu mengajak teman ikut belajar bersama dan menjelaskan alasan singkat "
                "mengapa kegiatan itu bermanfaat."
            ),
            "goal": "Invite someone and give a short reason.",
            "grammar": (
                "Gunakan هَلْ تُرِيدُ أَنْ ... untuk ajakan dan لِأَنَّ untuk alasan pendek."
            ),
            "patterns": [
                "هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟",
                "لِأَنَّ الدَّرْسَ مُهِمٌّ.",
                "فِكْرَةٌ جَيِّدَةٌ.",
                "أَنَا مَوْجُودٌ.",
            ],
            "phrases": [
                phrase("هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", "Apakah kamu ingin belajar bersama saya?", "Mengajak belajar bersama."),
                phrase("لِأَنَّ الدَّرْسَ مُهِمٌّ.", "Karena pelajarannya penting.", "Memberi alasan singkat."),
                phrase("فِكْرَةٌ جَيِّدَةٌ.", "Ide yang bagus.", "Menerima ajakan dengan reaksi positif."),
                phrase("أَنَا مَوْجُودٌ بَعْدَ الْعَصْرِ.", "Saya ada setelah Asar.", "Memberi ketersediaan waktu."),
                phrase("نَدْرُسُ فِي الْمَرْكَزِ.", "Kita belajar di pusat.", "Mengonfirmasi tempat kegiatan."),
            ],
            "dialogue": [
                line("Maryam", "هَلْ تُرِيدِينَ أَنْ تَدْرُسِي مَعِي الْيَوْمَ؟", "Apakah kamu ingin belajar bersama saya hari ini?"),
                line("Noura", "رُبَّمَا. لِمَاذَا؟", "Mungkin. Mengapa?"),
                line("Maryam", "لِأَنَّ الدَّرْسَ مُهِمٌّ، وَالِاخْتِبَارَ قَرِيبٌ.", "Karena pelajarannya penting, dan tesnya dekat."),
                line("Noura", "فِكْرَةٌ جَيِّدَةٌ. أَنَا مَوْجُودَةٌ بَعْدَ الْعَصْرِ.", "Ide yang bagus. Saya ada setelah Asar."),
                line("Maryam", "جَيِّدٌ. نَدْرُسُ فِي الْمَرْكَزِ.", "Bagus. Kita belajar di pusat."),
                line("Noura", "حَسَنًا، سَأَحْضُرُ.", "Baik, saya akan hadir."),
            ],
        },
        {
            "lesson_key": "lesson-03-accepting-and-declining",
            "slug": "arabic-accepting-and-declining",
            "title": "Accepting and Declining",
            "status": "published",
            "situation": (
                "Kamu menerima satu ajakan dan menolak ajakan lain dengan sopan sambil "
                "memberi alasan pendek."
            ),
            "goal": "Accept and decline politely with a simple reason.",
            "grammar": (
                "Gunakan أَسْتَطِيعُ untuk bisa, لَا أَسْتَطِيعُ untuk tidak bisa, dan "
                "لِأَنَّ untuk alasan."
            ),
            "patterns": [
                "نَعَمْ، أَسْتَطِيعُ.",
                "آسِفٌ، لَا أَسْتَطِيعُ.",
                "لِأَنَّ لَدَيَّ مَوْعِدًا.",
                "رُبَّمَا فِي وَقْتٍ آخَرَ.",
            ],
            "phrases": [
                phrase("نَعَمْ، أَسْتَطِيعُ.", "Ya, saya bisa.", "Menerima ajakan."),
                phrase("آسِفٌ، لَا أَسْتَطِيعُ.", "Maaf, saya tidak bisa.", "Menolak dengan sopan."),
                phrase("لِأَنَّ لَدَيَّ مَوْعِدًا.", "Karena saya punya janji.", "Memberi alasan pendek."),
                phrase("رُبَّمَا فِي وَقْتٍ آخَرَ.", "Mungkin di waktu lain.", "Menawarkan kemungkinan lain."),
                phrase("لَا مُشْكِلَةَ.", "Tidak masalah.", "Merespons penolakan dengan sopan."),
            ],
            "dialogue": [
                line("Omar", "هَلْ تَأْتِي إِلَى الْمَكْتَبَةِ مَعِي؟", "Apakah kamu datang ke perpustakaan bersama saya?"),
                line("Ahmad", "نَعَمْ، أَسْتَطِيعُ بَعْدَ الظُّهْرِ.", "Ya, saya bisa setelah Zuhur."),
                line("Omar", "وَهَلْ تَأْتِي إِلَى السُّوقِ مَسَاءً؟", "Dan apakah kamu datang ke pasar sore?"),
                line("Ahmad", "آسِفٌ، لَا أَسْتَطِيعُ.", "Maaf, saya tidak bisa."),
                line("Omar", "لِمَاذَا؟", "Mengapa?"),
                line("Ahmad", "لِأَنَّ لَدَيَّ مَوْعِدًا مَعَ أُسْرَتِي.", "Karena saya punya janji dengan keluarga saya."),
                line("Omar", "لَا مُشْكِلَةَ. رُبَّمَا فِي وَقْتٍ آخَرَ.", "Tidak masalah. Mungkin di waktu lain."),
            ],
        },
        {
            "lesson_key": "lesson-04-rescheduling-politely",
            "slug": "arabic-rescheduling-politely",
            "title": "Rescheduling Politely",
            "status": "published",
            "situation": (
                "Kamu tidak bisa datang pada waktu awal, lalu meminta perubahan waktu "
                "dengan sopan."
            ),
            "goal": "Reschedule politely and confirm the new time.",
            "grammar": (
                "Gunakan هَلْ يُمْكِنُ أَنْ ... untuk permintaan sopan dan نُغَيِّرَ "
                "untuk mengubah waktu."
            ),
            "patterns": [
                "لَا أَسْتَطِيعُ فِي هَذَا الْوَقْتِ.",
                "هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟",
                "مَاذَا عَنِ السَّاعَةِ ...؟",
                "الْوَقْتُ مُنَاسِبٌ.",
            ],
            "phrases": [
                phrase("لَا أَسْتَطِيعُ فِي هَذَا الْوَقْتِ.", "Saya tidak bisa pada waktu ini.", "Menyampaikan kendala waktu."),
                phrase("هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", "Bisakah kita mengubah jadwalnya?", "Meminta reschedule dengan sopan."),
                phrase("مَاذَا عَنِ السَّاعَةِ الْخَامِسَةِ؟", "Bagaimana dengan jam lima?", "Menawarkan waktu baru."),
                phrase("الْوَقْتُ مُنَاسِبٌ.", "Waktunya cocok.", "Menyetujui waktu baru."),
                phrase("شُكْرًا عَلَى التَّفَهُّمِ.", "Terima kasih atas pengertiannya.", "Menutup dengan sopan."),
            ],
            "dialogue": [
                line("Sara", "نَلْتَقِي السَّاعَةَ الرَّابِعَةَ، صَحِيحٌ؟", "Kita bertemu jam empat, benar?"),
                line("Layla", "آسِفَةٌ، لَا أَسْتَطِيعُ فِي هَذَا الْوَقْتِ.", "Maaf, saya tidak bisa pada waktu ini."),
                line("Sara", "لَا مُشْكِلَةَ. هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", "Tidak masalah. Bisakah kita mengubah jadwalnya?"),
                line("Layla", "نَعَمْ. مَاذَا عَنِ السَّاعَةِ الْخَامِسَةِ؟", "Ya. Bagaimana dengan jam lima?"),
                line("Sara", "الْوَقْتُ مُنَاسِبٌ.", "Waktunya cocok."),
                line("Layla", "شُكْرًا عَلَى التَّفَهُّمِ.", "Terima kasih atas pengertiannya."),
            ],
        },
        {
            "lesson_key": "lesson-05-invitation-mission",
            "slug": "arabic-invitation-mission",
            "title": "Invitation Mission",
            "status": "published",
            "situation": (
                "Kamu membuat rencana belajar bersama, mengajak teman, menerima perubahan "
                "waktu, dan mengonfirmasi detail akhir."
            ),
            "goal": "Combine inviting, accepting, rescheduling, and confirming details.",
            "grammar": (
                "Gabungkan ajakan dengan هَلْ تُرِيدُ أَنْ, alasan dengan لِأَنَّ, "
                "dan reschedule dengan نُغَيِّرَ الْمَوْعِدَ."
            ),
            "patterns": [
                "هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟",
                "لِأَنَّ الِاخْتِبَارَ قَرِيبٌ.",
                "هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟",
                "نَلْتَقِي أَمَامَ الْمَرْكَزِ.",
            ],
            "phrases": [
                phrase("هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", "Apakah kamu ingin belajar bersama saya?", "Mengajak teman."),
                phrase("لِأَنَّ الِاخْتِبَارَ قَرِيبٌ.", "Karena tesnya dekat.", "Memberi alasan ajakan."),
                phrase("هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", "Bisakah kita mengubah jadwalnya?", "Meminta perubahan waktu."),
                phrase("نَلْتَقِي أَمَامَ الْمَرْكَزِ.", "Kita bertemu di depan pusat.", "Mengonfirmasi tempat."),
                phrase("إِلَى اللِّقَاءِ.", "Sampai bertemu.", "Menutup rencana."),
            ],
            "dialogue": [
                line("Fatimah", "هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي الْيَوْمَ؟", "Apakah kamu ingin belajar bersama saya hari ini?"),
                line("Raka", "نَعَمْ، وَلَكِنْ لِمَاذَا الْيَوْمَ؟", "Ya, tetapi mengapa hari ini?"),
                line("Fatimah", "لِأَنَّ الِاخْتِبَارَ قَرِيبٌ.", "Karena tesnya dekat."),
                line("Raka", "حَسَنًا. نَلْتَقِي السَّاعَةَ الرَّابِعَةَ؟", "Baik. Kita bertemu jam empat?"),
                line("Fatimah", "آسِفَةٌ، هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", "Maaf, bisakah kita mengubah jadwalnya?"),
                line("Raka", "نَعَمْ. مَاذَا عَنِ السَّاعَةِ الْخَامِسَةِ؟", "Ya. Bagaimana dengan jam lima?"),
                line("Fatimah", "جَيِّدٌ. نَلْتَقِي أَمَامَ الْمَرْكَزِ.", "Bagus. Kita bertemu di depan pusat."),
                line("Raka", "حَسَنًا، إِلَى اللِّقَاءِ.", "Baik, sampai bertemu."),
            ],
        },
    ],
}


def main() -> None:
    generator.UNIT = UNIT
    generator.main()


if __name__ == "__main__":
    main()
