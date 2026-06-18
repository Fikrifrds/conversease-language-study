export const courseMarketingDescriptions: Record<string, string> = {
  "english-a1-start-simple-conversations":
    "Mulai dari sapaan, perkenalan, tanya-jawab pribadi sederhana, angka, waktu, tempat, belanja, bantuan, sampai misi percakapan A1 yang utuh.",
  "english-a2-everyday-conversations":
    "Bangun percakapan harian yang lebih natural: basa-basi ringan, rencana, undangan, transportasi, layanan, kesehatan, pengalaman lampau, dan opini sederhana.",
  "english-b1-confident-everyday-speaking":
    "Latihan cerita personal yang tersambung, situasi kerja dan perjalanan, menjelaskan masalah-solusi, membandingkan pilihan, dan menyampaikan alasan dengan jelas.",
  "english-b2-professional-discussions":
    "Latihan diskusi profesional: menyatakan posisi, mendukung argumen, rapat, negosiasi, presentasi ide, membaca informasi, komunikasi klien, dan pemecahan masalah.",
  "english-c1-advanced-fluency":
    "Latihan kefasihan tingkat lanjut: opini bernuansa, komunikasi strategis, presentasi kompleks, debat, lintas budaya, kepemimpinan, dan memahami respons panjang atau tidak langsung.",
  "arabic-a1-fusha-foundations":
    "Mulai dari sapaan formal, perkenalan, instruksi kelas, klarifikasi, ejaan, angka, kontak, rutinitas, tempat, belanja, permintaan bantuan, dan tinjauan A1.",
  "arabic-a2-everyday-conversations":
    "Bangun percakapan Arab harian formal: tanya lanjutan, membuat rencana, undangan, transportasi, layanan, kesehatan, pengalaman lampau, dan opini sederhana.",
  "arabic-b1-connected-conversations":
    "Latihan percakapan Arab yang lebih tersambung: cerita personal, kerja, perjalanan, masalah-solusi, tujuan, preferensi, komunitas, dan budaya.",
  "arabic-b2-professional-discussions":
    "Latihan diskusi Arab formal untuk konteks profesional: argumen, rapat, negosiasi, presentasi, informasi, komunikasi klien, dan pemecahan masalah.",
  "arabic-c1-advanced-fluency":
    "Latihan kefasihan Arab tingkat lanjut: opini bernuansa, komunikasi strategis, presentasi kompleks, debat, lintas budaya, kepemimpinan, dan pemahaman audio panjang."
};

export const courseGroupDescriptions = {
  english:
    "Jalur English lengkap untuk latihan berbicara dari A1 sampai C1, mulai dari percakapan dasar sampai diskusi profesional.",
  arabic:
    "Jalur Bahasa Arab formal lengkap dari A1 sampai C1, dengan harakat, audio, latihan peran, dan latihan percakapan bertahap."
};

export function courseMarketingDescription(slug: string, fallback: string) {
  return courseMarketingDescriptions[slug] ?? fallback;
}
