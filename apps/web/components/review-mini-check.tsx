"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { ChevronDown, ChevronUp, Eye, Mic, Play, Square, Sparkles } from "lucide-react";
import { useVoiceRecorder } from "@/lib/use-voice-recorder";
import { VoiceWaveform } from "@/components/voice-waveform";
import type { ReviewContentMap, ReviewItem } from "@/lib/review-utils";

function stableIndex(seed: string, size: number) {
  if (size <= 0) {
    return 0;
  }
  let hash = 0;
  for (let i = 0; i < seed.length; i += 1) {
    hash = (hash * 31 + seed.charCodeAt(i)) >>> 0;
  }
  return hash % size;
}

function sampleDialogueCard(item: ReviewItem, seedKey: string, content: ReviewContentMap) {
  const lesson = content[item.lessonSlug];
  if (!lesson?.dialogue?.length) {
    return null;
  }
  const idx = stableIndex(`${seedKey}:dialogue`, lesson.dialogue.length);
  const line = lesson.dialogue[idx];
  const translation = lesson.translation[idx] ?? "";
  if (!line?.text || !translation) {
    return null;
  }
  return { prompt: line.text, answer: translation };
}

function sampleWritingExample(item: ReviewItem, seedKey: string, content: ReviewContentMap) {
  const lesson = content[item.lessonSlug];
  if (!lesson) {
    return null;
  }

  const writingExampleMatch = lesson.writingSupport.match(/```(?:txt)?\n([\s\S]*?)```/);
  if (writingExampleMatch?.[1]) {
    return writingExampleMatch[1].trim();
  }

  if (lesson.prompts.length) {
    const start = stableIndex(`${seedKey}:write-prompt`, lesson.prompts.length);
    const promptSlice = Array.from({ length: Math.min(3, lesson.prompts.length) }, (_, index) => {
      return lesson.prompts[(start + index) % lesson.prompts.length];
    }).filter(Boolean);

    if (promptSlice.length) {
      return promptSlice.join("\n");
    }
  }

  return item.pattern;
}

export function ReviewMiniCheck({
  items,
  seedKey,
  content
}: {
  items: ReviewItem[];
  seedKey: string;
  content: ReviewContentMap;
}) {
  const [open, setOpen] = useState(false);
  const [revealMeaning, setRevealMeaning] = useState(false);
  const [revealWriting, setRevealWriting] = useState(false);
  const [recordingUrl, setRecordingUrl] = useState<string | null>(null);
  const recordingUrlRef = useRef<string | null>(null);
  const [error, setError] = useState("");
  const [writing, setWriting] = useState("");

  const unitTitle = items[0]?.unitTitle ?? "Unit";
  const focusItem = items[0] ?? null;

  const meaningCard = useMemo(
    () => (focusItem ? sampleDialogueCard(focusItem, seedKey, content) : null),
    [focusItem, seedKey, content]
  );
  const writingExample = useMemo(
    () => (focusItem ? sampleWritingExample(focusItem, seedKey, content) : null),
    [focusItem, seedKey, content]
  );

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
    maxSeconds: 20,
    autoStopOnSilence: true
  });

  useEffect(() => {
    return () => {
      if (recordingUrlRef.current) {
        URL.revokeObjectURL(recordingUrlRef.current);
      }
    };
  }, []);

  function playRecording() {
    if (!recordingUrl) {
      return;
    }
    void new Audio(recordingUrl).play();
  }

  const isRecording = recorder.status === "recording";
  const isProcessing = recorder.status === "processing";

  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <button
        type="button"
        onClick={() => setOpen((current) => !current)}
        className="focus-ring flex w-full items-center justify-between gap-3 text-left"
      >
        <div>
          <p className="text-sm font-semibold uppercase text-leaf">Cek Singkat</p>
          <h2 className="mt-2 text-lg font-semibold">3 tugas ringan untuk {unitTitle}</h2>
          <p className="mt-2 text-sm leading-6 text-ink/60">Santai saja. Tidak ada nilai, tujuannya biar skill-nya “nempel”.</p>
        </div>
        {open ? <ChevronUp className="h-5 w-5 text-ink/60" aria-hidden="true" /> : <ChevronDown className="h-5 w-5 text-ink/60" aria-hidden="true" />}
      </button>

      {open ? (
        <div className="mt-5 space-y-4">
          <div className="rounded-lg bg-paper p-4">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-coral" aria-hidden="true" />
              <p className="font-semibold">1) Pahami</p>
            </div>
            {meaningCard ? (
              <>
                <p className="mt-3 text-sm leading-6 text-ink/70">{meaningCard.prompt}</p>
                {revealMeaning ? (
                  <p className="mt-3 text-sm font-semibold text-leaf">{meaningCard.answer}</p>
                ) : (
                  <button
                    type="button"
                    onClick={() => setRevealMeaning(true)}
                    className="focus-ring mt-3 inline-flex items-center gap-2 rounded-lg border border-ink/15 bg-white px-3 py-2 text-sm font-semibold hover:bg-mint"
                  >
                    <Eye className="h-4 w-4" aria-hidden="true" />
                    Pikirkan dulu, lalu cek arti
                  </button>
                )}
              </>
            ) : (
              <p className="mt-3 text-sm text-ink/60">Mulai satu lesson dulu untuk mengaktifkan cek singkat.</p>
            )}
          </div>

          <div className="rounded-lg bg-paper p-4">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-coral" aria-hidden="true" />
              <p className="font-semibold">2) Bicara</p>
            </div>
            <p className="mt-3 text-sm leading-6 text-ink/70">
              Rekam 1 jawaban singkat. Ucapkan pelan dan jelas.
              {focusItem?.pattern ? ` Gunakan pola: ${focusItem.pattern}` : ""}
            </p>

            <div className="mt-4 flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={isRecording ? () => recorder.stop() : () => void recorder.start()}
                disabled={isProcessing}
                className={`focus-ring inline-flex h-10 items-center justify-center gap-2 rounded-lg px-3 text-sm font-semibold disabled:cursor-not-allowed disabled:bg-ink/30 ${
                  isRecording ? "bg-coral text-white hover:bg-ink" : "bg-leaf text-white hover:bg-ink"
                }`}
              >
                {isRecording ? <Square className="h-4 w-4" aria-hidden="true" /> : <Mic className="h-4 w-4" aria-hidden="true" />}
                {isProcessing ? "Menyimpan…" : isRecording ? "Berhenti" : "Rekam"}
              </button>

              {isRecording ? <VoiceWaveform level={recorder.micLevel} label="" /> : null}

              {recordingUrl && !isRecording && !isProcessing ? (
                <button
                  type="button"
                  onClick={playRecording}
                  className="focus-ring inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-ink/15 px-3 text-sm font-semibold hover:bg-mint"
                >
                  <Play className="h-4 w-4" aria-hidden="true" />
                  Dengar
                </button>
              ) : null}
            </div>

            {error ? <p className="mt-3 text-xs leading-5 text-coral">{error}</p> : null}
          </div>

          <div className="rounded-lg bg-paper p-4">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-coral" aria-hidden="true" />
              <p className="font-semibold">3) Tulis</p>
            </div>
            <p className="mt-3 text-sm leading-6 text-ink/70">
              Tulis 2 kalimat singkat. Tidak perlu sempurna.
              {focusItem?.pattern ? ` Pakai pola: ${focusItem.pattern}` : ""}
            </p>
            <textarea
              value={writing}
              onChange={(event) => setWriting(event.target.value)}
              rows={4}
              className="focus-ring mt-3 w-full rounded-lg border border-ink/15 bg-white px-3 py-2 text-sm leading-6"
              placeholder="Tulis di sini…"
            />
            {revealWriting ? (
              writingExample ? <p className="mt-3 text-sm font-semibold text-leaf">Contoh: {writingExample}</p> : null
            ) : (
              <button
                type="button"
                onClick={() => setRevealWriting(true)}
                className="focus-ring mt-3 inline-flex items-center gap-2 rounded-lg border border-ink/15 bg-white px-3 py-2 text-sm font-semibold hover:bg-mint"
              >
                <Eye className="h-4 w-4" aria-hidden="true" />
                Lihat contoh singkat
              </button>
            )}
          </div>
        </div>
      ) : null}
    </section>
  );
}
