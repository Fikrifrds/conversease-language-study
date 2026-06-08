"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { Mic, Play, Square, Volume2 } from "lucide-react";
import { useVoiceRecorder } from "@/lib/use-voice-recorder";
import { VoiceWaveform } from "@/components/voice-waveform";

function extractRepeatPhrases(markdown: string) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const startIndex = lines.findIndex((line) => line.trim().toLowerCase() === "## repeat");
  if (startIndex < 0) {
    return [];
  }

  const phrases: string[] = [];
  for (let i = startIndex + 1; i < lines.length; i += 1) {
    const line = (lines[i] ?? "").trim();
    if (!line) {
      if (phrases.length) {
        break;
      }
      continue;
    }
    if (line.startsWith("## ")) {
      break;
    }
    const numbered = line.match(/^\d+\.\s+(.*)$/);
    if (numbered?.[1]) {
      phrases.push(numbered[1].trim());
      continue;
    }
    const dashed = line.match(/^-+\s+(.*)$/);
    if (dashed?.[1]) {
      phrases.push(dashed[1].trim());
    }
  }

  return phrases.filter(Boolean);
}

function canSpeakExample() {
  return typeof window !== "undefined" && "speechSynthesis" in window && typeof SpeechSynthesisUtterance !== "undefined";
}

function speakExample(text: string) {
  if (!canSpeakExample()) {
    return;
  }
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = 0.95;
  window.speechSynthesis.speak(utterance);
}

export function PronunciationRepeatPractice({ drillMarkdown }: { drillMarkdown: string }) {
  const phrases = useMemo(() => extractRepeatPhrases(drillMarkdown), [drillMarkdown]);
  const items = phrases.length ? phrases : ["Practice the key phrases from this lesson."];

  return (
    <div className="mt-4 grid gap-3 md:grid-cols-2">
      {items.map((phrase, index) => (
        <RepeatItem key={`${phrase}-${index}`} phrase={phrase} enableExample={phrases.length > 0} />
      ))}
    </div>
  );
}

function RepeatItem({ phrase, enableExample }: { phrase: string; enableExample: boolean }) {
  const [error, setError] = useState("");
  const [recordingUrl, setRecordingUrl] = useState<string | null>(null);
  const recordingUrlRef = useRef<string | null>(null);

  const recorder = useVoiceRecorder({
    onResult: (blob) => {
      if (!blob.size) {
        setError("Audio belum terekam. Coba ulangi.");
        return;
      }
      const url = URL.createObjectURL(blob);
      if (recordingUrlRef.current) {
        URL.revokeObjectURL(recordingUrlRef.current);
      }
      recordingUrlRef.current = url;
      setRecordingUrl(url);
      setError("");
    },
    onError: (message) => setError(message),
    maxSeconds: 12,
    autoStopOnSilence: true
  });

  useEffect(() => {
    return () => {
      if (recordingUrlRef.current) {
        URL.revokeObjectURL(recordingUrlRef.current);
      }
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  function startRecording() {
    if (recorder.status !== "idle") {
      return;
    }
    setError("");
    void recorder.start();
  }

  function stopRecording() {
    recorder.stop();
  }

  function playRecording() {
    if (!recordingUrl) {
      return;
    }
    void new Audio(recordingUrl).play();
  }

  const isRecording = recorder.status === "recording";
  const isProcessing = recorder.status === "processing";
  const exampleAvailable = enableExample && canSpeakExample();

  return (
    <div className="rounded-lg bg-paper p-4">
      <p className="font-medium text-ink">{phrase}</p>
      <div className="mt-4 flex flex-wrap items-center gap-2">
        {exampleAvailable ? (
          <button
            type="button"
            onClick={() => speakExample(phrase)}
            className="focus-ring inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-ink/15 px-3 text-sm font-semibold hover:bg-mint"
          >
            <Volume2 className="h-4 w-4" aria-hidden="true" />
            Dengar contoh
          </button>
        ) : null}

        <button
          type="button"
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isProcessing}
          className={`focus-ring inline-flex h-10 items-center justify-center gap-2 rounded-lg px-3 text-sm font-semibold disabled:cursor-not-allowed disabled:bg-ink/30 ${
            isRecording ? "bg-coral text-white hover:bg-ink" : "bg-leaf text-white hover:bg-ink"
          }`}
        >
          {isRecording ? <Square className="h-4 w-4" aria-hidden="true" /> : <Mic className="h-4 w-4" aria-hidden="true" />}
          {isProcessing ? "Menyimpan" : isRecording ? "Berhenti" : "Rekam"}
        </button>

        {isRecording ? <VoiceWaveform level={recorder.micLevel} label="" /> : null}

        {recordingUrl && !isRecording && !isProcessing ? (
          <button
            type="button"
            onClick={playRecording}
            className="focus-ring inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-ink/15 px-3 text-sm font-semibold hover:bg-mint"
          >
            <Play className="h-4 w-4" aria-hidden="true" />
            Dengar rekaman
          </button>
        ) : null}
      </div>

      {error ? <p className="mt-3 text-xs leading-5 text-coral">{error}</p> : null}
    </div>
  );
}

