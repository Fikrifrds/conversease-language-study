"use client";

import { useEffect, useMemo, useState } from "react";
import { ClipboardCheck, KeyRound, RefreshCcw, Save } from "lucide-react";
import {
  listAdminLevelTestAttempts,
  scoreAdminLevelTestAttempt
} from "@/lib/admin-level-test-api";
import type { LevelTestAttempt } from "@/lib/learning-api";

const adminKeyStorageKey = "conversease.admin_key";
const reviewerStorageKey = "conversease.level_test_reviewer";
const statusOptions = [
  { label: "Submitted", value: "submitted" },
  { label: "Reviewed", value: "reviewed" },
  { label: "In Progress", value: "in_progress" },
  { label: "All", value: "" }
];

function formatDate(value: string | null) {
  if (!value) {
    return "-";
  }

  return new Intl.DateTimeFormat("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }).format(new Date(value));
}

function statusTone(status: string) {
  if (status === "reviewed") {
    return "bg-mint text-leaf";
  }
  if (status === "submitted") {
    return "bg-[#e8f0ff] text-[#1f3f91]";
  }
  return "bg-paper text-ink/70";
}

export function AdminLevelTestReviewManager() {
  const [apiKey, setApiKey] = useState("");
  const [reviewerName, setReviewerName] = useState("Admin");
  const [status, setStatus] = useState("submitted");
  const [attempts, setAttempts] = useState<LevelTestAttempt[]>([]);
  const [selectedAttempt, setSelectedAttempt] = useState<LevelTestAttempt | null>(null);
  const [scores, setScores] = useState<Record<string, number>>({});
  const [lessonCompletionPercent, setLessonCompletionPercent] = useState(80);
  const [notes, setNotes] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const storedKey = window.sessionStorage.getItem(adminKeyStorageKey);
    const storedReviewer = window.sessionStorage.getItem(reviewerStorageKey);
    if (storedKey) {
      setApiKey(storedKey);
    }
    if (storedReviewer) {
      setReviewerName(storedReviewer);
    }
  }, []);

  useEffect(() => {
    if (apiKey) {
      window.sessionStorage.setItem(adminKeyStorageKey, apiKey);
    }
  }, [apiKey]);

  useEffect(() => {
    if (reviewerName.trim()) {
      window.sessionStorage.setItem(reviewerStorageKey, reviewerName);
    }
  }, [reviewerName]);

  useEffect(() => {
    if (!selectedAttempt) {
      setScores({});
      setLessonCompletionPercent(80);
      setNotes("");
      return;
    }

    const nextScores = Object.fromEntries(
      selectedAttempt.evaluationSnapshot.sections.map((section) => [
        section.key,
        selectedAttempt.scores[section.key] ?? section.minimumScore
      ])
    );
    setScores(nextScores);
    setLessonCompletionPercent(
      selectedAttempt.lessonCompletionPercent ??
        selectedAttempt.evaluationSnapshot.lessonCompletionRequiredPercent
    );
    setNotes(selectedAttempt.adminNotes ?? "");
  }, [selectedAttempt]);

  const totals = useMemo(() => {
    return attempts.reduce(
      (acc, attempt) => {
        acc.count += 1;
        if (attempt.status === "submitted") {
          acc.submitted += 1;
        }
        if (attempt.status === "reviewed") {
          acc.reviewed += 1;
        }
        return acc;
      },
      { count: 0, reviewed: 0, submitted: 0 }
    );
  }, [attempts]);

  async function loadAttempts(input?: { nextStatus?: string }) {
    if (!apiKey) {
      setError("Masukkan admin key dulu.");
      return;
    }

    setIsLoading(true);
    setMessage("");
    setError("");

    try {
      const nextAttempts = await listAdminLevelTestAttempts({
        apiKey,
        levelCode: "A1",
        status: input?.nextStatus ?? status,
        limit: 100
      });
      setAttempts(nextAttempts);
      setSelectedAttempt(nextAttempts[0] ?? null);
      setMessage(
        nextAttempts.length
          ? `${nextAttempts.length} attempt dimuat.`
          : "Tidak ada attempt pada filter ini."
      );
    } catch {
      setError("Attempt belum bisa dimuat. Cek admin key atau koneksi API.");
    } finally {
      setIsLoading(false);
    }
  }

  async function saveReview() {
    if (!selectedAttempt) {
      return;
    }

    setIsSaving(true);
    setMessage("");
    setError("");

    try {
      const reviewed = await scoreAdminLevelTestAttempt({
        apiKey,
        attemptId: selectedAttempt.id,
        reviewedBy: reviewerName,
        lessonCompletionPercent,
        scores,
        notes
      });
      setSelectedAttempt(reviewed);
      setAttempts((current) =>
        current.map((attempt) => (attempt.id === reviewed.id ? reviewed : attempt))
      );
      setMessage("Review tersimpan dan report user sudah diperbarui.");
    } catch {
      setError("Review belum bisa disimpan. Pastikan attempt sudah submitted.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[0.36fr_0.64fr]">
      <section className="space-y-5">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-start gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-mint">
              <KeyRound className="h-5 w-5 text-leaf" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">Admin Review</p>
              <h1 className="mt-1 text-2xl font-semibold">A1 Test Attempts</h1>
              <p className="mt-2 text-sm leading-6 text-ink/60">
                Review submitted attempts dan simpan skor official untuk beta.
              </p>
            </div>
          </div>

          <div className="mt-5 grid gap-3">
            <label className="text-sm font-medium text-ink/70">
              Admin key
              <input
                type="password"
                value={apiKey}
                onChange={(event) => setApiKey(event.target.value)}
                className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
                placeholder="Paste admin key"
              />
            </label>
            <label className="text-sm font-medium text-ink/70">
              Reviewed by
              <input
                value={reviewerName}
                onChange={(event) => setReviewerName(event.target.value)}
                className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
              />
            </label>
          </div>
        </div>

        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-semibold">Queue</h2>
            <button
              type="button"
              onClick={() => loadAttempts()}
              disabled={isLoading || !apiKey}
              className="focus-ring inline-flex h-9 items-center justify-center gap-2 rounded-lg bg-ink px-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              <RefreshCcw className="h-4 w-4" aria-hidden="true" />
              Refresh
            </button>
          </div>

          <div className="mt-4 grid grid-cols-2 gap-2">
            {statusOptions.map((option) => (
              <button
                key={option.label}
                type="button"
                onClick={() => {
                  setStatus(option.value);
                  void loadAttempts({ nextStatus: option.value });
                }}
                disabled={!apiKey}
                className={`focus-ring min-h-10 rounded-lg px-3 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-60 ${
                  status === option.value ? "bg-ink text-white" : "bg-paper text-ink/70 hover:bg-mint"
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>

          <div className="mt-4 grid grid-cols-3 gap-2 text-sm">
            <Metric label="Attempts" value={totals.count} />
            <Metric label="Submitted" value={totals.submitted} />
            <Metric label="Reviewed" value={totals.reviewed} />
          </div>

          {message ? <p className="mt-4 rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">{message}</p> : null}
          {error ? <p className="mt-4 rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">{error}</p> : null}
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[0.42fr_0.58fr]">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <h2 className="font-semibold">Attempts</h2>
          <div className="mt-4 space-y-3">
            {attempts.map((attempt) => (
              <button
                key={attempt.id}
                type="button"
                onClick={() => setSelectedAttempt(attempt)}
                className={`focus-ring w-full rounded-lg p-4 text-left ${
                  selectedAttempt?.id === attempt.id ? "bg-mint" : "bg-paper hover:bg-mint"
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <p className="truncate font-semibold">{attempt.id}</p>
                  <span className={`rounded-md px-2 py-1 text-xs font-semibold ${statusTone(attempt.status)}`}>
                    {attempt.status}
                  </span>
                </div>
                <p className="mt-2 text-sm text-ink/60">{attempt.userId}</p>
                <p className="mt-1 text-xs text-ink/50">{formatDate(attempt.updatedAt)}</p>
              </button>
            ))}
            {!attempts.length ? (
              <p className="rounded-lg bg-paper p-4 text-sm text-ink/60">Load attempts dulu.</p>
            ) : null}
          </div>
        </div>

        {selectedAttempt ? (
          <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-sm font-semibold uppercase text-leaf">{selectedAttempt.levelCode}</p>
                <h2 className="mt-1 text-2xl font-semibold">Attempt Review</h2>
                <p className="mt-2 text-sm text-ink/60">{selectedAttempt.id}</p>
              </div>
              <span className={`rounded-md px-3 py-2 text-sm font-semibold ${statusTone(selectedAttempt.status)}`}>
                {selectedAttempt.status}
              </span>
            </div>

            <div className="mt-5 grid gap-3 sm:grid-cols-3">
              <Metric label="Current score" value={selectedAttempt.overallScore ?? "-"} />
              <Metric label="Passed" value={selectedAttempt.passed === null ? "-" : selectedAttempt.passed ? "Yes" : "No"} />
              <Metric label="Submitted" value={formatDate(selectedAttempt.submittedAt)} />
            </div>

            <div className="mt-5 grid gap-3">
              <label className="text-sm font-medium text-ink/70">
                Lesson completion
                <input
                  type="number"
                  min={0}
                  max={100}
                  value={lessonCompletionPercent}
                  onChange={(event) => setLessonCompletionPercent(clampScore(event.target.value))}
                  className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
                />
              </label>

              {selectedAttempt.evaluationSnapshot.sections.map((section) => (
                <label key={section.key} className="text-sm font-medium text-ink/70">
                  {section.title}
                  <input
                    type="number"
                    min={0}
                    max={100}
                    value={scores[section.key] ?? 0}
                    onChange={(event) =>
                      setScores({ ...scores, [section.key]: clampScore(event.target.value) })
                    }
                    className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-2 text-ink"
                  />
                </label>
              ))}

              <label className="text-sm font-medium text-ink/70">
                Review notes
                <textarea
                  value={notes}
                  onChange={(event) => setNotes(event.target.value)}
                  rows={4}
                  className="focus-ring mt-2 w-full resize-none rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
                />
              </label>

              <button
                type="button"
                onClick={saveReview}
                disabled={isSaving || selectedAttempt.status === "in_progress"}
                className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-leaf px-4 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Save className="h-4 w-4" aria-hidden="true" />
                {isSaving ? "Saving" : "Save Official Review"}
              </button>
            </div>
          </div>
        ) : (
          <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <ClipboardCheck className="h-6 w-6 text-leaf" aria-hidden="true" />
            <h2 className="mt-4 text-xl font-semibold">No Attempt Selected</h2>
            <p className="mt-2 text-sm leading-6 text-ink/60">Load queue dan pilih attempt untuk direview.</p>
          </div>
        )}
      </section>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-lg bg-paper p-3">
      <p className="text-xs font-semibold uppercase text-ink/50">{label}</p>
      <p className="mt-1 font-semibold">{value}</p>
    </div>
  );
}

function clampScore(value: string) {
  const parsed = Number(value);
  if (Number.isNaN(parsed)) {
    return 0;
  }
  return Math.max(0, Math.min(100, parsed));
}
