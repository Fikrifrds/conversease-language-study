"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, BookOpen, CircleDot } from "lucide-react";
import { getLearningProgress, type LearningLessonSummary } from "@/lib/learning-api";

function statusLabel(status: LearningLessonSummary["progressStatus"]) {
  if (status === "completed") {
    return "Selesai";
  }
  if (status === "in_progress") {
    return "Sedang berjalan";
  }
  return "Belum mulai";
}

export function DashboardRecommendedLessons() {
  const [lessons, setLessons] = useState<LearningLessonSummary[] | null>(null);

  useEffect(() => {
    let ignore = false;

    async function loadLessons() {
      try {
        const summary = await getLearningProgress();

        if (!ignore) {
          setLessons(summary.lessons);
        }
      } catch {
        if (!ignore) {
          setLessons([]);
        }
      }
    }

    loadLessons();

    return () => {
      ignore = true;
    };
  }, []);

  const recommended = (lessons ?? [])
    .filter((lesson) => lesson.progressStatus !== "completed")
    .slice(0, 3);

  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-2">
        <BookOpen className="h-5 w-5 text-leaf" aria-hidden="true" />
        <h2 className="text-lg font-semibold">Lesson Berikutnya</h2>
      </div>

      {lessons === null ? (
        <p className="mt-4 text-sm leading-6 text-ink/60">Rekomendasi lesson sedang dimuat.</p>
      ) : recommended.length === 0 ? (
        <div className="mt-4 rounded-lg bg-mint p-4 text-sm leading-6 text-ink/70">
          Semua lesson aktif sudah selesai. Lanjut ke A1 Test untuk evaluasi level.
          <Link href="/level-test/A1" className="focus-ring mt-3 inline-flex items-center gap-2 font-semibold text-leaf hover:text-ink">
            Mulai A1 Test
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Link>
        </div>
      ) : (
        <div className="mt-4 grid gap-3 md:grid-cols-3">
          {recommended.map((lesson) => (
            <Link
              key={lesson.slug}
              href={`/lessons/${lesson.slug}`}
              className="focus-ring rounded-lg bg-paper p-4 hover:bg-mint"
            >
              <span className="inline-flex items-center gap-1 text-xs font-semibold text-coral">
                <CircleDot className="h-3 w-3" aria-hidden="true" />
                {statusLabel(lesson.progressStatus)}
              </span>
              <h3 className="mt-2 font-semibold">{lesson.title}</h3>
              <p className="mt-2 text-sm leading-6 text-ink/60">{lesson.conversationGoal}</p>
            </Link>
          ))}
        </div>
      )}
    </section>
  );
}
