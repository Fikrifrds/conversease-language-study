"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowRight, CheckCircle2, CircleDot, PlayCircle } from "lucide-react";
import { getCourseProgress, type LearningProgressSummary } from "@/lib/learning-api";
import { course as defaultCourse, type courses } from "@/lib/data";

type Course = (typeof courses)[number];

export function CourseProgressList({ course = defaultCourse }: { course?: Course }) {
  const [summary, setSummary] = useState<LearningProgressSummary | null>(null);

  useEffect(() => {
    let ignore = false;

    async function loadProgress() {
      try {
        const nextSummary = await getCourseProgress(course.slug);

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
  }, [course.slug]);

  const progressBySlug = useMemo(
    () => new Map((summary?.lessons ?? []).map((lesson) => [lesson.slug, lesson])),
    [summary]
  );

  return (
    <div className="mt-8 space-y-4">
      {course.units.map((unit, unitIndex) => {
        const activeLessons = unit.lessons.filter((lesson) => ["published", "beta"].includes(lesson.status));
        const completedLessons = activeLessons.filter(
          (lesson) => progressBySlug.get(lesson.slug)?.progressStatus === "completed"
        ).length;
        const progressPercent = activeLessons.length
          ? Math.round((completedLessons / activeLessons.length) * 100)
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

            {activeLessons.length ? (
              <div className="mt-5 grid gap-3 md:grid-cols-3">
                {activeLessons.map((lesson, lessonIndex) => {
                  const lessonProgress = progressBySlug.get(lesson.slug);
                  const completed = lessonProgress?.progressStatus === "completed";
                  const inProgress = lessonProgress?.progressStatus === "in_progress";
                  const statusLabel = completed ? "Selesai" : inProgress ? "Lanjutkan" : "Mulai";

                  return (
                    <Link
                      key={lesson.slug}
                      href={`/lessons/${lesson.slug}`}
                      className="focus-ring group rounded-lg bg-paper p-4 transition hover:bg-mint"
                    >
                      <div className="flex items-center justify-between gap-3">
                        <span className="text-xs font-semibold uppercase text-leaf">
                          {course.level} · U{unitIndex + 1} · L{lessonIndex + 1}
                        </span>
                        <span className="flex items-center gap-2">
                          <span className={`text-xs font-semibold uppercase ${
                            completed ? "text-leaf" : inProgress ? "text-coral" : "text-ink/45"
                          }`}>
                            {statusLabel}
                          </span>
                          {completed ? (
                            <CheckCircle2 className="h-4 w-4 text-leaf" aria-hidden="true" />
                          ) : inProgress ? (
                            <CircleDot className="h-4 w-4 text-coral" aria-hidden="true" />
                          ) : (
                            <PlayCircle className="h-4 w-4 text-ink/40 group-hover:text-leaf" aria-hidden="true" />
                          )}
                        </span>
                      </div>
                      <h3 className="mt-3 font-semibold text-ink">{lesson.title}</h3>
                      <div className="mt-3 flex items-center justify-between gap-3 text-sm text-ink/60">
                        <span>{lesson.minutes} menit</span>
                        <ArrowRight className="h-4 w-4 opacity-0 transition group-hover:translate-x-0.5 group-hover:opacity-100" aria-hidden="true" />
                      </div>
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
