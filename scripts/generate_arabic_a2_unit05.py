#!/usr/bin/env python3
"""Generate Arabic A2 Unit 5 content."""
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
    "unit_key": "unit-05-health-appointments",
    "title": "Health & Appointments",
    "status": "published",
    "main_conversation_outcome": (
        "Describe simple symptoms, make appointments, and confirm basic health "
        "service details."
    ),
    "lessons": [
        {
            "lesson_key": "lesson-01-saying-how-you-feel",
            "slug": "arabic-saying-how-you-feel",
            "title": "Saying How You Feel",
            "status": "published",
            "situation": (
                "Kamu datang ke klinik dan perlu mengatakan kondisi umum dengan "
                "sederhana sebelum petugas mencatat informasi awal."
            ),
            "goal": "Say how you feel and ask to see a doctor.",
            "grammar": (
                "Gunakan أَشْعُرُ بِـ untuk perasaan fisik, عِنْدِي untuk gejala "
                "sederhana, dan هَلْ يُمْكِنُنِي untuk permintaan sopan."
            ),
            "patterns": [
                "أَشْعُرُ بِتَعَبٍ.",
                "عِنْدِي صُدَاعٌ خَفِيفٌ.",
                "لَا أَشْعُرُ بِالرَّاحَةِ.",
                "هَلْ يُمْكِنُنِي أَنْ أَرَى الطَّبِيبَ؟",
            ],
            "phrases": [
                phrase("أَشْعُرُ بِتَعَبٍ.", "Saya merasa lelah.", "Menyebut kondisi umum."),
                phrase("عِنْدِي صُدَاعٌ خَفِيفٌ.", "Saya punya sakit kepala ringan.", "Menyebut gejala sederhana."),
                phrase("لَا أَشْعُرُ بِالرَّاحَةِ.", "Saya tidak merasa nyaman.", "Menjelaskan kondisi umum."),
                phrase("مُنْذُ هَذَا الصَّبَاحِ.", "Sejak pagi ini.", "Menjawab sejak kapan."),
                phrase("هَلْ يُمْكِنُنِي أَنْ أَرَى الطَّبِيبَ؟", "Bisakah saya menemui dokter?", "Meminta layanan dokter."),
            ],
            "dialogue": [
                line("Maryam", "مَرْحَبًا، لَا أَشْعُرُ بِالرَّاحَةِ.", "Halo, saya tidak merasa nyaman."),
                line("Fatimah", "مَا الَّذِي تَشْعُرِينَ بِهِ؟", "Apa yang kamu rasakan?"),
                line("Maryam", "أَشْعُرُ بِتَعَبٍ، وَعِنْدِي صُدَاعٌ خَفِيفٌ.", "Saya merasa lelah, dan saya punya sakit kepala ringan."),
                line("Fatimah", "مُنْذُ مَتَى؟", "Sejak kapan?"),
                line("Maryam", "مُنْذُ هَذَا الصَّبَاحِ.", "Sejak pagi ini."),
                line("Fatimah", "هَلْ عِنْدَكِ مَوْعِدٌ؟", "Apakah kamu punya janji?"),
                line("Maryam", "لَا، هَلْ يُمْكِنُنِي أَنْ أَرَى الطَّبِيبَ؟", "Tidak, bisakah saya menemui dokter?"),
            ],
        },
        {
            "lesson_key": "lesson-02-describing-simple-symptoms",
            "slug": "arabic-describing-simple-symptoms",
            "title": "Describing Simple Symptoms",
            "status": "published",
            "situation": (
                "Kamu berbicara dengan petugas kesehatan dan menjelaskan gejala "
                "ringan secara jelas: bagian tubuh, intensitas, dan durasi."
            ),
            "goal": "Describe simple symptoms with duration and intensity.",
            "grammar": (
                "Gunakan عِنْدِي untuk gejala, فِي untuk bagian tubuh, dan مُنْذُ "
                "untuk durasi."
            ),
            "patterns": [
                "عِنْدِي أَلَمٌ فِي ...",
                "لَدَيَّ سُعَالٌ خَفِيفٌ.",
                "دَرَجَةُ حَرَارَتِي مُرْتَفِعَةٌ قَلِيلًا.",
                "مُنْذُ يَوْمَيْنِ.",
            ],
            "phrases": [
                phrase("عِنْدِي أَلَمٌ فِي الْحَلْقِ.", "Saya punya sakit di tenggorokan.", "Menyebut lokasi gejala."),
                phrase("لَدَيَّ سُعَالٌ خَفِيفٌ.", "Saya punya batuk ringan.", "Menyebut gejala ringan."),
                phrase("دَرَجَةُ حَرَارَتِي مُرْتَفِعَةٌ قَلِيلًا.", "Suhu badan saya sedikit tinggi.", "Menjelaskan kondisi suhu."),
                phrase("مُنْذُ يَوْمَيْنِ.", "Sejak dua hari.", "Menyebut durasi."),
                phrase("الْأَلَمُ لَيْسَ شَدِيدًا.", "Rasanya tidak berat.", "Menjelaskan intensitas."),
            ],
            "dialogue": [
                line("Omar", "عِنْدِي أَلَمٌ فِي الْحَلْقِ.", "Saya punya sakit di tenggorokan."),
                line("Hakim", "مُنْذُ مَتَى؟", "Sejak kapan?"),
                line("Omar", "مُنْذُ يَوْمَيْنِ.", "Sejak dua hari."),
                line("Hakim", "هَلْ عِنْدَكَ سُعَالٌ؟", "Apakah kamu punya batuk?"),
                line("Omar", "نَعَمْ، لَدَيَّ سُعَالٌ خَفِيفٌ.", "Ya, saya punya batuk ringan."),
                line("Hakim", "وَدَرَجَةُ الْحَرَارَةِ؟", "Dan suhu badan?"),
                line("Omar", "دَرَجَةُ حَرَارَتِي مُرْتَفِعَةٌ قَلِيلًا، وَلَكِنَّ الْأَلَمَ لَيْسَ شَدِيدًا.", "Suhu badan saya sedikit tinggi, tetapi sakitnya tidak berat."),
            ],
        },
        {
            "lesson_key": "lesson-03-making-an-appointment",
            "slug": "arabic-making-an-appointment",
            "title": "Making an Appointment",
            "status": "published",
            "situation": (
                "Kamu menelepon klinik untuk membuat janji, memilih hari dan waktu, "
                "serta menyebut nama untuk pendaftaran."
            ),
            "goal": "Make a clinic appointment and choose a suitable time.",
            "grammar": (
                "Gunakan أُرِيدُ مَوْعِدًا untuk membuat janji, هَلْ يُوجَدُ untuk "
                "menanyakan ketersediaan, dan مُنَاسِبٌ untuk waktu yang cocok."
            ),
            "patterns": [
                "أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.",
                "هَلْ يُوجَدُ مَوْعِدٌ غَدًا؟",
                "السَّاعَةُ الْعَاشِرَةُ مُنَاسِبَةٌ.",
                "بِاسْمِ مَنْ؟",
            ],
            "phrases": [
                phrase("أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", "Saya ingin janji dengan dokter.", "Membuka permintaan appointment."),
                phrase("هَلْ يُوجَدُ مَوْعِدٌ غَدًا؟", "Apakah ada janji besok?", "Menanyakan slot besok."),
                phrase("صَبَاحًا أَمْ مَسَاءً؟", "Pagi atau sore?", "Menanyakan pilihan waktu."),
                phrase("السَّاعَةُ الْعَاشِرَةُ مُنَاسِبَةٌ.", "Jam sepuluh cocok.", "Menyetujui waktu."),
                phrase("الْمَوْعِدُ بِاسْمِي.", "Janji atas nama saya.", "Mengonfirmasi nama appointment."),
            ],
            "dialogue": [
                line("Noura", "مَرْحَبًا، أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", "Halo, saya ingin janji dengan dokter."),
                line("Fatimah", "مَرْحَبًا. هَلْ تُرِيدِينَ الْمَوْعِدَ غَدًا؟", "Halo. Apakah kamu ingin janji besok?"),
                line("Noura", "نَعَمْ، هَلْ يُوجَدُ مَوْعِدٌ فِي الصَّبَاحِ؟", "Ya, apakah ada janji pada pagi hari?"),
                line("Fatimah", "يُوجَدُ مَوْعِدٌ السَّاعَةَ الْعَاشِرَةَ.", "Ada janji jam sepuluh."),
                line("Noura", "السَّاعَةُ الْعَاشِرَةُ مُنَاسِبَةٌ.", "Jam sepuluh cocok."),
                line("Fatimah", "بِاسْمِ مَنْ؟", "Atas nama siapa?"),
                line("Noura", "الْمَوْعِدُ بِاسْمِ نُورَةَ.", "Janji atas nama Noura."),
            ],
        },
        {
            "lesson_key": "lesson-04-confirming-appointment-details",
            "slug": "arabic-confirming-appointment-details",
            "title": "Confirming Appointment Details",
            "status": "published",
            "situation": (
                "Kamu ingin memastikan ulang detail janji: nama, tanggal, waktu, "
                "lokasi, dan nomor kontak."
            ),
            "goal": "Confirm appointment details clearly and politely.",
            "grammar": (
                "Gunakan أُرِيدُ أَنْ أُؤَكِّدَ untuk konfirmasi, هَلْ untuk mengecek "
                "detail, dan الصَّحِيحُ untuk memastikan data benar."
            ),
            "patterns": [
                "أُرِيدُ أَنْ أُؤَكِّدَ الْمَوْعِدَ.",
                "هَلِ الْمَوْعِدُ غَدًا؟",
                "هَلْ رَقْمِي صَحِيحٌ؟",
                "نَعَمْ، التَّفَاصِيلُ صَحِيحَةٌ.",
            ],
            "phrases": [
                phrase("أُرِيدُ أَنْ أُؤَكِّدَ الْمَوْعِدَ.", "Saya ingin mengonfirmasi janji.", "Membuka konfirmasi appointment."),
                phrase("هَلِ الْمَوْعِدُ غَدًا؟", "Apakah janjinya besok?", "Mengonfirmasi hari."),
                phrase("فِي أَيِّ طَابِقٍ؟", "Di lantai berapa?", "Menanyakan lokasi detail."),
                phrase("هَلْ رَقْمِي صَحِيحٌ؟", "Apakah nomor saya benar?", "Mengonfirmasi nomor kontak."),
                phrase("التَّفَاصِيلُ صَحِيحَةٌ.", "Detailnya benar.", "Menutup konfirmasi."),
            ],
            "dialogue": [
                line("Rami", "مَرْحَبًا، أُرِيدُ أَنْ أُؤَكِّدَ الْمَوْعِدَ.", "Halo, saya ingin mengonfirmasi janji."),
                line("Fatimah", "بِاسْمِ مَنْ؟", "Atas nama siapa?"),
                line("Rami", "بِاسْمِ رَامِي.", "Atas nama Rami."),
                line("Fatimah", "نَعَمْ، مَوْعِدُكَ غَدًا السَّاعَةَ التَّاسِعَةَ.", "Ya, janjimu besok jam sembilan."),
                line("Rami", "فِي أَيِّ طَابِقٍ؟", "Di lantai berapa?"),
                line("Fatimah", "فِي الطَّابِقِ الثَّانِي، غُرْفَةُ الِاسْتِقْبَالِ.", "Di lantai dua, ruang penerimaan."),
                line("Rami", "شُكْرًا. التَّفَاصِيلُ صَحِيحَةٌ.", "Terima kasih. Detailnya benar."),
            ],
        },
        {
            "lesson_key": "lesson-05-health-appointment-mission",
            "slug": "arabic-health-appointment-mission",
            "title": "Health Appointment Mission",
            "status": "published",
            "situation": (
                "Kamu menjelaskan kondisi ringan, membuat janji, lalu mengonfirmasi "
                "detail appointment dengan petugas klinik."
            ),
            "goal": "Combine symptom description, appointment booking, and detail confirmation.",
            "grammar": (
                "Gabungkan عِنْدِي untuk gejala, أُرِيدُ مَوْعِدًا untuk booking, "
                "dan أُؤَكِّدَ untuk konfirmasi."
            ),
            "patterns": [
                "لَا أَشْعُرُ بِالرَّاحَةِ.",
                "عِنْدِي أَلَمٌ خَفِيفٌ.",
                "أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.",
                "أُرِيدُ أَنْ أُؤَكِّدَ التَّفَاصِيلَ.",
            ],
            "phrases": [
                phrase("لَا أَشْعُرُ بِالرَّاحَةِ.", "Saya tidak merasa nyaman.", "Menyebut kondisi umum."),
                phrase("عِنْدِي أَلَمٌ خَفِيفٌ.", "Saya punya sakit ringan.", "Menyebut gejala umum."),
                phrase("أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", "Saya ingin janji dengan dokter.", "Meminta appointment."),
                phrase("السَّاعَةُ الْحَادِيَةَ عَشْرَةَ مُنَاسِبَةٌ.", "Jam sebelas cocok.", "Menyetujui waktu."),
                phrase("أُرِيدُ أَنْ أُؤَكِّدَ التَّفَاصِيلَ.", "Saya ingin mengonfirmasi detail.", "Memastikan detail akhir."),
            ],
            "dialogue": [
                line("Sara", "مَرْحَبًا، لَا أَشْعُرُ بِالرَّاحَةِ.", "Halo, saya tidak merasa nyaman."),
                line("Fatimah", "مَا الَّذِي تَشْعُرِينَ بِهِ؟", "Apa yang kamu rasakan?"),
                line("Sara", "عِنْدِي أَلَمٌ خَفِيفٌ فِي الْحَلْقِ مُنْذُ أَمْسِ.", "Saya punya sakit ringan di tenggorokan sejak kemarin."),
                line("Fatimah", "هَلْ تُرِيدِينَ مَوْعِدًا مَعَ الطَّبِيبِ؟", "Apakah kamu ingin janji dengan dokter?"),
                line("Sara", "نَعَمْ، هَلْ يُوجَدُ مَوْعِدٌ الْيَوْمَ؟", "Ya, apakah ada janji hari ini?"),
                line("Fatimah", "يُوجَدُ مَوْعِدٌ السَّاعَةَ الْحَادِيَةَ عَشْرَةَ.", "Ada janji jam sebelas."),
                line("Sara", "السَّاعَةُ الْحَادِيَةَ عَشْرَةَ مُنَاسِبَةٌ.", "Jam sebelas cocok."),
                line("Fatimah", "الْمَوْعِدُ بِاسْمِ سَارَةَ فِي الطَّابِقِ الثَّانِي.", "Janji atas nama Sara di lantai dua."),
                line("Sara", "شُكْرًا. أُرِيدُ أَنْ أُؤَكِّدَ التَّفَاصِيلَ: الْيَوْمَ، السَّاعَةَ الْحَادِيَةَ عَشْرَةَ، الطَّابِقَ الثَّانِي.", "Terima kasih. Saya ingin mengonfirmasi detail: hari ini, jam sebelas, lantai dua."),
                line("Fatimah", "نَعَمْ، التَّفَاصِيلُ صَحِيحَةٌ.", "Ya, detailnya benar."),
            ],
        },
    ],
}


def main() -> None:
    generator.UNIT = UNIT
    generator.main()


if __name__ == "__main__":
    main()
