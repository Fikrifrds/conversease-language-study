"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { CalendarDays, Headphones, MessageCircle, Mic, Play, Target } from "lucide-react";
import { getBillingAccess, type BillingAccess } from "@/lib/billing-api";
import { getLearningProgress, type LearningProgressSummary } from "@/lib/learning-api";
import { mission, lessonPlacementLabel } from "@/lib/data";
import { WeeklyStreakIndicator } from "@/components/weekly-streak-indicator";

const fallbackMission = {
  slug: mission.lessonSlug,
  title: mission.title,
  conversationGoal: mission.goal,
  estimatedMinutes: mission.minutes,
  progressStatus: "not_started"
};

export function DashboardLearningProgress() {
  const [summary, setSummary] = useState<LearningProgressSummary | null>(null);
  const [access, setAccess] = useState<BillingAccess | null>(null);

  useEffect(() => {
    let ignore = false;

    async function loadDashboardData() {
      try {
        const [nextSummary, nextAccess] = await Promise.all([
          getLearningProgress(),
          getBillingAccess()
        ]);

        if (!ignore) {
          setSummary(nextSummary);
          setAccess(nextAccess);
        }
      } catch {
        if (!ignore) {
          setSummary(null);
          setAccess(null);
        }
      }
    }

    loadDashboardData();

    return () => {
      ignore = true;
    };
  }, []);

  const currentMission = summary?.currentMission ?? fallbackMission;
  const completionPercent = summary?.course.completionPercent ?? 0;
  const completedLessons = summary?.course.completedLessons ?? 0;
  const totalLessons = summary?.course.totalLessons ?? 1;
  const dailyTarget = summary?.onboarding?.dailyTargetMinutes;
  const primaryGoal = summary?.onboarding?.primaryGoal;

  return (
    <div className="mt-8 grid items-start gap-5 lg:grid-cols-[1.15fr_0.85fr]">
      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm sm:p-6">
        <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm font-semibold text-coral">
              {lessonPlacementLabel(currentMission.slug) ?? "A1 Unit 1"}
            </p>
            <h2 className="mt-2 text-2xl font-semibold">{currentMission.title}</h2>
            {primaryGoal ? (
              <span className="mt-3 inline-flex items-center gap-1 rounded-lg bg-[#fff2dc] px-3 py-1 text-xs font-semibold text-ink/70">
                <Target className="h-3 w-3 text-coral" aria-hidden="true" />
                Tujuanmu: {primaryGoal}
              </span>
            ) : null}
            <p className="mt-3 max-w-2xl leading-7 text-ink/70">
              {currentMission.conversationGoal}
            </p>
          </div>
          <div className="flex w-full items-center justify-between rounded-lg bg-mint px-4 py-3 text-center sm:grid sm:h-24 sm:w-24 sm:shrink-0 sm:place-items-center md:self-start">
            <span className="text-3xl font-semibold leading-none">{currentMission.estimatedMinutes}</span>
            <span className="text-xs font-semibold text-ink/60 sm:-mt-5">menit</span>
          </div>
        </div>
        <div className="mt-6 grid gap-3 sm:grid-cols-3">
          {[
            { label: "Dengar", detail: "Audio dialog", icon: Headphones },
            { label: "Ulangi", detail: "Frasa berguna", icon: Mic },
            { label: "Respons", detail: "Prompt singkat", icon: MessageCircle }
          ].map((item) => (
            <div key={item.label} className="rounded-lg bg-paper p-4">
              <item.icon className="h-5 w-5 text-leaf" aria-hidden="true" />
              <p className="mt-3 font-semibold">{item.label}</p>
              <p className="text-sm text-ink/60">{item.detail}</p>
            </div>
          ))}
        </div>
        <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center">
          <Link
            href={`/lessons/${currentMission.slug}`}
            className="focus-ring inline-flex items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf"
          >
            <Play className="h-4 w-4" aria-hidden="true" />
            {currentMission.progressStatus === "completed" ? "Tinjau Lesson" : "Lanjutkan Lesson"}
          </Link>

          <Link
            href={`/conversation-coach?scenario=${encodeURIComponent(currentMission.slug)}`}
            className="focus-ring inline-flex items-center gap-2 text-sm font-semibold text-leaf hover:text-ink"
          >
            <MessageCircle className="h-4 w-4" aria-hidden="true" />
            Latihan Coach untuk misi ini
          </Link>
        </div>
      </section>

      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm sm:p-6">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-leaf">Progress jalur belajar</p>
            <h2 className="mt-1 text-3xl font-semibold">{completionPercent}%</h2>
          </div>
          <Target className="h-8 w-8 text-coral" aria-hidden="true" />
        </div>
        <div className="mt-5 h-3 overflow-hidden rounded-lg bg-ink/10">
          <div className="h-full rounded-lg bg-leaf" style={{ width: `${completionPercent}%` }} />
        </div>
        <p className="mt-3 text-sm text-ink/60">
          {completedLessons}/{totalLessons} lesson selesai.
        </p>
        <div className="mt-6 grid gap-3 sm:grid-cols-2">
          <Link href="/progress" className="focus-ring rounded-lg bg-mint px-4 py-3 text-center text-sm font-semibold">
            Lihat Progress
          </Link>
          <Link href="/onboarding" className="focus-ring rounded-lg bg-[#fff2dc] px-4 py-3 text-center text-sm font-semibold">
            {dailyTarget ? `${dailyTarget} mnt/hari` : "Atur Target"}
          </Link>
        </div>

        <WeeklyStreakIndicator />

        <div className="mt-5 rounded-lg bg-paper p-4">
          <div className="flex items-center gap-2">
            <CalendarDays className="h-4 w-4 text-leaf" aria-hidden="true" />
            <p className="text-sm font-semibold">Kuota Conversation Coach</p>
          </div>
          <p className="mt-2 text-2xl font-semibold">{access?.minutes.totalMinutes ?? "-"}</p>
          <p className="mt-1 text-sm text-ink/60">
            {access?.isPro ? "Sisa kuota Pro dan top-up bulan ini." : "Sisa trial Free dan top-up aktif."}
          </p>
        </div>
      </section>
    </div>
  );
}
