"use client";

import { useEffect, useState } from "react";
import { AlertCircle, Headphones, RefreshCcw } from "lucide-react";
import { ApiRequestError, getLessonAudio, type LearningLessonAudioAsset } from "@/lib/learning-api";

export function LessonAudioPlayer({ lessonSlug }: { lessonSlug: string }) {
  const [audio, setAudio] = useState<LearningLessonAudioAsset | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [canRetry, setCanRetry] = useState(true);

  async function loadAudio() {
    setIsLoading(true);
    setError("");
    setCanRetry(true);

    try {
      setAudio(await getLessonAudio(lessonSlug));
    } catch (err) {
      if (err instanceof ApiRequestError && err.status === 403) {
        setError("Audio tersedia untuk Pro");
        setCanRetry(false);
      } else if (err instanceof ApiRequestError && err.status === 401) {
        setError("Login untuk memutar audio");
        setCanRetry(false);
      } else {
        setError("Audio belum bisa dimuat.");
      }
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
    if (!canRetry) {
      return (
        <div className="inline-flex min-h-10 items-center gap-2 rounded-lg bg-paper px-3 text-sm font-semibold text-ink/55">
          <AlertCircle className="h-4 w-4 text-coral" aria-hidden="true" />
          {error}
        </div>
      );
    }

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
    <div className="w-full min-w-0 max-w-sm rounded-lg bg-paper p-2 sm:min-w-[260px]">
      <audio
        controls
        preload="metadata"
        src={audio.playbackUrl}
        className="h-10 w-full"
        aria-label="Listening dialogue audio"
      />
    </div>
  );
}
