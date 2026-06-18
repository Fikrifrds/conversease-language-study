#!/usr/bin/env python3
"""Generate Arabic C1 beta curriculum content.

C1 is the final authored Arabic level in the current roadmap. It keeps the
same operational structure as A1-B2, but raises the conversation target:
nuance, strategy, persuasion, debate, leadership, cross-cultural tact, and
advanced listening response in formal Arabic.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

import yaml

from generate_arabic_vocabulary import vocabulary_for_lesson


REPO_ROOT = Path(__file__).resolve().parents[1]
C1_ROOT = REPO_ROOT / "content" / "curriculum" / "arabic" / "C1"
UNITS_ROOT = C1_ROOT / "units"
TRACKER_PATH = REPO_ROOT / "content" / "production_tracker.csv"
CONTENT_PLAN_PATH = C1_ROOT / "content_plan.yaml"

REQUIRED_SECTIONS = [
    "conversation_goal",
    "situation_setup",
    "listening",
    "comprehension_check",
    "useful_phrases",
    "vocabulary",
    "grammar_for_conversation",
    "speak_clearly",
    "response_practice",
    "conversation_coach_roleplay",
    "conversation_feedback",
    "conversation_check",
]

TEXT_TRACKER_COLUMNS = [
    "lesson_md",
    "listening_script",
    "phrases",
    "grammar",
    "pronunciation",
    "response_prompts",
    "conversation_coach",
    "quiz",
    "reading",
    "writing",
]


def phrase(text: str, meaning: str, usage: str) -> dict[str, str]:
    return {"phrase": text, "meaning": meaning, "usage": usage}


def line(speaker: str, text: str, translation: str) -> tuple[str, str, str]:
    return (speaker, text, translation)


UNIT_PROFILES: dict[str, dict[str, Any]] = {
    "unit-01-nuanced-opinions": {
        "title": "Nuanced Opinions",
        "speakers": ("Ahmad", "Karim"),
        "outcome": "Express nuanced opinions with precision and flexibility.",
        "situation": "Kamu menyampaikan opini yang tidak hitam-putih: ada tingkat keyakinan, sisi lain, batasan, dan penutup yang tetap sopan.",
        "prompt": ("كَيْفَ تُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ فِي هَذَا الْمَوْضُوعِ؟", "Bagaimana kamu menyampaikan opini yang nuanced tentang topik ini?"),
        "phrases": [
            phrase("مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", "Secara prinsip, saya cenderung pada pendapat ini, tetapi saya punya satu catatan penting.", "Menyampaikan opini dengan nuance."),
            phrase("لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", "Saya belum sepenuhnya yakin, tetapi bukti mengarah ke arah ini.", "Menyatakan kepastian dan keraguan."),
            phrase("مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", "Di satu sisi opsi ini praktis, di sisi lain ia punya risiko yang jelas.", "Menyeimbangkan dua sudut pandang."),
            phrase("أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", "Saya menghargai sudut pandangmu, tetapi saya melihat masalah ini dari sisi lain.", "Melunakkan disagreement."),
            phrase("لِذَلِكَ أُفَضِّلُ صِيَاغَةً أَكْثَرَ دِقَّةً وَمُرُونَةً.", "Karena itu, saya lebih memilih formulasi yang lebih tepat dan fleksibel.", "Menutup opini dengan presisi."),
        ],
        "grammar": "Gunakan مِنْ حَيْثُ، لَسْتُ مُتَيَقِّنًا، مِنْ جِهَةٍ، غَيْرَ أَنَّ، dan لِذَلِكَ untuk opini C1 yang nuanced.",
        "patterns": ["مِنْ حَيْثُ الْمَبْدَأِ، ...", "لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ ...", "مِنْ جِهَةٍ ... وَمِنْ جِهَةٍ أُخْرَى ...", "أُقَدِّرُ ... غَيْرَ أَنَّنِي ..."],
    },
    "unit-02-strategic-workplace-communication": {
        "title": "Strategic Workplace Communication",
        "speakers": ("Maryam", "Noura"),
        "outcome": "Communicate strategically in complex professional situations.",
        "situation": "Kamu perlu menyelaraskan beberapa pihak, mengelola ekspektasi, memberi feedback sensitif, dan menyampaikan risiko dengan hati-hati.",
        "prompt": ("كَيْفَ نُدِيرُ هَذَا الْحِوَارَ بِطَرِيقَةٍ اِسْتِرَاتِيجِيَّةٍ؟", "Bagaimana kita mengelola percakapan ini secara strategis?"),
        "phrases": [
            phrase("نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", "Pertama kita perlu menyatukan pemahaman pihak-pihak utama.", "Menyelaraskan stakeholder."),
            phrase("مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", "Lebih baik kita mengelola ekspektasi sebelum menjanjikan sesuatu yang spesifik.", "Mengelola ekspektasi."),
            phrase("سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", "Saya akan menyampaikan feedback ini dengan sensitif karena topiknya penting.", "Memberi feedback sensitif."),
            phrase("يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", "Ada risiko potensial, tetapi kita bisa menguranginya dengan rencana yang jelas.", "Mengomunikasikan risiko."),
            phrase("إِذَا تَوَافَقْنَا عَلَى هَذَا الْإِطَارِ، فَسَيَكُونُ التَّنْفِيذُ أَسْهَلَ.", "Jika kita sepakat pada kerangka ini, implementasinya akan lebih mudah.", "Menutup dengan alignment."),
        ],
        "grammar": "Gunakan نَحْتَاجُ إِلَى، مِنَ الْأَفْضَلِ أَنْ، لِأَنَّ، dan إِذَا untuk komunikasi strategis.",
        "patterns": ["نَحْتَاجُ أَوَّلًا إِلَى ...", "مِنَ الْأَفْضَلِ أَنْ ...", "يُوجَدُ خَطَرٌ ... وَلَكِنْ ...", "إِذَا تَوَافَقْنَا ... فَـ ..."],
    },
    "unit-03-advanced-presentations": {
        "title": "Advanced Presentations",
        "speakers": ("Salma", "Lina"),
        "outcome": "Present complex ideas and handle challenging questions.",
        "situation": "Kamu membawakan presentasi kompleks, membangun alur persuasif, memakai transisi presisi, dan menjawab pertanyaan sulit.",
        "prompt": ("كَيْفَ تُقَدِّمِينَ مَوْضُوعًا مُعَقَّدًا بِوُضُوحٍ؟", "Bagaimana kamu mempresentasikan topik kompleks dengan jelas?"),
        "phrases": [
            phrase("سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", "Saya akan membingkai topiknya dulu agar audiens memahami konteksnya.", "Membingkai topik kompleks."),
            phrase("بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", "Setelah itu, saya akan membangun alur persuasif langkah demi langkah.", "Membangun persuasive flow."),
            phrase("الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", "Transisi yang lebih tepat di sini adalah berpindah dari sebab ke dampak.", "Memakai transisi presisi."),
            phrase("إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", "Jika ada pertanyaan sulit, saya akan mengakui batas jawaban lalu menjelaskan dasarnya.", "Menjawab pertanyaan menantang."),
            phrase("فِي النِّهَايَةِ، أُرِيدُ أَنْ يَخْرُجَ الْجُمْهُورُ بِرِسَالَةٍ وَاضِحَةٍ.", "Pada akhirnya, saya ingin audiens pulang dengan pesan yang jelas.", "Menutup presentasi advanced."),
        ],
        "grammar": "Gunakan حَتَّى، بَعْدَ ذَلِكَ، مِنْ ... إِلَى ...، dan إِذَا untuk presentasi C1.",
        "patterns": ["سَأُؤَطِّرُ ... حَتَّى ...", "سَأَبْنِي ... خُطْوَةً فَخُطْوَةً", "نَنْتَقِلُ مِنْ ... إِلَى ...", "إِذَا جَاءَ ... فَـ ... ثُمَّ ..."],
    },
    "unit-04-debate-and-analysis": {
        "title": "Debate & Analysis",
        "speakers": ("Khalid", "Omar"),
        "outcome": "Analyze arguments and respond persuasively in debate-style conversations.",
        "situation": "Kamu menganalisis asumsi, menantang argumen, menyajikan bukti, dan merespons tekanan dengan tetap tenang.",
        "prompt": ("مَا الِافْتِرَاضُ الَّذِي يَقُومُ عَلَيْهِ هَذَا الْحُجَّةُ؟", "Asumsi apa yang menjadi dasar argumen ini?"),
        "phrases": [
            phrase("أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", "Saya pikir asumsi dasarnya di sini belum disebutkan dengan jelas.", "Mengidentifikasi asumsi."),
            phrase("يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", "Kita bisa menantang argumen ini dari sisi bukti.", "Menantang argumen."),
            phrase("الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", "Bukti paling kuat adalah bahwa hasilnya berulang dalam lebih dari satu konteks.", "Menyajikan evidence."),
            phrase("تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", "Di bawah tekanan, saya akan fokus pada poin pusat dan tidak berpanjang-panjang.", "Merespons under pressure."),
            phrase("لِذَلِكَ فَالرَّدُّ الْأَقْوَى هُوَ تَوْضِيحُ الِافْتِرَاضِ ثُمَّ فَحْصُ الدَّلِيلِ.", "Karena itu, respons terkuat adalah memperjelas asumsi lalu memeriksa bukti.", "Menutup analisis debat."),
        ],
        "grammar": "Gunakan أَنَّ، مِنْ جِهَةِ، فِي أَكْثَرَ مِنْ، dan تَحْتَ الضَّغْطِ untuk debat analitis.",
        "patterns": ["أَعْتَقِدُ أَنَّ الِافْتِرَاضَ ...", "نُحَدِّي هَذِهِ الْحُجَّةَ مِنْ جِهَةِ ...", "الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ ...", "تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى ..."],
    },
    "unit-05-cross-cultural-professionalism": {
        "title": "Cross-cultural Professionalism",
        "speakers": ("Fatimah", "Aisha"),
        "outcome": "Communicate across cultures with tact, clarity, and professionalism.",
        "situation": "Kamu membaca konteks lintas budaya, bertanya dengan tact, menjelaskan norma lokal, dan memperbaiki salah paham.",
        "prompt": ("كَيْفَ نَتَصَرَّفُ بِمِهَنِيَّةٍ فِي سِيَاقٍ ثَقَافِيٍّ مُخْتَلِفٍ؟", "Bagaimana kita bersikap profesional dalam konteks budaya yang berbeda?"),
        "phrases": [
            phrase("قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", "Sebelum merespons, kita harus membaca konteks dengan cermat.", "Membaca konteks."),
            phrase("هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", "Bisakah saya bertanya dengan cara yang lebih tactful?", "Bertanya dengan halus."),
            phrase("فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", "Di negara saya, norma ini dipahami dengan cara yang berbeda.", "Menjelaskan norma lokal."),
            phrase("يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", "Sepertinya ada salah paham, jadi mari kita merumuskan ulang idenya.", "Memperbaiki misunderstanding."),
            phrase("الْهَدَفُ هُوَ الْوُضُوحُ مَعَ الِاحْتِرَامِ، لَا مُجَرَّدُ الصَّحَّةِ اللُّغَوِيَّةِ.", "Tujuannya adalah kejelasan dengan rasa hormat, bukan sekadar kebenaran bahasa.", "Menutup dengan prinsip profesional."),
        ],
        "grammar": "Gunakan قَبْلَ أَنْ، هَلْ يُمْكِنُ، فِي بَلَدِي، dan يَبْدُو أَنَّ untuk komunikasi lintas budaya.",
        "patterns": ["قَبْلَ أَنْ ... يَجِبُ أَنْ ...", "هَلْ يُمْكِنُ أَنْ ...؟", "فِي بَلَدِي، ... يُفْهَمُ ...", "يَبْدُو أَنَّ هُنَاكَ ... فَـ ..."],
    },
    "unit-06-leadership-and-coaching": {
        "title": "Leadership & Coaching",
        "speakers": ("Rami", "Tariq"),
        "outcome": "Lead conversations, coach others, and guide decisions.",
        "situation": "Kamu memimpin percakapan, menetapkan arah, melatih dengan pertanyaan, memberi feedback yang actionable, dan membimbing keputusan.",
        "prompt": ("كَيْفَ تُوَجِّهُ الْفَرِيقَ فِي هَذَا الْمَوْقِفِ؟", "Bagaimana kamu mengarahkan tim dalam situasi ini?"),
        "phrases": [
            phrase("أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", "Hal pertama adalah menetapkan arah dengan jelas.", "Menetapkan direction."),
            phrase("بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", "Daripada memberi jawaban langsung, saya akan bertanya pertanyaan yang membuka pemikiran.", "Coaching dengan pertanyaan."),
            phrase("الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", "Feedback yang berguna adalah yang berubah menjadi langkah yang dapat diterapkan.", "Memberi actionable feedback."),
            phrase("عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", "Saat mengambil keputusan, kita harus menyeimbangkan kecepatan dan kualitas.", "Membimbing keputusan."),
            phrase("سَأُغْلِقُ الْحِوَارَ بِتَوْضِيحِ الْمَسْؤُولِيَّةِ وَالْمَوْعِدِ.", "Saya akan menutup percakapan dengan memperjelas tanggung jawab dan tenggat.", "Menutup leadership conversation."),
        ],
        "grammar": "Gunakan بَدَلًا مِنْ أَنْ، الَّتِي، عِنْدَ، dan سَـ untuk leadership conversation yang matang.",
        "patterns": ["أَوَّلُ شَيْءٍ هُوَ ...", "بَدَلًا مِنْ أَنْ ... سَأَسْأَلُ ...", "... هِيَ الَّتِي ...", "يَجِبُ أَنْ نُوَازِنَ بَيْنَ ... وَ ..."],
    },
    "unit-07-advanced-listening-response": {
        "title": "Advanced Listening & Response",
        "speakers": ("Yusuf", "Hasan"),
        "outcome": "Respond accurately to dense, fast, or indirect speech.",
        "situation": "Kamu mendengar ujaran panjang atau tidak langsung, menangkap makna tersirat, merangkum, dan bertanya follow-up berkualitas.",
        "prompt": ("مَاذَا فَهِمْتَ مِنَ الْكَلَامِ الطَّوِيلِ الَّذِي سَمِعْتَهُ؟", "Apa yang kamu pahami dari ujaran panjang yang kamu dengar?"),
        "phrases": [
            phrase("الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", "Makna tersiratnya di sini adalah pembicara belum sepenuhnya yakin.", "Menangkap implied meaning."),
            phrase("سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", "Saya akan menjawab poin utama dulu, lalu kembali ke detail.", "Merespons long turn."),
            phrase("إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", "Jika saya merangkum apa yang saya dengar, ide utamanya adalah menunda keputusan.", "Merangkum yang didengar."),
            phrase("سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", "Pertanyaan follow-up terbaik adalah: apa yang akan mengubah keputusan ini?", "Bertanya follow-up berkualitas."),
            phrase("بِهَذِهِ الطَّرِيقَةِ، لَا أَرُدُّ عَلَى الْكَلِمَاتِ فَقَطْ، بَلْ عَلَى الْمَقْصُودِ.", "Dengan cara ini, saya tidak hanya merespons kata-kata, tetapi maksudnya.", "Menutup advanced listening response."),
        ],
        "grammar": "Gunakan الْمَعْنَى الضِّمْنِيُّ، إِذَا، ثُمَّ، dan بَلْ untuk respons listening C1.",
        "patterns": ["الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ ...", "سَأُجِيبُ أَوَّلًا عَلَى ... ثُمَّ ...", "إِذَا لَخَّصْتُ ... فَـ ...", "لَا ... فَقَطْ، بَلْ ..."],
    },
    "unit-08-c1-review-final": {
        "title": "C1 Review & Final Conversation",
        "speakers": ("Layla", "Noura"),
        "outcome": "Use C1 skills in complex professional and social conversations.",
        "situation": "Kamu menggabungkan nuance, strategi, presentasi, debat, cross-cultural tact, leadership, dan listening response dalam final conversation.",
        "prompt": ("مَا الْمَهَارَةُ الَّتِي تَحْتَاجُ إِلَى مُرَاجَعَةٍ أَخِيرَةٍ؟", "Skill apa yang perlu final review?"),
        "phrases": [
            phrase("أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", "Saya sedang mereview cara menyampaikan opini yang tepat tanpa berlebihan.", "Review nuance."),
            phrase("فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", "Dalam percakapan profesional, saya akan fokus pada konteks, ekspektasi, dan risiko.", "Review strategy."),
            phrase("عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", "Saat presentasi atau diskusi, saya akan membangun ide dengan urutan yang persuasif.", "Review presenting and debate."),
            phrase("إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", "Jika muncul salah paham, saya akan memperbaikinya dengan tact dan kejelasan.", "Review cross-cultural repair."),
            phrase("فِي التَّقْيِيمِ النِّهَائِيِّ، سَأُظْهِرُ الدِّقَّةَ وَالْمُرُونَةَ وَحُسْنَ الِاسْتِمَاعِ.", "Dalam tes akhir, saya akan menunjukkan presisi, fleksibilitas, dan listening yang baik.", "Menutup final C1."),
        ],
        "grammar": "Gabungkan دُونَ، فِي، عِنْدَ، إِذَا، dan وَ untuk final conversation yang kompleks tetapi jelas.",
        "patterns": ["أُرَاجِعُ كَيْفَ ... دُونَ ...", "فِي الْحِوَارِ ... سَأُرَكِّزُ عَلَى ...", "عِنْدَ ... سَأَبْنِي ...", "إِذَا ظَهَرَ ... فَسَأُصْلِحُهُ ..."],
    },
}


LESSONS_BY_UNIT: dict[str, list[tuple[str, str, str]]] = {
    "unit-01-nuanced-opinions": [
        ("lesson-01-qualifying-your-opinion", "arabic-c1-qualifying-your-opinion", "Qualifying Your Opinion"),
        ("lesson-02-expressing-certainty-and-doubt", "arabic-c1-expressing-certainty-and-doubt", "Expressing Certainty and Doubt"),
        ("lesson-03-balancing-two-viewpoints", "arabic-c1-balancing-two-viewpoints", "Balancing Two Viewpoints"),
        ("lesson-04-softening-disagreement", "arabic-c1-softening-disagreement", "Softening Disagreement"),
        ("lesson-05-nuanced-opinion-mission", "arabic-c1-nuanced-opinion-mission", "Nuanced Opinion Mission"),
    ],
    "unit-02-strategic-workplace-communication": [
        ("lesson-01-aligning-stakeholders", "arabic-c1-aligning-stakeholders", "Aligning Stakeholders"),
        ("lesson-02-managing-expectations", "arabic-c1-managing-expectations", "Managing Expectations"),
        ("lesson-03-handling-sensitive-feedback", "arabic-c1-handling-sensitive-feedback", "Handling Sensitive Feedback"),
        ("lesson-04-communicating-risk", "arabic-c1-communicating-risk", "Communicating Risk"),
        ("lesson-05-strategic-workplace-mission", "arabic-c1-strategic-workplace-mission", "Strategic Workplace Mission"),
    ],
    "unit-03-advanced-presentations": [
        ("lesson-01-framing-a-complex-topic", "arabic-c1-framing-a-complex-topic", "Framing a Complex Topic"),
        ("lesson-02-building-a-persuasive-flow", "arabic-c1-building-a-persuasive-flow", "Building a Persuasive Flow"),
        ("lesson-03-using-precise-transitions", "arabic-c1-using-precise-transitions", "Using Precise Transitions"),
        ("lesson-04-handling-challenging-questions", "arabic-c1-handling-challenging-questions", "Handling Challenging Questions"),
        ("lesson-05-advanced-presentation-mission", "arabic-c1-advanced-presentation-mission", "Advanced Presentation Mission"),
    ],
    "unit-04-debate-and-analysis": [
        ("lesson-01-identifying-assumptions", "arabic-c1-identifying-assumptions", "Identifying Assumptions"),
        ("lesson-02-challenging-an-argument", "arabic-c1-challenging-an-argument", "Challenging an Argument"),
        ("lesson-03-presenting-evidence", "arabic-c1-presenting-evidence", "Presenting Evidence"),
        ("lesson-04-responding-under-pressure", "arabic-c1-responding-under-pressure", "Responding Under Pressure"),
        ("lesson-05-debate-analysis-mission", "arabic-c1-debate-analysis-mission", "Debate Analysis Mission"),
    ],
    "unit-05-cross-cultural-professionalism": [
        ("lesson-01-reading-context", "arabic-c1-reading-context", "Reading Context"),
        ("lesson-02-asking-tactful-questions", "arabic-c1-asking-tactful-questions", "Asking Tactful Questions"),
        ("lesson-03-explaining-local-norms", "arabic-c1-explaining-local-norms", "Explaining Local Norms"),
        ("lesson-04-repairing-misunderstanding", "arabic-c1-repairing-misunderstanding", "Repairing Misunderstanding"),
        ("lesson-05-cross-cultural-mission", "arabic-c1-cross-cultural-mission", "Cross-cultural Mission"),
    ],
    "unit-06-leadership-and-coaching": [
        ("lesson-01-setting-direction", "arabic-c1-setting-direction", "Setting Direction"),
        ("lesson-02-coaching-with-questions", "arabic-c1-coaching-with-questions", "Coaching With Questions"),
        ("lesson-03-giving-actionable-feedback", "arabic-c1-giving-actionable-feedback", "Giving Actionable Feedback"),
        ("lesson-04-guiding-a-decision", "arabic-c1-guiding-a-decision", "Guiding a Decision"),
        ("lesson-05-leadership-coaching-mission", "arabic-c1-leadership-coaching-mission", "Leadership Coaching Mission"),
    ],
    "unit-07-advanced-listening-response": [
        ("lesson-01-catching-implied-meaning", "arabic-c1-catching-implied-meaning", "Catching Implied Meaning"),
        ("lesson-02-responding-to-long-turns", "arabic-c1-responding-to-long-turns", "Responding to Long Turns"),
        ("lesson-03-summarizing-what-you-heard", "arabic-c1-summarizing-what-you-heard", "Summarizing What You Heard"),
        ("lesson-04-asking-high-quality-follow-ups", "arabic-c1-asking-high-quality-follow-ups", "Asking High-quality Follow-ups"),
        ("lesson-05-advanced-listening-mission", "arabic-c1-advanced-listening-mission", "Advanced Listening Mission"),
    ],
    "unit-08-c1-review-final": [
        ("lesson-01-review-nuance-and-strategy", "arabic-c1-review-nuance-and-strategy", "Review Nuance and Strategy"),
        ("lesson-02-review-presenting-and-debate", "arabic-c1-review-presenting-and-debate", "Review Presenting and Debate"),
        ("lesson-03-review-leadership-and-listening", "arabic-c1-review-leadership-and-listening", "Review Leadership and Listening"),
        ("lesson-04-c1-final-test-practice", "arabic-c1-c1-final-test-practice", "C1 Final Test Practice"),
        ("lesson-05-c1-final-conversation", "arabic-c1-c1-final-conversation", "C1 Final Conversation"),
    ],
}


LESSON_FOCUS_BY_KEY: dict[str, tuple[str, str]] = {
    "lesson-01-qualifying-your-opinion": ("تَأْهِيلِ الرَّأْيِ قَبْلَ الْحُكْمِ", "qualifying opinion before making a claim"),
    "lesson-02-expressing-certainty-and-doubt": ("التَّفْرِيقِ بَيْنَ الْيَقِينِ وَالشَّكِّ", "separating certainty and doubt"),
    "lesson-03-balancing-two-viewpoints": ("الْمُوَازَنَةِ بَيْنَ وِجْهَتَيْ نَظَرٍ", "balancing two viewpoints"),
    "lesson-04-softening-disagreement": ("تَلْطِيفِ الِاخْتِلَافِ مَعَ الْآخَرِينَ", "softening disagreement"),
    "lesson-05-nuanced-opinion-mission": ("تَرْكِيبِ رَأْيٍ دَقِيقٍ مُتَكَامِلٍ", "building a complete nuanced opinion"),
    "lesson-01-aligning-stakeholders": ("مُوَاءَمَةِ أَصْحَابِ الْمَصْلَحَةِ", "aligning stakeholders"),
    "lesson-02-managing-expectations": ("إِدَارَةِ التَّوَقُّعَاتِ الْوَاقِعِيَّةِ", "managing realistic expectations"),
    "lesson-03-handling-sensitive-feedback": ("تَقْدِيمِ تَعْلِيقٍ حَسَّاسٍ بِلُطْفٍ", "handling sensitive feedback tactfully"),
    "lesson-04-communicating-risk": ("شَرْحِ الْمَخَاطِرِ بِدُونِ تَهْوِيلٍ", "communicating risk without exaggeration"),
    "lesson-05-strategic-workplace-mission": ("إِدَارَةِ حِوَارٍ مِهَنِيٍّ اِسْتِرَاتِيجِيٍّ", "running a strategic workplace conversation"),
    "lesson-01-framing-a-complex-topic": ("تَأْطِيرِ مَوْضُوعٍ مُعَقَّدٍ", "framing a complex topic"),
    "lesson-02-building-a-persuasive-flow": ("بِنَاءِ تَسَلْسُلٍ إِقْنَاعِيٍّ", "building a persuasive flow"),
    "lesson-03-using-precise-transitions": ("اِسْتِخْدَامِ اِنْتِقَالَاتٍ دَقِيقَةٍ", "using precise transitions"),
    "lesson-04-handling-challenging-questions": ("التَّعَامُلِ مَعَ أَسْئِلَةٍ صَعْبَةٍ", "handling challenging questions"),
    "lesson-05-advanced-presentation-mission": ("تَقْدِيمِ عَرْضٍ مُتَقَدِّمٍ وَاضِحٍ", "delivering an advanced presentation"),
    "lesson-01-identifying-assumptions": ("تَحْدِيدِ الِافْتِرَاضَاتِ الْخَفِيَّةِ", "identifying hidden assumptions"),
    "lesson-02-challenging-an-argument": ("مُنَاقَشَةِ حُجَّةٍ بِأَدَبٍ", "challenging an argument politely"),
    "lesson-03-presenting-evidence": ("تَقْدِيمِ دَلِيلٍ مُرْتَبِطٍ بِالْمَوْضُوعِ", "presenting relevant evidence"),
    "lesson-04-responding-under-pressure": ("الرَّدِّ تَحْتَ الضَّغْطِ بِهُدُوءٍ", "responding calmly under pressure"),
    "lesson-05-debate-analysis-mission": ("إِدَارَةِ نِقَاشٍ تَحْلِيلِيٍّ مُتَوَازِنٍ", "running a balanced analytical debate"),
    "lesson-01-reading-context": ("قِرَاءَةِ السِّيَاقِ الِاجْتِمَاعِيِّ", "reading social context"),
    "lesson-02-asking-tactful-questions": ("طَرْحِ أَسْئِلَةٍ لَبِقَةٍ", "asking tactful questions"),
    "lesson-03-explaining-local-norms": ("شَرْحِ الْأَعْرَافِ الْمَحَلِّيَّةِ", "explaining local norms"),
    "lesson-04-repairing-misunderstanding": ("إِصْلَاحِ سُوءِ الْفَهْمِ", "repairing misunderstanding"),
    "lesson-05-cross-cultural-mission": ("إِدَارَةِ حِوَارٍ عَبْرَ الثَّقَافَاتِ", "running a cross-cultural conversation"),
    "lesson-01-setting-direction": ("تَحْدِيدِ الِاتِّجَاهِ بِوُضُوحٍ", "setting direction clearly"),
    "lesson-02-coaching-with-questions": ("التَّوْجِيهِ بِالْأَسْئِلَةِ", "coaching with questions"),
    "lesson-03-giving-actionable-feedback": ("تَقْدِيمِ تَغْذِيَةٍ رَاجِعَةٍ قَابِلَةٍ لِلْعَمَلِ", "giving actionable feedback"),
    "lesson-04-guiding-a-decision": ("تَوْجِيهِ قَرَارٍ جَمَاعِيٍّ", "guiding a group decision"),
    "lesson-05-leadership-coaching-mission": ("إِدَارَةِ حِوَارٍ قِيَادِيٍّ تَوْجِيهِيٍّ", "running a leadership coaching conversation"),
    "lesson-01-catching-implied-meaning": ("الْتِقَاطِ الْمَعْنَى الضِّمْنِيِّ", "catching implied meaning"),
    "lesson-02-responding-to-long-turns": ("الرَّدِّ عَلَى كَلَامٍ طَوِيلٍ", "responding to long turns"),
    "lesson-03-summarizing-what-you-heard": ("تَلْخِيصِ مَا سَمِعْتَهُ بِدِقَّةٍ", "summarizing what you heard accurately"),
    "lesson-04-asking-high-quality-follow-ups": ("طَرْحِ أَسْئِلَةِ مُتَابَعَةٍ عَالِيَةِ الْجَوْدَةِ", "asking high-quality follow-ups"),
    "lesson-05-advanced-listening-mission": ("إِدَارَةِ رَدٍّ بَعْدَ اِسْتِمَاعٍ مُتَقَدِّمٍ", "responding after advanced listening"),
    "lesson-01-review-nuance-and-strategy": ("مُرَاجَعَةِ الدِّقَّةِ وَالِاسْتِرَاتِيجِيَّةِ", "reviewing nuance and strategy"),
    "lesson-02-review-presenting-and-debate": ("مُرَاجَعَةِ الْعَرْضِ وَالنِّقَاشِ", "reviewing presenting and debate"),
    "lesson-03-review-leadership-and-listening": ("مُرَاجَعَةِ الْقِيَادَةِ وَحُسْنِ الِاسْتِمَاعِ", "reviewing leadership and listening"),
    "lesson-04-c1-final-test-practice": ("تَدْرِيبِ الِاخْتِبَارِ النِّهَائِيِّ", "practicing the final test"),
    "lesson-05-c1-final-conversation": ("إِدَارَةِ مُحَادَثَةٍ نِهَائِيَّةٍ مُتَكَامِلَةٍ", "running a complete final conversation"),
}


def build_lesson(unit_key: str, lesson_data: tuple[str, str, str]) -> dict[str, Any]:
    profile = UNIT_PROFILES[unit_key]
    lesson_key, slug, title = lesson_data
    speaker_a, speaker_b = profile["speakers"]
    focus_ar, focus_id = LESSON_FOCUS_BY_KEY[lesson_key]
    base_phrases = profile["phrases"]
    phrases = [
        phrase(
            f"فِي مَهَارَةِ {focus_ar}، {base_phrases[0]['phrase']}",
            f"Dalam skill {focus_id}, {base_phrases[0]['meaning']}",
            f"{base_phrases[0]['usage']} Fokus lesson: {focus_id}.",
        ),
        phrase(
            f"عِنْدَ تَطْبِيقِ {focus_ar}، {base_phrases[1]['phrase']}",
            f"Saat menerapkan {focus_id}, {base_phrases[1]['meaning']}",
            f"{base_phrases[1]['usage']} Hubungkan dengan fokus lesson.",
        ),
        phrase(
            base_phrases[2]["phrase"],
            base_phrases[2]["meaning"],
            f"{base_phrases[2]['usage']} Pakai sebagai penghubung dalam {focus_id}.",
        ),
        phrase(
            f"إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، {base_phrases[3]['phrase']}",
            f"Jika muncul tantangan dalam skill ini, {base_phrases[3]['meaning']}",
            f"{base_phrases[3]['usage']} Gunakan untuk repair dalam {focus_id}.",
        ),
        phrase(
            f"فِي الصِّيَاغَةِ النِّهَائِيَّةِ لِهَذِهِ الْمَهَارَةِ، {base_phrases[4]['phrase']}",
            f"Dalam final formulation untuk {focus_id}, {base_phrases[4]['meaning']}",
            f"{base_phrases[4]['usage']} Tutup percakapan sesuai fokus lesson.",
        ),
    ]
    prompt_ar = f"كَيْفَ تُطَبِّقُ مَهَارَةَ {focus_ar} فِي حِوَارٍ رَسْمِيٍّ؟"
    prompt_id = f"Bagaimana kamu menerapkan {focus_id} dalam percakapan formal?"
    dialogue = [
        line(speaker_a, prompt_ar, prompt_id),
        line(speaker_b, phrases[0]["phrase"], phrases[0]["meaning"]),
        line(speaker_a, "هَذَا جَيِّدٌ، وَلَكِنْ مَا الْجَانِبُ الَّذِي يَحْتَاجُ إِلَى دِقَّةٍ أَكْبَرَ؟", "Bagus, tetapi sisi mana yang membutuhkan presisi lebih besar?"),
        line(speaker_b, f"{phrases[1]['phrase']} {phrases[2]['phrase']}", f"{phrases[1]['meaning']} {phrases[2]['meaning']}"),
        line(speaker_a, "كَيْفَ تَتَعَامَلُ مَعَ النُّقْطَةِ الْمُعَارِضَةِ أَوْ سُوءِ الْفَهْمِ؟", "Bagaimana kamu menangani counterpoint atau salah paham?"),
        line(speaker_b, phrases[3]["phrase"], phrases[3]["meaning"]),
        line(speaker_a, "مَا الصِّيَاغَةُ النِّهَائِيَّةُ الَّتِي تُنَاسِبُ مَوْقِفًا رَسْمِيًّا؟", "Apa formulasi akhir yang cocok untuk situasi formal?"),
        line(speaker_b, phrases[4]["phrase"], phrases[4]["meaning"]),
    ]
    return {
        "lesson_key": lesson_key,
        "slug": slug,
        "title": title,
        "status": "beta",
        "focus": focus_ar,
        "focus_id": focus_id,
        "situation": profile["situation"],
        "goal": f"Latih percakapan Arab C1 untuk {focus_id} dengan nuance, struktur, presisi, dan respons profesional.",
        "grammar": profile["grammar"],
        "patterns": profile["patterns"],
        "phrases": phrases,
        "dialogue": dialogue,
    }


def expand_units() -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    for unit_key, lessons in LESSONS_BY_UNIT.items():
        profile = UNIT_PROFILES[unit_key]
        units.append(
            {
                "unit_key": unit_key,
                "title": profile["title"],
                "main_conversation_outcome": profile["outcome"],
                "lessons": [build_lesson(unit_key, item) for item in lessons],
            }
        )
    return units


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")


def write_level_files(units: list[dict[str, Any]]) -> None:
    C1_ROOT.mkdir(parents=True, exist_ok=True)
    (C1_ROOT / "LEVEL_SPEC.md").write_text(
        "# Arabic C1 - Advanced Fluency\n\n"
        "## Level Outcome\n\n"
        "Learners can participate in complex professional and social conversations with nuance, precision, tact, strategic framing, persuasive structure, and accurate response to indirect or dense speech in formal Arabic.\n\n"
        "## Scope\n\n"
        "- Formal Arabic / Modern Standard Arabic, not dialect.\n"
        "- Indonesian explanations for adult learners.\n"
        "- Arabic script with harakat for learner-facing examples and listening scripts.\n"
        "- Complex but practical conversation targets: nuanced opinions, strategic work communication, advanced presentations, debate, cross-cultural professionalism, leadership, and advanced listening response.\n"
        "- Speaker labels are metadata and must not be spoken in generated audio.\n"
        "- No religious source text or devotional TTS content.\n\n"
        "## C1 Upgrade From B2\n\n"
        "- Dialogue length: 8 dense turns with explicit nuance and repair strategies.\n"
        "- Learner responses include qualification, uncertainty, counterpoint, tact, and precise final formulation.\n"
        "- Introduce advanced discourse markers and indirect meaning handling.\n"
        "- Keep language formal, natural, and usable for professional conversation.\n\n"
        "## Passing Threshold\n\n"
        "- Overall score: 82\n"
        "- Speaking / Conversation: 76\n"
        "- Listening: 74\n"
        "- Pronunciation: 68\n"
        "- Vocabulary / Useful Phrases: 74\n"
        "- Grammar: 74\n"
        "- Reading: 70\n"
        "- Writing: 70\n"
        "- Lesson completion: 90%\n",
        encoding="utf-8",
    )
    write_yaml(
        CONTENT_PLAN_PATH,
        {
            "language": "arabic",
            "language_code": "ar",
            "level_code": "C1",
            "course_slug": "arabic-c1-advanced-fluency",
            "course_title": "Arabic Advanced Fluency",
            "access_tier": "pro_beta",
            "target_lesson_count": 40,
            "quality_reference": "docs/arabic_content_standard.md",
            "units": [
                {
                    "unit_key": unit["unit_key"],
                    "title": unit["title"],
                    "status": "beta",
                    "main_conversation_outcome": unit["main_conversation_outcome"],
                    "lessons": [
                        {"lesson_key": item["lesson_key"], "slug": item["slug"], "title": item["title"], "status": item["status"]}
                        for item in unit["lessons"]
                    ],
                }
                for unit in units
            ],
        },
    )


def roleplay_payload(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "scenario_key": item["slug"].replace("-", "_"),
        "mode": "lesson_practice_coach",
        "level_code": "C1",
        "opening_line": item["dialogue"][0][1],
        "learner_goal": item["goal"],
        "max_turns": 8,
        "feedback_level": {"free": "basic", "pro": "detailed"},
        "turns": [
            {
                "coach": item["dialogue"][0][1] if index == 1 else f"استخدم الفكرة: {entry['phrase']}",
                "hint": f"Jawab dengan struktur C1 memakai: {entry['phrase']}",
                "sample_answer": entry["phrase"],
                "focus": entry["usage"],
                "expected_keywords": entry["phrase"].replace("؟", "").replace(".", "").split()[:5],
                "indonesian_explanation": entry["meaning"],
            }
            for index, entry in enumerate(item["phrases"][:4], 1)
        ],
        "target_phrases": [entry["phrase"] for entry in item["phrases"][:5]],
        "rubric": {
            "speaking": {"minimum_score": 76},
            "relevance": {"minimum_score": 76},
            "nuance": {"minimum_score": 74},
            "grammar": {"minimum_score": 74},
        },
    }


def phrase_options(phrases: list[dict[str, str]], correct_index: int) -> list[str]:
    correct = phrases[correct_index]["phrase"]
    options = [correct]
    for entry in phrases:
        if entry["phrase"] not in options:
            options.append(entry["phrase"])
        if len(options) == 3:
            break
    return options


def write_unit_and_lessons(unit: dict[str, Any]) -> None:
    unit_dir = UNITS_ROOT / unit["unit_key"]
    write_yaml(
        unit_dir / "unit.yaml",
        {
            "unit_key": unit["unit_key"],
            "level_code": "C1",
            "title": unit["title"],
            "main_conversation_outcome": unit["main_conversation_outcome"],
            "status": "beta",
            "lessons": [item["lesson_key"] for item in unit["lessons"]],
        },
    )

    for item in unit["lessons"]:
        lesson_dir = unit_dir / item["lesson_key"]
        lesson_dir.mkdir(parents=True, exist_ok=True)
        write_yaml(
            lesson_dir / "lesson.yaml",
            {
                "lesson_key": item["lesson_key"],
                "slug": item["slug"],
                "title": item["title"],
                "status": item["status"],
                "estimated_minutes": 18,
                "conversation_situation": item["slug"].replace("arabic-c1-", "").replace("-", "_"),
                "conversation_goal": item["goal"],
                "grammar_summary": item["grammar"],
                "required_sections": REQUIRED_SECTIONS,
                "completion_rules": {"listening_completed": True, "quiz_required": True, "speaking_attempt_required": True, "minimum_score": 76},
            },
        )
        (lesson_dir / "lesson.md").write_text(
            f"# {item['title']}\n\n"
            "Setelah lesson ini, kamu bisa memakai bahasa Arab formal untuk percakapan C1 yang lebih halus, strategis, dan presisi.\n\n"
            "## Situation\n\n"
            f"{item['situation']}\n\n"
            "## Catatan Belajar\n\n"
            "Di C1, tujuan utamanya bukan kalimat panjang. Tujuannya adalah memilih struktur yang tepat: nuance, batasan, alasan, repair, dan formulasi akhir yang matang.\n",
            encoding="utf-8",
        )
        (lesson_dir / "conversation_goal.md").write_text(
            f"# Target Percakapan\n\n{item['goal']}\n\nKamu akan berlatih mengatakan:\n\n"
            + "\n".join(f"- {entry['phrase']}" for entry in item["phrases"][:5])
            + "\n",
            encoding="utf-8",
        )
        (lesson_dir / "listening_script.md").write_text(
            "# Listening Script\n\n"
            + "\n".join(f"**{speaker}:** {text}" for speaker, text, _ in item["dialogue"])
            + "\n\n## Audio Direction\n\n"
            "Use Arabic only. Speaker labels are metadata and must not be spoken. "
            "Keep a confident C1 discussion pace with clean pauses after clauses. "
            "Use distinct voices according to speaker names and gender.\n",
            encoding="utf-8",
        )
        (lesson_dir / "transcript_translation.md").write_text(
            "# Transcript Translation\n\n"
            + "\n".join(f"- **{speaker}:** {text} -> {translation}" for speaker, text, translation in item["dialogue"])
            + "\n",
            encoding="utf-8",
        )
        write_yaml(
            lesson_dir / "useful_phrases.yaml",
            {"phrases": [{"phrase": entry["phrase"], "meaning_id": entry["meaning"], "usage_note": entry["usage"]} for entry in item["phrases"]]},
        )
        write_yaml(lesson_dir / "vocabulary.yaml", {"vocabulary": vocabulary_for_lesson(item["phrases"], item["dialogue"])})
        (lesson_dir / "grammar_for_conversation.md").write_text(
            "# Pola Percakapan\n\n"
            f"{item['grammar']}\n\n```txt\n"
            + "\n".join(item["patterns"])
            + "\n```\n\n"
            "Gunakan pola ini untuk menjaga presisi. Jawaban C1 boleh kompleks, tetapi setiap klausa harus punya fungsi yang jelas.\n",
            encoding="utf-8",
        )
        (lesson_dir / "pronunciation_drill.md").write_text(
            "# Latihan Pengucapan\n\n## Ulangi\n\n"
            + "\n".join(f"{index}. {entry['phrase']}" for index, entry in enumerate(item["phrases"][:5], 1))
            + "\n\n## Fokus\n\n"
            "- Beri jeda setelah frasa pembatas seperti وَلَكِنْ، غَيْرَ أَنَّ، dan إِذَا.\n"
            "- Jaga intonasi tetap tenang saat menyampaikan disagreement atau risk.\n"
            "- Jangan mengorbankan kejelasan demi kecepatan.\n",
            encoding="utf-8",
        )
        write_yaml(
            lesson_dir / "response_prompts.yaml",
            {"prompts": [{"prompt": f"Ucapkan dalam bahasa Arab: {entry['meaning']}", "target_response": entry["phrase"], "acceptable_responses": [entry["phrase"]]} for entry in item["phrases"][:4]]},
        )
        write_yaml(
            lesson_dir / "quiz.yaml",
            {"questions": [{"key": f"phrase_{index}", "prompt": f"Frasa mana yang berarti \"{entry['meaning']}\"?", "options": phrase_options(item["phrases"], index - 1), "correct_answer": entry["phrase"]} for index, entry in enumerate(item["phrases"][:2], 1)]},
        )
        write_yaml(lesson_dir / "conversation_coach_roleplay.yaml", roleplay_payload(item))
        (lesson_dir / "reading_support.md").write_text(
            "# Bantuan Membaca\n\n"
            "Cari dulu fungsi setiap klausa: qualification, uncertainty, contrast, repair, atau final formulation. Jangan menerjemahkan kata per kata sebelum memahami fungsi kalimat.\n\n"
            + "\n".join(f"- {entry['phrase']} -> {entry['meaning']}" for entry in item["phrases"][:5])
            + "\n",
            encoding="utf-8",
        )
        (lesson_dir / "writing_support.md").write_text(
            "# Bantuan Menulis\n\n"
            "Tulis jawaban C1 dalam lima bagian: framing, nuance, evidence atau reason, repair/counterpoint, dan final formulation.\n\n"
            + "\n".join(f"- {entry['phrase']}" for entry in item["phrases"][:5])
            + "\n",
            encoding="utf-8",
        )
        write_yaml(
            lesson_dir / "audio_manifest.yaml",
            {"lesson_key": item["lesson_key"], "status": "not_generated", "provider": "elevenlabs", "model": "eleven_v3", "default_voice_id": "multi_speaker", "assets": []},
        )


def update_tracker(units: list[dict[str, Any]]) -> None:
    raw_tracker = TRACKER_PATH.read_bytes()
    reader = csv.DictReader(io.StringIO(raw_tracker.decode("utf-8")))
    fieldnames = reader.fieldnames or []
    existing = {(row["level"], row["unit"], row["lesson"]) for row in reader}
    missing_rows: list[dict[str, str]] = []

    for unit in units:
        for item in unit["lessons"]:
            key = ("arabic/C1", unit["unit_key"], item["lesson_key"])
            if key in existing:
                continue
            row = {name: "" for name in fieldnames}
            row["level"], row["unit"], row["lesson"] = key
            for column in TEXT_TRACKER_COLUMNS:
                row[column] = "done"
            row["audio_generated"] = "not_generated"
            row["review_status"] = ""
            row["publish_status"] = "beta"
            missing_rows.append(row)

    if not missing_rows:
        return

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writerows(missing_rows)
    with TRACKER_PATH.open("ab") as file:
        if raw_tracker and not raw_tracker.endswith((b"\n", b"\r\n")):
            file.write(b"\n")
        file.write(buffer.getvalue().encode("utf-8"))


def main() -> int:
    units = expand_units()
    write_level_files(units)
    for unit in units:
        write_unit_and_lessons(unit)
    update_tracker(units)
    print("Generated Arabic C1 curriculum content.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
