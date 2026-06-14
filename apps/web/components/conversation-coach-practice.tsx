"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { CheckCircle2, ChevronDown, ChevronUp, Lightbulb, Loader2, MessageCircle, Mic, RotateCcw, Send, Sparkles, Square } from "lucide-react";
import {
  ApiRequestError,
  createConversationSession,
  getResumablePractice,
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
  expectedKeywords: string[];
  indonesianExplanation: string;
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

const coachTurnsByLessonSlug: Record<string, CoachTurn[]> = generatedCoachTurnsByLessonSlug;

const maxRecordingSeconds = 30;

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
  const activeTurns = coachTurnsByLessonSlug[lessonSlug];
  const activeScenario = coachScenarioBySlug[lessonSlug];
  const totalTurns = activeTurns?.length ?? 0;
  const hasRoleplayData = Boolean(activeScenario && totalTurns > 0);
  const effectiveStorageKey = storageKey ?? practiceStorageKeyForLesson(lessonSlug);
  const [messages, setMessages] = useState<ChatMessage[]>(() =>
    activeTurns?.[0]?.coach ? [{ role: "coach", text: activeTurns[0].coach }] : []
  );
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [turnIndex, setTurnIndex] = useState(0);
  const [feedbackTurnIndex, setFeedbackTurnIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState<CoachFeedback | null>(null);
  const [completedTurns, setCompletedTurns] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [syncStatus, setSyncStatus] = useState<"connecting" | "synced">("connecting");
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

  const completed = totalTurns > 0 && completedTurns >= totalTurns;
  const score = averageScore(feedback);
  const isRecording = recorder.status === "recording";
  const isProcessingRecording = recorder.status === "processing";

  const savedPractice: SavedPractice = useMemo(
    () => ({
      sessionId: sessionId ?? undefined,
      completedTurns,
      totalTurns,
      completed,
      lastScore: score,
      updatedAt: new Date().toISOString()
    }),
    [completed, completedTurns, score, sessionId, totalTurns]
  );

  useEffect(() => {
    if (completedTurns === 0 || !hasRoleplayData) {
      return;
    }

    saveSavedPractice(savedPractice, effectiveStorageKey);
    saveLatestPracticeSlug(lessonSlug);
  }, [completedTurns, effectiveStorageKey, hasRoleplayData, lessonSlug, savedPractice]);

  // Resume an in-progress server session on mount so a page refresh does not
  // lose the conversation (the component remounts per scenario via `key`).
  useEffect(() => {
    if (!hasRoleplayData) {
      return;
    }
    let cancelled = false;

    async function resume() {
      try {
        const saved = await getResumablePractice(lessonSlug);
        if (cancelled || !saved || saved.completedTurns === 0) {
          if (!cancelled) {
            setSyncStatus("connecting");
          }
          return;
        }

        const turnsForLesson = coachTurnsByLessonSlug[lessonSlug] ?? [];
        const rebuilt: ChatMessage[] = saved.firstCoachMessage
          ? [{ role: "coach", text: saved.firstCoachMessage }]
          : [];
        for (const turn of saved.turns) {
          rebuilt.push({ role: "user", text: turn.userTranscript });
          if (turn.coachReply) {
            rebuilt.push({ role: "coach", text: turn.coachReply });
          }
        }

        setMessages(rebuilt);
        setSessionId(saved.sessionId);
        setCompletedTurns(saved.completedTurns);
        setTurnIndex(Math.min(saved.completedTurns, turnsForLesson.length - 1));
        setFeedbackTurnIndex(
          Math.min(Math.max(saved.completedTurns - 1, 0), turnsForLesson.length - 1)
        );
        if (saved.lastFeedback) {
          setFeedback(saved.lastFeedback);
        }
        setSyncStatus("synced");
      } catch {
        if (!cancelled) {
          setSyncStatus("connecting");
        }
      }
    }

    void resume();
    return () => {
      cancelled = true;
    };
    // Mount-only: the component remounts per scenario (key={activeSlug}).
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!activeScenario || !activeTurns?.length) {
    return (
      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <p className="text-sm font-semibold uppercase text-leaf">Conversation Coach</p>
        <h2 className="mt-2 text-2xl font-semibold">Roleplay Belum Tersedia</h2>
        <p className="mt-3 max-w-2xl text-sm leading-7 text-ink/70">
          Lesson ini belum punya data roleplay generated yang siap dipakai di runtime. Pilih skenario lain dulu
          atau sinkronkan data lesson sebelum QA lanjutan.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          <Link
            href="/conversation-coach"
            className="focus-ring inline-flex items-center justify-center rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink"
          >
            Pilih Skenario Lain
          </Link>
          <Link
            href={`/lessons/${lessonSlug}`}
            className="focus-ring inline-flex items-center justify-center rounded-lg border border-ink/15 px-4 py-3 text-sm font-semibold hover:bg-mint"
          >
            Buka Lesson
          </Link>
        </div>
      </section>
    );
  }

  const activeTurn = activeTurns[Math.min(turnIndex, activeTurns.length - 1)];
  const feedbackTurn = activeTurns[Math.min(feedbackTurnIndex, activeTurns.length - 1)];
  const progressPercent = Math.round((completedTurns / activeTurns.length) * 100);

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
        const session = await createConversationSession(lessonSlug, activeScenario);
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
      if (
        error instanceof ApiRequestError &&
        (error.status === 402 || error.status === 403 || error.status === 429)
      ) {
        handleTurnError(error);
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
    setRecordingError("");

    // Server-authoritative: feedback, scoring, and progress always come from the
    // API so the learner never sees fabricated scores or divergent state. On any
    // failure we keep the answer in the box and ask the learner to retry.
    let activeSessionId = sessionId;

    try {
      if (!activeSessionId) {
        const session = await createConversationSession(lessonSlug, activeScenario);
        activeSessionId = session.sessionId;
        setSessionId(session.sessionId);
      }

      const result = await submitConversationTurn(activeSessionId, userAnswer);
      setSyncStatus("synced");
      applySummary(result.summary);
      applyTurnResult({
        userText: result.userTranscript || userAnswer,
        nextCompletedTurns: result.summary.completedTurns,
        nextTurnIndex: Math.min(result.summary.completedTurns, activeTurns.length - 1),
        nextCoachReply: result.coachReply,
        nextFeedback: result.feedback
      });
      setAnswer("");
    } catch (error) {
      handleTurnError(error);
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleTurnError(error: unknown) {
    if (error instanceof ApiRequestError) {
      if (error.status === 402) {
        setBillingNotice("Kuota Conversation Coach habis. Top-up atau upgrade untuk melanjutkan latihan tersinkron.");
        return;
      }
      if (error.status === 403) {
        setBillingNotice("Skenario level ini butuh paket Pro. Upgrade untuk berlatih Conversation Coach di A2 ke atas.");
        return;
      }
      if (error.status === 429) {
        setRecordingError("Terlalu banyak percakapan dalam waktu singkat. Tunggu sebentar lalu coba lagi.");
        return;
      }
    }
    setRecordingError("Jawaban belum terkirim ke server. Cek koneksi lalu kirim ulang.");
  }

  function handleUseSample() {
    if (!completed) {
      setAnswer(activeTurn.sampleAnswer);
    }
  }

  async function handleReset() {
    // Don't reset mid-request: a server turn could land after we clear state and
    // resurrect a stale session.
    if (isSubmitting || isProcessingRecording) {
      return;
    }
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
    setBillingNotice("");
    removeSavedPractice(effectiveStorageKey);

    try {
      await resetLatestPractice(lessonSlug);
      const session = await createConversationSession(lessonSlug, activeScenario);
      setSessionId(session.sessionId);
      setMessages([{ role: "coach", text: session.firstCoachMessage }]);
      setSyncStatus("synced");
    } catch {
      setSyncStatus("connecting");
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
                {syncStatus === "synced" ? "Sesi tersinkron" : "Siap mulai"}
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
            <div className="w-full min-w-0 rounded-lg bg-mint px-4 py-3 text-sm sm:w-auto sm:min-w-32">
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
                className={`max-w-[92%] rounded-lg p-4 text-sm leading-6 sm:max-w-[86%] ${
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
          <div className="mt-3 grid gap-2 sm:flex sm:flex-wrap sm:items-center">
            <button
              type="button"
              onClick={isRecording ? stopRecording : startRecording}
              disabled={completed || isSubmitting || isProcessingRecording}
              className={`focus-ring inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-lg px-4 py-3 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto ${
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
              className="focus-ring inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-lg border border-ink/15 px-4 py-3 text-sm font-semibold hover:bg-mint disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
            >
              <Sparkles className="h-4 w-4" aria-hidden="true" />
              Pakai Contoh
            </button>
            <button
              type="submit"
              disabled={!answer.trim() || completed || isSubmitting || isRecording || isProcessingRecording}
              className="focus-ring inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-lg bg-leaf px-5 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:bg-ink/30 sm:ml-auto sm:w-auto"
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
