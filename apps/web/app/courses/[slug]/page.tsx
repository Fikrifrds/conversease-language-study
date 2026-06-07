import Link from "next/link";
import { notFound } from "next/navigation";
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

  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase text-leaf">{course.level} Course</p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">{course.title}</h1>
            <p className="mt-3 leading-7 text-ink/70">{course.outcome}</p>
          </div>
          <Link
            href="/dashboard"
            className="focus-ring inline-flex items-center justify-center rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf"
          >
            Back to Mission
          </Link>
        </div>

        <CourseProgressList course={course} />
      </section>
    </AppShell>
  );
}
