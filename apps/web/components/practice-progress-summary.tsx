"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { CheckCircle2, MessageCircle, Play, TrendingUp } from "lucide-react";
import { getLatestPractice } from "@/lib/conversation-api";
import { coachScenarios } from "@/lib/data";
import {
  practiceStorageKeyForLesson,
  readLatestSavedPractice,
  saveLatestPracticeSlug,
  saveSavedPractice,
  type SavedPractice
} from "@/lib/practice-storage";

type PracticeProgressSummaryProps = {
  compact?: boolean;
  completedHref?: string;
  completedLabel?: string;
  incompleteHref?: string;
  incompleteLabel?: string;
};

function formatUpdatedAt(value: string) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Baru saja";
  }

  return new Intl.DateTimeFormat("id-ID", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
}

export function PracticeProgressSummary({
  compact = false,
  completedHref = "/progress",
  completedLabel = "Lihat Progress",
  incompleteHref = "/conversation-coach",
  incompleteLabel = "Lanjutkan Roleplay"
}: PracticeProgressSummaryProps) {
  const [practice, setPractice] = useState<SavedPractice | null>(null);
  const [lessonSlug, setLessonSlug] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    let ignore = false;

    async function loadPractice() {
      const local = readLatestSavedPractice();
      setPractice(local?.practice ?? null);
      setLessonSlug(local?.lessonSlug ?? null);
      setMounted(true);

      try {
        if (!local?.lessonSlug) {
          return;
        }

        const apiPractice = await getLatestPractice(local.lessonSlug);

        if (ignore || !apiPractice) {
          return;
        }

        const nextPractice = {
          sessionId: apiPractice.sessionId,
          completedTurns: apiPractice.completedTurns,
          totalTurns: apiPractice.totalTurns,
          completed: apiPractice.completed,
          lastScore: apiPractice.lastScore,
          updatedAt: apiPractice.updatedAt
        };
        saveSavedPractice(nextPractice, practiceStorageKeyForLesson(local.lessonSlug));
        saveLatestPracticeSlug(local.lessonSlug);
        setPractice(nextPractice);
      } catch {
        setPractice(local?.practice ?? null);
      }
    }

    loadPractice();

    return () => {
      ignore = true;
    };
  }, []);

  const completionPercent = practice ? Math.round((practice.completedTurns / practice.totalTurns) * 100) : 0;
  const status = practice ? (practice.completed ? "Roleplay selesai" : "Sedang berjalan") : "Belum mulai";
  const readiness = practice
    ? practice.completed && practice.lastScore >= 70
      ? "Sesuai Target"
      : "Perlu Latihan"
    : "Mulai Latihan";
  const statusLabel = compact && practice?.completed ? "Selesai" : status;
  const readinessLabel = compact && readiness === "Sesuai Target" ? "Siap" : readiness;
  const nextHref = practice?.completed
    ? completedHref
    : lessonSlug
      ? `${incompleteHref}?scenario=${encodeURIComponent(lessonSlug)}`
      : incompleteHref;
  const nextLabel = practice?.completed ? completedLabel : incompleteLabel;
  const Icon = practice?.completed ? CheckCircle2 : Play;
  const scenarioTitle = lessonSlug ? coachScenarios.find((scenario) => scenario.slug === lessonSlug)?.label : null;

  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <p className="text-sm font-semibold uppercase text-leaf">Latihan Terakhir</p>
          <h2 className="mt-2 break-words text-xl font-semibold">
            {scenarioTitle ? `Roleplay: ${scenarioTitle}` : "Mulai roleplay pertama"}
          </h2>
        </div>
        <MessageCircle className="h-5 w-5 text-coral" aria-hidden="true" />
      </div>

      <div className={`mt-5 grid gap-3 ${compact ? "" : "sm:grid-cols-3"}`}>
        <div className="rounded-lg bg-paper p-3">
          <p className="text-xs font-semibold uppercase text-ink/50">Status</p>
          <p className="mt-1 font-semibold">{mounted ? statusLabel : "Memuat"}</p>
        </div>
        <div className="rounded-lg bg-paper p-3">
          <p className="text-xs font-semibold uppercase text-ink/50">Skor</p>
          <p className="mt-1 font-semibold">{practice ? practice.lastScore : "-"}</p>
        </div>
        <div className="rounded-lg bg-paper p-3">
          <p className="text-xs font-semibold uppercase text-ink/50">Kesiapan</p>
          <p className="mt-1 font-semibold">{readinessLabel}</p>
        </div>
      </div>

      <div className="mt-5">
        <div className="mb-2 flex items-center justify-between text-sm">
          <span className="font-medium">Giliran roleplay</span>
          <span>{practice ? `${practice.completedTurns}/${practice.totalTurns}` : "0/3"}</span>
        </div>
        <div className="h-3 overflow-hidden rounded-lg bg-ink/10">
          <div className="h-full rounded-lg bg-leaf" style={{ width: `${completionPercent}%` }} />
        </div>
      </div>

      <p className="mt-4 text-sm leading-6 text-ink/60">
        {practice
          ? `Terakhir latihan: ${formatUpdatedAt(practice.updatedAt)}. ${
              practice.completed
                ? "Lanjutkan dengan review phrase dan final check."
                : "Selesaikan semua turn agar feedback progress lebih lengkap."
            }`
          : "Mulai dari roleplay greeting untuk membuka feedback, skor, dan rekomendasi berikutnya."}
      </p>

      <Link
        href={nextHref}
        className="focus-ring mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf"
      >
        <Icon className="h-4 w-4" aria-hidden="true" />
        {nextLabel}
      </Link>

      {practice?.completed ? (
        <div className="mt-4 flex items-start gap-2 rounded-lg bg-mint p-3 text-sm leading-6 text-ink/70">
          <TrendingUp className="mt-0.5 h-4 w-4 shrink-0 text-leaf" aria-hidden="true" />
          Speaking readiness naik karena kamu sudah menyelesaikan guided roleplay.
        </div>
      ) : null}
    </section>
  );
}
