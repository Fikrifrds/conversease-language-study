"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, BookOpen, CheckCircle2, Languages, Lock, Sparkles } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { courses } from "@/lib/data";
import { listCourses, type CourseSummary } from "@/lib/learning-api";

type Access = { unlocked: boolean; requiresPro: boolean; accessible: boolean };
type LanguageFilter = "all" | "english" | "arabic";
type Course = (typeof courses)[number];

const languageFilters: Array<{ key: LanguageFilter; label: string }> = [
  { key: "all", label: "Semua" },
  { key: "english", label: "English" },
  { key: "arabic", label: "Arabic" }
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

  const visibleCourseGroups = groupedCourses(languageFilter);

  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase text-leaf">Kurikulum</p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Jalur percakapan Conversease</h1>
            <p className="mt-3 leading-7 text-ink/70">
              Pilih track bahasa, lanjutkan level yang terbuka, dan belajar dari lesson yang sudah
              lengkap dengan dialog, latihan respons, roleplay, dan audio.
            </p>
          </div>

          <div className="flex flex-wrap gap-1 rounded-lg border border-ink/10 bg-white p-1 shadow-sm lg:inline-flex lg:shrink-0">
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

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          <TrackSummaryCard
            title="English Track"
            status="Ready"
            description="A1 sampai C1 untuk percakapan umum, kerja, presentasi, dan diskusi profesional."
            courses={courses.filter((course) => course.language === "english")}
            active={languageFilter === "english"}
            onClick={() => setLanguageFilter("english")}
          />
          <TrackSummaryCard
            title="Arabic Track"
            status="Ready"
            description="Arabic formal A1 sampai C1 dengan dialog bertahap, harakat, audio, dan roleplay."
            courses={courses.filter((course) => course.language === "arabic")}
            active={languageFilter === "arabic"}
            onClick={() => setLanguageFilter("arabic")}
          />
        </div>

        <div className="mt-8 space-y-10">
          {visibleCourseGroups.map((group) => (
            <section key={group.language} className="space-y-4">
              <div className="flex flex-wrap items-end justify-between gap-3">
                <div>
                  <p className="text-xs font-semibold uppercase text-leaf">{group.status}</p>
                  <h2 className="mt-1 text-2xl font-semibold">{group.title}</h2>
                  <p className="mt-1 max-w-2xl text-sm leading-6 text-ink/60">{group.description}</p>
                </div>
                <p className="text-sm font-semibold text-ink/50">
                  {group.courses.length} level / {group.courses.reduce((sum, course) => sum + course.units.length, 0)} unit
                </p>
              </div>

              <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
                {group.courses.map((course) => (
                  <CourseCard
                    key={course.slug}
                    course={course}
                    access={courseAccess(course, accessBySlug)}
                    loaded={loaded}
                  />
                ))}
              </div>
            </section>
          ))}
          {!visibleCourseGroups.length ? (
            <p className="rounded-lg bg-paper p-5 text-sm text-ink/60">Belum ada course untuk filter ini.</p>
          ) : null}
        </div>
      </section>
    </AppShell>
  );
}

function TrackSummaryCard({
  title,
  status,
  description,
  courses: trackCourses,
  active,
  onClick
}: {
  title: string;
  status: string;
  description: string;
  courses: Course[];
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`focus-ring rounded-lg border p-5 text-left transition ${
        active ? "border-leaf bg-mint" : "border-ink/10 bg-white hover:border-leaf/40"
      }`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <p className="text-xs font-semibold uppercase text-leaf">{status}</p>
          <h2 className="mt-1 break-words text-xl font-semibold">{title}</h2>
          <p className="mt-2 break-words text-sm leading-6 text-ink/65">{description}</p>
        </div>
        <BookOpen className="h-5 w-5 shrink-0 text-leaf" aria-hidden="true" />
      </div>
      <p className="mt-4 text-xs font-semibold uppercase text-ink/45">
        {trackCourses.length} level / {trackCourses.reduce((sum, course) => sum + course.units.length, 0)} unit
      </p>
    </button>
  );
}

function CourseCard({
  course,
  access,
  loaded
}: {
  course: Course;
  access: Access & { prevLevel: string | null };
  loaded: boolean;
}) {
  const badgeTone = course.language === "arabic" ? "bg-[#fff2dc] text-coral" : "bg-mint text-leaf";
  const lessonCount = course.units.reduce((sum, unit) => sum + unit.lessons.length, 0);

  if (access.accessible) {
    return (
      <Link
        href={`/courses/${course.slug}`}
        className="focus-ring flex min-h-[260px] flex-col rounded-lg border border-ink/10 bg-white p-5 shadow-sm transition-colors hover:border-leaf/40"
      >
        <CourseCardHeader course={course} badgeTone={badgeTone} lessonCount={lessonCount} />
        <p className="mt-3 text-sm leading-6 text-ink/70">{course.outcome}</p>
        <div className="mt-auto flex items-center justify-between gap-3 pt-5">
          <p className="inline-flex items-center gap-2 text-xs font-semibold uppercase text-leaf">
            <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
            Siap dipelajari
          </p>
          <span className="inline-flex items-center gap-2 text-sm font-semibold text-leaf">
            Buka
            <ArrowRight className="h-5 w-5" aria-hidden="true" />
          </span>
        </div>
      </Link>
    );
  }

  const lockedForPro = access.requiresPro && access.unlocked;
  return (
    <div
      className="flex min-h-[260px] flex-col rounded-lg border border-ink/10 bg-white p-5 text-ink/60 shadow-sm"
      aria-disabled="true"
    >
      <CourseCardHeader course={course} badgeTone="bg-paper text-ink/55" lessonCount={lessonCount} muted />
      <p className="mt-3 text-sm leading-6">{course.outcome}</p>
      <div className="mt-auto pt-5">
        {!loaded ? (
          <p className="text-xs font-semibold uppercase text-ink/40">Memeriksa akses...</p>
        ) : lockedForPro ? (
          <Link
            href="/pricing"
            className="focus-ring inline-flex items-center gap-2 rounded-lg bg-ink px-4 py-2 text-sm font-semibold text-white hover:bg-leaf"
          >
            <Sparkles className="h-4 w-4" aria-hidden="true" />
            Upgrade ke Pro
          </Link>
        ) : (
          <p className="inline-flex items-center gap-2 text-xs font-semibold uppercase text-coral">
            <Lock className="h-4 w-4" aria-hidden="true" />
            Selesaikan {access.prevLevel} dulu
          </p>
        )}
      </div>
    </div>
  );
}

function CourseCardHeader({
  course,
  badgeTone,
  lessonCount,
  muted = false
}: {
  course: Course;
  badgeTone: string;
  lessonCount: number;
  muted?: boolean;
}) {
  return (
    <div className="flex items-start justify-between gap-4">
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap gap-2">
          <span className={`rounded-lg px-3 py-1 text-xs font-bold ${badgeTone}`}>
            {course.languageLabel}
          </span>
          <span className="rounded-lg bg-paper px-3 py-1 text-xs font-bold text-ink/60">
            {course.level}
          </span>
          <span className="rounded-lg bg-paper px-3 py-1 text-xs font-bold text-ink/60">
            {course.units.length} unit
          </span>
          <span className="rounded-lg bg-paper px-3 py-1 text-xs font-bold text-ink/60">
            {lessonCount} lesson
          </span>
        </div>
        <h3 className={`mt-4 break-words text-2xl font-semibold ${muted ? "text-ink/70" : "text-ink"}`}>
          {course.title}
        </h3>
      </div>
    </div>
  );
}

function courseAccess(course: Course, accessBySlug: Record<string, Access>): Access & { prevLevel: string | null } {
  const courseIndex = courses.findIndex((item) => item.slug === course.slug);
  const access = accessBySlug[course.slug] ?? {
    unlocked: courseIndex === 0,
    requiresPro: courseIndex !== 0,
    accessible: courseIndex === 0
  };
  const languageCourses = courses.filter((item) => item.language === course.language);
  const languageIndex = languageCourses.findIndex((item) => item.slug === course.slug);
  return {
    ...access,
    prevLevel: languageIndex > 0 ? languageCourses[languageIndex - 1].level : null
  };
}

function groupedCourses(languageFilter: LanguageFilter) {
  const groups = [
    {
      language: "english",
      title: "English Track",
      status: "Ready curriculum",
      description: "Track utama untuk speaking dari A1 sampai C1.",
      courses: courses.filter((course) => course.language === "english")
    },
    {
      language: "arabic",
      title: "Arabic Track",
      status: "Ready curriculum",
      description: "Track Arabic formal lengkap dari A1 sampai C1 dengan audio dan roleplay.",
      courses: courses.filter((course) => course.language === "arabic")
    }
  ];
  return groups.filter((group) => languageFilter === "all" || group.language === languageFilter);
}
