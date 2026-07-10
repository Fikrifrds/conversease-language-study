export type EnglishSpeakingPage = {
  slug: string;
  title: string;
  description: string;
  level: string;
  context: string;
  outcome: string;
  dialogue: Array<{ speaker: string; text: string }>;
  phrases: Array<{ phrase: string; meaning: string }>;
  challenge: string;
  lessonSlug: string;
  lessonTitle: string;
};

// Curated editorial pages, not generated keyword variants. Every page has a
// distinct learner intent, a useful example, and a clear path into practice.
export const englishSpeakingPages: EnglishSpeakingPage[] = [
  {
    slug: "introduce-yourself-in-english",
    title: "How to Introduce Yourself in English",
    description: "Practice a short, natural English introduction with listening, useful phrases, and speaking prompts.",
    level: "A1",
    context: "Meeting someone for the first time at a class, event, or workplace.",
    outcome: "Introduce your name and origin, ask a question back, and close politely.",
    dialogue: [
      { speaker: "Raka", text: "Hi, my name is Raka. What is your name?" },
      { speaker: "Adi", text: "Hi Raka. I'm Adi. Nice to meet you." },
      { speaker: "Raka", text: "Nice to meet you too. I'm from Indonesia." }
    ],
    phrases: [
      { phrase: "My name is ...", meaning: "Nama saya ..." },
      { phrase: "Nice to meet you.", meaning: "Senang bertemu denganmu." },
      { phrase: "Where are you from?", meaning: "Kamu berasal dari mana?" }
    ],
    challenge: "Record a 20-second introduction without reading a full script.",
    lessonSlug: "first-conversation-mission",
    lessonTitle: "First Conversation Mission"
  },
  {
    slug: "talk-about-your-daily-routine",
    title: "Talk About Your Daily Routine in English",
    description: "Learn to describe your morning routine and ask about someone else's day in simple English.",
    level: "A1",
    context: "Making small talk about what you usually do each day.",
    outcome: "Say three routine actions with time words and ask a follow-up question.",
    dialogue: [
      { speaker: "Ben", text: "What time do you get up?" },
      { speaker: "Dimas", text: "I get up at six. I have breakfast at seven." },
      { speaker: "Ben", text: "What do you do after breakfast?" }
    ],
    phrases: [
      { phrase: "I usually ...", meaning: "Saya biasanya ..." },
      { phrase: "After that, I ...", meaning: "Setelah itu, saya ..." },
      { phrase: "What time do you ...?", meaning: "Jam berapa kamu ...?" }
    ],
    challenge: "Speak about your morning in three connected sentences.",
    lessonSlug: "talking-about-daily-routines",
    lessonTitle: "Talking About Daily Routines"
  },
  {
    slug: "order-food-and-drinks-in-english",
    title: "Order Food and Drinks in English",
    description: "Practice ordering a simple drink politely and responding to a cafe worker.",
    level: "A1",
    context: "Ordering at a cafe when you need a clear, short exchange.",
    outcome: "Order an item, answer a simple follow-up, and say thank you.",
    dialogue: [
      { speaker: "Staff", text: "What would you like?" },
      { speaker: "Dimas", text: "I'd like an iced tea, please." },
      { speaker: "Staff", text: "Anything else?" },
      { speaker: "Dimas", text: "No, thank you." }
    ],
    phrases: [
      { phrase: "I'd like ..., please.", meaning: "Saya mau ..., tolong." },
      { phrase: "Anything else?", meaning: "Ada lagi?" },
      { phrase: "No, thank you.", meaning: "Tidak, terima kasih." }
    ],
    challenge: "Roleplay the order twice: once slowly, then at a natural pace.",
    lessonSlug: "ordering-a-drink",
    lessonTitle: "Ordering a Drink"
  },
  {
    slug: "ask-for-directions-in-english",
    title: "Ask for Directions in English",
    description: "Build confidence asking where a place is and understanding a short direction.",
    level: "A1",
    context: "Finding a station, shop, or public place in an unfamiliar area.",
    outcome: "Ask for a location, understand one direction, and confirm the destination.",
    dialogue: [
      { speaker: "Visitor", text: "Excuse me. Where is the station?" },
      { speaker: "Local", text: "It's next to the bank." },
      { speaker: "Visitor", text: "Next to the bank? Thank you." }
    ],
    phrases: [
      { phrase: "Excuse me. Where is ...?", meaning: "Permisi. Di mana ...?" },
      { phrase: "It's next to ...", meaning: "Letaknya di sebelah ..." },
      { phrase: "Could you say that again?", meaning: "Bisa diulangi?" }
    ],
    challenge: "Ask for two different places using the same conversation pattern.",
    lessonSlug: "asking-where-a-place-is",
    lessonTitle: "Asking Where a Place Is"
  },
  {
    slug: "ask-about-prices-in-english",
    title: "Ask About Prices in English",
    description: "Practice asking how much something costs and responding naturally in a shop.",
    level: "A1",
    context: "Checking the price before choosing a simple item.",
    outcome: "Ask the price, understand the answer, and decide politely.",
    dialogue: [
      { speaker: "Customer", text: "How much is this shirt?" },
      { speaker: "Staff", text: "It's twenty dollars." },
      { speaker: "Customer", text: "Okay. I'll take it, please." }
    ],
    phrases: [
      { phrase: "How much is this?", meaning: "Berapa harganya?" },
      { phrase: "It's ... dollars.", meaning: "Harganya ... dolar." },
      { phrase: "I'll take it.", meaning: "Saya ambil." }
    ],
    challenge: "Ask about three items and respond to each price without translating first.",
    lessonSlug: "asking-about-prices",
    lessonTitle: "Asking About Prices"
  },
  {
    slug: "say-what-you-do-in-english",
    title: "Say What You Do in English",
    description: "Learn a natural way to talk about your work or studies and ask the same question back.",
    level: "A1",
    context: "Making a simple introduction at work, school, or a social event.",
    outcome: "Say what you do, add one detail, and keep the conversation moving.",
    dialogue: [
      { speaker: "Omar", text: "What do you do?" },
      { speaker: "Dimas", text: "I'm a designer. I work with a small team." },
      { speaker: "Omar", text: "That sounds interesting. What about you?" }
    ],
    phrases: [
      { phrase: "I'm a ...", meaning: "Saya seorang ..." },
      { phrase: "I work with ...", meaning: "Saya bekerja dengan ..." },
      { phrase: "What about you?", meaning: "Kalau kamu?" }
    ],
    challenge: "Give a short work or study introduction and ask one follow-up question.",
    lessonSlug: "saying-what-you-do",
    lessonTitle: "Saying What You Do"
  },
  {
    slug: "join-a-meeting-in-english",
    title: "Join a Meeting in English",
    description: "Practice entering a simple work conversation, giving an update, and asking for clarification.",
    level: "B1",
    context: "Joining a short meeting when you need to contribute clearly.",
    outcome: "Give a brief update, ask a useful clarification question, and confirm a deadline.",
    dialogue: [
      { speaker: "Faris", text: "Quick update on the report?" },
      { speaker: "Dimas", text: "I'm making good progress. I'm almost done with the summary." },
      { speaker: "Faris", text: "Please update the risk section too." },
      { speaker: "Dimas", text: "Could you clarify which risks you want me to focus on?" }
    ],
    phrases: [
      { phrase: "I'm making good progress.", meaning: "Progress saya berjalan baik." },
      { phrase: "Could you clarify ...?", meaning: "Bisa diperjelas ...?" },
      { phrase: "Just to confirm ...", meaning: "Untuk memastikan ..." }
    ],
    challenge: "Give a 30-second project update and ask one clarification question.",
    lessonSlug: "joining-a-simple-meeting",
    lessonTitle: "Joining a Simple Meeting"
  },
  {
    slug: "ask-for-clarification-in-english",
    title: "Ask for Clarification in English",
    description: "Learn polite phrases for checking meaning when a workplace instruction is unclear.",
    level: "B1",
    context: "A colleague gives an instruction and you need to confirm what they mean.",
    outcome: "Pause the conversation politely, ask a precise question, and restate your understanding.",
    dialogue: [
      { speaker: "Manager", text: "Please send the revised file before lunch." },
      { speaker: "Dimas", text: "Just to clarify, do you mean the budget file or the full report?" },
      { speaker: "Manager", text: "The budget file, please." },
      { speaker: "Dimas", text: "Got it. I'll send it before lunch." }
    ],
    phrases: [
      { phrase: "Just to clarify ...", meaning: "Untuk memperjelas ..." },
      { phrase: "Do you mean ...?", meaning: "Maksudnya ...?" },
      { phrase: "Got it. I'll ...", meaning: "Mengerti. Saya akan ..." }
    ],
    challenge: "Ask for clarification without apologizing repeatedly or switching to Indonesian.",
    lessonSlug: "asking-for-clarification",
    lessonTitle: "Asking for Clarification"
  },
  {
    slug: "travel-english-for-transport",
    title: "Travel English for Tickets and Transport",
    description: "Practice buying a ticket, confirming travel details, and asking a driver for help.",
    level: "A2",
    context: "Moving through a station and continuing to your hotel.",
    outcome: "Handle two connected travel exchanges with clear requests and confirmations.",
    dialogue: [
      { speaker: "Staff", text: "One-way or round-trip?" },
      { speaker: "Traveler", text: "One-way, please. Which platform?" },
      { speaker: "Staff", text: "Platform two." },
      { speaker: "Driver", text: "Where to?" },
      { speaker: "Traveler", text: "Can you take me to my hotel, please?" }
    ],
    phrases: [
      { phrase: "One-way, please.", meaning: "Sekali jalan, tolong." },
      { phrase: "Which platform?", meaning: "Peron berapa?" },
      { phrase: "Can you take me to ...?", meaning: "Bisa antar saya ke ...?" }
    ],
    challenge: "Complete the ticket and driver roleplay with no written script.",
    lessonSlug: "transport-mission",
    lessonTitle: "Transport Mission"
  },
  {
    slug: "make-small-talk-in-english",
    title: "Make Small Talk in English",
    description: "Practice keeping a short social conversation going with questions, reactions, and a simple plan.",
    level: "A2",
    context: "Talking with someone new before deciding what to do together.",
    outcome: "Share a preference, react naturally, ask a follow-up, and suggest a plan.",
    dialogue: [
      { speaker: "Sara", text: "Do you like live music?" },
      { speaker: "Arif", text: "Yes, I do. I saw a band last weekend." },
      { speaker: "Sara", text: "That sounds fun. Would you like to go to a concert this Friday?" }
    ],
    phrases: [
      { phrase: "Yes, I do. I ...", meaning: "Ya. Saya ..." },
      { phrase: "That sounds fun.", meaning: "Kedengarannya menyenangkan." },
      { phrase: "Would you like to ...?", meaning: "Maukah kamu ...?" }
    ],
    challenge: "Keep the conversation going for three turns by asking a follow-up question.",
    lessonSlug: "small-talk-mission",
    lessonTitle: "Small Talk Mission"
  }
];

export const englishSpeakingPagesBySlug = Object.fromEntries(
  englishSpeakingPages.map((page) => [page.slug, page])
) as Record<string, EnglishSpeakingPage>;
