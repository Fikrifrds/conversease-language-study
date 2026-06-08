"use client";

import { useEffect, useMemo, useState } from "react";
import { Award, CheckCircle2, ClipboardCheck, Loader2, XCircle } from "lucide-react";
import {
  getLevelTest,
  listMyLevelTestAttempts,
  previewLevelTestAttempt,
  startLevelTestAttempt,
  submitLevelTestAttempt,
  type LevelTest,
  type LevelTestAttempt,
  type LevelTestPreviewResult
} from "@/lib/learning-api";

const initialScores: Record<string, number> = {
  listening: 70,
  speaking_conversation: 70,
  pronunciation_fluency: 70,
  useful_phrases: 70,
  grammar: 70,
  reading: 70,
  writing: 70
};

export function LevelTestPanel({ levelCode }: { levelCode: string }) {
  const [test, setTest] = useState<LevelTest | null>(null);
  const [scores, setScores] = useState(initialScores);
  const [lessonCompletionPercent, setLessonCompletionPercent] = useState(80);
  const [preview, setPreview] = useState<LevelTestPreviewResult | null>(null);
  const [savedAttempt, setSavedAttempt] = useState<LevelTestAttempt | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isPreviewing, setIsPreviewing] = useState(false);
  const [isStarting, setIsStarting] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let ignore = false;

    async function loadTest() {
      setError("");
      setIsLoading(true);
      try {
        const nextTest = await getLevelTest(levelCode);
        if (!ignore) {
          setTest(nextTest);
          setScores(
            Object.fromEntries(
              nextTest.sections.map((section) => [section.key, Math.max(section.minimumScore, 70)])
            )
          );
          setLessonCompletionPercent(nextTest.lessonCompletionRequiredPercent);
        }
        const attempts = await listMyLevelTestAttempts(nextTest.levelCode);
        if (!ignore) {
          setSavedAttempt(attempts[0] ?? null);
        }
      } catch {
        if (!ignore) {
          setError("Level test belum bisa dimuat.");
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }

    loadTest();

    return () => {
      ignore = true;
    };
  }, [levelCode]);

  const totalWeight = useMemo(
    () => test?.sections.reduce((total, section) => total + section.weight, 0) ?? 0,
    [test]
  );

  async function runPreview() {
    if (!test) {
      return;
    }

    setError("");
    setIsPreviewing(true);
    try {
      setPreview(
        await previewLevelTestAttempt({
          levelCode: test.levelCode,
          lessonCompletionPercent,
          scores
        })
      );
    } catch {
      setError("Preview skor belum bisa dihitung.");
    } finally {
      setIsPreviewing(false);
    }
  }

  async function startSavedAttempt() {
    if (!test) {
      return;
    }

    setError("");
    setIsStarting(true);
    try {
      setSavedAttempt(await startLevelTestAttempt(test.levelCode));
    } catch {
      setError("Attempt belum bisa dimulai.");
    } finally {
      setIsStarting(false);
    }
  }

  async function submitSavedAttempt() {
    if (!test) {
      return;
    }

    setError("");
    setIsSubmitting(true);
    try {
      const activeAttempt =
        savedAttempt?.status === "in_progress"
          ? savedAttempt
          : await startLevelTestAttempt(test.levelCode);
      const submitted = await submitLevelTestAttempt({
        attemptId: activeAttempt.id,
        lessonCompletionPercent,
        scores,
        responses: {
          source: "web_level_test_panel"
        }
      });
      setSavedAttempt(submitted);
      setPreview({
        overallScore: submitted.overallScore ?? 0,
        passed: Boolean(submitted.passed),
        missingRequirements: submitted.missingRequirements,
        weakSkills: submitted.weakSkills
      });
    } catch {
      setError("Attempt belum bisa disubmit.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoading) {
    return (
      <section className="rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
        <Loader2 className="h-6 w-6 animate-spin text-leaf" aria-hidden="true" />
        <p className="mt-3 text-sm text-ink/60">Loading level test...</p>
      </section>
    );
  }

  if (!test) {
    return (
      <section className="rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
        <XCircle className="h-6 w-6 text-coral" aria-hidden="true" />
        <p className="mt-3 text-sm text-ink/70">{error || "Level test belum tersedia."}</p>
      </section>
    );
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[0.64fr_0.36fr]">
      <section className="space-y-4">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">{test.levelCode} Final Test</p>
              <h1 className="mt-2 text-3xl font-semibold">{test.title}</h1>
              <p className="mt-3 max-w-3xl leading-7 text-ink/70">{test.description}</p>
            </div>
            <span className="rounded-lg bg-mint px-3 py-2 text-sm font-semibold text-leaf">
              {test.status}
            </span>
          </div>

          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            <Metric label="Ambang keseluruhan" value={`${test.overallThreshold}`} />
            <Metric label="Penyelesaian lesson" value={`${test.lessonCompletionRequiredPercent}%`} />
            <Metric label="Bobot bagian" value={`${totalWeight}%`} />
          </div>
        </div>

        <div className="grid gap-3">
          {test.sections.map((section) => (
            <article key={section.key} className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="font-semibold">{section.title}</h2>
                  <p className="mt-2 text-sm leading-6 text-ink/65">{section.task.prompt}</p>
                </div>
                <div className="flex gap-2 text-xs font-semibold">
                  <span className="rounded-md bg-paper px-2 py-1">Weight {section.weight}%</span>
                  <span className="rounded-md bg-mint px-2 py-1 text-leaf">Min {section.minimumScore}</span>
                </div>
              </div>
              <div className="mt-4 grid gap-2">
                {section.task.successCriteria.map((criterion) => (
                  <p key={criterion} className="flex gap-2 text-sm text-ink/65">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-leaf" aria-hidden="true" />
                    {criterion}
                  </p>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>

      <aside className="space-y-4">
        <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <ClipboardCheck className="h-6 w-6 text-leaf" aria-hidden="true" />
          <h2 className="mt-3 text-xl font-semibold">Self-Assessment Readiness</h2>
          <p className="mt-2 text-sm leading-6 text-ink/60">
            Nilai sendiri perkiraan kemampuanmu per skill untuk melihat kesiapan. Ini self-assessment,
            bukan nilai otomatis. Skor final resmi ditentukan admin setelah review.
          </p>

          <label className="mt-4 block text-sm font-medium text-ink/70">
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

          <div className="mt-4 space-y-3">
            {test.sections.map((section) => (
              <label key={section.key} className="block text-sm font-medium text-ink/70">
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
          </div>

          <button
            type="button"
            onClick={runPreview}
            disabled={isPreviewing}
            className="focus-ring mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Award className="h-4 w-4" aria-hidden="true" />
            {isPreviewing ? "Menghitung" : "Cek Kesiapan"}
          </button>

          <div className="mt-3 grid gap-2 sm:grid-cols-2">
            <button
              type="button"
              onClick={startSavedAttempt}
              disabled={isStarting || savedAttempt?.status === "in_progress"}
              className="focus-ring inline-flex min-h-11 items-center justify-center rounded-lg border border-ink/20 px-4 text-sm font-semibold hover:bg-mint disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isStarting ? "Memulai" : savedAttempt?.status === "in_progress" ? "Percobaan Dimulai" : "Mulai Percobaan"}
            </button>
            <button
              type="button"
              onClick={submitSavedAttempt}
              disabled={isSubmitting || savedAttempt?.status === "submitted" || savedAttempt?.status === "reviewed"}
              className="focus-ring inline-flex min-h-11 items-center justify-center rounded-lg bg-leaf px-4 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting
                ? "Mengirim"
                : savedAttempt?.status === "submitted" || savedAttempt?.status === "reviewed"
                  ? "Terkirim"
                  : "Kirim Percobaan"}
            </button>
          </div>

          {error ? <p className="mt-3 rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{error}</p> : null}
        </section>

        {savedAttempt ? (
          <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <p className="text-sm font-semibold uppercase text-leaf">Percobaan Tersimpan</p>
            <h2 className="mt-2 text-xl font-semibold">
              {savedAttempt.status === "reviewed"
                ? "Sudah Ditinjau Admin"
                : savedAttempt.status === "submitted"
                  ? "Menunggu Tinjauan Admin"
                  : "Percobaan Sedang Berjalan"}
            </h2>
            <p className="mt-2 text-sm text-ink/60">{savedAttempt.id}</p>
            {savedAttempt.status === "submitted" || savedAttempt.status === "reviewed" ? (
              <div className="mt-4 rounded-lg bg-paper p-4">
                <p className="text-sm text-ink/60">
                  {savedAttempt.status === "reviewed" ? "Skor resmi" : "Skor penilaian sendiri"}
                </p>
                <p className="mt-1 text-3xl font-semibold">{savedAttempt.overallScore}</p>
                <p className="mt-2 text-sm text-ink/70">
                  {savedAttempt.status === "reviewed"
                    ? savedAttempt.passed
                      ? "Lulus"
                      : "Belum lulus"
                    : "Menunggu review admin"}
                </p>
                {savedAttempt.status === "reviewed" ? (
                  <p className="mt-2 text-xs text-ink/55">
                    Ditinjau oleh {savedAttempt.reviewedBy ?? "admin"}
                  </p>
                ) : null}
              </div>
            ) : null}
          </section>
        ) : null}

        {preview ? (
          <section className={`rounded-lg p-5 shadow-sm ${preview.passed ? "bg-mint" : "bg-[#fde7df]"}`}>
            {preview.passed ? (
              <CheckCircle2 className="h-6 w-6 text-leaf" aria-hidden="true" />
            ) : (
              <XCircle className="h-6 w-6 text-coral" aria-hidden="true" />
            )}
            <p className="mt-3 text-sm font-semibold uppercase text-ink/60">Perkiraan hasil</p>
            <h2 className="mt-1 text-3xl font-semibold">{preview.overallScore}</h2>
            <p className="mt-2 text-sm text-ink/70">{preview.passed ? "Siap untuk tes A1." : "Perlu review sebelum tes A1."}</p>
            {preview.missingRequirements.length ? (
              <div className="mt-4 space-y-2 text-sm text-ink/70">
                {preview.missingRequirements.map((requirement) => (
                  <p key={requirement}>{requirement}</p>
                ))}
              </div>
            ) : null}
          </section>
        ) : null}
      </aside>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-paper p-4">
      <p className="text-xs font-semibold uppercase text-ink/50">{label}</p>
      <p className="mt-2 text-2xl font-semibold">{value}</p>
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
