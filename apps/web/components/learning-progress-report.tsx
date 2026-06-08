"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { BookOpen, CheckCircle2, CircleDot } from "lucide-react";
import { getLearningProgress, type LearningProgressSummary } from "@/lib/learning-api";
import { lessonPlacementLabel } from "@/lib/data";

export function LearningProgressReport() {
  const [summary, setSummary] = useState<LearningProgressSummary | null>(null);

  useEffect(() => {
    let ignore = false;

    async function loadSummary() {
      try {
        const nextSummary = await getLearningProgress();

        if (!ignore) {
          setSummary(nextSummary);
        }
      } catch {
        if (!ignore) {
          setSummary(null);
        }
      }
    }

    loadSummary();

    return () => {
      ignore = true;
    };
  }, []);

  const completionPercent = summary?.course.completionPercent ?? 0;

  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-2">
        <BookOpen className="h-5 w-5 text-leaf" aria-hidden="true" />
        <h2 className="text-xl font-semibold">Progress Belajar</h2>
      </div>
      <div className="mt-6">
        <div className="mb-2 flex items-center justify-between text-sm">
          <span className="font-medium">{summary?.course.title ?? "Start Simple Conversations"}</span>
          <span>{completionPercent}%</span>
        </div>
        <div className="h-3 rounded-lg bg-ink/10">
          <div className="h-3 rounded-lg bg-leaf" style={{ width: `${completionPercent}%` }} />
        </div>
      </div>
      <div className="mt-5 space-y-3">
        {(summary?.lessons ?? []).map((lesson) => {
          const completed = lesson.progressStatus === "completed";

          return (
            <Link
              key={lesson.slug}
              href={`/lessons/${lesson.slug}`}
              className="focus-ring flex items-start justify-between gap-4 rounded-lg bg-paper p-4 hover:bg-mint"
            >
              <div>
                <p className="text-xs font-semibold uppercase text-coral">
                  {lessonPlacementLabel(lesson.slug) ?? lesson.unitTitle}
                </p>
                <h3 className="mt-1 font-semibold">{lesson.title}</h3>
                <p className="mt-1 text-sm text-ink/60">
                  {completed ? "Selesai" : lesson.progressStatus === "in_progress" ? "Sedang berjalan" : "Belum mulai"}
                </p>
              </div>
              {completed ? (
                <CheckCircle2 className="mt-1 h-5 w-5 shrink-0 text-leaf" aria-hidden="true" />
              ) : (
                <CircleDot className="mt-1 h-5 w-5 shrink-0 text-coral" aria-hidden="true" />
              )}
            </Link>
          );
        })}
      </div>
      {!summary ? (
        <p className="mt-5 text-sm leading-6 text-ink/60">Progress belajar sedang dimuat.</p>
      ) : null}
    </section>
  );
}
