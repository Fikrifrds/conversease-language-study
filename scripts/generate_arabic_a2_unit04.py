#!/usr/bin/env python3
"""Generate Arabic A2 Unit 4 content."""
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
    "unit_key": "unit-04-shopping-services",
    "title": "Shopping & Services",
    "status": "beta",
    "main_conversation_outcome": (
        "Ask for items, compare simple options, request service help, and confirm "
        "details."
    ),
    "lessons": [
        {
            "lesson_key": "lesson-01-asking-for-an-item",
            "slug": "arabic-asking-for-an-item",
            "title": "Asking for an Item",
            "status": "beta",
            "situation": (
                "Kamu berada di toko alat tulis dan ingin meminta barang tertentu, "
                "menanyakan pilihan warna, lalu memutuskan membeli satu barang."
            ),
            "goal": "Ask for an item and choose one option clearly.",
            "grammar": (
                "Gunakan أَبْحَثُ عَنْ untuk mencari barang, هَلْ عِنْدَكُمْ untuk "
                "menanyakan stok, dan سَآخُذُ untuk keputusan membeli."
            ),
            "patterns": [
                "أَبْحَثُ عَنْ ...",
                "هَلْ عِنْدَكُمْ هَذَا؟",
                "هَلْ يُوجَدُ لَوْنٌ آخَرُ؟",
                "سَآخُذُ هَذَا.",
            ],
            "phrases": [
                phrase("أَبْحَثُ عَنْ قَلَمٍ أَزْرَقَ.", "Saya mencari pulpen biru.", "Menyebut barang yang dicari."),
                phrase("هَلْ عِنْدَكُمْ هَذَا؟", "Apakah kalian punya ini?", "Menanyakan stok barang."),
                phrase("هَلْ يُوجَدُ لَوْنٌ آخَرُ؟", "Apakah ada warna lain?", "Menanyakan pilihan warna."),
                phrase("أُرِيدُ وَاحِدًا، مِنْ فَضْلِكَ.", "Saya ingin satu, tolong.", "Meminta jumlah barang."),
                phrase("سَآخُذُ هَذَا.", "Saya akan mengambil ini.", "Memutuskan membeli."),
            ],
            "dialogue": [
                line("Noura", "مَرْحَبًا، أَبْحَثُ عَنْ قَلَمٍ أَزْرَقَ.", "Halo, saya mencari pulpen biru."),
                line("Karim", "نَعَمْ، عِنْدَنَا هَذَا الْقَلَمُ.", "Ya, kami punya pulpen ini."),
                line("Noura", "هَلْ يُوجَدُ لَوْنٌ آخَرُ؟", "Apakah ada warna lain?"),
                line("Karim", "عِنْدَنَا أَزْرَقُ وَأَسْوَدُ وَأَحْمَرُ.", "Kami punya biru, hitam, dan merah."),
                line("Noura", "سَآخُذُ الْأَزْرَقَ، مِنْ فَضْلِكَ.", "Saya akan mengambil yang biru, tolong."),
                line("Karim", "تَفَضَّلِي.", "Silakan."),
            ],
        },
        {
            "lesson_key": "lesson-02-asking-about-size-and-color",
            "slug": "arabic-asking-about-size-and-color",
            "title": "Asking About Size and Color",
            "status": "beta",
            "situation": (
                "Kamu membeli pakaian sederhana dan perlu menanyakan ukuran, warna, "
                "serta izin mencoba barang."
            ),
            "goal": "Ask about size and color, then confirm what fits.",
            "grammar": (
                "Gunakan مَقَاسٌ untuk ukuran, لَوْنٌ untuk warna, dan هَلْ أَسْتَطِيعُ "
                "أَنْ ... untuk permintaan sopan."
            ),
            "patterns": [
                "هَلْ عِنْدَكُمْ مَقَاسٌ أَكْبَرُ؟",
                "أُرِيدُ اللَّوْنَ الْأَبْيَضَ.",
                "هَذَا صَغِيرٌ جِدًّا.",
                "هَلْ أَسْتَطِيعُ أَنْ أُجَرِّبَهُ؟",
            ],
            "phrases": [
                phrase("هَلْ عِنْدَكُمْ مَقَاسٌ أَكْبَرُ؟", "Apakah kalian punya ukuran yang lebih besar?", "Menanyakan ukuran lain."),
                phrase("أُرِيدُ اللَّوْنَ الْأَبْيَضَ.", "Saya ingin warna putih.", "Memilih warna."),
                phrase("هَذَا صَغِيرٌ جِدًّا.", "Ini terlalu kecil.", "Menjelaskan ukuran tidak cocok."),
                phrase("هَذَا مُنَاسِبٌ.", "Ini cocok.", "Mengonfirmasi ukuran cocok."),
                phrase("هَلْ أَسْتَطِيعُ أَنْ أُجَرِّبَهُ؟", "Bolehkah saya mencobanya?", "Meminta izin mencoba."),
            ],
            "dialogue": [
                line("Sami", "أُرِيدُ قَمِيصًا أَبْيَضَ، مِنْ فَضْلِكِ.", "Saya ingin kemeja putih, tolong."),
                line("Huda", "هَذَا قَمِيصٌ أَبْيَضُ. هَلِ الْمَقَاسُ مُنَاسِبٌ؟", "Ini kemeja putih. Apakah ukurannya cocok?"),
                line("Sami", "هَذَا صَغِيرٌ جِدًّا. هَلْ عِنْدَكُمْ مَقَاسٌ أَكْبَرُ؟", "Ini terlalu kecil. Apakah kalian punya ukuran yang lebih besar?"),
                line("Huda", "نَعَمْ، هَذَا مَقَاسٌ أَكْبَرُ.", "Ya, ini ukuran yang lebih besar."),
                line("Sami", "هَلْ أَسْتَطِيعُ أَنْ أُجَرِّبَهُ؟", "Bolehkah saya mencobanya?"),
                line("Huda", "نَعَمْ، غُرْفَةُ التَّجْرِبَةِ هُنَاكَ.", "Ya, ruang cobanya di sana."),
                line("Sami", "جَيِّدٌ، هَذَا مُنَاسِبٌ.", "Bagus, ini cocok."),
            ],
        },
        {
            "lesson_key": "lesson-03-comparing-simple-options",
            "slug": "arabic-comparing-simple-options",
            "title": "Comparing Simple Options",
            "status": "beta",
            "situation": (
                "Kamu membandingkan dua barang sederhana berdasarkan harga, kualitas, "
                "dan kecocokan sebelum memilih."
            ),
            "goal": "Compare two simple options and choose one with a short reason.",
            "grammar": (
                "Gunakan bentuk perbandingan sederhana seperti أَرْخَصُ, أَجْوَدُ, "
                "أَفْضَلُ, dan أُفَضِّلُ."
            ),
            "patterns": [
                "هَذَا أَرْخَصُ.",
                "هَذَا أَجْوَدُ.",
                "أَيُّهُمَا أَفْضَلُ؟",
                "أُفَضِّلُ هَذَا.",
            ],
            "phrases": [
                phrase("هَذَا أَرْخَصُ.", "Ini lebih murah.", "Membandingkan harga."),
                phrase("هَذَا أَجْوَدُ.", "Ini lebih bagus kualitasnya.", "Membandingkan kualitas."),
                phrase("أَيُّهُمَا أَفْضَلُ؟", "Mana yang lebih baik?", "Meminta saran perbandingan."),
                phrase("أُفَضِّلُ هَذَا.", "Saya lebih memilih ini.", "Menyatakan pilihan."),
                phrase("السِّعْرُ مُنَاسِبٌ.", "Harganya cocok.", "Memberi alasan harga."),
            ],
            "dialogue": [
                line("Layla", "أُرِيدُ حَقِيبَةً صَغِيرَةً. أَيُّهُمَا أَفْضَلُ؟", "Saya ingin tas kecil. Mana yang lebih baik?"),
                line("Rami", "هَذِهِ الْحَقِيبَةُ أَرْخَصُ.", "Tas ini lebih murah."),
                line("Layla", "وَهَذِهِ؟", "Dan yang ini?"),
                line("Rami", "هَذِهِ أَجْوَدُ، وَلَكِنَّهَا أَغْلَى قَلِيلًا.", "Yang ini lebih bagus kualitasnya, tetapi sedikit lebih mahal."),
                line("Layla", "أُفَضِّلُ هَذِهِ. السِّعْرُ مُنَاسِبٌ وَاللَّوْنُ جَمِيلٌ.", "Saya lebih memilih yang ini. Harganya cocok dan warnanya bagus."),
                line("Rami", "اِخْتِيَارٌ جَيِّدٌ.", "Pilihan yang bagus."),
            ],
        },
        {
            "lesson_key": "lesson-04-requesting-service-help",
            "slug": "arabic-requesting-service-help",
            "title": "Requesting Service Help",
            "status": "beta",
            "situation": (
                "Kamu datang ke bagian layanan karena sebuah perangkat tidak bekerja "
                "dan kamu perlu menjelaskan masalahnya dengan sopan."
            ),
            "goal": "Request service help and explain a simple problem.",
            "grammar": (
                "Gunakan هَلْ يُمْكِنُ أَنْ ... untuk meminta bantuan, لَا يَعْمَلُ "
                "untuk masalah, dan سَأَفْحَصُهُ untuk respons layanan."
            ),
            "patterns": [
                "هَلْ يُمْكِنُ أَنْ تُسَاعِدَنِي؟",
                "الْجِهَازُ لَا يَعْمَلُ.",
                "أَحْتَاجُ إِلَى إِصْلَاحٍ.",
                "سَأَفْحَصُهُ الآنَ.",
            ],
            "phrases": [
                phrase("هَلْ يُمْكِنُ أَنْ تُسَاعِدَنِي؟", "Bisakah Anda membantu saya?", "Meminta bantuan layanan."),
                phrase("الْجِهَازُ لَا يَعْمَلُ.", "Perangkatnya tidak bekerja.", "Menjelaskan masalah."),
                phrase("أَحْتَاجُ إِلَى إِصْلَاحٍ.", "Saya membutuhkan perbaikan.", "Menyatakan kebutuhan servis."),
                phrase("هَلْ عِنْدَكَ ضَمَانٌ؟", "Apakah kamu punya garansi?", "Menanyakan garansi."),
                phrase("سَأَفْحَصُهُ الآنَ.", "Saya akan memeriksanya sekarang.", "Respons dari petugas layanan."),
            ],
            "dialogue": [
                line("Dimas", "عَفْوًا، هَلْ يُمْكِنُ أَنْ تُسَاعِدَنِي؟", "Permisi, bisakah Anda membantu saya?"),
                line("Karim", "نَعَمْ، مَا الْمُشْكِلَةُ؟", "Ya, apa masalahnya?"),
                line("Dimas", "الْجِهَازُ لَا يَعْمَلُ مُنْذُ الصَّبَاحِ.", "Perangkatnya tidak bekerja sejak pagi."),
                line("Karim", "هَلْ عِنْدَكَ ضَمَانٌ؟", "Apakah kamu punya garansi?"),
                line("Dimas", "نَعَمْ، هَذَا الضَّمَانُ.", "Ya, ini garansinya."),
                line("Karim", "سَأَفْحَصُهُ الآنَ. اِنْتَظِرْ قَلِيلًا، مِنْ فَضْلِكَ.", "Saya akan memeriksanya sekarang. Tunggu sebentar, tolong."),
                line("Dimas", "حَسَنًا، شُكْرًا.", "Baik, terima kasih."),
            ],
        },
        {
            "lesson_key": "lesson-05-shopping-service-mission",
            "slug": "arabic-shopping-service-mission",
            "title": "Shopping Service Mission",
            "status": "beta",
            "situation": (
                "Kamu memilih barang di toko, membandingkan pilihan, lalu berpindah "
                "ke bagian layanan untuk meminta bantuan perangkat."
            ),
            "goal": "Combine item request, comparison, and service help in one practical visit.",
            "grammar": (
                "Gabungkan أَبْحَثُ عَنْ untuk mencari barang, أَيُّهُمَا أَفْضَلُ "
                "untuk membandingkan, dan هَلْ يُمْكِنُ أَنْ تُسَاعِدَنِي untuk layanan."
            ),
            "patterns": [
                "أَبْحَثُ عَنْ حَقِيبَةٍ.",
                "هَلْ يُوجَدُ لَوْنٌ أَزْرَقُ؟",
                "أَيُّهُمَا أَفْضَلُ؟",
                "الْجِهَازُ لَا يَعْمَلُ.",
            ],
            "phrases": [
                phrase("أَبْحَثُ عَنْ حَقِيبَةٍ صَغِيرَةٍ.", "Saya mencari tas kecil.", "Memulai permintaan barang."),
                phrase("هَلْ يُوجَدُ لَوْنٌ أَزْرَقُ؟", "Apakah ada warna biru?", "Menanyakan pilihan warna."),
                phrase("أَيُّهُمَا أَفْضَلُ؟", "Mana yang lebih baik?", "Membandingkan dua opsi."),
                phrase("سَآخُذُ الْأَزْرَقَ.", "Saya akan mengambil yang biru.", "Memutuskan pilihan."),
                phrase("الْجِهَازُ لَا يَعْمَلُ.", "Perangkatnya tidak bekerja.", "Menjelaskan masalah layanan."),
            ],
            "dialogue": [
                line("Layla", "أَبْحَثُ عَنْ حَقِيبَةٍ صَغِيرَةٍ.", "Saya mencari tas kecil."),
                line("Huda", "عِنْدَنَا هَذِهِ الْحَقِيبَةُ بِاللَّوْنِ الْأَسْوَدِ.", "Kami punya tas ini dengan warna hitam."),
                line("Layla", "هَلْ يُوجَدُ لَوْنٌ أَزْرَقُ؟", "Apakah ada warna biru?"),
                line("Huda", "نَعَمْ، وَهَذَا الْمَقَاسُ أَكْبَرُ قَلِيلًا.", "Ya, dan ukuran ini sedikit lebih besar."),
                line("Layla", "أَيُّهُمَا أَفْضَلُ؟", "Mana yang lebih baik?"),
                line("Huda", "الْأَزْرَقُ أَجْوَدُ، وَلَكِنَّهُ أَغْلَى.", "Yang biru lebih bagus kualitasnya, tetapi lebih mahal."),
                line("Layla", "سَآخُذُ الْأَزْرَقَ. وَأُرِيدُ مُسَاعَدَةً فِي هَذَا الْجِهَازِ.", "Saya akan mengambil yang biru. Dan saya ingin bantuan untuk perangkat ini."),
                line("Huda", "زَمِيلِي كَرِيمٌ فِي قِسْمِ الْخِدْمَةِ.", "Rekan saya Karim ada di bagian layanan."),
                line("Karim", "مَرْحَبًا، مَا الْمُشْكِلَةُ؟", "Halo, apa masalahnya?"),
                line("Layla", "الْجِهَازُ لَا يَعْمَلُ.", "Perangkatnya tidak bekerja."),
                line("Karim", "سَأَفْحَصُهُ الآنَ.", "Saya akan memeriksanya sekarang."),
            ],
        },
    ],
}


def main() -> None:
    generator.UNIT = UNIT
    generator.main()


if __name__ == "__main__":
    main()
