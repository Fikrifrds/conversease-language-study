import Link from "next/link";
import { ArrowRight, Lock, Unlock } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { course } from "@/lib/data";

export default function CoursesPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase text-leaf">Curriculum</p>
          <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">English conversation path</h1>
          <p className="mt-3 leading-7 text-ink/70">
            A1 is active for MVP. The system is ready for A2 and future languages without exposing
            them before content is prepared.
          </p>
        </div>

        <div className="mt-8 grid gap-5 lg:grid-cols-[0.85fr_1.15fr]">
          <Link
            href={`/courses/${course.slug}`}
            className="focus-ring rounded-lg border border-ink/10 bg-white p-5 shadow-sm hover:border-leaf/40"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <span className="rounded-lg bg-mint px-3 py-1 text-xs font-bold text-leaf">{course.level}</span>
                <h2 className="mt-4 text-2xl font-semibold">{course.title}</h2>
                <p className="mt-3 leading-7 text-ink/70">{course.outcome}</p>
              </div>
              <ArrowRight className="h-5 w-5 text-leaf" aria-hidden="true" />
            </div>
          </Link>

          <div className="grid gap-4 md:grid-cols-2">
            {["A2 Everyday Conversations", "B1 Confident Common Situations", "B2 Professional Conversations", "C1 Fluent Communication"].map((title) => (
              <div key={title} className="rounded-lg border border-ink/10 bg-white p-5 text-ink/70">
                <Lock className="h-5 w-5 text-coral" aria-hidden="true" />
                <h3 className="mt-4 font-semibold text-ink">{title}</h3>
                <p className="mt-2 text-sm">Coming soon</p>
              </div>
            ))}
          </div>
        </div>

        <section className="mt-8 rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-2">
            <Unlock className="h-5 w-5 text-leaf" aria-hidden="true" />
            <h2 className="text-lg font-semibold">A1 Unit Structure</h2>
          </div>
          <div className="mt-5 grid gap-3 md:grid-cols-5">
            {course.units.map((unit, index) => (
              <Link
                key={unit.title}
                href={`/courses/${course.slug}`}
                className="focus-ring rounded-lg bg-paper p-4 hover:bg-mint"
              >
                <span className="text-xs font-semibold text-coral">Unit {index + 1}</span>
                <h3 className="mt-2 font-semibold">{unit.title}</h3>
                <p className="mt-2 text-sm leading-6 text-ink/60">{unit.outcome}</p>
              </Link>
            ))}
          </div>
        </section>
      </section>
    </AppShell>
  );
}
