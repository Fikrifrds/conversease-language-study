"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, Languages, Lock, Sparkles } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { courses } from "@/lib/data";
import { listCourses, type CourseSummary } from "@/lib/learning-api";

type Access = { unlocked: boolean; requiresPro: boolean; accessible: boolean };
type LanguageFilter = "all" | "english" | "arabic";

const languageFilters: Array<{ key: LanguageFilter; label: string }> = [
  { key: "all", label: "Semua" },
  { key: "english", label: "English" },
  { key: "arabic", label: "Arabic Fusha" }
];

export default function CoursesPage() {
  const [accessBySlug, setAccessBySlug] = useState<Record<string, Access>>({});
  const [loaded, setLoaded] = useState(false);
  const [languageFilter, setLanguageFilter] = useState<LanguageFilter>("all");

  useEffect(() => {
    let cancelled = false;
    listCourses()
      .then((summaries: CourseSummary[]) => {
        if (cancelled) {
          return;
        }
        setAccessBySlug(
          Object.fromEntries(
            summaries.map((c) => [
              c.slug,
              { unlocked: c.unlocked, requiresPro: c.requiresPro, accessible: c.accessible }
            ])
          )
        );
      })
      .catch(() => {
        if (!cancelled) {
          setAccessBySlug(
            courses.length
              ? { [courses[0].slug]: { unlocked: true, requiresPro: false, accessible: true } }
              : {}
          );
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

  const visibleCourses = courses.filter(
    (course) => languageFilter === "all" || course.language === languageFilter
  );

  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase text-leaf">Kurikulum</p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Jalur percakapan Conversease</h1>
            <p className="mt-3 leading-7 text-ink/70">
              English track aktif dari A1 sampai C1. Arabic Fusha sedang masuk fase beta: formal,
              bukan amiyah, untuk dialog umum, instruksi kelas, dan bacaan pendek.
            </p>
          </div>

          <div className="inline-flex rounded-lg border border-ink/10 bg-white p-1 shadow-sm">
            {languageFilters.map((item) => (
              <button
                key={item.key}
                type="button"
                onClick={() => setLanguageFilter(item.key)}
                className={`focus-ring inline-flex h-10 items-center gap-2 rounded-lg px-3 text-sm font-semibold transition ${
                  languageFilter === item.key
                    ? "bg-ink text-white"
                    : "text-ink/65 hover:bg-paper hover:text-ink"
                }`}
              >
                {item.key === "all" ? <Languages className="h-4 w-4" aria-hidden="true" /> : null}
                {item.label}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {visibleCourses.map((course) => {
            const courseIndex = courses.findIndex((item) => item.slug === course.slug);
            const access = accessBySlug[course.slug] ?? {
              unlocked: courseIndex === 0,
              requiresPro: courseIndex !== 0,
              accessible: courseIndex === 0
            };
            const languageCourses = courses.filter((item) => item.language === course.language);
            const languageIndex = languageCourses.findIndex((item) => item.slug === course.slug);
            const prevLevel = languageIndex > 0 ? languageCourses[languageIndex - 1].level : null;
            const isBeta = course.accessTier === "pro_beta" || course.units.some((unit) =>
              unit.lessons.some((lesson) => lesson.status === "beta")
            );

            // Accessible: clickable link.
            if (access.accessible) {
              return (
                <Link
                  key={course.slug}
                  href={`/courses/${course.slug}`}
                  className="focus-ring rounded-lg border border-ink/10 bg-white p-5 shadow-sm transition-colors hover:border-leaf/40"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="flex flex-wrap gap-2">
                        <span className="rounded-lg bg-mint px-3 py-1 text-xs font-bold text-leaf">
                          {course.languageLabel}
                        </span>
                        <span className="rounded-lg bg-paper px-3 py-1 text-xs font-bold text-ink/60">
                          {course.level}
                        </span>
                        {isBeta ? (
                          <span className="rounded-lg bg-[#fff2dc] px-3 py-1 text-xs font-bold text-coral">
                            Beta
                          </span>
                        ) : null}
                      </div>
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
            }

            // Locked: either needs Pro, or the previous level isn't finished.
            const lockedForPro = access.requiresPro && access.unlocked;
            return (
              <div
                key={course.slug}
                className="rounded-lg border border-ink/10 bg-white p-5 text-ink/60 shadow-sm"
                aria-disabled="true"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex flex-wrap gap-2">
                      <span className="rounded-lg bg-paper px-3 py-1 text-xs font-bold text-ink/55">
                        {course.languageLabel}
                      </span>
                      <span className="rounded-lg bg-paper px-3 py-1 text-xs font-bold text-ink/50">
                        {course.level}
                      </span>
                      {isBeta ? (
                        <span className="rounded-lg bg-[#fff2dc] px-3 py-1 text-xs font-bold text-coral">
                          Beta
                        </span>
                      ) : null}
                    </div>
                    <h2 className="mt-4 text-2xl font-semibold text-ink/70">{course.title}</h2>
                    <p className="mt-3 text-sm leading-6">{course.outcome}</p>
                  </div>
                  {lockedForPro ? (
                    <Sparkles className="h-5 w-5 shrink-0 text-coral" aria-hidden="true" />
                  ) : (
                    <Lock className="h-5 w-5 shrink-0 text-coral" aria-hidden="true" />
                  )}
                </div>

                {!loaded ? (
                  <p className="mt-4 text-xs font-semibold uppercase text-ink/40">Memeriksa akses…</p>
                ) : lockedForPro ? (
                  <Link
                    href="/pricing"
                    className="focus-ring mt-4 inline-flex items-center gap-2 rounded-lg bg-ink px-4 py-2 text-sm font-semibold text-white hover:bg-leaf"
                  >
                    <Sparkles className="h-4 w-4" aria-hidden="true" />
                    Upgrade ke Pro
                  </Link>
                ) : (
                  <p className="mt-4 text-xs font-semibold uppercase text-coral">
                    Selesaikan {prevLevel} dulu
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </section>
    </AppShell>
  );
}
