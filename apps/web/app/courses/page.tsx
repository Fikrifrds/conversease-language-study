"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { ArrowRight, BookOpen, CheckCircle2, Languages, Layers3 } from "lucide-react";
import { isLanguageVisible } from "@conversease/shared";
import { AppShell } from "@/components/app-shell";
import { getAuthSession } from "@/lib/auth-api";
import { versionedAssetSrc } from "@/lib/assets";
import { courseGroupDescriptions, courseMarketingDescription } from "@/lib/course-marketing-copy";
import { courseHeroVisuals } from "@/lib/course-visuals";
import {
  getVisualPlacementManifest,
  type VisualPlacementManifest
} from "@/lib/course-visual-placement-api";
import { courses } from "@/lib/data";

type LanguageFilter = "all" | "english" | "arabic";
type Course = (typeof courses)[number];

const allLanguageFilters: Array<{ key: LanguageFilter; label: string }> = [
  { key: "all", label: "Semua" },
  { key: "english", label: "English" },
  { key: "arabic", label: "Arabic" }
];

export default function CoursesPage() {
  const [languageFilter, setLanguageFilter] = useState<LanguageFilter>("all");
  const [isAdmin, setIsAdmin] = useState(false);
  const [visualManifest, setVisualManifest] = useState<VisualPlacementManifest | null>(null);

  useEffect(() => {
    setIsAdmin(getAuthSession()?.user.role === "admin");
    void getVisualPlacementManifest().then(setVisualManifest);
  }, []);

  // Coming-soon tracks (e.g. Arabic) are admin-only — hide their tab and group.
  const languageFilters = allLanguageFilters.filter(
    (item) => item.key === "all" || isLanguageVisible(item.key, isAdmin)
  );
  const visibleCourseGroups = groupedCourses(languageFilter).filter((group) =>
    isLanguageVisible(group.language, isAdmin)
  );

  return (
    <AppShell>
      <section className="mx-auto max-w-7xl px-4 pb-10 pt-8 sm:px-6 lg:px-8">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm md:p-7">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
            <div className="max-w-3xl">
              <p className="text-sm font-semibold uppercase text-leaf">Kurikulum</p>
              <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Jalur percakapan Conversease</h1>
              <p className="mt-3 leading-7 text-ink/70">
                Pilih track bahasa, lanjutkan level yang terbuka, dan belajar dari lesson yang sudah
                lengkap dengan dialog, latihan respons, roleplay, dan audio.
              </p>
            </div>

            <div className="flex flex-wrap gap-1 rounded-lg border border-ink/10 bg-paper p-1 lg:inline-flex lg:shrink-0">
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
                  <CourseCard key={course.slug} course={course} visualManifest={visualManifest} />
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

function CourseCard({
  course,
  visualManifest
}: {
  course: Course;
  visualManifest: VisualPlacementManifest | null;
}) {
  const badgeTone = course.language === "arabic" ? "bg-[#fff2dc] text-coral" : "bg-mint text-leaf";
  const lessonCount = course.units.reduce((sum, unit) => sum + unit.lessons.length, 0);
  const visuals = courseHeroVisuals(course, 3, visualManifest);

  return (
    <Link
      href={`/courses/${course.slug}`}
      className="focus-ring group flex min-h-[390px] flex-col overflow-hidden rounded-lg border border-ink/10 bg-white shadow-sm transition hover:border-leaf/40 hover:shadow-soft"
    >
      {visuals.length ? (
        <CourseVisualMosaic visuals={visuals} />
      ) : null}
      <div className="flex flex-1 flex-col p-5">
        <CourseCardHeader course={course} badgeTone={badgeTone} />
        <p className="mt-3 text-sm leading-6 text-ink/70">
          {courseMarketingDescription(course.slug, course.outcome)}
        </p>
        <div className="mt-5 grid grid-cols-2 gap-2 text-xs font-semibold text-ink/60">
          <span className="inline-flex items-center gap-2 rounded-lg bg-paper px-3 py-2">
            <Layers3 className="h-4 w-4 text-leaf" aria-hidden="true" />
            {course.units.length} unit
          </span>
          <span className="inline-flex items-center gap-2 rounded-lg bg-paper px-3 py-2">
            <BookOpen className="h-4 w-4 text-leaf" aria-hidden="true" />
            {lessonCount} lesson
          </span>
        </div>
        <div className="mt-auto flex items-center justify-between gap-3 pt-5">
          <p className="inline-flex items-center gap-2 text-xs font-semibold uppercase text-leaf">
            <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
            Lihat modul
          </p>
          <span className="inline-flex items-center gap-2 text-sm font-semibold text-leaf">
            Buka
            <ArrowRight className="h-5 w-5 transition group-hover:translate-x-0.5" aria-hidden="true" />
          </span>
        </div>
      </div>
    </Link>
  );
}

function CourseVisualMosaic({
  visuals
}: {
  visuals: Array<{ src: string; alt: string }>;
}) {
  const [primary, secondary, tertiary] = visuals;

  if (!secondary) {
    return (
      <div className="relative aspect-[16/9] overflow-hidden bg-paper">
        <Image
          src={versionedAssetSrc(primary.src)}
          alt={primary.alt}
          fill
          sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
          className="object-cover transition duration-300 group-hover:scale-[1.03]"
        />
      </div>
    );
  }

  return (
    <div className="grid aspect-[16/9] grid-cols-[1.35fr_0.85fr] gap-1 bg-paper p-1">
      <div className="relative overflow-hidden rounded-[6px]">
        <Image
          src={versionedAssetSrc(primary.src)}
          alt={primary.alt}
          fill
          sizes="(min-width: 1024px) 22vw, (min-width: 768px) 34vw, 70vw"
          className="object-cover transition duration-300 group-hover:scale-[1.03]"
        />
      </div>
      <div className="grid min-h-0 gap-1">
        {[secondary, tertiary ?? primary].map((visual, index) => (
          <div key={`${visual.src}-${index}`} className="relative min-h-0 overflow-hidden rounded-[6px]">
            <Image
              src={versionedAssetSrc(visual.src)}
              alt={visual.alt}
              fill
              sizes="(min-width: 1024px) 12vw, (min-width: 768px) 18vw, 30vw"
              className="object-cover transition duration-300 group-hover:scale-[1.03]"
            />
          </div>
        ))}
      </div>
    </div>
  );
}

function CourseCardHeader({
  course,
  badgeTone
}: {
  course: Course;
  badgeTone: string;
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
        </div>
        <h3 className="mt-4 break-words text-[1.45rem] font-semibold leading-tight text-ink">
          {course.title}
        </h3>
      </div>
    </div>
  );
}

function groupedCourses(languageFilter: LanguageFilter) {
  const groups = [
    {
      language: "english",
      title: "English Track",
      status: "Ready curriculum",
      description: courseGroupDescriptions.english,
      courses: courses.filter((course) => course.language === "english")
    },
    {
      language: "arabic",
      title: "Arabic Track",
      status: "Ready curriculum",
      description: courseGroupDescriptions.arabic,
      courses: courses.filter((course) => course.language === "arabic")
    }
  ];
  return groups.filter((group) => languageFilter === "all" || group.language === languageFilter);
}
