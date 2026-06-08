"use client";

import { useEffect, useRef, useState } from "react";
import { CheckCircle2, Mic, Play, Square } from "lucide-react";
import { ApiRequestError, checkPronunciation, type PronunciationCheckResult } from "@/lib/conversation-api";
import { useVoiceRecorder } from "@/lib/use-voice-recorder";
import { VoiceWaveform } from "@/components/voice-waveform";

type SpeakClearlyPracticeProps = {
  prompts: string[];
};

const maxRecordingSeconds = 15;

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
      return "STT belum aktif di server. Hubungi admin untuk mengaktifkan transkripsi.";
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
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState("");
  const [recordingUrl, setRecordingUrl] = useState<string | null>(null);
  const [result, setResult] = useState<PronunciationCheckResult | null>(null);

  const recordingUrlRef = useRef<string | null>(null);

  const recorder = useVoiceRecorder({
    onResult: (blob) => submitForCheck(blob),
    onError: (message) => setError(message),
    maxSeconds: maxRecordingSeconds,
    autoStopOnSilence: true
  });

  function setRecording(url: string | null) {
    if (recordingUrlRef.current) {
      URL.revokeObjectURL(recordingUrlRef.current);
    }
    recordingUrlRef.current = url;
    setRecordingUrl(url);
  }

  useEffect(() => {
    return () => {
      if (recordingUrlRef.current) {
        URL.revokeObjectURL(recordingUrlRef.current);
      }
    };
  }, []);

  function startRecording() {
    if (recorder.status !== "idle") {
      return;
    }
    setError("");
    setResult(null);
    setRecording(null);
    void recorder.start();
  }

  function stopRecording() {
    recorder.stop();
  }

  async function submitForCheck(blob: Blob) {
    if (!blob.size) {
      setError("Audio belum terekam. Coba ulangi.");
      return;
    }
    setRecording(URL.createObjectURL(blob));
    setError("");

    try {
      const checkResult = await checkPronunciation(target, blob);
      setResult(checkResult);
      setIsReady(true);
    } catch (caught) {
      setError(checkErrorMessage(caught));
      setIsReady(true);
    }
  }

  function playRecording() {
    if (recordingUrl) {
      void new Audio(recordingUrl).play();
    }
  }

  const isRecording = recorder.status === "recording";
  const isProcessing = recorder.status === "processing";
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
          aria-label={isRecording ? "Berhenti merekam" : "Rekam"}
        >
          {isRecording ? <Square className="h-4 w-4" aria-hidden="true" /> : <Mic className="h-4 w-4" aria-hidden="true" />}
          {isProcessing ? "Mengecek" : isRecording ? "Berhenti" : isReady ? "Rekam Ulang" : "Rekam"}
        </button>
        {isRecording ? <VoiceWaveform level={recorder.micLevel} label="" /> : null}
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
        </div>
      ) : null}

      {error ? <p className="mt-3 text-xs leading-5 text-coral">{error}</p> : null}
    </div>
  );
}
