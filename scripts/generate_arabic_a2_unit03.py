#!/usr/bin/env python3
"""Generate Arabic A2 Unit 3 content."""
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
    "unit_key": "unit-03-transport-travel",
    "title": "Transport & Travel",
    "status": "beta",
    "main_conversation_outcome": (
        "Ask about transport, tickets, departure time, directions, and simple "
        "travel help."
    ),
    "lessons": [
        {
            "lesson_key": "lesson-01-buying-a-ticket",
            "slug": "arabic-buying-a-ticket",
            "title": "Buying a Ticket",
            "status": "beta",
            "situation": (
                "Kamu berada di loket stasiun dan ingin membeli tiket sederhana: "
                "tujuan, jenis tiket, kelas, dan harga."
            ),
            "goal": "Buy a simple ticket and confirm basic travel details.",
            "grammar": (
                "Gunakan أُرِيدُ untuk permintaan, إِلَى untuk tujuan, dan pilihan "
                "dengan أَمْ saat membandingkan dua opsi."
            ),
            "patterns": [
                "أُرِيدُ تَذْكِرَةً إِلَى ...",
                "ذَهَابًا فَقَطْ أَمْ ذَهَابًا وَعَوْدَةً؟",
                "الدَّرَجَةُ الِاقْتِصَادِيَّةُ.",
                "كَمِ السِّعْرُ؟",
            ],
            "phrases": [
                phrase("أُرِيدُ تَذْكِرَةً إِلَى جَاكَرْتَا.", "Saya ingin tiket ke Jakarta.", "Meminta tiket dengan tujuan."),
                phrase("ذَهَابًا فَقَطْ.", "Sekali jalan saja.", "Memilih jenis perjalanan."),
                phrase("ذَهَابًا وَعَوْدَةً.", "Pulang pergi.", "Menyebut opsi perjalanan pulang pergi."),
                phrase("الدَّرَجَةُ الِاقْتِصَادِيَّةُ.", "Kelas ekonomi.", "Memilih kelas tiket."),
                phrase("كَمِ السِّعْرُ؟", "Berapa harganya?", "Menanyakan harga."),
            ],
            "dialogue": [
                line("Sami", "أُرِيدُ تَذْكِرَةً إِلَى جَاكَرْتَا، مِنْ فَضْلِكِ.", "Saya ingin tiket ke Jakarta, tolong."),
                line("Huda", "ذَهَابًا فَقَطْ أَمْ ذَهَابًا وَعَوْدَةً؟", "Sekali jalan saja atau pulang pergi?"),
                line("Sami", "ذَهَابًا فَقَطْ.", "Sekali jalan saja."),
                line("Huda", "الدَّرَجَةُ الِاقْتِصَادِيَّةُ أَمِ الدَّرَجَةُ الْأُولَى؟", "Kelas ekonomi atau kelas pertama?"),
                line("Sami", "الدَّرَجَةُ الِاقْتِصَادِيَّةُ، مِنْ فَضْلِكِ.", "Kelas ekonomi, tolong."),
                line("Huda", "السِّعْرُ خَمْسُونَ أَلْفَ رُوبِيَّةٍ.", "Harganya lima puluh ribu rupiah."),
                line("Sami", "تَفَضَّلِي. شُكْرًا.", "Silakan. Terima kasih."),
            ],
        },
        {
            "lesson_key": "lesson-02-asking-about-departure-time",
            "slug": "arabic-asking-about-departure-time",
            "title": "Asking About Departure Time",
            "status": "beta",
            "situation": (
                "Kamu sudah punya tiket dan ingin memastikan jam keberangkatan, "
                "peron, serta waktu tiba."
            ),
            "goal": "Ask and confirm departure time, platform, and arrival time.",
            "grammar": (
                "Gunakan مَتَى untuk waktu, مِنْ أَيِّ untuk asal/peron, dan يَصِلُ "
                "untuk menanyakan waktu tiba."
            ),
            "patterns": [
                "مَتَى يَغَادِرُ الْقِطَارُ؟",
                "يُغَادِرُ السَّاعَةَ ...",
                "مِنْ أَيِّ رَصِيفٍ؟",
                "مَتَى يَصِلُ؟",
            ],
            "phrases": [
                phrase("مَتَى يَغَادِرُ الْقِطَارُ؟", "Kapan keretanya berangkat?", "Menanyakan waktu berangkat."),
                phrase("يُغَادِرُ السَّاعَةَ السَّابِعَةَ.", "Berangkat jam tujuh.", "Menjawab waktu berangkat."),
                phrase("مِنْ أَيِّ رَصِيفٍ؟", "Dari peron berapa?", "Menanyakan peron."),
                phrase("مِنَ الرَّصِيفِ الثَّانِي.", "Dari peron dua.", "Menjawab lokasi peron."),
                phrase("يَصِلُ السَّاعَةَ التَّاسِعَةَ.", "Tiba jam sembilan.", "Mengonfirmasi waktu tiba."),
            ],
            "dialogue": [
                line("Rami", "مَتَى يَغَادِرُ الْقِطَارُ إِلَى بَانْدُونْغ؟", "Kapan kereta ke Bandung berangkat?"),
                line("Alya", "يُغَادِرُ السَّاعَةَ السَّابِعَةَ وَالنِّصْفِ.", "Berangkat jam tujuh tiga puluh."),
                line("Rami", "مِنْ أَيِّ رَصِيفٍ؟", "Dari peron berapa?"),
                line("Alya", "مِنَ الرَّصِيفِ الثَّانِي.", "Dari peron dua."),
                line("Rami", "وَمَتَى يَصِلُ إِلَى بَانْدُونْغ؟", "Dan kapan tiba di Bandung?"),
                line("Alya", "يَصِلُ السَّاعَةَ التَّاسِعَةَ وَعَشْرَ دَقَائِقَ.", "Tiba jam sembilan lewat sepuluh menit."),
                line("Rami", "جَيِّدٌ، شُكْرًا عَلَى الْمُسَاعَدَةِ.", "Bagus, terima kasih atas bantuannya."),
            ],
        },
        {
            "lesson_key": "lesson-03-checking-directions",
            "slug": "arabic-checking-directions",
            "title": "Checking Directions",
            "status": "beta",
            "situation": (
                "Kamu berada di terminal dan ingin memastikan arah menuju pintu, "
                "peron, atau tempat tunggu tanpa salah jalur."
            ),
            "goal": "Ask for directions and check that you understood them correctly.",
            "grammar": (
                "Gunakan كَيْفَ أَذْهَبُ إِلَى ... untuk arah, ثُمَّ untuk urutan, "
                "dan هَلْ هَذَا صَحِيحٌ؟ untuk konfirmasi."
            ),
            "patterns": [
                "كَيْفَ أَذْهَبُ إِلَى ...؟",
                "اِمْشِ مُسْتَقِيمًا.",
                "ثُمَّ اِتَّجِهْ يَمِينًا.",
                "هَلْ هَذَا صَحِيحٌ؟",
            ],
            "phrases": [
                phrase("كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", "Bagaimana saya pergi ke peron?", "Menanyakan arah ke peron."),
                phrase("اِمْشِ مُسْتَقِيمًا.", "Berjalan lurus.", "Memberi arah pertama."),
                phrase("ثُمَّ اِتَّجِهْ يَمِينًا.", "Lalu belok kanan.", "Memberi arah berikutnya."),
                phrase("بِجَانِبِ الْمَصْعَدِ.", "Di samping lift.", "Menjelaskan lokasi."),
                phrase("هَلْ هَذَا صَحِيحٌ؟", "Apakah ini benar?", "Memastikan pemahaman."),
            ],
            "dialogue": [
                line("Noura", "عَفْوًا، كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ الثَّالِثِ؟", "Permisi, bagaimana saya pergi ke peron tiga?"),
                line("Karim", "اِمْشِي مُسْتَقِيمًا إِلَى نِهَايَةِ الْمَمَرِّ.", "Berjalanlah lurus sampai ujung lorong."),
                line("Noura", "ثُمَّ؟", "Lalu?"),
                line("Karim", "ثُمَّ اِتَّجِهِي يَمِينًا. الرَّصِيفُ بِجَانِبِ الْمَصْعَدِ.", "Lalu belok kanan. Peronnya di samping lift."),
                line("Noura", "أَمْشِي مُسْتَقِيمًا، ثُمَّ أَتَّجِهُ يَمِينًا. هَلْ هَذَا صَحِيحٌ؟", "Saya berjalan lurus, lalu belok kanan. Apakah ini benar?"),
                line("Karim", "نَعَمْ، هَذَا صَحِيحٌ.", "Ya, itu benar."),
            ],
        },
        {
            "lesson_key": "lesson-04-talking-to-a-driver",
            "slug": "arabic-talking-to-a-driver",
            "title": "Talking to a Driver",
            "status": "beta",
            "situation": (
                "Kamu naik taksi atau kendaraan online dan perlu memastikan tujuan, "
                "waktu perjalanan, dan tempat turun."
            ),
            "goal": "Talk to a driver clearly and confirm destination and drop-off point.",
            "grammar": (
                "Gunakan إِلَى untuk tujuan, كَمْ يَسْتَغْرِقُ untuk durasi, dan "
                "تَوَقَّفْ untuk meminta berhenti."
            ),
            "patterns": [
                "إِلَى الْفُنْدُقِ، مِنْ فَضْلِكَ.",
                "هَلْ هَذَا الْعُنْوَانُ صَحِيحٌ؟",
                "كَمْ يَسْتَغْرِقُ الطَّرِيقُ؟",
                "تَوَقَّفْ هُنَا، مِنْ فَضْلِكَ.",
            ],
            "phrases": [
                phrase("إِلَى الْفُنْدُقِ، مِنْ فَضْلِكَ.", "Ke hotel, tolong.", "Memberi tujuan kepada sopir."),
                phrase("هَلْ هَذَا الْعُنْوَانُ صَحِيحٌ؟", "Apakah alamat ini benar?", "Memastikan alamat."),
                phrase("كَمْ يَسْتَغْرِقُ الطَّرِيقُ؟", "Berapa lama perjalanannya?", "Menanyakan durasi."),
                phrase("حَوَالَيْ عِشْرِينَ دَقِيقَةً.", "Sekitar dua puluh menit.", "Menjawab durasi perjalanan."),
                phrase("تَوَقَّفْ هُنَا، مِنْ فَضْلِكَ.", "Berhenti di sini, tolong.", "Meminta berhenti."),
            ],
            "dialogue": [
                line("Layla", "إِلَى فُنْدُقِ النُّورِ، مِنْ فَضْلِكَ.", "Ke Hotel An-Nur, tolong."),
                line("Karim", "حَسَنًا. هَلْ هَذَا الْعُنْوَانُ صَحِيحٌ؟", "Baik. Apakah alamat ini benar?"),
                line("Layla", "نَعَمْ، الْعُنْوَانُ صَحِيحٌ.", "Ya, alamatnya benar."),
                line("Karim", "الطَّرِيقُ مُزْدَحِمٌ قَلِيلًا الْيَوْمَ.", "Jalan agak macet hari ini."),
                line("Layla", "كَمْ يَسْتَغْرِقُ الطَّرِيقُ؟", "Berapa lama perjalanannya?"),
                line("Karim", "حَوَالَيْ عِشْرِينَ دَقِيقَةً.", "Sekitar dua puluh menit."),
                line("Layla", "حَسَنًا. تَوَقَّفْ عِنْدَ الْبَابِ، مِنْ فَضْلِكَ.", "Baik. Berhenti di pintu, tolong."),
            ],
        },
        {
            "lesson_key": "lesson-05-transport-travel-mission",
            "slug": "arabic-transport-travel-mission",
            "title": "Transport and Travel Mission",
            "status": "beta",
            "situation": (
                "Kamu menyelesaikan perjalanan pendek: membeli tiket, mengecek jam "
                "berangkat, mencari peron, lalu memastikan tujuan dengan sopir."
            ),
            "goal": "Combine ticket buying, time checking, directions, and driver conversation.",
            "grammar": (
                "Gabungkan permintaan dengan أُرِيدُ, waktu dengan مَتَى, arah dengan "
                "كَيْفَ, dan durasi dengan كَمْ يَسْتَغْرِقُ."
            ),
            "patterns": [
                "أُرِيدُ تَذْكِرَةً إِلَى ...",
                "مَتَى يَغَادِرُ؟",
                "كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟",
                "كَمْ يَسْتَغْرِقُ الطَّرِيقُ؟",
            ],
            "phrases": [
                phrase("أُرِيدُ تَذْكِرَةً إِلَى الْمَدِينَةِ.", "Saya ingin tiket ke kota.", "Meminta tiket."),
                phrase("مَتَى يَغَادِرُ الْقِطَارُ؟", "Kapan keretanya berangkat?", "Menanyakan jam berangkat."),
                phrase("كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", "Bagaimana saya pergi ke peron?", "Menanyakan arah."),
                phrase("هَلْ هَذَا الْعُنْوَانُ صَحِيحٌ؟", "Apakah alamat ini benar?", "Memastikan alamat."),
                phrase("تَوَقَّفْ هُنَا، مِنْ فَضْلِكَ.", "Berhenti di sini, tolong.", "Menutup perjalanan."),
            ],
            "dialogue": [
                line("Dimas", "أُرِيدُ تَذْكِرَةً إِلَى الْمَدِينَةِ، مِنْ فَضْلِكِ.", "Saya ingin tiket ke kota, tolong."),
                line("Huda", "ذَهَابًا فَقَطْ؟", "Sekali jalan saja?"),
                line("Dimas", "نَعَمْ. مَتَى يَغَادِرُ الْقِطَارُ؟", "Ya. Kapan keretanya berangkat?"),
                line("Huda", "يُغَادِرُ السَّاعَةَ الثَّامِنَةَ مِنَ الرَّصِيفِ الْأَوَّلِ.", "Berangkat jam delapan dari peron satu."),
                line("Dimas", "شُكْرًا. كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", "Terima kasih. Bagaimana saya pergi ke peron?"),
                line("Huda", "اِمْشِ مُسْتَقِيمًا، ثُمَّ اِتَّجِهْ يَسَارًا.", "Berjalan lurus, lalu belok kiri."),
                line("Dimas", "بَعْدَ الْوُصُولِ، سَأَذْهَبُ إِلَى الْفُنْدُقِ.", "Setelah tiba, saya akan pergi ke hotel."),
                line("Karim", "هَلْ هَذَا الْعُنْوَانُ صَحِيحٌ؟", "Apakah alamat ini benar?"),
                line("Dimas", "نَعَمْ. تَوَقَّفْ عِنْدَ الْبَابِ، مِنْ فَضْلِكَ.", "Ya. Berhenti di pintu, tolong."),
            ],
        },
    ],
}


def main() -> None:
    generator.UNIT = UNIT
    generator.main()


if __name__ == "__main__":
    main()
