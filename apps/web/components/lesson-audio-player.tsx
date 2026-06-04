"use client";

import { useEffect, useState } from "react";
import { AlertCircle, Headphones, RefreshCcw } from "lucide-react";
import { getLessonAudio, type LearningLessonAudioAsset } from "@/lib/learning-api";

export function LessonAudioPlayer({ lessonSlug }: { lessonSlug: string }) {
  const [audio, setAudio] = useState<LearningLessonAudioAsset | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadAudio() {
    setIsLoading(true);
    setError("");

    try {
      setAudio(await getLessonAudio(lessonSlug));
    } catch {
      setError("Audio belum bisa dimuat.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadAudio();
    // Refreshes only when the lesson changes.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lessonSlug]);

  if (isLoading) {
    return (
      <div className="inline-flex min-h-10 items-center gap-2 rounded-lg bg-paper px-3 text-sm font-semibold text-ink/60">
        <Headphones className="h-4 w-4 text-leaf" aria-hidden="true" />
        Loading audio
      </div>
    );
  }

  if (error) {
    return (
      <button
        type="button"
        onClick={loadAudio}
        className="focus-ring inline-flex min-h-10 items-center gap-2 rounded-lg bg-[#fde7df] px-3 text-sm font-semibold text-coral hover:bg-mint"
      >
        <RefreshCcw className="h-4 w-4" aria-hidden="true" />
        Retry audio
      </button>
    );
  }

  if (!audio?.playbackUrl) {
    return (
      <div className="inline-flex min-h-10 items-center gap-2 rounded-lg bg-paper px-3 text-sm font-semibold text-ink/55">
        <AlertCircle className="h-4 w-4 text-coral" aria-hidden="true" />
        Audio pending
      </div>
    );
  }

  return (
    <div className="w-full min-w-[260px] max-w-sm rounded-lg bg-paper p-2">
      <audio controls preload="metadata" src={audio.playbackUrl} className="h-10 w-full" />
      <p className="mt-1 truncate px-1 text-xs text-ink/45">
        {audio.model || "audio"} / {audio.lineCount > 1 ? `${audio.lineCount} dialogue lines` : audio.voiceId || "voice"}
      </p>
    </div>
  );
}
