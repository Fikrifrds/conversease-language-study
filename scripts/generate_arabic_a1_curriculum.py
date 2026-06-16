#!/usr/bin/env python3
"""Generate the Arabic A1 beta curriculum.

This is intentionally deterministic: the authored lesson specs below expand
into the same file layout used by the English curriculum and the Arabic pilot.
Run it after editing the Arabic A1 outline.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
A1_ROOT = REPO_ROOT / "content" / "curriculum" / "arabic" / "A1"
UNITS_ROOT = A1_ROOT / "units"
TRACKER_PATH = REPO_ROOT / "content" / "production_tracker.csv"

REQUIRED_SECTIONS = [
    "conversation_goal",
    "situation_setup",
    "listening",
    "comprehension_check",
    "useful_phrases",
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


def lesson(
    key: str,
    slug: str,
    title: str,
    situation: str,
    goal: str,
    grammar: str,
    patterns: list[str],
    phrases: list[dict[str, str]],
    dialogue: list[tuple[str, str, str]],
) -> dict[str, Any]:
    return {
        "lesson_key": key,
        "slug": slug,
        "title": title,
        "status": "beta",
        "situation": situation,
        "goal": goal,
        "grammar": grammar,
        "patterns": patterns,
        "phrases": phrases,
        "dialogue": dialogue,
    }


UNIT_PLANS: list[dict[str, Any]] = [
    {
        "unit_key": "unit-01-fusha-foundations",
        "title": "Arabic Foundations",
        "status": "beta",
        "main_conversation_outcome": "Start a simple formal Arabic conversation, follow basic study instructions, and ask for repetition when you do not understand.",
        "lessons": [
            {
                "lesson_key": "lesson-01-greetings-and-salam",
                "slug": "arabic-formal-greetings",
                "title": "Formal Greetings",
                "status": "beta",
            },
            {
                "lesson_key": "lesson-02-name-and-origin",
                "slug": "arabic-name-and-origin",
                "title": "Name and Origin",
                "status": "beta",
            },
            {
                "lesson_key": "lesson-03-class-and-study-instructions",
                "slug": "arabic-class-and-study-instructions",
                "title": "Class and Study Instructions",
                "status": "beta",
            },
            {
                "lesson_key": "lesson-04-asking-when-you-do-not-understand",
                "slug": "arabic-asking-when-you-do-not-understand",
                "title": "Asking When You Do Not Understand",
                "status": "beta",
            },
            {
                "lesson_key": "lesson-05-fusha-introduction-mission",
                "slug": "arabic-fusha-introduction-mission",
                "title": "Arabic Introduction Mission",
                "status": "beta",
            },
        ],
    },
    {
        "unit_key": "unit-02-letters-numbers-contact",
        "title": "Letters, Numbers & Contact",
        "status": "beta",
        "main_conversation_outcome": "Spell simple names, exchange numbers, and share basic contact details in Arabic.",
        "lessons": [
            lesson(
                "lesson-01-spelling-your-name",
                "arabic-spelling-your-name",
                "Spelling Your Name",
                "Kamu mengisi formulir kelas. Guru meminta kamu mengeja nama dengan huruf Arab sederhana.",
                "Spell a short name in Arabic and ask whether the spelling is correct.",
                "Use أكتب اسمي + name to say how you write your name, and هل هذا صحيح؟ to check.",
                ["أكتب اسمي: ...", "هذا حرف ...", "هل هذا صحيح؟"],
                [
                    phrase("كيف تكتب اسمك؟", "Bagaimana kamu menulis namamu?", "Ask someone to spell or write a name."),
                    phrase("أكتب اسمي ...", "Saya menulis nama saya ...", "Say how you write your name."),
                    phrase("هذا حرف ...", "Ini huruf ...", "Identify one Arabic letter."),
                    phrase("هل هذا صحيح؟", "Apakah ini benar?", "Check spelling politely."),
                ],
                [
                    line("Muallim", "كيف تكتب اسمك؟", "Bagaimana kamu menulis namamu?"),
                    line("Ahmad", "أكتب اسمي: أحمد.", "Saya menulis nama saya: Ahmad."),
                    line("Muallim", "هذا حرف الألف، وهذا حرف الحاء.", "Ini huruf alif, dan ini huruf ha."),
                    line("Ahmad", "هل هذا صحيح؟", "Apakah ini benar?"),
                    line("Muallim", "نعم، هذا صحيح.", "Ya, ini benar."),
                ],
            ),
            lesson(
                "lesson-02-arabic-numbers-and-phone",
                "arabic-numbers-and-phone",
                "Arabic Numbers and Phone",
                "Kamu bertukar nomor telepon dengan teman kelas. Kamu perlu mengucapkan angka pelan dan jelas.",
                "Say a simple phone number and ask someone to repeat it.",
                "Use رقمي + number for 'my number is' and أعد الرقم من فضلك for repetition.",
                ["رقمي ...", "أعد الرقم من فضلك.", "الرقم صحيح."],
                [
                    phrase("ما رقم هاتفك؟", "Berapa nomor teleponmu?", "Ask for a phone number."),
                    phrase("رقمي ...", "Nomor saya ...", "Say your number."),
                    phrase("واحد، اثنان، ثلاثة", "Satu, dua, tiga", "Start counting clearly."),
                    phrase("أعد الرقم من فضلك", "Ulangi nomornya, tolong.", "Ask for repetition."),
                    phrase("الرقم صحيح", "Nomornya benar.", "Confirm the number."),
                ],
                [
                    line("Maryam", "ما رقم هاتفك؟", "Berapa nomor teleponmu?"),
                    line("Khalid", "رقمي واحد، اثنان، ثلاثة، أربعة.", "Nomor saya satu, dua, tiga, empat."),
                    line("Maryam", "أعد الرقم من فضلك.", "Ulangi nomornya, tolong."),
                    line("Khalid", "واحد، اثنان، ثلاثة، أربعة.", "Satu, dua, tiga, empat."),
                    line("Maryam", "نعم، الرقم صحيح.", "Ya, nomornya benar."),
                ],
            ),
            lesson(
                "lesson-03-sharing-email-addresses",
                "arabic-sharing-email-addresses",
                "Sharing Email Addresses",
                "Kamu menulis email di daftar kelas. Kamu perlu menyebutkan bagian email dengan pelan.",
                "Share a simple email address and ask someone to write it.",
                "Use بريدي الإلكتروني + address, and اكتب to ask someone to write.",
                ["بريدي الإلكتروني ...", "اكتب من فضلك.", "نقطة", "شرطة"],
                [
                    phrase("ما بريدك الإلكتروني؟", "Apa alamat emailmu?", "Ask for an email address."),
                    phrase("بريدي الإلكتروني ...", "Email saya ...", "Share your email."),
                    phrase("اكتب من فضلك", "Tulis, tolong.", "Ask someone to write it."),
                    phrase("نقطة", "Titik", "Say dot in an address."),
                    phrase("شرطة", "Tanda hubung", "Say dash in an address."),
                ],
                [
                    line("Noura", "ما بريدك الإلكتروني؟", "Apa alamat emailmu?"),
                    line("Ahmad", "بريدي الإلكتروني أحمد نقطة واحد.", "Email saya Ahmad titik satu."),
                    line("Noura", "اكتب من فضلك.", "Tulis, tolong."),
                    line("Ahmad", "أحمد نقطة واحد.", "Ahmad titik satu."),
                    line("Noura", "شكرًا، هذا واضح.", "Terima kasih, ini jelas."),
                ],
            ),
            lesson(
                "lesson-04-asking-to-repeat-a-letter",
                "arabic-asking-to-repeat-a-letter",
                "Asking to Repeat a Letter",
                "Saat mendengar nama atau email, kamu tidak yakin satu huruf. Kamu meminta pengulangan dengan sopan.",
                "Ask someone to repeat a letter slowly and confirm what you heard.",
                "Use لم أسمع + object and هل قلت ...؟ to confirm a heard word or letter.",
                ["لم أسمع الحرف.", "ببطء من فضلك.", "هل قلت ...؟"],
                [
                    phrase("لم أسمع الحرف", "Saya tidak mendengar hurufnya.", "Explain what you missed."),
                    phrase("ببطء من فضلك", "Pelan-pelan, tolong.", "Ask for slower speech."),
                    phrase("هل قلت باء؟", "Apakah Anda mengatakan ba?", "Confirm one letter."),
                    phrase("نعم، قلت باء", "Ya, saya mengatakan ba.", "Confirm clearly."),
                ],
                [
                    line("Layla", "لم أسمع الحرف.", "Saya tidak mendengar hurufnya."),
                    line("Zayd", "الحرف باء.", "Hurufnya ba."),
                    line("Layla", "ببطء من فضلك.", "Pelan-pelan, tolong."),
                    line("Zayd", "باء.", "Ba."),
                    line("Layla", "هل قلت باء؟", "Apakah Anda mengatakan ba?"),
                    line("Zayd", "نعم، قلت باء.", "Ya, saya mengatakan ba."),
                ],
            ),
            lesson(
                "lesson-05-contact-details-mission",
                "arabic-contact-details-mission",
                "Contact Details Mission",
                "Kamu memperkenalkan diri di kelas baru dan memberikan informasi kontak sederhana.",
                "Combine name, spelling, number, and email in one short formal exchange.",
                "Combine اسمي, أكتب اسمي, رقمي, and بريدي الإلكتروني in one conversation.",
                ["اسمي ...", "أكتب اسمي ...", "رقمي ...", "بريدي الإلكتروني ..."],
                [
                    phrase("اسمي ...", "Nama saya ...", "Start your contact details."),
                    phrase("أكتب اسمي ...", "Saya menulis nama saya ...", "Spell your name."),
                    phrase("رقمي ...", "Nomor saya ...", "Give your number."),
                    phrase("بريدي الإلكتروني ...", "Email saya ...", "Give your email."),
                    phrase("هل هذا واضح؟", "Apakah ini jelas?", "Check understanding."),
                ],
                [
                    line("Muallimah", "ما اسمك؟", "Siapa namamu?"),
                    line("Ahmad", "اسمي أحمد.", "Nama saya Ahmad."),
                    line("Muallimah", "كيف تكتب اسمك؟", "Bagaimana kamu menulis namamu?"),
                    line("Ahmad", "أكتب اسمي: أحمد.", "Saya menulis nama saya: Ahmad."),
                    line("Muallimah", "ما رقم هاتفك؟", "Berapa nomor teleponmu?"),
                    line("Ahmad", "رقمي واحد، اثنان، ثلاثة، أربعة.", "Nomor saya satu, dua, tiga, empat."),
                    line("Muallimah", "هل هذا واضح؟", "Apakah ini jelas?"),
                    line("Ahmad", "نعم، واضح.", "Ya, jelas."),
                ],
            ),
        ],
    },
    {
        "unit_key": "unit-03-time-and-routine",
        "title": "Time & Daily Routine",
        "status": "beta",
        "main_conversation_outcome": "Talk about simple time, days, schedules, and daily activities in Arabic.",
        "lessons": [
            lesson(
                "lesson-01-asking-the-time",
                "arabic-asking-the-time",
                "Asking the Time",
                "Kamu menunggu kelas dimulai dan ingin tahu jam sekarang.",
                "Ask the time and answer with a simple hour.",
                "Use الساعة + number for 'it is ... o'clock' and صباحًا/مساءً for morning/evening.",
                ["كم الساعة؟", "الساعة ...", "صباحًا", "مساءً"],
                [
                    phrase("كم الساعة؟", "Jam berapa?", "Ask the time."),
                    phrase("الساعة الثامنة", "Jam delapan.", "Answer with an hour."),
                    phrase("الآن", "Sekarang", "Refer to the current time."),
                    phrase("صباحًا", "Pagi", "Clarify morning time."),
                    phrase("مساءً", "Sore/malam", "Clarify evening time."),
                ],
                [
                    line("Khalid", "كم الساعة الآن؟", "Jam berapa sekarang?"),
                    line("Maryam", "الساعة الثامنة صباحًا.", "Jam delapan pagi."),
                    line("Khalid", "متى الدرس؟", "Kapan pelajarannya?"),
                    line("Maryam", "الدرس الساعة التاسعة.", "Pelajarannya jam sembilan."),
                    line("Khalid", "شكرًا.", "Terima kasih."),
                ],
            ),
            lesson(
                "lesson-02-days-of-the-week",
                "arabic-days-of-the-week",
                "Days of the Week",
                "Kamu melihat jadwal kelas dan perlu menyebut hari ini serta hari berikutnya.",
                "Say today, tomorrow, and a simple class day.",
                "Use اليوم + day and غدًا + day to speak about today and tomorrow.",
                ["اليوم ...", "غدًا ...", "عندي درس ..."],
                [
                    phrase("أي يوم اليوم؟", "Hari apa hari ini?", "Ask today's day."),
                    phrase("اليوم الإثنين", "Hari ini Senin.", "Say today's day."),
                    phrase("غدًا الثلاثاء", "Besok Selasa.", "Say tomorrow's day."),
                    phrase("عندي درس", "Saya punya pelajaran.", "Talk about a scheduled lesson."),
                    phrase("في يوم ...", "Pada hari ...", "Name a day for an event."),
                ],
                [
                    line("Noura", "أي يوم اليوم؟", "Hari apa hari ini?"),
                    line("Ahmad", "اليوم الإثنين.", "Hari ini Senin."),
                    line("Noura", "هل عندك درس؟", "Apakah kamu punya pelajaran?"),
                    line("Ahmad", "نعم، عندي درس في يوم الثلاثاء.", "Ya, saya punya pelajaran pada hari Selasa."),
                    line("Noura", "جيد.", "Bagus."),
                ],
            ),
            lesson(
                "lesson-03-talking-about-daily-routines",
                "arabic-talking-about-daily-routines",
                "Talking About Daily Routines",
                "Kamu menceritakan rutinitas pagi dengan kalimat Arab yang sangat pendek.",
                "Say a few simple daily actions in order.",
                "Use present verbs like أقرأ, أكتب, أدرس, and ثم to connect actions.",
                ["أقرأ", "أكتب", "أدرس العربية", "ثم أعمل"],
                [
                    phrase("ماذا تفعل صباحًا؟", "Apa yang kamu lakukan pagi hari?", "Ask about a morning routine."),
                    phrase("أقرأ", "Saya membaca.", "Say a reading action."),
                    phrase("أكتب", "Saya menulis.", "Say a writing action."),
                    phrase("أدرس العربية", "Saya belajar bahasa Arab.", "Say what you study."),
                    phrase("ثم أعمل", "Lalu saya bekerja.", "Connect the next action."),
                ],
                [
                    line("Layla", "ماذا تفعل صباحًا؟", "Apa yang kamu lakukan pagi hari?"),
                    line("Zayd", "أقرأ وأكتب.", "Saya membaca dan menulis."),
                    line("Layla", "هل تدرس العربية؟", "Apakah kamu belajar bahasa Arab?"),
                    line("Zayd", "نعم، أدرس العربية صباحًا.", "Ya, saya belajar bahasa Arab pagi hari."),
                    line("Layla", "ثم ماذا تفعل؟", "Lalu apa yang kamu lakukan?"),
                    line("Zayd", "ثم أعمل.", "Lalu saya bekerja."),
                ],
            ),
            lesson(
                "lesson-04-asking-when",
                "arabic-asking-when",
                "Asking When",
                "Kamu perlu bertanya kapan kelas, latihan, atau pertemuan dimulai.",
                "Ask when something happens and answer with a simple time phrase.",
                "Use متى + noun/verb for 'when' and في + time phrase for the answer.",
                ["متى الدرس؟", "في الصباح", "بعد الظهر", "قبل الدرس"],
                [
                    phrase("متى الدرس؟", "Kapan pelajarannya?", "Ask when a lesson happens."),
                    phrase("في الصباح", "Pada pagi hari", "Answer with a time of day."),
                    phrase("بعد الظهر", "Setelah tengah hari", "Answer with afternoon timing."),
                    phrase("قبل الدرس", "Sebelum pelajaran", "Say before the lesson."),
                    phrase("بعد الدرس", "Setelah pelajaran", "Say after the lesson."),
                ],
                [
                    line("Ahmad", "متى الدرس؟", "Kapan pelajarannya?"),
                    line("Maryam", "الدرس في الصباح.", "Pelajarannya pada pagi hari."),
                    line("Ahmad", "هل نكتب قبل الدرس؟", "Apakah kita menulis sebelum pelajaran?"),
                    line("Maryam", "نعم، نكتب قبل الدرس.", "Ya, kita menulis sebelum pelajaran."),
                    line("Ahmad", "وماذا نفعل بعد الدرس؟", "Dan apa yang kita lakukan setelah pelajaran?"),
                    line("Maryam", "نراجع الكلمات.", "Kita mengulang kosakata."),
                ],
            ),
            lesson(
                "lesson-05-routine-and-time-mission",
                "arabic-routine-and-time-mission",
                "Routine and Time Mission",
                "Kamu menjelaskan jadwal belajar sederhana kepada teman kelas.",
                "Combine day, time, and routine phrases in one short conversation.",
                "Combine اليوم, الساعة, عندي درس, and أدرس العربية.",
                ["اليوم ...", "الساعة ...", "عندي درس", "أدرس العربية"],
                [
                    phrase("اليوم ...", "Hari ini ...", "Start with the day."),
                    phrase("الساعة ...", "Jam ...", "Say a time."),
                    phrase("عندي درس", "Saya punya pelajaran.", "Mention a scheduled lesson."),
                    phrase("أدرس العربية", "Saya belajar bahasa Arab.", "Mention the activity."),
                    phrase("بعد الدرس", "Setelah pelajaran", "Continue the schedule."),
                ],
                [
                    line("Muallim", "أي يوم اليوم؟", "Hari apa hari ini?"),
                    line("Layla", "اليوم الأربعاء.", "Hari ini Rabu."),
                    line("Muallim", "متى تدرسين العربية؟", "Kapan kamu belajar bahasa Arab?"),
                    line("Layla", "أدرس العربية الساعة الثامنة صباحًا.", "Saya belajar bahasa Arab jam delapan pagi."),
                    line("Muallim", "وماذا تفعلين بعد الدرس؟", "Dan apa yang kamu lakukan setelah pelajaran?"),
                    line("Layla", "أقرأ وأكتب.", "Saya membaca dan menulis."),
                ],
            ),
        ],
    },
    {
        "unit_key": "unit-04-family-work-study",
        "title": "Family, Work & Study",
        "status": "beta",
        "main_conversation_outcome": "Talk simply about family, work, study, likes, and basic ability.",
        "lessons": [
            lesson(
                "lesson-01-family-members",
                "arabic-family-members",
                "Family Members",
                "Kamu menunjukkan foto keluarga dan menyebut anggota keluarga dengan kalimat pendek.",
                "Name simple family members and ask who someone is.",
                "Use هذا for masculine nouns and هذه for feminine nouns in simple identification.",
                ["من هذا؟", "هذا أبي.", "هذه أمي.", "هذه عائلتي."],
                [
                    phrase("من هذا؟", "Siapa ini?", "Ask about a person."),
                    phrase("هذا أبي", "Ini ayah saya.", "Identify father."),
                    phrase("هذه أمي", "Ini ibu saya.", "Identify mother."),
                    phrase("هذا أخي", "Ini saudara laki-laki saya.", "Identify brother."),
                    phrase("هذه عائلتي", "Ini keluarga saya.", "Talk about family."),
                ],
                [
                    line("Noura", "من هذا؟", "Siapa ini?"),
                    line("Ahmad", "هذا أبي.", "Ini ayah saya."),
                    line("Noura", "ومن هذه؟", "Dan siapa ini?"),
                    line("Ahmad", "هذه أمي.", "Ini ibu saya."),
                    line("Noura", "هل هذه عائلتك؟", "Apakah ini keluargamu?"),
                    line("Ahmad", "نعم، هذه عائلتي.", "Ya, ini keluarga saya."),
                ],
            ),
            lesson(
                "lesson-02-saying-what-you-do",
                "arabic-saying-what-you-do",
                "Saying What You Do",
                "Kamu memperkenalkan pekerjaan atau status belajar dalam percakapan formal ringan.",
                "Say whether you are a student, teacher, or worker.",
                "Use أنا + noun for identity and أعمل في + place for work.",
                ["أنا طالب.", "أنا معلم.", "أعمل في ...", "أدرس في ..."],
                [
                    phrase("ماذا تعمل؟", "Apa pekerjaanmu?", "Ask about work."),
                    phrase("أنا طالب", "Saya pelajar.", "Say student identity."),
                    phrase("أنا معلم", "Saya guru.", "Say teacher identity."),
                    phrase("أعمل في مكتب", "Saya bekerja di kantor.", "Say work place."),
                    phrase("أدرس في مدرسة", "Saya belajar di sekolah.", "Say study place."),
                ],
                [
                    line("Khalid", "ماذا تعمل؟", "Apa pekerjaanmu?"),
                    line("Zayd", "أنا طالب.", "Saya pelajar."),
                    line("Khalid", "أين تدرس؟", "Di mana kamu belajar?"),
                    line("Zayd", "أدرس في مدرسة.", "Saya belajar di sekolah."),
                    line("Khalid", "وأنت؟", "Dan kamu?"),
                    line("Zayd", "أنا أتعلم العربية.", "Saya sedang belajar bahasa Arab."),
                ],
            ),
            lesson(
                "lesson-03-asking-about-work-or-study",
                "arabic-asking-about-work-or-study",
                "Asking About Work or Study",
                "Kamu bertanya kepada teman baru tentang tempat belajar dan bidang yang dipelajari.",
                "Ask simple questions about work or study and answer briefly.",
                "Use أين for place and ماذا for what someone studies or does.",
                ["أين تدرس؟", "ماذا تدرس؟", "هل تعمل؟", "نعم، أعمل."],
                [
                    phrase("أين تدرس؟", "Di mana kamu belajar?", "Ask study place."),
                    phrase("ماذا تدرس؟", "Apa yang kamu pelajari?", "Ask study topic."),
                    phrase("أدرس اللغة العربية", "Saya belajar bahasa Arab.", "Answer study topic."),
                    phrase("هل تعمل؟", "Apakah kamu bekerja?", "Ask about work."),
                    phrase("نعم، أعمل", "Ya, saya bekerja.", "Answer yes to work."),
                ],
                [
                    line("Maryam", "أين تدرس؟", "Di mana kamu belajar?"),
                    line("Layla", "أدرس في المركز.", "Saya belajar di pusat belajar."),
                    line("Maryam", "ماذا تدرسين؟", "Apa yang kamu pelajari?"),
                    line("Layla", "أدرس اللغة العربية.", "Saya belajar bahasa Arab."),
                    line("Maryam", "هل تعملين أيضًا؟", "Apakah kamu juga bekerja?"),
                    line("Layla", "نعم، أعمل.", "Ya, saya bekerja."),
                ],
            ),
            lesson(
                "lesson-04-likes-and-ability",
                "arabic-likes-and-ability",
                "Likes and Ability",
                "Kamu menyebut hal yang disukai dan kemampuan sederhana dalam konteks belajar.",
                "Say what you like and what you can do a little.",
                "Use أحب for likes and أستطيع for ability.",
                ["أحب ...", "لا أحب ...", "أستطيع ...", "قليلًا"],
                [
                    phrase("أحب القراءة", "Saya suka membaca.", "Say a like."),
                    phrase("لا أحب الانتظار", "Saya tidak suka menunggu.", "Say a dislike."),
                    phrase("أستطيع القراءة", "Saya bisa membaca.", "Say ability."),
                    phrase("لا أستطيع الآن", "Saya belum bisa sekarang.", "Say inability."),
                    phrase("قليلًا", "Sedikit", "Limit your ability."),
                ],
                [
                    line("Ahmad", "ماذا تحبين؟", "Apa yang kamu sukai?"),
                    line("Noura", "أحب القراءة.", "Saya suka membaca."),
                    line("Ahmad", "هل تستطيعين الكتابة بالعربية؟", "Apakah kamu bisa menulis dalam bahasa Arab?"),
                    line("Noura", "أستطيع الكتابة قليلًا.", "Saya bisa menulis sedikit."),
                    line("Ahmad", "جيد جدًا.", "Bagus sekali."),
                ],
            ),
            lesson(
                "lesson-05-family-work-study-mission",
                "arabic-family-work-study-mission",
                "Family, Work, and Study Mission",
                "Kamu memperkenalkan diri sedikit lebih lengkap: keluarga, pekerjaan/belajar, dan minat.",
                "Combine family, work/study, and likes in one short formal conversation.",
                "Combine هذا/هذه, أنا, أدرس, أعمل, and أحب.",
                ["هذه عائلتي.", "أنا طالب.", "أدرس العربية.", "أحب القراءة."],
                [
                    phrase("هذه عائلتي", "Ini keluarga saya.", "Introduce family."),
                    phrase("أنا طالب", "Saya pelajar.", "Say study identity."),
                    phrase("أدرس العربية", "Saya belajar bahasa Arab.", "Say study topic."),
                    phrase("أعمل في مكتب", "Saya bekerja di kantor.", "Say work place."),
                    phrase("أحب القراءة", "Saya suka membaca.", "Say a preference."),
                ],
                [
                    line("Muallimah", "حدثيني عن نفسك.", "Ceritakan tentang dirimu."),
                    line("Layla", "اسمي ليلى، وهذه عائلتي.", "Nama saya Layla, dan ini keluarga saya."),
                    line("Muallimah", "هل تدرسين؟", "Apakah kamu belajar?"),
                    line("Layla", "نعم، أدرس العربية.", "Ya, saya belajar bahasa Arab."),
                    line("Muallimah", "ماذا تحبين؟", "Apa yang kamu sukai?"),
                    line("Layla", "أحب القراءة والكتابة.", "Saya suka membaca dan menulis."),
                ],
            ),
        ],
    },
    {
        "unit_key": "unit-05-places-directions",
        "title": "Places & Directions",
        "status": "beta",
        "main_conversation_outcome": "Ask where places are and understand simple directions in Arabic.",
        "lessons": [
            lesson(
                "lesson-01-asking-where-a-place-is",
                "arabic-asking-where-a-place-is",
                "Asking Where a Place Is",
                "Kamu mencari perpustakaan di gedung belajar dan bertanya dengan sopan.",
                "Ask where a place is and understand here/there.",
                "Use أين + place for location questions and هنا/هناك for here/there.",
                ["أين المكتبة؟", "المكتبة هنا.", "هناك.", "قريبة."],
                [
                    phrase("أين المكتبة؟", "Di mana perpustakaan?", "Ask location."),
                    phrase("المكتبة هنا", "Perpustakaan di sini.", "Answer here."),
                    phrase("هناك", "Di sana", "Point to another place."),
                    phrase("قريبة", "Dekat", "Describe distance."),
                    phrase("بعيدة", "Jauh", "Describe distance."),
                ],
                [
                    line("Zayd", "أين المكتبة؟", "Di mana perpustakaan?"),
                    line("Maryam", "المكتبة هناك.", "Perpustakaan di sana."),
                    line("Zayd", "هل هي قريبة؟", "Apakah dekat?"),
                    line("Maryam", "نعم، هي قريبة.", "Ya, dekat."),
                    line("Zayd", "شكرًا.", "Terima kasih."),
                ],
            ),
            lesson(
                "lesson-02-simple-place-words",
                "arabic-simple-place-words",
                "Simple Place Words",
                "Kamu menyebut beberapa tempat umum yang sering muncul dalam percakapan formal.",
                "Recognize and use simple place nouns in short questions.",
                "Use أين + place and هذا/هذه + place noun for simple place identification.",
                ["البيت", "المدرسة", "السوق", "المكتب", "المقهى"],
                [
                    phrase("البيت", "Rumah", "Name a home."),
                    phrase("المدرسة", "Sekolah", "Name a school."),
                    phrase("السوق", "Pasar", "Name a market."),
                    phrase("المكتب", "Kantor", "Name an office."),
                    phrase("المقهى", "Kafe", "Name a cafe."),
                ],
                [
                    line("Noura", "أين المدرسة؟", "Di mana sekolah?"),
                    line("Ahmad", "المدرسة قريبة.", "Sekolah dekat."),
                    line("Noura", "وأين السوق؟", "Dan di mana pasar?"),
                    line("Ahmad", "السوق بعيد.", "Pasar jauh."),
                    line("Noura", "هل المقهى هنا؟", "Apakah kafe di sini?"),
                    line("Ahmad", "نعم، المقهى هنا.", "Ya, kafe di sini."),
                ],
            ),
            lesson(
                "lesson-03-understanding-simple-directions",
                "arabic-understanding-simple-directions",
                "Understanding Simple Directions",
                "Kamu menerima arahan singkat menuju kelas atau perpustakaan.",
                "Understand right, left, forward, beside, and in front of.",
                "Use اذهب + direction and prepositions like بجانب and أمام.",
                ["اذهب يمينًا", "اذهب يسارًا", "إلى الأمام", "بجانب", "أمام"],
                [
                    phrase("اذهب يمينًا", "Pergi ke kanan.", "Give a right direction."),
                    phrase("اذهب يسارًا", "Pergi ke kiri.", "Give a left direction."),
                    phrase("إلى الأمام", "Ke depan", "Give forward direction."),
                    phrase("بجانب المكتب", "Di samping kantor", "Describe beside."),
                    phrase("أمام المدرسة", "Di depan sekolah", "Describe in front."),
                ],
                [
                    line("Khalid", "كيف أذهب إلى المكتبة؟", "Bagaimana saya pergi ke perpustakaan?"),
                    line("Layla", "اذهب إلى الأمام.", "Pergilah ke depan."),
                    line("Khalid", "ثم؟", "Lalu?"),
                    line("Layla", "ثم اذهب يمينًا.", "Lalu pergilah ke kanan."),
                    line("Khalid", "أين المكتبة؟", "Di mana perpustakaan?"),
                    line("Layla", "هي بجانب المكتب.", "Perpustakaan di samping kantor."),
                ],
            ),
            lesson(
                "lesson-04-asking-how-to-get-there",
                "arabic-asking-how-to-get-there",
                "Asking How to Get There",
                "Kamu meminta arahan menuju tempat tertentu di sekitar kelas.",
                "Ask how to get to a place and follow two-step directions.",
                "Use كيف أذهب إلى + place and ثم to link steps.",
                ["كيف أذهب إلى ...؟", "امشِ", "ثم", "عند الباب", "شكرًا"],
                [
                    phrase("كيف أذهب إلى المكتبة؟", "Bagaimana saya pergi ke perpustakaan?", "Ask how to get somewhere."),
                    phrase("امشِ إلى الأمام", "Berjalanlah ke depan.", "Give walking direction."),
                    phrase("ثم", "Lalu", "Connect steps."),
                    phrase("عند الباب", "Di dekat pintu", "Give a landmark."),
                    phrase("شكرًا", "Terima kasih.", "Close politely."),
                ],
                [
                    line("Ahmad", "كيف أذهب إلى المقهى؟", "Bagaimana saya pergi ke kafe?"),
                    line("Maryam", "امشِ إلى الأمام.", "Berjalanlah ke depan."),
                    line("Ahmad", "ثم ماذا؟", "Lalu apa?"),
                    line("Maryam", "ثم اذهب يسارًا عند الباب.", "Lalu pergilah ke kiri di dekat pintu."),
                    line("Ahmad", "شكرًا.", "Terima kasih."),
                ],
            ),
            lesson(
                "lesson-05-finding-a-place-mission",
                "arabic-finding-a-place-mission",
                "Finding a Place Mission",
                "Kamu mencari kelas baru, bertanya lokasi, dan mengikuti arahan singkat.",
                "Combine place questions and simple directions in one conversation.",
                "Combine أين, كيف أذهب, يمينًا, يسارًا, and بجانب.",
                ["أين الفصل؟", "كيف أذهب إلى الفصل؟", "اذهب يمينًا", "هو بجانب المكتبة"],
                [
                    phrase("أين الفصل؟", "Di mana kelas?", "Ask where the classroom is."),
                    phrase("كيف أذهب إلى الفصل؟", "Bagaimana saya pergi ke kelas?", "Ask for directions."),
                    phrase("اذهب يمينًا", "Pergi ke kanan.", "Follow direction."),
                    phrase("هو بجانب المكتبة", "Itu di samping perpustakaan.", "Describe location."),
                    phrase("واضح", "Jelas", "Confirm understanding."),
                ],
                [
                    line("Muallim", "أين تريد أن تذهب؟", "Ke mana kamu ingin pergi?"),
                    line("Noura", "أريد أن أذهب إلى الفصل.", "Saya ingin pergi ke kelas."),
                    line("Muallim", "اذهبي يمينًا، ثم إلى الأمام.", "Pergilah ke kanan, lalu ke depan."),
                    line("Noura", "أين الفصل؟", "Di mana kelasnya?"),
                    line("Muallim", "هو بجانب المكتبة.", "Kelas di samping perpustakaan."),
                    line("Noura", "واضح، شكرًا.", "Jelas, terima kasih."),
                ],
            ),
        ],
    },
    {
        "unit_key": "unit-06-food-shopping-prices",
        "title": "Food, Shopping & Prices",
        "status": "beta",
        "main_conversation_outcome": "Order simple items, ask prices, and say what you want in Arabic.",
        "lessons": [
            lesson(
                "lesson-01-ordering-a-drink",
                "arabic-ordering-a-drink",
                "Ordering a Drink",
                "Kamu berada di kafe dan ingin memesan minuman sederhana dengan sopan.",
                "Order water or coffee using polite Arabic phrases.",
                "Use أريد + noun and من فضلك for a polite request.",
                ["أريد ماءً", "أريد قهوة", "من فضلك", "هل عندكم ...؟"],
                [
                    phrase("أريد ماءً", "Saya ingin air.", "Order water."),
                    phrase("أريد قهوة", "Saya ingin kopi.", "Order coffee."),
                    phrase("من فضلك", "Tolong.", "Make it polite."),
                    phrase("هل عندكم شاي؟", "Apakah kalian punya teh?", "Ask availability."),
                    phrase("تفضل", "Silakan.", "Offer something."),
                ],
                [
                    line("Khalid", "مرحبًا.", "Halo."),
                    line("Layla", "مرحبًا، ماذا تريد؟", "Halo, apa yang kamu inginkan?"),
                    line("Khalid", "أريد ماءً من فضلك.", "Saya ingin air, tolong."),
                    line("Layla", "تفضل.", "Silakan."),
                    line("Khalid", "شكرًا.", "Terima kasih."),
                ],
            ),
            lesson(
                "lesson-02-asking-about-prices",
                "arabic-asking-about-prices",
                "Asking About Prices",
                "Kamu melihat barang sederhana dan perlu menanyakan harganya.",
                "Ask a price and understand a simple answer.",
                "Use كم السعر؟ for price and السعر + number + currency for answer.",
                ["كم السعر؟", "السعر خمسة ريالات", "غالٍ", "رخيص", "مناسب"],
                [
                    phrase("كم السعر؟", "Berapa harganya?", "Ask price."),
                    phrase("السعر خمسة ريالات", "Harganya lima riyal.", "Say a price."),
                    phrase("غالٍ", "Mahal", "Describe expensive."),
                    phrase("رخيص", "Murah", "Describe cheap."),
                    phrase("مناسب", "Cocok/pas", "Say price is acceptable."),
                ],
                [
                    line("Maryam", "كم السعر؟", "Berapa harganya?"),
                    line("Zayd", "السعر خمسة ريالات.", "Harganya lima riyal."),
                    line("Maryam", "هل السعر مناسب؟", "Apakah harganya cocok?"),
                    line("Zayd", "نعم، السعر مناسب.", "Ya, harganya cocok."),
                    line("Maryam", "آخذ واحدًا.", "Saya ambil satu."),
                ],
            ),
            lesson(
                "lesson-03-buying-a-simple-item",
                "arabic-buying-a-simple-item",
                "Buying a Simple Item",
                "Kamu membeli alat tulis sederhana untuk kelas.",
                "Ask for an item, say you want one, and close the purchase.",
                "Use هل عندكم + noun and آخذ واحدًا for taking one item.",
                ["هل عندكم قلم؟", "نعم، موجود.", "أريد هذا.", "آخذ واحدًا."],
                [
                    phrase("هل عندكم قلم؟", "Apakah kalian punya pena?", "Ask item availability."),
                    phrase("نعم، موجود", "Ya, ada.", "Confirm availability."),
                    phrase("أريد هذا", "Saya ingin ini.", "Choose an item."),
                    phrase("آخذ واحدًا", "Saya ambil satu.", "Buy one."),
                    phrase("الحساب من فضلك", "Tagihannya, tolong.", "Ask for the bill."),
                ],
                [
                    line("Ahmad", "هل عندكم قلم؟", "Apakah kalian punya pena?"),
                    line("Noura", "نعم، موجود.", "Ya, ada."),
                    line("Ahmad", "أريد هذا.", "Saya ingin ini."),
                    line("Noura", "كم قلمًا تريد؟", "Berapa pena yang kamu inginkan?"),
                    line("Ahmad", "آخذ واحدًا.", "Saya ambil satu."),
                ],
            ),
            lesson(
                "lesson-04-saying-what-you-want",
                "arabic-saying-what-you-want",
                "Saying What You Want",
                "Kamu menjawab pertanyaan sederhana tentang apa yang diinginkan atau dibutuhkan.",
                "Say what you want, do not want, and need.",
                "Use أريد, لا أريد, and أحتاج with a simple noun.",
                ["ماذا تريد؟", "أريد ...", "لا أريد ...", "أحتاج ..."],
                [
                    phrase("ماذا تريد؟", "Apa yang kamu inginkan?", "Ask what someone wants."),
                    phrase("أريد كتابًا", "Saya ingin buku.", "Say a wanted item."),
                    phrase("لا أريد قهوة", "Saya tidak ingin kopi.", "Say what you do not want."),
                    phrase("أحتاج قلمًا", "Saya butuh pena.", "Say a need."),
                    phrase("فقط", "Saja", "Limit the request."),
                ],
                [
                    line("Layla", "ماذا تريد؟", "Apa yang kamu inginkan?"),
                    line("Khalid", "أريد كتابًا.", "Saya ingin buku."),
                    line("Layla", "هل تريد قهوة أيضًا؟", "Apakah kamu juga ingin kopi?"),
                    line("Khalid", "لا أريد قهوة.", "Saya tidak ingin kopi."),
                    line("Layla", "هل تحتاج شيئًا آخر؟", "Apakah kamu membutuhkan hal lain?"),
                    line("Khalid", "أحتاج قلمًا فقط.", "Saya hanya butuh pena."),
                ],
            ),
            lesson(
                "lesson-05-cafe-and-shop-mission",
                "arabic-cafe-and-shop-mission",
                "Cafe and Shop Mission",
                "Kamu memesan minuman, bertanya harga, dan membeli satu barang sederhana.",
                "Combine ordering, price, and buying phrases in one short conversation.",
                "Combine أريد, كم السعر, آخذ واحدًا, and من فضلك.",
                ["أريد ماءً.", "كم السعر؟", "آخذ واحدًا.", "من فضلك."],
                [
                    phrase("أريد ماءً", "Saya ingin air.", "Order a drink."),
                    phrase("كم السعر؟", "Berapa harganya?", "Ask price."),
                    phrase("السعر مناسب", "Harganya cocok.", "Accept price."),
                    phrase("آخذ واحدًا", "Saya ambil satu.", "Buy one."),
                    phrase("الحساب من فضلك", "Tagihannya, tolong.", "Close the purchase."),
                ],
                [
                    line("Muallimah", "ماذا تريد؟", "Apa yang kamu inginkan?"),
                    line("Zayd", "أريد ماءً وقلمًا.", "Saya ingin air dan pena."),
                    line("Muallimah", "السعر ستة ريالات.", "Harganya enam riyal."),
                    line("Zayd", "السعر مناسب. آخذ واحدًا.", "Harganya cocok. Saya ambil satu."),
                    line("Muallimah", "تفضل.", "Silakan."),
                    line("Zayd", "شكرًا.", "Terima kasih."),
                ],
            ),
        ],
    },
    {
        "unit_key": "unit-07-help-problems-requests",
        "title": "Help, Problems & Requests",
        "status": "beta",
        "main_conversation_outcome": "Ask for help, explain simple problems, and make polite requests in Arabic.",
        "lessons": [
            lesson(
                "lesson-01-saying-you-do-not-understand",
                "arabic-saying-you-do-not-understand",
                "Saying You Do Not Understand",
                "Kamu tidak paham kata atau instruksi dan perlu menjelaskannya dengan sopan.",
                "Say you do not understand and ask for a word meaning.",
                "Use لا أفهم and ماذا يعني ...؟ to ask for meaning.",
                ["لا أفهم.", "لا أعرف الكلمة.", "ماذا يعني ...؟", "مرة أخرى"],
                [
                    phrase("لا أفهم", "Saya tidak paham.", "State lack of understanding."),
                    phrase("لا أعرف الكلمة", "Saya tidak tahu katanya.", "Identify the problem."),
                    phrase("ماذا يعني هذا؟", "Apa arti ini?", "Ask meaning."),
                    phrase("ببطء من فضلك", "Pelan-pelan, tolong.", "Ask for slower speech."),
                    phrase("مرة أخرى", "Sekali lagi", "Ask repetition."),
                ],
                [
                    line("Maryam", "اقرأ الجملة.", "Bacalah kalimatnya."),
                    line("Ahmad", "لا أفهم الكلمة.", "Saya tidak paham katanya."),
                    line("Maryam", "أي كلمة؟", "Kata yang mana?"),
                    line("Ahmad", "ماذا يعني هذا؟", "Apa arti ini?"),
                    line("Maryam", "يعني: كتاب.", "Artinya: buku."),
                    line("Ahmad", "شكرًا، الآن أفهم.", "Terima kasih, sekarang saya paham."),
                ],
            ),
            lesson(
                "lesson-02-asking-for-help",
                "arabic-asking-for-help",
                "Asking for Help",
                "Kamu kesulitan menemukan halaman atau latihan dan perlu meminta bantuan.",
                "Ask for help and say what you need.",
                "Use هل تساعدني؟ and أحتاج مساعدة for simple help requests.",
                ["هل تساعدني؟", "أحتاج مساعدة.", "أين أجد ...؟", "افتح الصفحة."],
                [
                    phrase("هل تساعدني؟", "Bisakah Anda membantu saya?", "Ask for help."),
                    phrase("أحتاج مساعدة", "Saya butuh bantuan.", "State need."),
                    phrase("أين أجد الدرس؟", "Di mana saya menemukan pelajaran?", "Ask where to find something."),
                    phrase("افتح الصفحة", "Buka halamannya.", "Give a simple instruction."),
                    phrase("شكرًا على المساعدة", "Terima kasih atas bantuannya.", "Thank someone."),
                ],
                [
                    line("Khalid", "هل تساعدني؟", "Bisakah Anda membantu saya?"),
                    line("Noura", "نعم، ماذا تحتاج؟", "Ya, apa yang kamu butuhkan?"),
                    line("Khalid", "أحتاج مساعدة في الدرس.", "Saya butuh bantuan dalam pelajaran."),
                    line("Noura", "افتح الصفحة الثانية.", "Buka halaman kedua."),
                    line("Khalid", "شكرًا على المساعدة.", "Terima kasih atas bantuannya."),
                ],
            ),
            lesson(
                "lesson-03-making-simple-requests",
                "arabic-making-simple-requests",
                "Making Simple Requests",
                "Kamu meminta teman atau guru melakukan instruksi sederhana dalam konteks belajar.",
                "Make polite classroom requests using short imperative forms.",
                "Use imperative verbs plus من فضلك for polite requests.",
                ["افتح الكتاب", "اكتب الجملة", "استمع", "تكلم ببطء"],
                [
                    phrase("افتح الكتاب", "Buka bukunya.", "Ask someone to open a book."),
                    phrase("اكتب الجملة", "Tulis kalimatnya.", "Ask someone to write."),
                    phrase("استمع", "Dengarkan.", "Ask someone to listen."),
                    phrase("تكلم ببطء", "Bicaralah pelan.", "Ask someone to speak slowly."),
                    phrase("من فضلك", "Tolong.", "Make the request polite."),
                ],
                [
                    line("Muallim", "افتح الكتاب من فضلك.", "Buka bukunya, tolong."),
                    line("Layla", "نعم، أفتح الكتاب.", "Ya, saya buka bukunya."),
                    line("Muallim", "اكتبي الجملة.", "Tulis kalimatnya."),
                    line("Layla", "أكتب الجملة الآن.", "Saya menulis kalimatnya sekarang."),
                    line("Muallim", "استمعي ثم تكلمي.", "Dengarkan lalu bicaralah."),
                    line("Layla", "حسنًا.", "Baik."),
                ],
            ),
            lesson(
                "lesson-04-apologizing-and-thanking",
                "arabic-apologizing-and-thanking",
                "Apologizing and Thanking",
                "Kamu terlambat merespons atau membuat kesalahan kecil dan ingin menjawab sopan.",
                "Apologize, thank someone, and respond politely.",
                "Use آسف/آسفة for sorry and شكرًا for thanks.",
                ["آسف.", "عذرًا.", "لا مشكلة.", "شكرًا."],
                [
                    phrase("آسف", "Maaf.", "Male speaker apology."),
                    phrase("آسفة", "Maaf.", "Female speaker apology."),
                    phrase("عذرًا", "Permisi/maaf.", "General apology or excuse."),
                    phrase("لا مشكلة", "Tidak masalah.", "Respond to apology."),
                    phrase("على الرحب والسعة", "Sama-sama.", "Respond to thanks."),
                ],
                [
                    line("Ahmad", "عذرًا، لا أفهم.", "Maaf, saya tidak paham."),
                    line("Maryam", "لا مشكلة. أشرح مرة أخرى.", "Tidak masalah. Saya jelaskan sekali lagi."),
                    line("Ahmad", "شكرًا.", "Terima kasih."),
                    line("Maryam", "على الرحب والسعة.", "Sama-sama."),
                    line("Ahmad", "آسف على السؤال.", "Maaf atas pertanyaannya."),
                    line("Maryam", "لا مشكلة.", "Tidak masalah."),
                ],
            ),
            lesson(
                "lesson-05-help-and-problem-mission",
                "arabic-help-and-problem-mission",
                "Help and Problem Mission",
                "Kamu menghadapi masalah kecil dalam kelas dan menyelesaikannya dengan permintaan sopan.",
                "Combine not understanding, asking for help, and thanking in one conversation.",
                "Combine لا أفهم, هل تساعدني, من فضلك, and شكرًا.",
                ["لا أفهم.", "هل تساعدني؟", "ببطء من فضلك.", "شكرًا."],
                [
                    phrase("لا أفهم", "Saya tidak paham.", "Explain the problem."),
                    phrase("هل تساعدني؟", "Bisakah Anda membantu saya?", "Ask for help."),
                    phrase("ببطء من فضلك", "Pelan-pelan, tolong.", "Ask for slower speech."),
                    phrase("أعد مرة أخرى", "Ulangi sekali lagi.", "Ask repetition."),
                    phrase("شكرًا على المساعدة", "Terima kasih atas bantuannya.", "Close politely."),
                ],
                [
                    line("Muallimah", "اقرئي الجملة.", "Bacalah kalimatnya."),
                    line("Noura", "لا أفهم. هل تساعدينني؟", "Saya tidak paham. Bisa membantu saya?"),
                    line("Muallimah", "نعم. استمعي ببطء.", "Ya. Dengarkan pelan-pelan."),
                    line("Noura", "أعيدي مرة أخرى من فضلك.", "Ulangi sekali lagi, tolong."),
                    line("Muallimah", "حسنًا، مرة أخرى.", "Baik, sekali lagi."),
                    line("Noura", "شكرًا على المساعدة.", "Terima kasih atas bantuannya."),
                ],
            ),
        ],
    },
    {
        "unit_key": "unit-08-a1-review-final",
        "title": "A1 Review & Final Conversation",
        "status": "beta",
        "main_conversation_outcome": "Combine Arabic A1 skills in longer but still simple formal conversations.",
        "lessons": [
            lesson(
                "lesson-01-review-introductions-and-contact",
                "arabic-review-introductions-and-contact",
                "Review Introductions and Contact",
                "Kamu mengulang perkenalan, asal, ejaan nama, dan informasi kontak sederhana.",
                "Review introductions and contact details in one smooth exchange.",
                "Review اسمي, أنا من, أكتب اسمي, رقمي, and بريدي الإلكتروني.",
                ["اسمي ...", "أنا من ...", "أكتب اسمي ...", "رقمي ..."],
                [
                    phrase("اسمي أحمد", "Nama saya Ahmad.", "Say your name."),
                    phrase("أنا من إندونيسيا", "Saya dari Indonesia.", "Say origin."),
                    phrase("أكتب اسمي", "Saya menulis nama saya.", "Spell your name."),
                    phrase("رقمي ...", "Nomor saya ...", "Share a number."),
                    phrase("بريدي الإلكتروني ...", "Email saya ...", "Share email."),
                ],
                [
                    line("Muallim", "ما اسمك ومن أين أنت؟", "Siapa namamu dan dari mana kamu?"),
                    line("Ahmad", "اسمي أحمد، وأنا من إندونيسيا.", "Nama saya Ahmad, dan saya dari Indonesia."),
                    line("Muallim", "كيف تكتب اسمك؟", "Bagaimana kamu menulis namamu?"),
                    line("Ahmad", "أكتب اسمي: أحمد.", "Saya menulis nama saya: Ahmad."),
                    line("Muallim", "ما رقم هاتفك؟", "Berapa nomor teleponmu?"),
                    line("Ahmad", "رقمي واحد، اثنان، ثلاثة.", "Nomor saya satu, dua, tiga."),
                ],
            ),
            lesson(
                "lesson-02-review-routine-and-study",
                "arabic-review-routine-and-study",
                "Review Routine and Study",
                "Kamu menceritakan jadwal belajar bahasa Arab dan aktivitas sederhana.",
                "Review days, time, and daily study routine.",
                "Review اليوم, الساعة, أدرس, أقرأ, and أكتب.",
                ["اليوم ...", "الساعة ...", "أدرس العربية", "أقرأ وأكتب"],
                [
                    phrase("اليوم الإثنين", "Hari ini Senin.", "Say the day."),
                    phrase("الساعة الثامنة", "Jam delapan.", "Say the time."),
                    phrase("أدرس العربية", "Saya belajar bahasa Arab.", "Say study action."),
                    phrase("أقرأ وأكتب", "Saya membaca dan menulis.", "Say routine actions."),
                    phrase("بعد الدرس", "Setelah pelajaran", "Continue the sequence."),
                ],
                [
                    line("Maryam", "متى تدرس العربية؟", "Kapan kamu belajar bahasa Arab?"),
                    line("Zayd", "أدرس العربية اليوم الساعة الثامنة.", "Saya belajar bahasa Arab hari ini jam delapan."),
                    line("Maryam", "ماذا تفعل في الدرس؟", "Apa yang kamu lakukan dalam pelajaran?"),
                    line("Zayd", "أقرأ وأكتب وأستمع.", "Saya membaca, menulis, dan mendengarkan."),
                    line("Maryam", "وماذا تفعل بعد الدرس؟", "Dan apa yang kamu lakukan setelah pelajaran?"),
                    line("Zayd", "أراجع الكلمات.", "Saya mengulang kosakata."),
                ],
            ),
            lesson(
                "lesson-03-review-places-and-shopping",
                "arabic-review-places-and-shopping",
                "Review Places and Shopping",
                "Kamu mencari kafe, bertanya arah, lalu membeli minuman sederhana.",
                "Review place, direction, ordering, and price phrases.",
                "Review أين, كيف أذهب, أريد, and كم السعر.",
                ["أين المقهى؟", "كيف أذهب؟", "أريد ماءً", "كم السعر؟"],
                [
                    phrase("أين المقهى؟", "Di mana kafe?", "Ask place."),
                    phrase("كيف أذهب إلى المقهى؟", "Bagaimana saya pergi ke kafe?", "Ask directions."),
                    phrase("أريد ماءً", "Saya ingin air.", "Order a drink."),
                    phrase("كم السعر؟", "Berapa harganya?", "Ask price."),
                    phrase("السعر مناسب", "Harganya cocok.", "Accept price."),
                ],
                [
                    line("Khalid", "أين المقهى؟", "Di mana kafe?"),
                    line("Layla", "المقهى بجانب المكتبة.", "Kafe di samping perpustakaan."),
                    line("Khalid", "كيف أذهب إليه؟", "Bagaimana saya pergi ke sana?"),
                    line("Layla", "اذهب إلى الأمام ثم يسارًا.", "Pergilah ke depan lalu ke kiri."),
                    line("Khalid", "في المقهى أريد ماءً. كم السعر؟", "Di kafe saya ingin air. Berapa harganya?"),
                    line("Layla", "السعر ريالان.", "Harganya dua riyal."),
                ],
            ),
            lesson(
                "lesson-04-a1-final-test-practice",
                "arabic-a1-final-test-practice",
                "A1 Final Test Practice",
                "Kamu berlatih menjawab pertanyaan final A1 secara singkat dan jelas.",
                "Practice answering mixed A1 questions before the final conversation.",
                "Use short complete answers with أنا, عندي, أريد, and لا أفهم.",
                ["أنا من ...", "عندي درس", "أريد ...", "لا أفهم"],
                [
                    phrase("أنا من إندونيسيا", "Saya dari Indonesia.", "Answer origin."),
                    phrase("عندي درس", "Saya punya pelajaran.", "Answer schedule."),
                    phrase("أريد كتابًا", "Saya ingin buku.", "Answer want."),
                    phrase("لا أفهم", "Saya tidak paham.", "Ask for help."),
                    phrase("أعد من فضلك", "Ulangi, tolong.", "Request repetition."),
                ],
                [
                    line("Muallimah", "من أين أنت؟", "Dari mana kamu?"),
                    line("Noura", "أنا من إندونيسيا.", "Saya dari Indonesia."),
                    line("Muallimah", "متى الدرس؟", "Kapan pelajarannya?"),
                    line("Noura", "الدرس الساعة الثامنة.", "Pelajarannya jam delapan."),
                    line("Muallimah", "ماذا تريد؟", "Apa yang kamu inginkan?"),
                    line("Noura", "أريد كتابًا.", "Saya ingin buku."),
                    line("Muallimah", "هل تفهمين؟", "Apakah kamu paham?"),
                    line("Noura", "نعم، أفهم.", "Ya, saya paham."),
                ],
            ),
            lesson(
                "lesson-05-a1-final-conversation",
                "arabic-a1-final-conversation",
                "A1 Final Conversation",
                "Kamu menjalani percakapan final: perkenalan, rutinitas belajar, tempat, belanja, dan bantuan.",
                "Complete a short Arabic A1 conversation using core skills from the level.",
                "Combine greetings, introductions, schedule, directions, ordering, and help requests.",
                ["مرحبًا", "اسمي ...", "أدرس العربية", "أين ...؟", "أريد ..."],
                [
                    phrase("مرحبًا", "Halo.", "Start politely."),
                    phrase("اسمي ...", "Nama saya ...", "Introduce yourself."),
                    phrase("أدرس العربية", "Saya belajar bahasa Arab.", "Talk about study."),
                    phrase("أين المكتبة؟", "Di mana perpustakaan?", "Ask location."),
                    phrase("أحتاج مساعدة", "Saya butuh bantuan.", "Ask for help."),
                ],
                [
                    line("Muallim", "مرحبًا، ما اسمك؟", "Halo, siapa namamu?"),
                    line("Ahmad", "مرحبًا، اسمي أحمد.", "Halo, nama saya Ahmad."),
                    line("Muallim", "متى تدرس العربية؟", "Kapan kamu belajar bahasa Arab?"),
                    line("Ahmad", "أدرس العربية في الصباح.", "Saya belajar bahasa Arab pada pagi hari."),
                    line("Muallim", "أين تريد أن تذهب بعد الدرس؟", "Ke mana kamu ingin pergi setelah pelajaran?"),
                    line("Ahmad", "أريد أن أذهب إلى المكتبة.", "Saya ingin pergi ke perpustakaan."),
                    line("Muallim", "هل تحتاج مساعدة؟", "Apakah kamu butuh bantuan?"),
                    line("Ahmad", "نعم، أحتاج مساعدة من فضلك.", "Ya, saya butuh bantuan, tolong."),
                ],
            ),
        ],
    },
]


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def lesson_plan_entries(unit: dict[str, Any]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for item in unit["lessons"]:
        entries.append(
            {
                "lesson_key": item["lesson_key"],
                "slug": item["slug"],
                "title": item["title"],
                "status": item.get("status", "beta"),
            }
        )
    return entries


def update_content_plan() -> None:
    plan = {
        "language": "arabic",
        "language_code": "ar",
        "level_code": "A1",
        "course_slug": "arabic-a1-fusha-foundations",
        "course_title": "Arabic Foundations",
        "access_tier": "pro_beta",
        "target_lesson_count": sum(len(unit["lessons"]) for unit in UNIT_PLANS),
        "units": [
            {
                "unit_key": unit["unit_key"],
                "title": unit["title"],
                "status": unit["status"],
                "main_conversation_outcome": unit["main_conversation_outcome"],
                "lessons": lesson_plan_entries(unit),
            }
            for unit in UNIT_PLANS
        ],
    }
    write_yaml(A1_ROOT / "content_plan.yaml", plan)


def write_unit(unit: dict[str, Any]) -> None:
    unit_dir = UNITS_ROOT / unit["unit_key"]
    unit_dir.mkdir(parents=True, exist_ok=True)

    unit_yaml = {
        "unit_key": unit["unit_key"],
        "level_code": "A1",
        "title": unit["title"],
        "main_conversation_outcome": unit["main_conversation_outcome"],
        "status": unit["status"],
        "lessons": [item["lesson_key"] for item in unit["lessons"]],
    }
    write_yaml(unit_dir / "unit.yaml", unit_yaml)


def generated_units() -> list[dict[str, Any]]:
    return [unit for unit in UNIT_PLANS if unit["unit_key"] != "unit-01-fusha-foundations"]


def write_lesson_files(unit: dict[str, Any], item: dict[str, Any]) -> None:
    lesson_dir = UNITS_ROOT / unit["unit_key"] / item["lesson_key"]
    lesson_dir.mkdir(parents=True, exist_ok=True)

    write_yaml(
        lesson_dir / "lesson.yaml",
        {
            "lesson_key": item["lesson_key"],
            "slug": item["slug"],
            "title": item["title"],
            "status": item["status"],
            "estimated_minutes": 10,
            "conversation_situation": item["slug"].replace("arabic-", "").replace("-", "_"),
            "conversation_goal": item["goal"],
            "grammar_summary": item["grammar"],
            "required_sections": REQUIRED_SECTIONS,
            "completion_rules": {
                "listening_completed": True,
                "quiz_required": True,
                "speaking_attempt_required": True,
                "minimum_score": 60,
            },
        },
    )

    (lesson_dir / "lesson.md").write_text(
        f"# {item['title']}\n\n"
        f"After this lesson, learners can {item['goal'][0].lower() + item['goal'][1:]}\n\n"
        "## Situation\n\n"
        f"{item['situation']}\n\n"
        "## Learning Notes\n\n"
        "Arabic is formal and precise. Fokus latihan ini adalah kalimat pendek yang aman "
        "untuk percakapan umum, kelas, dan situasi belajar.\n",
        encoding="utf-8",
    )

    (lesson_dir / "conversation_goal.md").write_text(
        f"# Conversation Goal\n\n{item['goal']}\n\n"
        "Learners should be able to say:\n\n"
        + "\n".join(f"- {entry['phrase']}" for entry in item["phrases"][:5])
        + "\n",
        encoding="utf-8",
    )

    (lesson_dir / "listening_script.md").write_text(
        "# Listening Script\n\n"
        + "\n".join(f"**{speaker}:** {text}" for speaker, text, _ in item["dialogue"])
        + "\n\n## Audio Direction\n\n"
        "Use Arabic only. Speaker labels are metadata and must not be spoken. "
        "Keep a calm pace with a short natural pause between speakers.\n",
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
                {
                    "phrase": entry["phrase"],
                    "meaning_id": entry["meaning"],
                    "usage_note": entry["usage"],
                }
                for entry in item["phrases"]
            ]
        },
    )

    (lesson_dir / "grammar_for_conversation.md").write_text(
        "# Grammar for Conversation\n\n"
        f"{item['grammar']}\n\n"
        "```txt\n"
        + "\n".join(item["patterns"])
        + "\n```\n\n"
        "Keep the sentence short first. Setelah pola terasa mudah, ganti nama, tempat, waktu, "
        "atau benda sesuai kebutuhan percakapan.\n",
        encoding="utf-8",
    )

    (lesson_dir / "pronunciation_drill.md").write_text(
        "# Speak Clearly\n\n## Repeat\n\n"
        + "\n".join(f"{index}. {entry['phrase']}" for index, entry in enumerate(item["phrases"][:5], 1))
        + "\n\n## Focus\n\n"
        "- Speak slowly and keep long vowels clear.\n"
        "- Do not swallow final consonants in short phrases.\n"
        "- Pause briefly between question and answer.\n",
        encoding="utf-8",
    )

    write_yaml(
        lesson_dir / "response_prompts.yaml",
        {
            "prompts": [
                {
                    "prompt": f"Say: {entry['meaning']}",
                    "target_response": entry["phrase"],
                    "acceptable_responses": [entry["phrase"]],
                }
                for entry in item["phrases"][:3]
            ]
        },
    )

    write_yaml(
        lesson_dir / "quiz.yaml",
        {
            "questions": [
                {
                    "key": f"phrase_{index}",
                    "prompt": f"Which phrase means \"{entry['meaning']}\"?",
                    "options": phrase_options(item["phrases"], index - 1),
                    "correct_answer": entry["phrase"],
                }
                for index, entry in enumerate(item["phrases"][:2], 1)
            ]
        },
    )

    write_yaml(lesson_dir / "conversation_coach_roleplay.yaml", roleplay_payload(item))

    (lesson_dir / "reading_support.md").write_text(
        "# Reading Support\n\n"
        "Read the Arabic phrases from right to left. Focus on recognizing the full phrase first, "
        "then identify the changing word.\n\n"
        + "\n".join(f"- {entry['phrase']} -> {entry['meaning']}" for entry in item["phrases"][:5])
        + "\n",
        encoding="utf-8",
    )

    (lesson_dir / "writing_support.md").write_text(
        "# Writing Support\n\n"
        "Copy the phrase by hand or type it slowly. Replace only the name, place, number, "
        "or object when the pattern is stable.\n\n"
        + "\n".join(f"- {entry['phrase']}" for entry in item["phrases"][:4])
        + "\n",
        encoding="utf-8",
    )

    write_yaml(
        lesson_dir / "audio_manifest.yaml",
        {
            "lesson_key": item["lesson_key"],
            "status": "not_generated",
            "provider": "elevenlabs",
            "model": "eleven_multilingual_v2",
            "default_voice_id": "multi_speaker",
            "assets": [],
        },
    )


def phrase_options(phrases: list[dict[str, str]], correct_index: int) -> list[str]:
    correct = phrases[correct_index]["phrase"]
    options = [correct]
    for entry in phrases:
        candidate = entry["phrase"]
        if candidate not in options:
            options.append(candidate)
        if len(options) == 3:
            break
    return options


def roleplay_payload(item: dict[str, Any]) -> dict[str, Any]:
    turns = []
    for index, entry in enumerate(item["phrases"][:3], 1):
        turns.append(
            {
                "coach": item["dialogue"][0][1] if index == 1 else f"استخدم: {entry['phrase']}",
                "hint": f"Jawab dengan pola: {entry['phrase']}",
                "sample_answer": entry["phrase"],
                "focus": entry["usage"],
                "expected_keywords": entry["phrase"].replace("؟", "").replace(".", "").split()[:3],
                "indonesian_explanation": entry["meaning"],
            }
        )

    return {
        "scenario_key": item["slug"].replace("arabic-", "arabic_").replace("-", "_"),
        "mode": "lesson_practice_coach",
        "level_code": "A1",
        "opening_line": item["dialogue"][0][1],
        "learner_goal": item["goal"],
        "max_turns": 4,
        "feedback_level": {"free": "basic", "pro": "detailed"},
        "turns": turns,
        "target_phrases": [entry["phrase"] for entry in item["phrases"][:4]],
        "rubric": {
            "speaking": {"minimum_score": 60},
            "relevance": {"minimum_score": 60},
            "grammar": {"minimum_score": 55},
        },
    }


def update_tracker() -> None:
    with TRACKER_PATH.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    rows_by_key = {(row["level"], row["unit"], row["lesson"]): row for row in rows}
    for unit in generated_units():
        for item in unit["lessons"]:
            key = ("arabic/A1", unit["unit_key"], item["lesson_key"])
            row = rows_by_key.get(key)
            if row is None:
                row = {field: "" for field in fieldnames}
                row.update({"level": key[0], "unit": key[1], "lesson": key[2]})
                rows.append(row)
            for column in TEXT_TRACKER_COLUMNS:
                row[column] = "done"
            row["audio_generated"] = "not_generated"
            row["publish_status"] = "beta"

    with TRACKER_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    update_content_plan()
    for unit in UNIT_PLANS:
        write_unit(unit)
    for unit in generated_units():
        for item in unit["lessons"]:
            write_lesson_files(unit, item)
    update_tracker()
    lesson_count = sum(len(unit["lessons"]) for unit in UNIT_PLANS)
    print(f"Generated Arabic A1 curriculum: {len(UNIT_PLANS)} units, {lesson_count} lessons")


if __name__ == "__main__":
    main()
