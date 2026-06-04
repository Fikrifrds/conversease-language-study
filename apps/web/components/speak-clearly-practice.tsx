"use client";

import { useEffect, useRef, useState } from "react";
import { CheckCircle2, Mic, Play, Square } from "lucide-react";
import { ApiRequestError, checkPronunciation, type PronunciationCheckResult } from "@/lib/conversation-api";

type SpeakClearlyPracticeProps = {
  prompts: string[];
};

type RecorderState = "idle" | "recording" | "processing" | "ready";

const maxRecordingSeconds = 15;

function preferredRecordingMimeType() {
  if (typeof MediaRecorder === "undefined") {
    return "";
  }

  const candidates = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/ogg;codecs=opus"];
  return candidates.find((candidate) => MediaRecorder.isTypeSupported(candidate)) ?? "";
}

// Lesson prompts are instructions like `Say: Good morning. How are you?`.
// The phrase the learner should actually speak is the part after the first colon.
function targetPhraseFromPrompt(prompt: string) {
  const separatorIndex = prompt.indexOf(":");
  const candidate = separatorIndex >= 0 ? prompt.slice(separatorIndex + 1) : prompt;
  return candidate.trim() || prompt.trim();
}

function checkErrorMessage(error: unknown) {
  if (error instanceof ApiRequestError) {
    if (error.status === 503) {
      return "STT belum aktif di server. Hubungi admin untuk mengaktifkan AssemblyAI.";
    }
    if (error.status === 504) {
      return "Transkripsi terlalu lama. Coba rekam ulang yang lebih pendek.";
    }
    if (error.status === 422) {
      return "Audio belum bisa ditranskrip. Coba rekam ulang dengan suara lebih jelas.";
    }
  }
  return "Pengecekan pronunciation belum berhasil. Coba rekam ulang.";
}

export function SpeakClearlyPractice({ prompts }: SpeakClearlyPracticeProps) {
  return (
    <div className="mt-4 grid gap-3 md:grid-cols-3">
      {prompts.map((prompt, index) => (
        <PhraseRecorder key={`${prompt}-${index}`} prompt={prompt} target={targetPhraseFromPrompt(prompt)} />
      ))}
    </div>
  );
}

function PhraseRecorder({ prompt, target }: { prompt: string; target: string }) {
  const [state, setState] = useState<RecorderState>("idle");
  const [seconds, setSeconds] = useState(0);
  const [error, setError] = useState("");
  const [recordingUrl, setRecordingUrl] = useState<string | null>(null);
  const [result, setResult] = useState<PronunciationCheckResult | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const recordingUrlRef = useRef<string | null>(null);

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
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
  }

  function setRecording(url: string | null) {
    if (recordingUrlRef.current) {
      URL.revokeObjectURL(recordingUrlRef.current);
    }
    recordingUrlRef.current = url;
    setRecordingUrl(url);
  }

  useEffect(() => {
    return () => {
      clearTimers();
      stopStream();
      if (recordingUrlRef.current) {
        URL.revokeObjectURL(recordingUrlRef.current);
      }
    };
  }, []);

  async function startRecording() {
    if (state === "recording" || state === "processing") {
      return;
    }

    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
      setError("Browser belum mendukung rekam audio.");
      return;
    }

    setError("");
    setResult(null);
    setSeconds(0);
    setRecording(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = preferredRecordingMimeType();
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      chunksRef.current = [];
      streamRef.current = stream;
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = () => {
        clearTimers();
        stopStream();
        const blob = new Blob(chunksRef.current, { type: recorder.mimeType || mimeType || "audio/webm" });
        chunksRef.current = [];
        mediaRecorderRef.current = null;

        if (blob.size > 0) {
          setRecording(URL.createObjectURL(blob));
          void submitForCheck(blob);
        } else {
          setState("idle");
        }
      };

      recorder.start();
      setState("recording");
      intervalRef.current = setInterval(() => {
        setSeconds((current) => Math.min(current + 1, maxRecordingSeconds));
      }, 1000);
      timeoutRef.current = setTimeout(() => stopRecording(), maxRecordingSeconds * 1000);
    } catch {
      clearTimers();
      stopStream();
      mediaRecorderRef.current = null;
      setState("idle");
      setError("Mic belum bisa diakses. Cek izin microphone browser.");
    }
  }

  function stopRecording() {
    const recorder = mediaRecorderRef.current;
    if (!recorder || recorder.state === "inactive") {
      return;
    }
    setState("processing");
    recorder.stop();
  }

  async function submitForCheck(blob: Blob) {
    setState("processing");
    setError("");

    try {
      const checkResult = await checkPronunciation(target, blob);
      setResult(checkResult);
      setState("ready");
    } catch (caught) {
      setError(checkErrorMessage(caught));
      setState("ready");
    }
  }

  function playRecording() {
    if (recordingUrl) {
      void new Audio(recordingUrl).play();
    }
  }

  const isRecording = state === "recording";
  const isProcessing = state === "processing";
  const matchPercent = result ? Math.round(result.matchRatio * 100) : 0;
  const matchTone = matchPercent >= 80 ? "text-leaf" : matchPercent >= 50 ? "text-coral" : "text-ink/60";

  return (
    <div className="rounded-lg bg-paper p-4">
      <p className="text-sm leading-6 text-ink/70">{prompt}</p>
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <button
          type="button"
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isProcessing}
          className={`focus-ring inline-flex h-10 items-center justify-center gap-2 rounded-lg px-3 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-50 ${
            isRecording ? "bg-coral text-white hover:bg-ink" : "bg-leaf text-white hover:bg-ink"
          }`}
          aria-label={isRecording ? "Stop recording" : "Record"}
        >
          {isRecording ? <Square className="h-4 w-4" aria-hidden="true" /> : <Mic className="h-4 w-4" aria-hidden="true" />}
          {isProcessing ? "Mengecek" : isRecording ? `Stop ${seconds}s` : state === "ready" ? "Rekam Ulang" : "Rekam"}
        </button>
        {recordingUrl && !isRecording && !isProcessing ? (
          <button
            type="button"
            onClick={playRecording}
            className="focus-ring inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-ink/15 px-3 text-sm font-semibold hover:bg-mint"
            aria-label="Putar rekaman"
          >
            <Play className="h-4 w-4" aria-hidden="true" />
            Dengar
          </button>
        ) : null}
      </div>

      {result && !error ? (
        <div className="mt-3 space-y-2 text-sm leading-6">
          <p className={`flex items-center gap-2 font-semibold ${matchTone}`}>
            <CheckCircle2 className="h-4 w-4 shrink-0" aria-hidden="true" />
            {matchPercent}% kata cocok
          </p>
          <p className="text-ink/70">
            <span className="font-medium text-ink/50">Terdengar:</span> &ldquo;{result.transcript}&rdquo;
          </p>
          <p className="text-xs text-ink/45">Transkrip oleh {result.provider}.</p>
        </div>
      ) : null}

      {error ? <p className="mt-3 text-xs leading-5 text-coral">{error}</p> : null}
    </div>
  );
}
