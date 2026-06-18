import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, BookOpen, CheckCircle2, Headphones, Layers3 } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { CourseProgressList } from "@/components/course-progress-list";
import { courses } from "@/lib/data";

export function generateStaticParams() {
  return courses.map((course) => ({ slug: course.slug }));
}

export default function CourseDetailPage({ params }: { params: { slug: string } }) {
  const course = courses.find((item) => item.slug === params.slug);

  if (!course) {
    notFound();
  }
  const lessonCount = course.units.reduce((sum, unit) => sum + unit.lessons.length, 0);

  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-10 pt-8 sm:px-6 lg:px-8">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm md:p-7">
          <div className="flex flex-col gap-6 md:flex-row md:items-start md:justify-between">
            <div className="max-w-3xl">
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
              <p className="mt-3 leading-7 text-ink/70">{course.outcome}</p>
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
                  <Headphones className="h-4 w-4 text-leaf" aria-hidden="true" />
                  Audio lengkap
                </span>
              </div>
            </div>
            <Link
              href="/courses"
              className="focus-ring inline-flex items-center justify-center gap-2 rounded-lg border border-ink/10 bg-paper px-4 py-3 text-sm font-semibold text-ink hover:bg-mint"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              Kembali ke Kurikulum
            </Link>
          </div>
        </div>

        <CourseProgressList course={course} />
      </section>
    </AppShell>
  );
}
