import { BookOpen, CircleCheck, Headphones, Mic, MessageCircle, PenLine, Repeat, Sparkles } from "lucide-react";

export const mission = {
  title: "Greeting & Introducing Yourself",
  lessonSlug: "saying-hello-and-goodbye",
  level: "A1",
  minutes: 8,
  goal: "Start and close a very simple English conversation.",
  prompt: "Say hello, introduce your name, and ask where your partner is from."
};

export const learningLoop = [
  { label: "Listen", icon: Headphones },
  { label: "Understand", icon: BookOpen },
  { label: "Repeat", icon: Repeat },
  { label: "Respond", icon: Mic },
  { label: "Converse", icon: MessageCircle },
  { label: "Feedback", icon: Sparkles }
];

export const plans = [
  {
    key: "free",
    name: "Free",
    price: "Rp0",
    cadence: "Selamanya",
    access: "Akses terbatas",
    coachAllowance: "Termasuk sesi coba Conversation Coach",
    description: "Coba beberapa lesson A1 dan feedback dasar sebelum upgrade.",
    features: ["Lesson A1 pilihan", "Conversation Check dasar", "Progress belajar dasar", "Coba praktik speaking"]
  },
  {
    key: "pro_1_month",
    name: "Pro 1 Month",
    price: "Rp49.000",
    cadence: "1 bulan",
    access: "Akses Pro 1 bulan",
    coachAllowance: "Termasuk kuota pendamping Conversation Coach bulanan",
    description: "Akses penuh ke kurikulum aktif, feedback detail, dan evaluasi level.",
    features: ["Semua lesson aktif", "Detailed Conversation Feedback", "Full A1 Conversation Test", "Skill report dan progress"]
  },
  {
    key: "pro_3_months",
    name: "Pro 3 Months",
    price: "Rp129.000",
    cadence: "3 bulan",
    access: "Akses Pro 3 bulan",
    coachAllowance: "Termasuk kuota pendamping Conversation Coach bulanan",
    description: "Paket lebih hemat untuk menyelesaikan A1 dengan ritme belajar rutin.",
    features: ["Semua lesson aktif", "Detailed Conversation Feedback", "Full A1 Conversation Test", "Pengingat renewal"]
  },
  {
    key: "pro_12_months",
    name: "Pro 12 Months",
    price: "Rp399.000",
    cadence: "12 bulan",
    access: "Akses Pro 12 bulan",
    coachAllowance: "Termasuk kuota pendamping Conversation Coach bulanan",
    description: "Best value untuk belajar konsisten, evaluasi level, dan lanjut ke path berikutnya.",
    features: ["Semua lesson aktif", "Skill reports", "Level evaluation", "Review plan personal"]
  }
];

export const topups = [
  { key: "topup_60", name: "Paket 60 menit tambahan", price: "Rp15.000", minutes: 60 },
  { key: "topup_200", name: "Paket 200 menit tambahan", price: "Rp39.000", minutes: 200 },
  { key: "topup_500", name: "Paket 500 menit tambahan", price: "Rp79.000", minutes: 500 }
];

const lessonSections = [
  { label: "Conversation Goal", icon: CircleCheck },
  { label: "Listen", icon: Headphones },
  { label: "Useful Phrases", icon: BookOpen },
  { label: "Speak Clearly", icon: Mic },
  { label: "Respond", icon: PenLine },
  { label: "Conversation Coach", icon: MessageCircle }
];

export const lessonCatalog = [
  {
    slug: "saying-hello-and-goodbye",
    title: "Saying Hello and Goodbye",
    unit: "Greeting & Introducing Yourself",
    conversationGoal: "Start and close a very simple English conversation.",
    setup: "Kamu bertemu seseorang di kelas online. Mulai dengan sapaan singkat, lalu tutup percakapan dengan sopan.",
    dialogue: [
      { speaker: "Alya", text: "Hi, good morning." },
      { speaker: "Ben", text: "Good morning. How are you?" },
      { speaker: "Alya", text: "I'm good, thank you. Nice to meet you." },
      { speaker: "Ben", text: "Nice to meet you too. See you later." },
      { speaker: "Alya", text: "See you." }
    ],
    translation: [
      "Hai, selamat pagi.",
      "Selamat pagi. Apa kabar?",
      "Aku baik, terima kasih. Senang bertemu denganmu.",
      "Senang bertemu denganmu juga. Sampai nanti.",
      "Sampai jumpa."
    ],
    phrases: [
      { phrase: "Good morning", meaning: "Selamat pagi", usage: "Use before noon." },
      { phrase: "How are you?", meaning: "Apa kabar?", usage: "A friendly opening question." },
      { phrase: "I'm good, thank you.", meaning: "Aku baik, terima kasih.", usage: "Simple polite answer." },
      { phrase: "Nice to meet you.", meaning: "Senang bertemu denganmu.", usage: "Use when meeting someone for the first time." },
      { phrase: "See you later.", meaning: "Sampai nanti.", usage: "Casual way to close a conversation." }
    ],
    grammar: "Use I am or I'm for simple personal responses: I'm good. I'm Fikri. I'm from Indonesia.",
    prompts: [
      "Say: Good morning. How are you?",
      "Answer: I'm good, thank you.",
      "Close the conversation with: See you later."
    ],
    quiz: [
      { question: "Which phrase is best for meeting someone for the first time?", answer: "Nice to meet you." },
      { question: "What does See you later mean?", answer: "Sampai nanti." }
    ],
    sections: lessonSections
  },
  {
    slug: "saying-your-name",
    title: "Saying Your Name",
    unit: "Greeting & Introducing Yourself",
    conversationGoal: "Say your name naturally and respond when someone introduces themselves.",
    setup: "Kamu masuk kelas online dan diminta memperkenalkan nama dengan kalimat pendek yang jelas.",
    dialogue: [
      { speaker: "Coach", text: "Hi, my name is Sara." },
      { speaker: "Learner", text: "Hi Sara. My name is Fikri." },
      { speaker: "Coach", text: "Nice to meet you, Fikri." },
      { speaker: "Learner", text: "Nice to meet you too." }
    ],
    translation: [
      "Hai, nama saya Sara.",
      "Hai Sara. Nama saya Fikri.",
      "Senang bertemu denganmu, Fikri.",
      "Senang bertemu denganmu juga."
    ],
    phrases: [
      { phrase: "My name is ...", meaning: "Nama saya ...", usage: "Clear, neutral way to say your name." },
      { phrase: "I'm ...", meaning: "Saya ...", usage: "Natural shorter form for introductions." },
      { phrase: "Nice to meet you too.", meaning: "Senang bertemu denganmu juga.", usage: "Use after someone says nice to meet you." },
      { phrase: "Please call me ...", meaning: "Panggil saya ...", usage: "Use when your nickname is easier." }
    ],
    grammar: "Use My name is + name for clear introductions. Use I'm + name for a shorter, more natural answer.",
    prompts: [
      "Say your name with: My name is ...",
      "Respond to: Nice to meet you.",
      "Say a nickname with: Please call me ..."
    ],
    quiz: [
      { question: "Which sentence is correct?", answer: "My name is Fikri." },
      { question: "What is a natural reply to Nice to meet you?", answer: "Nice to meet you too." }
    ],
    sections: lessonSections
  },
  {
    slug: "asking-someones-name",
    title: "Asking Someone's Name",
    unit: "Greeting & Introducing Yourself",
    conversationGoal: "Ask someone's name politely and confirm what you heard.",
    setup: "Kamu bertemu peserta baru di kelas. Tanyakan namanya, lalu ulangi nama itu dengan sopan.",
    dialogue: [
      { speaker: "Learner", text: "Hi. What's your name?" },
      { speaker: "Mina", text: "My name is Mina." },
      { speaker: "Learner", text: "Nice to meet you, Mina." },
      { speaker: "Mina", text: "Nice to meet you too." }
    ],
    translation: [
      "Hai. Siapa namamu?",
      "Nama saya Mina.",
      "Senang bertemu denganmu, Mina.",
      "Senang bertemu denganmu juga."
    ],
    phrases: [
      { phrase: "What's your name?", meaning: "Siapa namamu?", usage: "Common simple question." },
      { phrase: "May I know your name?", meaning: "Boleh tahu nama Anda?", usage: "More polite version." },
      { phrase: "Is it Mina?", meaning: "Apakah Mina?", usage: "Use to confirm a name." },
      { phrase: "Nice to meet you, ...", meaning: "Senang bertemu denganmu, ...", usage: "Add the person's name to sound attentive." }
    ],
    grammar: "Use What's your + noun for simple questions: What's your name? What's your job?",
    prompts: [
      "Ask: What's your name?",
      "Confirm the name with: Is it ...?",
      "Reply with: Nice to meet you, ..."
    ],
    quiz: [
      { question: "Which question asks for a name?", answer: "What's your name?" },
      { question: "Which phrase sounds more polite?", answer: "May I know your name?" }
    ],
    sections: lessonSections
  },
  {
    slug: "saying-where-you-are-from",
    title: "Saying Where You Are From",
    unit: "Greeting & Introducing Yourself",
    conversationGoal: "Say where you are from and ask the same question back.",
    setup: "Kamu melanjutkan perkenalan singkat. Jawab asalmu, lalu tanyakan balik agar percakapan berjalan.",
    dialogue: [
      { speaker: "Coach", text: "Where are you from?" },
      { speaker: "Learner", text: "I'm from Indonesia." },
      { speaker: "Coach", text: "Oh, nice." },
      { speaker: "Learner", text: "How about you?" }
    ],
    translation: [
      "Kamu berasal dari mana?",
      "Saya dari Indonesia.",
      "Oh, bagus.",
      "Kalau kamu?"
    ],
    phrases: [
      { phrase: "I'm from ...", meaning: "Saya dari ...", usage: "Simple answer for origin." },
      { phrase: "I live in ...", meaning: "Saya tinggal di ...", usage: "Use for current city." },
      { phrase: "How about you?", meaning: "Kalau kamu?", usage: "Ask the same question back." },
      { phrase: "I'm from Indonesia.", meaning: "Saya dari Indonesia.", usage: "A complete model answer." }
    ],
    grammar: "Use from for origin and in for current place: I'm from Indonesia. I live in Jakarta.",
    prompts: [
      "Answer: Where are you from?",
      "Say where you live with: I live in ...",
      "Ask back: How about you?"
    ],
    quiz: [
      { question: "Which sentence talks about origin?", answer: "I'm from Indonesia." },
      { question: "Which phrase keeps the conversation going?", answer: "How about you?" }
    ],
    sections: lessonSections
  },
  {
    slug: "first-conversation-mission",
    title: "First Conversation Mission",
    unit: "Greeting & Introducing Yourself",
    conversationGoal: "Combine greeting, name, origin, and a polite closing in one short conversation.",
    setup: "Ini misi gabungan Unit 1. Selesaikan percakapan pendek tanpa melihat contoh terlalu sering.",
    dialogue: [
      { speaker: "Learner", text: "Hi, good morning. My name is Fikri." },
      { speaker: "Coach", text: "Good morning, Fikri. Where are you from?" },
      { speaker: "Learner", text: "I'm from Indonesia. How about you?" },
      { speaker: "Coach", text: "I'm from Malaysia. Nice to meet you." },
      { speaker: "Learner", text: "Nice to meet you too. See you later." }
    ],
    translation: [
      "Hai, selamat pagi. Nama saya Fikri.",
      "Selamat pagi, Fikri. Kamu dari mana?",
      "Saya dari Indonesia. Kalau kamu?",
      "Saya dari Malaysia. Senang bertemu denganmu.",
      "Senang bertemu denganmu juga. Sampai nanti."
    ],
    phrases: [
      { phrase: "Good morning. My name is ...", meaning: "Selamat pagi. Nama saya ...", usage: "Open and introduce yourself." },
      { phrase: "Where are you from?", meaning: "Kamu dari mana?", usage: "Ask about origin." },
      { phrase: "How about you?", meaning: "Kalau kamu?", usage: "Return the question." },
      { phrase: "See you later.", meaning: "Sampai nanti.", usage: "Close the conversation." }
    ],
    grammar: "Keep A1 conversations short: greeting + name + origin + question back + closing.",
    prompts: [
      "Introduce yourself in two short sentences.",
      "Answer where you are from and ask back.",
      "Close with Nice to meet you too and See you later."
    ],
    quiz: [
      { question: "What should you say after someone says Nice to meet you?", answer: "Nice to meet you too." },
      { question: "Which question can you ask back after answering your origin?", answer: "How about you?" }
    ],
    sections: lessonSections
  },
  {
    slug: "spelling-your-name",
    title: "Spelling Your Name",
    unit: "Spelling, Numbers & Contact Details",
    conversationGoal: "Spell your name clearly when someone needs to write it down.",
    setup: "Kamu mendaftar di kelas online dan petugas perlu menulis namamu. Sebutkan namamu, lalu eja huruf demi huruf dengan jelas.",
    dialogue: [
      { speaker: "Officer", text: "Hi. What is your name?" },
      { speaker: "Dimas", text: "My name is Dimas." },
      { speaker: "Officer", text: "How do you spell it?" },
      { speaker: "Dimas", text: "It's spelled D-I-M-A-S." },
      { speaker: "Officer", text: "Thank you. Let me read it back. D-I-M-A-S." },
      { speaker: "Dimas", text: "That's right." }
    ],
    translation: [
      "Hai. Siapa namamu?",
      "Nama saya Dimas.",
      "Bagaimana cara mengejanya?",
      "Ejaannya D-I-M-A-S.",
      "Terima kasih. Saya ulangi ya. D-I-M-A-S.",
      "Betul."
    ],
    phrases: [
      { phrase: "How do you spell it?", meaning: "Bagaimana cara mengejanya?", usage: "Ask someone to spell a word or name." },
      { phrase: "Let me spell it for you.", meaning: "Biar saya ejakan untukmu.", usage: "Offer to spell your name." },
      { phrase: "It's spelled D-I-M-A-S.", meaning: "Ejaannya D-I-M-A-S.", usage: "Say each letter clearly, one by one." },
      { phrase: "Can you repeat that, please?", meaning: "Bisa diulang, tolong?", usage: "Ask for a repeat when you miss a letter." },
      { phrase: "That's right.", meaning: "Betul.", usage: "Confirm that the spelling is correct." }
    ],
    grammar: "Use How do you spell + it/that to ask about spelling. Use It's spelled + letters to answer: It's spelled D-I-M-A-S.",
    prompts: [
      "Say: My name is Dimas.",
      "Spell it: D-I-M-A-S.",
      "Confirm with: That's right."
    ],
    quiz: [
      { question: "Which question asks someone to spell a word?", answer: "How do you spell it?" },
      { question: "What does That's right mean?", answer: "Betul." }
    ],
    sections: lessonSections
  },
  {
    slug: "giving-phone-numbers",
    title: "Giving Phone Numbers",
    unit: "Spelling, Numbers & Contact Details",
    conversationGoal: "Give a phone number clearly and confirm it when someone reads it back.",
    setup: "Kamu mengisi formulir kelas online. Petugas meminta nomor teleponmu. Sebutkan angka dengan pelan, lalu konfirmasi saat petugas membacanya kembali.",
    dialogue: [
      { speaker: "Officer", text: "What is your phone number?" },
      { speaker: "Dimas", text: "It's zero eight one two, three four five six, seven eight nine zero." },
      { speaker: "Officer", text: "Let me check. Zero eight one two, three four five six, seven eight nine zero?" },
      { speaker: "Dimas", text: "Yes, that's correct." },
      { speaker: "Officer", text: "Thank you. We will send you a message." },
      { speaker: "Dimas", text: "Thank you." }
    ],
    translation: [
      "Berapa nomor teleponmu?",
      "Nomornya nol delapan satu dua, tiga empat lima enam, tujuh delapan sembilan nol.",
      "Saya cek ya. Nol delapan satu dua, tiga empat lima enam, tujuh delapan sembilan nol?",
      "Ya, itu benar.",
      "Terima kasih. Kami akan mengirim pesan kepadamu.",
      "Terima kasih."
    ],
    phrases: [
      { phrase: "What is your phone number?", meaning: "Berapa nomor teleponmu?", usage: "Ask for a phone number in a clear, direct way." },
      { phrase: "It's zero eight one two.", meaning: "Nomornya nol delapan satu dua.", usage: "Start giving a phone number." },
      { phrase: "Let me check.", meaning: "Saya cek ya.", usage: "Introduce a quick confirmation before repeating information." },
      { phrase: "Yes, that's correct.", meaning: "Ya, itu benar.", usage: "Confirm that the repeated information is right." },
      { phrase: "Can you repeat that, please?", meaning: "Bisa diulang, tolong?", usage: "Ask politely when you miss a number." }
    ],
    grammar: "Use What is your + noun? to ask for contact information. Use It's + number to answer: It's zero eight one two.",
    prompts: [
      "Say your phone number in small groups.",
      "Confirm with: Yes, that's correct.",
      "Ask for repetition with: Can you repeat that, please?"
    ],
    quiz: [
      { question: "Which question asks for a phone number?", answer: "What is your phone number?" },
      { question: "What does Yes, that's correct mean?", answer: "Ya, itu benar." }
    ],
    sections: lessonSections
  },
  {
    slug: "sharing-email-addresses",
    title: "Sharing Email Addresses",
    unit: "Spelling, Numbers & Contact Details",
    conversationGoal: "Share an email address slowly and spell the important parts.",
    setup: "Kamu ingin menerima informasi kelas lewat email. Petugas meminta alamat emailmu. Sebutkan alamat email dengan pelan, lalu eja bagian yang penting.",
    dialogue: [
      { speaker: "Officer", text: "What is your email address?" },
      { speaker: "Ben", text: "It's ben dot rama at example dot com." },
      { speaker: "Officer", text: "Can you spell that, please?" },
      { speaker: "Ben", text: "B-E-N dot R-A-M-A at example dot com." },
      { speaker: "Officer", text: "Thank you. Is that correct?" },
      { speaker: "Ben", text: "Yes, that's correct." }
    ],
    translation: [
      "Apa alamat emailmu?",
      "Alamatnya ben titik rama at example titik com.",
      "Bisa dieja, tolong?",
      "B-E-N titik R-A-M-A at example titik com.",
      "Terima kasih. Apakah itu benar?",
      "Ya, itu benar."
    ],
    phrases: [
      { phrase: "What is your email address?", meaning: "Apa alamat emailmu?", usage: "Ask for someone's email address." },
      { phrase: "It's ben dot rama at example dot com.", meaning: "Alamatnya ben titik rama at example titik com.", usage: "Say an email address slowly." },
      { phrase: "Can you spell that, please?", meaning: "Bisa dieja, tolong?", usage: "Ask someone to spell the email address." },
      { phrase: "Is that correct?", meaning: "Apakah itu benar?", usage: "Ask for confirmation after writing information." },
      { phrase: "Yes, that's correct.", meaning: "Ya, itu benar.", usage: "Confirm the email address is right." }
    ],
    grammar: "When saying an email address, use at for @ and dot for a period: ben dot rama at example dot com.",
    prompts: [
      "Say an email address using at and dot.",
      "Spell the name part of an email.",
      "Confirm with: Yes, that's correct."
    ],
    quiz: [
      { question: "Which question asks for an email address?", answer: "What is your email address?" },
      { question: "How do you say . in an email address?", answer: "dot" }
    ],
    sections: lessonSections
  },
  {
    slug: "asking-for-repetition",
    title: "Asking for Repetition",
    unit: "Spelling, Numbers & Contact Details",
    conversationGoal: "Ask someone to repeat a name, number, or email address politely.",
    setup: "Kamu tidak mendengar informasi dengan jelas. Daripada menebak, kamu meminta orang lain mengulang dengan sopan dan mengecek bagian yang kamu dengar.",
    dialogue: [
      { speaker: "Alya", text: "My phone number is zero eight one three, two two five five, nine zero one." },
      { speaker: "Ben", text: "Sorry, can you repeat that, please?" },
      { speaker: "Alya", text: "Sure. Zero eight one three, two two five five, nine zero one." },
      { speaker: "Ben", text: "Thank you. Did you say two two five five?" },
      { speaker: "Alya", text: "Yes, that's right." },
      { speaker: "Ben", text: "Got it. Thank you." }
    ],
    translation: [
      "Nomor telepon saya nol delapan satu tiga, dua dua lima lima, sembilan nol satu.",
      "Maaf, bisa diulang, tolong?",
      "Tentu. Nol delapan satu tiga, dua dua lima lima, sembilan nol satu.",
      "Terima kasih. Apakah kamu bilang dua dua lima lima?",
      "Ya, betul.",
      "Sudah saya mengerti. Terima kasih."
    ],
    phrases: [
      { phrase: "Sorry, can you repeat that, please?", meaning: "Maaf, bisa diulang, tolong?", usage: "Ask politely when you do not hear clearly." },
      { phrase: "Sure.", meaning: "Tentu.", usage: "Agree to repeat information." },
      { phrase: "Did you say two two five five?", meaning: "Apakah kamu bilang dua dua lima lima?", usage: "Check a specific part of what you heard." },
      { phrase: "Yes, that's right.", meaning: "Ya, betul.", usage: "Confirm that the listener heard correctly." },
      { phrase: "Got it.", meaning: "Sudah saya mengerti.", usage: "Show that you understand now." }
    ],
    grammar: "Use Can you repeat that, please? when you need to hear something again. Use Did you say + detail? to check one part.",
    prompts: [
      "Ask for repetition politely.",
      "Check one detail with: Did you say ...?",
      "Show understanding with: Got it. Thank you."
    ],
    quiz: [
      { question: "Which sentence politely asks someone to repeat?", answer: "Can you repeat that, please?" },
      { question: "What is Did you say ...? used for?", answer: "Checking a detail." }
    ],
    sections: lessonSections
  },
  {
    slug: "contact-details-mission",
    title: "Contact Details Mission",
    unit: "Spelling, Numbers & Contact Details",
    conversationGoal: "Share your name, spelling, phone number, and email address in one simple conversation.",
    setup: "Ini adalah misi akhir unit. Kamu memberikan detail kontak lengkap untuk pendaftaran kelas: nama, ejaan nama, nomor telepon, dan alamat email.",
    dialogue: [
      { speaker: "Officer", text: "Hi. I need your contact details." },
      { speaker: "Dimas", text: "Sure. My name is Dimas." },
      { speaker: "Officer", text: "How do you spell your name?" },
      { speaker: "Dimas", text: "D-I-M-A-S." },
      { speaker: "Officer", text: "What is your phone number?" },
      { speaker: "Dimas", text: "It's zero eight one two, three four five six, seven eight nine zero." },
      { speaker: "Officer", text: "And your email address?" },
      { speaker: "Dimas", text: "It's dimas at example dot com." },
      { speaker: "Officer", text: "Thank you. Is everything correct?" },
      { speaker: "Dimas", text: "Yes, everything is correct." }
    ],
    translation: [
      "Hai. Saya perlu detail kontakmu.",
      "Tentu. Nama saya Dimas.",
      "Bagaimana kamu mengeja namamu?",
      "D-I-M-A-S.",
      "Berapa nomor teleponmu?",
      "Nomornya nol delapan satu dua, tiga empat lima enam, tujuh delapan sembilan nol.",
      "Dan alamat emailmu?",
      "Alamatnya dimas at example titik com.",
      "Terima kasih. Apakah semuanya benar?",
      "Ya, semuanya benar."
    ],
    phrases: [
      { phrase: "I need your contact details.", meaning: "Saya perlu detail kontakmu.", usage: "Start a request for name, phone number, and email." },
      { phrase: "How do you spell your name?", meaning: "Bagaimana kamu mengeja namamu?", usage: "Ask someone to spell their name." },
      { phrase: "And your email address?", meaning: "Dan alamat emailmu?", usage: "Ask the next contact detail after another question." },
      { phrase: "Is everything correct?", meaning: "Apakah semuanya benar?", usage: "Check all contact information at the end." },
      { phrase: "Yes, everything is correct.", meaning: "Ya, semuanya benar.", usage: "Confirm all information is correct." }
    ],
    grammar: "Use short follow-up questions when the topic is clear: And your phone number? And your email address?",
    prompts: [
      "Share your name and spell it.",
      "Give your phone number and email address.",
      "Confirm with: Yes, everything is correct."
    ],
    quiz: [
      { question: "Which phrase asks for all contact information?", answer: "I need your contact details." },
      { question: "What does Is everything correct? mean?", answer: "Apakah semuanya benar?" }
    ],
    sections: lessonSections
  },
  {
    slug: "telling-the-time",
    title: "Telling the Time",
    unit: "Daily Routine & Time",
    conversationGoal: "Ask and answer a simple question about time.",
    setup: "Kamu ingin tahu jam mulai kelas online. Tanyakan waktunya, lalu cek apakah itu pagi, siang, atau malam.",
    dialogue: [
      { speaker: "Alya", text: "What time is the class?" },
      { speaker: "Ben", text: "It's at nine o'clock." },
      { speaker: "Alya", text: "In the morning?" },
      { speaker: "Ben", text: "Yes, in the morning." },
      { speaker: "Alya", text: "Thank you." },
      { speaker: "Ben", text: "You're welcome." }
    ],
    translation: [
      "Jam berapa kelasnya?",
      "Kelasnya jam sembilan.",
      "Pagi?",
      "Ya, pagi.",
      "Terima kasih.",
      "Sama-sama."
    ],
    phrases: [
      { phrase: "What time is the class?", meaning: "Jam berapa kelasnya?", usage: "Ask about the time of an event." },
      { phrase: "It's at nine o'clock.", meaning: "Jam sembilan.", usage: "Answer with a clear time." },
      { phrase: "In the morning?", meaning: "Pagi?", usage: "Check the part of the day." },
      { phrase: "Yes, in the morning.", meaning: "Ya, pagi.", usage: "Confirm the time of day." },
      { phrase: "You're welcome.", meaning: "Sama-sama.", usage: "Reply after someone says thank you." }
    ],
    grammar: "Use What time is + event? to ask about time. Use at + time to answer: It's at nine o'clock.",
    prompts: [
      "Ask: What time is the class?",
      "Answer with: It's at nine o'clock.",
      "Check with: In the morning?"
    ],
    quiz: [
      { question: "Which question asks about time?", answer: "What time is the class?" },
      { question: "Which word comes before a time?", answer: "at" }
    ],
    sections: lessonSections
  },
  {
    slug: "talking-about-daily-routines",
    title: "Talking About Daily Routines",
    unit: "Daily Routine & Time",
    conversationGoal: "Say a simple daily routine with time words.",
    setup: "Kamu mengobrol dengan teman kelas tentang kebiasaan pagi. Sebutkan kegiatan sederhana dan kapan kamu melakukannya.",
    dialogue: [
      { speaker: "Alya", text: "What do you do in the morning?" },
      { speaker: "Ben", text: "I wake up at six." },
      { speaker: "Alya", text: "What do you do after that?" },
      { speaker: "Ben", text: "I study English at seven." },
      { speaker: "Alya", text: "Nice. Do you work in the afternoon?" },
      { speaker: "Ben", text: "Yes, I work at one." }
    ],
    translation: [
      "Apa yang kamu lakukan di pagi hari?",
      "Saya bangun jam enam.",
      "Apa yang kamu lakukan setelah itu?",
      "Saya belajar bahasa Inggris jam tujuh.",
      "Bagus. Apakah kamu bekerja siang hari?",
      "Ya, saya bekerja jam satu."
    ],
    phrases: [
      { phrase: "What do you do in the morning?", meaning: "Apa yang kamu lakukan di pagi hari?", usage: "Ask about a morning routine." },
      { phrase: "I wake up at six.", meaning: "Saya bangun jam enam.", usage: "Say when you wake up." },
      { phrase: "What do you do after that?", meaning: "Apa yang kamu lakukan setelah itu?", usage: "Ask for the next routine step." },
      { phrase: "I study English at seven.", meaning: "Saya belajar bahasa Inggris jam tujuh.", usage: "Say a study routine." },
      { phrase: "I work at one.", meaning: "Saya bekerja jam satu.", usage: "Say a work routine." }
    ],
    grammar: "Use I + verb + at + time for a simple routine: I wake up at six. Use after that for the next step.",
    prompts: [
      "Say when you wake up.",
      "Say what you do after that.",
      "Say when you work or study."
    ],
    quiz: [
      { question: "Which sentence talks about a routine?", answer: "I wake up at six." },
      { question: "What does after that mean?", answer: "setelah itu" }
    ],
    sections: lessonSections
  },
  {
    slug: "days-and-simple-schedules",
    title: "Days and Simple Schedules",
    unit: "Daily Routine & Time",
    conversationGoal: "Talk about simple days and class schedules.",
    setup: "Kamu ingin tahu hari apa kelas berlangsung. Tanyakan jadwal sederhana, lalu ulangi hari dan jamnya.",
    dialogue: [
      { speaker: "Alya", text: "When is the English class?" },
      { speaker: "Ben", text: "It's on Monday and Wednesday." },
      { speaker: "Alya", text: "What time?" },
      { speaker: "Ben", text: "At seven in the evening." },
      { speaker: "Alya", text: "Great. See you on Monday." },
      { speaker: "Ben", text: "See you." }
    ],
    translation: [
      "Kapan kelas bahasa Inggrisnya?",
      "Kelasnya hari Senin dan Rabu.",
      "Jam berapa?",
      "Jam tujuh malam.",
      "Bagus. Sampai jumpa hari Senin.",
      "Sampai jumpa."
    ],
    phrases: [
      { phrase: "When is the English class?", meaning: "Kapan kelas bahasa Inggrisnya?", usage: "Ask about the day or schedule." },
      { phrase: "It's on Monday and Wednesday.", meaning: "Kelasnya hari Senin dan Rabu.", usage: "Answer with class days." },
      { phrase: "What time?", meaning: "Jam berapa?", usage: "Ask a short follow-up about time." },
      { phrase: "At seven in the evening.", meaning: "Jam tujuh malam.", usage: "Answer with time of day." },
      { phrase: "See you on Monday.", meaning: "Sampai jumpa hari Senin.", usage: "Close with the day you will meet." }
    ],
    grammar: "Use on + day for schedules and at + time for clock time: on Monday at seven.",
    prompts: [
      "Ask when the English class is.",
      "Answer with days: on Monday and Wednesday.",
      "Answer the time: at seven in the evening."
    ],
    quiz: [
      { question: "Which word comes before Monday?", answer: "on" },
      { question: "Which short question asks about time?", answer: "What time?" }
    ],
    sections: lessonSections
  },
  {
    slug: "asking-when-something-happens",
    title: "Asking When Something Happens",
    unit: "Daily Routine & Time",
    conversationGoal: "Ask when a simple event happens and confirm the details.",
    setup: "Kamu perlu ikut meeting singkat. Tanyakan kapan meeting berlangsung, apakah online, dan konfirmasi waktunya.",
    dialogue: [
      { speaker: "Dimas", text: "When is the meeting?" },
      { speaker: "Alya", text: "It's tomorrow at ten." },
      { speaker: "Dimas", text: "Is it online?" },
      { speaker: "Alya", text: "Yes, it is online." },
      { speaker: "Dimas", text: "Tomorrow at ten. Is that right?" },
      { speaker: "Alya", text: "Yes, that's right." }
    ],
    translation: [
      "Kapan meetingnya?",
      "Besok jam sepuluh.",
      "Apakah online?",
      "Ya, online.",
      "Besok jam sepuluh. Benar begitu?",
      "Ya, betul."
    ],
    phrases: [
      { phrase: "When is the meeting?", meaning: "Kapan meetingnya?", usage: "Ask when an event happens." },
      { phrase: "It's tomorrow at ten.", meaning: "Besok jam sepuluh.", usage: "Answer with day and time." },
      { phrase: "Is it online?", meaning: "Apakah online?", usage: "Ask about the meeting format." },
      { phrase: "Is that right?", meaning: "Benar begitu?", usage: "Check that your understanding is correct." },
      { phrase: "Yes, that's right.", meaning: "Ya, betul.", usage: "Confirm the detail." }
    ],
    grammar: "Use When is + event? to ask about timing. Use Is it + online/today/tomorrow? for yes/no questions.",
    prompts: [
      "Ask when the meeting is.",
      "Ask if it is online.",
      "Confirm with: Is that right?"
    ],
    quiz: [
      { question: "Which question asks when an event happens?", answer: "When is the meeting?" },
      { question: "Which sentence asks if something is online?", answer: "Is it online?" }
    ],
    sections: lessonSections
  },
  {
    slug: "routine-conversation-mission",
    title: "Routine Conversation Mission",
    unit: "Daily Routine & Time",
    conversationGoal: "Combine time, routine, days, and schedule questions in one simple conversation.",
    setup: "Ini misi akhir unit. Kamu berbicara tentang rutinitas pagi, jadwal belajar, hari kelas, dan waktu meeting sederhana.",
    dialogue: [
      { speaker: "Alya", text: "Hi, Ben. What time do you wake up?" },
      { speaker: "Ben", text: "I wake up at six." },
      { speaker: "Alya", text: "When do you study English?" },
      { speaker: "Ben", text: "I study on Monday and Wednesday at seven." },
      { speaker: "Alya", text: "Is the class online?" },
      { speaker: "Ben", text: "Yes, it is online." },
      { speaker: "Alya", text: "Great. See you on Monday." },
      { speaker: "Ben", text: "See you." }
    ],
    translation: [
      "Hai, Ben. Jam berapa kamu bangun?",
      "Saya bangun jam enam.",
      "Kapan kamu belajar bahasa Inggris?",
      "Saya belajar hari Senin dan Rabu jam tujuh.",
      "Apakah kelasnya online?",
      "Ya, online.",
      "Bagus. Sampai jumpa hari Senin.",
      "Sampai jumpa."
    ],
    phrases: [
      { phrase: "What time do you wake up?", meaning: "Jam berapa kamu bangun?", usage: "Ask about a routine time." },
      { phrase: "I wake up at six.", meaning: "Saya bangun jam enam.", usage: "Say a morning routine." },
      { phrase: "When do you study English?", meaning: "Kapan kamu belajar bahasa Inggris?", usage: "Ask about a study schedule." },
      { phrase: "I study on Monday and Wednesday at seven.", meaning: "Saya belajar hari Senin dan Rabu jam tujuh.", usage: "Give days and time together." },
      { phrase: "Is the class online?", meaning: "Apakah kelasnya online?", usage: "Ask about class format." }
    ],
    grammar: "Combine on + day and at + time in one sentence: I study on Monday at seven.",
    prompts: [
      "Say your wake-up time.",
      "Say your study schedule.",
      "Ask if the class is online."
    ],
    quiz: [
      { question: "Which sentence uses day and time correctly?", answer: "I study on Monday at seven." },
      { question: "Which question asks about routine time?", answer: "What time do you wake up?" }
    ],
    sections: lessonSections
  }
];

export const lessonsBySlug = Object.fromEntries(lessonCatalog.map((item) => [item.slug, item]));

export const course = {
  slug: "english-a1-start-simple-conversations",
  level: "A1",
  title: "Start Simple Conversations",
  outcome: "Start simple conversations with greetings, introductions, daily routines, and basic questions.",
  units: [
    {
      title: "Greeting & Introducing Yourself",
      outcome: "Greet, introduce yourself, ask someone's name, say where you are from, and complete a first short conversation.",
      progress: 0,
      lessons: lessonCatalog
        .filter((item) => item.unit === "Greeting & Introducing Yourself")
        .map((item) => ({
          slug: item.slug,
          title: item.title,
          status: "published",
          minutes: item.slug === "first-conversation-mission" ? 10 : 8
        }))
    },
    {
      title: "Spelling, Numbers & Contact Details",
      outcome: "Spell your name, share numbers and contact details, and ask for repetition.",
      progress: 0,
      lessons: lessonCatalog
        .filter((item) => item.unit === "Spelling, Numbers & Contact Details")
        .map((item) => ({
          slug: item.slug,
          title: item.title,
          status: "published",
          minutes: 8
        }))
    },
    {
      title: "Daily Routine & Time",
      outcome: "Talk about simple routines, days, class schedules, and event times.",
      progress: 0,
      lessons: lessonCatalog
        .filter((item) => item.unit === "Daily Routine & Time")
        .map((item) => ({
          slug: item.slug,
          title: item.title,
          status: "published",
          minutes: item.slug === "routine-conversation-mission" ? 10 : 8
        }))
    },
    {
      title: "Family, Friends, and Simple Questions",
      outcome: "Ask and answer simple personal questions.",
      progress: 0,
      lessons: []
    },
    {
      title: "Daily Places and Situations",
      outcome: "Handle food, shopping, and direction situations.",
      progress: 0,
      lessons: []
    }
  ]
};

export const lesson = lessonCatalog[0];
