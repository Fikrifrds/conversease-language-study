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
    description: "Coba beberapa lesson awal dan feedback dasar sebelum upgrade.",
    features: ["Lesson pilihan", "Conversation Check dasar", "Progress belajar dasar", "Coba praktik speaking"]
  },
  {
    key: "pro_1_month",
    name: "Pro 1 Month",
    price: "Rp49.000",
    cadence: "1 bulan",
    access: "Pro All Access 1 bulan",
    coachAllowance: "Termasuk kuota pendamping Conversation Coach bulanan",
    description: "Akses penuh ke English dan Arabic, feedback detail, evaluasi level, dan progress report.",
    features: ["English track lengkap", "Arabic track lengkap", "Detailed Conversation Feedback", "Skill report dan progress"]
  },
  {
    key: "pro_3_months",
    name: "Pro 3 Months",
    price: "Rp129.000",
    cadence: "3 bulan",
    access: "Pro All Access 3 bulan",
    coachAllowance: "Termasuk kuota pendamping Conversation Coach bulanan",
    description: "Paket lebih hemat untuk menyelesaikan satu track dengan ritme belajar rutin.",
    features: ["English track lengkap", "Arabic track lengkap", "Detailed Conversation Feedback", "Pengingat renewal"]
  },
  {
    key: "pro_12_months",
    name: "Pro 12 Months",
    price: "Rp399.000",
    cadence: "12 bulan",
    access: "Pro All Access 12 bulan",
    coachAllowance: "Termasuk kuota pendamping Conversation Coach bulanan",
    description: "Best value untuk belajar konsisten lintas track, evaluasi level, dan review plan.",
    features: ["English track lengkap", "Arabic track lengkap", "Skill reports", "Review plan personal"]
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
  { label: "Vocabulary", icon: BookOpen },
  { label: "Speak Clearly", icon: Mic },
  { label: "Respond", icon: PenLine },
  { label: "Conversation Coach", icon: MessageCircle }
];

// GENERATED — do not edit by hand. Edit the curriculum under
// content/curriculum/<LANGUAGE>/<LEVEL>, then run:
//   PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_web_lesson_data.py
export const lessonCatalog = [
  // <generated:lessons>
    {
      slug: "saying-hello-and-goodbye",
      language: "english",
      languageLabel: "English",
      title: "Saying Hello and Goodbye",
      unit: "Greeting & Introducing Yourself",
      conversationGoal: "Start and close a very simple English conversation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying Hello and Goodbye di Indonesia.", caption: "Konteks percakapan nyata: Saying Hello and Goodbye." }
      },
      sections: lessonSections
    },
    {
      slug: "saying-your-name",
      language: "english",
      languageLabel: "English",
      title: "Saying Your Name",
      unit: "Greeting & Introducing Yourself",
      conversationGoal: "Say your name naturally and respond when someone introduces themselves.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying Your Name di Indonesia.", caption: "Konteks percakapan nyata: Saying Your Name." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-someones-name",
      language: "english",
      languageLabel: "English",
      title: "Asking Someone's Name",
      unit: "Greeting & Introducing Yourself",
      conversationGoal: "Ask someone's name politely and confirm what you heard.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking Someone's Name di Indonesia.", caption: "Konteks percakapan nyata: Asking Someone's Name." }
      },
      sections: lessonSections
    },
    {
      slug: "saying-where-you-are-from",
      language: "english",
      languageLabel: "English",
      title: "Saying Where You Are From",
      unit: "Greeting & Introducing Yourself",
      conversationGoal: "Say where you are from and ask the same question back.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying Where You Are From di Indonesia.", caption: "Konteks percakapan nyata: Saying Where You Are From." }
      },
      sections: lessonSections
    },
    {
      slug: "first-conversation-mission",
      language: "english",
      languageLabel: "English",
      title: "First Conversation Mission",
      unit: "Greeting & Introducing Yourself",
      conversationGoal: "Combine greeting, name, origin, and a polite closing in one short conversation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks First Conversation Mission di Indonesia.", caption: "Konteks percakapan nyata: First Conversation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "spelling-your-name",
      language: "english",
      languageLabel: "English",
      title: "Spelling Your Name",
      unit: "Spelling, Numbers & Contact Details",
      conversationGoal: "Spell your name clearly when someone needs to write it down.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Spelling Your Name di Indonesia.", caption: "Konteks percakapan nyata: Spelling Your Name." }
      },
      sections: lessonSections
    },
    {
      slug: "giving-phone-numbers",
      language: "english",
      languageLabel: "English",
      title: "Giving Phone Numbers",
      unit: "Spelling, Numbers & Contact Details",
      conversationGoal: "Give a phone number clearly and confirm it when someone reads it back.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Giving Phone Numbers di Indonesia.", caption: "Konteks percakapan nyata: Giving Phone Numbers." }
      },
      sections: lessonSections
    },
    {
      slug: "sharing-email-addresses",
      language: "english",
      languageLabel: "English",
      title: "Sharing Email Addresses",
      unit: "Spelling, Numbers & Contact Details",
      conversationGoal: "Share an email address slowly and spell the important parts.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Sharing Email Addresses di Indonesia.", caption: "Konteks percakapan nyata: Sharing Email Addresses." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-for-repetition",
      language: "english",
      languageLabel: "English",
      title: "Asking for Repetition",
      unit: "Spelling, Numbers & Contact Details",
      conversationGoal: "Ask someone to repeat a name, number, or email address politely.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for Repetition di Indonesia.", caption: "Konteks percakapan nyata: Asking for Repetition." }
      },
      sections: lessonSections
    },
    {
      slug: "contact-details-mission",
      language: "english",
      languageLabel: "English",
      title: "Contact Details Mission",
      unit: "Spelling, Numbers & Contact Details",
      conversationGoal: "Share your name, spelling, phone number, and email address in one simple conversation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Contact Details Mission di Indonesia.", caption: "Konteks percakapan nyata: Contact Details Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "telling-the-time",
      language: "english",
      languageLabel: "English",
      title: "Telling the Time",
      unit: "Daily Routine & Time",
      conversationGoal: "Learners can ask and answer a simple question about time.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Telling the Time di Indonesia.", caption: "Konteks percakapan nyata: Telling the Time." }
      },
      sections: lessonSections
    },
    {
      slug: "talking-about-daily-routines",
      language: "english",
      languageLabel: "English",
      title: "Talking About Daily Routines",
      unit: "Daily Routine & Time",
      conversationGoal: "Learners can say a simple daily routine with time words.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About Daily Routines di Indonesia.", caption: "Konteks percakapan nyata: Talking About Daily Routines." }
      },
      sections: lessonSections
    },
    {
      slug: "days-and-simple-schedules",
      language: "english",
      languageLabel: "English",
      title: "Days and Simple Schedules",
      unit: "Daily Routine & Time",
      conversationGoal: "Learners can talk about simple days and class schedules.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Days and Simple Schedules di Indonesia.", caption: "Konteks percakapan nyata: Days and Simple Schedules." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-when-something-happens",
      language: "english",
      languageLabel: "English",
      title: "Asking When Something Happens",
      unit: "Daily Routine & Time",
      conversationGoal: "Learners can ask when a simple event happens and confirm the details.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking When Something Happens di Indonesia.", caption: "Konteks percakapan nyata: Asking When Something Happens." }
      },
      sections: lessonSections
    },
    {
      slug: "routine-conversation-mission",
      language: "english",
      languageLabel: "English",
      title: "Routine Conversation Mission",
      unit: "Daily Routine & Time",
      conversationGoal: "Learners can combine time, routine, days, and schedule questions in one simple conversation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Routine Conversation Mission di Indonesia.", caption: "Konteks percakapan nyata: Routine Conversation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "saying-what-you-do",
      language: "english",
      languageLabel: "English",
      title: "Saying What You Do",
      unit: "Work, Study & Preferences",
      conversationGoal: "Learners can say what they do in a simple work or study conversation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying What You Do di Indonesia.", caption: "Konteks percakapan nyata: Saying What You Do." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-about-work-or-study",
      language: "english",
      languageLabel: "English",
      title: "Asking About Work or Study",
      unit: "Work, Study & Preferences",
      conversationGoal: "Learners can ask if someone works or studies and ask one simple follow-up question.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Work or Study di Indonesia.", caption: "Konteks percakapan nyata: Asking About Work or Study." }
      },
      sections: lessonSections
    },
    {
      slug: "talking-about-likes",
      language: "english",
      languageLabel: "English",
      title: "Talking About Likes",
      unit: "Work, Study & Preferences",
      conversationGoal: "Learners can say what they like and ask someone about simple preferences.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About Likes di Indonesia.", caption: "Konteks percakapan nyata: Talking About Likes." }
      },
      sections: lessonSections
    },
    {
      slug: "saying-what-you-can-do",
      language: "english",
      languageLabel: "English",
      title: "Saying What You Can Do",
      unit: "Work, Study & Preferences",
      conversationGoal: "Learners can say what they can do in English with simple ability sentences.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying What You Can Do di Indonesia.", caption: "Konteks percakapan nyata: Saying What You Can Do." }
      },
      sections: lessonSections
    },
    {
      slug: "work-study-conversation-mission",
      language: "english",
      languageLabel: "English",
      title: "Work and Study Conversation Mission",
      unit: "Work, Study & Preferences",
      conversationGoal: "Learners can combine work, study, preferences, and simple abilities in one conversation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Work and Study Conversation Mission di Indonesia.", caption: "Konteks percakapan nyata: Work and Study Conversation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-where-a-place-is",
      language: "english",
      languageLabel: "English",
      title: "Asking Where a Place Is",
      unit: "Places & Directions",
      conversationGoal: "Learners can ask where a place is and understand a short location answer.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking Where a Place Is di Indonesia.", caption: "Konteks percakapan nyata: Asking Where a Place Is." }
      },
      sections: lessonSections
    },
    {
      slug: "simple-place-words",
      language: "english",
      languageLabel: "English",
      title: "Simple Place Words",
      unit: "Places & Directions",
      conversationGoal: "Learners can name common places and answer where someone is going.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Simple Place Words di Indonesia.", caption: "Konteks percakapan nyata: Simple Place Words." }
      },
      sections: lessonSections
    },
    {
      slug: "understanding-simple-directions",
      language: "english",
      languageLabel: "English",
      title: "Understanding Simple Directions",
      unit: "Places & Directions",
      conversationGoal: "Learners can understand very simple directions with go straight, turn left, and turn right.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Understanding Simple Directions di Indonesia.", caption: "Konteks percakapan nyata: Understanding Simple Directions." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-how-to-get-there",
      language: "english",
      languageLabel: "English",
      title: "Asking How to Get There",
      unit: "Places & Directions",
      conversationGoal: "Learners can ask how to get to a place and follow two simple steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking How to Get There di Indonesia.", caption: "Konteks percakapan nyata: Asking How to Get There." }
      },
      sections: lessonSections
    },
    {
      slug: "finding-a-place-mission",
      language: "english",
      languageLabel: "English",
      title: "Finding a Place Mission",
      unit: "Places & Directions",
      conversationGoal: "Learners can complete a short place-finding conversation from question to confirmation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Finding a Place Mission di Indonesia.", caption: "Konteks percakapan nyata: Finding a Place Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "ordering-a-drink",
      language: "english",
      languageLabel: "English",
      title: "Ordering a Drink",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Learners can order one drink politely and answer a simple size question.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Ordering a Drink di Indonesia.", caption: "Konteks percakapan nyata: Ordering a Drink." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-about-prices",
      language: "english",
      languageLabel: "English",
      title: "Asking About Prices",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Learners can ask the price of one item and understand a short price answer.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Prices di Indonesia.", caption: "Konteks percakapan nyata: Asking About Prices." }
      },
      sections: lessonSections
    },
    {
      slug: "buying-a-simple-item",
      language: "english",
      languageLabel: "English",
      title: "Buying a Simple Item",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Learners can buy one simple item, ask the price, and complete the payment.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Buying a Simple Item di Indonesia.", caption: "Konteks percakapan nyata: Buying a Simple Item." }
      },
      sections: lessonSections
    },
    {
      slug: "saying-what-you-want",
      language: "english",
      languageLabel: "English",
      title: "Saying What You Want",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Learners can say what they want and choose between two simple options.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying What You Want di Indonesia.", caption: "Konteks percakapan nyata: Saying What You Want." }
      },
      sections: lessonSections
    },
    {
      slug: "cafe-and-shop-mission",
      language: "english",
      languageLabel: "English",
      title: "Cafe and Shop Mission",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Learners can order, ask a price, choose an option, and complete a simple purchase.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Cafe and Shop Mission di Indonesia.", caption: "Konteks percakapan nyata: Cafe and Shop Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "saying-you-do-not-understand",
      language: "english",
      languageLabel: "English",
      title: "Saying You Do Not Understand",
      unit: "Help, Problems & Requests",
      conversationGoal: "Learners can say they do not understand and ask for repetition politely.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying You Do Not Understand di Indonesia.", caption: "Konteks percakapan nyata: Saying You Do Not Understand." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-for-help",
      language: "english",
      languageLabel: "English",
      title: "Asking for Help",
      unit: "Help, Problems & Requests",
      conversationGoal: "Learners can ask for help with one simple task and respond to the helper.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for Help di Indonesia.", caption: "Konteks percakapan nyata: Asking for Help." }
      },
      sections: lessonSections
    },
    {
      slug: "making-simple-requests",
      language: "english",
      languageLabel: "English",
      title: "Making Simple Requests",
      unit: "Help, Problems & Requests",
      conversationGoal: "Learners can make a simple request with please and respond to yes or no.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making Simple Requests di Indonesia.", caption: "Konteks percakapan nyata: Making Simple Requests." }
      },
      sections: lessonSections
    },
    {
      slug: "apologizing-and-thanking",
      language: "english",
      languageLabel: "English",
      title: "Apologizing and Thanking",
      unit: "Help, Problems & Requests",
      conversationGoal: "Learners can apologize for a small problem and thank someone for help.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Apologizing and Thanking di Indonesia.", caption: "Konteks percakapan nyata: Apologizing and Thanking." }
      },
      sections: lessonSections
    },
    {
      slug: "help-and-problem-mission",
      language: "english",
      languageLabel: "English",
      title: "Help and Problem Mission",
      unit: "Help, Problems & Requests",
      conversationGoal: "Learners can explain a simple problem, ask for help, make a request, and close politely.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Help and Problem Mission di Indonesia.", caption: "Konteks percakapan nyata: Help and Problem Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "review-introductions",
      language: "english",
      languageLabel: "English",
      title: "Review Introductions",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Learners can greet someone, introduce themselves, say where they are from, and ask simple follow-up questions.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Introductions di Indonesia.", caption: "Konteks percakapan nyata: Review Introductions." }
      },
      sections: lessonSections
    },
    {
      slug: "review-routines-and-time",
      language: "english",
      languageLabel: "English",
      title: "Review Routines and Time",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Learners can talk about a simple daily routine, class day, and class time in one short conversation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Routines and Time di Indonesia.", caption: "Konteks percakapan nyata: Review Routines and Time." }
      },
      sections: lessonSections
    },
    {
      slug: "review-places-and-shopping",
      language: "english",
      languageLabel: "English",
      title: "Review Places and Shopping",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Learners can ask where a place is, follow simple directions, order one item, and ask the price.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Places and Shopping di Indonesia.", caption: "Konteks percakapan nyata: Review Places and Shopping." }
      },
      sections: lessonSections
    },
    {
      slug: "final-test-practice",
      language: "english",
      languageLabel: "English",
      title: "Final Test Practice",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Learners can answer common A1 test questions about identity, routine, schedule, places, requests, and simple needs.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "a1-final-conversation",
      language: "english",
      languageLabel: "English",
      title: "A1 Final Conversation",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Learners can complete a full A1 conversation with greetings, identity, routine, places, ordering, help language, and polite closing.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks A1 Final Conversation di Indonesia.", caption: "Konteks percakapan nyata: A1 Final Conversation." }
      },
      sections: lessonSections
    },
    {
      slug: "starting-small-talk",
      language: "english",
      languageLabel: "English",
      title: "Starting Small Talk",
      unit: "Social Small Talk",
      conversationGoal: "Start a short small-talk conversation and keep it going with one follow-up question.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Starting Small Talk di Indonesia.", caption: "Konteks percakapan nyata: Starting Small Talk." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-follow-up-questions",
      language: "english",
      languageLabel: "English",
      title: "Asking Follow-up Questions",
      unit: "Social Small Talk",
      conversationGoal: "Ask simple follow-up questions to keep a conversation going.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking Follow-up Questions di Indonesia.", caption: "Konteks percakapan nyata: Asking Follow-up Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "talking-about-weekends",
      language: "english",
      languageLabel: "English",
      title: "Talking About Weekends",
      unit: "Social Small Talk",
      conversationGoal: "Ask about weekend plans and answer with simple details.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About Weekends di Indonesia.", caption: "Konteks percakapan nyata: Talking About Weekends." }
      },
      sections: lessonSections
    },
    {
      slug: "reacting-politely",
      language: "english",
      languageLabel: "English",
      title: "Reacting Politely",
      unit: "Social Small Talk",
      conversationGoal: "React politely to good news and to a small problem.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Reacting Politely di Indonesia.", caption: "Konteks percakapan nyata: Reacting Politely." }
      },
      sections: lessonSections
    },
    {
      slug: "small-talk-mission",
      language: "english",
      languageLabel: "English",
      title: "Small Talk Mission",
      unit: "Social Small Talk",
      conversationGoal: "Start small talk, ask follow-up questions, react politely, and make a simple weekend plan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Small Talk Mission di Indonesia.", caption: "Konteks percakapan nyata: Small Talk Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "making-plans",
      language: "english",
      languageLabel: "English",
      title: "Making Plans",
      unit: "Plans & Invitations",
      conversationGoal: "Make a simple plan with a time and a place.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making Plans di Indonesia.", caption: "Konteks percakapan nyata: Making Plans." }
      },
      sections: lessonSections
    },
    {
      slug: "inviting-someone",
      language: "english",
      languageLabel: "English",
      title: "Inviting Someone",
      unit: "Plans & Invitations",
      conversationGoal: "Invite someone to an activity and respond politely.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Inviting Someone di Indonesia.", caption: "Konteks percakapan nyata: Inviting Someone." }
      },
      sections: lessonSections
    },
    {
      slug: "accepting-and-declining",
      language: "english",
      languageLabel: "English",
      title: "Accepting and Declining",
      unit: "Plans & Invitations",
      conversationGoal: "Accept or decline an invitation politely with a short reason.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Accepting and Declining di Indonesia.", caption: "Konteks percakapan nyata: Accepting and Declining." }
      },
      sections: lessonSections
    },
    {
      slug: "rescheduling",
      language: "english",
      languageLabel: "English",
      title: "Rescheduling",
      unit: "Plans & Invitations",
      conversationGoal: "Reschedule a plan and agree on a new time.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Rescheduling di Indonesia.", caption: "Konteks percakapan nyata: Rescheduling." }
      },
      sections: lessonSections
    },
    {
      slug: "invitation-mission",
      language: "english",
      languageLabel: "English",
      title: "Invitation Mission",
      unit: "Plans & Invitations",
      conversationGoal: "Invite someone, decline politely with a reason, reschedule, and confirm the new plan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Invitation Mission di Indonesia.", caption: "Konteks percakapan nyata: Invitation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "buying-a-ticket",
      language: "english",
      languageLabel: "English",
      title: "Buying a Ticket",
      unit: "Travel & Transport",
      conversationGoal: "Buy a simple ticket and confirm the destination.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Buying a Ticket di Indonesia.", caption: "Konteks percakapan nyata: Buying a Ticket." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-about-departure-time",
      language: "english",
      languageLabel: "English",
      title: "Asking About Departure Time",
      unit: "Travel & Transport",
      conversationGoal: "Ask about a departure time and confirm the platform.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Departure Time di Indonesia.", caption: "Konteks percakapan nyata: Asking About Departure Time." }
      },
      sections: lessonSections
    },
    {
      slug: "checking-directions",
      language: "english",
      languageLabel: "English",
      title: "Checking Directions",
      unit: "Travel & Transport",
      conversationGoal: "Check directions and confirm you are going the right way.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Checking Directions di Indonesia.", caption: "Konteks percakapan nyata: Checking Directions." }
      },
      sections: lessonSections
    },
    {
      slug: "talking-to-a-driver",
      language: "english",
      languageLabel: "English",
      title: "Talking to a Driver",
      unit: "Travel & Transport",
      conversationGoal: "Tell a driver where you want to go and ask about the travel time.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking to a Driver di Indonesia.", caption: "Konteks percakapan nyata: Talking to a Driver." }
      },
      sections: lessonSections
    },
    {
      slug: "transport-mission",
      language: "english",
      languageLabel: "English",
      title: "Transport Mission",
      unit: "Travel & Transport",
      conversationGoal: "Buy a ticket, confirm time and platform, then tell a driver your destination.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Transport Mission di Indonesia.", caption: "Konteks percakapan nyata: Transport Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-for-an-item",
      language: "english",
      languageLabel: "English",
      title: "Asking for an Item",
      unit: "Shopping & Services",
      conversationGoal: "Ask for an item in a shop and check if it is available.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for an Item di Indonesia.", caption: "Konteks percakapan nyata: Asking for an Item." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-about-size-and-color",
      language: "english",
      languageLabel: "English",
      title: "Asking About Size and Color",
      unit: "Shopping & Services",
      conversationGoal: "Ask about size and color and choose one option.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Size and Color di Indonesia.", caption: "Konteks percakapan nyata: Asking About Size and Color." }
      },
      sections: lessonSections
    },
    {
      slug: "comparing-simple-options",
      language: "english",
      languageLabel: "English",
      title: "Comparing Simple Options",
      unit: "Shopping & Services",
      conversationGoal: "Compare two simple options and choose one.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Comparing Simple Options di Indonesia.", caption: "Konteks percakapan nyata: Comparing Simple Options." }
      },
      sections: lessonSections
    },
    {
      slug: "requesting-service-help",
      language: "english",
      languageLabel: "English",
      title: "Requesting Service Help",
      unit: "Shopping & Services",
      conversationGoal: "Ask for simple service help and respond politely.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Requesting Service Help di Indonesia.", caption: "Konteks percakapan nyata: Requesting Service Help." }
      },
      sections: lessonSections
    },
    {
      slug: "shopping-service-mission",
      language: "english",
      languageLabel: "English",
      title: "Shopping Service Mission",
      unit: "Shopping & Services",
      conversationGoal: "Ask for an item, ask about size and color, compare options, and request help politely.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Shopping Service Mission di Indonesia.", caption: "Konteks percakapan nyata: Shopping Service Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "saying-how-you-feel",
      language: "english",
      languageLabel: "English",
      title: "Saying How You Feel",
      unit: "Health & Appointments",
      conversationGoal: "Say how you feel and mention one or two simple symptoms.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying How You Feel di Indonesia.", caption: "Konteks percakapan nyata: Saying How You Feel." }
      },
      sections: lessonSections
    },
    {
      slug: "describing-simple-symptoms",
      language: "english",
      languageLabel: "English",
      title: "Describing Simple Symptoms",
      unit: "Health & Appointments",
      conversationGoal: "Describe simple symptoms and say how long you have had them.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing Simple Symptoms di Indonesia.", caption: "Konteks percakapan nyata: Describing Simple Symptoms." }
      },
      sections: lessonSections
    },
    {
      slug: "making-an-appointment",
      language: "english",
      languageLabel: "English",
      title: "Making an Appointment",
      unit: "Health & Appointments",
      conversationGoal: "Ask for an appointment and choose a day and time.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making an Appointment di Indonesia.", caption: "Konteks percakapan nyata: Making an Appointment." }
      },
      sections: lessonSections
    },
    {
      slug: "confirming-details",
      language: "english",
      languageLabel: "English",
      title: "Confirming Details",
      unit: "Health & Appointments",
      conversationGoal: "Confirm the appointment date, time, and name details.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Confirming Details di Indonesia.", caption: "Konteks percakapan nyata: Confirming Details." }
      },
      sections: lessonSections
    },
    {
      slug: "health-appointment-mission",
      language: "english",
      languageLabel: "English",
      title: "Health Appointment Mission",
      unit: "Health & Appointments",
      conversationGoal: "Check in for an appointment, confirm details, and describe a symptom briefly.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Health Appointment Mission di Indonesia.", caption: "Konteks percakapan nyata: Health Appointment Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "talking-about-yesterday",
      language: "english",
      languageLabel: "English",
      title: "Talking About Yesterday",
      unit: "Past Experiences",
      conversationGoal: "Talk about what you did yesterday using simple past tense verbs.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About Yesterday di Indonesia.", caption: "Konteks percakapan nyata: Talking About Yesterday." }
      },
      sections: lessonSections
    },
    {
      slug: "saying-where-you-went",
      language: "english",
      languageLabel: "English",
      title: "Saying Where You Went",
      unit: "Past Experiences",
      conversationGoal: "Say where you went and ask where someone went.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying Where You Went di Indonesia.", caption: "Konteks percakapan nyata: Saying Where You Went." }
      },
      sections: lessonSections
    },
    {
      slug: "describing-a-simple-experience",
      language: "english",
      languageLabel: "English",
      title: "Describing a Simple Experience",
      unit: "Past Experiences",
      conversationGoal: "Describe a simple experience and how it felt.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing a Simple Experience di Indonesia.", caption: "Konteks percakapan nyata: Describing a Simple Experience." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-about-past-activities",
      language: "english",
      languageLabel: "English",
      title: "Asking About Past Activities",
      unit: "Past Experiences",
      conversationGoal: "Ask what someone did and ask follow-up questions about their past activities.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Past Activities di Indonesia.", caption: "Konteks percakapan nyata: Asking About Past Activities." }
      },
      sections: lessonSections
    },
    {
      slug: "past-experience-mission",
      language: "english",
      languageLabel: "English",
      title: "Past Experience Mission",
      unit: "Past Experiences",
      conversationGoal: "Tell someone about yesterday: where you went, what you did, and how it was.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Past Experience Mission di Indonesia.", caption: "Konteks percakapan nyata: Past Experience Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "saying-what-you-think",
      language: "english",
      languageLabel: "English",
      title: "Saying What You Think",
      unit: "Opinions & Reasons",
      conversationGoal: "Say what you think about a simple topic and give a short opinion.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying What You Think di Indonesia.", caption: "Konteks percakapan nyata: Saying What You Think." }
      },
      sections: lessonSections
    },
    {
      slug: "giving-simple-reasons",
      language: "english",
      languageLabel: "English",
      title: "Giving Simple Reasons",
      unit: "Opinions & Reasons",
      conversationGoal: "Give a simple opinion and a short reason using because.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Giving Simple Reasons di Indonesia.", caption: "Konteks percakapan nyata: Giving Simple Reasons." }
      },
      sections: lessonSections
    },
    {
      slug: "agreeing-and-disagreeing-politely",
      language: "english",
      languageLabel: "English",
      title: "Agreeing and Disagreeing Politely",
      unit: "Opinions & Reasons",
      conversationGoal: "Agree or disagree politely and give a short reason.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Agreeing and Disagreeing Politely di Indonesia.", caption: "Konteks percakapan nyata: Agreeing and Disagreeing Politely." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-for-opinions",
      language: "english",
      languageLabel: "English",
      title: "Asking for Opinions",
      unit: "Opinions & Reasons",
      conversationGoal: "Ask for someone's opinion and respond with a simple opinion and reason.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for Opinions di Indonesia.", caption: "Konteks percakapan nyata: Asking for Opinions." }
      },
      sections: lessonSections
    },
    {
      slug: "opinion-conversation-mission",
      language: "english",
      languageLabel: "English",
      title: "Opinion Conversation Mission",
      unit: "Opinions & Reasons",
      conversationGoal: "Have a short opinion conversation: ask for an opinion, give a reason, and respond politely.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Opinion Conversation Mission di Indonesia.", caption: "Konteks percakapan nyata: Opinion Conversation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "review-social-and-plans",
      language: "english",
      languageLabel: "English",
      title: "Review Social and Plans",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Review social small talk and making simple plans with follow-up questions.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Social and Plans di Indonesia.", caption: "Konteks percakapan nyata: Review Social and Plans." }
      },
      sections: lessonSections
    },
    {
      slug: "review-travel-and-shopping",
      language: "english",
      languageLabel: "English",
      title: "Review Travel and Shopping",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Review asking travel questions and shopping requests (tickets, directions, items, sizes).",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Travel and Shopping di Indonesia.", caption: "Konteks percakapan nyata: Review Travel and Shopping." }
      },
      sections: lessonSections
    },
    {
      slug: "review-health-and-past",
      language: "english",
      languageLabel: "English",
      title: "Review Health and Past",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Review describing symptoms and talking about the past (yesterday, last night).",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Health and Past di Indonesia.", caption: "Konteks percakapan nyata: Review Health and Past." }
      },
      sections: lessonSections
    },
    {
      slug: "a2-final-test-practice",
      language: "english",
      languageLabel: "English",
      title: "A2 Final Test Practice",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Practice mixed A2 skills with short prompts (plans, shopping, symptoms, past, opinions).",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks A2 Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: A2 Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "a2-final-conversation",
      language: "english",
      languageLabel: "English",
      title: "A2 Final Conversation",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Complete a longer everyday conversation using multiple A2 skills (plans, past, opinions, requests).",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks A2 Final Conversation di Indonesia.", caption: "Konteks percakapan nyata: A2 Final Conversation." }
      },
      sections: lessonSections
    },
    {
      slug: "setting-the-scene",
      language: "english",
      languageLabel: "English",
      title: "Setting the Scene",
      unit: "Personal Stories",
      conversationGoal: "Set the scene for a short story (when, where, who) before telling what happened.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Setting the Scene di Indonesia.", caption: "Konteks percakapan nyata: Setting the Scene." }
      },
      sections: lessonSections
    },
    {
      slug: "telling-events-in-order",
      language: "english",
      languageLabel: "English",
      title: "Telling Events in Order",
      unit: "Personal Stories",
      conversationGoal: "Tell story events in order using simple linking words (first, then, after that, finally).",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Telling Events in Order di Indonesia.", caption: "Konteks percakapan nyata: Telling Events in Order." }
      },
      sections: lessonSections
    },
    {
      slug: "describing-feelings",
      language: "english",
      languageLabel: "English",
      title: "Describing Feelings",
      unit: "Personal Stories",
      conversationGoal: "Describe how you felt during a story using feeling adjectives.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing Feelings di Indonesia.", caption: "Konteks percakapan nyata: Describing Feelings." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-about-someones-story",
      language: "english",
      languageLabel: "English",
      title: "Asking About Someone's Story",
      unit: "Personal Stories",
      conversationGoal: "Ask follow-up questions to keep someone's story going (next event, reason, feelings).",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Someone's Story di Indonesia.", caption: "Konteks percakapan nyata: Asking About Someone's Story." }
      },
      sections: lessonSections
    },
    {
      slug: "personal-story-mission",
      language: "english",
      languageLabel: "English",
      title: "Personal Story Mission",
      unit: "Personal Stories",
      conversationGoal: "Tell a connected personal story with a clear scene, ordered events, and feelings, then answer a follow-up question.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Personal Story Mission di Indonesia.", caption: "Konteks percakapan nyata: Personal Story Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "explaining-your-task",
      language: "english",
      languageLabel: "English",
      title: "Explaining Your Task",
      unit: "Workplace Conversations",
      conversationGoal: "Explain what you are working on and what the next step is in a short, clear way.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining Your Task di Indonesia.", caption: "Konteks percakapan nyata: Explaining Your Task." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-for-clarification",
      language: "english",
      languageLabel: "English",
      title: "Asking for Clarification",
      unit: "Workplace Conversations",
      conversationGoal: "Ask for clarification politely when you are not sure about a task.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for Clarification di Indonesia.", caption: "Konteks percakapan nyata: Asking for Clarification." }
      },
      sections: lessonSections
    },
    {
      slug: "giving-a-short-update",
      language: "english",
      languageLabel: "English",
      title: "Giving a Short Update",
      unit: "Workplace Conversations",
      conversationGoal: "Give a short work update with progress, a plan, and one risk or blocker.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Giving a Short Update di Indonesia.", caption: "Konteks percakapan nyata: Giving a Short Update." }
      },
      sections: lessonSections
    },
    {
      slug: "joining-a-simple-meeting",
      language: "english",
      languageLabel: "English",
      title: "Joining a Simple Meeting",
      unit: "Workplace Conversations",
      conversationGoal: "Join a simple meeting, state your point briefly, and ask for the next step.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Joining a Simple Meeting di Indonesia.", caption: "Konteks percakapan nyata: Joining a Simple Meeting." }
      },
      sections: lessonSections
    },
    {
      slug: "workplace-mission",
      language: "english",
      languageLabel: "English",
      title: "Workplace Mission",
      unit: "Workplace Conversations",
      conversationGoal: "Complete a workplace mini-conversation: give an update, ask for clarification, and confirm a deadline.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Workplace Mission di Indonesia.", caption: "Konteks percakapan nyata: Workplace Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "describing-a-problem",
      language: "english",
      languageLabel: "English",
      title: "Describing a Problem",
      unit: "Problems & Solutions",
      conversationGoal: "Describe a problem clearly and explain what happened and why it matters.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing a Problem di Indonesia.", caption: "Konteks percakapan nyata: Describing a Problem." }
      },
      sections: lessonSections
    },
    {
      slug: "suggesting-a-solution",
      language: "english",
      languageLabel: "English",
      title: "Suggesting a Solution",
      unit: "Problems & Solutions",
      conversationGoal: "Suggest a solution politely and explain why it could help.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Suggesting a Solution di Indonesia.", caption: "Konteks percakapan nyata: Suggesting a Solution." }
      },
      sections: lessonSections
    },
    {
      slug: "responding-to-advice",
      language: "english",
      languageLabel: "English",
      title: "Responding to Advice",
      unit: "Problems & Solutions",
      conversationGoal: "Respond to advice politely and decide what you will do next.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding to Advice di Indonesia.", caption: "Konteks percakapan nyata: Responding to Advice." }
      },
      sections: lessonSections
    },
    {
      slug: "making-a-simple-decision",
      language: "english",
      languageLabel: "English",
      title: "Making a Simple Decision",
      unit: "Problems & Solutions",
      conversationGoal: "Compare two options and make a simple decision with a clear reason.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making a Simple Decision di Indonesia.", caption: "Konteks percakapan nyata: Making a Simple Decision." }
      },
      sections: lessonSections
    },
    {
      slug: "problem-solving-mission",
      language: "english",
      languageLabel: "English",
      title: "Problem Solving Mission",
      unit: "Problems & Solutions",
      conversationGoal: "Complete a mini problem-solving conversation: describe a problem, suggest a solution, respond to a concern, and decide next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Problem Solving Mission di Indonesia.", caption: "Konteks percakapan nyata: Problem Solving Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "checking-in",
      language: "english",
      languageLabel: "English",
      title: "Checking In",
      unit: "Travel Situations",
      conversationGoal: "Check in at a hotel, confirm your reservation, and ask one practical question.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Checking In di Indonesia.", caption: "Konteks percakapan nyata: Checking In." }
      },
      sections: lessonSections
    },
    {
      slug: "explaining-a-delay",
      language: "english",
      languageLabel: "English",
      title: "Explaining a Delay",
      unit: "Travel Situations",
      conversationGoal: "Explain that you are delayed, give an updated arrival time, and ask to adjust the plan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining a Delay di Indonesia.", caption: "Konteks percakapan nyata: Explaining a Delay." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-for-recommendations",
      language: "english",
      languageLabel: "English",
      title: "Asking for Recommendations",
      unit: "Travel Situations",
      conversationGoal: "Ask for recommendations, describe what you want, and ask one follow-up question.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for Recommendations di Indonesia.", caption: "Konteks percakapan nyata: Asking for Recommendations." }
      },
      sections: lessonSections
    },
    {
      slug: "handling-a-simple-complaint",
      language: "english",
      languageLabel: "English",
      title: "Handling a Simple Complaint",
      unit: "Travel Situations",
      conversationGoal: "Explain a simple problem politely and ask for help or an alternative.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Handling a Simple Complaint di Indonesia.", caption: "Konteks percakapan nyata: Handling a Simple Complaint." }
      },
      sections: lessonSections
    },
    {
      slug: "travel-situation-mission",
      language: "english",
      languageLabel: "English",
      title: "Travel Situation Mission",
      unit: "Travel Situations",
      conversationGoal: "Complete a travel mini-conversation: explain a delay, check in, ask for a recommendation, and request help with a small issue.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Travel Situation Mission di Indonesia.", caption: "Konteks percakapan nyata: Travel Situation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "talking-about-goals",
      language: "english",
      languageLabel: "English",
      title: "Talking About Goals",
      unit: "Goals & Progress",
      conversationGoal: "Talk about a personal goal, give a time frame, and explain why it matters.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About Goals di Indonesia.", caption: "Konteks percakapan nyata: Talking About Goals." }
      },
      sections: lessonSections
    },
    {
      slug: "explaining-progress",
      language: "english",
      languageLabel: "English",
      title: "Explaining Progress",
      unit: "Goals & Progress",
      conversationGoal: "Explain your progress clearly, mention what improved, and say what you still need to work on.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining Progress di Indonesia.", caption: "Konteks percakapan nyata: Explaining Progress." }
      },
      sections: lessonSections
    },
    {
      slug: "discussing-challenges",
      language: "english",
      languageLabel: "English",
      title: "Discussing Challenges",
      unit: "Goals & Progress",
      conversationGoal: "Describe a challenge, explain why it is difficult, and ask for a simple suggestion.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Discussing Challenges di Indonesia.", caption: "Konteks percakapan nyata: Discussing Challenges." }
      },
      sections: lessonSections
    },
    {
      slug: "making-next-step-plans",
      language: "english",
      languageLabel: "English",
      title: "Making Next-step Plans",
      unit: "Goals & Progress",
      conversationGoal: "State your next step, set a simple schedule, and confirm the plan clearly.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making Next-step Plans di Indonesia.", caption: "Konteks percakapan nyata: Making Next-step Plans." }
      },
      sections: lessonSections
    },
    {
      slug: "goals-progress-mission",
      language: "english",
      languageLabel: "English",
      title: "Goals Progress Mission",
      unit: "Goals & Progress",
      conversationGoal: "Complete a mini conversation: state a goal, share progress, describe a challenge, and set a next-step plan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Goals Progress Mission di Indonesia.", caption: "Konteks percakapan nyata: Goals Progress Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "comparing-two-options",
      language: "english",
      languageLabel: "English",
      title: "Comparing Two Options",
      unit: "Explaining Preferences",
      conversationGoal: "Compare two options and ask what the other person prefers.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Comparing Two Options di Indonesia.", caption: "Konteks percakapan nyata: Comparing Two Options." }
      },
      sections: lessonSections
    },
    {
      slug: "explaining-why-you-prefer-something",
      language: "english",
      languageLabel: "English",
      title: "Explaining Why You Prefer Something",
      unit: "Explaining Preferences",
      conversationGoal: "State a preference and explain the main reason clearly.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining Why You Prefer Something di Indonesia.", caption: "Konteks percakapan nyata: Explaining Why You Prefer Something." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-about-pros-and-cons",
      language: "english",
      languageLabel: "English",
      title: "Asking About Pros and Cons",
      unit: "Explaining Preferences",
      conversationGoal: "Ask about pros and cons and respond with one advantage and one downside.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Pros and Cons di Indonesia.", caption: "Konteks percakapan nyata: Asking About Pros and Cons." }
      },
      sections: lessonSections
    },
    {
      slug: "reaching-agreement",
      language: "english",
      languageLabel: "English",
      title: "Reaching Agreement",
      unit: "Explaining Preferences",
      conversationGoal: "Suggest a plan, respond politely, and confirm an agreement.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Reaching Agreement di Indonesia.", caption: "Konteks percakapan nyata: Reaching Agreement." }
      },
      sections: lessonSections
    },
    {
      slug: "preference-discussion-mission",
      language: "english",
      languageLabel: "English",
      title: "Preference Discussion Mission",
      unit: "Explaining Preferences",
      conversationGoal: "Complete a mini conversation: compare options, explain your preference with reasons, discuss pros and cons, and reach an agreement.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Preference Discussion Mission di Indonesia.", caption: "Konteks percakapan nyata: Preference Discussion Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "describing-your-community",
      language: "english",
      languageLabel: "English",
      title: "Describing Your Community",
      unit: "Community & Culture",
      conversationGoal: "Describe your neighborhood, mention what you like, and invite a follow-up question.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing Your Community di Indonesia.", caption: "Konteks percakapan nyata: Describing Your Community." }
      },
      sections: lessonSections
    },
    {
      slug: "talking-about-local-habits",
      language: "english",
      languageLabel: "English",
      title: "Talking About Local Habits",
      unit: "Community & Culture",
      conversationGoal: "Describe a local habit, say how often it happens, and give a simple example.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About Local Habits di Indonesia.", caption: "Konteks percakapan nyata: Talking About Local Habits." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-about-culture",
      language: "english",
      languageLabel: "English",
      title: "Asking About Culture",
      unit: "Community & Culture",
      conversationGoal: "Ask about cultural traditions politely and respond with a short explanation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Culture di Indonesia.", caption: "Konteks percakapan nyata: Asking About Culture." }
      },
      sections: lessonSections
    },
    {
      slug: "being-polite-with-differences",
      language: "english",
      languageLabel: "English",
      title: "Being Polite With Differences",
      unit: "Community & Culture",
      conversationGoal: "Talk about cultural differences politely and show respect even if you do things differently.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Being Polite With Differences di Indonesia.", caption: "Konteks percakapan nyata: Being Polite With Differences." }
      },
      sections: lessonSections
    },
    {
      slug: "community-culture-mission",
      language: "english",
      languageLabel: "English",
      title: "Community Culture Mission",
      unit: "Community & Culture",
      conversationGoal: "Complete a mini conversation: describe your community, share a local habit, ask about culture, and respond politely to differences.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Community Culture Mission di Indonesia.", caption: "Konteks percakapan nyata: Community Culture Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "review-stories-and-work",
      language: "english",
      languageLabel: "English",
      title: "Review Stories and Work",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "Tell a short story and give a clear work update with one next step.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Stories and Work di Indonesia.", caption: "Konteks percakapan nyata: Review Stories and Work." }
      },
      sections: lessonSections
    },
    {
      slug: "review-problems-and-travel",
      language: "english",
      languageLabel: "English",
      title: "Review Problems and Travel",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "Explain a problem, describe the impact, and give a travel-style delay update with an estimate.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Problems and Travel di Indonesia.", caption: "Konteks percakapan nyata: Review Problems and Travel." }
      },
      sections: lessonSections
    },
    {
      slug: "review-goals-and-preferences",
      language: "english",
      languageLabel: "English",
      title: "Review Goals and Preferences",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "State a goal, share progress, and explain a preference with a clear reason.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Goals and Preferences di Indonesia.", caption: "Konteks percakapan nyata: Review Goals and Preferences." }
      },
      sections: lessonSections
    },
    {
      slug: "b1-final-test-practice",
      language: "english",
      languageLabel: "English",
      title: "B1 Final Test Practice",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "Practice a short mixed conversation with clear, accurate sentences across B1 topics.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks B1 Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: B1 Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "b1-final-conversation",
      language: "english",
      languageLabel: "English",
      title: "B1 Final Conversation",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "Hold a connected conversation that includes a story, a plan, a problem, a preference, and a next step.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks B1 Final Conversation di Indonesia.", caption: "Konteks percakapan nyata: B1 Final Conversation." }
      },
      sections: lessonSections
    },
    {
      slug: "stating-your-position",
      language: "english",
      languageLabel: "English",
      title: "Stating Your Position",
      unit: "Clear Arguments",
      conversationGoal: "State your position clearly, acknowledge another view, and give one short reason.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Stating Your Position di Indonesia.", caption: "Konteks percakapan nyata: Stating Your Position." }
      },
      sections: lessonSections
    },
    {
      slug: "supporting-with-reasons",
      language: "english",
      languageLabel: "English",
      title: "Supporting With Reasons",
      unit: "Clear Arguments",
      conversationGoal: "Support your argument with two structured reasons and keep it concise.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Supporting With Reasons di Indonesia.", caption: "Konteks percakapan nyata: Supporting With Reasons." }
      },
      sections: lessonSections
    },
    {
      slug: "using-examples",
      language: "english",
      languageLabel: "English",
      title: "Using Examples",
      unit: "Clear Arguments",
      conversationGoal: "Support your point with a clear example and connect it back to your argument.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Using Examples di Indonesia.", caption: "Konteks percakapan nyata: Using Examples." }
      },
      sections: lessonSections
    },
    {
      slug: "responding-to-counterpoints",
      language: "english",
      languageLabel: "English",
      title: "Responding to Counterpoints",
      unit: "Clear Arguments",
      conversationGoal: "Respond to a counterpoint politely, show you understand it, and reinforce your position.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding to Counterpoints di Indonesia.", caption: "Konteks percakapan nyata: Responding to Counterpoints." }
      },
      sections: lessonSections
    },
    {
      slug: "clear-argument-mission",
      language: "english",
      languageLabel: "English",
      title: "Clear Argument Mission",
      unit: "Clear Arguments",
      conversationGoal: "Complete a mini argument: state your position, give reasons and an example, respond to a counterpoint, and agree on next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Clear Argument Mission di Indonesia.", caption: "Konteks percakapan nyata: Clear Argument Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "opening-a-meeting-point",
      language: "english",
      languageLabel: "English",
      title: "Opening a Meeting Point",
      unit: "Professional Meetings",
      conversationGoal: "Open a discussion point clearly, explain why it matters, and invite input.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Opening a Meeting Point di Indonesia.", caption: "Konteks percakapan nyata: Opening a Meeting Point." }
      },
      sections: lessonSections
    },
    {
      slug: "clarifying-scope",
      language: "english",
      languageLabel: "English",
      title: "Clarifying Scope",
      unit: "Professional Meetings",
      conversationGoal: "Clarify scope, ask what is included, and confirm what is out of scope.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Clarifying Scope di Indonesia.", caption: "Konteks percakapan nyata: Clarifying Scope." }
      },
      sections: lessonSections
    },
    {
      slug: "giving-constructive-feedback",
      language: "english",
      languageLabel: "English",
      title: "Giving Constructive Feedback",
      unit: "Professional Meetings",
      conversationGoal: "Give constructive feedback politely, focus on impact, and suggest one improvement.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Giving Constructive Feedback di Indonesia.", caption: "Konteks percakapan nyata: Giving Constructive Feedback." }
      },
      sections: lessonSections
    },
    {
      slug: "summarizing-decisions",
      language: "english",
      languageLabel: "English",
      title: "Summarizing Decisions",
      unit: "Professional Meetings",
      conversationGoal: "Summarize decisions clearly, confirm action items, and assign owners.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Summarizing Decisions di Indonesia.", caption: "Konteks percakapan nyata: Summarizing Decisions." }
      },
      sections: lessonSections
    },
    {
      slug: "meeting-participation-mission",
      language: "english",
      languageLabel: "English",
      title: "Meeting Participation Mission",
      unit: "Professional Meetings",
      conversationGoal: "Complete a mini meeting: open a point, clarify scope, give constructive feedback, and summarize decisions with action items.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Meeting Participation Mission di Indonesia.", caption: "Konteks percakapan nyata: Meeting Participation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "expressing-priorities",
      language: "english",
      languageLabel: "English",
      title: "Expressing Priorities",
      unit: "Negotiation & Compromise",
      conversationGoal: "State your priorities clearly, explain what matters most, and ask about the other person's priorities.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Expressing Priorities di Indonesia.", caption: "Konteks percakapan nyata: Expressing Priorities." }
      },
      sections: lessonSections
    },
    {
      slug: "making-a-proposal",
      language: "english",
      languageLabel: "English",
      title: "Making a Proposal",
      unit: "Negotiation & Compromise",
      conversationGoal: "Make a clear proposal, suggest a timeline, and ask if it works.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making a Proposal di Indonesia.", caption: "Konteks percakapan nyata: Making a Proposal." }
      },
      sections: lessonSections
    },
    {
      slug: "handling-objections",
      language: "english",
      languageLabel: "English",
      title: "Handling Objections",
      unit: "Negotiation & Compromise",
      conversationGoal: "Respond to an objection politely, ask a clarifying question, and offer a revised proposal.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Handling Objections di Indonesia.", caption: "Konteks percakapan nyata: Handling Objections." }
      },
      sections: lessonSections
    },
    {
      slug: "finding-middle-ground",
      language: "english",
      languageLabel: "English",
      title: "Finding Middle Ground",
      unit: "Negotiation & Compromise",
      conversationGoal: "Find a compromise, propose a middle-ground option, and confirm agreement.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Finding Middle Ground di Indonesia.", caption: "Konteks percakapan nyata: Finding Middle Ground." }
      },
      sections: lessonSections
    },
    {
      slug: "negotiation-mission",
      language: "english",
      languageLabel: "English",
      title: "Negotiation Mission",
      unit: "Negotiation & Compromise",
      conversationGoal: "Complete a negotiation: align priorities, make a proposal, handle objections, find middle ground, and agree on next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Negotiation Mission di Indonesia.", caption: "Konteks percakapan nyata: Negotiation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "structuring-a-short-presentation",
      language: "english",
      languageLabel: "English",
      title: "Structuring a Short Presentation",
      unit: "Presenting Ideas",
      conversationGoal: "Present an idea with a clear structure: context, proposal, and next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Structuring a Short Presentation di Indonesia.", caption: "Konteks percakapan nyata: Structuring a Short Presentation." }
      },
      sections: lessonSections
    },
    {
      slug: "signposting-clearly",
      language: "english",
      languageLabel: "English",
      title: "Signposting Clearly",
      unit: "Presenting Ideas",
      conversationGoal: "Use clear signposting to guide listeners through your presentation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Signposting Clearly di Indonesia.", caption: "Konteks percakapan nyata: Signposting Clearly." }
      },
      sections: lessonSections
    },
    {
      slug: "explaining-benefits-and-risks",
      language: "english",
      languageLabel: "English",
      title: "Explaining Benefits and Risks",
      unit: "Presenting Ideas",
      conversationGoal: "Explain two benefits, mention one risk, and propose a mitigation plan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining Benefits and Risks di Indonesia.", caption: "Konteks percakapan nyata: Explaining Benefits and Risks." }
      },
      sections: lessonSections
    },
    {
      slug: "answering-questions",
      language: "english",
      languageLabel: "English",
      title: "Answering Questions",
      unit: "Presenting Ideas",
      conversationGoal: "Answer a question clearly, admit uncertainty when needed, and offer to follow up.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Answering Questions di Indonesia.", caption: "Konteks percakapan nyata: Answering Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "idea-presentation-mission",
      language: "english",
      languageLabel: "English",
      title: "Idea Presentation Mission",
      unit: "Presenting Ideas",
      conversationGoal: "Complete a mini presentation: structure the idea, signpost clearly, explain benefits and risks, and answer questions professionally.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Idea Presentation Mission di Indonesia.", caption: "Konteks percakapan nyata: Idea Presentation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "summarizing-an-article",
      language: "english",
      languageLabel: "English",
      title: "Summarizing an Article",
      unit: "Media & Information",
      conversationGoal: "Summarize an article in 2–3 sentences: main topic, key point, and conclusion.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Summarizing an Article di Indonesia.", caption: "Konteks percakapan nyata: Summarizing an Article." }
      },
      sections: lessonSections
    },
    {
      slug: "discussing-reliable-sources",
      language: "english",
      languageLabel: "English",
      title: "Discussing Reliable Sources",
      unit: "Media & Information",
      conversationGoal: "Discuss whether a source is reliable, explain why, and suggest a better source.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Discussing Reliable Sources di Indonesia.", caption: "Konteks percakapan nyata: Discussing Reliable Sources." }
      },
      sections: lessonSections
    },
    {
      slug: "explaining-a-viewpoint",
      language: "english",
      languageLabel: "English",
      title: "Explaining a Viewpoint",
      unit: "Media & Information",
      conversationGoal: "Explain a viewpoint clearly, support it with one reason, and acknowledge another perspective.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining a Viewpoint di Indonesia.", caption: "Konteks percakapan nyata: Explaining a Viewpoint." }
      },
      sections: lessonSections
    },
    {
      slug: "responding-to-new-information",
      language: "english",
      languageLabel: "English",
      title: "Responding to New Information",
      unit: "Media & Information",
      conversationGoal: "Respond to new information, update your opinion, and ask a follow-up question.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding to New Information di Indonesia.", caption: "Konteks percakapan nyata: Responding to New Information." }
      },
      sections: lessonSections
    },
    {
      slug: "information-discussion-mission",
      language: "english",
      languageLabel: "English",
      title: "Information Discussion Mission",
      unit: "Media & Information",
      conversationGoal: "Complete a discussion: summarize an article, evaluate source reliability, explain a viewpoint, and respond to new information with next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Information Discussion Mission di Indonesia.", caption: "Konteks percakapan nyata: Information Discussion Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "understanding-client-needs",
      language: "english",
      languageLabel: "English",
      title: "Understanding Client Needs",
      unit: "Customer & Client Communication",
      conversationGoal: "Ask clarifying questions to understand client needs, confirm requirements, and summarize what you heard.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Understanding Client Needs di Indonesia.", caption: "Konteks percakapan nyata: Understanding Client Needs." }
      },
      sections: lessonSections
    },
    {
      slug: "explaining-options",
      language: "english",
      languageLabel: "English",
      title: "Explaining Options",
      unit: "Customer & Client Communication",
      conversationGoal: "Explain two options clearly, compare trade-offs, and recommend one option.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining Options di Indonesia.", caption: "Konteks percakapan nyata: Explaining Options." }
      },
      sections: lessonSections
    },
    {
      slug: "handling-concerns",
      language: "english",
      languageLabel: "English",
      title: "Handling Concerns",
      unit: "Customer & Client Communication",
      conversationGoal: "Acknowledge a client concern, ask a clarifying question, and propose a mitigation plan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Handling Concerns di Indonesia.", caption: "Konteks percakapan nyata: Handling Concerns." }
      },
      sections: lessonSections
    },
    {
      slug: "confirming-next-steps",
      language: "english",
      languageLabel: "English",
      title: "Confirming Next Steps",
      unit: "Customer & Client Communication",
      conversationGoal: "Confirm next steps, assign owners, and set a timeline clearly.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Confirming Next Steps di Indonesia.", caption: "Konteks percakapan nyata: Confirming Next Steps." }
      },
      sections: lessonSections
    },
    {
      slug: "client-conversation-mission",
      language: "english",
      languageLabel: "English",
      title: "Client Conversation Mission",
      unit: "Customer & Client Communication",
      conversationGoal: "Complete a client conversation: understand needs, explain options, handle concerns, and confirm next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Client Conversation Mission di Indonesia.", caption: "Konteks percakapan nyata: Client Conversation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "framing-the-problem",
      language: "english",
      languageLabel: "English",
      title: "Framing the Problem",
      unit: "Complex Problem Solving",
      conversationGoal: "Frame a complex problem clearly by defining scope, success criteria, and constraints.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Framing the Problem di Indonesia.", caption: "Konteks percakapan nyata: Framing the Problem." }
      },
      sections: lessonSections
    },
    {
      slug: "explaining-causes",
      language: "english",
      languageLabel: "English",
      title: "Explaining Causes",
      unit: "Complex Problem Solving",
      conversationGoal: "Explain possible causes using evidence language and clarify what data supports each cause.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining Causes di Indonesia.", caption: "Konteks percakapan nyata: Explaining Causes." }
      },
      sections: lessonSections
    },
    {
      slug: "discussing-tradeoffs",
      language: "english",
      languageLabel: "English",
      title: "Discussing Tradeoffs",
      unit: "Complex Problem Solving",
      conversationGoal: "Discuss trade-offs between options, highlighting impact on cost, time, and risk.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Discussing Tradeoffs di Indonesia.", caption: "Konteks percakapan nyata: Discussing Tradeoffs." }
      },
      sections: lessonSections
    },
    {
      slug: "recommending-a-solution",
      language: "english",
      languageLabel: "English",
      title: "Recommending a Solution",
      unit: "Complex Problem Solving",
      conversationGoal: "Recommend a solution clearly by summarizing reasoning, risks, and next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Recommending a Solution di Indonesia.", caption: "Konteks percakapan nyata: Recommending a Solution." }
      },
      sections: lessonSections
    },
    {
      slug: "problem-solving-discussion-mission",
      language: "english",
      languageLabel: "English",
      title: "Problem Solving Discussion Mission",
      unit: "Complex Problem Solving",
      conversationGoal: "Lead a problem-solving discussion: frame the problem, explain causes, discuss trade-offs, and recommend next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Problem Solving Discussion Mission di Indonesia.", caption: "Konteks percakapan nyata: Problem Solving Discussion Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "review-arguments-and-meetings",
      language: "english",
      languageLabel: "English",
      title: "Review Arguments and Meetings",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Summarize your position clearly, support it with reasons, and close with clear next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Arguments and Meetings di Indonesia.", caption: "Konteks percakapan nyata: Review Arguments and Meetings." }
      },
      sections: lessonSections
    },
    {
      slug: "review-negotiation-and-presenting",
      language: "english",
      languageLabel: "English",
      title: "Review Negotiation and Presenting",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Propose a compromise, explain trade-offs, and present a recommendation with clear signposting.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Negotiation and Presenting di Indonesia.", caption: "Konteks percakapan nyata: Review Negotiation and Presenting." }
      },
      sections: lessonSections
    },
    {
      slug: "review-information-and-clients",
      language: "english",
      languageLabel: "English",
      title: "Review Information and Clients",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Discuss information sources carefully and handle a client call with clarity, empathy, and next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Information and Clients di Indonesia.", caption: "Konteks percakapan nyata: Review Information and Clients." }
      },
      sections: lessonSections
    },
    {
      slug: "b2-final-test-practice",
      language: "english",
      languageLabel: "English",
      title: "B2 Final Test Practice",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Answer a set of B2-style prompts: position, evidence, trade-offs, recommendation, and next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks B2 Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: B2 Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "b2-final-discussion",
      language: "english",
      languageLabel: "English",
      title: "B2 Final Discussion",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Hold a final B2 discussion: frame the issue, compare options, address concerns, and align on a decision.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks B2 Final Discussion di Indonesia.", caption: "Konteks percakapan nyata: B2 Final Discussion." }
      },
      sections: lessonSections
    },
    {
      slug: "qualifying-your-opinion",
      language: "english",
      languageLabel: "English",
      title: "Qualifying Your Opinion",
      unit: "Nuanced Opinions",
      conversationGoal: "Qualify your opinion with nuance by signaling scope, conditions, and limits.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Qualifying Your Opinion di Indonesia.", caption: "Konteks percakapan nyata: Qualifying Your Opinion." }
      },
      sections: lessonSections
    },
    {
      slug: "expressing-certainty-and-doubt",
      language: "english",
      languageLabel: "English",
      title: "Expressing Certainty and Doubt",
      unit: "Nuanced Opinions",
      conversationGoal: "Express degrees of certainty and doubt using precise language and evidence framing.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Expressing Certainty and Doubt di Indonesia.", caption: "Konteks percakapan nyata: Expressing Certainty and Doubt." }
      },
      sections: lessonSections
    },
    {
      slug: "balancing-two-viewpoints",
      language: "english",
      languageLabel: "English",
      title: "Balancing Two Viewpoints",
      unit: "Nuanced Opinions",
      conversationGoal: "Balance two viewpoints fairly and reach a nuanced conclusion.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Balancing Two Viewpoints di Indonesia.", caption: "Konteks percakapan nyata: Balancing Two Viewpoints." }
      },
      sections: lessonSections
    },
    {
      slug: "softening-disagreement",
      language: "english",
      languageLabel: "English",
      title: "Softening Disagreement",
      unit: "Nuanced Opinions",
      conversationGoal: "Disagree tactfully while staying precise and constructive.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Softening Disagreement di Indonesia.", caption: "Konteks percakapan nyata: Softening Disagreement." }
      },
      sections: lessonSections
    },
    {
      slug: "nuanced-opinion-mission",
      language: "english",
      languageLabel: "English",
      title: "Nuanced Opinion Mission",
      unit: "Nuanced Opinions",
      conversationGoal: "Hold a nuanced discussion: qualify your stance, calibrate certainty, balance viewpoints, and disagree tactfully.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Nuanced Opinion Mission di Indonesia.", caption: "Konteks percakapan nyata: Nuanced Opinion Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "aligning-stakeholders",
      language: "english",
      languageLabel: "English",
      title: "Aligning Stakeholders",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Align stakeholders by clarifying priorities, surfacing constraints, and confirming a shared decision.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Aligning Stakeholders di Indonesia.", caption: "Konteks percakapan nyata: Aligning Stakeholders." }
      },
      sections: lessonSections
    },
    {
      slug: "managing-expectations",
      language: "english",
      languageLabel: "English",
      title: "Managing Expectations",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Manage expectations by setting clear boundaries, timelines, and what success looks like.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Managing Expectations di Indonesia.", caption: "Konteks percakapan nyata: Managing Expectations." }
      },
      sections: lessonSections
    },
    {
      slug: "handling-sensitive-feedback",
      language: "english",
      languageLabel: "English",
      title: "Handling Sensitive Feedback",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Give sensitive feedback tactfully, focusing on impact and concrete next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Handling Sensitive Feedback di Indonesia.", caption: "Konteks percakapan nyata: Handling Sensitive Feedback." }
      },
      sections: lessonSections
    },
    {
      slug: "communicating-risk",
      language: "english",
      languageLabel: "English",
      title: "Communicating Risk",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Communicate risk clearly by describing likelihood, impact, and mitigation options.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Communicating Risk di Indonesia.", caption: "Konteks percakapan nyata: Communicating Risk." }
      },
      sections: lessonSections
    },
    {
      slug: "strategic-workplace-mission",
      language: "english",
      languageLabel: "English",
      title: "Strategic Workplace Mission",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Lead a strategic workplace conversation: align stakeholders, manage expectations, give sensitive feedback, and communicate risk.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Strategic Workplace Mission di Indonesia.", caption: "Konteks percakapan nyata: Strategic Workplace Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "framing-a-complex-topic",
      language: "english",
      languageLabel: "English",
      title: "Framing a Complex Topic",
      unit: "Advanced Presentations",
      conversationGoal: "Frame a complex topic by setting context, defining terms, and stating the purpose clearly.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Framing a Complex Topic di Indonesia.", caption: "Konteks percakapan nyata: Framing a Complex Topic." }
      },
      sections: lessonSections
    },
    {
      slug: "building-a-persuasive-flow",
      language: "english",
      languageLabel: "English",
      title: "Building a Persuasive Flow",
      unit: "Advanced Presentations",
      conversationGoal: "Build a persuasive flow by stating a claim, supporting it with evidence, and addressing counterarguments.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Building a Persuasive Flow di Indonesia.", caption: "Konteks percakapan nyata: Building a Persuasive Flow." }
      },
      sections: lessonSections
    },
    {
      slug: "using-precise-transitions",
      language: "english",
      languageLabel: "English",
      title: "Using Precise Transitions",
      unit: "Advanced Presentations",
      conversationGoal: "Use precise transitions to guide listeners through complex ideas smoothly.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Using Precise Transitions di Indonesia.", caption: "Konteks percakapan nyata: Using Precise Transitions." }
      },
      sections: lessonSections
    },
    {
      slug: "handling-challenging-questions",
      language: "english",
      languageLabel: "English",
      title: "Handling Challenging Questions",
      unit: "Advanced Presentations",
      conversationGoal: "Handle challenging questions by acknowledging concerns, answering precisely, and reframing when needed.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Handling Challenging Questions di Indonesia.", caption: "Konteks percakapan nyata: Handling Challenging Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "advanced-presentation-mission",
      language: "english",
      languageLabel: "English",
      title: "Advanced Presentation Mission",
      unit: "Advanced Presentations",
      conversationGoal: "Deliver an advanced presentation and handle challenging questions with clear signposting and strategic answers.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Advanced Presentation Mission di Indonesia.", caption: "Konteks percakapan nyata: Advanced Presentation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "identifying-assumptions",
      language: "english",
      languageLabel: "English",
      title: "Identifying Assumptions",
      unit: "Debate & Analysis",
      conversationGoal: "Identify assumptions behind an argument and ask clarifying questions about the premise.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Identifying Assumptions di Indonesia.", caption: "Konteks percakapan nyata: Identifying Assumptions." }
      },
      sections: lessonSections
    },
    {
      slug: "challenging-an-argument",
      language: "english",
      languageLabel: "English",
      title: "Challenging an Argument",
      unit: "Debate & Analysis",
      conversationGoal: "Challenge an argument constructively using counterexamples, alternative explanations, and precise questions.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Challenging an Argument di Indonesia.", caption: "Konteks percakapan nyata: Challenging an Argument." }
      },
      sections: lessonSections
    },
    {
      slug: "presenting-evidence",
      language: "english",
      languageLabel: "English",
      title: "Presenting Evidence",
      unit: "Debate & Analysis",
      conversationGoal: "Present evidence clearly, distinguish facts from interpretations, and reference sources confidently.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Presenting Evidence di Indonesia.", caption: "Konteks percakapan nyata: Presenting Evidence." }
      },
      sections: lessonSections
    },
    {
      slug: "responding-under-pressure",
      language: "english",
      languageLabel: "English",
      title: "Responding Under Pressure",
      unit: "Debate & Analysis",
      conversationGoal: "Respond under pressure by staying calm, addressing the core point, and tightening your argument.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding Under Pressure di Indonesia.", caption: "Konteks percakapan nyata: Responding Under Pressure." }
      },
      sections: lessonSections
    },
    {
      slug: "debate-analysis-mission",
      language: "english",
      languageLabel: "English",
      title: "Debate Analysis Mission",
      unit: "Debate & Analysis",
      conversationGoal: "Lead a debate-style discussion: identify assumptions, challenge claims, present evidence, and respond under pressure.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Debate Analysis Mission di Indonesia.", caption: "Konteks percakapan nyata: Debate Analysis Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "reading-context",
      language: "english",
      languageLabel: "English",
      title: "Reading Context",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Read context carefully by noticing tone, hierarchy, and implied expectations before responding.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Reading Context di Indonesia.", caption: "Konteks percakapan nyata: Reading Context." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-tactful-questions",
      language: "english",
      languageLabel: "English",
      title: "Asking Tactful Questions",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Ask tactful questions to clarify expectations, boundaries, and sensitive topics without causing discomfort.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking Tactful Questions di Indonesia.", caption: "Konteks percakapan nyata: Asking Tactful Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "explaining-local-norms",
      language: "english",
      languageLabel: "English",
      title: "Explaining Local Norms",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Explain local work norms tactfully and help others adapt without sounding judgmental.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining Local Norms di Indonesia.", caption: "Konteks percakapan nyata: Explaining Local Norms." }
      },
      sections: lessonSections
    },
    {
      slug: "repairing-misunderstanding",
      language: "english",
      languageLabel: "English",
      title: "Repairing Misunderstanding",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Repair a misunderstanding by acknowledging it, clarifying intent, and proposing a constructive next step.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Repairing Misunderstanding di Indonesia.", caption: "Konteks percakapan nyata: Repairing Misunderstanding." }
      },
      sections: lessonSections
    },
    {
      slug: "cross-cultural-mission",
      language: "english",
      languageLabel: "English",
      title: "Cross-cultural Mission",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Handle a cross-cultural situation: read context, ask tactful questions, explain norms, and repair misunderstandings.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Cross-cultural Mission di Indonesia.", caption: "Konteks percakapan nyata: Cross-cultural Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "setting-direction",
      language: "english",
      languageLabel: "English",
      title: "Setting Direction",
      unit: "Leadership & Coaching",
      conversationGoal: "Set direction by clarifying priorities, success criteria, and ownership.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Setting Direction di Indonesia.", caption: "Konteks percakapan nyata: Setting Direction." }
      },
      sections: lessonSections
    },
    {
      slug: "coaching-with-questions",
      language: "english",
      languageLabel: "English",
      title: "Coaching with Questions",
      unit: "Leadership & Coaching",
      conversationGoal: "Coach others using questions that build ownership, clarify thinking, and unblock decisions.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Coaching with Questions di Indonesia.", caption: "Konteks percakapan nyata: Coaching with Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "giving-actionable-feedback",
      language: "english",
      languageLabel: "English",
      title: "Giving Actionable Feedback",
      unit: "Leadership & Coaching",
      conversationGoal: "Give actionable feedback by describing impact, being specific, and proposing a clear improvement.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Giving Actionable Feedback di Indonesia.", caption: "Konteks percakapan nyata: Giving Actionable Feedback." }
      },
      sections: lessonSections
    },
    {
      slug: "guiding-a-decision",
      language: "english",
      languageLabel: "English",
      title: "Guiding a Decision",
      unit: "Leadership & Coaching",
      conversationGoal: "Guide a decision by structuring options, trade-offs, and a clear recommendation.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Guiding a Decision di Indonesia.", caption: "Konteks percakapan nyata: Guiding a Decision." }
      },
      sections: lessonSections
    },
    {
      slug: "leadership-coaching-mission",
      language: "english",
      languageLabel: "English",
      title: "Leadership Coaching Mission",
      unit: "Leadership & Coaching",
      conversationGoal: "Lead a coaching conversation: set direction, ask coaching questions, give actionable feedback, and guide a decision.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Leadership Coaching Mission di Indonesia.", caption: "Konteks percakapan nyata: Leadership Coaching Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "catching-implied-meaning",
      language: "english",
      languageLabel: "English",
      title: "Catching Implied Meaning",
      unit: "Advanced Listening & Response",
      conversationGoal: "Catch implied meaning by listening for hints, hedges, and what is not said explicitly.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Catching Implied Meaning di Indonesia.", caption: "Konteks percakapan nyata: Catching Implied Meaning." }
      },
      sections: lessonSections
    },
    {
      slug: "responding-to-long-turns",
      language: "english",
      languageLabel: "English",
      title: "Responding to Long Turns",
      unit: "Advanced Listening & Response",
      conversationGoal: "Respond to long turns by extracting key points, acknowledging emotions, and replying in a structured way.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding to Long Turns di Indonesia.", caption: "Konteks percakapan nyata: Responding to Long Turns." }
      },
      sections: lessonSections
    },
    {
      slug: "summarizing-what-you-heard",
      language: "english",
      languageLabel: "English",
      title: "Summarizing What You Heard",
      unit: "Advanced Listening & Response",
      conversationGoal: "Summarize accurately by separating facts, concerns, and decisions, then confirm with the speaker.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Summarizing What You Heard di Indonesia.", caption: "Konteks percakapan nyata: Summarizing What You Heard." }
      },
      sections: lessonSections
    },
    {
      slug: "asking-high-quality-follow-ups",
      language: "english",
      languageLabel: "English",
      title: "Asking High-quality Follow-ups",
      unit: "Advanced Listening & Response",
      conversationGoal: "Ask high-quality follow-up questions that clarify scope, assumptions, and next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking High-quality Follow-ups di Indonesia.", caption: "Konteks percakapan nyata: Asking High-quality Follow-ups." }
      },
      sections: lessonSections
    },
    {
      slug: "advanced-listening-mission",
      language: "english",
      languageLabel: "English",
      title: "Advanced Listening Mission",
      unit: "Advanced Listening & Response",
      conversationGoal: "Handle advanced listening: implied meaning, long turns, accurate summary, and high-quality follow-ups.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Advanced Listening Mission di Indonesia.", caption: "Konteks percakapan nyata: Advanced Listening Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "review-nuance-and-strategy",
      language: "english",
      languageLabel: "English",
      title: "Review Nuance and Strategy",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Express a nuanced position, manage expectations, and align stakeholders on a careful plan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Nuance and Strategy di Indonesia.", caption: "Konteks percakapan nyata: Review Nuance and Strategy." }
      },
      sections: lessonSections
    },
    {
      slug: "review-presenting-and-debate",
      language: "english",
      languageLabel: "English",
      title: "Review Presenting and Debate",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Present a structured argument, challenge assumptions respectfully, and respond under pressure with clarity.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Presenting and Debate di Indonesia.", caption: "Konteks percakapan nyata: Review Presenting and Debate." }
      },
      sections: lessonSections
    },
    {
      slug: "review-leadership-and-listening",
      language: "english",
      languageLabel: "English",
      title: "Review Leadership and Listening",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Coach someone with questions, catch implied meaning, and align on a decision with clear next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Leadership and Listening di Indonesia.", caption: "Konteks percakapan nyata: Review Leadership and Listening." }
      },
      sections: lessonSections
    },
    {
      slug: "c1-final-test-practice",
      language: "english",
      languageLabel: "English",
      title: "C1 Final Test Practice",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Answer C1-style prompts with nuance, structure, and precise language under time pressure.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks C1 Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: C1 Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "c1-final-conversation",
      language: "english",
      languageLabel: "English",
      title: "C1 Final Conversation",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Lead a complex conversation from framing to decision: nuance, debate, leadership listening, and clear next steps.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks C1 Final Conversation di Indonesia.", caption: "Konteks percakapan nyata: C1 Final Conversation." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-formal-greetings",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Formal Greetings",
      unit: "Arabic Foundations",
      conversationGoal: "Latih sapaan formal sederhana dan jawaban kabar dalam bahasa Arab.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Formal Greetings di Indonesia.", caption: "Konteks percakapan nyata: Formal Greetings." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-name-and-origin",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Name and Origin",
      unit: "Arabic Foundations",
      conversationGoal: "Latih menyebutkan nama dan asal negara, lalu tanyakan balik dengan sopan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Name and Origin di Indonesia.", caption: "Konteks percakapan nyata: Name and Origin." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-class-and-study-instructions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Class and Study Instructions",
      unit: "Arabic Foundations",
      conversationGoal: "Latih memahami dan merespons instruksi dasar dalam kelas Arab atau lesson terpandu.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Class and Study Instructions di Indonesia.", caption: "Konteks percakapan nyata: Class and Study Instructions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-when-you-do-not-understand",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking When You Do Not Understand",
      unit: "Arabic Foundations",
      conversationGoal: "Latih mengatakan belum paham, lalu minta pengulangan atau penjelasan makna kata.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking When You Do Not Understand di Indonesia.", caption: "Konteks percakapan nyata: Asking When You Do Not Understand." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-fusha-introduction-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Arabic Introduction Mission",
      unit: "Arabic Foundations",
      conversationGoal: "Latih perkenalan Arab singkat memakai sapaan, nama, asal, dan frasa klarifikasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Arabic Introduction Mission di Indonesia.", caption: "Konteks percakapan nyata: Arabic Introduction Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-spelling-your-name",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Spelling Your Name",
      unit: "Letters, Numbers & Contact",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu mengisi formulir kelas. Guru meminta kamu mengeja nama dengan huruf Arab sederhana.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Spelling Your Name di Indonesia.", caption: "Konteks percakapan nyata: Spelling Your Name." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-numbers-and-phone",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Arabic Numbers and Phone",
      unit: "Letters, Numbers & Contact",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu bertukar nomor telepon dengan teman kelas. Kamu perlu mengucapkan angka pelan dan jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Arabic Numbers and Phone di Indonesia.", caption: "Konteks percakapan nyata: Arabic Numbers and Phone." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-sharing-email-addresses",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Sharing Email Addresses",
      unit: "Letters, Numbers & Contact",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menulis email di daftar kelas. Kamu perlu menyebutkan bagian email dengan pelan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Sharing Email Addresses di Indonesia.", caption: "Konteks percakapan nyata: Sharing Email Addresses." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-to-repeat-a-letter",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking to Repeat a Letter",
      unit: "Letters, Numbers & Contact",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Saat mendengar nama atau email, kamu tidak yakin satu huruf. Kamu meminta pengulangan dengan sopan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking to Repeat a Letter di Indonesia.", caption: "Konteks percakapan nyata: Asking to Repeat a Letter." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-contact-details-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Contact Details Mission",
      unit: "Letters, Numbers & Contact",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu memperkenalkan diri di kelas baru dan memberikan informasi kontak sederhana.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Contact Details Mission di Indonesia.", caption: "Konteks percakapan nyata: Contact Details Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-the-time",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking the Time",
      unit: "Time & Daily Routine",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menunggu kelas dimulai dan ingin tahu jam sekarang.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking the Time di Indonesia.", caption: "Konteks percakapan nyata: Asking the Time." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-days-of-the-week",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Days of the Week",
      unit: "Time & Daily Routine",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu melihat jadwal kelas dan perlu menyebut hari ini serta hari berikutnya.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Days of the Week di Indonesia.", caption: "Konteks percakapan nyata: Days of the Week." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-talking-about-daily-routines",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Talking About Daily Routines",
      unit: "Time & Daily Routine",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menceritakan rutinitas pagi dengan kalimat Arab yang sangat pendek.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About Daily Routines di Indonesia.", caption: "Konteks percakapan nyata: Talking About Daily Routines." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-when",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking When",
      unit: "Time & Daily Routine",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu perlu bertanya kapan kelas, latihan, atau pertemuan dimulai.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking When di Indonesia.", caption: "Konteks percakapan nyata: Asking When." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-routine-and-time-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Routine and Time Mission",
      unit: "Time & Daily Routine",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menjelaskan jadwal belajar sederhana kepada teman kelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Routine and Time Mission di Indonesia.", caption: "Konteks percakapan nyata: Routine and Time Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-family-members",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Family Members",
      unit: "Family, Work & Study",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menunjukkan foto keluarga dan menyebut anggota keluarga dengan kalimat pendek.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Family Members di Indonesia.", caption: "Konteks percakapan nyata: Family Members." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-saying-what-you-do",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Saying What You Do",
      unit: "Family, Work & Study",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu memperkenalkan pekerjaan atau status belajar dalam percakapan formal ringan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying What You Do di Indonesia.", caption: "Konteks percakapan nyata: Saying What You Do." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-about-work-or-study",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking About Work or Study",
      unit: "Family, Work & Study",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu bertanya kepada teman baru tentang tempat belajar dan bidang yang dipelajari.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Asking About Work or Study di Indonesia.", caption: "Konteks percakapan nyata: Asking About Work or Study." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-likes-and-ability",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Likes and Ability",
      unit: "Family, Work & Study",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menyebut hal yang disukai dan kemampuan sederhana dalam konteks belajar.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Likes and Ability di Indonesia.", caption: "Konteks percakapan nyata: Likes and Ability." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-family-work-study-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Family, Work, and Study Mission",
      unit: "Family, Work & Study",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu memperkenalkan diri sedikit lebih lengkap: keluarga, pekerjaan/belajar, dan minat.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Family, Work, and Study Mission di Indonesia.", caption: "Konteks percakapan nyata: Family, Work, and Study Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-where-a-place-is",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking Where a Place Is",
      unit: "Places & Directions",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu mencari perpustakaan di gedung belajar dan bertanya dengan sopan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking Where a Place Is di Indonesia.", caption: "Konteks percakapan nyata: Asking Where a Place Is." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-simple-place-words",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Simple Place Words",
      unit: "Places & Directions",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menyebut beberapa tempat umum yang sering muncul dalam percakapan formal.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Simple Place Words di Indonesia.", caption: "Konteks percakapan nyata: Simple Place Words." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-understanding-simple-directions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Understanding Simple Directions",
      unit: "Places & Directions",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menerima arahan singkat menuju kelas atau perpustakaan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Understanding Simple Directions di Indonesia.", caption: "Konteks percakapan nyata: Understanding Simple Directions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-how-to-get-there",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking How to Get There",
      unit: "Places & Directions",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu meminta arahan menuju tempat tertentu di sekitar kelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking How to Get There di Indonesia.", caption: "Konteks percakapan nyata: Asking How to Get There." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-finding-a-place-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Finding a Place Mission",
      unit: "Places & Directions",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu mencari kelas baru, bertanya lokasi, dan mengikuti arahan singkat.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Finding a Place Mission di Indonesia.", caption: "Konteks percakapan nyata: Finding a Place Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-ordering-a-drink",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Ordering a Drink",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu berada di kafe dan ingin memesan minuman sederhana dengan sopan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Ordering a Drink di Indonesia.", caption: "Konteks percakapan nyata: Ordering a Drink." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-about-prices",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking About Prices",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu melihat barang sederhana dan perlu menanyakan harganya.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Prices di Indonesia.", caption: "Konteks percakapan nyata: Asking About Prices." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-buying-a-simple-item",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Buying a Simple Item",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu membeli alat tulis sederhana untuk kelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Buying a Simple Item di Indonesia.", caption: "Konteks percakapan nyata: Buying a Simple Item." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-saying-what-you-want",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Saying What You Want",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menjawab pertanyaan sederhana tentang apa yang diinginkan atau dibutuhkan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying What You Want di Indonesia.", caption: "Konteks percakapan nyata: Saying What You Want." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-cafe-and-shop-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Cafe and Shop Mission",
      unit: "Food, Shopping & Prices",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu memesan minuman, bertanya harga, dan membeli satu barang sederhana.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Cafe and Shop Mission di Indonesia.", caption: "Konteks percakapan nyata: Cafe and Shop Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-saying-you-do-not-understand",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Saying You Do Not Understand",
      unit: "Help, Problems & Requests",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu tidak paham kata atau instruksi dan perlu menjelaskannya dengan sopan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying You Do Not Understand di Indonesia.", caption: "Konteks percakapan nyata: Saying You Do Not Understand." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-for-help",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking for Help",
      unit: "Help, Problems & Requests",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu kesulitan menemukan halaman atau latihan dan perlu meminta bantuan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for Help di Indonesia.", caption: "Konteks percakapan nyata: Asking for Help." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-making-simple-requests",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Making Simple Requests",
      unit: "Help, Problems & Requests",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu meminta teman atau guru melakukan instruksi sederhana dalam konteks belajar.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making Simple Requests di Indonesia.", caption: "Konteks percakapan nyata: Making Simple Requests." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-apologizing-and-thanking",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Apologizing and Thanking",
      unit: "Help, Problems & Requests",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu terlambat merespons atau membuat kesalahan kecil dan ingin menjawab sopan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Apologizing and Thanking di Indonesia.", caption: "Konteks percakapan nyata: Apologizing and Thanking." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-help-and-problem-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Help and Problem Mission",
      unit: "Help, Problems & Requests",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menghadapi masalah kecil dalam kelas dan menyelesaikannya dengan permintaan sopan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Help and Problem Mission di Indonesia.", caption: "Konteks percakapan nyata: Help and Problem Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-review-introductions-and-contact",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Introductions and Contact",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu mengulang perkenalan, asal, ejaan nama, dan informasi kontak sederhana.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Introductions and Contact di Indonesia.", caption: "Konteks percakapan nyata: Review Introductions and Contact." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-review-routine-and-study",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Routine and Study",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menceritakan jadwal belajar bahasa Arab dan aktivitas sederhana.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Routine and Study di Indonesia.", caption: "Konteks percakapan nyata: Review Routine and Study." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-review-places-and-shopping",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Places and Shopping",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu mencari kafe, bertanya arah, lalu membeli minuman sederhana.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Places and Shopping di Indonesia.", caption: "Konteks percakapan nyata: Review Places and Shopping." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-a1-final-test-practice",
      language: "arabic",
      languageLabel: "Arabic",
      title: "A1 Final Test Practice",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu berlatih menjawab pertanyaan final A1 secara singkat dan jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks A1 Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: A1 Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-a1-final-conversation",
      language: "arabic",
      languageLabel: "Arabic",
      title: "A1 Final Conversation",
      unit: "A1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab sederhana untuk situasi ini: Kamu menjalani percakapan final: perkenalan, rutinitas belajar, tempat, belanja, dan bantuan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks A1 Final Conversation di Indonesia.", caption: "Konteks percakapan nyata: A1 Final Conversation." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-reconnecting-after-class",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Reconnecting After Class",
      unit: "Social Follow-up",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu bertemu teman setelah kelas bahasa Arab dan membuka percakapan singkat dengan kabar, kelas, dan rencana belajar.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Reconnecting After Class di Indonesia.", caption: "Konteks percakapan nyata: Reconnecting After Class." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-follow-up-questions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking Follow-up Questions",
      unit: "Social Follow-up",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu berbicara dengan teman kelas dan menjaga percakapan tetap berjalan dengan pertanyaan lanjutan yang sederhana.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking Follow-up Questions di Indonesia.", caption: "Konteks percakapan nyata: Asking Follow-up Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-talking-about-the-weekend",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Talking About the Weekend",
      unit: "Social Follow-up",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menceritakan kegiatan akhir pekan secara pendek: ke mana pergi, dengan siapa, dan bagaimana rasanya.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About the Weekend di Indonesia.", caption: "Konteks percakapan nyata: Talking About the Weekend." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-reacting-with-interest",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Reacting With Interest",
      unit: "Social Follow-up",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu merespons cerita teman dengan ekspresi pendek yang sopan, lalu bertanya satu pertanyaan lanjutan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Reacting With Interest di Indonesia.", caption: "Konteks percakapan nyata: Reacting With Interest." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-social-follow-up-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Social Follow-up Mission",
      unit: "Social Follow-up",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menjaga percakapan singkat dengan teman: membuka kabar, menanyakan kegiatan, memberi reaksi, dan menutup dengan rencana sederhana.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Social Follow-up Mission di Indonesia.", caption: "Konteks percakapan nyata: Social Follow-up Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-making-a-simple-plan",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Making a Simple Plan",
      unit: "Plans & Invitations",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu membuat rencana sederhana dengan teman: menentukan kegiatan, hari, waktu, dan tempat bertemu.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making a Simple Plan di Indonesia.", caption: "Konteks percakapan nyata: Making a Simple Plan." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-inviting-someone",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Inviting Someone",
      unit: "Plans & Invitations",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu mengajak teman ikut belajar bersama dan menjelaskan alasan singkat mengapa kegiatan itu bermanfaat.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Inviting Someone di Indonesia.", caption: "Konteks percakapan nyata: Inviting Someone." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-accepting-and-declining",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Accepting and Declining",
      unit: "Plans & Invitations",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menerima satu ajakan dan menolak ajakan lain dengan sopan sambil memberi alasan pendek.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Accepting and Declining di Indonesia.", caption: "Konteks percakapan nyata: Accepting and Declining." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-rescheduling-politely",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Rescheduling Politely",
      unit: "Plans & Invitations",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu tidak bisa datang pada waktu awal, lalu meminta perubahan waktu dengan sopan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Rescheduling Politely di Indonesia.", caption: "Konteks percakapan nyata: Rescheduling Politely." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-invitation-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Invitation Mission",
      unit: "Plans & Invitations",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu membuat rencana belajar bersama, mengajak teman, menerima perubahan waktu, dan mengonfirmasi detail akhir.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Invitation Mission di Indonesia.", caption: "Konteks percakapan nyata: Invitation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-buying-a-ticket",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Buying a Ticket",
      unit: "Transport & Travel",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu berada di loket stasiun dan ingin membeli tiket sederhana: tujuan, jenis tiket, kelas, dan harga.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Buying a Ticket di Indonesia.", caption: "Konteks percakapan nyata: Buying a Ticket." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-about-departure-time",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking About Departure Time",
      unit: "Transport & Travel",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu sudah punya tiket dan ingin memastikan jam keberangkatan, peron, serta waktu tiba.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Departure Time di Indonesia.", caption: "Konteks percakapan nyata: Asking About Departure Time." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-checking-directions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Checking Directions",
      unit: "Transport & Travel",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu berada di terminal dan ingin memastikan arah menuju pintu, peron, atau tempat tunggu tanpa salah jalur.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Checking Directions di Indonesia.", caption: "Konteks percakapan nyata: Checking Directions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-talking-to-a-driver",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Talking to a Driver",
      unit: "Transport & Travel",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu naik taksi atau kendaraan online dan perlu memastikan tujuan, waktu perjalanan, dan tempat turun.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking to a Driver di Indonesia.", caption: "Konteks percakapan nyata: Talking to a Driver." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-transport-travel-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Transport and Travel Mission",
      unit: "Transport & Travel",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menyelesaikan perjalanan pendek: membeli tiket, mengecek jam berangkat, mencari peron, lalu memastikan tujuan dengan sopir.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Transport and Travel Mission di Indonesia.", caption: "Konteks percakapan nyata: Transport and Travel Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-for-an-item",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking for an Item",
      unit: "Shopping & Services",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu berada di toko alat tulis dan ingin meminta barang tertentu, menanyakan pilihan warna, lalu memutuskan membeli satu barang.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for an Item di Indonesia.", caption: "Konteks percakapan nyata: Asking for an Item." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-about-size-and-color",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking About Size and Color",
      unit: "Shopping & Services",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu membeli pakaian sederhana dan perlu menanyakan ukuran, warna, serta izin mencoba barang.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Size and Color di Indonesia.", caption: "Konteks percakapan nyata: Asking About Size and Color." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-comparing-simple-options",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Comparing Simple Options",
      unit: "Shopping & Services",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu membandingkan dua barang sederhana berdasarkan harga, kualitas, dan kecocokan sebelum memilih.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Comparing Simple Options di Indonesia.", caption: "Konteks percakapan nyata: Comparing Simple Options." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-requesting-service-help",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Requesting Service Help",
      unit: "Shopping & Services",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu datang ke bagian layanan karena sebuah perangkat tidak bekerja dan kamu perlu menjelaskan masalahnya dengan sopan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Requesting Service Help di Indonesia.", caption: "Konteks percakapan nyata: Requesting Service Help." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-shopping-service-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Shopping Service Mission",
      unit: "Shopping & Services",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu memilih barang di toko, membandingkan pilihan, lalu berpindah ke bagian layanan untuk meminta bantuan perangkat.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Shopping Service Mission di Indonesia.", caption: "Konteks percakapan nyata: Shopping Service Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-saying-how-you-feel",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Saying How You Feel",
      unit: "Health & Appointments",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu datang ke klinik dan perlu mengatakan kondisi umum dengan sederhana sebelum petugas mencatat informasi awal.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Saying How You Feel di Indonesia.", caption: "Konteks percakapan nyata: Saying How You Feel." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-describing-simple-symptoms",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Describing Simple Symptoms",
      unit: "Health & Appointments",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu berbicara dengan petugas kesehatan dan menjelaskan gejala ringan secara jelas: bagian tubuh, intensitas, dan durasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing Simple Symptoms di Indonesia.", caption: "Konteks percakapan nyata: Describing Simple Symptoms." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-making-an-appointment",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Making an Appointment",
      unit: "Health & Appointments",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menelepon klinik untuk membuat janji, memilih hari dan waktu, serta menyebut nama untuk pendaftaran.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Making an Appointment di Indonesia.", caption: "Konteks percakapan nyata: Making an Appointment." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-confirming-appointment-details",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Confirming Appointment Details",
      unit: "Health & Appointments",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu ingin memastikan ulang detail janji: nama, tanggal, waktu, lokasi, dan nomor kontak.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Confirming Appointment Details di Indonesia.", caption: "Konteks percakapan nyata: Confirming Appointment Details." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-health-appointment-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Health Appointment Mission",
      unit: "Health & Appointments",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menjelaskan kondisi ringan, membuat janji, lalu mengonfirmasi detail appointment dengan petugas klinik.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Health Appointment Mission di Indonesia.", caption: "Konteks percakapan nyata: Health Appointment Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-talking-about-yesterday",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Talking About Yesterday",
      unit: "Past Experiences",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu bertemu teman setelah kelas dan menceritakan kegiatan kemarin dengan kalimat pendek.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About Yesterday di Indonesia.", caption: "Konteks percakapan nyata: Talking About Yesterday." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-saying-where-you-went",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Saying Where You Went",
      unit: "Past Experiences",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menceritakan tempat yang kamu datangi akhir pekan lalu: pasar, taman, rumah teman, atau pusat kota.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying Where You Went di Indonesia.", caption: "Konteks percakapan nyata: Saying Where You Went." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-describing-a-simple-experience",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Describing a Simple Experience",
      unit: "Past Experiences",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menceritakan pengalaman sederhana di tempat umum: apa yang kamu lihat, apa yang kamu lakukan, dan bagaimana rasanya.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing a Simple Experience di Indonesia.", caption: "Konteks percakapan nyata: Describing a Simple Experience." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-about-past-activities",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking About Past Activities",
      unit: "Past Experiences",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu ingin menjaga percakapan tetap berjalan dengan bertanya tentang aktivitas masa lalu teman secara sopan dan natural.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Past Activities di Indonesia.", caption: "Konteks percakapan nyata: Asking About Past Activities." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-past-experience-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Past Experience Mission",
      unit: "Past Experiences",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menceritakan pengalaman akhir pekan dan menjawab pertanyaan lanjutan tentang tempat, teman, kegiatan, dan kesan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Past Experience Mission di Indonesia.", caption: "Konteks percakapan nyata: Past Experience Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-saying-what-you-think",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Saying What You Think",
      unit: "Opinions & Reasons",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu berdiskusi santai setelah kelas dan ingin menyampaikan pendapat tentang pelajaran, tempat belajar, atau aktivitas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Saying What You Think di Indonesia.", caption: "Konteks percakapan nyata: Saying What You Think." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-giving-simple-reasons",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Giving Simple Reasons",
      unit: "Opinions & Reasons",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menjelaskan alasan pendek untuk pendapatmu: karena mudah, dekat, murah, jelas, atau cocok untuk jadwalmu.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Giving Simple Reasons di Indonesia.", caption: "Konteks percakapan nyata: Giving Simple Reasons." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-agreeing-and-disagreeing-politely",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Agreeing and Disagreeing Politely",
      unit: "Opinions & Reasons",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu berdiskusi dengan teman dan perlu setuju, kurang setuju, atau memberi pendapat berbeda tanpa terdengar kasar.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Agreeing and Disagreeing Politely di Indonesia.", caption: "Konteks percakapan nyata: Agreeing and Disagreeing Politely." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-asking-for-opinions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking for Opinions",
      unit: "Opinions & Reasons",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu meminta pendapat teman sebelum memilih tempat, waktu, aktivitas, atau opsi sederhana.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for Opinions di Indonesia.", caption: "Konteks percakapan nyata: Asking for Opinions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-opinion-conversation-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Opinion Conversation Mission",
      unit: "Opinions & Reasons",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu memilih rencana belajar bersama teman: meminta pendapat, memberi alasan, setuju/kurang setuju, lalu mengambil keputusan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Opinion Conversation Mission di Indonesia.", caption: "Konteks percakapan nyata: Opinion Conversation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-review-social-and-plans",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Social and Plans",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu bertemu teman setelah kelas, bertanya kabar, menanyakan rencana, lalu menentukan waktu belajar bersama.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Social and Plans di Indonesia.", caption: "Konteks percakapan nyata: Review Social and Plans." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-review-travel-and-services",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Travel and Services",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu membeli tiket, menanyakan arah, lalu meminta bantuan layanan untuk barang kecil yang bermasalah.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Travel and Services di Indonesia.", caption: "Konteks percakapan nyata: Review Travel and Services." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-review-health-and-past",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Health and Past",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menghubungi klinik, menjelaskan gejala ringan, lalu menceritakan aktivitas kemarin yang mungkin perlu dicatat.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Review Health and Past di Indonesia.", caption: "Konteks percakapan nyata: Review Health and Past." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-a2-final-test-practice",
      language: "arabic",
      languageLabel: "Arabic",
      title: "A2 Final Test Practice",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu latihan simulasi tes A2: menjawab pertanyaan sosial, membuat rencana, menceritakan pengalaman, dan memberi pendapat pendek.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks A2 Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: A2 Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-a2-final-conversation",
      language: "arabic",
      languageLabel: "Arabic",
      title: "A2 Final Conversation",
      unit: "A2 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab A2 untuk situasi ini: Kamu menyelesaikan percakapan A2 lengkap: bertemu teman, membahas pengalaman, membuat rencana, menangani kebutuhan layanan, dan memberi pendapat.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks A2 Final Conversation di Indonesia.", caption: "Konteks percakapan nyata: A2 Final Conversation." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-setting-the-scene",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Setting the Scene",
      unit: "Personal Stories",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu membuka cerita pendek dengan waktu, tempat, dan orang yang terlibat sebelum masuk ke kejadian utama.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Setting the Scene di Indonesia.", caption: "Konteks percakapan nyata: Setting the Scene." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-telling-events-in-order",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Telling Events in Order",
      unit: "Personal Stories",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu menceritakan kejadian secara berurutan agar lawan bicara mudah mengikuti alurnya.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Telling Events in Order di Indonesia.", caption: "Konteks percakapan nyata: Telling Events in Order." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-describing-feelings",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Describing Feelings",
      unit: "Personal Stories",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu menjelaskan perasaan dalam cerita dan memberi alasan singkat mengapa merasa begitu.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing Feelings di Indonesia.", caption: "Konteks percakapan nyata: Describing Feelings." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-asking-about-someones-story",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking About Someone's Story",
      unit: "Personal Stories",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu bertanya lanjutan tentang cerita seseorang tanpa memotong alur pembicaraan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Someone's Story di Indonesia.", caption: "Konteks percakapan nyata: Asking About Someone's Story." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-personal-story-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Personal Story Mission",
      unit: "Personal Stories",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu menggabungkan konteks, urutan kejadian, perasaan, dan pertanyaan lanjutan dalam satu cerita.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Personal Story Mission di Indonesia.", caption: "Konteks percakapan nyata: Personal Story Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-explaining-your-task",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Explaining Your Task",
      unit: "Workplace Conversations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu menjelaskan tugas kerja atau belajar secara jelas: tujuan, langkah, dan hasil yang diharapkan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Explaining Your Task di Indonesia.", caption: "Konteks percakapan nyata: Explaining Your Task." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-asking-for-clarification",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking for Clarification",
      unit: "Workplace Conversations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu meminta klarifikasi ketika instruksi belum cukup jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Asking for Clarification di Indonesia.", caption: "Konteks percakapan nyata: Asking for Clarification." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-giving-a-short-update",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Giving a Short Update",
      unit: "Workplace Conversations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu memberi update singkat tentang progress, kendala, dan langkah berikutnya.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Giving a Short Update di Indonesia.", caption: "Konteks percakapan nyata: Giving a Short Update." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-joining-a-simple-meeting",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Joining a Simple Meeting",
      unit: "Workplace Conversations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu masuk meeting sederhana, memberi pendapat, dan menanyakan langkah berikutnya.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Joining a Simple Meeting di Indonesia.", caption: "Konteks percakapan nyata: Joining a Simple Meeting." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-workplace-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Workplace Mission",
      unit: "Workplace Conversations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu menjelaskan tugas, meminta klarifikasi, memberi update, dan menutup dengan action point.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Workplace Mission di Indonesia.", caption: "Konteks percakapan nyata: Workplace Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-describing-a-problem",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Describing a Problem",
      unit: "Problems & Solutions",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: describing a problem, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing a Problem di Indonesia.", caption: "Konteks percakapan nyata: Describing a Problem." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-suggesting-a-solution",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Suggesting a Solution",
      unit: "Problems & Solutions",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: suggesting a solution, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Suggesting a Solution di Indonesia.", caption: "Konteks percakapan nyata: Suggesting a Solution." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-responding-to-advice",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Responding to Advice",
      unit: "Problems & Solutions",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: responding to advice, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding to Advice di Indonesia.", caption: "Konteks percakapan nyata: Responding to Advice." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-making-a-simple-decision",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Making a Simple Decision",
      unit: "Problems & Solutions",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: making a simple decision, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making a Simple Decision di Indonesia.", caption: "Konteks percakapan nyata: Making a Simple Decision." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-problem-solving-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Problem Solving Mission",
      unit: "Problems & Solutions",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: problem solving mission, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Problem Solving Mission di Indonesia.", caption: "Konteks percakapan nyata: Problem Solving Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-checking-in",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Checking In",
      unit: "Travel Situations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: checking in, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Checking In di Indonesia.", caption: "Konteks percakapan nyata: Checking In." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-explaining-a-delay",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Explaining a Delay",
      unit: "Travel Situations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: explaining a delay, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining a Delay di Indonesia.", caption: "Konteks percakapan nyata: Explaining a Delay." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-asking-for-recommendations",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking for Recommendations",
      unit: "Travel Situations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: asking for recommendations, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking for Recommendations di Indonesia.", caption: "Konteks percakapan nyata: Asking for Recommendations." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-handling-a-simple-complaint",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Handling a Simple Complaint",
      unit: "Travel Situations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: handling a simple complaint, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Handling a Simple Complaint di Indonesia.", caption: "Konteks percakapan nyata: Handling a Simple Complaint." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-travel-situation-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Travel Situation Mission",
      unit: "Travel Situations",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: travel situation mission, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Travel Situation Mission di Indonesia.", caption: "Konteks percakapan nyata: Travel Situation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-talking-about-goals",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Talking About Goals",
      unit: "Goals & Progress",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: talking about goals, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Talking About Goals di Indonesia.", caption: "Konteks percakapan nyata: Talking About Goals." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-explaining-progress",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Explaining Progress",
      unit: "Goals & Progress",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: explaining progress, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Explaining Progress di Indonesia.", caption: "Konteks percakapan nyata: Explaining Progress." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-discussing-challenges",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Discussing Challenges",
      unit: "Goals & Progress",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: discussing challenges, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Discussing Challenges di Indonesia.", caption: "Konteks percakapan nyata: Discussing Challenges." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-making-next-step-plans",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Making Next-step Plans",
      unit: "Goals & Progress",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: making next-step plans, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Making Next-step Plans di Indonesia.", caption: "Konteks percakapan nyata: Making Next-step Plans." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-goals-progress-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Goals Progress Mission",
      unit: "Goals & Progress",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: goals progress mission, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Goals Progress Mission di Indonesia.", caption: "Konteks percakapan nyata: Goals Progress Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-comparing-two-options",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Comparing Two Options",
      unit: "Explaining Preferences",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: comparing two options, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Comparing Two Options di Indonesia.", caption: "Konteks percakapan nyata: Comparing Two Options." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-explaining-why-you-prefer-something",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Explaining Why You Prefer Something",
      unit: "Explaining Preferences",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: explaining why you prefer something, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Explaining Why You Prefer Something di Indonesia.", caption: "Konteks percakapan nyata: Explaining Why You Prefer Something." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-asking-about-pros-and-cons",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking About Pros and Cons",
      unit: "Explaining Preferences",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: asking about pros and cons, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Asking About Pros and Cons di Indonesia.", caption: "Konteks percakapan nyata: Asking About Pros and Cons." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-reaching-agreement",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Reaching Agreement",
      unit: "Explaining Preferences",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: reaching agreement, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Reaching Agreement di Indonesia.", caption: "Konteks percakapan nyata: Reaching Agreement." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-preference-discussion-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Preference Discussion Mission",
      unit: "Explaining Preferences",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: preference discussion mission, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Preference Discussion Mission di Indonesia.", caption: "Konteks percakapan nyata: Preference Discussion Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-describing-your-community",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Describing Your Community",
      unit: "Community & Culture",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: describing your community, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Describing Your Community di Indonesia.", caption: "Konteks percakapan nyata: Describing Your Community." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-talking-about-local-habits",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Talking About Local Habits",
      unit: "Community & Culture",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: talking about local habits, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Talking About Local Habits di Indonesia.", caption: "Konteks percakapan nyata: Talking About Local Habits." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-asking-about-culture",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking About Culture",
      unit: "Community & Culture",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: asking about culture, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking About Culture di Indonesia.", caption: "Konteks percakapan nyata: Asking About Culture." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-being-polite-with-differences",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Being Polite With Differences",
      unit: "Community & Culture",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: being polite with differences, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Being Polite With Differences di Indonesia.", caption: "Konteks percakapan nyata: Being Polite With Differences." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-community-culture-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Community Culture Mission",
      unit: "Community & Culture",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: community culture mission, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Community Culture Mission di Indonesia.", caption: "Konteks percakapan nyata: Community Culture Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-review-stories-and-work",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Stories and Work",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: review stories and work, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Stories and Work di Indonesia.", caption: "Konteks percakapan nyata: Review Stories and Work." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-review-problems-and-travel",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Problems and Travel",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: review problems and travel, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Problems and Travel di Indonesia.", caption: "Konteks percakapan nyata: Review Problems and Travel." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-review-goals-and-preferences",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Goals and Preferences",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: review goals and preferences, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Review Goals and Preferences di Indonesia.", caption: "Konteks percakapan nyata: Review Goals and Preferences." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-b1-final-test-practice",
      language: "arabic",
      languageLabel: "Arabic",
      title: "B1 Final Test Practice",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: b1 final test practice, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks B1 Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: B1 Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b1-b1-final-conversation",
      language: "arabic",
      languageLabel: "Arabic",
      title: "B1 Final Conversation",
      unit: "B1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab B1 untuk situasi ini: Kamu berlatih topik B1: b1 final conversation, dengan jawaban yang lebih terhubung dan alasan yang jelas.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks B1 Final Conversation di Indonesia.", caption: "Konteks percakapan nyata: B1 Final Conversation." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-stating-your-position",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Stating Your Position",
      unit: "Clear Arguments",
      conversationGoal: "Latih percakapan Arab B2 untuk menentukan posisi dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Stating Your Position di Indonesia.", caption: "Konteks percakapan nyata: Stating Your Position." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-supporting-with-reasons",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Supporting With Reasons",
      unit: "Clear Arguments",
      conversationGoal: "Latih percakapan Arab B2 untuk mendukung pendapat dengan alasan dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Supporting With Reasons di Indonesia.", caption: "Konteks percakapan nyata: Supporting With Reasons." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-using-examples",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Using Examples",
      unit: "Clear Arguments",
      conversationGoal: "Latih percakapan Arab B2 untuk menggunakan contoh dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Using Examples di Indonesia.", caption: "Konteks percakapan nyata: Using Examples." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-responding-to-counterpoints",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Responding to Counterpoints",
      unit: "Clear Arguments",
      conversationGoal: "Latih percakapan Arab B2 untuk menanggapi keberatan dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding to Counterpoints di Indonesia.", caption: "Konteks percakapan nyata: Responding to Counterpoints." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-clear-argument-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Clear Argument Mission",
      unit: "Clear Arguments",
      conversationGoal: "Latih percakapan Arab B2 untuk membangun argumen jelas dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Clear Argument Mission di Indonesia.", caption: "Konteks percakapan nyata: Clear Argument Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-opening-a-meeting-point",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Opening a Meeting Point",
      unit: "Professional Meetings",
      conversationGoal: "Latih percakapan Arab B2 untuk membuka topik rapat, memberi alasan, meminta keputusan, dan menutup dengan action item.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Opening a Meeting Point di Indonesia.", caption: "Konteks percakapan nyata: Opening a Meeting Point." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-clarifying-scope",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Clarifying Scope",
      unit: "Professional Meetings",
      conversationGoal: "Latih percakapan Arab B2 untuk memperjelas scope rapat, menetapkan batasan, dan mengonfirmasi tindak lanjut.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Clarifying Scope di Indonesia.", caption: "Konteks percakapan nyata: Clarifying Scope." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-giving-constructive-feedback",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Giving Constructive Feedback",
      unit: "Professional Meetings",
      conversationGoal: "Latih percakapan Arab B2 untuk memberi feedback konstruktif, menyebut kekuatan, memberi saran, dan menawarkan perbaikan.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Giving Constructive Feedback di Indonesia.", caption: "Konteks percakapan nyata: Giving Constructive Feedback." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-summarizing-decisions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Summarizing Decisions",
      unit: "Professional Meetings",
      conversationGoal: "Latih percakapan Arab B2 untuk merangkum keputusan rapat dengan jelas dan bisa ditindaklanjuti.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Summarizing Decisions di Indonesia.", caption: "Konteks percakapan nyata: Summarizing Decisions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-meeting-participation-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Meeting Participation Mission",
      unit: "Professional Meetings",
      conversationGoal: "Latih percakapan Arab B2 untuk berpartisipasi aktif dalam rapat profesional dari pembuka sampai ringkasan akhir.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Meeting Participation Mission di Indonesia.", caption: "Konteks percakapan nyata: Meeting Participation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-expressing-priorities",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Expressing Priorities",
      unit: "Negotiation & Compromise",
      conversationGoal: "Latih percakapan Arab B2 untuk menjelaskan prioritas dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Expressing Priorities di Indonesia.", caption: "Konteks percakapan nyata: Expressing Priorities." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-making-a-proposal",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Making a Proposal",
      unit: "Negotiation & Compromise",
      conversationGoal: "Latih percakapan Arab B2 untuk mengajukan usulan praktis dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Making a Proposal di Indonesia.", caption: "Konteks percakapan nyata: Making a Proposal." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-handling-objections",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Handling Objections",
      unit: "Negotiation & Compromise",
      conversationGoal: "Latih percakapan Arab B2 untuk menangani keberatan dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Handling Objections di Indonesia.", caption: "Konteks percakapan nyata: Handling Objections." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-finding-middle-ground",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Finding Middle Ground",
      unit: "Negotiation & Compromise",
      conversationGoal: "Latih percakapan Arab B2 untuk mencari jalan tengah dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Finding Middle Ground di Indonesia.", caption: "Konteks percakapan nyata: Finding Middle Ground." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-negotiation-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Negotiation Mission",
      unit: "Negotiation & Compromise",
      conversationGoal: "Latih percakapan Arab B2 untuk mengelola negosiasi jelas dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Negotiation Mission di Indonesia.", caption: "Konteks percakapan nyata: Negotiation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-structuring-a-short-presentation",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Structuring a Short Presentation",
      unit: "Presenting Ideas",
      conversationGoal: "Latih percakapan Arab B2 untuk menyusun presentasi singkat dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Structuring a Short Presentation di Indonesia.", caption: "Konteks percakapan nyata: Structuring a Short Presentation." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-signposting-clearly",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Signposting Clearly",
      unit: "Presenting Ideas",
      conversationGoal: "Latih percakapan Arab B2 untuk memberi transisi jelas dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Signposting Clearly di Indonesia.", caption: "Konteks percakapan nyata: Signposting Clearly." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-explaining-benefits-and-risks",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Explaining Benefits and Risks",
      unit: "Presenting Ideas",
      conversationGoal: "Latih percakapan Arab B2 untuk menjelaskan manfaat dan risiko dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Explaining Benefits and Risks di Indonesia.", caption: "Konteks percakapan nyata: Explaining Benefits and Risks." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-answering-questions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Answering Questions",
      unit: "Presenting Ideas",
      conversationGoal: "Latih percakapan Arab B2 untuk menjawab pertanyaan dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Answering Questions di Indonesia.", caption: "Konteks percakapan nyata: Answering Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-idea-presentation-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Idea Presentation Mission",
      unit: "Presenting Ideas",
      conversationGoal: "Latih percakapan Arab B2 untuk mempresentasikan dan mempertahankan ide dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Idea Presentation Mission di Indonesia.", caption: "Konteks percakapan nyata: Idea Presentation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-summarizing-an-article",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Summarizing an Article",
      unit: "Media & Information",
      conversationGoal: "Latih percakapan Arab B2 untuk merangkum artikel dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Summarizing an Article di Indonesia.", caption: "Konteks percakapan nyata: Summarizing an Article." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-discussing-reliable-sources",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Discussing Reliable Sources",
      unit: "Media & Information",
      conversationGoal: "Latih percakapan Arab B2 untuk membahas sumber tepercaya dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Discussing Reliable Sources di Indonesia.", caption: "Konteks percakapan nyata: Discussing Reliable Sources." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-explaining-a-viewpoint",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Explaining a Viewpoint",
      unit: "Media & Information",
      conversationGoal: "Latih percakapan Arab B2 untuk menjelaskan sudut pandang dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining a Viewpoint di Indonesia.", caption: "Konteks percakapan nyata: Explaining a Viewpoint." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-responding-to-new-information",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Responding to New Information",
      unit: "Media & Information",
      conversationGoal: "Latih percakapan Arab B2 untuk menanggapi informasi baru dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding to New Information di Indonesia.", caption: "Konteks percakapan nyata: Responding to New Information." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-information-discussion-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Information Discussion Mission",
      unit: "Media & Information",
      conversationGoal: "Latih percakapan Arab B2 untuk mengelola diskusi informasi dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Information Discussion Mission di Indonesia.", caption: "Konteks percakapan nyata: Information Discussion Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-understanding-client-needs",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Understanding Client Needs",
      unit: "Customer & Client Communication",
      conversationGoal: "Latih percakapan Arab B2 untuk memahami kebutuhan klien dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Understanding Client Needs di Indonesia.", caption: "Konteks percakapan nyata: Understanding Client Needs." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-explaining-options",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Explaining Options",
      unit: "Customer & Client Communication",
      conversationGoal: "Latih percakapan Arab B2 untuk menjelaskan opsi dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Explaining Options di Indonesia.", caption: "Konteks percakapan nyata: Explaining Options." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-handling-concerns",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Handling Concerns",
      unit: "Customer & Client Communication",
      conversationGoal: "Latih percakapan Arab B2 untuk menangani concern klien dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Handling Concerns di Indonesia.", caption: "Konteks percakapan nyata: Handling Concerns." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-confirming-next-steps",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Confirming Next Steps",
      unit: "Customer & Client Communication",
      conversationGoal: "Latih percakapan Arab B2 untuk mengonfirmasi langkah berikutnya dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Confirming Next Steps di Indonesia.", caption: "Konteks percakapan nyata: Confirming Next Steps." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-client-conversation-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Client Conversation Mission",
      unit: "Customer & Client Communication",
      conversationGoal: "Latih percakapan Arab B2 untuk mengelola percakapan dengan klien dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Client Conversation Mission di Indonesia.", caption: "Konteks percakapan nyata: Client Conversation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-framing-the-problem",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Framing the Problem",
      unit: "Complex Problem Solving",
      conversationGoal: "Latih percakapan Arab B2 untuk membingkai masalah dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Framing the Problem di Indonesia.", caption: "Konteks percakapan nyata: Framing the Problem." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-explaining-causes",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Explaining Causes",
      unit: "Complex Problem Solving",
      conversationGoal: "Latih percakapan Arab B2 untuk menjelaskan penyebab dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Explaining Causes di Indonesia.", caption: "Konteks percakapan nyata: Explaining Causes." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-discussing-tradeoffs",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Discussing Tradeoffs",
      unit: "Complex Problem Solving",
      conversationGoal: "Latih percakapan Arab B2 untuk membahas tradeoff dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Discussing Tradeoffs di Indonesia.", caption: "Konteks percakapan nyata: Discussing Tradeoffs." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-recommending-a-solution",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Recommending a Solution",
      unit: "Complex Problem Solving",
      conversationGoal: "Latih percakapan Arab B2 untuk merekomendasikan solusi dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Recommending a Solution di Indonesia.", caption: "Konteks percakapan nyata: Recommending a Solution." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-problem-solving-discussion-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Problem Solving Discussion Mission",
      unit: "Complex Problem Solving",
      conversationGoal: "Latih percakapan Arab B2 untuk mendiskusikan solusi masalah kompleks dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Problem Solving Discussion Mission di Indonesia.", caption: "Konteks percakapan nyata: Problem Solving Discussion Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-review-arguments-and-meetings",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Arguments and Meetings",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Latih percakapan Arab B2 untuk meninjau argumen dan rapat dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Review Arguments and Meetings di Indonesia.", caption: "Konteks percakapan nyata: Review Arguments and Meetings." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-review-negotiation-and-presenting",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Negotiation and Presenting",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Latih percakapan Arab B2 untuk meninjau negosiasi dan presentasi dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Review Negotiation and Presenting di Indonesia.", caption: "Konteks percakapan nyata: Review Negotiation and Presenting." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-review-information-and-clients",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Information and Clients",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Latih percakapan Arab B2 untuk meninjau cara menangani informasi dan klien dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Review Information and Clients di Indonesia.", caption: "Konteks percakapan nyata: Review Information and Clients." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-b2-final-test-practice",
      language: "arabic",
      languageLabel: "Arabic",
      title: "B2 Final Test Practice",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Latih percakapan Arab B2 untuk mempersiapkan tes akhir dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks B2 Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: B2 Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-b2-b2-final-discussion",
      language: "arabic",
      languageLabel: "Arabic",
      title: "B2 Final Discussion",
      unit: "B2 Review & Final Discussion",
      conversationGoal: "Latih percakapan Arab B2 untuk menjalani diskusi akhir dengan alasan, contoh, respons, dan rekomendasi.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks B2 Final Discussion di Indonesia.", caption: "Konteks percakapan nyata: B2 Final Discussion." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-qualifying-your-opinion",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Qualifying Your Opinion",
      unit: "Nuanced Opinions",
      conversationGoal: "Latih percakapan Arab C1 untuk qualifying opinion before making a claim dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Qualifying Your Opinion di Indonesia.", caption: "Konteks percakapan nyata: Qualifying Your Opinion." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-expressing-certainty-and-doubt",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Expressing Certainty and Doubt",
      unit: "Nuanced Opinions",
      conversationGoal: "Latih percakapan Arab C1 untuk separating certainty and doubt dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Expressing Certainty and Doubt di Indonesia.", caption: "Konteks percakapan nyata: Expressing Certainty and Doubt." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-balancing-two-viewpoints",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Balancing Two Viewpoints",
      unit: "Nuanced Opinions",
      conversationGoal: "Latih percakapan Arab C1 untuk balancing two viewpoints dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Balancing Two Viewpoints di Indonesia.", caption: "Konteks percakapan nyata: Balancing Two Viewpoints." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-softening-disagreement",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Softening Disagreement",
      unit: "Nuanced Opinions",
      conversationGoal: "Latih percakapan Arab C1 untuk softening disagreement dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Softening Disagreement di Indonesia.", caption: "Konteks percakapan nyata: Softening Disagreement." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-nuanced-opinion-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Nuanced Opinion Mission",
      unit: "Nuanced Opinions",
      conversationGoal: "Latih percakapan Arab C1 untuk building a complete nuanced opinion dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Nuanced Opinion Mission di Indonesia.", caption: "Konteks percakapan nyata: Nuanced Opinion Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-aligning-stakeholders",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Aligning Stakeholders",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Latih percakapan Arab C1 untuk aligning stakeholders dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Aligning Stakeholders di Indonesia.", caption: "Konteks percakapan nyata: Aligning Stakeholders." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-managing-expectations",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Managing Expectations",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Latih percakapan Arab C1 untuk managing realistic expectations dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Managing Expectations di Indonesia.", caption: "Konteks percakapan nyata: Managing Expectations." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-handling-sensitive-feedback",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Handling Sensitive Feedback",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Latih percakapan Arab C1 untuk handling sensitive feedback tactfully dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Handling Sensitive Feedback di Indonesia.", caption: "Konteks percakapan nyata: Handling Sensitive Feedback." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-communicating-risk",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Communicating Risk",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Latih percakapan Arab C1 untuk communicating risk without exaggeration dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Communicating Risk di Indonesia.", caption: "Konteks percakapan nyata: Communicating Risk." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-strategic-workplace-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Strategic Workplace Mission",
      unit: "Strategic Workplace Communication",
      conversationGoal: "Latih percakapan Arab C1 untuk running a strategic workplace conversation dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Strategic Workplace Mission di Indonesia.", caption: "Konteks percakapan nyata: Strategic Workplace Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-framing-a-complex-topic",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Framing a Complex Topic",
      unit: "Advanced Presentations",
      conversationGoal: "Latih percakapan Arab C1 untuk framing a complex topic dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Framing a Complex Topic di Indonesia.", caption: "Konteks percakapan nyata: Framing a Complex Topic." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-building-a-persuasive-flow",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Building a Persuasive Flow",
      unit: "Advanced Presentations",
      conversationGoal: "Latih percakapan Arab C1 untuk building a persuasive flow dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Building a Persuasive Flow di Indonesia.", caption: "Konteks percakapan nyata: Building a Persuasive Flow." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-using-precise-transitions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Using Precise Transitions",
      unit: "Advanced Presentations",
      conversationGoal: "Latih percakapan Arab C1 untuk using precise transitions dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Using Precise Transitions di Indonesia.", caption: "Konteks percakapan nyata: Using Precise Transitions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-handling-challenging-questions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Handling Challenging Questions",
      unit: "Advanced Presentations",
      conversationGoal: "Latih percakapan Arab C1 untuk handling challenging questions dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Handling Challenging Questions di Indonesia.", caption: "Konteks percakapan nyata: Handling Challenging Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-advanced-presentation-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Advanced Presentation Mission",
      unit: "Advanced Presentations",
      conversationGoal: "Latih percakapan Arab C1 untuk delivering an advanced presentation dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Advanced Presentation Mission di Indonesia.", caption: "Konteks percakapan nyata: Advanced Presentation Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-identifying-assumptions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Identifying Assumptions",
      unit: "Debate & Analysis",
      conversationGoal: "Latih percakapan Arab C1 untuk identifying hidden assumptions dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Identifying Assumptions di Indonesia.", caption: "Konteks percakapan nyata: Identifying Assumptions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-challenging-an-argument",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Challenging an Argument",
      unit: "Debate & Analysis",
      conversationGoal: "Latih percakapan Arab C1 untuk challenging an argument politely dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Challenging an Argument di Indonesia.", caption: "Konteks percakapan nyata: Challenging an Argument." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-presenting-evidence",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Presenting Evidence",
      unit: "Debate & Analysis",
      conversationGoal: "Latih percakapan Arab C1 untuk presenting relevant evidence dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Presenting Evidence di Indonesia.", caption: "Konteks percakapan nyata: Presenting Evidence." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-responding-under-pressure",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Responding Under Pressure",
      unit: "Debate & Analysis",
      conversationGoal: "Latih percakapan Arab C1 untuk responding calmly under pressure dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding Under Pressure di Indonesia.", caption: "Konteks percakapan nyata: Responding Under Pressure." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-debate-analysis-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Debate Analysis Mission",
      unit: "Debate & Analysis",
      conversationGoal: "Latih percakapan Arab C1 untuk running a balanced analytical debate dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Debate Analysis Mission di Indonesia.", caption: "Konteks percakapan nyata: Debate Analysis Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-reading-context",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Reading Context",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Latih percakapan Arab C1 untuk reading social context dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Reading Context di Indonesia.", caption: "Konteks percakapan nyata: Reading Context." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-asking-tactful-questions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking Tactful Questions",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Latih percakapan Arab C1 untuk asking tactful questions dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Asking Tactful Questions di Indonesia.", caption: "Konteks percakapan nyata: Asking Tactful Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-explaining-local-norms",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Explaining Local Norms",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Latih percakapan Arab C1 untuk explaining local norms dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Explaining Local Norms di Indonesia.", caption: "Konteks percakapan nyata: Explaining Local Norms." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-repairing-misunderstanding",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Repairing Misunderstanding",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Latih percakapan Arab C1 untuk repairing misunderstanding dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Repairing Misunderstanding di Indonesia.", caption: "Konteks percakapan nyata: Repairing Misunderstanding." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-cross-cultural-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Cross-cultural Mission",
      unit: "Cross-cultural Professionalism",
      conversationGoal: "Latih percakapan Arab C1 untuk running a cross-cultural conversation dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Cross-cultural Mission di Indonesia.", caption: "Konteks percakapan nyata: Cross-cultural Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-setting-direction",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Setting Direction",
      unit: "Leadership & Coaching",
      conversationGoal: "Latih percakapan Arab C1 untuk setting direction clearly dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Setting Direction di Indonesia.", caption: "Konteks percakapan nyata: Setting Direction." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-coaching-with-questions",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Coaching With Questions",
      unit: "Leadership & Coaching",
      conversationGoal: "Latih percakapan Arab C1 untuk coaching with questions dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Coaching With Questions di Indonesia.", caption: "Konteks percakapan nyata: Coaching With Questions." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-giving-actionable-feedback",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Giving Actionable Feedback",
      unit: "Leadership & Coaching",
      conversationGoal: "Latih percakapan Arab C1 untuk giving actionable feedback dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Giving Actionable Feedback di Indonesia.", caption: "Konteks percakapan nyata: Giving Actionable Feedback." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-guiding-a-decision",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Guiding a Decision",
      unit: "Leadership & Coaching",
      conversationGoal: "Latih percakapan Arab C1 untuk guiding a group decision dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Guiding a Decision di Indonesia.", caption: "Konteks percakapan nyata: Guiding a Decision." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-leadership-coaching-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Leadership Coaching Mission",
      unit: "Leadership & Coaching",
      conversationGoal: "Latih percakapan Arab C1 untuk running a leadership coaching conversation dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Leadership Coaching Mission di Indonesia.", caption: "Konteks percakapan nyata: Leadership Coaching Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-catching-implied-meaning",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Catching Implied Meaning",
      unit: "Advanced Listening & Response",
      conversationGoal: "Latih percakapan Arab C1 untuk catching implied meaning dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Catching Implied Meaning di Indonesia.", caption: "Konteks percakapan nyata: Catching Implied Meaning." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-responding-to-long-turns",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Responding to Long Turns",
      unit: "Advanced Listening & Response",
      conversationGoal: "Latih percakapan Arab C1 untuk responding to long turns dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/service-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Responding to Long Turns di Indonesia.", caption: "Konteks percakapan nyata: Responding to Long Turns." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-summarizing-what-you-heard",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Summarizing What You Heard",
      unit: "Advanced Listening & Response",
      conversationGoal: "Latih percakapan Arab C1 untuk summarizing what you heard accurately dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/travel-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Summarizing What You Heard di Indonesia.", caption: "Konteks percakapan nyata: Summarizing What You Heard." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-asking-high-quality-follow-ups",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Asking High-quality Follow-ups",
      unit: "Advanced Listening & Response",
      conversationGoal: "Latih percakapan Arab C1 untuk asking high-quality follow-ups dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Asking High-quality Follow-ups di Indonesia.", caption: "Konteks percakapan nyata: Asking High-quality Follow-ups." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-advanced-listening-mission",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Advanced Listening Mission",
      unit: "Advanced Listening & Response",
      conversationGoal: "Latih percakapan Arab C1 untuk responding after advanced listening dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/health-male/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless laki-laki untuk konteks Advanced Listening Mission di Indonesia.", caption: "Konteks percakapan nyata: Advanced Listening Mission." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-review-nuance-and-strategy",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Nuance and Strategy",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab C1 untuk reviewing nuance and strategy dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Review Nuance and Strategy di Indonesia.", caption: "Konteks percakapan nyata: Review Nuance and Strategy." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-review-presenting-and-debate",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Presenting and Debate",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab C1 untuk reviewing presenting and debate dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Review Presenting and Debate di Indonesia.", caption: "Konteks percakapan nyata: Review Presenting and Debate." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-review-leadership-and-listening",
      language: "arabic",
      languageLabel: "Arabic",
      title: "Review Leadership and Listening",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab C1 untuk reviewing leadership and listening dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/workplace-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks Review Leadership and Listening di Indonesia.", caption: "Konteks percakapan nyata: Review Leadership and Listening." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-c1-final-test-practice",
      language: "arabic",
      languageLabel: "Arabic",
      title: "C1 Final Test Practice",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab C1 untuk practicing the final test dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks C1 Final Test Practice di Indonesia.", caption: "Konteks percakapan nyata: C1 Final Test Practice." }
      },
      sections: lessonSections
    },
    {
      slug: "arabic-c1-c1-final-conversation",
      language: "arabic",
      languageLabel: "Arabic",
      title: "C1 Final Conversation",
      unit: "C1 Review & Final Conversation",
      conversationGoal: "Latih percakapan Arab C1 untuk running a complete final conversation dengan nuance, struktur, presisi, dan respons profesional.",
      visuals: {
        hero: { src: "/images/lesson-visual-library/classroom-female/hero.png", width: 1672, height: 941, alt: "Ilustrasi cartoon faceless perempuan untuk konteks C1 Final Conversation di Indonesia.", caption: "Konteks percakapan nyata: C1 Final Conversation." }
      },
      sections: lessonSections
    }
  // </generated:lessons>
];

export const lessonsBySlug = Object.fromEntries(lessonCatalog.map((item) => [item.slug, item]));

export const coachTurnsByLessonSlug = {
  // <generated:coach_turns>
  "a1-final-conversation": [
    { coach: "Hi, good morning. What is your name?", hint: "Perkenalkan diri dengan kalimat lengkap.", sampleAnswer: "Good morning. My name is Faris.", focus: "Final opening", expectedKeywords: ["morning", "name", "faris"], indonesianExplanation: "" },
    { coach: "Nice to meet you. Where are you from?", hint: "Jawab asal dan tanyakan balik.", sampleAnswer: "I'm from Indonesia. How about you?", focus: "Origin and follow-up", expectedKeywords: ["i'm", "from", "indonesia", "how", "?"], indonesianExplanation: "" },
    { coach: "I'm from Malaysia. What do you do every morning?", hint: "Sebutkan rutinitas dan waktu.", sampleAnswer: "I study English at seven.", focus: "Routine", expectedKeywords: ["study", "english", "seven"], indonesianExplanation: "" },
    { coach: "Great. The cafe is open now.", hint: "Tanyakan lokasi cafe.", sampleAnswer: "Where is the cafe?", focus: "Place", expectedKeywords: ["where", "cafe", "?"], indonesianExplanation: "" },
    { coach: "Go straight and turn left.", hint: "Pesan satu item dengan sopan.", sampleAnswer: "Thank you. I would like one tea, please.", focus: "Order", expectedKeywords: ["one", "tea"], indonesianExplanation: "" },
    { coach: "Sure. It is two dollars.", hint: "Minta ulang harga jika perlu.", sampleAnswer: "Sorry, can you repeat that, please?", focus: "Clarification", expectedKeywords: ["sorry", "repeat", "?"], indonesianExplanation: "" },
    { coach: "Two dollars.", hint: "Bayar dan tutup dengan terima kasih.", sampleAnswer: "Here you go. Thank you for your help.", focus: "Final closing", expectedKeywords: ["help"], indonesianExplanation: "" },
  ],
  "a2-final-conversation": [
    { coach: "Hey! How have you been?", hint: "Jawab singkat, lalu bilang kabar kamu.", sampleAnswer: "Good. A bit tired, though.", focus: "Small talk", expectedKeywords: ["good", "tired"], indonesianExplanation: "" },
    { coach: "Would you recommend the cafe?", hint: "Jawab dengan yes + because + reason.", sampleAnswer: "Yes, because the coffee is good and it is quiet.", focus: "Recommend with reason", expectedKeywords: ["because", "coffee"], indonesianExplanation: "" },
    { coach: "Nice. Are you free on Saturday afternoon?", hint: "Jawab ya/tidak + usulkan waktu.", sampleAnswer: "Yes, I am. Let's meet at 3 p.m.", focus: "Confirm plan", expectedKeywords: ["yes", "meet"], indonesianExplanation: "" },
  ],
  "a2-final-test-practice": [
    { coach: "Hi. Ready?", hint: "Jawab siap.", sampleAnswer: "Yes, ready.", focus: "Start practice", expectedKeywords: ["yes"], indonesianExplanation: "" },
    { coach: "We haven't had coffee in a while.", hint: "Gunakan Do you want to...?", sampleAnswer: "Do you want to grab coffee this weekend?", focus: "Invitation", expectedKeywords: ["want to", "weekend"], indonesianExplanation: "" },
    { coach: "Maybe, but you don't look well today.", hint: "Gunakan I've had ... for ...", sampleAnswer: "I've had a cough for two days.", focus: "Symptom + duration", expectedKeywords: ["have had", "for"], indonesianExplanation: "" },
  ],
  "accepting-and-declining": [
    { coach: "Do you want to join our dinner tonight?", hint: "Tolak dengan sopan.", sampleAnswer: "Thanks, but I can't.", focus: "Decline politely", expectedKeywords: ["can't", "thanks"], indonesianExplanation: "" },
    { coach: "Oh, okay. Are you busy?", hint: "Beri alasan singkat dengan because.", sampleAnswer: "Yes. I'm busy tonight because I have a meeting.", focus: "Give a reason", expectedKeywords: ["i'm busy", "because"], indonesianExplanation: "" },
    { coach: "No problem. Maybe another time.", hint: "Usulkan waktu lain dengan singkat.", sampleAnswer: "Yes, maybe tomorrow.", focus: "Suggest another time", expectedKeywords: ["maybe", "tomorrow"], indonesianExplanation: "" },
  ],
  "advanced-listening-mission": [
    { coach: "Part of me wants to push ahead, but if this fails publicly, we'll lose confidence fast.", hint: "It sounds like... Just to check, are you implying...?", sampleAnswer: "It sounds like timing and risk are the main concerns. Just to check, are you implying we should slow down?", focus: "Implied meaning", expectedKeywords: ["sounds like", "just to check", "implying"], indonesianExplanation: "" },
    { coach: "Yes, that's close. Given that, how would you summarize it and label the decision?", hint: "Let me make sure I got this... The decision is...", sampleAnswer: "Let me make sure I got this: dependencies, time pressure, and visibility. The decision is to propose a phased rollout with clear metrics.", focus: "Summary + decision", expectedKeywords: ["make sure", "decision"], indonesianExplanation: "" },
    { coach: "When I say we should be more cautious, what do you think I mean, and what should we do next?", hint: "When you say... do you mean... or...? Next steps are...", sampleAnswer: "When you say 'more cautious', do you mean smaller scope or slower timing? Next steps are: I'll send the summary and draft phased options.", focus: "Follow-up + next steps", expectedKeywords: ["do you mean", "next steps"], indonesianExplanation: "" },
  ],
  "advanced-presentation-mission": [
    { coach: "Before we get into details, can you frame the proposal and define what you mean by modular architecture?", hint: "Today I'd like to... By X, I mean...", sampleAnswer: "Today I'd like to walk you through the proposal and why it matters. By 'modular architecture', I mean independent components.", focus: "Framing", expectedKeywords: ["today", "by", "i mean"], indonesianExplanation: "" },
    { coach: "Okay. What's your main claim, what evidence supports it, and what's the main trade-off?", hint: "The core claim is... The evidence suggests... That brings me to...", sampleAnswer: "The core claim is that this will improve delivery speed. The evidence suggests teams move faster with clear ownership. That brings me to the key trade-off: speed versus reliability.", focus: "Persuasion + transition", expectedKeywords: ["core claim", "evidence suggests", "trade-off"], indonesianExplanation: "" },
    { coach: "Fair question: isn't this going to create extra complexity? How would you answer that, and what are the next steps if we move ahead?", hint: "That's a fair question... The short answer is... In short... Next steps are...", sampleAnswer: "That's a fair question. The short answer is: it's manageable if we pilot first and monitor closely. In short, the benefits outweigh the risks if we set guardrails early. Next steps are: I'll share the plan today, and you'll review it by Friday.", focus: "Q&A + close", expectedKeywords: ["fair question", "short answer", "next steps", "by"], indonesianExplanation: "" },
  ],
  "agreeing-and-disagreeing-politely": [
    { coach: "I think this restaurant is the best.", hint: "Tolak halus + alasan singkat.", sampleAnswer: "I'm not sure. It's a bit expensive.", focus: "Soft disagreement with reason", expectedKeywords: ["not sure", "expensive"], indonesianExplanation: "" },
    { coach: "Really? What do you like about it?", hint: "Setuju 1 hal, tapi tambah tapi (but).", sampleAnswer: "I agree the food is good, but the service is slow.", focus: "Agree and contrast", expectedKeywords: ["agree", "but"], indonesianExplanation: "" },
    { coach: "Okay. Should we try another place next time?", hint: "Jawab setuju + That's fair.", sampleAnswer: "Yes, that's fair. Let's try another place.", focus: "Accept and plan", expectedKeywords: ["fair", "try"], indonesianExplanation: "" },
  ],
  "aligning-stakeholders": [
    { coach: "We have conflicting priorities across teams.", hint: "Mulai dengan alignment question.", sampleAnswer: "To make sure we're aligned, can you share your top priority?", focus: "Priorities", expectedKeywords: ["aligned", "priority"], indonesianExplanation: "" },
    { coach: "Our top priority is speed. What do you ask next?", hint: "Tanya constraint.", sampleAnswer: "Got it. From your perspective, what's the biggest constraint?", focus: "Constraints", expectedKeywords: ["perspective", "constraint"], indonesianExplanation: "" },
    { coach: "We can't add headcount. Close with a decision.", hint: "Can we agree that ...", sampleAnswer: "Understood. The key constraint is capacity. Can we agree that we ship a smaller scope first?", focus: "Decision", expectedKeywords: ["key constraint", "agree", "scope"], indonesianExplanation: "" },
  ],
  "answering-questions": [
    { coach: "How much effort will this take?", hint: "That's a good question. As far as I know...", sampleAnswer: "That's a good question. As far as I know, the first version takes about one day.", focus: "Answer with confidence level", expectedKeywords: ["good question", "as far as I know"], indonesianExplanation: "" },
    { coach: "What about maintenance?", hint: "I'm not sure yet, but I can follow up...", sampleAnswer: "I'm not sure yet, but I can follow up with an estimate by tomorrow.", focus: "Uncertainty + follow up", expectedKeywords: ["not sure", "follow up"], indonesianExplanation: "" },
    { coach: "Who will own it?", hint: "I suggest we assign...", sampleAnswer: "I suggest we assign one owner per quarter to keep it updated.", focus: "Ownership answer", expectedKeywords: ["suggest", "assign", "owner"], indonesianExplanation: "" },
  ],
  "apologizing-and-thanking": [
    { coach: "Hello, Ben. You are late today.", hint: "Minta maaf karena terlambat.", sampleAnswer: "Sorry I'm late.", focus: "Apology", expectedKeywords: ["sorry", "i'm", "late"], indonesianExplanation: "" },
    { coach: "That's okay. What happened?", hint: "Berikan alasan singkat.", sampleAnswer: "My internet was slow.", focus: "Reason", expectedKeywords: ["internet", "was", "slow"], indonesianExplanation: "" },
    { coach: "No problem. Please join the class.", hint: "Ucapkan terima kasih sudah menunggu.", sampleAnswer: "Thank you for waiting.", focus: "Thanking", expectedKeywords: ["waiting"], indonesianExplanation: "" },
    { coach: "You're welcome.", hint: "Katakan kamu siap sekarang.", sampleAnswer: "I am ready now.", focus: "Ready", expectedKeywords: ["ready"], indonesianExplanation: "" },
  ],
  "arabic-a1-final-conversation": [
    { coach: "مَرْحَبًا، مَا اسْمُكَ؟", hint: "Jawab dengan pola: مَرْحَبًا", sampleAnswer: "مَرْحَبًا", focus: "Latihan frasa: Halo.", expectedKeywords: ["مَرْحَبًا"], indonesianExplanation: "Halo." },
    { coach: "استخدم: اِسْمِي ...", hint: "Jawab dengan pola: اِسْمِي ...", sampleAnswer: "اِسْمِي ...", focus: "Latihan frasa: Nama saya ...", expectedKeywords: ["اِسْمِي"], indonesianExplanation: "Nama saya ..." },
    { coach: "استخدم: أَدْرُسُ الْعَرَبِيَّةَ", hint: "Jawab dengan pola: أَدْرُسُ الْعَرَبِيَّةَ", sampleAnswer: "أَدْرُسُ الْعَرَبِيَّةَ", focus: "Latihan frasa: Saya belajar bahasa Arab.", expectedKeywords: ["أَدْرُسُ", "الْعَرَبِيَّةَ"], indonesianExplanation: "Saya belajar bahasa Arab." },
  ],
  "arabic-a1-final-test-practice": [
    { coach: "مِنْ أَيْنَ أَنْتِ؟", hint: "Jawab dengan pola: أَنَا مِنْ إِنْدُونِيسِيَا", sampleAnswer: "أَنَا مِنْ إِنْدُونِيسِيَا", focus: "Latihan frasa: Saya dari Indonesia.", expectedKeywords: ["أَنَا", "من", "إِنْدُونِيسِيَا"], indonesianExplanation: "Saya dari Indonesia." },
    { coach: "استخدم: عِنْدِي دَرْسٌ", hint: "Jawab dengan pola: عِنْدِي دَرْسٌ", sampleAnswer: "عِنْدِي دَرْسٌ", focus: "Latihan frasa: Saya punya pelajaran.", expectedKeywords: ["عِنْدِي", "دَرْسٌ"], indonesianExplanation: "Saya punya pelajaran." },
    { coach: "استخدم: أُرِيدُ كِتَابًا", hint: "Jawab dengan pola: أُرِيدُ كِتَابًا", sampleAnswer: "أُرِيدُ كِتَابًا", focus: "Latihan frasa: Saya ingin buku.", expectedKeywords: ["أُرِيدُ", "كِتَابًا"], indonesianExplanation: "Saya ingin buku." },
  ],
  "arabic-a2-final-conversation": [
    { coach: "كَيْفَ كَانَتْ تَجْرِبَتُكَ فِي الْمَدِينَةِ يَا خَالِدُ؟", hint: "Jawab dengan pola: كَيْفَ كَانَتْ تَجْرِبَتُكَ؟", sampleAnswer: "كَيْفَ كَانَتْ تَجْرِبَتُكَ؟", focus: "Latihan frasa: Bagaimana pengalamanmu?", expectedKeywords: ["كَيْفَ", "كَانَتْ", "تَجْرِبَتُكَ"], indonesianExplanation: "Bagaimana pengalamanmu?" },
    { coach: "استخدم: هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي؟", hint: "Jawab dengan pola: هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي؟", sampleAnswer: "هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي؟", focus: "Latihan frasa: Apakah kamu ingin pergi bersama saya?", expectedKeywords: ["هَلْ", "تُرِيدُ", "أَنْ"], indonesianExplanation: "Apakah kamu ingin pergi bersama saya?" },
    { coach: "استخدم: كَيْفَ أَذْهَبُ إِلَى الْمَرْكَزِ؟", hint: "Jawab dengan pola: كَيْفَ أَذْهَبُ إِلَى الْمَرْكَزِ؟", sampleAnswer: "كَيْفَ أَذْهَبُ إِلَى الْمَرْكَزِ؟", focus: "Latihan frasa: Bagaimana saya pergi ke pusat?", expectedKeywords: ["كَيْفَ", "أَذْهَبُ", "إِلَى"], indonesianExplanation: "Bagaimana saya pergi ke pusat?" },
  ],
  "arabic-a2-final-test-practice": [
    { coach: "مَاذَا فَعَلْتَ أَمْسِ يَا رَامِي؟", hint: "Jawab dengan pola: أَسْتَطِيعُ أَنْ أَتَحَدَّثَ عَنْ يَوْمِي.", sampleAnswer: "أَسْتَطِيعُ أَنْ أَتَحَدَّثَ عَنْ يَوْمِي.", focus: "Latihan frasa: Saya bisa berbicara tentang hari saya.", expectedKeywords: ["أَسْتَطِيعُ", "أَنْ", "أَتَحَدَّثَ"], indonesianExplanation: "Saya bisa berbicara tentang hari saya." },
    { coach: "استخدم: ذَهَبْتُ إِلَى مَكَانٍ جَدِيدٍ.", hint: "Jawab dengan pola: ذَهَبْتُ إِلَى مَكَانٍ جَدِيدٍ.", sampleAnswer: "ذَهَبْتُ إِلَى مَكَانٍ جَدِيدٍ.", focus: "Latihan frasa: Saya pergi ke tempat baru.", expectedKeywords: ["ذَهَبْتُ", "إِلَى", "مَكَانٍ"], indonesianExplanation: "Saya pergi ke tempat baru." },
    { coach: "استخدم: أُفَضِّلُ الصَّبَاحَ لِأَنَّهُ أَهْدَأُ.", hint: "Jawab dengan pola: أُفَضِّلُ الصَّبَاحَ لِأَنَّهُ أَهْدَأُ.", sampleAnswer: "أُفَضِّلُ الصَّبَاحَ لِأَنَّهُ أَهْدَأُ.", focus: "Latihan frasa: Saya lebih memilih pagi karena lebih tenang.", expectedKeywords: ["أُفَضِّلُ", "الصَّبَاحَ", "لِأَنَّهُ"], indonesianExplanation: "Saya lebih memilih pagi karena lebih tenang." },
  ],
  "arabic-accepting-and-declining": [
    { coach: "هَلْ تَأْتِي إِلَى الْمَكْتَبَةِ مَعِي؟", hint: "Jawab dengan pola: نَعَمْ، أَسْتَطِيعُ.", sampleAnswer: "نَعَمْ، أَسْتَطِيعُ.", focus: "Latihan frasa: Ya, saya bisa.", expectedKeywords: ["نَعَمْ،", "أَسْتَطِيعُ"], indonesianExplanation: "Ya, saya bisa." },
    { coach: "استخدم: آسِفٌ، لَا أَسْتَطِيعُ.", hint: "Jawab dengan pola: آسِفٌ، لَا أَسْتَطِيعُ.", sampleAnswer: "آسِفٌ، لَا أَسْتَطِيعُ.", focus: "Latihan frasa: Maaf, saya tidak bisa.", expectedKeywords: ["آسِفٌ،", "لَا", "أَسْتَطِيعُ"], indonesianExplanation: "Maaf, saya tidak bisa." },
    { coach: "استخدم: لِأَنَّ لَدَيَّ مَوْعِدًا.", hint: "Jawab dengan pola: لِأَنَّ لَدَيَّ مَوْعِدًا.", sampleAnswer: "لِأَنَّ لَدَيَّ مَوْعِدًا.", focus: "Latihan frasa: Karena saya punya janji.", expectedKeywords: ["لِأَنَّ", "لَدَيَّ", "مَوْعِدًا"], indonesianExplanation: "Karena saya punya janji." },
  ],
  "arabic-agreeing-and-disagreeing-politely": [
    { coach: "أَعْتَقِدُ أَنَّ الدِّرَاسَةَ فِي الْبَيْتِ أَفْضَلُ.", hint: "Jawab dengan pola: أُوَافِقُكَ.", sampleAnswer: "أُوَافِقُكَ.", focus: "Latihan frasa: Saya setuju denganmu.", expectedKeywords: ["أُوَافِقُكَ"], indonesianExplanation: "Saya setuju denganmu." },
    { coach: "استخدم: أُوَافِقُكَ فِي هَذَا.", hint: "Jawab dengan pola: أُوَافِقُكَ فِي هَذَا.", sampleAnswer: "أُوَافِقُكَ فِي هَذَا.", focus: "Latihan frasa: Saya setuju denganmu dalam hal ini.", expectedKeywords: ["أُوَافِقُكَ", "فِي", "هَذَا"], indonesianExplanation: "Saya setuju denganmu dalam hal ini." },
    { coach: "استخدم: لَا أُوَافِقُ تَمَامًا.", hint: "Jawab dengan pola: لَا أُوَافِقُ تَمَامًا.", sampleAnswer: "لَا أُوَافِقُ تَمَامًا.", focus: "Latihan frasa: Saya tidak sepenuhnya setuju.", expectedKeywords: ["لَا", "أُوَافِقُ", "تَمَامًا"], indonesianExplanation: "Saya tidak sepenuhnya setuju." },
  ],
  "arabic-apologizing-and-thanking": [
    { coach: "عُذْرًا، لَا أَفْهَمُ.", hint: "Jawab dengan pola: آسِفٌ", sampleAnswer: "آسِفٌ", focus: "Latihan frasa: Maaf.", expectedKeywords: ["آسِفٌ"], indonesianExplanation: "Maaf." },
    { coach: "استخدم: آسِفَةٌ", hint: "Jawab dengan pola: آسِفَةٌ", sampleAnswer: "آسِفَةٌ", focus: "Latihan frasa: Maaf.", expectedKeywords: ["آسِفَةٌ"], indonesianExplanation: "Maaf." },
    { coach: "استخدم: عُذْرًا", hint: "Jawab dengan pola: عُذْرًا", sampleAnswer: "عُذْرًا", focus: "Latihan frasa: Permisi/maaf.", expectedKeywords: ["عُذْرًا"], indonesianExplanation: "Permisi/maaf." },
  ],
  "arabic-asking-about-departure-time": [
    { coach: "مَتَى يَغَادِرُ الْقِطَارُ إِلَى بَانْدُونْغ؟", hint: "Jawab dengan pola: مَتَى يَغَادِرُ الْقِطَارُ؟", sampleAnswer: "مَتَى يَغَادِرُ الْقِطَارُ؟", focus: "Latihan frasa: Kapan keretanya berangkat?", expectedKeywords: ["مَتَى", "يَغَادِرُ", "الْقِطَارُ"], indonesianExplanation: "Kapan keretanya berangkat?" },
    { coach: "استخدم: يُغَادِرُ السَّاعَةَ السَّابِعَةَ.", hint: "Jawab dengan pola: يُغَادِرُ السَّاعَةَ السَّابِعَةَ.", sampleAnswer: "يُغَادِرُ السَّاعَةَ السَّابِعَةَ.", focus: "Latihan frasa: Berangkat jam tujuh.", expectedKeywords: ["يُغَادِرُ", "السَّاعَةَ", "السَّابِعَةَ"], indonesianExplanation: "Berangkat jam tujuh." },
    { coach: "استخدم: مِنْ أَيِّ رَصِيفٍ؟", hint: "Jawab dengan pola: مِنْ أَيِّ رَصِيفٍ؟", sampleAnswer: "مِنْ أَيِّ رَصِيفٍ؟", focus: "Latihan frasa: Dari peron berapa?", expectedKeywords: ["مِنْ", "أَيِّ", "رَصِيفٍ"], indonesianExplanation: "Dari peron berapa?" },
  ],
  "arabic-asking-about-past-activities": [
    { coach: "مَاذَا فَعَلْتَ بَعْدَ الدَّرْسِ يَا كَرِيمُ؟", hint: "Jawab dengan pola: مَاذَا فَعَلْتَ بَعْدَ الدَّرْسِ؟", sampleAnswer: "مَاذَا فَعَلْتَ بَعْدَ الدَّرْسِ؟", focus: "Latihan frasa: Apa yang kamu lakukan setelah pelajaran?", expectedKeywords: ["مَاذَا", "فَعَلْتَ", "بَعْدَ"], indonesianExplanation: "Apa yang kamu lakukan setelah pelajaran?" },
    { coach: "استخدم: مَعَ مَنْ ذَهَبْتَ؟", hint: "Jawab dengan pola: مَعَ مَنْ ذَهَبْتَ؟", sampleAnswer: "مَعَ مَنْ ذَهَبْتَ؟", focus: "Latihan frasa: Dengan siapa kamu pergi?", expectedKeywords: ["مَعَ", "مَنْ", "ذَهَبْتَ"], indonesianExplanation: "Dengan siapa kamu pergi?" },
    { coach: "استخدم: كَيْفَ كَانَ الْمَكَانُ؟", hint: "Jawab dengan pola: كَيْفَ كَانَ الْمَكَانُ؟", sampleAnswer: "كَيْفَ كَانَ الْمَكَانُ؟", focus: "Latihan frasa: Bagaimana tempatnya?", expectedKeywords: ["كَيْفَ", "كَانَ", "الْمَكَانُ"], indonesianExplanation: "Bagaimana tempatnya?" },
  ],
  "arabic-asking-about-prices": [
    { coach: "كَمْ سِعْرُ الْقَلَمِ؟", hint: "Jawab dengan pola: كَمِ السِّعْرُ؟", sampleAnswer: "كَمِ السِّعْرُ؟", focus: "Latihan frasa: Berapa harganya?", expectedKeywords: ["كَمِ", "السِّعْرُ"], indonesianExplanation: "Berapa harganya?" },
    { coach: "استخدم: السِّعْرُ خَمْسَةُ رِيَالَاتٍ", hint: "Jawab dengan pola: السِّعْرُ خَمْسَةُ رِيَالَاتٍ", sampleAnswer: "السِّعْرُ خَمْسَةُ رِيَالَاتٍ", focus: "Latihan frasa: Harganya lima riyal.", expectedKeywords: ["السِّعْرُ", "خَمْسَةُ", "رِيَالَاتٍ"], indonesianExplanation: "Harganya lima riyal." },
    { coach: "استخدم: غَالٍ", hint: "Jawab dengan pola: غَالٍ", sampleAnswer: "غَالٍ", focus: "Latihan frasa: Mahal", expectedKeywords: ["غَالٍ"], indonesianExplanation: "Mahal" },
  ],
  "arabic-asking-about-size-and-color": [
    { coach: "أُرِيدُ قَمِيصًا أَبْيَضَ، مِنْ فَضْلِكِ.", hint: "Jawab dengan pola: هَلْ عِنْدَكُمْ مَقَاسٌ أَكْبَرُ؟", sampleAnswer: "هَلْ عِنْدَكُمْ مَقَاسٌ أَكْبَرُ؟", focus: "Latihan frasa: Apakah kalian punya ukuran yang lebih besar?", expectedKeywords: ["هَلْ", "عِنْدَكُمْ", "مَقَاسٌ"], indonesianExplanation: "Apakah kalian punya ukuran yang lebih besar?" },
    { coach: "استخدم: أُرِيدُ اللَّوْنَ الْأَبْيَضَ.", hint: "Jawab dengan pola: أُرِيدُ اللَّوْنَ الْأَبْيَضَ.", sampleAnswer: "أُرِيدُ اللَّوْنَ الْأَبْيَضَ.", focus: "Latihan frasa: Saya ingin warna putih.", expectedKeywords: ["أُرِيدُ", "اللَّوْنَ", "الْأَبْيَضَ"], indonesianExplanation: "Saya ingin warna putih." },
    { coach: "استخدم: هَذَا صَغِيرٌ جِدًّا.", hint: "Jawab dengan pola: هَذَا صَغِيرٌ جِدًّا.", sampleAnswer: "هَذَا صَغِيرٌ جِدًّا.", focus: "Latihan frasa: Ini terlalu kecil.", expectedKeywords: ["هَذَا", "صَغِيرٌ", "جِدًّا"], indonesianExplanation: "Ini terlalu kecil." },
  ],
  "arabic-asking-about-work-or-study": [
    { coach: "أَيْنَ تَدْرُسُ؟", hint: "Jawab dengan pola: أَيْنَ تَدْرُسُ؟", sampleAnswer: "أَيْنَ تَدْرُسُ؟", focus: "Latihan frasa: Di mana kamu belajar?", expectedKeywords: ["أَيْنَ", "تَدْرُسُ"], indonesianExplanation: "Di mana kamu belajar?" },
    { coach: "استخدم: مَاذَا تَدْرُسُ؟", hint: "Jawab dengan pola: مَاذَا تَدْرُسُ؟", sampleAnswer: "مَاذَا تَدْرُسُ؟", focus: "Latihan frasa: Apa yang kamu pelajari?", expectedKeywords: ["مَاذَا", "تَدْرُسُ"], indonesianExplanation: "Apa yang kamu pelajari?" },
    { coach: "استخدم: أَدْرُسُ اللُّغَةَ الْعَرَبِيَّةَ", hint: "Jawab dengan pola: أَدْرُسُ اللُّغَةَ الْعَرَبِيَّةَ", sampleAnswer: "أَدْرُسُ اللُّغَةَ الْعَرَبِيَّةَ", focus: "Latihan frasa: Saya belajar bahasa Arab.", expectedKeywords: ["أَدْرُسُ", "اللُّغَةَ", "الْعَرَبِيَّةَ"], indonesianExplanation: "Saya belajar bahasa Arab." },
  ],
  "arabic-asking-follow-up-questions": [
    { coach: "مَاذَا تَفْعَلُ بَعْدَ الدَّرْسِ؟", hint: "Jawab dengan pola: مَاذَا تَفْعَلُ بَعْدَ الدَّرْسِ؟", sampleAnswer: "مَاذَا تَفْعَلُ بَعْدَ الدَّرْسِ؟", focus: "Latihan frasa: Apa yang kamu lakukan setelah pelajaran?", expectedKeywords: ["مَاذَا", "تَفْعَلُ", "بَعْدَ"], indonesianExplanation: "Apa yang kamu lakukan setelah pelajaran?" },
    { coach: "استخدم: لِمَاذَا؟", hint: "Jawab dengan pola: لِمَاذَا؟", sampleAnswer: "لِمَاذَا؟", focus: "Latihan frasa: Mengapa?", expectedKeywords: ["لِمَاذَا"], indonesianExplanation: "Mengapa?" },
    { coach: "استخدم: لِأَنَّنِي أُرِيدُ أَنْ أَتَدَرَّبَ.", hint: "Jawab dengan pola: لِأَنَّنِي أُرِيدُ أَنْ أَتَدَرَّبَ.", sampleAnswer: "لِأَنَّنِي أُرِيدُ أَنْ أَتَدَرَّبَ.", focus: "Latihan frasa: Karena saya ingin berlatih.", expectedKeywords: ["لِأَنَّنِي", "أُرِيدُ", "أَنْ"], indonesianExplanation: "Karena saya ingin berlatih." },
  ],
  "arabic-asking-for-an-item": [
    { coach: "مَرْحَبًا، أَبْحَثُ عَنْ قَلَمٍ أَزْرَقَ.", hint: "Jawab dengan pola: أَبْحَثُ عَنْ قَلَمٍ أَزْرَقَ.", sampleAnswer: "أَبْحَثُ عَنْ قَلَمٍ أَزْرَقَ.", focus: "Latihan frasa: Saya mencari pulpen biru.", expectedKeywords: ["أَبْحَثُ", "عَنْ", "قَلَمٍ"], indonesianExplanation: "Saya mencari pulpen biru." },
    { coach: "استخدم: هَلْ عِنْدَكُمْ هَذَا؟", hint: "Jawab dengan pola: هَلْ عِنْدَكُمْ هَذَا؟", sampleAnswer: "هَلْ عِنْدَكُمْ هَذَا؟", focus: "Latihan frasa: Apakah kalian punya ini?", expectedKeywords: ["هَلْ", "عِنْدَكُمْ", "هَذَا"], indonesianExplanation: "Apakah kalian punya ini?" },
    { coach: "استخدم: هَلْ يُوجَدُ لَوْنٌ آخَرُ؟", hint: "Jawab dengan pola: هَلْ يُوجَدُ لَوْنٌ آخَرُ؟", sampleAnswer: "هَلْ يُوجَدُ لَوْنٌ آخَرُ؟", focus: "Latihan frasa: Apakah ada warna lain?", expectedKeywords: ["هَلْ", "يُوجَدُ", "لَوْنٌ"], indonesianExplanation: "Apakah ada warna lain?" },
  ],
  "arabic-asking-for-help": [
    { coach: "هَلْ تُسَاعِدُنِي؟", hint: "Jawab dengan pola: هَلْ تُسَاعِدُنِي؟", sampleAnswer: "هَلْ تُسَاعِدُنِي؟", focus: "Latihan frasa: Bisakah Anda membantu saya?", expectedKeywords: ["هَلْ", "تُسَاعِدُنِي"], indonesianExplanation: "Bisakah Anda membantu saya?" },
    { coach: "استخدم: أَحْتَاجُ مُسَاعَدَةً", hint: "Jawab dengan pola: أَحْتَاجُ مُسَاعَدَةً", sampleAnswer: "أَحْتَاجُ مُسَاعَدَةً", focus: "Latihan frasa: Saya butuh bantuan.", expectedKeywords: ["أَحْتَاجُ", "مُسَاعَدَةً"], indonesianExplanation: "Saya butuh bantuan." },
    { coach: "استخدم: أَيْنَ أَجِدُ الدَّرْسَ؟", hint: "Jawab dengan pola: أَيْنَ أَجِدُ الدَّرْسَ؟", sampleAnswer: "أَيْنَ أَجِدُ الدَّرْسَ؟", focus: "Latihan frasa: Di mana saya menemukan pelajaran?", expectedKeywords: ["أَيْنَ", "أَجِدُ", "الدَّرْسَ"], indonesianExplanation: "Di mana saya menemukan pelajaran?" },
  ],
  "arabic-asking-for-opinions": [
    { coach: "مَا رَأْيُكَ فِي هَذَا الْجَدْوَلِ يَا دِيمَاسُ؟", hint: "Jawab dengan pola: مَا رَأْيُكَ فِي هَذَا؟", sampleAnswer: "مَا رَأْيُكَ فِي هَذَا؟", focus: "Latihan frasa: Apa pendapatmu tentang ini?", expectedKeywords: ["مَا", "رَأْيُكَ", "فِي"], indonesianExplanation: "Apa pendapatmu tentang ini?" },
    { coach: "استخدم: مَا رَأْيُكَ فِي الْخِيَارِ الثَّانِي؟", hint: "Jawab dengan pola: مَا رَأْيُكَ فِي الْخِيَارِ الثَّانِي؟", sampleAnswer: "مَا رَأْيُكَ فِي الْخِيَارِ الثَّانِي؟", focus: "Latihan frasa: Apa pendapatmu tentang pilihan kedua?", expectedKeywords: ["مَا", "رَأْيُكَ", "فِي"], indonesianExplanation: "Apa pendapatmu tentang pilihan kedua?" },
    { coach: "استخدم: أَيُّهُمَا أَفْضَلُ؟", hint: "Jawab dengan pola: أَيُّهُمَا أَفْضَلُ؟", sampleAnswer: "أَيُّهُمَا أَفْضَلُ؟", focus: "Latihan frasa: Mana dari keduanya yang lebih baik?", expectedKeywords: ["أَيُّهُمَا", "أَفْضَلُ"], indonesianExplanation: "Mana dari keduanya yang lebih baik?" },
  ],
  "arabic-asking-how-to-get-there": [
    { coach: "كَيْفَ أَذْهَبُ إِلَى الْمَقْهَى؟", hint: "Jawab dengan pola: كَيْفَ أَذْهَبُ إِلَى الْمَكْتَبَةِ؟", sampleAnswer: "كَيْفَ أَذْهَبُ إِلَى الْمَكْتَبَةِ؟", focus: "Latihan frasa: Bagaimana saya pergi ke perpustakaan?", expectedKeywords: ["كَيْفَ", "أَذْهَبُ", "إِلَى"], indonesianExplanation: "Bagaimana saya pergi ke perpustakaan?" },
    { coach: "استخدم: امشِ إِلَى الْأَمَامِ", hint: "Jawab dengan pola: امشِ إِلَى الْأَمَامِ", sampleAnswer: "امشِ إِلَى الْأَمَامِ", focus: "Latihan frasa: Berjalanlah ke depan.", expectedKeywords: ["امشِ", "إِلَى", "الْأَمَامِ"], indonesianExplanation: "Berjalanlah ke depan." },
    { coach: "استخدم: ثُمَّ", hint: "Jawab dengan pola: ثُمَّ", sampleAnswer: "ثُمَّ", focus: "Latihan frasa: Lalu", expectedKeywords: ["ثُمَّ"], indonesianExplanation: "Lalu" },
  ],
  "arabic-asking-the-time": [
    { coach: "كَمِ السَّاعَةُ الْآنَ؟", hint: "Jawab dengan pola: كَمِ السَّاعَةُ؟", sampleAnswer: "كَمِ السَّاعَةُ؟", focus: "Latihan frasa: Jam berapa?", expectedKeywords: ["كَمِ", "السَّاعَةُ"], indonesianExplanation: "Jam berapa?" },
    { coach: "استخدم: السَّاعَةُ الثَّامِنَةُ", hint: "Jawab dengan pola: السَّاعَةُ الثَّامِنَةُ", sampleAnswer: "السَّاعَةُ الثَّامِنَةُ", focus: "Latihan frasa: Jam delapan.", expectedKeywords: ["السَّاعَةُ", "الثَّامِنَةُ"], indonesianExplanation: "Jam delapan." },
    { coach: "استخدم: الْآنَ", hint: "Jawab dengan pola: الْآنَ", sampleAnswer: "الْآنَ", focus: "Latihan frasa: Sekarang", expectedKeywords: ["الْآنَ"], indonesianExplanation: "Sekarang" },
  ],
  "arabic-asking-to-repeat-a-letter": [
    { coach: "لم أَسْمَعُ الْحَرْفَ.", hint: "Jawab dengan pola: لم أَسْمَعُ الْحَرْفَ", sampleAnswer: "لم أَسْمَعُ الْحَرْفَ", focus: "Latihan frasa: Saya tidak mendengar hurufnya.", expectedKeywords: ["لم", "أَسْمَعُ", "الْحَرْفَ"], indonesianExplanation: "Saya tidak mendengar hurufnya." },
    { coach: "استخدم: بِبُطْءٍ مِنْ فَضْلِكَ", hint: "Jawab dengan pola: بِبُطْءٍ مِنْ فَضْلِكَ", sampleAnswer: "بِبُطْءٍ مِنْ فَضْلِكَ", focus: "Latihan frasa: Pelan-pelan, tolong.", expectedKeywords: ["بِبُطْءٍ", "مِنْ", "فَضْلِكَ"], indonesianExplanation: "Pelan-pelan, tolong." },
    { coach: "استخدم: هَلْ قُلْتَ بَاءً؟", hint: "Jawab dengan pola: هَلْ قُلْتَ بَاءً؟", sampleAnswer: "هَلْ قُلْتَ بَاءً؟", focus: "Latihan frasa: Apakah Anda mengatakan ba?", expectedKeywords: ["هَلْ", "قُلْتَ", "بَاءً"], indonesianExplanation: "Apakah Anda mengatakan ba?" },
  ],
  "arabic-asking-when": [
    { coach: "مَتَى الدَّرْسُ؟", hint: "Jawab dengan pola: مَتَى الدَّرْسُ؟", sampleAnswer: "مَتَى الدَّرْسُ؟", focus: "Latihan frasa: Kapan pelajarannya?", expectedKeywords: ["مَتَى", "الدَّرْسُ"], indonesianExplanation: "Kapan pelajarannya?" },
    { coach: "استخدم: فِي الصَّبَاحِ", hint: "Jawab dengan pola: فِي الصَّبَاحِ", sampleAnswer: "فِي الصَّبَاحِ", focus: "Latihan frasa: Pada pagi hari", expectedKeywords: ["فِي", "الصَّبَاحِ"], indonesianExplanation: "Pada pagi hari" },
    { coach: "استخدم: بَعْدَ الظُّهْرِ", hint: "Jawab dengan pola: بَعْدَ الظُّهْرِ", sampleAnswer: "بَعْدَ الظُّهْرِ", focus: "Latihan frasa: Setelah tengah hari", expectedKeywords: ["بَعْدَ", "الظُّهْرِ"], indonesianExplanation: "Setelah tengah hari" },
  ],
  "arabic-asking-when-you-do-not-understand": [
    { coach: "اِقرأِ الجملةَ.", hint: "Katakan bahwa kamu belum paham.", sampleAnswer: "عفوًا، لا أفهم.", focus: "Mengatakan belum paham", expectedKeywords: ["لا", "أفهم"], indonesianExplanation: "لا أفهم berarti saya tidak paham." },
    { coach: "هل تريد الإعادة؟", hint: "Minta pengulangan dengan sopan.", sampleAnswer: "نعم، أَعِدْ مِنْ فَضْلِكَ.", focus: "Meminta pengulangan", expectedKeywords: ["أَعِدْ", "فَضْلِكَ"], indonesianExplanation: "أَعِدْ مِنْ فَضْلِكَ berarti ulangi, tolong." },
    { coach: "الكلمة هي جديدة.", hint: "Tanyakan makna الكلمة.", sampleAnswer: "ما معنى الكلمة؟", focus: "Bertanya makna", expectedKeywords: ["ما", "معنى", "الكلمة"], indonesianExplanation: "Gunakan ما معنى untuk bertanya makna kata." },
  ],
  "arabic-asking-where-a-place-is": [
    { coach: "أَيْنَ الْمَكْتَبَةُ؟", hint: "Jawab dengan pola: أَيْنَ الْمَكْتَبَةُ؟", sampleAnswer: "أَيْنَ الْمَكْتَبَةُ؟", focus: "Latihan frasa: Di mana perpustakaan?", expectedKeywords: ["أَيْنَ", "الْمَكْتَبَةُ"], indonesianExplanation: "Di mana perpustakaan?" },
    { coach: "استخدم: الْمَكْتَبَةُ هُنَا", hint: "Jawab dengan pola: الْمَكْتَبَةُ هُنَا", sampleAnswer: "الْمَكْتَبَةُ هُنَا", focus: "Latihan frasa: Perpustakaan di sini.", expectedKeywords: ["الْمَكْتَبَةُ", "هُنَا"], indonesianExplanation: "Perpustakaan di sini." },
    { coach: "استخدم: هُنَاكَ", hint: "Jawab dengan pola: هُنَاكَ", sampleAnswer: "هُنَاكَ", focus: "Latihan frasa: Di sana", expectedKeywords: ["هُنَاكَ"], indonesianExplanation: "Di sana" },
  ],
  "arabic-b1-asking-about-culture": [
    { coach: "مَا السُّؤَالُ الَّذِي يُسَاعِدُكَ عَلَى فَهْمِ الْمَوْقِفِ؟", hint: "Jawab dengan kalimat terhubung memakai: هَلْ يُمْكِنُ أَنْ أَسْأَلَ عَنْ هَذِهِ الْعَادَةِ؟", sampleAnswer: "هَلْ يُمْكِنُ أَنْ أَسْأَلَ عَنْ هَذِهِ الْعَادَةِ؟", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَلْ", "يُمْكِنُ", "أَنْ", "أَسْأَلَ"], indonesianExplanation: "Bolehkah saya bertanya tentang kebiasaan ini?" },
    { coach: "استخدم الفكرة: أُرِيدُ أَنْ أَفْهَمَ السِّبَاقَ الثَّقَافِيَّ.", hint: "Jawab dengan kalimat terhubung memakai: أُرِيدُ أَنْ أَفْهَمَ السِّبَاقَ الثَّقَافِيَّ.", sampleAnswer: "أُرِيدُ أَنْ أَفْهَمَ السِّبَاقَ الثَّقَافِيَّ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أَفْهَمَ", "السِّبَاقَ"], indonesianExplanation: "Saya ingin memahami konteks budaya." },
    { coach: "استخدم الفكرة: هَلْ هَذَا أَمْرٌ رَسْمِيٌّ أَمْ عَادِيٌّ؟", hint: "Jawab dengan kalimat terhubung memakai: هَلْ هَذَا أَمْرٌ رَسْمِيٌّ أَمْ عَادِيٌّ؟", sampleAnswer: "هَلْ هَذَا أَمْرٌ رَسْمِيٌّ أَمْ عَادِيٌّ؟", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَلْ", "هَذَا", "أَمْرٌ", "رَسْمِيٌّ"], indonesianExplanation: "Apakah ini hal resmi atau biasa?" },
  ],
  "arabic-b1-asking-about-pros-and-cons": [
    { coach: "مَا السُّؤَالُ الَّذِي يُسَاعِدُكَ عَلَى فَهْمِ الْمَوْقِفِ؟", hint: "Jawab dengan kalimat terhubung memakai: مَا إِيجَابِيَّاتُ هَذَا الْخِيَارِ؟", sampleAnswer: "مَا إِيجَابِيَّاتُ هَذَا الْخِيَارِ؟", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["مَا", "إِيجَابِيَّاتُ", "هَذَا", "الْخِيَارِ"], indonesianExplanation: "Apa kelebihan pilihan ini?" },
    { coach: "استخدم الفكرة: وَمَا السَّلْبِيَّاتُ الْمُمْكِنَةُ؟", hint: "Jawab dengan kalimat terhubung memakai: وَمَا السَّلْبِيَّاتُ الْمُمْكِنَةُ؟", sampleAnswer: "وَمَا السَّلْبِيَّاتُ الْمُمْكِنَةُ؟", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["وَمَا", "السَّلْبِيَّاتُ", "الْمُمْكِنَةُ"], indonesianExplanation: "Dan apa kemungkinan kekurangannya?" },
    { coach: "استخدم الفكرة: هَلِ الْمَزَايَا أَكْثَرُ مِنَ الْمَشَاكِلِ؟", hint: "Jawab dengan kalimat terhubung memakai: هَلِ الْمَزَايَا أَكْثَرُ مِنَ الْمَشَاكِلِ؟", sampleAnswer: "هَلِ الْمَزَايَا أَكْثَرُ مِنَ الْمَشَاكِلِ؟", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَلِ", "الْمَزَايَا", "أَكْثَرُ", "مِنَ"], indonesianExplanation: "Apakah kelebihannya lebih banyak dari masalahnya?" },
  ],
  "arabic-b1-asking-about-someones-story": [
    { coach: "كَيْفَ تَسْأَلُ عَنْ قِصَّةِ شَخْصٍ آخَرَ؟", hint: "Jawab dengan kalimat terhubung memakai: مَاذَا حَدَثَ بَعْدَ ذَلِكَ؟", sampleAnswer: "مَاذَا حَدَثَ بَعْدَ ذَلِكَ؟", focus: "Meminta lanjutan cerita.", expectedKeywords: ["مَاذَا", "حَدَثَ", "بَعْدَ", "ذَلِكَ"], indonesianExplanation: "Apa yang terjadi setelah itu?" },
    { coach: "استخدم الفكرة: كَيْفَ شَعَرْتَ فِي تِلْكَ اللَّحْظَةِ؟", hint: "Jawab dengan kalimat terhubung memakai: كَيْفَ شَعَرْتَ فِي تِلْكَ اللَّحْظَةِ؟", sampleAnswer: "كَيْفَ شَعَرْتَ فِي تِلْكَ اللَّحْظَةِ؟", focus: "Menanyakan perasaan.", expectedKeywords: ["كَيْفَ", "شَعَرْتَ", "فِي", "تِلْكَ"], indonesianExplanation: "Bagaimana perasaanmu pada saat itu?" },
    { coach: "استخدم الفكرة: لِمَاذَا كَانَ ذَلِكَ مُهِمًّا لَكَ؟", hint: "Jawab dengan kalimat terhubung memakai: لِمَاذَا كَانَ ذَلِكَ مُهِمًّا لَكَ؟", sampleAnswer: "لِمَاذَا كَانَ ذَلِكَ مُهِمًّا لَكَ؟", focus: "Menanyakan makna cerita.", expectedKeywords: ["لِمَاذَا", "كَانَ", "ذَلِكَ", "مُهِمًّا"], indonesianExplanation: "Mengapa itu penting bagimu?" },
  ],
  "arabic-b1-asking-for-clarification": [
    { coach: "هَلِ التَّعْلِيمَاتُ وَاضِحَةٌ؟", hint: "Jawab dengan kalimat terhubung memakai: هَلْ تَقْصِدِينَ أَنَّ الْمَوْعِدَ تَغَيَّرَ؟", sampleAnswer: "هَلْ تَقْصِدِينَ أَنَّ الْمَوْعِدَ تَغَيَّرَ؟", focus: "Mengecek maksud.", expectedKeywords: ["هَلْ", "تَقْصِدِينَ", "أَنَّ", "الْمَوْعِدَ"], indonesianExplanation: "Apakah maksudmu jadwalnya berubah?" },
    { coach: "استخدم الفكرة: مَا الْمَقْصُودُ بِهَذِهِ النُّقْطَةِ؟", hint: "Jawab dengan kalimat terhubung memakai: مَا الْمَقْصُودُ بِهَذِهِ النُّقْطَةِ؟", sampleAnswer: "مَا الْمَقْصُودُ بِهَذِهِ النُّقْطَةِ؟", focus: "Meminta penjelasan detail.", expectedKeywords: ["مَا", "الْمَقْصُودُ", "بِهَذِهِ", "النُّقْطَةِ"], indonesianExplanation: "Apa maksud poin ini?" },
    { coach: "استخدم الفكرة: أَسْأَلُ لِكَيْ أَتَأَكَّدَ فَقَطْ.", hint: "Jawab dengan kalimat terhubung memakai: أَسْأَلُ لِكَيْ أَتَأَكَّدَ فَقَطْ.", sampleAnswer: "أَسْأَلُ لِكَيْ أَتَأَكَّدَ فَقَطْ.", focus: "Melembutkan klarifikasi.", expectedKeywords: ["أَسْأَلُ", "لِكَيْ", "أَتَأَكَّدَ", "فَقَطْ"], indonesianExplanation: "Saya bertanya hanya untuk memastikan." },
  ],
  "arabic-b1-asking-for-recommendations": [
    { coach: "مَا السُّؤَالُ الَّذِي يُسَاعِدُكَ عَلَى فَهْمِ الْمَوْقِفِ؟", hint: "Jawab dengan kalimat terhubung memakai: هَلْ تُوصِي بِمَطْعَمٍ قَرِيبٍ؟", sampleAnswer: "هَلْ تُوصِي بِمَطْعَمٍ قَرِيبٍ؟", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَلْ", "تُوصِي", "بِمَطْعَمٍ", "قَرِيبٍ"], indonesianExplanation: "Apakah kamu merekomendasikan restoran dekat?" },
    { coach: "استخدم الفكرة: أُفَضِّلُ مَكَانًا هَادِئًا.", hint: "Jawab dengan kalimat terhubung memakai: أُفَضِّلُ مَكَانًا هَادِئًا.", sampleAnswer: "أُفَضِّلُ مَكَانًا هَادِئًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُفَضِّلُ", "مَكَانًا", "هَادِئًا"], indonesianExplanation: "Saya lebih suka tempat yang tenang." },
    { coach: "استخدم الفكرة: يَهُمُّنِي أَنْ يَكُونَ السِّعْرُ مُنَاسِبًا.", hint: "Jawab dengan kalimat terhubung memakai: يَهُمُّنِي أَنْ يَكُونَ السِّعْرُ مُنَاسِبًا.", sampleAnswer: "يَهُمُّنِي أَنْ يَكُونَ السِّعْرُ مُنَاسِبًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["يَهُمُّنِي", "أَنْ", "يَكُونَ", "السِّعْرُ"], indonesianExplanation: "Penting bagi saya agar harganya cocok." },
  ],
  "arabic-b1-b1-final-conversation": [
    { coach: "كَيْفَ تُنْهِي الْحِوَارَ بِخُطْوَةٍ تَالِيَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: سَأَتَحَدَّثُ عَنْ تَجْرِبَةٍ شَخْصِيَّةٍ.", sampleAnswer: "سَأَتَحَدَّثُ عَنْ تَجْرِبَةٍ شَخْصِيَّةٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأَتَحَدَّثُ", "عَنْ", "تَجْرِبَةٍ", "شَخْصِيَّةٍ"], indonesianExplanation: "Saya akan berbicara tentang pengalaman pribadi." },
    { coach: "استخدم الفكرة: ثُمَّ أَشْرَحُ مُشْكِلَةً وَحَلًّا.", hint: "Jawab dengan kalimat terhubung memakai: ثُمَّ أَشْرَحُ مُشْكِلَةً وَحَلًّا.", sampleAnswer: "ثُمَّ أَشْرَحُ مُشْكِلَةً وَحَلًّا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["ثُمَّ", "أَشْرَحُ", "مُشْكِلَةً", "وَحَلًّا"], indonesianExplanation: "Lalu saya menjelaskan masalah dan solusi." },
    { coach: "استخدم الفكرة: بَعْدَ ذَلِكَ، أُبَيِّنُ رَأْيِي بِسَبَبٍ.", hint: "Jawab dengan kalimat terhubung memakai: بَعْدَ ذَلِكَ، أُبَيِّنُ رَأْيِي بِسَبَبٍ.", sampleAnswer: "بَعْدَ ذَلِكَ، أُبَيِّنُ رَأْيِي بِسَبَبٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["بَعْدَ", "ذَلِكَ،", "أُبَيِّنُ", "رَأْيِي"], indonesianExplanation: "Setelah itu, saya menjelaskan pendapat saya dengan alasan." },
  ],
  "arabic-b1-b1-final-test-practice": [
    { coach: "كَيْفَ تَرُدُّ بِطَرِيقَةٍ وَاضِحَةٍ وَمُهَذَّبَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: سَأُجِيبُ بِجُمَلٍ مُتَرَابِطَةٍ.", sampleAnswer: "سَأُجِيبُ بِجُمَلٍ مُتَرَابِطَةٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأُجِيبُ", "بِجُمَلٍ", "مُتَرَابِطَةٍ"], indonesianExplanation: "Saya akan menjawab dengan kalimat yang terhubung." },
    { coach: "استخدم الفكرة: أَذْكُرُ السِّبَاقَ وَالسَّبَبَ وَالنَّتِيجَةَ.", hint: "Jawab dengan kalimat terhubung memakai: أَذْكُرُ السِّبَاقَ وَالسَّبَبَ وَالنَّتِيجَةَ.", sampleAnswer: "أَذْكُرُ السِّبَاقَ وَالسَّبَبَ وَالنَّتِيجَةَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَذْكُرُ", "السِّبَاقَ", "وَالسَّبَبَ", "وَالنَّتِيجَةَ"], indonesianExplanation: "Saya menyebut konteks, alasan, dan hasil." },
    { coach: "استخدم الفكرة: إِذَا لَمْ أَفْهَمْ، أَطْلُبُ تَوْضِيحًا.", hint: "Jawab dengan kalimat terhubung memakai: إِذَا لَمْ أَفْهَمْ، أَطْلُبُ تَوْضِيحًا.", sampleAnswer: "إِذَا لَمْ أَفْهَمْ، أَطْلُبُ تَوْضِيحًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["إِذَا", "لَمْ", "أَفْهَمْ،", "أَطْلُبُ"], indonesianExplanation: "Jika saya tidak paham, saya meminta klarifikasi." },
  ],
  "arabic-b1-being-polite-with-differences": [
    { coach: "كَيْفَ تَرُدُّ بِطَرِيقَةٍ وَاضِحَةٍ وَمُهَذَّبَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: أَفْهَمُ أَنَّ الْعَادَاتِ تَخْتَلِفُ.", sampleAnswer: "أَفْهَمُ أَنَّ الْعَادَاتِ تَخْتَلِفُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَفْهَمُ", "أَنَّ", "الْعَادَاتِ", "تَخْتَلِفُ"], indonesianExplanation: "Saya paham bahwa kebiasaan berbeda-beda." },
    { coach: "استخدم الفكرة: لَا أُرِيدُ أَنْ أُسِيءَ الْفَهْمَ.", hint: "Jawab dengan kalimat terhubung memakai: لَا أُرِيدُ أَنْ أُسِيءَ الْفَهْمَ.", sampleAnswer: "لَا أُرِيدُ أَنْ أُسِيءَ الْفَهْمَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["لَا", "أُرِيدُ", "أَنْ", "أُسِيءَ"], indonesianExplanation: "Saya tidak ingin salah paham." },
    { coach: "استخدم الفكرة: مِنَ الْأَفْضَلِ أَنْ نَسْأَلَ بِأَدَبٍ.", hint: "Jawab dengan kalimat terhubung memakai: مِنَ الْأَفْضَلِ أَنْ نَسْأَلَ بِأَدَبٍ.", sampleAnswer: "مِنَ الْأَفْضَلِ أَنْ نَسْأَلَ بِأَدَبٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["مِنَ", "الْأَفْضَلِ", "أَنْ", "نَسْأَلَ"], indonesianExplanation: "Lebih baik bertanya dengan sopan." },
  ],
  "arabic-b1-checking-in": [
    { coach: "مَا الْفِكْرَةُ الرَّئِيسِيَّةُ الَّتِي تُرِيدُ بَدْءَ الْحِوَارِ بِهَا؟", hint: "Jawab dengan kalimat terhubung memakai: لَدَيَّ حَجْزٌ بِاسْمِ أَحْمَدَ.", sampleAnswer: "لَدَيَّ حَجْزٌ بِاسْمِ أَحْمَدَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["لَدَيَّ", "حَجْزٌ", "بِاسْمِ", "أَحْمَدَ"], indonesianExplanation: "Saya punya reservasi atas nama Ahmad." },
    { coach: "استخدم الفكرة: أُرِيدُ أَنْ أُؤَكِّدَ التَّفَاصِيلَ.", hint: "Jawab dengan kalimat terhubung memakai: أُرِيدُ أَنْ أُؤَكِّدَ التَّفَاصِيلَ.", sampleAnswer: "أُرِيدُ أَنْ أُؤَكِّدَ التَّفَاصِيلَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أُؤَكِّدَ", "التَّفَاصِيلَ"], indonesianExplanation: "Saya ingin mengonfirmasi detailnya." },
    { coach: "استخدم الفكرة: هَلِ الْغُرْفَةُ جَاهِزَةٌ الآنَ؟", hint: "Jawab dengan kalimat terhubung memakai: هَلِ الْغُرْفَةُ جَاهِزَةٌ الآنَ؟", sampleAnswer: "هَلِ الْغُرْفَةُ جَاهِزَةٌ الآنَ؟", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَلِ", "الْغُرْفَةُ", "جَاهِزَةٌ", "الآنَ"], indonesianExplanation: "Apakah kamarnya sudah siap sekarang?" },
  ],
  "arabic-b1-community-culture-mission": [
    { coach: "كَيْفَ تُنْهِي الْحِوَارَ بِخُطْوَةٍ تَالِيَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: سَأَصِفُ مُجْتَمَعِي بِاخْتِصَارٍ.", sampleAnswer: "سَأَصِفُ مُجْتَمَعِي بِاخْتِصَارٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأَصِفُ", "مُجْتَمَعِي", "بِاخْتِصَارٍ"], indonesianExplanation: "Saya akan menjelaskan komunitas saya dengan singkat." },
    { coach: "استخدم الفكرة: تُوجَدُ عَادَةٌ مُهِمَّةٌ عِنْدَنَا.", hint: "Jawab dengan kalimat terhubung memakai: تُوجَدُ عَادَةٌ مُهِمَّةٌ عِنْدَنَا.", sampleAnswer: "تُوجَدُ عَادَةٌ مُهِمَّةٌ عِنْدَنَا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["تُوجَدُ", "عَادَةٌ", "مُهِمَّةٌ", "عِنْدَنَا"], indonesianExplanation: "Ada kebiasaan penting di tempat kami." },
    { coach: "استخدم الفكرة: أُرِيدُ أَنْ أَفْهَمَ عَادَتَكُمْ أَيْضًا.", hint: "Jawab dengan kalimat terhubung memakai: أُرِيدُ أَنْ أَفْهَمَ عَادَتَكُمْ أَيْضًا.", sampleAnswer: "أُرِيدُ أَنْ أَفْهَمَ عَادَتَكُمْ أَيْضًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أَفْهَمَ", "عَادَتَكُمْ"], indonesianExplanation: "Saya ingin memahami kebiasaan kalian juga." },
  ],
  "arabic-b1-comparing-two-options": [
    { coach: "مَا الْفِكْرَةُ الرَّئِيسِيَّةُ الَّتِي تُرِيدُ بَدْءَ الْحِوَارِ بِهَا؟", hint: "Jawab dengan kalimat terhubung memakai: عِنْدَنَا خِيَارَانِ مُخْتَلِفَانِ.", sampleAnswer: "عِنْدَنَا خِيَارَانِ مُخْتَلِفَانِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["عِنْدَنَا", "خِيَارَانِ", "مُخْتَلِفَانِ"], indonesianExplanation: "Kita punya dua pilihan berbeda." },
    { coach: "استخدم الفكرة: الْخِيَارُ الْأَوَّلُ أَسْرَعُ.", hint: "Jawab dengan kalimat terhubung memakai: الْخِيَارُ الْأَوَّلُ أَسْرَعُ.", sampleAnswer: "الْخِيَارُ الْأَوَّلُ أَسْرَعُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["الْخِيَارُ", "الْأَوَّلُ", "أَسْرَعُ"], indonesianExplanation: "Pilihan pertama lebih cepat." },
    { coach: "استخدم الفكرة: الْخِيَارُ الثَّانِي أَرْخَصُ.", hint: "Jawab dengan kalimat terhubung memakai: الْخِيَارُ الثَّانِي أَرْخَصُ.", sampleAnswer: "الْخِيَارُ الثَّانِي أَرْخَصُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["الْخِيَارُ", "الثَّانِي", "أَرْخَصُ"], indonesianExplanation: "Pilihan kedua lebih murah." },
  ],
  "arabic-b1-describing-a-problem": [
    { coach: "مَا الْفِكْرَةُ الرَّئِيسِيَّةُ الَّتِي تُرِيدُ بَدْءَ الْحِوَارِ بِهَا؟", hint: "Jawab dengan kalimat terhubung memakai: تُوجَدُ مُشْكِلَةٌ فِي الْخِدْمَةِ.", sampleAnswer: "تُوجَدُ مُشْكِلَةٌ فِي الْخِدْمَةِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["تُوجَدُ", "مُشْكِلَةٌ", "فِي", "الْخِدْمَةِ"], indonesianExplanation: "Ada masalah pada layanan." },
    { coach: "استخدم الفكرة: الْمُشْكِلَةُ بَدَأَتْ مُنْذُ الصَّبَاحِ.", hint: "Jawab dengan kalimat terhubung memakai: الْمُشْكِلَةُ بَدَأَتْ مُنْذُ الصَّبَاحِ.", sampleAnswer: "الْمُشْكِلَةُ بَدَأَتْ مُنْذُ الصَّبَاحِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["الْمُشْكِلَةُ", "بَدَأَتْ", "مُنْذُ", "الصَّبَاحِ"], indonesianExplanation: "Masalahnya mulai sejak pagi." },
    { coach: "استخدم الفكرة: أَثَّرَ ذَلِكَ عَلَى الْعَمَلِ.", hint: "Jawab dengan kalimat terhubung memakai: أَثَّرَ ذَلِكَ عَلَى الْعَمَلِ.", sampleAnswer: "أَثَّرَ ذَلِكَ عَلَى الْعَمَلِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَثَّرَ", "ذَلِكَ", "عَلَى", "الْعَمَلِ"], indonesianExplanation: "Itu memengaruhi pekerjaan." },
  ],
  "arabic-b1-describing-feelings": [
    { coach: "كَيْفَ شَعَرْتَ فِي ذَلِكَ الْمَوْقِفِ؟", hint: "Jawab dengan kalimat terhubung memakai: شَعَرْتُ بِالْقَلَقِ فِي الْبِدَايَةِ.", sampleAnswer: "شَعَرْتُ بِالْقَلَقِ فِي الْبِدَايَةِ.", focus: "Menyebut perasaan awal.", expectedKeywords: ["شَعَرْتُ", "بِالْقَلَقِ", "فِي", "الْبِدَايَةِ"], indonesianExplanation: "Saya merasa khawatir di awal." },
    { coach: "استخدم الفكرة: لِأَنَّ الْمَوْقِفَ كَانَ جَدِيدًا عَلَيَّ.", hint: "Jawab dengan kalimat terhubung memakai: لِأَنَّ الْمَوْقِفَ كَانَ جَدِيدًا عَلَيَّ.", sampleAnswer: "لِأَنَّ الْمَوْقِفَ كَانَ جَدِيدًا عَلَيَّ.", focus: "Memberi alasan perasaan.", expectedKeywords: ["لِأَنَّ", "الْمَوْقِفَ", "كَانَ", "جَدِيدًا"], indonesianExplanation: "Karena situasinya baru bagi saya." },
    { coach: "استخدم الفكرة: بَعْدَ قَلِيلٍ، شَعَرْتُ بِالرَّاحَةِ.", hint: "Jawab dengan kalimat terhubung memakai: بَعْدَ قَلِيلٍ، شَعَرْتُ بِالرَّاحَةِ.", sampleAnswer: "بَعْدَ قَلِيلٍ، شَعَرْتُ بِالرَّاحَةِ.", focus: "Menunjukkan perubahan perasaan.", expectedKeywords: ["بَعْدَ", "قَلِيلٍ،", "شَعَرْتُ", "بِالرَّاحَةِ"], indonesianExplanation: "Setelah sebentar, saya merasa nyaman." },
  ],
  "arabic-b1-describing-your-community": [
    { coach: "مَا الْفِكْرَةُ الرَّئِيسِيَّةُ الَّتِي تُرِيدُ بَدْءَ الْحِوَارِ بِهَا؟", hint: "Jawab dengan kalimat terhubung memakai: أَعِيشُ فِي مُجْتَمَعٍ هَادِئٍ.", sampleAnswer: "أَعِيشُ فِي مُجْتَمَعٍ هَادِئٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَعِيشُ", "فِي", "مُجْتَمَعٍ", "هَادِئٍ"], indonesianExplanation: "Saya tinggal di komunitas yang tenang." },
    { coach: "استخدم الفكرة: النَّاسُ يَتَعَاوَنُونَ فِي الْأَعْمَالِ الْيَوْمِيَّةِ.", hint: "Jawab dengan kalimat terhubung memakai: النَّاسُ يَتَعَاوَنُونَ فِي الْأَعْمَالِ الْيَوْمِيَّةِ.", sampleAnswer: "النَّاسُ يَتَعَاوَنُونَ فِي الْأَعْمَالِ الْيَوْمِيَّةِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["النَّاسُ", "يَتَعَاوَنُونَ", "فِي", "الْأَعْمَالِ"], indonesianExplanation: "Orang-orang saling membantu dalam pekerjaan harian." },
    { coach: "استخدم الفكرة: تُوجَدُ عَادَاتٌ جَمِيلَةٌ فِي الْحَيِّ.", hint: "Jawab dengan kalimat terhubung memakai: تُوجَدُ عَادَاتٌ جَمِيلَةٌ فِي الْحَيِّ.", sampleAnswer: "تُوجَدُ عَادَاتٌ جَمِيلَةٌ فِي الْحَيِّ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["تُوجَدُ", "عَادَاتٌ", "جَمِيلَةٌ", "فِي"], indonesianExplanation: "Ada kebiasaan indah di lingkungan." },
  ],
  "arabic-b1-discussing-challenges": [
    { coach: "مَا السُّؤَالُ الَّذِي يُسَاعِدُكَ عَلَى فَهْمِ الْمَوْقِفِ؟", hint: "Jawab dengan kalimat terhubung memakai: أَكْبَرُ تَحَدٍّ هُوَ السُّرْعَةُ.", sampleAnswer: "أَكْبَرُ تَحَدٍّ هُوَ السُّرْعَةُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَكْبَرُ", "تَحَدٍّ", "هُوَ", "السُّرْعَةُ"], indonesianExplanation: "Tantangan terbesar adalah kecepatan." },
    { coach: "استخدم الفكرة: أَحْتَاجُ إِلَى وَقْتٍ لِلتَّفْكِيرِ.", hint: "Jawab dengan kalimat terhubung memakai: أَحْتَاجُ إِلَى وَقْتٍ لِلتَّفْكِيرِ.", sampleAnswer: "أَحْتَاجُ إِلَى وَقْتٍ لِلتَّفْكِيرِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَحْتَاجُ", "إِلَى", "وَقْتٍ", "لِلتَّفْكِيرِ"], indonesianExplanation: "Saya butuh waktu untuk berpikir." },
    { coach: "استخدم الفكرة: أَحْيَانًا أَنْسَى الْكَلِمَاتِ الْمُنَاسِبَةَ.", hint: "Jawab dengan kalimat terhubung memakai: أَحْيَانًا أَنْسَى الْكَلِمَاتِ الْمُنَاسِبَةَ.", sampleAnswer: "أَحْيَانًا أَنْسَى الْكَلِمَاتِ الْمُنَاسِبَةَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَحْيَانًا", "أَنْسَى", "الْكَلِمَاتِ", "الْمُنَاسِبَةَ"], indonesianExplanation: "Kadang saya lupa kata yang cocok." },
  ],
  "arabic-b1-explaining-a-delay": [
    { coach: "مَا أَوَّلُ تَفْصِيلٍ يَحْتَاجُ إِلَى شَرْحٍ؟", hint: "Jawab dengan kalimat terhubung memakai: تَأَخَّرَتِ الرِّحْلَةُ قَلِيلًا.", sampleAnswer: "تَأَخَّرَتِ الرِّحْلَةُ قَلِيلًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["تَأَخَّرَتِ", "الرِّحْلَةُ", "قَلِيلًا"], indonesianExplanation: "Perjalanannya sedikit terlambat." },
    { coach: "استخدم الفكرة: السَّبَبُ هُوَ الِازْدِحَامُ فِي الطَّرِيقِ.", hint: "Jawab dengan kalimat terhubung memakai: السَّبَبُ هُوَ الِازْدِحَامُ فِي الطَّرِيقِ.", sampleAnswer: "السَّبَبُ هُوَ الِازْدِحَامُ فِي الطَّرِيقِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["السَّبَبُ", "هُوَ", "الِازْدِحَامُ", "فِي"], indonesianExplanation: "Alasannya adalah kemacetan di jalan." },
    { coach: "استخدم الفكرة: سَأَصِلُ بَعْدَ ثَلَاثِينَ دَقِيقَةً.", hint: "Jawab dengan kalimat terhubung memakai: سَأَصِلُ بَعْدَ ثَلَاثِينَ دَقِيقَةً.", sampleAnswer: "سَأَصِلُ بَعْدَ ثَلَاثِينَ دَقِيقَةً.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأَصِلُ", "بَعْدَ", "ثَلَاثِينَ", "دَقِيقَةً"], indonesianExplanation: "Saya akan tiba setelah tiga puluh menit." },
  ],
  "arabic-b1-explaining-progress": [
    { coach: "مَا أَوَّلُ تَفْصِيلٍ يَحْتَاجُ إِلَى شَرْحٍ؟", hint: "Jawab dengan kalimat terhubung memakai: تَقَدَّمْتُ قَلِيلًا هَذَا الشَّهْرَ.", sampleAnswer: "تَقَدَّمْتُ قَلِيلًا هَذَا الشَّهْرَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["تَقَدَّمْتُ", "قَلِيلًا", "هَذَا", "الشَّهْرَ"], indonesianExplanation: "Saya sedikit maju bulan ini." },
    { coach: "استخدم الفكرة: أَصْبَحْتُ أَفْهَمُ الْحِوَارَ أَسْرَعَ.", hint: "Jawab dengan kalimat terhubung memakai: أَصْبَحْتُ أَفْهَمُ الْحِوَارَ أَسْرَعَ.", sampleAnswer: "أَصْبَحْتُ أَفْهَمُ الْحِوَارَ أَسْرَعَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَصْبَحْتُ", "أَفْهَمُ", "الْحِوَارَ", "أَسْرَعَ"], indonesianExplanation: "Saya menjadi lebih cepat memahami dialog." },
    { coach: "استخدم الفكرة: مَا زِلْتُ أُخْطِئُ فِي بَعْضِ الْجُمَلِ.", hint: "Jawab dengan kalimat terhubung memakai: مَا زِلْتُ أُخْطِئُ فِي بَعْضِ الْجُمَلِ.", sampleAnswer: "مَا زِلْتُ أُخْطِئُ فِي بَعْضِ الْجُمَلِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["مَا", "زِلْتُ", "أُخْطِئُ", "فِي"], indonesianExplanation: "Saya masih salah pada beberapa kalimat." },
  ],
  "arabic-b1-explaining-why-you-prefer-something": [
    { coach: "مَا أَوَّلُ تَفْصِيلٍ يَحْتَاجُ إِلَى شَرْحٍ؟", hint: "Jawab dengan kalimat terhubung memakai: أُفَضِّلُ هَذَا الْخِيَارَ لِأَنَّهُ أَوْضَحُ.", sampleAnswer: "أُفَضِّلُ هَذَا الْخِيَارَ لِأَنَّهُ أَوْضَحُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُفَضِّلُ", "هَذَا", "الْخِيَارَ", "لِأَنَّهُ"], indonesianExplanation: "Saya lebih memilih pilihan ini karena lebih jelas." },
    { coach: "استخدم الفكرة: يُنَاسِبُ هَدَفَنَا أَكْثَرَ.", hint: "Jawab dengan kalimat terhubung memakai: يُنَاسِبُ هَدَفَنَا أَكْثَرَ.", sampleAnswer: "يُنَاسِبُ هَدَفَنَا أَكْثَرَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["يُنَاسِبُ", "هَدَفَنَا", "أَكْثَرَ"], indonesianExplanation: "Ini lebih cocok dengan tujuan kita." },
    { coach: "استخدم الفكرة: رَغْمَ أَنَّهُ أَغْلَى قَلِيلًا.", hint: "Jawab dengan kalimat terhubung memakai: رَغْمَ أَنَّهُ أَغْلَى قَلِيلًا.", sampleAnswer: "رَغْمَ أَنَّهُ أَغْلَى قَلِيلًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["رَغْمَ", "أَنَّهُ", "أَغْلَى", "قَلِيلًا"], indonesianExplanation: "Meskipun sedikit lebih mahal." },
  ],
  "arabic-b1-explaining-your-task": [
    { coach: "مَا الْمَهَمَّةُ الَّتِي تَعْمَلِينَ عَلَيْهَا؟", hint: "Jawab dengan kalimat terhubung memakai: أَعْمَلُ عَلَى مَهَمَّةٍ جَدِيدَةٍ هَذَا الْأُسْبُوعَ.", sampleAnswer: "أَعْمَلُ عَلَى مَهَمَّةٍ جَدِيدَةٍ هَذَا الْأُسْبُوعَ.", focus: "Menjelaskan tugas utama.", expectedKeywords: ["أَعْمَلُ", "عَلَى", "مَهَمَّةٍ", "جَدِيدَةٍ"], indonesianExplanation: "Saya mengerjakan tugas baru minggu ini." },
    { coach: "استخدم الفكرة: الْهَدَفُ هُوَ تَحْسِينُ التَّنْظِيمِ.", hint: "Jawab dengan kalimat terhubung memakai: الْهَدَفُ هُوَ تَحْسِينُ التَّنْظِيمِ.", sampleAnswer: "الْهَدَفُ هُوَ تَحْسِينُ التَّنْظِيمِ.", focus: "Menjelaskan tujuan.", expectedKeywords: ["الْهَدَفُ", "هُوَ", "تَحْسِينُ", "التَّنْظِيمِ"], indonesianExplanation: "Tujuannya adalah memperbaiki pengaturan." },
    { coach: "استخدم الفكرة: أَحْتَاجُ إِلَى مَرَاجَعَةِ التَّفَاصِيلِ أَوَّلًا.", hint: "Jawab dengan kalimat terhubung memakai: أَحْتَاجُ إِلَى مَرَاجَعَةِ التَّفَاصِيلِ أَوَّلًا.", sampleAnswer: "أَحْتَاجُ إِلَى مَرَاجَعَةِ التَّفَاصِيلِ أَوَّلًا.", focus: "Menjelaskan langkah awal.", expectedKeywords: ["أَحْتَاجُ", "إِلَى", "مَرَاجَعَةِ", "التَّفَاصِيلِ"], indonesianExplanation: "Saya perlu meninjau detailnya dulu." },
  ],
  "arabic-b1-giving-a-short-update": [
    { coach: "هَلْ عِنْدَكِ تَحْدِيثٌ قَصِيرٌ؟", hint: "Jawab dengan kalimat terhubung memakai: أَنْجَزْتُ الْجُزْءَ الْأَوَّلَ مِنَ الْمَهَمَّةِ.", sampleAnswer: "أَنْجَزْتُ الْجُزْءَ الْأَوَّلَ مِنَ الْمَهَمَّةِ.", focus: "Menyebut progress.", expectedKeywords: ["أَنْجَزْتُ", "الْجُزْءَ", "الْأَوَّلَ", "مِنَ"], indonesianExplanation: "Saya sudah menyelesaikan bagian pertama tugas." },
    { coach: "استخدم الفكرة: مَا زِلْتُ أَعْمَلُ عَلَى التَّفَاصِيلِ.", hint: "Jawab dengan kalimat terhubung memakai: مَا زِلْتُ أَعْمَلُ عَلَى التَّفَاصِيلِ.", sampleAnswer: "مَا زِلْتُ أَعْمَلُ عَلَى التَّفَاصِيلِ.", focus: "Menyebut yang belum selesai.", expectedKeywords: ["مَا", "زِلْتُ", "أَعْمَلُ", "عَلَى"], indonesianExplanation: "Saya masih mengerjakan detailnya." },
    { coach: "استخدم الفكرة: لَا تُوجَدُ مُشْكِلَةٌ كَبِيرَةٌ حَتَّى الْآنَ.", hint: "Jawab dengan kalimat terhubung memakai: لَا تُوجَدُ مُشْكِلَةٌ كَبِيرَةٌ حَتَّى الْآنَ.", sampleAnswer: "لَا تُوجَدُ مُشْكِلَةٌ كَبِيرَةٌ حَتَّى الْآنَ.", focus: "Memberi status kendala.", expectedKeywords: ["لَا", "تُوجَدُ", "مُشْكِلَةٌ", "كَبِيرَةٌ"], indonesianExplanation: "Belum ada masalah besar sampai sekarang." },
  ],
  "arabic-b1-goals-progress-mission": [
    { coach: "كَيْفَ تُنْهِي الْحِوَارَ بِخُطْوَةٍ تَالِيَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: هَدَفِي وَاضِحٌ لِهَذَا الشَّهْرِ.", sampleAnswer: "هَدَفِي وَاضِحٌ لِهَذَا الشَّهْرِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَدَفِي", "وَاضِحٌ", "لِهَذَا", "الشَّهْرِ"], indonesianExplanation: "Tujuan saya jelas untuk bulan ini." },
    { coach: "استخدم الفكرة: تَقَدَّمْتُ فِي الِاسْتِمَاعِ، وَلَكِنَّ الْكَلَامَ أَصْعَبُ.", hint: "Jawab dengan kalimat terhubung memakai: تَقَدَّمْتُ فِي الِاسْتِمَاعِ، وَلَكِنَّ الْكَلَامَ أَصْعَبُ.", sampleAnswer: "تَقَدَّمْتُ فِي الِاسْتِمَاعِ، وَلَكِنَّ الْكَلَامَ أَصْعَبُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["تَقَدَّمْتُ", "فِي", "الِاسْتِمَاعِ،", "وَلَكِنَّ"], indonesianExplanation: "Saya maju dalam listening, tetapi speaking lebih sulit." },
    { coach: "استخدم الفكرة: أَكْبَرُ تَحَدٍّ هُوَ التَّرَدُّدُ.", hint: "Jawab dengan kalimat terhubung memakai: أَكْبَرُ تَحَدٍّ هُوَ التَّرَدُّدُ.", sampleAnswer: "أَكْبَرُ تَحَدٍّ هُوَ التَّرَدُّدُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَكْبَرُ", "تَحَدٍّ", "هُوَ", "التَّرَدُّدُ"], indonesianExplanation: "Tantangan terbesar adalah keraguan." },
  ],
  "arabic-b1-handling-a-simple-complaint": [
    { coach: "كَيْفَ تَرُدُّ بِطَرِيقَةٍ وَاضِحَةٍ وَمُهَذَّبَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: أُرِيدُ أَنْ أُوَضِّحَ مُشْكِلَةً صَغِيرَةً.", sampleAnswer: "أُرِيدُ أَنْ أُوَضِّحَ مُشْكِلَةً صَغِيرَةً.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أُوَضِّحَ", "مُشْكِلَةً"], indonesianExplanation: "Saya ingin menjelaskan masalah kecil." },
    { coach: "استخدم الفكرة: الْغُرْفَةُ غَيْرُ نَظِيفَةٍ تَمَامًا.", hint: "Jawab dengan kalimat terhubung memakai: الْغُرْفَةُ غَيْرُ نَظِيفَةٍ تَمَامًا.", sampleAnswer: "الْغُرْفَةُ غَيْرُ نَظِيفَةٍ تَمَامًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["الْغُرْفَةُ", "غَيْرُ", "نَظِيفَةٍ", "تَمَامًا"], indonesianExplanation: "Kamarnya tidak sepenuhnya bersih." },
    { coach: "استخدم الفكرة: هَلْ يُمْكِنُ أَنْ تُرْسِلُوا أَحَدًا؟", hint: "Jawab dengan kalimat terhubung memakai: هَلْ يُمْكِنُ أَنْ تُرْسِلُوا أَحَدًا؟", sampleAnswer: "هَلْ يُمْكِنُ أَنْ تُرْسِلُوا أَحَدًا؟", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَلْ", "يُمْكِنُ", "أَنْ", "تُرْسِلُوا"], indonesianExplanation: "Bisakah kalian mengirim seseorang?" },
  ],
  "arabic-b1-joining-a-simple-meeting": [
    { coach: "هَلْ تُرِيدِينَ أَنْ تُضِيفِي شَيْئًا؟", hint: "Jawab dengan kalimat terhubung memakai: أُرِيدُ أَنْ أُضِيفَ نُقْطَةً صَغِيرَةً.", sampleAnswer: "أُرِيدُ أَنْ أُضِيفَ نُقْطَةً صَغِيرَةً.", focus: "Masuk diskusi dengan sopan.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أُضِيفَ", "نُقْطَةً"], indonesianExplanation: "Saya ingin menambahkan poin kecil." },
    { coach: "استخدم الفكرة: أَقْتَرِحُ أَنْ نُرَاجِعَ الْخُطَّةَ أَوَّلًا.", hint: "Jawab dengan kalimat terhubung memakai: أَقْتَرِحُ أَنْ نُرَاجِعَ الْخُطَّةَ أَوَّلًا.", sampleAnswer: "أَقْتَرِحُ أَنْ نُرَاجِعَ الْخُطَّةَ أَوَّلًا.", focus: "Memberi saran.", expectedKeywords: ["أَقْتَرِحُ", "أَنْ", "نُرَاجِعَ", "الْخُطَّةَ"], indonesianExplanation: "Saya menyarankan kita meninjau rencana dulu." },
    { coach: "استخدم الفكرة: هَذَا يُمْكِنُ أَنْ يُقَلِّلَ الْخَطَأَ.", hint: "Jawab dengan kalimat terhubung memakai: هَذَا يُمْكِنُ أَنْ يُقَلِّلَ الْخَطَأَ.", sampleAnswer: "هَذَا يُمْكِنُ أَنْ يُقَلِّلَ الْخَطَأَ.", focus: "Memberi alasan saran.", expectedKeywords: ["هَذَا", "يُمْكِنُ", "أَنْ", "يُقَلِّلَ"], indonesianExplanation: "Ini bisa mengurangi kesalahan." },
  ],
  "arabic-b1-making-a-simple-decision": [
    { coach: "كَيْفَ تَرُدُّ بِطَرِيقَةٍ وَاضِحَةٍ وَمُهَذَّبَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: لَدَيْنَا خِيَارَانِ مُنَاسِبَانِ.", sampleAnswer: "لَدَيْنَا خِيَارَانِ مُنَاسِبَانِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["لَدَيْنَا", "خِيَارَانِ", "مُنَاسِبَانِ"], indonesianExplanation: "Kita punya dua pilihan yang cocok." },
    { coach: "استخدم الفكرة: الْخِيَارُ الْأَوَّلُ أَسْهَلُ.", hint: "Jawab dengan kalimat terhubung memakai: الْخِيَارُ الْأَوَّلُ أَسْهَلُ.", sampleAnswer: "الْخِيَارُ الْأَوَّلُ أَسْهَلُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["الْخِيَارُ", "الْأَوَّلُ", "أَسْهَلُ"], indonesianExplanation: "Pilihan pertama lebih mudah." },
    { coach: "استخدم الفكرة: الْخِيَارُ الثَّانِي أَفْضَلُ عَلَى الْمَدَى الطَّوِيلِ.", hint: "Jawab dengan kalimat terhubung memakai: الْخِيَارُ الثَّانِي أَفْضَلُ عَلَى الْمَدَى الطَّوِيلِ.", sampleAnswer: "الْخِيَارُ الثَّانِي أَفْضَلُ عَلَى الْمَدَى الطَّوِيلِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["الْخِيَارُ", "الثَّانِي", "أَفْضَلُ", "عَلَى"], indonesianExplanation: "Pilihan kedua lebih baik untuk jangka panjang." },
  ],
  "arabic-b1-making-next-step-plans": [
    { coach: "كَيْفَ تَرُدُّ بِطَرِيقَةٍ وَاضِحَةٍ وَمُهَذَّبَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: الْخُطْوَةُ التَّالِيَةُ هِيَ التَّدْرِيبُ الْيَوْمِيُّ.", sampleAnswer: "الْخُطْوَةُ التَّالِيَةُ هِيَ التَّدْرِيبُ الْيَوْمِيُّ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["الْخُطْوَةُ", "التَّالِيَةُ", "هِيَ", "التَّدْرِيبُ"], indonesianExplanation: "Langkah berikutnya adalah latihan harian." },
    { coach: "استخدم الفكرة: سَأُرَاجِعُ خَمْسَ عِبَارَاتٍ كُلَّ يَوْمٍ.", hint: "Jawab dengan kalimat terhubung memakai: سَأُرَاجِعُ خَمْسَ عِبَارَاتٍ كُلَّ يَوْمٍ.", sampleAnswer: "سَأُرَاجِعُ خَمْسَ عِبَارَاتٍ كُلَّ يَوْمٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأُرَاجِعُ", "خَمْسَ", "عِبَارَاتٍ", "كُلَّ"], indonesianExplanation: "Saya akan meninjau lima frasa setiap hari." },
    { coach: "استخدم الفكرة: سَأُسَجِّلُ صَوْتِي مَرَّةً وَاحِدَةً.", hint: "Jawab dengan kalimat terhubung memakai: سَأُسَجِّلُ صَوْتِي مَرَّةً وَاحِدَةً.", sampleAnswer: "سَأُسَجِّلُ صَوْتِي مَرَّةً وَاحِدَةً.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأُسَجِّلُ", "صَوْتِي", "مَرَّةً", "وَاحِدَةً"], indonesianExplanation: "Saya akan merekam suara saya satu kali." },
  ],
  "arabic-b1-personal-story-mission": [
    { coach: "احْكِ لِي قِصَّةً قَصِيرَةً عَنْ تَجْرِبَتِكَ.", hint: "Jawab dengan kalimat terhubung memakai: فِي الْبِدَايَةِ، كَانَ الْمَوْقِفُ غَيْرَ وَاضِحٍ.", sampleAnswer: "فِي الْبِدَايَةِ، كَانَ الْمَوْقِفُ غَيْرَ وَاضِحٍ.", focus: "Membuka cerita dengan masalah ringan.", expectedKeywords: ["فِي", "الْبِدَايَةِ،", "كَانَ", "الْمَوْقِفُ"], indonesianExplanation: "Di awal, situasinya belum jelas." },
    { coach: "استخدم الفكرة: ثُمَّ سَأَلْتُ صَدِيقِي عَنْ التَّفَاصِيلِ.", hint: "Jawab dengan kalimat terhubung memakai: ثُمَّ سَأَلْتُ صَدِيقِي عَنْ التَّفَاصِيلِ.", sampleAnswer: "ثُمَّ سَأَلْتُ صَدِيقِي عَنْ التَّفَاصِيلِ.", focus: "Menyebut tindakan.", expectedKeywords: ["ثُمَّ", "سَأَلْتُ", "صَدِيقِي", "عَنْ"], indonesianExplanation: "Lalu saya bertanya kepada teman saya tentang detailnya." },
    { coach: "استخدم الفكرة: بَعْدَ ذَلِكَ، فَهِمْتُ السَّبَبَ.", hint: "Jawab dengan kalimat terhubung memakai: بَعْدَ ذَلِكَ، فَهِمْتُ السَّبَبَ.", sampleAnswer: "بَعْدَ ذَلِكَ، فَهِمْتُ السَّبَبَ.", focus: "Menunjukkan perkembangan cerita.", expectedKeywords: ["بَعْدَ", "ذَلِكَ،", "فَهِمْتُ", "السَّبَبَ"], indonesianExplanation: "Setelah itu, saya memahami alasannya." },
  ],
  "arabic-b1-preference-discussion-mission": [
    { coach: "كَيْفَ تُنْهِي الْحِوَارَ بِخُطْوَةٍ تَالِيَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: سَأُقَارِنُ بَيْنَ خِيَارَيْنِ.", sampleAnswer: "سَأُقَارِنُ بَيْنَ خِيَارَيْنِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأُقَارِنُ", "بَيْنَ", "خِيَارَيْنِ"], indonesianExplanation: "Saya akan membandingkan dua pilihan." },
    { coach: "استخدم الفكرة: أُفَضِّلُ الْخِيَارَ الْأَوَّلَ لِأَنَّهُ أَسْهَلُ.", hint: "Jawab dengan kalimat terhubung memakai: أُفَضِّلُ الْخِيَارَ الْأَوَّلَ لِأَنَّهُ أَسْهَلُ.", sampleAnswer: "أُفَضِّلُ الْخِيَارَ الْأَوَّلَ لِأَنَّهُ أَسْهَلُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُفَضِّلُ", "الْخِيَارَ", "الْأَوَّلَ", "لِأَنَّهُ"], indonesianExplanation: "Saya lebih memilih pilihan pertama karena lebih mudah." },
    { coach: "استخدم الفكرة: لَكِنَّ الْخِيَارَ الثَّانِي أَقْوَى.", hint: "Jawab dengan kalimat terhubung memakai: لَكِنَّ الْخِيَارَ الثَّانِي أَقْوَى.", sampleAnswer: "لَكِنَّ الْخِيَارَ الثَّانِي أَقْوَى.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["لَكِنَّ", "الْخِيَارَ", "الثَّانِي", "أَقْوَى"], indonesianExplanation: "Tetapi pilihan kedua lebih kuat." },
  ],
  "arabic-b1-problem-solving-mission": [
    { coach: "كَيْفَ تُنْهِي الْحِوَارَ بِخُطْوَةٍ تَالِيَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: سَأَشْرَحُ الْمُشْكِلَةَ بِاخْتِصَارٍ.", sampleAnswer: "سَأَشْرَحُ الْمُشْكِلَةَ بِاخْتِصَارٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأَشْرَحُ", "الْمُشْكِلَةَ", "بِاخْتِصَارٍ"], indonesianExplanation: "Saya akan menjelaskan masalahnya dengan singkat." },
    { coach: "استخدم الفكرة: السَّبَبُ غَيْرُ وَاضِحٍ حَتَّى الْآنَ.", hint: "Jawab dengan kalimat terhubung memakai: السَّبَبُ غَيْرُ وَاضِحٍ حَتَّى الْآنَ.", sampleAnswer: "السَّبَبُ غَيْرُ وَاضِحٍ حَتَّى الْآنَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["السَّبَبُ", "غَيْرُ", "وَاضِحٍ", "حَتَّى"], indonesianExplanation: "Penyebabnya belum jelas sampai sekarang." },
    { coach: "استخدم الفكرة: أَقْتَرِحُ أَنْ نُجَرِّبَ حَلًّا مُؤَقَّتًا.", hint: "Jawab dengan kalimat terhubung memakai: أَقْتَرِحُ أَنْ نُجَرِّبَ حَلًّا مُؤَقَّتًا.", sampleAnswer: "أَقْتَرِحُ أَنْ نُجَرِّبَ حَلًّا مُؤَقَّتًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَقْتَرِحُ", "أَنْ", "نُجَرِّبَ", "حَلًّا"], indonesianExplanation: "Saya menyarankan kita mencoba solusi sementara." },
  ],
  "arabic-b1-reaching-agreement": [
    { coach: "كَيْفَ تَرُدُّ بِطَرِيقَةٍ وَاضِحَةٍ وَمُهَذَّبَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: أَتَّفِقُ مَعَكِ فِي النُّقْطَةِ الْأُولَى.", sampleAnswer: "أَتَّفِقُ مَعَكِ فِي النُّقْطَةِ الْأُولَى.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَتَّفِقُ", "مَعَكِ", "فِي", "النُّقْطَةِ"], indonesianExplanation: "Saya setuju denganmu pada poin pertama." },
    { coach: "استخدم الفكرة: لَكِنَّنِي أَرَى خِيَارًا آخَرَ.", hint: "Jawab dengan kalimat terhubung memakai: لَكِنَّنِي أَرَى خِيَارًا آخَرَ.", sampleAnswer: "لَكِنَّنِي أَرَى خِيَارًا آخَرَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["لَكِنَّنِي", "أَرَى", "خِيَارًا", "آخَرَ"], indonesianExplanation: "Tetapi saya melihat pilihan lain." },
    { coach: "استخدم الفكرة: مُمْكِنٌ أَنْ نَجْمَعَ بَيْنَ الْفِكْرَتَيْنِ.", hint: "Jawab dengan kalimat terhubung memakai: مُمْكِنٌ أَنْ نَجْمَعَ بَيْنَ الْفِكْرَتَيْنِ.", sampleAnswer: "مُمْكِنٌ أَنْ نَجْمَعَ بَيْنَ الْفِكْرَتَيْنِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["مُمْكِنٌ", "أَنْ", "نَجْمَعَ", "بَيْنَ"], indonesianExplanation: "Mungkin kita bisa menggabungkan dua ide." },
  ],
  "arabic-b1-responding-to-advice": [
    { coach: "مَا السُّؤَالُ الَّذِي يُسَاعِدُكَ عَلَى فَهْمِ الْمَوْقِفِ؟", hint: "Jawab dengan kalimat terhubung memakai: نَصِيحَتُكَ مُفِيدَةٌ.", sampleAnswer: "نَصِيحَتُكَ مُفِيدَةٌ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["نَصِيحَتُكَ", "مُفِيدَةٌ"], indonesianExplanation: "Nasihatmu bermanfaat." },
    { coach: "استخدم الفكرة: سَأُجَرِّبُ ذَلِكَ الْيَوْمَ.", hint: "Jawab dengan kalimat terhubung memakai: سَأُجَرِّبُ ذَلِكَ الْيَوْمَ.", sampleAnswer: "سَأُجَرِّبُ ذَلِكَ الْيَوْمَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأُجَرِّبُ", "ذَلِكَ", "الْيَوْمَ"], indonesianExplanation: "Saya akan mencoba itu hari ini." },
    { coach: "استخدم الفكرة: أَتَّفِقُ مَعَكَ فِي هَذِهِ النُّقْطَةِ.", hint: "Jawab dengan kalimat terhubung memakai: أَتَّفِقُ مَعَكَ فِي هَذِهِ النُّقْطَةِ.", sampleAnswer: "أَتَّفِقُ مَعَكَ فِي هَذِهِ النُّقْطَةِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَتَّفِقُ", "مَعَكَ", "فِي", "هَذِهِ"], indonesianExplanation: "Saya setuju denganmu pada poin ini." },
  ],
  "arabic-b1-review-goals-and-preferences": [
    { coach: "مَا السُّؤَالُ الَّذِي يُسَاعِدُكَ عَلَى فَهْمِ الْمَوْقِفِ؟", hint: "Jawab dengan kalimat terhubung memakai: هَدَفِي وَاضِحٌ وَلَكِنَّ التَّحَدِّي مَوْجُودٌ.", sampleAnswer: "هَدَفِي وَاضِحٌ وَلَكِنَّ التَّحَدِّي مَوْجُودٌ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَدَفِي", "وَاضِحٌ", "وَلَكِنَّ", "التَّحَدِّي"], indonesianExplanation: "Tujuan saya jelas tetapi tantangannya ada." },
    { coach: "استخدم الفكرة: أُفَضِّلُ خُطَّةً بَسِيطَةً وَمُسْتَمِرَّةً.", hint: "Jawab dengan kalimat terhubung memakai: أُفَضِّلُ خُطَّةً بَسِيطَةً وَمُسْتَمِرَّةً.", sampleAnswer: "أُفَضِّلُ خُطَّةً بَسِيطَةً وَمُسْتَمِرَّةً.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُفَضِّلُ", "خُطَّةً", "بَسِيطَةً", "وَمُسْتَمِرَّةً"], indonesianExplanation: "Saya lebih memilih rencana sederhana dan berkelanjutan." },
    { coach: "استخدم الفكرة: سَأُقَارِنُ بَيْنَ خِيَارَيْنِ.", hint: "Jawab dengan kalimat terhubung memakai: سَأُقَارِنُ بَيْنَ خِيَارَيْنِ.", sampleAnswer: "سَأُقَارِنُ بَيْنَ خِيَارَيْنِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأُقَارِنُ", "بَيْنَ", "خِيَارَيْنِ"], indonesianExplanation: "Saya akan membandingkan dua pilihan." },
  ],
  "arabic-b1-review-problems-and-travel": [
    { coach: "مَا أَوَّلُ تَفْصِيلٍ يَحْتَاجُ إِلَى شَرْحٍ؟", hint: "Jawab dengan kalimat terhubung memakai: سَأَشْرَحُ مُشْكِلَةً ثُمَّ أَقْتَرِحُ حَلًّا.", sampleAnswer: "سَأَشْرَحُ مُشْكِلَةً ثُمَّ أَقْتَرِحُ حَلًّا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأَشْرَحُ", "مُشْكِلَةً", "ثُمَّ", "أَقْتَرِحُ"], indonesianExplanation: "Saya akan menjelaskan masalah lalu menyarankan solusi." },
    { coach: "استخدم الفكرة: فِي السَّفَرِ، أَحْتَاجُ إِلَى تَفَاصِيلَ وَاضِحَةٍ.", hint: "Jawab dengan kalimat terhubung memakai: فِي السَّفَرِ، أَحْتَاجُ إِلَى تَفَاصِيلَ وَاضِحَةٍ.", sampleAnswer: "فِي السَّفَرِ، أَحْتَاجُ إِلَى تَفَاصِيلَ وَاضِحَةٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["فِي", "السَّفَرِ،", "أَحْتَاجُ", "إِلَى"], indonesianExplanation: "Dalam perjalanan, saya butuh detail jelas." },
    { coach: "استخدم الفكرة: إِذَا حَدَثَ تَأْخِيرٌ، سَأُخْبِرُ الطَّرَفَ الْآخَرَ.", hint: "Jawab dengan kalimat terhubung memakai: إِذَا حَدَثَ تَأْخِيرٌ، سَأُخْبِرُ الطَّرَفَ الْآخَرَ.", sampleAnswer: "إِذَا حَدَثَ تَأْخِيرٌ، سَأُخْبِرُ الطَّرَفَ الْآخَرَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["إِذَا", "حَدَثَ", "تَأْخِيرٌ،", "سَأُخْبِرُ"], indonesianExplanation: "Jika terjadi keterlambatan, saya akan memberi tahu pihak lain." },
  ],
  "arabic-b1-review-stories-and-work": [
    { coach: "مَا الْفِكْرَةُ الرَّئِيسِيَّةُ الَّتِي تُرِيدُ بَدْءَ الْحِوَارِ بِهَا؟", hint: "Jawab dengan kalimat terhubung memakai: سَأَبْدَأُ بِقِصَّةٍ قَصِيرَةٍ.", sampleAnswer: "سَأَبْدَأُ بِقِصَّةٍ قَصِيرَةٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["سَأَبْدَأُ", "بِقِصَّةٍ", "قَصِيرَةٍ"], indonesianExplanation: "Saya akan mulai dengan cerita singkat." },
    { coach: "استخدم الفكرة: بَعْدَ ذَلِكَ، أُعْطِي تَحْدِيثًا عَنِ الْعَمَلِ.", hint: "Jawab dengan kalimat terhubung memakai: بَعْدَ ذَلِكَ، أُعْطِي تَحْدِيثًا عَنِ الْعَمَلِ.", sampleAnswer: "بَعْدَ ذَلِكَ، أُعْطِي تَحْدِيثًا عَنِ الْعَمَلِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["بَعْدَ", "ذَلِكَ،", "أُعْطِي", "تَحْدِيثًا"], indonesianExplanation: "Setelah itu, saya memberi update tentang pekerjaan." },
    { coach: "استخدم الفكرة: أَحْتَاجُ إِلَى تَوْضِيحٍ فِي نُقْطَةٍ وَاحِدَةٍ.", hint: "Jawab dengan kalimat terhubung memakai: أَحْتَاجُ إِلَى تَوْضِيحٍ فِي نُقْطَةٍ وَاحِدَةٍ.", sampleAnswer: "أَحْتَاجُ إِلَى تَوْضِيحٍ فِي نُقْطَةٍ وَاحِدَةٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَحْتَاجُ", "إِلَى", "تَوْضِيحٍ", "فِي"], indonesianExplanation: "Saya butuh klarifikasi pada satu poin." },
  ],
  "arabic-b1-setting-the-scene": [
    { coach: "كَيْفَ تَبْدَأُ قِصَّةً شَخْصِيَّةً؟", hint: "Jawab dengan kalimat terhubung memakai: فِي الْأُسْبُوعِ الْمَاضِي، كُنْتُ فِي الْمَكْتَبَةِ.", sampleAnswer: "فِي الْأُسْبُوعِ الْمَاضِي، كُنْتُ فِي الْمَكْتَبَةِ.", focus: "Membuka cerita dengan waktu dan tempat.", expectedKeywords: ["فِي", "الْأُسْبُوعِ", "الْمَاضِي،", "كُنْتُ"], indonesianExplanation: "Minggu lalu, saya berada di perpustakaan." },
    { coach: "استخدم الفكرة: كُنْتُ مَعَ صَدِيقِي فِي ذَلِكَ الْوَقْتِ.", hint: "Jawab dengan kalimat terhubung memakai: كُنْتُ مَعَ صَدِيقِي فِي ذَلِكَ الْوَقْتِ.", sampleAnswer: "كُنْتُ مَعَ صَدِيقِي فِي ذَلِكَ الْوَقْتِ.", focus: "Menyebut siapa yang ikut.", expectedKeywords: ["كُنْتُ", "مَعَ", "صَدِيقِي", "فِي"], indonesianExplanation: "Saya bersama teman saya pada waktu itu." },
    { coach: "استخدم الفكرة: كَانَ الْمَكَانُ هَادِئًا وَمُنَاسِبًا.", hint: "Jawab dengan kalimat terhubung memakai: كَانَ الْمَكَانُ هَادِئًا وَمُنَاسِبًا.", sampleAnswer: "كَانَ الْمَكَانُ هَادِئًا وَمُنَاسِبًا.", focus: "Memberi suasana cerita.", expectedKeywords: ["كَانَ", "الْمَكَانُ", "هَادِئًا", "وَمُنَاسِبًا"], indonesianExplanation: "Tempatnya tenang dan cocok." },
  ],
  "arabic-b1-suggesting-a-solution": [
    { coach: "مَا أَوَّلُ تَفْصِيلٍ يَحْتَاجُ إِلَى شَرْحٍ؟", hint: "Jawab dengan kalimat terhubung memakai: أَقْتَرِحُ أَنْ نُجَرِّبَ حَلًّا بَسِيطًا.", sampleAnswer: "أَقْتَرِحُ أَنْ نُجَرِّبَ حَلًّا بَسِيطًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أَقْتَرِحُ", "أَنْ", "نُجَرِّبَ", "حَلًّا"], indonesianExplanation: "Saya menyarankan kita mencoba solusi sederhana." },
    { coach: "استخدم الفكرة: يُمْكِنُنَا أَنْ نُغَيِّرَ الْخُطَّةَ قَلِيلًا.", hint: "Jawab dengan kalimat terhubung memakai: يُمْكِنُنَا أَنْ نُغَيِّرَ الْخُطَّةَ قَلِيلًا.", sampleAnswer: "يُمْكِنُنَا أَنْ نُغَيِّرَ الْخُطَّةَ قَلِيلًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["يُمْكِنُنَا", "أَنْ", "نُغَيِّرَ", "الْخُطَّةَ"], indonesianExplanation: "Kita bisa mengubah rencana sedikit." },
    { coach: "استخدم الفكرة: هَذَا الْحَلُّ أَسْرَعُ مِنَ الْخِيَارِ الْآخَرِ.", hint: "Jawab dengan kalimat terhubung memakai: هَذَا الْحَلُّ أَسْرَعُ مِنَ الْخِيَارِ الْآخَرِ.", sampleAnswer: "هَذَا الْحَلُّ أَسْرَعُ مِنَ الْخِيَارِ الْآخَرِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَذَا", "الْحَلُّ", "أَسْرَعُ", "مِنَ"], indonesianExplanation: "Solusi ini lebih cepat dari pilihan lain." },
  ],
  "arabic-b1-talking-about-goals": [
    { coach: "مَا الْفِكْرَةُ الرَّئِيسِيَّةُ الَّتِي تُرِيدُ بَدْءَ الْحِوَارِ بِهَا؟", hint: "Jawab dengan kalimat terhubung memakai: هَدَفِي هُوَ تَحْسِينُ الْمُحَادَثَةِ.", sampleAnswer: "هَدَفِي هُوَ تَحْسِينُ الْمُحَادَثَةِ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَدَفِي", "هُوَ", "تَحْسِينُ", "الْمُحَادَثَةِ"], indonesianExplanation: "Tujuan saya adalah memperbaiki percakapan." },
    { coach: "استخدم الفكرة: أُرِيدُ أَنْ أَتَكَلَّمَ بِثِقَةٍ أَكْبَرَ.", hint: "Jawab dengan kalimat terhubung memakai: أُرِيدُ أَنْ أَتَكَلَّمَ بِثِقَةٍ أَكْبَرَ.", sampleAnswer: "أُرِيدُ أَنْ أَتَكَلَّمَ بِثِقَةٍ أَكْبَرَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أَتَكَلَّمَ", "بِثِقَةٍ"], indonesianExplanation: "Saya ingin berbicara dengan lebih percaya diri." },
    { coach: "استخدم الفكرة: لِذَلِكَ أَتَدَرَّبُ كُلَّ يَوْمٍ.", hint: "Jawab dengan kalimat terhubung memakai: لِذَلِكَ أَتَدَرَّبُ كُلَّ يَوْمٍ.", sampleAnswer: "لِذَلِكَ أَتَدَرَّبُ كُلَّ يَوْمٍ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["لِذَلِكَ", "أَتَدَرَّبُ", "كُلَّ", "يَوْمٍ"], indonesianExplanation: "Karena itu saya berlatih setiap hari." },
  ],
  "arabic-b1-talking-about-local-habits": [
    { coach: "مَا أَوَّلُ تَفْصِيلٍ يَحْتَاجُ إِلَى شَرْحٍ؟", hint: "Jawab dengan kalimat terhubung memakai: مِنَ الْعَادَةِ أَنْ نُحَيِّيَ الْجِيرَانَ.", sampleAnswer: "مِنَ الْعَادَةِ أَنْ نُحَيِّيَ الْجِيرَانَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["مِنَ", "الْعَادَةِ", "أَنْ", "نُحَيِّيَ"], indonesianExplanation: "Biasanya kami menyapa tetangga." },
    { coach: "استخدم الفكرة: فِي الصَّبَاحِ، يَكُونُ الشَّارِعُ نَشِيطًا.", hint: "Jawab dengan kalimat terhubung memakai: فِي الصَّبَاحِ، يَكُونُ الشَّارِعُ نَشِيطًا.", sampleAnswer: "فِي الصَّبَاحِ، يَكُونُ الشَّارِعُ نَشِيطًا.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["فِي", "الصَّبَاحِ،", "يَكُونُ", "الشَّارِعُ"], indonesianExplanation: "Pada pagi hari, jalan menjadi aktif." },
    { coach: "استخدم الفكرة: بَعْضُ النَّاسِ يَفْضِّلُونَ الْهُدُوءَ.", hint: "Jawab dengan kalimat terhubung memakai: بَعْضُ النَّاسِ يَفْضِّلُونَ الْهُدُوءَ.", sampleAnswer: "بَعْضُ النَّاسِ يَفْضِّلُونَ الْهُدُوءَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["بَعْضُ", "النَّاسِ", "يَفْضِّلُونَ", "الْهُدُوءَ"], indonesianExplanation: "Sebagian orang lebih suka ketenangan." },
  ],
  "arabic-b1-telling-events-in-order": [
    { coach: "مَاذَا حَدَثَ بَعْدَ ذَلِكَ؟", hint: "Jawab dengan kalimat terhubung memakai: أَوَّلًا، وَصَلْتُ إِلَى الْمَكَانِ مُبَكِّرًا.", sampleAnswer: "أَوَّلًا، وَصَلْتُ إِلَى الْمَكَانِ مُبَكِّرًا.", focus: "Memulai urutan kejadian.", expectedKeywords: ["أَوَّلًا،", "وَصَلْتُ", "إِلَى", "الْمَكَانِ"], indonesianExplanation: "Pertama, saya tiba di tempat itu lebih awal." },
    { coach: "استخدم الفكرة: ثُمَّ انْتَظَرْتُ صَدِيقِي قَلِيلًا.", hint: "Jawab dengan kalimat terhubung memakai: ثُمَّ انْتَظَرْتُ صَدِيقِي قَلِيلًا.", sampleAnswer: "ثُمَّ انْتَظَرْتُ صَدِيقِي قَلِيلًا.", focus: "Menyebut kejadian berikutnya.", expectedKeywords: ["ثُمَّ", "انْتَظَرْتُ", "صَدِيقِي", "قَلِيلًا"], indonesianExplanation: "Lalu saya menunggu teman saya sebentar." },
    { coach: "استخدم الفكرة: بَعْدَ ذَلِكَ، تَحَدَّثْنَا عَنِ الْخُطَّةِ.", hint: "Jawab dengan kalimat terhubung memakai: بَعْدَ ذَلِكَ، تَحَدَّثْنَا عَنِ الْخُطَّةِ.", sampleAnswer: "بَعْدَ ذَلِكَ، تَحَدَّثْنَا عَنِ الْخُطَّةِ.", focus: "Menyambung urutan.", expectedKeywords: ["بَعْدَ", "ذَلِكَ،", "تَحَدَّثْنَا", "عَنِ"], indonesianExplanation: "Setelah itu, kami berbicara tentang rencana." },
  ],
  "arabic-b1-travel-situation-mission": [
    { coach: "كَيْفَ تُنْهِي الْحِوَارَ بِخُطْوَةٍ تَالِيَةٍ؟", hint: "Jawab dengan kalimat terhubung memakai: عِنْدِي حَجْزٌ وَلَكِنَّنِي تَأَخَّرْتُ.", sampleAnswer: "عِنْدِي حَجْزٌ وَلَكِنَّنِي تَأَخَّرْتُ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["عِنْدِي", "حَجْزٌ", "وَلَكِنَّنِي", "تَأَخَّرْتُ"], indonesianExplanation: "Saya punya reservasi tetapi terlambat." },
    { coach: "استخدم الفكرة: أُرِيدُ أَنْ أُؤَكِّدَ الْوُصُولَ.", hint: "Jawab dengan kalimat terhubung memakai: أُرِيدُ أَنْ أُؤَكِّدَ الْوُصُولَ.", sampleAnswer: "أُرِيدُ أَنْ أُؤَكِّدَ الْوُصُولَ.", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أُؤَكِّدَ", "الْوُصُولَ"], indonesianExplanation: "Saya ingin mengonfirmasi kedatangan." },
    { coach: "استخدم الفكرة: هَلْ تُوصِي بِمَكَانٍ قَرِيبٍ لِلطَّعَامِ؟", hint: "Jawab dengan kalimat terhubung memakai: هَلْ تُوصِي بِمَكَانٍ قَرِيبٍ لِلطَّعَامِ؟", sampleAnswer: "هَلْ تُوصِي بِمَكَانٍ قَرِيبٍ لِلطَّعَامِ؟", focus: "Gunakan untuk percakapan B1 yang lebih terhubung.", expectedKeywords: ["هَلْ", "تُوصِي", "بِمَكَانٍ", "قَرِيبٍ"], indonesianExplanation: "Apakah kamu merekomendasikan tempat makan dekat?" },
  ],
  "arabic-b1-workplace-mission": [
    { coach: "أَعْطِينِي تَحْدِيثًا عَنِ الْعَمَلِ.", hint: "Jawab dengan kalimat terhubung memakai: أَعْمَلُ عَلَى تَنْظِيمِ الْمَلَفَّاتِ.", sampleAnswer: "أَعْمَلُ عَلَى تَنْظِيمِ الْمَلَفَّاتِ.", focus: "Menjelaskan tugas.", expectedKeywords: ["أَعْمَلُ", "عَلَى", "تَنْظِيمِ", "الْمَلَفَّاتِ"], indonesianExplanation: "Saya mengerjakan pengaturan file." },
    { coach: "استخدم الفكرة: هَلْ تَقْصِدِينَ الْمَلَفَّاتِ الْجَدِيدَةَ فَقَطْ؟", hint: "Jawab dengan kalimat terhubung memakai: هَلْ تَقْصِدِينَ الْمَلَفَّاتِ الْجَدِيدَةَ فَقَطْ؟", sampleAnswer: "هَلْ تَقْصِدِينَ الْمَلَفَّاتِ الْجَدِيدَةَ فَقَطْ؟", focus: "Meminta klarifikasi.", expectedKeywords: ["هَلْ", "تَقْصِدِينَ", "الْمَلَفَّاتِ", "الْجَدِيدَةَ"], indonesianExplanation: "Apakah maksudmu hanya file baru?" },
    { coach: "استخدم الفكرة: أَنْجَزْتُ نِصْفَ الْعَمَلِ حَتَّى الْآنَ.", hint: "Jawab dengan kalimat terhubung memakai: أَنْجَزْتُ نِصْفَ الْعَمَلِ حَتَّى الْآنَ.", sampleAnswer: "أَنْجَزْتُ نِصْفَ الْعَمَلِ حَتَّى الْآنَ.", focus: "Memberi progress.", expectedKeywords: ["أَنْجَزْتُ", "نِصْفَ", "الْعَمَلِ", "حَتَّى"], indonesianExplanation: "Saya sudah menyelesaikan setengah pekerjaan sampai sekarang." },
  ],
  "arabic-b2-answering-questions": [
    { coach: "كَيْفَ سَتُقَدِّمِينَ هَذِهِ الْفِكْرَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى الْإِجَابَةُ عَنِ الْأَسْئِلَةِ.", hint: "Jawab dengan struktur B2 memakai: سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ الْإِجَابَةُ عَنِ الْأَسْئِلَةِ.", sampleAnswer: "سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ الْإِجَابَةُ عَنِ الْأَسْئِلَةِ.", focus: "Membuka presentasi.", expectedKeywords: ["سَأَبْدَأُ", "بِمُقَدِّمَةٍ", "قَصِيرَةٍ", "عَنْ", "الْإِجَابَةُ"], indonesianExplanation: "Saya akan mulai dengan pembuka singkat tentang menjawab pertanyaan." },
    { coach: "استخدم الفكرة: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", sampleAnswer: "بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", focus: "Memberi signposting.", expectedKeywords: ["بَعْدَ", "ذَلِكَ،", "سَأَشْرَحُ", "الْفَائِدَةَ", "الْأَسَاسِيَّةَ"], indonesianExplanation: "Setelah itu, saya akan menjelaskan manfaat utamanya." },
    { coach: "استخدم الفكرة: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", hint: "Jawab dengan struktur B2 memakai: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", sampleAnswer: "مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", focus: "Menjelaskan risk secara seimbang.", expectedKeywords: ["مِنَ", "الْمُهِمِّ", "أَنْ", "نَذْكُرَ", "الْمَخَاطِرَ"], indonesianExplanation: "Penting juga untuk menyebutkan risikonya." },
    { coach: "استخدم الفكرة: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", sampleAnswer: "إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", focus: "Menyiapkan Q&A.", expectedKeywords: ["إِذَا", "كَانَتْ", "هُنَاكَ", "أَسْئِلَةٌ،", "فَسَأُجِيبُ"], indonesianExplanation: "Jika ada pertanyaan, saya akan menjawabnya dengan jelas." },
  ],
  "arabic-b2-b2-final-discussion": [
    { coach: "مَا أَهَمُّ مَهَارَةٍ تُرَاجِعِينَها الْآنَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى النِّقَاشِ النِّهَائِيِّ.", hint: "Jawab dengan struktur B2 memakai: أُرَاجِعُ النِّقَاشَ النِّهَائِيَّ لِأَنَّهُ يَجْمَعُ مَهَارَاتِ الْمُسْتَوَى.", sampleAnswer: "أُرَاجِعُ النِّقَاشَ النِّهَائِيَّ لِأَنَّهُ يَجْمَعُ مَهَارَاتِ الْمُسْتَوَى.", focus: "Membuka review.", expectedKeywords: ["أُرَاجِعُ", "النِّقَاشَ", "النِّهَائِيَّ", "لِأَنَّهُ", "يَجْمَعُ"], indonesianExplanation: "Saya mereview diskusi akhir karena itu menggabungkan keterampilan level ini." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", sampleAnswer: "أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", focus: "Mereview kemampuan menyusun argumen.", expectedKeywords: ["أَسْتَطِيعُ", "أَنْ", "أُقَدِّمَ", "رَأْيًا", "وَأَدْعَمَهُ"], indonesianExplanation: "Saya bisa menyampaikan pendapat dan mendukungnya dengan bukti." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", sampleAnswer: "أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", focus: "Mereview kemampuan percakapan profesional.", expectedKeywords: ["أَسْتَطِيعُ", "أَيْضًا", "أَنْ", "أُدِيرَ", "حِوَارًا"], indonesianExplanation: "Saya juga bisa mengelola percakapan profesional dengan jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", sampleAnswer: "إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", focus: "Mereview respons terhadap keberatan.", expectedKeywords: ["إِذَا", "ظَهَرَ", "اِعْتِرَاضٌ،", "فَسَأَرُدُّ", "عَلَيْهِ"], indonesianExplanation: "Jika muncul keberatan, saya akan menanggapinya dengan tenang." },
  ],
  "arabic-b2-b2-final-test-practice": [
    { coach: "مَا أَهَمُّ مَهَارَةٍ تُرَاجِعِينَها الْآنَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَدْرِيبِ الِاخْتِبَارِ النِّهَائِيِّ.", hint: "Jawab dengan struktur B2 memakai: أُرَاجِعُ تَدْرِيبَ الِاخْتِبَارِ النِّهَائِيِّ لِأَنَّهُ يُسَاعِدُنِي عَلَى الِاسْتِعْدَادِ.", sampleAnswer: "أُرَاجِعُ تَدْرِيبَ الِاخْتِبَارِ النِّهَائِيِّ لِأَنَّهُ يُسَاعِدُنِي عَلَى الِاسْتِعْدَادِ.", focus: "Membuka review.", expectedKeywords: ["أُرَاجِعُ", "تَدْرِيبَ", "الِاخْتِبَارِ", "النِّهَائِيِّ", "لِأَنَّهُ"], indonesianExplanation: "Saya mereview latihan tes akhir karena itu membantu saya bersiap." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", sampleAnswer: "أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", focus: "Mereview kemampuan menyusun argumen.", expectedKeywords: ["أَسْتَطِيعُ", "أَنْ", "أُقَدِّمَ", "رَأْيًا", "وَأَدْعَمَهُ"], indonesianExplanation: "Saya bisa menyampaikan pendapat dan mendukungnya dengan bukti." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", sampleAnswer: "أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", focus: "Mereview kemampuan percakapan profesional.", expectedKeywords: ["أَسْتَطِيعُ", "أَيْضًا", "أَنْ", "أُدِيرَ", "حِوَارًا"], indonesianExplanation: "Saya juga bisa mengelola percakapan profesional dengan jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", sampleAnswer: "إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", focus: "Mereview respons terhadap keberatan.", expectedKeywords: ["إِذَا", "ظَهَرَ", "اِعْتِرَاضٌ،", "فَسَأَرُدُّ", "عَلَيْهِ"], indonesianExplanation: "Jika muncul keberatan, saya akan menanggapinya dengan tenang." },
  ],
  "arabic-b2-clarifying-scope": [
    { coach: "قَبْلَ أَنْ نُكْمِلَ، هَلِ النِّطَاقُ وَاضِحٌ؟", hint: "Jawab dengan struktur B2 memakai: لَيْسَ النِّطَاقُ وَاضِحًا تَمَامًا.", sampleAnswer: "لَيْسَ النِّطَاقُ وَاضِحًا تَمَامًا.", focus: "Membuka klarifikasi scope.", expectedKeywords: ["لَيْسَ", "النِّطَاقُ", "وَاضِحًا", "تَمَامًا"], indonesianExplanation: "Cakupannya belum sepenuhnya jelas." },
    { coach: "استخدم الفكرة: نُدْخِلُ الصَّفْحَةَ الرَّئِيسِيَّةَ وَنُؤَجِّلُ التَّقَارِيرَ.", hint: "Jawab dengan struktur B2 memakai: نُدْخِلُ الصَّفْحَةَ الرَّئِيسِيَّةَ وَنُؤَجِّلُ التَّقَارِيرَ.", sampleAnswer: "نُدْخِلُ الصَّفْحَةَ الرَّئِيسِيَّةَ وَنُؤَجِّلُ التَّقَارِيرَ.", focus: "Membatasi scope.", expectedKeywords: ["نُدْخِلُ", "الصَّفْحَةَ", "الرَّئِيسِيَّةَ", "وَنُؤَجِّلُ", "التَّقَارِيرَ"], indonesianExplanation: "Kita memasukkan halaman utama dan menunda laporan." },
    { coach: "استخدم الفكرة: هَذَا يُبْقِي الْمَوْعِدَ وَاقِعِيًّا وَيُقَلِّلُ الْمَخَاطِرَ.", hint: "Jawab dengan struktur B2 memakai: هَذَا يُبْقِي الْمَوْعِدَ وَاقِعِيًّا وَيُقَلِّلُ الْمَخَاطِرَ.", sampleAnswer: "هَذَا يُبْقِي الْمَوْعِدَ وَاقِعِيًّا وَيُقَلِّلُ الْمَخَاطِرَ.", focus: "Memberi alasan batasan.", expectedKeywords: ["هَذَا", "يُبْقِي", "الْمَوْعِدَ", "وَاقِعِيًّا", "وَيُقَلِّلُ"], indonesianExplanation: "Ini membuat tenggat tetap realistis dan mengurangi risiko." },
    { coach: "استخدم الفكرة: سَأُؤَكِّدُ ذَلِكَ فِي رِسَالَةٍ قَصِيرَةٍ بَعْدَ الِاجْتِمَاعِ.", hint: "Jawab dengan struktur B2 memakai: سَأُؤَكِّدُ ذَلِكَ فِي رِسَالَةٍ قَصِيرَةٍ بَعْدَ الِاجْتِمَاعِ.", sampleAnswer: "سَأُؤَكِّدُ ذَلِكَ فِي رِسَالَةٍ قَصِيرَةٍ بَعْدَ الِاجْتِمَاعِ.", focus: "Mengonfirmasi follow-up.", expectedKeywords: ["سَأُؤَكِّدُ", "ذَلِكَ", "فِي", "رِسَالَةٍ", "قَصِيرَةٍ"], indonesianExplanation: "Saya akan mengonfirmasi itu dalam pesan singkat setelah rapat." },
  ],
  "arabic-b2-clear-argument-mission": [
    { coach: "مَا مَوْقِفُكَ مِنْ هَذَا الْمَوْضُوعِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى بِنَاءُ حُجَّةٍ وَاضِحَةٍ.", hint: "Jawab dengan struktur B2 memakai: مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", sampleAnswer: "مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", focus: "Menyatakan posisi dengan jelas.", expectedKeywords: ["مَوْقِفِي", "هُوَ", "أَنَّ", "هَذَا", "الْمَوْضُوعَ"], indonesianExplanation: "Posisi saya adalah bahwa topik membangun argumen jelas penting dalam diskusi." },
    { coach: "استخدم الفكرة: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", hint: "Jawab dengan struktur B2 memakai: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", sampleAnswer: "أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", focus: "Memberi kerangka argumen.", expectedKeywords: ["أَدْعَمُ", "هَذَا", "الرَّأْيَ", "بِسَبَبَيْنِ", "وَاضِحَيْنِ"], indonesianExplanation: "Saya mendukung pendapat ini dengan dua alasan yang jelas." },
    { coach: "استخدم الفكرة: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", hint: "Jawab dengan struktur B2 memakai: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", sampleAnswer: "مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", focus: "Memberi contoh konkret.", expectedKeywords: ["مِثَالُ", "ذَلِكَ", "أَنَّ", "الْفَرِيقَ", "يَحْتَاجُ"], indonesianExplanation: "Contohnya, tim membutuhkan keputusan yang cepat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", sampleAnswer: "أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", focus: "Merespons counterpoint dengan sopan.", expectedKeywords: ["أَفْهَمُ", "هَذِهِ", "النُّقْطَةَ", "الْمُعَارِضَةَ،", "وَلَكِنَّ"], indonesianExplanation: "Saya memahami poin lawannya, tetapi manfaatnya lebih besar." },
  ],
  "arabic-b2-client-conversation-mission": [
    { coach: "مَا الَّذِي يَحْتَاجُ إِلَيْهِ الْعَمِيلُ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى إِدَارَةُ حِوَارٍ مَعَ عَمِيلٍ.", hint: "Jawab dengan struktur B2 memakai: أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ إِدَارَةُ حِوَارٍ مَعَ عَمِيلٍ.", sampleAnswer: "أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ إِدَارَةُ حِوَارٍ مَعَ عَمِيلٍ.", focus: "Memahami kebutuhan klien.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أَفْهَمَ", "اِحْتِيَاجَ", "الْعَمِيلِ"], indonesianExplanation: "Saya ingin memahami kebutuhan klien tentang mengelola percakapan dengan klien." },
    { coach: "استخدم الفكرة: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", hint: "Jawab dengan struktur B2 memakai: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", sampleAnswer: "لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", focus: "Menjelaskan opsi.", expectedKeywords: ["لَدَيْنَا", "خِيَارَانِ،", "وَكُلُّ", "خِيَارٍ", "لَهُ"], indonesianExplanation: "Kita punya dua opsi, dan setiap opsi memiliki manfaat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", sampleAnswer: "أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", focus: "Menangani concern.", expectedKeywords: ["أَفْهَمُ", "هَذَا", "الِاهْتِمَامَ،", "وَسَأُوَضِّحُ", "التَّفَاصِيلَ"], indonesianExplanation: "Saya memahami kekhawatiran ini, dan saya akan menjelaskan detailnya." },
    { coach: "استخدم الفكرة: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", hint: "Jawab dengan struktur B2 memakai: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", sampleAnswer: "الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", focus: "Mengonfirmasi next step.", expectedKeywords: ["الْخُطْوَةُ", "التَّالِيَةُ", "هِيَ", "مُرَاجَعَةُ", "الِاتِّفَاقِ"], indonesianExplanation: "Langkah berikutnya adalah meninjau kesepakatan." },
  ],
  "arabic-b2-confirming-next-steps": [
    { coach: "مَا الَّذِي يَحْتَاجُ إِلَيْهِ الْعَمِيلُ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَأْكِيدُ الْخُطْوَاتِ التَّالِيَةِ.", hint: "Jawab dengan struktur B2 memakai: أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ تَأْكِيدُ الْخُطْوَاتِ التَّالِيَةِ.", sampleAnswer: "أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ تَأْكِيدُ الْخُطْوَاتِ التَّالِيَةِ.", focus: "Memahami kebutuhan klien.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أَفْهَمَ", "اِحْتِيَاجَ", "الْعَمِيلِ"], indonesianExplanation: "Saya ingin memahami kebutuhan klien tentang mengonfirmasi langkah berikutnya." },
    { coach: "استخدم الفكرة: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", hint: "Jawab dengan struktur B2 memakai: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", sampleAnswer: "لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", focus: "Menjelaskan opsi.", expectedKeywords: ["لَدَيْنَا", "خِيَارَانِ،", "وَكُلُّ", "خِيَارٍ", "لَهُ"], indonesianExplanation: "Kita punya dua opsi, dan setiap opsi memiliki manfaat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", sampleAnswer: "أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", focus: "Menangani concern.", expectedKeywords: ["أَفْهَمُ", "هَذَا", "الِاهْتِمَامَ،", "وَسَأُوَضِّحُ", "التَّفَاصِيلَ"], indonesianExplanation: "Saya memahami kekhawatiran ini, dan saya akan menjelaskan detailnya." },
    { coach: "استخدم الفكرة: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", hint: "Jawab dengan struktur B2 memakai: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", sampleAnswer: "الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", focus: "Mengonfirmasi next step.", expectedKeywords: ["الْخُطْوَةُ", "التَّالِيَةُ", "هِيَ", "مُرَاجَعَةُ", "الِاتِّفَاقِ"], indonesianExplanation: "Langkah berikutnya adalah meninjau kesepakatan." },
  ],
  "arabic-b2-discussing-reliable-sources": [
    { coach: "كَيْفَ تُلَخِّصُ هَذِهِ الْمَعْلُومَاتِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى مُنَاقَشَةُ الْمَصَادِرِ الْمَوْثُوقَةِ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", focus: "Merangkum artikel.", expectedKeywords: ["أَفْهَمُ", "مِنَ", "الْمَقَالِ", "أَنَّ", "هَذَا"], indonesianExplanation: "Saya memahami dari artikel bahwa topik membahas sumber tepercaya penting." },
    { coach: "استخدم الفكرة: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", hint: "Jawab dengan struktur B2 memakai: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", sampleAnswer: "يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", focus: "Mengevaluasi sumber.", expectedKeywords: ["يَجِبُ", "أَنْ", "نَتَأَكَّدَ", "مِنْ", "أَنَّ"], indonesianExplanation: "Kita harus memastikan bahwa sumbernya tepercaya." },
    { coach: "استخدم الفكرة: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", hint: "Jawab dengan struktur B2 memakai: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", sampleAnswer: "وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", focus: "Menguji viewpoint.", expectedKeywords: ["وِجْهَةُ", "النَّظَرِ", "هَذِهِ", "تَحْتَاجُ", "إِلَى"], indonesianExplanation: "Sudut pandang ini membutuhkan bukti yang lebih kuat." },
    { coach: "استخدم الفكرة: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", sampleAnswer: "بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", focus: "Merespons informasi baru.", expectedKeywords: ["بَعْدَ", "الْمَعْلُومَاتِ", "الْجَدِيدَةِ،", "تَغَيَّرَ", "رَأْيِي"], indonesianExplanation: "Setelah informasi baru, pendapat saya sedikit berubah." },
  ],
  "arabic-b2-discussing-tradeoffs": [
    { coach: "كَيْفَ نُحَدِّدُ هَذِهِ الْمُشْكِلَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى مُنَاقَشَةُ الْمُوَازَنَاتِ.", hint: "Jawab dengan struktur B2 memakai: أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", sampleAnswer: "أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", focus: "Melakukan framing problem.", expectedKeywords: ["أَرَى", "أَنَّ", "هَذِهِ", "النُّقْطَةَ", "جُزْءٌ"], indonesianExplanation: "Saya melihat bahwa poin membahas tradeoff adalah bagian dari masalah yang lebih besar." },
    { coach: "استخدم الفكرة: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", hint: "Jawab dengan struktur B2 memakai: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", sampleAnswer: "السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", focus: "Menjelaskan cause.", expectedKeywords: ["السَّبَبُ", "الْأَسَاسِيُّ", "قَدْ", "يَكُونُ", "ضَعْفَ"], indonesianExplanation: "Penyebab utamanya mungkin lemahnya pengaturan." },
    { coach: "استخدم الفكرة: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", hint: "Jawab dengan struktur B2 memakai: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", sampleAnswer: "لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", focus: "Membahas tradeoff.", expectedKeywords: ["لِكُلِّ", "حَلٍّ", "فَائِدَةٌ", "وَتَأْثِيرٌ", "جَانِبِيٌّ"], indonesianExplanation: "Setiap solusi punya manfaat dan efek samping." },
    { coach: "استخدم الفكرة: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", hint: "Jawab dengan struktur B2 memakai: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", sampleAnswer: "أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", focus: "Memberi rekomendasi.", expectedKeywords: ["أُوصِي", "بِحَلٍّ", "تَدْرِيجِيٍّ", "لِتَقْلِيلِ", "الْمَخَاطِرِ"], indonesianExplanation: "Saya merekomendasikan solusi bertahap untuk mengurangi risiko." },
  ],
  "arabic-b2-explaining-a-viewpoint": [
    { coach: "كَيْفَ تُلَخِّصُ هَذِهِ الْمَعْلُومَاتِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى شَرْحُ وِجْهَةِ نَظَرٍ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", focus: "Merangkum artikel.", expectedKeywords: ["أَفْهَمُ", "مِنَ", "الْمَقَالِ", "أَنَّ", "هَذَا"], indonesianExplanation: "Saya memahami dari artikel bahwa topik menjelaskan sudut pandang penting." },
    { coach: "استخدم الفكرة: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", hint: "Jawab dengan struktur B2 memakai: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", sampleAnswer: "يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", focus: "Mengevaluasi sumber.", expectedKeywords: ["يَجِبُ", "أَنْ", "نَتَأَكَّدَ", "مِنْ", "أَنَّ"], indonesianExplanation: "Kita harus memastikan bahwa sumbernya tepercaya." },
    { coach: "استخدم الفكرة: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", hint: "Jawab dengan struktur B2 memakai: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", sampleAnswer: "وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", focus: "Menguji viewpoint.", expectedKeywords: ["وِجْهَةُ", "النَّظَرِ", "هَذِهِ", "تَحْتَاجُ", "إِلَى"], indonesianExplanation: "Sudut pandang ini membutuhkan bukti yang lebih kuat." },
    { coach: "استخدم الفكرة: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", sampleAnswer: "بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", focus: "Merespons informasi baru.", expectedKeywords: ["بَعْدَ", "الْمَعْلُومَاتِ", "الْجَدِيدَةِ،", "تَغَيَّرَ", "رَأْيِي"], indonesianExplanation: "Setelah informasi baru, pendapat saya sedikit berubah." },
  ],
  "arabic-b2-explaining-benefits-and-risks": [
    { coach: "كَيْفَ سَتُقَدِّمِينَ هَذِهِ الْفِكْرَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى شَرْحُ الْفَوَائِدِ وَالْمَخَاطِرِ.", hint: "Jawab dengan struktur B2 memakai: سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ شَرْحُ الْفَوَائِدِ وَالْمَخَاطِرِ.", sampleAnswer: "سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ شَرْحُ الْفَوَائِدِ وَالْمَخَاطِرِ.", focus: "Membuka presentasi.", expectedKeywords: ["سَأَبْدَأُ", "بِمُقَدِّمَةٍ", "قَصِيرَةٍ", "عَنْ", "شَرْحُ"], indonesianExplanation: "Saya akan mulai dengan pembuka singkat tentang menjelaskan manfaat dan risiko." },
    { coach: "استخدم الفكرة: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", sampleAnswer: "بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", focus: "Memberi signposting.", expectedKeywords: ["بَعْدَ", "ذَلِكَ،", "سَأَشْرَحُ", "الْفَائِدَةَ", "الْأَسَاسِيَّةَ"], indonesianExplanation: "Setelah itu, saya akan menjelaskan manfaat utamanya." },
    { coach: "استخدم الفكرة: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", hint: "Jawab dengan struktur B2 memakai: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", sampleAnswer: "مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", focus: "Menjelaskan risk secara seimbang.", expectedKeywords: ["مِنَ", "الْمُهِمِّ", "أَنْ", "نَذْكُرَ", "الْمَخَاطِرَ"], indonesianExplanation: "Penting juga untuk menyebutkan risikonya." },
    { coach: "استخدم الفكرة: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", sampleAnswer: "إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", focus: "Menyiapkan Q&A.", expectedKeywords: ["إِذَا", "كَانَتْ", "هُنَاكَ", "أَسْئِلَةٌ،", "فَسَأُجِيبُ"], indonesianExplanation: "Jika ada pertanyaan, saya akan menjawabnya dengan jelas." },
  ],
  "arabic-b2-explaining-causes": [
    { coach: "كَيْفَ نُحَدِّدُ هَذِهِ الْمُشْكِلَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى شَرْحُ الْأَسْبَابِ.", hint: "Jawab dengan struktur B2 memakai: أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", sampleAnswer: "أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", focus: "Melakukan framing problem.", expectedKeywords: ["أَرَى", "أَنَّ", "هَذِهِ", "النُّقْطَةَ", "جُزْءٌ"], indonesianExplanation: "Saya melihat bahwa poin menjelaskan penyebab adalah bagian dari masalah yang lebih besar." },
    { coach: "استخدم الفكرة: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", hint: "Jawab dengan struktur B2 memakai: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", sampleAnswer: "السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", focus: "Menjelaskan cause.", expectedKeywords: ["السَّبَبُ", "الْأَسَاسِيُّ", "قَدْ", "يَكُونُ", "ضَعْفَ"], indonesianExplanation: "Penyebab utamanya mungkin lemahnya pengaturan." },
    { coach: "استخدم الفكرة: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", hint: "Jawab dengan struktur B2 memakai: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", sampleAnswer: "لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", focus: "Membahas tradeoff.", expectedKeywords: ["لِكُلِّ", "حَلٍّ", "فَائِدَةٌ", "وَتَأْثِيرٌ", "جَانِبِيٌّ"], indonesianExplanation: "Setiap solusi punya manfaat dan efek samping." },
    { coach: "استخدم الفكرة: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", hint: "Jawab dengan struktur B2 memakai: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", sampleAnswer: "أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", focus: "Memberi rekomendasi.", expectedKeywords: ["أُوصِي", "بِحَلٍّ", "تَدْرِيجِيٍّ", "لِتَقْلِيلِ", "الْمَخَاطِرِ"], indonesianExplanation: "Saya merekomendasikan solusi bertahap untuk mengurangi risiko." },
  ],
  "arabic-b2-explaining-options": [
    { coach: "مَا الَّذِي يَحْتَاجُ إِلَيْهِ الْعَمِيلُ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى شَرْحُ الْخِيَارَاتِ.", hint: "Jawab dengan struktur B2 memakai: أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ شَرْحُ الْخِيَارَاتِ.", sampleAnswer: "أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ شَرْحُ الْخِيَارَاتِ.", focus: "Memahami kebutuhan klien.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أَفْهَمَ", "اِحْتِيَاجَ", "الْعَمِيلِ"], indonesianExplanation: "Saya ingin memahami kebutuhan klien tentang menjelaskan opsi." },
    { coach: "استخدم الفكرة: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", hint: "Jawab dengan struktur B2 memakai: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", sampleAnswer: "لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", focus: "Menjelaskan opsi.", expectedKeywords: ["لَدَيْنَا", "خِيَارَانِ،", "وَكُلُّ", "خِيَارٍ", "لَهُ"], indonesianExplanation: "Kita punya dua opsi, dan setiap opsi memiliki manfaat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", sampleAnswer: "أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", focus: "Menangani concern.", expectedKeywords: ["أَفْهَمُ", "هَذَا", "الِاهْتِمَامَ،", "وَسَأُوَضِّحُ", "التَّفَاصِيلَ"], indonesianExplanation: "Saya memahami kekhawatiran ini, dan saya akan menjelaskan detailnya." },
    { coach: "استخدم الفكرة: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", hint: "Jawab dengan struktur B2 memakai: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", sampleAnswer: "الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", focus: "Mengonfirmasi next step.", expectedKeywords: ["الْخُطْوَةُ", "التَّالِيَةُ", "هِيَ", "مُرَاجَعَةُ", "الِاتِّفَاقِ"], indonesianExplanation: "Langkah berikutnya adalah meninjau kesepakatan." },
  ],
  "arabic-b2-expressing-priorities": [
    { coach: "مَا أَوْلَوِيَّتُكَ فِي هَذَا الِاتِّفَاقِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَوْضِيحُ الْأَوْلَوِيَّاتِ.", hint: "Jawab dengan struktur B2 memakai: أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى تَوْضِيحُ الْأَوْلَوِيَّاتِ وَاضِحًا.", sampleAnswer: "أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى تَوْضِيحُ الْأَوْلَوِيَّاتِ وَاضِحًا.", focus: "Menyatakan prioritas.", expectedKeywords: ["أَوْلَوِيَّتِي", "هِيَ", "أَنْ", "يَبْقَى", "تَوْضِيحُ"], indonesianExplanation: "Prioritas saya adalah agar menjelaskan prioritas tetap jelas." },
    { coach: "استخدم الفكرة: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", hint: "Jawab dengan struktur B2 memakai: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", sampleAnswer: "أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", focus: "Membuat proposal.", expectedKeywords: ["أُقَدِّمُ", "الِاقْتِرَاحَ", "التَّالِيَ", "كَحَلٍّ", "عَمَلِيٍّ"], indonesianExplanation: "Saya mengajukan usulan berikut sebagai solusi praktis." },
    { coach: "استخدم الفكرة: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", sampleAnswer: "أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", focus: "Menangani objection.", expectedKeywords: ["أَفْهَمُ", "قَلَقَكَ،", "وَلَكِنْ", "لَدَيْنَا", "خِيَارٌ"], indonesianExplanation: "Saya memahami kekhawatiranmu, tetapi kita punya pilihan lain." },
    { coach: "استخدم الفكرة: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", hint: "Jawab dengan struktur B2 memakai: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", sampleAnswer: "يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", focus: "Mencari kompromi.", expectedKeywords: ["يُمْكِنُنَا", "أَنْ", "نَصِلَ", "إِلَى", "حَلٍّ"], indonesianExplanation: "Kita bisa mencapai solusi tengah." },
  ],
  "arabic-b2-finding-middle-ground": [
    { coach: "مَا أَوْلَوِيَّتُكَ فِي هَذَا الِاتِّفَاقِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى الْوُصُولُ إِلَى حَلٍّ وَسَطٍ.", hint: "Jawab dengan struktur B2 memakai: أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى الْوُصُولُ إِلَى حَلٍّ وَسَطٍ وَاضِحًا.", sampleAnswer: "أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى الْوُصُولُ إِلَى حَلٍّ وَسَطٍ وَاضِحًا.", focus: "Menyatakan prioritas.", expectedKeywords: ["أَوْلَوِيَّتِي", "هِيَ", "أَنْ", "يَبْقَى", "الْوُصُولُ"], indonesianExplanation: "Prioritas saya adalah agar mencari jalan tengah tetap jelas." },
    { coach: "استخدم الفكرة: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", hint: "Jawab dengan struktur B2 memakai: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", sampleAnswer: "أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", focus: "Membuat proposal.", expectedKeywords: ["أُقَدِّمُ", "الِاقْتِرَاحَ", "التَّالِيَ", "كَحَلٍّ", "عَمَلِيٍّ"], indonesianExplanation: "Saya mengajukan usulan berikut sebagai solusi praktis." },
    { coach: "استخدم الفكرة: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", sampleAnswer: "أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", focus: "Menangani objection.", expectedKeywords: ["أَفْهَمُ", "قَلَقَكَ،", "وَلَكِنْ", "لَدَيْنَا", "خِيَارٌ"], indonesianExplanation: "Saya memahami kekhawatiranmu, tetapi kita punya pilihan lain." },
    { coach: "استخدم الفكرة: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", hint: "Jawab dengan struktur B2 memakai: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", sampleAnswer: "يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", focus: "Mencari kompromi.", expectedKeywords: ["يُمْكِنُنَا", "أَنْ", "نَصِلَ", "إِلَى", "حَلٍّ"], indonesianExplanation: "Kita bisa mencapai solusi tengah." },
  ],
  "arabic-b2-framing-the-problem": [
    { coach: "كَيْفَ نُحَدِّدُ هَذِهِ الْمُشْكِلَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَحْدِيدُ إِطَارِ الْمُشْكِلَةِ.", hint: "Jawab dengan struktur B2 memakai: أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", sampleAnswer: "أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", focus: "Melakukan framing problem.", expectedKeywords: ["أَرَى", "أَنَّ", "هَذِهِ", "النُّقْطَةَ", "جُزْءٌ"], indonesianExplanation: "Saya melihat bahwa poin membingkai masalah adalah bagian dari masalah yang lebih besar." },
    { coach: "استخدم الفكرة: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", hint: "Jawab dengan struktur B2 memakai: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", sampleAnswer: "السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", focus: "Menjelaskan cause.", expectedKeywords: ["السَّبَبُ", "الْأَسَاسِيُّ", "قَدْ", "يَكُونُ", "ضَعْفَ"], indonesianExplanation: "Penyebab utamanya mungkin lemahnya pengaturan." },
    { coach: "استخدم الفكرة: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", hint: "Jawab dengan struktur B2 memakai: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", sampleAnswer: "لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", focus: "Membahas tradeoff.", expectedKeywords: ["لِكُلِّ", "حَلٍّ", "فَائِدَةٌ", "وَتَأْثِيرٌ", "جَانِبِيٌّ"], indonesianExplanation: "Setiap solusi punya manfaat dan efek samping." },
    { coach: "استخدم الفكرة: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", hint: "Jawab dengan struktur B2 memakai: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", sampleAnswer: "أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", focus: "Memberi rekomendasi.", expectedKeywords: ["أُوصِي", "بِحَلٍّ", "تَدْرِيجِيٍّ", "لِتَقْلِيلِ", "الْمَخَاطِرِ"], indonesianExplanation: "Saya merekomendasikan solusi bertahap untuk mengurangi risiko." },
  ],
  "arabic-b2-giving-constructive-feedback": [
    { coach: "رَأَيْتُ مُسَوَّدَةَ الِاقْتِرَاحِ. مَا مُلَاحَظَتُكِ الأُولَى؟", hint: "Jawab dengan struktur B2 memakai: الْهَيْكَلُ جَيِّدٌ، وَلَكِنَّ الْمُقَدِّمَةَ تَحْتَاجُ إِلَى هَدَفٍ أَوْضَحَ.", sampleAnswer: "الْهَيْكَلُ جَيِّدٌ، وَلَكِنَّ الْمُقَدِّمَةَ تَحْتَاجُ إِلَى هَدَفٍ أَوْضَحَ.", focus: "Memberi feedback seimbang.", expectedKeywords: ["الْهَيْكَلُ", "جَيِّدٌ،", "وَلَكِنَّ", "الْمُقَدِّمَةَ", "تَحْتَاجُ"], indonesianExplanation: "Strukturnya bagus, tetapi pembuka membutuhkan tujuan yang lebih jelas." },
    { coach: "استخدم الفكرة: الْفِكْرَةُ قَوِيَّةٌ، وَإِضَافَةُ هَدَفٍ وَاحِدٍ سَتَجْعَلُهَا أَقْوَى.", hint: "Jawab dengan struktur B2 memakai: الْفِكْرَةُ قَوِيَّةٌ، وَإِضَافَةُ هَدَفٍ وَاحِدٍ سَتَجْعَلُهَا أَقْوَى.", sampleAnswer: "الْفِكْرَةُ قَوِيَّةٌ، وَإِضَافَةُ هَدَفٍ وَاحِدٍ سَتَجْعَلُهَا أَقْوَى.", focus: "Membuat feedback konstruktif.", expectedKeywords: ["الْفِكْرَةُ", "قَوِيَّةٌ،", "وَإِضَافَةُ", "هَدَفٍ", "وَاحِدٍ"], indonesianExplanation: "Idenya kuat, dan menambahkan satu tujuan akan membuatnya lebih kuat." },
    { coach: "استخدم الفكرة: نَذْكُرُ كَيْفَ سَيَقِيسُ الْعَمِيلُ النَّجَاحَ بَعْدَ شَهْرٍ.", hint: "Jawab dengan struktur B2 memakai: نَذْكُرُ كَيْفَ سَيَقِيسُ الْعَمِيلُ النَّجَاحَ بَعْدَ شَهْرٍ.", sampleAnswer: "نَذْكُرُ كَيْفَ سَيَقِيسُ الْعَمِيلُ النَّجَاحَ بَعْدَ شَهْرٍ.", focus: "Memberi contoh konkret.", expectedKeywords: ["نَذْكُرُ", "كَيْفَ", "سَيَقِيسُ", "الْعَمِيلُ", "النَّجَاحَ"], indonesianExplanation: "Kita sebutkan bagaimana klien akan mengukur keberhasilan setelah satu bulan." },
    { coach: "استخدم الفكرة: أُرْسِلُ التَّعْلِيقَ مَعَ اقْتِرَاحٍ صَغِيرٍ لِإِعَادَةِ الصِّيَاغَةِ.", hint: "Jawab dengan struktur B2 memakai: أُرْسِلُ التَّعْلِيقَ مَعَ اقْتِرَاحٍ صَغِيرٍ لِإِعَادَةِ الصِّيَاغَةِ.", sampleAnswer: "أُرْسِلُ التَّعْلِيقَ مَعَ اقْتِرَاحٍ صَغِيرٍ لِإِعَادَةِ الصِّيَاغَةِ.", focus: "Menutup feedback dengan bantuan.", expectedKeywords: ["أُرْسِلُ", "التَّعْلِيقَ", "مَعَ", "اقْتِرَاحٍ", "صَغِيرٍ"], indonesianExplanation: "Saya mengirim komentar dengan saran kecil untuk merumuskan ulang." },
  ],
  "arabic-b2-handling-concerns": [
    { coach: "مَا الَّذِي يَحْتَاجُ إِلَيْهِ الْعَمِيلُ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى التَّعَامُلُ مَعَ اهْتِمَامَاتِ الْعَمِيلِ.", hint: "Jawab dengan struktur B2 memakai: أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ التَّعَامُلُ مَعَ اهْتِمَامَاتِ الْعَمِيلِ.", sampleAnswer: "أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ التَّعَامُلُ مَعَ اهْتِمَامَاتِ الْعَمِيلِ.", focus: "Memahami kebutuhan klien.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أَفْهَمَ", "اِحْتِيَاجَ", "الْعَمِيلِ"], indonesianExplanation: "Saya ingin memahami kebutuhan klien tentang menangani concern klien." },
    { coach: "استخدم الفكرة: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", hint: "Jawab dengan struktur B2 memakai: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", sampleAnswer: "لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", focus: "Menjelaskan opsi.", expectedKeywords: ["لَدَيْنَا", "خِيَارَانِ،", "وَكُلُّ", "خِيَارٍ", "لَهُ"], indonesianExplanation: "Kita punya dua opsi, dan setiap opsi memiliki manfaat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", sampleAnswer: "أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", focus: "Menangani concern.", expectedKeywords: ["أَفْهَمُ", "هَذَا", "الِاهْتِمَامَ،", "وَسَأُوَضِّحُ", "التَّفَاصِيلَ"], indonesianExplanation: "Saya memahami kekhawatiran ini, dan saya akan menjelaskan detailnya." },
    { coach: "استخدم الفكرة: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", hint: "Jawab dengan struktur B2 memakai: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", sampleAnswer: "الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", focus: "Mengonfirmasi next step.", expectedKeywords: ["الْخُطْوَةُ", "التَّالِيَةُ", "هِيَ", "مُرَاجَعَةُ", "الِاتِّفَاقِ"], indonesianExplanation: "Langkah berikutnya adalah meninjau kesepakatan." },
  ],
  "arabic-b2-handling-objections": [
    { coach: "مَا أَوْلَوِيَّتُكَ فِي هَذَا الِاتِّفَاقِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى التَّعَامُلُ مَعَ الِاعْتِرَاضَاتِ.", hint: "Jawab dengan struktur B2 memakai: أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى التَّعَامُلُ مَعَ الِاعْتِرَاضَاتِ وَاضِحًا.", sampleAnswer: "أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى التَّعَامُلُ مَعَ الِاعْتِرَاضَاتِ وَاضِحًا.", focus: "Menyatakan prioritas.", expectedKeywords: ["أَوْلَوِيَّتِي", "هِيَ", "أَنْ", "يَبْقَى", "التَّعَامُلُ"], indonesianExplanation: "Prioritas saya adalah agar menangani keberatan tetap jelas." },
    { coach: "استخدم الفكرة: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", hint: "Jawab dengan struktur B2 memakai: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", sampleAnswer: "أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", focus: "Membuat proposal.", expectedKeywords: ["أُقَدِّمُ", "الِاقْتِرَاحَ", "التَّالِيَ", "كَحَلٍّ", "عَمَلِيٍّ"], indonesianExplanation: "Saya mengajukan usulan berikut sebagai solusi praktis." },
    { coach: "استخدم الفكرة: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", sampleAnswer: "أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", focus: "Menangani objection.", expectedKeywords: ["أَفْهَمُ", "قَلَقَكَ،", "وَلَكِنْ", "لَدَيْنَا", "خِيَارٌ"], indonesianExplanation: "Saya memahami kekhawatiranmu, tetapi kita punya pilihan lain." },
    { coach: "استخدم الفكرة: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", hint: "Jawab dengan struktur B2 memakai: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", sampleAnswer: "يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", focus: "Mencari kompromi.", expectedKeywords: ["يُمْكِنُنَا", "أَنْ", "نَصِلَ", "إِلَى", "حَلٍّ"], indonesianExplanation: "Kita bisa mencapai solusi tengah." },
  ],
  "arabic-b2-idea-presentation-mission": [
    { coach: "كَيْفَ سَتُقَدِّمِينَ هَذِهِ الْفِكْرَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَقْدِيمُ فِكْرَةٍ وَالدِّفَاعُ عَنْهَا.", hint: "Jawab dengan struktur B2 memakai: سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ تَقْدِيمُ فِكْرَةٍ وَالدِّفَاعُ عَنْهَا.", sampleAnswer: "سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ تَقْدِيمُ فِكْرَةٍ وَالدِّفَاعُ عَنْهَا.", focus: "Membuka presentasi.", expectedKeywords: ["سَأَبْدَأُ", "بِمُقَدِّمَةٍ", "قَصِيرَةٍ", "عَنْ", "تَقْدِيمُ"], indonesianExplanation: "Saya akan mulai dengan pembuka singkat tentang mempresentasikan dan mempertahankan ide." },
    { coach: "استخدم الفكرة: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", sampleAnswer: "بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", focus: "Memberi signposting.", expectedKeywords: ["بَعْدَ", "ذَلِكَ،", "سَأَشْرَحُ", "الْفَائِدَةَ", "الْأَسَاسِيَّةَ"], indonesianExplanation: "Setelah itu, saya akan menjelaskan manfaat utamanya." },
    { coach: "استخدم الفكرة: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", hint: "Jawab dengan struktur B2 memakai: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", sampleAnswer: "مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", focus: "Menjelaskan risk secara seimbang.", expectedKeywords: ["مِنَ", "الْمُهِمِّ", "أَنْ", "نَذْكُرَ", "الْمَخَاطِرَ"], indonesianExplanation: "Penting juga untuk menyebutkan risikonya." },
    { coach: "استخدم الفكرة: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", sampleAnswer: "إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", focus: "Menyiapkan Q&A.", expectedKeywords: ["إِذَا", "كَانَتْ", "هُنَاكَ", "أَسْئِلَةٌ،", "فَسَأُجِيبُ"], indonesianExplanation: "Jika ada pertanyaan, saya akan menjawabnya dengan jelas." },
  ],
  "arabic-b2-information-discussion-mission": [
    { coach: "كَيْفَ تُلَخِّصُ هَذِهِ الْمَعْلُومَاتِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى إِدَارَةُ نِقَاشٍ عَنِ الْمَعْلُومَاتِ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", focus: "Merangkum artikel.", expectedKeywords: ["أَفْهَمُ", "مِنَ", "الْمَقَالِ", "أَنَّ", "هَذَا"], indonesianExplanation: "Saya memahami dari artikel bahwa topik mengelola diskusi informasi penting." },
    { coach: "استخدم الفكرة: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", hint: "Jawab dengan struktur B2 memakai: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", sampleAnswer: "يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", focus: "Mengevaluasi sumber.", expectedKeywords: ["يَجِبُ", "أَنْ", "نَتَأَكَّدَ", "مِنْ", "أَنَّ"], indonesianExplanation: "Kita harus memastikan bahwa sumbernya tepercaya." },
    { coach: "استخدم الفكرة: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", hint: "Jawab dengan struktur B2 memakai: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", sampleAnswer: "وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", focus: "Menguji viewpoint.", expectedKeywords: ["وِجْهَةُ", "النَّظَرِ", "هَذِهِ", "تَحْتَاجُ", "إِلَى"], indonesianExplanation: "Sudut pandang ini membutuhkan bukti yang lebih kuat." },
    { coach: "استخدم الفكرة: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", sampleAnswer: "بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", focus: "Merespons informasi baru.", expectedKeywords: ["بَعْدَ", "الْمَعْلُومَاتِ", "الْجَدِيدَةِ،", "تَغَيَّرَ", "رَأْيِي"], indonesianExplanation: "Setelah informasi baru, pendapat saya sedikit berubah." },
  ],
  "arabic-b2-making-a-proposal": [
    { coach: "مَا أَوْلَوِيَّتُكَ فِي هَذَا الِاتِّفَاقِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَقْدِيمُ اِقْتِرَاحٍ عَمَلِيٍّ.", hint: "Jawab dengan struktur B2 memakai: أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى تَقْدِيمُ اِقْتِرَاحٍ عَمَلِيٍّ وَاضِحًا.", sampleAnswer: "أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى تَقْدِيمُ اِقْتِرَاحٍ عَمَلِيٍّ وَاضِحًا.", focus: "Menyatakan prioritas.", expectedKeywords: ["أَوْلَوِيَّتِي", "هِيَ", "أَنْ", "يَبْقَى", "تَقْدِيمُ"], indonesianExplanation: "Prioritas saya adalah agar mengajukan usulan praktis tetap jelas." },
    { coach: "استخدم الفكرة: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", hint: "Jawab dengan struktur B2 memakai: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", sampleAnswer: "أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", focus: "Membuat proposal.", expectedKeywords: ["أُقَدِّمُ", "الِاقْتِرَاحَ", "التَّالِيَ", "كَحَلٍّ", "عَمَلِيٍّ"], indonesianExplanation: "Saya mengajukan usulan berikut sebagai solusi praktis." },
    { coach: "استخدم الفكرة: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", sampleAnswer: "أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", focus: "Menangani objection.", expectedKeywords: ["أَفْهَمُ", "قَلَقَكَ،", "وَلَكِنْ", "لَدَيْنَا", "خِيَارٌ"], indonesianExplanation: "Saya memahami kekhawatiranmu, tetapi kita punya pilihan lain." },
    { coach: "استخدم الفكرة: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", hint: "Jawab dengan struktur B2 memakai: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", sampleAnswer: "يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", focus: "Mencari kompromi.", expectedKeywords: ["يُمْكِنُنَا", "أَنْ", "نَصِلَ", "إِلَى", "حَلٍّ"], indonesianExplanation: "Kita bisa mencapai solusi tengah." },
  ],
  "arabic-b2-meeting-participation-mission": [
    { coach: "الْيَوْمَ سَتُدِيرِينَ جُزْءًا مِنَ الِاجْتِمَاعِ. كَيْفَ سَتَبْدَئِينَ؟", hint: "Jawab dengan struktur B2 memakai: سَأَفْتَحُ الْمَوْضُوعَ بِجُمْلَةٍ قَصِيرَةٍ ثُمَّ أَسْأَلُ عَنِ النِّطَاقِ.", sampleAnswer: "سَأَفْتَحُ الْمَوْضُوعَ بِجُمْلَةٍ قَصِيرَةٍ ثُمَّ أَسْأَلُ عَنِ النِّطَاقِ.", focus: "Memulai bagian rapat.", expectedKeywords: ["سَأَفْتَحُ", "الْمَوْضُوعَ", "بِجُمْلَةٍ", "قَصِيرَةٍ", "ثُمَّ"], indonesianExplanation: "Saya akan membuka topik dengan kalimat singkat lalu bertanya tentang scope." },
    { coach: "استخدم الفكرة: سَأَشْكُرُ صَاحِبَ الْمُلَاحَظَةِ وَأَطْلُبُ مِثَالًا مُحَدَّدًا.", hint: "Jawab dengan struktur B2 memakai: سَأَشْكُرُ صَاحِبَ الْمُلَاحَظَةِ وَأَطْلُبُ مِثَالًا مُحَدَّدًا.", sampleAnswer: "سَأَشْكُرُ صَاحِبَ الْمُلَاحَظَةِ وَأَطْلُبُ مِثَالًا مُحَدَّدًا.", focus: "Merespons objection.", expectedKeywords: ["سَأَشْكُرُ", "صَاحِبَ", "الْمُلَاحَظَةِ", "وَأَطْلُبُ", "مِثَالًا"], indonesianExplanation: "Saya akan berterima kasih kepada pemberi masukan dan meminta contoh spesifik." },
    { coach: "استخدم الفكرة: سَأُقَارِنُ الْخِيَارَيْنِ ثُمَّ أَقْتَرِحُ خُطْوَةً وَاحِدَةً.", hint: "Jawab dengan struktur B2 memakai: سَأُقَارِنُ الْخِيَارَيْنِ ثُمَّ أَقْتَرِحُ خُطْوَةً وَاحِدَةً.", sampleAnswer: "سَأُقَارِنُ الْخِيَارَيْنِ ثُمَّ أَقْتَرِحُ خُطْوَةً وَاحِدَةً.", focus: "Mengarahkan ke keputusan.", expectedKeywords: ["سَأُقَارِنُ", "الْخِيَارَيْنِ", "ثُمَّ", "أَقْتَرِحُ", "خُطْوَةً"], indonesianExplanation: "Saya akan membandingkan dua opsi lalu mengusulkan satu langkah." },
    { coach: "استخدم الفكرة: سَأُلَخِّصُ الْقَرَارَ وَالْمَسْؤُولِيَّاتِ وَأُرْسِلُهَا بَعْدَ الِاجْتِمَاعِ.", hint: "Jawab dengan struktur B2 memakai: سَأُلَخِّصُ الْقَرَارَ وَالْمَسْؤُولِيَّاتِ وَأُرْسِلُهَا بَعْدَ الِاجْتِمَاعِ.", sampleAnswer: "سَأُلَخِّصُ الْقَرَارَ وَالْمَسْؤُولِيَّاتِ وَأُرْسِلُهَا بَعْدَ الِاجْتِمَاعِ.", focus: "Menutup rapat.", expectedKeywords: ["سَأُلَخِّصُ", "الْقَرَارَ", "وَالْمَسْؤُولِيَّاتِ", "وَأُرْسِلُهَا", "بَعْدَ"], indonesianExplanation: "Saya akan merangkum keputusan dan tanggung jawab lalu mengirimkannya setelah rapat." },
  ],
  "arabic-b2-negotiation-mission": [
    { coach: "مَا أَوْلَوِيَّتُكَ فِي هَذَا الِاتِّفَاقِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى إِدَارَةُ تَفَاوُضٍ وَاضِحٍ.", hint: "Jawab dengan struktur B2 memakai: أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى إِدَارَةُ تَفَاوُضٍ وَاضِحٍ وَاضِحًا.", sampleAnswer: "أَوْلَوِيَّتِي هِيَ أَنْ يَبْقَى إِدَارَةُ تَفَاوُضٍ وَاضِحٍ وَاضِحًا.", focus: "Menyatakan prioritas.", expectedKeywords: ["أَوْلَوِيَّتِي", "هِيَ", "أَنْ", "يَبْقَى", "إِدَارَةُ"], indonesianExplanation: "Prioritas saya adalah agar mengelola negosiasi jelas tetap jelas." },
    { coach: "استخدم الفكرة: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", hint: "Jawab dengan struktur B2 memakai: أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", sampleAnswer: "أُقَدِّمُ الِاقْتِرَاحَ التَّالِيَ كَحَلٍّ عَمَلِيٍّ.", focus: "Membuat proposal.", expectedKeywords: ["أُقَدِّمُ", "الِاقْتِرَاحَ", "التَّالِيَ", "كَحَلٍّ", "عَمَلِيٍّ"], indonesianExplanation: "Saya mengajukan usulan berikut sebagai solusi praktis." },
    { coach: "استخدم الفكرة: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", sampleAnswer: "أَفْهَمُ قَلَقَكَ، وَلَكِنْ لَدَيْنَا خِيَارٌ آخَرُ.", focus: "Menangani objection.", expectedKeywords: ["أَفْهَمُ", "قَلَقَكَ،", "وَلَكِنْ", "لَدَيْنَا", "خِيَارٌ"], indonesianExplanation: "Saya memahami kekhawatiranmu, tetapi kita punya pilihan lain." },
    { coach: "استخدم الفكرة: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", hint: "Jawab dengan struktur B2 memakai: يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", sampleAnswer: "يُمْكِنُنَا أَنْ نَصِلَ إِلَى حَلٍّ وَسَطٍ.", focus: "Mencari kompromi.", expectedKeywords: ["يُمْكِنُنَا", "أَنْ", "نَصِلَ", "إِلَى", "حَلٍّ"], indonesianExplanation: "Kita bisa mencapai solusi tengah." },
  ],
  "arabic-b2-opening-a-meeting-point": [
    { coach: "لِنَبْدَأِ الِاجْتِمَاعَ. مَا النُّقْطَةُ الأُولَى الَّتِي تُرِيدِينَ طَرْحَهَا؟", hint: "Jawab dengan struktur B2 memakai: أَوَدُّ أَنْ أَفْتَحَ النِّقَاشَ حَوْلَ مَوْعِدِ تَسْلِيمِ الْمَشْرُوعِ.", sampleAnswer: "أَوَدُّ أَنْ أَفْتَحَ النِّقَاشَ حَوْلَ مَوْعِدِ تَسْلِيمِ الْمَشْرُوعِ.", focus: "Membuka topik rapat.", expectedKeywords: ["أَوَدُّ", "أَنْ", "أَفْتَحَ", "النِّقَاشَ", "حَوْلَ"], indonesianExplanation: "Saya ingin membuka diskusi tentang tenggat penyerahan proyek." },
    { coach: "استخدم الفكرة: لِأَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ قَبْلَ نِهَايَةِ الْيَوْمِ.", hint: "Jawab dengan struktur B2 memakai: لِأَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ قَبْلَ نِهَايَةِ الْيَوْمِ.", sampleAnswer: "لِأَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ قَبْلَ نِهَايَةِ الْيَوْمِ.", focus: "Memberi alasan rapat.", expectedKeywords: ["لِأَنَّ", "الْفَرِيقَ", "يَحْتَاجُ", "إِلَى", "قَرَارٍ"], indonesianExplanation: "Karena tim membutuhkan keputusan sebelum akhir hari." },
    { coach: "استخدم الفكرة: نُحَدِّدُ الْمَوْعِدَ النِّهَائِيَّ وَمَنْ سَيُرَاجِعُ النُّسْخَةَ الأَخِيرَةَ.", hint: "Jawab dengan struktur B2 memakai: نُحَدِّدُ الْمَوْعِدَ النِّهَائِيَّ وَمَنْ سَيُرَاجِعُ النُّسْخَةَ الأَخِيرَةَ.", sampleAnswer: "نُحَدِّدُ الْمَوْعِدَ النِّهَائِيَّ وَمَنْ سَيُرَاجِعُ النُّسْخَةَ الأَخِيرَةَ.", focus: "Meminta keputusan konkret.", expectedKeywords: ["نُحَدِّدُ", "الْمَوْعِدَ", "النِّهَائِيَّ", "وَمَنْ", "سَيُرَاجِعُ"], indonesianExplanation: "Kita menentukan tenggat akhir dan siapa yang akan meninjau versi terakhir." },
    { coach: "استخدم الفكرة: سَأُرْسِلُ مُلَخَّصًا قَصِيرًا مَعَ الْقَرَارِ وَالْمَسْؤُولِيَّاتِ.", hint: "Jawab dengan struktur B2 memakai: سَأُرْسِلُ مُلَخَّصًا قَصِيرًا مَعَ الْقَرَارِ وَالْمَسْؤُولِيَّاتِ.", sampleAnswer: "سَأُرْسِلُ مُلَخَّصًا قَصِيرًا مَعَ الْقَرَارِ وَالْمَسْؤُولِيَّاتِ.", focus: "Menutup dengan action item.", expectedKeywords: ["سَأُرْسِلُ", "مُلَخَّصًا", "قَصِيرًا", "مَعَ", "الْقَرَارِ"], indonesianExplanation: "Saya akan mengirim ringkasan singkat berisi keputusan dan tanggung jawab." },
  ],
  "arabic-b2-problem-solving-discussion-mission": [
    { coach: "كَيْفَ نُحَدِّدُ هَذِهِ الْمُشْكِلَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى نِقَاشُ حَلِّ مُشْكِلَةٍ مُعَقَّدَةٍ.", hint: "Jawab dengan struktur B2 memakai: أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", sampleAnswer: "أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", focus: "Melakukan framing problem.", expectedKeywords: ["أَرَى", "أَنَّ", "هَذِهِ", "النُّقْطَةَ", "جُزْءٌ"], indonesianExplanation: "Saya melihat bahwa poin mendiskusikan solusi masalah kompleks adalah bagian dari masalah yang lebih besar." },
    { coach: "استخدم الفكرة: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", hint: "Jawab dengan struktur B2 memakai: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", sampleAnswer: "السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", focus: "Menjelaskan cause.", expectedKeywords: ["السَّبَبُ", "الْأَسَاسِيُّ", "قَدْ", "يَكُونُ", "ضَعْفَ"], indonesianExplanation: "Penyebab utamanya mungkin lemahnya pengaturan." },
    { coach: "استخدم الفكرة: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", hint: "Jawab dengan struktur B2 memakai: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", sampleAnswer: "لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", focus: "Membahas tradeoff.", expectedKeywords: ["لِكُلِّ", "حَلٍّ", "فَائِدَةٌ", "وَتَأْثِيرٌ", "جَانِبِيٌّ"], indonesianExplanation: "Setiap solusi punya manfaat dan efek samping." },
    { coach: "استخدم الفكرة: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", hint: "Jawab dengan struktur B2 memakai: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", sampleAnswer: "أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", focus: "Memberi rekomendasi.", expectedKeywords: ["أُوصِي", "بِحَلٍّ", "تَدْرِيجِيٍّ", "لِتَقْلِيلِ", "الْمَخَاطِرِ"], indonesianExplanation: "Saya merekomendasikan solusi bertahap untuk mengurangi risiko." },
  ],
  "arabic-b2-recommending-a-solution": [
    { coach: "كَيْفَ نُحَدِّدُ هَذِهِ الْمُشْكِلَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَقْدِيمُ تَوْصِيَةٍ بِحَلٍّ.", hint: "Jawab dengan struktur B2 memakai: أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", sampleAnswer: "أَرَى أَنَّ هَذِهِ النُّقْطَةَ جُزْءٌ مِنْ مُشْكِلَةٍ أَكْبَرَ.", focus: "Melakukan framing problem.", expectedKeywords: ["أَرَى", "أَنَّ", "هَذِهِ", "النُّقْطَةَ", "جُزْءٌ"], indonesianExplanation: "Saya melihat bahwa poin merekomendasikan solusi adalah bagian dari masalah yang lebih besar." },
    { coach: "استخدم الفكرة: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", hint: "Jawab dengan struktur B2 memakai: السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", sampleAnswer: "السَّبَبُ الْأَسَاسِيُّ قَدْ يَكُونُ ضَعْفَ التَّنْظِيمِ.", focus: "Menjelaskan cause.", expectedKeywords: ["السَّبَبُ", "الْأَسَاسِيُّ", "قَدْ", "يَكُونُ", "ضَعْفَ"], indonesianExplanation: "Penyebab utamanya mungkin lemahnya pengaturan." },
    { coach: "استخدم الفكرة: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", hint: "Jawab dengan struktur B2 memakai: لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", sampleAnswer: "لِكُلِّ حَلٍّ فَائِدَةٌ وَتَأْثِيرٌ جَانِبِيٌّ.", focus: "Membahas tradeoff.", expectedKeywords: ["لِكُلِّ", "حَلٍّ", "فَائِدَةٌ", "وَتَأْثِيرٌ", "جَانِبِيٌّ"], indonesianExplanation: "Setiap solusi punya manfaat dan efek samping." },
    { coach: "استخدم الفكرة: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", hint: "Jawab dengan struktur B2 memakai: أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", sampleAnswer: "أُوصِي بِحَلٍّ تَدْرِيجِيٍّ لِتَقْلِيلِ الْمَخَاطِرِ.", focus: "Memberi rekomendasi.", expectedKeywords: ["أُوصِي", "بِحَلٍّ", "تَدْرِيجِيٍّ", "لِتَقْلِيلِ", "الْمَخَاطِرِ"], indonesianExplanation: "Saya merekomendasikan solusi bertahap untuk mengurangi risiko." },
  ],
  "arabic-b2-responding-to-counterpoints": [
    { coach: "مَا مَوْقِفُكَ مِنْ هَذَا الْمَوْضُوعِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى الرَّدُّ عَلَى الِاعْتِرَاضِ.", hint: "Jawab dengan struktur B2 memakai: مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", sampleAnswer: "مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", focus: "Menyatakan posisi dengan jelas.", expectedKeywords: ["مَوْقِفِي", "هُوَ", "أَنَّ", "هَذَا", "الْمَوْضُوعَ"], indonesianExplanation: "Posisi saya adalah bahwa topik menanggapi keberatan penting dalam diskusi." },
    { coach: "استخدم الفكرة: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", hint: "Jawab dengan struktur B2 memakai: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", sampleAnswer: "أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", focus: "Memberi kerangka argumen.", expectedKeywords: ["أَدْعَمُ", "هَذَا", "الرَّأْيَ", "بِسَبَبَيْنِ", "وَاضِحَيْنِ"], indonesianExplanation: "Saya mendukung pendapat ini dengan dua alasan yang jelas." },
    { coach: "استخدم الفكرة: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", hint: "Jawab dengan struktur B2 memakai: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", sampleAnswer: "مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", focus: "Memberi contoh konkret.", expectedKeywords: ["مِثَالُ", "ذَلِكَ", "أَنَّ", "الْفَرِيقَ", "يَحْتَاجُ"], indonesianExplanation: "Contohnya, tim membutuhkan keputusan yang cepat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", sampleAnswer: "أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", focus: "Merespons counterpoint dengan sopan.", expectedKeywords: ["أَفْهَمُ", "هَذِهِ", "النُّقْطَةَ", "الْمُعَارِضَةَ،", "وَلَكِنَّ"], indonesianExplanation: "Saya memahami poin lawannya, tetapi manfaatnya lebih besar." },
  ],
  "arabic-b2-responding-to-new-information": [
    { coach: "كَيْفَ تُلَخِّصُ هَذِهِ الْمَعْلُومَاتِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى الرَّدُّ عَلَى مَعْلُومَاتٍ جَدِيدَةٍ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", focus: "Merangkum artikel.", expectedKeywords: ["أَفْهَمُ", "مِنَ", "الْمَقَالِ", "أَنَّ", "هَذَا"], indonesianExplanation: "Saya memahami dari artikel bahwa topik menanggapi informasi baru penting." },
    { coach: "استخدم الفكرة: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", hint: "Jawab dengan struktur B2 memakai: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", sampleAnswer: "يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", focus: "Mengevaluasi sumber.", expectedKeywords: ["يَجِبُ", "أَنْ", "نَتَأَكَّدَ", "مِنْ", "أَنَّ"], indonesianExplanation: "Kita harus memastikan bahwa sumbernya tepercaya." },
    { coach: "استخدم الفكرة: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", hint: "Jawab dengan struktur B2 memakai: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", sampleAnswer: "وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", focus: "Menguji viewpoint.", expectedKeywords: ["وِجْهَةُ", "النَّظَرِ", "هَذِهِ", "تَحْتَاجُ", "إِلَى"], indonesianExplanation: "Sudut pandang ini membutuhkan bukti yang lebih kuat." },
    { coach: "استخدم الفكرة: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", sampleAnswer: "بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", focus: "Merespons informasi baru.", expectedKeywords: ["بَعْدَ", "الْمَعْلُومَاتِ", "الْجَدِيدَةِ،", "تَغَيَّرَ", "رَأْيِي"], indonesianExplanation: "Setelah informasi baru, pendapat saya sedikit berubah." },
  ],
  "arabic-b2-review-arguments-and-meetings": [
    { coach: "مَا أَهَمُّ مَهَارَةٍ تُرَاجِعِينَها الْآنَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى الْحُجَجِ وَالِاجْتِمَاعَاتِ.", hint: "Jawab dengan struktur B2 memakai: أُرَاجِعُ الْحُجَجَ وَالِاجْتِمَاعَاتِ لِأَنَّهَا مُهِمَّةٌ فِي النِّقَاشِ.", sampleAnswer: "أُرَاجِعُ الْحُجَجَ وَالِاجْتِمَاعَاتِ لِأَنَّهَا مُهِمَّةٌ فِي النِّقَاشِ.", focus: "Membuka review.", expectedKeywords: ["أُرَاجِعُ", "الْحُجَجَ", "وَالِاجْتِمَاعَاتِ", "لِأَنَّهَا", "مُهِمَّةٌ"], indonesianExplanation: "Saya mereview argumen dan rapat karena itu penting dalam diskusi." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", sampleAnswer: "أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", focus: "Mereview kemampuan menyusun argumen.", expectedKeywords: ["أَسْتَطِيعُ", "أَنْ", "أُقَدِّمَ", "رَأْيًا", "وَأَدْعَمَهُ"], indonesianExplanation: "Saya bisa menyampaikan pendapat dan mendukungnya dengan bukti." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", sampleAnswer: "أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", focus: "Mereview kemampuan percakapan profesional.", expectedKeywords: ["أَسْتَطِيعُ", "أَيْضًا", "أَنْ", "أُدِيرَ", "حِوَارًا"], indonesianExplanation: "Saya juga bisa mengelola percakapan profesional dengan jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", sampleAnswer: "إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", focus: "Mereview respons terhadap keberatan.", expectedKeywords: ["إِذَا", "ظَهَرَ", "اِعْتِرَاضٌ،", "فَسَأَرُدُّ", "عَلَيْهِ"], indonesianExplanation: "Jika muncul keberatan, saya akan menanggapinya dengan tenang." },
  ],
  "arabic-b2-review-information-and-clients": [
    { coach: "مَا أَهَمُّ مَهَارَةٍ تُرَاجِعِينَها الْآنَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى التَّعَامُلِ مَعَ الْمَعْلُومَاتِ وَالْعُمَلَاءِ.", hint: "Jawab dengan struktur B2 memakai: أُرَاجِعُ التَّعَامُلَ مَعَ الْمَعْلُومَاتِ وَالْعُمَلَاءِ لِأَنَّهُ مُهِمٌّ فِي النِّقَاشِ.", sampleAnswer: "أُرَاجِعُ التَّعَامُلَ مَعَ الْمَعْلُومَاتِ وَالْعُمَلَاءِ لِأَنَّهُ مُهِمٌّ فِي النِّقَاشِ.", focus: "Membuka review.", expectedKeywords: ["أُرَاجِعُ", "التَّعَامُلَ", "مَعَ", "الْمَعْلُومَاتِ", "وَالْعُمَلَاءِ"], indonesianExplanation: "Saya mereview cara menangani informasi dan klien karena itu penting dalam diskusi." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", sampleAnswer: "أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", focus: "Mereview kemampuan menyusun argumen.", expectedKeywords: ["أَسْتَطِيعُ", "أَنْ", "أُقَدِّمَ", "رَأْيًا", "وَأَدْعَمَهُ"], indonesianExplanation: "Saya bisa menyampaikan pendapat dan mendukungnya dengan bukti." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", sampleAnswer: "أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", focus: "Mereview kemampuan percakapan profesional.", expectedKeywords: ["أَسْتَطِيعُ", "أَيْضًا", "أَنْ", "أُدِيرَ", "حِوَارًا"], indonesianExplanation: "Saya juga bisa mengelola percakapan profesional dengan jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", sampleAnswer: "إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", focus: "Mereview respons terhadap keberatan.", expectedKeywords: ["إِذَا", "ظَهَرَ", "اِعْتِرَاضٌ،", "فَسَأَرُدُّ", "عَلَيْهِ"], indonesianExplanation: "Jika muncul keberatan, saya akan menanggapinya dengan tenang." },
  ],
  "arabic-b2-review-negotiation-and-presenting": [
    { coach: "مَا أَهَمُّ مَهَارَةٍ تُرَاجِعِينَها الْآنَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى التَّفَاوُضِ وَالْعَرْضِ.", hint: "Jawab dengan struktur B2 memakai: أُرَاجِعُ التَّفَاوُضَ وَالْعَرْضَ لِأَنَّهُمَا مُهِمَّانِ فِي النِّقَاشِ.", sampleAnswer: "أُرَاجِعُ التَّفَاوُضَ وَالْعَرْضَ لِأَنَّهُمَا مُهِمَّانِ فِي النِّقَاشِ.", focus: "Membuka review.", expectedKeywords: ["أُرَاجِعُ", "التَّفَاوُضَ", "وَالْعَرْضَ", "لِأَنَّهُمَا", "مُهِمَّانِ"], indonesianExplanation: "Saya mereview negosiasi dan presentasi karena keduanya penting dalam diskusi." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", sampleAnswer: "أَسْتَطِيعُ أَنْ أُقَدِّمَ رَأْيًا وَأَدْعَمَهُ بِدَلِيلٍ.", focus: "Mereview kemampuan menyusun argumen.", expectedKeywords: ["أَسْتَطِيعُ", "أَنْ", "أُقَدِّمَ", "رَأْيًا", "وَأَدْعَمَهُ"], indonesianExplanation: "Saya bisa menyampaikan pendapat dan mendukungnya dengan bukti." },
    { coach: "استخدم الفكرة: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", sampleAnswer: "أَسْتَطِيعُ أَيْضًا أَنْ أُدِيرَ حِوَارًا مِهَنِيًّا بِوُضُوحٍ.", focus: "Mereview kemampuan percakapan profesional.", expectedKeywords: ["أَسْتَطِيعُ", "أَيْضًا", "أَنْ", "أُدِيرَ", "حِوَارًا"], indonesianExplanation: "Saya juga bisa mengelola percakapan profesional dengan jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", sampleAnswer: "إِذَا ظَهَرَ اِعْتِرَاضٌ، فَسَأَرُدُّ عَلَيْهِ بِهُدُوءٍ.", focus: "Mereview respons terhadap keberatan.", expectedKeywords: ["إِذَا", "ظَهَرَ", "اِعْتِرَاضٌ،", "فَسَأَرُدُّ", "عَلَيْهِ"], indonesianExplanation: "Jika muncul keberatan, saya akan menanggapinya dengan tenang." },
  ],
  "arabic-b2-signposting-clearly": [
    { coach: "كَيْفَ سَتُقَدِّمِينَ هَذِهِ الْفِكْرَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَوْضِيحُ الِانْتِقَالَاتِ.", hint: "Jawab dengan struktur B2 memakai: سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ تَوْضِيحُ الِانْتِقَالَاتِ.", sampleAnswer: "سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ تَوْضِيحُ الِانْتِقَالَاتِ.", focus: "Membuka presentasi.", expectedKeywords: ["سَأَبْدَأُ", "بِمُقَدِّمَةٍ", "قَصِيرَةٍ", "عَنْ", "تَوْضِيحُ"], indonesianExplanation: "Saya akan mulai dengan pembuka singkat tentang memberi transisi jelas." },
    { coach: "استخدم الفكرة: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", sampleAnswer: "بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", focus: "Memberi signposting.", expectedKeywords: ["بَعْدَ", "ذَلِكَ،", "سَأَشْرَحُ", "الْفَائِدَةَ", "الْأَسَاسِيَّةَ"], indonesianExplanation: "Setelah itu, saya akan menjelaskan manfaat utamanya." },
    { coach: "استخدم الفكرة: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", hint: "Jawab dengan struktur B2 memakai: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", sampleAnswer: "مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", focus: "Menjelaskan risk secara seimbang.", expectedKeywords: ["مِنَ", "الْمُهِمِّ", "أَنْ", "نَذْكُرَ", "الْمَخَاطِرَ"], indonesianExplanation: "Penting juga untuk menyebutkan risikonya." },
    { coach: "استخدم الفكرة: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", sampleAnswer: "إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", focus: "Menyiapkan Q&A.", expectedKeywords: ["إِذَا", "كَانَتْ", "هُنَاكَ", "أَسْئِلَةٌ،", "فَسَأُجِيبُ"], indonesianExplanation: "Jika ada pertanyaan, saya akan menjawabnya dengan jelas." },
  ],
  "arabic-b2-stating-your-position": [
    { coach: "مَا مَوْقِفُكَ مِنْ هَذَا الْمَوْضُوعِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَحْدِيدُ الْمَوْقِفِ.", hint: "Jawab dengan struktur B2 memakai: مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", sampleAnswer: "مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", focus: "Menyatakan posisi dengan jelas.", expectedKeywords: ["مَوْقِفِي", "هُوَ", "أَنَّ", "هَذَا", "الْمَوْضُوعَ"], indonesianExplanation: "Posisi saya adalah bahwa topik menentukan posisi penting dalam diskusi." },
    { coach: "استخدم الفكرة: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", hint: "Jawab dengan struktur B2 memakai: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", sampleAnswer: "أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", focus: "Memberi kerangka argumen.", expectedKeywords: ["أَدْعَمُ", "هَذَا", "الرَّأْيَ", "بِسَبَبَيْنِ", "وَاضِحَيْنِ"], indonesianExplanation: "Saya mendukung pendapat ini dengan dua alasan yang jelas." },
    { coach: "استخدم الفكرة: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", hint: "Jawab dengan struktur B2 memakai: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", sampleAnswer: "مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", focus: "Memberi contoh konkret.", expectedKeywords: ["مِثَالُ", "ذَلِكَ", "أَنَّ", "الْفَرِيقَ", "يَحْتَاجُ"], indonesianExplanation: "Contohnya, tim membutuhkan keputusan yang cepat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", sampleAnswer: "أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", focus: "Merespons counterpoint dengan sopan.", expectedKeywords: ["أَفْهَمُ", "هَذِهِ", "النُّقْطَةَ", "الْمُعَارِضَةَ،", "وَلَكِنَّ"], indonesianExplanation: "Saya memahami poin lawannya, tetapi manfaatnya lebih besar." },
  ],
  "arabic-b2-structuring-a-short-presentation": [
    { coach: "كَيْفَ سَتُقَدِّمِينَ هَذِهِ الْفِكْرَةَ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَنْظِيمُ عَرْضٍ قَصِيرٍ.", hint: "Jawab dengan struktur B2 memakai: سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ تَنْظِيمُ عَرْضٍ قَصِيرٍ.", sampleAnswer: "سَأَبْدَأُ بِمُقَدِّمَةٍ قَصِيرَةٍ عَنْ تَنْظِيمُ عَرْضٍ قَصِيرٍ.", focus: "Membuka presentasi.", expectedKeywords: ["سَأَبْدَأُ", "بِمُقَدِّمَةٍ", "قَصِيرَةٍ", "عَنْ", "تَنْظِيمُ"], indonesianExplanation: "Saya akan mulai dengan pembuka singkat tentang menyusun presentasi singkat." },
    { coach: "استخدم الفكرة: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", sampleAnswer: "بَعْدَ ذَلِكَ، سَأَشْرَحُ الْفَائِدَةَ الْأَسَاسِيَّةَ.", focus: "Memberi signposting.", expectedKeywords: ["بَعْدَ", "ذَلِكَ،", "سَأَشْرَحُ", "الْفَائِدَةَ", "الْأَسَاسِيَّةَ"], indonesianExplanation: "Setelah itu, saya akan menjelaskan manfaat utamanya." },
    { coach: "استخدم الفكرة: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", hint: "Jawab dengan struktur B2 memakai: مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", sampleAnswer: "مِنَ الْمُهِمِّ أَنْ نَذْكُرَ الْمَخَاطِرَ أَيْضًا.", focus: "Menjelaskan risk secara seimbang.", expectedKeywords: ["مِنَ", "الْمُهِمِّ", "أَنْ", "نَذْكُرَ", "الْمَخَاطِرَ"], indonesianExplanation: "Penting juga untuk menyebutkan risikonya." },
    { coach: "استخدم الفكرة: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", hint: "Jawab dengan struktur B2 memakai: إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", sampleAnswer: "إِذَا كَانَتْ هُنَاكَ أَسْئِلَةٌ، فَسَأُجِيبُ عَنْهَا بِوُضُوحٍ.", focus: "Menyiapkan Q&A.", expectedKeywords: ["إِذَا", "كَانَتْ", "هُنَاكَ", "أَسْئِلَةٌ،", "فَسَأُجِيبُ"], indonesianExplanation: "Jika ada pertanyaan, saya akan menjawabnya dengan jelas." },
  ],
  "arabic-b2-summarizing-an-article": [
    { coach: "كَيْفَ تُلَخِّصُ هَذِهِ الْمَعْلُومَاتِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى تَلْخِيصُ مَقَالٍ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "أَفْهَمُ مِنَ الْمَقَالِ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ.", focus: "Merangkum artikel.", expectedKeywords: ["أَفْهَمُ", "مِنَ", "الْمَقَالِ", "أَنَّ", "هَذَا"], indonesianExplanation: "Saya memahami dari artikel bahwa topik merangkum artikel penting." },
    { coach: "استخدم الفكرة: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", hint: "Jawab dengan struktur B2 memakai: يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", sampleAnswer: "يَجِبُ أَنْ نَتَأَكَّدَ مِنْ أَنَّ الْمَصْدَرَ مَوْثُوقٌ.", focus: "Mengevaluasi sumber.", expectedKeywords: ["يَجِبُ", "أَنْ", "نَتَأَكَّدَ", "مِنْ", "أَنَّ"], indonesianExplanation: "Kita harus memastikan bahwa sumbernya tepercaya." },
    { coach: "استخدم الفكرة: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", hint: "Jawab dengan struktur B2 memakai: وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", sampleAnswer: "وِجْهَةُ النَّظَرِ هَذِهِ تَحْتَاجُ إِلَى دَلِيلٍ أَقْوَى.", focus: "Menguji viewpoint.", expectedKeywords: ["وِجْهَةُ", "النَّظَرِ", "هَذِهِ", "تَحْتَاجُ", "إِلَى"], indonesianExplanation: "Sudut pandang ini membutuhkan bukti yang lebih kuat." },
    { coach: "استخدم الفكرة: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", hint: "Jawab dengan struktur B2 memakai: بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", sampleAnswer: "بَعْدَ الْمَعْلُومَاتِ الْجَدِيدَةِ، تَغَيَّرَ رَأْيِي قَلِيلًا.", focus: "Merespons informasi baru.", expectedKeywords: ["بَعْدَ", "الْمَعْلُومَاتِ", "الْجَدِيدَةِ،", "تَغَيَّرَ", "رَأْيِي"], indonesianExplanation: "Setelah informasi baru, pendapat saya sedikit berubah." },
  ],
  "arabic-b2-summarizing-decisions": [
    { coach: "قَبْلَ أَنْ نُنْهِيَ الِاجْتِمَاعَ، مَا الَّذِي اتَّفَقْنَا عَلَيْهِ؟", hint: "Jawab dengan struktur B2 memakai: اتَّفَقْنَا عَلَى تَسْلِيمِ النُّسْخَةِ الأُولَى يَوْمَ الْخَمِيسِ.", sampleAnswer: "اتَّفَقْنَا عَلَى تَسْلِيمِ النُّسْخَةِ الأُولَى يَوْمَ الْخَمِيسِ.", focus: "Menyebut keputusan.", expectedKeywords: ["اتَّفَقْنَا", "عَلَى", "تَسْلِيمِ", "النُّسْخَةِ", "الأُولَى"], indonesianExplanation: "Kita sepakat menyerahkan versi pertama pada hari Kamis." },
    { coach: "استخدم الفكرة: أَنَا أُرَاجِعُ النَّصَّ، وَفَاطِمَةُ تُرَاجِعُ التَّصْمِيمَ.", hint: "Jawab dengan struktur B2 memakai: أَنَا أُرَاجِعُ النَّصَّ، وَفَاطِمَةُ تُرَاجِعُ التَّصْمِيمَ.", sampleAnswer: "أَنَا أُرَاجِعُ النَّصَّ، وَفَاطِمَةُ تُرَاجِعُ التَّصْمِيمَ.", focus: "Menyebut tanggung jawab.", expectedKeywords: ["أَنَا", "أُرَاجِعُ", "النَّصَّ،", "وَفَاطِمَةُ", "تُرَاجِعُ"], indonesianExplanation: "Saya meninjau teks, dan Fatimah meninjau desain." },
    { coach: "استخدم الفكرة: نَحْتَاجُ إِلَى مُوَافَقَةِ الْعَمِيلِ عَلَى الصُّوَرِ.", hint: "Jawab dengan struktur B2 memakai: نَحْتَاجُ إِلَى مُوَافَقَةِ الْعَمِيلِ عَلَى الصُّوَرِ.", sampleAnswer: "نَحْتَاجُ إِلَى مُوَافَقَةِ الْعَمِيلِ عَلَى الصُّوَرِ.", focus: "Menyebut poin terbuka.", expectedKeywords: ["نَحْتَاجُ", "إِلَى", "مُوَافَقَةِ", "الْعَمِيلِ", "عَلَى"], indonesianExplanation: "Kita membutuhkan persetujuan klien untuk gambar." },
    { coach: "استخدم الفكرة: سَأَكْتُبُ ثَلَاثَ نِقَاطٍ: الْقَرَارَ، الْمَسْؤُولَ، وَالْمَوْعِدَ.", hint: "Jawab dengan struktur B2 memakai: سَأَكْتُبُ ثَلَاثَ نِقَاطٍ: الْقَرَارَ، الْمَسْؤُولَ، وَالْمَوْعِدَ.", sampleAnswer: "سَأَكْتُبُ ثَلَاثَ نِقَاطٍ: الْقَرَارَ، الْمَسْؤُولَ، وَالْمَوْعِدَ.", focus: "Merangkum action items.", expectedKeywords: ["سَأَكْتُبُ", "ثَلَاثَ", "نِقَاطٍ:", "الْقَرَارَ،", "الْمَسْؤُولَ،"], indonesianExplanation: "Saya akan menulis tiga poin: keputusan, penanggung jawab, dan tenggat." },
  ],
  "arabic-b2-supporting-with-reasons": [
    { coach: "مَا مَوْقِفُكَ مِنْ هَذَا الْمَوْضُوعِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى دَعْمُ الرَّأْيِ بِالْأَسْبَابِ.", hint: "Jawab dengan struktur B2 memakai: مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", sampleAnswer: "مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", focus: "Menyatakan posisi dengan jelas.", expectedKeywords: ["مَوْقِفِي", "هُوَ", "أَنَّ", "هَذَا", "الْمَوْضُوعَ"], indonesianExplanation: "Posisi saya adalah bahwa topik mendukung pendapat dengan alasan penting dalam diskusi." },
    { coach: "استخدم الفكرة: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", hint: "Jawab dengan struktur B2 memakai: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", sampleAnswer: "أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", focus: "Memberi kerangka argumen.", expectedKeywords: ["أَدْعَمُ", "هَذَا", "الرَّأْيَ", "بِسَبَبَيْنِ", "وَاضِحَيْنِ"], indonesianExplanation: "Saya mendukung pendapat ini dengan dua alasan yang jelas." },
    { coach: "استخدم الفكرة: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", hint: "Jawab dengan struktur B2 memakai: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", sampleAnswer: "مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", focus: "Memberi contoh konkret.", expectedKeywords: ["مِثَالُ", "ذَلِكَ", "أَنَّ", "الْفَرِيقَ", "يَحْتَاجُ"], indonesianExplanation: "Contohnya, tim membutuhkan keputusan yang cepat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", sampleAnswer: "أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", focus: "Merespons counterpoint dengan sopan.", expectedKeywords: ["أَفْهَمُ", "هَذِهِ", "النُّقْطَةَ", "الْمُعَارِضَةَ،", "وَلَكِنَّ"], indonesianExplanation: "Saya memahami poin lawannya, tetapi manfaatnya lebih besar." },
  ],
  "arabic-b2-understanding-client-needs": [
    { coach: "مَا الَّذِي يَحْتَاجُ إِلَيْهِ الْعَمِيلُ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى فَهْمُ اِحْتِيَاجِ الْعَمِيلِ.", hint: "Jawab dengan struktur B2 memakai: أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ فَهْمُ اِحْتِيَاجِ الْعَمِيلِ.", sampleAnswer: "أُرِيدُ أَنْ أَفْهَمَ اِحْتِيَاجَ الْعَمِيلِ حَوْلَ فَهْمُ اِحْتِيَاجِ الْعَمِيلِ.", focus: "Memahami kebutuhan klien.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أَفْهَمَ", "اِحْتِيَاجَ", "الْعَمِيلِ"], indonesianExplanation: "Saya ingin memahami kebutuhan klien tentang memahami kebutuhan klien." },
    { coach: "استخدم الفكرة: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", hint: "Jawab dengan struktur B2 memakai: لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", sampleAnswer: "لَدَيْنَا خِيَارَانِ، وَكُلُّ خِيَارٍ لَهُ فَائِدَةٌ.", focus: "Menjelaskan opsi.", expectedKeywords: ["لَدَيْنَا", "خِيَارَانِ،", "وَكُلُّ", "خِيَارٍ", "لَهُ"], indonesianExplanation: "Kita punya dua opsi, dan setiap opsi memiliki manfaat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", sampleAnswer: "أَفْهَمُ هَذَا الِاهْتِمَامَ، وَسَأُوَضِّحُ التَّفَاصِيلَ.", focus: "Menangani concern.", expectedKeywords: ["أَفْهَمُ", "هَذَا", "الِاهْتِمَامَ،", "وَسَأُوَضِّحُ", "التَّفَاصِيلَ"], indonesianExplanation: "Saya memahami kekhawatiran ini, dan saya akan menjelaskan detailnya." },
    { coach: "استخدم الفكرة: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", hint: "Jawab dengan struktur B2 memakai: الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", sampleAnswer: "الْخُطْوَةُ التَّالِيَةُ هِيَ مُرَاجَعَةُ الِاتِّفَاقِ.", focus: "Mengonfirmasi next step.", expectedKeywords: ["الْخُطْوَةُ", "التَّالِيَةُ", "هِيَ", "مُرَاجَعَةُ", "الِاتِّفَاقِ"], indonesianExplanation: "Langkah berikutnya adalah meninjau kesepakatan." },
  ],
  "arabic-b2-using-examples": [
    { coach: "مَا مَوْقِفُكَ مِنْ هَذَا الْمَوْضُوعِ؟ أُرِيدُ أَنْ أُرَكِّزَ عَلَى اِسْتِخْدَامُ الْأَمْثِلَةِ.", hint: "Jawab dengan struktur B2 memakai: مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", sampleAnswer: "مَوْقِفِي هُوَ أَنَّ هَذَا الْمَوْضُوعَ مُهِمٌّ فِي النِّقَاشِ.", focus: "Menyatakan posisi dengan jelas.", expectedKeywords: ["مَوْقِفِي", "هُوَ", "أَنَّ", "هَذَا", "الْمَوْضُوعَ"], indonesianExplanation: "Posisi saya adalah bahwa topik menggunakan contoh penting dalam diskusi." },
    { coach: "استخدم الفكرة: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", hint: "Jawab dengan struktur B2 memakai: أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", sampleAnswer: "أَدْعَمُ هَذَا الرَّأْيَ بِسَبَبَيْنِ وَاضِحَيْنِ.", focus: "Memberi kerangka argumen.", expectedKeywords: ["أَدْعَمُ", "هَذَا", "الرَّأْيَ", "بِسَبَبَيْنِ", "وَاضِحَيْنِ"], indonesianExplanation: "Saya mendukung pendapat ini dengan dua alasan yang jelas." },
    { coach: "استخدم الفكرة: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", hint: "Jawab dengan struktur B2 memakai: مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", sampleAnswer: "مِثَالُ ذَلِكَ أَنَّ الْفَرِيقَ يَحْتَاجُ إِلَى قَرَارٍ سَرِيعٍ.", focus: "Memberi contoh konkret.", expectedKeywords: ["مِثَالُ", "ذَلِكَ", "أَنَّ", "الْفَرِيقَ", "يَحْتَاجُ"], indonesianExplanation: "Contohnya, tim membutuhkan keputusan yang cepat." },
    { coach: "استخدم الفكرة: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", hint: "Jawab dengan struktur B2 memakai: أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", sampleAnswer: "أَفْهَمُ هَذِهِ النُّقْطَةَ الْمُعَارِضَةَ، وَلَكِنَّ الْفَائِدَةَ أَكْبَرُ.", focus: "Merespons counterpoint dengan sopan.", expectedKeywords: ["أَفْهَمُ", "هَذِهِ", "النُّقْطَةَ", "الْمُعَارِضَةَ،", "وَلَكِنَّ"], indonesianExplanation: "Saya memahami poin lawannya, tetapi manfaatnya lebih besar." },
  ],
  "arabic-buying-a-simple-item": [
    { coach: "هَلْ عِنْدَكُمْ قَلَمٌ؟", hint: "Jawab dengan pola: هَلْ عِنْدَكُمْ قَلَمٌ؟", sampleAnswer: "هَلْ عِنْدَكُمْ قَلَمٌ؟", focus: "Latihan frasa: Apakah kalian punya pena?", expectedKeywords: ["هَلْ", "عِنْدَكُمْ", "قَلَمٌ"], indonesianExplanation: "Apakah kalian punya pena?" },
    { coach: "استخدم: نَعَمْ، مَوْجُودٌ", hint: "Jawab dengan pola: نَعَمْ، مَوْجُودٌ", sampleAnswer: "نَعَمْ، مَوْجُودٌ", focus: "Latihan frasa: Ya, ada.", expectedKeywords: ["نَعَمْ،", "مَوْجُودٌ"], indonesianExplanation: "Ya, ada." },
    { coach: "استخدم: أُرِيدُ هَذَا", hint: "Jawab dengan pola: أُرِيدُ هَذَا", sampleAnswer: "أُرِيدُ هَذَا", focus: "Latihan frasa: Saya ingin ini.", expectedKeywords: ["أُرِيدُ", "هَذَا"], indonesianExplanation: "Saya ingin ini." },
  ],
  "arabic-buying-a-ticket": [
    { coach: "أُرِيدُ تَذْكِرَةً إِلَى جَاكَرْتَا، مِنْ فَضْلِكِ.", hint: "Jawab dengan pola: أُرِيدُ تَذْكِرَةً إِلَى جَاكَرْتَا.", sampleAnswer: "أُرِيدُ تَذْكِرَةً إِلَى جَاكَرْتَا.", focus: "Latihan frasa: Saya ingin tiket ke Jakarta.", expectedKeywords: ["أُرِيدُ", "تَذْكِرَةً", "إِلَى"], indonesianExplanation: "Saya ingin tiket ke Jakarta." },
    { coach: "استخدم: ذَهَابًا فَقَطْ.", hint: "Jawab dengan pola: ذَهَابًا فَقَطْ.", sampleAnswer: "ذَهَابًا فَقَطْ.", focus: "Latihan frasa: Sekali jalan saja.", expectedKeywords: ["ذَهَابًا", "فَقَطْ"], indonesianExplanation: "Sekali jalan saja." },
    { coach: "استخدم: ذَهَابًا وَعَوْدَةً.", hint: "Jawab dengan pola: ذَهَابًا وَعَوْدَةً.", sampleAnswer: "ذَهَابًا وَعَوْدَةً.", focus: "Latihan frasa: Pulang pergi.", expectedKeywords: ["ذَهَابًا", "وَعَوْدَةً"], indonesianExplanation: "Pulang pergi." },
  ],
  "arabic-c1-advanced-listening-mission": [
    { coach: "كَيْفَ تُحَوِّلُ هَذِهِ الْمَهَارَةَ إِلَى خُطْوَةٍ عَمَلِيَّةٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ إِدَارَةِ رَدٍّ بَعْدَ اِسْتِمَاعٍ مُتَقَدِّمٍ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", sampleAnswer: "فِي مَهَارَةِ إِدَارَةِ رَدٍّ بَعْدَ اِسْتِمَاعٍ مُتَقَدِّمٍ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", focus: "Menangkap implied meaning. Fokus lesson: responding after advanced listening.", expectedKeywords: ["فِي", "مَهَارَةِ", "إِدَارَةِ", "رَدٍّ", "بَعْدَ"], indonesianExplanation: "Dalam skill responding after advanced listening, Makna tersiratnya di sini adalah pembicara belum sepenuhnya yakin." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ إِدَارَةِ رَدٍّ بَعْدَ اِسْتِمَاعٍ مُتَقَدِّمٍ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ إِدَارَةِ رَدٍّ بَعْدَ اِسْتِمَاعٍ مُتَقَدِّمٍ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ إِدَارَةِ رَدٍّ بَعْدَ اِسْتِمَاعٍ مُتَقَدِّمٍ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", focus: "Merespons long turn. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "إِدَارَةِ", "رَدٍّ", "بَعْدَ"], indonesianExplanation: "Saat menerapkan responding after advanced listening, Saya akan menjawab poin utama dulu, lalu kembali ke detail." },
    { coach: "استخدم الفكرة: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", sampleAnswer: "إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", focus: "Merangkum yang didengar. Pakai sebagai penghubung dalam responding after advanced listening.", expectedKeywords: ["إِذَا", "لَخَّصْتُ", "مَا", "سَمِعْتُهُ،", "فَالْفِكْرَةُ"], indonesianExplanation: "Jika saya merangkum apa yang saya dengar, ide utamanya adalah menunda keputusan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", focus: "Bertanya follow-up berkualitas. Gunakan untuk repair dalam responding after advanced listening.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Pertanyaan follow-up terbaik adalah: apa yang akan mengubah keputusan ini?" },
  ],
  "arabic-c1-advanced-presentation-mission": [
    { coach: "كَيْفَ تُحَوِّلُ هَذِهِ الْمَهَارَةَ إِلَى خُطْوَةٍ عَمَلِيَّةٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَقْدِيمِ عَرْضٍ مُتَقَدِّمٍ وَاضِحٍ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", sampleAnswer: "فِي مَهَارَةِ تَقْدِيمِ عَرْضٍ مُتَقَدِّمٍ وَاضِحٍ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", focus: "Membingkai topik kompleks. Fokus lesson: delivering an advanced presentation.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَقْدِيمِ", "عَرْضٍ", "مُتَقَدِّمٍ"], indonesianExplanation: "Dalam skill delivering an advanced presentation, Saya akan membingkai topiknya dulu agar audiens memahami konteksnya." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَقْدِيمِ عَرْضٍ مُتَقَدِّمٍ وَاضِحٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَقْدِيمِ عَرْضٍ مُتَقَدِّمٍ وَاضِحٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَقْدِيمِ عَرْضٍ مُتَقَدِّمٍ وَاضِحٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", focus: "Membangun persuasive flow. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَقْدِيمِ", "عَرْضٍ", "مُتَقَدِّمٍ"], indonesianExplanation: "Saat menerapkan delivering an advanced presentation, Setelah itu, saya akan membangun alur persuasif langkah demi langkah." },
    { coach: "استخدم الفكرة: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", hint: "Jawab dengan struktur C1 memakai: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", sampleAnswer: "الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", focus: "Memakai transisi presisi. Pakai sebagai penghubung dalam delivering an advanced presentation.", expectedKeywords: ["الِانْتِقَالُ", "الْأَدَقُّ", "هُنَا", "هُوَ", "أَنْ"], indonesianExplanation: "Transisi yang lebih tepat di sini adalah berpindah dari sebab ke dampak." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", focus: "Menjawab pertanyaan menantang. Gunakan untuk repair dalam delivering an advanced presentation.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika ada pertanyaan sulit, saya akan mengakui batas jawaban lalu menjelaskan dasarnya." },
  ],
  "arabic-c1-aligning-stakeholders": [
    { coach: "كَيْفَ تُطَبِّقُ هَذِهِ الْمَهَارَةَ فِي حِوَارٍ رَسْمِيٍّ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ مُوَاءَمَةِ أَصْحَابِ الْمَصْلَحَةِ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", sampleAnswer: "فِي مَهَارَةِ مُوَاءَمَةِ أَصْحَابِ الْمَصْلَحَةِ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", focus: "Menyelaraskan stakeholder. Fokus lesson: aligning stakeholders.", expectedKeywords: ["فِي", "مَهَارَةِ", "مُوَاءَمَةِ", "أَصْحَابِ", "الْمَصْلَحَةِ،"], indonesianExplanation: "Dalam skill aligning stakeholders, Pertama kita perlu menyatukan pemahaman pihak-pihak utama." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ مُوَاءَمَةِ أَصْحَابِ الْمَصْلَحَةِ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ مُوَاءَمَةِ أَصْحَابِ الْمَصْلَحَةِ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", sampleAnswer: "عِنْدَ تَطْبِيقِ مُوَاءَمَةِ أَصْحَابِ الْمَصْلَحَةِ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", focus: "Mengelola ekspektasi. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "مُوَاءَمَةِ", "أَصْحَابِ", "الْمَصْلَحَةِ،"], indonesianExplanation: "Saat menerapkan aligning stakeholders, Lebih baik kita mengelola ekspektasi sebelum menjanjikan sesuatu yang spesifik." },
    { coach: "استخدم الفكرة: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", hint: "Jawab dengan struktur C1 memakai: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", focus: "Memberi feedback sensitif. Pakai sebagai penghubung dalam aligning stakeholders.", expectedKeywords: ["سَأُقَدِّمُ", "هَذِهِ", "الْمُلَاحَظَةَ", "بِحَسَاسِيَّةٍ،", "لِأَنَّ"], indonesianExplanation: "Saya akan menyampaikan feedback ini dengan sensitif karena topiknya penting." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", focus: "Mengomunikasikan risiko. Gunakan untuk repair dalam aligning stakeholders.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Ada risiko potensial, tetapi kita bisa menguranginya dengan rencana yang jelas." },
  ],
  "arabic-c1-asking-high-quality-follow-ups": [
    { coach: "كَيْفَ تُحَافِظُ عَلَى الْوُضُوحِ عِنْدَ وُجُودِ ضَغْطٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ طَرْحِ أَسْئِلَةِ مُتَابَعَةٍ عَالِيَةِ الْجَوْدَةِ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", sampleAnswer: "فِي مَهَارَةِ طَرْحِ أَسْئِلَةِ مُتَابَعَةٍ عَالِيَةِ الْجَوْدَةِ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", focus: "Menangkap implied meaning. Fokus lesson: asking high-quality follow-ups.", expectedKeywords: ["فِي", "مَهَارَةِ", "طَرْحِ", "أَسْئِلَةِ", "مُتَابَعَةٍ"], indonesianExplanation: "Dalam skill asking high-quality follow-ups, Makna tersiratnya di sini adalah pembicara belum sepenuhnya yakin." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ طَرْحِ أَسْئِلَةِ مُتَابَعَةٍ عَالِيَةِ الْجَوْدَةِ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ طَرْحِ أَسْئِلَةِ مُتَابَعَةٍ عَالِيَةِ الْجَوْدَةِ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ طَرْحِ أَسْئِلَةِ مُتَابَعَةٍ عَالِيَةِ الْجَوْدَةِ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", focus: "Merespons long turn. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "طَرْحِ", "أَسْئِلَةِ", "مُتَابَعَةٍ"], indonesianExplanation: "Saat menerapkan asking high-quality follow-ups, Saya akan menjawab poin utama dulu, lalu kembali ke detail." },
    { coach: "استخدم الفكرة: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", sampleAnswer: "إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", focus: "Merangkum yang didengar. Pakai sebagai penghubung dalam asking high-quality follow-ups.", expectedKeywords: ["إِذَا", "لَخَّصْتُ", "مَا", "سَمِعْتُهُ،", "فَالْفِكْرَةُ"], indonesianExplanation: "Jika saya merangkum apa yang saya dengar, ide utamanya adalah menunda keputusan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", focus: "Bertanya follow-up berkualitas. Gunakan untuk repair dalam asking high-quality follow-ups.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Pertanyaan follow-up terbaik adalah: apa yang akan mengubah keputusan ini?" },
  ],
  "arabic-c1-asking-tactful-questions": [
    { coach: "مَا الطَّرِيقَةُ الأَدَقُّ لِاسْتِخْدَامِ هَذِهِ الْمَهَارَةِ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ طَرْحِ أَسْئِلَةٍ لَبِقَةٍ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", sampleAnswer: "فِي مَهَارَةِ طَرْحِ أَسْئِلَةٍ لَبِقَةٍ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", focus: "Membaca konteks. Fokus lesson: asking tactful questions.", expectedKeywords: ["فِي", "مَهَارَةِ", "طَرْحِ", "أَسْئِلَةٍ", "لَبِقَةٍ،"], indonesianExplanation: "Dalam skill asking tactful questions, Sebelum merespons, kita harus membaca konteks dengan cermat." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ طَرْحِ أَسْئِلَةٍ لَبِقَةٍ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ طَرْحِ أَسْئِلَةٍ لَبِقَةٍ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", sampleAnswer: "عِنْدَ تَطْبِيقِ طَرْحِ أَسْئِلَةٍ لَبِقَةٍ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", focus: "Bertanya dengan halus. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "طَرْحِ", "أَسْئِلَةٍ", "لَبِقَةٍ،"], indonesianExplanation: "Saat menerapkan asking tactful questions, Bisakah saya bertanya dengan cara yang lebih tactful?" },
    { coach: "استخدم الفكرة: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", hint: "Jawab dengan struktur C1 memakai: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", sampleAnswer: "فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", focus: "Menjelaskan norma lokal. Pakai sebagai penghubung dalam asking tactful questions.", expectedKeywords: ["فِي", "بَلَدِي،", "هَذَا", "الْمِعْيَارُ", "يُفْهَمُ"], indonesianExplanation: "Di negara saya, norma ini dipahami dengan cara yang berbeda." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", focus: "Memperbaiki misunderstanding. Gunakan untuk repair dalam asking tactful questions.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Sepertinya ada salah paham, jadi mari kita merumuskan ulang idenya." },
  ],
  "arabic-c1-balancing-two-viewpoints": [
    { coach: "كَيْفَ تَجْعَلُ هَذَا الْجَوَابَ مُقْنِعًا وَمُتَوَازِنًا؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ الْمُوَازَنَةِ بَيْنَ وِجْهَتَيْ نَظَرٍ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", sampleAnswer: "فِي مَهَارَةِ الْمُوَازَنَةِ بَيْنَ وِجْهَتَيْ نَظَرٍ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", focus: "Menyampaikan opini dengan nuance. Fokus lesson: balancing two viewpoints.", expectedKeywords: ["فِي", "مَهَارَةِ", "الْمُوَازَنَةِ", "بَيْنَ", "وِجْهَتَيْ"], indonesianExplanation: "Dalam skill balancing two viewpoints, Secara prinsip, saya cenderung pada pendapat ini, tetapi saya punya satu catatan penting." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ الْمُوَازَنَةِ بَيْنَ وِجْهَتَيْ نَظَرٍ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ الْمُوَازَنَةِ بَيْنَ وِجْهَتَيْ نَظَرٍ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ الْمُوَازَنَةِ بَيْنَ وِجْهَتَيْ نَظَرٍ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", focus: "Menyatakan kepastian dan keraguan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "الْمُوَازَنَةِ", "بَيْنَ", "وِجْهَتَيْ"], indonesianExplanation: "Saat menerapkan balancing two viewpoints, Saya belum sepenuhnya yakin, tetapi bukti mengarah ke arah ini." },
    { coach: "استخدم الفكرة: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", hint: "Jawab dengan struktur C1 memakai: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", sampleAnswer: "مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", focus: "Menyeimbangkan dua sudut pandang. Pakai sebagai penghubung dalam balancing two viewpoints.", expectedKeywords: ["مِنْ", "جِهَةٍ،", "هَذَا", "الْخِيَارُ", "عَمَلِيٌّ،"], indonesianExplanation: "Di satu sisi opsi ini praktis, di sisi lain ia punya risiko yang jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", focus: "Melunakkan disagreement. Gunakan untuk repair dalam balancing two viewpoints.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saya menghargai sudut pandangmu, tetapi saya melihat masalah ini dari sisi lain." },
  ],
  "arabic-c1-building-a-persuasive-flow": [
    { coach: "مَا الطَّرِيقَةُ الأَدَقُّ لِاسْتِخْدَامِ هَذِهِ الْمَهَارَةِ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ بِنَاءِ تَسَلْسُلٍ إِقْنَاعِيٍّ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", sampleAnswer: "فِي مَهَارَةِ بِنَاءِ تَسَلْسُلٍ إِقْنَاعِيٍّ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", focus: "Membingkai topik kompleks. Fokus lesson: building a persuasive flow.", expectedKeywords: ["فِي", "مَهَارَةِ", "بِنَاءِ", "تَسَلْسُلٍ", "إِقْنَاعِيٍّ،"], indonesianExplanation: "Dalam skill building a persuasive flow, Saya akan membingkai topiknya dulu agar audiens memahami konteksnya." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ بِنَاءِ تَسَلْسُلٍ إِقْنَاعِيٍّ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ بِنَاءِ تَسَلْسُلٍ إِقْنَاعِيٍّ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", sampleAnswer: "عِنْدَ تَطْبِيقِ بِنَاءِ تَسَلْسُلٍ إِقْنَاعِيٍّ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", focus: "Membangun persuasive flow. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "بِنَاءِ", "تَسَلْسُلٍ", "إِقْنَاعِيٍّ،"], indonesianExplanation: "Saat menerapkan building a persuasive flow, Setelah itu, saya akan membangun alur persuasif langkah demi langkah." },
    { coach: "استخدم الفكرة: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", hint: "Jawab dengan struktur C1 memakai: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", sampleAnswer: "الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", focus: "Memakai transisi presisi. Pakai sebagai penghubung dalam building a persuasive flow.", expectedKeywords: ["الِانْتِقَالُ", "الْأَدَقُّ", "هُنَا", "هُوَ", "أَنْ"], indonesianExplanation: "Transisi yang lebih tepat di sini adalah berpindah dari sebab ke dampak." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", focus: "Menjawab pertanyaan menantang. Gunakan untuk repair dalam building a persuasive flow.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika ada pertanyaan sulit, saya akan mengakui batas jawaban lalu menjelaskan dasarnya." },
  ],
  "arabic-c1-c1-final-conversation": [
    { coach: "كَيْفَ تُحَوِّلُ هَذِهِ الْمَهَارَةَ إِلَى خُطْوَةٍ عَمَلِيَّةٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ إِدَارَةِ مُحَادَثَةٍ نِهَائِيَّةٍ مُتَكَامِلَةٍ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", sampleAnswer: "فِي مَهَارَةِ إِدَارَةِ مُحَادَثَةٍ نِهَائِيَّةٍ مُتَكَامِلَةٍ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", focus: "Review nuance. Fokus lesson: running a complete final conversation.", expectedKeywords: ["فِي", "مَهَارَةِ", "إِدَارَةِ", "مُحَادَثَةٍ", "نِهَائِيَّةٍ"], indonesianExplanation: "Dalam skill running a complete final conversation, Saya sedang mereview cara menyampaikan opini yang tepat tanpa berlebihan." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ إِدَارَةِ مُحَادَثَةٍ نِهَائِيَّةٍ مُتَكَامِلَةٍ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ إِدَارَةِ مُحَادَثَةٍ نِهَائِيَّةٍ مُتَكَامِلَةٍ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ إِدَارَةِ مُحَادَثَةٍ نِهَائِيَّةٍ مُتَكَامِلَةٍ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", focus: "Review strategy. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "إِدَارَةِ", "مُحَادَثَةٍ", "نِهَائِيَّةٍ"], indonesianExplanation: "Saat menerapkan running a complete final conversation, Dalam percakapan profesional, saya akan fokus pada konteks, ekspektasi, dan risiko." },
    { coach: "استخدم الفكرة: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", sampleAnswer: "عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", focus: "Review presenting and debate. Pakai sebagai penghubung dalam running a complete final conversation.", expectedKeywords: ["عِنْدَ", "الْعَرْضِ", "أَوِ", "النِّقَاشِ،", "سَأَبْنِي"], indonesianExplanation: "Saat presentasi atau diskusi, saya akan membangun ide dengan urutan yang persuasif." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", focus: "Review cross-cultural repair. Gunakan untuk repair dalam running a complete final conversation.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika muncul salah paham, saya akan memperbaikinya dengan tact dan kejelasan." },
  ],
  "arabic-c1-c1-final-test-practice": [
    { coach: "كَيْفَ تُحَافِظُ عَلَى الْوُضُوحِ عِنْدَ وُجُودِ ضَغْطٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَدْرِيبِ الِاخْتِبَارِ النِّهَائِيِّ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", sampleAnswer: "فِي مَهَارَةِ تَدْرِيبِ الِاخْتِبَارِ النِّهَائِيِّ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", focus: "Review nuance. Fokus lesson: practicing the final test.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَدْرِيبِ", "الِاخْتِبَارِ", "النِّهَائِيِّ،"], indonesianExplanation: "Dalam skill practicing the final test, Saya sedang mereview cara menyampaikan opini yang tepat tanpa berlebihan." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَدْرِيبِ الِاخْتِبَارِ النِّهَائِيِّ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَدْرِيبِ الِاخْتِبَارِ النِّهَائِيِّ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَدْرِيبِ الِاخْتِبَارِ النِّهَائِيِّ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", focus: "Review strategy. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَدْرِيبِ", "الِاخْتِبَارِ", "النِّهَائِيِّ،"], indonesianExplanation: "Saat menerapkan practicing the final test, Dalam percakapan profesional, saya akan fokus pada konteks, ekspektasi, dan risiko." },
    { coach: "استخدم الفكرة: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", sampleAnswer: "عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", focus: "Review presenting and debate. Pakai sebagai penghubung dalam practicing the final test.", expectedKeywords: ["عِنْدَ", "الْعَرْضِ", "أَوِ", "النِّقَاشِ،", "سَأَبْنِي"], indonesianExplanation: "Saat presentasi atau diskusi, saya akan membangun ide dengan urutan yang persuasif." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", focus: "Review cross-cultural repair. Gunakan untuk repair dalam practicing the final test.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika muncul salah paham, saya akan memperbaikinya dengan tact dan kejelasan." },
  ],
  "arabic-c1-catching-implied-meaning": [
    { coach: "كَيْفَ تُطَبِّقُ هَذِهِ الْمَهَارَةَ فِي حِوَارٍ رَسْمِيٍّ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ الْتِقَاطِ الْمَعْنَى الضِّمْنِيِّ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", sampleAnswer: "فِي مَهَارَةِ الْتِقَاطِ الْمَعْنَى الضِّمْنِيِّ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", focus: "Menangkap implied meaning. Fokus lesson: catching implied meaning.", expectedKeywords: ["فِي", "مَهَارَةِ", "الْتِقَاطِ", "الْمَعْنَى", "الضِّمْنِيِّ،"], indonesianExplanation: "Dalam skill catching implied meaning, Makna tersiratnya di sini adalah pembicara belum sepenuhnya yakin." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ الْتِقَاطِ الْمَعْنَى الضِّمْنِيِّ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ الْتِقَاطِ الْمَعْنَى الضِّمْنِيِّ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ الْتِقَاطِ الْمَعْنَى الضِّمْنِيِّ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", focus: "Merespons long turn. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "الْتِقَاطِ", "الْمَعْنَى", "الضِّمْنِيِّ،"], indonesianExplanation: "Saat menerapkan catching implied meaning, Saya akan menjawab poin utama dulu, lalu kembali ke detail." },
    { coach: "استخدم الفكرة: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", sampleAnswer: "إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", focus: "Merangkum yang didengar. Pakai sebagai penghubung dalam catching implied meaning.", expectedKeywords: ["إِذَا", "لَخَّصْتُ", "مَا", "سَمِعْتُهُ،", "فَالْفِكْرَةُ"], indonesianExplanation: "Jika saya merangkum apa yang saya dengar, ide utamanya adalah menunda keputusan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", focus: "Bertanya follow-up berkualitas. Gunakan untuk repair dalam catching implied meaning.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Pertanyaan follow-up terbaik adalah: apa yang akan mengubah keputusan ini?" },
  ],
  "arabic-c1-challenging-an-argument": [
    { coach: "مَا الطَّرِيقَةُ الأَدَقُّ لِاسْتِخْدَامِ هَذِهِ الْمَهَارَةِ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ مُنَاقَشَةِ حُجَّةٍ بِأَدَبٍ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", sampleAnswer: "فِي مَهَارَةِ مُنَاقَشَةِ حُجَّةٍ بِأَدَبٍ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", focus: "Mengidentifikasi asumsi. Fokus lesson: challenging an argument politely.", expectedKeywords: ["فِي", "مَهَارَةِ", "مُنَاقَشَةِ", "حُجَّةٍ", "بِأَدَبٍ،"], indonesianExplanation: "Dalam skill challenging an argument politely, Saya pikir asumsi dasarnya di sini belum disebutkan dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ مُنَاقَشَةِ حُجَّةٍ بِأَدَبٍ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ مُنَاقَشَةِ حُجَّةٍ بِأَدَبٍ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ مُنَاقَشَةِ حُجَّةٍ بِأَدَبٍ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", focus: "Menantang argumen. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "مُنَاقَشَةِ", "حُجَّةٍ", "بِأَدَبٍ،"], indonesianExplanation: "Saat menerapkan challenging an argument politely, Kita bisa menantang argumen ini dari sisi bukti." },
    { coach: "استخدم الفكرة: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", hint: "Jawab dengan struktur C1 memakai: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", sampleAnswer: "الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", focus: "Menyajikan evidence. Pakai sebagai penghubung dalam challenging an argument politely.", expectedKeywords: ["الدَّلِيلُ", "الْأَقْوَى", "هُوَ", "أَنَّ", "النَّتِيجَةَ"], indonesianExplanation: "Bukti paling kuat adalah bahwa hasilnya berulang dalam lebih dari satu konteks." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", focus: "Merespons under pressure. Gunakan untuk repair dalam challenging an argument politely.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Di bawah tekanan, saya akan fokus pada poin pusat dan tidak berpanjang-panjang." },
  ],
  "arabic-c1-coaching-with-questions": [
    { coach: "مَا الطَّرِيقَةُ الأَدَقُّ لِاسْتِخْدَامِ هَذِهِ الْمَهَارَةِ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ التَّوْجِيهِ بِالْأَسْئِلَةِ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", sampleAnswer: "فِي مَهَارَةِ التَّوْجِيهِ بِالْأَسْئِلَةِ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", focus: "Menetapkan direction. Fokus lesson: coaching with questions.", expectedKeywords: ["فِي", "مَهَارَةِ", "التَّوْجِيهِ", "بِالْأَسْئِلَةِ،", "أَوَّلُ"], indonesianExplanation: "Dalam skill coaching with questions, Hal pertama adalah menetapkan arah dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ التَّوْجِيهِ بِالْأَسْئِلَةِ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ التَّوْجِيهِ بِالْأَسْئِلَةِ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", sampleAnswer: "عِنْدَ تَطْبِيقِ التَّوْجِيهِ بِالْأَسْئِلَةِ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", focus: "Coaching dengan pertanyaan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "التَّوْجِيهِ", "بِالْأَسْئِلَةِ،", "بَدَلًا"], indonesianExplanation: "Saat menerapkan coaching with questions, Daripada memberi jawaban langsung, saya akan bertanya pertanyaan yang membuka pemikiran." },
    { coach: "استخدم الفكرة: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", hint: "Jawab dengan struktur C1 memakai: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", sampleAnswer: "الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", focus: "Memberi actionable feedback. Pakai sebagai penghubung dalam coaching with questions.", expectedKeywords: ["الْمُلَاحَظَةُ", "الْمُفِيدَةُ", "هِيَ", "الَّتِي", "تَتَحَوَّلُ"], indonesianExplanation: "Feedback yang berguna adalah yang berubah menjadi langkah yang dapat diterapkan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", focus: "Membimbing keputusan. Gunakan untuk repair dalam coaching with questions.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saat mengambil keputusan, kita harus menyeimbangkan kecepatan dan kualitas." },
  ],
  "arabic-c1-communicating-risk": [
    { coach: "كَيْفَ تُحَافِظُ عَلَى الْوُضُوحِ عِنْدَ وُجُودِ ضَغْطٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ شَرْحِ الْمَخَاطِرِ بِدُونِ تَهْوِيلٍ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", sampleAnswer: "فِي مَهَارَةِ شَرْحِ الْمَخَاطِرِ بِدُونِ تَهْوِيلٍ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", focus: "Menyelaraskan stakeholder. Fokus lesson: communicating risk without exaggeration.", expectedKeywords: ["فِي", "مَهَارَةِ", "شَرْحِ", "الْمَخَاطِرِ", "بِدُونِ"], indonesianExplanation: "Dalam skill communicating risk without exaggeration, Pertama kita perlu menyatukan pemahaman pihak-pihak utama." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ شَرْحِ الْمَخَاطِرِ بِدُونِ تَهْوِيلٍ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ شَرْحِ الْمَخَاطِرِ بِدُونِ تَهْوِيلٍ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", sampleAnswer: "عِنْدَ تَطْبِيقِ شَرْحِ الْمَخَاطِرِ بِدُونِ تَهْوِيلٍ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", focus: "Mengelola ekspektasi. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "شَرْحِ", "الْمَخَاطِرِ", "بِدُونِ"], indonesianExplanation: "Saat menerapkan communicating risk without exaggeration, Lebih baik kita mengelola ekspektasi sebelum menjanjikan sesuatu yang spesifik." },
    { coach: "استخدم الفكرة: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", hint: "Jawab dengan struktur C1 memakai: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", focus: "Memberi feedback sensitif. Pakai sebagai penghubung dalam communicating risk without exaggeration.", expectedKeywords: ["سَأُقَدِّمُ", "هَذِهِ", "الْمُلَاحَظَةَ", "بِحَسَاسِيَّةٍ،", "لِأَنَّ"], indonesianExplanation: "Saya akan menyampaikan feedback ini dengan sensitif karena topiknya penting." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", focus: "Mengomunikasikan risiko. Gunakan untuk repair dalam communicating risk without exaggeration.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Ada risiko potensial, tetapi kita bisa menguranginya dengan rencana yang jelas." },
  ],
  "arabic-c1-cross-cultural-mission": [
    { coach: "كَيْفَ تُحَوِّلُ هَذِهِ الْمَهَارَةَ إِلَى خُطْوَةٍ عَمَلِيَّةٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ إِدَارَةِ حِوَارٍ عَبْرَ الثَّقَافَاتِ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", sampleAnswer: "فِي مَهَارَةِ إِدَارَةِ حِوَارٍ عَبْرَ الثَّقَافَاتِ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", focus: "Membaca konteks. Fokus lesson: running a cross-cultural conversation.", expectedKeywords: ["فِي", "مَهَارَةِ", "إِدَارَةِ", "حِوَارٍ", "عَبْرَ"], indonesianExplanation: "Dalam skill running a cross-cultural conversation, Sebelum merespons, kita harus membaca konteks dengan cermat." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ إِدَارَةِ حِوَارٍ عَبْرَ الثَّقَافَاتِ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ إِدَارَةِ حِوَارٍ عَبْرَ الثَّقَافَاتِ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", sampleAnswer: "عِنْدَ تَطْبِيقِ إِدَارَةِ حِوَارٍ عَبْرَ الثَّقَافَاتِ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", focus: "Bertanya dengan halus. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "إِدَارَةِ", "حِوَارٍ", "عَبْرَ"], indonesianExplanation: "Saat menerapkan running a cross-cultural conversation, Bisakah saya bertanya dengan cara yang lebih tactful?" },
    { coach: "استخدم الفكرة: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", hint: "Jawab dengan struktur C1 memakai: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", sampleAnswer: "فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", focus: "Menjelaskan norma lokal. Pakai sebagai penghubung dalam running a cross-cultural conversation.", expectedKeywords: ["فِي", "بَلَدِي،", "هَذَا", "الْمِعْيَارُ", "يُفْهَمُ"], indonesianExplanation: "Di negara saya, norma ini dipahami dengan cara yang berbeda." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", focus: "Memperbaiki misunderstanding. Gunakan untuk repair dalam running a cross-cultural conversation.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Sepertinya ada salah paham, jadi mari kita merumuskan ulang idenya." },
  ],
  "arabic-c1-debate-analysis-mission": [
    { coach: "كَيْفَ تُحَوِّلُ هَذِهِ الْمَهَارَةَ إِلَى خُطْوَةٍ عَمَلِيَّةٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ إِدَارَةِ نِقَاشٍ تَحْلِيلِيٍّ مُتَوَازِنٍ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", sampleAnswer: "فِي مَهَارَةِ إِدَارَةِ نِقَاشٍ تَحْلِيلِيٍّ مُتَوَازِنٍ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", focus: "Mengidentifikasi asumsi. Fokus lesson: running a balanced analytical debate.", expectedKeywords: ["فِي", "مَهَارَةِ", "إِدَارَةِ", "نِقَاشٍ", "تَحْلِيلِيٍّ"], indonesianExplanation: "Dalam skill running a balanced analytical debate, Saya pikir asumsi dasarnya di sini belum disebutkan dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ إِدَارَةِ نِقَاشٍ تَحْلِيلِيٍّ مُتَوَازِنٍ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ إِدَارَةِ نِقَاشٍ تَحْلِيلِيٍّ مُتَوَازِنٍ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ إِدَارَةِ نِقَاشٍ تَحْلِيلِيٍّ مُتَوَازِنٍ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", focus: "Menantang argumen. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "إِدَارَةِ", "نِقَاشٍ", "تَحْلِيلِيٍّ"], indonesianExplanation: "Saat menerapkan running a balanced analytical debate, Kita bisa menantang argumen ini dari sisi bukti." },
    { coach: "استخدم الفكرة: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", hint: "Jawab dengan struktur C1 memakai: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", sampleAnswer: "الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", focus: "Menyajikan evidence. Pakai sebagai penghubung dalam running a balanced analytical debate.", expectedKeywords: ["الدَّلِيلُ", "الْأَقْوَى", "هُوَ", "أَنَّ", "النَّتِيجَةَ"], indonesianExplanation: "Bukti paling kuat adalah bahwa hasilnya berulang dalam lebih dari satu konteks." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", focus: "Merespons under pressure. Gunakan untuk repair dalam running a balanced analytical debate.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Di bawah tekanan, saya akan fokus pada poin pusat dan tidak berpanjang-panjang." },
  ],
  "arabic-c1-explaining-local-norms": [
    { coach: "كَيْفَ تَجْعَلُ هَذَا الْجَوَابَ مُقْنِعًا وَمُتَوَازِنًا؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ شَرْحِ الْأَعْرَافِ الْمَحَلِّيَّةِ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", sampleAnswer: "فِي مَهَارَةِ شَرْحِ الْأَعْرَافِ الْمَحَلِّيَّةِ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", focus: "Membaca konteks. Fokus lesson: explaining local norms.", expectedKeywords: ["فِي", "مَهَارَةِ", "شَرْحِ", "الْأَعْرَافِ", "الْمَحَلِّيَّةِ،"], indonesianExplanation: "Dalam skill explaining local norms, Sebelum merespons, kita harus membaca konteks dengan cermat." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ شَرْحِ الْأَعْرَافِ الْمَحَلِّيَّةِ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ شَرْحِ الْأَعْرَافِ الْمَحَلِّيَّةِ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", sampleAnswer: "عِنْدَ تَطْبِيقِ شَرْحِ الْأَعْرَافِ الْمَحَلِّيَّةِ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", focus: "Bertanya dengan halus. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "شَرْحِ", "الْأَعْرَافِ", "الْمَحَلِّيَّةِ،"], indonesianExplanation: "Saat menerapkan explaining local norms, Bisakah saya bertanya dengan cara yang lebih tactful?" },
    { coach: "استخدم الفكرة: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", hint: "Jawab dengan struktur C1 memakai: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", sampleAnswer: "فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", focus: "Menjelaskan norma lokal. Pakai sebagai penghubung dalam explaining local norms.", expectedKeywords: ["فِي", "بَلَدِي،", "هَذَا", "الْمِعْيَارُ", "يُفْهَمُ"], indonesianExplanation: "Di negara saya, norma ini dipahami dengan cara yang berbeda." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", focus: "Memperbaiki misunderstanding. Gunakan untuk repair dalam explaining local norms.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Sepertinya ada salah paham, jadi mari kita merumuskan ulang idenya." },
  ],
  "arabic-c1-expressing-certainty-and-doubt": [
    { coach: "مَا الطَّرِيقَةُ الأَدَقُّ لِاسْتِخْدَامِ هَذِهِ الْمَهَارَةِ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ التَّفْرِيقِ بَيْنَ الْيَقِينِ وَالشَّكِّ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", sampleAnswer: "فِي مَهَارَةِ التَّفْرِيقِ بَيْنَ الْيَقِينِ وَالشَّكِّ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", focus: "Menyampaikan opini dengan nuance. Fokus lesson: separating certainty and doubt.", expectedKeywords: ["فِي", "مَهَارَةِ", "التَّفْرِيقِ", "بَيْنَ", "الْيَقِينِ"], indonesianExplanation: "Dalam skill separating certainty and doubt, Secara prinsip, saya cenderung pada pendapat ini, tetapi saya punya satu catatan penting." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ التَّفْرِيقِ بَيْنَ الْيَقِينِ وَالشَّكِّ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ التَّفْرِيقِ بَيْنَ الْيَقِينِ وَالشَّكِّ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ التَّفْرِيقِ بَيْنَ الْيَقِينِ وَالشَّكِّ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", focus: "Menyatakan kepastian dan keraguan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "التَّفْرِيقِ", "بَيْنَ", "الْيَقِينِ"], indonesianExplanation: "Saat menerapkan separating certainty and doubt, Saya belum sepenuhnya yakin, tetapi bukti mengarah ke arah ini." },
    { coach: "استخدم الفكرة: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", hint: "Jawab dengan struktur C1 memakai: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", sampleAnswer: "مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", focus: "Menyeimbangkan dua sudut pandang. Pakai sebagai penghubung dalam separating certainty and doubt.", expectedKeywords: ["مِنْ", "جِهَةٍ،", "هَذَا", "الْخِيَارُ", "عَمَلِيٌّ،"], indonesianExplanation: "Di satu sisi opsi ini praktis, di sisi lain ia punya risiko yang jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", focus: "Melunakkan disagreement. Gunakan untuk repair dalam separating certainty and doubt.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saya menghargai sudut pandangmu, tetapi saya melihat masalah ini dari sisi lain." },
  ],
  "arabic-c1-framing-a-complex-topic": [
    { coach: "كَيْفَ تُطَبِّقُ هَذِهِ الْمَهَارَةَ فِي حِوَارٍ رَسْمِيٍّ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَأْطِيرِ مَوْضُوعٍ مُعَقَّدٍ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", sampleAnswer: "فِي مَهَارَةِ تَأْطِيرِ مَوْضُوعٍ مُعَقَّدٍ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", focus: "Membingkai topik kompleks. Fokus lesson: framing a complex topic.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَأْطِيرِ", "مَوْضُوعٍ", "مُعَقَّدٍ،"], indonesianExplanation: "Dalam skill framing a complex topic, Saya akan membingkai topiknya dulu agar audiens memahami konteksnya." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَأْطِيرِ مَوْضُوعٍ مُعَقَّدٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَأْطِيرِ مَوْضُوعٍ مُعَقَّدٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَأْطِيرِ مَوْضُوعٍ مُعَقَّدٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", focus: "Membangun persuasive flow. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَأْطِيرِ", "مَوْضُوعٍ", "مُعَقَّدٍ،"], indonesianExplanation: "Saat menerapkan framing a complex topic, Setelah itu, saya akan membangun alur persuasif langkah demi langkah." },
    { coach: "استخدم الفكرة: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", hint: "Jawab dengan struktur C1 memakai: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", sampleAnswer: "الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", focus: "Memakai transisi presisi. Pakai sebagai penghubung dalam framing a complex topic.", expectedKeywords: ["الِانْتِقَالُ", "الْأَدَقُّ", "هُنَا", "هُوَ", "أَنْ"], indonesianExplanation: "Transisi yang lebih tepat di sini adalah berpindah dari sebab ke dampak." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", focus: "Menjawab pertanyaan menantang. Gunakan untuk repair dalam framing a complex topic.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika ada pertanyaan sulit, saya akan mengakui batas jawaban lalu menjelaskan dasarnya." },
  ],
  "arabic-c1-giving-actionable-feedback": [
    { coach: "كَيْفَ تَجْعَلُ هَذَا الْجَوَابَ مُقْنِعًا وَمُتَوَازِنًا؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَقْدِيمِ تَغْذِيَةٍ رَاجِعَةٍ قَابِلَةٍ لِلْعَمَلِ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", sampleAnswer: "فِي مَهَارَةِ تَقْدِيمِ تَغْذِيَةٍ رَاجِعَةٍ قَابِلَةٍ لِلْعَمَلِ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", focus: "Menetapkan direction. Fokus lesson: giving actionable feedback.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَقْدِيمِ", "تَغْذِيَةٍ", "رَاجِعَةٍ"], indonesianExplanation: "Dalam skill giving actionable feedback, Hal pertama adalah menetapkan arah dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَقْدِيمِ تَغْذِيَةٍ رَاجِعَةٍ قَابِلَةٍ لِلْعَمَلِ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَقْدِيمِ تَغْذِيَةٍ رَاجِعَةٍ قَابِلَةٍ لِلْعَمَلِ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَقْدِيمِ تَغْذِيَةٍ رَاجِعَةٍ قَابِلَةٍ لِلْعَمَلِ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", focus: "Coaching dengan pertanyaan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَقْدِيمِ", "تَغْذِيَةٍ", "رَاجِعَةٍ"], indonesianExplanation: "Saat menerapkan giving actionable feedback, Daripada memberi jawaban langsung, saya akan bertanya pertanyaan yang membuka pemikiran." },
    { coach: "استخدم الفكرة: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", hint: "Jawab dengan struktur C1 memakai: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", sampleAnswer: "الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", focus: "Memberi actionable feedback. Pakai sebagai penghubung dalam giving actionable feedback.", expectedKeywords: ["الْمُلَاحَظَةُ", "الْمُفِيدَةُ", "هِيَ", "الَّتِي", "تَتَحَوَّلُ"], indonesianExplanation: "Feedback yang berguna adalah yang berubah menjadi langkah yang dapat diterapkan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", focus: "Membimbing keputusan. Gunakan untuk repair dalam giving actionable feedback.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saat mengambil keputusan, kita harus menyeimbangkan kecepatan dan kualitas." },
  ],
  "arabic-c1-guiding-a-decision": [
    { coach: "كَيْفَ تُحَافِظُ عَلَى الْوُضُوحِ عِنْدَ وُجُودِ ضَغْطٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَوْجِيهِ قَرَارٍ جَمَاعِيٍّ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", sampleAnswer: "فِي مَهَارَةِ تَوْجِيهِ قَرَارٍ جَمَاعِيٍّ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", focus: "Menetapkan direction. Fokus lesson: guiding a group decision.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَوْجِيهِ", "قَرَارٍ", "جَمَاعِيٍّ،"], indonesianExplanation: "Dalam skill guiding a group decision, Hal pertama adalah menetapkan arah dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَوْجِيهِ قَرَارٍ جَمَاعِيٍّ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَوْجِيهِ قَرَارٍ جَمَاعِيٍّ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَوْجِيهِ قَرَارٍ جَمَاعِيٍّ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", focus: "Coaching dengan pertanyaan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَوْجِيهِ", "قَرَارٍ", "جَمَاعِيٍّ،"], indonesianExplanation: "Saat menerapkan guiding a group decision, Daripada memberi jawaban langsung, saya akan bertanya pertanyaan yang membuka pemikiran." },
    { coach: "استخدم الفكرة: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", hint: "Jawab dengan struktur C1 memakai: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", sampleAnswer: "الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", focus: "Memberi actionable feedback. Pakai sebagai penghubung dalam guiding a group decision.", expectedKeywords: ["الْمُلَاحَظَةُ", "الْمُفِيدَةُ", "هِيَ", "الَّتِي", "تَتَحَوَّلُ"], indonesianExplanation: "Feedback yang berguna adalah yang berubah menjadi langkah yang dapat diterapkan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", focus: "Membimbing keputusan. Gunakan untuk repair dalam guiding a group decision.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saat mengambil keputusan, kita harus menyeimbangkan kecepatan dan kualitas." },
  ],
  "arabic-c1-handling-challenging-questions": [
    { coach: "كَيْفَ تُحَافِظُ عَلَى الْوُضُوحِ عِنْدَ وُجُودِ ضَغْطٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ التَّعَامُلِ مَعَ أَسْئِلَةٍ صَعْبَةٍ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", sampleAnswer: "فِي مَهَارَةِ التَّعَامُلِ مَعَ أَسْئِلَةٍ صَعْبَةٍ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", focus: "Membingkai topik kompleks. Fokus lesson: handling challenging questions.", expectedKeywords: ["فِي", "مَهَارَةِ", "التَّعَامُلِ", "مَعَ", "أَسْئِلَةٍ"], indonesianExplanation: "Dalam skill handling challenging questions, Saya akan membingkai topiknya dulu agar audiens memahami konteksnya." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ التَّعَامُلِ مَعَ أَسْئِلَةٍ صَعْبَةٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ التَّعَامُلِ مَعَ أَسْئِلَةٍ صَعْبَةٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", sampleAnswer: "عِنْدَ تَطْبِيقِ التَّعَامُلِ مَعَ أَسْئِلَةٍ صَعْبَةٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", focus: "Membangun persuasive flow. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "التَّعَامُلِ", "مَعَ", "أَسْئِلَةٍ"], indonesianExplanation: "Saat menerapkan handling challenging questions, Setelah itu, saya akan membangun alur persuasif langkah demi langkah." },
    { coach: "استخدم الفكرة: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", hint: "Jawab dengan struktur C1 memakai: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", sampleAnswer: "الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", focus: "Memakai transisi presisi. Pakai sebagai penghubung dalam handling challenging questions.", expectedKeywords: ["الِانْتِقَالُ", "الْأَدَقُّ", "هُنَا", "هُوَ", "أَنْ"], indonesianExplanation: "Transisi yang lebih tepat di sini adalah berpindah dari sebab ke dampak." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", focus: "Menjawab pertanyaan menantang. Gunakan untuk repair dalam handling challenging questions.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika ada pertanyaan sulit, saya akan mengakui batas jawaban lalu menjelaskan dasarnya." },
  ],
  "arabic-c1-handling-sensitive-feedback": [
    { coach: "كَيْفَ تَجْعَلُ هَذَا الْجَوَابَ مُقْنِعًا وَمُتَوَازِنًا؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَقْدِيمِ تَعْلِيقٍ حَسَّاسٍ بِلُطْفٍ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", sampleAnswer: "فِي مَهَارَةِ تَقْدِيمِ تَعْلِيقٍ حَسَّاسٍ بِلُطْفٍ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", focus: "Menyelaraskan stakeholder. Fokus lesson: handling sensitive feedback tactfully.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَقْدِيمِ", "تَعْلِيقٍ", "حَسَّاسٍ"], indonesianExplanation: "Dalam skill handling sensitive feedback tactfully, Pertama kita perlu menyatukan pemahaman pihak-pihak utama." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَقْدِيمِ تَعْلِيقٍ حَسَّاسٍ بِلُطْفٍ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَقْدِيمِ تَعْلِيقٍ حَسَّاسٍ بِلُطْفٍ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَقْدِيمِ تَعْلِيقٍ حَسَّاسٍ بِلُطْفٍ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", focus: "Mengelola ekspektasi. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَقْدِيمِ", "تَعْلِيقٍ", "حَسَّاسٍ"], indonesianExplanation: "Saat menerapkan handling sensitive feedback tactfully, Lebih baik kita mengelola ekspektasi sebelum menjanjikan sesuatu yang spesifik." },
    { coach: "استخدم الفكرة: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", hint: "Jawab dengan struktur C1 memakai: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", focus: "Memberi feedback sensitif. Pakai sebagai penghubung dalam handling sensitive feedback tactfully.", expectedKeywords: ["سَأُقَدِّمُ", "هَذِهِ", "الْمُلَاحَظَةَ", "بِحَسَاسِيَّةٍ،", "لِأَنَّ"], indonesianExplanation: "Saya akan menyampaikan feedback ini dengan sensitif karena topiknya penting." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", focus: "Mengomunikasikan risiko. Gunakan untuk repair dalam handling sensitive feedback tactfully.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Ada risiko potensial, tetapi kita bisa menguranginya dengan rencana yang jelas." },
  ],
  "arabic-c1-identifying-assumptions": [
    { coach: "كَيْفَ تُطَبِّقُ هَذِهِ الْمَهَارَةَ فِي حِوَارٍ رَسْمِيٍّ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَحْدِيدِ الِافْتِرَاضَاتِ الْخَفِيَّةِ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", sampleAnswer: "فِي مَهَارَةِ تَحْدِيدِ الِافْتِرَاضَاتِ الْخَفِيَّةِ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", focus: "Mengidentifikasi asumsi. Fokus lesson: identifying hidden assumptions.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَحْدِيدِ", "الِافْتِرَاضَاتِ", "الْخَفِيَّةِ،"], indonesianExplanation: "Dalam skill identifying hidden assumptions, Saya pikir asumsi dasarnya di sini belum disebutkan dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَحْدِيدِ الِافْتِرَاضَاتِ الْخَفِيَّةِ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَحْدِيدِ الِافْتِرَاضَاتِ الْخَفِيَّةِ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَحْدِيدِ الِافْتِرَاضَاتِ الْخَفِيَّةِ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", focus: "Menantang argumen. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَحْدِيدِ", "الِافْتِرَاضَاتِ", "الْخَفِيَّةِ،"], indonesianExplanation: "Saat menerapkan identifying hidden assumptions, Kita bisa menantang argumen ini dari sisi bukti." },
    { coach: "استخدم الفكرة: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", hint: "Jawab dengan struktur C1 memakai: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", sampleAnswer: "الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", focus: "Menyajikan evidence. Pakai sebagai penghubung dalam identifying hidden assumptions.", expectedKeywords: ["الدَّلِيلُ", "الْأَقْوَى", "هُوَ", "أَنَّ", "النَّتِيجَةَ"], indonesianExplanation: "Bukti paling kuat adalah bahwa hasilnya berulang dalam lebih dari satu konteks." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", focus: "Merespons under pressure. Gunakan untuk repair dalam identifying hidden assumptions.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Di bawah tekanan, saya akan fokus pada poin pusat dan tidak berpanjang-panjang." },
  ],
  "arabic-c1-leadership-coaching-mission": [
    { coach: "كَيْفَ تُحَوِّلُ هَذِهِ الْمَهَارَةَ إِلَى خُطْوَةٍ عَمَلِيَّةٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ إِدَارَةِ حِوَارٍ قِيَادِيٍّ تَوْجِيهِيٍّ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", sampleAnswer: "فِي مَهَارَةِ إِدَارَةِ حِوَارٍ قِيَادِيٍّ تَوْجِيهِيٍّ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", focus: "Menetapkan direction. Fokus lesson: running a leadership coaching conversation.", expectedKeywords: ["فِي", "مَهَارَةِ", "إِدَارَةِ", "حِوَارٍ", "قِيَادِيٍّ"], indonesianExplanation: "Dalam skill running a leadership coaching conversation, Hal pertama adalah menetapkan arah dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ إِدَارَةِ حِوَارٍ قِيَادِيٍّ تَوْجِيهِيٍّ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ إِدَارَةِ حِوَارٍ قِيَادِيٍّ تَوْجِيهِيٍّ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", sampleAnswer: "عِنْدَ تَطْبِيقِ إِدَارَةِ حِوَارٍ قِيَادِيٍّ تَوْجِيهِيٍّ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", focus: "Coaching dengan pertanyaan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "إِدَارَةِ", "حِوَارٍ", "قِيَادِيٍّ"], indonesianExplanation: "Saat menerapkan running a leadership coaching conversation, Daripada memberi jawaban langsung, saya akan bertanya pertanyaan yang membuka pemikiran." },
    { coach: "استخدم الفكرة: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", hint: "Jawab dengan struktur C1 memakai: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", sampleAnswer: "الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", focus: "Memberi actionable feedback. Pakai sebagai penghubung dalam running a leadership coaching conversation.", expectedKeywords: ["الْمُلَاحَظَةُ", "الْمُفِيدَةُ", "هِيَ", "الَّتِي", "تَتَحَوَّلُ"], indonesianExplanation: "Feedback yang berguna adalah yang berubah menjadi langkah yang dapat diterapkan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", focus: "Membimbing keputusan. Gunakan untuk repair dalam running a leadership coaching conversation.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saat mengambil keputusan, kita harus menyeimbangkan kecepatan dan kualitas." },
  ],
  "arabic-c1-managing-expectations": [
    { coach: "مَا الطَّرِيقَةُ الأَدَقُّ لِاسْتِخْدَامِ هَذِهِ الْمَهَارَةِ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ إِدَارَةِ التَّوَقُّعَاتِ الْوَاقِعِيَّةِ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", sampleAnswer: "فِي مَهَارَةِ إِدَارَةِ التَّوَقُّعَاتِ الْوَاقِعِيَّةِ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", focus: "Menyelaraskan stakeholder. Fokus lesson: managing realistic expectations.", expectedKeywords: ["فِي", "مَهَارَةِ", "إِدَارَةِ", "التَّوَقُّعَاتِ", "الْوَاقِعِيَّةِ،"], indonesianExplanation: "Dalam skill managing realistic expectations, Pertama kita perlu menyatukan pemahaman pihak-pihak utama." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ إِدَارَةِ التَّوَقُّعَاتِ الْوَاقِعِيَّةِ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ إِدَارَةِ التَّوَقُّعَاتِ الْوَاقِعِيَّةِ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", sampleAnswer: "عِنْدَ تَطْبِيقِ إِدَارَةِ التَّوَقُّعَاتِ الْوَاقِعِيَّةِ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", focus: "Mengelola ekspektasi. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "إِدَارَةِ", "التَّوَقُّعَاتِ", "الْوَاقِعِيَّةِ،"], indonesianExplanation: "Saat menerapkan managing realistic expectations, Lebih baik kita mengelola ekspektasi sebelum menjanjikan sesuatu yang spesifik." },
    { coach: "استخدم الفكرة: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", hint: "Jawab dengan struktur C1 memakai: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", focus: "Memberi feedback sensitif. Pakai sebagai penghubung dalam managing realistic expectations.", expectedKeywords: ["سَأُقَدِّمُ", "هَذِهِ", "الْمُلَاحَظَةَ", "بِحَسَاسِيَّةٍ،", "لِأَنَّ"], indonesianExplanation: "Saya akan menyampaikan feedback ini dengan sensitif karena topiknya penting." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", focus: "Mengomunikasikan risiko. Gunakan untuk repair dalam managing realistic expectations.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Ada risiko potensial, tetapi kita bisa menguranginya dengan rencana yang jelas." },
  ],
  "arabic-c1-nuanced-opinion-mission": [
    { coach: "كَيْفَ تُحَوِّلُ هَذِهِ الْمَهَارَةَ إِلَى خُطْوَةٍ عَمَلِيَّةٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَرْكِيبِ رَأْيٍ دَقِيقٍ مُتَكَامِلٍ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", sampleAnswer: "فِي مَهَارَةِ تَرْكِيبِ رَأْيٍ دَقِيقٍ مُتَكَامِلٍ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", focus: "Menyampaikan opini dengan nuance. Fokus lesson: building a complete nuanced opinion.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَرْكِيبِ", "رَأْيٍ", "دَقِيقٍ"], indonesianExplanation: "Dalam skill building a complete nuanced opinion, Secara prinsip, saya cenderung pada pendapat ini, tetapi saya punya satu catatan penting." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَرْكِيبِ رَأْيٍ دَقِيقٍ مُتَكَامِلٍ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَرْكِيبِ رَأْيٍ دَقِيقٍ مُتَكَامِلٍ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَرْكِيبِ رَأْيٍ دَقِيقٍ مُتَكَامِلٍ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", focus: "Menyatakan kepastian dan keraguan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَرْكِيبِ", "رَأْيٍ", "دَقِيقٍ"], indonesianExplanation: "Saat menerapkan building a complete nuanced opinion, Saya belum sepenuhnya yakin, tetapi bukti mengarah ke arah ini." },
    { coach: "استخدم الفكرة: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", hint: "Jawab dengan struktur C1 memakai: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", sampleAnswer: "مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", focus: "Menyeimbangkan dua sudut pandang. Pakai sebagai penghubung dalam building a complete nuanced opinion.", expectedKeywords: ["مِنْ", "جِهَةٍ،", "هَذَا", "الْخِيَارُ", "عَمَلِيٌّ،"], indonesianExplanation: "Di satu sisi opsi ini praktis, di sisi lain ia punya risiko yang jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", focus: "Melunakkan disagreement. Gunakan untuk repair dalam building a complete nuanced opinion.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saya menghargai sudut pandangmu, tetapi saya melihat masalah ini dari sisi lain." },
  ],
  "arabic-c1-presenting-evidence": [
    { coach: "كَيْفَ تَجْعَلُ هَذَا الْجَوَابَ مُقْنِعًا وَمُتَوَازِنًا؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَقْدِيمِ دَلِيلٍ مُرْتَبِطٍ بِالْمَوْضُوعِ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", sampleAnswer: "فِي مَهَارَةِ تَقْدِيمِ دَلِيلٍ مُرْتَبِطٍ بِالْمَوْضُوعِ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", focus: "Mengidentifikasi asumsi. Fokus lesson: presenting relevant evidence.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَقْدِيمِ", "دَلِيلٍ", "مُرْتَبِطٍ"], indonesianExplanation: "Dalam skill presenting relevant evidence, Saya pikir asumsi dasarnya di sini belum disebutkan dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَقْدِيمِ دَلِيلٍ مُرْتَبِطٍ بِالْمَوْضُوعِ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَقْدِيمِ دَلِيلٍ مُرْتَبِطٍ بِالْمَوْضُوعِ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَقْدِيمِ دَلِيلٍ مُرْتَبِطٍ بِالْمَوْضُوعِ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", focus: "Menantang argumen. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَقْدِيمِ", "دَلِيلٍ", "مُرْتَبِطٍ"], indonesianExplanation: "Saat menerapkan presenting relevant evidence, Kita bisa menantang argumen ini dari sisi bukti." },
    { coach: "استخدم الفكرة: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", hint: "Jawab dengan struktur C1 memakai: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", sampleAnswer: "الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", focus: "Menyajikan evidence. Pakai sebagai penghubung dalam presenting relevant evidence.", expectedKeywords: ["الدَّلِيلُ", "الْأَقْوَى", "هُوَ", "أَنَّ", "النَّتِيجَةَ"], indonesianExplanation: "Bukti paling kuat adalah bahwa hasilnya berulang dalam lebih dari satu konteks." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", focus: "Merespons under pressure. Gunakan untuk repair dalam presenting relevant evidence.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Di bawah tekanan, saya akan fokus pada poin pusat dan tidak berpanjang-panjang." },
  ],
  "arabic-c1-qualifying-your-opinion": [
    { coach: "كَيْفَ تُطَبِّقُ هَذِهِ الْمَهَارَةَ فِي حِوَارٍ رَسْمِيٍّ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَأْهِيلِ الرَّأْيِ قَبْلَ الْحُكْمِ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", sampleAnswer: "فِي مَهَارَةِ تَأْهِيلِ الرَّأْيِ قَبْلَ الْحُكْمِ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", focus: "Menyampaikan opini dengan nuance. Fokus lesson: qualifying opinion before making a claim.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَأْهِيلِ", "الرَّأْيِ", "قَبْلَ"], indonesianExplanation: "Dalam skill qualifying opinion before making a claim, Secara prinsip, saya cenderung pada pendapat ini, tetapi saya punya satu catatan penting." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَأْهِيلِ الرَّأْيِ قَبْلَ الْحُكْمِ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَأْهِيلِ الرَّأْيِ قَبْلَ الْحُكْمِ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَأْهِيلِ الرَّأْيِ قَبْلَ الْحُكْمِ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", focus: "Menyatakan kepastian dan keraguan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَأْهِيلِ", "الرَّأْيِ", "قَبْلَ"], indonesianExplanation: "Saat menerapkan qualifying opinion before making a claim, Saya belum sepenuhnya yakin, tetapi bukti mengarah ke arah ini." },
    { coach: "استخدم الفكرة: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", hint: "Jawab dengan struktur C1 memakai: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", sampleAnswer: "مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", focus: "Menyeimbangkan dua sudut pandang. Pakai sebagai penghubung dalam qualifying opinion before making a claim.", expectedKeywords: ["مِنْ", "جِهَةٍ،", "هَذَا", "الْخِيَارُ", "عَمَلِيٌّ،"], indonesianExplanation: "Di satu sisi opsi ini praktis, di sisi lain ia punya risiko yang jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", focus: "Melunakkan disagreement. Gunakan untuk repair dalam qualifying opinion before making a claim.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saya menghargai sudut pandangmu, tetapi saya melihat masalah ini dari sisi lain." },
  ],
  "arabic-c1-reading-context": [
    { coach: "كَيْفَ تُطَبِّقُ هَذِهِ الْمَهَارَةَ فِي حِوَارٍ رَسْمِيٍّ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ قِرَاءَةِ السِّيَاقِ الِاجْتِمَاعِيِّ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", sampleAnswer: "فِي مَهَارَةِ قِرَاءَةِ السِّيَاقِ الِاجْتِمَاعِيِّ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", focus: "Membaca konteks. Fokus lesson: reading social context.", expectedKeywords: ["فِي", "مَهَارَةِ", "قِرَاءَةِ", "السِّيَاقِ", "الِاجْتِمَاعِيِّ،"], indonesianExplanation: "Dalam skill reading social context, Sebelum merespons, kita harus membaca konteks dengan cermat." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ قِرَاءَةِ السِّيَاقِ الِاجْتِمَاعِيِّ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ قِرَاءَةِ السِّيَاقِ الِاجْتِمَاعِيِّ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", sampleAnswer: "عِنْدَ تَطْبِيقِ قِرَاءَةِ السِّيَاقِ الِاجْتِمَاعِيِّ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", focus: "Bertanya dengan halus. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "قِرَاءَةِ", "السِّيَاقِ", "الِاجْتِمَاعِيِّ،"], indonesianExplanation: "Saat menerapkan reading social context, Bisakah saya bertanya dengan cara yang lebih tactful?" },
    { coach: "استخدم الفكرة: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", hint: "Jawab dengan struktur C1 memakai: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", sampleAnswer: "فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", focus: "Menjelaskan norma lokal. Pakai sebagai penghubung dalam reading social context.", expectedKeywords: ["فِي", "بَلَدِي،", "هَذَا", "الْمِعْيَارُ", "يُفْهَمُ"], indonesianExplanation: "Di negara saya, norma ini dipahami dengan cara yang berbeda." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", focus: "Memperbaiki misunderstanding. Gunakan untuk repair dalam reading social context.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Sepertinya ada salah paham, jadi mari kita merumuskan ulang idenya." },
  ],
  "arabic-c1-repairing-misunderstanding": [
    { coach: "كَيْفَ تُحَافِظُ عَلَى الْوُضُوحِ عِنْدَ وُجُودِ ضَغْطٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ إِصْلَاحِ سُوءِ الْفَهْمِ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", sampleAnswer: "فِي مَهَارَةِ إِصْلَاحِ سُوءِ الْفَهْمِ، قَبْلَ أَنْ نَرُدَّ، يَجِبُ أَنْ نَقْرَأَ السِّيَاقَ بِدِقَّةٍ.", focus: "Membaca konteks. Fokus lesson: repairing misunderstanding.", expectedKeywords: ["فِي", "مَهَارَةِ", "إِصْلَاحِ", "سُوءِ", "الْفَهْمِ،"], indonesianExplanation: "Dalam skill repairing misunderstanding, Sebelum merespons, kita harus membaca konteks dengan cermat." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ إِصْلَاحِ سُوءِ الْفَهْمِ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ إِصْلَاحِ سُوءِ الْفَهْمِ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", sampleAnswer: "عِنْدَ تَطْبِيقِ إِصْلَاحِ سُوءِ الْفَهْمِ، هَلْ يُمْكِنُ أَنْ أَسْأَلَ بِطَرِيقَةٍ أَكْثَرَ لَبَاقَةً؟", focus: "Bertanya dengan halus. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "إِصْلَاحِ", "سُوءِ", "الْفَهْمِ،"], indonesianExplanation: "Saat menerapkan repairing misunderstanding, Bisakah saya bertanya dengan cara yang lebih tactful?" },
    { coach: "استخدم الفكرة: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", hint: "Jawab dengan struktur C1 memakai: فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", sampleAnswer: "فِي بَلَدِي، هَذَا الْمِعْيَارُ يُفْهَمُ بِطَرِيقَةٍ مُخْتَلِفَةٍ.", focus: "Menjelaskan norma lokal. Pakai sebagai penghubung dalam repairing misunderstanding.", expectedKeywords: ["فِي", "بَلَدِي،", "هَذَا", "الْمِعْيَارُ", "يُفْهَمُ"], indonesianExplanation: "Di negara saya, norma ini dipahami dengan cara yang berbeda." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يَبْدُو أَنَّ هُنَاكَ سُوءَ فَهْمٍ، فَدَعِينَا نُعِيدُ صِيَاغَةَ الْفِكْرَةِ.", focus: "Memperbaiki misunderstanding. Gunakan untuk repair dalam repairing misunderstanding.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Sepertinya ada salah paham, jadi mari kita merumuskan ulang idenya." },
  ],
  "arabic-c1-responding-to-long-turns": [
    { coach: "مَا الطَّرِيقَةُ الأَدَقُّ لِاسْتِخْدَامِ هَذِهِ الْمَهَارَةِ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ الرَّدِّ عَلَى كَلَامٍ طَوِيلٍ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", sampleAnswer: "فِي مَهَارَةِ الرَّدِّ عَلَى كَلَامٍ طَوِيلٍ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", focus: "Menangkap implied meaning. Fokus lesson: responding to long turns.", expectedKeywords: ["فِي", "مَهَارَةِ", "الرَّدِّ", "عَلَى", "كَلَامٍ"], indonesianExplanation: "Dalam skill responding to long turns, Makna tersiratnya di sini adalah pembicara belum sepenuhnya yakin." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ الرَّدِّ عَلَى كَلَامٍ طَوِيلٍ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ الرَّدِّ عَلَى كَلَامٍ طَوِيلٍ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ الرَّدِّ عَلَى كَلَامٍ طَوِيلٍ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", focus: "Merespons long turn. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "الرَّدِّ", "عَلَى", "كَلَامٍ"], indonesianExplanation: "Saat menerapkan responding to long turns, Saya akan menjawab poin utama dulu, lalu kembali ke detail." },
    { coach: "استخدم الفكرة: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", sampleAnswer: "إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", focus: "Merangkum yang didengar. Pakai sebagai penghubung dalam responding to long turns.", expectedKeywords: ["إِذَا", "لَخَّصْتُ", "مَا", "سَمِعْتُهُ،", "فَالْفِكْرَةُ"], indonesianExplanation: "Jika saya merangkum apa yang saya dengar, ide utamanya adalah menunda keputusan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", focus: "Bertanya follow-up berkualitas. Gunakan untuk repair dalam responding to long turns.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Pertanyaan follow-up terbaik adalah: apa yang akan mengubah keputusan ini?" },
  ],
  "arabic-c1-responding-under-pressure": [
    { coach: "كَيْفَ تُحَافِظُ عَلَى الْوُضُوحِ عِنْدَ وُجُودِ ضَغْطٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ الرَّدِّ تَحْتَ الضَّغْطِ بِهُدُوءٍ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", sampleAnswer: "فِي مَهَارَةِ الرَّدِّ تَحْتَ الضَّغْطِ بِهُدُوءٍ، أَعْتَقِدُ أَنَّ الِافْتِرَاضَ الْأَسَاسِيَّ هُنَا غَيْرُ مَذْكُورٍ بِوُضُوحٍ.", focus: "Mengidentifikasi asumsi. Fokus lesson: responding calmly under pressure.", expectedKeywords: ["فِي", "مَهَارَةِ", "الرَّدِّ", "تَحْتَ", "الضَّغْطِ"], indonesianExplanation: "Dalam skill responding calmly under pressure, Saya pikir asumsi dasarnya di sini belum disebutkan dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ الرَّدِّ تَحْتَ الضَّغْطِ بِهُدُوءٍ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ الرَّدِّ تَحْتَ الضَّغْطِ بِهُدُوءٍ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ الرَّدِّ تَحْتَ الضَّغْطِ بِهُدُوءٍ، يُمْكِنُنَا أَنْ نُحَدِّيَ هَذِهِ الْحُجَّةَ مِنْ جِهَةِ الْأَدِلَّةِ.", focus: "Menantang argumen. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "الرَّدِّ", "تَحْتَ", "الضَّغْطِ"], indonesianExplanation: "Saat menerapkan responding calmly under pressure, Kita bisa menantang argumen ini dari sisi bukti." },
    { coach: "استخدم الفكرة: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", hint: "Jawab dengan struktur C1 memakai: الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", sampleAnswer: "الدَّلِيلُ الْأَقْوَى هُوَ أَنَّ النَّتِيجَةَ تَكَرَّرَتْ فِي أَكْثَرَ مِنْ سِيَاقٍ.", focus: "Menyajikan evidence. Pakai sebagai penghubung dalam responding calmly under pressure.", expectedKeywords: ["الدَّلِيلُ", "الْأَقْوَى", "هُوَ", "أَنَّ", "النَّتِيجَةَ"], indonesianExplanation: "Bukti paling kuat adalah bahwa hasilnya berulang dalam lebih dari satu konteks." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، تَحْتَ الضَّغْطِ، سَأُرَكِّزُ عَلَى النُّقْطَةِ الْمَرْكَزِيَّةِ وَلَا أُطِيلُ.", focus: "Merespons under pressure. Gunakan untuk repair dalam responding calmly under pressure.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Di bawah tekanan, saya akan fokus pada poin pusat dan tidak berpanjang-panjang." },
  ],
  "arabic-c1-review-leadership-and-listening": [
    { coach: "كَيْفَ تَجْعَلُ هَذَا الْجَوَابَ مُقْنِعًا وَمُتَوَازِنًا؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ مُرَاجَعَةِ الْقِيَادَةِ وَحُسْنِ الِاسْتِمَاعِ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", sampleAnswer: "فِي مَهَارَةِ مُرَاجَعَةِ الْقِيَادَةِ وَحُسْنِ الِاسْتِمَاعِ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", focus: "Review nuance. Fokus lesson: reviewing leadership and listening.", expectedKeywords: ["فِي", "مَهَارَةِ", "مُرَاجَعَةِ", "الْقِيَادَةِ", "وَحُسْنِ"], indonesianExplanation: "Dalam skill reviewing leadership and listening, Saya sedang mereview cara menyampaikan opini yang tepat tanpa berlebihan." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ مُرَاجَعَةِ الْقِيَادَةِ وَحُسْنِ الِاسْتِمَاعِ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ مُرَاجَعَةِ الْقِيَادَةِ وَحُسْنِ الِاسْتِمَاعِ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ مُرَاجَعَةِ الْقِيَادَةِ وَحُسْنِ الِاسْتِمَاعِ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", focus: "Review strategy. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "مُرَاجَعَةِ", "الْقِيَادَةِ", "وَحُسْنِ"], indonesianExplanation: "Saat menerapkan reviewing leadership and listening, Dalam percakapan profesional, saya akan fokus pada konteks, ekspektasi, dan risiko." },
    { coach: "استخدم الفكرة: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", sampleAnswer: "عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", focus: "Review presenting and debate. Pakai sebagai penghubung dalam reviewing leadership and listening.", expectedKeywords: ["عِنْدَ", "الْعَرْضِ", "أَوِ", "النِّقَاشِ،", "سَأَبْنِي"], indonesianExplanation: "Saat presentasi atau diskusi, saya akan membangun ide dengan urutan yang persuasif." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", focus: "Review cross-cultural repair. Gunakan untuk repair dalam reviewing leadership and listening.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika muncul salah paham, saya akan memperbaikinya dengan tact dan kejelasan." },
  ],
  "arabic-c1-review-nuance-and-strategy": [
    { coach: "كَيْفَ تُطَبِّقُ هَذِهِ الْمَهَارَةَ فِي حِوَارٍ رَسْمِيٍّ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ مُرَاجَعَةِ الدِّقَّةِ وَالِاسْتِرَاتِيجِيَّةِ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", sampleAnswer: "فِي مَهَارَةِ مُرَاجَعَةِ الدِّقَّةِ وَالِاسْتِرَاتِيجِيَّةِ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", focus: "Review nuance. Fokus lesson: reviewing nuance and strategy.", expectedKeywords: ["فِي", "مَهَارَةِ", "مُرَاجَعَةِ", "الدِّقَّةِ", "وَالِاسْتِرَاتِيجِيَّةِ،"], indonesianExplanation: "Dalam skill reviewing nuance and strategy, Saya sedang mereview cara menyampaikan opini yang tepat tanpa berlebihan." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ مُرَاجَعَةِ الدِّقَّةِ وَالِاسْتِرَاتِيجِيَّةِ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ مُرَاجَعَةِ الدِّقَّةِ وَالِاسْتِرَاتِيجِيَّةِ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ مُرَاجَعَةِ الدِّقَّةِ وَالِاسْتِرَاتِيجِيَّةِ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", focus: "Review strategy. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "مُرَاجَعَةِ", "الدِّقَّةِ", "وَالِاسْتِرَاتِيجِيَّةِ،"], indonesianExplanation: "Saat menerapkan reviewing nuance and strategy, Dalam percakapan profesional, saya akan fokus pada konteks, ekspektasi, dan risiko." },
    { coach: "استخدم الفكرة: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", sampleAnswer: "عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", focus: "Review presenting and debate. Pakai sebagai penghubung dalam reviewing nuance and strategy.", expectedKeywords: ["عِنْدَ", "الْعَرْضِ", "أَوِ", "النِّقَاشِ،", "سَأَبْنِي"], indonesianExplanation: "Saat presentasi atau diskusi, saya akan membangun ide dengan urutan yang persuasif." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", focus: "Review cross-cultural repair. Gunakan untuk repair dalam reviewing nuance and strategy.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika muncul salah paham, saya akan memperbaikinya dengan tact dan kejelasan." },
  ],
  "arabic-c1-review-presenting-and-debate": [
    { coach: "مَا الطَّرِيقَةُ الأَدَقُّ لِاسْتِخْدَامِ هَذِهِ الْمَهَارَةِ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ مُرَاجَعَةِ الْعَرْضِ وَالنِّقَاشِ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", sampleAnswer: "فِي مَهَارَةِ مُرَاجَعَةِ الْعَرْضِ وَالنِّقَاشِ، أُرَاجِعُ الْآنَ كَيْفَ أُعَبِّرُ عَنْ رَأْيٍ دَقِيقٍ دُونَ مُبَالَغَةٍ.", focus: "Review nuance. Fokus lesson: reviewing presenting and debate.", expectedKeywords: ["فِي", "مَهَارَةِ", "مُرَاجَعَةِ", "الْعَرْضِ", "وَالنِّقَاشِ،"], indonesianExplanation: "Dalam skill reviewing presenting and debate, Saya sedang mereview cara menyampaikan opini yang tepat tanpa berlebihan." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ مُرَاجَعَةِ الْعَرْضِ وَالنِّقَاشِ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ مُرَاجَعَةِ الْعَرْضِ وَالنِّقَاشِ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ مُرَاجَعَةِ الْعَرْضِ وَالنِّقَاشِ، فِي الْحِوَارِ الْمِهَنِيِّ، سَأُرَكِّزُ عَلَى السِّيَاقِ وَالتَّوَقُّعَاتِ وَالْمَخَاطِرِ.", focus: "Review strategy. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "مُرَاجَعَةِ", "الْعَرْضِ", "وَالنِّقَاشِ،"], indonesianExplanation: "Saat menerapkan reviewing presenting and debate, Dalam percakapan profesional, saya akan fokus pada konteks, ekspektasi, dan risiko." },
    { coach: "استخدم الفكرة: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", sampleAnswer: "عِنْدَ الْعَرْضِ أَوِ النِّقَاشِ، سَأَبْنِي الْفِكْرَةَ بِتَسَلْسُلٍ مُقْنِعٍ.", focus: "Review presenting and debate. Pakai sebagai penghubung dalam reviewing presenting and debate.", expectedKeywords: ["عِنْدَ", "الْعَرْضِ", "أَوِ", "النِّقَاشِ،", "سَأَبْنِي"], indonesianExplanation: "Saat presentasi atau diskusi, saya akan membangun ide dengan urutan yang persuasif." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا ظَهَرَ سُوءُ فَهْمٍ، فَسَأُصْلِحُهُ بِلَبَاقَةٍ وَوُضُوحٍ.", focus: "Review cross-cultural repair. Gunakan untuk repair dalam reviewing presenting and debate.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika muncul salah paham, saya akan memperbaikinya dengan tact dan kejelasan." },
  ],
  "arabic-c1-setting-direction": [
    { coach: "كَيْفَ تُطَبِّقُ هَذِهِ الْمَهَارَةَ فِي حِوَارٍ رَسْمِيٍّ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَحْدِيدِ الِاتِّجَاهِ بِوُضُوحٍ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", sampleAnswer: "فِي مَهَارَةِ تَحْدِيدِ الِاتِّجَاهِ بِوُضُوحٍ، أَوَّلُ شَيْءٍ هُوَ تَحْدِيدُ الْمَسَارِ بِصُورَةٍ وَاضِحَةٍ.", focus: "Menetapkan direction. Fokus lesson: setting direction clearly.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَحْدِيدِ", "الِاتِّجَاهِ", "بِوُضُوحٍ،"], indonesianExplanation: "Dalam skill setting direction clearly, Hal pertama adalah menetapkan arah dengan jelas." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَحْدِيدِ الِاتِّجَاهِ بِوُضُوحٍ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَحْدِيدِ الِاتِّجَاهِ بِوُضُوحٍ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَحْدِيدِ الِاتِّجَاهِ بِوُضُوحٍ، بَدَلًا مِنْ أَنْ أُعْطِيَ جَوَابًا مُبَاشِرًا، سَأَسْأَلُ سُؤَالًا يُفَتِّحُ التَّفْكِيرَ.", focus: "Coaching dengan pertanyaan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَحْدِيدِ", "الِاتِّجَاهِ", "بِوُضُوحٍ،"], indonesianExplanation: "Saat menerapkan setting direction clearly, Daripada memberi jawaban langsung, saya akan bertanya pertanyaan yang membuka pemikiran." },
    { coach: "استخدم الفكرة: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", hint: "Jawab dengan struktur C1 memakai: الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", sampleAnswer: "الْمُلَاحَظَةُ الْمُفِيدَةُ هِيَ الَّتِي تَتَحَوَّلُ إِلَى خُطْوَةٍ قَابِلَةٍ لِلتَّطْبِيقِ.", focus: "Memberi actionable feedback. Pakai sebagai penghubung dalam setting direction clearly.", expectedKeywords: ["الْمُلَاحَظَةُ", "الْمُفِيدَةُ", "هِيَ", "الَّتِي", "تَتَحَوَّلُ"], indonesianExplanation: "Feedback yang berguna adalah yang berubah menjadi langkah yang dapat diterapkan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، عِنْدَ اتِّخَاذِ الْقَرَارِ، يَجِبُ أَنْ نُوَازِنَ بَيْنَ السُّرْعَةِ وَالْجَوْدَةِ.", focus: "Membimbing keputusan. Gunakan untuk repair dalam setting direction clearly.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saat mengambil keputusan, kita harus menyeimbangkan kecepatan dan kualitas." },
  ],
  "arabic-c1-softening-disagreement": [
    { coach: "كَيْفَ تُحَافِظُ عَلَى الْوُضُوحِ عِنْدَ وُجُودِ ضَغْطٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَلْطِيفِ الِاخْتِلَافِ مَعَ الْآخَرِينَ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", sampleAnswer: "فِي مَهَارَةِ تَلْطِيفِ الِاخْتِلَافِ مَعَ الْآخَرِينَ، مِنْ حَيْثُ الْمَبْدَأُ، أَمِيلُ إِلَى هَذَا الرَّأْيِ، وَلَكِنْ لَدَيَّ تَحَفُّظٌ مُهِمٌّ.", focus: "Menyampaikan opini dengan nuance. Fokus lesson: softening disagreement.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَلْطِيفِ", "الِاخْتِلَافِ", "مَعَ"], indonesianExplanation: "Dalam skill softening disagreement, Secara prinsip, saya cenderung pada pendapat ini, tetapi saya punya satu catatan penting." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَلْطِيفِ الِاخْتِلَافِ مَعَ الْآخَرِينَ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَلْطِيفِ الِاخْتِلَافِ مَعَ الْآخَرِينَ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَلْطِيفِ الِاخْتِلَافِ مَعَ الْآخَرِينَ، لَسْتُ مُتَيَقِّنًا تَمَامًا، لَكِنَّ الْأَدِلَّةَ تُشِيرُ إِلَى هَذَا الْمَسَارِ.", focus: "Menyatakan kepastian dan keraguan. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَلْطِيفِ", "الِاخْتِلَافِ", "مَعَ"], indonesianExplanation: "Saat menerapkan softening disagreement, Saya belum sepenuhnya yakin, tetapi bukti mengarah ke arah ini." },
    { coach: "استخدم الفكرة: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", hint: "Jawab dengan struktur C1 memakai: مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", sampleAnswer: "مِنْ جِهَةٍ، هَذَا الْخِيَارُ عَمَلِيٌّ، وَمِنْ جِهَةٍ أُخْرَى، لَهُ مَخَاطِرُ وَاضِحَةٌ.", focus: "Menyeimbangkan dua sudut pandang. Pakai sebagai penghubung dalam softening disagreement.", expectedKeywords: ["مِنْ", "جِهَةٍ،", "هَذَا", "الْخِيَارُ", "عَمَلِيٌّ،"], indonesianExplanation: "Di satu sisi opsi ini praktis, di sisi lain ia punya risiko yang jelas." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، أُقَدِّرُ وِجْهَةَ نَظَرِكَ، غَيْرَ أَنَّنِي أَرَى الْمَسْأَلَةَ مِنْ زَاوِيَةٍ أُخْرَى.", focus: "Melunakkan disagreement. Gunakan untuk repair dalam softening disagreement.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Saya menghargai sudut pandangmu, tetapi saya melihat masalah ini dari sisi lain." },
  ],
  "arabic-c1-strategic-workplace-mission": [
    { coach: "كَيْفَ تُحَوِّلُ هَذِهِ الْمَهَارَةَ إِلَى خُطْوَةٍ عَمَلِيَّةٍ؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ إِدَارَةِ حِوَارٍ مِهَنِيٍّ اِسْتِرَاتِيجِيٍّ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", sampleAnswer: "فِي مَهَارَةِ إِدَارَةِ حِوَارٍ مِهَنِيٍّ اِسْتِرَاتِيجِيٍّ، نَحْتَاجُ أَوَّلًا إِلَى تَوْحِيدِ فَهْمِ الْأَطْرَافِ الرَّئِيسِيَّةِ.", focus: "Menyelaraskan stakeholder. Fokus lesson: running a strategic workplace conversation.", expectedKeywords: ["فِي", "مَهَارَةِ", "إِدَارَةِ", "حِوَارٍ", "مِهَنِيٍّ"], indonesianExplanation: "Dalam skill running a strategic workplace conversation, Pertama kita perlu menyatukan pemahaman pihak-pihak utama." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ إِدَارَةِ حِوَارٍ مِهَنِيٍّ اِسْتِرَاتِيجِيٍّ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ إِدَارَةِ حِوَارٍ مِهَنِيٍّ اِسْتِرَاتِيجِيٍّ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", sampleAnswer: "عِنْدَ تَطْبِيقِ إِدَارَةِ حِوَارٍ مِهَنِيٍّ اِسْتِرَاتِيجِيٍّ، مِنَ الْأَفْضَلِ أَنْ نُدِيرَ التَّوَقُّعَاتِ قَبْلَ أَنْ نَعِدَ بِشَيْءٍ مُحَدَّدٍ.", focus: "Mengelola ekspektasi. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "إِدَارَةِ", "حِوَارٍ", "مِهَنِيٍّ"], indonesianExplanation: "Saat menerapkan running a strategic workplace conversation, Lebih baik kita mengelola ekspektasi sebelum menjanjikan sesuatu yang spesifik." },
    { coach: "استخدم الفكرة: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", hint: "Jawab dengan struktur C1 memakai: سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", sampleAnswer: "سَأُقَدِّمُ هَذِهِ الْمُلَاحَظَةَ بِحَسَاسِيَّةٍ، لِأَنَّ الْمَوْضُوعَ مُهِمٌّ.", focus: "Memberi feedback sensitif. Pakai sebagai penghubung dalam running a strategic workplace conversation.", expectedKeywords: ["سَأُقَدِّمُ", "هَذِهِ", "الْمُلَاحَظَةَ", "بِحَسَاسِيَّةٍ،", "لِأَنَّ"], indonesianExplanation: "Saya akan menyampaikan feedback ini dengan sensitif karena topiknya penting." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، يُوجَدُ خَطَرٌ مُحْتَمَلٌ، وَلَكِنْ يُمْكِنُنَا تَقْلِيلُهُ بِخُطَّةٍ وَاضِحَةٍ.", focus: "Mengomunikasikan risiko. Gunakan untuk repair dalam running a strategic workplace conversation.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Ada risiko potensial, tetapi kita bisa menguranginya dengan rencana yang jelas." },
  ],
  "arabic-c1-summarizing-what-you-heard": [
    { coach: "كَيْفَ تَجْعَلُ هَذَا الْجَوَابَ مُقْنِعًا وَمُتَوَازِنًا؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ تَلْخِيصِ مَا سَمِعْتَهُ بِدِقَّةٍ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", sampleAnswer: "فِي مَهَارَةِ تَلْخِيصِ مَا سَمِعْتَهُ بِدِقَّةٍ، الْمَعْنَى الضِّمْنِيُّ هُنَا هُوَ أَنَّ الْمُتَحَدِّثَ غَيْرُ مُتَأَكِّدٍ تَمَامًا.", focus: "Menangkap implied meaning. Fokus lesson: summarizing what you heard accurately.", expectedKeywords: ["فِي", "مَهَارَةِ", "تَلْخِيصِ", "مَا", "سَمِعْتَهُ"], indonesianExplanation: "Dalam skill summarizing what you heard accurately, Makna tersiratnya di sini adalah pembicara belum sepenuhnya yakin." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ تَلْخِيصِ مَا سَمِعْتَهُ بِدِقَّةٍ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ تَلْخِيصِ مَا سَمِعْتَهُ بِدِقَّةٍ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", sampleAnswer: "عِنْدَ تَطْبِيقِ تَلْخِيصِ مَا سَمِعْتَهُ بِدِقَّةٍ، سَأُجِيبُ أَوَّلًا عَلَى النُّقْطَةِ الْأَسَاسِيَّةِ، ثُمَّ أَعُودُ إِلَى التَّفَاصِيلِ.", focus: "Merespons long turn. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "تَلْخِيصِ", "مَا", "سَمِعْتَهُ"], indonesianExplanation: "Saat menerapkan summarizing what you heard accurately, Saya akan menjawab poin utama dulu, lalu kembali ke detail." },
    { coach: "استخدم الفكرة: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", hint: "Jawab dengan struktur C1 memakai: إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", sampleAnswer: "إِذَا لَخَّصْتُ مَا سَمِعْتُهُ، فَالْفِكْرَةُ الرَّئِيسِيَّةُ هِيَ تَأْخِيرُ الْقَرَارِ.", focus: "Merangkum yang didengar. Pakai sebagai penghubung dalam summarizing what you heard accurately.", expectedKeywords: ["إِذَا", "لَخَّصْتُ", "مَا", "سَمِعْتُهُ،", "فَالْفِكْرَةُ"], indonesianExplanation: "Jika saya merangkum apa yang saya dengar, ide utamanya adalah menunda keputusan." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، سُؤَالُ الْمُتَابَعَةِ الْأَفْضَلُ هُوَ: مَا الَّذِي سَيُغَيِّرُ هَذَا الْقَرَارَ؟", focus: "Bertanya follow-up berkualitas. Gunakan untuk repair dalam summarizing what you heard accurately.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Pertanyaan follow-up terbaik adalah: apa yang akan mengubah keputusan ini?" },
  ],
  "arabic-c1-using-precise-transitions": [
    { coach: "كَيْفَ تَجْعَلُ هَذَا الْجَوَابَ مُقْنِعًا وَمُتَوَازِنًا؟", hint: "Jawab dengan struktur C1 memakai: فِي مَهَارَةِ اِسْتِخْدَامِ اِنْتِقَالَاتٍ دَقِيقَةٍ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", sampleAnswer: "فِي مَهَارَةِ اِسْتِخْدَامِ اِنْتِقَالَاتٍ دَقِيقَةٍ، سَأُؤَطِّرُ الْمَوْضُوعَ أَوَّلًا حَتَّى يَفْهَمَ الْجُمْهُورُ سِيَاقَهُ.", focus: "Membingkai topik kompleks. Fokus lesson: using precise transitions.", expectedKeywords: ["فِي", "مَهَارَةِ", "اِسْتِخْدَامِ", "اِنْتِقَالَاتٍ", "دَقِيقَةٍ،"], indonesianExplanation: "Dalam skill using precise transitions, Saya akan membingkai topiknya dulu agar audiens memahami konteksnya." },
    { coach: "استخدم الفكرة: عِنْدَ تَطْبِيقِ اِسْتِخْدَامِ اِنْتِقَالَاتٍ دَقِيقَةٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", hint: "Jawab dengan struktur C1 memakai: عِنْدَ تَطْبِيقِ اِسْتِخْدَامِ اِنْتِقَالَاتٍ دَقِيقَةٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", sampleAnswer: "عِنْدَ تَطْبِيقِ اِسْتِخْدَامِ اِنْتِقَالَاتٍ دَقِيقَةٍ، بَعْدَ ذَلِكَ، سَأَبْنِي التَّسَلْسُلَ الْإِقْنَاعِيَّ خُطْوَةً فَخُطْوَةً.", focus: "Membangun persuasive flow. Hubungkan dengan fokus lesson.", expectedKeywords: ["عِنْدَ", "تَطْبِيقِ", "اِسْتِخْدَامِ", "اِنْتِقَالَاتٍ", "دَقِيقَةٍ،"], indonesianExplanation: "Saat menerapkan using precise transitions, Setelah itu, saya akan membangun alur persuasif langkah demi langkah." },
    { coach: "استخدم الفكرة: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", hint: "Jawab dengan struktur C1 memakai: الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", sampleAnswer: "الِانْتِقَالُ الْأَدَقُّ هُنَا هُوَ أَنْ نَنْتَقِلَ مِنَ السَّبَبِ إِلَى التَّأْثِيرِ.", focus: "Memakai transisi presisi. Pakai sebagai penghubung dalam using precise transitions.", expectedKeywords: ["الِانْتِقَالُ", "الْأَدَقُّ", "هُنَا", "هُوَ", "أَنْ"], indonesianExplanation: "Transisi yang lebih tepat di sini adalah berpindah dari sebab ke dampak." },
    { coach: "استخدم الفكرة: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", hint: "Jawab dengan struktur C1 memakai: إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", sampleAnswer: "إِذَا ظَهَرَ تَحَدٍّ فِي هَذِهِ الْمَهَارَةِ، إِذَا جَاءَ سُؤَالٌ صَعْبٌ، فَسَأَعْتَرِفُ بِحُدُودِ الْجَوَابِ ثُمَّ أُوَضِّحُ الْأَسَاسَ.", focus: "Menjawab pertanyaan menantang. Gunakan untuk repair dalam using precise transitions.", expectedKeywords: ["إِذَا", "ظَهَرَ", "تَحَدٍّ", "فِي", "هَذِهِ"], indonesianExplanation: "Jika muncul tantangan dalam skill ini, Jika ada pertanyaan sulit, saya akan mengakui batas jawaban lalu menjelaskan dasarnya." },
  ],
  "arabic-cafe-and-shop-mission": [
    { coach: "مَاذَا تُرِيدُ؟", hint: "Jawab dengan pola: أُرِيدُ مَاءً", sampleAnswer: "أُرِيدُ مَاءً", focus: "Latihan frasa: Saya ingin air.", expectedKeywords: ["أُرِيدُ", "مَاءً"], indonesianExplanation: "Saya ingin air." },
    { coach: "استخدم: كَمِ السِّعْرُ؟", hint: "Jawab dengan pola: كَمِ السِّعْرُ؟", sampleAnswer: "كَمِ السِّعْرُ؟", focus: "Latihan frasa: Berapa harganya?", expectedKeywords: ["كَمِ", "السِّعْرُ"], indonesianExplanation: "Berapa harganya?" },
    { coach: "استخدم: السِّعْرُ مُنَاسِبٌ", hint: "Jawab dengan pola: السِّعْرُ مُنَاسِبٌ", sampleAnswer: "السِّعْرُ مُنَاسِبٌ", focus: "Latihan frasa: Harganya cocok.", expectedKeywords: ["السِّعْرُ", "مُنَاسِبٌ"], indonesianExplanation: "Harganya cocok." },
  ],
  "arabic-checking-directions": [
    { coach: "عَفْوًا، كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ الثَّالِثِ؟", hint: "Jawab dengan pola: كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", sampleAnswer: "كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", focus: "Latihan frasa: Bagaimana saya pergi ke peron?", expectedKeywords: ["كَيْفَ", "أَذْهَبُ", "إِلَى"], indonesianExplanation: "Bagaimana saya pergi ke peron?" },
    { coach: "استخدم: اِمْشِ مُسْتَقِيمًا.", hint: "Jawab dengan pola: اِمْشِ مُسْتَقِيمًا.", sampleAnswer: "اِمْشِ مُسْتَقِيمًا.", focus: "Latihan frasa: Berjalan lurus.", expectedKeywords: ["اِمْشِ", "مُسْتَقِيمًا"], indonesianExplanation: "Berjalan lurus." },
    { coach: "استخدم: ثُمَّ اِتَّجِهْ يَمِينًا.", hint: "Jawab dengan pola: ثُمَّ اِتَّجِهْ يَمِينًا.", sampleAnswer: "ثُمَّ اِتَّجِهْ يَمِينًا.", focus: "Latihan frasa: Lalu belok kanan.", expectedKeywords: ["ثُمَّ", "اِتَّجِهْ", "يَمِينًا"], indonesianExplanation: "Lalu belok kanan." },
  ],
  "arabic-class-and-study-instructions": [
    { coach: "اِقرأِ الجملةَ.", hint: "Jawab bahwa kamu siap: نعم يا مُعَلِّم.", sampleAnswer: "نعم يا مُعَلِّم.", focus: "Respons sopan di kelas", expectedKeywords: ["نعم", "مُعَلِّم"], indonesianExplanation: "نعم يا مُعَلِّم adalah respons sopan kepada guru laki-laki." },
    { coach: "اِستمعْ ثم أَعِدْ.", hint: "Ulangi instruksi pendek ini.", sampleAnswer: "اِستمعْ ثم أَعِدْ.", focus: "Mengulangi instruksi", expectedKeywords: ["اِستمعْ", "أَعِدْ"], indonesianExplanation: "اِستمعْ berarti dengarkan, ثم berarti lalu, أَعِدْ berarti ulangilah." },
    { coach: "اُكتبِ الكلمةَ.", hint: "Jawab siap menulis.", sampleAnswer: "نعم، أكتبُ الكلمةَ.", focus: "Mengonfirmasi siap menulis", expectedKeywords: ["نعم", "أكتب", "الكلمة"], indonesianExplanation: "أكتب berarti saya menulis." },
  ],
  "arabic-comparing-simple-options": [
    { coach: "أُرِيدُ حَقِيبَةً صَغِيرَةً. أَيُّهُمَا أَفْضَلُ؟", hint: "Jawab dengan pola: هَذَا أَرْخَصُ.", sampleAnswer: "هَذَا أَرْخَصُ.", focus: "Latihan frasa: Ini lebih murah.", expectedKeywords: ["هَذَا", "أَرْخَصُ"], indonesianExplanation: "Ini lebih murah." },
    { coach: "استخدم: هَذَا أَجْوَدُ.", hint: "Jawab dengan pola: هَذَا أَجْوَدُ.", sampleAnswer: "هَذَا أَجْوَدُ.", focus: "Latihan frasa: Ini lebih bagus kualitasnya.", expectedKeywords: ["هَذَا", "أَجْوَدُ"], indonesianExplanation: "Ini lebih bagus kualitasnya." },
    { coach: "استخدم: أَيُّهُمَا أَفْضَلُ؟", hint: "Jawab dengan pola: أَيُّهُمَا أَفْضَلُ؟", sampleAnswer: "أَيُّهُمَا أَفْضَلُ؟", focus: "Latihan frasa: Mana yang lebih baik?", expectedKeywords: ["أَيُّهُمَا", "أَفْضَلُ"], indonesianExplanation: "Mana yang lebih baik?" },
  ],
  "arabic-confirming-appointment-details": [
    { coach: "مَرْحَبًا، أُرِيدُ أَنْ أُؤَكِّدَ الْمَوْعِدَ.", hint: "Jawab dengan pola: أُرِيدُ أَنْ أُؤَكِّدَ الْمَوْعِدَ.", sampleAnswer: "أُرِيدُ أَنْ أُؤَكِّدَ الْمَوْعِدَ.", focus: "Latihan frasa: Saya ingin mengonfirmasi janji.", expectedKeywords: ["أُرِيدُ", "أَنْ", "أُؤَكِّدَ"], indonesianExplanation: "Saya ingin mengonfirmasi janji." },
    { coach: "استخدم: هَلِ الْمَوْعِدُ غَدًا؟", hint: "Jawab dengan pola: هَلِ الْمَوْعِدُ غَدًا؟", sampleAnswer: "هَلِ الْمَوْعِدُ غَدًا؟", focus: "Latihan frasa: Apakah janjinya besok?", expectedKeywords: ["هَلِ", "الْمَوْعِدُ", "غَدًا"], indonesianExplanation: "Apakah janjinya besok?" },
    { coach: "استخدم: فِي أَيِّ طَابِقٍ؟", hint: "Jawab dengan pola: فِي أَيِّ طَابِقٍ؟", sampleAnswer: "فِي أَيِّ طَابِقٍ؟", focus: "Latihan frasa: Di lantai berapa?", expectedKeywords: ["فِي", "أَيِّ", "طَابِقٍ"], indonesianExplanation: "Di lantai berapa?" },
  ],
  "arabic-contact-details-mission": [
    { coach: "مَا اسْمُكَ؟", hint: "Jawab dengan pola: اِسْمِي ...", sampleAnswer: "اِسْمِي ...", focus: "Latihan frasa: Nama saya ...", expectedKeywords: ["اِسْمِي"], indonesianExplanation: "Nama saya ..." },
    { coach: "استخدم: أَكْتُبُ اسْمِي ...", hint: "Jawab dengan pola: أَكْتُبُ اسْمِي ...", sampleAnswer: "أَكْتُبُ اسْمِي ...", focus: "Latihan frasa: Saya menulis nama saya ...", expectedKeywords: ["أَكْتُبُ", "اسْمِي"], indonesianExplanation: "Saya menulis nama saya ..." },
    { coach: "استخدم: رَقْمِي ...", hint: "Jawab dengan pola: رَقْمِي ...", sampleAnswer: "رَقْمِي ...", focus: "Latihan frasa: Nomor saya ...", expectedKeywords: ["رَقْمِي"], indonesianExplanation: "Nomor saya ..." },
  ],
  "arabic-days-of-the-week": [
    { coach: "أي يَوْمَ الْيَوْمُ؟", hint: "Jawab dengan pola: أي يَوْمَ الْيَوْمُ؟", sampleAnswer: "أي يَوْمَ الْيَوْمُ؟", focus: "Latihan frasa: Hari apa hari ini?", expectedKeywords: ["أي", "يَوْمَ", "الْيَوْمُ"], indonesianExplanation: "Hari apa hari ini?" },
    { coach: "استخدم: الْيَوْمُ الْإِثْنَيْنِ", hint: "Jawab dengan pola: الْيَوْمُ الْإِثْنَيْنِ", sampleAnswer: "الْيَوْمُ الْإِثْنَيْنِ", focus: "Latihan frasa: Hari ini Senin.", expectedKeywords: ["الْيَوْمُ", "الْإِثْنَيْنِ"], indonesianExplanation: "Hari ini Senin." },
    { coach: "استخدم: غَدًا الثُّلَاثَاءُ", hint: "Jawab dengan pola: غَدًا الثُّلَاثَاءُ", sampleAnswer: "غَدًا الثُّلَاثَاءُ", focus: "Latihan frasa: Besok Selasa.", expectedKeywords: ["غَدًا", "الثُّلَاثَاءُ"], indonesianExplanation: "Besok Selasa." },
  ],
  "arabic-describing-a-simple-experience": [
    { coach: "كَيْفَ كَانَتْ رِحْلَتُكَ إِلَى الْحَدِيقَةِ؟", hint: "Jawab dengan pola: كَانَتِ التَّجْرِبَةُ جَيِّدَةً.", sampleAnswer: "كَانَتِ التَّجْرِبَةُ جَيِّدَةً.", focus: "Latihan frasa: Pengalamannya baik.", expectedKeywords: ["كَانَتِ", "التَّجْرِبَةُ", "جَيِّدَةً"], indonesianExplanation: "Pengalamannya baik." },
    { coach: "استخدم: رَأَيْتُ مَكَانًا جَمِيلًا.", hint: "Jawab dengan pola: رَأَيْتُ مَكَانًا جَمِيلًا.", sampleAnswer: "رَأَيْتُ مَكَانًا جَمِيلًا.", focus: "Latihan frasa: Saya melihat tempat yang indah.", expectedKeywords: ["رَأَيْتُ", "مَكَانًا", "جَمِيلًا"], indonesianExplanation: "Saya melihat tempat yang indah." },
    { coach: "استخدم: أَعْجَبَنِي الطَّعَامُ.", hint: "Jawab dengan pola: أَعْجَبَنِي الطَّعَامُ.", sampleAnswer: "أَعْجَبَنِي الطَّعَامُ.", focus: "Latihan frasa: Saya suka makanannya.", expectedKeywords: ["أَعْجَبَنِي", "الطَّعَامُ"], indonesianExplanation: "Saya suka makanannya." },
  ],
  "arabic-describing-simple-symptoms": [
    { coach: "عِنْدِي أَلَمٌ فِي الْحَلْقِ.", hint: "Jawab dengan pola: عِنْدِي أَلَمٌ فِي الْحَلْقِ.", sampleAnswer: "عِنْدِي أَلَمٌ فِي الْحَلْقِ.", focus: "Latihan frasa: Saya punya sakit di tenggorokan.", expectedKeywords: ["عِنْدِي", "أَلَمٌ", "فِي"], indonesianExplanation: "Saya punya sakit di tenggorokan." },
    { coach: "استخدم: لَدَيَّ سُعَالٌ خَفِيفٌ.", hint: "Jawab dengan pola: لَدَيَّ سُعَالٌ خَفِيفٌ.", sampleAnswer: "لَدَيَّ سُعَالٌ خَفِيفٌ.", focus: "Latihan frasa: Saya punya batuk ringan.", expectedKeywords: ["لَدَيَّ", "سُعَالٌ", "خَفِيفٌ"], indonesianExplanation: "Saya punya batuk ringan." },
    { coach: "استخدم: دَرَجَةُ حَرَارَتِي مُرْتَفِعَةٌ قَلِيلًا.", hint: "Jawab dengan pola: دَرَجَةُ حَرَارَتِي مُرْتَفِعَةٌ قَلِيلًا.", sampleAnswer: "دَرَجَةُ حَرَارَتِي مُرْتَفِعَةٌ قَلِيلًا.", focus: "Latihan frasa: Suhu badan saya sedikit tinggi.", expectedKeywords: ["دَرَجَةُ", "حَرَارَتِي", "مُرْتَفِعَةٌ"], indonesianExplanation: "Suhu badan saya sedikit tinggi." },
  ],
  "arabic-family-members": [
    { coach: "مَنْ هَذَا؟", hint: "Jawab dengan pola: مَنْ هَذَا؟", sampleAnswer: "مَنْ هَذَا؟", focus: "Latihan frasa: Siapa ini?", expectedKeywords: ["مَنْ", "هَذَا"], indonesianExplanation: "Siapa ini?" },
    { coach: "استخدم: هَذَا أَبِي", hint: "Jawab dengan pola: هَذَا أَبِي", sampleAnswer: "هَذَا أَبِي", focus: "Latihan frasa: Ini ayah saya.", expectedKeywords: ["هَذَا", "أَبِي"], indonesianExplanation: "Ini ayah saya." },
    { coach: "استخدم: هَذِهِ أُمِّي", hint: "Jawab dengan pola: هَذِهِ أُمِّي", sampleAnswer: "هَذِهِ أُمِّي", focus: "Latihan frasa: Ini ibu saya.", expectedKeywords: ["هَذِهِ", "أُمِّي"], indonesianExplanation: "Ini ibu saya." },
  ],
  "arabic-family-work-study-mission": [
    { coach: "حَدِّثِينِي عَنْ نَفْسِكِ.", hint: "Jawab dengan pola: هَذِهِ عَائِلَتِي", sampleAnswer: "هَذِهِ عَائِلَتِي", focus: "Latihan frasa: Ini keluarga saya.", expectedKeywords: ["هَذِهِ", "عَائِلَتِي"], indonesianExplanation: "Ini keluarga saya." },
    { coach: "استخدم: أَنَا طَالِبٌ", hint: "Jawab dengan pola: أَنَا طَالِبٌ", sampleAnswer: "أَنَا طَالِبٌ", focus: "Latihan frasa: Saya pelajar.", expectedKeywords: ["أَنَا", "طَالِبٌ"], indonesianExplanation: "Saya pelajar." },
    { coach: "استخدم: أَدْرُسُ الْعَرَبِيَّةَ", hint: "Jawab dengan pola: أَدْرُسُ الْعَرَبِيَّةَ", sampleAnswer: "أَدْرُسُ الْعَرَبِيَّةَ", focus: "Latihan frasa: Saya belajar bahasa Arab.", expectedKeywords: ["أَدْرُسُ", "الْعَرَبِيَّةَ"], indonesianExplanation: "Saya belajar bahasa Arab." },
  ],
  "arabic-finding-a-place-mission": [
    { coach: "إِلَى أَيْنَ تُرِيدُ أَنْ تَذْهَبَ؟", hint: "Jawab dengan pola: أَيْنَ الْفَصْلُ؟", sampleAnswer: "أَيْنَ الْفَصْلُ؟", focus: "Latihan frasa: Di mana kelas?", expectedKeywords: ["أَيْنَ", "الْفَصْلُ"], indonesianExplanation: "Di mana kelas?" },
    { coach: "استخدم: كَيْفَ أَذْهَبُ إِلَى الْفَصْلِ؟", hint: "Jawab dengan pola: كَيْفَ أَذْهَبُ إِلَى الْفَصْلِ؟", sampleAnswer: "كَيْفَ أَذْهَبُ إِلَى الْفَصْلِ؟", focus: "Latihan frasa: Bagaimana saya pergi ke kelas?", expectedKeywords: ["كَيْفَ", "أَذْهَبُ", "إِلَى"], indonesianExplanation: "Bagaimana saya pergi ke kelas?" },
    { coach: "استخدم: اِذْهَبْ يَمِينًا", hint: "Jawab dengan pola: اِذْهَبْ يَمِينًا", sampleAnswer: "اِذْهَبْ يَمِينًا", focus: "Latihan frasa: Pergi ke kanan.", expectedKeywords: ["اِذْهَبْ", "يَمِينًا"], indonesianExplanation: "Pergi ke kanan." },
  ],
  "arabic-formal-greetings": [
    { coach: "مرحبًا.", hint: "Jawab sapaan dengan أهلًا وسهلًا.", sampleAnswer: "أهلًا وسهلًا.", focus: "Menjawab sapaan", expectedKeywords: ["أهلًا", "وسهلًا"], indonesianExplanation: "Untuk membalas sapaan formal, gunakan أهلًا وسهلًا." },
    { coach: "كيف حالك اليوم؟", hint: "Jawab kabar dengan أنا بخير، شكرًا.", sampleAnswer: "أنا بخير، شكرًا.", focus: "Menjawab pertanyaan kabar", expectedKeywords: ["أنا", "بخير", "شكرًا"], indonesianExplanation: "Jawaban pendek yang sopan adalah أنا بخير، شكرًا." },
  ],
  "arabic-fusha-introduction-mission": [
    { coach: "مرحبًا. ما اسمُكَ؟", hint: "Balas sapaan dan sebutkan nama.", sampleAnswer: "مرحبًا. اسمي أحمد.", focus: "Sapaan dan nama", expectedKeywords: ["مرحبًا", "اسمي"], indonesianExplanation: "Gabungkan sapaan umum dengan اسمي untuk menyebut nama." },
    { coach: "من أين أنتَ؟", hint: "Sebutkan asal negara.", sampleAnswer: "أنا من إندونيسيا.", focus: "Asal negara", expectedKeywords: ["أنا", "من", "إندونيسيا"], indonesianExplanation: "أنا من إندونيسيا berarti saya dari Indonesia." },
    { coach: "اِقرأِ الجملةَ.", hint: "Kalau belum paham, katakan tidak paham dan minta pengulangan.", sampleAnswer: "عفوًا، لا أفهم. أَعِدْ مِنْ فَضْلِكَ.", focus: "Meminta bantuan", expectedKeywords: ["لا", "أفهم", "أَعِدْ", "فَضْلِكَ"], indonesianExplanation: "Ini frasa aman saat kamu belum mengerti instruksi." },
  ],
  "arabic-giving-simple-reasons": [
    { coach: "أَيُّ مَكَانٍ تُفَضِّلُ لِلدِّرَاسَةِ يَا رَامِي؟", hint: "Jawab dengan pola: أُحِبُّ هَذَا لِأَنَّهُ سَهْلٌ.", sampleAnswer: "أُحِبُّ هَذَا لِأَنَّهُ سَهْلٌ.", focus: "Latihan frasa: Saya suka ini karena mudah.", expectedKeywords: ["أُحِبُّ", "هَذَا", "لِأَنَّهُ"], indonesianExplanation: "Saya suka ini karena mudah." },
    { coach: "استخدم: أُفَضِّلُ هَذَا لِأَنَّهُ قَرِيبٌ.", hint: "Jawab dengan pola: أُفَضِّلُ هَذَا لِأَنَّهُ قَرِيبٌ.", sampleAnswer: "أُفَضِّلُ هَذَا لِأَنَّهُ قَرِيبٌ.", focus: "Latihan frasa: Saya lebih memilih ini karena dekat.", expectedKeywords: ["أُفَضِّلُ", "هَذَا", "لِأَنَّهُ"], indonesianExplanation: "Saya lebih memilih ini karena dekat." },
    { coach: "استخدم: هُوَ جَيِّدٌ، وَلَكِنَّهُ غَالٍ.", hint: "Jawab dengan pola: هُوَ جَيِّدٌ، وَلَكِنَّهُ غَالٍ.", sampleAnswer: "هُوَ جَيِّدٌ، وَلَكِنَّهُ غَالٍ.", focus: "Latihan frasa: Itu bagus, tetapi mahal.", expectedKeywords: ["هُوَ", "جَيِّدٌ،", "وَلَكِنَّهُ"], indonesianExplanation: "Itu bagus, tetapi mahal." },
  ],
  "arabic-health-appointment-mission": [
    { coach: "مَرْحَبًا، لَا أَشْعُرُ بِالرَّاحَةِ.", hint: "Jawab dengan pola: لَا أَشْعُرُ بِالرَّاحَةِ.", sampleAnswer: "لَا أَشْعُرُ بِالرَّاحَةِ.", focus: "Latihan frasa: Saya tidak merasa nyaman.", expectedKeywords: ["لَا", "أَشْعُرُ", "بِالرَّاحَةِ"], indonesianExplanation: "Saya tidak merasa nyaman." },
    { coach: "استخدم: عِنْدِي أَلَمٌ خَفِيفٌ.", hint: "Jawab dengan pola: عِنْدِي أَلَمٌ خَفِيفٌ.", sampleAnswer: "عِنْدِي أَلَمٌ خَفِيفٌ.", focus: "Latihan frasa: Saya punya sakit ringan.", expectedKeywords: ["عِنْدِي", "أَلَمٌ", "خَفِيفٌ"], indonesianExplanation: "Saya punya sakit ringan." },
    { coach: "استخدم: أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", hint: "Jawab dengan pola: أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", sampleAnswer: "أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", focus: "Latihan frasa: Saya ingin janji dengan dokter.", expectedKeywords: ["أُرِيدُ", "مَوْعِدًا", "مَعَ"], indonesianExplanation: "Saya ingin janji dengan dokter." },
  ],
  "arabic-help-and-problem-mission": [
    { coach: "اِقْرَئِي الْجُمْلَةَ.", hint: "Jawab dengan pola: لَا أَفْهَمُ", sampleAnswer: "لَا أَفْهَمُ", focus: "Latihan frasa: Saya tidak paham.", expectedKeywords: ["لَا", "أَفْهَمُ"], indonesianExplanation: "Saya tidak paham." },
    { coach: "استخدم: أَحْتَاجُ مُسَاعَدَةً", hint: "Jawab dengan pola: أَحْتَاجُ مُسَاعَدَةً", sampleAnswer: "أَحْتَاجُ مُسَاعَدَةً", focus: "Latihan frasa: Saya butuh bantuan.", expectedKeywords: ["أَحْتَاجُ", "مُسَاعَدَةً"], indonesianExplanation: "Saya butuh bantuan." },
    { coach: "استخدم: بِبُطْءٍ مِنْ فَضْلِكَ", hint: "Jawab dengan pola: بِبُطْءٍ مِنْ فَضْلِكَ", sampleAnswer: "بِبُطْءٍ مِنْ فَضْلِكَ", focus: "Latihan frasa: Pelan-pelan, tolong.", expectedKeywords: ["بِبُطْءٍ", "مِنْ", "فَضْلِكَ"], indonesianExplanation: "Pelan-pelan, tolong." },
  ],
  "arabic-invitation-mission": [
    { coach: "هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي الْيَوْمَ؟", hint: "Jawab dengan pola: هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", sampleAnswer: "هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", focus: "Latihan frasa: Apakah kamu ingin belajar bersama saya?", expectedKeywords: ["هَلْ", "تُرِيدُ", "أَنْ"], indonesianExplanation: "Apakah kamu ingin belajar bersama saya?" },
    { coach: "استخدم: لِأَنَّ الِاخْتِبَارَ قَرِيبٌ.", hint: "Jawab dengan pola: لِأَنَّ الِاخْتِبَارَ قَرِيبٌ.", sampleAnswer: "لِأَنَّ الِاخْتِبَارَ قَرِيبٌ.", focus: "Latihan frasa: Karena tesnya dekat.", expectedKeywords: ["لِأَنَّ", "الِاخْتِبَارَ", "قَرِيبٌ"], indonesianExplanation: "Karena tesnya dekat." },
    { coach: "استخدم: هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", hint: "Jawab dengan pola: هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", sampleAnswer: "هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", focus: "Latihan frasa: Bisakah kita mengubah jadwalnya?", expectedKeywords: ["هَلْ", "يُمْكِنُ", "أَنْ"], indonesianExplanation: "Bisakah kita mengubah jadwalnya?" },
  ],
  "arabic-inviting-someone": [
    { coach: "هَلْ تُرِيدِينَ أَنْ تَدْرُسِي مَعِي الْيَوْمَ؟", hint: "Jawab dengan pola: هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", sampleAnswer: "هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", focus: "Latihan frasa: Apakah kamu ingin belajar bersama saya?", expectedKeywords: ["هَلْ", "تُرِيدُ", "أَنْ"], indonesianExplanation: "Apakah kamu ingin belajar bersama saya?" },
    { coach: "استخدم: لِأَنَّ الدَّرْسَ مُهِمٌّ.", hint: "Jawab dengan pola: لِأَنَّ الدَّرْسَ مُهِمٌّ.", sampleAnswer: "لِأَنَّ الدَّرْسَ مُهِمٌّ.", focus: "Latihan frasa: Karena pelajarannya penting.", expectedKeywords: ["لِأَنَّ", "الدَّرْسَ", "مُهِمٌّ"], indonesianExplanation: "Karena pelajarannya penting." },
    { coach: "استخدم: فِكْرَةٌ جَيِّدَةٌ.", hint: "Jawab dengan pola: فِكْرَةٌ جَيِّدَةٌ.", sampleAnswer: "فِكْرَةٌ جَيِّدَةٌ.", focus: "Latihan frasa: Ide yang bagus.", expectedKeywords: ["فِكْرَةٌ", "جَيِّدَةٌ"], indonesianExplanation: "Ide yang bagus." },
  ],
  "arabic-likes-and-ability": [
    { coach: "مَاذَا تُحِبِّينَ؟", hint: "Jawab dengan pola: أُحِبُّ الْقِرَاءَةَ", sampleAnswer: "أُحِبُّ الْقِرَاءَةَ", focus: "Latihan frasa: Saya suka membaca.", expectedKeywords: ["أُحِبُّ", "الْقِرَاءَةَ"], indonesianExplanation: "Saya suka membaca." },
    { coach: "استخدم: لَا أُحِبُّ الِانْتِظَارَ", hint: "Jawab dengan pola: لَا أُحِبُّ الِانْتِظَارَ", sampleAnswer: "لَا أُحِبُّ الِانْتِظَارَ", focus: "Latihan frasa: Saya tidak suka menunggu.", expectedKeywords: ["لَا", "أُحِبُّ", "الِانْتِظَارَ"], indonesianExplanation: "Saya tidak suka menunggu." },
    { coach: "استخدم: أَسْتَطِيعُ الْقِرَاءَةَ", hint: "Jawab dengan pola: أَسْتَطِيعُ الْقِرَاءَةَ", sampleAnswer: "أَسْتَطِيعُ الْقِرَاءَةَ", focus: "Latihan frasa: Saya bisa membaca.", expectedKeywords: ["أَسْتَطِيعُ", "الْقِرَاءَةَ"], indonesianExplanation: "Saya bisa membaca." },
  ],
  "arabic-making-a-simple-plan": [
    { coach: "سَأَذْهَبُ إِلَى الْمَكْتَبَةِ بَعْدَ الدَّرْسِ.", hint: "Jawab dengan pola: سَأَذْهَبُ إِلَى الْمَكْتَبَةِ.", sampleAnswer: "سَأَذْهَبُ إِلَى الْمَكْتَبَةِ.", focus: "Latihan frasa: Saya akan pergi ke perpustakaan.", expectedKeywords: ["سَأَذْهَبُ", "إِلَى", "الْمَكْتَبَةِ"], indonesianExplanation: "Saya akan pergi ke perpustakaan." },
    { coach: "استخدم: هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي؟", hint: "Jawab dengan pola: هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي؟", sampleAnswer: "هَلْ تُرِيدُ أَنْ تَذْهَبَ مَعِي؟", focus: "Latihan frasa: Apakah kamu ingin pergi bersama saya?", expectedKeywords: ["هَلْ", "تُرِيدُ", "أَنْ"], indonesianExplanation: "Apakah kamu ingin pergi bersama saya?" },
    { coach: "استخدم: مَتَى نَلْتَقِي؟", hint: "Jawab dengan pola: مَتَى نَلْتَقِي؟", sampleAnswer: "مَتَى نَلْتَقِي؟", focus: "Latihan frasa: Kapan kita bertemu?", expectedKeywords: ["مَتَى", "نَلْتَقِي"], indonesianExplanation: "Kapan kita bertemu?" },
  ],
  "arabic-making-an-appointment": [
    { coach: "مَرْحَبًا، أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", hint: "Jawab dengan pola: أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", sampleAnswer: "أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", focus: "Latihan frasa: Saya ingin janji dengan dokter.", expectedKeywords: ["أُرِيدُ", "مَوْعِدًا", "مَعَ"], indonesianExplanation: "Saya ingin janji dengan dokter." },
    { coach: "استخدم: هَلْ يُوجَدُ مَوْعِدٌ غَدًا؟", hint: "Jawab dengan pola: هَلْ يُوجَدُ مَوْعِدٌ غَدًا؟", sampleAnswer: "هَلْ يُوجَدُ مَوْعِدٌ غَدًا؟", focus: "Latihan frasa: Apakah ada janji besok?", expectedKeywords: ["هَلْ", "يُوجَدُ", "مَوْعِدٌ"], indonesianExplanation: "Apakah ada janji besok?" },
    { coach: "استخدم: صَبَاحًا أَمْ مَسَاءً؟", hint: "Jawab dengan pola: صَبَاحًا أَمْ مَسَاءً؟", sampleAnswer: "صَبَاحًا أَمْ مَسَاءً؟", focus: "Latihan frasa: Pagi atau sore?", expectedKeywords: ["صَبَاحًا", "أَمْ", "مَسَاءً"], indonesianExplanation: "Pagi atau sore?" },
  ],
  "arabic-making-simple-requests": [
    { coach: "اِفْتَحِ الْكِتَابَ مِنْ فَضْلِكَ.", hint: "Jawab dengan pola: اِفْتَحِ الْكِتَابَ", sampleAnswer: "اِفْتَحِ الْكِتَابَ", focus: "Latihan frasa: Buka bukunya.", expectedKeywords: ["اِفْتَحِ", "الْكِتَابَ"], indonesianExplanation: "Buka bukunya." },
    { coach: "استخدم: اُكْتُبِ الْجُمْلَةَ", hint: "Jawab dengan pola: اُكْتُبِ الْجُمْلَةَ", sampleAnswer: "اُكْتُبِ الْجُمْلَةَ", focus: "Latihan frasa: Tulis kalimatnya.", expectedKeywords: ["اُكْتُبِ", "الْجُمْلَةَ"], indonesianExplanation: "Tulis kalimatnya." },
    { coach: "استخدم: اِسْتَمِعْ", hint: "Jawab dengan pola: اِسْتَمِعْ", sampleAnswer: "اِسْتَمِعْ", focus: "Latihan frasa: Dengarkan.", expectedKeywords: ["اِسْتَمِعْ"], indonesianExplanation: "Dengarkan." },
  ],
  "arabic-name-and-origin": [
    { coach: "ما اسمُكَ؟", hint: "Jawab dengan اسمي + nama.", sampleAnswer: "اسمي أحمد.", focus: "Menyebutkan nama", expectedKeywords: ["اسمي"], indonesianExplanation: "Gunakan اسمي untuk mengatakan nama saya." },
    { coach: "من أين أنتَ؟", hint: "Jawab dengan أنا من إندونيسيا.", sampleAnswer: "أنا من إندونيسيا.", focus: "Menyebutkan asal", expectedKeywords: ["أنا", "من", "إندونيسيا"], indonesianExplanation: "Gunakan أنا من untuk mengatakan asal." },
    { coach: "وأنتَ؟", hint: "Tanyakan balik dengan من أين أنتَ؟", sampleAnswer: "من أين أنتَ؟", focus: "Bertanya balik", expectedKeywords: ["من", "أين", "أنت"], indonesianExplanation: "Untuk bertanya balik, gunakan من أين أنتَ؟" },
  ],
  "arabic-numbers-and-phone": [
    { coach: "مَا رَقْمُ هَاتِفِكَ؟", hint: "Jawab dengan pola: مَا رَقْمُ هَاتِفِكَ؟", sampleAnswer: "مَا رَقْمُ هَاتِفِكَ؟", focus: "Latihan frasa: Berapa nomor teleponmu?", expectedKeywords: ["مَا", "رَقْمُ", "هَاتِفِكَ"], indonesianExplanation: "Berapa nomor teleponmu?" },
    { coach: "استخدم: رَقْمِي ...", hint: "Jawab dengan pola: رَقْمِي ...", sampleAnswer: "رَقْمِي ...", focus: "Latihan frasa: Nomor saya ...", expectedKeywords: ["رَقْمِي"], indonesianExplanation: "Nomor saya ..." },
    { coach: "استخدم: وَاحِدٌ، اِثْنَانِ، ثَلَاثَةٌ", hint: "Jawab dengan pola: وَاحِدٌ، اِثْنَانِ، ثَلَاثَةٌ", sampleAnswer: "وَاحِدٌ، اِثْنَانِ، ثَلَاثَةٌ", focus: "Latihan frasa: Satu, dua, tiga", expectedKeywords: ["وَاحِدٌ،", "اِثْنَانِ،", "ثَلَاثَةٌ"], indonesianExplanation: "Satu, dua, tiga" },
  ],
  "arabic-opinion-conversation-mission": [
    { coach: "مَا رَأْيُكَ فِي هَذِهِ الْخُطَّةِ يَا رَامِي؟", hint: "Jawab dengan pola: مَا رَأْيُكَ فِي هَذِهِ الْخُطَّةِ؟", sampleAnswer: "مَا رَأْيُكَ فِي هَذِهِ الْخُطَّةِ؟", focus: "Latihan frasa: Apa pendapatmu tentang rencana ini?", expectedKeywords: ["مَا", "رَأْيُكَ", "فِي"], indonesianExplanation: "Apa pendapatmu tentang rencana ini?" },
    { coach: "استخدم: أَعْتَقِدُ أَنَّهَا جَيِّدَةٌ.", hint: "Jawab dengan pola: أَعْتَقِدُ أَنَّهَا جَيِّدَةٌ.", sampleAnswer: "أَعْتَقِدُ أَنَّهَا جَيِّدَةٌ.", focus: "Latihan frasa: Saya pikir itu baik.", expectedKeywords: ["أَعْتَقِدُ", "أَنَّهَا", "جَيِّدَةٌ"], indonesianExplanation: "Saya pikir itu baik." },
    { coach: "استخدم: أُفَضِّلُ الصَّبَاحَ لِأَنَّهُ أَهْدَأُ.", hint: "Jawab dengan pola: أُفَضِّلُ الصَّبَاحَ لِأَنَّهُ أَهْدَأُ.", sampleAnswer: "أُفَضِّلُ الصَّبَاحَ لِأَنَّهُ أَهْدَأُ.", focus: "Latihan frasa: Saya lebih memilih pagi karena lebih tenang.", expectedKeywords: ["أُفَضِّلُ", "الصَّبَاحَ", "لِأَنَّهُ"], indonesianExplanation: "Saya lebih memilih pagi karena lebih tenang." },
  ],
  "arabic-ordering-a-drink": [
    { coach: "مَرْحَبًا.", hint: "Jawab dengan pola: أُرِيدُ مَاءً", sampleAnswer: "أُرِيدُ مَاءً", focus: "Latihan frasa: Saya ingin air.", expectedKeywords: ["أُرِيدُ", "مَاءً"], indonesianExplanation: "Saya ingin air." },
    { coach: "استخدم: أُرِيدُ قَهْوَةً", hint: "Jawab dengan pola: أُرِيدُ قَهْوَةً", sampleAnswer: "أُرِيدُ قَهْوَةً", focus: "Latihan frasa: Saya ingin kopi.", expectedKeywords: ["أُرِيدُ", "قَهْوَةً"], indonesianExplanation: "Saya ingin kopi." },
    { coach: "استخدم: من فضلك", hint: "Jawab dengan pola: من فضلك", sampleAnswer: "من فضلك", focus: "Latihan frasa: Tolong.", expectedKeywords: ["من", "فضلك"], indonesianExplanation: "Tolong." },
  ],
  "arabic-past-experience-mission": [
    { coach: "مَاذَا فَعَلْتَ فِي نِهَايَةِ الْأُسْبُوعِ يَا رَامِي؟", hint: "Jawab dengan pola: فِي نِهَايَةِ الْأُسْبُوعِ، ذَهَبْتُ إِلَى الْمَدِينَةِ.", sampleAnswer: "فِي نِهَايَةِ الْأُسْبُوعِ، ذَهَبْتُ إِلَى الْمَدِينَةِ.", focus: "Latihan frasa: Pada akhir pekan, saya pergi ke kota.", expectedKeywords: ["فِي", "نِهَايَةِ", "الْأُسْبُوعِ،"], indonesianExplanation: "Pada akhir pekan, saya pergi ke kota." },
    { coach: "استخدم: رَأَيْتُ مَكَانًا جَدِيدًا.", hint: "Jawab dengan pola: رَأَيْتُ مَكَانًا جَدِيدًا.", sampleAnswer: "رَأَيْتُ مَكَانًا جَدِيدًا.", focus: "Latihan frasa: Saya melihat tempat baru.", expectedKeywords: ["رَأَيْتُ", "مَكَانًا", "جَدِيدًا"], indonesianExplanation: "Saya melihat tempat baru." },
    { coach: "استخدم: اشْتَرَيْتُ شَيْئًا صَغِيرًا.", hint: "Jawab dengan pola: اشْتَرَيْتُ شَيْئًا صَغِيرًا.", sampleAnswer: "اشْتَرَيْتُ شَيْئًا صَغِيرًا.", focus: "Latihan frasa: Saya membeli sesuatu yang kecil.", expectedKeywords: ["اشْتَرَيْتُ", "شَيْئًا", "صَغِيرًا"], indonesianExplanation: "Saya membeli sesuatu yang kecil." },
  ],
  "arabic-reacting-with-interest": [
    { coach: "ذَهَبْتُ إِلَى مَكْتَبَةٍ جَدِيدَةٍ أَمْسِ.", hint: "Jawab dengan pola: حَقًّا؟", sampleAnswer: "حَقًّا؟", focus: "Latihan frasa: Benarkah?", expectedKeywords: ["حَقًّا"], indonesianExplanation: "Benarkah?" },
    { coach: "استخدم: هَذَا مُمْتَازٌ.", hint: "Jawab dengan pola: هَذَا مُمْتَازٌ.", sampleAnswer: "هَذَا مُمْتَازٌ.", focus: "Latihan frasa: Itu luar biasa.", expectedKeywords: ["هَذَا", "مُمْتَازٌ"], indonesianExplanation: "Itu luar biasa." },
    { coach: "استخدم: كَيْفَ كَانَ الْمَكَانُ؟", hint: "Jawab dengan pola: كَيْفَ كَانَ الْمَكَانُ؟", sampleAnswer: "كَيْفَ كَانَ الْمَكَانُ؟", focus: "Latihan frasa: Bagaimana tempatnya?", expectedKeywords: ["كَيْفَ", "كَانَ", "الْمَكَانُ"], indonesianExplanation: "Bagaimana tempatnya?" },
  ],
  "arabic-reconnecting-after-class": [
    { coach: "السَّلَامُ عَلَيْكَ يَا كَرِيمُ.", hint: "Jawab dengan pola: كَيْفَ حَالُكَ؟", sampleAnswer: "كَيْفَ حَالُكَ؟", focus: "Latihan frasa: Apa kabarmu?", expectedKeywords: ["كَيْفَ", "حَالُكَ"], indonesianExplanation: "Apa kabarmu?" },
    { coach: "استخدم: أَنَا بِخَيْرٍ، وَأَنْتَ؟", hint: "Jawab dengan pola: أَنَا بِخَيْرٍ، وَأَنْتَ؟", sampleAnswer: "أَنَا بِخَيْرٍ، وَأَنْتَ؟", focus: "Latihan frasa: Saya baik, dan kamu?", expectedKeywords: ["أَنَا", "بِخَيْرٍ،", "وَأَنْتَ"], indonesianExplanation: "Saya baik, dan kamu?" },
    { coach: "استخدم: كَانَ الدَّرْسُ جَيِّدًا.", hint: "Jawab dengan pola: كَانَ الدَّرْسُ جَيِّدًا.", sampleAnswer: "كَانَ الدَّرْسُ جَيِّدًا.", focus: "Latihan frasa: Pelajarannya bagus.", expectedKeywords: ["كَانَ", "الدَّرْسُ", "جَيِّدًا"], indonesianExplanation: "Pelajarannya bagus." },
  ],
  "arabic-requesting-service-help": [
    { coach: "عَفْوًا، هَلْ يُمْكِنُ أَنْ تُسَاعِدَنِي؟", hint: "Jawab dengan pola: هَلْ يُمْكِنُ أَنْ تُسَاعِدَنِي؟", sampleAnswer: "هَلْ يُمْكِنُ أَنْ تُسَاعِدَنِي؟", focus: "Latihan frasa: Bisakah Anda membantu saya?", expectedKeywords: ["هَلْ", "يُمْكِنُ", "أَنْ"], indonesianExplanation: "Bisakah Anda membantu saya?" },
    { coach: "استخدم: الْجِهَازُ لَا يَعْمَلُ.", hint: "Jawab dengan pola: الْجِهَازُ لَا يَعْمَلُ.", sampleAnswer: "الْجِهَازُ لَا يَعْمَلُ.", focus: "Latihan frasa: Perangkatnya tidak bekerja.", expectedKeywords: ["الْجِهَازُ", "لَا", "يَعْمَلُ"], indonesianExplanation: "Perangkatnya tidak bekerja." },
    { coach: "استخدم: أَحْتَاجُ إِلَى إِصْلَاحٍ.", hint: "Jawab dengan pola: أَحْتَاجُ إِلَى إِصْلَاحٍ.", sampleAnswer: "أَحْتَاجُ إِلَى إِصْلَاحٍ.", focus: "Latihan frasa: Saya membutuhkan perbaikan.", expectedKeywords: ["أَحْتَاجُ", "إِلَى", "إِصْلَاحٍ"], indonesianExplanation: "Saya membutuhkan perbaikan." },
  ],
  "arabic-rescheduling-politely": [
    { coach: "نَلْتَقِي السَّاعَةَ الرَّابِعَةَ، صَحِيحٌ؟", hint: "Jawab dengan pola: لَا أَسْتَطِيعُ فِي هَذَا الْوَقْتِ.", sampleAnswer: "لَا أَسْتَطِيعُ فِي هَذَا الْوَقْتِ.", focus: "Latihan frasa: Saya tidak bisa pada waktu ini.", expectedKeywords: ["لَا", "أَسْتَطِيعُ", "فِي"], indonesianExplanation: "Saya tidak bisa pada waktu ini." },
    { coach: "استخدم: هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", hint: "Jawab dengan pola: هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", sampleAnswer: "هَلْ يُمْكِنُ أَنْ نُغَيِّرَ الْمَوْعِدَ؟", focus: "Latihan frasa: Bisakah kita mengubah jadwalnya?", expectedKeywords: ["هَلْ", "يُمْكِنُ", "أَنْ"], indonesianExplanation: "Bisakah kita mengubah jadwalnya?" },
    { coach: "استخدم: مَاذَا عَنِ السَّاعَةِ الْخَامِسَةِ؟", hint: "Jawab dengan pola: مَاذَا عَنِ السَّاعَةِ الْخَامِسَةِ؟", sampleAnswer: "مَاذَا عَنِ السَّاعَةِ الْخَامِسَةِ؟", focus: "Latihan frasa: Bagaimana dengan jam lima?", expectedKeywords: ["مَاذَا", "عَنِ", "السَّاعَةِ"], indonesianExplanation: "Bagaimana dengan jam lima?" },
  ],
  "arabic-review-health-and-past": [
    { coach: "مَرْحَبًا، أُرِيدُ مَوْعِدًا مَعَ الطَّبِيبِ.", hint: "Jawab dengan pola: لَا أَشْعُرُ بِالرَّاحَةِ.", sampleAnswer: "لَا أَشْعُرُ بِالرَّاحَةِ.", focus: "Latihan frasa: Saya tidak merasa nyaman.", expectedKeywords: ["لَا", "أَشْعُرُ", "بِالرَّاحَةِ"], indonesianExplanation: "Saya tidak merasa nyaman." },
    { coach: "استخدم: عِنْدِي أَلَمٌ خَفِيفٌ.", hint: "Jawab dengan pola: عِنْدِي أَلَمٌ خَفِيفٌ.", sampleAnswer: "عِنْدِي أَلَمٌ خَفِيفٌ.", focus: "Latihan frasa: Saya punya sakit ringan.", expectedKeywords: ["عِنْدِي", "أَلَمٌ", "خَفِيفٌ"], indonesianExplanation: "Saya punya sakit ringan." },
    { coach: "استخدم: مُنْذُ أَمْسِ.", hint: "Jawab dengan pola: مُنْذُ أَمْسِ.", sampleAnswer: "مُنْذُ أَمْسِ.", focus: "Latihan frasa: Sejak kemarin.", expectedKeywords: ["مُنْذُ", "أَمْسِ"], indonesianExplanation: "Sejak kemarin." },
  ],
  "arabic-review-introductions-and-contact": [
    { coach: "مَا اسْمُكَ؟", hint: "Jawab dengan pola: اِسْمِي أَحْمَدُ", sampleAnswer: "اِسْمِي أَحْمَدُ", focus: "Latihan frasa: Nama saya Ahmad.", expectedKeywords: ["اِسْمِي", "أَحْمَدُ"], indonesianExplanation: "Nama saya Ahmad." },
    { coach: "استخدم: أَنَا مِنْ إِنْدُونِيسِيَا", hint: "Jawab dengan pola: أَنَا مِنْ إِنْدُونِيسِيَا", sampleAnswer: "أَنَا مِنْ إِنْدُونِيسِيَا", focus: "Latihan frasa: Saya dari Indonesia.", expectedKeywords: ["أَنَا", "من", "إِنْدُونِيسِيَا"], indonesianExplanation: "Saya dari Indonesia." },
    { coach: "استخدم: أَكْتُبُ اسْمِي", hint: "Jawab dengan pola: أَكْتُبُ اسْمِي", sampleAnswer: "أَكْتُبُ اسْمِي", focus: "Latihan frasa: Saya menulis nama saya.", expectedKeywords: ["أَكْتُبُ", "اسْمِي"], indonesianExplanation: "Saya menulis nama saya." },
  ],
  "arabic-review-places-and-shopping": [
    { coach: "أَيْنَ الْمَقْهَى؟", hint: "Jawab dengan pola: أَيْنَ الْمَقْهَى؟", sampleAnswer: "أَيْنَ الْمَقْهَى؟", focus: "Latihan frasa: Di mana kafe?", expectedKeywords: ["أَيْنَ", "الْمَقْهَى"], indonesianExplanation: "Di mana kafe?" },
    { coach: "استخدم: كَيْفَ أَذْهَبُ إِلَى الْمَقْهَى؟", hint: "Jawab dengan pola: كَيْفَ أَذْهَبُ إِلَى الْمَقْهَى؟", sampleAnswer: "كَيْفَ أَذْهَبُ إِلَى الْمَقْهَى؟", focus: "Latihan frasa: Bagaimana saya pergi ke kafe?", expectedKeywords: ["كَيْفَ", "أَذْهَبُ", "إِلَى"], indonesianExplanation: "Bagaimana saya pergi ke kafe?" },
    { coach: "استخدم: أُرِيدُ مَاءً", hint: "Jawab dengan pola: أُرِيدُ مَاءً", sampleAnswer: "أُرِيدُ مَاءً", focus: "Latihan frasa: Saya ingin air.", expectedKeywords: ["أُرِيدُ", "مَاءً"], indonesianExplanation: "Saya ingin air." },
  ],
  "arabic-review-routine-and-study": [
    { coach: "مَتَى تَدْرُسُ الْعَرَبِيَّةَ؟", hint: "Jawab dengan pola: الْيَوْمُ الْإِثْنَيْنِ", sampleAnswer: "الْيَوْمُ الْإِثْنَيْنِ", focus: "Latihan frasa: Hari ini Senin.", expectedKeywords: ["الْيَوْمُ", "الْإِثْنَيْنِ"], indonesianExplanation: "Hari ini Senin." },
    { coach: "استخدم: السَّاعَةُ الثَّامِنَةُ", hint: "Jawab dengan pola: السَّاعَةُ الثَّامِنَةُ", sampleAnswer: "السَّاعَةُ الثَّامِنَةُ", focus: "Latihan frasa: Jam delapan.", expectedKeywords: ["السَّاعَةُ", "الثَّامِنَةُ"], indonesianExplanation: "Jam delapan." },
    { coach: "استخدم: أَدْرُسُ الْعَرَبِيَّةَ", hint: "Jawab dengan pola: أَدْرُسُ الْعَرَبِيَّةَ", sampleAnswer: "أَدْرُسُ الْعَرَبِيَّةَ", focus: "Latihan frasa: Saya belajar bahasa Arab.", expectedKeywords: ["أَدْرُسُ", "الْعَرَبِيَّةَ"], indonesianExplanation: "Saya belajar bahasa Arab." },
  ],
  "arabic-review-social-and-plans": [
    { coach: "كَيْفَ كَانَ دَرْسُكَ الْيَوْمَ يَا كَرِيمُ؟", hint: "Jawab dengan pola: كَيْفَ كَانَ دَرْسُكَ؟", sampleAnswer: "كَيْفَ كَانَ دَرْسُكَ؟", focus: "Latihan frasa: Bagaimana pelajaranmu?", expectedKeywords: ["كَيْفَ", "كَانَ", "دَرْسُكَ"], indonesianExplanation: "Bagaimana pelajaranmu?" },
    { coach: "استخدم: مَاذَا فَعَلْتَ بَعْدَ الدَّرْسِ؟", hint: "Jawab dengan pola: مَاذَا فَعَلْتَ بَعْدَ الدَّرْسِ؟", sampleAnswer: "مَاذَا فَعَلْتَ بَعْدَ الدَّرْسِ؟", focus: "Latihan frasa: Apa yang kamu lakukan setelah pelajaran?", expectedKeywords: ["مَاذَا", "فَعَلْتَ", "بَعْدَ"], indonesianExplanation: "Apa yang kamu lakukan setelah pelajaran?" },
    { coach: "استخدم: هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", hint: "Jawab dengan pola: هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", sampleAnswer: "هَلْ تُرِيدُ أَنْ تَدْرُسَ مَعِي؟", focus: "Latihan frasa: Apakah kamu ingin belajar bersama saya?", expectedKeywords: ["هَلْ", "تُرِيدُ", "أَنْ"], indonesianExplanation: "Apakah kamu ingin belajar bersama saya?" },
  ],
  "arabic-review-travel-and-services": [
    { coach: "أُرِيدُ تَذْكِرَةً إِلَى بَانْدُونْغ، مِنْ فَضْلِكِ.", hint: "Jawab dengan pola: أُرِيدُ تَذْكِرَةً إِلَى بَانْدُونْغ.", sampleAnswer: "أُرِيدُ تَذْكِرَةً إِلَى بَانْدُونْغ.", focus: "Latihan frasa: Saya ingin tiket ke Bandung.", expectedKeywords: ["أُرِيدُ", "تَذْكِرَةً", "إِلَى"], indonesianExplanation: "Saya ingin tiket ke Bandung." },
    { coach: "استخدم: مَتَى يَغَادِرُ الْقِطَارُ؟", hint: "Jawab dengan pola: مَتَى يَغَادِرُ الْقِطَارُ؟", sampleAnswer: "مَتَى يَغَادِرُ الْقِطَارُ؟", focus: "Latihan frasa: Kapan keretanya berangkat?", expectedKeywords: ["مَتَى", "يَغَادِرُ", "الْقِطَارُ"], indonesianExplanation: "Kapan keretanya berangkat?" },
    { coach: "استخدم: كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", hint: "Jawab dengan pola: كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", sampleAnswer: "كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", focus: "Latihan frasa: Bagaimana saya pergi ke peron?", expectedKeywords: ["كَيْفَ", "أَذْهَبُ", "إِلَى"], indonesianExplanation: "Bagaimana saya pergi ke peron?" },
  ],
  "arabic-routine-and-time-mission": [
    { coach: "أي يَوْمَ الْيَوْمُ؟", hint: "Jawab dengan pola: الْيَوْمُ ...", sampleAnswer: "الْيَوْمُ ...", focus: "Latihan frasa: Hari ini ...", expectedKeywords: ["الْيَوْمُ"], indonesianExplanation: "Hari ini ..." },
    { coach: "استخدم: الساعة ...", hint: "Jawab dengan pola: الساعة ...", sampleAnswer: "الساعة ...", focus: "Latihan frasa: Jam ...", expectedKeywords: ["الساعة"], indonesianExplanation: "Jam ..." },
    { coach: "استخدم: عِنْدِي دَرْسٌ", hint: "Jawab dengan pola: عِنْدِي دَرْسٌ", sampleAnswer: "عِنْدِي دَرْسٌ", focus: "Latihan frasa: Saya punya pelajaran.", expectedKeywords: ["عِنْدِي", "دَرْسٌ"], indonesianExplanation: "Saya punya pelajaran." },
  ],
  "arabic-saying-how-you-feel": [
    { coach: "مَرْحَبًا، لَا أَشْعُرُ بِالرَّاحَةِ.", hint: "Jawab dengan pola: أَشْعُرُ بِتَعَبٍ.", sampleAnswer: "أَشْعُرُ بِتَعَبٍ.", focus: "Latihan frasa: Saya merasa lelah.", expectedKeywords: ["أَشْعُرُ", "بِتَعَبٍ"], indonesianExplanation: "Saya merasa lelah." },
    { coach: "استخدم: عِنْدِي صُدَاعٌ خَفِيفٌ.", hint: "Jawab dengan pola: عِنْدِي صُدَاعٌ خَفِيفٌ.", sampleAnswer: "عِنْدِي صُدَاعٌ خَفِيفٌ.", focus: "Latihan frasa: Saya punya sakit kepala ringan.", expectedKeywords: ["عِنْدِي", "صُدَاعٌ", "خَفِيفٌ"], indonesianExplanation: "Saya punya sakit kepala ringan." },
    { coach: "استخدم: لَا أَشْعُرُ بِالرَّاحَةِ.", hint: "Jawab dengan pola: لَا أَشْعُرُ بِالرَّاحَةِ.", sampleAnswer: "لَا أَشْعُرُ بِالرَّاحَةِ.", focus: "Latihan frasa: Saya tidak merasa nyaman.", expectedKeywords: ["لَا", "أَشْعُرُ", "بِالرَّاحَةِ"], indonesianExplanation: "Saya tidak merasa nyaman." },
  ],
  "arabic-saying-what-you-do": [
    { coach: "مَاذَا تَعْمَلُ؟", hint: "Jawab dengan pola: مَاذَا تَعْمَلُ؟", sampleAnswer: "مَاذَا تَعْمَلُ؟", focus: "Latihan frasa: Apa pekerjaanmu?", expectedKeywords: ["مَاذَا", "تَعْمَلُ"], indonesianExplanation: "Apa pekerjaanmu?" },
    { coach: "استخدم: أَنَا طَالِبٌ", hint: "Jawab dengan pola: أَنَا طَالِبٌ", sampleAnswer: "أَنَا طَالِبٌ", focus: "Latihan frasa: Saya pelajar.", expectedKeywords: ["أَنَا", "طَالِبٌ"], indonesianExplanation: "Saya pelajar." },
    { coach: "استخدم: أَنَا معلم", hint: "Jawab dengan pola: أَنَا معلم", sampleAnswer: "أَنَا معلم", focus: "Latihan frasa: Saya guru.", expectedKeywords: ["أَنَا", "معلم"], indonesianExplanation: "Saya guru." },
  ],
  "arabic-saying-what-you-think": [
    { coach: "مَا رَأْيُكَ فِي الدَّرْسِ الْيَوْمَ يَا زَيْدُ؟", hint: "Jawab dengan pola: أَعْتَقِدُ أَنَّ الدَّرْسَ مُفِيدٌ.", sampleAnswer: "أَعْتَقِدُ أَنَّ الدَّرْسَ مُفِيدٌ.", focus: "Latihan frasa: Saya pikir pelajarannya bermanfaat.", expectedKeywords: ["أَعْتَقِدُ", "أَنَّ", "الدَّرْسَ"], indonesianExplanation: "Saya pikir pelajarannya bermanfaat." },
    { coach: "استخدم: فِي رَأْيِي، هَذَا جَيِّدٌ.", hint: "Jawab dengan pola: فِي رَأْيِي، هَذَا جَيِّدٌ.", sampleAnswer: "فِي رَأْيِي، هَذَا جَيِّدٌ.", focus: "Latihan frasa: Menurut saya, ini baik.", expectedKeywords: ["فِي", "رَأْيِي،", "هَذَا"], indonesianExplanation: "Menurut saya, ini baik." },
    { coach: "استخدم: أَرَى أَنَّ الْمَكَانَ مُنَاسِبٌ.", hint: "Jawab dengan pola: أَرَى أَنَّ الْمَكَانَ مُنَاسِبٌ.", sampleAnswer: "أَرَى أَنَّ الْمَكَانَ مُنَاسِبٌ.", focus: "Latihan frasa: Saya melihat bahwa tempatnya cocok.", expectedKeywords: ["أَرَى", "أَنَّ", "الْمَكَانَ"], indonesianExplanation: "Saya melihat bahwa tempatnya cocok." },
  ],
  "arabic-saying-what-you-want": [
    { coach: "مَاذَا تُرِيدُ؟", hint: "Jawab dengan pola: مَاذَا تُرِيدُ؟", sampleAnswer: "مَاذَا تُرِيدُ؟", focus: "Latihan frasa: Apa yang kamu inginkan?", expectedKeywords: ["مَاذَا", "تُرِيدُ"], indonesianExplanation: "Apa yang kamu inginkan?" },
    { coach: "استخدم: أُرِيدُ كِتَابًا", hint: "Jawab dengan pola: أُرِيدُ كِتَابًا", sampleAnswer: "أُرِيدُ كِتَابًا", focus: "Latihan frasa: Saya ingin buku.", expectedKeywords: ["أُرِيدُ", "كِتَابًا"], indonesianExplanation: "Saya ingin buku." },
    { coach: "استخدم: لَا أُرِيدُ قَهْوَةً", hint: "Jawab dengan pola: لَا أُرِيدُ قَهْوَةً", sampleAnswer: "لَا أُرِيدُ قَهْوَةً", focus: "Latihan frasa: Saya tidak ingin kopi.", expectedKeywords: ["لَا", "أُرِيدُ", "قَهْوَةً"], indonesianExplanation: "Saya tidak ingin kopi." },
  ],
  "arabic-saying-where-you-went": [
    { coach: "أَيْنَ ذَهَبْتَ فِي نِهَايَةِ الْأُسْبُوعِ يَا عُمَرُ؟", hint: "Jawab dengan pola: أَيْنَ ذَهَبْتَ؟", sampleAnswer: "أَيْنَ ذَهَبْتَ؟", focus: "Latihan frasa: Ke mana kamu pergi?", expectedKeywords: ["أَيْنَ", "ذَهَبْتَ"], indonesianExplanation: "Ke mana kamu pergi?" },
    { coach: "استخدم: ذَهَبْتُ إِلَى السُّوقِ.", hint: "Jawab dengan pola: ذَهَبْتُ إِلَى السُّوقِ.", sampleAnswer: "ذَهَبْتُ إِلَى السُّوقِ.", focus: "Latihan frasa: Saya pergi ke pasar.", expectedKeywords: ["ذَهَبْتُ", "إِلَى", "السُّوقِ"], indonesianExplanation: "Saya pergi ke pasar." },
    { coach: "استخدم: ذَهَبْتُ مَعَ صَدِيقِي.", hint: "Jawab dengan pola: ذَهَبْتُ مَعَ صَدِيقِي.", sampleAnswer: "ذَهَبْتُ مَعَ صَدِيقِي.", focus: "Latihan frasa: Saya pergi bersama teman saya.", expectedKeywords: ["ذَهَبْتُ", "مَعَ", "صَدِيقِي"], indonesianExplanation: "Saya pergi bersama teman saya." },
  ],
  "arabic-saying-you-do-not-understand": [
    { coach: "اِقْرَأِ الْجُمْلَةَ.", hint: "Jawab dengan pola: لَا أَفْهَمُ", sampleAnswer: "لَا أَفْهَمُ", focus: "Latihan frasa: Saya tidak paham.", expectedKeywords: ["لَا", "أَفْهَمُ"], indonesianExplanation: "Saya tidak paham." },
    { coach: "استخدم: لَا أَعْرِفُ الْكَلِمَةَ", hint: "Jawab dengan pola: لَا أَعْرِفُ الْكَلِمَةَ", sampleAnswer: "لَا أَعْرِفُ الْكَلِمَةَ", focus: "Latihan frasa: Saya tidak tahu katanya.", expectedKeywords: ["لَا", "أَعْرِفُ", "الْكَلِمَةَ"], indonesianExplanation: "Saya tidak tahu katanya." },
    { coach: "استخدم: مَاذَا يَعْنِي هَذَا؟", hint: "Jawab dengan pola: مَاذَا يَعْنِي هَذَا؟", sampleAnswer: "مَاذَا يَعْنِي هَذَا؟", focus: "Latihan frasa: Apa arti ini?", expectedKeywords: ["مَاذَا", "يَعْنِي", "هَذَا"], indonesianExplanation: "Apa arti ini?" },
  ],
  "arabic-sharing-email-addresses": [
    { coach: "مَا بَرِيدُكَ الْإِلِكْتُرُونِيُّ؟", hint: "Jawab dengan pola: مَا بَرِيدُكَ الْإِلِكْتُرُونِيُّ؟", sampleAnswer: "مَا بَرِيدُكَ الْإِلِكْتُرُونِيُّ؟", focus: "Latihan frasa: Apa alamat emailmu?", expectedKeywords: ["مَا", "بَرِيدُكَ", "الْإِلِكْتُرُونِيُّ"], indonesianExplanation: "Apa alamat emailmu?" },
    { coach: "استخدم: بَرِيدِي الْإِلِكْتُرُونِيُّ ...", hint: "Jawab dengan pola: بَرِيدِي الْإِلِكْتُرُونِيُّ ...", sampleAnswer: "بَرِيدِي الْإِلِكْتُرُونِيُّ ...", focus: "Latihan frasa: Email saya ...", expectedKeywords: ["بَرِيدِي", "الْإِلِكْتُرُونِيُّ"], indonesianExplanation: "Email saya ..." },
    { coach: "استخدم: اُكْتُبْ مِنْ فَضْلِكَ", hint: "Jawab dengan pola: اُكْتُبْ مِنْ فَضْلِكَ", sampleAnswer: "اُكْتُبْ مِنْ فَضْلِكَ", focus: "Latihan frasa: Tulis, tolong.", expectedKeywords: ["اُكْتُبْ", "مِنْ", "فَضْلِكَ"], indonesianExplanation: "Tulis, tolong." },
  ],
  "arabic-shopping-service-mission": [
    { coach: "أَبْحَثُ عَنْ حَقِيبَةٍ صَغِيرَةٍ.", hint: "Jawab dengan pola: أَبْحَثُ عَنْ حَقِيبَةٍ صَغِيرَةٍ.", sampleAnswer: "أَبْحَثُ عَنْ حَقِيبَةٍ صَغِيرَةٍ.", focus: "Latihan frasa: Saya mencari tas kecil.", expectedKeywords: ["أَبْحَثُ", "عَنْ", "حَقِيبَةٍ"], indonesianExplanation: "Saya mencari tas kecil." },
    { coach: "استخدم: هَلْ يُوجَدُ لَوْنٌ أَزْرَقُ؟", hint: "Jawab dengan pola: هَلْ يُوجَدُ لَوْنٌ أَزْرَقُ؟", sampleAnswer: "هَلْ يُوجَدُ لَوْنٌ أَزْرَقُ؟", focus: "Latihan frasa: Apakah ada warna biru?", expectedKeywords: ["هَلْ", "يُوجَدُ", "لَوْنٌ"], indonesianExplanation: "Apakah ada warna biru?" },
    { coach: "استخدم: أَيُّهُمَا أَفْضَلُ؟", hint: "Jawab dengan pola: أَيُّهُمَا أَفْضَلُ؟", sampleAnswer: "أَيُّهُمَا أَفْضَلُ؟", focus: "Latihan frasa: Mana yang lebih baik?", expectedKeywords: ["أَيُّهُمَا", "أَفْضَلُ"], indonesianExplanation: "Mana yang lebih baik?" },
  ],
  "arabic-simple-place-words": [
    { coach: "أَيْنَ الْمَدْرَسَةُ؟", hint: "Jawab dengan pola: الْبَيْتُ", sampleAnswer: "الْبَيْتُ", focus: "Latihan frasa: Rumah", expectedKeywords: ["الْبَيْتُ"], indonesianExplanation: "Rumah" },
    { coach: "استخدم: الْمَدْرَسَةُ", hint: "Jawab dengan pola: الْمَدْرَسَةُ", sampleAnswer: "الْمَدْرَسَةُ", focus: "Latihan frasa: Sekolah", expectedKeywords: ["الْمَدْرَسَةُ"], indonesianExplanation: "Sekolah" },
    { coach: "استخدم: السُّوقُ", hint: "Jawab dengan pola: السُّوقُ", sampleAnswer: "السُّوقُ", focus: "Latihan frasa: Pasar", expectedKeywords: ["السُّوقُ"], indonesianExplanation: "Pasar" },
  ],
  "arabic-social-follow-up-mission": [
    { coach: "السَّلَامُ عَلَيْكَ يَا أَحْمَدُ. كَيْفَ حَالُكَ؟", hint: "Jawab dengan pola: كَيْفَ حَالُكَ؟", sampleAnswer: "كَيْفَ حَالُكَ؟", focus: "Latihan frasa: Apa kabarmu?", expectedKeywords: ["كَيْفَ", "حَالُكَ"], indonesianExplanation: "Apa kabarmu?" },
    { coach: "استخدم: مَاذَا فَعَلْتَ أَمْسِ؟", hint: "Jawab dengan pola: مَاذَا فَعَلْتَ أَمْسِ؟", sampleAnswer: "مَاذَا فَعَلْتَ أَمْسِ؟", focus: "Latihan frasa: Apa yang kamu lakukan kemarin?", expectedKeywords: ["مَاذَا", "فَعَلْتَ", "أَمْسِ"], indonesianExplanation: "Apa yang kamu lakukan kemarin?" },
    { coach: "استخدم: هَذَا جَيِّدٌ.", hint: "Jawab dengan pola: هَذَا جَيِّدٌ.", sampleAnswer: "هَذَا جَيِّدٌ.", focus: "Latihan frasa: Itu bagus.", expectedKeywords: ["هَذَا", "جَيِّدٌ"], indonesianExplanation: "Itu bagus." },
  ],
  "arabic-spelling-your-name": [
    { coach: "كَيْفَ تَكْتُبُ اِسْمَكَ؟", hint: "Jawab dengan pola: كَيْفَ تَكْتُبُ اِسْمَكَ؟", sampleAnswer: "كَيْفَ تَكْتُبُ اِسْمَكَ؟", focus: "Latihan frasa: Bagaimana kamu menulis namamu?", expectedKeywords: ["كَيْفَ", "تَكْتُبُ", "اِسْمَكَ"], indonesianExplanation: "Bagaimana kamu menulis namamu?" },
    { coach: "استخدم: أَكْتُبُ اسْمِي ...", hint: "Jawab dengan pola: أَكْتُبُ اسْمِي ...", sampleAnswer: "أَكْتُبُ اسْمِي ...", focus: "Latihan frasa: Saya menulis nama saya ...", expectedKeywords: ["أَكْتُبُ", "اسْمِي"], indonesianExplanation: "Saya menulis nama saya ..." },
    { coach: "استخدم: هَذَا حَرْفُ ...", hint: "Jawab dengan pola: هَذَا حَرْفُ ...", sampleAnswer: "هَذَا حَرْفُ ...", focus: "Latihan frasa: Ini huruf ...", expectedKeywords: ["هَذَا", "حَرْفُ"], indonesianExplanation: "Ini huruf ..." },
  ],
  "arabic-talking-about-daily-routines": [
    { coach: "مَاذَا تَفْعَلُ صَبَاحًا؟", hint: "Jawab dengan pola: مَاذَا تَفْعَلُ صَبَاحًا؟", sampleAnswer: "مَاذَا تَفْعَلُ صَبَاحًا؟", focus: "Latihan frasa: Apa yang kamu lakukan pagi hari?", expectedKeywords: ["مَاذَا", "تَفْعَلُ", "صَبَاحًا"], indonesianExplanation: "Apa yang kamu lakukan pagi hari?" },
    { coach: "استخدم: أَقْرَأُ", hint: "Jawab dengan pola: أَقْرَأُ", sampleAnswer: "أَقْرَأُ", focus: "Latihan frasa: Saya membaca.", expectedKeywords: ["أَقْرَأُ"], indonesianExplanation: "Saya membaca." },
    { coach: "استخدم: أكتب", hint: "Jawab dengan pola: أكتب", sampleAnswer: "أكتب", focus: "Latihan frasa: Saya menulis.", expectedKeywords: ["أكتب"], indonesianExplanation: "Saya menulis." },
  ],
  "arabic-talking-about-the-weekend": [
    { coach: "مَاذَا فَعَلْتَ فِي نِهَايَةِ الْأُسْبُوعِ؟", hint: "Jawab dengan pola: مَاذَا فَعَلْتَ فِي نِهَايَةِ الْأُسْبُوعِ؟", sampleAnswer: "مَاذَا فَعَلْتَ فِي نِهَايَةِ الْأُسْبُوعِ؟", focus: "Latihan frasa: Apa yang kamu lakukan pada akhir pekan?", expectedKeywords: ["مَاذَا", "فَعَلْتَ", "فِي"], indonesianExplanation: "Apa yang kamu lakukan pada akhir pekan?" },
    { coach: "استخدم: ذَهَبْتُ إِلَى الْحَدِيقَةِ.", hint: "Jawab dengan pola: ذَهَبْتُ إِلَى الْحَدِيقَةِ.", sampleAnswer: "ذَهَبْتُ إِلَى الْحَدِيقَةِ.", focus: "Latihan frasa: Saya pergi ke taman.", expectedKeywords: ["ذَهَبْتُ", "إِلَى", "الْحَدِيقَةِ"], indonesianExplanation: "Saya pergi ke taman." },
    { coach: "استخدم: مَعَ أُسْرَتِي.", hint: "Jawab dengan pola: مَعَ أُسْرَتِي.", sampleAnswer: "مَعَ أُسْرَتِي.", focus: "Latihan frasa: Bersama keluarga saya.", expectedKeywords: ["مَعَ", "أُسْرَتِي"], indonesianExplanation: "Bersama keluarga saya." },
  ],
  "arabic-talking-about-yesterday": [
    { coach: "مَاذَا فَعَلْتَ أَمْسِ يَا رَامِي؟", hint: "Jawab dengan pola: مَاذَا فَعَلْتَ أَمْسِ؟", sampleAnswer: "مَاذَا فَعَلْتَ أَمْسِ؟", focus: "Latihan frasa: Apa yang kamu lakukan kemarin?", expectedKeywords: ["مَاذَا", "فَعَلْتَ", "أَمْسِ"], indonesianExplanation: "Apa yang kamu lakukan kemarin?" },
    { coach: "استخدم: ذَهَبْتُ إِلَى الْمَكْتَبَةِ.", hint: "Jawab dengan pola: ذَهَبْتُ إِلَى الْمَكْتَبَةِ.", sampleAnswer: "ذَهَبْتُ إِلَى الْمَكْتَبَةِ.", focus: "Latihan frasa: Saya pergi ke perpustakaan.", expectedKeywords: ["ذَهَبْتُ", "إِلَى", "الْمَكْتَبَةِ"], indonesianExplanation: "Saya pergi ke perpustakaan." },
    { coach: "استخدم: دَرَسْتُ بَعْضَ الْعَرَبِيَّةِ.", hint: "Jawab dengan pola: دَرَسْتُ بَعْضَ الْعَرَبِيَّةِ.", sampleAnswer: "دَرَسْتُ بَعْضَ الْعَرَبِيَّةِ.", focus: "Latihan frasa: Saya belajar sedikit bahasa Arab.", expectedKeywords: ["دَرَسْتُ", "بَعْضَ", "الْعَرَبِيَّةِ"], indonesianExplanation: "Saya belajar sedikit bahasa Arab." },
  ],
  "arabic-talking-to-a-driver": [
    { coach: "إِلَى فُنْدُقِ النُّورِ، مِنْ فَضْلِكَ.", hint: "Jawab dengan pola: إِلَى الْفُنْدُقِ، مِنْ فَضْلِكَ.", sampleAnswer: "إِلَى الْفُنْدُقِ، مِنْ فَضْلِكَ.", focus: "Latihan frasa: Ke hotel, tolong.", expectedKeywords: ["إِلَى", "الْفُنْدُقِ،", "مِنْ"], indonesianExplanation: "Ke hotel, tolong." },
    { coach: "استخدم: هَلْ هَذَا الْعُنْوَانُ صَحِيحٌ؟", hint: "Jawab dengan pola: هَلْ هَذَا الْعُنْوَانُ صَحِيحٌ؟", sampleAnswer: "هَلْ هَذَا الْعُنْوَانُ صَحِيحٌ؟", focus: "Latihan frasa: Apakah alamat ini benar?", expectedKeywords: ["هَلْ", "هَذَا", "الْعُنْوَانُ"], indonesianExplanation: "Apakah alamat ini benar?" },
    { coach: "استخدم: كَمْ يَسْتَغْرِقُ الطَّرِيقُ؟", hint: "Jawab dengan pola: كَمْ يَسْتَغْرِقُ الطَّرِيقُ؟", sampleAnswer: "كَمْ يَسْتَغْرِقُ الطَّرِيقُ؟", focus: "Latihan frasa: Berapa lama perjalanannya?", expectedKeywords: ["كَمْ", "يَسْتَغْرِقُ", "الطَّرِيقُ"], indonesianExplanation: "Berapa lama perjalanannya?" },
  ],
  "arabic-transport-travel-mission": [
    { coach: "أُرِيدُ تَذْكِرَةً إِلَى الْمَدِينَةِ، مِنْ فَضْلِكِ.", hint: "Jawab dengan pola: أُرِيدُ تَذْكِرَةً إِلَى الْمَدِينَةِ.", sampleAnswer: "أُرِيدُ تَذْكِرَةً إِلَى الْمَدِينَةِ.", focus: "Latihan frasa: Saya ingin tiket ke kota.", expectedKeywords: ["أُرِيدُ", "تَذْكِرَةً", "إِلَى"], indonesianExplanation: "Saya ingin tiket ke kota." },
    { coach: "استخدم: مَتَى يَغَادِرُ الْقِطَارُ؟", hint: "Jawab dengan pola: مَتَى يَغَادِرُ الْقِطَارُ؟", sampleAnswer: "مَتَى يَغَادِرُ الْقِطَارُ؟", focus: "Latihan frasa: Kapan keretanya berangkat?", expectedKeywords: ["مَتَى", "يَغَادِرُ", "الْقِطَارُ"], indonesianExplanation: "Kapan keretanya berangkat?" },
    { coach: "استخدم: كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", hint: "Jawab dengan pola: كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", sampleAnswer: "كَيْفَ أَذْهَبُ إِلَى الرَّصِيفِ؟", focus: "Latihan frasa: Bagaimana saya pergi ke peron?", expectedKeywords: ["كَيْفَ", "أَذْهَبُ", "إِلَى"], indonesianExplanation: "Bagaimana saya pergi ke peron?" },
  ],
  "arabic-understanding-simple-directions": [
    { coach: "كَيْفَ أَذْهَبُ إِلَى الْمَكْتَبَةِ؟", hint: "Jawab dengan pola: اِذْهَبْ يَمِينًا", sampleAnswer: "اِذْهَبْ يَمِينًا", focus: "Latihan frasa: Pergi ke kanan.", expectedKeywords: ["اِذْهَبْ", "يَمِينًا"], indonesianExplanation: "Pergi ke kanan." },
    { coach: "استخدم: اِذْهَبْ يَسَارًا", hint: "Jawab dengan pola: اِذْهَبْ يَسَارًا", sampleAnswer: "اِذْهَبْ يَسَارًا", focus: "Latihan frasa: Pergi ke kiri.", expectedKeywords: ["اِذْهَبْ", "يَسَارًا"], indonesianExplanation: "Pergi ke kiri." },
    { coach: "استخدم: إِلَى الْأَمَامِ", hint: "Jawab dengan pola: إِلَى الْأَمَامِ", sampleAnswer: "إِلَى الْأَمَامِ", focus: "Latihan frasa: Ke depan", expectedKeywords: ["إِلَى", "الْأَمَامِ"], indonesianExplanation: "Ke depan" },
  ],
  "asking-about-culture": [
    { coach: "Ask me about a tradition in my country.", hint: "Gunakan What is it like...?", sampleAnswer: "What is it like in your country during big holidays?", focus: "Ask culture question", expectedKeywords: ["what is it like", "country"], indonesianExplanation: "" },
    { coach: "Answer about your country in 1-2 sentences.", hint: "Jawab: It's ... but ... Mostly ...", sampleAnswer: "It's busy, but it's also meaningful. Mostly we share food and spend time together.", focus: "Explain briefly", expectedKeywords: ["busy", "mostly"], indonesianExplanation: "" },
    { coach: "Ask back politely.", hint: "Gunakan How about in your country?", sampleAnswer: "How about in your country?", focus: "Ask back", expectedKeywords: ["how about"], indonesianExplanation: "" },
  ],
  "asking-about-departure-time": [
    { coach: "Which train?", hint: "Sebutkan tujuan keretanya.", sampleAnswer: "The train to Bandung.", focus: "Specify the train", expectedKeywords: ["train", "bandung"], indonesianExplanation: "" },
    { coach: "It leaves at 6:30 pm.", hint: "Konfirmasi platformnya.", sampleAnswer: "Okay. Which platform?", focus: "Ask the platform", expectedKeywords: ["which platform", "?"], indonesianExplanation: "" },
    { coach: "Platform 2.", hint: "Tanya durasi perjalanan.", sampleAnswer: "Great. How long is the trip?", focus: "Ask the duration", expectedKeywords: ["how long", "?"], indonesianExplanation: "" },
  ],
  "asking-about-past-activities": [
    { coach: "What did you do yesterday evening?", hint: "Jawab dengan 1-2 aktivitas (past).", sampleAnswer: "I cooked dinner and listened to music.", focus: "Answer with past activities", expectedKeywords: ["cooked", "listened"], indonesianExplanation: "" },
    { coach: "Nice. Did you cook at home?", hint: "Jawab singkat.", sampleAnswer: "Yes, I did.", focus: "Short past answer", expectedKeywords: ["did"], indonesianExplanation: "" },
    { coach: "What did you cook?", hint: "Sebutkan satu makanan.", sampleAnswer: "I made fried rice.", focus: "Answer follow-up", expectedKeywords: ["made"], indonesianExplanation: "" },
  ],
  "asking-about-prices": [
    { coach: "Hello. Can I help you?", hint: "Tanyakan harga coffee.", sampleAnswer: "How much is the coffee?", focus: "Price question", expectedKeywords: ["how", "much", "coffee", "?"], indonesianExplanation: "" },
    { coach: "It is twenty thousand rupiah.", hint: "Konfirmasi harga.", sampleAnswer: "Twenty thousand rupiah?", focus: "Price confirmation", expectedKeywords: ["twenty", "thousand", "rupiah", "?"], indonesianExplanation: "" },
    { coach: "Yes, twenty thousand rupiah.", hint: "Tanyakan harga cake.", sampleAnswer: "How much is the cake?", focus: "Second price", expectedKeywords: ["how", "much", "cake", "?"], indonesianExplanation: "" },
    { coach: "It is twenty-five thousand rupiah.", hint: "Tutup dengan thank you.", sampleAnswer: "Okay. Thank you.", focus: "Closing", expectedKeywords: [], indonesianExplanation: "" },
  ],
  "asking-about-pros-and-cons": [
    { coach: "Ask me about pros and cons of this option.", hint: "Tanya: What are the pros and cons ...?", sampleAnswer: "What are the pros and cons of working remotely?", focus: "Ask about trade-offs", expectedKeywords: ["pros", "cons"], indonesianExplanation: "" },
    { coach: "Give one advantage.", hint: "Mulai dengan The advantage is ...", sampleAnswer: "The advantage is you save time.", focus: "State an advantage", expectedKeywords: ["advantage"], indonesianExplanation: "" },
    { coach: "Now give one downside.", hint: "Mulai dengan One downside is ...", sampleAnswer: "One downside is you might feel isolated.", focus: "State a downside", expectedKeywords: ["downside", "might"], indonesianExplanation: "" },
  ],
  "asking-about-size-and-color": [
    { coach: "Sorry, we don't have black. We have blue and white.", hint: "Tanya ukuran yang kamu butuhkan.", sampleAnswer: "Okay. Do you have it in size M?", focus: "Ask about size", expectedKeywords: ["size", "?"], indonesianExplanation: "" },
    { coach: "Yes, size M is available.", hint: "Pilih salah satu warna.", sampleAnswer: "Great. I'll take the blue one.", focus: "Choose an option", expectedKeywords: ["i'll take", "blue"], indonesianExplanation: "" },
    { coach: "Sure.", hint: "Tutup dengan sopan.", sampleAnswer: "Thank you.", focus: "Close politely", expectedKeywords: ["thank"], indonesianExplanation: "" },
  ],
  "asking-about-someones-story": [
    { coach: "So you got lost. What happened next?", hint: "Jawab dengan 1 aksi di masa lalu.", sampleAnswer: "We asked a local person for help.", focus: "Continue the story", expectedKeywords: ["asked", "help"], indonesianExplanation: "" },
    { coach: "Why did you do that?", hint: "Jawab dengan because + reason.", sampleAnswer: "Because we did not want to waste time.", focus: "Give a reason", expectedKeywords: ["because"], indonesianExplanation: "" },
    { coach: "How did you feel at that moment?", hint: "Sebutkan perasaan (felt...).", sampleAnswer: "I felt worried, but then I felt relieved.", focus: "Describe feelings", expectedKeywords: ["felt", "but"], indonesianExplanation: "" },
  ],
  "asking-about-work-or-study": [
    { coach: "Do you work or study?", hint: "Jawab apakah kamu bekerja atau belajar.", sampleAnswer: "I study English online.", focus: "Work or study", expectedKeywords: ["study", "english", "online"], indonesianExplanation: "" },
    { coach: "What do you do there?", hint: "Sebutkan role sederhana.", sampleAnswer: "I'm an assistant.", focus: "Simple role", expectedKeywords: ["i'm", "assistant"], indonesianExplanation: "" },
    { coach: "Nice. How about you?", hint: "Tanyakan balik dengan How about you?", sampleAnswer: "How about you?", focus: "Question back", expectedKeywords: ["how", "about", "?"], indonesianExplanation: "" },
  ],
  "asking-follow-up-questions": [
    { coach: "I went to a new cafe yesterday.", hint: "Tanya lokasi atau detailnya dengan pertanyaan singkat.", sampleAnswer: "Oh nice! Where is it?", focus: "Ask a follow-up question", expectedKeywords: ["where is it", "?"], indonesianExplanation: "" },
    { coach: "It's near the station.", hint: "Tanya apa yang dia pesan atau lakukan di sana.", sampleAnswer: "What did you order?", focus: "Ask for details", expectedKeywords: ["what did you order", "?"], indonesianExplanation: "" },
    { coach: "I ordered iced coffee. It was great.", hint: "Reaksi positif dan ajak dengan kalimat pendek.", sampleAnswer: "That sounds fun. Do you want to go sometime?", focus: "React and invite", expectedKeywords: ["that sounds fun", "do you want to go"], indonesianExplanation: "" },
  ],
  "asking-for-an-item": [
    { coach: "Hi. Can I help you?", hint: "Jelaskan barang yang kamu cari.", sampleAnswer: "Yes, please. I'm looking for a phone charger.", focus: "Ask for an item", expectedKeywords: ["i'm looking for", "charger"], indonesianExplanation: "" },
    { coach: "Sure. What kind?", hint: "Sebutkan jenisnya dengan singkat.", sampleAnswer: "A USB-C charger, please.", focus: "Specify the type", expectedKeywords: ["usb", "charger"], indonesianExplanation: "" },
    { coach: "Okay. Do you need a cable too?", hint: "Jawab singkat, lalu konfirmasi ketersediaannya.", sampleAnswer: "No, just the charger. Do you have it?", focus: "Confirm availability", expectedKeywords: ["do you have", "?"], indonesianExplanation: "" },
  ],
  "asking-for-clarification": [
    { coach: "Can you update the report for Friday?", hint: "Terima dulu, lalu minta klarifikasi.", sampleAnswer: "Sure. Could you clarify which sections you need?", focus: "Ask for clarification", expectedKeywords: ["clarify", "sections"], indonesianExplanation: "" },
    { coach: "Focus on the summary and the risks.", hint: "Konfirmasi satu detail penting.", sampleAnswer: "Got it. Just to confirm, you want the latest numbers too, right?", focus: "Confirm details", expectedKeywords: ["confirm", "latest"], indonesianExplanation: "" },
    { coach: "Yes, please include the latest numbers.", hint: "Janji deadline singkat.", sampleAnswer: "Okay. I'll send it by Thursday afternoon.", focus: "Confirm deadline", expectedKeywords: ["send", "by"], indonesianExplanation: "" },
  ],
  "asking-for-help": [
    { coach: "Hello. Do you need help?", hint: "Minta bantuan.", sampleAnswer: "Can you help me?", focus: "Help request", expectedKeywords: ["help", "?"], indonesianExplanation: "" },
    { coach: "Sure. What is the problem?", hint: "Jelaskan masalah file.", sampleAnswer: "I can't open this file.", focus: "Problem statement", expectedKeywords: ["can't", "open", "file"], indonesianExplanation: "" },
    { coach: "Okay. Click this button.", hint: "Konfirmasi tombol.", sampleAnswer: "This button?", focus: "Instruction check", expectedKeywords: ["button", "?"], indonesianExplanation: "" },
    { coach: "Yes. Try again.", hint: "Katakan berhasil dan terima kasih.", sampleAnswer: "It works. Thank you.", focus: "Result", expectedKeywords: ["works"], indonesianExplanation: "" },
  ],
  "asking-for-opinions": [
    { coach: "What do you think about going to Bali?", hint: "Jawab dengan opini: I think it's + adjective.", sampleAnswer: "I think it's a great idea.", focus: "Give opinion", expectedKeywords: ["i think", "idea"], indonesianExplanation: "" },
    { coach: "Why?", hint: "Jawab dengan because + reason.", sampleAnswer: "Because the beaches are beautiful.", focus: "Give reason", expectedKeywords: ["because", "beaches"], indonesianExplanation: "" },
    { coach: "Any concern?", hint: "Sebutkan kekhawatiran: It might be ...", sampleAnswer: "It might be crowded.", focus: "Add concern politely", expectedKeywords: ["might", "crowded"], indonesianExplanation: "" },
  ],
  "asking-for-recommendations": [
    { coach: "Hi. How can I help you today?", hint: "Tanya rekomendasi buat dinner.", sampleAnswer: "Do you have any recommendations for dinner?", focus: "Ask for recommendations", expectedKeywords: ["recommendations"], indonesianExplanation: "" },
    { coach: "Sure. What kind of place are you looking for?", hint: "Jelaskan yang kamu cari (local / quiet / cheap).", sampleAnswer: "I'm looking for something local. Something local would be great.", focus: "Describe what you want", expectedKeywords: ["looking for", "local"], indonesianExplanation: "" },
    { coach: "I recommend a place nearby. Any questions?", hint: "Tanya jarak atau cara pergi.", sampleAnswer: "Great. Is it far from here?", focus: "Ask a follow-up question", expectedKeywords: ["far", "here"], indonesianExplanation: "" },
  ],
  "asking-for-repetition": [
    { coach: "My phone number is zero eight one three, two two five five.", hint: "Minta lawan bicara mengulang.", sampleAnswer: "Sorry, can you repeat that, please?", focus: "Polite repetition", expectedKeywords: ["sorry", "repeat", "?"], indonesianExplanation: "" },
    { coach: "Sure. Zero eight one three, two two five five.", hint: "Cek satu detail dengan: Did you say ...?", sampleAnswer: "Did you say two two five five?", focus: "Checking a detail", expectedKeywords: ["did", "say", "two", "five", "?"], indonesianExplanation: "" },
    { coach: "Yes, that's right.", hint: "Tunjukkan bahwa kamu sudah paham.", sampleAnswer: "Got it. Thank you.", focus: "Showing understanding", expectedKeywords: ["got"], indonesianExplanation: "" },
  ],
  "asking-high-quality-follow-ups": [
    { coach: "Clarify what 'more cautious' means.", hint: "When you say..., do you mean X or Y?", sampleAnswer: "When you say 'more cautious', do you mean smaller scope or slower timing?", focus: "Clarify", expectedKeywords: ["when you say", "do you mean"], indonesianExplanation: "" },
    { coach: "Ask about assumptions and decision criteria.", hint: "What's your assumption... What would change your mind...?", sampleAnswer: "What's your assumption about the main risk? And what would change your mind about the timeline?", focus: "Assumptions + criteria", expectedKeywords: ["assumption", "change your mind"], indonesianExplanation: "" },
    { coach: "Move to action.", hint: "What's the next step today?", sampleAnswer: "Got it. What's the next step we should take today?", focus: "Action", expectedKeywords: ["next step", "today"], indonesianExplanation: "" },
  ],
  "asking-how-to-get-there": [
    { coach: "Where do you want to go?", hint: "Tanyakan cara ke station.", sampleAnswer: "How do I get to the station?", focus: "Direction question", expectedKeywords: ["how", "get", "station", "?"], indonesianExplanation: "" },
    { coach: "Go straight for two minutes.", hint: "Ulangi durasi arahnya.", sampleAnswer: "Okay. Go straight for two minutes.", focus: "Time direction", expectedKeywords: ["straight", "two", "minutes"], indonesianExplanation: "" },
    { coach: "Then turn right at the bank.", hint: "Konfirmasi landmark.", sampleAnswer: "Turn right at the bank?", focus: "Landmark confirmation", expectedKeywords: ["turn", "right", "bank", "?"], indonesianExplanation: "" },
    { coach: "Yes. The station is there.", hint: "Tutup dengan sopan.", sampleAnswer: "Thank you for your help.", focus: "Thanking", expectedKeywords: ["help"], indonesianExplanation: "" },
  ],
  "asking-someones-name": [
    { coach: "Hi. I am new here.", hint: "Tanyakan nama dengan: What's your name?", sampleAnswer: "Hi. What's your name?", focus: "Asking a name", expectedKeywords: ["what's your name", "what is your name", "may i know your name", "?"], indonesianExplanation: "Tanyakan nama dengan pertanyaan sederhana. 'What's your name?' cukup untuk konteks santai." },
    { coach: "My name is Mina.", hint: "Ulangi nama orang itu dalam responsmu.", sampleAnswer: "Nice to meet you, Mina.", focus: "Using the name", expectedKeywords: ["nice to meet you", "mina"], indonesianExplanation: "Mengulang nama lawan bicara membuat responsmu terdengar lebih perhatian." },
    { coach: "Nice to meet you too.", hint: "Tutup dengan respons singkat yang natural.", sampleAnswer: "See you later.", focus: "Closing", expectedKeywords: ["see you", "later", "bye"], indonesianExplanation: "Gunakan closing sederhana seperti 'See you later' agar percakapan selesai dengan sopan." },
  ],
  "asking-tactful-questions": [
    { coach: "Ask how they prefer to receive feedback.", hint: "Would you mind if I ask...?", sampleAnswer: "Would you mind if I ask how you prefer to receive feedback?", focus: "Preference", expectedKeywords: ["would you mind", "prefer"], indonesianExplanation: "" },
    { coach: "Clarify the format politely.", hint: "If it's okay, could you clarify whether...?", sampleAnswer: "If it's okay, could you clarify whether you'd prefer feedback in writing or in a call?", focus: "Clarify", expectedKeywords: ["if it's okay", "clarify", "whether"], indonesianExplanation: "" },
    { coach: "Check understanding about privacy.", hint: "Just to make sure I understand...", sampleAnswer: "Just to make sure I understand, should we share concerns privately first?", focus: "Confirm", expectedKeywords: ["make sure", "privately"], indonesianExplanation: "" },
  ],
  "asking-when-something-happens": [
    { coach: "When is the meeting?", hint: "Jawab dengan hari dan jam.", sampleAnswer: "It's tomorrow at ten.", focus: "Event time", expectedKeywords: ["it's", "tomorrow", "ten"], indonesianExplanation: "" },
    { coach: "Is it online?", hint: "Jawab yes/no dengan kalimat lengkap.", sampleAnswer: "Yes, it is online.", focus: "Meeting format", expectedKeywords: ["online"], indonesianExplanation: "" },
    { coach: "Tomorrow at ten. Is that right?", hint: "Konfirmasi dengan: Yes, that's right.", sampleAnswer: "Yes, that's right.", focus: "Confirming details", expectedKeywords: ["that's", "right"], indonesianExplanation: "" },
  ],
  "asking-where-a-place-is": [
    { coach: "Excuse me. What do you need?", hint: "Tanyakan lokasi classroom.", sampleAnswer: "Where is the classroom?", focus: "Place question", expectedKeywords: ["where", "classroom", "?"], indonesianExplanation: "" },
    { coach: "It is on the first floor.", hint: "Tanyakan apakah dekat office.", sampleAnswer: "Is it near the office?", focus: "Confirming location", expectedKeywords: ["near", "office", "?"], indonesianExplanation: "" },
    { coach: "Yes, it is next to the office.", hint: "Tutup dengan thank you.", sampleAnswer: "Thank you.", focus: "Polite closing", expectedKeywords: [], indonesianExplanation: "" },
  ],
  "b1-final-conversation": [
    { coach: "How was your practice last week?", hint: "At first..., but then... because...", sampleAnswer: "At first it was hard, but then it got easier because I kept sessions short.", focus: "Story + reason", expectedKeywords: ["at first", "but", "because"], indonesianExplanation: "" },
    { coach: "Nice. What's your goal now?", hint: "My goal is to... by ...", sampleAnswer: "My goal is to speak more confidently by next month.", focus: "Goal with deadline", expectedKeywords: ["goal", "by"], indonesianExplanation: "" },
    { coach: "What usually gets in your way, what helps you most, and what's your next step?", hint: "Sometimes..., so... What helps me most is... My next step is...", sampleAnswer: "Sometimes I get distracted, so I leave my phone in another room. I prefer Conversation Coach because it gives feedback. So my next step is to practice three times this week.", focus: "Problem + preference + next step", expectedKeywords: ["so", "prefer", "because", "next step"], indonesianExplanation: "" },
  ],
  "b1-final-test-practice": [
    { coach: "What's your goal this month?", hint: "Goal + by ...", sampleAnswer: "My goal is to speak more confidently by the end of this month.", focus: "Goal with deadline", expectedKeywords: ["goal", "by"], indonesianExplanation: "" },
    { coach: "What's your biggest challenge, and what will you do?", hint: "Challenge + so ...", sampleAnswer: "The biggest challenge is staying consistent, so I'm keeping sessions short.", focus: "Challenge + solution", expectedKeywords: ["challenge", "so"], indonesianExplanation: "" },
    { coach: "Compare and choose: option A or B?", hint: "I prefer ... because ... but ...", sampleAnswer: "I prefer option B because it's cheaper, but it might be crowded.", focus: "Preference with reason + concern", expectedKeywords: ["prefer", "because", "might"], indonesianExplanation: "" },
  ],
  "b2-final-discussion": [
    { coach: "Before we decide, can you define the scope and what success looks like?", hint: "Let's define the scope... what does success look like?", sampleAnswer: "We should keep the scope to the core workflow, and success means fewer incidents without delaying the release.", focus: "Frame", expectedKeywords: ["scope", "success"], indonesianExplanation: "" },
    { coach: "Leadership still wants new features, and I'm worried we'll overload the team.", hint: "I understand the concern... The trade-off is...", sampleAnswer: "I understand the concern. The trade-off is speed versus reliability, so we should keep scope tight.", focus: "Concerns + trade-offs", expectedKeywords: ["understand", "trade-off"], indonesianExplanation: "" },
    { coach: "Given all that, what do you recommend, and what are the next steps?", hint: "Given these constraints... Next steps are... today... by Friday.", sampleAnswer: "Given these constraints, I'd recommend a time-boxed pilot. Next steps are: I'll share a plan today, and you'll review it by Friday.", focus: "Decision + next steps", expectedKeywords: ["recommend", "next steps", "by"], indonesianExplanation: "" },
  ],
  "b2-final-test-practice": [
    { coach: "What's your position?", hint: "My position is that...", sampleAnswer: "My position is that we should run a two-week pilot before a full rollout.", focus: "Position", expectedKeywords: ["position", "pilot"], indonesianExplanation: "" },
    { coach: "What's your evidence and trade-off?", hint: "Based on the data... The trade-off is...", sampleAnswer: "Based on the data, drop-offs increased after the redesign. The trade-off is speed versus long-term reliability.", focus: "Evidence + trade-off", expectedKeywords: ["based on", "data", "trade-off"], indonesianExplanation: "" },
    { coach: "Recommend a next step and timeline.", hint: "I'd recommend... Next steps are... by Friday.", sampleAnswer: "I'd recommend the pilot. Next steps are: I'll draft the plan today, and you'll review it by Friday.", focus: "Recommendation + next steps", expectedKeywords: ["recommend", "next steps", "by"], indonesianExplanation: "" },
  ],
  "balancing-two-viewpoints": [
    { coach: "We need to choose between growth and stability.", hint: "Mulai dengan on the one hand... on the other hand...", sampleAnswer: "On the one hand, growth could unlock new revenue. On the other hand, stability reduces long-term risk.", focus: "Balance", expectedKeywords: ["on the one hand", "on the other hand"], indonesianExplanation: "" },
    { coach: "Give a nuanced conclusion.", hint: "While it's true... On balance...", sampleAnswer: "While it's true that growth matters, the incident rate is concerning. On balance, I'd prioritize stability.", focus: "Conclusion", expectedKeywords: ["while it's true", "on balance"], indonesianExplanation: "" },
    { coach: "Offer a compromise plan.", hint: "Ring-fence a small budget...", sampleAnswer: "I'd ring-fence a small budget for growth experiments while we focus on stability.", focus: "Compromise", expectedKeywords: ["ring-fence", "budget"], indonesianExplanation: "" },
  ],
  "being-polite-with-differences": [
    { coach: "In my country, people usually eat dinner early, around 6 p.m.", hint: "Reaksi sopan + jelaskan kebiasaanmu.", sampleAnswer: "Oh, that's interesting. In my country, we often eat later.", focus: "Polite reaction + difference", expectedKeywords: ["interesting", "in my country"], indonesianExplanation: "" },
    { coach: "Really? Are you used to eating early?", hint: "Jawab dengan I'm not used to...", sampleAnswer: "I'm not used to eating that early.", focus: "Say unfamiliar politely", expectedKeywords: ["not used to"], indonesianExplanation: "" },
    { coach: "Say something respectful about my habit.", hint: "Gunakan That sounds nice.", sampleAnswer: "That sounds nice, especially if you sleep early.", focus: "Show respect", expectedKeywords: ["sounds nice"], indonesianExplanation: "" },
  ],
  "building-a-persuasive-flow": [
    { coach: "What's the main argument for this proposal?", hint: "Start with The core claim is...", sampleAnswer: "The core claim is that modularization will improve delivery speed.", focus: "Claim", expectedKeywords: ["core claim"], indonesianExplanation: "" },
    { coach: "What's the evidence?", hint: "Use The evidence suggests...", sampleAnswer: "The evidence suggests teams ship faster when ownership is clear.", focus: "Evidence", expectedKeywords: ["evidence suggests"], indonesianExplanation: "" },
    { coach: "Address a concern and conclude.", hint: "A common concern is... That said... In short...", sampleAnswer: "A common concern is fragmentation. That said, shared standards can mitigate it. In short, the benefits outweigh the risks if we set guardrails early.", focus: "Concern + conclusion", expectedKeywords: ["concern", "that said", "in short"], indonesianExplanation: "" },
  ],
  "buying-a-simple-item": [
    { coach: "Hello. What do you need?", hint: "Minta beli pen ini.", sampleAnswer: "Can I have this pen?", focus: "Buying item", expectedKeywords: ["have", "pen", "?"], indonesianExplanation: "" },
    { coach: "Yes, of course.", hint: "Tanyakan harganya.", sampleAnswer: "How much is it?", focus: "Price", expectedKeywords: ["how", "much", "?"], indonesianExplanation: "" },
    { coach: "It is one dollar.", hint: "Bayar dengan Here you go.", sampleAnswer: "Okay. Here you go.", focus: "Payment", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "Thank you. Here is your pen.", hint: "Tutup singkat.", sampleAnswer: "Thanks.", focus: "Closing", expectedKeywords: [], indonesianExplanation: "" },
  ],
  "buying-a-ticket": [
    { coach: "Hi. Where are you going?", hint: "Sebutkan tujuan dan minta tiket dengan sopan.", sampleAnswer: "I'd like one ticket to Bandung, please.", focus: "Request a ticket", expectedKeywords: ["i'd like", "ticket"], indonesianExplanation: "" },
    { coach: "One-way or round-trip?", hint: "Pilih jenis tiket.", sampleAnswer: "One-way, please.", focus: "Choose the ticket type", expectedKeywords: ["one-way"], indonesianExplanation: "" },
    { coach: "Okay. That's 120,000 rupiah.", hint: "Konfirmasi harga dengan pertanyaan singkat.", sampleAnswer: "Okay. How much is it again?", focus: "Confirm the price", expectedKeywords: ["how much", "?"], indonesianExplanation: "" },
  ],
  "c1-final-conversation": [
    { coach: "Before we decide, what are we optimizing for here?", hint: "Let me frame this...", sampleAnswer: "Let me frame this: we need reliable outcomes and stakeholder confidence before scaling.", focus: "Frame", expectedKeywords: ["frame", "confidence"], indonesianExplanation: "" },
    { coach: "I agree, but some people still want to move faster, and no one wants to own a visible failure.", hint: "On balance... What I'm hearing is... do you mean X or Y?", sampleAnswer: "On balance, we can move fast, but only if we limit scope and validate metrics. What I'm hearing is some fear of visibility. Do you mean scope concerns or accountability concerns?", focus: "Nuance + listening", expectedKeywords: ["on balance", "only if", "hearing"], indonesianExplanation: "" },
    { coach: "Given that, what's your decision, and what should we do next?", hint: "The decision is... Next steps are... today... tomorrow...", sampleAnswer: "The decision is to run a two-week pilot with clear success criteria. Next steps are: I'll send a one-page plan today, and we'll align stakeholders tomorrow.", focus: "Decision + next steps", expectedKeywords: ["decision", "next steps", "today"], indonesianExplanation: "" },
  ],
  "c1-final-test-practice": [
    { coach: "Before we go further, what's the issue in one line?", hint: "Let me frame this...", sampleAnswer: "Let me frame this: we need reliability and stakeholder confidence before scaling.", focus: "Frame", expectedKeywords: ["frame", "reliability"], indonesianExplanation: "" },
    { coach: "Would you support the rollout now, or only under certain conditions?", hint: "On balance... but only after...", sampleAnswer: "On balance, I support the rollout, but only after we validate pilot metrics.", focus: "Nuance", expectedKeywords: ["on balance", "only after", "validate"], indonesianExplanation: "" },
    { coach: "Okay. So what's the decision, what are the open questions, and what should we do next?", hint: "The decision is... The open questions are... Next steps are...", sampleAnswer: "The decision is to run a two-week pilot. The open questions are resourcing and change management. Next steps are: I'll send a summary today, and we'll align tomorrow.", focus: "Structure", expectedKeywords: ["decision", "open questions", "next steps"], indonesianExplanation: "" },
  ],
  "cafe-and-shop-mission": [
    { coach: "Hi. What would you like?", hint: "Pesan coffee dan sandwich.", sampleAnswer: "Can I have a coffee and a sandwich, please?", focus: "Mission order", expectedKeywords: ["have", "coffee", "sandwich", "?"], indonesianExplanation: "" },
    { coach: "Sure. Small or large coffee?", hint: "Pilih small.", sampleAnswer: "Small, please.", focus: "Size", expectedKeywords: ["small"], indonesianExplanation: "" },
    { coach: "Anything else?", hint: "Tanyakan total harga.", sampleAnswer: "How much is it?", focus: "Total price", expectedKeywords: ["how", "much", "?"], indonesianExplanation: "" },
    { coach: "It is five dollars.", hint: "Bayar dengan sopan.", sampleAnswer: "Okay. Here you go.", focus: "Payment", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "Thank you. Here is your order.", hint: "Tutup singkat.", sampleAnswer: "Thanks.", focus: "Closing", expectedKeywords: [], indonesianExplanation: "" },
  ],
  "catching-implied-meaning": [
    { coach: "Interpret the concern neutrally.", hint: "Use It sounds like...", sampleAnswer: "It sounds like timing is the main concern.", focus: "Interpretation", expectedKeywords: ["sounds like", "concern"], indonesianExplanation: "" },
    { coach: "Confirm implied meaning politely.", hint: "Just to check... are you implying...?", sampleAnswer: "Just to check, are you implying that we should delay the rollout?", focus: "Check", expectedKeywords: ["just to check", "implying", "delay"], indonesianExplanation: "" },
    { coach: "Summarize and propose a next step.", hint: "What I'm hearing is... I'll...", sampleAnswer: "What I'm hearing is we need a phased plan to reduce risk. I'll draft a phased option and share it today.", focus: "Next step", expectedKeywords: ["hearing", "phased", "share"], indonesianExplanation: "" },
  ],
  "challenging-an-argument": [
    { coach: "Fewer steps always increases conversion.", hint: "Challenge logic politely.", sampleAnswer: "I'm not sure that follows. What's the evidence for that claim?", focus: "Logic + evidence", expectedKeywords: ["not sure", "evidence"], indonesianExplanation: "" },
    { coach: "I think it's common sense. What's your response?", hint: "Introduce another explanation + example.", sampleAnswer: "Could there be another explanation, like unclear copy or missing reassurance? For example, we reduced steps last quarter, but conversion didn't change.", focus: "Alternatives", expectedKeywords: ["another explanation", "for example"], indonesianExplanation: "" },
    { coach: "Close with a constructive next step.", hint: "Let's test...", sampleAnswer: "Let's test messaging changes alongside step reduction and compare results.", focus: "Next step", expectedKeywords: ["test", "compare"], indonesianExplanation: "" },
  ],
  "checking-directions": [
    { coach: "Go straight and turn left at the stairs.", hint: "Ulangi arahan untuk memastikan.", sampleAnswer: "Turn left at the stairs. Okay.", focus: "Confirm directions", expectedKeywords: ["turn left", "stairs"], indonesianExplanation: "" },
    { coach: "Yes. Platform 2 is on the left.", hint: "Tanyakan konfirmasi singkat.", sampleAnswer: "Great. Is this the right way?", focus: "Check the way", expectedKeywords: ["right way", "?"], indonesianExplanation: "" },
    { coach: "Yes, you're going the right way.", hint: "Tutup dengan sopan.", sampleAnswer: "Thank you.", focus: "Close politely", expectedKeywords: ["thank"], indonesianExplanation: "" },
  ],
  "checking-in": [
    { coach: "Welcome. How can I help you?", hint: "Mulai dengan: I'd like to check in.", sampleAnswer: "Hi. I'd like to check in.", focus: "Start check-in", expectedKeywords: ["check in"], indonesianExplanation: "" },
    { coach: "Sure. Do you have a reservation?", hint: "Jawab dengan under + name.", sampleAnswer: "Yes. I have a reservation under Faris Kim.", focus: "Confirm reservation name", expectedKeywords: ["reservation", "under"], indonesianExplanation: "" },
    { coach: "Great. Any questions about your stay?", hint: "Tanya 1 hal (check-out / breakfast).", sampleAnswer: "Yes. What time is check-out?", focus: "Ask a practical question", expectedKeywords: ["what time", "check-out"], indonesianExplanation: "" },
  ],
  "clarifying-scope": [
    { coach: "Ask what is in scope for this sprint.", hint: "Gunakan Just to clarify...", sampleAnswer: "Just to clarify, what exactly is in scope for this sprint?", focus: "Ask scope", expectedKeywords: ["clarify", "in scope"], indonesianExplanation: "" },
    { coach: "Ask if the admin dashboard is included.", hint: "Gunakan Does this include...?", sampleAnswer: "Does this include the admin dashboard changes?", focus: "Ask inclusion", expectedKeywords: ["include", "admin"], indonesianExplanation: "" },
    { coach: "Confirm what is out of scope and next step.", hint: "Use out of scope + I'll update...", sampleAnswer: "Got it. So that's out of scope for now. I'll update the ticket list.", focus: "Confirm + next step", expectedKeywords: ["out of scope", "update"], indonesianExplanation: "" },
  ],
  "clear-argument-mission": [
    { coach: "Do you think we should change our meeting format?", hint: "Mulai dengan In my view...", sampleAnswer: "In my view, we should move routine updates to a written summary.", focus: "Position", expectedKeywords: ["in my view", "should"], indonesianExplanation: "" },
    { coach: "Why do you think that?", hint: "One reason is... Another reason is...", sampleAnswer: "One reason is it saves time. Another reason is it improves focus.", focus: "Reasons", expectedKeywords: ["one reason", "another reason"], indonesianExplanation: "" },
    { coach: "I worry we'll lose useful discussion. How would you answer that, and what should we try next?", hint: "For example... That's a fair point. However... Let's...", sampleAnswer: "For example, last month we spent 30 minutes repeating updates. That's a fair point. However, we can keep one monthly live session. Let's run a one-month trial and review the results.", focus: "Example + counterpoint + next steps", expectedKeywords: ["for example", "fair point", "however", "trial"], indonesianExplanation: "" },
  ],
  "client-conversation-mission": [
    { coach: "We're onboarding a lot of new hires, and the current process is messy.", hint: "Just to clarify... biggest pain point...", sampleAnswer: "Just to clarify, who is the main user group and what's the biggest pain point today?", focus: "Discovery", expectedKeywords: ["clarify", "pain point"], indonesianExplanation: "" },
    { coach: "The biggest issue is delays, but we also need something reliable. What options do you recommend?", hint: "We have two options... The trade-off is... I'd recommend...", sampleAnswer: "We have two options: a quick fix this week, or a more robust solution in two weeks. The trade-off is speed versus stability. I'd recommend the robust option if the timeline allows.", focus: "Options + recommendation", expectedKeywords: ["two options", "trade-off", "recommend"], indonesianExplanation: "" },
    { coach: "I'm concerned about disruption during rollout. How would you reduce the risk, and what are the next steps?", hint: "I understand the concern... To reduce the risk... Next steps are... Does that timeline work...?", sampleAnswer: "I understand the concern. To reduce the risk, we can run a two-week pilot and send weekly summaries. Next steps are: I'll send a draft plan today, and you'll review it by Friday. Does that timeline work for you?", focus: "Concerns + next steps", expectedKeywords: ["understand", "reduce", "next steps", "timeline"], indonesianExplanation: "" },
  ],
  "coaching-with-questions": [
    { coach: "I'm stuck on how to handle this.", hint: "Start with options.", sampleAnswer: "Got it. What options do you see right now?", focus: "Options", expectedKeywords: ["options"], indonesianExplanation: "" },
    { coach: "Now help define success.", hint: "What would success look like...?", sampleAnswer: "What would success look like for the pilot?", focus: "Success", expectedKeywords: ["success look like"], indonesianExplanation: "" },
    { coach: "Unblock with a small next step and offer support.", hint: "Smallest next step... support...", sampleAnswer: "What's the smallest next step you can take today? And what support do you need from me?", focus: "Next step + support", expectedKeywords: ["smallest", "next step", "support"], indonesianExplanation: "" },
  ],
  "communicating-risk": [
    { coach: "What risks should we highlight to leadership?", hint: "Start with The main risk is...", sampleAnswer: "The main risk is a spike in incidents during rollout.", focus: "Risk", expectedKeywords: ["main risk", "incidents"], indonesianExplanation: "" },
    { coach: "How likely is that?", hint: "There's a reasonable chance... given...", sampleAnswer: "There's a reasonable chance, given recent instability.", focus: "Likelihood", expectedKeywords: ["reasonable chance", "given"], indonesianExplanation: "" },
    { coach: "Close with mitigation steps.", hint: "We can mitigate it by... monitoring... rollback...", sampleAnswer: "We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan.", focus: "Mitigation", expectedKeywords: ["mitigate", "monitoring", "rollback"], indonesianExplanation: "" },
  ],
  "community-culture-mission": [
    { coach: "Tell me about your neighborhood.", hint: "I live in... It's known for...", sampleAnswer: "I live in a quiet neighborhood. It's known for food stalls and small parks.", focus: "Describe community", expectedKeywords: ["neighborhood", "known for"], indonesianExplanation: "" },
    { coach: "Share one local habit.", hint: "People usually... especially on weekends.", sampleAnswer: "People usually eat outside in the evening, especially on weekends.", focus: "Share local habit", expectedKeywords: ["usually", "especially"], indonesianExplanation: "" },
    { coach: "Now respond politely to a cultural difference.", hint: "That's interesting. I'm not used to..., but it sounds nice.", sampleAnswer: "Oh, that's interesting. I'm not used to that, but it sounds nice.", focus: "Polite differences", expectedKeywords: ["interesting", "not used to", "sounds nice"], indonesianExplanation: "" },
  ],
  "comparing-simple-options": [
    { coach: "This one is cheaper. It's 80,000 rupiah.", hint: "Tanyakan opsi satunya.", sampleAnswer: "And the other one?", focus: "Ask about the other option", expectedKeywords: ["other one", "?"], indonesianExplanation: "" },
    { coach: "The other one is 120,000 rupiah, but it's better quality.", hint: "Pilih salah satu dengan singkat.", sampleAnswer: "Okay. I'll take the cheaper one.", focus: "Choose an option", expectedKeywords: ["i'll take", "cheaper"], indonesianExplanation: "" },
    { coach: "Sure.", hint: "Tutup dengan sopan.", sampleAnswer: "Thank you.", focus: "Close politely", expectedKeywords: ["thank"], indonesianExplanation: "" },
  ],
  "comparing-two-options": [
    { coach: "We have two options. What's the difference?", hint: "Bandingin pakai but.", sampleAnswer: "Option A is nicer, but it's more expensive.", focus: "Compare options", expectedKeywords: ["but", "more"], indonesianExplanation: "" },
    { coach: "Okay. And option B?", hint: "Sebutkan 1-2 poin: cheaper/faster/crowded.", sampleAnswer: "It's cheaper and faster, but it's usually crowded.", focus: "Describe option B", expectedKeywords: ["cheaper", "faster"], indonesianExplanation: "" },
    { coach: "Got it. Ask me what I prefer.", hint: "Tanya: Which do you prefer?", sampleAnswer: "Which do you prefer?", focus: "Ask preference", expectedKeywords: ["prefer"], indonesianExplanation: "" },
  ],
  "confirming-details": [
    { coach: "Okay, you're booked for tomorrow at 3:30 p.m.", hint: "Konfirmasi jamnya.", sampleAnswer: "Let me confirm the time: 3:30 p.m., right?", focus: "Confirm the time", expectedKeywords: ["confirm", "3:30", "right"], indonesianExplanation: "" },
    { coach: "Yes, that's right.", hint: "Sebutkan nama dan eja.", sampleAnswer: "My name is Raka Park. P-A-R-K.", focus: "Give name and spelling", expectedKeywords: ["my name is", "p-a-r-k"], indonesianExplanation: "" },
    { coach: "Thank you. Do you have a phone number?", hint: "Berikan nomor telepon.", sampleAnswer: "Yes. It's 0812-345-678.", focus: "Provide phone number", expectedKeywords: ["it's", "0812"], indonesianExplanation: "" },
  ],
  "confirming-next-steps": [
    { coach: "Confirm the decision.", hint: "To confirm, ...", sampleAnswer: "To confirm, we'll start with a two-week pilot.", focus: "Confirm decision", expectedKeywords: ["to confirm", "pilot"], indonesianExplanation: "" },
    { coach: "List next steps with owners and deadlines.", hint: "Next steps are: I'll... today, and you'll... by Friday.", sampleAnswer: "Next steps are: I'll send the draft plan today, and you'll review it by Friday.", focus: "Next steps", expectedKeywords: ["next steps", "by"], indonesianExplanation: "" },
    { coach: "Check if the timeline works.", hint: "Does that timeline work for you?", sampleAnswer: "Great. Does that timeline work for you?", focus: "Confirm timeline", expectedKeywords: ["timeline", "work"], indonesianExplanation: "" },
  ],
  "contact-details-mission": [
    { coach: "Hi. I need your contact details.", hint: "Mulai dengan nama lengkapmu.", sampleAnswer: "Sure. My name is Dimas.", focus: "Sharing a name", expectedKeywords: ["sure", "name", "dimas"], indonesianExplanation: "" },
    { coach: "How do you spell your name?", hint: "Eja nama huruf demi huruf.", sampleAnswer: "D-I-M-A-S.", focus: "Spelling a name", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "What is your phone number?", hint: "Sebutkan nomor telepon dalam kelompok kecil.", sampleAnswer: "It's zero eight one two, three four five six.", focus: "Sharing a phone number", expectedKeywords: ["it's", "zero", "eight", "one"], indonesianExplanation: "" },
    { coach: "And your email address?", hint: "Sebutkan email dengan at dan dot.", sampleAnswer: "It's dimas at example dot com.", focus: "Sharing an email", expectedKeywords: ["it's", "dimas", "example", "dot"], indonesianExplanation: "" },
    { coach: "Is everything correct?", hint: "Konfirmasi semua informasi benar.", sampleAnswer: "Yes, everything is correct.", focus: "Confirming all details", expectedKeywords: ["everything", "correct"], indonesianExplanation: "" },
  ],
  "cross-cultural-mission": [
    { coach: "They sounded polite, but I think they were uncomfortable. How do you read that?", hint: "My sense is that... Before we decide, can we clarify...?", sampleAnswer: "My sense is that they're signaling concern indirectly. Before we decide, can we clarify whether they prioritize speed or risk reduction?", focus: "Context", expectedKeywords: ["my sense", "clarify", "priority"], indonesianExplanation: "" },
    { coach: "That makes sense. How would you ask about feedback preferences tactfully?", hint: "Would you mind if I ask...?", sampleAnswer: "Would you mind if I ask how you prefer to receive feedback—writing or a call?", focus: "Tactful question", expectedKeywords: ["would you mind", "prefer"], indonesianExplanation: "" },
    { coach: "I may have come across too directly. How would you repair that and suggest a next step?", hint: "I may have misunderstood... Just to clarify... How about we...?", sampleAnswer: "I may have misunderstood their tone. Just to clarify, my intent was to confirm constraints, not reject the request. How about we send a short note and offer a quick call?", focus: "Repair", expectedKeywords: ["misunderstood", "intent", "how about"], indonesianExplanation: "" },
  ],
  "days-and-simple-schedules": [
    { coach: "When is the English class?", hint: "Jawab dengan hari: on Monday and Wednesday.", sampleAnswer: "It's on Monday and Wednesday.", focus: "Class days", expectedKeywords: ["it's", "monday", "wednesday"], indonesianExplanation: "" },
    { coach: "What time?", hint: "Jawab dengan at + time.", sampleAnswer: "At seven in the evening.", focus: "Class time", expectedKeywords: ["seven", "evening"], indonesianExplanation: "" },
    { coach: "Great. See you on Monday.", hint: "Tutup dengan singkat.", sampleAnswer: "See you.", focus: "Schedule closing", expectedKeywords: ["see"], indonesianExplanation: "" },
  ],
  "debate-analysis-mission": [
    { coach: "Challenge the claim by surfacing an assumption and asking for evidence.", hint: "It seems you're assuming... What's the evidence for...?", sampleAnswer: "It seems you're assuming fewer steps automatically mean better conversion. What's the evidence for that claim?", focus: "Assumption + evidence", expectedKeywords: ["assuming", "evidence"], indonesianExplanation: "" },
    { coach: "Present evidence carefully and be precise about what it shows.", hint: "According to... To be precise...", sampleAnswer: "According to the support dashboard, drop-offs increased after the redesign. To be precise, the data indicates correlation, not necessarily causation.", focus: "Evidence + precision", expectedKeywords: ["according to", "precise", "correlation"], indonesianExplanation: "" },
    { coach: "Respond under pressure and propose a controlled next step.", hint: "Let me be clear... key point... pilot...", sampleAnswer: "Let me be clear: we have indicators, not proof yet. However, the key point is waiting increases risk. We run a pilot this week and review results before scaling.", focus: "Pressure response", expectedKeywords: ["be clear", "key point", "pilot"], indonesianExplanation: "" },
  ],
  "describing-a-problem": [
    { coach: "What's going on?", hint: "Mulai dengan: There's a problem with ...", sampleAnswer: "There's a problem with the login page.", focus: "State the problem", expectedKeywords: ["problem", "with"], indonesianExplanation: "" },
    { coach: "When did it start?", hint: "Jawab kapan mulai.", sampleAnswer: "It started this morning when we deployed the update.", focus: "State timing and trigger", expectedKeywords: ["started", "when"], indonesianExplanation: "" },
    { coach: "What is the impact?", hint: "Jelaskan dampak pakai so.", sampleAnswer: "Users can't sign in, so they can't access their lessons.", focus: "Explain impact", expectedKeywords: ["can't", "so"], indonesianExplanation: "" },
  ],
  "describing-a-simple-experience": [
    { coach: "Oh nice. How was it?", hint: "Jawab dengan It was + adjective.", sampleAnswer: "It was delicious.", focus: "Describe with adjective", expectedKeywords: ["it was"], indonesianExplanation: "" },
    { coach: "What did you eat?", hint: "Sebutkan makanan (past).", sampleAnswer: "I ate grilled chicken and salad.", focus: "Say what you ate", expectedKeywords: ["ate"], indonesianExplanation: "" },
    { coach: "Would you go again?", hint: "Jawab dan bilang kamu suka / tidak suka.", sampleAnswer: "Yes. I really liked it.", focus: "Give opinion", expectedKeywords: ["liked"], indonesianExplanation: "" },
  ],
  "describing-feelings": [
    { coach: "How did you feel when that happened?", hint: "Sebutkan perasaan + sebab singkat.", sampleAnswer: "I felt nervous because we got lost.", focus: "Describe feeling with reason", expectedKeywords: ["felt", "because"], indonesianExplanation: "" },
    { coach: "What did you do next?", hint: "Sebutkan solusi singkat.", sampleAnswer: "We asked for directions.", focus: "Describe an action", expectedKeywords: ["asked"], indonesianExplanation: "" },
    { coach: "And how did you feel after that?", hint: "Sebutkan perasaan setelahnya.", sampleAnswer: "I felt relieved after that.", focus: "Describe feeling after", expectedKeywords: ["relieved"], indonesianExplanation: "" },
  ],
  "describing-simple-symptoms": [
    { coach: "What seems to be the problem?", hint: "Sebutkan gejala + durasi.", sampleAnswer: "I've had a sore throat since yesterday.", focus: "Describe symptom with duration", expectedKeywords: ["have had", "since", "throat"], indonesianExplanation: "" },
    { coach: "Do you have a fever?", hint: "Jawab singkat, lalu tambah gejala.", sampleAnswer: "A little. And I have a cough.", focus: "Add another symptom", expectedKeywords: ["a little", "cough"], indonesianExplanation: "" },
    { coach: "How long have you been coughing?", hint: "Jawab durasinya.", sampleAnswer: "For two days.", focus: "State duration", expectedKeywords: ["for", "days"], indonesianExplanation: "" },
  ],
  "describing-your-community": [
    { coach: "What's your neighborhood like?", hint: "Mulai dengan I live in ... neighborhood.", sampleAnswer: "I live in a quiet neighborhood near the city center.", focus: "Describe neighborhood", expectedKeywords: ["neighborhood"], indonesianExplanation: "" },
    { coach: "What is it known for?", hint: "Jawab dengan It's known for ...", sampleAnswer: "It's known for its food stalls and small parks.", focus: "Say what it's known for", expectedKeywords: ["known for"], indonesianExplanation: "" },
    { coach: "What do you like about it?", hint: "Jawab dengan because + reason.", sampleAnswer: "I like it because it's convenient but still peaceful.", focus: "Give a reason", expectedKeywords: ["because", "convenient"], indonesianExplanation: "" },
  ],
  "discussing-challenges": [
    { coach: "What's the biggest challenge?", hint: "Jawab dengan The biggest challenge is ...", sampleAnswer: "The biggest challenge is staying consistent after work.", focus: "Name the challenge", expectedKeywords: ["challenge", "consistent"], indonesianExplanation: "" },
    { coach: "Why is it hard?", hint: "Sebutkan satu alasan (distracted/tired).", sampleAnswer: "I get distracted by my phone, and I feel tired.", focus: "Explain the reason", expectedKeywords: ["distracted", "tired"], indonesianExplanation: "" },
    { coach: "Okay. What do you want to ask me?", hint: "Minta saran singkat.", sampleAnswer: "Do you have any tips?", focus: "Ask for a suggestion", expectedKeywords: ["tips"], indonesianExplanation: "" },
  ],
  "discussing-reliable-sources": [
    { coach: "Is this source reliable?", hint: "I'm not sure it's reliable.", sampleAnswer: "I'm not sure that source is reliable.", focus: "Express doubt", expectedKeywords: ["not sure", "reliable"], indonesianExplanation: "" },
    { coach: "Why not?", hint: "Because it doesn't cite... / mention...", sampleAnswer: "Because it doesn't cite data or mention the author.", focus: "Give criteria", expectedKeywords: ["doesn't", "cite"], indonesianExplanation: "" },
    { coach: "What would you do next?", hint: "I'd check ...", sampleAnswer: "I'd check official reports or reputable news outlets before sharing.", focus: "Suggest verification", expectedKeywords: ["I'd check", "official"], indonesianExplanation: "" },
  ],
  "discussing-tradeoffs": [
    { coach: "We have two options. Compare them.", hint: "Mulai dengan trade-off.", sampleAnswer: "The trade-off is speed versus long-term reliability.", focus: "Trade-off", expectedKeywords: ["trade-off"], indonesianExplanation: "" },
    { coach: "Explain the downside of the fast option.", hint: "If we optimize for speed, we might...", sampleAnswer: "If we optimize for speed, we might introduce more bugs.", focus: "Impact", expectedKeywords: ["optimize", "might"], indonesianExplanation: "" },
    { coach: "Now contrast with the safer option.", hint: "On the other hand...", sampleAnswer: "On the other hand, the slower option reduces risk but takes more effort.", focus: "Contrast", expectedKeywords: ["on the other hand", "risk"], indonesianExplanation: "" },
  ],
  "explaining-a-delay": [
    { coach: "Hi. Are you on your way?", hint: "Jawab + bilang kamu telat.", sampleAnswer: "Yes, but I'm running a bit late.", focus: "State you are late", expectedKeywords: ["running", "late"], indonesianExplanation: "" },
    { coach: "What happened?", hint: "Sebutkan transport kamu delayed.", sampleAnswer: "My train is delayed because of a signal problem.", focus: "Give a reason", expectedKeywords: ["delayed", "because"], indonesianExplanation: "" },
    { coach: "When will you arrive?", hint: "Kasih estimasi in about + time.", sampleAnswer: "I'll be there in about 20 minutes.", focus: "Give an estimate", expectedKeywords: ["in about", "minutes"], indonesianExplanation: "" },
  ],
  "explaining-a-viewpoint": [
    { coach: "What's your take on this?", hint: "From my perspective, ...", sampleAnswer: "From my perspective, some regulation is necessary.", focus: "Viewpoint", expectedKeywords: ["from my perspective"], indonesianExplanation: "" },
    { coach: "Why?", hint: "The reason is ...", sampleAnswer: "The reason is it protects users from misuse and misinformation.", focus: "Reason", expectedKeywords: ["the reason is"], indonesianExplanation: "" },
    { coach: "I disagree. It could slow innovation.", hint: "Acknowledge: I see the other side, but...", sampleAnswer: "I see the other side, but basic safety rules can still support innovation.", focus: "Acknowledge + respond", expectedKeywords: ["other side", "but"], indonesianExplanation: "" },
  ],
  "explaining-benefits-and-risks": [
    { coach: "What is the main benefit?", hint: "The main benefit is ...", sampleAnswer: "The main benefit is faster onboarding for new hires.", focus: "Benefit 1", expectedKeywords: ["main benefit"], indonesianExplanation: "" },
    { coach: "Give another benefit.", hint: "Another benefit is ...", sampleAnswer: "Another benefit is fewer repeated questions for the team.", focus: "Benefit 2", expectedKeywords: ["another benefit"], indonesianExplanation: "" },
    { coach: "Now mention a key risk and mitigation.", hint: "A key risk is... To reduce the risk, we can...", sampleAnswer: "A key risk is that it becomes outdated. To reduce the risk, we can review it monthly and assign an owner.", focus: "Risk + mitigation", expectedKeywords: ["risk", "reduce"], indonesianExplanation: "" },
  ],
  "explaining-causes": [
    { coach: "Why do you think this problem is happening?", hint: "Jawab dengan one possible cause is...", sampleAnswer: "One possible cause is the new checkout design.", focus: "Possible cause", expectedKeywords: ["possible cause"], indonesianExplanation: "" },
    { coach: "What evidence do we have?", hint: "Pakai based on the data.", sampleAnswer: "Based on the data, drop-offs increased right after the redesign.", focus: "Evidence", expectedKeywords: ["based on", "data"], indonesianExplanation: "" },
    { coach: "How can we confirm this?", hint: "Usulkan test/compare.", sampleAnswer: "Let's compare load times and run a small A/B test.", focus: "Confirm", expectedKeywords: ["compare", "test"], indonesianExplanation: "" },
  ],
  "explaining-local-norms": [
    { coach: "Explain a local norm about disagreement.", hint: "In our context... people tend to...", sampleAnswer: "In our context, people tend to be indirect when disagreeing in group settings.", focus: "Norm", expectedKeywords: ["context", "tend to", "indirect"], indonesianExplanation: "" },
    { coach: "Explain what's generally expected.", hint: "It's generally expected that...", sampleAnswer: "It's generally expected that you raise concerns one-on-one first.", focus: "Expectation", expectedKeywords: ["generally expected", "one-on-one"], indonesianExplanation: "" },
    { coach: "Offer a practical tip.", hint: "It might help to...", sampleAnswer: "It might help to start with appreciation, then ask a question instead of stating a critique.", focus: "Tip", expectedKeywords: ["might help", "appreciation", "question"], indonesianExplanation: "" },
  ],
  "explaining-options": [
    { coach: "Can you explain our options?", hint: "Mulai dengan We have two options.", sampleAnswer: "We have two options. Option A is a quick fix we can deliver this week.", focus: "Option A", expectedKeywords: ["two options", "option a"], indonesianExplanation: "" },
    { coach: "And option B?", hint: "Option B is..., but it takes...", sampleAnswer: "Option B is a more robust solution, but it takes two more weeks.", focus: "Option B", expectedKeywords: ["option b", "but"], indonesianExplanation: "" },
    { coach: "Explain the trade-off and recommend one.", hint: "The trade-off is... I'd recommend...", sampleAnswer: "The trade-off is speed versus long-term stability. I'd recommend option B if the timeline allows.", focus: "Trade-off + recommendation", expectedKeywords: ["trade-off", "recommend"], indonesianExplanation: "" },
  ],
  "explaining-progress": [
    { coach: "How's your goal going?", hint: "Mulai dengan: I'm making good progress.", sampleAnswer: "I'm making good progress.", focus: "Share progress", expectedKeywords: ["progress"], indonesianExplanation: "" },
    { coach: "What have you been doing?", hint: "Jawab dengan I've been practicing ...", sampleAnswer: "I've been practicing every morning for five minutes.", focus: "Explain practice habit", expectedKeywords: ["been", "practicing"], indonesianExplanation: "" },
    { coach: "What still needs work?", hint: "Jawab dengan I still need to ...", sampleAnswer: "I still need to improve my pronunciation.", focus: "State what's next to improve", expectedKeywords: ["still", "improve"], indonesianExplanation: "" },
  ],
  "explaining-why-you-prefer-something": [
    { coach: "Which one do you prefer?", hint: "Jawab dengan I prefer ...", sampleAnswer: "I prefer the earlier flight.", focus: "State preference", expectedKeywords: ["prefer"], indonesianExplanation: "" },
    { coach: "Why?", hint: "Jawab dengan because + reason.", sampleAnswer: "Because it gives us more time in the afternoon.", focus: "Explain reason", expectedKeywords: ["because", "time"], indonesianExplanation: "" },
    { coach: "What is the main reason?", hint: "Gunakan The main reason is ...", sampleAnswer: "The main reason is I don't want to arrive too late.", focus: "State main reason", expectedKeywords: ["main reason", "don't want"], indonesianExplanation: "" },
  ],
  "explaining-your-task": [
    { coach: "Hi. What are you working on today?", hint: "Jelaskan task kamu: I'm working on ...", sampleAnswer: "I'm working on the onboarding email flow.", focus: "State current task", expectedKeywords: ["working on"], indonesianExplanation: "" },
    { coach: "Great. What's the next step?", hint: "Gunakan Next, I'll ...", sampleAnswer: "Next, I'll review the copy and update the templates.", focus: "State next step", expectedKeywords: ["next", "review"], indonesianExplanation: "" },
    { coach: "Any blockers?", hint: "Jawab singkat (none / one blocker).", sampleAnswer: "Not right now, but I may need feedback later.", focus: "Mention blockers", expectedKeywords: ["not", "feedback"], indonesianExplanation: "" },
  ],
  "expressing-certainty-and-doubt": [
    { coach: "Will this change work as expected?", hint: "Jawab dengan I'm fairly confident... given...", sampleAnswer: "I'm fairly confident it will, given the support trends.", focus: "Confidence", expectedKeywords: ["fairly confident", "given"], indonesianExplanation: "" },
    { coach: "So we can roll it out broadly?", hint: "I'm not entirely convinced... strong chance...", sampleAnswer: "I'm not entirely convinced. There's a strong chance we'll see edge cases.", focus: "Doubt", expectedKeywords: ["not entirely convinced", "strong chance"], indonesianExplanation: "" },
    { coach: "Close with a safe plan.", hint: "Limited rollout + metrics.", sampleAnswer: "Let's start with a limited rollout and define clear success metrics.", focus: "Plan", expectedKeywords: ["limited rollout", "metrics"], indonesianExplanation: "" },
  ],
  "expressing-priorities": [
    { coach: "What's your top priority?", hint: "Mulai dengan My top priority is...", sampleAnswer: "My top priority is shipping the core feature safely.", focus: "State top priority", expectedKeywords: ["top priority", "is"], indonesianExplanation: "" },
    { coach: "Why is that important?", hint: "Jawab dengan because + reason.", sampleAnswer: "Because it's the main value for users and the deadline is close.", focus: "Give reason", expectedKeywords: ["because", "deadline"], indonesianExplanation: "" },
    { coach: "Ask about my priorities.", hint: "Gunakan What about you? What's your top priority?", sampleAnswer: "What about you? What's your top priority?", focus: "Ask other priorities", expectedKeywords: ["what about you", "top priority"], indonesianExplanation: "" },
  ],
  "final-test-practice": [
    { coach: "Hello. What is your name?", hint: "Jawab dengan nama lengkap atau nama panggilan.", sampleAnswer: "My name is Alya.", focus: "Test identity", expectedKeywords: ["name", "alya"], indonesianExplanation: "" },
    { coach: "Where are you from?", hint: "Jawab asal dengan I'm from ...", sampleAnswer: "I'm from Indonesia.", focus: "Test origin", expectedKeywords: ["i'm", "from", "indonesia"], indonesianExplanation: "" },
    { coach: "What do you do every morning?", hint: "Sebutkan rutinitas belajar dan jam.", sampleAnswer: "I study English at seven.", focus: "Test routine", expectedKeywords: ["study", "english", "seven"], indonesianExplanation: "" },
    { coach: "When is your class?", hint: "Kalau perlu, minta pengulangan dulu.", sampleAnswer: "Sorry, can you repeat that, please?", focus: "Clarification", expectedKeywords: ["sorry", "repeat", "?"], indonesianExplanation: "" },
    { coach: "Sure. When is your class?", hint: "Jawab hari dan jam.", sampleAnswer: "It is on Tuesday at eight.", focus: "Schedule answer", expectedKeywords: ["tuesday", "eight"], indonesianExplanation: "" },
  ],
  "finding-a-place-mission": [
    { coach: "Hello. Can I help you?", hint: "Mulai sopan dan tanya cara ke room A.", sampleAnswer: "Excuse me. How do I get to room A?", focus: "Mission opening", expectedKeywords: ["excuse", "how", "get", "room", "?"], indonesianExplanation: "" },
    { coach: "Go straight and turn left.", hint: "Ulangi arahan lengkap.", sampleAnswer: "Go straight and turn left.", focus: "Combined directions", expectedKeywords: ["straight", "turn", "left"], indonesianExplanation: "" },
    { coach: "Room A is next to the office.", hint: "Konfirmasi lantai.", sampleAnswer: "Is it on the first floor?", focus: "Floor confirmation", expectedKeywords: ["first", "floor", "?"], indonesianExplanation: "" },
    { coach: "Yes, it is.", hint: "Tutup dengan thank you.", sampleAnswer: "Great. Thank you.", focus: "Closing", expectedKeywords: ["great"], indonesianExplanation: "" },
  ],
  "finding-middle-ground": [
    { coach: "We disagree. How can we move forward?", hint: "Mulai dengan Maybe we can find a compromise.", sampleAnswer: "Maybe we can find a compromise.", focus: "Suggest compromise", expectedKeywords: ["compromise"], indonesianExplanation: "" },
    { coach: "Propose a middle-ground option.", hint: "A compromise could be...", sampleAnswer: "A compromise could be launching to 10% of users first.", focus: "Propose middle ground", expectedKeywords: ["could be", "users"], indonesianExplanation: "" },
    { coach: "Ask for agreement with a condition.", hint: "If we do X, can we agree on Y?", sampleAnswer: "If we do a small rollout, can we agree on one extra day for testing?", focus: "Confirm agreement", expectedKeywords: ["if", "agree"], indonesianExplanation: "" },
  ],
  "first-conversation-mission": [
    { coach: "Hi, good morning. My name is Sara.", hint: "Sapa balik dan sebutkan namamu.", sampleAnswer: "Good morning. My name is Arif.", focus: "Greeting and name", expectedKeywords: ["good morning", "my name is", "i'm", "i am"], indonesianExplanation: "Gabungkan greeting dan nama dalam dua kalimat pendek agar pembuka percakapan terasa jelas." },
    { coach: "Nice to meet you. Where are you from?", hint: "Jawab asalmu lalu tanyakan balik.", sampleAnswer: "I'm from Indonesia. How about you?", focus: "Origin and follow-up", expectedKeywords: ["from", "indonesia", "how about you", "?"], indonesianExplanation: "Setelah menjawab asal, tanyakan balik supaya percakapan tidak berhenti." },
    { coach: "I'm from Malaysia. Nice to meet you.", hint: "Balas dan tutup percakapan.", sampleAnswer: "Nice to meet you too. See you later.", focus: "Closing mission", expectedKeywords: ["nice to meet you too", "see you", "later"], indonesianExplanation: "Tutup misi dengan respons sopan dan closing singkat seperti 'See you later'." },
  ],
  "framing-a-complex-topic": [
    { coach: "Can you present the proposal?", hint: "Start with Today I'd like to...", sampleAnswer: "Sure. Today I'd like to walk you through the proposal and why it matters.", focus: "Opener", expectedKeywords: ["today", "walk you through", "matters"], indonesianExplanation: "" },
    { coach: "Define the key term clearly.", hint: "By X, I mean...", sampleAnswer: "By 'modular architecture', I mean we separate features into independent components.", focus: "Definition", expectedKeywords: ["by", "i mean", "independent"], indonesianExplanation: "" },
    { coach: "State the purpose and preview the structure.", hint: "The purpose of this is... First, I'll...", sampleAnswer: "The purpose of this is to reduce coupling and speed up delivery. First, I'll outline the problem, then the proposed approach.", focus: "Purpose + structure", expectedKeywords: ["purpose", "first", "then"], indonesianExplanation: "" },
  ],
  "framing-the-problem": [
    { coach: "We have a complex issue to solve.", hint: "Mulai dengan ajak tim framing dulu.", sampleAnswer: "Got it. Let's define the problem statement first.", focus: "Frame first", expectedKeywords: ["define", "problem"], indonesianExplanation: "" },
    { coach: "Okay. What should we clarify first?", hint: "Tanya scope.", sampleAnswer: "Can we agree on the scope? Which area is affected?", focus: "Scope", expectedKeywords: ["scope", "affected"], indonesianExplanation: "" },
    { coach: "How do we know we succeeded?", hint: "Tanya success criteria.", sampleAnswer: "What does success look like for the next four weeks?", focus: "Success criteria", expectedKeywords: ["success", "look like"], indonesianExplanation: "" },
  ],
  "giving-a-short-update": [
    { coach: "Quick update: how is it going?", hint: "Jawab dengan progress.", sampleAnswer: "I'm making good progress. I'm almost done with the summary.", focus: "Share progress", expectedKeywords: ["progress", "almost"], indonesianExplanation: "" },
    { coach: "Great. What's left?", hint: "Sebutkan 1-2 item yang tersisa.", sampleAnswer: "I still need to update the risk section and double-check the numbers.", focus: "Say what's left", expectedKeywords: ["still need", "double-check"], indonesianExplanation: "" },
    { coach: "Any concerns?", hint: "Sebutkan 1 concern dengan might need.", sampleAnswer: "One concern is time. I might need an extra hour to review everything.", focus: "Mention a concern", expectedKeywords: ["concern", "might"], indonesianExplanation: "" },
  ],
  "giving-actionable-feedback": [
    { coach: "Give one suggestion, starting with a positive frame.", hint: "Overall it's... One thing I'd suggest is...", sampleAnswer: "Overall it's solid. One thing I'd suggest is leading with the decision.", focus: "Suggestion", expectedKeywords: ["overall", "one thing"], indonesianExplanation: "" },
    { coach: "Explain the impact.", hint: "The impact is that...", sampleAnswer: "The impact is that stakeholders scan quickly and might miss the point.", focus: "Impact", expectedKeywords: ["impact", "might miss"], indonesianExplanation: "" },
    { coach: "Propose a concrete improvement and invite revision.", hint: "A concrete improvement would be... Would you be open to...?", sampleAnswer: "A concrete improvement would be a one-line summary at the top. Would you be open to revising it and sending a second draft?", focus: "Improve + invite", expectedKeywords: ["concrete", "open to"], indonesianExplanation: "" },
  ],
  "giving-constructive-feedback": [
    { coach: "Any feedback on my demo?", hint: "Mulai positif + I noticed...", sampleAnswer: "Overall it was clear. I noticed the introduction was a bit long.", focus: "Positive + observation", expectedKeywords: ["overall", "noticed"], indonesianExplanation: "" },
    { coach: "What was the impact?", hint: "Jelaskan impact dengan so.", sampleAnswer: "Some people lost focus, so the key message came late.", focus: "Explain impact", expectedKeywords: ["so", "message"], indonesianExplanation: "" },
    { coach: "What would you suggest?", hint: "Gunakan One suggestion is... / It might help if...", sampleAnswer: "One suggestion is to start with the main takeaway. It might help if you keep the intro under one minute.", focus: "Give a suggestion", expectedKeywords: ["suggestion", "might help"], indonesianExplanation: "" },
  ],
  "giving-phone-numbers": [
    { coach: "What is your phone number?", hint: "Sebutkan nomor telepon dalam kelompok kecil.", sampleAnswer: "It's zero eight one two, three four five six.", focus: "Giving a phone number", expectedKeywords: ["it's", "zero", "eight", "one"], indonesianExplanation: "" },
    { coach: "Let me check. Zero eight one two, three four five six?", hint: "Konfirmasi dengan: Yes, that's correct.", sampleAnswer: "Yes, that's correct.", focus: "Confirming a number", expectedKeywords: ["that's", "correct"], indonesianExplanation: "" },
    { coach: "My number is zero eight one three, two two five five.", hint: "Minta diulang dengan sopan.", sampleAnswer: "Can you repeat that, please?", focus: "Asking for repetition", expectedKeywords: ["repeat", "?"], indonesianExplanation: "" },
  ],
  "giving-simple-reasons": [
    { coach: "Do you like this cafe?", hint: "Jawab yes/no + opini singkat.", sampleAnswer: "Yes, I like it.", focus: "Give an opinion", expectedKeywords: ["yes", "like"], indonesianExplanation: "" },
    { coach: "Why?", hint: "Jawab dengan because + reason.", sampleAnswer: "Because the coffee is good.", focus: "Give a reason", expectedKeywords: ["because", "good"], indonesianExplanation: "" },
    { coach: "What else do you like about it?", hint: "Tambahkan satu alasan lain.", sampleAnswer: "Because it is quiet and relaxing.", focus: "Add another reason", expectedKeywords: ["because", "quiet"], indonesianExplanation: "" },
  ],
  "goals-progress-mission": [
    { coach: "What's your goal right now?", hint: "Goal + deadline (by ...).", sampleAnswer: "My goal is to speak more confidently by the end of this month.", focus: "Goal with deadline", expectedKeywords: ["goal", "by"], indonesianExplanation: "" },
    { coach: "How's it going?", hint: "Progress + I've been practicing ...", sampleAnswer: "I'm making progress. I've been practicing every morning.", focus: "Progress update", expectedKeywords: ["progress", "been"], indonesianExplanation: "" },
    { coach: "Any challenges and next steps?", hint: "Challenge + next step plan.", sampleAnswer: "The biggest challenge is staying consistent after work. My next step is to practice three times this week.", focus: "Challenge and next step", expectedKeywords: ["challenge", "next step", "times"], indonesianExplanation: "" },
  ],
  "guiding-a-decision": [
    { coach: "Structure the options.", hint: "We have three options...", sampleAnswer: "We have three options: pilot, phased rollout, or full rollout.", focus: "Options", expectedKeywords: ["options"], indonesianExplanation: "" },
    { coach: "Explain the trade-off and recommend an option.", hint: "The trade-off is... Given our constraints, I'd recommend...", sampleAnswer: "The trade-off is speed versus risk and operational load. Given our constraints, I'd recommend a phased rollout with clear monitoring.", focus: "Trade-off + recommend", expectedKeywords: ["trade-off", "constraints", "recommend"], indonesianExplanation: "" },
    { coach: "Confirm agreement on next steps.", hint: "Can we agree on... review weekly...", sampleAnswer: "Can we agree on the scope today and review metrics weekly?", focus: "Agreement", expectedKeywords: ["agree", "scope", "weekly"], indonesianExplanation: "" },
  ],
  "handling-a-simple-complaint": [
    { coach: "Hi. How can I help you?", hint: "Mulai dengan: There's a problem with ...", sampleAnswer: "Hi. There's a problem with my room.", focus: "Start complaint politely", expectedKeywords: ["problem", "room"], indonesianExplanation: "" },
    { coach: "I'm sorry to hear that. What's wrong?", hint: "Jelaskan masalahnya (isn't working).", sampleAnswer: "The air conditioning isn't working.", focus: "Explain the issue", expectedKeywords: ["isn't working"], indonesianExplanation: "" },
    { coach: "Okay. What would you like us to do?", hint: "Minta bantuan (Could you...) atau opsi (Could I...).", sampleAnswer: "Could you send someone to take a look? Could I change rooms if it can't be fixed?", focus: "Request help or alternative", expectedKeywords: ["could", "send", "change"], indonesianExplanation: "" },
  ],
  "handling-challenging-questions": [
    { coach: "Isn't this approach too risky?", hint: "That's a fair question... Let me clarify...", sampleAnswer: "That's a fair question. Let me clarify what risk we're accepting.", focus: "Acknowledge", expectedKeywords: ["fair question", "clarify"], indonesianExplanation: "" },
    { coach: "Give the short answer and condition.", hint: "The short answer is...", sampleAnswer: "The short answer is: it's manageable if we pilot first and monitor closely.", focus: "Short answer", expectedKeywords: ["short answer", "manageable", "pilot"], indonesianExplanation: "" },
    { coach: "Close with emphasis and a fallback plan.", hint: "What I'd emphasize... If adoption stalls...", sampleAnswer: "What I'd emphasize is that standards need ownership and enforcement. If adoption stalls, we pause expansion and revisit the design.", focus: "Emphasis + fallback", expectedKeywords: ["emphasize", "ownership", "pause"], indonesianExplanation: "" },
  ],
  "handling-concerns": [
    { coach: "I'm concerned this change will disrupt our team.", hint: "Mulai dengan I understand the concern.", sampleAnswer: "I understand the concern.", focus: "Acknowledge", expectedKeywords: ["understand", "concern"], indonesianExplanation: "" },
    { coach: "Ask me what I mean.", hint: "Could you clarify...?", sampleAnswer: "Could you clarify what disruption you expect?", focus: "Clarify", expectedKeywords: ["clarify"], indonesianExplanation: "" },
    { coach: "Offer a mitigation plan.", hint: "To reduce the risk, we can...", sampleAnswer: "To reduce the risk, we can run a two-week trial, send weekly summaries, and gather feedback.", focus: "Mitigation", expectedKeywords: ["reduce", "trial", "feedback"], indonesianExplanation: "" },
  ],
  "handling-objections": [
    { coach: "I'm concerned this plan will slow us down.", hint: "Mulai dengan I understand the concern.", sampleAnswer: "I understand the concern.", focus: "Acknowledge", expectedKeywords: ["understand", "concern"], indonesianExplanation: "" },
    { coach: "Ask me what part feels risky.", hint: "Gunakan What part feels risky to you?", sampleAnswer: "What part feels risky to you?", focus: "Clarify", expectedKeywords: ["risky"], indonesianExplanation: "" },
    { coach: "Offer a revised proposal.", hint: "Would it help if... / What if we...", sampleAnswer: "Would it help if we limit reviews to high-risk changes only? What if we define simple criteria together?", focus: "Revise proposal", expectedKeywords: ["would it help", "what if"], indonesianExplanation: "" },
  ],
  "handling-sensitive-feedback": [
    { coach: "How did the last review go?", hint: "Mulai dengan I wanted to flag...", sampleAnswer: "It went well overall. I wanted to flag one point about the messaging.", focus: "Opener", expectedKeywords: ["flag", "messaging"], indonesianExplanation: "" },
    { coach: "What was the issue?", hint: "Fokus ke impact.", sampleAnswer: "The impact is that some teams interpreted it as a hard deadline.", focus: "Impact", expectedKeywords: ["impact", "interpreted", "deadline"], indonesianExplanation: "" },
    { coach: "Suggest a fix politely.", hint: "Would you be open to...?", sampleAnswer: "Would you be open to adding an explicit 'earliest possible' line to clarify the timeline?", focus: "Suggestion", expectedKeywords: ["open to", "explicit", "clarify"], indonesianExplanation: "" },
  ],
  "health-appointment-mission": [
    { coach: "Hello. How can I help you today?", hint: "Bilang kamu ada janji + jamnya.", sampleAnswer: "Hi. I have an appointment at 3:30.", focus: "Check in for appointment", expectedKeywords: ["appointment", "3:30"], indonesianExplanation: "" },
    { coach: "Sure. What's your name?", hint: "Sebutkan nama dan eja.", sampleAnswer: "Raka Park. P-A-R-K.", focus: "Provide name and spelling", expectedKeywords: ["p-a-r-k", "raka"], indonesianExplanation: "" },
    { coach: "Thank you. What seems to be the problem?", hint: "Sebutkan gejala + durasi.", sampleAnswer: "I've had a cough for two days, and I feel tired.", focus: "Describe symptoms with duration", expectedKeywords: ["have had", "for", "days", "tired"], indonesianExplanation: "" },
  ],
  "help-and-problem-mission": [
    { coach: "Hi. Is everything okay?", hint: "Katakan kamu tidak mengerti.", sampleAnswer: "Sorry, I don't understand.", focus: "Mission opening", expectedKeywords: ["sorry", "don't", "understand"], indonesianExplanation: "" },
    { coach: "That's okay. What is the problem?", hint: "Jelaskan masalah file.", sampleAnswer: "I can't open this file.", focus: "Problem", expectedKeywords: ["can't", "open", "file"], indonesianExplanation: "" },
    { coach: "Can you send me a screenshot?", hint: "Terima dan minta tunggu sebentar.", sampleAnswer: "Sure. Can you wait a minute?", focus: "Request", expectedKeywords: ["sure", "wait", "minute", "?"], indonesianExplanation: "" },
    { coach: "No problem.", hint: "Kirim screenshot.", sampleAnswer: "Here is the screenshot.", focus: "Sending info", expectedKeywords: ["screenshot"], indonesianExplanation: "" },
    { coach: "Good. Click this button.", hint: "Katakan berhasil dan terima kasih.", sampleAnswer: "It works. Thank you for your help.", focus: "Closing", expectedKeywords: ["works", "help"], indonesianExplanation: "" },
  ],
  "idea-presentation-mission": [
    { coach: "Present your idea in 2-3 sentences with signposting.", hint: "Today I'd like to... First... Next... Finally...", sampleAnswer: "Today I'd like to propose a shared onboarding checklist. First, the problem is inconsistency. Next, the proposal is a checklist plus a buddy. Finally, we'll pilot it next week.", focus: "Presentation with signposting", expectedKeywords: ["today", "first", "next", "finally"], indonesianExplanation: "" },
    { coach: "Explain benefits and one risk with mitigation.", hint: "The main benefit is... Another benefit is... A key risk is... To reduce the risk...", sampleAnswer: "The main benefit is faster onboarding. Another benefit is fewer repeated questions. A key risk is it becomes outdated. To reduce the risk, we'll review it monthly and assign an owner.", focus: "Benefits + risk + mitigation", expectedKeywords: ["benefit", "risk", "reduce"], indonesianExplanation: "" },
    { coach: "Answer a question and offer follow-up if needed.", hint: "That's a good question... I'm not sure yet, but I can follow up by...", sampleAnswer: "That's a good question. As far as I know, it takes about one day. I'm not sure about maintenance yet, but I can follow up by tomorrow.", focus: "Q&A", expectedKeywords: ["good question", "as far as I know", "follow up"], indonesianExplanation: "" },
  ],
  "identifying-assumptions": [
    { coach: "We should cut steps to increase conversion.", hint: "Surface an assumption politely.", sampleAnswer: "It seems you're assuming fewer steps automatically mean better conversion.", focus: "Assumption", expectedKeywords: ["assuming", "steps", "conversion"], indonesianExplanation: "" },
    { coach: "Ask a clarifying question about the premise.", hint: "What are we assuming about...?", sampleAnswer: "What are we assuming about user trust and clarity?", focus: "Premise", expectedKeywords: ["assuming", "trust", "clarity"], indonesianExplanation: "" },
    { coach: "Make it testable and propose a next step.", hint: "If that's true, then... Let's...", sampleAnswer: "If that's true, then we should see drop-offs mainly on longer forms. Let's separate essential steps from redundant ones and measure impact.", focus: "Test", expectedKeywords: ["if that's true", "measure"], indonesianExplanation: "" },
  ],
  "information-discussion-mission": [
    { coach: "I just read an article about remote work and productivity. What was the main point?", hint: "The article is about... The main point is...", sampleAnswer: "The article is about remote work and productivity. The main point is clear rules improve focus.", focus: "Summary", expectedKeywords: ["article is about", "main point"], indonesianExplanation: "" },
    { coach: "Do you think the source is reliable? Why or why not?", hint: "I'm not sure it's reliable because... I'd check...", sampleAnswer: "I'm not sure it's reliable because it doesn't cite data. I'd check official reports or reputable outlets.", focus: "Reliability", expectedKeywords: ["reliable", "because", "I'd check"], indonesianExplanation: "" },
    { coach: "I found another source that says the opposite. How does that change your view, and what should we do next?", hint: "I wasn't aware... That changes things... I'd like to understand... Can you share...?", sampleAnswer: "I wasn't aware of that. That changes things. I'd like to understand the methodology. Can you share the link so we can revise our conclusion?", focus: "New info + next steps", expectedKeywords: ["aware", "changes", "understand", "share"], indonesianExplanation: "" },
  ],
  "invitation-mission": [
    { coach: "Do you want to grab coffee tomorrow?", hint: "Tolak dengan sopan dan beri alasan singkat.", sampleAnswer: "Thanks, but I can't tomorrow. Something came up.", focus: "Decline with a reason", expectedKeywords: ["can't", "something came up"], indonesianExplanation: "" },
    { coach: "No problem. How about Saturday?", hint: "Setuju, lalu tanya jamnya.", sampleAnswer: "Saturday is good. What time?", focus: "Ask for the time", expectedKeywords: ["what time", "?"], indonesianExplanation: "" },
    { coach: "Does 3 pm work for you?", hint: "Setuju dan konfirmasi tempat.", sampleAnswer: "Yes, 3 pm works. Where should we meet?", focus: "Confirm time and ask place", expectedKeywords: ["works", "where should we meet", "?"], indonesianExplanation: "" },
    { coach: "Let's meet at the cafe near the station.", hint: "Tutup percakapan dengan sopan.", sampleAnswer: "Great. See you then.", focus: "Close the plan", expectedKeywords: ["see you then"], indonesianExplanation: "" },
  ],
  "inviting-someone": [
    { coach: "Do you want to watch a movie tonight?", hint: "Reaksi positif, lalu tanya detailnya.", sampleAnswer: "That sounds fun. What time?", focus: "React and ask details", expectedKeywords: ["that sounds fun", "what time", "?"], indonesianExplanation: "" },
    { coach: "How about 8 pm?", hint: "Setuju, lalu tanya filmnya.", sampleAnswer: "8 pm works. Which movie?", focus: "Confirm time", expectedKeywords: ["works", "which movie", "?"], indonesianExplanation: "" },
    { coach: "The new action movie.", hint: "Terima ajakan dengan sopan.", sampleAnswer: "Nice. I'd love to go.", focus: "Accept politely", expectedKeywords: ["i'd love to", "go"], indonesianExplanation: "" },
  ],
  "joining-a-simple-meeting": [
    { coach: "Any updates before we close?", hint: "Minta kesempatan bicara dengan sopan.", sampleAnswer: "I'd like to add one point about the schedule.", focus: "Speak up politely", expectedKeywords: ["like to", "point"], indonesianExplanation: "" },
    { coach: "Sure, go ahead.", hint: "Sampaikan saran singkat.", sampleAnswer: "I suggest we move the deadline to Thursday to reduce risk.", focus: "Give a suggestion", expectedKeywords: ["suggest", "deadline"], indonesianExplanation: "" },
    { coach: "That makes sense. Anything else?", hint: "Tutup dan tanya next step.", sampleAnswer: "No. What are the next steps?", focus: "Ask for next steps", expectedKeywords: ["next steps"], indonesianExplanation: "" },
  ],
  "leadership-coaching-mission": [
    { coach: "We're stuck between moving fast and reducing risk. What direction would you set?", hint: "The direction I'd like to set is... What options do you see?", sampleAnswer: "The direction I'd like to set is stabilizing billing first. What options do you see right now?", focus: "Direction + options", expectedKeywords: ["direction", "options"], indonesianExplanation: "" },
    { coach: "That helps. What's the smallest next step we could take, and what would success look like?", hint: "What would success look like? smallest next step?", sampleAnswer: "What would success look like for the pilot, and what's the smallest next step you can take today?", focus: "Coach", expectedKeywords: ["success", "smallest next step"], indonesianExplanation: "" },
    { coach: "Given our constraints, which option would you recommend, and can we align on it today?", hint: "Given our constraints... Can we agree on...?", sampleAnswer: "Given our constraints, I'd recommend a phased rollout. Can we agree on scope today and review metrics weekly?", focus: "Decision", expectedKeywords: ["constraints", "recommend", "agree"], indonesianExplanation: "" },
  ],
  "making-a-proposal": [
    { coach: "What do you propose?", hint: "Gunakan I propose we...", sampleAnswer: "I propose we do a small pilot first.", focus: "Make proposal", expectedKeywords: ["propose"], indonesianExplanation: "" },
    { coach: "What's the timeline?", hint: "How about we run it for ... weeks?", sampleAnswer: "How about we run it for two weeks and review the results?", focus: "Suggest timeline", expectedKeywords: ["how about", "weeks"], indonesianExplanation: "" },
    { coach: "Check if it works for me.", hint: "Would that work for you?", sampleAnswer: "Would that work for you?", focus: "Check agreement", expectedKeywords: ["would", "work"], indonesianExplanation: "" },
  ],
  "making-a-simple-decision": [
    { coach: "We have two options. What do you prefer?", hint: "Gunakan I'd rather + because.", sampleAnswer: "I'd rather fix it now because users are blocked.", focus: "State preference with reason", expectedKeywords: ["rather", "because"], indonesianExplanation: "" },
    { coach: "But it's late. Any compromise?", hint: "Gunakan We could ...", sampleAnswer: "We could do a quick rollback and review tomorrow.", focus: "Suggest compromise", expectedKeywords: ["could", "rollback"], indonesianExplanation: "" },
    { coach: "Okay. What's the decision?", hint: "Gunakan Let's ...", sampleAnswer: "Okay, let's roll back now.", focus: "Make decision", expectedKeywords: ["let's"], indonesianExplanation: "" },
  ],
  "making-an-appointment": [
    { coach: "Good morning. Green Clinic. How can I help you?", hint: "Minta buat janji (polite).", sampleAnswer: "Hi. I'd like to make an appointment.", focus: "Make a polite request", expectedKeywords: ["i'd like", "appointment"], indonesianExplanation: "" },
    { coach: "Sure. What day works for you?", hint: "Usulkan waktu.", sampleAnswer: "Is tomorrow afternoon okay?", focus: "Suggest a day/time", expectedKeywords: ["tomorrow", "afternoon"], indonesianExplanation: "" },
    { coach: "We have 3:30 p.m. available.", hint: "Terima dan konfirmasi.", sampleAnswer: "Great. I'll take it.", focus: "Accept the time", expectedKeywords: ["i'll take", "3:30"], indonesianExplanation: "" },
  ],
  "making-next-step-plans": [
    { coach: "What's your next step?", hint: "Jawab dengan My next step is to ...", sampleAnswer: "My next step is to practice with Conversation Coach.", focus: "State next step", expectedKeywords: ["next step", "to"], indonesianExplanation: "" },
    { coach: "How often will you do it this week?", hint: "Jawab dengan ... times this week.", sampleAnswer: "I'll do it three times this week.", focus: "Set schedule", expectedKeywords: ["times", "week"], indonesianExplanation: "" },
    { coach: "Great. How will you keep it realistic?", hint: "Gunakan keep it simple.", sampleAnswer: "I'm going to keep it simple and do short sessions.", focus: "Keep the plan realistic", expectedKeywords: ["keep", "simple"], indonesianExplanation: "" },
  ],
  "making-plans": [
    { coach: "Are you free tomorrow?", hint: "Jawab singkat, lalu tanya rencananya.", sampleAnswer: "Yes, I think so. Why?", focus: "Check availability", expectedKeywords: ["True", "why"], indonesianExplanation: "" },
    { coach: "Let's get coffee after work.", hint: "Tanyakan jamnya dengan pertanyaan pendek.", sampleAnswer: "Sure. What time?", focus: "Ask the time", expectedKeywords: ["what time", "?"], indonesianExplanation: "" },
    { coach: "How about 6 pm?", hint: "Setuju, lalu tanya tempat ketemunya.", sampleAnswer: "6 pm works for me. Where should we meet?", focus: "Confirm and ask place", expectedKeywords: ["works for me", "where should we meet", "?"], indonesianExplanation: "" },
  ],
  "making-simple-requests": [
    { coach: "What do you need?", hint: "Minta link dengan sopan.", sampleAnswer: "Can you send me the link, please?", focus: "Polite request", expectedKeywords: ["send", "link", "?"], indonesianExplanation: "" },
    { coach: "Yes, of course.", hint: "Ucapkan terima kasih.", sampleAnswer: "Thank you.", focus: "Thanking", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "Can you wait a minute?", hint: "Terima request untuk menunggu.", sampleAnswer: "Sure. No problem.", focus: "Accepting request", expectedKeywords: ["sure", "problem"], indonesianExplanation: "" },
    { coach: "Here is the link.", hint: "Tutup dengan thanks.", sampleAnswer: "Great. Thanks.", focus: "Closing", expectedKeywords: ["great"], indonesianExplanation: "" },
  ],
  "managing-expectations": [
    { coach: "Can we deliver the full scope by next week?", hint: "Start with what you can commit to.", sampleAnswer: "What we can commit to is a smaller release by next week.", focus: "Commitment", expectedKeywords: ["commit", "smaller"], indonesianExplanation: "" },
    { coach: "When can we deliver everything?", hint: "The earliest we can deliver... assuming...", sampleAnswer: "The earliest we can deliver the full scope is two weeks later, assuming no new blockers.", focus: "Timeline + condition", expectedKeywords: ["earliest", "assuming", "blockers"], indonesianExplanation: "" },
    { coach: "Define success criteria.", hint: "Success means...", sampleAnswer: "Success means fewer incidents and a stable rollout with clear monitoring.", focus: "Success", expectedKeywords: ["success means", "stable"], indonesianExplanation: "" },
  ],
  "meeting-participation-mission": [
    { coach: "What's the first point you want to bring up today?", hint: "I'd like to bring up...", sampleAnswer: "I'd like to bring up the timeline for the next release.", focus: "Open topic", expectedKeywords: ["bring up", "timeline"], indonesianExplanation: "" },
    { coach: "Okay. Does this include the admin dashboard work, or is that separate?", hint: "Just to clarify... Does this include...? out of scope...", sampleAnswer: "Just to clarify, does this include the admin dashboard changes? If not, that's out of scope for now.", focus: "Clarify scope", expectedKeywords: ["clarify", "include", "out of scope"], indonesianExplanation: "" },
    { coach: "Thanks. Before we wrap up, do you have any feedback, and what are the action items?", hint: "Overall... I noticed... To summarize... Action items are...", sampleAnswer: "Overall it was clear, but I noticed the intro was long. To summarize, action items are: I'll update the tickets, and you'll confirm the design handoff.", focus: "Feedback + summary", expectedKeywords: ["noticed", "to summarize", "action items"], indonesianExplanation: "" },
  ],
  "negotiation-mission": [
    { coach: "What's your top priority?", hint: "My top priority is ... + ask mine.", sampleAnswer: "My top priority is quality. What matters most to you?", focus: "Priorities", expectedKeywords: ["top priority", "matters most"], indonesianExplanation: "" },
    { coach: "Make a proposal with a timeline.", hint: "I propose we ... for ... weeks.", sampleAnswer: "I propose we run a small pilot for two weeks.", focus: "Proposal", expectedKeywords: ["propose", "weeks"], indonesianExplanation: "" },
    { coach: "I’m concerned it will delay the launch. Respond and offer a compromise.", hint: "I understand the concern. Would it help if... A compromise could be...", sampleAnswer: "I understand the concern. Would it help if we prepare in parallel? A compromise could be launching to 10% first, then expanding if results look good.", focus: "Objection + compromise", expectedKeywords: ["understand", "help", "compromise"], indonesianExplanation: "" },
  ],
  "nuanced-opinion-mission": [
    { coach: "Do you think we should standardize the process across all teams?", hint: "To some extent... That said...", sampleAnswer: "To some extent, yes—especially for new projects. That said, we need exceptions for legacy systems.", focus: "Nuanced stance", expectedKeywords: ["to some extent", "that said"], indonesianExplanation: "" },
    { coach: "Some people say speed matters more, while others worry about stability. How do you see it?", hint: "On the one hand... On the other hand... On balance...", sampleAnswer: "On the one hand, speed matters. On the other hand, stability reduces risk. On balance, I'd prioritize stability with a limited rollout.", focus: "Balance", expectedKeywords: ["on the one hand", "on the other hand", "on balance"], indonesianExplanation: "" },
    { coach: "I still think a full rollout right now is the best option.", hint: "I see your point, but... I might frame it differently...", sampleAnswer: "I see your point, but I'm not sure I'd go that far. I might frame it differently: limited launch first, then full rollout after we review the data.", focus: "Soft disagreement", expectedKeywords: ["see your point", "frame", "limited"], indonesianExplanation: "" },
  ],
  "opening-a-meeting-point": [
    { coach: "What would you like to bring up?", hint: "Mulai dengan I'd like to bring up...", sampleAnswer: "I'd like to bring up the timeline for the next release.", focus: "Open a topic", expectedKeywords: ["bring up", "timeline"], indonesianExplanation: "" },
    { coach: "What's the main point?", hint: "Gunakan The main point is...", sampleAnswer: "The main point is we need to confirm the scope today.", focus: "State main point", expectedKeywords: ["main point", "scope"], indonesianExplanation: "" },
    { coach: "Thanks. I'd like to hear your thoughts too.", hint: "Gunakan I'd like to hear your thoughts.", sampleAnswer: "I'd like to hear your thoughts first, then we can decide.", focus: "Invite input", expectedKeywords: ["hear", "thoughts"], indonesianExplanation: "" },
  ],
  "opinion-conversation-mission": [
    { coach: "What do you think about this restaurant?", hint: "Jawab dengan opini + because.", sampleAnswer: "I think it's good because it's cheap.", focus: "Opinion with reason", expectedKeywords: ["i think", "because"], indonesianExplanation: "" },
    { coach: "Any concern?", hint: "Tolak halus: I'm not sure + might be ...", sampleAnswer: "I'm not sure. The service might be slow.", focus: "Polite concern", expectedKeywords: ["not sure", "might"], indonesianExplanation: "" },
    { coach: "That's fair. Do you have another idea?", hint: "Kasih alternatif + because.", sampleAnswer: "Yes. I think the cafe next door is better because it is quieter.", focus: "Suggest alternative with reason", expectedKeywords: ["better", "because"], indonesianExplanation: "" },
  ],
  "ordering-a-drink": [
    { coach: "Hi. What would you like?", hint: "Pesan teh dengan sopan.", sampleAnswer: "Can I have a tea, please?", focus: "Polite order", expectedKeywords: ["have", "tea", "?"], indonesianExplanation: "" },
    { coach: "Small or large?", hint: "Pilih ukuran kecil.", sampleAnswer: "Small, please.", focus: "Size choice", expectedKeywords: ["small"], indonesianExplanation: "" },
    { coach: "Anything else?", hint: "Katakan tidak ada lagi dengan sopan.", sampleAnswer: "No, thank you.", focus: "Finishing order", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "Here you go.", hint: "Tutup dengan thank you.", sampleAnswer: "Thank you.", focus: "Thanking", expectedKeywords: [], indonesianExplanation: "" },
  ],
  "past-experience-mission": [
    { coach: "Hey! What did you do yesterday?", hint: "Jawab dengan tempat + aktivitas (past).", sampleAnswer: "I went to the museum and took photos.", focus: "Tell where and what you did", expectedKeywords: ["went", "took"], indonesianExplanation: "" },
    { coach: "Nice. How was it?", hint: "Jawab dengan It was + adjective, lalu opini singkat.", sampleAnswer: "It was really interesting. I liked it.", focus: "Describe and give opinion", expectedKeywords: ["it was", "liked"], indonesianExplanation: "" },
    { coach: "Did you go with anyone?", hint: "Jawab dan sebutkan dengan siapa.", sampleAnswer: "Yes, I went with my friend.", focus: "Say who you went with", expectedKeywords: ["with", "friend"], indonesianExplanation: "" },
  ],
  "personal-story-mission": [
    { coach: "Tell me about something interesting that happened recently.", hint: "Mulai dengan scene: time + place + who.", sampleAnswer: "Last weekend, I was in Bandung with my cousin.", focus: "Start with scene", expectedKeywords: ["last", "was", "with"], indonesianExplanation: "" },
    { coach: "What happened?", hint: "Ceritakan 2 event pakai first/then.", sampleAnswer: "First, we explored the city. Then we got lost for a while.", focus: "Tell events in order", expectedKeywords: ["first", "then"], indonesianExplanation: "" },
    { coach: "How did you feel?", hint: "Sebutkan feeling + contrast (but).", sampleAnswer: "I felt nervous, but after we asked for directions, I felt relieved.", focus: "Describe feelings", expectedKeywords: ["felt", "but", "relieved"], indonesianExplanation: "" },
  ],
  "preference-discussion-mission": [
    { coach: "We have two options. Compare them.", hint: "Bandingin pakai but.", sampleAnswer: "Option A is easier, but it's more expensive.", focus: "Compare options", expectedKeywords: ["but", "more"], indonesianExplanation: "" },
    { coach: "Okay. Which do you prefer and why?", hint: "Jawab dengan I prefer ... because ...", sampleAnswer: "I prefer option B because it's cheaper.", focus: "Preference with reason", expectedKeywords: ["prefer", "because"], indonesianExplanation: "" },
    { coach: "Give one advantage and one downside, then confirm agreement.", hint: "The advantage is... One downside is... So we agree on...?", sampleAnswer: "The advantage is it's healthier. One downside is it takes time. So we agree on option B?", focus: "Pros/cons + agreement", expectedKeywords: ["advantage", "downside", "agree"], indonesianExplanation: "" },
  ],
  "presenting-evidence": [
    { coach: "Do we have data to support this?", hint: "Use According to...", sampleAnswer: "According to the support dashboard, drop-offs increased after the redesign.", focus: "Source", expectedKeywords: ["according to", "dashboard"], indonesianExplanation: "" },
    { coach: "So the redesign caused it?", hint: "Clarify correlation vs causation.", sampleAnswer: "To be precise, the data indicates correlation, not necessarily causation.", focus: "Precision", expectedKeywords: ["precise", "correlation", "causation"], indonesianExplanation: "" },
    { coach: "Close with a careful implication and another source.", hint: "This suggests... Another source shows...", sampleAnswer: "This suggests we should investigate the checkout experience. Session recordings also show confusion on the verification step.", focus: "Implication + triangulation", expectedKeywords: ["suggests", "recordings", "confusion"], indonesianExplanation: "" },
  ],
  "problem-solving-discussion-mission": [
    { coach: "Before we jump to solutions, how would you define the problem and scope?", hint: "Let's define... Can we agree on the scope?", sampleAnswer: "Let's define the problem statement first. Can we agree on the scope?", focus: "Framing", expectedKeywords: ["define", "scope"], indonesianExplanation: "" },
    { coach: "The data shows drop-off after the checkout changes. What could be causing it?", hint: "Based on the data... one possible cause is...", sampleAnswer: "Based on the data, one possible cause is confusion in checkout after the redesign.", focus: "Causes", expectedKeywords: ["based on", "data", "possible"], indonesianExplanation: "" },
    { coach: "Okay. What trade-off do you see, and what would you recommend next?", hint: "The trade-off is... Given these constraints... We can mitigate it by...", sampleAnswer: "The trade-off is speed versus reliability. Given these constraints, I'd recommend a two-week pilot. We can mitigate risk by setting clear metrics and a strict timeline.", focus: "Trade-offs + recommendation", expectedKeywords: ["trade-off", "recommend", "mitigate"], indonesianExplanation: "" },
  ],
  "problem-solving-mission": [
    { coach: "Quick check: what's the issue?", hint: "Jelaskan problem + impact singkat.", sampleAnswer: "There's a problem with the login page. Users can't sign in.", focus: "Describe problem and impact", expectedKeywords: ["problem", "can't"], indonesianExplanation: "" },
    { coach: "What should we do?", hint: "Kasih solusi dengan could/should + because.", sampleAnswer: "We could roll back now because it's quick.", focus: "Suggest solution with reason", expectedKeywords: ["could", "because"], indonesianExplanation: "" },
    { coach: "But will it affect other features?", hint: "Jawab dengan might + next steps (so let's...).", sampleAnswer: "It might, so let's roll back and then test the key flows.", focus: "Respond to concern and decide next steps", expectedKeywords: ["might", "so", "let's"], indonesianExplanation: "" },
  ],
  "qualifying-your-opinion": [
    { coach: "Should we adopt the new policy immediately?", hint: "Jawab dengan partial agreement + scope.", sampleAnswer: "To some extent, yes—especially for new projects.", focus: "Scope", expectedKeywords: ["to some extent", "especially"], indonesianExplanation: "" },
    { coach: "So you're fully in favor?", hint: "Broadly speaking... That said...", sampleAnswer: "Broadly speaking, I support it. That said, we need a clear exception for legacy systems.", focus: "Limitation", expectedKeywords: ["broadly", "that said", "exception"], indonesianExplanation: "" },
    { coach: "What would you suggest instead?", hint: "Propose a phased approach.", sampleAnswer: "I'd phase it in over two quarters and review adoption data along the way.", focus: "Suggestion", expectedKeywords: ["phase", "review"], indonesianExplanation: "" },
  ],
  "reaching-agreement": [
    { coach: "We need to decide. What do you suggest?", hint: "Usul dengan How about we...", sampleAnswer: "How about we go with the cheaper one tonight?", focus: "Make a suggestion", expectedKeywords: ["how about", "cheaper"], indonesianExplanation: "" },
    { coach: "I'm okay with that, but I'm worried it's crowded.", hint: "Tanggapi concern pakai might + so let's...", sampleAnswer: "It might be, so let's go early.", focus: "Respond to concern", expectedKeywords: ["might", "so", "let's"], indonesianExplanation: "" },
    { coach: "Great. Confirm the agreement.", hint: "Konfirmasi: So we agree on ...?", sampleAnswer: "Great. So we agree on Noodle House at 6:30?", focus: "Confirm agreement", expectedKeywords: ["agree", "at"], indonesianExplanation: "" },
  ],
  "reacting-politely": [
    { coach: "I'm a bit tired today.", hint: "Tunjukkan empati dan tanya balik dengan lembut.", sampleAnswer: "Oh no. Are you okay?", focus: "React to a problem", expectedKeywords: ["are you okay", "?"], indonesianExplanation: "" },
    { coach: "Yeah, I'm fine. I didn't sleep well.", hint: "Beri respons sopan, lalu tanya singkat tentang kondisi mereka.", sampleAnswer: "I'm sorry to hear that. Do you need a break?", focus: "Polite follow-up", expectedKeywords: ["i'm sorry to hear that", "?"], indonesianExplanation: "" },
    { coach: "Thanks. But I finished my project today.", hint: "Reaksi positif dan beri pujian singkat.", sampleAnswer: "That's great! Nice work.", focus: "React to good news", expectedKeywords: ["that's great", "nice work"], indonesianExplanation: "" },
  ],
  "reading-context": [
    { coach: "The client says the timeline is 'ambitious'. What does that mean?", hint: "Interpret cautiously: My sense is that...", sampleAnswer: "My sense is that they're signaling concern without saying no directly.", focus: "Interpretation", expectedKeywords: ["my sense", "signaling", "concern"], indonesianExplanation: "" },
    { coach: "What should we do before replying?", hint: "Ask to clarify priority.", sampleAnswer: "Before we decide, can we clarify what their priority is—speed or risk reduction?", focus: "Clarify", expectedKeywords: ["before we decide", "clarify", "priority"], indonesianExplanation: "" },
    { coach: "Offer a tactful option and set the right tone.", hint: "May be worth considering... stay respectful...", sampleAnswer: "It may be worth considering a phased plan to show flexibility. We should stay respectful and avoid sounding defensive.", focus: "Option + tone", expectedKeywords: ["worth considering", "phased", "respectful"], indonesianExplanation: "" },
  ],
  "recommending-a-solution": [
    { coach: "We need a recommendation. What should we do?", hint: "Given these constraints, I'd recommend...", sampleAnswer: "Given these constraints, I'd recommend starting with a two-week pilot.", focus: "Recommend", expectedKeywords: ["recommend", "pilot"], indonesianExplanation: "" },
    { coach: "What's the main risk?", hint: "The main risk is... if...", sampleAnswer: "The main risk is slower progress if we over-scope the pilot.", focus: "Risk", expectedKeywords: ["main risk", "if"], indonesianExplanation: "" },
    { coach: "How do we mitigate it?", hint: "We can mitigate it by...", sampleAnswer: "We can mitigate it by setting clear success metrics and a strict timeline.", focus: "Mitigation", expectedKeywords: ["mitigate", "metrics"], indonesianExplanation: "" },
  ],
  "repairing-misunderstanding": [
    { coach: "Acknowledge the misunderstanding and clarify intent.", hint: "I may have misunderstood... I didn't mean to...", sampleAnswer: "I may have misunderstood their tone. I didn't mean to come across as dismissive.", focus: "Acknowledge", expectedKeywords: ["misunderstood", "didn't mean", "dismissive"], indonesianExplanation: "" },
    { coach: "Clarify what you meant.", hint: "Just to clarify, my intent was ...", sampleAnswer: "Just to clarify, my intent was to confirm the constraints, not reject the request.", focus: "Clarify intent", expectedKeywords: ["just to clarify", "intent", "not reject"], indonesianExplanation: "" },
    { coach: "Propose a repair plan and timeline.", hint: "How about we... I'll draft it...", sampleAnswer: "How about we send a short note acknowledging the misunderstanding and offer a quick call? I'll draft it and share it in ten minutes.", focus: "Repair plan", expectedKeywords: ["how about", "acknowledging", "call", "draft"], indonesianExplanation: "" },
  ],
  "requesting-service-help": [
    { coach: "Sure. What do you need?", hint: "Tanyakan lokasi barang.", sampleAnswer: "Can you show me where the batteries are?", focus: "Ask for a location", expectedKeywords: ["where", "batteries", "?"], indonesianExplanation: "" },
    { coach: "They're over there, next to the cash register.", hint: "Konfirmasi dan ucapkan terima kasih.", sampleAnswer: "Great. Thank you for your help.", focus: "Thank politely", expectedKeywords: ["thank", "help"], indonesianExplanation: "" },
    { coach: "You're welcome.", hint: "Tutup dengan sopan.", sampleAnswer: "Have a good day.", focus: "Close politely", expectedKeywords: ["good day"], indonesianExplanation: "" },
  ],
  "rescheduling": [
    { coach: "Can we reschedule our coffee?", hint: "Setuju, lalu tanya sebabnya.", sampleAnswer: "Sure. What happened?", focus: "Ask for the reason", expectedKeywords: ["what happened", "?"], indonesianExplanation: "" },
    { coach: "Something came up at work.", hint: "Tawarkan waktu baru dengan how about.", sampleAnswer: "No problem. How about Friday evening?", focus: "Propose a new time", expectedKeywords: ["how about", "friday"], indonesianExplanation: "" },
    { coach: "Friday is good. Does 7 pm work for you?", hint: "Setuju dan konfirmasi tempat.", sampleAnswer: "Yes, 7 pm works. Same cafe?", focus: "Confirm time and place", expectedKeywords: ["works", "same cafe", "?"], indonesianExplanation: "" },
  ],
  "responding-to-advice": [
    { coach: "Maybe you should try a small daily goal.", hint: "Terima saran dengan sopan.", sampleAnswer: "That sounds good.", focus: "Accept advice", expectedKeywords: ["sounds"], indonesianExplanation: "" },
    { coach: "When will you start?", hint: "Jawab dengan rencana singkat.", sampleAnswer: "I'll try that starting tomorrow.", focus: "Commit to action", expectedKeywords: ["try", "tomorrow"], indonesianExplanation: "" },
    { coach: "How will you keep it consistent?", hint: "Sebutkan satu cara (checklist/alarm).", sampleAnswer: "I'll set a reminder and track it in a checklist.", focus: "Plan for consistency", expectedKeywords: ["reminder", "checklist"], indonesianExplanation: "" },
  ],
  "responding-to-counterpoints": [
    { coach: "I like your idea, but I'm worried it will increase costs.", hint: "Mulai dengan That's a fair point / I understand the concern.", sampleAnswer: "That's a fair point. However, the long-term savings could be significant.", focus: "Acknowledge + respond", expectedKeywords: ["fair point", "however"], indonesianExplanation: "" },
    { coach: "The upfront investment is still high.", hint: "Tawarkan mitigasi: phase it in / pilot.", sampleAnswer: "I understand the concern, but we can phase it in and measure results.", focus: "Mitigation plan", expectedKeywords: ["phase", "measure"], indonesianExplanation: "" },
    { coach: "Great. What's the next step?", hint: "Usul langkah berikutnya.", sampleAnswer: "Let's define success metrics first and run a small pilot.", focus: "Next steps", expectedKeywords: ["metrics", "pilot"], indonesianExplanation: "" },
  ],
  "responding-to-long-turns": [
    { coach: "We're dealing with several issues at once: dependencies across teams, time pressure from leadership, and visibility if anything slips.", hint: "Let me make sure I got this...", sampleAnswer: "Let me make sure I got this: we need to manage dependencies, time pressure, and stakeholder visibility.", focus: "Summary", expectedKeywords: ["make sure", "got this"], indonesianExplanation: "" },
    { coach: "Exactly. We need to keep changes small, communicate clearly, and monitor risk as we go.", hint: "The key points are...", sampleAnswer: "The key points are: keep changes small, communicate clearly, and monitor risk.", focus: "Key points", expectedKeywords: ["key points"], indonesianExplanation: "" },
    { coach: "Given all that, what would your response be?", hint: "Here's how I'd respond...", sampleAnswer: "Here's how I'd respond: propose phases, share metrics, and set weekly check-ins.", focus: "Response", expectedKeywords: ["here's how", "phases", "weekly"], indonesianExplanation: "" },
  ],
  "responding-to-new-information": [
    { coach: "I found a report that contradicts what we read.", hint: "I wasn't aware of that.", sampleAnswer: "Oh, I wasn't aware of that.", focus: "Acknowledge", expectedKeywords: ["aware"], indonesianExplanation: "" },
    { coach: "It says the sample size was very small.", hint: "That changes things + request understanding.", sampleAnswer: "That changes things. I'd like to understand the methodology.", focus: "Update view + ask", expectedKeywords: ["changes", "understand"], indonesianExplanation: "" },
    { coach: "That makes sense. What should we do next?", hint: "We should check... Can you share... Then we can revise...", sampleAnswer: "We should check the full report. Can you share the link? Then we can revise our conclusion.", focus: "Next steps", expectedKeywords: ["check", "share", "revise"], indonesianExplanation: "" },
  ],
  "responding-under-pressure": [
    { coach: "This is just speculation. Do you have anything solid?", hint: "Clarify calmly: indicators, not proof.", sampleAnswer: "Let me be clear: we have indicators, not proof yet.", focus: "Clarity", expectedKeywords: ["be clear", "indicators", "not proof"], indonesianExplanation: "" },
    { coach: "So why should we act now?", hint: "Acknowledge + key point.", sampleAnswer: "I understand the concern. However, the key point is that waiting increases risk.", focus: "Key point", expectedKeywords: ["understand", "however", "key point"], indonesianExplanation: "" },
    { coach: "Show me the numbers and propose next step.", hint: "If you look at... doubled... pilot...", sampleAnswer: "If you look at the last four weeks, incident volume has doubled. We run a pilot this week and review results before scaling.", focus: "Evidence + proposal", expectedKeywords: ["last four weeks", "doubled", "pilot"], indonesianExplanation: "" },
  ],
  "review-arguments-and-meetings": [
    { coach: "Can you summarize your position?", hint: "My position is that...", sampleAnswer: "My position is that we should prioritize fixing the billing flow.", focus: "Position", expectedKeywords: ["position", "prioritize"], indonesianExplanation: "" },
    { coach: "What's your main reason?", hint: "The main reason is...", sampleAnswer: "The main reason is it affects revenue and support workload.", focus: "Reason", expectedKeywords: ["main reason", "affects"], indonesianExplanation: "" },
    { coach: "Close with a summary and next steps.", hint: "To summarize... Next steps are...", sampleAnswer: "To summarize, we focus on billing first. Next steps are: I'll share a plan today, and you'll review it by Friday.", focus: "Close", expectedKeywords: ["to summarize", "next steps", "by"], indonesianExplanation: "" },
  ],
  "review-goals-and-preferences": [
    { coach: "What's your goal right now?", hint: "Goal + by ...", sampleAnswer: "My goal is to speak more confidently by the end of this month.", focus: "Goal with deadline", expectedKeywords: ["goal", "by"], indonesianExplanation: "" },
    { coach: "How's it going?", hint: "I've been practicing ...", sampleAnswer: "I'm making progress. I've been practicing every morning.", focus: "Progress update", expectedKeywords: ["progress", "been"], indonesianExplanation: "" },
    { coach: "Which practice method do you prefer, and why?", hint: "I prefer ... because ...", sampleAnswer: "I prefer Conversation Coach because it gives me feedback.", focus: "Preference with reason", expectedKeywords: ["prefer", "because"], indonesianExplanation: "" },
  ],
  "review-health-and-past": [
    { coach: "You don't look well. What's wrong?", hint: "Bilang kamu nggak enak badan + 1 gejala.", sampleAnswer: "I don't feel well. I have a headache.", focus: "Describe symptom", expectedKeywords: ["feel well", "headache"], indonesianExplanation: "" },
    { coach: "Did you sleep late last night?", hint: "Jawab yes/no, lalu tambah detail singkat.", sampleAnswer: "Yes. I went to bed late.", focus: "Answer past question", expectedKeywords: ["yes", "late"], indonesianExplanation: "" },
    { coach: "And what did you do yesterday?", hint: "Jawab dengan 1-2 aktivitas (past).", sampleAnswer: "I went to the clinic and stayed home.", focus: "Describe yesterday", expectedKeywords: ["went", "stayed"], indonesianExplanation: "" },
  ],
  "review-information-and-clients": [
    { coach: "Is this report reliable?", hint: "Based on the source... verify...", sampleAnswer: "Based on the source, it's a partial snapshot. We should verify it with our support data.", focus: "Reliability", expectedKeywords: ["source", "verify"], indonesianExplanation: "" },
    { coach: "Clients are worried about delays. What do you say?", hint: "I understand the concern... Just to clarify...", sampleAnswer: "I understand the concern. Just to clarify, what timeline did we promise?", focus: "Concern + clarify", expectedKeywords: ["understand", "clarify", "timeline"], indonesianExplanation: "" },
    { coach: "Close with next steps and a deadline.", hint: "Next steps are... today... by Friday.", sampleAnswer: "Next steps are: I'll share an update today, and we'll confirm a revised timeline by Friday.", focus: "Next steps", expectedKeywords: ["next steps", "today", "by"], indonesianExplanation: "" },
  ],
  "review-introductions": [
    { coach: "Hi, good morning. My name is Omar.", hint: "Sapa balik dan sebutkan namamu.", sampleAnswer: "Good morning. My name is Dimas.", focus: "Name review", expectedKeywords: ["morning", "name", "dimas"], indonesianExplanation: "" },
    { coach: "Nice to meet you. Where are you from?", hint: "Jawab asalmu dengan I'm from ...", sampleAnswer: "I'm from Indonesia.", focus: "Origin review", expectedKeywords: ["i'm", "from", "indonesia"], indonesianExplanation: "" },
    { coach: "I live in Jakarta now.", hint: "Tanyakan balik dengan How about you?", sampleAnswer: "How about you?", focus: "Question back", expectedKeywords: ["how", "about", "?"], indonesianExplanation: "" },
    { coach: "I'm from Malaysia.", hint: "Tutup percakapan dengan sopan.", sampleAnswer: "Oh, nice. See you in class.", focus: "Closing", expectedKeywords: ["nice", "see", "class"], indonesianExplanation: "" },
  ],
  "review-leadership-and-listening": [
    { coach: "Something feels off, but I can't tell what the real concern is.", hint: "What I'm hearing is...", sampleAnswer: "What I'm hearing is there's some concern under the surface.", focus: "Mirror", expectedKeywords: ["hearing", "concern"], indonesianExplanation: "" },
    { coach: "I think people are worried about blame, but I'm not sure what that means.", hint: "When you say X, do you mean Y or Z?", sampleAnswer: "When you say 'worried about blame', do you mean fear of mistakes or fear of visibility?", focus: "Clarify", expectedKeywords: ["do you mean", "fear"], indonesianExplanation: "" },
    { coach: "That makes sense. What would success look like in the next two weeks, and what should we do next?", hint: "What would success look like...? Next steps are...", sampleAnswer: "What would success look like in the next two weeks? Next steps are: you'll propose the pilot plan, and I'll help align stakeholders tomorrow.", focus: "Criteria + next steps", expectedKeywords: ["success", "next steps", "tomorrow"], indonesianExplanation: "" },
  ],
  "review-negotiation-and-presenting": [
    { coach: "We need this delivered next week.", hint: "Mulai dengan Here's my proposal...", sampleAnswer: "Here's my proposal: we deliver a smaller scope next week, then the full version two weeks later.", focus: "Proposal", expectedKeywords: ["proposal", "scope"], indonesianExplanation: "" },
    { coach: "What's the trade-off?", hint: "The trade-off is...", sampleAnswer: "The trade-off is speed versus completeness.", focus: "Trade-off", expectedKeywords: ["trade-off"], indonesianExplanation: "" },
    { coach: "Close with a recommendation and summary.", hint: "I'd recommend... To summarize...", sampleAnswer: "I'd recommend that compromise. To summarize: top two features next week, the rest in two weeks.", focus: "Close", expectedKeywords: ["recommend", "to summarize"], indonesianExplanation: "" },
  ],
  "review-nuance-and-strategy": [
    { coach: "Do you support the plan as it is?", hint: "On balance... but I'd...", sampleAnswer: "On balance, I support it, but I'd adjust the scope to reduce risk.", focus: "Nuance", expectedKeywords: ["on balance", "scope", "risk"], indonesianExplanation: "" },
    { coach: "Okay. To be precise, what would you change?", hint: "To be precise...", sampleAnswer: "To be precise, I'd keep the core workflow and postpone optional add-ons.", focus: "Precision", expectedKeywords: ["to be precise", "core", "postpone"], indonesianExplanation: "" },
    { coach: "That sounds reasonable. What can you commit to, and what's the next step?", hint: "What I can commit to is... Next steps are...", sampleAnswer: "What I can commit to is a pilot next week. Next steps are: I'll share a one-page summary today, and we'll align tomorrow.", focus: "Commitment + next steps", expectedKeywords: ["commit", "next steps", "today"], indonesianExplanation: "" },
  ],
  "review-places-and-shopping": [
    { coach: "Excuse me. Can I help you?", hint: "Tanyakan lokasi cafe.", sampleAnswer: "Where is the cafe?", focus: "Place question", expectedKeywords: ["where", "cafe", "?"], indonesianExplanation: "" },
    { coach: "Go straight and turn right.", hint: "Konfirmasi lokasinya dekat library.", sampleAnswer: "Is it next to the library?", focus: "Confirm place", expectedKeywords: ["next", "library", "?"], indonesianExplanation: "" },
    { coach: "Yes, it is. Great, you walk there. Now you're at the cafe. What would you like?", hint: "Pesan satu teh dengan sopan.", sampleAnswer: "I would like one tea, please.", focus: "Order", expectedKeywords: ["one", "tea"], indonesianExplanation: "" },
    { coach: "Sure. It is two dollars.", hint: "Bayar dan ucapkan terima kasih.", sampleAnswer: "Here you go. Thank you.", focus: "Payment", expectedKeywords: [], indonesianExplanation: "" },
  ],
  "review-presenting-and-debate": [
    { coach: "Give me the short version of your argument.", hint: "Let me frame this...", sampleAnswer: "Let me frame this: the goal is reliability, not just speed.", focus: "Frame", expectedKeywords: ["frame", "goal"], indonesianExplanation: "" },
    { coach: "What assumption is that based on?", hint: "The core assumption is that...", sampleAnswer: "The core assumption is that incidents cost more than delay.", focus: "Assumption", expectedKeywords: ["assumption", "incidents"], indonesianExplanation: "" },
    { coach: "If speed matters most, how would you defend that position in short?", hint: "If we accept..., then... In short...", sampleAnswer: "If we accept speed as the priority, then we should time-box a pilot and limit scope. In short: validate with metrics, then expand safely.", focus: "Pressure response", expectedKeywords: ["if", "then", "in short"], indonesianExplanation: "" },
  ],
  "review-problems-and-travel": [
    { coach: "What's the issue?", hint: "Mulai dengan There's a problem with...", sampleAnswer: "There's a problem with the meeting link.", focus: "State problem", expectedKeywords: ["problem", "with"], indonesianExplanation: "" },
    { coach: "What's the impact?", hint: "Gunakan so untuk dampak.", sampleAnswer: "People can't join, so we need a new link.", focus: "Explain impact", expectedKeywords: ["can't", "so"], indonesianExplanation: "" },
    { coach: "Now say you're late and give an estimate.", hint: "I'm running late... I'll be there in about...", sampleAnswer: "I'm running a bit late. I'll be there in about 15 minutes.", focus: "Delay + estimate", expectedKeywords: ["running", "in about"], indonesianExplanation: "" },
  ],
  "review-routines-and-time": [
    { coach: "What do you do in the morning?", hint: "Sebutkan satu rutinitas dan jam.", sampleAnswer: "I wake up at six.", focus: "Routine time", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "Nice. Do you study English after that?", hint: "Jawab dengan Yes, lalu sebutkan jam belajar.", sampleAnswer: "Yes, I study English at seven.", focus: "Study routine", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "Good. We have speaking class this week.", hint: "Tanyakan kapan kelas speaking.", sampleAnswer: "When is our speaking class?", focus: "Class schedule question", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "It is on Tuesday at eight.", hint: "Tutup dengan See you then.", sampleAnswer: "Great. See you then.", focus: "Closing", expectedKeywords: [], indonesianExplanation: "" },
  ],
  "review-social-and-plans": [
    { coach: "Hey! Long time no see. How have you been?", hint: "Jawab singkat, lalu balas tanya.", sampleAnswer: "Pretty good. How about you?", focus: "Small talk response", expectedKeywords: ["pretty", "how about"], indonesianExplanation: "" },
    { coach: "Busy with work. What have you been working on?", hint: "Jawab singkat dengan 1 topik.", sampleAnswer: "I've been working on a new project.", focus: "Answer follow-up", expectedKeywords: ["working on", "project"], indonesianExplanation: "" },
    { coach: "Do you want to grab coffee this weekend?", hint: "Terima, lalu usulkan waktu.", sampleAnswer: "Sure. Are you free on Saturday afternoon?", focus: "Accept and propose time", expectedKeywords: ["free", "saturday"], indonesianExplanation: "" },
  ],
  "review-stories-and-work": [
    { coach: "Tell me about your weekend.", hint: "Ceritain 2 kalimat (visited/went...).", sampleAnswer: "It was great. I visited my cousin and we went to a small concert.", focus: "Tell a short story", expectedKeywords: ["visited", "went"], indonesianExplanation: "" },
    { coach: "What happened after that?", hint: "Jawab pakai then.", sampleAnswer: "Then we grabbed street food and talked until late.", focus: "Continue the story", expectedKeywords: ["then"], indonesianExplanation: "" },
    { coach: "Now give a work update and next step.", hint: "I'm working on... Next, I'll...", sampleAnswer: "I'm working on the release checklist. Next, I'll review the risks.", focus: "Work update + next step", expectedKeywords: ["working on", "next"], indonesianExplanation: "" },
  ],
  "review-travel-and-shopping": [
    { coach: "Hi. Can I help you?", hint: "Tanya lokasi atau jadwal.", sampleAnswer: "Yes, please. What time is the next train?", focus: "Ask travel question", expectedKeywords: ["what time", "train"], indonesianExplanation: "" },
    { coach: "It's at 4:15. Anything else?", hint: "Tanya barang (availability).", sampleAnswer: "Yes. Do you have a phone charger?", focus: "Ask availability", expectedKeywords: ["do you have", "charger"], indonesianExplanation: "" },
    { coach: "Sure. What kind do you need?", hint: "Sebutkan jenisnya.", sampleAnswer: "A USB-C charger, please.", focus: "Specify type", expectedKeywords: ["usb", "please"], indonesianExplanation: "" },
  ],
  "routine-conversation-mission": [
    { coach: "What time do you wake up?", hint: "Sebutkan jam bangun.", sampleAnswer: "I wake up at six.", focus: "Wake-up time", expectedKeywords: ["wake", "six"], indonesianExplanation: "" },
    { coach: "When do you study English?", hint: "Sebutkan hari dan jam.", sampleAnswer: "I study on Monday and Wednesday at seven.", focus: "Study schedule", expectedKeywords: ["study", "monday", "wednesday", "seven"], indonesianExplanation: "" },
    { coach: "Is the class online?", hint: "Jawab dengan yes/no lengkap.", sampleAnswer: "Yes, it is online.", focus: "Class format", expectedKeywords: ["online"], indonesianExplanation: "" },
    { coach: "Great. See you on Monday.", hint: "Tutup percakapan.", sampleAnswer: "See you.", focus: "Closing", expectedKeywords: ["see"], indonesianExplanation: "" },
  ],
  "saying-hello-and-goodbye": [
    { coach: "Hi. Good morning. How are you today?", hint: "Jawab sapaan, lalu beri respons singkat.", sampleAnswer: "Good morning. I'm good, thank you. How are you?", focus: "Greeting response", expectedKeywords: ["good morning", "morning", "hi", "hello", "thank", "thanks"], indonesianExplanation: "Jawabanmu sudah masuk konteks. Akan lebih natural kalau menambahkan pertanyaan balik singkat." },
    { coach: "Nice. What is your name?", hint: "Sebutkan nama dengan pola: My name is ... atau I'm ...", sampleAnswer: "My name is Arif. Nice to meet you.", focus: "Self introduction", expectedKeywords: ["my name is", "i'm", "i am", "nice to meet"], indonesianExplanation: "Untuk perkenalan, pola 'My name is ...' atau 'I'm ...' sudah cukup. Tambahkan 'Nice to meet you' agar lebih ramah." },
    { coach: "Nice to meet you. Where are you from?", hint: "Jawab asalmu, lalu tambahkan pertanyaan balik sederhana.", sampleAnswer: "I'm from Indonesia. How about you?", focus: "Follow-up question", expectedKeywords: ["from", "indonesia", "jakarta", "how about you", "?"], indonesianExplanation: "Saat menjawab asal, tambahkan pertanyaan balik seperti 'How about you?' supaya percakapan terus berjalan." },
  ],
  "saying-how-you-feel": [
    { coach: "Hey, are you okay?", hint: "Jawab singkat, lalu bilang kamu nggak enak badan.", sampleAnswer: "Not really. I don't feel well.", focus: "Say you feel unwell", expectedKeywords: ["don't feel well", "not really"], indonesianExplanation: "" },
    { coach: "What's wrong?", hint: "Sebutkan satu gejala.", sampleAnswer: "I have a headache.", focus: "Name a symptom", expectedKeywords: ["have", "headache"], indonesianExplanation: "" },
    { coach: "Do you want to go home?", hint: "Jawab, lalu tambahkan satu gejala lagi.", sampleAnswer: "Yes. I think I have a fever.", focus: "Add another symptom", expectedKeywords: ["think", "fever"], indonesianExplanation: "" },
  ],
  "saying-what-you-can-do": [
    { coach: "Can you speak English?", hint: "Sebutkan kemampuanmu dengan I can.", sampleAnswer: "I can speak a little.", focus: "Speaking ability", expectedKeywords: ["speak", "little"], indonesianExplanation: "" },
    { coach: "Can you write simple emails?", hint: "Jawab dengan Yes, I can.", sampleAnswer: "Yes, I can.", focus: "Writing ability", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "Can you join a meeting in English?", hint: "Gunakan Not yet kalau belum bisa.", sampleAnswer: "Not yet, but I can try.", focus: "Honest ability", expectedKeywords: ["not", "yet", "but", "try"], indonesianExplanation: "" },
  ],
  "saying-what-you-do": [
    { coach: "What do you do?", hint: "Jawab dengan status sederhana.", sampleAnswer: "I'm a student.", focus: "Work or study status", expectedKeywords: ["i'm", "student"], indonesianExplanation: "" },
    { coach: "What do you study?", hint: "Sebutkan subjek yang kamu pelajari.", sampleAnswer: "I study design.", focus: "Study subject", expectedKeywords: ["study", "design"], indonesianExplanation: "" },
    { coach: "Do you study online?", hint: "Jawab dengan yes/no lengkap.", sampleAnswer: "Yes, I study online.", focus: "Study format", expectedKeywords: ["study", "online"], indonesianExplanation: "" },
  ],
  "saying-what-you-think": [
    { coach: "Oh yeah? What did you think?", hint: "Kasih opini singkat: I think it's + adjective.", sampleAnswer: "I think it's really good.", focus: "Give an opinion", expectedKeywords: ["i think", "it's"], indonesianExplanation: "" },
    { coach: "What did you like about it?", hint: "Sebutkan satu hal: story/actor/music.", sampleAnswer: "I liked the story. It was fun.", focus: "Add a comment", expectedKeywords: ["liked"], indonesianExplanation: "" },
    { coach: "Would you recommend it?", hint: "Jawab yes/no + alasan singkat.", sampleAnswer: "Yes, I would. It is simple, but fun.", focus: "Recommend with reason", expectedKeywords: ["yes", "but"], indonesianExplanation: "" },
  ],
  "saying-what-you-want": [
    { coach: "What do you want?", hint: "Sebutkan kamu mau sandwich.", sampleAnswer: "I want a sandwich.", focus: "Want statement", expectedKeywords: ["want", "sandwich"], indonesianExplanation: "" },
    { coach: "Do you want tea or coffee?", hint: "Pilih tea dengan sopan.", sampleAnswer: "Tea, please.", focus: "Choosing option", expectedKeywords: ["tea"], indonesianExplanation: "" },
    { coach: "Do you want sugar?", hint: "Katakan tanpa gula.", sampleAnswer: "No sugar, please.", focus: "No extra item", expectedKeywords: ["sugar"], indonesianExplanation: "" },
  ],
  "saying-where-you-are-from": [
    { coach: "Where are you from?", hint: "Jawab dengan pola: I'm from ...", sampleAnswer: "I'm from Indonesia.", focus: "Origin", expectedKeywords: ["from", "indonesia", "jakarta", "bandung", "surabaya"], indonesianExplanation: "Untuk asal negara atau kota, gunakan pola 'I'm from ...' dengan singkat dan jelas." },
    { coach: "Where do you live now?", hint: "Gunakan pola: I live in ...", sampleAnswer: "I live in Jakarta.", focus: "Current city", expectedKeywords: ["live in", "jakarta", "bandung", "surabaya"], indonesianExplanation: "Bedakan origin dan tempat tinggal sekarang: 'I'm from ...' dan 'I live in ...'." },
    { coach: "Nice. How about you?", hint: "Tanyakan balik dengan: How about you?", sampleAnswer: "How about you?", focus: "Question back", expectedKeywords: ["how about you", "where are you from", "?"], indonesianExplanation: "Pertanyaan balik seperti 'How about you?' menjaga percakapan tetap berjalan." },
  ],
  "saying-where-you-went": [
    { coach: "Hi! Did you go anywhere interesting yesterday?", hint: "Jawab, lalu bilang kamu pergi ke mana.", sampleAnswer: "Yes, I went to the museum.", focus: "Say where you went", expectedKeywords: ["went", "to"], indonesianExplanation: "" },
    { coach: "Oh nice. Where did you go after that?", hint: "Sebutkan tempat kedua.", sampleAnswer: "I went to a cafe near the river.", focus: "Add another place", expectedKeywords: ["went", "cafe"], indonesianExplanation: "" },
    { coach: "Sounds relaxing. Where did you go?", hint: "Balik tanya.", sampleAnswer: "Where did you go?", focus: "Ask back", expectedKeywords: ["where", "did"], indonesianExplanation: "" },
  ],
  "saying-you-do-not-understand": [
    { coach: "Please open your book.", hint: "Katakan kamu tidak mengerti.", sampleAnswer: "Sorry, I don't understand.", focus: "Saying confusion", expectedKeywords: ["sorry", "don't", "understand"], indonesianExplanation: "" },
    { coach: "That's okay. I can say it again.", hint: "Minta diulangi dengan sopan.", sampleAnswer: "Can you repeat that, please?", focus: "Asking repetition", expectedKeywords: ["repeat", "?"], indonesianExplanation: "" },
    { coach: "Yes. Open your book.", hint: "Konfirmasi instruksi.", sampleAnswer: "Open my book?", focus: "Confirmation", expectedKeywords: ["open", "book", "?"], indonesianExplanation: "" },
    { coach: "Yes, that's right.", hint: "Katakan sudah paham.", sampleAnswer: "Thank you. I understand now.", focus: "Closing", expectedKeywords: ["understand"], indonesianExplanation: "" },
  ],
  "saying-your-name": [
    { coach: "Hi, my name is Omar. What is your name?", hint: "Jawab dengan pola: My name is ... atau I'm ...", sampleAnswer: "My name is Arif. Nice to meet you.", focus: "Saying your name", expectedKeywords: ["my name is", "i'm", "i am", "nice to meet"], indonesianExplanation: "Sebutkan nama dengan satu kalimat jelas, lalu tambahkan respons ramah seperti 'Nice to meet you'." },
    { coach: "Nice to meet you. What should I call you?", hint: "Gunakan pola: Please call me ...", sampleAnswer: "Please call me Arif.", focus: "Nickname", expectedKeywords: ["please call me", "call me"], indonesianExplanation: "Kalau ingin menyebut nama panggilan, gunakan pola pendek 'Please call me ...'." },
    { coach: "Great. Nice to meet you, Arif.", hint: "Balas dengan sopan: Nice to meet you too.", sampleAnswer: "Nice to meet you too.", focus: "Polite response", expectedKeywords: ["nice to meet you too", "you too"], indonesianExplanation: "Untuk membalas sapaan perkenalan, 'Nice to meet you too' sudah natural dan sopan." },
  ],
  "setting-direction": [
    { coach: "What should the team focus on this sprint?", hint: "Set direction clearly.", sampleAnswer: "The direction I'd like to set is stabilizing the billing flow first.", focus: "Direction", expectedKeywords: ["direction", "first"], indonesianExplanation: "" },
    { coach: "How do we define success?", hint: "Success looks like...", sampleAnswer: "Success looks like fewer incidents and faster completion rates.", focus: "Success", expectedKeywords: ["success", "incidents"], indonesianExplanation: "" },
    { coach: "Assign ownership and boundaries.", hint: "I'd like you to own... Let's align on scope...", sampleAnswer: "I'd like you to own the rollout plan, and I'll own stakeholder updates. Let's align on scope and keep it time-boxed to two weeks.", focus: "Ownership + scope", expectedKeywords: ["own", "scope", "time-boxed"], indonesianExplanation: "" },
  ],
  "setting-the-scene": [
    { coach: "You look happy today. What happened?", hint: "Mulai dengan kapan + di mana.", sampleAnswer: "Last weekend, I was in Bandung.", focus: "Set time and place", expectedKeywords: ["last", "was", "in"], indonesianExplanation: "" },
    { coach: "Oh nice. Who were you with?", hint: "Jawab dengan with + person.", sampleAnswer: "I was there with my cousin.", focus: "Say who you were with", expectedKeywords: ["with", "cousin"], indonesianExplanation: "" },
    { coach: "What were you doing there?", hint: "Tambah 1 aktivitas background.", sampleAnswer: "We were visiting my aunt and exploring the city.", focus: "Add background activity", expectedKeywords: ["were", "visiting"], indonesianExplanation: "" },
  ],
  "sharing-email-addresses": [
    { coach: "What is your email address?", hint: "Sebutkan email dengan at dan dot.", sampleAnswer: "It's ben dot rama at example dot com.", focus: "Giving an email address", expectedKeywords: ["it's", "ben", "dot", "rama"], indonesianExplanation: "" },
    { coach: "Can you spell that, please?", hint: "Eja bagian nama email pelan-pelan.", sampleAnswer: "B-E-N dot R-A-M-A.", focus: "Spelling an email", expectedKeywords: ["dot"], indonesianExplanation: "" },
    { coach: "Is that correct?", hint: "Konfirmasi dengan: Yes, that's correct.", sampleAnswer: "Yes, that's correct.", focus: "Confirming an email", expectedKeywords: ["that's", "correct"], indonesianExplanation: "" },
  ],
  "shopping-service-mission": [
    { coach: "Hi. Can I help you?", hint: "Jelaskan barang yang kamu cari.", sampleAnswer: "Yes, please. I'm looking for a USB-C charger.", focus: "Ask for an item", expectedKeywords: ["i'm looking for", "charger"], indonesianExplanation: "" },
    { coach: "Sure. We have this one and that one.", hint: "Bandingkan dua opsi dengan pertanyaan.", sampleAnswer: "Which one is cheaper?", focus: "Compare options", expectedKeywords: ["cheaper", "?"], indonesianExplanation: "" },
    { coach: "This one is cheaper.", hint: "Pilih satu opsi dengan singkat.", sampleAnswer: "Okay. I'll take this one.", focus: "Choose an option", expectedKeywords: ["i'll take"], indonesianExplanation: "" },
    { coach: "Anything else?", hint: "Minta bantuan cari barang lain.", sampleAnswer: "Yes. Could you help me? Where are the batteries?", focus: "Request help", expectedKeywords: ["could you help me", "where", "?"], indonesianExplanation: "" },
  ],
  "signposting-clearly": [
    { coach: "Start with a signposting opener.", hint: "Let me walk you through...", sampleAnswer: "Let me quickly walk you through the plan.", focus: "Opener", expectedKeywords: ["walk you through"], indonesianExplanation: "" },
    { coach: "Use first, next, finally to outline your structure.", hint: "First... Next... Finally...", sampleAnswer: "First, I'll explain the problem. Next, I'll share the proposal. Finally, I'll outline next steps.", focus: "Structure", expectedKeywords: ["first", "next", "finally"], indonesianExplanation: "" },
    { coach: "Wrap up with a short summary phrase.", hint: "Let me summarize...", sampleAnswer: "Let me summarize the key points in one sentence.", focus: "Summary", expectedKeywords: ["summarize"], indonesianExplanation: "" },
  ],
  "simple-place-words": [
    { coach: "Where are you going?", hint: "Sebutkan kamu pergi ke cafe.", sampleAnswer: "I'm going to the cafe.", focus: "Destination", expectedKeywords: ["i'm", "going", "cafe"], indonesianExplanation: "" },
    { coach: "Is the cafe near here?", hint: "Jawab dan sebutkan dekat library.", sampleAnswer: "Yes. It is near the library.", focus: "Nearby place", expectedKeywords: ["near", "library"], indonesianExplanation: "" },
    { coach: "I am going to the library.", hint: "Ajak pergi bersama.", sampleAnswer: "Let's go together.", focus: "Friendly suggestion", expectedKeywords: ["let's", "together"], indonesianExplanation: "" },
  ],
  "small-talk-mission": [
    { coach: "Hi! How's it going?", hint: "Jawab singkat, lalu tanya balik.", sampleAnswer: "Hi! I'm good, thanks. How about you?", focus: "Start the chat", expectedKeywords: ["i'm good", "thanks", "how about you", "?"], indonesianExplanation: "" },
    { coach: "I'm a bit tired today.", hint: "Tunjukkan empati dan tanya sebabnya dengan simple past.", sampleAnswer: "I'm sorry to hear that. Did you sleep well?", focus: "Ask about the reason", expectedKeywords: ["i'm sorry to hear that", "did you", "?"], indonesianExplanation: "" },
    { coach: "Not really. I stayed up late.", hint: "Pindah topik dengan halus, lalu ajak buat rencana weekend.", sampleAnswer: "Oh okay. By the way, any plans for the weekend?", focus: "Change topic and plan", expectedKeywords: ["by the way", "any plans for the weekend", "?"], indonesianExplanation: "" },
    { coach: "I'm going to a new cafe on Saturday at 3 pm. Do you want to join?", hint: "Terima ajakan dan konfirmasi waktu dengan singkat.", sampleAnswer: "That sounds fun. Great, see you then!", focus: "Accept and close", expectedKeywords: ["that sounds fun", "see you"], indonesianExplanation: "" },
  ],
  "softening-disagreement": [
    { coach: "We should launch next week, no matter what.", hint: "Acknowledge + soften.", sampleAnswer: "I see your point, but I'm not sure I'd go that far.", focus: "Soften", expectedKeywords: ["see your point", "not sure"], indonesianExplanation: "" },
    { coach: "Explain your concern respectfully.", hint: "With respect... suggests...", sampleAnswer: "With respect, the current error rate suggests we're not ready.", focus: "Evidence", expectedKeywords: ["with respect", "suggests"], indonesianExplanation: "" },
    { coach: "Offer an alternative plan.", hint: "I might frame it differently...", sampleAnswer: "I might frame it differently: we launch a limited version next week and keep the rest behind a feature flag.", focus: "Alternative", expectedKeywords: ["frame", "limited", "feature flag"], indonesianExplanation: "" },
  ],
  "spelling-your-name": [
    { coach: "Hi. What is your name?", hint: "Sebutkan namamu dengan pola: My name is ... atau I'm ...", sampleAnswer: "My name is Dimas.", focus: "Saying your name clearly", expectedKeywords: ["my name is", "i'm", "i am", "dimas"], indonesianExplanation: "Sebutkan nama dengan satu kalimat pendek dan jelas. Pola 'My name is ...' sudah cukup untuk konteks registrasi." },
    { coach: "How do you spell it?", hint: "Eja nama huruf demi huruf, lalu boleh ulangi namanya.", sampleAnswer: "It's spelled D-I-M-A-S.", focus: "Spelling your name", expectedKeywords: ["spelled", "d-i-m-a-s", "dimas"], indonesianExplanation: "Saat diminta mengeja, sebutkan huruf satu per satu dengan jeda pendek. Kamu bisa memakai pola 'It's spelled ...'." },
    { coach: "Thank you. Let me read it back: D-I-M-A-S.", hint: "Konfirmasi bahwa ejaannya benar.", sampleAnswer: "That's right.", focus: "Confirming spelling", expectedKeywords: ["that's right", "right", "yes"], indonesianExplanation: "Untuk mengonfirmasi ejaan, 'That's right' terdengar natural dan sopan." },
  ],
  "starting-small-talk": [
    { coach: "Hi! How's your day?", hint: "Jawab singkat, lalu tanya balik dengan sopan.", sampleAnswer: "Hi! It's pretty good, thanks. How about you?", focus: "Start small talk", expectedKeywords: ["pretty good", "thanks", "how about you", "?"], indonesianExplanation: "" },
    { coach: "Pretty good. It's busy today. How about you?", hint: "Katakan kondisi harimu (mis. busy/okay) dengan satu kalimat pendek.", sampleAnswer: "I'm good. It's a bit busy too.", focus: "Describe your day", expectedKeywords: ["i'm good", "busy"], indonesianExplanation: "" },
    { coach: "Nice. By the way, how was your weekend?", hint: "Jawab tentang weekend dengan 1 kegiatan sederhana.", sampleAnswer: "It was nice. I went to the park.", focus: "Weekend follow-up", expectedKeywords: ["it was", "nice", "went to"], indonesianExplanation: "" },
  ],
  "stating-your-position": [
    { coach: "What's your position on switching to written updates?", hint: "Mulai dengan In my view / I believe.", sampleAnswer: "In my view, a written update would be better for routine topics.", focus: "State position", expectedKeywords: ["in my view", "better"], indonesianExplanation: "" },
    { coach: "Why?", hint: "Jawab dengan because + satu alasan.", sampleAnswer: "Because it saves time and helps people focus.", focus: "Give reason", expectedKeywords: ["because", "time"], indonesianExplanation: "" },
    { coach: "But some people want real-time discussion.", hint: "Acknowledge + but + solusi singkat.", sampleAnswer: "I see your point, but we can keep one live meeting per month.", focus: "Respond to counterpoint", expectedKeywords: ["see your point", "but"], indonesianExplanation: "" },
  ],
  "strategic-workplace-mission": [
    { coach: "We're under pressure to deliver soon, but we can't afford a messy rollout.", hint: "To make sure we're aligned... top priority... biggest constraint...", sampleAnswer: "To make sure we're aligned, what's your top priority and biggest constraint?", focus: "Align", expectedKeywords: ["aligned", "priority", "constraint"], indonesianExplanation: "" },
    { coach: "Top priority is reducing incidents, and the biggest constraint is time.", hint: "What we can commit to is... by... assuming...", sampleAnswer: "What we can commit to is a smaller release by next week, assuming no critical blockers appear.", focus: "Expectations", expectedKeywords: ["commit", "assuming"], indonesianExplanation: "" },
    { coach: "Okay, but what's the main risk if we do that, and how would you mitigate it?", hint: "The main risk is... We can mitigate it by...", sampleAnswer: "The main risk is incidents during rollout. We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan.", focus: "Risk", expectedKeywords: ["main risk", "mitigate", "rollback"], indonesianExplanation: "" },
  ],
  "structuring-a-short-presentation": [
    { coach: "Open your presentation.", hint: "Today I'd like to...", sampleAnswer: "Today I'd like to share an idea to improve our onboarding.", focus: "Opening", expectedKeywords: ["today", "idea"], indonesianExplanation: "" },
    { coach: "State the problem and proposal.", hint: "The problem is... My proposal is...", sampleAnswer: "The problem is new hires feel lost. My proposal is a simple checklist and a buddy system.", focus: "Problem + proposal", expectedKeywords: ["problem", "proposal"], indonesianExplanation: "" },
    { coach: "Close with next steps.", hint: "Next steps are...", sampleAnswer: "Next steps are: draft the checklist today, then pilot it with the next hire.", focus: "Next steps", expectedKeywords: ["next steps", "draft", "pilot"], indonesianExplanation: "" },
  ],
  "suggesting-a-solution": [
    { coach: "Any ideas to fix it?", hint: "Kasih saran dengan could.", sampleAnswer: "We could roll back the update.", focus: "Suggest a solution", expectedKeywords: ["could", "roll"], indonesianExplanation: "" },
    { coach: "Why?", hint: "Jawab dengan because + reason.", sampleAnswer: "Because rollback is quick and low risk.", focus: "Give a reason", expectedKeywords: ["because"], indonesianExplanation: "" },
    { coach: "How can we prevent it next time?", hint: "Gunakan should + so.", sampleAnswer: "We should add a quick test so it doesn't happen again.", focus: "Preventive step", expectedKeywords: ["should", "so"], indonesianExplanation: "" },
  ],
  "summarizing-an-article": [
    { coach: "What's the article about?", hint: "The article is about ...", sampleAnswer: "The article is about how remote work affects productivity.", focus: "Topic", expectedKeywords: ["article is about"], indonesianExplanation: "" },
    { coach: "What's the main point?", hint: "The main point is ...", sampleAnswer: "The main point is productivity improves with clear communication rules.", focus: "Main point", expectedKeywords: ["main point"], indonesianExplanation: "" },
    { coach: "How does it conclude?", hint: "It concludes that ...", sampleAnswer: "It concludes that hybrid setups work best for many teams.", focus: "Conclusion", expectedKeywords: ["concludes"], indonesianExplanation: "" },
  ],
  "summarizing-decisions": [
    { coach: "Before we finish, what did we decide?", hint: "Gunakan To summarize...", sampleAnswer: "To summarize, we agreed to keep scope limited to the core feature.", focus: "Summarize decision", expectedKeywords: ["to summarize", "agreed"], indonesianExplanation: "" },
    { coach: "Good. Who owns the action items?", hint: "Action items are: I'll..., you'll...", sampleAnswer: "Action items are: I'll update the tickets, and you'll confirm the design handoff.", focus: "Action items", expectedKeywords: ["action items", "I'll", "you'll"], indonesianExplanation: "" },
    { coach: "Great. When should we check progress again?", hint: "We'll check progress on ...", sampleAnswer: "We'll check progress on Thursday.", focus: "Next checkpoint", expectedKeywords: ["check progress"], indonesianExplanation: "" },
  ],
  "summarizing-what-you-heard": [
    { coach: "We've discussed the timeline, client concerns, and rollout risk. Can you summarize where we are?", hint: "So, to summarize...", sampleAnswer: "So, to summarize: the timeline is tight and clients are sensitive to change.", focus: "Summary", expectedKeywords: ["to summarize", "timeline"], indonesianExplanation: "" },
    { coach: "Good. Now what's the decision, and what are the open questions?", hint: "The decision is... The open questions are...", sampleAnswer: "The decision is to propose a phased rollout with clear metrics. The open questions are around resourcing and internal alignment.", focus: "Decision + open questions", expectedKeywords: ["decision", "open questions"], indonesianExplanation: "" },
    { coach: "That sounds close. Can you confirm it one more time before we close?", hint: "Just to confirm... Does that capture it...?", sampleAnswer: "Just to confirm, does that capture it accurately?", focus: "Confirm", expectedKeywords: ["confirm", "capture"], indonesianExplanation: "" },
  ],
  "supporting-with-reasons": [
    { coach: "Why should we invest in automated tests?", hint: "Mulai dengan One reason is...", sampleAnswer: "One reason is it reduces bugs in production.", focus: "Reason 1", expectedKeywords: ["one reason", "reduces"], indonesianExplanation: "" },
    { coach: "What's another reason?", hint: "Gunakan Another reason is...", sampleAnswer: "Another reason is it speeds up releases because we can deploy with more confidence.", focus: "Reason 2", expectedKeywords: ["another reason", "because"], indonesianExplanation: "" },
    { coach: "But writing tests takes time.", hint: "Acknowledge + but + solusi singkat.", sampleAnswer: "That's true, but we can start small and it saves time later.", focus: "Address concern", expectedKeywords: ["that's true", "but"], indonesianExplanation: "" },
  ],
  "talking-about-daily-routines": [
    { coach: "What do you do in the morning?", hint: "Sebutkan kegiatan dan waktunya.", sampleAnswer: "I wake up at six.", focus: "Morning routine", expectedKeywords: ["wake", "six"], indonesianExplanation: "" },
    { coach: "What do you do after that?", hint: "Gunakan after that untuk kegiatan berikutnya.", sampleAnswer: "I study English at seven.", focus: "Next routine step", expectedKeywords: ["study", "english", "seven"], indonesianExplanation: "" },
    { coach: "Do you work in the afternoon?", hint: "Jawab ya/tidak lalu beri waktu.", sampleAnswer: "Yes, I work at one.", focus: "Afternoon routine", expectedKeywords: ["work", "one"], indonesianExplanation: "" },
  ],
  "talking-about-goals": [
    { coach: "What's your goal this month?", hint: "Jawab dengan: My goal is to ...", sampleAnswer: "My goal is to speak more confidently.", focus: "State the goal", expectedKeywords: ["goal", "to"], indonesianExplanation: "" },
    { coach: "By when?", hint: "Gunakan by + waktu.", sampleAnswer: "By the end of this month.", focus: "State the deadline", expectedKeywords: ["by", "end"], indonesianExplanation: "" },
    { coach: "Why does it matter to you?", hint: "Jawab dengan because + reason.", sampleAnswer: "Because I want to join meetings without feeling nervous.", focus: "Give a reason", expectedKeywords: ["because", "meetings"], indonesianExplanation: "" },
  ],
  "talking-about-likes": [
    { coach: "Do you like English?", hint: "Jawab dengan: Yes, I like it.", sampleAnswer: "Yes, I like it.", focus: "Simple preference", expectedKeywords: [], indonesianExplanation: "" },
    { coach: "What do you like?", hint: "Sebutkan bagian belajar yang kamu suka.", sampleAnswer: "I like speaking practice.", focus: "Learning preference", expectedKeywords: ["speaking", "practice"], indonesianExplanation: "" },
    { coach: "Do you like grammar?", hint: "Jawab jujur dengan kalimat pendek.", sampleAnswer: "It's okay, but speaking is my favorite.", focus: "Favorite part", expectedKeywords: ["it's", "but", "speaking", "favorite"], indonesianExplanation: "" },
  ],
  "talking-about-local-habits": [
    { coach: "Tell me a local habit in your area.", hint: "Mulai dengan People usually...", sampleAnswer: "People usually eat outside in the evening.", focus: "Describe habit", expectedKeywords: ["usually"], indonesianExplanation: "" },
    { coach: "Can you give an example?", hint: "Gunakan In my area, people often...", sampleAnswer: "In my area, people often grab noodles or satay after work.", focus: "Give example", expectedKeywords: ["often", "in my area"], indonesianExplanation: "" },
    { coach: "How often does it happen?", hint: "Tambahkan detail: especially on weekends.", sampleAnswer: "Especially on weekends.", focus: "Add frequency detail", expectedKeywords: ["especially", "weekends"], indonesianExplanation: "" },
  ],
  "talking-about-weekends": [
    { coach: "Any plans for the weekend?", hint: "Jawab dengan going to + satu aktivitas.", sampleAnswer: "Yes. I'm going to visit my parents.", focus: "Share a plan", expectedKeywords: ["i'm going to", "visit"], indonesianExplanation: "" },
    { coach: "Nice. Where do they live?", hint: "Jawab tempatnya dengan singkat.", sampleAnswer: "They live in Bandung.", focus: "Give a detail", expectedKeywords: ["they live in", "bandung"], indonesianExplanation: "" },
    { coach: "Sounds good. How are you getting there?", hint: "Jawab transportnya, lalu tutup dengan sopan.", sampleAnswer: "I'm taking the train. Have a great weekend.", focus: "Transport and closing", expectedKeywords: ["i'm taking", "train", "have a great weekend"], indonesianExplanation: "" },
  ],
  "talking-about-yesterday": [
    { coach: "Hey, how was your day yesterday?", hint: "Jawab singkat (good/okay), lalu bilang kamu pergi ke mana.", sampleAnswer: "It was good. I went to the mall.", focus: "Answer and say where you went", expectedKeywords: ["was", "went"], indonesianExplanation: "" },
    { coach: "Nice. What did you do there?", hint: "Sebutkan 1-2 aktivitas (past verb).", sampleAnswer: "I bought a jacket and ate ramen.", focus: "Describe past activities", expectedKeywords: ["bought", "ate"], indonesianExplanation: "" },
    { coach: "Did you go alone?", hint: "Jawab dan sebutkan dengan siapa.", sampleAnswer: "No, I went with my brother.", focus: "Say who you went with", expectedKeywords: ["with", "brother"], indonesianExplanation: "" },
  ],
  "talking-to-a-driver": [
    { coach: "Hi. Where to?", hint: "Sebutkan tujuan dengan sopan.", sampleAnswer: "Can you take me to the station, please?", focus: "Say the destination", expectedKeywords: ["take me to", "station"], indonesianExplanation: "" },
    { coach: "Sure. To the station.", hint: "Tanya durasi perjalanannya.", sampleAnswer: "Thanks. How long will it take?", focus: "Ask travel time", expectedKeywords: ["how long", "?"], indonesianExplanation: "" },
    { coach: "About 20 minutes.", hint: "Buat satu request sopan.", sampleAnswer: "Okay. Please take the fastest route.", focus: "Make a request", expectedKeywords: ["please", "fastest"], indonesianExplanation: "" },
  ],
  "telling-events-in-order": [
    { coach: "So what did you do on your trip?", hint: "Mulai dengan first.", sampleAnswer: "First, we checked in at the hotel.", focus: "Start the sequence", expectedKeywords: ["first"], indonesianExplanation: "" },
    { coach: "Nice. What did you do next?", hint: "Gunakan then atau after that.", sampleAnswer: "Then we walked around and tried street food.", focus: "Continue the sequence", expectedKeywords: ["then"], indonesianExplanation: "" },
    { coach: "And finally?", hint: "Tutup dengan finally + reason singkat.", sampleAnswer: "Finally, we went back early because we were tired.", focus: "End the sequence", expectedKeywords: ["finally", "because"], indonesianExplanation: "" },
  ],
  "telling-the-time": [
    { coach: "What time is the class?", hint: "Jawab dengan pola: It's at ...", sampleAnswer: "It's at nine o'clock.", focus: "Class time", expectedKeywords: ["it's", "nine", "o'clock"], indonesianExplanation: "" },
    { coach: "In the morning?", hint: "Konfirmasi bagian hari.", sampleAnswer: "Yes, in the morning.", focus: "Time of day", expectedKeywords: ["morning"], indonesianExplanation: "" },
    { coach: "Thank you.", hint: "Balas dengan sopan.", sampleAnswer: "You're welcome.", focus: "Polite reply", expectedKeywords: ["you're", "welcome"], indonesianExplanation: "" },
  ],
  "transport-mission": [
    { coach: "Hi. Where are you going?", hint: "Minta tiket dan sebutkan tujuan.", sampleAnswer: "I'd like one ticket to Bandung, please.", focus: "Ticket request", expectedKeywords: ["i'd like", "ticket"], indonesianExplanation: "" },
    { coach: "One-way or round-trip?", hint: "Pilih satu-way.", sampleAnswer: "One-way, please.", focus: "Ticket type", expectedKeywords: ["one-way"], indonesianExplanation: "" },
    { coach: "Okay. It leaves at 6:30 pm from platform 2.", hint: "Tanya balik platform atau durasi dengan singkat.", sampleAnswer: "Great. Which platform again?", focus: "Confirm details", expectedKeywords: ["platform", "?"], indonesianExplanation: "" },
    { coach: "Hi. Where to?", hint: "Minta driver antar ke hotel.", sampleAnswer: "Can you take me to my hotel, please?", focus: "Driver request", expectedKeywords: ["take me to", "hotel"], indonesianExplanation: "" },
  ],
  "travel-situation-mission": [
    { coach: "Hi. Are you on your way to the hotel?", hint: "Jelaskan kamu telat + alasan + estimasi.", sampleAnswer: "Yes, but I'm running a bit late. My train is delayed. I'll be there in about 20 minutes.", focus: "Delay explanation with estimate", expectedKeywords: ["running", "delayed", "in about"], indonesianExplanation: "" },
    { coach: "Okay. Do you have a reservation?", hint: "Jawab dengan under + name.", sampleAnswer: "Yes. I have a reservation under Faris Kim.", focus: "Confirm reservation", expectedKeywords: ["reservation", "under"], indonesianExplanation: "" },
    { coach: "Great. Anything else you need?", hint: "Tanya rekomendasi + minta bantuan dengan could you.", sampleAnswer: "Do you have any recommendations for dinner? If there's a problem with my room, could you help me?", focus: "Ask recommendations and request help", expectedKeywords: ["recommendations", "could you", "problem"], indonesianExplanation: "" },
  ],
  "understanding-client-needs": [
    { coach: "We want to improve our product experience.", hint: "Mulai dengan pertanyaan klarifikasi (Just to clarify...).", sampleAnswer: "Got it. Just to clarify, who is the main user group?", focus: "Clarify user group", expectedKeywords: ["clarify", "user"], indonesianExplanation: "" },
    { coach: "The main users are new hires. What's next?", hint: "Minta detail pain point.", sampleAnswer: "Thanks. Could you share more about the biggest pain point today?", focus: "Ask for pain point", expectedKeywords: ["share more", "pain point"], indonesianExplanation: "" },
    { coach: "They can't find key docs. Summarize and confirm.", hint: "So what you need is ... right?", sampleAnswer: "Understood. So what you need is a clear starting point and a simple checklist, right?", focus: "Summarize need", expectedKeywords: ["need", "right"], indonesianExplanation: "" },
  ],
  "understanding-simple-directions": [
    { coach: "Where is the meeting room?", hint: "Tanyakan lokasi meeting room.", sampleAnswer: "Where is the meeting room?", focus: "Room question", expectedKeywords: ["where", "meeting", "room", "?"], indonesianExplanation: "" },
    { coach: "Go straight.", hint: "Ulangi arahan pertama.", sampleAnswer: "Okay. Go straight.", focus: "Repeating direction", expectedKeywords: ["straight"], indonesianExplanation: "" },
    { coach: "Then turn left.", hint: "Konfirmasi turn left.", sampleAnswer: "Turn left?", focus: "Direction confirmation", expectedKeywords: ["turn", "left", "?"], indonesianExplanation: "" },
    { coach: "Yes. The room is on the right.", hint: "Katakan kamu mengerti.", sampleAnswer: "Thank you. I understand.", focus: "Understanding", expectedKeywords: ["understand"], indonesianExplanation: "" },
  ],
  "using-examples": [
    { coach: "Why should onboarding be more structured?", hint: "Because... + For example...", sampleAnswer: "Because new hires need clarity. For example, last quarter three new joiners felt lost in week one.", focus: "Use an example", expectedKeywords: ["because", "for example"], indonesianExplanation: "" },
    { coach: "What's the impact?", hint: "Gunakan so untuk dampak.", sampleAnswer: "So they kept asking in multiple channels and it slowed the team down.", focus: "Explain impact", expectedKeywords: ["so", "kept"], indonesianExplanation: "" },
    { coach: "Give a specific suggestion.", hint: "Gunakan such as...", sampleAnswer: "Such as pairing each new hire with one mentor for two weeks.", focus: "Give specific suggestion", expectedKeywords: ["such as", "mentor"], indonesianExplanation: "" },
  ],
  "using-precise-transitions": [
    { coach: "Your explanation is clear so far. What's next?", hint: "Use That brings me to...", sampleAnswer: "That brings me to the key trade-off: speed versus reliability.", focus: "Transition", expectedKeywords: ["brings me to", "trade-off"], indonesianExplanation: "" },
    { coach: "Highlight the key point.", hint: "What's crucial here is...", sampleAnswer: "What's crucial here is that we set clear standards early.", focus: "Key point", expectedKeywords: ["crucial", "standards"], indonesianExplanation: "" },
    { coach: "Restate it and propose a next step.", hint: "To put it differently... With that in mind...", sampleAnswer: "To put it differently, standards let teams move fast without breaking consistency. With that in mind, I'd propose a pilot with strict guardrails.", focus: "Restate + propose", expectedKeywords: ["differently", "with that in mind", "pilot"], indonesianExplanation: "" },
  ],
  "work-study-conversation-mission": [
    { coach: "Do you work or study?", hint: "Sebutkan kerja atau studi.", sampleAnswer: "I study English online.", focus: "Work or study", expectedKeywords: ["study", "english", "online"], indonesianExplanation: "" },
    { coach: "What do you like about English?", hint: "Sebutkan bagian yang kamu suka.", sampleAnswer: "I like speaking practice.", focus: "Preference", expectedKeywords: ["speaking", "practice"], indonesianExplanation: "" },
    { coach: "What can you do in English?", hint: "Sebutkan satu kemampuan.", sampleAnswer: "I can introduce myself.", focus: "Ability", expectedKeywords: ["introduce", "myself"], indonesianExplanation: "" },
    { coach: "Great. Keep practicing.", hint: "Balas dengan singkat dan positif.", sampleAnswer: "Thank you. I will.", focus: "Closing", expectedKeywords: ["will"], indonesianExplanation: "" },
  ],
  "workplace-mission": [
    { coach: "Hi. Quick update on the report?", hint: "Mulai dengan progress singkat.", sampleAnswer: "I'm making good progress. I'm almost done with the summary.", focus: "Give update", expectedKeywords: ["progress", "almost"], indonesianExplanation: "" },
    { coach: "Great. Please update the risk section too.", hint: "Terima, lalu minta klarifikasi scope.", sampleAnswer: "Sure. Could you clarify which risks you want me to focus on?", focus: "Ask clarification", expectedKeywords: ["clarify", "focus"], indonesianExplanation: "" },
    { coach: "Focus on timeline and budget risks.", hint: "Konfirmasi deadline singkat.", sampleAnswer: "Got it. Just to confirm, you need it by Friday morning, right?", focus: "Confirm deadline", expectedKeywords: ["confirm", "by"], indonesianExplanation: "" },
  ],
  // </generated:coach_turns>
};

export const coachScenarios = [
  // <generated:coach_scenarios>
  { slug: "a1-final-conversation", label: "A1 Final Conversation", description: "A1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "completing_a_full_a1_final_conversation", mode: "lesson_practice_coach" },
  { slug: "a2-final-conversation", label: "A2 Final Conversation", description: "A2 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_final_conversation", mode: "lesson_practice_coach" },
  { slug: "a2-final-test-practice", label: "A2 Final Test Practice", description: "A2 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_final_test_practice", mode: "lesson_practice_coach" },
  { slug: "accepting-and-declining", label: "Accepting and Declining", description: "Plans & Invitations", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_accept_or_decline_invitation", mode: "lesson_practice_coach" },
  { slug: "advanced-listening-mission", label: "Advanced Listening Mission", description: "Advanced Listening & Response", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_advanced_listening_mission", mode: "lesson_practice_coach" },
  { slug: "advanced-presentation-mission", label: "Advanced Presentation Mission", description: "Advanced Presentations", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_advanced_presentation_mission", mode: "lesson_practice_coach" },
  { slug: "agreeing-and-disagreeing-politely", label: "Agreeing and Disagreeing Politely", description: "Opinions & Reasons", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_opinion_agree_disagree", mode: "lesson_practice_coach" },
  { slug: "aligning-stakeholders", label: "Aligning Stakeholders", description: "Strategic Workplace Communication", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_aligning_stakeholders", mode: "lesson_practice_coach" },
  { slug: "answering-questions", label: "Answering Questions", description: "Presenting Ideas", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_present_answer_questions", mode: "lesson_practice_coach" },
  { slug: "apologizing-and-thanking", label: "Apologizing and Thanking", description: "Help, Problems & Requests", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "apologizing_and_thanking_after_a_small_problem", mode: "lesson_practice_coach" },
  { slug: "arabic-a1-final-conversation", label: "A1 Final Conversation", description: "A1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_a1_final_conversation", mode: "lesson_practice_coach" },
  { slug: "arabic-a1-final-test-practice", label: "A1 Final Test Practice", description: "A1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_a1_final_test_practice", mode: "lesson_practice_coach" },
  { slug: "arabic-a2-final-conversation", label: "A2 Final Conversation", description: "A2 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_a2_final_conversation", mode: "lesson_practice_coach" },
  { slug: "arabic-a2-final-test-practice", label: "A2 Final Test Practice", description: "A2 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_a2_final_test_practice", mode: "lesson_practice_coach" },
  { slug: "arabic-accepting-and-declining", label: "Accepting and Declining", description: "Plans & Invitations", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_accepting_and_declining", mode: "lesson_practice_coach" },
  { slug: "arabic-agreeing-and-disagreeing-politely", label: "Agreeing and Disagreeing Politely", description: "Opinions & Reasons", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_agreeing_and_disagreeing_politely", mode: "lesson_practice_coach" },
  { slug: "arabic-apologizing-and-thanking", label: "Apologizing and Thanking", description: "Help, Problems & Requests", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_apologizing_and_thanking", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-about-departure-time", label: "Asking About Departure Time", description: "Transport & Travel", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_asking_about_departure_time", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-about-past-activities", label: "Asking About Past Activities", description: "Past Experiences", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_asking_about_past_activities", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-about-prices", label: "Asking About Prices", description: "Food, Shopping & Prices", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_asking_about_prices", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-about-size-and-color", label: "Asking About Size and Color", description: "Shopping & Services", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_asking_about_size_and_color", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-about-work-or-study", label: "Asking About Work or Study", description: "Family, Work & Study", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_asking_about_work_or_study", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-follow-up-questions", label: "Asking Follow-up Questions", description: "Social Follow-up", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_asking_follow_up_questions", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-for-an-item", label: "Asking for an Item", description: "Shopping & Services", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_asking_for_an_item", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-for-help", label: "Asking for Help", description: "Help, Problems & Requests", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_asking_for_help", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-for-opinions", label: "Asking for Opinions", description: "Opinions & Reasons", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_asking_for_opinions", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-how-to-get-there", label: "Asking How to Get There", description: "Places & Directions", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_asking_how_to_get_there", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-the-time", label: "Asking the Time", description: "Time & Daily Routine", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_asking_the_time", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-to-repeat-a-letter", label: "Asking to Repeat a Letter", description: "Letters, Numbers & Contact", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_asking_to_repeat_a_letter", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-when", label: "Asking When", description: "Time & Daily Routine", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_asking_when", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-when-you-do-not-understand", label: "Asking When You Do Not Understand", description: "Arabic Foundations", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_asking_when_you_do_not_understand", mode: "lesson_practice_coach" },
  { slug: "arabic-asking-where-a-place-is", label: "Asking Where a Place Is", description: "Places & Directions", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_asking_where_a_place_is", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-asking-about-culture", label: "Asking About Culture", description: "Community & Culture", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_asking_about_culture", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-asking-about-pros-and-cons", label: "Asking About Pros and Cons", description: "Explaining Preferences", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_asking_about_pros_and_cons", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-asking-about-someones-story", label: "Asking About Someone's Story", description: "Personal Stories", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_asking_about_someones_story", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-asking-for-clarification", label: "Asking for Clarification", description: "Workplace Conversations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_asking_for_clarification", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-asking-for-recommendations", label: "Asking for Recommendations", description: "Travel Situations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_asking_for_recommendations", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-b1-final-conversation", label: "B1 Final Conversation", description: "B1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_b1_final_conversation", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-b1-final-test-practice", label: "B1 Final Test Practice", description: "B1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_b1_final_test_practice", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-being-polite-with-differences", label: "Being Polite With Differences", description: "Community & Culture", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_being_polite_with_differences", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-checking-in", label: "Checking In", description: "Travel Situations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_checking_in", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-community-culture-mission", label: "Community Culture Mission", description: "Community & Culture", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_community_culture_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-comparing-two-options", label: "Comparing Two Options", description: "Explaining Preferences", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_comparing_two_options", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-describing-a-problem", label: "Describing a Problem", description: "Problems & Solutions", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_describing_a_problem", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-describing-feelings", label: "Describing Feelings", description: "Personal Stories", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_describing_feelings", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-describing-your-community", label: "Describing Your Community", description: "Community & Culture", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_describing_your_community", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-discussing-challenges", label: "Discussing Challenges", description: "Goals & Progress", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_discussing_challenges", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-explaining-a-delay", label: "Explaining a Delay", description: "Travel Situations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_explaining_a_delay", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-explaining-progress", label: "Explaining Progress", description: "Goals & Progress", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_explaining_progress", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-explaining-why-you-prefer-something", label: "Explaining Why You Prefer Something", description: "Explaining Preferences", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_explaining_why_you_prefer_something", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-explaining-your-task", label: "Explaining Your Task", description: "Workplace Conversations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_explaining_your_task", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-giving-a-short-update", label: "Giving a Short Update", description: "Workplace Conversations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_giving_a_short_update", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-goals-progress-mission", label: "Goals Progress Mission", description: "Goals & Progress", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_goals_progress_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-handling-a-simple-complaint", label: "Handling a Simple Complaint", description: "Travel Situations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_handling_a_simple_complaint", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-joining-a-simple-meeting", label: "Joining a Simple Meeting", description: "Workplace Conversations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_joining_a_simple_meeting", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-making-a-simple-decision", label: "Making a Simple Decision", description: "Problems & Solutions", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_making_a_simple_decision", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-making-next-step-plans", label: "Making Next-step Plans", description: "Goals & Progress", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_making_next_step_plans", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-personal-story-mission", label: "Personal Story Mission", description: "Personal Stories", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_personal_story_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-preference-discussion-mission", label: "Preference Discussion Mission", description: "Explaining Preferences", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_preference_discussion_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-problem-solving-mission", label: "Problem Solving Mission", description: "Problems & Solutions", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_problem_solving_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-reaching-agreement", label: "Reaching Agreement", description: "Explaining Preferences", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_reaching_agreement", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-responding-to-advice", label: "Responding to Advice", description: "Problems & Solutions", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_responding_to_advice", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-review-goals-and-preferences", label: "Review Goals and Preferences", description: "B1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_review_goals_and_preferences", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-review-problems-and-travel", label: "Review Problems and Travel", description: "B1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_review_problems_and_travel", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-review-stories-and-work", label: "Review Stories and Work", description: "B1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_review_stories_and_work", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-setting-the-scene", label: "Setting the Scene", description: "Personal Stories", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_setting_the_scene", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-suggesting-a-solution", label: "Suggesting a Solution", description: "Problems & Solutions", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_suggesting_a_solution", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-talking-about-goals", label: "Talking About Goals", description: "Goals & Progress", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_talking_about_goals", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-talking-about-local-habits", label: "Talking About Local Habits", description: "Community & Culture", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_talking_about_local_habits", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-telling-events-in-order", label: "Telling Events in Order", description: "Personal Stories", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_telling_events_in_order", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-travel-situation-mission", label: "Travel Situation Mission", description: "Travel Situations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_travel_situation_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b1-workplace-mission", label: "Workplace Mission", description: "Workplace Conversations", language: "arabic", languageLabel: "Arabic", levelCode: "B1", scenarioKey: "arabic_b1_workplace_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-answering-questions", label: "Answering Questions", description: "Presenting Ideas", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_answering_questions", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-b2-final-discussion", label: "B2 Final Discussion", description: "B2 Review & Final Discussion", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_b2_final_discussion", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-b2-final-test-practice", label: "B2 Final Test Practice", description: "B2 Review & Final Discussion", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_b2_final_test_practice", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-clarifying-scope", label: "Clarifying Scope", description: "Professional Meetings", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_clarifying_scope", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-clear-argument-mission", label: "Clear Argument Mission", description: "Clear Arguments", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_clear_argument_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-client-conversation-mission", label: "Client Conversation Mission", description: "Customer & Client Communication", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_client_conversation_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-confirming-next-steps", label: "Confirming Next Steps", description: "Customer & Client Communication", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_confirming_next_steps", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-discussing-reliable-sources", label: "Discussing Reliable Sources", description: "Media & Information", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_discussing_reliable_sources", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-discussing-tradeoffs", label: "Discussing Tradeoffs", description: "Complex Problem Solving", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_discussing_tradeoffs", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-explaining-a-viewpoint", label: "Explaining a Viewpoint", description: "Media & Information", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_explaining_a_viewpoint", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-explaining-benefits-and-risks", label: "Explaining Benefits and Risks", description: "Presenting Ideas", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_explaining_benefits_and_risks", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-explaining-causes", label: "Explaining Causes", description: "Complex Problem Solving", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_explaining_causes", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-explaining-options", label: "Explaining Options", description: "Customer & Client Communication", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_explaining_options", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-expressing-priorities", label: "Expressing Priorities", description: "Negotiation & Compromise", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_expressing_priorities", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-finding-middle-ground", label: "Finding Middle Ground", description: "Negotiation & Compromise", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_finding_middle_ground", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-framing-the-problem", label: "Framing the Problem", description: "Complex Problem Solving", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_framing_the_problem", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-giving-constructive-feedback", label: "Giving Constructive Feedback", description: "Professional Meetings", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_giving_constructive_feedback", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-handling-concerns", label: "Handling Concerns", description: "Customer & Client Communication", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_handling_concerns", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-handling-objections", label: "Handling Objections", description: "Negotiation & Compromise", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_handling_objections", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-idea-presentation-mission", label: "Idea Presentation Mission", description: "Presenting Ideas", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_idea_presentation_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-information-discussion-mission", label: "Information Discussion Mission", description: "Media & Information", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_information_discussion_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-making-a-proposal", label: "Making a Proposal", description: "Negotiation & Compromise", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_making_a_proposal", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-meeting-participation-mission", label: "Meeting Participation Mission", description: "Professional Meetings", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_meeting_participation_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-negotiation-mission", label: "Negotiation Mission", description: "Negotiation & Compromise", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_negotiation_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-opening-a-meeting-point", label: "Opening a Meeting Point", description: "Professional Meetings", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_opening_a_meeting_point", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-problem-solving-discussion-mission", label: "Problem Solving Discussion Mission", description: "Complex Problem Solving", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_problem_solving_discussion_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-recommending-a-solution", label: "Recommending a Solution", description: "Complex Problem Solving", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_recommending_a_solution", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-responding-to-counterpoints", label: "Responding to Counterpoints", description: "Clear Arguments", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_responding_to_counterpoints", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-responding-to-new-information", label: "Responding to New Information", description: "Media & Information", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_responding_to_new_information", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-review-arguments-and-meetings", label: "Review Arguments and Meetings", description: "B2 Review & Final Discussion", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_review_arguments_and_meetings", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-review-information-and-clients", label: "Review Information and Clients", description: "B2 Review & Final Discussion", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_review_information_and_clients", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-review-negotiation-and-presenting", label: "Review Negotiation and Presenting", description: "B2 Review & Final Discussion", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_review_negotiation_and_presenting", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-signposting-clearly", label: "Signposting Clearly", description: "Presenting Ideas", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_signposting_clearly", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-stating-your-position", label: "Stating Your Position", description: "Clear Arguments", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_stating_your_position", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-structuring-a-short-presentation", label: "Structuring a Short Presentation", description: "Presenting Ideas", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_structuring_a_short_presentation", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-summarizing-an-article", label: "Summarizing an Article", description: "Media & Information", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_summarizing_an_article", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-summarizing-decisions", label: "Summarizing Decisions", description: "Professional Meetings", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_summarizing_decisions", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-supporting-with-reasons", label: "Supporting With Reasons", description: "Clear Arguments", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_supporting_with_reasons", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-understanding-client-needs", label: "Understanding Client Needs", description: "Customer & Client Communication", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_understanding_client_needs", mode: "lesson_practice_coach" },
  { slug: "arabic-b2-using-examples", label: "Using Examples", description: "Clear Arguments", language: "arabic", languageLabel: "Arabic", levelCode: "B2", scenarioKey: "arabic_b2_using_examples", mode: "lesson_practice_coach" },
  { slug: "arabic-buying-a-simple-item", label: "Buying a Simple Item", description: "Food, Shopping & Prices", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_buying_a_simple_item", mode: "lesson_practice_coach" },
  { slug: "arabic-buying-a-ticket", label: "Buying a Ticket", description: "Transport & Travel", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_buying_a_ticket", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-advanced-listening-mission", label: "Advanced Listening Mission", description: "Advanced Listening & Response", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_advanced_listening_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-advanced-presentation-mission", label: "Advanced Presentation Mission", description: "Advanced Presentations", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_advanced_presentation_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-aligning-stakeholders", label: "Aligning Stakeholders", description: "Strategic Workplace Communication", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_aligning_stakeholders", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-asking-high-quality-follow-ups", label: "Asking High-quality Follow-ups", description: "Advanced Listening & Response", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_asking_high_quality_follow_ups", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-asking-tactful-questions", label: "Asking Tactful Questions", description: "Cross-cultural Professionalism", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_asking_tactful_questions", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-balancing-two-viewpoints", label: "Balancing Two Viewpoints", description: "Nuanced Opinions", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_balancing_two_viewpoints", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-building-a-persuasive-flow", label: "Building a Persuasive Flow", description: "Advanced Presentations", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_building_a_persuasive_flow", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-c1-final-conversation", label: "C1 Final Conversation", description: "C1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_c1_final_conversation", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-c1-final-test-practice", label: "C1 Final Test Practice", description: "C1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_c1_final_test_practice", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-catching-implied-meaning", label: "Catching Implied Meaning", description: "Advanced Listening & Response", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_catching_implied_meaning", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-challenging-an-argument", label: "Challenging an Argument", description: "Debate & Analysis", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_challenging_an_argument", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-coaching-with-questions", label: "Coaching With Questions", description: "Leadership & Coaching", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_coaching_with_questions", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-communicating-risk", label: "Communicating Risk", description: "Strategic Workplace Communication", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_communicating_risk", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-cross-cultural-mission", label: "Cross-cultural Mission", description: "Cross-cultural Professionalism", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_cross_cultural_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-debate-analysis-mission", label: "Debate Analysis Mission", description: "Debate & Analysis", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_debate_analysis_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-explaining-local-norms", label: "Explaining Local Norms", description: "Cross-cultural Professionalism", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_explaining_local_norms", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-expressing-certainty-and-doubt", label: "Expressing Certainty and Doubt", description: "Nuanced Opinions", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_expressing_certainty_and_doubt", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-framing-a-complex-topic", label: "Framing a Complex Topic", description: "Advanced Presentations", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_framing_a_complex_topic", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-giving-actionable-feedback", label: "Giving Actionable Feedback", description: "Leadership & Coaching", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_giving_actionable_feedback", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-guiding-a-decision", label: "Guiding a Decision", description: "Leadership & Coaching", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_guiding_a_decision", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-handling-challenging-questions", label: "Handling Challenging Questions", description: "Advanced Presentations", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_handling_challenging_questions", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-handling-sensitive-feedback", label: "Handling Sensitive Feedback", description: "Strategic Workplace Communication", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_handling_sensitive_feedback", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-identifying-assumptions", label: "Identifying Assumptions", description: "Debate & Analysis", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_identifying_assumptions", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-leadership-coaching-mission", label: "Leadership Coaching Mission", description: "Leadership & Coaching", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_leadership_coaching_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-managing-expectations", label: "Managing Expectations", description: "Strategic Workplace Communication", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_managing_expectations", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-nuanced-opinion-mission", label: "Nuanced Opinion Mission", description: "Nuanced Opinions", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_nuanced_opinion_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-presenting-evidence", label: "Presenting Evidence", description: "Debate & Analysis", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_presenting_evidence", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-qualifying-your-opinion", label: "Qualifying Your Opinion", description: "Nuanced Opinions", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_qualifying_your_opinion", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-reading-context", label: "Reading Context", description: "Cross-cultural Professionalism", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_reading_context", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-repairing-misunderstanding", label: "Repairing Misunderstanding", description: "Cross-cultural Professionalism", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_repairing_misunderstanding", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-responding-to-long-turns", label: "Responding to Long Turns", description: "Advanced Listening & Response", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_responding_to_long_turns", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-responding-under-pressure", label: "Responding Under Pressure", description: "Debate & Analysis", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_responding_under_pressure", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-review-leadership-and-listening", label: "Review Leadership and Listening", description: "C1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_review_leadership_and_listening", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-review-nuance-and-strategy", label: "Review Nuance and Strategy", description: "C1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_review_nuance_and_strategy", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-review-presenting-and-debate", label: "Review Presenting and Debate", description: "C1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_review_presenting_and_debate", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-setting-direction", label: "Setting Direction", description: "Leadership & Coaching", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_setting_direction", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-softening-disagreement", label: "Softening Disagreement", description: "Nuanced Opinions", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_softening_disagreement", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-strategic-workplace-mission", label: "Strategic Workplace Mission", description: "Strategic Workplace Communication", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_strategic_workplace_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-summarizing-what-you-heard", label: "Summarizing What You Heard", description: "Advanced Listening & Response", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_summarizing_what_you_heard", mode: "lesson_practice_coach" },
  { slug: "arabic-c1-using-precise-transitions", label: "Using Precise Transitions", description: "Advanced Presentations", language: "arabic", languageLabel: "Arabic", levelCode: "C1", scenarioKey: "arabic_c1_using_precise_transitions", mode: "lesson_practice_coach" },
  { slug: "arabic-cafe-and-shop-mission", label: "Cafe and Shop Mission", description: "Food, Shopping & Prices", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_cafe_and_shop_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-checking-directions", label: "Checking Directions", description: "Transport & Travel", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_checking_directions", mode: "lesson_practice_coach" },
  { slug: "arabic-class-and-study-instructions", label: "Class and Study Instructions", description: "Arabic Foundations", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_class_and_study_instructions", mode: "lesson_practice_coach" },
  { slug: "arabic-comparing-simple-options", label: "Comparing Simple Options", description: "Shopping & Services", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_comparing_simple_options", mode: "lesson_practice_coach" },
  { slug: "arabic-confirming-appointment-details", label: "Confirming Appointment Details", description: "Health & Appointments", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_confirming_appointment_details", mode: "lesson_practice_coach" },
  { slug: "arabic-contact-details-mission", label: "Contact Details Mission", description: "Letters, Numbers & Contact", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_contact_details_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-days-of-the-week", label: "Days of the Week", description: "Time & Daily Routine", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_days_of_the_week", mode: "lesson_practice_coach" },
  { slug: "arabic-describing-a-simple-experience", label: "Describing a Simple Experience", description: "Past Experiences", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_describing_a_simple_experience", mode: "lesson_practice_coach" },
  { slug: "arabic-describing-simple-symptoms", label: "Describing Simple Symptoms", description: "Health & Appointments", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_describing_simple_symptoms", mode: "lesson_practice_coach" },
  { slug: "arabic-family-members", label: "Family Members", description: "Family, Work & Study", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_family_members", mode: "lesson_practice_coach" },
  { slug: "arabic-family-work-study-mission", label: "Family, Work, and Study Mission", description: "Family, Work & Study", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_family_work_study_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-finding-a-place-mission", label: "Finding a Place Mission", description: "Places & Directions", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_finding_a_place_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-formal-greetings", label: "Formal Greetings", description: "Arabic Foundations", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_greetings_and_salam", mode: "lesson_practice_coach" },
  { slug: "arabic-fusha-introduction-mission", label: "Arabic Introduction Mission", description: "Arabic Foundations", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_fusha_introduction_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-giving-simple-reasons", label: "Giving Simple Reasons", description: "Opinions & Reasons", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_giving_simple_reasons", mode: "lesson_practice_coach" },
  { slug: "arabic-health-appointment-mission", label: "Health Appointment Mission", description: "Health & Appointments", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_health_appointment_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-help-and-problem-mission", label: "Help and Problem Mission", description: "Help, Problems & Requests", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_help_and_problem_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-invitation-mission", label: "Invitation Mission", description: "Plans & Invitations", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_invitation_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-inviting-someone", label: "Inviting Someone", description: "Plans & Invitations", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_inviting_someone", mode: "lesson_practice_coach" },
  { slug: "arabic-likes-and-ability", label: "Likes and Ability", description: "Family, Work & Study", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_likes_and_ability", mode: "lesson_practice_coach" },
  { slug: "arabic-making-a-simple-plan", label: "Making a Simple Plan", description: "Plans & Invitations", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_making_a_simple_plan", mode: "lesson_practice_coach" },
  { slug: "arabic-making-an-appointment", label: "Making an Appointment", description: "Health & Appointments", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_making_an_appointment", mode: "lesson_practice_coach" },
  { slug: "arabic-making-simple-requests", label: "Making Simple Requests", description: "Help, Problems & Requests", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_making_simple_requests", mode: "lesson_practice_coach" },
  { slug: "arabic-name-and-origin", label: "Name and Origin", description: "Arabic Foundations", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_name_and_origin", mode: "lesson_practice_coach" },
  { slug: "arabic-numbers-and-phone", label: "Arabic Numbers and Phone", description: "Letters, Numbers & Contact", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_numbers_and_phone", mode: "lesson_practice_coach" },
  { slug: "arabic-opinion-conversation-mission", label: "Opinion Conversation Mission", description: "Opinions & Reasons", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_opinion_conversation_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-ordering-a-drink", label: "Ordering a Drink", description: "Food, Shopping & Prices", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_ordering_a_drink", mode: "lesson_practice_coach" },
  { slug: "arabic-past-experience-mission", label: "Past Experience Mission", description: "Past Experiences", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_past_experience_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-reacting-with-interest", label: "Reacting With Interest", description: "Social Follow-up", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_reacting_with_interest", mode: "lesson_practice_coach" },
  { slug: "arabic-reconnecting-after-class", label: "Reconnecting After Class", description: "Social Follow-up", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_reconnecting_after_class", mode: "lesson_practice_coach" },
  { slug: "arabic-requesting-service-help", label: "Requesting Service Help", description: "Shopping & Services", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_requesting_service_help", mode: "lesson_practice_coach" },
  { slug: "arabic-rescheduling-politely", label: "Rescheduling Politely", description: "Plans & Invitations", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_rescheduling_politely", mode: "lesson_practice_coach" },
  { slug: "arabic-review-health-and-past", label: "Review Health and Past", description: "A2 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_review_health_and_past", mode: "lesson_practice_coach" },
  { slug: "arabic-review-introductions-and-contact", label: "Review Introductions and Contact", description: "A1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_review_introductions_and_contact", mode: "lesson_practice_coach" },
  { slug: "arabic-review-places-and-shopping", label: "Review Places and Shopping", description: "A1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_review_places_and_shopping", mode: "lesson_practice_coach" },
  { slug: "arabic-review-routine-and-study", label: "Review Routine and Study", description: "A1 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_review_routine_and_study", mode: "lesson_practice_coach" },
  { slug: "arabic-review-social-and-plans", label: "Review Social and Plans", description: "A2 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_review_social_and_plans", mode: "lesson_practice_coach" },
  { slug: "arabic-review-travel-and-services", label: "Review Travel and Services", description: "A2 Review & Final Conversation", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_review_travel_and_services", mode: "lesson_practice_coach" },
  { slug: "arabic-routine-and-time-mission", label: "Routine and Time Mission", description: "Time & Daily Routine", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_routine_and_time_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-saying-how-you-feel", label: "Saying How You Feel", description: "Health & Appointments", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_saying_how_you_feel", mode: "lesson_practice_coach" },
  { slug: "arabic-saying-what-you-do", label: "Saying What You Do", description: "Family, Work & Study", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_saying_what_you_do", mode: "lesson_practice_coach" },
  { slug: "arabic-saying-what-you-think", label: "Saying What You Think", description: "Opinions & Reasons", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_saying_what_you_think", mode: "lesson_practice_coach" },
  { slug: "arabic-saying-what-you-want", label: "Saying What You Want", description: "Food, Shopping & Prices", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_saying_what_you_want", mode: "lesson_practice_coach" },
  { slug: "arabic-saying-where-you-went", label: "Saying Where You Went", description: "Past Experiences", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_saying_where_you_went", mode: "lesson_practice_coach" },
  { slug: "arabic-saying-you-do-not-understand", label: "Saying You Do Not Understand", description: "Help, Problems & Requests", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_saying_you_do_not_understand", mode: "lesson_practice_coach" },
  { slug: "arabic-sharing-email-addresses", label: "Sharing Email Addresses", description: "Letters, Numbers & Contact", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_sharing_email_addresses", mode: "lesson_practice_coach" },
  { slug: "arabic-shopping-service-mission", label: "Shopping Service Mission", description: "Shopping & Services", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_shopping_service_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-simple-place-words", label: "Simple Place Words", description: "Places & Directions", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_simple_place_words", mode: "lesson_practice_coach" },
  { slug: "arabic-social-follow-up-mission", label: "Social Follow-up Mission", description: "Social Follow-up", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_social_follow_up_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-spelling-your-name", label: "Spelling Your Name", description: "Letters, Numbers & Contact", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_spelling_your_name", mode: "lesson_practice_coach" },
  { slug: "arabic-talking-about-daily-routines", label: "Talking About Daily Routines", description: "Time & Daily Routine", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_talking_about_daily_routines", mode: "lesson_practice_coach" },
  { slug: "arabic-talking-about-the-weekend", label: "Talking About the Weekend", description: "Social Follow-up", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_talking_about_the_weekend", mode: "lesson_practice_coach" },
  { slug: "arabic-talking-about-yesterday", label: "Talking About Yesterday", description: "Past Experiences", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_talking_about_yesterday", mode: "lesson_practice_coach" },
  { slug: "arabic-talking-to-a-driver", label: "Talking to a Driver", description: "Transport & Travel", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_talking_to_a_driver", mode: "lesson_practice_coach" },
  { slug: "arabic-transport-travel-mission", label: "Transport and Travel Mission", description: "Transport & Travel", language: "arabic", languageLabel: "Arabic", levelCode: "A2", scenarioKey: "arabic_transport_travel_mission", mode: "lesson_practice_coach" },
  { slug: "arabic-understanding-simple-directions", label: "Understanding Simple Directions", description: "Places & Directions", language: "arabic", languageLabel: "Arabic", levelCode: "A1", scenarioKey: "arabic_understanding_simple_directions", mode: "lesson_practice_coach" },
  { slug: "asking-about-culture", label: "Asking About Culture", description: "Community & Culture", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_culture_asking_about_culture", mode: "lesson_practice_coach" },
  { slug: "asking-about-departure-time", label: "Asking About Departure Time", description: "Travel & Transport", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_ask_departure_time_station", mode: "lesson_practice_coach" },
  { slug: "asking-about-past-activities", label: "Asking About Past Activities", description: "Past Experiences", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_past_ask_activities", mode: "lesson_practice_coach" },
  { slug: "asking-about-prices", label: "Asking About Prices", description: "Food, Shopping & Prices", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "asking_for_a_simple_price", mode: "lesson_practice_coach" },
  { slug: "asking-about-pros-and-cons", label: "Asking About Pros and Cons", description: "Explaining Preferences", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_preference_pros_cons", mode: "lesson_practice_coach" },
  { slug: "asking-about-size-and-color", label: "Asking About Size and Color", description: "Shopping & Services", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_shop_size_and_color", mode: "lesson_practice_coach" },
  { slug: "asking-about-someones-story", label: "Asking About Someone's Story", description: "Personal Stories", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_story_ask_followups", mode: "lesson_practice_coach" },
  { slug: "asking-about-work-or-study", label: "Asking About Work or Study", description: "Work, Study & Preferences", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "asking_about_work_or_study", mode: "lesson_practice_coach" },
  { slug: "asking-follow-up-questions", label: "Asking Follow-up Questions", description: "Social Small Talk", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_follow_up_questions_cafe", mode: "lesson_practice_coach" },
  { slug: "asking-for-an-item", label: "Asking for an Item", description: "Shopping & Services", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_shop_ask_for_item", mode: "lesson_practice_coach" },
  { slug: "asking-for-clarification", label: "Asking for Clarification", description: "Workplace Conversations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_work_clarification", mode: "lesson_practice_coach" },
  { slug: "asking-for-help", label: "Asking for Help", description: "Help, Problems & Requests", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "asking_for_help_with_a_simple_task", mode: "lesson_practice_coach" },
  { slug: "asking-for-opinions", label: "Asking for Opinions", description: "Opinions & Reasons", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_opinion_ask_for_opinion", mode: "lesson_practice_coach" },
  { slug: "asking-for-recommendations", label: "Asking for Recommendations", description: "Travel Situations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_travel_recommendations", mode: "lesson_practice_coach" },
  { slug: "asking-for-repetition", label: "Asking for Repetition", description: "Spelling, Numbers & Contact Details", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "asking_for_repetition_contact_info", mode: "lesson_practice_coach" },
  { slug: "asking-high-quality-follow-ups", label: "Asking High-quality Follow-ups", description: "Advanced Listening & Response", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_followups", mode: "lesson_practice_coach" },
  { slug: "asking-how-to-get-there", label: "Asking How to Get There", description: "Places & Directions", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "asking_for_steps_to_reach_a_place", mode: "lesson_practice_coach" },
  { slug: "asking-someones-name", label: "Asking Someone's Name", description: "Greeting & Introducing Yourself", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "asking_someones_name_class", mode: "lesson_practice_coach" },
  { slug: "asking-tactful-questions", label: "Asking Tactful Questions", description: "Cross-cultural Professionalism", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_tactful_questions", mode: "lesson_practice_coach" },
  { slug: "asking-when-something-happens", label: "Asking When Something Happens", description: "Daily Routine & Time", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "asking_about_meeting_time", mode: "lesson_practice_coach" },
  { slug: "asking-where-a-place-is", label: "Asking Where a Place Is", description: "Places & Directions", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "asking_for_a_place_location", mode: "lesson_practice_coach" },
  { slug: "b1-final-conversation", label: "B1 Final Conversation", description: "B1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_final_conversation", mode: "lesson_practice_coach" },
  { slug: "b1-final-test-practice", label: "B1 Final Test Practice", description: "B1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_final_test_practice", mode: "lesson_practice_coach" },
  { slug: "b2-final-discussion", label: "B2 Final Discussion", description: "B2 Review & Final Discussion", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_final_discussion", mode: "lesson_practice_coach" },
  { slug: "b2-final-test-practice", label: "B2 Final Test Practice", description: "B2 Review & Final Discussion", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_final_practice", mode: "lesson_practice_coach" },
  { slug: "balancing-two-viewpoints", label: "Balancing Two Viewpoints", description: "Nuanced Opinions", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_balancing_viewpoints", mode: "lesson_practice_coach" },
  { slug: "being-polite-with-differences", label: "Being Polite With Differences", description: "Community & Culture", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_culture_polite_differences", mode: "lesson_practice_coach" },
  { slug: "building-a-persuasive-flow", label: "Building a Persuasive Flow", description: "Advanced Presentations", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_persuasive_flow", mode: "lesson_practice_coach" },
  { slug: "buying-a-simple-item", label: "Buying a Simple Item", description: "Food, Shopping & Prices", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "buying_one_basic_item_in_a_shop", mode: "lesson_practice_coach" },
  { slug: "buying-a-ticket", label: "Buying a Ticket", description: "Travel & Transport", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_buy_ticket_at_station", mode: "lesson_practice_coach" },
  { slug: "c1-final-conversation", label: "C1 Final Conversation", description: "C1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_final_conversation", mode: "lesson_practice_coach" },
  { slug: "c1-final-test-practice", label: "C1 Final Test Practice", description: "C1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_final_test_practice", mode: "lesson_practice_coach" },
  { slug: "cafe-and-shop-mission", label: "Cafe and Shop Mission", description: "Food, Shopping & Prices", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "completing_a_simple_cafe_or_shop_purchase", mode: "lesson_practice_coach" },
  { slug: "catching-implied-meaning", label: "Catching Implied Meaning", description: "Advanced Listening & Response", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_implied_meaning", mode: "lesson_practice_coach" },
  { slug: "challenging-an-argument", label: "Challenging an Argument", description: "Debate & Analysis", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_challenging_argument", mode: "lesson_practice_coach" },
  { slug: "checking-directions", label: "Checking Directions", description: "Travel & Transport", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_check_directions_station", mode: "lesson_practice_coach" },
  { slug: "checking-in", label: "Checking In", description: "Travel Situations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_travel_check_in", mode: "lesson_practice_coach" },
  { slug: "clarifying-scope", label: "Clarifying Scope", description: "Professional Meetings", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_meeting_clarify_scope", mode: "lesson_practice_coach" },
  { slug: "clear-argument-mission", label: "Clear Argument Mission", description: "Clear Arguments", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_argument_mission", mode: "lesson_practice_coach" },
  { slug: "client-conversation-mission", label: "Client Conversation Mission", description: "Customer & Client Communication", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_client_mission", mode: "lesson_practice_coach" },
  { slug: "coaching-with-questions", label: "Coaching with Questions", description: "Leadership & Coaching", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_coaching_questions", mode: "lesson_practice_coach" },
  { slug: "communicating-risk", label: "Communicating Risk", description: "Strategic Workplace Communication", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_communicating_risk", mode: "lesson_practice_coach" },
  { slug: "community-culture-mission", label: "Community Culture Mission", description: "Community & Culture", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_culture_mission", mode: "lesson_practice_coach" },
  { slug: "comparing-simple-options", label: "Comparing Simple Options", description: "Shopping & Services", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_shop_compare_options", mode: "lesson_practice_coach" },
  { slug: "comparing-two-options", label: "Comparing Two Options", description: "Explaining Preferences", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_preference_compare_options", mode: "lesson_practice_coach" },
  { slug: "confirming-details", label: "Confirming Details", description: "Health & Appointments", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_health_confirm_details", mode: "lesson_practice_coach" },
  { slug: "confirming-next-steps", label: "Confirming Next Steps", description: "Customer & Client Communication", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_client_next_steps", mode: "lesson_practice_coach" },
  { slug: "contact-details-mission", label: "Contact Details Mission", description: "Spelling, Numbers & Contact Details", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "contact_details_unit_mission", mode: "lesson_practice_coach" },
  { slug: "cross-cultural-mission", label: "Cross-cultural Mission", description: "Cross-cultural Professionalism", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_cross_cultural_mission", mode: "lesson_practice_coach" },
  { slug: "days-and-simple-schedules", label: "Days and Simple Schedules", description: "Daily Routine & Time", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "checking_class_days", mode: "lesson_practice_coach" },
  { slug: "debate-analysis-mission", label: "Debate Analysis Mission", description: "Debate & Analysis", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_debate_mission", mode: "lesson_practice_coach" },
  { slug: "describing-a-problem", label: "Describing a Problem", description: "Problems & Solutions", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_problem_describe", mode: "lesson_practice_coach" },
  { slug: "describing-a-simple-experience", label: "Describing a Simple Experience", description: "Past Experiences", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_past_simple_experience", mode: "lesson_practice_coach" },
  { slug: "describing-feelings", label: "Describing Feelings", description: "Personal Stories", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_story_feelings", mode: "lesson_practice_coach" },
  { slug: "describing-simple-symptoms", label: "Describing Simple Symptoms", description: "Health & Appointments", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_health_describing_symptoms", mode: "lesson_practice_coach" },
  { slug: "describing-your-community", label: "Describing Your Community", description: "Community & Culture", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_culture_describe_community", mode: "lesson_practice_coach" },
  { slug: "discussing-challenges", label: "Discussing Challenges", description: "Goals & Progress", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_goals_discuss_challenges", mode: "lesson_practice_coach" },
  { slug: "discussing-reliable-sources", label: "Discussing Reliable Sources", description: "Media & Information", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_info_reliable_sources", mode: "lesson_practice_coach" },
  { slug: "discussing-tradeoffs", label: "Discussing Tradeoffs", description: "Complex Problem Solving", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_tradeoffs", mode: "lesson_practice_coach" },
  { slug: "explaining-a-delay", label: "Explaining a Delay", description: "Travel Situations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_travel_delay", mode: "lesson_practice_coach" },
  { slug: "explaining-a-viewpoint", label: "Explaining a Viewpoint", description: "Media & Information", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_info_viewpoint", mode: "lesson_practice_coach" },
  { slug: "explaining-benefits-and-risks", label: "Explaining Benefits and Risks", description: "Presenting Ideas", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_present_benefits_risks", mode: "lesson_practice_coach" },
  { slug: "explaining-causes", label: "Explaining Causes", description: "Complex Problem Solving", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_root_causes", mode: "lesson_practice_coach" },
  { slug: "explaining-local-norms", label: "Explaining Local Norms", description: "Cross-cultural Professionalism", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_explaining_norms", mode: "lesson_practice_coach" },
  { slug: "explaining-options", label: "Explaining Options", description: "Customer & Client Communication", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_client_options", mode: "lesson_practice_coach" },
  { slug: "explaining-progress", label: "Explaining Progress", description: "Goals & Progress", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_goals_explain_progress", mode: "lesson_practice_coach" },
  { slug: "explaining-why-you-prefer-something", label: "Explaining Why You Prefer Something", description: "Explaining Preferences", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_preference_explain_reason", mode: "lesson_practice_coach" },
  { slug: "explaining-your-task", label: "Explaining Your Task", description: "Workplace Conversations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_work_explain_task", mode: "lesson_practice_coach" },
  { slug: "expressing-certainty-and-doubt", label: "Expressing Certainty and Doubt", description: "Nuanced Opinions", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_certainty_doubt", mode: "lesson_practice_coach" },
  { slug: "expressing-priorities", label: "Expressing Priorities", description: "Negotiation & Compromise", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_negotiation_priorities", mode: "lesson_practice_coach" },
  { slug: "final-test-practice", label: "Final Test Practice", description: "A1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "practicing_the_a1_final_conversation_test", mode: "lesson_practice_coach" },
  { slug: "finding-a-place-mission", label: "Finding a Place Mission", description: "Places & Directions", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "finding_a_place_with_simple_directions", mode: "lesson_practice_coach" },
  { slug: "finding-middle-ground", label: "Finding Middle Ground", description: "Negotiation & Compromise", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_negotiation_middle_ground", mode: "lesson_practice_coach" },
  { slug: "first-conversation-mission", label: "First Conversation Mission", description: "Greeting & Introducing Yourself", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "first_conversation_mission_class", mode: "lesson_practice_coach" },
  { slug: "framing-a-complex-topic", label: "Framing a Complex Topic", description: "Advanced Presentations", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_presentation_framing", mode: "lesson_practice_coach" },
  { slug: "framing-the-problem", label: "Framing the Problem", description: "Complex Problem Solving", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_problem_framing", mode: "lesson_practice_coach" },
  { slug: "giving-a-short-update", label: "Giving a Short Update", description: "Workplace Conversations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_work_short_update", mode: "lesson_practice_coach" },
  { slug: "giving-actionable-feedback", label: "Giving Actionable Feedback", description: "Leadership & Coaching", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_actionable_feedback", mode: "lesson_practice_coach" },
  { slug: "giving-constructive-feedback", label: "Giving Constructive Feedback", description: "Professional Meetings", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_meeting_feedback", mode: "lesson_practice_coach" },
  { slug: "giving-phone-numbers", label: "Giving Phone Numbers", description: "Spelling, Numbers & Contact Details", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "giving_phone_number_for_registration", mode: "lesson_practice_coach" },
  { slug: "giving-simple-reasons", label: "Giving Simple Reasons", description: "Opinions & Reasons", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_opinion_because_reasons", mode: "lesson_practice_coach" },
  { slug: "goals-progress-mission", label: "Goals Progress Mission", description: "Goals & Progress", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_goals_mission", mode: "lesson_practice_coach" },
  { slug: "guiding-a-decision", label: "Guiding a Decision", description: "Leadership & Coaching", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_guiding_decision", mode: "lesson_practice_coach" },
  { slug: "handling-a-simple-complaint", label: "Handling a Simple Complaint", description: "Travel Situations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_travel_complaint", mode: "lesson_practice_coach" },
  { slug: "handling-challenging-questions", label: "Handling Challenging Questions", description: "Advanced Presentations", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_challenging_questions", mode: "lesson_practice_coach" },
  { slug: "handling-concerns", label: "Handling Concerns", description: "Customer & Client Communication", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_client_concerns", mode: "lesson_practice_coach" },
  { slug: "handling-objections", label: "Handling Objections", description: "Negotiation & Compromise", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_negotiation_objections", mode: "lesson_practice_coach" },
  { slug: "handling-sensitive-feedback", label: "Handling Sensitive Feedback", description: "Strategic Workplace Communication", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_sensitive_feedback", mode: "lesson_practice_coach" },
  { slug: "health-appointment-mission", label: "Health Appointment Mission", description: "Health & Appointments", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_health_appointment_mission", mode: "lesson_practice_coach" },
  { slug: "help-and-problem-mission", label: "Help and Problem Mission", description: "Help, Problems & Requests", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "handling_a_small_problem_and_requesting_help", mode: "lesson_practice_coach" },
  { slug: "idea-presentation-mission", label: "Idea Presentation Mission", description: "Presenting Ideas", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_present_mission", mode: "lesson_practice_coach" },
  { slug: "identifying-assumptions", label: "Identifying Assumptions", description: "Debate & Analysis", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_identifying_assumptions", mode: "lesson_practice_coach" },
  { slug: "information-discussion-mission", label: "Information Discussion Mission", description: "Media & Information", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_info_mission", mode: "lesson_practice_coach" },
  { slug: "invitation-mission", label: "Invitation Mission", description: "Plans & Invitations", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_invitation_mission_reschedule", mode: "lesson_practice_coach" },
  { slug: "inviting-someone", label: "Inviting Someone", description: "Plans & Invitations", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_invite_to_movie", mode: "lesson_practice_coach" },
  { slug: "joining-a-simple-meeting", label: "Joining a Simple Meeting", description: "Workplace Conversations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_work_meeting", mode: "lesson_practice_coach" },
  { slug: "leadership-coaching-mission", label: "Leadership Coaching Mission", description: "Leadership & Coaching", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_leadership_coaching_mission", mode: "lesson_practice_coach" },
  { slug: "making-a-proposal", label: "Making a Proposal", description: "Negotiation & Compromise", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_negotiation_proposal", mode: "lesson_practice_coach" },
  { slug: "making-a-simple-decision", label: "Making a Simple Decision", description: "Problems & Solutions", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_problem_make_decision", mode: "lesson_practice_coach" },
  { slug: "making-an-appointment", label: "Making an Appointment", description: "Health & Appointments", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_health_make_appointment", mode: "lesson_practice_coach" },
  { slug: "making-next-step-plans", label: "Making Next-step Plans", description: "Goals & Progress", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_goals_next_step_plan", mode: "lesson_practice_coach" },
  { slug: "making-plans", label: "Making Plans", description: "Plans & Invitations", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_make_plans_after_class", mode: "lesson_practice_coach" },
  { slug: "making-simple-requests", label: "Making Simple Requests", description: "Help, Problems & Requests", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "making_a_simple_polite_request", mode: "lesson_practice_coach" },
  { slug: "managing-expectations", label: "Managing Expectations", description: "Strategic Workplace Communication", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_managing_expectations", mode: "lesson_practice_coach" },
  { slug: "meeting-participation-mission", label: "Meeting Participation Mission", description: "Professional Meetings", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_meeting_mission", mode: "lesson_practice_coach" },
  { slug: "negotiation-mission", label: "Negotiation Mission", description: "Negotiation & Compromise", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_negotiation_mission", mode: "lesson_practice_coach" },
  { slug: "nuanced-opinion-mission", label: "Nuanced Opinion Mission", description: "Nuanced Opinions", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_nuance_mission", mode: "lesson_practice_coach" },
  { slug: "opening-a-meeting-point", label: "Opening a Meeting Point", description: "Professional Meetings", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_meeting_open_topic", mode: "lesson_practice_coach" },
  { slug: "opinion-conversation-mission", label: "Opinion Conversation Mission", description: "Opinions & Reasons", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_opinion_mission_restaurant", mode: "lesson_practice_coach" },
  { slug: "ordering-a-drink", label: "Ordering a Drink", description: "Food, Shopping & Prices", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "ordering_a_simple_drink_at_a_cafe", mode: "lesson_practice_coach" },
  { slug: "past-experience-mission", label: "Past Experience Mission", description: "Past Experiences", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_past_mission_yesterday", mode: "lesson_practice_coach" },
  { slug: "personal-story-mission", label: "Personal Story Mission", description: "Personal Stories", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_story_mission", mode: "lesson_practice_coach" },
  { slug: "preference-discussion-mission", label: "Preference Discussion Mission", description: "Explaining Preferences", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_preference_mission", mode: "lesson_practice_coach" },
  { slug: "presenting-evidence", label: "Presenting Evidence", description: "Debate & Analysis", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_presenting_evidence", mode: "lesson_practice_coach" },
  { slug: "problem-solving-discussion-mission", label: "Problem Solving Discussion Mission", description: "Complex Problem Solving", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_problem_mission", mode: "lesson_practice_coach" },
  { slug: "problem-solving-mission", label: "Problem Solving Mission", description: "Problems & Solutions", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_problem_mission", mode: "lesson_practice_coach" },
  { slug: "qualifying-your-opinion", label: "Qualifying Your Opinion", description: "Nuanced Opinions", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_qualifying_opinion", mode: "lesson_practice_coach" },
  { slug: "reaching-agreement", label: "Reaching Agreement", description: "Explaining Preferences", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_preference_reach_agreement", mode: "lesson_practice_coach" },
  { slug: "reacting-politely", label: "Reacting Politely", description: "Social Small Talk", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_polite_reactions_chat", mode: "lesson_practice_coach" },
  { slug: "reading-context", label: "Reading Context", description: "Cross-cultural Professionalism", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_reading_context", mode: "lesson_practice_coach" },
  { slug: "recommending-a-solution", label: "Recommending a Solution", description: "Complex Problem Solving", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_solution_recommendation", mode: "lesson_practice_coach" },
  { slug: "repairing-misunderstanding", label: "Repairing Misunderstanding", description: "Cross-cultural Professionalism", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_repairing_misunderstanding", mode: "lesson_practice_coach" },
  { slug: "requesting-service-help", label: "Requesting Service Help", description: "Shopping & Services", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_shop_request_help", mode: "lesson_practice_coach" },
  { slug: "rescheduling", label: "Rescheduling", description: "Plans & Invitations", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_reschedule_coffee_plan", mode: "lesson_practice_coach" },
  { slug: "responding-to-advice", label: "Responding to Advice", description: "Problems & Solutions", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_problem_respond_advice", mode: "lesson_practice_coach" },
  { slug: "responding-to-counterpoints", label: "Responding to Counterpoints", description: "Clear Arguments", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_argument_counterpoints", mode: "lesson_practice_coach" },
  { slug: "responding-to-long-turns", label: "Responding to Long Turns", description: "Advanced Listening & Response", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_long_turns", mode: "lesson_practice_coach" },
  { slug: "responding-to-new-information", label: "Responding to New Information", description: "Media & Information", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_info_new_information", mode: "lesson_practice_coach" },
  { slug: "responding-under-pressure", label: "Responding Under Pressure", description: "Debate & Analysis", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_under_pressure", mode: "lesson_practice_coach" },
  { slug: "review-arguments-and-meetings", label: "Review Arguments and Meetings", description: "B2 Review & Final Discussion", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_review_meeting", mode: "lesson_practice_coach" },
  { slug: "review-goals-and-preferences", label: "Review Goals and Preferences", description: "B1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_review_goals_preferences", mode: "lesson_practice_coach" },
  { slug: "review-health-and-past", label: "Review Health and Past", description: "A2 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_review_health_past", mode: "lesson_practice_coach" },
  { slug: "review-information-and-clients", label: "Review Information and Clients", description: "B2 Review & Final Discussion", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_review_clients", mode: "lesson_practice_coach" },
  { slug: "review-introductions", label: "Review Introductions", description: "A1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "reviewing_introductions_before_class", mode: "lesson_practice_coach" },
  { slug: "review-leadership-and-listening", label: "Review Leadership and Listening", description: "C1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_review_leadership_listening", mode: "lesson_practice_coach" },
  { slug: "review-negotiation-and-presenting", label: "Review Negotiation and Presenting", description: "B2 Review & Final Discussion", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_review_negotiation", mode: "lesson_practice_coach" },
  { slug: "review-nuance-and-strategy", label: "Review Nuance and Strategy", description: "C1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_review_nuance_strategy", mode: "lesson_practice_coach" },
  { slug: "review-places-and-shopping", label: "Review Places and Shopping", description: "A1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "reviewing_places_directions_and_a_simple_order", mode: "lesson_practice_coach" },
  { slug: "review-presenting-and-debate", label: "Review Presenting and Debate", description: "C1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_review_presenting_debate", mode: "lesson_practice_coach" },
  { slug: "review-problems-and-travel", label: "Review Problems and Travel", description: "B1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_review_problem_travel", mode: "lesson_practice_coach" },
  { slug: "review-routines-and-time", label: "Review Routines and Time", description: "A1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "reviewing_routine_and_class_time", mode: "lesson_practice_coach" },
  { slug: "review-social-and-plans", label: "Review Social and Plans", description: "A2 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_review_social_plans", mode: "lesson_practice_coach" },
  { slug: "review-stories-and-work", label: "Review Stories and Work", description: "B1 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_review_stories_work", mode: "lesson_practice_coach" },
  { slug: "review-travel-and-shopping", label: "Review Travel and Shopping", description: "A2 Review & Final Conversation", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_review_travel_shopping", mode: "lesson_practice_coach" },
  { slug: "routine-conversation-mission", label: "Routine Conversation Mission", description: "Daily Routine & Time", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "routine_and_schedule_unit_mission", mode: "lesson_practice_coach" },
  { slug: "saying-hello-and-goodbye", label: "Saying Hello and Goodbye", description: "Greeting & Introducing Yourself", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "greeting_intro_class", mode: "lesson_practice_coach" },
  { slug: "saying-how-you-feel", label: "Saying How You Feel", description: "Health & Appointments", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_health_saying_how_you_feel", mode: "lesson_practice_coach" },
  { slug: "saying-what-you-can-do", label: "Saying What You Can Do", description: "Work, Study & Preferences", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "saying_simple_english_abilities", mode: "lesson_practice_coach" },
  { slug: "saying-what-you-do", label: "Saying What You Do", description: "Work, Study & Preferences", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "saying_work_or_study_status", mode: "lesson_practice_coach" },
  { slug: "saying-what-you-think", label: "Saying What You Think", description: "Opinions & Reasons", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_opinion_say_what_you_think", mode: "lesson_practice_coach" },
  { slug: "saying-what-you-want", label: "Saying What You Want", description: "Food, Shopping & Prices", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "saying_a_simple_food_or_drink_preference", mode: "lesson_practice_coach" },
  { slug: "saying-where-you-are-from", label: "Saying Where You Are From", description: "Greeting & Introducing Yourself", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "saying_where_you_are_from_class", mode: "lesson_practice_coach" },
  { slug: "saying-where-you-went", label: "Saying Where You Went", description: "Past Experiences", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_past_where_you_went", mode: "lesson_practice_coach" },
  { slug: "saying-you-do-not-understand", label: "Saying You Do Not Understand", description: "Help, Problems & Requests", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "saying_you_do_not_understand", mode: "lesson_practice_coach" },
  { slug: "saying-your-name", label: "Saying Your Name", description: "Greeting & Introducing Yourself", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "saying_your_name_class", mode: "lesson_practice_coach" },
  { slug: "setting-direction", label: "Setting Direction", description: "Leadership & Coaching", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_setting_direction", mode: "lesson_practice_coach" },
  { slug: "setting-the-scene", label: "Setting the Scene", description: "Personal Stories", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_story_setting_scene", mode: "lesson_practice_coach" },
  { slug: "sharing-email-addresses", label: "Sharing Email Addresses", description: "Spelling, Numbers & Contact Details", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "sharing_email_for_class_updates", mode: "lesson_practice_coach" },
  { slug: "shopping-service-mission", label: "Shopping Service Mission", description: "Shopping & Services", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_shopping_mission_full", mode: "lesson_practice_coach" },
  { slug: "signposting-clearly", label: "Signposting Clearly", description: "Presenting Ideas", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_present_signposting", mode: "lesson_practice_coach" },
  { slug: "simple-place-words", label: "Simple Place Words", description: "Places & Directions", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "naming_common_places_nearby", mode: "lesson_practice_coach" },
  { slug: "small-talk-mission", label: "Small Talk Mission", description: "Social Small Talk", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_small_talk_mission_make_a_plan", mode: "lesson_practice_coach" },
  { slug: "softening-disagreement", label: "Softening Disagreement", description: "Nuanced Opinions", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_soft_disagreement", mode: "lesson_practice_coach" },
  { slug: "spelling-your-name", label: "Spelling Your Name", description: "Spelling, Numbers & Contact Details", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "spelling_name_for_registration", mode: "lesson_practice_coach" },
  { slug: "starting-small-talk", label: "Starting Small Talk", description: "Social Small Talk", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_small_talk_at_work", mode: "lesson_practice_coach" },
  { slug: "stating-your-position", label: "Stating Your Position", description: "Clear Arguments", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_argument_position", mode: "lesson_practice_coach" },
  { slug: "strategic-workplace-mission", label: "Strategic Workplace Mission", description: "Strategic Workplace Communication", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_strategic_workplace_mission", mode: "lesson_practice_coach" },
  { slug: "structuring-a-short-presentation", label: "Structuring a Short Presentation", description: "Presenting Ideas", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_present_structure", mode: "lesson_practice_coach" },
  { slug: "suggesting-a-solution", label: "Suggesting a Solution", description: "Problems & Solutions", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_problem_suggest_solution", mode: "lesson_practice_coach" },
  { slug: "summarizing-an-article", label: "Summarizing an Article", description: "Media & Information", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_info_summarize_article", mode: "lesson_practice_coach" },
  { slug: "summarizing-decisions", label: "Summarizing Decisions", description: "Professional Meetings", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_meeting_summarize", mode: "lesson_practice_coach" },
  { slug: "summarizing-what-you-heard", label: "Summarizing What You Heard", description: "Advanced Listening & Response", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_summarizing", mode: "lesson_practice_coach" },
  { slug: "supporting-with-reasons", label: "Supporting With Reasons", description: "Clear Arguments", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_argument_reasons", mode: "lesson_practice_coach" },
  { slug: "talking-about-daily-routines", label: "Talking About Daily Routines", description: "Daily Routine & Time", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "talking_about_morning_routine", mode: "lesson_practice_coach" },
  { slug: "talking-about-goals", label: "Talking About Goals", description: "Goals & Progress", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_goals_talk_about_goal", mode: "lesson_practice_coach" },
  { slug: "talking-about-likes", label: "Talking About Likes", description: "Work, Study & Preferences", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "talking_about_learning_preferences", mode: "lesson_practice_coach" },
  { slug: "talking-about-local-habits", label: "Talking About Local Habits", description: "Community & Culture", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_culture_local_habits", mode: "lesson_practice_coach" },
  { slug: "talking-about-weekends", label: "Talking About Weekends", description: "Social Small Talk", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_weekend_plans_chat", mode: "lesson_practice_coach" },
  { slug: "talking-about-yesterday", label: "Talking About Yesterday", description: "Past Experiences", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_past_yesterday_chat", mode: "lesson_practice_coach" },
  { slug: "talking-to-a-driver", label: "Talking to a Driver", description: "Travel & Transport", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_taxi_to_station", mode: "lesson_practice_coach" },
  { slug: "telling-events-in-order", label: "Telling Events in Order", description: "Personal Stories", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_story_events_in_order", mode: "lesson_practice_coach" },
  { slug: "telling-the-time", label: "Telling the Time", description: "Daily Routine & Time", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "asking_class_time", mode: "lesson_practice_coach" },
  { slug: "transport-mission", label: "Transport Mission", description: "Travel & Transport", language: "english", languageLabel: "English", levelCode: "A2", scenarioKey: "a2_transport_mission_ticket_and_driver", mode: "lesson_practice_coach" },
  { slug: "travel-situation-mission", label: "Travel Situation Mission", description: "Travel Situations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_travel_mission", mode: "lesson_practice_coach" },
  { slug: "understanding-client-needs", label: "Understanding Client Needs", description: "Customer & Client Communication", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_client_needs", mode: "lesson_practice_coach" },
  { slug: "understanding-simple-directions", label: "Understanding Simple Directions", description: "Places & Directions", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "understanding_turn_left_and_right", mode: "lesson_practice_coach" },
  { slug: "using-examples", label: "Using Examples", description: "Clear Arguments", language: "english", languageLabel: "English", levelCode: "B2", scenarioKey: "b2_argument_examples", mode: "lesson_practice_coach" },
  { slug: "using-precise-transitions", label: "Using Precise Transitions", description: "Advanced Presentations", language: "english", languageLabel: "English", levelCode: "C1", scenarioKey: "c1_precise_transitions", mode: "lesson_practice_coach" },
  { slug: "work-study-conversation-mission", label: "Work and Study Conversation Mission", description: "Work, Study & Preferences", language: "english", languageLabel: "English", levelCode: "A1", scenarioKey: "work_study_preferences_unit_mission", mode: "lesson_practice_coach" },
  { slug: "workplace-mission", label: "Workplace Mission", description: "Workplace Conversations", language: "english", languageLabel: "English", levelCode: "B1", scenarioKey: "b1_work_mission", mode: "lesson_practice_coach" }
  // </generated:coach_scenarios>
];

export const coachScenarioBySlug = Object.fromEntries(coachScenarios.map((item) => [item.slug, item]));

export const courses = [
  // <generated:courses>
    {
      slug: "english-a1-start-simple-conversations",
      language: "english",
      languageCode: "en",
      languageLabel: "English",
      level: "A1",
      title: "Start Simple Conversations",
      outcome: "Learners can start and close simple conversations, introduce themselves, ask and answer simple personal questions, understand short slow dialogues, and respond without freezing.",
      accessTier: "",
      units: [
        {
          slug: "unit-01-greeting-introducing-yourself",
          title: "Greeting & Introducing Yourself",
          outcome: "User can greet, introduce themselves, and ask someone's name.",
          progress: 0,
          lessons: [
            {
              slug: "saying-hello-and-goodbye",
              title: "Saying Hello and Goodbye",
              status: "published",
              minutes: 8
            },
            {
              slug: "saying-your-name",
              title: "Saying Your Name",
              status: "published",
              minutes: 8
            },
            {
              slug: "asking-someones-name",
              title: "Asking Someone's Name",
              status: "published",
              minutes: 8
            },
            {
              slug: "saying-where-you-are-from",
              title: "Saying Where You Are From",
              status: "published",
              minutes: 8
            },
            {
              slug: "first-conversation-mission",
              title: "First Conversation Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-02-spelling-numbers-contact",
          title: "Spelling, Numbers & Contact Details",
          outcome: "User can spell their name and share simple contact details.",
          progress: 0,
          lessons: [
            {
              slug: "spelling-your-name",
              title: "Spelling Your Name",
              status: "published",
              minutes: 8
            },
            {
              slug: "giving-phone-numbers",
              title: "Giving Phone Numbers",
              status: "published",
              minutes: 8
            },
            {
              slug: "sharing-email-addresses",
              title: "Sharing Email Addresses",
              status: "published",
              minutes: 8
            },
            {
              slug: "asking-for-repetition",
              title: "Asking for Repetition",
              status: "published",
              minutes: 8
            },
            {
              slug: "contact-details-mission",
              title: "Contact Details Mission",
              status: "published",
              minutes: 8
            },
          ]
        },
        {
          slug: "unit-03-daily-routine-time",
          title: "Daily Routine & Time",
          outcome: "User can talk about simple routines, days, and time.",
          progress: 0,
          lessons: [
            {
              slug: "telling-the-time",
              title: "Telling the Time",
              status: "published",
              minutes: 8
            },
            {
              slug: "talking-about-daily-routines",
              title: "Talking About Daily Routines",
              status: "published",
              minutes: 8
            },
            {
              slug: "days-and-simple-schedules",
              title: "Days and Simple Schedules",
              status: "published",
              minutes: 8
            },
            {
              slug: "asking-when-something-happens",
              title: "Asking When Something Happens",
              status: "published",
              minutes: 8
            },
            {
              slug: "routine-conversation-mission",
              title: "Routine Conversation Mission",
              status: "published",
              minutes: 8
            },
          ]
        },
        {
          slug: "unit-04-work-study-and-preferences",
          title: "Work, Study & Preferences",
          outcome: "User can say what they do and talk about simple likes, dislikes, and abilities.",
          progress: 0,
          lessons: [
            {
              slug: "saying-what-you-do",
              title: "Saying What You Do",
              status: "published",
              minutes: 8
            },
            {
              slug: "asking-about-work-or-study",
              title: "Asking About Work or Study",
              status: "published",
              minutes: 8
            },
            {
              slug: "talking-about-likes",
              title: "Talking About Likes",
              status: "published",
              minutes: 8
            },
            {
              slug: "saying-what-you-can-do",
              title: "Saying What You Can Do",
              status: "published",
              minutes: 8
            },
            {
              slug: "work-study-conversation-mission",
              title: "Work and Study Conversation Mission",
              status: "published",
              minutes: 8
            },
          ]
        },
        {
          slug: "unit-05-places-directions",
          title: "Places & Directions",
          outcome: "Ask where places are and understand simple directions.",
          progress: 0,
          lessons: [
            {
              slug: "asking-where-a-place-is",
              title: "Asking Where a Place Is",
              status: "published",
              minutes: 8
            },
            {
              slug: "simple-place-words",
              title: "Simple Place Words",
              status: "published",
              minutes: 8
            },
            {
              slug: "understanding-simple-directions",
              title: "Understanding Simple Directions",
              status: "published",
              minutes: 9
            },
            {
              slug: "asking-how-to-get-there",
              title: "Asking How to Get There",
              status: "published",
              minutes: 9
            },
            {
              slug: "finding-a-place-mission",
              title: "Finding a Place Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-06-food-shopping-prices",
          title: "Food, Shopping & Prices",
          outcome: "Order simple food or drinks, ask prices, and buy basic items.",
          progress: 0,
          lessons: [
            {
              slug: "ordering-a-drink",
              title: "Ordering a Drink",
              status: "published",
              minutes: 8
            },
            {
              slug: "asking-about-prices",
              title: "Asking About Prices",
              status: "published",
              minutes: 8
            },
            {
              slug: "buying-a-simple-item",
              title: "Buying a Simple Item",
              status: "published",
              minutes: 9
            },
            {
              slug: "saying-what-you-want",
              title: "Saying What You Want",
              status: "published",
              minutes: 8
            },
            {
              slug: "cafe-and-shop-mission",
              title: "Cafe and Shop Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-07-help-problems-requests",
          title: "Help, Problems & Requests",
          outcome: "Ask for help, explain a simple problem, and respond politely.",
          progress: 0,
          lessons: [
            {
              slug: "saying-you-do-not-understand",
              title: "Saying You Do Not Understand",
              status: "published",
              minutes: 8
            },
            {
              slug: "asking-for-help",
              title: "Asking for Help",
              status: "published",
              minutes: 8
            },
            {
              slug: "making-simple-requests",
              title: "Making Simple Requests",
              status: "published",
              minutes: 8
            },
            {
              slug: "apologizing-and-thanking",
              title: "Apologizing and Thanking",
              status: "published",
              minutes: 8
            },
            {
              slug: "help-and-problem-mission",
              title: "Help and Problem Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-08-a1-review-final",
          title: "A1 Review & Final Conversation",
          outcome: "Combine A1 skills in a longer but still simple conversation.",
          progress: 0,
          lessons: [
            {
              slug: "review-introductions",
              title: "Review Introductions",
              status: "published",
              minutes: 9
            },
            {
              slug: "review-routines-and-time",
              title: "Review Routines and Time",
              status: "published",
              minutes: 9
            },
            {
              slug: "review-places-and-shopping",
              title: "Review Places and Shopping",
              status: "published",
              minutes: 9
            },
            {
              slug: "final-test-practice",
              title: "Final Test Practice",
              status: "published",
              minutes: 10
            },
            {
              slug: "a1-final-conversation",
              title: "A1 Final Conversation",
              status: "published",
              minutes: 12
            },
          ]
        },
      ]
    },
    {
      slug: "english-a2-everyday-conversations",
      language: "english",
      languageCode: "en",
      languageLabel: "English",
      level: "A2",
      title: "Everyday Conversations",
      outcome: "Learners can handle short everyday conversations, ask simple follow-up questions, talk about plans and recent past activities, and respond naturally with basic reactions.",
      accessTier: "",
      units: [
        {
          slug: "unit-01-social-small-talk",
          title: "Social Small Talk",
          outcome: "Keep short everyday conversations going with follow-up questions.",
          progress: 0,
          lessons: [
            {
              slug: "starting-small-talk",
              title: "Starting Small Talk",
              status: "published",
              minutes: 10
            },
            {
              slug: "asking-follow-up-questions",
              title: "Asking Follow-up Questions",
              status: "published",
              minutes: 10
            },
            {
              slug: "talking-about-weekends",
              title: "Talking About Weekends",
              status: "published",
              minutes: 10
            },
            {
              slug: "reacting-politely",
              title: "Reacting Politely",
              status: "published",
              minutes: 10
            },
            {
              slug: "small-talk-mission",
              title: "Small Talk Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-02-plans-and-invitations",
          title: "Plans & Invitations",
          outcome: "Make simple plans, invite someone, accept, decline, and reschedule.",
          progress: 0,
          lessons: [
            {
              slug: "making-plans",
              title: "Making Plans",
              status: "published",
              minutes: 10
            },
            {
              slug: "inviting-someone",
              title: "Inviting Someone",
              status: "published",
              minutes: 10
            },
            {
              slug: "accepting-and-declining",
              title: "Accepting and Declining",
              status: "published",
              minutes: 10
            },
            {
              slug: "rescheduling",
              title: "Rescheduling",
              status: "published",
              minutes: 10
            },
            {
              slug: "invitation-mission",
              title: "Invitation Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-03-travel-and-transport",
          title: "Travel & Transport",
          outcome: "Ask transport questions and handle simple travel situations.",
          progress: 0,
          lessons: [
            {
              slug: "buying-a-ticket",
              title: "Buying a Ticket",
              status: "published",
              minutes: 10
            },
            {
              slug: "asking-about-departure-time",
              title: "Asking About Departure Time",
              status: "published",
              minutes: 10
            },
            {
              slug: "checking-directions",
              title: "Checking Directions",
              status: "published",
              minutes: 10
            },
            {
              slug: "talking-to-a-driver",
              title: "Talking to a Driver",
              status: "published",
              minutes: 10
            },
            {
              slug: "transport-mission",
              title: "Transport Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-04-shopping-services",
          title: "Shopping & Services",
          outcome: "Ask for items, sizes, availability, and simple service help.",
          progress: 0,
          lessons: [
            {
              slug: "asking-for-an-item",
              title: "Asking for an Item",
              status: "published",
              minutes: 10
            },
            {
              slug: "asking-about-size-and-color",
              title: "Asking About Size and Color",
              status: "published",
              minutes: 10
            },
            {
              slug: "comparing-simple-options",
              title: "Comparing Simple Options",
              status: "published",
              minutes: 10
            },
            {
              slug: "requesting-service-help",
              title: "Requesting Service Help",
              status: "published",
              minutes: 10
            },
            {
              slug: "shopping-service-mission",
              title: "Shopping Service Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-05-health-and-appointments",
          title: "Health & Appointments",
          outcome: "Describe simple symptoms and arrange appointments.",
          progress: 0,
          lessons: [
            {
              slug: "saying-how-you-feel",
              title: "Saying How You Feel",
              status: "published",
              minutes: 10
            },
            {
              slug: "describing-simple-symptoms",
              title: "Describing Simple Symptoms",
              status: "published",
              minutes: 10
            },
            {
              slug: "making-an-appointment",
              title: "Making an Appointment",
              status: "published",
              minutes: 10
            },
            {
              slug: "confirming-details",
              title: "Confirming Details",
              status: "published",
              minutes: 10
            },
            {
              slug: "health-appointment-mission",
              title: "Health Appointment Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-06-past-experiences",
          title: "Past Experiences",
          outcome: "Talk about simple past activities and experiences.",
          progress: 0,
          lessons: [
            {
              slug: "talking-about-yesterday",
              title: "Talking About Yesterday",
              status: "published",
              minutes: 10
            },
            {
              slug: "saying-where-you-went",
              title: "Saying Where You Went",
              status: "published",
              minutes: 10
            },
            {
              slug: "describing-a-simple-experience",
              title: "Describing a Simple Experience",
              status: "published",
              minutes: 10
            },
            {
              slug: "asking-about-past-activities",
              title: "Asking About Past Activities",
              status: "published",
              minutes: 10
            },
            {
              slug: "past-experience-mission",
              title: "Past Experience Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-07-opinions-and-reasons",
          title: "Opinions & Reasons",
          outcome: "Give simple opinions and short reasons.",
          progress: 0,
          lessons: [
            {
              slug: "saying-what-you-think",
              title: "Saying What You Think",
              status: "published",
              minutes: 10
            },
            {
              slug: "giving-simple-reasons",
              title: "Giving Simple Reasons",
              status: "published",
              minutes: 10
            },
            {
              slug: "agreeing-and-disagreeing-politely",
              title: "Agreeing and Disagreeing Politely",
              status: "published",
              minutes: 10
            },
            {
              slug: "asking-for-opinions",
              title: "Asking for Opinions",
              status: "published",
              minutes: 10
            },
            {
              slug: "opinion-conversation-mission",
              title: "Opinion Conversation Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-08-a2-review-final",
          title: "A2 Review & Final Conversation",
          outcome: "Combine A2 everyday skills in a practical conversation.",
          progress: 0,
          lessons: [
            {
              slug: "review-social-and-plans",
              title: "Review Social and Plans",
              status: "published",
              minutes: 10
            },
            {
              slug: "review-travel-and-shopping",
              title: "Review Travel and Shopping",
              status: "published",
              minutes: 10
            },
            {
              slug: "review-health-and-past",
              title: "Review Health and Past",
              status: "published",
              minutes: 10
            },
            {
              slug: "a2-final-test-practice",
              title: "A2 Final Test Practice",
              status: "published",
              minutes: 10
            },
            {
              slug: "a2-final-conversation",
              title: "A2 Final Conversation",
              status: "published",
              minutes: 10
            },
          ]
        },
      ]
    },
    {
      slug: "english-b1-confident-everyday-speaking",
      language: "english",
      languageCode: "en",
      languageLabel: "English",
      level: "B1",
      title: "Confident Everyday Speaking",
      outcome: "Learners can tell connected personal stories, handle common workplace and travel situations, explain problems and solutions, and share opinions with clear reasons in everyday conversations.",
      accessTier: "",
      units: [
        {
          slug: "unit-01-personal-stories",
          title: "Personal Stories",
          outcome: "Tell simple connected stories about personal experiences.",
          progress: 0,
          lessons: [
            {
              slug: "setting-the-scene",
              title: "Setting the Scene",
              status: "published",
              minutes: 12
            },
            {
              slug: "telling-events-in-order",
              title: "Telling Events in Order",
              status: "published",
              minutes: 12
            },
            {
              slug: "describing-feelings",
              title: "Describing Feelings",
              status: "published",
              minutes: 12
            },
            {
              slug: "asking-about-someones-story",
              title: "Asking About Someone's Story",
              status: "published",
              minutes: 12
            },
            {
              slug: "personal-story-mission",
              title: "Personal Story Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-02-workplace-conversations",
          title: "Workplace Conversations",
          outcome: "Handle common workplace conversations with clear, polite language.",
          progress: 0,
          lessons: [
            {
              slug: "explaining-your-task",
              title: "Explaining Your Task",
              status: "published",
              minutes: 12
            },
            {
              slug: "asking-for-clarification",
              title: "Asking for Clarification",
              status: "published",
              minutes: 12
            },
            {
              slug: "giving-a-short-update",
              title: "Giving a Short Update",
              status: "published",
              minutes: 12
            },
            {
              slug: "joining-a-simple-meeting",
              title: "Joining a Simple Meeting",
              status: "published",
              minutes: 12
            },
            {
              slug: "workplace-mission",
              title: "Workplace Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-03-problems-and-solutions",
          title: "Problems & Solutions",
          outcome: "Explain a problem, suggest a solution, and respond to advice.",
          progress: 0,
          lessons: [
            {
              slug: "describing-a-problem",
              title: "Describing a Problem",
              status: "published",
              minutes: 12
            },
            {
              slug: "suggesting-a-solution",
              title: "Suggesting a Solution",
              status: "published",
              minutes: 12
            },
            {
              slug: "responding-to-advice",
              title: "Responding to Advice",
              status: "published",
              minutes: 12
            },
            {
              slug: "making-a-simple-decision",
              title: "Making a Simple Decision",
              status: "published",
              minutes: 12
            },
            {
              slug: "problem-solving-mission",
              title: "Problem Solving Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-04-travel-situations",
          title: "Travel Situations",
          outcome: "Handle travel issues, requests, and explanations.",
          progress: 0,
          lessons: [
            {
              slug: "checking-in",
              title: "Checking In",
              status: "published",
              minutes: 12
            },
            {
              slug: "explaining-a-delay",
              title: "Explaining a Delay",
              status: "published",
              minutes: 12
            },
            {
              slug: "asking-for-recommendations",
              title: "Asking for Recommendations",
              status: "published",
              minutes: 12
            },
            {
              slug: "handling-a-simple-complaint",
              title: "Handling a Simple Complaint",
              status: "published",
              minutes: 12
            },
            {
              slug: "travel-situation-mission",
              title: "Travel Situation Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-05-goals-and-progress",
          title: "Goals & Progress",
          outcome: "Talk about goals, plans, progress, and challenges.",
          progress: 0,
          lessons: [
            {
              slug: "talking-about-goals",
              title: "Talking About Goals",
              status: "published",
              minutes: 12
            },
            {
              slug: "explaining-progress",
              title: "Explaining Progress",
              status: "published",
              minutes: 12
            },
            {
              slug: "discussing-challenges",
              title: "Discussing Challenges",
              status: "published",
              minutes: 12
            },
            {
              slug: "making-next-step-plans",
              title: "Making Next-step Plans",
              status: "published",
              minutes: 12
            },
            {
              slug: "goals-progress-mission",
              title: "Goals Progress Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-06-explaining-preferences",
          title: "Explaining Preferences",
          outcome: "Compare options and explain preferences with reasons.",
          progress: 0,
          lessons: [
            {
              slug: "comparing-two-options",
              title: "Comparing Two Options",
              status: "published",
              minutes: 12
            },
            {
              slug: "explaining-why-you-prefer-something",
              title: "Explaining Why You Prefer Something",
              status: "published",
              minutes: 12
            },
            {
              slug: "asking-about-pros-and-cons",
              title: "Asking About Pros and Cons",
              status: "published",
              minutes: 12
            },
            {
              slug: "reaching-agreement",
              title: "Reaching Agreement",
              status: "published",
              minutes: 12
            },
            {
              slug: "preference-discussion-mission",
              title: "Preference Discussion Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-07-community-and-culture",
          title: "Community & Culture",
          outcome: "Discuss community, habits, and cultural differences politely.",
          progress: 0,
          lessons: [
            {
              slug: "describing-your-community",
              title: "Describing Your Community",
              status: "published",
              minutes: 12
            },
            {
              slug: "talking-about-local-habits",
              title: "Talking About Local Habits",
              status: "published",
              minutes: 12
            },
            {
              slug: "asking-about-culture",
              title: "Asking About Culture",
              status: "published",
              minutes: 12
            },
            {
              slug: "being-polite-with-differences",
              title: "Being Polite With Differences",
              status: "published",
              minutes: 12
            },
            {
              slug: "community-culture-mission",
              title: "Community Culture Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-08-b1-review-final",
          title: "B1 Review & Final Conversation",
          outcome: "Use B1 speaking skills in a connected conversation.",
          progress: 0,
          lessons: [
            {
              slug: "review-stories-and-work",
              title: "Review Stories and Work",
              status: "published",
              minutes: 12
            },
            {
              slug: "review-problems-and-travel",
              title: "Review Problems and Travel",
              status: "published",
              minutes: 12
            },
            {
              slug: "review-goals-and-preferences",
              title: "Review Goals and Preferences",
              status: "published",
              minutes: 12
            },
            {
              slug: "b1-final-test-practice",
              title: "B1 Final Test Practice",
              status: "published",
              minutes: 12
            },
            {
              slug: "b1-final-conversation",
              title: "B1 Final Conversation",
              status: "published",
              minutes: 12
            },
          ]
        },
      ]
    },
    {
      slug: "english-b2-professional-discussions",
      language: "english",
      languageCode: "en",
      languageLabel: "English",
      level: "B2",
      title: "Professional Discussions",
      outcome: "",
      accessTier: "",
      units: [
        {
          slug: "unit-01-clear-arguments",
          title: "Clear Arguments",
          outcome: "Present and support an argument clearly in conversation.",
          progress: 0,
          lessons: [
            {
              slug: "stating-your-position",
              title: "Stating Your Position",
              status: "published",
              minutes: 12
            },
            {
              slug: "supporting-with-reasons",
              title: "Supporting With Reasons",
              status: "published",
              minutes: 12
            },
            {
              slug: "using-examples",
              title: "Using Examples",
              status: "published",
              minutes: 12
            },
            {
              slug: "responding-to-counterpoints",
              title: "Responding to Counterpoints",
              status: "published",
              minutes: 12
            },
            {
              slug: "clear-argument-mission",
              title: "Clear Argument Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-02-professional-meetings",
          title: "Professional Meetings",
          outcome: "Participate actively and professionally in meetings.",
          progress: 0,
          lessons: [
            {
              slug: "opening-a-meeting-point",
              title: "Opening a Meeting Point",
              status: "published",
              minutes: 12
            },
            {
              slug: "clarifying-scope",
              title: "Clarifying Scope",
              status: "published",
              minutes: 12
            },
            {
              slug: "giving-constructive-feedback",
              title: "Giving Constructive Feedback",
              status: "published",
              minutes: 12
            },
            {
              slug: "summarizing-decisions",
              title: "Summarizing Decisions",
              status: "published",
              minutes: 12
            },
            {
              slug: "meeting-participation-mission",
              title: "Meeting Participation Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-03-negotiation-and-compromise",
          title: "Negotiation & Compromise",
          outcome: "Negotiate simple professional outcomes and find compromise.",
          progress: 0,
          lessons: [
            {
              slug: "expressing-priorities",
              title: "Expressing Priorities",
              status: "published",
              minutes: 12
            },
            {
              slug: "making-a-proposal",
              title: "Making a Proposal",
              status: "published",
              minutes: 12
            },
            {
              slug: "handling-objections",
              title: "Handling Objections",
              status: "published",
              minutes: 12
            },
            {
              slug: "finding-middle-ground",
              title: "Finding Middle Ground",
              status: "published",
              minutes: 12
            },
            {
              slug: "negotiation-mission",
              title: "Negotiation Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-04-presenting-ideas",
          title: "Presenting Ideas",
          outcome: "Present an idea and answer questions naturally.",
          progress: 0,
          lessons: [
            {
              slug: "structuring-a-short-presentation",
              title: "Structuring a Short Presentation",
              status: "published",
              minutes: 12
            },
            {
              slug: "signposting-clearly",
              title: "Signposting Clearly",
              status: "published",
              minutes: 12
            },
            {
              slug: "explaining-benefits-and-risks",
              title: "Explaining Benefits and Risks",
              status: "published",
              minutes: 12
            },
            {
              slug: "answering-questions",
              title: "Answering Questions",
              status: "published",
              minutes: 12
            },
            {
              slug: "idea-presentation-mission",
              title: "Idea Presentation Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-05-media-and-information",
          title: "Media & Information",
          outcome: "Discuss information, sources, and viewpoints critically.",
          progress: 0,
          lessons: [
            {
              slug: "summarizing-an-article",
              title: "Summarizing an Article",
              status: "published",
              minutes: 12
            },
            {
              slug: "discussing-reliable-sources",
              title: "Discussing Reliable Sources",
              status: "published",
              minutes: 12
            },
            {
              slug: "explaining-a-viewpoint",
              title: "Explaining a Viewpoint",
              status: "published",
              minutes: 12
            },
            {
              slug: "responding-to-new-information",
              title: "Responding to New Information",
              status: "published",
              minutes: 12
            },
            {
              slug: "information-discussion-mission",
              title: "Information Discussion Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-06-customer-and-client-communication",
          title: "Customer & Client Communication",
          outcome: "Handle client conversations with clarity, empathy, and professionalism.",
          progress: 0,
          lessons: [
            {
              slug: "understanding-client-needs",
              title: "Understanding Client Needs",
              status: "published",
              minutes: 12
            },
            {
              slug: "explaining-options",
              title: "Explaining Options",
              status: "published",
              minutes: 12
            },
            {
              slug: "handling-concerns",
              title: "Handling Concerns",
              status: "published",
              minutes: 12
            },
            {
              slug: "confirming-next-steps",
              title: "Confirming Next Steps",
              status: "published",
              minutes: 12
            },
            {
              slug: "client-conversation-mission",
              title: "Client Conversation Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-07-complex-problem-solving",
          title: "Complex Problem Solving",
          outcome: "Analyze a complex problem and discuss tradeoffs.",
          progress: 0,
          lessons: [
            {
              slug: "framing-the-problem",
              title: "Framing the Problem",
              status: "published",
              minutes: 12
            },
            {
              slug: "explaining-causes",
              title: "Explaining Causes",
              status: "published",
              minutes: 12
            },
            {
              slug: "discussing-tradeoffs",
              title: "Discussing Tradeoffs",
              status: "published",
              minutes: 12
            },
            {
              slug: "recommending-a-solution",
              title: "Recommending a Solution",
              status: "published",
              minutes: 12
            },
            {
              slug: "problem-solving-discussion-mission",
              title: "Problem Solving Discussion Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-08-b2-review-final",
          title: "B2 Review & Final Discussion",
          outcome: "Use B2 discussion skills in professional and social contexts.",
          progress: 0,
          lessons: [
            {
              slug: "review-arguments-and-meetings",
              title: "Review Arguments and Meetings",
              status: "published",
              minutes: 12
            },
            {
              slug: "review-negotiation-and-presenting",
              title: "Review Negotiation and Presenting",
              status: "published",
              minutes: 12
            },
            {
              slug: "review-information-and-clients",
              title: "Review Information and Clients",
              status: "published",
              minutes: 12
            },
            {
              slug: "b2-final-test-practice",
              title: "B2 Final Test Practice",
              status: "published",
              minutes: 12
            },
            {
              slug: "b2-final-discussion",
              title: "B2 Final Discussion",
              status: "published",
              minutes: 12
            },
          ]
        },
      ]
    },
    {
      slug: "english-c1-advanced-fluency",
      language: "english",
      languageCode: "en",
      languageLabel: "English",
      level: "C1",
      title: "Advanced Fluency",
      outcome: "",
      accessTier: "",
      units: [
        {
          slug: "unit-01-nuanced-opinions",
          title: "Nuanced Opinions",
          outcome: "Express nuanced opinions with precision and flexibility.",
          progress: 0,
          lessons: [
            {
              slug: "qualifying-your-opinion",
              title: "Qualifying Your Opinion",
              status: "published",
              minutes: 12
            },
            {
              slug: "expressing-certainty-and-doubt",
              title: "Expressing Certainty and Doubt",
              status: "published",
              minutes: 12
            },
            {
              slug: "balancing-two-viewpoints",
              title: "Balancing Two Viewpoints",
              status: "published",
              minutes: 12
            },
            {
              slug: "softening-disagreement",
              title: "Softening Disagreement",
              status: "published",
              minutes: 12
            },
            {
              slug: "nuanced-opinion-mission",
              title: "Nuanced Opinion Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-02-strategic-workplace-communication",
          title: "Strategic Workplace Communication",
          outcome: "Communicate strategically in complex professional situations.",
          progress: 0,
          lessons: [
            {
              slug: "aligning-stakeholders",
              title: "Aligning Stakeholders",
              status: "published",
              minutes: 12
            },
            {
              slug: "managing-expectations",
              title: "Managing Expectations",
              status: "published",
              minutes: 12
            },
            {
              slug: "handling-sensitive-feedback",
              title: "Handling Sensitive Feedback",
              status: "published",
              minutes: 12
            },
            {
              slug: "communicating-risk",
              title: "Communicating Risk",
              status: "published",
              minutes: 12
            },
            {
              slug: "strategic-workplace-mission",
              title: "Strategic Workplace Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-03-advanced-presentations",
          title: "Advanced Presentations",
          outcome: "Present complex ideas and handle challenging questions.",
          progress: 0,
          lessons: [
            {
              slug: "framing-a-complex-topic",
              title: "Framing a Complex Topic",
              status: "published",
              minutes: 12
            },
            {
              slug: "building-a-persuasive-flow",
              title: "Building a Persuasive Flow",
              status: "published",
              minutes: 12
            },
            {
              slug: "using-precise-transitions",
              title: "Using Precise Transitions",
              status: "published",
              minutes: 12
            },
            {
              slug: "handling-challenging-questions",
              title: "Handling Challenging Questions",
              status: "published",
              minutes: 12
            },
            {
              slug: "advanced-presentation-mission",
              title: "Advanced Presentation Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-04-debate-and-analysis",
          title: "Debate & Analysis",
          outcome: "Analyze arguments and respond persuasively in debate-style conversations.",
          progress: 0,
          lessons: [
            {
              slug: "identifying-assumptions",
              title: "Identifying Assumptions",
              status: "published",
              minutes: 12
            },
            {
              slug: "challenging-an-argument",
              title: "Challenging an Argument",
              status: "published",
              minutes: 12
            },
            {
              slug: "presenting-evidence",
              title: "Presenting Evidence",
              status: "published",
              minutes: 12
            },
            {
              slug: "responding-under-pressure",
              title: "Responding Under Pressure",
              status: "published",
              minutes: 12
            },
            {
              slug: "debate-analysis-mission",
              title: "Debate Analysis Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-05-cross-cultural-professionalism",
          title: "Cross-cultural Professionalism",
          outcome: "Communicate across cultures with tact, clarity, and professionalism.",
          progress: 0,
          lessons: [
            {
              slug: "reading-context",
              title: "Reading Context",
              status: "published",
              minutes: 12
            },
            {
              slug: "asking-tactful-questions",
              title: "Asking Tactful Questions",
              status: "published",
              minutes: 12
            },
            {
              slug: "explaining-local-norms",
              title: "Explaining Local Norms",
              status: "published",
              minutes: 12
            },
            {
              slug: "repairing-misunderstanding",
              title: "Repairing Misunderstanding",
              status: "published",
              minutes: 12
            },
            {
              slug: "cross-cultural-mission",
              title: "Cross-cultural Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-06-leadership-and-coaching",
          title: "Leadership & Coaching",
          outcome: "Lead conversations, coach others, and guide decisions.",
          progress: 0,
          lessons: [
            {
              slug: "setting-direction",
              title: "Setting Direction",
              status: "published",
              minutes: 12
            },
            {
              slug: "coaching-with-questions",
              title: "Coaching with Questions",
              status: "published",
              minutes: 12
            },
            {
              slug: "giving-actionable-feedback",
              title: "Giving Actionable Feedback",
              status: "published",
              minutes: 12
            },
            {
              slug: "guiding-a-decision",
              title: "Guiding a Decision",
              status: "published",
              minutes: 12
            },
            {
              slug: "leadership-coaching-mission",
              title: "Leadership Coaching Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-07-advanced-listening-response",
          title: "Advanced Listening & Response",
          outcome: "Respond accurately to dense, fast, or indirect speech.",
          progress: 0,
          lessons: [
            {
              slug: "catching-implied-meaning",
              title: "Catching Implied Meaning",
              status: "published",
              minutes: 12
            },
            {
              slug: "responding-to-long-turns",
              title: "Responding to Long Turns",
              status: "published",
              minutes: 12
            },
            {
              slug: "summarizing-what-you-heard",
              title: "Summarizing What You Heard",
              status: "published",
              minutes: 12
            },
            {
              slug: "asking-high-quality-follow-ups",
              title: "Asking High-quality Follow-ups",
              status: "published",
              minutes: 12
            },
            {
              slug: "advanced-listening-mission",
              title: "Advanced Listening Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-08-c1-review-final",
          title: "C1 Review & Final Conversation",
          outcome: "Use C1 skills in complex professional and social conversations.",
          progress: 0,
          lessons: [
            {
              slug: "review-nuance-and-strategy",
              title: "Review Nuance and Strategy",
              status: "published",
              minutes: 12
            },
            {
              slug: "review-presenting-and-debate",
              title: "Review Presenting and Debate",
              status: "published",
              minutes: 12
            },
            {
              slug: "review-leadership-and-listening",
              title: "Review Leadership and Listening",
              status: "published",
              minutes: 12
            },
            {
              slug: "c1-final-test-practice",
              title: "C1 Final Test Practice",
              status: "published",
              minutes: 12
            },
            {
              slug: "c1-final-conversation",
              title: "C1 Final Conversation",
              status: "published",
              minutes: 12
            },
          ]
        },
      ]
    },
    {
      slug: "arabic-a1-fusha-foundations",
      language: "arabic",
      languageCode: "ar",
      languageLabel: "Arabic",
      level: "A1",
      title: "Arabic Foundations",
      outcome: "Learners can recognize and produce very simple Arabic phrases for greetings, introductions, classroom instructions, and asking for clarification, while beginning to understand short formal study-circle expressions.",
      accessTier: "pro",
      units: [
        {
          slug: "unit-01-fusha-foundations",
          title: "Arabic Foundations",
          outcome: "Start a simple formal Arabic conversation, follow basic study instructions, and ask for repetition when you do not understand.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-formal-greetings",
              title: "Formal Greetings",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-name-and-origin",
              title: "Name and Origin",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-class-and-study-instructions",
              title: "Class and Study Instructions",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-asking-when-you-do-not-understand",
              title: "Asking When You Do Not Understand",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-fusha-introduction-mission",
              title: "Arabic Introduction Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-02-letters-numbers-contact",
          title: "Letters, Numbers & Contact",
          outcome: "Spell simple names, exchange numbers, and share basic contact details in Arabic.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-spelling-your-name",
              title: "Spelling Your Name",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-numbers-and-phone",
              title: "Arabic Numbers and Phone",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-sharing-email-addresses",
              title: "Sharing Email Addresses",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-asking-to-repeat-a-letter",
              title: "Asking to Repeat a Letter",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-contact-details-mission",
              title: "Contact Details Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-03-time-and-routine",
          title: "Time & Daily Routine",
          outcome: "Talk about simple time, days, schedules, and daily activities in Arabic.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-asking-the-time",
              title: "Asking the Time",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-days-of-the-week",
              title: "Days of the Week",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-talking-about-daily-routines",
              title: "Talking About Daily Routines",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-asking-when",
              title: "Asking When",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-routine-and-time-mission",
              title: "Routine and Time Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-04-family-work-study",
          title: "Family, Work & Study",
          outcome: "Talk simply about family, work, study, likes, and basic ability.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-family-members",
              title: "Family Members",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-saying-what-you-do",
              title: "Saying What You Do",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-asking-about-work-or-study",
              title: "Asking About Work or Study",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-likes-and-ability",
              title: "Likes and Ability",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-family-work-study-mission",
              title: "Family, Work, and Study Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-05-places-directions",
          title: "Places & Directions",
          outcome: "Ask where places are and understand simple directions in Arabic.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-asking-where-a-place-is",
              title: "Asking Where a Place Is",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-simple-place-words",
              title: "Simple Place Words",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-understanding-simple-directions",
              title: "Understanding Simple Directions",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-asking-how-to-get-there",
              title: "Asking How to Get There",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-finding-a-place-mission",
              title: "Finding a Place Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-06-food-shopping-prices",
          title: "Food, Shopping & Prices",
          outcome: "Order simple items, ask prices, and say what you want in Arabic.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-ordering-a-drink",
              title: "Ordering a Drink",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-asking-about-prices",
              title: "Asking About Prices",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-buying-a-simple-item",
              title: "Buying a Simple Item",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-saying-what-you-want",
              title: "Saying What You Want",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-cafe-and-shop-mission",
              title: "Cafe and Shop Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-07-help-problems-requests",
          title: "Help, Problems & Requests",
          outcome: "Ask for help, explain simple problems, and make polite requests in Arabic.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-saying-you-do-not-understand",
              title: "Saying You Do Not Understand",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-asking-for-help",
              title: "Asking for Help",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-making-simple-requests",
              title: "Making Simple Requests",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-apologizing-and-thanking",
              title: "Apologizing and Thanking",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-help-and-problem-mission",
              title: "Help and Problem Mission",
              status: "published",
              minutes: 10
            },
          ]
        },
        {
          slug: "unit-08-a1-review-final",
          title: "A1 Review & Final Conversation",
          outcome: "Combine Arabic A1 skills in longer but still simple formal conversations.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-review-introductions-and-contact",
              title: "Review Introductions and Contact",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-review-routine-and-study",
              title: "Review Routine and Study",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-review-places-and-shopping",
              title: "Review Places and Shopping",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-a1-final-test-practice",
              title: "A1 Final Test Practice",
              status: "published",
              minutes: 10
            },
            {
              slug: "arabic-a1-final-conversation",
              title: "A1 Final Conversation",
              status: "published",
              minutes: 10
            },
          ]
        },
      ]
    },
    {
      slug: "arabic-a2-everyday-conversations",
      language: "arabic",
      languageCode: "ar",
      languageLabel: "Arabic",
      level: "A2",
      title: "Arabic Everyday Conversations",
      outcome: "Learners can handle short everyday Arabic conversations, ask simple follow-up questions, make plans, describe simple past experiences, ask for service help, and give short reasons while maintaining clear formal Arabic pronunciation and basic reading support.",
      accessTier: "pro",
      units: [
        {
          slug: "unit-01-social-follow-up",
          title: "Social Follow-up",
          outcome: "Keep a short Arabic conversation going with follow-up questions, reactions, and simple personal details.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-reconnecting-after-class",
              title: "Reconnecting After Class",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-asking-follow-up-questions",
              title: "Asking Follow-up Questions",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-talking-about-the-weekend",
              title: "Talking About the Weekend",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-reacting-with-interest",
              title: "Reacting With Interest",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-social-follow-up-mission",
              title: "Social Follow-up Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-02-plans-invitations",
          title: "Plans & Invitations",
          outcome: "Invite someone, accept or decline politely, reschedule, and confirm time and place in Arabic.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-making-a-simple-plan",
              title: "Making a Simple Plan",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-inviting-someone",
              title: "Inviting Someone",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-accepting-and-declining",
              title: "Accepting and Declining",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-rescheduling-politely",
              title: "Rescheduling Politely",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-invitation-mission",
              title: "Invitation Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-03-transport-travel",
          title: "Transport & Travel",
          outcome: "Ask about transport, tickets, departure time, directions, and simple travel help.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-buying-a-ticket",
              title: "Buying a Ticket",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-asking-about-departure-time",
              title: "Asking About Departure Time",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-checking-directions",
              title: "Checking Directions",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-talking-to-a-driver",
              title: "Talking to a Driver",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-transport-travel-mission",
              title: "Transport and Travel Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-04-shopping-services",
          title: "Shopping & Services",
          outcome: "Ask for items, compare simple options, request service help, and confirm details.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-asking-for-an-item",
              title: "Asking for an Item",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-asking-about-size-and-color",
              title: "Asking About Size and Color",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-comparing-simple-options",
              title: "Comparing Simple Options",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-requesting-service-help",
              title: "Requesting Service Help",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-shopping-service-mission",
              title: "Shopping Service Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-05-health-appointments",
          title: "Health & Appointments",
          outcome: "Describe simple symptoms, make appointments, and confirm basic health service details.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-saying-how-you-feel",
              title: "Saying How You Feel",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-describing-simple-symptoms",
              title: "Describing Simple Symptoms",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-making-an-appointment",
              title: "Making an Appointment",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-confirming-appointment-details",
              title: "Confirming Appointment Details",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-health-appointment-mission",
              title: "Health Appointment Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-06-past-experiences",
          title: "Past Experiences",
          outcome: "Talk about recent activities, where you went, what happened, and how it felt.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-talking-about-yesterday",
              title: "Talking About Yesterday",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-saying-where-you-went",
              title: "Saying Where You Went",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-describing-a-simple-experience",
              title: "Describing a Simple Experience",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-asking-about-past-activities",
              title: "Asking About Past Activities",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-past-experience-mission",
              title: "Past Experience Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-07-opinions-reasons",
          title: "Opinions & Reasons",
          outcome: "Give simple opinions, short reasons, agreement, disagreement, and preference in Arabic.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-saying-what-you-think",
              title: "Saying What You Think",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-giving-simple-reasons",
              title: "Giving Simple Reasons",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-agreeing-and-disagreeing-politely",
              title: "Agreeing and Disagreeing Politely",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-asking-for-opinions",
              title: "Asking for Opinions",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-opinion-conversation-mission",
              title: "Opinion Conversation Mission",
              status: "published",
              minutes: 12
            },
          ]
        },
        {
          slug: "unit-08-a2-review-final",
          title: "A2 Review & Final Conversation",
          outcome: "Combine Arabic A2 social, planning, travel, service, health, past, and opinion skills in practical formal conversations.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-review-social-and-plans",
              title: "Review Social and Plans",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-review-travel-and-services",
              title: "Review Travel and Services",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-review-health-and-past",
              title: "Review Health and Past",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-a2-final-test-practice",
              title: "A2 Final Test Practice",
              status: "published",
              minutes: 12
            },
            {
              slug: "arabic-a2-final-conversation",
              title: "A2 Final Conversation",
              status: "published",
              minutes: 12
            },
          ]
        },
      ]
    },
    {
      slug: "arabic-b1-connected-conversations",
      language: "arabic",
      languageCode: "ar",
      languageLabel: "Arabic",
      level: "B1",
      title: "Arabic Connected Conversations",
      outcome: "Learners can tell connected personal stories, handle work and travel situations, explain problems and solutions, compare options, discuss goals, and ask polite cultural questions in clear formal Arabic.",
      accessTier: "pro",
      units: [
        {
          slug: "unit-01-personal-stories",
          title: "Personal Stories",
          outcome: "Tell connected personal stories with time, place, sequence, feeling, and follow-up details.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b1-setting-the-scene",
              title: "Setting the Scene",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-telling-events-in-order",
              title: "Telling Events in Order",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-describing-feelings",
              title: "Describing Feelings",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-asking-about-someones-story",
              title: "Asking About Someone's Story",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-personal-story-mission",
              title: "Personal Story Mission",
              status: "published",
              minutes: 14
            },
          ]
        },
        {
          slug: "unit-02-workplace-conversations",
          title: "Workplace Conversations",
          outcome: "Explain tasks, clarify requests, give updates, join simple meetings, and close with action points.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b1-explaining-your-task",
              title: "Explaining Your Task",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-asking-for-clarification",
              title: "Asking for Clarification",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-giving-a-short-update",
              title: "Giving a Short Update",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-joining-a-simple-meeting",
              title: "Joining a Simple Meeting",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-workplace-mission",
              title: "Workplace Mission",
              status: "published",
              minutes: 14
            },
          ]
        },
        {
          slug: "unit-03-problems-and-solutions",
          title: "Problems & Solutions",
          outcome: "Explain a problem, suggest solutions, respond to advice, and make a simple decision.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b1-describing-a-problem",
              title: "Describing a Problem",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-suggesting-a-solution",
              title: "Suggesting a Solution",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-responding-to-advice",
              title: "Responding to Advice",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-making-a-simple-decision",
              title: "Making a Simple Decision",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-problem-solving-mission",
              title: "Problem Solving Mission",
              status: "published",
              minutes: 14
            },
          ]
        },
        {
          slug: "unit-04-travel-situations",
          title: "Travel Situations",
          outcome: "Handle travel check-in, delays, recommendations, complaints, and practical travel requests.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b1-checking-in",
              title: "Checking In",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-explaining-a-delay",
              title: "Explaining a Delay",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-asking-for-recommendations",
              title: "Asking for Recommendations",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-handling-a-simple-complaint",
              title: "Handling a Simple Complaint",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-travel-situation-mission",
              title: "Travel Situation Mission",
              status: "published",
              minutes: 14
            },
          ]
        },
        {
          slug: "unit-05-goals-and-progress",
          title: "Goals & Progress",
          outcome: "Talk about goals, progress, challenges, and next steps with connected reasons.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b1-talking-about-goals",
              title: "Talking About Goals",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-explaining-progress",
              title: "Explaining Progress",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-discussing-challenges",
              title: "Discussing Challenges",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-making-next-step-plans",
              title: "Making Next-step Plans",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-goals-progress-mission",
              title: "Goals Progress Mission",
              status: "published",
              minutes: 14
            },
          ]
        },
        {
          slug: "unit-06-explaining-preferences",
          title: "Explaining Preferences",
          outcome: "Compare options, explain preferences, ask about pros and cons, and reach agreement.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b1-comparing-two-options",
              title: "Comparing Two Options",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-explaining-why-you-prefer-something",
              title: "Explaining Why You Prefer Something",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-asking-about-pros-and-cons",
              title: "Asking About Pros and Cons",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-reaching-agreement",
              title: "Reaching Agreement",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-preference-discussion-mission",
              title: "Preference Discussion Mission",
              status: "published",
              minutes: 14
            },
          ]
        },
        {
          slug: "unit-07-community-and-culture",
          title: "Community & Culture",
          outcome: "Discuss community, habits, differences, and polite cultural questions in clear formal Arabic.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b1-describing-your-community",
              title: "Describing Your Community",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-talking-about-local-habits",
              title: "Talking About Local Habits",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-asking-about-culture",
              title: "Asking About Culture",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-being-polite-with-differences",
              title: "Being Polite With Differences",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-community-culture-mission",
              title: "Community Culture Mission",
              status: "published",
              minutes: 14
            },
          ]
        },
        {
          slug: "unit-08-b1-review-final",
          title: "B1 Review & Final Conversation",
          outcome: "Use B1 Arabic skills in connected conversations across stories, work, problems, travel, goals, and culture.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b1-review-stories-and-work",
              title: "Review Stories and Work",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-review-problems-and-travel",
              title: "Review Problems and Travel",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-review-goals-and-preferences",
              title: "Review Goals and Preferences",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-b1-final-test-practice",
              title: "B1 Final Test Practice",
              status: "published",
              minutes: 14
            },
            {
              slug: "arabic-b1-b1-final-conversation",
              title: "B1 Final Conversation",
              status: "published",
              minutes: 14
            },
          ]
        },
      ]
    },
    {
      slug: "arabic-b2-professional-discussions",
      language: "arabic",
      languageCode: "ar",
      languageLabel: "Arabic",
      level: "B2",
      title: "Arabic Professional Discussions",
      outcome: "Learners can participate in structured professional and social discussions: state a position, support it with reasons and examples, respond to objections, take part in meetings, negotiate compromises, present ideas, evaluate sources, communicate with clients, and recommend solutions in clear formal Arabic.",
      accessTier: "pro",
      units: [
        {
          slug: "unit-01-clear-arguments",
          title: "Clear Arguments",
          outcome: "Present and support an argument clearly in formal Arabic conversation.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b2-stating-your-position",
              title: "Stating Your Position",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-supporting-with-reasons",
              title: "Supporting With Reasons",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-using-examples",
              title: "Using Examples",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-responding-to-counterpoints",
              title: "Responding to Counterpoints",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-clear-argument-mission",
              title: "Clear Argument Mission",
              status: "published",
              minutes: 16
            },
          ]
        },
        {
          slug: "unit-02-professional-meetings",
          title: "Professional Meetings",
          outcome: "Participate actively and professionally in meetings.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b2-opening-a-meeting-point",
              title: "Opening a Meeting Point",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-clarifying-scope",
              title: "Clarifying Scope",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-giving-constructive-feedback",
              title: "Giving Constructive Feedback",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-summarizing-decisions",
              title: "Summarizing Decisions",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-meeting-participation-mission",
              title: "Meeting Participation Mission",
              status: "published",
              minutes: 16
            },
          ]
        },
        {
          slug: "unit-03-negotiation-and-compromise",
          title: "Negotiation & Compromise",
          outcome: "Negotiate simple professional outcomes and find compromise.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b2-expressing-priorities",
              title: "Expressing Priorities",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-making-a-proposal",
              title: "Making a Proposal",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-handling-objections",
              title: "Handling Objections",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-finding-middle-ground",
              title: "Finding Middle Ground",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-negotiation-mission",
              title: "Negotiation Mission",
              status: "published",
              minutes: 16
            },
          ]
        },
        {
          slug: "unit-04-presenting-ideas",
          title: "Presenting Ideas",
          outcome: "Present an idea and answer questions naturally.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b2-structuring-a-short-presentation",
              title: "Structuring a Short Presentation",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-signposting-clearly",
              title: "Signposting Clearly",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-explaining-benefits-and-risks",
              title: "Explaining Benefits and Risks",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-answering-questions",
              title: "Answering Questions",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-idea-presentation-mission",
              title: "Idea Presentation Mission",
              status: "published",
              minutes: 16
            },
          ]
        },
        {
          slug: "unit-05-media-and-information",
          title: "Media & Information",
          outcome: "Discuss information, sources, and viewpoints critically.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b2-summarizing-an-article",
              title: "Summarizing an Article",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-discussing-reliable-sources",
              title: "Discussing Reliable Sources",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-explaining-a-viewpoint",
              title: "Explaining a Viewpoint",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-responding-to-new-information",
              title: "Responding to New Information",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-information-discussion-mission",
              title: "Information Discussion Mission",
              status: "published",
              minutes: 16
            },
          ]
        },
        {
          slug: "unit-06-customer-and-client-communication",
          title: "Customer & Client Communication",
          outcome: "Handle client conversations with clarity, empathy, and professionalism.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b2-understanding-client-needs",
              title: "Understanding Client Needs",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-explaining-options",
              title: "Explaining Options",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-handling-concerns",
              title: "Handling Concerns",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-confirming-next-steps",
              title: "Confirming Next Steps",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-client-conversation-mission",
              title: "Client Conversation Mission",
              status: "published",
              minutes: 16
            },
          ]
        },
        {
          slug: "unit-07-complex-problem-solving",
          title: "Complex Problem Solving",
          outcome: "Analyze a complex problem and discuss tradeoffs.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b2-framing-the-problem",
              title: "Framing the Problem",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-explaining-causes",
              title: "Explaining Causes",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-discussing-tradeoffs",
              title: "Discussing Tradeoffs",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-recommending-a-solution",
              title: "Recommending a Solution",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-problem-solving-discussion-mission",
              title: "Problem Solving Discussion Mission",
              status: "published",
              minutes: 16
            },
          ]
        },
        {
          slug: "unit-08-b2-review-final",
          title: "B2 Review & Final Discussion",
          outcome: "Use B2 discussion skills in professional and social contexts.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-b2-review-arguments-and-meetings",
              title: "Review Arguments and Meetings",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-review-negotiation-and-presenting",
              title: "Review Negotiation and Presenting",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-review-information-and-clients",
              title: "Review Information and Clients",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-b2-final-test-practice",
              title: "B2 Final Test Practice",
              status: "published",
              minutes: 16
            },
            {
              slug: "arabic-b2-b2-final-discussion",
              title: "B2 Final Discussion",
              status: "published",
              minutes: 16
            },
          ]
        },
      ]
    },
    {
      slug: "arabic-c1-advanced-fluency",
      language: "arabic",
      languageCode: "ar",
      languageLabel: "Arabic",
      level: "C1",
      title: "Arabic Advanced Fluency",
      outcome: "Learners can participate in complex professional and social conversations with nuance, precision, tact, strategic framing, persuasive structure, and accurate response to indirect or dense speech in formal Arabic.",
      accessTier: "pro",
      units: [
        {
          slug: "unit-01-nuanced-opinions",
          title: "Nuanced Opinions",
          outcome: "Express nuanced opinions with precision and flexibility.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-c1-qualifying-your-opinion",
              title: "Qualifying Your Opinion",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-expressing-certainty-and-doubt",
              title: "Expressing Certainty and Doubt",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-balancing-two-viewpoints",
              title: "Balancing Two Viewpoints",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-softening-disagreement",
              title: "Softening Disagreement",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-nuanced-opinion-mission",
              title: "Nuanced Opinion Mission",
              status: "published",
              minutes: 18
            },
          ]
        },
        {
          slug: "unit-02-strategic-workplace-communication",
          title: "Strategic Workplace Communication",
          outcome: "Communicate strategically in complex professional situations.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-c1-aligning-stakeholders",
              title: "Aligning Stakeholders",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-managing-expectations",
              title: "Managing Expectations",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-handling-sensitive-feedback",
              title: "Handling Sensitive Feedback",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-communicating-risk",
              title: "Communicating Risk",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-strategic-workplace-mission",
              title: "Strategic Workplace Mission",
              status: "published",
              minutes: 18
            },
          ]
        },
        {
          slug: "unit-03-advanced-presentations",
          title: "Advanced Presentations",
          outcome: "Present complex ideas and handle challenging questions.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-c1-framing-a-complex-topic",
              title: "Framing a Complex Topic",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-building-a-persuasive-flow",
              title: "Building a Persuasive Flow",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-using-precise-transitions",
              title: "Using Precise Transitions",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-handling-challenging-questions",
              title: "Handling Challenging Questions",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-advanced-presentation-mission",
              title: "Advanced Presentation Mission",
              status: "published",
              minutes: 18
            },
          ]
        },
        {
          slug: "unit-04-debate-and-analysis",
          title: "Debate & Analysis",
          outcome: "Analyze arguments and respond persuasively in debate-style conversations.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-c1-identifying-assumptions",
              title: "Identifying Assumptions",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-challenging-an-argument",
              title: "Challenging an Argument",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-presenting-evidence",
              title: "Presenting Evidence",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-responding-under-pressure",
              title: "Responding Under Pressure",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-debate-analysis-mission",
              title: "Debate Analysis Mission",
              status: "published",
              minutes: 18
            },
          ]
        },
        {
          slug: "unit-05-cross-cultural-professionalism",
          title: "Cross-cultural Professionalism",
          outcome: "Communicate across cultures with tact, clarity, and professionalism.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-c1-reading-context",
              title: "Reading Context",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-asking-tactful-questions",
              title: "Asking Tactful Questions",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-explaining-local-norms",
              title: "Explaining Local Norms",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-repairing-misunderstanding",
              title: "Repairing Misunderstanding",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-cross-cultural-mission",
              title: "Cross-cultural Mission",
              status: "published",
              minutes: 18
            },
          ]
        },
        {
          slug: "unit-06-leadership-and-coaching",
          title: "Leadership & Coaching",
          outcome: "Lead conversations, coach others, and guide decisions.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-c1-setting-direction",
              title: "Setting Direction",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-coaching-with-questions",
              title: "Coaching With Questions",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-giving-actionable-feedback",
              title: "Giving Actionable Feedback",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-guiding-a-decision",
              title: "Guiding a Decision",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-leadership-coaching-mission",
              title: "Leadership Coaching Mission",
              status: "published",
              minutes: 18
            },
          ]
        },
        {
          slug: "unit-07-advanced-listening-response",
          title: "Advanced Listening & Response",
          outcome: "Respond accurately to dense, fast, or indirect speech.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-c1-catching-implied-meaning",
              title: "Catching Implied Meaning",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-responding-to-long-turns",
              title: "Responding to Long Turns",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-summarizing-what-you-heard",
              title: "Summarizing What You Heard",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-asking-high-quality-follow-ups",
              title: "Asking High-quality Follow-ups",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-advanced-listening-mission",
              title: "Advanced Listening Mission",
              status: "published",
              minutes: 18
            },
          ]
        },
        {
          slug: "unit-08-c1-review-final",
          title: "C1 Review & Final Conversation",
          outcome: "Use C1 skills in complex professional and social conversations.",
          progress: 0,
          lessons: [
            {
              slug: "arabic-c1-review-nuance-and-strategy",
              title: "Review Nuance and Strategy",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-review-presenting-and-debate",
              title: "Review Presenting and Debate",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-review-leadership-and-listening",
              title: "Review Leadership and Listening",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-c1-final-test-practice",
              title: "C1 Final Test Practice",
              status: "published",
              minutes: 18
            },
            {
              slug: "arabic-c1-c1-final-conversation",
              title: "C1 Final Conversation",
              status: "published",
              minutes: 18
            },
          ]
        },
      ]
    }
  // </generated:courses>
];

export const coursesBySlug = Object.fromEntries(courses.map((item) => [item.slug, item]));

export type LessonPlacement = {
  level: string;
  languageLabel: string;
  unitNumber: number;
  unitTitle: string;
  lessonNumber: number;
};

// Derived from the courses structure: for each lesson slug, its level, unit
// number, unit title, and lesson number within the unit.
export const lessonPlacementBySlug: Record<string, LessonPlacement> = (() => {
  const placements: Record<string, LessonPlacement> = {};
  for (const course of courses) {
    course.units.forEach((unit, unitIndex) => {
      unit.lessons.forEach((lessonItem, lessonIndex) => {
        placements[lessonItem.slug] = {
          level: course.level,
          languageLabel: course.languageLabel,
          unitNumber: unitIndex + 1,
          unitTitle: unit.title,
          lessonNumber: lessonIndex + 1
        };
      });
    });
  }
  return placements;
})();

// Short label like "A1 · Unit 1 · Lesson 3" for a lesson slug.
export function lessonPlacementLabel(slug: string): string | null {
  const placement = lessonPlacementBySlug[slug];
  if (!placement) {
    return null;
  }
  return `${placement.languageLabel} · ${placement.level} · Unit ${placement.unitNumber} · Lesson ${placement.lessonNumber}`;
}

export const course = courses[0];

export const lesson = lessonCatalog[0];
