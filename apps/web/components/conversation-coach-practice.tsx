"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { CheckCircle2, ChevronDown, ChevronUp, Lightbulb, Loader2, MessageCircle, Mic, RotateCcw, Send, Sparkles, Square } from "lucide-react";
import {
  ApiRequestError,
  createConversationSession,
  resetLatestPractice,
  submitConversationAudioTurn,
  submitConversationTurn,
  type ApiPracticeSummary
} from "@/lib/conversation-api";
import {
  practiceStorageKeyForLesson,
  removeSavedPractice,
  saveSavedPractice,
  saveLatestPracticeSlug,
  type SavedPractice
} from "@/lib/practice-storage";
import { useVoiceRecorder } from "@/lib/use-voice-recorder";
import { VoiceWaveform } from "@/components/voice-waveform";
import { coachScenarioBySlug, coachTurnsByLessonSlug as generatedCoachTurnsByLessonSlug } from "@/lib/data";

type CoachTurn = {
  coach: string;
  hint: string;
  sampleAnswer: string;
  focus: string;
};

type CoachFeedback = {
  betterVersion: string;
  explanation: string;
  nextPractice: string;
  scores: {
    speaking: number;
    grammar: number;
    fluency: number;
  };
};

type ChatMessage = {
  role: "coach" | "user";
  text: string;
};

type ConversationCoachPracticeProps = {
  compact?: boolean;
  lessonSlug?: string;
  storageKey?: string;
};

const defaultTurns: CoachTurn[] = [
  {
    coach: "Hi. Good morning. How are you today?",
    hint: "Jawab sapaan, lalu beri respons singkat.",
    sampleAnswer: "Good morning. I'm good, thank you.",
    focus: "Greeting response"
  },
  {
    coach: "Nice. What is your name?",
    hint: "Sebutkan nama dengan pola: My name is ... atau I'm ...",
    sampleAnswer: "My name is Arif. Nice to meet you.",
    focus: "Self introduction"
  },
  {
    coach: "Nice to meet you. Where are you from?",
    hint: "Jawab asalmu, lalu tambahkan pertanyaan balik sederhana.",
    sampleAnswer: "I'm from Indonesia. How about you?",
    focus: "Follow-up question"
  }
];

const turnsByLessonSlug: Record<string, CoachTurn[]> = {
  "saying-hello-and-goodbye": defaultTurns,
  "saying-your-name": [
    {
      coach: "Hi, my name is Sara. What is your name?",
      hint: "Jawab dengan pola: My name is ... atau I'm ...",
      sampleAnswer: "My name is Arif. Nice to meet you.",
      focus: "Saying your name"
    },
    {
      coach: "Nice to meet you. What should I call you?",
      hint: "Gunakan pola: Please call me ...",
      sampleAnswer: "Please call me Arif.",
      focus: "Nickname"
    },
    {
      coach: "Great. Nice to meet you, Arif.",
      hint: "Balas dengan sopan: Nice to meet you too.",
      sampleAnswer: "Nice to meet you too.",
      focus: "Polite response"
    }
  ],
  "asking-someones-name": [
    {
      coach: "Hi. I am new here.",
      hint: "Tanyakan nama dengan: What's your name?",
      sampleAnswer: "Hi. What's your name?",
      focus: "Asking a name"
    },
    {
      coach: "My name is Mina.",
      hint: "Ulangi nama orang itu dalam responsmu.",
      sampleAnswer: "Nice to meet you, Mina.",
      focus: "Using the name"
    },
    {
      coach: "Nice to meet you too.",
      hint: "Tutup dengan respons singkat yang natural.",
      sampleAnswer: "See you later.",
      focus: "Closing"
    }
  ],
  "saying-where-you-are-from": [
    {
      coach: "Where are you from?",
      hint: "Jawab dengan pola: I'm from ...",
      sampleAnswer: "I'm from Indonesia.",
      focus: "Origin"
    },
    {
      coach: "Where do you live now?",
      hint: "Gunakan pola: I live in ...",
      sampleAnswer: "I live in Jakarta.",
      focus: "Current city"
    },
    {
      coach: "Nice. Ask me the same question.",
      hint: "Tanyakan balik dengan: How about you?",
      sampleAnswer: "How about you?",
      focus: "Question back"
    }
  ],
  "first-conversation-mission": [
    {
      coach: "Hi, good morning. My name is Sara.",
      hint: "Sapa balik dan sebutkan namamu.",
      sampleAnswer: "Good morning. My name is Arif.",
      focus: "Greeting and name"
    },
    {
      coach: "Nice to meet you. Where are you from?",
      hint: "Jawab asalmu lalu tanyakan balik.",
      sampleAnswer: "I'm from Indonesia. How about you?",
      focus: "Origin and follow-up"
    },
    {
      coach: "I'm from Malaysia. Nice to meet you.",
      hint: "Balas dan tutup percakapan.",
      sampleAnswer: "Nice to meet you too. See you later.",
      focus: "Closing mission"
    }
  ],
  "spelling-your-name": [
    {
      coach: "Hi. What is your name?",
      hint: "Sebutkan namamu dengan pola: My name is ...",
      sampleAnswer: "My name is Dimas.",
      focus: "Saying your name"
    },
    {
      coach: "How do you spell it?",
      hint: "Eja namamu huruf demi huruf, contoh: D-I-M-A-S.",
      sampleAnswer: "D-I-M-A-S. Dimas.",
      focus: "Spelling out loud"
    },
    {
      coach: "Thank you. Let me read it back. D-I-M-A-S.",
      hint: "Konfirmasi dengan: That's right.",
      sampleAnswer: "That's right.",
      focus: "Confirming"
    }
  ],
  "giving-phone-numbers": [
    {
      coach: "What is your phone number?",
      hint: "Sebutkan nomor telepon dalam kelompok kecil.",
      sampleAnswer: "It's zero eight one two, three four five six.",
      focus: "Giving a phone number"
    },
    {
      coach: "Let me check. Zero eight one two, three four five six?",
      hint: "Konfirmasi dengan: Yes, that's correct.",
      sampleAnswer: "Yes, that's correct.",
      focus: "Confirming a number"
    },
    {
      coach: "My number is zero eight one three, two two five five.",
      hint: "Minta diulang dengan sopan.",
      sampleAnswer: "Can you repeat that, please?",
      focus: "Asking for repetition"
    }
  ],
  "sharing-email-addresses": [
    {
      coach: "What is your email address?",
      hint: "Sebutkan email dengan at dan dot.",
      sampleAnswer: "It's ben dot rama at example dot com.",
      focus: "Giving an email address"
    },
    {
      coach: "Can you spell that, please?",
      hint: "Eja bagian nama email pelan-pelan.",
      sampleAnswer: "B-E-N dot R-A-M-A.",
      focus: "Spelling an email"
    },
    {
      coach: "Is that correct?",
      hint: "Konfirmasi dengan: Yes, that's correct.",
      sampleAnswer: "Yes, that's correct.",
      focus: "Confirming an email"
    }
  ],
  "asking-for-repetition": [
    {
      coach: "My phone number is zero eight one three, two two five five.",
      hint: "Minta lawan bicara mengulang.",
      sampleAnswer: "Sorry, can you repeat that, please?",
      focus: "Polite repetition"
    },
    {
      coach: "Sure. Zero eight one three, two two five five.",
      hint: "Cek satu detail dengan: Did you say ...?",
      sampleAnswer: "Did you say two two five five?",
      focus: "Checking a detail"
    },
    {
      coach: "Yes, that's right.",
      hint: "Tunjukkan bahwa kamu sudah paham.",
      sampleAnswer: "Got it. Thank you.",
      focus: "Showing understanding"
    }
  ],
  "contact-details-mission": [
    {
      coach: "Hi. I need your contact details.",
      hint: "Mulai dengan nama lengkapmu.",
      sampleAnswer: "Sure. My name is Dimas.",
      focus: "Sharing a name"
    },
    {
      coach: "How do you spell your name?",
      hint: "Eja nama huruf demi huruf.",
      sampleAnswer: "D-I-M-A-S.",
      focus: "Spelling a name"
    },
    {
      coach: "What is your phone number?",
      hint: "Sebutkan nomor telepon dalam kelompok kecil.",
      sampleAnswer: "It's zero eight one two, three four five six.",
      focus: "Sharing a phone number"
    },
    {
      coach: "And your email address?",
      hint: "Sebutkan email dengan at dan dot.",
      sampleAnswer: "It's dimas at example dot com.",
      focus: "Sharing an email"
    },
    {
      coach: "Is everything correct?",
      hint: "Konfirmasi semua informasi benar.",
      sampleAnswer: "Yes, everything is correct.",
      focus: "Confirming all details"
    }
  ],
  "telling-the-time": [
    {
      coach: "What time is the class?",
      hint: "Jawab dengan pola: It's at ...",
      sampleAnswer: "It's at nine o'clock.",
      focus: "Class time"
    },
    {
      coach: "In the morning?",
      hint: "Konfirmasi bagian hari.",
      sampleAnswer: "Yes, in the morning.",
      focus: "Time of day"
    },
    {
      coach: "Thank you.",
      hint: "Balas dengan sopan.",
      sampleAnswer: "You're welcome.",
      focus: "Polite reply"
    }
  ],
  "talking-about-daily-routines": [
    {
      coach: "What do you do in the morning?",
      hint: "Sebutkan kegiatan dan waktunya.",
      sampleAnswer: "I wake up at six.",
      focus: "Morning routine"
    },
    {
      coach: "What do you do after that?",
      hint: "Gunakan after that untuk kegiatan berikutnya.",
      sampleAnswer: "I study English at seven.",
      focus: "Next routine step"
    },
    {
      coach: "Do you work in the afternoon?",
      hint: "Jawab ya/tidak lalu beri waktu.",
      sampleAnswer: "Yes, I work at one.",
      focus: "Afternoon routine"
    }
  ],
  "days-and-simple-schedules": [
    {
      coach: "When is the English class?",
      hint: "Jawab dengan hari: on Monday and Wednesday.",
      sampleAnswer: "It's on Monday and Wednesday.",
      focus: "Class days"
    },
    {
      coach: "What time?",
      hint: "Jawab dengan at + time.",
      sampleAnswer: "At seven in the evening.",
      focus: "Class time"
    },
    {
      coach: "Great. See you on Monday.",
      hint: "Tutup dengan singkat.",
      sampleAnswer: "See you.",
      focus: "Schedule closing"
    }
  ],
  "asking-when-something-happens": [
    {
      coach: "When is the meeting?",
      hint: "Jawab dengan hari dan jam.",
      sampleAnswer: "It's tomorrow at ten.",
      focus: "Event time"
    },
    {
      coach: "Is it online?",
      hint: "Jawab yes/no dengan kalimat lengkap.",
      sampleAnswer: "Yes, it is online.",
      focus: "Meeting format"
    },
    {
      coach: "Tomorrow at ten. Is that right?",
      hint: "Konfirmasi dengan: Yes, that's right.",
      sampleAnswer: "Yes, that's right.",
      focus: "Confirming details"
    }
  ],
  "routine-conversation-mission": [
    {
      coach: "What time do you wake up?",
      hint: "Sebutkan jam bangun.",
      sampleAnswer: "I wake up at six.",
      focus: "Wake-up time"
    },
    {
      coach: "When do you study English?",
      hint: "Sebutkan hari dan jam.",
      sampleAnswer: "I study on Monday and Wednesday at seven.",
      focus: "Study schedule"
    },
    {
      coach: "Is the class online?",
      hint: "Jawab dengan yes/no lengkap.",
      sampleAnswer: "Yes, it is online.",
      focus: "Class format"
    },
    {
      coach: "Great. See you on Monday.",
      hint: "Tutup percakapan.",
      sampleAnswer: "See you.",
      focus: "Closing"
    }
  ],
  "saying-what-you-do": [
    {
      coach: "What do you do?",
      hint: "Jawab dengan status sederhana.",
      sampleAnswer: "I'm a student.",
      focus: "Work or study status"
    },
    {
      coach: "What do you study?",
      hint: "Sebutkan subjek yang kamu pelajari.",
      sampleAnswer: "I study design.",
      focus: "Study subject"
    },
    {
      coach: "Do you study online?",
      hint: "Jawab dengan yes/no lengkap.",
      sampleAnswer: "Yes, I study online.",
      focus: "Study format"
    }
  ],
  "asking-about-work-or-study": [
    {
      coach: "Do you work or study?",
      hint: "Jawab apakah kamu bekerja atau belajar.",
      sampleAnswer: "I study English online.",
      focus: "Work or study"
    },
    {
      coach: "What do you do there?",
      hint: "Sebutkan role sederhana.",
      sampleAnswer: "I'm an assistant.",
      focus: "Simple role"
    },
    {
      coach: "Ask me the same question.",
      hint: "Tanyakan balik dengan How about you?",
      sampleAnswer: "How about you?",
      focus: "Question back"
    }
  ],
  "talking-about-likes": [
    {
      coach: "Do you like English?",
      hint: "Jawab dengan: Yes, I like it.",
      sampleAnswer: "Yes, I like it.",
      focus: "Simple preference"
    },
    {
      coach: "What do you like?",
      hint: "Sebutkan bagian belajar yang kamu suka.",
      sampleAnswer: "I like speaking practice.",
      focus: "Learning preference"
    },
    {
      coach: "Do you like grammar?",
      hint: "Jawab jujur dengan kalimat pendek.",
      sampleAnswer: "It's okay, but speaking is my favorite.",
      focus: "Favorite part"
    }
  ],
  "saying-what-you-can-do": [
    {
      coach: "Can you speak English?",
      hint: "Sebutkan kemampuanmu dengan I can.",
      sampleAnswer: "I can speak a little.",
      focus: "Speaking ability"
    },
    {
      coach: "Can you write simple emails?",
      hint: "Jawab dengan Yes, I can.",
      sampleAnswer: "Yes, I can.",
      focus: "Writing ability"
    },
    {
      coach: "Can you join a meeting in English?",
      hint: "Gunakan Not yet kalau belum bisa.",
      sampleAnswer: "Not yet, but I can try.",
      focus: "Honest ability"
    }
  ],
  "work-study-conversation-mission": [
    {
      coach: "Do you work or study?",
      hint: "Sebutkan kerja atau studi.",
      sampleAnswer: "I study English online.",
      focus: "Work or study"
    },
    {
      coach: "What do you like about English?",
      hint: "Sebutkan bagian yang kamu suka.",
      sampleAnswer: "I like speaking practice.",
      focus: "Preference"
    },
    {
      coach: "What can you do in English?",
      hint: "Sebutkan satu kemampuan.",
      sampleAnswer: "I can introduce myself.",
      focus: "Ability"
    },
    {
      coach: "Great. Keep practicing.",
      hint: "Balas dengan singkat dan positif.",
      sampleAnswer: "Thank you. I will.",
      focus: "Closing"
    }
  ],
  "asking-where-a-place-is": [
    {
      coach: "Excuse me. What do you need?",
      hint: "Tanyakan lokasi classroom.",
      sampleAnswer: "Where is the classroom?",
      focus: "Place question"
    },
    {
      coach: "It is on the first floor.",
      hint: "Tanyakan apakah dekat office.",
      sampleAnswer: "Is it near the office?",
      focus: "Confirming location"
    },
    {
      coach: "Yes, it is next to the office.",
      hint: "Tutup dengan thank you.",
      sampleAnswer: "Thank you.",
      focus: "Polite closing"
    }
  ],
  "simple-place-words": [
    {
      coach: "Where are you going?",
      hint: "Sebutkan kamu pergi ke cafe.",
      sampleAnswer: "I'm going to the cafe.",
      focus: "Destination"
    },
    {
      coach: "Is the cafe near here?",
      hint: "Jawab dan sebutkan dekat library.",
      sampleAnswer: "Yes. It is near the library.",
      focus: "Nearby place"
    },
    {
      coach: "I am going to the library.",
      hint: "Ajak pergi bersama.",
      sampleAnswer: "Let's go together.",
      focus: "Friendly suggestion"
    }
  ],
  "understanding-simple-directions": [
    {
      coach: "Where is the meeting room?",
      hint: "Tanyakan lokasi meeting room.",
      sampleAnswer: "Where is the meeting room?",
      focus: "Room question"
    },
    {
      coach: "Go straight.",
      hint: "Ulangi arahan pertama.",
      sampleAnswer: "Okay. Go straight.",
      focus: "Repeating direction"
    },
    {
      coach: "Then turn left.",
      hint: "Konfirmasi turn left.",
      sampleAnswer: "Turn left?",
      focus: "Direction confirmation"
    },
    {
      coach: "Yes. The room is on the right.",
      hint: "Katakan kamu mengerti.",
      sampleAnswer: "Thank you. I understand.",
      focus: "Understanding"
    }
  ],
  "asking-how-to-get-there": [
    {
      coach: "Where do you want to go?",
      hint: "Tanyakan cara ke station.",
      sampleAnswer: "How do I get to the station?",
      focus: "Direction question"
    },
    {
      coach: "Go straight for two minutes.",
      hint: "Ulangi durasi arahnya.",
      sampleAnswer: "Okay. Go straight for two minutes.",
      focus: "Time direction"
    },
    {
      coach: "Then turn right at the bank.",
      hint: "Konfirmasi landmark.",
      sampleAnswer: "Turn right at the bank?",
      focus: "Landmark confirmation"
    },
    {
      coach: "Yes. The station is there.",
      hint: "Tutup dengan sopan.",
      sampleAnswer: "Thank you for your help.",
      focus: "Thanking"
    }
  ],
  "finding-a-place-mission": [
    {
      coach: "Hello. Can I help you?",
      hint: "Mulai sopan dan tanya cara ke room A.",
      sampleAnswer: "Excuse me. How do I get to room A?",
      focus: "Mission opening"
    },
    {
      coach: "Go straight and turn left.",
      hint: "Ulangi arahan lengkap.",
      sampleAnswer: "Go straight and turn left.",
      focus: "Combined directions"
    },
    {
      coach: "Room A is next to the office.",
      hint: "Konfirmasi lantai.",
      sampleAnswer: "Is it on the first floor?",
      focus: "Floor confirmation"
    },
    {
      coach: "Yes, it is.",
      hint: "Tutup dengan thank you.",
      sampleAnswer: "Great. Thank you.",
      focus: "Closing"
    }
  ],
  "ordering-a-drink": [
    {
      coach: "Hi. What would you like?",
      hint: "Pesan teh dengan sopan.",
      sampleAnswer: "Can I have a tea, please?",
      focus: "Polite order"
    },
    {
      coach: "Small or large?",
      hint: "Pilih ukuran kecil.",
      sampleAnswer: "Small, please.",
      focus: "Size choice"
    },
    {
      coach: "Anything else?",
      hint: "Katakan tidak ada lagi dengan sopan.",
      sampleAnswer: "No, thank you.",
      focus: "Finishing order"
    },
    {
      coach: "Here you go.",
      hint: "Tutup dengan thank you.",
      sampleAnswer: "Thank you.",
      focus: "Thanking"
    }
  ],
  "asking-about-prices": [
    {
      coach: "Hello. Can I help you?",
      hint: "Tanyakan harga coffee.",
      sampleAnswer: "How much is the coffee?",
      focus: "Price question"
    },
    {
      coach: "It is two dollars.",
      hint: "Konfirmasi harga.",
      sampleAnswer: "Two dollars?",
      focus: "Price confirmation"
    },
    {
      coach: "Yes, two dollars.",
      hint: "Tanyakan harga cake.",
      sampleAnswer: "How much is the cake?",
      focus: "Second price"
    },
    {
      coach: "It is three dollars.",
      hint: "Tutup dengan thank you.",
      sampleAnswer: "Okay. Thank you.",
      focus: "Closing"
    }
  ],
  "buying-a-simple-item": [
    {
      coach: "Hello. What do you need?",
      hint: "Minta beli pen ini.",
      sampleAnswer: "Can I have this pen?",
      focus: "Buying item"
    },
    {
      coach: "Yes, of course.",
      hint: "Tanyakan harganya.",
      sampleAnswer: "How much is it?",
      focus: "Price"
    },
    {
      coach: "It is one dollar.",
      hint: "Bayar dengan Here you go.",
      sampleAnswer: "Okay. Here you go.",
      focus: "Payment"
    },
    {
      coach: "Thank you. Here is your pen.",
      hint: "Tutup singkat.",
      sampleAnswer: "Thanks.",
      focus: "Closing"
    }
  ],
  "saying-what-you-want": [
    {
      coach: "What do you want?",
      hint: "Sebutkan kamu mau sandwich.",
      sampleAnswer: "I want a sandwich.",
      focus: "Want statement"
    },
    {
      coach: "Do you want tea or coffee?",
      hint: "Pilih tea dengan sopan.",
      sampleAnswer: "Tea, please.",
      focus: "Choosing option"
    },
    {
      coach: "Do you want sugar?",
      hint: "Katakan tanpa gula.",
      sampleAnswer: "No sugar, please.",
      focus: "No extra item"
    }
  ],
  "cafe-and-shop-mission": [
    {
      coach: "Hi. What would you like?",
      hint: "Pesan coffee dan sandwich.",
      sampleAnswer: "Can I have a coffee and a sandwich, please?",
      focus: "Mission order"
    },
    {
      coach: "Sure. Small or large coffee?",
      hint: "Pilih small.",
      sampleAnswer: "Small, please.",
      focus: "Size"
    },
    {
      coach: "Anything else?",
      hint: "Tanyakan total harga.",
      sampleAnswer: "How much is it?",
      focus: "Total price"
    },
    {
      coach: "It is five dollars.",
      hint: "Bayar dengan sopan.",
      sampleAnswer: "Okay. Here you go.",
      focus: "Payment"
    },
    {
      coach: "Thank you. Here is your order.",
      hint: "Tutup singkat.",
      sampleAnswer: "Thanks.",
      focus: "Closing"
    }
  ],
  "saying-you-do-not-understand": [
    {
      coach: "Please open your book.",
      hint: "Katakan kamu tidak mengerti.",
      sampleAnswer: "Sorry, I don't understand.",
      focus: "Saying confusion"
    },
    {
      coach: "That's okay. I can say it again.",
      hint: "Minta diulangi dengan sopan.",
      sampleAnswer: "Can you repeat that, please?",
      focus: "Asking repetition"
    },
    {
      coach: "Yes. Open your book.",
      hint: "Konfirmasi instruksi.",
      sampleAnswer: "Open my book?",
      focus: "Confirmation"
    },
    {
      coach: "Yes, that's right.",
      hint: "Katakan sudah paham.",
      sampleAnswer: "Thank you. I understand now.",
      focus: "Closing"
    }
  ],
  "asking-for-help": [
    {
      coach: "Hello. Do you need help?",
      hint: "Minta bantuan.",
      sampleAnswer: "Can you help me?",
      focus: "Help request"
    },
    {
      coach: "Sure. What is the problem?",
      hint: "Jelaskan masalah file.",
      sampleAnswer: "I can't open this file.",
      focus: "Problem statement"
    },
    {
      coach: "Okay. Click this button.",
      hint: "Konfirmasi tombol.",
      sampleAnswer: "This button?",
      focus: "Instruction check"
    },
    {
      coach: "Yes. Try again.",
      hint: "Katakan berhasil dan terima kasih.",
      sampleAnswer: "It works. Thank you.",
      focus: "Result"
    }
  ],
  "making-simple-requests": [
    {
      coach: "What do you need?",
      hint: "Minta link dengan sopan.",
      sampleAnswer: "Can you send me the link, please?",
      focus: "Polite request"
    },
    {
      coach: "Yes, of course.",
      hint: "Ucapkan terima kasih.",
      sampleAnswer: "Thank you.",
      focus: "Thanking"
    },
    {
      coach: "Can you wait a minute?",
      hint: "Terima request untuk menunggu.",
      sampleAnswer: "Sure. No problem.",
      focus: "Accepting request"
    },
    {
      coach: "Here is the link.",
      hint: "Tutup dengan thanks.",
      sampleAnswer: "Great. Thanks.",
      focus: "Closing"
    }
  ],
  "apologizing-and-thanking": [
    {
      coach: "Hello, Ben. You are late today.",
      hint: "Minta maaf karena terlambat.",
      sampleAnswer: "Sorry I'm late.",
      focus: "Apology"
    },
    {
      coach: "That's okay. What happened?",
      hint: "Berikan alasan singkat.",
      sampleAnswer: "My internet was slow.",
      focus: "Reason"
    },
    {
      coach: "No problem. Please join the class.",
      hint: "Ucapkan terima kasih sudah menunggu.",
      sampleAnswer: "Thank you for waiting.",
      focus: "Thanking"
    },
    {
      coach: "You're welcome.",
      hint: "Katakan kamu siap sekarang.",
      sampleAnswer: "I am ready now.",
      focus: "Ready"
    }
  ],
  "help-and-problem-mission": [
    {
      coach: "Hi. Is everything okay?",
      hint: "Katakan kamu tidak mengerti.",
      sampleAnswer: "Sorry, I don't understand.",
      focus: "Mission opening"
    },
    {
      coach: "That's okay. What is the problem?",
      hint: "Jelaskan masalah file.",
      sampleAnswer: "I can't open this file.",
      focus: "Problem"
    },
    {
      coach: "Can you send me a screenshot?",
      hint: "Terima dan minta tunggu sebentar.",
      sampleAnswer: "Sure. Can you wait a minute?",
      focus: "Request"
    },
    {
      coach: "No problem.",
      hint: "Kirim screenshot.",
      sampleAnswer: "Here is the screenshot.",
      focus: "Sending info"
    },
    {
      coach: "Good. Click this button.",
      hint: "Katakan berhasil dan terima kasih.",
      sampleAnswer: "It works. Thank you for your help.",
      focus: "Closing"
    }
  ],
  "review-introductions": [
    {
      coach: "Hi, good morning. My name is Sara.",
      hint: "Sapa balik dan sebutkan namamu.",
      sampleAnswer: "Good morning. My name is Dimas.",
      focus: "Name review"
    },
    {
      coach: "Nice to meet you. Where are you from?",
      hint: "Jawab asalmu dengan I'm from ...",
      sampleAnswer: "I'm from Indonesia.",
      focus: "Origin review"
    },
    {
      coach: "I live in Jakarta now.",
      hint: "Tanyakan balik dengan How about you?",
      sampleAnswer: "How about you?",
      focus: "Question back"
    },
    {
      coach: "I'm from Malaysia.",
      hint: "Tutup percakapan dengan sopan.",
      sampleAnswer: "Oh, nice. See you in class.",
      focus: "Closing"
    }
  ],
  "review-routines-and-time": [
    {
      coach: "What do you do in the morning?",
      hint: "Sebutkan satu rutinitas dan jam.",
      sampleAnswer: "I wake up at six.",
      focus: "Routine time"
    },
    {
      coach: "Nice. Do you study English after that?",
      hint: "Jawab dengan Yes, lalu sebutkan jam belajar.",
      sampleAnswer: "Yes, I study English at seven.",
      focus: "Study routine"
    },
    {
      coach: "Good. We have speaking class this week.",
      hint: "Tanyakan kapan kelas speaking.",
      sampleAnswer: "When is our speaking class?",
      focus: "Class schedule question"
    },
    {
      coach: "It is on Tuesday at eight.",
      hint: "Tutup dengan See you then.",
      sampleAnswer: "Great. See you then.",
      focus: "Closing"
    }
  ],
  "review-places-and-shopping": [
    {
      coach: "Excuse me. Can I help you?",
      hint: "Tanyakan lokasi cafe.",
      sampleAnswer: "Where is the cafe?",
      focus: "Place question"
    },
    {
      coach: "Go straight and turn right.",
      hint: "Konfirmasi lokasinya dekat library.",
      sampleAnswer: "Is it next to the library?",
      focus: "Confirm place"
    },
    {
      coach: "Yes, it is. You are at the cafe now.",
      hint: "Pesan satu teh dengan sopan.",
      sampleAnswer: "I would like one tea, please.",
      focus: "Order"
    },
    {
      coach: "Sure. It is two dollars.",
      hint: "Bayar dan ucapkan terima kasih.",
      sampleAnswer: "Here you go. Thank you.",
      focus: "Payment"
    }
  ],
  "final-test-practice": [
    {
      coach: "Hello. What is your name?",
      hint: "Jawab dengan nama lengkap atau nama panggilan.",
      sampleAnswer: "My name is Alya.",
      focus: "Test identity"
    },
    {
      coach: "Where are you from?",
      hint: "Jawab asal dengan I'm from ...",
      sampleAnswer: "I'm from Indonesia.",
      focus: "Test origin"
    },
    {
      coach: "What do you do every morning?",
      hint: "Sebutkan rutinitas belajar dan jam.",
      sampleAnswer: "I study English at seven.",
      focus: "Test routine"
    },
    {
      coach: "When is your class?",
      hint: "Kalau perlu, minta pengulangan dulu.",
      sampleAnswer: "Sorry, can you repeat that, please?",
      focus: "Clarification"
    },
    {
      coach: "Sure. When is your class?",
      hint: "Jawab hari dan jam.",
      sampleAnswer: "It is on Tuesday at eight.",
      focus: "Schedule answer"
    }
  ],
  "a1-final-conversation": [
    {
      coach: "Hi, good morning. What is your name?",
      hint: "Perkenalkan diri dengan kalimat lengkap.",
      sampleAnswer: "Good morning. My name is Mina.",
      focus: "Final opening"
    },
    {
      coach: "Nice to meet you. Where are you from?",
      hint: "Jawab asal dan tanyakan balik.",
      sampleAnswer: "I'm from Indonesia. How about you?",
      focus: "Origin and follow-up"
    },
    {
      coach: "I'm from Malaysia. What do you do every morning?",
      hint: "Sebutkan rutinitas dan waktu.",
      sampleAnswer: "I study English at seven.",
      focus: "Routine"
    },
    {
      coach: "Great. The cafe is open now.",
      hint: "Tanyakan lokasi cafe.",
      sampleAnswer: "Where is the cafe?",
      focus: "Place"
    },
    {
      coach: "Go straight and turn left.",
      hint: "Pesan satu item dengan sopan.",
      sampleAnswer: "Thank you. I would like one tea, please.",
      focus: "Order"
    },
    {
      coach: "Sure. It is two dollars.",
      hint: "Minta ulang harga jika perlu.",
      sampleAnswer: "Sorry, can you repeat that, please?",
      focus: "Clarification"
    },
    {
      coach: "Two dollars.",
      hint: "Bayar dan tutup dengan terima kasih.",
      sampleAnswer: "Here you go. Thank you for your help.",
      focus: "Final closing"
    }
  ]
};

const mergedTurnsByLessonSlug: Record<string, CoachTurn[]> = {
  ...turnsByLessonSlug,
  ...generatedCoachTurnsByLessonSlug
};

const maxRecordingSeconds = 30;

function clampScore(score: number) {
  return Math.max(55, Math.min(score, 95));
}

function looksLikeRefusal(normalized: string) {
  const cleaned = normalized.replace(/[^a-z\s]/g, " ").trim();
  if (!cleaned) {
    return true;
  }
  const tokens = cleaned.split(/\s+/).filter(Boolean);
  if (!tokens.length) {
    return true;
  }
  if (tokens.length <= 2 && tokens.every((token) => ["no", "nope", "nah"].includes(token))) {
    return true;
  }
  if (tokens.length <= 2 && tokens[0] === "sorry") {
    return true;
  }
  return false;
}

function matchesSamplePattern(answer: string, sampleAnswer: string) {
  const stopwords = new Set(["the", "that", "this", "with", "your", "please", "thank", "you"]);
  const answerTokens = new Set(answer.match(/[a-z0-9]+/g) ?? []);
  const sampleTokens = (sampleAnswer.toLowerCase().match(/[a-z0-9]+/g) ?? []).filter(
    (token) => token.length > 2 && !stopwords.has(token)
  );

  if (!sampleTokens.length) {
    return false;
  }

  const matched = sampleTokens.filter((token) => answerTokens.has(token)).length;
  return matched >= Math.min(2, sampleTokens.length);
}

function evaluateAnswer(answer: string, turnIndex: number, activeTurns: CoachTurn[]): CoachFeedback {
  const text = answer.trim();
  const normalized = text.toLowerCase();
  const hasGreeting = /\b(hi|hello|morning|good morning)\b/.test(normalized);
  const hasThanks = /\b(thank|thanks)\b/.test(normalized);
  const nameMatch = normalized.match(/\b(my name is|i am|i'm)\s+([a-z]+)/);
  const hasName = Boolean(nameMatch && !["good", "fine", "ok", "okay", "happy", "sad"].includes(nameMatch[2]));
  const hasOrigin = /\b(from|indonesia|jakarta|bandung|surabaya|malaysia|singapore)\b/.test(normalized);
  const hasQuestion = normalized.includes("?");
  const enoughWords = text.split(/\s+/).filter(Boolean).length >= 5;

  const target = activeTurns[turnIndex] ?? activeTurns[0];
  const matchedSamplePattern = matchesSamplePattern(normalized, target.sampleAnswer);
  const offTrack =
    looksLikeRefusal(normalized) ||
    (!matchedSamplePattern &&
      !(turnIndex === 0 && (hasGreeting || hasThanks)) &&
      !(turnIndex === 1 && hasName) &&
      !(turnIndex === 2 && hasOrigin));

  let speaking = offTrack ? 58 : 64;
  let grammar = offTrack ? 56 : 66;
  let fluency = offTrack ? 55 : 64;

  if (enoughWords) {
    speaking += 8;
    fluency += 8;
  }

  if (turnIndex === 0 && (hasGreeting || hasThanks)) {
    speaking += 10;
    grammar += 7;
  }

  if (turnIndex === 1 && hasName) {
    speaking += 12;
    grammar += 8;
  }

  if (turnIndex === 2 && hasOrigin) {
    speaking += 10;
    grammar += 7;
  }

  if (hasQuestion) {
    fluency += 8;
    speaking += 5;
  }

  if (matchedSamplePattern) {
    speaking += 10;
    grammar += 6;
    fluency += 4;
  }

  const matchedExpected =
    matchedSamplePattern ||
    (turnIndex === 0 && (hasGreeting || hasThanks)) ||
    (turnIndex === 1 && hasName) ||
    (turnIndex === 2 && hasOrigin);

  const explanation = offTrack
    ? `Jawabanmu belum menjawab pertanyaan ini. Coba jawab seperti: ${target.sampleAnswer}`
    : matchedExpected
      ? `Jawabanmu sudah masuk konteks. Latih pola ini agar lebih natural: ${target.sampleAnswer}`
      : `Jawabanmu belum memakai pola yang diharapkan untuk "${target.focus}". Coba ikuti contoh ini: ${target.sampleAnswer}`;

  return {
    betterVersion: target.sampleAnswer,
    explanation,
    nextPractice:
      turnIndex >= activeTurns.length - 1
        ? "Ulangi roleplay dari awal tanpa melihat contoh jawaban."
        : `Next: ${activeTurns[turnIndex + 1].focus}`,
    scores: {
      speaking: clampScore(speaking),
      grammar: clampScore(grammar),
      fluency: clampScore(fluency)
    }
  };
}

function averageScore(feedback: CoachFeedback | null) {
  if (!feedback) {
    return 0;
  }

  return Math.round((feedback.scores.speaking + feedback.scores.grammar + feedback.scores.fluency) / 3);
}

function strengthMessage(feedback: CoachFeedback) {
  const { speaking, grammar, fluency } = feedback.scores;
  if (speaking >= grammar && speaking >= fluency) {
    return "Pelafalanmu sudah cukup jelas. Pertahankan ritmenya.";
  }
  if (grammar >= speaking && grammar >= fluency) {
    return "Struktur kalimatmu sudah rapi. Ini bikin jawabanmu mudah dipahami.";
  }
  return "Jawabanmu terasa mengalir. Bagus, itu membantu percakapan tetap natural.";
}

function improvementTitle(feedback: CoachFeedback) {
  const { speaking, grammar, fluency } = feedback.scores;
  if (speaking <= grammar && speaking <= fluency) {
    return "Fokus: pelafalan";
  }
  if (grammar <= speaking && grammar <= fluency) {
    return "Fokus: struktur kalimat";
  }
  return "Fokus: kelancaran";
}

function improvementMessage(feedback: CoachFeedback, turn: CoachTurn) {
  const { speaking, grammar, fluency } = feedback.scores;
  if (speaking <= grammar && speaking <= fluency) {
    return `Ulangi contoh ini pelan-pelan, lalu perjelas kata kunci: ${turn.sampleAnswer}`;
  }
  if (grammar <= speaking && grammar <= fluency) {
    return `Ikuti susunan kata pada contoh ini, lalu ulangi 1x: ${turn.sampleAnswer}`;
  }
  return `Coba ucapkan sekali tanpa berhenti panjang, lalu lanjut: ${turn.sampleAnswer}`;
}

function formatNextPractice(nextPractice: string) {
  const trimmed = nextPractice.trim();
  if (!trimmed) {
    return "";
  }
  if (trimmed.toLowerCase().startsWith("next:")) {
    return `Lanjut: ${trimmed.slice(5).trim()}`;
  }
  return trimmed;
}

function uniqueExamples(...examples: string[]) {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const raw of examples) {
    const value = raw.trim();
    if (!value) {
      continue;
    }
    const key = value.toLowerCase();
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    out.push(value);
    if (out.length >= 2) {
      break;
    }
  }
  return out;
}

function isOffTrackExplanation(explanation: string) {
  const normalized = explanation.toLowerCase();
  return normalized.includes("belum menjawab") || normalized.includes("belum memakai pola") || normalized.includes("belum sesuai");
}


function recordingSubmitErrorMessage(error: unknown) {
  if (error instanceof ApiRequestError) {
    if (error.status === 503) {
      return "STT belum aktif. Pastikan kunci API STT sudah terbaca di server.";
    }
    if (error.status === 504) {
      return "Transkripsi terlalu lama. Coba rekam jawaban yang lebih pendek.";
    }
    if (error.status === 422) {
      return "Audio belum bisa ditranskrip. Coba rekam ulang dengan suara lebih jelas.";
    }
  }
  return "Transkripsi belum berhasil. Coba rekam ulang.";
}

export function ConversationCoachPractice({
  compact = false,
  lessonSlug = "saying-hello-and-goodbye",
  storageKey
}: ConversationCoachPracticeProps) {
  const activeTurns = mergedTurnsByLessonSlug[lessonSlug] ?? defaultTurns;
  const activeScenario = coachScenarioBySlug[lessonSlug];
  const effectiveStorageKey = storageKey ?? practiceStorageKeyForLesson(lessonSlug);
  const [messages, setMessages] = useState<ChatMessage[]>([{ role: "coach", text: activeTurns[0].coach }]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [turnIndex, setTurnIndex] = useState(0);
  const [feedbackTurnIndex, setFeedbackTurnIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState<CoachFeedback | null>(null);
  const [completedTurns, setCompletedTurns] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [syncStatus, setSyncStatus] = useState<"connecting" | "synced" | "local">("connecting");
  const [billingNotice, setBillingNotice] = useState("");
  const [recordingError, setRecordingError] = useState("");
  const [isFeedbackOpen, setIsFeedbackOpen] = useState(false);
  const [isScoreOpen, setIsScoreOpen] = useState(false);

  const recorder = useVoiceRecorder({
    onResult: (blob) => submitRecordedAudio(blob),
    onError: (message) => setRecordingError(message),
    maxSeconds: maxRecordingSeconds,
    autoStopOnSilence: true
  });

  const completed = completedTurns >= activeTurns.length;
  const activeTurn = activeTurns[Math.min(turnIndex, activeTurns.length - 1)];
  const feedbackTurn = activeTurns[Math.min(feedbackTurnIndex, activeTurns.length - 1)];
  const progressPercent = Math.round((completedTurns / activeTurns.length) * 100);
  const score = averageScore(feedback);
  const isRecording = recorder.status === "recording";
  const isProcessingRecording = recorder.status === "processing";

  const savedPractice: SavedPractice = useMemo(
    () => ({
      sessionId: sessionId ?? undefined,
      completedTurns,
      totalTurns: activeTurns.length,
      completed,
      lastScore: score,
      updatedAt: new Date().toISOString()
    }),
    [activeTurns.length, completed, completedTurns, score, sessionId]
  );

  useEffect(() => {
    if (completedTurns === 0) {
      return;
    }

    saveSavedPractice(savedPractice, effectiveStorageKey);
    saveLatestPracticeSlug(lessonSlug);
  }, [completedTurns, effectiveStorageKey, savedPractice]);

  function applySummary(summary: ApiPracticeSummary) {
    setCompletedTurns(summary.completedTurns);
    setTurnIndex(Math.min(summary.completedTurns, activeTurns.length - 1));
    saveSavedPractice(
      {
        sessionId: summary.sessionId,
        completedTurns: summary.completedTurns,
        totalTurns: summary.totalTurns,
        completed: summary.completed,
        lastScore: summary.lastScore,
        updatedAt: summary.updatedAt
      },
      effectiveStorageKey
    );
    saveLatestPracticeSlug(lessonSlug);
  }

  function applyTurnResult(input: {
    userText: string;
    nextCompletedTurns: number;
    nextTurnIndex: number;
    nextCoachReply: string | null;
    nextFeedback: CoachFeedback;
  }) {
    setMessages((currentMessages) => {
      const nextMessages: ChatMessage[] = [
        ...currentMessages,
        { role: "user", text: input.userText }
      ];

      if (input.nextCompletedTurns < activeTurns.length && input.nextCoachReply) {
        nextMessages.push({ role: "coach", text: input.nextCoachReply });
      }

      return nextMessages;
    });
    setFeedback(input.nextFeedback);
    setIsFeedbackOpen(true);
    setIsScoreOpen(false);
    setCompletedTurns(input.nextCompletedTurns);
    setTurnIndex(input.nextTurnIndex);
    setFeedbackTurnIndex(Math.min(Math.max(input.nextCompletedTurns - 1, 0), activeTurns.length - 1));
  }

  function startRecording() {
    if (completed || isSubmitting || isRecording || isProcessingRecording) {
      return;
    }
    setRecordingError("");
    setBillingNotice("");
    void recorder.start();
  }

  function stopRecording() {
    recorder.stop();
  }

  async function submitRecordedAudio(audioBlob: Blob) {
    if (!audioBlob.size) {
      setRecordingError("Audio belum terekam. Coba ulangi.");
      return;
    }

    setIsSubmitting(true);
    setBillingNotice("");
    setRecordingError("");

    let activeSessionId = sessionId;

    try {
      if (!activeSessionId) {
        const session = await createConversationSession(lessonSlug, coachScenarioBySlug[lessonSlug]);
        activeSessionId = session.sessionId;
        setSessionId(session.sessionId);
      }

      const result = await submitConversationAudioTurn(activeSessionId, audioBlob);
      const nextCompletedTurns = result.summary.completedTurns;
      const nextTurnIndex = Math.min(result.summary.completedTurns, activeTurns.length - 1);
      setSyncStatus("synced");
      applySummary(result.summary);
      applyTurnResult({
        userText: result.userTranscript,
        nextCompletedTurns,
        nextTurnIndex,
        nextCoachReply: result.coachReply,
        nextFeedback: result.feedback
      });
    } catch (error) {
      if (error instanceof ApiRequestError && error.status === 402) {
        setBillingNotice("Kuota Conversation Coach habis. Top-up atau upgrade untuk melanjutkan latihan tersinkron.");
      } else {
        setRecordingError(recordingSubmitErrorMessage(error));
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const userAnswer = answer.trim();
    if (!userAnswer || completed || isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    setBillingNotice("");

    let activeSessionId = sessionId;
    let newFeedback = evaluateAnswer(userAnswer, turnIndex, activeTurns);
    let nextCompletedTurns = Math.min(completedTurns + 1, activeTurns.length);
    let nextTurnIndex = Math.min(turnIndex + 1, activeTurns.length - 1);
    let nextCoachReply: string | null = nextCompletedTurns < activeTurns.length ? activeTurns[nextTurnIndex].coach : null;
    let submittedTranscript = userAnswer;

    try {
      if (!activeSessionId) {
        const session = await createConversationSession(lessonSlug, coachScenarioBySlug[lessonSlug]);
        activeSessionId = session.sessionId;
        setSessionId(session.sessionId);
      }

      const result = await submitConversationTurn(activeSessionId, userAnswer);
      nextCompletedTurns = result.summary.completedTurns;
      nextTurnIndex = Math.min(result.summary.completedTurns, activeTurns.length - 1);
      nextCoachReply = result.coachReply;
      newFeedback = result.feedback;
      submittedTranscript = result.userTranscript || userAnswer;
      setSyncStatus("synced");
      applySummary(result.summary);
    } catch (error) {
      if (error instanceof ApiRequestError && error.status === 402) {
        setBillingNotice("Kuota Conversation Coach habis. Top-up atau upgrade untuk melanjutkan latihan tersinkron.");
        setIsSubmitting(false);
        return;
      }
      setSyncStatus("local");
    }

    applyTurnResult({
      userText: submittedTranscript,
      nextCompletedTurns,
      nextTurnIndex,
      nextCoachReply,
      nextFeedback: newFeedback
    });
    setAnswer("");
    setIsSubmitting(false);
  }

  function handleUseSample() {
    if (!completed) {
      setAnswer(activeTurn.sampleAnswer);
    }
  }

  async function handleReset() {
    if (isRecording) {
      recorder.cancel();
    }
    setMessages([{ role: "coach", text: activeTurns[0].coach }]);
    setSessionId(null);
    setTurnIndex(0);
    setAnswer("");
    setFeedback(null);
    setCompletedTurns(0);
    setRecordingError("");
    removeSavedPractice(effectiveStorageKey);

    try {
      await resetLatestPractice(lessonSlug);
      const session = await createConversationSession(lessonSlug, coachScenarioBySlug[lessonSlug]);
      setSessionId(session.sessionId);
      setMessages([{ role: "coach", text: session.firstCoachMessage }]);
      setSyncStatus("synced");
    } catch {
      setSyncStatus("local");
    }
  }

  return (
    <div className={compact ? "grid gap-4 lg:grid-cols-[0.65fr_0.35fr]" : "grid gap-5 lg:grid-cols-[0.72fr_0.28fr]"}>
      <section className="rounded-lg border border-ink/10 bg-white shadow-sm">
        <div className="border-b border-ink/10 p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">Conversation Coach</p>
              <h2 className={compact ? "mt-2 text-2xl font-semibold" : "mt-2 text-3xl font-semibold"}>
                Roleplay Terarah
              </h2>
              <p className="mt-3 leading-7 text-ink/70">
                {activeScenario ? `Skenario: ${activeScenario.label}. ${activeScenario.description}` : "Skenario: latihan roleplay singkat."}
              </p>
              <p className="mt-2 text-xs font-semibold uppercase text-ink/45">
                {syncStatus === "synced"
                  ? "Sesi tersinkron"
                  : syncStatus === "local"
                    ? "Mode lokal"
                    : "Siap mulai"}
              </p>
              {billingNotice ? (
                <Link
                  href="/billing"
                  className="focus-ring mt-3 inline-flex rounded-lg bg-[#fde7df] px-3 py-2 text-xs font-semibold text-ink hover:bg-mint"
                >
                  {billingNotice}
                </Link>
              ) : null}
            </div>
            <div className="min-w-32 rounded-lg bg-mint px-4 py-3 text-sm">
              <p className="font-semibold">{progressPercent}% selesai</p>
              <div className="mt-2 h-2 rounded-lg bg-white">
                <div className="h-2 rounded-lg bg-leaf" style={{ width: `${progressPercent}%` }} />
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-4 p-5">
          {messages.map((message, index) => (
            <div key={`${message.role}-${index}`} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[86%] rounded-lg p-4 text-sm leading-6 ${
                  message.role === "user" ? "bg-leaf text-white" : "bg-paper text-ink"
                }`}
              >
                {message.text}
              </div>
            </div>
          ))}

          {completed ? (
            <div className="rounded-lg border border-leaf/30 bg-mint p-4 text-sm leading-6">
              <div className="flex items-center gap-2 font-semibold">
                <CheckCircle2 className="h-4 w-4 text-leaf" aria-hidden="true" />
                Roleplay selesai
              </div>
              <p className="mt-2 text-ink/70">
                Kamu sudah menyelesaikan semua turn roleplay. Lanjut cek progress untuk melihat rekomendasi berikutnya.
              </p>
            </div>
          ) : (
            <div className="rounded-lg bg-[#fff2dc] p-4 text-sm leading-6">
              <div className="flex items-start gap-2">
                <Lightbulb className="mt-0.5 h-4 w-4 shrink-0 text-coral" aria-hidden="true" />
                <div>
                  <p className="font-semibold">{activeTurn.focus}</p>
                  <p className="text-ink/70">{activeTurn.hint}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="border-t border-ink/10 p-5">
          <textarea
            value={answer}
            onChange={(event) => setAnswer(event.target.value)}
            disabled={completed || isSubmitting || isRecording || isProcessingRecording}
            rows={compact ? 2 : 3}
            className="focus-ring min-h-24 w-full resize-none rounded-lg border border-ink/10 bg-paper px-4 py-3 text-sm leading-6 text-ink placeholder:text-ink/40 disabled:opacity-60"
            placeholder={completed ? "Roleplay selesai" : "Tulis jawabanmu dalam bahasa Inggris..."}
          />
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={isRecording ? stopRecording : startRecording}
              disabled={completed || isSubmitting || isProcessingRecording}
              className={`focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg px-4 py-3 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-50 ${
                isRecording ? "bg-coral text-white hover:bg-ink" : "border border-ink/15 hover:bg-mint"
              }`}
            >
              {isRecording ? (
                <Square className="h-4 w-4" aria-hidden="true" />
              ) : (
                <Mic className="h-4 w-4" aria-hidden="true" />
              )}
              {isProcessingRecording ? "Memproses" : isRecording ? "Berhenti" : "Rekam"}
            </button>
            {isRecording ? <VoiceWaveform level={recorder.micLevel} label="" /> : null}
            <button
              type="button"
              onClick={handleUseSample}
              disabled={completed || isSubmitting || isRecording || isProcessingRecording}
              className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border border-ink/15 px-4 py-3 text-sm font-semibold hover:bg-mint disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Sparkles className="h-4 w-4" aria-hidden="true" />
              Pakai Contoh
            </button>
            <button
              type="submit"
              disabled={!answer.trim() || completed || isSubmitting || isRecording || isProcessingRecording}
              className="focus-ring ml-auto inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-leaf px-5 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:bg-ink/30"
              aria-busy={isSubmitting}
            >
              {isSubmitting ? (
                <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
              ) : (
                <Send className="h-4 w-4" aria-hidden="true" />
              )}
              {isSubmitting ? "Mengirim..." : "Kirim"}
            </button>
          </div>
          {isSubmitting ? <p className="mt-2 text-xs text-ink/60">Sedang memproses jawaban...</p> : null}
          {recordingError ? (
            <p className="mt-3 rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{recordingError}</p>
          ) : null}
        </form>
      </section>

      <aside className="space-y-4">
        <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-2">
            <MessageCircle className="h-5 w-5 text-leaf" aria-hidden="true" />
            <h2 className="font-semibold">Feedback Percakapan</h2>
          </div>

          {feedback ? (
            <>
              <button
                type="button"
                onClick={() => setIsFeedbackOpen((current) => !current)}
                className="focus-ring mt-4 flex w-full items-center justify-between gap-3 rounded-lg bg-paper px-4 py-3 text-left"
              >
                <span className="text-sm font-semibold">{isFeedbackOpen ? "Sembunyikan feedback singkat" : "Lihat feedback singkat"}</span>
                {isFeedbackOpen ? (
                  <ChevronUp className="h-4 w-4 text-ink/60" aria-hidden="true" />
                ) : (
                  <ChevronDown className="h-4 w-4 text-ink/60" aria-hidden="true" />
                )}
              </button>

              {isFeedbackOpen ? (
                <div className="mt-4 space-y-4 text-sm leading-6">
                  <div>
                    <p className="font-semibold">Ringkasan</p>
                    <p className="mt-1 text-ink/70">{feedback.explanation}</p>
                  </div>
                  <div>
                    <p className="font-semibold">
                      {isOffTrackExplanation(feedback.explanation) ? "Fokus: jawab sesuai pertanyaan" : improvementTitle(feedback)}
                    </p>
                    <p className="mt-1 text-ink/70">
                      {isOffTrackExplanation(feedback.explanation)
                        ? `Coba jawab seperti ini: ${feedbackTurn.sampleAnswer}`
                        : improvementMessage(feedback, feedbackTurn)}
                    </p>
                    {formatNextPractice(feedback.nextPractice) ? (
                      <p className="mt-2 text-ink/60">{formatNextPractice(feedback.nextPractice)}</p>
                    ) : null}
                  </div>
                  <div>
                    <p className="font-semibold">Contoh jawaban natural (1–2)</p>
                    <div className="mt-2 space-y-2">
                      {uniqueExamples(feedbackTurn.sampleAnswer, feedback.betterVersion).map((example) => (
                        <p key={example} className="rounded-lg bg-mint px-3 py-2 text-ink/75">
                          {example}
                        </p>
                      ))}
                    </div>
                  </div>
                </div>
              ) : null}

              <button
                type="button"
                onClick={() => setIsScoreOpen((current) => !current)}
                className="focus-ring mt-4 inline-flex items-center gap-2 rounded-lg border border-ink/15 px-3 py-2 text-sm font-semibold hover:bg-mint"
              >
                {isScoreOpen ? "Sembunyikan skor" : "Lihat skor"}
              </button>

              {isScoreOpen ? (
                <div className="mt-4 grid grid-cols-3 gap-2 text-center text-sm">
                  {[
                    ["Speaking", feedback?.scores.speaking],
                    ["Grammar", feedback?.scores.grammar],
                    ["Fluency", feedback?.scores.fluency]
                  ].map(([label, value]) => (
                    <div key={label} className="rounded-lg bg-paper p-3">
                      <p className="text-lg font-semibold">{value ?? "–"}</p>
                      <p className="text-xs text-ink/60">{label}</p>
                    </div>
                  ))}
                </div>
              ) : null}
            </>
          ) : (
            <p className="mt-4 text-sm leading-6 text-ink/60">
              Submit jawaban pertama untuk melihat versi yang lebih natural, penjelasan, dan skor.
            </p>
          )}
        </section>

        <section className="rounded-lg bg-ink p-5 text-white">
          <p className="text-sm text-white/70">Status latihan</p>
          <p className="mt-2 text-3xl font-semibold">{completedTurns}/{activeTurns.length}</p>
          <p className="mt-2 text-sm leading-6 text-white/70">
            Selesaikan semua turn untuk membuka rekomendasi progress berikutnya.
          </p>
          <div className="mt-5 grid gap-2">
            <Link
              href="/progress"
              className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-lg bg-white px-4 py-3 text-sm font-semibold text-ink hover:bg-mint"
            >
              <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
              Lihat Progress
            </Link>
            <button
              type="button"
              onClick={handleReset}
              className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-lg border border-white/20 px-4 py-3 text-sm font-semibold text-white hover:bg-white/10"
            >
              <RotateCcw className="h-4 w-4" aria-hidden="true" />
              Ulangi Latihan
            </button>
          </div>
        </section>
      </aside>
    </div>
  );
}
