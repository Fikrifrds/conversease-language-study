"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowRight, CheckCircle2, CircleDot } from "lucide-react";
import { getLearningProgress, type LearningProgressSummary } from "@/lib/learning-api";
import { course as defaultCourse, type courses } from "@/lib/data";

type Course = (typeof courses)[number];

export function CourseProgressList({ course = defaultCourse }: { course?: Course }) {
  const [summary, setSummary] = useState<LearningProgressSummary | null>(null);

  useEffect(() => {
    let ignore = false;

    async function loadProgress() {
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

    loadProgress();

    return () => {
      ignore = true;
    };
  }, []);

  const progressBySlug = useMemo(
    () => new Map((summary?.lessons ?? []).map((lesson) => [lesson.slug, lesson])),
    [summary]
  );

  return (
    <div className="mt-8 space-y-4">
      {course.units.map((unit, unitIndex) => {
        const publishedLessons = unit.lessons.filter((lesson) => lesson.status === "published");
        const completedLessons = publishedLessons.filter(
          (lesson) => progressBySlug.get(lesson.slug)?.progressStatus === "completed"
        ).length;
        const progressPercent = publishedLessons.length
          ? Math.round((completedLessons / publishedLessons.length) * 100)
          : 0;

        return (
          <section
            key={unit.title}
            id={`unit-${unitIndex + 1}`}
            className="scroll-mt-24 rounded-lg border border-ink/10 bg-white p-5 shadow-sm"
          >
            <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              <div>
                <span className="text-xs font-semibold uppercase text-coral">Unit {unitIndex + 1}</span>
                <h2 className="mt-2 text-xl font-semibold">{unit.title}</h2>
                <p className="mt-2 text-sm leading-6 text-ink/70">{unit.outcome}</p>
              </div>
              <div className="w-full max-w-xs">
                <div className="mb-2 flex justify-between text-sm">
                  <span>Progress</span>
                  <span>{progressPercent}%</span>
                </div>
                <div className="h-2 rounded-lg bg-ink/10">
                  <div className="h-2 rounded-lg bg-leaf" style={{ width: `${progressPercent}%` }} />
                </div>
              </div>
            </div>

            {unit.lessons.length ? (
              <div className="mt-5 grid gap-3 md:grid-cols-3">
                {unit.lessons.map((lesson) => {
                  const lessonProgress = progressBySlug.get(lesson.slug);
                  const completed = lessonProgress?.progressStatus === "completed";
                  const inProgress = lessonProgress?.progressStatus === "in_progress";

                  return (
                    <Link
                      key={lesson.slug}
                      href={`/lessons/${lesson.slug}`}
                      className="focus-ring rounded-lg bg-paper p-4 hover:bg-mint"
                    >
                      <div className="flex items-center justify-between gap-3">
                        <span className="text-xs font-semibold uppercase text-leaf">
                          {completed ? "selesai" : inProgress ? "sedang berjalan" : lesson.status}
                        </span>
                        {completed ? (
                          <CheckCircle2 className="h-4 w-4 text-leaf" aria-hidden="true" />
                        ) : inProgress ? (
                          <CircleDot className="h-4 w-4 text-coral" aria-hidden="true" />
                        ) : (
                          <ArrowRight className="h-4 w-4 text-ink/40" aria-hidden="true" />
                        )}
                      </div>
                      <h3 className="mt-3 font-semibold">{lesson.title}</h3>
                      <p className="mt-2 text-sm text-ink/60">{lesson.minutes} menit</p>
                    </Link>
                  );
                })}
              </div>
            ) : null}
          </section>
        );
      })}
    </div>
  );
}
