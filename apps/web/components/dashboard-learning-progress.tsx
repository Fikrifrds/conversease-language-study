"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { CalendarDays, Headphones, MessageCircle, Mic, Play, Target } from "lucide-react";
import { getBillingAccess, type BillingAccess } from "@/lib/billing-api";
import { getLearningProgress, type LearningProgressSummary } from "@/lib/learning-api";
import { mission } from "@/lib/data";

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

  return (
    <div className="mt-8 grid gap-5 lg:grid-cols-[1.15fr_0.85fr]">
      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm font-semibold text-coral">A1 Unit 1</p>
            <h2 className="mt-2 text-2xl font-semibold">{currentMission.title}</h2>
            <p className="mt-3 max-w-2xl leading-7 text-ink/70">
              {currentMission.conversationGoal}
            </p>
          </div>
          <div className="grid h-24 w-24 place-items-center rounded-lg bg-mint text-center">
            <span className="text-3xl font-semibold">{currentMission.estimatedMinutes}</span>
            <span className="-mt-5 text-xs font-semibold text-ink/60">minutes</span>
          </div>
        </div>
        <div className="mt-6 grid gap-3 sm:grid-cols-3">
          {[
            { label: "Listen", detail: "Dialogue audio", icon: Headphones },
            { label: "Repeat", detail: "Useful phrases", icon: Mic },
            { label: "Respond", detail: "Short prompt", icon: MessageCircle }
          ].map((item) => (
            <div key={item.label} className="rounded-lg bg-paper p-4">
              <item.icon className="h-5 w-5 text-leaf" aria-hidden="true" />
              <p className="mt-3 font-semibold">{item.label}</p>
              <p className="text-sm text-ink/60">{item.detail}</p>
            </div>
          ))}
        </div>
        <Link
          href={`/lessons/${currentMission.slug}`}
          className="focus-ring mt-6 inline-flex items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf"
        >
          <Play className="h-4 w-4" aria-hidden="true" />
          {currentMission.progressStatus === "completed" ? "Review Lesson" : "Continue Lesson"}
        </Link>
      </section>

      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-leaf">Learning path progress</p>
            <h2 className="mt-1 text-3xl font-semibold">{completionPercent}%</h2>
          </div>
          <Target className="h-8 w-8 text-coral" aria-hidden="true" />
        </div>
        <div className="mt-5 h-3 overflow-hidden rounded-lg bg-ink/10">
          <div className="h-full rounded-lg bg-leaf" style={{ width: `${completionPercent}%` }} />
        </div>
        <p className="mt-3 text-sm text-ink/60">
          {completedLessons}/{totalLessons} published lesson selesai.
        </p>
        <div className="mt-6 grid grid-cols-2 gap-3">
          <Link href="/progress" className="focus-ring rounded-lg bg-mint px-4 py-3 text-center text-sm font-semibold">
            View Progress
          </Link>
          <Link href="/onboarding" className="focus-ring rounded-lg bg-[#fff2dc] px-4 py-3 text-center text-sm font-semibold">
            {dailyTarget ? `${dailyTarget} min/day` : "Set Target"}
          </Link>
        </div>

        <div className="mt-5 rounded-lg bg-paper p-4">
          <div className="flex items-center gap-2">
            <CalendarDays className="h-4 w-4 text-leaf" aria-hidden="true" />
            <p className="text-sm font-semibold">Conversation Coach quota</p>
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
