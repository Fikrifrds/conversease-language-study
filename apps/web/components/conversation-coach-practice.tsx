"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { CheckCircle2, Lightbulb, MessageCircle, RotateCcw, Send, Sparkles } from "lucide-react";
import {
  ApiRequestError,
  createConversationSession,
  resetLatestPractice,
  submitConversationTurn,
  type ApiPracticeSummary
} from "@/lib/conversation-api";
import {
  defaultPracticeStorageKey,
  removeSavedPractice,
  saveSavedPractice,
  type SavedPractice
} from "@/lib/practice-storage";

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
    sampleAnswer: "My name is Fikri. Nice to meet you.",
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
      sampleAnswer: "My name is Fikri. Nice to meet you.",
      focus: "Saying your name"
    },
    {
      coach: "Nice to meet you. What should I call you?",
      hint: "Gunakan pola: Please call me ...",
      sampleAnswer: "Please call me Fikri.",
      focus: "Nickname"
    },
    {
      coach: "Great. Nice to meet you, Fikri.",
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
      sampleAnswer: "Good morning. My name is Fikri.",
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
  ]
};

function clampScore(score: number) {
  return Math.max(55, Math.min(score, 95));
}

function evaluateAnswer(answer: string, turnIndex: number, activeTurns: CoachTurn[]): CoachFeedback {
  const text = answer.trim();
  const normalized = text.toLowerCase();
  const hasGreeting = /\b(hi|hello|morning|good morning)\b/.test(normalized);
  const hasThanks = /\b(thank|thanks)\b/.test(normalized);
  const hasName = /\b(my name is|i'm|i am)\b/.test(normalized);
  const hasOrigin = /\b(from|indonesia|jakarta|bandung|surabaya|malaysia|singapore)\b/.test(normalized);
  const hasQuestion = normalized.includes("?");
  const enoughWords = text.split(/\s+/).filter(Boolean).length >= 5;

  const target = activeTurns[turnIndex] ?? activeTurns[0];
  let speaking = 64;
  let grammar = 66;
  let fluency = 64;

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

  return {
    betterVersion: target.sampleAnswer,
    explanation: `Jawabanmu sudah masuk konteks. Latih pola ini agar lebih natural: ${target.sampleAnswer}`,
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

export function ConversationCoachPractice({
  compact = false,
  lessonSlug = "saying-hello-and-goodbye",
  storageKey
}: ConversationCoachPracticeProps) {
  const activeTurns = turnsByLessonSlug[lessonSlug] ?? defaultTurns;
  const effectiveStorageKey = storageKey ?? `${defaultPracticeStorageKey}.${lessonSlug}`;
  const [messages, setMessages] = useState<ChatMessage[]>([{ role: "coach", text: activeTurns[0].coach }]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [turnIndex, setTurnIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState<CoachFeedback | null>(null);
  const [completedTurns, setCompletedTurns] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [syncStatus, setSyncStatus] = useState<"connecting" | "synced" | "local">("connecting");
  const [billingNotice, setBillingNotice] = useState("");

  const completed = completedTurns >= activeTurns.length;
  const activeTurn = activeTurns[Math.min(turnIndex, activeTurns.length - 1)];
  const progressPercent = Math.round((completedTurns / activeTurns.length) * 100);
  const score = averageScore(feedback);

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

    try {
      if (!activeSessionId) {
        const session = await createConversationSession(lessonSlug);
        activeSessionId = session.sessionId;
        setSessionId(session.sessionId);
      }

      const result = await submitConversationTurn(activeSessionId, userAnswer);
      nextCompletedTurns = result.summary.completedTurns;
      nextTurnIndex = Math.min(result.summary.completedTurns, activeTurns.length - 1);
      nextCoachReply = result.coachReply;
      newFeedback = result.feedback;
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

    const nextMessages: ChatMessage[] = [...messages, { role: "user", text: userAnswer }];

    if (nextCompletedTurns < activeTurns.length && nextCoachReply) {
      nextMessages.push({ role: "coach", text: nextCoachReply });
    }

    setMessages(nextMessages);
    setFeedback(newFeedback);
    setCompletedTurns(nextCompletedTurns);
    setTurnIndex(nextTurnIndex);
    setAnswer("");
    setIsSubmitting(false);
  }

  function handleUseSample() {
    if (!completed) {
      setAnswer(activeTurn.sampleAnswer);
    }
  }

  async function handleReset() {
    setMessages([{ role: "coach", text: activeTurns[0].coach }]);
    setSessionId(null);
    setTurnIndex(0);
    setAnswer("");
    setFeedback(null);
    setCompletedTurns(0);
    removeSavedPractice(effectiveStorageKey);

    try {
      await resetLatestPractice(lessonSlug);
      const session = await createConversationSession(lessonSlug);
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
                Scenario: meet a new friend in an online English class.
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
              <p className="font-semibold">{progressPercent}% complete</p>
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
          <div className="grid gap-3 md:grid-cols-[1fr_auto_auto]">
            <textarea
              value={answer}
              onChange={(event) => setAnswer(event.target.value)}
              disabled={completed || isSubmitting}
              rows={compact ? 2 : 3}
              className="focus-ring min-h-24 resize-none rounded-lg border border-ink/10 bg-paper px-4 py-3 text-sm leading-6 text-ink placeholder:text-ink/40 disabled:opacity-60"
              placeholder={completed ? "Roleplay selesai" : "Tulis jawabanmu dalam bahasa Inggris..."}
            />
            <button
              type="button"
              onClick={handleUseSample}
              disabled={completed || isSubmitting}
              className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border border-ink/15 px-4 py-3 text-sm font-semibold hover:bg-mint disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Sparkles className="h-4 w-4" aria-hidden="true" />
              Pakai Contoh
            </button>
            <button
              type="submit"
              disabled={!answer.trim() || completed || isSubmitting}
              className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:bg-ink/30"
            >
              <Send className="h-4 w-4" aria-hidden="true" />
              {isSubmitting ? "Mengirim" : "Kirim"}
            </button>
          </div>
        </form>
      </section>

      <aside className="space-y-4">
        <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-2">
            <MessageCircle className="h-5 w-5 text-leaf" aria-hidden="true" />
            <h2 className="font-semibold">Feedback Percakapan</h2>
          </div>

          {feedback ? (
            <div className="mt-4 space-y-4 text-sm leading-6">
              <div>
                <p className="font-semibold">Versi lebih natural</p>
                <p className="mt-1 text-ink/70">{feedback.betterVersion}</p>
              </div>
              <div>
                <p className="font-semibold">Penjelasan</p>
                <p className="mt-1 text-ink/70">{feedback.explanation}</p>
              </div>
              <div>
                <p className="font-semibold">Latihan berikutnya</p>
                <p className="mt-1 text-ink/70">{feedback.nextPractice}</p>
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sm leading-6 text-ink/60">
              Submit jawaban pertama untuk melihat versi yang lebih natural, penjelasan, dan skor.
            </p>
          )}

          <div className="mt-5 grid grid-cols-3 gap-2 text-center text-sm">
            {[
              ["Speaking", feedback?.scores.speaking ?? 0],
              ["Grammar", feedback?.scores.grammar ?? 0],
              ["Fluency", feedback?.scores.fluency ?? 0]
            ].map(([label, value]) => (
              <div key={label} className="rounded-lg bg-paper p-3">
                <p className="text-lg font-semibold">{value}</p>
                <p className="text-xs text-ink/60">{label}</p>
              </div>
            ))}
          </div>
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
