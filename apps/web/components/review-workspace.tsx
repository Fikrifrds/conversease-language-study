"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { BookOpen, Sparkles } from "lucide-react";
import { getLearningProgress, type LearningLessonSummary } from "@/lib/learning-api";
import { buildReviewItems, collectPatternBank, selectReviewLessonSlugs } from "@/lib/review-utils";
import { PatternDrill } from "@/components/pattern-drill";
import { ReviewMiniCheck } from "@/components/review-mini-check";

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

export function ReviewWorkspace() {
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
          const slugs = selectReviewLessonSlugs(summary.lessons, todayKey, 5);
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

  const completedSlugs = useMemo(
    () => (lessons ?? []).filter((lesson) => lesson.progressStatus === "completed").map((lesson) => lesson.slug),
    [lessons]
  );
  const patternBank = useMemo(() => collectPatternBank(completedSlugs, 30), [completedSlugs]);

  if (lessons === null) {
    return <p className="mt-8 text-sm leading-6 text-ink/60">Menyiapkan review…</p>;
  }

  return (
    <div className="mt-8 grid gap-5 lg:grid-cols-[1.05fr_0.95fr]">
      <div className="space-y-5">
        <ReviewMiniCheck items={items} seedKey={todayKey} />
      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-leaf" aria-hidden="true" />
          <h2 className="text-lg font-semibold">Review Tasks</h2>
        </div>
        <p className="mt-2 text-sm leading-6 text-ink/60">
          Ucapkan phrase-nya, lalu buat 1–2 kalimat baru memakai pattern yang sama.
        </p>

        {items.length ? (
          <div className="mt-4 space-y-3">
            {items.map((item) => (
              <div key={item.lessonSlug} className="rounded-lg bg-paper p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <p className="text-xs font-semibold uppercase text-ink/50">{item.unitTitle}</p>
                    <p className="mt-1 font-semibold">{item.lessonTitle}</p>
                  </div>
                  <Link
                    href={`/lessons/${item.lessonSlug}`}
                    className="focus-ring inline-flex items-center justify-center rounded-lg border border-ink/15 bg-white px-3 py-2 text-sm font-semibold hover:bg-mint"
                  >
                    Buka lesson
                  </Link>
                </div>

                <div className="mt-4 space-y-2 text-sm leading-6 text-ink/70">
                  <p>
                    <span className="font-semibold text-ink">Say:</span> {item.phrase}
                  </p>
                  {item.pattern ? (
                    <>
                      <p>
                        <span className="font-semibold text-ink">Pattern:</span> {item.pattern}
                      </p>
                      <PatternDrill pattern={item.pattern} seedKey={`${todayKey}:${item.lessonSlug}`} />
                    </>
                  ) : null}
                  <p className="text-ink/60">
                    Tantangan: buat 2 contoh kalimat baru (konteks lain) dengan pattern ini.
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="mt-4 text-sm leading-6 text-ink/60">Belum ada lesson untuk direview. Mulai 1 lesson dulu.</p>
        )}
      </section>
      </div>


      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex items-center gap-2">
          <BookOpen className="h-5 w-5 text-leaf" aria-hidden="true" />
        </div>
        <p className="mt-2 text-sm leading-6 text-ink/60">
          Kumpulan pola dari lesson yang sudah kamu selesaikan. Ini yang bikin kamu bisa pindah konteks dengan cepat.
        </p>

        {patternBank.length ? (
          <div className="mt-4 space-y-3">
            {patternBank.map((entry) => (
              <div key={entry.pattern} className="rounded-lg bg-paper p-4">
                <p className="font-semibold">{entry.pattern}</p>
                <Link href={`/lessons/${entry.lessonSlug}`} className="focus-ring mt-2 inline-flex text-sm font-semibold text-leaf hover:text-ink">
                  {entry.lessonTitle}
                </Link>
                <p className="mt-1 text-xs text-ink/50">{entry.unitTitle}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="mt-4 text-sm leading-6 text-ink/60">Selesaikan beberapa lesson untuk membangun Pattern Bank.</p>
        )}
      </section>
    </div>
  );
}
