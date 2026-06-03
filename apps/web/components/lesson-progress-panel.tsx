"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { CheckCircle2, CircleDot, Loader2 } from "lucide-react";
import {
  completeLessonProgress,
  getLessonProgress,
  startLessonProgress,
  type LessonProgress
} from "@/lib/learning-api";

export function LessonProgressPanel({
  lessonSlug,
  sections
}: {
  lessonSlug: string;
  sections: string[];
}) {
  const [progress, setProgress] = useState<LessonProgress | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCompleting, setIsCompleting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let ignore = false;

    async function ensureStarted() {
      try {
        const existing = await getLessonProgress(lessonSlug);
        const nextProgress = existing ?? (await startLessonProgress(lessonSlug));

        if (!ignore) {
          setProgress(nextProgress);
        }
      } catch {
        if (!ignore) {
          setError("Progress lesson belum tersambung.");
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }

    ensureStarted();

    return () => {
      ignore = true;
    };
  }, [lessonSlug]);

  async function handleComplete() {
    setError("");
    setIsCompleting(true);

    try {
      const nextProgress = await completeLessonProgress(lessonSlug, sections);
      setProgress(nextProgress);
    } catch {
      setError("Lesson belum bisa ditandai selesai.");
    } finally {
      setIsCompleting(false);
    }
  }

  const completed = progress?.status === "completed";

  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-2">
        {completed ? (
          <CheckCircle2 className="h-5 w-5 text-leaf" aria-hidden="true" />
        ) : isLoading ? (
          <Loader2 className="h-5 w-5 animate-spin text-leaf" aria-hidden="true" />
        ) : (
          <CircleDot className="h-5 w-5 text-coral" aria-hidden="true" />
        )}
        <h2 className="font-semibold">Lesson Progress</h2>
      </div>
      <p className="mt-3 text-sm leading-6 text-ink/60">
        {completed
          ? "Lesson ini sudah tersimpan sebagai selesai."
          : "Progress lesson tersimpan otomatis saat halaman dibuka."}
      </p>
      {error ? <p className="mt-3 rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{error}</p> : null}
      <button
        type="button"
        onClick={handleComplete}
        disabled={completed || isCompleting || isLoading}
        className="focus-ring mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:bg-ink/30"
      >
        <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
        {completed ? "Completed" : isCompleting ? "Saving" : "Mark Lesson Complete"}
      </button>
      {completed ? (
        <Link
          href="/progress"
          className="focus-ring mt-3 inline-flex w-full items-center justify-center rounded-lg bg-mint px-4 py-3 text-sm font-semibold hover:bg-[#fff2dc]"
        >
          View Progress
        </Link>
      ) : null}
    </section>
  );
}
