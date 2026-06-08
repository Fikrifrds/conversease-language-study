import { MessageCircle } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { ActionButton } from "@/components/action-button";
import { DashboardLearningProgress } from "@/components/dashboard-learning-progress";
import { DashboardReviewToday } from "@/components/dashboard-review-today";
import { DashboardRecommendedLessons } from "@/components/dashboard-recommended-lessons";
import { PracticeProgressSummary } from "@/components/practice-progress-summary";

export default function DashboardPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-leaf">A1 Beginner</p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Misi Percakapan Hari Ini</h1>
          </div>
          <ActionButton href="/conversation-coach" icon={MessageCircle} tone="leaf">
            Latihan dengan Conversation Coach
          </ActionButton>
        </div>

        <DashboardLearningProgress />

        <div className="mt-5 grid items-start gap-5 lg:grid-cols-3">
          <PracticeProgressSummary />
          <DashboardReviewToday />
          <DashboardRecommendedLessons />
        </div>
      </section>
    </AppShell>
  );
}
