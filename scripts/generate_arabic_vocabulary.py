#!/usr/bin/env python3
"""Generate concise Arabic vocabulary files from authored lesson content.

The lesson dialogue and useful phrases remain the source of truth. This script
adds a small curated vocabulary layer so every Arabic lesson teaches a few new
words without turning the page into a dictionary.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
ARABIC_ROOT = REPO_ROOT / "content" / "curriculum" / "arabic"

ARABIC_DIACRITICS_RE = re.compile(r"[\u064B-\u065F\u0670]")
ARABIC_TOKEN_RE = re.compile(r"[\u0621-\u064A\u0671-\u06D3\u064B-\u065F\u0670]+")
AUDIO_TAG_RE = re.compile(r"\((?:[a-z][a-z-]*)\)|<#\d+(?:\.\d+)?#>")

STOP_WORDS = {
    "أَنَا",
    "أَنْتَ",
    "أَنْتِ",
    "أَنْ",
    "إِلَى",
    "فِي",
    "مِنْ",
    "عَلَى",
    "عَنْ",
    "مَعَ",
    "هَذَا",
    "هَذِهِ",
    "هَلْ",
    "لَا",
    "نَعَمْ",
    "وَ",
    "يَا",
    "ثُمَّ",
    "أَمْ",
    "لِأَنَّ",
    "لِأَنَّنِي",
    "مِنْ فَضْلِكَ",
    "مِنْ فَضْلِكِ",
}

VOCABULARY: dict[str, tuple[str, str]] = {
    "السلام": ("السَّلَامُ", "salam"),
    "وعليكم": ("وَعَلَيْكُمُ", "dan atas kalian"),
    "مرحبا": ("مَرْحَبًا", "halo"),
    "اهلا": ("أَهْلًا", "selamat datang"),
    "صباح": ("صَبَاحٌ", "pagi"),
    "مساء": ("مَسَاءٌ", "sore/malam"),
    "خير": ("خَيْرٌ", "baik"),
    "حال": ("حَالٌ", "keadaan/kabar"),
    "شكرا": ("شُكْرًا", "terima kasih"),
    "اسف": ("آسِفٌ", "maaf"),
    "اسفة": ("آسِفَةٌ", "maaf"),
    "عذرا": ("عُذْرًا", "permisi/maaf"),
    "مشكلة": ("مُشْكِلَةٌ", "masalah"),
    "اسم": ("اِسْمٌ", "nama"),
    "اسمي": ("اِسْمِي", "nama saya"),
    "حرف": ("حَرْفٌ", "huruf"),
    "رقم": ("رَقْمٌ", "nomor"),
    "رقمي": ("رَقْمِي", "nomor saya"),
    "هاتف": ("هَاتِفٌ", "telepon"),
    "بريد": ("بَرِيدٌ", "surat/email"),
    "الالكتروني": ("الْإِلِكْتُرُونِيُّ", "elektronik"),
    "نقطة": ("نُقْطَةٌ", "titik"),
    "باء": ("بَاءٌ", "huruf ba"),
    "صحيح": ("صَحِيحٌ", "benar"),
    "واضح": ("وَاضِحٌ", "jelas"),
    "ببطء": ("بِبُطْءٍ", "pelan-pelan"),
    "مرة": ("مَرَّةٌ", "sekali/kali"),
    "اخرى": ("أُخْرَى", "lagi/lain"),
    "افهم": ("أَفْهَمُ", "saya paham"),
    "اعرف": ("أَعْرِفُ", "saya tahu"),
    "يعني": ("يَعْنِي", "artinya"),
    "اسمع": ("أَسْمَعُ", "saya mendengar"),
    "قلت": ("قُلْتَ", "kamu mengatakan"),
    "احتاج": ("أَحْتَاجُ", "saya butuh"),
    "مساعدة": ("مُسَاعَدَةٌ", "bantuan"),
    "اريد": ("أُرِيدُ", "saya ingin"),
    "افتح": ("اِفْتَحْ", "bukalah"),
    "اكتب": ("اُكْتُبْ", "tulislah"),
    "اكتبي": ("اُكْتُبِي", "tulislah"),
    "استمع": ("اِسْتَمِعْ", "dengarkan"),
    "تكلم": ("تَكَلَّمْ", "berbicaralah"),
    "تكلمي": ("تَكَلَّمِي", "berbicaralah"),
    "جملة": ("جُمْلَةٌ", "kalimat"),
    "مثال": ("مِثَالٌ", "contoh"),
    "اليوم": ("الْيَوْمُ", "hari ini"),
    "غدا": ("غَدًا", "besok"),
    "امس": ("أَمْسِ", "kemarin"),
    "يوم": ("يَوْمٌ", "hari"),
    "عندي": ("عِنْدِي", "saya punya"),
    "ابي": ("أَبِي", "ayah saya"),
    "امي": ("أُمِّي", "ibu saya"),
    "اخي": ("أَخِي", "saudara laki-laki saya"),
    "عائلة": ("عَائِلَةٌ", "keluarga"),
    "عائلتي": ("عَائِلَتِي", "keluarga saya"),
    "ساعة": ("سَاعَةٌ", "jam"),
    "الثامنة": ("الثَّامِنَةُ", "jam delapan/kedelapan"),
    "التاسعة": ("التَّاسِعَةُ", "jam sembilan/kesembilan"),
    "العاشرة": ("الْعَاشِرَةُ", "jam sepuluh/kesepuluh"),
    "الصباح": ("الصَّبَاحُ", "pagi"),
    "الظهر": ("الظُّهْرُ", "siang"),
    "العصر": ("الْعَصْرُ", "sore"),
    "الاثنين": ("الْإِثْنَيْنِ", "Senin"),
    "الثلاثاء": ("الثُّلَاثَاءُ", "Selasa"),
    "الاربعاء": ("الْأَرْبِعَاءُ", "Rabu"),
    "الدرس": ("الدَّرْسُ", "pelajaran"),
    "الكلمات": ("الْكَلِمَاتُ", "kata-kata"),
    "الكلمة": ("الْكَلِمَةُ", "kata"),
    "الصفحة": ("الصَّفْحَةُ", "halaman"),
    "الكتاب": ("الْكِتَابُ", "buku"),
    "العربية": ("الْعَرَبِيَّةُ", "bahasa Arab"),
    "اندونيسيا": ("إِنْدُونِيسِيَا", "Indonesia"),
    "مدرسة": ("مَدْرَسَةٌ", "sekolah"),
    "مركز": ("مَرْكَزٌ", "pusat"),
    "فصل": ("فَصْلٌ", "kelas/ruang kelas"),
    "مكتبة": ("مَكْتَبَةٌ", "perpustakaan"),
    "مكتب": ("مَكْتَبٌ", "kantor/meja kerja"),
    "مقهى": ("مَقْهًى", "kafe"),
    "سوق": ("سُوقٌ", "pasar"),
    "بيت": ("بَيْتٌ", "rumah"),
    "باب": ("بَابٌ", "pintu"),
    "مصعد": ("مِصْعَدٌ", "lift"),
    "رصيف": ("رَصِيفٌ", "peron"),
    "فندق": ("فُنْدُقٌ", "hotel"),
    "عنوان": ("عُنْوَانٌ", "alamat"),
    "مدينة": ("مَدِينَةٌ", "kota"),
    "جاكرتا": ("جَاكَرْتَا", "Jakarta"),
    "باندونغ": ("بَانْدُونْغ", "Bandung"),
    "اين": ("أَيْنَ", "di mana"),
    "كيف": ("كَيْفَ", "bagaimana"),
    "ماذا": ("مَاذَا", "apa"),
    "لماذا": ("لِمَاذَا", "mengapa"),
    "متى": ("مَتَى", "kapan"),
    "كم": ("كَمْ", "berapa"),
    "قريب": ("قَرِيبٌ", "dekat"),
    "قريبة": ("قَرِيبَةٌ", "dekat"),
    "بعيد": ("بَعِيدٌ", "jauh"),
    "بعيدة": ("بَعِيدَةٌ", "jauh"),
    "امام": ("أَمَامَ", "di depan"),
    "بجانب": ("بِجَانِبِ", "di samping"),
    "يمين": ("يَمِينًا", "kanan"),
    "يسار": ("يَسَارًا", "kiri"),
    "مستقيما": ("مُسْتَقِيمًا", "lurus"),
    "طريق": ("طَرِيقٌ", "jalan"),
    "ماء": ("مَاءٌ", "air"),
    "قهوة": ("قَهْوَةٌ", "kopi"),
    "حساب": ("حِسَابٌ", "tagihan"),
    "سعر": ("سِعْرٌ", "harga"),
    "ريال": ("رِيَالٌ", "riyal"),
    "ريالات": ("رِيَالَاتٌ", "riyal"),
    "روبية": ("رُوبِيَّةٌ", "rupiah"),
    "قلم": ("قَلَمٌ", "pena"),
    "كتابا": ("كِتَابٌ", "buku"),
    "واحد": ("وَاحِدٌ", "satu"),
    "واحدة": ("وَاحِدَةٌ", "satu"),
    "اثنان": ("اِثْنَانِ", "dua"),
    "ثلاثة": ("ثَلَاثَةٌ", "tiga"),
    "اربعة": ("أَرْبَعَةٌ", "empat"),
    "خمسة": ("خَمْسَةٌ", "lima"),
    "خمسون": ("خَمْسُونَ", "lima puluh"),
    "الف": ("أَلْفٌ", "seribu"),
    "تذكرة": ("تَذْكِرَةٌ", "tiket"),
    "قطار": ("قِطَارٌ", "kereta"),
    "يغادر": ("يُغَادِرُ", "berangkat"),
    "يصل": ("يَصِلُ", "tiba"),
    "ذهابا": ("ذَهَابًا", "pergi/sekali jalan"),
    "عودة": ("عَوْدَةٌ", "pulang/kembali"),
    "درجة": ("دَرَجَةٌ", "kelas/tingkat"),
    "اقتصادية": ("اِقْتِصَادِيَّةٌ", "ekonomi"),
    "اولى": ("أُولَى", "pertama"),
    "لون": ("لَوْنٌ", "warna"),
    "ازرق": ("أَزْرَقُ", "biru"),
    "ابيض": ("أَبْيَضُ", "putih"),
    "اسود": ("أَسْوَدُ", "hitam"),
    "احمر": ("أَحْمَرُ", "merah"),
    "مقاس": ("مَقَاسٌ", "ukuran"),
    "اكبر": ("أَكْبَرُ", "lebih besar"),
    "اصغر": ("أَصْغَرُ", "lebih kecil"),
    "صغير": ("صَغِيرٌ", "kecil"),
    "صغيرة": ("صَغِيرَةٌ", "kecil"),
    "ارخص": ("أَرْخَصُ", "lebih murah"),
    "اجود": ("أَجْوَدُ", "lebih berkualitas"),
    "افضل": ("أَفْضَلُ", "lebih baik"),
    "غالي": ("غَالٍ", "mahal"),
    "مناسب": ("مُنَاسِبٌ", "cocok/sesuai"),
    "مناسبة": ("مُنَاسِبَةٌ", "cocok/sesuai"),
    "حقيبة": ("حَقِيبَةٌ", "tas"),
    "جهاز": ("جِهَازٌ", "alat/perangkat"),
    "يعمل": ("يَعْمَلُ", "berfungsi/bekerja"),
    "اصلاح": ("إِصْلَاحٌ", "perbaikan"),
    "ضمان": ("ضَمَانٌ", "garansi"),
    "طبيب": ("طَبِيبٌ", "dokter"),
    "موعد": ("مَوْعِدٌ", "janji temu"),
    "عيادة": ("عِيَادَةٌ", "klinik"),
    "تعب": ("تَعَبٌ", "lelah"),
    "صداع": ("صُدَاعٌ", "sakit kepala"),
    "الم": ("أَلَمٌ", "sakit/nyeri"),
    "حلق": ("حَلْقٌ", "tenggorokan"),
    "سعال": ("سُعَالٌ", "batuk"),
    "حرارة": ("حَرَارَةٌ", "suhu/demam"),
    "راحة": ("رَاحَةٌ", "nyaman/istirahat"),
    "خفيف": ("خَفِيفٌ", "ringan"),
    "خفيفة": ("خَفِيفَةٌ", "ringan"),
    "منذ": ("مُنْذُ", "sejak"),
    "طابق": ("طَابِقٌ", "lantai"),
    "غرفة": ("غُرْفَةٌ", "ruangan/kamar"),
    "ذهبت": ("ذَهَبْتُ", "saya pergi"),
    "رجعت": ("رَجَعْتُ", "saya kembali"),
    "اشتريت": ("اِشْتَرَيْتُ", "saya membeli"),
    "رايت": ("رَأَيْتُ", "saya melihat"),
    "فعلت": ("فَعَلْتُ", "saya melakukan"),
    "حديقة": ("حَدِيقَةٌ", "taman"),
    "مكان": ("مَكَانٌ", "tempat"),
    "جميل": ("جَمِيلٌ", "indah/bagus"),
    "جميلة": ("جَمِيلَةٌ", "indah/bagus"),
    "هادئ": ("هَادِئٌ", "tenang"),
    "هادئة": ("هَادِئَةٌ", "tenang"),
    "نظيف": ("نَظِيفٌ", "bersih"),
    "تجربة": ("تَجْرِبَةٌ", "pengalaman"),
    "طعام": ("طَعَامٌ", "makanan"),
    "مزدحم": ("مُزْدَحِمٌ", "ramai/padat"),
    "راي": ("رَأْيٌ", "pendapat"),
    "اعتقد": ("أَعْتَقِدُ", "saya pikir"),
    "افضل": ("أُفَضِّلُ", "saya lebih memilih"),
    "اوافق": ("أُوَافِقُ", "saya setuju"),
    "خطة": ("خُطَّةٌ", "rencana"),
    "خيار": ("خِيَارٌ", "pilihan"),
    "سبب": ("سَبَبٌ", "alasan"),
    "بسيط": ("بَسِيطٌ", "sederhana"),
    "مفيد": ("مُفِيدٌ", "bermanfaat"),
    "قصة": ("قِصَّةٌ", "cerita"),
    "السياق": ("السِّيَاقُ", "konteks"),
    "سياق": ("سِيَاقٌ", "konteks"),
    "حدث": ("حَدَثٌ", "kejadian"),
    "اساسي": ("أَسَاسِيٌّ", "utama"),
    "خلاصة": ("خُلَاصَةٌ", "ringkasan"),
    "بداية": ("بِدَايَةٌ", "awal"),
    "نهاية": ("نِهَايَةٌ", "akhir"),
    "اولا": ("أَوَّلًا", "pertama"),
    "اخيرا": ("أَخِيرًا", "akhirnya"),
    "وصلت": ("وَصَلْتُ", "saya tiba"),
    "انتظرت": ("اِنْتَظَرْتُ", "saya menunggu"),
    "اتفقنا": ("اِتَّفَقْنَا", "kami sepakat"),
    "شعرت": ("شَعَرْتُ", "saya merasa"),
    "قلق": ("قَلَقٌ", "khawatir"),
    "راحة": ("رَاحَةٌ", "nyaman/lega"),
    "نتيجة": ("نَتِيجَةٌ", "hasil"),
    "تغيير": ("تَغْيِيرٌ", "perubahan"),
    "لحظة": ("لَحْظَةٌ", "momen"),
    "مهمة": ("مَهَمَّةٌ", "tugas"),
    "تفاصيل": ("تَفَاصِيلُ", "detail"),
    "تنظيم": ("تَنْظِيمٌ", "pengaturan"),
    "تحسين": ("تَحْسِينٌ", "perbaikan"),
    "مراجعة": ("مُرَاجَعَةٌ", "review/tinjauan"),
    "ملخص": ("مُلَخَّصٌ", "ringkasan"),
    "تعليمات": ("تَعْلِيمَاتٌ", "instruksi"),
    "توضيح": ("تَوْضِيحٌ", "klarifikasi/penjelasan"),
    "تقصد": ("تَقْصِدُ", "maksudmu"),
    "المقصود": ("الْمَقْصُودُ", "maksud"),
    "انجزت": ("أَنْجَزْتُ", "saya menyelesaikan"),
    "جزء": ("جُزْءٌ", "bagian"),
    "تحديث": ("تَحْدِيثٌ", "update"),
    "وضع": ("وَضْعٌ", "kondisi/status"),
    "حالي": ("حَالِيٌّ", "saat ini"),
    "اضيف": ("أُضِيفُ", "saya menambahkan"),
    "اقترح": ("أَقْتَرِحُ", "saya menyarankan"),
    "خطا": ("خَطَأٌ", "kesalahan"),
    "مؤقت": ("مُؤَقَّتٌ", "sementara"),
    "نصيحة": ("نَصِيحَةٌ", "nasihat"),
    "توجيه": ("تَوْجِيهٌ", "arahan"),
    "قرار": ("قَرَارٌ", "keputusan"),
    "حجز": ("حَجْزٌ", "reservasi"),
    "جاهزة": ("جَاهِزَةٌ", "siap"),
    "بطاقة": ("بِطَاقَةٌ", "kartu"),
    "دخول": ("دُخُولٌ", "masuk"),
    "تاخير": ("تَأْخِيرٌ", "keterlambatan"),
    "ازدحام": ("اِزْدِحَامٌ", "kemacetan/keramaian"),
    "توصي": ("تُوصِي", "merekomendasikan"),
    "مطعم": ("مَطْعَمٌ", "restoran"),
    "شكوى": ("شَكْوَى", "keluhan"),
    "هدف": ("هَدَفٌ", "tujuan"),
    "ثقة": ("ثِقَةٌ", "percaya diri"),
    "تقدم": ("تَقَدُّمٌ", "kemajuan"),
    "تحسن": ("تَحَسُّنٌ", "perbaikan"),
    "تحد": ("تَحَدٍّ", "tantangan"),
    "تردد": ("تَرَدُّدٌ", "keraguan"),
    "طلاقة": ("طَلَاقَةٌ", "kelancaran"),
    "اسجل": ("أُسَجِّلُ", "saya merekam"),
    "اقيم": ("أُقَيِّمُ", "saya menilai"),
    "اقارن": ("أُقَارِنُ", "saya membandingkan"),
    "مقارنة": ("مُقَارَنَةٌ", "perbandingan"),
    "مختلف": ("مُخْتَلِفٌ", "berbeda"),
    "جودة": ("جَوْدَةٌ", "kualitas"),
    "ايجابيات": ("إِيجَابِيَّاتٌ", "kelebihan"),
    "سلبيات": ("سَلْبِيَّاتٌ", "kekurangan"),
    "مزايا": ("مَزَايَا", "kelebihan"),
    "متوازن": ("مُتَوَازِنٌ", "seimbang"),
    "مجتمع": ("مُجْتَمَعٌ", "komunitas"),
    "الناس": ("النَّاسُ", "orang-orang"),
    "يتعاونون": ("يَتَعَاوَنُونَ", "mereka saling membantu"),
    "عادة": ("عَادَةٌ", "kebiasaan"),
    "عادات": ("عَادَاتٌ", "kebiasaan-kebiasaan"),
    "حي": ("حَيٌّ", "lingkungan"),
    "انتماء": ("اِنْتِمَاءٌ", "rasa memiliki"),
    "ثقافي": ("ثَقَافِيٌّ", "budaya"),
    "رسمي": ("رَسْمِيٌّ", "resmi"),
    "احترام": ("اِحْتِرَامٌ", "penghormatan"),
    "اختلاف": ("اِخْتِلَافٌ", "perbedaan"),
    "تواصل": ("تَوَاصُلٌ", "komunikasi"),
    "احب": ("أُحِبُّ", "saya suka"),
    "استطيع": ("أَسْتَطِيعُ", "saya bisa"),
    "قليلا": ("قَلِيلًا", "sedikit"),
    "ادرس": ("أَدْرُسُ", "saya belajar"),
    "اعمل": ("أَعْمَلُ", "saya bekerja"),
    "اتعلم": ("أَتَعَلَّمُ", "saya belajar"),
    "اخذ": ("آخُذُ", "saya ambil"),
    "موجود": ("مَوْجُودٌ", "tersedia/ada"),
    "واجب": ("وَاجِبٌ", "tugas"),
    "سهل": ("سَهْلٌ", "mudah"),
    "صعب": ("صَعْبٌ", "sulit"),
    "تدريب": ("تَدْرِيبٌ", "latihan"),
    "قراءة": ("قِرَاءَةٌ", "membaca"),
    "كتابة": ("كِتَابَةٌ", "menulis"),
    "اتدرب": ("أَتَدَرَّبُ", "saya berlatih"),
    "اراجع": ("أُرَاجِعُ", "saya mengulang/review"),
    "التقي": ("أَلْتَقِي", "saya bertemu"),
    "اختبار": ("اِخْتِبَارٌ", "ujian"),
    "وقت": ("وَقْتٌ", "waktu"),
    "اخر": ("آخَرُ", "lain"),
    "موقف": ("مَوْقِفٌ", "posisi/sikap"),
    "حجة": ("حُجَّةٌ", "argumen"),
    "دليل": ("دَلِيلٌ", "bukti/petunjuk"),
    "اعتراض": ("اِعْتِرَاضٌ", "keberatan"),
    "فائدة": ("فَائِدَةٌ", "manfaat"),
    "مسار": ("مَسَارٌ", "jalur/arah"),
    "اجتماع": ("اِجْتِمَاعٌ", "rapat/pertemuan"),
    "نطاق": ("نِطَاقٌ", "cakupan"),
    "ملاحظة": ("مُلَاحَظَةٌ", "catatan/masukan"),
    "بناءة": ("بَنَّاءَةٌ", "konstruktif"),
    "اولوية": ("أَوْلَوِيَّةٌ", "prioritas"),
    "اولويات": ("أَوْلَوِيَّاتٌ", "prioritas-prioritas"),
    "اقتراح": ("اِقْتِرَاحٌ", "usulan"),
    "حل": ("حَلٌّ", "solusi"),
    "وسط": ("وَسَطٌ", "tengah"),
    "عرض": ("عَرْضٌ", "presentasi/tawaran"),
    "مقدمة": ("مُقَدِّمَةٌ", "pembuka/pengantar"),
    "مخاطر": ("مَخَاطِرُ", "risiko"),
    "اسئلة": ("أَسْئِلَةٌ", "pertanyaan-pertanyaan"),
    "مصدر": ("مَصْدَرٌ", "sumber"),
    "مصادر": ("مَصَادِرُ", "sumber-sumber"),
    "موثوق": ("مَوْثُوقٌ", "tepercaya"),
    "معلومات": ("مَعْلُومَاتٌ", "informasi"),
    "وجهة": ("وِجْهَةٌ", "arah/sudut pandang"),
    "نظر": ("نَظَرٌ", "pandangan"),
    "عميل": ("عَمِيلٌ", "klien/pelanggan"),
    "احتياج": ("اِحْتِيَاجٌ", "kebutuhan"),
    "اهتمام": ("اِهْتِمَامٌ", "perhatian/kepedulian"),
    "خطوة": ("خُطْوَةٌ", "langkah"),
    "اطار": ("إِطَارٌ", "kerangka"),
    "سببان": ("سَبَبَانِ", "dua alasan"),
    "تاثير": ("تَأْثِيرٌ", "dampak/pengaruh"),
    "توصية": ("تَوْصِيَةٌ", "rekomendasi"),
    "نقاش": ("نِقَاشٌ", "diskusi"),
    "مهني": ("مِهَنِيٌّ", "profesional"),
    "مشروع": ("مَشْرُوعٌ", "proyek"),
    "جمهور": ("جُمْهُورٌ", "audiens"),
    "دقة": ("دِقَّةٌ", "ketepatan"),
    "مرونة": ("مُرُونَةٌ", "fleksibilitas"),
    "يقين": ("يَقِينٌ", "kepastian"),
    "شك": ("شَكٌّ", "keraguan"),
    "احتمال": ("اِحْتِمَالٌ", "kemungkinan"),
    "منظور": ("مَنْظُورٌ", "perspektif"),
    "توازن": ("تَوَازُنٌ", "keseimbangan"),
    "مخالفة": ("مُخَالَفَةٌ", "ketidaksetujuan/perbedaan"),
    "استراتيجية": ("اِسْتِرَاتِيجِيَّةٌ", "strategi"),
    "اطراف": ("أَطْرَافٌ", "pihak-pihak"),
    "توقعات": ("تَوَقُّعَاتٌ", "ekspektasi"),
    "حساس": ("حَسَّاسٌ", "sensitif"),
    "حساسة": ("حَسَّاسَةٌ", "sensitif"),
    "اقناع": ("إِقْنَاعٌ", "persuasi"),
    "افتراض": ("اِفْتِرَاضٌ", "asumsi"),
    "ادلة": ("أَدِلَّةٌ", "bukti-bukti"),
    "ضغط": ("ضَغْطٌ", "tekanan"),
    "لباقة": ("لَبَاقَةٌ", "takt/kesantunan"),
    "معيار": ("مِعْيَارٌ", "norma/standar"),
    "سوء": ("سُوءٌ", "keburukan/salah"),
    "فهم": ("فَهْمٌ", "pemahaman"),
    "قيادة": ("قِيَادَةٌ", "kepemimpinan"),
    "تدريب": ("تَدْرِيبٌ", "coaching/latihan"),
    "اتجاه": ("اِتِّجَاهٌ", "arah"),
    "قابل": ("قَابِلٌ", "dapat/mampu"),
    "تطبيق": ("تَطْبِيقٌ", "penerapan"),
    "ضمني": ("ضِمْنِيٌّ", "tersirat"),
    "طويل": ("طَوِيلٌ", "panjang"),
    "متابعة": ("مُتَابَعَةٌ", "follow-up/lanjutan"),
}


def normalize_arabic(value: str) -> str:
    value = ARABIC_DIACRITICS_RE.sub("", value)
    value = value.replace("ـ", "")
    value = value.replace("ٱ", "ا")
    value = value.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    value = value.replace("ى", "ي")
    return value.strip(" .،؟!:؛\"'()[]{}")


def token_lookup(token: str) -> tuple[str, str] | None:
    normalized = normalize_arabic(token)
    if not normalized:
        return None
    if normalized in {normalize_arabic(word) for word in STOP_WORDS}:
        return None

    candidates = [normalized]
    if normalized.startswith("ال") and len(normalized) > 2:
        candidates.append(normalized[2:])
    if normalized.startswith("و") and len(normalized) > 1:
        candidates.append(normalized[1:])
    if normalized.startswith("بال") and len(normalized) > 3:
        candidates.append(normalized[3:])
    if normalized.startswith("لل") and len(normalized) > 2:
        candidates.append(normalized[2:])

    for candidate in candidates:
        if candidate in VOCABULARY:
            return VOCABULARY[candidate]
    return None


def clean_example(text: str) -> str:
    cleaned = AUDIO_TAG_RE.sub("", text)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned


def shorten_example(text: str, max_chars: int = 96) -> str:
    if len(text) <= max_chars:
        return text

    shortened = text[:max_chars].rstrip(" ،,.;؛")
    return f"{shortened}..."


def ordered_token_sources(
    phrases: list[dict[str, Any]],
    dialogue: list[Any] | None = None,
) -> list[tuple[str, str]]:
    text_chunks: list[str] = []
    for entry in phrases:
        text_chunks.append(str(entry.get("phrase") or ""))
    for turn in dialogue or []:
        if isinstance(turn, (tuple, list)) and len(turn) >= 2:
            text_chunks.append(str(turn[1]))
        elif isinstance(turn, dict):
            text_chunks.append(str(turn.get("text") or ""))
    return [
        (match.group(0), clean_example(text))
        for text in text_chunks
        for match in ARABIC_TOKEN_RE.finditer(text)
    ]


def usage_note_for(word: str, meaning: str, source: str) -> str:
    note = f"Dipakai untuk arti \"{meaning}\"."
    if source:
        return f"{note} Contoh: \"{shorten_example(source)}\""
    return note


def vocabulary_for_lesson(
    phrases: list[dict[str, Any]],
    dialogue: list[Any] | None = None,
    *,
    max_items: int = 8,
) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    seen: set[str] = set()

    for token, source in ordered_token_sources(phrases, dialogue):
        match = token_lookup(token)
        if not match:
            continue
        word, meaning = match
        key = normalize_arabic(word)
        if key in seen:
            continue
        seen.add(key)
        entries.append(
            {
                "word": word,
                "meaning_id": meaning,
                "usage_note": usage_note_for(word, meaning, source),
            }
        )
        if len(entries) >= max_items:
            break

    return entries


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return data


def parse_listening_script(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    turns: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("**") or ":**" not in stripped:
            continue
        speaker, text = stripped[2:].split(":**", 1)
        turns.append((speaker.strip(), text.strip()))
    return turns


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def lesson_dirs_for(levels: list[str]) -> list[Path]:
    dirs: list[Path] = []
    for level in levels:
        units_root = ARABIC_ROOT / level / "units"
        if units_root.exists():
            dirs.extend(sorted(units_root.glob("*/lesson-*")))
    return [path for path in dirs if path.is_dir()]


def generate(levels: list[str]) -> int:
    count = 0
    for lesson_dir in lesson_dirs_for(levels):
        phrases_yaml = read_yaml(lesson_dir / "useful_phrases.yaml")
        phrases = phrases_yaml.get("phrases", [])
        dialogue = parse_listening_script(lesson_dir / "listening_script.md")
        vocabulary = vocabulary_for_lesson(phrases, dialogue)
        write_yaml(lesson_dir / "vocabulary.yaml", {"vocabulary": vocabulary})
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--levels",
        nargs="+",
        default=["A1", "A2", "B1", "B2", "C1"],
        help="Arabic levels to process, for example: --levels A1 A2",
    )
    args = parser.parse_args()

    count = generate(args.levels)
    print(f"Generated vocabulary.yaml for {count} Arabic lessons.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
