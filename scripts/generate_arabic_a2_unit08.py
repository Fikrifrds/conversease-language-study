#!/usr/bin/env python3
"""Generate Arabic A2 Unit 8 review and final content."""
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
    "unit_key": "unit-08-a2-review-final",
    "title": "A2 Review & Final Conversation",
    "status": "beta",
    "main_conversation_outcome": (
        "Combine Arabic A2 social, planning, travel, service, health, past, and "
        "opinion skills in practical formal conversations."
    ),
    "lessons": [
        {
            "lesson_key": "lesson-01-review-social-and-plans",
            "slug": "arabic-review-social-and-plans",
            "title": "Review Social and Plans",
            "status": "beta",
            "situation": (
                "Kamu bertemu teman setelah kelas, bertanya kabar, menanyakan rencana, "
                "lalu menentukan waktu belajar bersama."
            ),
            "goal": "Review follow-up questions, invitations, and confirming time/place.",
            "grammar": (
                "Ulangi كَيْفَ كَانَ, مَاذَا فَعَلْتَ, هَلْ تُرِيدُ أَنْ, dan "
                "نَلْتَقِي السَّاعَةَ untuk menjaga percakapan sosial dan rencana."
            ),
            "patterns": [
                "كَيْفَ كَانَ دَرْسُكَ؟",
                "مَاذَا فَعَلْتَ بَعْدَ الدَّرْسِ؟",
                "هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟",
                "نَلْتَقِي أَمَامَ الْمَرْكَزِ.",
            ],
            "phrases": [
                phrase("كَيْفَ كَانَ دَرْسُكَ؟", "Bagaimana pelajaranmu?", "Membuka follow-up sosial."),
                phrase("مَاذَا فَعَلْتَ بَعْدَ الدَّرْسِ؟", "Apa yang kamu lakukan setelah pelajaran?", "Menanyakan aktivitas."),
                phrase("هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", "Apakah kamu ingin belajar bersama saya?", "Mengajak belajar."),
                phrase("نَلْتَقِي السَّاعَةَ الْخَامِسَةَ.", "Kita bertemu jam lima.", "Mengonfirmasi waktu."),
                phrase("أَمَامَ الْمَرْكَزِ.", "Di depan pusat.", "Mengonfirmasi tempat."),
            ],
            "dialogue": [
                line("Khalid", "كَيْفَ كَانَ دَرْسُكِ الْيَوْمَ يَا مَرْيَمُ؟", "Bagaimana pelajaranmu hari ini, Maryam?"),
                line("Maryam", "كَانَ مُفِيدًا، وَلَكِنَّهُ كَانَ طَوِيلًا قَلِيلًا.", "Pelajarannya bermanfaat, tetapi sedikit panjang."),
                line("Khalid", "مَاذَا فَعَلْتِ بَعْدَ الدَّرْسِ؟", "Apa yang kamu lakukan setelah pelajaran?"),
                line("Maryam", "قَرَأْتُ النَّصَّ مَرَّةً أُخْرَى.", "Saya membaca teks sekali lagi."),
                line("Khalid", "هَلْ تُرِيدِينَ أَنْ تَدْرُسِي مَعِي مَسَاءً؟", "Apakah kamu ingin belajar bersama saya sore ini?"),
                line("Maryam", "نَعَمْ. مَتَى نَلْتَقِي؟", "Ya. Kapan kita bertemu?"),
                line("Khalid", "نَلْتَقِي السَّاعَةَ الْخَامِسَةَ أَمَامَ الْمَرْكَزِ.", "Kita bertemu jam lima di depan pusat."),
                line("Maryam", "حَسَنًا، الْوَقْتُ مُنَاسِبٌ.", "Baik, waktunya cocok."),
            ],
        },
        {
            "lesson_key": "lesson-02-review-travel-and-services",
            "slug": "arabic-review-travel-and-services",
            "title": "Review Travel and Services",
            "status": "beta",
            "situation": (
                "Kamu membeli tiket, menanyakan arah, lalu meminta bantuan layanan "
                "untuk barang kecil yang bermasalah."
            ),
            "goal": "Review ticket buying, directions, item choice, and service help.",
            "grammar": (
                "Ulangi أُرِيدُ, مَتَى يَغَادِرُ, كَيْفَ أَذْهَبُ, هَلْ عِنْدَكُمْ, "
                "dan هَلْ يُمْكِنُ أَنْ تُسَاعِدَنِي."
            ),
            "patterns": [
                "أُرِيدُ تَذْكِرَةً إِلَى ...",
                "مَتَى يَغَادِرُ الْقِطَارُ؟",
                "كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟",
                "هَلْ يُمْكِنُ أَنْ تُسَاعِدَنِي؟",
            ],
            "phrases": [
                phrase("أُرِيدُ تَذْكِرَةً إِلَى بَانْدُونْغ.", "Saya ingin tiket ke Bandung.", "Membeli tiket."),
                phrase("مَتَى يَغَادِرُ الْقِطَارُ؟", "Kapan keretanya berangkat?", "Menanyakan keberangkatan."),
                phrase("كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", "Bagaimana saya pergi ke peron?", "Menanyakan arah."),
                phrase("هَلْ عِنْدَكُمْ لَوْنٌ آخَرُ؟", "Apakah kalian punya warna lain?", "Menanyakan opsi barang."),
                phrase("الْجِهَازُ لَا يَعْمَلُ.", "Perangkatnya tidak bekerja.", "Menjelaskan masalah layanan."),
            ],
            "dialogue": [
                line("Dimas", "أُرِيدُ تَذْكِرَةً إِلَى بَانْدُونْغ، مِنْ فَضْلِكَ.", "Saya ingin tiket ke Bandung, tolong."),
                line("Ahmad", "ذَهَابًا فَقَطْ؟", "Sekali jalan saja?"),
                line("Dimas", "نَعَمْ. مَتَى يَغَادِرُ الْقِطَارُ؟", "Ya. Kapan keretanya berangkat?"),
                line("Ahmad", "يُغَادِرُ السَّاعَةَ الثَّامِنَةَ مِنَ الرَّصِيفِ الثَّانِي.", "Berangkat jam delapan dari peron dua."),
                line("Dimas", "كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", "Bagaimana saya pergi ke peron?"),
                line("Ahmad", "اِمْشِ مُسْتَقِيمًا، ثُمَّ اِتَّجِهْ يَمِينًا.", "Berjalan lurus, lalu belok kanan."),
                line("Dimas", "شُكْرًا. وَبَعْدَ الرِّحْلَةِ أَحْتَاجُ إِلَى مُسَاعَدَةٍ فِي هَذَا الْجِهَازِ.", "Terima kasih. Setelah perjalanan, saya butuh bantuan untuk perangkat ini."),
                line("Ahmad", "قِسْمُ الْخِدْمَةِ بِجَانِبِ الْبَابِ.", "Bagian layanan ada di samping pintu."),
            ],
        },
        {
            "lesson_key": "lesson-03-review-health-and-past",
            "slug": "arabic-review-health-and-past",
            "title": "Review Health and Past",
            "status": "beta",
            "situation": (
                "Kamu menghubungi klinik, menjelaskan gejala ringan, lalu menceritakan "
                "aktivitas kemarin yang mungkin perlu dicatat."
            ),
            "goal": "Review simple health phrases and past activity narration.",
            "grammar": (
                "Ulangi لَا أَشْعُرُ بِالرَّاحَةِ, عِنْدِي, مُنْذُ, ذَهَبْتُ, "
                "ورَجَعْتُ untuk menggabungkan kondisi dan aktivitas masa lalu."
            ),
            "patterns": [
                "لَا أَشْعُرُ بِالرَّاحَةِ.",
                "عِنْدِي أَلَمٌ خَفِيفٌ.",
                "مُنْذُ أَمْسِ.",
                "ذَهَبْتُ إِلَى ...",
            ],
            "phrases": [
                phrase("لَا أَشْعُرُ بِالرَّاحَةِ.", "Saya tidak merasa nyaman.", "Menyebut kondisi."),
                phrase("عِنْدِي أَلَمٌ خَفِيفٌ.", "Saya punya sakit ringan.", "Menyebut gejala."),
                phrase("مُنْذُ أَمْسِ.", "Sejak kemarin.", "Menyebut durasi."),
                phrase("ذَهَبْتُ إِلَى الْمَدِينَةِ.", "Saya pergi ke kota.", "Menceritakan aktivitas lalu."),
                phrase("رَجَعْتُ فِي الْمَسَاءِ.", "Saya kembali pada sore hari.", "Menutup urutan aktivitas."),
            ],
            "dialogue": [
                line("Sara", "مَرْحَبًا، أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", "Halo, saya ingin janji dengan dokter."),
                line("Fatimah", "مَا الَّذِي تَشْعُرِينَ بِهِ؟", "Apa yang kamu rasakan?"),
                line("Sara", "لَا أَشْعُرُ بِالرَّاحَةِ، وَعِنْدِي أَلَمٌ خَفِيفٌ مُنْذُ أَمْسِ.", "Saya tidak merasa nyaman, dan punya sakit ringan sejak kemarin."),
                line("Fatimah", "مَاذَا فَعَلْتِ أَمْسِ؟", "Apa yang kamu lakukan kemarin?"),
                line("Sara", "ذَهَبْتُ إِلَى الْمَدِينَةِ، ثُمَّ رَجَعْتُ فِي الْمَسَاءِ.", "Saya pergi ke kota, lalu kembali pada sore hari."),
                line("Fatimah", "حَسَنًا. يُوجَدُ مَوْعِدٌ السَّاعَةَ الْحَادِيَةَ عَشْرَةَ.", "Baik. Ada janji jam sebelas."),
                line("Sara", "السَّاعَةُ الْحَادِيَةَ عَشْرَةَ مُنَاسِبَةٌ.", "Jam sebelas cocok."),
            ],
        },
        {
            "lesson_key": "lesson-04-a2-final-test-practice",
            "slug": "arabic-a2-final-test-practice",
            "title": "A2 Final Test Practice",
            "status": "beta",
            "situation": (
                "Kamu latihan simulasi tes A2: menjawab pertanyaan sosial, membuat "
                "rencana, menceritakan pengalaman, dan memberi pendapat pendek."
            ),
            "goal": "Practice short A2 test answers across social, past, plans, and opinions.",
            "grammar": (
                "Gunakan jawaban lengkap tapi pendek: satu informasi utama ditambah "
                "satu alasan atau detail."
            ),
            "patterns": [
                "أَعْتَقِدُ أَنَّ ...",
                "ذَهَبْتُ إِلَى ...",
                "أُفَضِّلُ ... لِأَنَّ ...",
                "نَلْتَقِي السَّاعَةَ ...",
            ],
            "phrases": [
                phrase("أَسْتَطِيعُ أَنْ أَتَحَدَّثَ عَنْ يَوْمِي.", "Saya bisa berbicara tentang hari saya.", "Menyatakan kemampuan A2."),
                phrase("ذَهَبْتُ إِلَى مَكَانٍ جَدِيدٍ.", "Saya pergi ke tempat baru.", "Menceritakan pengalaman."),
                phrase("أُفَضِّلُ الصَّبَاحَ لِأَنَّهُ أَهْدَأُ.", "Saya lebih memilih pagi karena lebih tenang.", "Memberi preferensi dan alasan."),
                phrase("أُرِيدُ أَنْ أُؤَكِّدَ الْمَوْعِدَ.", "Saya ingin mengonfirmasi janji.", "Mengonfirmasi detail."),
                phrase("فِي رَأْيِي، هَذَا خِيَارٌ جَيِّدٌ.", "Menurut saya, ini pilihan yang baik.", "Memberi opini pendek."),
            ],
            "dialogue": [
                line("Hakim", "مَاذَا فَعَلْتَ أَمْسِ يَا رَامِي؟", "Apa yang kamu lakukan kemarin, Rami?"),
                line("Rami", "ذَهَبْتُ إِلَى الْمَكْتَبَةِ، ثُمَّ دَرَسْتُ بَعْضَ الْعَرَبِيَّةِ.", "Saya pergi ke perpustakaan, lalu belajar sedikit bahasa Arab."),
                line("Hakim", "أَيْنَ تُفَضِّلُ أَنْ تَدْرُسَ؟", "Di mana kamu lebih suka belajar?"),
                line("Rami", "أُفَضِّلُ الْمَكْتَبَةَ لِأَنَّهَا هَادِئَةٌ.", "Saya lebih memilih perpustakaan karena tenang."),
                line("Hakim", "كَيْفَ تَطْلُبُ مَوْعِدًا؟", "Bagaimana kamu meminta janji?"),
                line("Rami", "أَقُولُ: أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", "Saya mengatakan: saya ingin janji dengan dokter."),
                line("Hakim", "جَيِّدٌ. مَا رَأْيُكَ فِي الدِّرَاسَةِ كُلَّ يَوْمٍ؟", "Bagus. Apa pendapatmu tentang belajar setiap hari?"),
                line("Rami", "فِي رَأْيِي، هَذَا مُفِيدٌ، وَلَكِنَّهُ يَحْتَاجُ إِلَى وَقْتٍ.", "Menurut saya, itu bermanfaat, tetapi membutuhkan waktu."),
            ],
        },
        {
            "lesson_key": "lesson-05-a2-final-conversation",
            "slug": "arabic-a2-final-conversation",
            "title": "A2 Final Conversation",
            "status": "beta",
            "situation": (
                "Kamu menyelesaikan percakapan A2 lengkap: bertemu teman, membahas "
                "pengalaman, membuat rencana, menangani kebutuhan layanan, dan memberi pendapat."
            ),
            "goal": "Complete a practical A2 conversation using the whole level skill set.",
            "grammar": (
                "Gabungkan pertanyaan lanjutan, rencana, arah, layanan, appointment, "
                "past experience, dan opini dalam satu dialog yang runtut."
            ),
            "patterns": [
                "كَيْفَ كَانَتْ تَجْرِبَتُكَ؟",
                "هَلْ تُرِيدُ أَنْ ...؟",
                "كَيْفَ أَذْهَبُ إِلَى ...؟",
                "أَعْتَقِدُ أَنَّ ...",
            ],
            "phrases": [
                phrase("كَيْفَ كَانَتْ تَجْرِبَتُكَ؟", "Bagaimana pengalamanmu?", "Membuka cerita pengalaman."),
                phrase("هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي؟", "Apakah kamu ingin pergi bersama saya?", "Mengajak."),
                phrase("كَيْفَ أَذْهَبُ إِلَى الْمَرْكَزِ؟", "Bagaimana saya pergi ke pusat?", "Menanyakan arah."),
                phrase("أُرِيدُ أَنْ أُؤَكِّدَ الْمَوْعِدَ.", "Saya ingin mengonfirmasi janji.", "Mengonfirmasi jadwal."),
                phrase("أَعْتَقِدُ أَنَّ الْخُطَّةَ جَيِّدَةٌ.", "Saya pikir rencananya baik.", "Memberi opini akhir."),
            ],
            "dialogue": [
                line("Maryam", "كَيْفَ كَانَتْ تَجْرِبَتُكَ فِي الْمَدِينَةِ يَا خَالِدُ؟", "Bagaimana pengalamanmu di kota, Khalid?"),
                line("Khalid", "كَانَتْ جَيِّدَةً. رَأَيْتُ مَكَانًا جَدِيدًا وَاشْتَرَيْتُ كِتَابًا.", "Pengalamannya baik. Saya melihat tempat baru dan membeli buku."),
                line("Maryam", "هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي إِلَى الْمَرْكَزِ غَدًا؟", "Apakah kamu ingin pergi bersama saya ke pusat besok?"),
                line("Khalid", "نَعَمْ، وَلَكِنْ كَيْفَ أَذْهَبُ إِلَى الْمَرْكَزِ؟", "Ya, tetapi bagaimana saya pergi ke pusat?"),
                line("Maryam", "اِمْشِ مُسْتَقِيمًا، ثُمَّ اِتَّجِهْ يَسَارًا عِنْدَ الْمَكْتَبَةِ.", "Berjalan lurus, lalu belok kiri di perpustakaan."),
                line("Khalid", "جَيِّدٌ. أُرِيدُ أَيْضًا أَنْ أُؤَكِّدَ مَوْعِدِي فِي الْعِيَادَةِ.", "Bagus. Saya juga ingin mengonfirmasi janji saya di klinik."),
                line("Maryam", "اِتَّصِلْ بِالِاسْتِقْبَالِ وَقُلْ: أُرِيدُ أَنْ أُؤَكِّدَ الْمَوْعِدَ.", "Hubungi penerimaan dan katakan: saya ingin mengonfirmasi janji."),
                line("Khalid", "شُكْرًا. مَا رَأْيُكِ فِي خُطَّتِنَا؟", "Terima kasih. Apa pendapatmu tentang rencana kita?"),
                line("Maryam", "أَعْتَقِدُ أَنَّ الْخُطَّةَ جَيِّدَةٌ لِأَنَّهَا وَاضِحَةٌ.", "Saya pikir rencananya baik karena jelas."),
                line("Khalid", "أُوَافِقُكِ. نَلْتَقِي غَدًا السَّاعَةَ الْعَاشِرَةَ.", "Saya setuju denganmu. Kita bertemu besok jam sepuluh."),
            ],
        },
    ],
}


def main() -> None:
    generator.UNIT = UNIT
    generator.main()


if __name__ == "__main__":
    main()
