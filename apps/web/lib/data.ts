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
      { speaker: "Dimas", text: "D-I-M-A-S. Dimas." },
      { speaker: "Officer", text: "Thank you. Let me read it back. D-I-M-A-S." },
      { speaker: "Dimas", text: "That's right." }
    ],
    translation: [
      "Hai. Siapa namamu?",
      "Nama saya Dimas.",
      "Bagaimana cara mengejanya?",
      "D-I-M-A-S. Dimas.",
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
    grammar: "Use How do you spell + it/that to ask about spelling: How do you spell it? How do you spell that?",
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
      title: "Talk About Yourself",
      outcome: "Talk about job, home, routine, and hobbies.",
      progress: 0,
      lessons: []
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
