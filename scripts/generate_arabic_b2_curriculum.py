#!/usr/bin/env python3
"""Generate Arabic B2 beta curriculum content.

B2 follows the English B2 professional-discussion scope while keeping the
Arabic A1-B1 authoring standard: formal Arabic, harakat on listening scripts,
Indonesian learner guidance, structured vocabulary, and audio manifests that
can be generated later.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

import yaml

from generate_arabic_vocabulary import vocabulary_for_lesson


REPO_ROOT = Path(__file__).resolve().parents[1]
B2_ROOT = REPO_ROOT / "content" / "curriculum" / "arabic" / "B2"
UNITS_ROOT = B2_ROOT / "units"
TRACKER_PATH = REPO_ROOT / "content" / "production_tracker.csv"
CONTENT_PLAN_PATH = B2_ROOT / "content_plan.yaml"

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
    "unit-01-clear-arguments": {
        "title": "Clear Arguments",
        "speakers": ("Ahmad", "Karim"),
        "outcome": "Present and support an argument clearly in formal Arabic conversation.",
        "situation": "Kamu menyampaikan pendapat dalam diskusi profesional dan perlu mendukungnya dengan alasan, contoh, serta respons terhadap keberatan.",
        "prompt": ("مَا مَوْقِفُكَ مِنْ هَذَا الْمَوْضُوعِ؟", "Apa posisimu tentang topik ini?"),
        "phrases": [
            ("مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", "Posisi saya adalah bahwa topik {focus_id} penting dalam diskusi.", "Menyatakan posisi dengan jelas."),
            ("أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", "Saya mendukung pendapat ini dengan dua alasan yang jelas.", "Memberi kerangka argumen."),
            ("مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", "Contohnya, tim membutuhkan keputusan yang cepat.", "Memberi contoh konkret."),
            ("أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", "Saya memahami poin lawannya, tetapi manfaatnya lebih besar.", "Merespons counterpoint dengan sopan."),
            ("لِذَلِكَ أُفَضِّلُ أَنْ نَتَّفِقَ عَلَى هَذَا الْمَسَارِ.", "Karena itu, saya lebih memilih kita sepakat pada arah ini.", "Menutup argumen dengan rekomendasi."),
        ],
        "grammar": "Gunakan مَوْقِفِي هُوَ، أَدْعَمُ، مِثَالُ ذَلِكَ، dan وَلَكِنَّ untuk membuat argumen B2 yang terstruktur.",
        "patterns": ["مَوْقِفِي هُوَ أَنَّ ...", "أَدْعَمُ هَذَا الرَّأْيَ بِـ ...", "مِثَالُ ذَلِكَ أَنَّ ...", "أَفْهَمُ ... وَلَكِنَّ ..."],
    },
    "unit-02-professional-meetings": {
        "title": "Professional Meetings",
        "speakers": ("Maryam", "Noura"),
        "outcome": "Participate actively and professionally in meetings.",
        "situation": "Kamu mengikuti rapat kerja dan perlu membuka poin, memperjelas cakupan, memberi masukan, serta merangkum keputusan.",
        "prompt": ("مَا النُّقْطَةُ الَّتِي تُرِيدِينَ مُنَاقَشَتَهَا؟", "Poin apa yang ingin kamu bahas?"),
        "phrases": [
            ("أُرِيدُ أَنْ أَبْدَأَ بِنُقْطَةٍ عَنْ {focus}.", "Saya ingin mulai dengan poin tentang {focus_id}.", "Membuka kontribusi rapat."),
            ("هَلْ نِطَاقُ النِّقَاشِ وَاضِحٌ لِلْجَمِيعِ؟", "Apakah cakupan diskusi jelas untuk semua orang?", "Memastikan scope."),
            ("عِنْدِي مُلَاحَظَةٌ بَنَّاءَةٌ عَلَى هَذَا الِاقْتِرَاحِ.", "Saya punya masukan konstruktif untuk usulan ini.", "Memberi feedback profesional."),
            ("الْقَرَارُ الْأَسَاسِيُّ هُوَ أَنْ نُكْمِلَ الْخُطْوَةَ التَّالِيَةَ.", "Keputusan utamanya adalah kita menyelesaikan langkah berikutnya.", "Merangkum keputusan."),
            ("سَأُرْسِلُ مُلَخَّصًا قَصِيرًا بَعْدَ الِاجْتِمَاعِ.", "Saya akan mengirim ringkasan singkat setelah rapat.", "Menutup dengan action item."),
        ],
        "grammar": "Gunakan أُرِيدُ أَنْ، هَلْ، عِنْدِي مُلَاحَظَةٌ، dan سَـ untuk meeting yang jelas dan profesional.",
        "patterns": ["أُرِيدُ أَنْ أَبْدَأَ بِـ ...", "هَلْ نِطَاقُ ... وَاضِحٌ؟", "عِنْدِي مُلَاحَظَةٌ ...", "سَأُرْسِلُ ... بَعْدَ ..."],
    },
    "unit-03-negotiation-and-compromise": {
        "title": "Negotiation & Compromise",
        "speakers": ("Khalid", "Omar"),
        "outcome": "Negotiate simple professional outcomes and find compromise.",
        "situation": "Kamu bernegosiasi tentang prioritas, proposal, keberatan, dan jalan tengah tanpa membuat percakapan terasa keras.",
        "prompt": ("مَا أَوْلَوِيَّتُكَ فِي هَذَا الِاتِّفَاقِ؟", "Apa prioritasmu dalam kesepakatan ini?"),
        "phrases": [
            ("أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى {focus} وَاضِحًا.", "Prioritas saya adalah agar {focus_id} tetap jelas.", "Menyatakan prioritas."),
            ("أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", "Saya mengajukan usulan berikut sebagai solusi praktis.", "Membuat proposal."),
            ("أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", "Saya memahami kekhawatiranmu, tetapi kita punya pilihan lain.", "Menangani objection."),
            ("يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", "Kita bisa mencapai solusi tengah.", "Mencari kompromi."),
            ("إِذَا اتَّفَقْنَا عَلَى ذَلِكَ، فَالْخُطْوَةُ التَّالِيَةُ وَاضِحَةٌ.", "Jika kita sepakat tentang itu, langkah berikutnya jelas.", "Menutup negosiasi."),
        ],
        "grammar": "Gunakan أَوْلَوِيَّتِي، أُقَدِّمُ، وَلَكِنْ، dan إِذَا untuk negosiasi yang sopan dan terarah.",
        "patterns": ["أَوْلَوِيَّتِي هِيَ أَنْ ...", "أُقَدِّمُ ... كَـ ...", "أَفْهَمُ ... وَلَكِنْ ...", "إِذَا اتَّفَقْنَا ... فَـ ..."],
    },
    "unit-04-presenting-ideas": {
        "title": "Presenting Ideas",
        "speakers": ("Salma", "Lina"),
        "outcome": "Present an idea and answer questions naturally.",
        "situation": "Kamu mempresentasikan ide singkat, memberi struktur, menjelaskan manfaat dan risiko, lalu menjawab pertanyaan.",
        "prompt": ("كَيْفَ سَتُقَدِّمِينَ هَذِهِ الْفِكْرَةَ؟", "Bagaimana kamu akan mempresentasikan ide ini?"),
        "phrases": [
            ("سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ {focus}.", "Saya akan mulai dengan pembuka singkat tentang {focus_id}.", "Membuka presentasi."),
            ("بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", "Setelah itu, saya akan menjelaskan manfaat utamanya.", "Memberi signposting."),
            ("مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", "Penting juga untuk menyebutkan risikonya.", "Menjelaskan risk secara seimbang."),
            ("إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", "Jika ada pertanyaan, saya akan menjawabnya dengan jelas.", "Menyiapkan Q&A."),
            ("فِي الْخِتَامِ، سَأَقْتَرِحُ خُطْوَةً عَمَلِيَّةً.", "Sebagai penutup, saya akan mengusulkan langkah praktis.", "Menutup presentasi."),
        ],
        "grammar": "Gunakan سَـ، بَعْدَ ذَلِكَ، مِنَ الْمُهِمِّ أَنْ، dan إِذَا untuk presentasi yang runtut.",
        "patterns": ["سَأَبْدَأُ بِـ ...", "بَعْدَ ذَلِكَ، سَأَشْرَحُ ...", "مِنَ الْمُهِمِّ أَنْ ...", "إِذَا كَانَتْ ... فَـ ..."],
    },
    "unit-05-media-and-information": {
        "title": "Media & Information",
        "speakers": ("Yusuf", "Hasan"),
        "outcome": "Discuss information, sources, and viewpoints critically.",
        "situation": "Kamu membahas artikel, sumber informasi, sudut pandang, dan perubahan pendapat berdasarkan informasi baru.",
        "prompt": ("كَيْفَ تُلَخِّصُ هَذِهِ الْمَعْلُومَاتِ؟", "Bagaimana kamu merangkum informasi ini?"),
        "phrases": [
            ("أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", "Saya memahami dari artikel bahwa topik {focus_id} penting.", "Merangkum artikel."),
            ("يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", "Kita harus memastikan bahwa sumbernya tepercaya.", "Mengevaluasi sumber."),
            ("وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", "Sudut pandang ini membutuhkan bukti yang lebih kuat.", "Menguji viewpoint."),
            ("بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", "Setelah informasi baru, pendapat saya sedikit berubah.", "Merespons informasi baru."),
            ("لِذَلِكَ أُفَضِّلُ أَنْ نُوَازِنَ بَيْنَ الْمَصَادِرِ.", "Karena itu, saya lebih memilih kita menyeimbangkan berbagai sumber.", "Menutup diskusi kritis."),
        ],
        "grammar": "Gunakan أَفْهَمُ مِنْ، يَجِبُ أَنْ، تَحْتَاجُ إِلَى، dan بَعْدَ untuk diskusi informasi yang kritis.",
        "patterns": ["أَفْهَمُ مِنَ ... أَنَّ ...", "يَجِبُ أَنْ نَتَأَكَّدَ مِنْ ...", "تَحْتَاجُ إِلَى ...", "بَعْدَ ... تَغَيَّرَ ..."],
    },
    "unit-06-customer-and-client-communication": {
        "title": "Customer & Client Communication",
        "speakers": ("Fatimah", "Aisha"),
        "outcome": "Handle client conversations with clarity, empathy, and professionalism.",
        "situation": "Kamu berbicara dengan klien, memahami kebutuhan, menjelaskan opsi, menangani kekhawatiran, dan mengonfirmasi langkah berikutnya.",
        "prompt": ("مَا الَّذِي يَحْتَاجُ إِلَيْهِ الْعَمِيلُ؟", "Apa yang dibutuhkan klien?"),
        "phrases": [
            ("أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ {focus}.", "Saya ingin memahami kebutuhan klien tentang {focus_id}.", "Memahami kebutuhan klien."),
            ("لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", "Kita punya dua opsi, dan setiap opsi memiliki manfaat.", "Menjelaskan opsi."),
            ("أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", "Saya memahami kekhawatiran ini, dan saya akan menjelaskan detailnya.", "Menangani concern."),
            ("الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", "Langkah berikutnya adalah meninjau kesepakatan.", "Mengonfirmasi next step."),
            ("سَأُرْسِلُ تَأْكِيدًا مَكْتُوبًا بَعْدَ هَذِهِ الْمُكَالَمَةِ.", "Saya akan mengirim konfirmasi tertulis setelah panggilan ini.", "Menutup dengan profesional."),
        ],
        "grammar": "Gunakan أُرِيدُ أَنْ أَفْهَمَ، لَدَيْنَا، أَفْهَمُ، dan سَأُرْسِلُ untuk komunikasi klien.",
        "patterns": ["أُرِيدُ أَنْ أَفْهَمَ ...", "لَدَيْنَا خِيَارَانِ ...", "أَفْهَمُ ... وَسَأُوَضِّحُ ...", "الْخُطْوَةُ التَّالِيَةُ هِيَ ..."],
    },
    "unit-07-complex-problem-solving": {
        "title": "Complex Problem Solving",
        "speakers": ("Rami", "Tariq"),
        "outcome": "Analyze a complex problem and discuss tradeoffs.",
        "situation": "Kamu menganalisis masalah yang lebih kompleks: framing, penyebab, tradeoff, solusi, dan rekomendasi.",
        "prompt": ("كَيْفَ نُحَدِّدُ هَذِهِ الْمُشْكِلَةَ؟", "Bagaimana kita mendefinisikan masalah ini?"),
        "phrases": [
            ("أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", "Saya melihat bahwa poin {focus_id} adalah bagian dari masalah yang lebih besar.", "Melakukan framing problem."),
            ("السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", "Penyebab utamanya mungkin lemahnya pengaturan.", "Menjelaskan cause."),
            ("لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", "Setiap solusi punya manfaat dan efek samping.", "Membahas tradeoff."),
            ("أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", "Saya merekomendasikan solusi bertahap untuk mengurangi risiko.", "Memberi rekomendasi."),
            ("بَعْدَ التَّجْرِبَةِ، نُقَيِّمُ النَّتِيجَةَ مَرَّةً أُخْرَى.", "Setelah percobaan, kita menilai hasilnya lagi.", "Menutup dengan evaluasi."),
        ],
        "grammar": "Gunakan أَرَى أَنَّ، قَدْ يَكُونُ، لِكُلِّ، dan أُوصِي بِـ untuk problem solving B2.",
        "patterns": ["أَرَى أَنَّ ... جُزْءٌ مِنْ ...", "السَّبَبُ ... قَدْ يَكُونُ ...", "لِكُلِّ حَلٍّ ...", "أُوصِي بِـ ..."],
    },
    "unit-08-b2-review-final": {
        "title": "B2 Review & Final Discussion",
        "speakers": ("Layla", "Noura"),
        "outcome": "Use B2 discussion skills in professional and social contexts.",
        "situation": "Kamu menggabungkan argumen, meeting, negosiasi, presentasi, informasi, klien, dan problem solving dalam final discussion.",
        "prompt": ("مَا أَهَمُّ مَهَارَةٍ تُرَاجِعِينَها الْآنَ؟", "Skill terpenting apa yang sedang kamu review sekarang?"),
        "phrases": [
            ("أُرَاجِعُ مَهَارَةَ {focus} لِأَنَّهَا مُهِمَّةٌ فِي النِّقَاشِ.", "Saya mengulang skill {focus_id} karena itu penting dalam diskusi.", "Membuka review."),
            ("أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", "Saya bisa menyampaikan pendapat dan mendukungnya dengan bukti.", "Mereview argument skill."),
            ("أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", "Saya juga bisa mengelola percakapan profesional dengan jelas.", "Mereview professional skill."),
            ("إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", "Jika muncul keberatan, saya akan menanggapinya dengan tenang.", "Mereview counterpoint skill."),
            ("فِي الِاخْتِبَارِ النِّهَائِيِّ، سَأُرَكِّزُ عَلَى التَّرَابُطِ وَالْوُضُوحِ.", "Dalam tes akhir, saya akan fokus pada koherensi dan kejelasan.", "Menutup dengan strategy."),
        ],
        "grammar": "Gabungkan أَسْتَطِيعُ أَنْ، إِذَا، فَـ، dan لِأَنَّ untuk final discussion yang koheren.",
        "patterns": ["أُرَاجِعُ ... لِأَنَّ ...", "أَسْتَطِيعُ أَنْ ...", "إِذَا ظَهَرَ ... فَـ ...", "سَأُرَكِّزُ عَلَى ..."],
    },
}


LESSONS_BY_UNIT: dict[str, list[tuple[str, str, str, str, str]]] = {
    "unit-01-clear-arguments": [
        ("lesson-01-stating-your-position", "arabic-b2-stating-your-position", "Stating Your Position", "تَحْدِيدُ الْمَوْقِفِ", "menentukan posisi"),
        ("lesson-02-supporting-with-reasons", "arabic-b2-supporting-with-reasons", "Supporting With Reasons", "دَعْمُ الرَّأْيِ بِالْأَسْبَابِ", "mendukung pendapat dengan alasan"),
        ("lesson-03-using-examples", "arabic-b2-using-examples", "Using Examples", "اِسْتِخْدَامُ الْأَمْثِلَةِ", "menggunakan contoh"),
        ("lesson-04-responding-to-counterpoints", "arabic-b2-responding-to-counterpoints", "Responding to Counterpoints", "الرَّدُّ عَلَى الِاعْتِرَاضِ", "menanggapi keberatan"),
        ("lesson-05-clear-argument-mission", "arabic-b2-clear-argument-mission", "Clear Argument Mission", "بِنَاءُ حُجَّةٍ وَاضِحَةٍ", "membangun argumen jelas"),
    ],
    "unit-02-professional-meetings": [
        ("lesson-01-opening-a-meeting-point", "arabic-b2-opening-a-meeting-point", "Opening a Meeting Point", "فَتْحُ نُقْطَةٍ فِي الِاجْتِمَاعِ", "membuka poin rapat"),
        ("lesson-02-clarifying-scope", "arabic-b2-clarifying-scope", "Clarifying Scope", "تَوْضِيحُ نِطَاقِ النِّقَاشِ", "memperjelas scope diskusi"),
        ("lesson-03-giving-constructive-feedback", "arabic-b2-giving-constructive-feedback", "Giving Constructive Feedback", "تَقْدِيمُ مُلَاحَظَةٍ بَنَّاءَةٍ", "memberi masukan konstruktif"),
        ("lesson-04-summarizing-decisions", "arabic-b2-summarizing-decisions", "Summarizing Decisions", "تَلْخِيصُ الْقَرَارَاتِ", "merangkum keputusan"),
        ("lesson-05-meeting-participation-mission", "arabic-b2-meeting-participation-mission", "Meeting Participation Mission", "الْمُشَارَكَةُ فِي اِجْتِمَاعٍ مِهَنِيٍّ", "berpartisipasi dalam rapat profesional"),
    ],
    "unit-03-negotiation-and-compromise": [
        ("lesson-01-expressing-priorities", "arabic-b2-expressing-priorities", "Expressing Priorities", "تَوْضِيحُ الْأَوْلَوِيَّاتِ", "menjelaskan prioritas"),
        ("lesson-02-making-a-proposal", "arabic-b2-making-a-proposal", "Making a Proposal", "تَقْدِيمُ اِقْتِرَاحٍ عَمَلِيٍّ", "mengajukan usulan praktis"),
        ("lesson-03-handling-objections", "arabic-b2-handling-objections", "Handling Objections", "التَّعَامُلُ مَعَ الِاعْتِرَاضَاتِ", "menangani keberatan"),
        ("lesson-04-finding-middle-ground", "arabic-b2-finding-middle-ground", "Finding Middle Ground", "الْوُصُولُ إِلَى حَلٍّ وَسَطٍ", "mencari jalan tengah"),
        ("lesson-05-negotiation-mission", "arabic-b2-negotiation-mission", "Negotiation Mission", "إِدَارَةُ تَفَاوُضٍ وَاضِحٍ", "mengelola negosiasi jelas"),
    ],
    "unit-04-presenting-ideas": [
        ("lesson-01-structuring-a-short-presentation", "arabic-b2-structuring-a-short-presentation", "Structuring a Short Presentation", "تَنْظِيمُ عَرْضٍ قَصِيرٍ", "menyusun presentasi singkat"),
        ("lesson-02-signposting-clearly", "arabic-b2-signposting-clearly", "Signposting Clearly", "تَوْضِيحُ الِانْتِقَالَاتِ", "memberi transisi jelas"),
        ("lesson-03-explaining-benefits-and-risks", "arabic-b2-explaining-benefits-and-risks", "Explaining Benefits and Risks", "شَرْحُ الْفَوَائِدِ وَالْمَخَاطِرِ", "menjelaskan manfaat dan risiko"),
        ("lesson-04-answering-questions", "arabic-b2-answering-questions", "Answering Questions", "الْإِجَابَةُ عَنِ الْأَسْئِلَةِ", "menjawab pertanyaan"),
        ("lesson-05-idea-presentation-mission", "arabic-b2-idea-presentation-mission", "Idea Presentation Mission", "تَقْدِيمُ فِكْرَةٍ وَالدِّفَاعُ عَنْهَا", "mempresentasikan dan mempertahankan ide"),
    ],
    "unit-05-media-and-information": [
        ("lesson-01-summarizing-an-article", "arabic-b2-summarizing-an-article", "Summarizing an Article", "تَلْخِيصُ مَقَالٍ", "merangkum artikel"),
        ("lesson-02-discussing-reliable-sources", "arabic-b2-discussing-reliable-sources", "Discussing Reliable Sources", "مُنَاقَشَةُ الْمَصَادِرِ الْمَوْثُوقَةِ", "membahas sumber tepercaya"),
        ("lesson-03-explaining-a-viewpoint", "arabic-b2-explaining-a-viewpoint", "Explaining a Viewpoint", "شَرْحُ وِجْهَةِ نَظَرٍ", "menjelaskan sudut pandang"),
        ("lesson-04-responding-to-new-information", "arabic-b2-responding-to-new-information", "Responding to New Information", "الرَّدُّ عَلَى مَعْلُومَاتٍ جَدِيدَةٍ", "menanggapi informasi baru"),
        ("lesson-05-information-discussion-mission", "arabic-b2-information-discussion-mission", "Information Discussion Mission", "إِدَارَةُ نِقَاشٍ عَنِ الْمَعْلُومَاتِ", "mengelola diskusi informasi"),
    ],
    "unit-06-customer-and-client-communication": [
        ("lesson-01-understanding-client-needs", "arabic-b2-understanding-client-needs", "Understanding Client Needs", "فَهْمُ اِحْتِيَاجِ الْعَمِيلِ", "memahami kebutuhan klien"),
        ("lesson-02-explaining-options", "arabic-b2-explaining-options", "Explaining Options", "شَرْحُ الْخِيَارَاتِ", "menjelaskan opsi"),
        ("lesson-03-handling-concerns", "arabic-b2-handling-concerns", "Handling Concerns", "التَّعَامُلُ مَعَ اهْتِمَامَاتِ الْعَمِيلِ", "menangani concern klien"),
        ("lesson-04-confirming-next-steps", "arabic-b2-confirming-next-steps", "Confirming Next Steps", "تَأْكِيدُ الْخُطْوَاتِ التَّالِيَةِ", "mengonfirmasi langkah berikutnya"),
        ("lesson-05-client-conversation-mission", "arabic-b2-client-conversation-mission", "Client Conversation Mission", "إِدَارَةُ حِوَارٍ مَعَ عَمِيلٍ", "mengelola percakapan dengan klien"),
    ],
    "unit-07-complex-problem-solving": [
        ("lesson-01-framing-the-problem", "arabic-b2-framing-the-problem", "Framing the Problem", "تَحْدِيدُ إِطَارِ الْمُشْكِلَةِ", "membingkai masalah"),
        ("lesson-02-explaining-causes", "arabic-b2-explaining-causes", "Explaining Causes", "شَرْحُ الْأَسْبَابِ", "menjelaskan penyebab"),
        ("lesson-03-discussing-tradeoffs", "arabic-b2-discussing-tradeoffs", "Discussing Tradeoffs", "مُنَاقَشَةُ الْمُوَازَنَاتِ", "membahas tradeoff"),
        ("lesson-04-recommending-a-solution", "arabic-b2-recommending-a-solution", "Recommending a Solution", "تَقْدِيمُ تَوْصِيَةٍ بِحَلٍّ", "merekomendasikan solusi"),
        ("lesson-05-problem-solving-discussion-mission", "arabic-b2-problem-solving-discussion-mission", "Problem Solving Discussion Mission", "نِقَاشُ حَلِّ مُشْكِلَةٍ مُعَقَّدَةٍ", "mendiskusikan solusi masalah kompleks"),
    ],
    "unit-08-b2-review-final": [
        ("lesson-01-review-arguments-and-meetings", "arabic-b2-review-arguments-and-meetings", "Review Arguments and Meetings", "مُرَاجَعَةُ الْحُجَجِ وَالِاجْتِمَاعَاتِ", "review argumen dan rapat"),
        ("lesson-02-review-negotiation-and-presenting", "arabic-b2-review-negotiation-and-presenting", "Review Negotiation and Presenting", "مُرَاجَعَةُ التَّفَاوُضِ وَالْعَرْضِ", "review negosiasi dan presentasi"),
        ("lesson-03-review-information-and-clients", "arabic-b2-review-information-and-clients", "Review Information and Clients", "مُرَاجَعَةُ الْمَعْلُومَاتِ وَالْعُمَلَاءِ", "review informasi dan klien"),
        ("lesson-04-b2-final-test-practice", "arabic-b2-b2-final-test-practice", "B2 Final Test Practice", "تَدْرِيبُ الِاخْتِبَارِ النِّهَائِيِّ", "latihan tes akhir"),
        ("lesson-05-b2-final-discussion", "arabic-b2-b2-final-discussion", "B2 Final Discussion", "النِّقَاشُ النِّهَائِيُّ", "diskusi akhir"),
    ],
}


def build_lesson(unit_key: str, lesson_data: tuple[str, str, str, str, str]) -> dict[str, Any]:
    profile = UNIT_PROFILES[unit_key]
    lesson_key, slug, title, focus, focus_id = lesson_data
    phrases = [
        phrase(text.format(focus=focus, focus_id=focus_id), meaning.format(focus_id=focus_id), usage)
        for text, meaning, usage in profile["phrases"]
    ]
    speaker_a, speaker_b = profile["speakers"]
    prompt_ar, prompt_id = profile["prompt"]
    prompt_ar = f"{prompt_ar} أُرِيدُ أَنْ أُرَكِّزَ عَلَى {focus}."
    prompt_id = f"{prompt_id} Saya ingin fokus pada {focus_id}."
    dialogue = [
        line(speaker_a, prompt_ar, prompt_id),
        line(speaker_b, phrases[0]["phrase"], phrases[0]["meaning"]),
        line(speaker_a, "مَا الدَّلِيلُ أَوِ الْمِثَالُ الَّذِي يُوَضِّحُ ذَلِكَ؟", "Apa bukti atau contoh yang menjelaskan itu?"),
        line(speaker_b, f"{phrases[1]['phrase']} {phrases[2]['phrase']}", f"{phrases[1]['meaning']} {phrases[2]['meaning']}"),
        line(speaker_a, "هَذَا وَاضِحٌ، وَلَكِنْ مَا النُّقْطَةُ الْمُعَارِضَةُ الْمُمْكِنَةُ؟", "Itu jelas, tetapi apa counterpoint yang mungkin muncul?"),
        line(speaker_b, phrases[3]["phrase"], phrases[3]["meaning"]),
        line(speaker_a, "مَا التَّوْصِيَةُ النِّهَائِيَّةُ إِذَنْ؟", "Jadi apa rekomendasi akhirnya?"),
        line(speaker_b, phrases[4]["phrase"], phrases[4]["meaning"]),
    ]
    return {
        "lesson_key": lesson_key,
        "slug": slug,
        "title": title,
        "status": "beta",
        "focus": focus,
        "focus_id": focus_id,
        "situation": profile["situation"],
        "goal": f"Latih percakapan Arab B2 untuk {focus_id} dengan alasan, contoh, respons, dan rekomendasi.",
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
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def write_level_files(units: list[dict[str, Any]]) -> None:
    B2_ROOT.mkdir(parents=True, exist_ok=True)
    (B2_ROOT / "LEVEL_SPEC.md").write_text(
        "# Arabic B2 - Professional Discussions\n\n"
        "## Level Outcome\n\n"
        "Learners can participate in structured professional and social discussions: "
        "state a position, support it with reasons and examples, respond to objections, "
        "take part in meetings, negotiate compromises, present ideas, evaluate sources, "
        "communicate with clients, and recommend solutions in clear formal Arabic.\n\n"
        "## Scope\n\n"
        "- Formal Arabic / Modern Standard Arabic, not dialect.\n"
        "- Indonesian explanations for adult learners.\n"
        "- Arabic script with harakat for learner-facing examples and listening scripts.\n"
        "- Discussion-first lessons with explicit argument, meeting, and problem-solving patterns.\n"
        "- Speaker labels are metadata and must not be spoken in generated audio.\n"
        "- No religious source text or devotional TTS content.\n\n"
        "## B2 Upgrade From B1\n\n"
        "- Dialogue length: 8 connected turns.\n"
        "- Learner responses include position, reason, example, counterpoint response, and recommendation.\n"
        "- Introduce professional discussion, negotiation, presentation, source evaluation, and tradeoffs.\n"
        "- Keep grammar functional and conversation-first.\n\n"
        "## Passing Threshold\n\n"
        "- Overall score: 78\n"
        "- Speaking / Conversation: 72\n"
        "- Listening: 70\n"
        "- Pronunciation: 64\n"
        "- Vocabulary / Useful Phrases: 70\n"
        "- Grammar: 70\n"
        "- Reading: 65\n"
        "- Writing: 65\n"
        "- Lesson completion: 85%\n",
        encoding="utf-8",
    )

    write_yaml(
        CONTENT_PLAN_PATH,
        {
            "language": "arabic",
            "language_code": "ar",
            "level_code": "B2",
            "course_slug": "arabic-b2-professional-discussions",
            "course_title": "Arabic Professional Discussions",
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
                        {
                            "lesson_key": item["lesson_key"],
                            "slug": item["slug"],
                            "title": item["title"],
                            "status": item["status"],
                        }
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
        "level_code": "B2",
        "opening_line": item["dialogue"][0][1],
        "learner_goal": item["goal"],
        "max_turns": 8,
        "feedback_level": {"free": "basic", "pro": "detailed"},
        "turns": [
            {
                "coach": item["dialogue"][0][1] if index == 1 else f"استخدم الفكرة: {entry['phrase']}",
                "hint": f"Jawab dengan struktur B2 memakai: {entry['phrase']}",
                "sample_answer": entry["phrase"],
                "focus": entry["usage"],
                "expected_keywords": entry["phrase"].replace("؟", "").replace(".", "").split()[:5],
                "indonesian_explanation": entry["meaning"],
            }
            for index, entry in enumerate(item["phrases"][:4], 1)
        ],
        "target_phrases": [entry["phrase"] for entry in item["phrases"][:5]],
        "rubric": {
            "speaking": {"minimum_score": 72},
            "relevance": {"minimum_score": 72},
            "argument_structure": {"minimum_score": 70},
            "grammar": {"minimum_score": 70},
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
            "level_code": "B2",
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
                "estimated_minutes": 16,
                "conversation_situation": item["slug"].replace("arabic-b2-", "").replace("-", "_"),
                "conversation_goal": item["goal"],
                "grammar_summary": item["grammar"],
                "required_sections": REQUIRED_SECTIONS,
                "completion_rules": {
                    "listening_completed": True,
                    "quiz_required": True,
                    "speaking_attempt_required": True,
                    "minimum_score": 72,
                },
            },
        )

        (lesson_dir / "lesson.md").write_text(
            f"# {item['title']}\n\n"
            "Setelah lesson ini, kamu bisa membangun diskusi Arab B2 yang lebih matang: "
            "posisi, alasan, contoh, respons terhadap keberatan, dan rekomendasi akhir.\n\n"
            "## Situation\n\n"
            f"{item['situation']}\n\n"
            "## Catatan Belajar\n\n"
            "Di B2, jawaban tidak hanya benar secara frasa. Jawaban harus punya struktur: "
            "opening yang jelas, alasan, contoh, respons sopan, dan penutup yang bisa ditindaklanjuti.\n",
            encoding="utf-8",
        )

        (lesson_dir / "conversation_goal.md").write_text(
            f"# Target Percakapan\n\n{item['goal']}\n\n"
            "Kamu akan berlatih mengatakan:\n\n"
            + "\n".join(f"- {entry['phrase']}" for entry in item["phrases"][:5])
            + "\n",
            encoding="utf-8",
        )

        (lesson_dir / "listening_script.md").write_text(
            "# Listening Script\n\n"
            + "\n".join(f"**{speaker}:** {text}" for speaker, text, _ in item["dialogue"])
            + "\n\n## Audio Direction\n\n"
            "Use Arabic only. Speaker labels are metadata and must not be spoken. "
            "Keep a measured B2 discussion pace with a short natural pause between speakers. "
            "Use distinct voices according to speaker names and gender.\n",
            encoding="utf-8",
        )

        (lesson_dir / "transcript_translation.md").write_text(
            "# Transcript Translation\n\n"
            + "\n".join(
                f"- **{speaker}:** {text} -> {translation}"
                for speaker, text, translation in item["dialogue"]
            )
            + "\n",
            encoding="utf-8",
        )

        write_yaml(
            lesson_dir / "useful_phrases.yaml",
            {
                "phrases": [
                    {"phrase": entry["phrase"], "meaning_id": entry["meaning"], "usage_note": entry["usage"]}
                    for entry in item["phrases"]
                ]
            },
        )
        write_yaml(lesson_dir / "vocabulary.yaml", {"vocabulary": vocabulary_for_lesson(item["phrases"], item["dialogue"])})

        (lesson_dir / "grammar_for_conversation.md").write_text(
            "# Pola Percakapan\n\n"
            f"{item['grammar']}\n\n"
            "```txt\n"
            + "\n".join(item["patterns"])
            + "\n```\n\n"
            "Pakai pola ini untuk menjaga jawaban tetap koheren. Jika respons terasa panjang, "
            "pisahkan menjadi dua kalimat tetapi tetap jaga hubungan logisnya.\n",
            encoding="utf-8",
        )

        (lesson_dir / "pronunciation_drill.md").write_text(
            "# Latihan Pengucapan\n\n## Ulangi\n\n"
            + "\n".join(f"{index}. {entry['phrase']}" for index, entry in enumerate(item["phrases"][:5], 1))
            + "\n\n## Fokus\n\n"
            "- Jaga tekanan pada frasa penghubung seperti وَلَكِنَّ، لِذَلِكَ، dan إِذَا.\n"
            "- Beri jeda sebelum alasan, contoh, dan rekomendasi.\n"
            "- Jangan membaca seluruh argumen sebagai satu kalimat panjang.\n",
            encoding="utf-8",
        )

        write_yaml(
            lesson_dir / "response_prompts.yaml",
            {
                "prompts": [
                    {
                        "prompt": f"Ucapkan dalam bahasa Arab: {entry['meaning']}",
                        "target_response": entry["phrase"],
                        "acceptable_responses": [entry["phrase"]],
                    }
                    for entry in item["phrases"][:4]
                ]
            },
        )

        write_yaml(
            lesson_dir / "quiz.yaml",
            {
                "questions": [
                    {
                        "key": f"phrase_{index}",
                        "prompt": f"Frasa mana yang berarti \"{entry['meaning']}\"?",
                        "options": phrase_options(item["phrases"], index - 1),
                        "correct_answer": entry["phrase"],
                    }
                    for index, entry in enumerate(item["phrases"][:2], 1)
                ]
            },
        )
        write_yaml(lesson_dir / "conversation_coach_roleplay.yaml", roleplay_payload(item))

        (lesson_dir / "reading_support.md").write_text(
            "# Bantuan Membaca\n\n"
            "Baca dialog sebagai rangkaian argumen. Cari posisi utama, alasan, contoh, "
            "respons terhadap keberatan, lalu rekomendasi akhir.\n\n"
            + "\n".join(f"- {entry['phrase']} -> {entry['meaning']}" for entry in item["phrases"][:5])
            + "\n",
            encoding="utf-8",
        )

        (lesson_dir / "writing_support.md").write_text(
            "# Bantuan Menulis\n\n"
            "Tulis jawaban B2 dalam lima bagian pendek: posisi, alasan, contoh, respons "
            "terhadap kemungkinan keberatan, dan rekomendasi. Gunakan kerangka berikut.\n\n"
            + "\n".join(f"- {entry['phrase']}" for entry in item["phrases"][:5])
            + "\n",
            encoding="utf-8",
        )

        write_yaml(
            lesson_dir / "audio_manifest.yaml",
            {
                "lesson_key": item["lesson_key"],
                "status": "not_generated",
                "provider": "elevenlabs",
                "model": "eleven_v3",
                "default_voice_id": "multi_speaker",
                "assets": [],
            },
        )


def update_tracker(units: list[dict[str, Any]]) -> None:
    raw_tracker = TRACKER_PATH.read_bytes()
    reader = csv.DictReader(io.StringIO(raw_tracker.decode("utf-8")))
    fieldnames = reader.fieldnames or []
    existing = {(row["level"], row["unit"], row["lesson"]) for row in reader}

    missing_rows: list[dict[str, str]] = []
    for unit in units:
        for item in unit["lessons"]:
            key = ("arabic/B2", unit["unit_key"], item["lesson_key"])
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
    print("Generated Arabic B2 curriculum content.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
