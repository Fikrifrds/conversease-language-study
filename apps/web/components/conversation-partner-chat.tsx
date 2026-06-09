"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { CheckCircle2, Mic, MicOff, Sparkles, Square, Volume2 } from "lucide-react";
import { ApiRequestError } from "@/lib/conversation-api";
import {
  createPartnerSession,
  fetchPartnerSummary,
  submitPartnerAudioTurn,
  type PartnerSummary,
  type PartnerTopic
} from "@/lib/conversation-partner-api";
import { useVoiceRecorder } from "@/lib/use-voice-recorder";
import { VoiceWaveform } from "@/components/voice-waveform";

type ChatMessage = {
  role: "partner" | "user";
  text: string;
  audio?: string | null;
};

function turnErrorMessage(error: unknown) {
  if (error instanceof ApiRequestError) {
    if (error.status === 402) {
      return "Kuota Conversation Partner habis. Top-up atau upgrade untuk lanjut.";
    }
    if (error.status === 503) {
      return "STT belum aktif. Pastikan kunci API STT terbaca di server.";
    }
    if (error.status === 504) {
      return "Transkripsi terlalu lama. Coba bicara lebih singkat.";
    }
    if (error.status === 422) {
      return "Audio belum bisa ditranskrip. Coba bicara lebih jelas.";
    }
  }
  return "Terjadi kendala. Coba lagi.";
}

export function ConversationPartnerChat({
  topic,
  onSessionEnd
}: {
  topic: PartnerTopic;
  onSessionEnd?: () => void;
}) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "partner", text: topic.openingLine }
  ]);
  const [completedTurns, setCompletedTurns] = useState(0);
  const [ended, setEnded] = useState(false);
  const [summary, setSummary] = useState<PartnerSummary | null>(null);
  const [isBusy, setIsBusy] = useState(false);
  const [error, setError] = useState("");
  const [offTopicNote, setOffTopicNote] = useState(false);
  const [handsFree, setHandsFree] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  // The session begins only when the learner presses Start. Until then nothing
  // is spoken and the mic stays closed, so the AI never "talks first" before the
  // learner is ready. Start -> AI speaks the opening -> mic opens -> alternate.
  const [started, setStarted] = useState(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const handsFreeRef = useRef(false);
  // Source of truth for the session id across async callbacks (state updates are
  // async, so reading from a closure can be stale and accidentally create a new
  // session each turn, losing conversation memory).
  const sessionIdRef = useRef<string | null>(null);

  const recorder = useVoiceRecorder({
    onResult: (blob) => submitRecording(blob),
    onError: (message) => {
      setError(message);
      handsFreeRef.current = false;
      setHandsFree(false);
    },
    maxSeconds: 30,
    autoStopOnSilence: true
  });

  const isRecording = recorder.status === "recording";
  const isProcessing = recorder.status === "processing";
  const progressPercent = Math.min(100, Math.round((completedTurns / topic.maxTurns) * 100));

  useEffect(() => {
    return () => {
      handsFreeRef.current = false;
      audioRef.current?.pause();
    };
  }, []);

  function playAudio(dataUrl: string | null | undefined, onEnded?: () => void) {
    if (!dataUrl) {
      onEnded?.();
      return;
    }
    audioRef.current?.pause();
    const audio = new Audio(dataUrl);
    audioRef.current = audio;

    // Guarantee the continuation runs exactly once, whatever happens: normal
    // end, playback error, or autoplay block. Without this, a missed `onended`
    // would strand hands-free on "Menunggu AI…" with no recording in progress.
    let settled = false;
    const finish = () => {
      if (settled) {
        return;
      }
      settled = true;
      setIsSpeaking(false);
      onEnded?.();
    };

    audio.onended = finish;
    audio.onerror = finish;
    setIsSpeaking(true);
    void audio.play().catch(() => {
      /* autoplay may be blocked; user can replay manually */
      finish();
    });
  }

  async function submitRecording(blob: Blob) {
    if (!blob.size) {
      setError("Audio belum terekam. Coba ulangi.");
      return;
    }

    setIsBusy(true);
    setError("");

    try {
      let activeSessionId = sessionIdRef.current;
      if (!activeSessionId) {
        const session = await createPartnerSession(topic.key);
        activeSessionId = session.sessionId;
        sessionIdRef.current = session.sessionId;
        // The opening line is already shown/spoken up front, so we do NOT replay
        // session.openingAudio here — it would overlap the upcoming reply.
      }

      const result = await submitPartnerAudioTurn(activeSessionId, blob);
      setMessages((current) => [
        ...current,
        { role: "user", text: result.userTranscript },
        { role: "partner", text: result.partnerReply, audio: result.partnerAudio }
      ]);
      setCompletedTurns(result.completedTurns);
      setOffTopicNote(!result.onTopic);

      if (result.shouldEnd) {
        playAudio(result.partnerAudio);
        handsFreeRef.current = false;
        setHandsFree(false);
        setEnded(true);
        void loadSummary(activeSessionId);
      } else {
        // Hands-free: listen again once the AI finishes speaking.
        playAudio(result.partnerAudio, () => {
          if (handsFreeRef.current) {
            void recorder.start();
          }
        });
      }
    } catch (caught) {
      setError(turnErrorMessage(caught));
      // A transcription miss (too quiet / too short) is recoverable: keep
      // hands-free on and listen again instead of ending the conversation.
      const recoverable = caught instanceof ApiRequestError && caught.status === 422;
      if (recoverable && handsFreeRef.current) {
        setIsBusy(false);
        void recorder.start();
        return;
      }
      handsFreeRef.current = false;
      setHandsFree(false);
    } finally {
      setIsBusy(false);
    }
  }

  // Start the session: create it, let the AI speak the opening line, then open
  // the mic so the learner answers. After that the turn loop alternates
  // automatically (each AI reply's audio `onended` re-opens the mic).
  async function startSession() {
    if (ended || isBusy || started) {
      return;
    }
    setStarted(true);
    handsFreeRef.current = true;
    setHandsFree(true);
    setError("");
    try {
      if (!sessionIdRef.current) {
        const session = await createPartnerSession(topic.key);
        sessionIdRef.current = session.sessionId;
        // AI greets first, then the learner's mic opens when the greeting ends.
        playAudio(session.openingAudio, () => {
          if (handsFreeRef.current) {
            void recorder.start();
          }
        });
        return;
      }
    } catch (caught) {
      setError(turnErrorMessage(caught));
      setStarted(false);
      handsFreeRef.current = false;
      setHandsFree(false);
      return;
    }
    void recorder.start();
  }

  // Resume the automatic turn loop after a manual pause, without replaying the
  // opening (the session already exists).
  function resumeHandsFree() {
    if (ended || isBusy || isSpeaking) {
      return;
    }
    handsFreeRef.current = true;
    setHandsFree(true);
    void recorder.start();
  }

  function stopHandsFree() {
    handsFreeRef.current = false;
    setHandsFree(false);
    audioRef.current?.pause();
    setIsSpeaking(false);
    recorder.cancel();
  }

  async function loadSummary(activeSessionId: string) {
    try {
      const result = await fetchPartnerSummary(activeSessionId);
      setSummary(result);
    } catch {
      /* summary is best-effort */
    } finally {
      // Tell the workspace to refresh the history list now that this session is
      // finished and its score persisted.
      onSessionEnd?.();
    }
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[0.72fr_0.28fr]">
      <section className="rounded-lg border border-ink/10 bg-white shadow-sm">
        <div className="border-b border-ink/10 p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">{topic.title}</p>
              <h2 className="mt-2 text-2xl font-semibold">Ngobrol dengan AI</h2>
              <p className="mt-2 text-sm leading-6 text-ink/70">{topic.description}</p>
              {offTopicNote && !ended ? (
                <p className="mt-3 inline-flex rounded-lg bg-[#fff2dc] px-3 py-2 text-xs font-semibold text-ink/70">
                  Tetap fokus ke topik ini supaya latihannya maksimal.
                </p>
              ) : null}
            </div>
            <div className="w-full min-w-0 rounded-lg bg-mint px-4 py-3 text-sm sm:w-auto sm:min-w-32">
              <p className="font-semibold">
                {completedTurns}/{topic.maxTurns} turn
              </p>
              <div className="mt-2 h-2 rounded-lg bg-white">
                <div className="h-2 rounded-lg bg-leaf" style={{ width: `${progressPercent}%` }} />
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-4 p-5">
          {messages.map((message, index) => (
            <div
              key={`${message.role}-${index}`}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[92%] rounded-lg p-4 text-sm leading-6 sm:max-w-[86%] ${
                  message.role === "user" ? "bg-leaf text-white" : "bg-paper text-ink"
                }`}
              >
                <p>{message.text}</p>
                {message.role === "partner" && message.audio ? (
                  <button
                    type="button"
                    onClick={() => playAudio(message.audio)}
                    className="focus-ring mt-2 inline-flex items-center gap-1 text-xs font-semibold text-leaf hover:text-ink"
                  >
                    <Volume2 className="h-3.5 w-3.5" aria-hidden="true" />
                    Putar lagi
                  </button>
                ) : null}
              </div>
            </div>
          ))}

          {ended ? (
            <div className="rounded-lg border border-leaf/30 bg-mint p-4 text-sm leading-6">
              <div className="flex items-center gap-2 font-semibold">
                <CheckCircle2 className="h-4 w-4 text-leaf" aria-hidden="true" />
                Percakapan selesai
              </div>
              <p className="mt-2 text-ink/70">
                Kamu menyelesaikan latihan ngobrol topik ini. Lihat ringkasan dan skor di samping.
              </p>
            </div>
          ) : (
            <div className="rounded-lg bg-[#fff2dc] p-4 text-sm leading-6">
              <div className="flex items-start gap-2">
                <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-coral" aria-hidden="true" />
                <div>
                  <p className="font-semibold">Tujuan latihan</p>
                  <p className="text-ink/70">{topic.goals.join(" → ")}</p>
                  {!started ? (
                    <p className="mt-2 text-xs text-ink/60">
                      Tekan <span className="font-semibold">Mulai Sesi</span> di bawah. AI akan menyapa
                      lebih dulu, lalu giliranmu bicara.
                    </p>
                  ) : null}
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="border-t border-ink/10 p-5">
          {!started ? (
            <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
              <button
                type="button"
                onClick={startSession}
                disabled={ended || isBusy}
                className="focus-ring inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-lg bg-leaf px-6 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
              >
                <Mic className="h-4 w-4" aria-hidden="true" />
                {ended ? "Selesai" : isBusy ? "Memulai…" : "Mulai Sesi"}
              </button>
              <span className="text-xs text-ink/50">
                Tekan Mulai — AI menyapa lebih dulu, lalu giliranmu bicara otomatis.
              </span>
            </div>
          ) : handsFree ? (
            <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
              <button
                type="button"
                onClick={stopHandsFree}
                className="focus-ring inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-lg bg-coral px-5 py-3 text-sm font-semibold text-white hover:bg-ink sm:w-auto"
              >
                <MicOff className="h-4 w-4" aria-hidden="true" />
                Jeda
              </button>
              <span className="inline-flex items-center gap-3 text-sm font-medium text-ink/70">
                {isBusy || isProcessing ? (
                  <>Memproses…</>
                ) : isSpeaking ? (
                  <span className="inline-flex items-center gap-2">
                    <Volume2 className="h-4 w-4 text-leaf" aria-hidden="true" />
                    AI sedang berbicara…
                  </span>
                ) : isRecording ? (
                  <span className="inline-flex items-center gap-2">
                    <VoiceWaveform level={recorder.micLevel} />
                    Giliranmu — silakan bicara…
                  </span>
                ) : (
                  <>Mendengarkan…</>
                )}
              </span>
            </div>
          ) : (
            <div className="flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:items-center">
              <button
                type="button"
                onClick={resumeHandsFree}
                disabled={ended || isBusy || isProcessing || isSpeaking}
                className="focus-ring inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-lg bg-leaf px-5 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
              >
                <Mic className="h-4 w-4" aria-hidden="true" />
                Lanjut Bicara
              </button>
              <button
                type="button"
                onClick={isRecording ? recorder.stop : recorder.start}
                disabled={ended || isBusy || isProcessing || isSpeaking}
                className={`focus-ring inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-lg border px-4 py-3 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto ${
                  isRecording ? "border-coral bg-coral text-white hover:bg-ink" : "border-ink/15 hover:bg-mint"
                }`}
              >
                {isRecording ? (
                  <Square className="h-4 w-4" aria-hidden="true" />
                ) : (
                  <Mic className="h-4 w-4" aria-hidden="true" />
                )}
                {isProcessing
                  ? "Memproses"
                  : isBusy
                    ? "Mengirim"
                    : isRecording
                      ? "Berhenti"
                      : "Rekam manual"}
              </button>
              {isRecording ? <VoiceWaveform level={recorder.micLevel} label="" /> : null}
            </div>
          )}
          {error ? (
            <p className="mt-3 rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{error}</p>
          ) : null}
        </div>
      </section>

      <aside className="space-y-4">
        <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <h2 className="font-semibold">Ringkasan & Skor</h2>
          {summary ? (
            <div className="mt-4 space-y-4 text-sm leading-6">
              <div>
                <p className="font-semibold">Catatan</p>
                <p className="mt-1 text-ink/70">{summary.summary}</p>
              </div>
              <div>
                <p className="font-semibold">Penjelasan</p>
                <p className="mt-1 text-ink/70">{summary.indonesianExplanation}</p>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center">
                {[
                  ["Speaking", summary.scores.speaking],
                  ["Grammar", summary.scores.grammar],
                  ["Fluency", summary.scores.fluency]
                ].map(([label, value]) => (
                  <div key={label} className="rounded-lg bg-paper p-3">
                    <p className="text-lg font-semibold">{value}</p>
                    <p className="text-xs text-ink/60">{label}</p>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sm leading-6 text-ink/60">
              Selesaikan percakapan untuk melihat ringkasan dan skor speaking, grammar, dan fluency.
            </p>
          )}
        </section>

        <section className="rounded-lg bg-ink p-5 text-white">
          <p className="text-sm text-white/70">Partner</p>
          <p className="mt-2 text-2xl font-semibold">AI Partner</p>
          <p className="mt-2 text-sm leading-6 text-white/70">
            AI yang berperan sebagai {topic.partnerRole}.
          </p>
          <Link
            href="/progress"
            className="focus-ring mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-white px-4 py-3 text-sm font-semibold text-ink hover:bg-mint"
          >
            <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
            Lihat Progress
          </Link>
        </section>
      </aside>
    </div>
  );
}
