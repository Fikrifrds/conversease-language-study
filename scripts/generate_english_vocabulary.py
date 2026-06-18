#!/usr/bin/env python3
"""Generate concise English vocabulary files from authored lesson content.

The useful phrases and dialogue remain the source of truth. This script adds a
small word-focused vocabulary layer for every English lesson so learners get
practical words and chunks without duplicating the whole useful phrase section.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
ENGLISH_ROOT = REPO_ROOT / "content" / "curriculum" / "english"

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "don't",
    "for",
    "from",
    "get",
    "have",
    "how",
    "i",
    "i'm",
    "in",
    "is",
    "it",
    "it's",
    "let",
    "let's",
    "me",
    "my",
    "not",
    "of",
    "on",
    "or",
    "our",
    "please",
    "see",
    "some",
    "that",
    "that's",
    "there's",
    "they",
    "the",
    "there",
    "this",
    "to",
    "we",
    "we're",
    "was",
    "wasn't",
    "what",
    "when",
    "where",
    "which",
    "with",
    "would",
    "you",
    "you're",
    "your",
    "yes",
}

# Ordered from basic to advanced. Earlier matches win when lessons have many
# possible terms.
CURATED_TERMS: list[tuple[str, str, str]] = [
    ("good morning", "selamat pagi", "Sapaan yang dipakai sebelum siang."),
    ("nice", "ramah/menyenangkan", "Dipakai untuk menyatakan kesan positif."),
    ("later", "nanti", "Dipakai saat menutup percakapan santai."),
    ("meet", "bertemu", "Kata kerja untuk bertemu seseorang."),
    ("name", "nama", "Dipakai saat memperkenalkan diri."),
    ("spell", "mengeja", "Dipakai saat menyebut huruf satu per satu."),
    ("repeat", "mengulang", "Dipakai saat meminta lawan bicara mengatakan lagi."),
    ("phone number", "nomor telepon", "Dipakai saat bertukar kontak."),
    ("email address", "alamat email", "Dipakai saat memberikan kontak email."),
    ("contact details", "detail kontak", "Informasi seperti nomor telepon dan email."),
    ("from", "dari", "Dipakai untuk asal kota atau negara."),
    ("say", "mengatakan/menyebutkan", "Dipakai saat menyampaikan kata atau informasi."),
    ("tell", "memberi tahu/menceritakan", "Dipakai saat menyampaikan informasi kepada orang lain."),
    ("routine", "rutinitas", "Kebiasaan yang dilakukan secara teratur."),
    ("schedule", "jadwal", "Rencana waktu kegiatan."),
    ("class", "kelas", "Dipakai saat membicarakan pelajaran atau sesi belajar."),
    ("monday", "Senin", "Nama hari; gunakan on sebelum nama hari."),
    ("wednesday", "Rabu", "Nama hari; gunakan on sebelum nama hari."),
    ("evening", "malam/sore", "Bagian hari setelah afternoon."),
    ("appointment", "janji temu", "Waktu yang disepakati untuk bertemu atau layanan."),
    ("work", "bekerja/pekerjaan", "Dipakai saat membicarakan pekerjaan."),
    ("study", "belajar/kuliah", "Dipakai saat membicarakan kegiatan belajar."),
    ("like", "suka", "Dipakai untuk menyatakan hal yang disukai."),
    ("ability", "kemampuan", "Dipakai saat mengatakan apa yang bisa dilakukan."),
    ("place", "tempat", "Lokasi yang ingin dituju atau dijelaskan."),
    ("direction", "arah", "Petunjuk jalan atau posisi."),
    ("going", "pergi/menuju", "Dipakai saat menanyakan atau menyatakan tujuan."),
    ("went", "pergi", "Bentuk lampau dari go."),
    ("cafe", "kafe", "Tempat untuk membeli minuman atau makanan ringan."),
    ("near", "dekat", "Dipakai untuk menjelaskan jarak yang dekat."),
    ("straight", "lurus", "Dipakai dalam instruksi arah."),
    ("together", "bersama", "Dipakai saat mengajak orang melakukan sesuatu bersama."),
    ("price", "harga", "Dipakai saat bertanya atau menyebut biaya."),
    ("order", "memesan", "Dipakai saat membeli makanan atau minuman."),
    ("want", "mau/ingin", "Dipakai untuk menyatakan keinginan."),
    ("sandwich", "sandwich/roti lapis", "Contoh makanan yang bisa dipesan."),
    ("tea", "teh", "Minuman yang umum dipesan."),
    ("sugar", "gula", "Tambahan untuk minuman atau makanan."),
    ("small", "kecil", "Ukuran yang tidak besar."),
    ("pen", "pulpen", "Alat untuk menulis."),
    ("problem", "masalah", "Hal yang perlu dijelaskan atau diselesaikan."),
    ("help", "bantuan", "Dipakai saat meminta bantuan."),
    ("request", "permintaan", "Cara meminta sesuatu dengan sopan."),
    ("apologize", "meminta maaf", "Dipakai saat mengakui kesalahan kecil."),
    ("thank", "berterima kasih", "Dipakai saat mengucapkan terima kasih."),
    ("today", "hari ini", "Dipakai untuk membicarakan waktu sekarang."),
    ("tomorrow", "besok", "Dipakai untuk rencana hari berikutnya."),
    ("now", "sekarang", "Dipakai untuk menyatakan waktu saat ini."),
    ("small talk", "basa-basi ringan", "Percakapan ringan untuk membuka interaksi."),
    ("follow-up question", "pertanyaan lanjutan", "Pertanyaan untuk menjaga percakapan tetap berjalan."),
    ("weekend", "akhir pekan", "Sabtu dan Minggu atau waktu libur mingguan."),
    ("react", "merespons", "Memberi tanggapan singkat pada cerita orang lain."),
    ("plan", "rencana", "Hal yang akan dilakukan."),
    ("invite", "mengundang", "Mengajak seseorang melakukan sesuatu."),
    ("accept", "menerima", "Menyetujui ajakan atau tawaran."),
    ("decline", "menolak dengan sopan", "Menolak ajakan tanpa terdengar kasar."),
    ("reschedule", "menjadwalkan ulang", "Mengubah waktu rencana atau janji."),
    ("departure", "keberangkatan", "Waktu atau proses berangkat."),
    ("excuse me", "permisi", "Pembuka sopan untuk meminta perhatian."),
    ("train", "kereta", "Transportasi rel."),
    ("leave", "berangkat/meninggalkan", "Dipakai untuk jadwal keberangkatan."),
    ("platform", "peron/platform", "Tempat menunggu kereta."),
    ("trip", "perjalanan", "Perjalanan dari satu tempat ke tempat lain."),
    ("driver", "pengemudi", "Orang yang mengendarai kendaraan."),
    ("item", "barang", "Benda yang ingin dibeli atau diminta."),
    ("size", "ukuran", "Ukuran pakaian atau barang."),
    ("color", "warna", "Warna barang."),
    ("compare", "membandingkan", "Melihat perbedaan dua pilihan."),
    ("cheaper", "lebih murah", "Bentuk perbandingan dari cheap."),
    ("quality", "kualitas", "Tingkat mutu suatu barang atau layanan."),
    ("take", "mengambil/memilih", "Dipakai saat memilih barang yang akan dibeli."),
    ("symptom", "gejala", "Tanda kondisi kesehatan."),
    ("headache", "sakit kepala", "Gejala sakit pada kepala."),
    ("fever", "demam", "Kondisi suhu tubuh naik saat sakit."),
    ("tired", "lelah", "Kondisi ketika energi sedang rendah."),
    ("wrong", "salah/ada masalah", "Dipakai untuk menanyakan apa yang terjadi."),
    ("confirm", "mengonfirmasi", "Memastikan detail sudah benar."),
    ("yesterday", "kemarin", "Hari sebelum hari ini."),
    ("experience", "pengalaman", "Hal yang pernah dialami."),
    ("opinion", "pendapat", "Apa yang kamu pikirkan tentang sesuatu."),
    ("think", "berpikir/berpendapat", "Dipakai saat menyatakan pendapat."),
    ("reason", "alasan", "Penjelasan mengapa sesuatu dipilih atau terjadi."),
    ("agree", "setuju", "Menerima pendapat orang lain."),
    ("disagree", "tidak setuju", "Berbeda pendapat dengan sopan."),
    ("setting the scene", "memberi konteks awal", "Membuka cerita dengan waktu, tempat, atau situasi."),
    ("event", "peristiwa", "Hal yang terjadi dalam cerita."),
    ("feeling", "perasaan", "Emosi atau kondisi batin."),
    ("task", "tugas", "Pekerjaan yang perlu dilakukan."),
    ("clarification", "klarifikasi", "Penjelasan tambahan agar sesuatu lebih jelas."),
    ("update", "kabar terbaru", "Informasi terbaru tentang progres."),
    ("meeting", "rapat", "Percakapan kerja dengan beberapa orang."),
    ("solution", "solusi", "Cara menyelesaikan masalah."),
    ("advice", "saran", "Masukan tentang apa yang sebaiknya dilakukan."),
    ("decision", "keputusan", "Pilihan akhir setelah mempertimbangkan opsi."),
    ("option", "opsi/pilihan", "Salah satu pilihan yang tersedia."),
    ("rather", "lebih memilih", "Dipakai untuk menyatakan preferensi."),
    ("rollback", "mengembalikan perubahan", "Istilah kerja untuk kembali ke kondisi sebelumnya."),
    ("reasonable", "masuk akal", "Dipakai saat menyetujui ide yang terdengar baik."),
    ("review", "meninjau ulang", "Memeriksa sesuatu dengan lebih teliti."),
    ("check in", "check-in", "Proses masuk hotel atau melapor kedatangan."),
    ("delay", "keterlambatan", "Saat sesuatu terjadi lebih lambat dari jadwal."),
    ("recommendation", "rekomendasi", "Saran pilihan yang dianggap baik."),
    ("complaint", "keluhan", "Pernyataan tentang masalah layanan atau produk."),
    ("goal", "tujuan", "Hal yang ingin dicapai."),
    ("progress", "kemajuan", "Perkembangan menuju tujuan."),
    ("challenge", "tantangan", "Hal yang membuat sesuatu sulit."),
    ("preference", "preferensi", "Pilihan yang lebih disukai."),
    ("prefer", "lebih memilih", "Dipakai untuk menyatakan pilihan yang disukai."),
    ("pros and cons", "kelebihan dan kekurangan", "Sisi baik dan buruk dari pilihan."),
    ("agreement", "kesepakatan", "Hasil yang disetujui bersama."),
    ("community", "komunitas", "Kelompok orang dalam lingkungan tertentu."),
    ("culture", "budaya", "Kebiasaan dan nilai dalam masyarakat."),
    ("position", "posisi/pendapat", "Sikap utama dalam diskusi."),
    ("argument", "argumen", "Alasan yang mendukung posisi."),
    ("counterpoint", "sanggahan", "Poin yang menantang argumen."),
    ("example", "contoh", "Detail yang membuat argumen lebih jelas."),
    ("share", "membagikan/menyampaikan", "Dipakai saat menyampaikan ide atau informasi."),
    ("idea", "ide", "Gagasan yang ingin disampaikan."),
    ("improve", "meningkatkan/memperbaiki", "Membuat sesuatu menjadi lebih baik."),
    ("try", "mencoba", "Melakukan sesuatu untuk melihat hasilnya."),
    ("tried", "mencoba", "Bentuk lampau dari try."),
    ("happen", "terjadi", "Dipakai saat menjelaskan peristiwa."),
    ("happened", "terjadi", "Bentuk lampau dari happen."),
    ("notice", "menyadari/memperhatikan", "Melihat sesuatu yang penting."),
    ("noticed", "menyadari/memperhatikan", "Bentuk lampau dari notice."),
    ("look", "terlihat/melihat", "Dipakai untuk kesan atau pengamatan."),
    ("looking", "terlihat/sedang melihat", "Bentuk -ing dari look."),
    ("seem", "terlihat/terkesan", "Dipakai untuk kesan yang belum pasti."),
    ("seems", "terlihat/terkesan", "Bentuk present untuk he/she/it."),
    ("onboarding", "proses orientasi", "Proses membantu orang baru mulai bekerja atau belajar."),
    ("scope", "ruang lingkup", "Batas topik atau pekerjaan."),
    ("feedback", "masukan", "Tanggapan untuk memperbaiki sesuatu."),
    ("summary", "ringkasan", "Versi singkat dari informasi utama."),
    ("article", "artikel", "Tulisan informatif di media atau publikasi."),
    ("overall", "secara keseluruhan", "Dipakai saat memberi ringkasan umum."),
    ("context", "konteks", "Latar atau situasi yang membantu memahami topik."),
    ("priority", "prioritas", "Hal yang paling penting didahulukan."),
    ("proposal", "usulan", "Ide atau rencana yang diajukan."),
    ("objection", "keberatan", "Alasan menolak atau belum setuju."),
    ("compromise", "kompromi", "Solusi tengah yang bisa diterima bersama."),
    ("presentation", "presentasi", "Penyampaian ide di depan audiens."),
    ("signpost", "penanda alur", "Frasa yang membantu audiens mengikuti struktur."),
    ("modular", "modular/terpisah per bagian", "Struktur yang dibagi menjadi komponen mandiri."),
    ("purpose", "tujuan", "Alasan utama sesuatu dilakukan."),
    ("benefit", "manfaat", "Dampak positif dari pilihan."),
    ("advantage", "keunggulan", "Sisi positif dari sebuah pilihan."),
    ("risk", "risiko", "Kemungkinan dampak negatif."),
    ("reliable source", "sumber tepercaya", "Sumber informasi yang bisa dipercaya."),
    ("viewpoint", "sudut pandang", "Cara seseorang melihat sebuah topik."),
    ("client", "klien", "Pihak yang menerima layanan profesional."),
    ("concern", "kekhawatiran", "Hal yang membuat seseorang ragu."),
    ("next steps", "langkah berikutnya", "Aksi yang dilakukan setelah diskusi."),
    ("cause", "penyebab", "Alasan sesuatu terjadi."),
    ("tradeoff", "kompromi pilihan", "Hal yang dikorbankan saat memilih opsi."),
    ("trade-off", "kompromi pilihan", "Hal yang dikorbankan saat memilih opsi."),
    ("nuance", "nuansa", "Perbedaan makna yang halus."),
    ("certainty", "kepastian", "Tingkat keyakinan terhadap sesuatu."),
    ("doubt", "keraguan", "Perasaan belum yakin."),
    ("stakeholder", "pemangku kepentingan", "Orang atau pihak yang terdampak keputusan."),
    ("expectation", "ekspektasi", "Harapan tentang hasil atau proses."),
    ("impact", "dampak", "Pengaruh atau akibat dari suatu tindakan."),
    ("appreciate", "menghargai", "Dipakai untuk menunjukkan penghargaan dengan sopan."),
    ("sensitive feedback", "masukan sensitif", "Feedback yang perlu disampaikan dengan hati-hati."),
    ("frame", "membingkai", "Menjelaskan konteks agar pembahasan jelas."),
    ("persuasive flow", "alur persuasif", "Urutan ide yang membuat argumen meyakinkan."),
    ("transition", "transisi", "Jembatan antar ide."),
    ("reliability", "keandalan", "Tingkat bisa dipercaya atau stabilnya sesuatu."),
    ("crucial", "sangat penting", "Dipakai untuk menekankan poin utama."),
    ("standard", "standar", "Ukuran atau aturan mutu yang disepakati."),
    ("differently", "dengan cara berbeda", "Dipakai saat menjelaskan ulang dengan kata lain."),
    ("connect", "menghubungkan", "Menyambungkan satu ide ke ide lain."),
    ("assumption", "asumsi", "Anggapan awal yang belum tentu benar."),
    ("evidence", "bukti", "Data atau contoh yang mendukung argumen."),
    ("under pressure", "di bawah tekanan", "Saat harus merespons dalam situasi sulit."),
    ("tactful", "bijak dan halus", "Cara berbicara yang menjaga perasaan orang lain."),
    ("norm", "norma", "Kebiasaan atau aturan sosial."),
    ("misunderstanding", "salah paham", "Ketika maksud tidak diterima dengan benar."),
    ("direction", "arah/tujuan", "Arah pembicaraan atau keputusan."),
    ("coaching", "membimbing", "Membantu orang lain berpikir dan berkembang."),
    ("actionable feedback", "masukan yang bisa ditindaklanjuti", "Feedback yang jelas dan bisa dilakukan."),
    ("implied meaning", "makna tersirat", "Maksud yang tidak diucapkan secara langsung."),
    ("long turn", "giliran bicara panjang", "Respons panjang dari lawan bicara."),
]


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def lesson_dirs(root: Path) -> list[Path]:
    return sorted(path for path in root.glob("*/units/*/lesson-*") if path.is_dir())


def useful_phrases(lesson_dir: Path) -> list[dict[str, str]]:
    data = read_yaml(lesson_dir / "useful_phrases.yaml")
    return [
        {
            "phrase": str(item.get("phrase") or "").strip(),
            "meaning": str(item.get("meaning_id") or item.get("meaning") or "").strip(),
            "usage": str(item.get("usage_note") or item.get("usage") or "").strip(),
        }
        for item in data.get("phrases", [])
        if item.get("phrase")
    ]


def dialogue_lines(lesson_dir: Path) -> list[str]:
    path = lesson_dir / "listening_script.md"
    if not path.exists():
        return []

    lines: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("**") or ":**" not in line:
            continue
        text = line.split(":**", 1)[1].strip()
        text = re.sub(r"\s{2,}$", "", text).strip()
        if text:
            lines.append(text)
    return lines


def contains_term(text: str, term: str) -> bool:
    pattern = r"(?<![A-Za-z])" + re.escape(term).replace(r"\ ", r"\s+") + r"s?(?![A-Za-z])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def source_example(term: str, phrases: list[dict[str, str]], dialogue: list[str]) -> str:
    for item in phrases:
        if contains_term(item["phrase"], term):
            return item["phrase"].strip()
    for line in dialogue:
        if contains_term(line, term):
            return line.strip()
    return ""


def example_sentence(example: str) -> str:
    if not example or "..." in example or example.endswith(","):
        return ""
    return example if example.endswith((".", "?", "!")) else f"{example}."


def item_from_term(term: str, meaning: str, note: str, phrases: list[dict[str, str]], dialogue: list[str]) -> dict[str, str]:
    example = source_example(term, phrases, dialogue)
    usage = note
    formatted_example = example_sentence(example)
    if formatted_example:
        usage = f"{note} Contoh: \"{formatted_example}\""
    return {
        "word": term,
        "meaning_id": meaning,
        "usage_note": usage,
    }


def phrase_fallbacks(phrases: list[dict[str, str]]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for phrase in phrases:
        words = [w.lower() for w in WORD_RE.findall(phrase["phrase"])]
        content_words = [w for w in words if w not in STOP_WORDS]
        term = next((word for word in content_words if len(word) >= 3), "")
        if not term:
            continue
        usage = (
            f"Muncul dalam frasa lesson: \"{example_sentence(phrase['phrase'])}\""
            if example_sentence(phrase["phrase"])
            else "Muncul sebagai bagian dari frasa lesson."
        )
        items.append(
            {
                "word": term,
                "meaning_id": f"bagian dari frasa: {phrase['meaning']}",
                "usage_note": usage,
            }
        )
    return items


def vocabulary_for_lesson(lesson_dir: Path, max_items: int = 6) -> list[dict[str, str]]:
    phrases = useful_phrases(lesson_dir)
    dialogue = dialogue_lines(lesson_dir)
    haystack = "\n".join([p["phrase"] for p in phrases] + dialogue)

    items: list[dict[str, str]] = []
    seen: set[str] = set()

    for term, meaning, note in CURATED_TERMS:
        if len(items) >= max_items:
            break
        key = term.lower()
        if key in seen or not contains_term(haystack, term):
            continue
        items.append(item_from_term(term, meaning, note, phrases, dialogue))
        seen.add(key)

    for item in phrase_fallbacks(phrases):
        if len(items) >= 4:
            break
        if len(items) >= max_items:
            break
        key = item["word"].lower()
        if key in seen or any(key in selected_key.split() for selected_key in seen):
            continue
        items.append(item)
        seen.add(key)

    return items


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate English vocabulary.yaml files.")
    parser.add_argument("--root", type=Path, default=ENGLISH_ROOT)
    parser.add_argument("--max-items", type=int, default=6)
    args = parser.parse_args()

    count = 0
    for lesson_dir in lesson_dirs(args.root):
        vocabulary = vocabulary_for_lesson(lesson_dir, max_items=args.max_items)
        if not vocabulary:
            raise RuntimeError(f"No vocabulary generated for {lesson_dir}")
        write_yaml(lesson_dir / "vocabulary.yaml", {"vocabulary": vocabulary})
        count += 1

    print(f"Generated vocabulary.yaml for {count} English lessons.")


if __name__ == "__main__":
    main()
