"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { CheckCircle2, Mic, Sparkles, Square, Volume2 } from "lucide-react";
import { ApiRequestError } from "@/lib/conversation-api";
import {
  createPartnerSession,
  fetchPartnerSummary,
  submitPartnerAudioTurn,
  type PartnerSummary,
  type PartnerTopic
} from "@/lib/conversation-partner-api";

type ChatMessage = {
  role: "partner" | "user";
  text: string;
  audio?: string | null;
};

const maxRecordingSeconds = 30;

function preferredRecordingMimeType() {
  if (typeof MediaRecorder === "undefined") {
    return "";
  }
  const candidates = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/ogg;codecs=opus"];
  return candidates.find((candidate) => MediaRecorder.isTypeSupported(candidate)) ?? "";
}

function turnErrorMessage(error: unknown) {
  if (error instanceof ApiRequestError) {
    if (error.status === 402) {
      return "Kuota Conversation Partner habis. Top-up atau upgrade untuk lanjut.";
    }
    if (error.status === 503) {
      return "STT belum aktif. Pastikan ASSEMBLYAI_API_KEY terbaca di API.";
    }
    if (error.status === 504) {
      return "Transkripsi terlalu lama. Coba rekam jawaban lebih pendek.";
    }
    if (error.status === 422) {
      return "Audio belum bisa ditranskrip. Coba rekam ulang dengan suara lebih jelas.";
    }
  }
  return "Terjadi kendala. Coba rekam ulang.";
}

export function ConversationPartnerChat({ topic }: { topic: PartnerTopic }) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "partner", text: topic.openingLine }
  ]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [completedTurns, setCompletedTurns] = useState(0);
  const [ended, setEnded] = useState(false);
  const [summary, setSummary] = useState<PartnerSummary | null>(null);
  const [isBusy, setIsBusy] = useState(false);
  const [recordingStatus, setRecordingStatus] = useState<"idle" | "recording" | "processing">("idle");
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [error, setError] = useState("");
  const [offTopicNote, setOffTopicNote] = useState(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recordingStreamRef = useRef<MediaStream | null>(null);
  const recordedChunksRef = useRef<BlobPart[]>([]);
  const discardRef = useRef(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const isRecording = recordingStatus === "recording";
  const isProcessing = recordingStatus === "processing";
  const progressPercent = Math.min(100, Math.round((completedTurns / topic.maxTurns) * 100));

  useEffect(() => {
    return () => {
      clearTimers();
      stopStream();
      audioRef.current?.pause();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function playAudio(dataUrl: string | null | undefined) {
    if (!dataUrl) {
      return;
    }
    audioRef.current?.pause();
    const audio = new Audio(dataUrl);
    audioRef.current = audio;
    void audio.play().catch(() => {
      /* autoplay may be blocked; user can replay */
    });
  }

  function clearTimers() {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }

  function stopStream() {
    recordingStreamRef.current?.getTracks().forEach((track) => track.stop());
    recordingStreamRef.current = null;
  }

  async function startRecording() {
    if (ended || isBusy || isRecording || isProcessing) {
      return;
    }
    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
      setError("Browser belum mendukung rekam audio.");
      return;
    }

    setError("");
    setOffTopicNote(false);
    setRecordingSeconds(0);
    discardRef.current = false;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = preferredRecordingMimeType();
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      recordedChunksRef.current = [];
      recordingStreamRef.current = stream;
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = () => {
        clearTimers();
        stopStream();
        if (discardRef.current) {
          recordedChunksRef.current = [];
          mediaRecorderRef.current = null;
          discardRef.current = false;
          setRecordingStatus("idle");
          return;
        }
        const blob = new Blob(recordedChunksRef.current, {
          type: recorder.mimeType || mimeType || "audio/webm"
        });
        recordedChunksRef.current = [];
        mediaRecorderRef.current = null;
        void submitRecording(blob);
      };

      recorder.start();
      setRecordingStatus("recording");
      intervalRef.current = setInterval(() => {
        setRecordingSeconds((current) => Math.min(current + 1, maxRecordingSeconds));
      }, 1000);
      timeoutRef.current = setTimeout(() => stopRecording(), maxRecordingSeconds * 1000);
    } catch {
      clearTimers();
      stopStream();
      mediaRecorderRef.current = null;
      setRecordingStatus("idle");
      setError("Mic belum bisa diakses. Cek izin microphone browser.");
    }
  }

  function stopRecording() {
    const recorder = mediaRecorderRef.current;
    if (!recorder || recorder.state === "inactive") {
      return;
    }
    setRecordingStatus("processing");
    clearTimers();
    recorder.stop();
  }

  async function submitRecording(blob: Blob) {
    if (!blob.size) {
      setRecordingStatus("idle");
      setError("Audio belum terekam. Coba ulangi.");
      return;
    }

    setIsBusy(true);
    setError("");

    try {
      let activeSessionId = sessionId;
      if (!activeSessionId) {
        const session = await createPartnerSession(topic.key);
        activeSessionId = session.sessionId;
        setSessionId(session.sessionId);
        if (session.openingAudio) {
          playAudio(session.openingAudio);
        }
      }

      const result = await submitPartnerAudioTurn(activeSessionId, blob);
      setMessages((current) => [
        ...current,
        { role: "user", text: result.userTranscript },
        { role: "partner", text: result.partnerReply, audio: result.partnerAudio }
      ]);
      setCompletedTurns(result.completedTurns);
      setOffTopicNote(!result.onTopic);
      playAudio(result.partnerAudio);

      if (result.shouldEnd) {
        setEnded(true);
        void loadSummary(activeSessionId);
      }
    } catch (caught) {
      setError(turnErrorMessage(caught));
    } finally {
      setRecordingStatus("idle");
      setIsBusy(false);
    }
  }

  async function loadSummary(activeSessionId: string) {
    try {
      const result = await fetchPartnerSummary(activeSessionId);
      setSummary(result);
    } catch {
      /* summary is best-effort */
    }
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[0.72fr_0.28fr]">
      <section className="rounded-lg border border-ink/10 bg-white shadow-sm">
        <div className="border-b border-ink/10 p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">{topic.title}</p>
              <h2 className="mt-2 text-2xl font-semibold">Ngobrol dengan {topic.partnerName}</h2>
              <p className="mt-2 text-sm leading-6 text-ink/70">{topic.description}</p>
              {offTopicNote && !ended ? (
                <p className="mt-3 inline-flex rounded-lg bg-[#fff2dc] px-3 py-2 text-xs font-semibold text-ink/70">
                  Tetap fokus ke topik ini supaya latihannya maksimal.
                </p>
              ) : null}
            </div>
            <div className="min-w-32 rounded-lg bg-mint px-4 py-3 text-sm">
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
                className={`max-w-[86%] rounded-lg p-4 text-sm leading-6 ${
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
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="border-t border-ink/10 p-5">
          <div className="flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={isRecording ? stopRecording : startRecording}
              disabled={ended || isBusy || isProcessing}
              className={`focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg px-5 py-3 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-50 ${
                isRecording ? "bg-coral text-white hover:bg-ink" : "bg-leaf text-white hover:bg-ink"
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
                    ? `Stop ${recordingSeconds}s`
                    : ended
                      ? "Selesai"
                      : "Rekam & Bicara"}
            </button>
            <p className="text-xs text-ink/50">Tekan rekam, bicara dalam bahasa Inggris, lalu stop.</p>
          </div>
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
          <p className="mt-2 text-2xl font-semibold">{topic.partnerName}</p>
          <p className="mt-2 text-sm leading-6 text-white/70">{topic.partnerRole}.</p>
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
