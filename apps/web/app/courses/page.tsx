"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, Lock } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { courses } from "@/lib/data";
import { listCourses, type CourseSummary } from "@/lib/learning-api";

export default function CoursesPage() {
  const [unlockBySlug, setUnlockBySlug] = useState<Record<string, boolean>>({});
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    listCourses()
      .then((summaries: CourseSummary[]) => {
        if (cancelled) {
          return;
        }
        setUnlockBySlug(Object.fromEntries(summaries.map((c) => [c.slug, c.unlocked])));
      })
      .catch(() => {
        // If the call fails, default to only the first level unlocked.
        if (!cancelled) {
          setUnlockBySlug(courses.length ? { [courses[0].slug]: true } : {});
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoaded(true);
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase text-leaf">Curriculum</p>
          <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">English conversation path</h1>
          <p className="mt-3 leading-7 text-ink/70">
            Lima level dari A1 sampai C1. Selesaikan semua lesson di satu level untuk membuka level
            berikutnya.
          </p>
        </div>

        <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {courses.map((course, index) => {
            const unlocked = unlockBySlug[course.slug] ?? index === 0;
            const prevLevel = index > 0 ? courses[index - 1].level : null;

            if (!unlocked) {
              return (
                <div
                  key={course.slug}
                  className="rounded-lg border border-ink/10 bg-white p-5 text-ink/60 shadow-sm"
                  aria-disabled="true"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <span className="rounded-lg bg-paper px-3 py-1 text-xs font-bold text-ink/50">
                        {course.level}
                      </span>
                      <h2 className="mt-4 text-2xl font-semibold text-ink/70">{course.title}</h2>
                      <p className="mt-3 text-sm leading-6">{course.outcome}</p>
                    </div>
                    <Lock className="h-5 w-5 shrink-0 text-coral" aria-hidden="true" />
                  </div>
                  <p className="mt-4 text-xs font-semibold uppercase text-coral">
                    {loaded ? `Selesaikan ${prevLevel} dulu` : "Memeriksa akses…"}
                  </p>
                </div>
              );
            }

            return (
              <Link
                key={course.slug}
                href={`/courses/${course.slug}`}
                className="focus-ring rounded-lg border border-ink/10 bg-white p-5 shadow-sm transition-colors hover:border-leaf/40"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <span className="rounded-lg bg-mint px-3 py-1 text-xs font-bold text-leaf">
                      {course.level}
                    </span>
                    <h2 className="mt-4 text-2xl font-semibold">{course.title}</h2>
                    <p className="mt-3 text-sm leading-6 text-ink/70">{course.outcome}</p>
                  </div>
                  <ArrowRight className="h-5 w-5 shrink-0 text-leaf" aria-hidden="true" />
                </div>
                <p className="mt-4 text-xs font-semibold uppercase text-leaf">
                  {course.units.length} unit
                </p>
              </Link>
            );
          })}
        </div>
      </section>
    </AppShell>
  );
}
