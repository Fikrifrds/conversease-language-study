"use client";

import { useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  Award,
  CheckCircle2,
  ClipboardCheck,
  Loader2,
  PlayCircle,
  Save,
  Send,
  XCircle
} from "lucide-react";
import {
  getLevelTest,
  listMyLevelTestAttempts,
  previewLevelTestAttempt,
  saveLevelTestDraft,
  startLevelTestAttempt,
  submitLevelTestAttempt,
  type LevelTest,
  type LevelTestAttempt,
  type LevelTestPreviewResult
} from "@/lib/learning-api";

type SectionResponseEntry = {
  answer: string;
  notes: string;
};

type SectionResponseMap = Record<string, SectionResponseEntry>;

const initialScores: Record<string, number> = {
  listening: 70,
  speaking_conversation: 70,
  pronunciation_fluency: 70,
  useful_phrases: 70,
  grammar: 70,
  reading: 70,
  writing: 70
};

export function LevelTestPanel({
  levelCode,
  language = "english"
}: {
  levelCode: string;
  language?: string;
}) {
  const [test, setTest] = useState<LevelTest | null>(null);
  const [scores, setScores] = useState(initialScores);
  const [responses, setResponses] = useState<SectionResponseMap>({});
  const [lessonCompletionPercent, setLessonCompletionPercent] = useState(80);
  const [preview, setPreview] = useState<LevelTestPreviewResult | null>(null);
  const [savedAttempt, setSavedAttempt] = useState<LevelTestAttempt | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isPreviewing, setIsPreviewing] = useState(false);
  const [isStarting, setIsStarting] = useState(false);
  const [isSavingDraft, setIsSavingDraft] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isTakingTest, setIsTakingTest] = useState(false);
  const [activeSectionIndex, setActiveSectionIndex] = useState(0);
  const [error, setError] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  useEffect(() => {
    let ignore = false;

    async function loadTest() {
      setError("");
      setStatusMessage("");
      setIsLoading(true);
      try {
        const nextTest = await getLevelTest(levelCode, language);
        const attempts = await listMyLevelTestAttempts(nextTest.attemptLevelCode);
        const nextAttempt = attempts[0] ?? null;

        if (ignore) {
          return;
        }

        setTest(nextTest);
        setSavedAttempt(nextAttempt);
        setScores(buildInitialScores(nextTest, nextAttempt));
        setResponses(buildInitialResponses(nextTest, nextAttempt));
        setLessonCompletionPercent(
          nextAttempt?.lessonCompletionPercent ?? nextTest.lessonCompletionRequiredPercent
        );
        setPreview(getPreviewFromAttempt(nextAttempt));
        setIsTakingTest(false);
        setActiveSectionIndex(0);
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
  }, [language, levelCode]);

  const totalWeight = useMemo(
    () => test?.sections.reduce((total, section) => total + section.weight, 0) ?? 0,
    [test]
  );

  const answeredCount = useMemo(() => {
    if (!test) {
      return 0;
    }
    return test.sections.filter((section) => Boolean(responses[section.key]?.answer.trim())).length;
  }, [responses, test]);

  const currentSection = test?.sections[activeSectionIndex] ?? null;
  const canSubmit = Boolean(test && answeredCount === test.sections.length);
  const isAttemptInProgress = savedAttempt?.status === "in_progress";
  const statusTone = preview?.passed ? "bg-mint" : "bg-[#fde7df]";

  async function runPreview() {
    if (!test) {
      return;
    }

    setError("");
    setStatusMessage("");
    setIsPreviewing(true);
    try {
      setPreview(
        await previewLevelTestAttempt({
          levelCode: test.levelCode,
          language: test.language,
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

  async function startOrResumeAttempt() {
    if (!test) {
      return;
    }

    setError("");
    setStatusMessage("");

    if (savedAttempt?.status === "in_progress") {
      setIsTakingTest(true);
      return;
    }

    setIsStarting(true);
    try {
      const attempt = await startLevelTestAttempt(test.levelCode, test.language);
      setSavedAttempt(attempt);
      setScores(buildInitialScores(test, attempt));
      setResponses(buildInitialResponses(test, attempt));
      setLessonCompletionPercent(
        attempt.lessonCompletionPercent ?? test.lessonCompletionRequiredPercent
      );
      setPreview(getPreviewFromAttempt(attempt));
      setIsTakingTest(true);
      setActiveSectionIndex(0);
      setStatusMessage("Tes dimulai. Isi jawaban per bagian lalu simpan draft atau kirim saat selesai.");
    } catch {
      setError("Attempt belum bisa dimulai.");
    } finally {
      setIsStarting(false);
    }
  }

  async function persistDraft(options?: { silent?: boolean }) {
    if (!test) {
      return false;
    }

    setError("");
    setStatusMessage("");
    setIsSavingDraft(true);
    try {
      const activeAttempt =
        savedAttempt?.status === "in_progress"
          ? savedAttempt
          : await startLevelTestAttempt(test.levelCode, test.language);
      const updatedAttempt = await saveLevelTestDraft({
        attemptId: activeAttempt.id,
        lessonCompletionPercent,
        scores,
        responses: serializeResponses(responses)
      });
      setSavedAttempt(updatedAttempt);
      setPreview(getPreviewFromAttempt(updatedAttempt));
      if (!options?.silent) {
        setStatusMessage("Draft tes berhasil disimpan.");
      }
      return true;
    } catch {
      setError("Draft tes belum bisa disimpan.");
      return false;
    } finally {
      setIsSavingDraft(false);
    }
  }

  async function goToSection(nextIndex: number) {
    if (!test || nextIndex < 0 || nextIndex >= test.sections.length) {
      return;
    }

    const saved = await persistDraft({ silent: true });
    if (saved) {
      setActiveSectionIndex(nextIndex);
    }
  }

  async function submitSavedAttempt() {
    if (!test) {
      return;
    }

    if (!canSubmit) {
      setError("Lengkapi semua jawaban section sebelum mengirim tes.");
      return;
    }

    setError("");
    setStatusMessage("");
    setIsSubmitting(true);
    try {
      const activeAttempt =
        savedAttempt?.status === "in_progress"
          ? savedAttempt
          : await startLevelTestAttempt(test.levelCode, test.language);
      const submitted = await submitLevelTestAttempt({
        attemptId: activeAttempt.id,
        lessonCompletionPercent,
        scores,
        responses: {
          source: "web_level_test_workspace",
          sections: serializeResponses(responses)
        }
      });
      setSavedAttempt(submitted);
      setPreview(getPreviewFromAttempt(submitted));
      setIsTakingTest(false);
      setStatusMessage("Tes berhasil dikirim. Hasil resmi akan muncul setelah review admin.");
    } catch {
      setError("Attempt belum bisa disubmit.");
    } finally {
      setIsSubmitting(false);
    }
  }

  function updateResponse(sectionKey: string, field: keyof SectionResponseEntry, value: string) {
    setResponses((current) => ({
      ...current,
      [sectionKey]: {
        answer: current[sectionKey]?.answer ?? "",
        notes: current[sectionKey]?.notes ?? "",
        [field]: value
      }
    }));
  }

  function updateScore(sectionKey: string, value: string) {
    setScores((current) => ({
      ...current,
      [sectionKey]: clampScore(value)
    }));
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
    <div className="grid gap-5 lg:grid-cols-[0.66fr_0.34fr]">
      <section className="space-y-4">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">
                {languageLabel(test.language)} {test.levelCode} Final Test
              </p>
              <h1 className="mt-2 text-3xl font-semibold">{test.title}</h1>
              <p className="mt-3 max-w-3xl leading-7 text-ink/70">{test.description}</p>
            </div>
            <div className="flex flex-col items-start gap-3">
              <span className={`rounded-lg px-3 py-2 text-sm font-semibold ${badgeClassName(test.status)}`}>
                {formatStatus(test.status)}
              </span>
              <button
                type="button"
                onClick={startOrResumeAttempt}
                disabled={isStarting}
                className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isStarting ? (
                  <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                ) : (
                  <PlayCircle className="h-4 w-4" aria-hidden="true" />
                )}
                {savedAttempt?.status === "in_progress"
                  ? "Lanjutkan Tes"
                  : savedAttempt?.status === "submitted" || savedAttempt?.status === "reviewed"
                    ? "Mulai Attempt Baru"
                    : "Mulai Tes"}
              </button>
            </div>
          </div>

          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            <Metric label="Ambang keseluruhan" value={`${test.overallThreshold}`} />
            <Metric label="Penyelesaian lesson" value={`${test.lessonCompletionRequiredPercent}%`} />
            <Metric label="Bobot bagian" value={`${totalWeight}%`} />
          </div>
        </div>

        {isTakingTest && currentSection ? (
          <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-sm font-semibold uppercase text-leaf">Take Test Flow</p>
                <h2 className="mt-2 text-2xl font-semibold">Section {activeSectionIndex + 1} dari {test.sections.length}</h2>
                <p className="mt-2 text-sm text-ink/60">
                  Jawab setiap bagian, beri self-score, lalu simpan draft jika ingin lanjut nanti.
                </p>
              </div>
              <div className="rounded-lg bg-paper px-4 py-3 text-sm text-ink/70">
                {answeredCount}/{test.sections.length} section terisi
              </div>
            </div>

            <div className="mt-5 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
              {test.sections.map((section, index) => {
                const answered = Boolean(responses[section.key]?.answer.trim());
                const active = index === activeSectionIndex;
                return (
                  <button
                    key={section.key}
                    type="button"
                    onClick={() => setActiveSectionIndex(index)}
                    className={`rounded-lg border px-3 py-3 text-left text-sm transition ${
                      active
                        ? "border-leaf bg-mint"
                        : answered
                          ? "border-leaf/30 bg-white"
                          : "border-ink/10 bg-white hover:bg-paper"
                    }`}
                  >
                    <p className="font-semibold text-ink">{section.title}</p>
                    <p className="mt-1 text-xs text-ink/60">{answered ? "Sudah dijawab" : "Belum dijawab"}</p>
                  </button>
                );
              })}
            </div>

            <article className="mt-5 rounded-xl border border-ink/10 bg-paper p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold uppercase text-leaf">{currentSection.title}</p>
                  <h3 className="mt-2 text-xl font-semibold">Tugas Section</h3>
                  <p className="mt-3 max-w-3xl text-sm leading-7 text-ink/70">{currentSection.task.prompt}</p>
                </div>
                <div className="flex gap-2 text-xs font-semibold">
                  <span className="rounded-md bg-white px-2 py-1">Weight {currentSection.weight}%</span>
                  <span className="rounded-md bg-mint px-2 py-1 text-leaf">Min {currentSection.minimumScore}</span>
                </div>
              </div>

              <div className="mt-4 grid gap-2">
                {currentSection.task.successCriteria.map((criterion) => (
                  <p key={criterion} className="flex gap-2 text-sm text-ink/65">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-leaf" aria-hidden="true" />
                    {criterion}
                  </p>
                ))}
              </div>

              <div className="mt-5 grid gap-4">
                <label className="block text-sm font-medium text-ink/70">
                  Jawaban kamu
                  <textarea
                    value={responses[currentSection.key]?.answer ?? ""}
                    onChange={(event) => updateResponse(currentSection.key, "answer", event.target.value)}
                    rows={6}
                    placeholder={responsePlaceholder(currentSection.task.type, currentSection.title)}
                    className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-sm text-ink"
                  />
                </label>

                <div className="grid gap-4 sm:grid-cols-[0.3fr_0.7fr]">
                  <label className="block text-sm font-medium text-ink/70">
                    Self-score
                    <input
                      type="number"
                      min={0}
                      max={100}
                      value={scores[currentSection.key] ?? 0}
                      onChange={(event) => updateScore(currentSection.key, event.target.value)}
                      className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
                    />
                  </label>
                  <label className="block text-sm font-medium text-ink/70">
                    Catatan opsional
                    <textarea
                      value={responses[currentSection.key]?.notes ?? ""}
                      onChange={(event) => updateResponse(currentSection.key, "notes", event.target.value)}
                      rows={3}
                      placeholder="Tulis konteks, hal yang masih ragu, atau poin yang ingin dicek admin."
                      className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-sm text-ink"
                    />
                  </label>
                </div>
              </div>
            </article>

            <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
              <button
                type="button"
                onClick={() => void goToSection(activeSectionIndex - 1)}
                disabled={activeSectionIndex === 0 || isSavingDraft}
                className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg border border-ink/20 px-4 text-sm font-semibold hover:bg-paper disabled:cursor-not-allowed disabled:opacity-60"
              >
                <ArrowLeft className="h-4 w-4" aria-hidden="true" />
                Sebelumnya
              </button>
              <div className="flex flex-wrap items-center gap-2">
                <button
                  type="button"
                  onClick={() => void persistDraft()}
                  disabled={isSavingDraft}
                  className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg border border-ink/20 px-4 text-sm font-semibold hover:bg-mint disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {isSavingDraft ? (
                    <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                  ) : (
                    <Save className="h-4 w-4" aria-hidden="true" />
                  )}
                  Simpan Draft
                </button>
                {activeSectionIndex < test.sections.length - 1 ? (
                  <button
                    type="button"
                    onClick={() => void goToSection(activeSectionIndex + 1)}
                    disabled={isSavingDraft}
                    className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    Lanjut
                    <ArrowRight className="h-4 w-4" aria-hidden="true" />
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={submitSavedAttempt}
                    disabled={isSubmitting || !canSubmit}
                    className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-leaf px-4 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {isSubmitting ? (
                      <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                    ) : (
                      <Send className="h-4 w-4" aria-hidden="true" />
                    )}
                    Kirim Tes
                  </button>
                )}
              </div>
            </div>
          </section>
        ) : null}

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
          <h2 className="mt-3 text-xl font-semibold">Kontrol Tes</h2>
          <p className="mt-2 text-sm leading-6 text-ink/60">
            Flow sekarang lengkap: mulai tes, isi jawaban per bagian, simpan draft, cek kesiapan,
            lalu kirim untuk review admin.
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
              <div key={section.key} className="rounded-lg border border-ink/10 bg-paper px-3 py-3">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-sm font-semibold text-ink">{section.title}</p>
                    <p className="mt-1 text-xs text-ink/55">
                      {responses[section.key]?.answer.trim() ? "Jawaban terisi" : "Belum dijawab"}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs font-semibold uppercase text-ink/45">Score</p>
                    <p className="text-lg font-semibold">{scores[section.key] ?? 0}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <button
            type="button"
            onClick={runPreview}
            disabled={isPreviewing}
            className="focus-ring mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isPreviewing ? (
              <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            ) : (
              <Award className="h-4 w-4" aria-hidden="true" />
            )}
            {isPreviewing ? "Menghitung" : "Cek Kesiapan"}
          </button>

          <div className="mt-3 grid gap-2 sm:grid-cols-2">
            <button
              type="button"
              onClick={startOrResumeAttempt}
              disabled={isStarting}
              className="focus-ring inline-flex min-h-11 items-center justify-center rounded-lg border border-ink/20 px-4 text-sm font-semibold hover:bg-mint disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isStarting
                ? "Memulai"
                : isAttemptInProgress
                  ? "Lanjutkan Tes"
                  : "Mulai Tes"}
            </button>
            <button
              type="button"
              onClick={submitSavedAttempt}
              disabled={isSubmitting || !isAttemptInProgress || !canSubmit}
              className="focus-ring inline-flex min-h-11 items-center justify-center rounded-lg bg-leaf px-4 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting ? "Mengirim" : "Kirim Tes"}
            </button>
          </div>

          {statusMessage ? (
            <p className="mt-3 rounded-lg bg-mint px-3 py-2 text-sm text-ink/70">{statusMessage}</p>
          ) : null}
          {error ? <p className="mt-3 rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{error}</p> : null}
        </section>

        {savedAttempt ? (
          <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <p className="text-sm font-semibold uppercase text-leaf">Attempt Saat Ini</p>
            <h2 className="mt-2 text-xl font-semibold">
              {savedAttempt.status === "reviewed"
                ? "Sudah Ditinjau Admin"
                : savedAttempt.status === "submitted"
                  ? "Menunggu Tinjauan Admin"
                  : "Draft Tes Tersimpan"}
            </h2>
            <p className="mt-2 text-sm text-ink/60">{savedAttempt.id}</p>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              <Metric label="Jawaban terisi" value={`${answeredCount}/${test.sections.length}`} />
              <Metric
                label="Skor terbaru"
                value={savedAttempt.overallScore !== null ? String(savedAttempt.overallScore) : "-"}
              />
            </div>
            {savedAttempt.status === "submitted" || savedAttempt.status === "reviewed" ? (
              <div className="mt-4 rounded-lg bg-paper p-4">
                <p className="text-sm text-ink/60">
                  {savedAttempt.status === "reviewed" ? "Skor resmi" : "Skor penilaian diri"}
                </p>
                <p className="mt-1 text-3xl font-semibold">{savedAttempt.overallScore ?? "-"}</p>
                <p className="mt-2 text-sm text-ink/70">
                  {savedAttempt.status === "reviewed"
                    ? savedAttempt.passed
                      ? "Lulus"
                      : "Belum lulus"
                    : "Menunggu review admin"}
                </p>
                {savedAttempt.reviewedBy ? (
                  <p className="mt-2 text-xs text-ink/55">Ditinjau oleh {savedAttempt.reviewedBy}</p>
                ) : null}
                {savedAttempt.adminNotes ? (
                  <p className="mt-2 text-sm text-ink/65">Catatan admin: {savedAttempt.adminNotes}</p>
                ) : null}
              </div>
            ) : null}
          </section>
        ) : null}

        {preview ? (
          <section className={`rounded-lg p-5 shadow-sm ${statusTone}`}>
            {preview.passed ? (
              <CheckCircle2 className="h-6 w-6 text-leaf" aria-hidden="true" />
            ) : (
              <XCircle className="h-6 w-6 text-coral" aria-hidden="true" />
            )}
            <p className="mt-3 text-sm font-semibold uppercase text-ink/60">Perkiraan hasil</p>
            <h2 className="mt-1 text-3xl font-semibold">{preview.overallScore}</h2>
            <p className="mt-2 text-sm text-ink/70">
              {preview.passed
                ? `Siap untuk level test ${languageLabel(test.language)} ${test.levelCode}.`
                : `Perlu review lagi sebelum kirim level test ${languageLabel(test.language)} ${test.levelCode}.`}
            </p>
            {preview.missingRequirements.length ? (
              <div className="mt-4 space-y-2 text-sm text-ink/70">
                {preview.missingRequirements.map((requirement) => (
                  <p key={requirement}>{requirement}</p>
                ))}
              </div>
            ) : null}
            {preview.weakSkills.length ? (
              <div className="mt-4 rounded-lg bg-white/70 px-3 py-3 text-sm text-ink/70">
                Weak skills: {preview.weakSkills.join(", ")}
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

function buildInitialScores(test: LevelTest, attempt: LevelTestAttempt | null) {
  return Object.fromEntries(
    test.sections.map((section) => [
      section.key,
      attempt?.scores?.[section.key] ?? Math.max(initialScores[section.key] ?? 70, section.minimumScore)
    ])
  );
}

function buildInitialResponses(test: LevelTest, attempt: LevelTestAttempt | null): SectionResponseMap {
  const storedSections = normalizeStoredSections(attempt?.responses);
  return Object.fromEntries(
    test.sections.map((section) => [
      section.key,
      {
        answer: storedSections[section.key]?.answer ?? "",
        notes: storedSections[section.key]?.notes ?? ""
      }
    ])
  );
}

function normalizeStoredSections(rawResponses: Record<string, unknown> | undefined): SectionResponseMap {
  const source =
    rawResponses && typeof rawResponses.sections === "object" && rawResponses.sections !== null
      ? (rawResponses.sections as Record<string, unknown>)
      : rawResponses ?? {};

  return Object.fromEntries(
    Object.entries(source)
      .filter(([key]) => key !== "source")
      .map(([key, value]) => [key, normalizeStoredEntry(value)])
  );
}

function normalizeStoredEntry(value: unknown): SectionResponseEntry {
  if (typeof value === "string") {
    return { answer: value, notes: "" };
  }

  if (value && typeof value === "object") {
    const candidate = value as { answer?: unknown; notes?: unknown };
    return {
      answer: typeof candidate.answer === "string" ? candidate.answer : "",
      notes: typeof candidate.notes === "string" ? candidate.notes : ""
    };
  }

  return { answer: "", notes: "" };
}

function serializeResponses(responses: SectionResponseMap) {
  return Object.fromEntries(
    Object.entries(responses).map(([key, value]) => [
      key,
      {
        answer: value.answer.trim(),
        notes: value.notes.trim()
      }
    ])
  );
}

function getPreviewFromAttempt(attempt: LevelTestAttempt | null): LevelTestPreviewResult | null {
  if (!attempt || attempt.overallScore === null || attempt.passed === null) {
    return null;
  }

  return {
    overallScore: attempt.overallScore,
    passed: attempt.passed,
    missingRequirements: attempt.missingRequirements,
    weakSkills: attempt.weakSkills
  };
}

function responsePlaceholder(taskType: string, sectionTitle: string) {
  switch (taskType) {
    case "dialogue_understanding":
      return `Tulis pemahamanmu untuk bagian ${sectionTitle}. Sebutkan detail inti yang kamu tangkap.`;
    case "roleplay_response":
      return `Tulis atau transkripkan respons yang akan kamu ucapkan untuk bagian ${sectionTitle}.`;
    case "repeat_and_read_aloud":
      return `Tulis teks yang kamu latih atau catatan pengucapan untuk bagian ${sectionTitle}.`;
    case "phrase_selection":
      return `Tulis frasa yang kamu pilih beserta alasan singkat untuk bagian ${sectionTitle}.`;
    case "sentence_completion":
      return `Tulis jawaban kalimat yang kamu pilih untuk bagian ${sectionTitle}.`;
    case "short_message_reading":
      return `Tulis jawaban pemahaman bacaanmu untuk bagian ${sectionTitle}.`;
    case "short_reply_writing":
      return `Tulis jawaban finalmu untuk bagian ${sectionTitle}.`;
    default:
      return `Tulis jawabanmu untuk bagian ${sectionTitle}.`;
  }
}

function formatStatus(status: string) {
  if (status === "published") {
    return "Published";
  }
  if (status === "planned") {
    return "Draft";
  }
  return status;
}

function languageLabel(language: string) {
  return language === "arabic" ? "Arabic" : "English";
}

function badgeClassName(status: string) {
  if (status === "published") {
    return "bg-mint text-leaf";
  }
  if (status === "planned") {
    return "bg-paper text-ink/75";
  }
  return "bg-paper text-ink/75";
}
