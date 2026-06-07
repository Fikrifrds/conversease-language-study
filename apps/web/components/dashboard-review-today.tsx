"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";
import { getLearningProgress, type LearningLessonSummary } from "@/lib/learning-api";
import { buildReviewItems, selectReviewLessonSlugs } from "@/lib/review-utils";

function dateKeyForToday() {
  return new Date().toISOString().slice(0, 10);
}

type ReviewState = {
  slugs: string[];
};

function loadCachedReview(dateKey: string): ReviewState | null {
  if (typeof window === "undefined") {
    return null;
  }
  try {
    const raw = window.localStorage.getItem(`review.today.${dateKey}`);
    if (!raw) {
      return null;
    }
    const parsed = JSON.parse(raw) as ReviewState;
    if (!parsed?.slugs?.length) {
      return null;
    }
    return parsed;
  } catch {
    return null;
  }
}

function saveCachedReview(dateKey: string, state: ReviewState) {
  if (typeof window === "undefined") {
    return;
  }
  try {
    window.localStorage.setItem(`review.today.${dateKey}`, JSON.stringify(state));
  } catch {}
}

export function DashboardReviewToday() {
  const [lessons, setLessons] = useState<LearningLessonSummary[] | null>(null);
  const [reviewSlugs, setReviewSlugs] = useState<string[]>([]);

  const todayKey = useMemo(() => dateKeyForToday(), []);

  useEffect(() => {
    let ignore = false;

    async function load() {
      const cached = loadCachedReview(todayKey);
      if (cached?.slugs?.length) {
        setReviewSlugs(cached.slugs);
      }

      try {
        const summary = await getLearningProgress();
        if (ignore) {
          return;
        }
        setLessons(summary.lessons);
        if (!cached?.slugs?.length) {
          const slugs = selectReviewLessonSlugs(summary.lessons, todayKey, 3);
          setReviewSlugs(slugs);
          saveCachedReview(todayKey, { slugs });
        }
      } catch {
        if (!ignore) {
          setLessons([]);
        }
      }
    }

    load();

    return () => {
      ignore = true;
    };
  }, [todayKey]);

  const items = useMemo(() => buildReviewItems(reviewSlugs, todayKey), [reviewSlugs, todayKey]);
  const empty = lessons !== null && items.length === 0;

  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase text-leaf">Review Today</p>
          <h2 className="mt-2 text-lg font-semibold">Ulangi pattern dan phrase penting</h2>
        </div>
        <Sparkles className="h-5 w-5 text-coral" aria-hidden="true" />
      </div>

      {lessons === null ? (
        <p className="mt-4 text-sm leading-6 text-ink/60">Review harian sedang disiapkan.</p>
      ) : empty ? (
        <p className="mt-4 text-sm leading-6 text-ink/60">Belum ada lesson untuk direview. Mulai 1 lesson dulu.</p>
      ) : (
        <div className="mt-4 space-y-3">
          {items.map((item) => (
            <div key={item.lessonSlug} className="rounded-lg bg-paper p-4">
              <p className="text-xs font-semibold uppercase text-ink/50">{item.unitTitle}</p>
              <p className="mt-1 font-semibold">{item.lessonTitle}</p>
              <p className="mt-3 text-sm text-ink/70">
                <span className="font-semibold text-ink">Phrase:</span> {item.phrase}
              </p>
              {item.pattern ? (
                <p className="mt-2 text-sm text-ink/70">
                  <span className="font-semibold text-ink">Pattern:</span> {item.pattern}
                </p>
              ) : null}
            </div>
          ))}
        </div>
      )}

      <Link
        href="/review"
        className="focus-ring mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf"
      >
        Lihat review lengkap
        <ArrowRight className="h-4 w-4" aria-hidden="true" />
      </Link>
    </section>
  );
}

