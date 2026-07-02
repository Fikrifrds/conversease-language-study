import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, BookOpen, CheckCircle2, MessageCircle, Layers3 } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { CourseProgressList } from "@/components/course-progress-list";
import { TrackGuard } from "@/components/track-guard";
import { versionedAssetSrc } from "@/lib/assets";
import { courseMarketingDescription } from "@/lib/course-marketing-copy";
import { courseHeroVisual } from "@/lib/course-visuals";
import { getVisualPlacementManifest } from "@/lib/course-visual-placement-api";
import { courses } from "@/lib/data";

type Course = (typeof courses)[number];

export function generateStaticParams() {
  return courses.map((course) => ({ slug: course.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const course = courses.find((item) => item.slug === params.slug);

  if (!course) {
    return { title: "Kurikulum tidak ditemukan", robots: { index: false, follow: false } };
  }

  // Keep Arabic courses out of search results while that track is coming-soon.
  if (course.language !== "english") {
    return { title: course.title, robots: { index: false, follow: false } };
  }

  return {
    title: `${course.title} (${course.level})`,
    description: courseMarketingDescription(course.slug, course.outcome),
    alternates: { canonical: `/courses/${course.slug}` }
  };
}

export default async function CourseDetailPage({ params }: { params: { slug: string } }) {
  const course = courses.find((item) => item.slug === params.slug);

  if (!course) {
    notFound();
  }
  const lessonCount = course.units.reduce((sum, unit) => sum + unit.lessons.length, 0);
  const visualManifest = await getVisualPlacementManifest();
  const visual = courseHeroVisual(course, visualManifest);
  const summaryItems = courseDetailSummary(course);

  return (
    <AppShell>
      <TrackGuard language={course.language}>
      <section className="mx-auto max-w-7xl px-4 pb-10 pt-8 sm:px-6 lg:px-8">
        <div className="overflow-hidden rounded-lg border border-ink/10 bg-white shadow-sm">
          <div className="grid gap-0 lg:grid-cols-[minmax(0,1fr)_420px]">
            <div className="p-5 md:p-7">
              <Link
                href="/courses"
                className="focus-ring mb-5 inline-flex items-center justify-center gap-2 rounded-lg border border-ink/10 bg-paper px-4 py-3 text-sm font-semibold text-ink hover:bg-mint"
              >
                <ArrowLeft className="h-4 w-4" aria-hidden="true" />
                Kembali ke Kurikulum
              </Link>
              <div className="flex flex-wrap gap-2">
                <span className="rounded-lg bg-mint px-3 py-1 text-xs font-bold uppercase text-leaf">
                  {course.languageLabel}
                </span>
                <span className="rounded-lg bg-paper px-3 py-1 text-xs font-bold uppercase text-ink/60">
                  Kursus {course.level}
                </span>
                <span className="inline-flex items-center gap-1 rounded-lg bg-[#fff2dc] px-3 py-1 text-xs font-bold uppercase text-coral">
                  <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" />
                  Siap
                </span>
              </div>
              <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">{course.title}</h1>
              <p className="mt-3 leading-7 text-ink/70">
                {courseMarketingDescription(course.slug, course.outcome)}
              </p>
              <div className="mt-5 grid gap-2 text-sm font-semibold text-ink/65 sm:grid-cols-3">
                <span className="inline-flex items-center gap-2 rounded-lg bg-paper px-3 py-3">
                  <Layers3 className="h-4 w-4 text-leaf" aria-hidden="true" />
                  {course.units.length} unit
                </span>
                <span className="inline-flex items-center gap-2 rounded-lg bg-paper px-3 py-3">
                  <BookOpen className="h-4 w-4 text-leaf" aria-hidden="true" />
                  {lessonCount} lesson
                </span>
                <span className="inline-flex items-center gap-2 rounded-lg bg-paper px-3 py-3">
                  <MessageCircle className="h-4 w-4 text-leaf" aria-hidden="true" />
                  Roleplay & audio
                </span>
              </div>
              <dl className="mt-5 grid gap-x-5 gap-y-3 border-t border-ink/10 pt-5 text-sm md:grid-cols-3">
                {summaryItems.map((item) => (
                  <div key={item.label} className="min-w-0">
                    <dt className="text-xs font-bold uppercase text-coral">{item.label}</dt>
                    <dd className="mt-1 leading-6 text-ink/70">{item.value}</dd>
                  </div>
                ))}
              </dl>
            </div>
            {visual ? (
              <div className="relative min-h-[240px] bg-paper lg:min-h-full">
                <Image
                  src={versionedAssetSrc(visual.src)}
                  alt={visual.alt}
                  fill
                  priority
                  sizes="(min-width: 1024px) 420px, 100vw"
                  className="object-cover"
                />
              </div>
            ) : null}
          </div>
        </div>

        <CourseProgressList course={course} visualManifest={visualManifest} />
      </section>
      </TrackGuard>
    </AppShell>
  );
}

function courseDetailSummary(course: Course) {
  const levelSummary: Record<string, string> = {
    A1: "Percakapan dasar yang aman untuk mulai bicara.",
    A2: "Situasi harian dengan respons yang lebih natural.",
    B1: "Cerita, alasan, dan solusi yang tersambung.",
    B2: "Diskusi profesional dengan argumen dan keputusan.",
    C1: "Komunikasi kompleks yang presisi dan fleksibel."
  };
  const firstThemes = course.units
    .slice(0, 3)
    .map((unit) => unit.title)
    .join(" · ");

  return [
    {
      label: "Level",
      value: levelSummary[course.level] ?? course.outcome
    },
    {
      label: "Fokus",
      value: firstThemes
    },
    {
      label: "Target",
      value: course.language === "arabic" ? "Bahasa Arab formal bertahap." : "Percakapan English aktif bertahap."
    }
  ];
}
