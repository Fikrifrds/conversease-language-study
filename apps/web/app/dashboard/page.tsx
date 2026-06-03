import Link from "next/link";
import { BookOpen, MessageCircle, TrendingUp } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { ActionButton } from "@/components/action-button";
import { DashboardLearningProgress } from "@/components/dashboard-learning-progress";
import { PracticeProgressSummary } from "@/components/practice-progress-summary";
import { progressScores } from "@/lib/data";

export default function DashboardPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-leaf">A1 Beginner</p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Today&apos;s Conversation Mission</h1>
          </div>
          <ActionButton href="/conversation-coach" icon={MessageCircle} tone="leaf">
            Practice with Conversation Coach
          </ActionButton>
        </div>

        <DashboardLearningProgress />

        <div className="mt-5">
          <PracticeProgressSummary />
        </div>

        <div className="mt-5 grid gap-5 lg:grid-cols-[0.85fr_1.15fr]">
          <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-leaf" aria-hidden="true" />
              <h2 className="text-lg font-semibold">Skill Scores</h2>
            </div>
            <div className="mt-5 space-y-4">
              {progressScores.map((score) => (
                <div key={score.label}>
                  <div className="mb-2 flex items-center justify-between text-sm">
                    <span className="font-medium">{score.label}</span>
                    <span>{score.value}</span>
                  </div>
                  <div className="h-2 rounded-lg bg-ink/10">
                    <div className="h-2 rounded-lg bg-coral" style={{ width: `${score.value}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <div className="flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-leaf" aria-hidden="true" />
              <h2 className="text-lg font-semibold">Next Recommended Lessons</h2>
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-3">
              {["Saying Your Name", "Asking Someone's Name", "Where Are You From"].map((title, index) => (
                <Link key={title} href="/courses/english-a1-start-simple-conversations" className="focus-ring rounded-lg bg-paper p-4 hover:bg-mint">
                  <span className="text-xs font-semibold text-coral">Lesson {index + 2}</span>
                  <h3 className="mt-2 font-semibold">{title}</h3>
                  <p className="mt-2 text-sm leading-6 text-ink/60">A1 Unit 1 practice path</p>
                </Link>
              ))}
            </div>
          </section>
        </div>
      </section>
    </AppShell>
  );
}
