import Link from "next/link";
import { Award, CheckCircle2 } from "lucide-react";
import { productRoutes } from "@conversease/shared";
import { AppShell } from "@/components/app-shell";
import { LearningProgressReport } from "@/components/learning-progress-report";
import { PracticeProgressSummary } from "@/components/practice-progress-summary";

export default function ProgressPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase text-leaf">Progress</p>
          <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">A1 conversation readiness</h1>
          <p className="mt-3 leading-7 text-ink/70">
            Passing A1 requires overall score 70, lesson completion 80%, and minimums for speaking and listening.
          </p>
        </div>

        <div className="mt-8 grid gap-5 lg:grid-cols-[0.72fr_0.28fr]">
          <LearningProgressReport />

          <aside className="space-y-4">
            <PracticeProgressSummary
              compact
              completedHref="/lessons/saying-hello-and-goodbye#conversation-coach"
              completedLabel="Review Lesson"
            />
            <section className="rounded-lg bg-ink p-5 text-white">
              <Award className="h-6 w-6 text-sun" aria-hidden="true" />
              <p className="mt-4 text-sm text-white/70">Projected result</p>
              <h2 className="mt-1 text-2xl font-semibold">Needs Review</h2>
              <p className="mt-3 text-sm leading-6 text-white/70">Speaking and useful phrases should improve before A1 test.</p>
              <Link
                href={productRoutes.levelTestA1}
                className="focus-ring mt-4 inline-flex w-full items-center justify-center rounded-lg bg-white px-4 py-3 text-sm font-semibold text-ink hover:bg-sun"
              >
                Open A1 Test
              </Link>
            </section>
            <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
              <CheckCircle2 className="h-5 w-5 text-leaf" aria-hidden="true" />
              <h2 className="mt-4 font-semibold">Review Plan</h2>
              <div className="mt-3 space-y-3 text-sm text-ink/70">
                <p>Repeat Unit 1 Lesson 1.</p>
                <p>Practice greeting roleplay for 10 minutes.</p>
                <p>Save 5 useful phrases.</p>
              </div>
            </section>
          </aside>
        </div>
      </section>
    </AppShell>
  );
}
