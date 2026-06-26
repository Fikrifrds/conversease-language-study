"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  AlertCircle,
  CheckCircle2,
  Clock3,
  Loader2,
  Mic,
  PauseCircle,
  PlayCircle,
  Save,
  Send
} from "lucide-react";

import {
  ApiRequestError,
  ExamStartBlockedError,
  getExamAttemptStatus,
  getExamManifest,
  getExamRunnerStatus,
  getExamSectionContent,
  getRealExamResult,
  listExamTemplatesByLevel,
  navigateExamSession,
  saveExamItemResponse,
  startRealExam,
  submitRealExam,
  uploadExamSpeakingAudio,
  type ExamAttemptStatus,
  type ExamManifest,
  type ExamRunnerItem,
  type ExamRunnerSectionContent,
  type ExamTemplateSummary,
  type RealExamResult
} from "@/lib/learning-api";
import { useVoiceRecorder } from "@/lib/use-voice-recorder";
import { trackEvent } from "@/lib/analytics";

type ItemDraft = {
  textResponse?: string;
  selectedOptionIds?: string[];
  matchedPairs?: Record<string, string>;
  fileUrl?: string | null;
  localPlaybackUrl?: string | null;
  audioDurationSeconds?: number | null;
};

type DraftMap = Record<string, ItemDraft>;

function sessionStorageKey(levelCode: string) {
  return `conversease.real-exam.${levelCode.toUpperCase()}.session`;
}

function lastResultStorageKey(levelCode: string) {
  return `conversease.real-exam.${levelCode.toUpperCase()}.last-result`;
}

function formatSeconds(totalSeconds: number | null) {
  if (totalSeconds === null) {
    return "--:--";
  }
  const safe = Math.max(0, totalSeconds);
  const minutes = Math.floor(safe / 60);
  const seconds = safe % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function blankCount(text: string | null | undefined) {
  if (!text) {
    return 0;
  }
  return (text.match(/\[BLANK\]/g) ?? []).length;
}

function safeItemDraft(drafts: DraftMap, itemId: string): ItemDraft {
  return drafts[itemId] ?? {};
}

function isExpiredSessionError(error: unknown): boolean {
  return (
    error instanceof ApiRequestError &&
    error.status === 400 &&
    error.detail.toLowerCase().includes("expired")
  );
}

export function RealExamPanel({ levelCode }: { levelCode: string }) {
  const [templates, setTemplates] = useState<ExamTemplateSummary[]>([]);
  const [activeTemplate, setActiveTemplate] = useState<ExamTemplateSummary | null>(null);
  const [manifest, setManifest] = useState<ExamManifest | null>(null);
  const [content, setContent] = useState<ExamRunnerSectionContent | null>(null);
  const [drafts, setDrafts] = useState<DraftMap>({});
  const [timeRemaining, setTimeRemaining] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isStarting, setIsStarting] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [activeSpeakingItemId, setActiveSpeakingItemId] = useState<string | null>(null);
  const [lastResult, setLastResult] = useState<RealExamResult | null>(null);
  const [attemptStatus, setAttemptStatus] = useState<ExamAttemptStatus | null>(null);

  const refreshAttemptStatus = useCallback(async (templateId: string) => {
    try {
      setAttemptStatus(await getExamAttemptStatus(templateId));
    } catch {
      // Non-fatal: the start call still enforces the policy server-side.
    }
  }, []);
  const audioUrlRef = useRef<Record<string, string>>({});

  const refreshLastResult = useCallback(async () => {
    const lastSessionId =
      typeof window !== "undefined" ? window.localStorage.getItem(lastResultStorageKey(levelCode)) : null;
    if (!lastSessionId) {
      return;
    }
    try {
      setLastResult(await getRealExamResult(lastSessionId));
    } catch {
      // Result may not exist yet (or session was cleaned up) — keep the card hidden.
    }
  }, [levelCode]);

  const recorder = useVoiceRecorder({
    onResult: async (blob) => {
      if (!activeSpeakingItemId) {
        return;
      }
      const itemId = activeSpeakingItemId;
      const previousUrl = audioUrlRef.current[itemId];
      if (previousUrl) {
        URL.revokeObjectURL(previousUrl);
      }
      const objectUrl = URL.createObjectURL(blob);
      audioUrlRef.current[itemId] = objectUrl;
      setDrafts((current) => ({
        ...current,
        [itemId]: {
          ...current[itemId],
          fileUrl: null,
          localPlaybackUrl: objectUrl,
          audioDurationSeconds: recorder.seconds || null
        }
      }));
      setActiveSpeakingItemId(null);

      if (!manifest) {
        return;
      }
      setNotice("Mengunggah jawaban speaking...");
      try {
        const uploaded = await uploadExamSpeakingAudio({
          sessionId: manifest.sessionId,
          itemId,
          audio: blob
        });
        setDrafts((current) => ({
          ...current,
          [itemId]: {
            ...current[itemId],
            fileUrl: uploaded.fileUrl
          }
        }));
        setNotice("Jawaban speaking terunggah. Simpan bagian ini untuk menyimpannya.");
      } catch {
        setNotice("");
        setError(
          "Rekaman belum bisa diunggah. Kamu bisa merekam ulang atau lanjut; jawaban tertulis tetap akan dikirim."
        );
      }
    },
    onError: (message) => {
      setError(message);
      setActiveSpeakingItemId(null);
    },
    maxSeconds: 60,
    autoStopOnSilence: true
  });

  useEffect(() => {
    const audioUrls = audioUrlRef.current;
    return () => {
      Object.values(audioUrls).forEach((url) => URL.revokeObjectURL(url));
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setIsLoading(true);
      setError("");
      setNotice("");
      try {
        const nextTemplates = await listExamTemplatesByLevel(levelCode.toUpperCase());
        if (cancelled) {
          return;
        }
        setTemplates(nextTemplates);
        setActiveTemplate(nextTemplates[0] ?? null);
        void refreshLastResult();
        if (nextTemplates[0]) {
          void refreshAttemptStatus(nextTemplates[0].id);
        }

        const savedSessionId =
          typeof window !== "undefined" ? window.localStorage.getItem(sessionStorageKey(levelCode)) : null;
        if (!savedSessionId) {
          return;
        }

        try {
          const nextManifest = await getExamManifest(savedSessionId);
          if (cancelled) {
            return;
          }
          setManifest(nextManifest);
          setActiveTemplate(
            nextTemplates.find((entry) => entry.id === nextManifest.examTemplateId) ?? nextTemplates[0] ?? null
          );
          if (nextManifest.currentSectionId) {
            const nextContent = await getExamSectionContent(savedSessionId, nextManifest.currentSectionId);
            if (!cancelled) {
              setContent(nextContent);
            }
          }
        } catch {
          // The saved session no longer exists (e.g. the exam was reseeded).
          // Drop it and show the start screen instead of a page-level error.
          window.localStorage.removeItem(sessionStorageKey(levelCode));
        }
      } catch {
        if (!cancelled) {
          setError("Exam belum bisa dimuat.");
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, [levelCode, refreshAttemptStatus, refreshLastResult]);

  useEffect(() => {
    if (!manifest?.sessionId) {
      return;
    }
    const sessionId: string = manifest.sessionId;
    let disposed = false;

    async function refreshStatus() {
      try {
        const status = await getExamRunnerStatus(sessionId);
        if (!disposed) {
          setTimeRemaining(status.timeRemainingSeconds);
        }
      } catch {
        if (!disposed) {
          setTimeRemaining(null);
        }
      }
    }

    void refreshStatus();
    const interval = window.setInterval(() => {
      void refreshStatus();
    }, 1000);

    return () => {
      disposed = true;
      window.clearInterval(interval);
    };
  }, [manifest?.sessionId]);

  const sectionIndex = useMemo(() => {
    if (!manifest || !content) {
      return -1;
    }
    return manifest.sections.findIndex((section) => section.id === content.section.id);
  }, [content, manifest]);

  async function startExam() {
    if (!activeTemplate) {
      return;
    }
    setIsStarting(true);
    setError("");
    setNotice("");
    try {
      const session = await startRealExam(activeTemplate.id);
      const nextManifest = await getExamManifest(session.sessionId);
      const firstSectionId = nextManifest.currentSectionId ?? nextManifest.sections[0]?.id;
      const nextContent = firstSectionId
        ? await getExamSectionContent(session.sessionId, firstSectionId)
        : null;
      setManifest(nextManifest);
      setContent(nextContent);
      setTimeRemaining(session.timeRemainingSeconds);
      setDrafts({});
      window.localStorage.setItem(sessionStorageKey(levelCode), session.sessionId);
      trackEvent("exam_start", { level: levelCode.toUpperCase() });
      setNotice("Exam dimulai. Kerjakan tiap bagian dengan tenang; jawaban akan disimpan saat kamu lanjut.");
    } catch (startError) {
      if (startError instanceof ExamStartBlockedError) {
        if (startError.code === "exam_cooldown" && startError.nextAvailableAt) {
          const when = new Date(startError.nextAvailableAt).toLocaleDateString("id-ID", {
            day: "numeric",
            month: "long",
            year: "numeric"
          });
          setError(`Kamu sudah memakai kesempatan ujian ini. Bisa mengulang lagi pada ${when}.`);
        } else {
          setError("Kamu sudah memakai semua kesempatan untuk ujian ini.");
        }
        void refreshAttemptStatus(activeTemplate.id);
      } else {
          setError("Exam belum bisa dimulai.");
      }
    } finally {
      setIsStarting(false);
    }
  }

  async function openSection(
    sectionId: string,
    options: { saveBeforeNavigate?: boolean } = {}
  ) {
    if (!manifest) {
      return;
    }
    if (isSaving || isSubmitting) {
      return;
    }
    setError("");
    try {
      if (
        options.saveBeforeNavigate !== false &&
        content &&
        content.section.id !== sectionId
      ) {
        const saved = await saveCurrentSection();
        if (!saved) {
          return;
        }
      }
      await navigateExamSession({
        sessionId: manifest.sessionId,
        targetSectionId: sectionId
      });
      const nextContent = await getExamSectionContent(manifest.sessionId, sectionId);
      setContent(nextContent);
    } catch {
      setError("Bagian yang dipilih belum bisa dibuka.");
    }
  }

  function updateDraft(itemId: string, next: Partial<ItemDraft>) {
    setDrafts((current) => ({
      ...current,
      [itemId]: {
        ...current[itemId],
        ...next
      }
    }));
  }

  async function saveCurrentSection() {
    if (!manifest || !content) {
      return false;
    }
    setIsSaving(true);
    setError("");
    setNotice("");
    try {
      for (const item of content.items) {
        const draft = safeItemDraft(drafts, item.id);
        await saveExamItemResponse({
          sessionId: manifest.sessionId,
          itemId: item.id,
          sectionId: content.section.id,
          responseType: item.itemType,
          textResponse: draft.textResponse ?? "",
          selectedOptionIds: draft.selectedOptionIds ?? null,
          matchedPairs: draft.matchedPairs ?? null,
          fileUrl: draft.fileUrl ?? null,
          audioDurationSeconds: draft.audioDurationSeconds ?? null,
          timeSpentSeconds: null
        });
      }
      setNotice("Jawaban bagian ini tersimpan.");
      return true;
    } catch (saveError) {
      // An expired session is the common case and needs its own actionable
      // message — the generic "belum bisa disimpan" hides why saving failed.
      if (isExpiredSessionError(saveError)) {
        setManifest((current) => (current ? { ...current, status: "expired" } : current));
        setTimeRemaining(0);
        setError(
          "Waktu exam sudah habis, jadi jawaban tidak bisa disimpan lagi. Mulai percobaan baru untuk mengulang."
        );
      } else if (saveError instanceof ApiRequestError && saveError.detail) {
        setError(`Jawaban bagian ini belum bisa disimpan: ${saveError.detail}`);
      } else {
        setError("Jawaban bagian ini belum bisa disimpan. Periksa koneksi lalu coba lagi.");
      }
      return false;
    } finally {
      setIsSaving(false);
    }
  }

  async function saveAndContinue() {
    if (!manifest || !content || sectionIndex < 0) {
      return;
    }
    const saved = await saveCurrentSection();
    if (!saved) {
      return;
    }
    const nextSection = manifest.sections[sectionIndex + 1];
    if (nextSection) {
      await openSection(nextSection.id, { saveBeforeNavigate: false });
      setNotice("Bagian tersimpan. Lanjut ke bagian berikutnya.");
    }
  }

  async function finishExam() {
    if (!manifest) {
      return;
    }
    const saved = await saveCurrentSection();
    if (!saved) {
      return;
    }
    setIsSubmitting(true);
    setError("");
    setNotice("");
    try {
      const submitResult = await submitRealExam(manifest.sessionId);
      window.localStorage.removeItem(sessionStorageKey(levelCode));
      window.localStorage.setItem(lastResultStorageKey(levelCode), manifest.sessionId);
      void refreshLastResult();
      const scorePercent = Math.round(submitResult.score_percent);
      trackEvent("exam_submit", {
        level: levelCode.toUpperCase(),
        score_percent: scorePercent,
        result_status: submitResult.result_status
      });
      if (submitResult.pending_review_count > 0) {
        setNotice(
          `Exam terkirim. Nilai sementara: ${scorePercent}%. ` +
            `${submitResult.pending_review_count} jawaban speaking/writing menunggu review, ` +
            "jadi hasil final masih bisa berubah."
        );
      } else {
        setNotice(
          `Exam terkirim. Nilai final: ${scorePercent}% - ${submitResult.passed ? "Lulus" : "Belum lulus"}.`
        );
      }
      setManifest((current) => (current ? { ...current, status: "submitted" } : current));
      if (activeTemplate) {
        void refreshAttemptStatus(activeTemplate.id);
      }
    } catch {
      setError("Exam belum bisa dikirim.");
    } finally {
      setIsSubmitting(false);
    }
  }

  function speakStimulus(item: ExamRunnerItem) {
    if (typeof window === "undefined" || !("speechSynthesis" in window) || !item.stimulusText) {
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(item.stimulusText.replace(/\[BLANK\]/g, "blank"));
    utterance.lang = "en-US";
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  }

  function renderItem(item: ExamRunnerItem) {
    const draft = safeItemDraft(drafts, item.id);

    if (item.itemType === "mcq") {
      return (
        <div className="space-y-3">
          {item.options?.map((option) => (
            <label
              key={option.id}
              className="flex cursor-pointer items-start gap-3 rounded-xl border border-slate-200 px-4 py-3 text-sm text-slate-700"
            >
              <input
                type="radio"
                name={item.id}
                className="mt-1"
                checked={draft.selectedOptionIds?.[0] === option.id}
                onChange={() => updateDraft(item.id, { selectedOptionIds: [option.id] })}
              />
              <span>{option.text}</span>
            </label>
          ))}
        </div>
      );
    }

    if (item.itemType === "fill_blank") {
      const count = Math.max(1, blankCount(item.stimulusText));
      const values = (draft.textResponse ?? "").split("\n");
      return (
        <div className="space-y-3">
          {Array.from({ length: count }).map((_, index) => (
            <input
              key={`${item.id}-${index}`}
              value={values[index] ?? ""}
              onChange={(event) => {
                const next = [...values];
                next[index] = event.target.value;
                updateDraft(item.id, { textResponse: next.join("\n") });
              }}
              placeholder={`Blank ${index + 1}`}
              className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none ring-0 focus:border-emerald-500"
            />
          ))}
        </div>
      );
    }

    if (item.itemType === "matching") {
      const optionData = item.optionsData as
        | {
            left_items?: Array<{ id: string; text: string }>;
            right_items?: Array<{ id: string; text: string }>;
          }
        | undefined;
      const leftItems = optionData?.left_items ?? [];
      const rightItems = optionData?.right_items ?? [];

      return (
        <div className="space-y-3">
          {leftItems.map((leftItem) => (
            <div key={leftItem.id} className="grid gap-3 rounded-xl border border-slate-200 p-4 md:grid-cols-[1fr_220px]">
              <p className="text-sm text-slate-700">{leftItem.text}</p>
              <select
                value={draft.matchedPairs?.[leftItem.id] ?? ""}
                onChange={(event) =>
                  updateDraft(item.id, {
                    matchedPairs: {
                      ...(draft.matchedPairs ?? {}),
                      [leftItem.id]: event.target.value
                    }
                  })
                }
                className="rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:border-emerald-500"
              >
                <option value="">Pilih pasangan</option>
                {rightItems.map((rightItem) => (
                  <option key={rightItem.id} value={rightItem.id}>
                    {rightItem.text}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>
      );
    }

    if (item.itemType === "audio_response") {
      const localAudioUrl = draft.localPlaybackUrl ?? draft.fileUrl;
      return (
        <div className="space-y-3">
          <div className="flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={() => {
                setActiveSpeakingItemId(item.id);
                void recorder.start();
              }}
              disabled={recorder.status !== "idle"}
              className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              <Mic className="h-4 w-4" />
              {recorder.status === "recording" && activeSpeakingItemId === item.id ? "Merekam..." : "Rekam jawaban"}
            </button>
            {recorder.status === "recording" && activeSpeakingItemId === item.id ? (
              <button
                type="button"
                onClick={() => recorder.stop()}
                className="inline-flex items-center gap-2 rounded-xl border border-slate-300 px-4 py-3 text-sm font-semibold text-slate-700"
              >
                <PauseCircle className="h-4 w-4" />
                Hentikan
              </button>
            ) : null}
            {localAudioUrl ? <audio controls src={localAudioUrl} className="max-w-full" /> : null}
          </div>
          <textarea
            value={draft.textResponse ?? ""}
            onChange={(event) => updateDraft(item.id, { textResponse: event.target.value })}
            rows={4}
            placeholder="Catatan atau transkrip opsional untuk jawaban lisanmu"
            className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-emerald-500"
          />
        </div>
      );
    }

    return (
      <textarea
        value={draft.textResponse ?? ""}
        onChange={(event) => updateDraft(item.id, { textResponse: event.target.value })}
        rows={6}
        placeholder="Tulis jawaban di sini"
        className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-emerald-500"
      />
    );
  }

  if (isLoading) {
    return (
      <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex items-center gap-3 text-slate-700">
          <Loader2 className="h-5 w-5 animate-spin" />
          <span>Memuat exam...</span>
        </div>
      </section>
    );
  }

  if (!activeTemplate) {
    return (
      <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex items-start gap-3 text-slate-700">
          <AlertCircle className="mt-0.5 h-5 w-5 text-amber-600" />
          <div>
            <p className="font-semibold">Exam aktif untuk {levelCode.toUpperCase()} belum diterbitkan.</p>
            <p className="mt-1 text-sm text-slate-500">Setelah template exam dipublikasikan, halaman ini akan langsung bisa dipakai.</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
      <section className="space-y-5">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-emerald-700">
                Exam Resmi {activeTemplate.levelCode}
              </p>
              <h1 className="mt-2 text-3xl font-semibold text-slate-900">{activeTemplate.title}</h1>
              <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                {activeTemplate.description ?? "Sesi exam resmi untuk level ini."}
              </p>
            </div>
            <div className="rounded-2xl bg-slate-900 px-5 py-4 text-white">
              <p className="text-xs uppercase tracking-wide text-slate-300">Sisa Waktu</p>
              <p className="mt-2 flex items-center gap-2 text-2xl font-semibold">
                <Clock3 className="h-5 w-5" />
                {formatSeconds(timeRemaining)}
              </p>
            </div>
          </div>
          <div className="mt-5 flex flex-wrap items-center gap-3 text-sm">
            <span className="rounded-full bg-emerald-50 px-3 py-1 font-medium text-emerald-700">
              {activeTemplate.durationMinutes} menit
            </span>
            <span className="rounded-full bg-slate-100 px-3 py-1 font-medium text-slate-700">
              Nilai lulus {activeTemplate.passingScorePercent}%
            </span>
            {attemptStatus && attemptStatus.maxAttempts !== null ? (
              <span className="rounded-full bg-slate-100 px-3 py-1 font-medium text-slate-700">
                {attemptStatus.hasOpenSession
                  ? "Lanjutkan percobaan"
                  : `${attemptStatus.attemptsRemaining ?? 0} dari ${attemptStatus.maxAttempts} kesempatan tersisa`}
              </span>
            ) : null}
            {!manifest ? (
              <button
                type="button"
                onClick={() => void startExam()}
                disabled={isStarting || (attemptStatus ? !attemptStatus.canStart : false)}
                className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isStarting ? <Loader2 className="h-4 w-4 animate-spin" /> : <PlayCircle className="h-4 w-4" />}
                {attemptStatus?.hasOpenSession ? "Lanjutkan exam" : "Mulai exam"}
              </button>
            ) : (
              <span className="rounded-full bg-blue-50 px-3 py-1 font-medium text-blue-700">
                Sesi {manifest.status}
              </span>
            )}
          </div>
        </div>

        {manifest && manifest.status !== "submitted" && timeRemaining === 0 ? (
          <div className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
            Waktu exam sudah habis. Jawaban baru tidak bisa disimpan lagi — mulai percobaan baru untuk mengulang.
          </div>
        ) : null}
        {error ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>
        ) : null}
        {notice ? (
          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">{notice}</div>
        ) : null}

        {!manifest && lastResult ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Hasil exam terakhir</p>
                {lastResult.status === "published" ? (
                  <p className="mt-2 text-2xl font-semibold text-slate-900">
                    {Math.round(lastResult.scorePercent)}%{" "}
                    <span className={lastResult.passed ? "text-emerald-600" : "text-rose-600"}>
                      {lastResult.passed ? "Lulus" : "Belum lulus"}
                    </span>
                  </p>
                ) : (
                  <p className="mt-2 text-lg font-semibold text-slate-900">
                    Nilai sementara {Math.round(lastResult.scorePercent)}% - jawaban speaking/writing masih direview.
                  </p>
                )}
              </div>
              <span
                className={`rounded-full px-3 py-1 text-xs font-semibold ${
                  lastResult.status === "published" ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-700"
                }`}
              >
                {lastResult.status === "published" ? "Final" : "Menunggu review"}
              </span>
            </div>
            <div className="mt-4 grid gap-2 sm:grid-cols-2">
              {Object.entries(lastResult.sectionScores).map(([code, section]) => (
                <div key={code} className="rounded-xl bg-slate-50 px-4 py-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium capitalize text-slate-700">
                      {code.replace(/_/g, " ").toLowerCase()}
                    </span>
                    <span className="text-slate-600">
                      {section.score}/{section.max} ({Math.round(section.percentage)}%)
                    </span>
                  </div>
                  <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-200">
                    <div
                      className="h-full rounded-full bg-emerald-500"
                      style={{ width: `${Math.min(100, Math.max(0, section.percentage))}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : null}

        {manifest && content ? (
          <div className="space-y-4">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Bagian {content.currentSectionNumber} dari {content.totalSections}
                  </p>
                  <h2 className="mt-2 text-2xl font-semibold text-slate-900">{content.section.title}</h2>
                  <p className="mt-2 text-sm text-slate-600">{content.section.description}</p>
                </div>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">
                  {content.section.durationMinutes} min
                </span>
              </div>
            </div>

            {content.items.map((item, index) => (
              <article key={item.id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Soal {index + 1}
                    </p>
                    <h3 className="mt-2 text-lg font-semibold text-slate-900">{item.promptText}</h3>
                  </div>
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                    {item.scorePoints} pts
                  </span>
                </div>

                {item.stimulusText ? (
                  <div className="mt-4 rounded-2xl bg-slate-50 p-4">
                    {/* Hide the listening transcript when real audio exists — reading it would
                        defeat the listening test. Gapped (fill-blank) text stays visible. */}
                    {content.section.code === "LISTENING" &&
                    item.stimulusAudioUrl &&
                    !item.stimulusText.includes("[BLANK]") ? (
                      <p className="text-sm font-medium text-slate-600">
                        Dengarkan audio, lalu jawab. Audio bisa diputar ulang.
                      </p>
                    ) : (
                      <p className="whitespace-pre-wrap text-sm leading-7 text-slate-700">{item.stimulusText}</p>
                    )}
                    <div className="mt-3 flex flex-wrap gap-3">
                      {item.stimulusAudioUrl ? (
                        <audio controls src={item.stimulusAudioUrl} className="max-w-full" />
                      ) : (
                        <button
                          type="button"
                          onClick={() => speakStimulus(item)}
                          className="inline-flex items-center gap-2 rounded-xl border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700"
                        >
                          <PlayCircle className="h-4 w-4" />
                          Putar audio prompt
                        </button>
                      )}
                    </div>
                  </div>
                ) : null}

                <div className="mt-5">{renderItem(item)}</div>
              </article>
            ))}

            <div className="flex flex-wrap justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <button
                type="button"
                onClick={() => void saveCurrentSection()}
                disabled={isSaving || isSubmitting}
                className="inline-flex items-center gap-2 rounded-xl border border-slate-300 px-4 py-3 text-sm font-semibold text-slate-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
                Simpan bagian
              </button>

              <div className="flex flex-wrap gap-3">
                {sectionIndex < manifest.sections.length - 1 ? (
                  <button
                    type="button"
                    onClick={() => void saveAndContinue()}
                    disabled={isSaving || isSubmitting}
                    className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
                    Simpan dan lanjut
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={() => void finishExam()}
                    disabled={isSaving || isSubmitting}
                    className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                    Kirim exam
                  </button>
                )}
              </div>
            </div>
          </div>
        ) : null}
      </section>

      <aside className="space-y-4">
        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Bagian</h2>
          <div className="mt-4 space-y-3">
            {(manifest?.sections ?? []).map((section) => {
              const isActive = content?.section.id === section.id;
              return (
                <button
                  key={section.id}
                  type="button"
                  onClick={() => void openSection(section.id)}
                  disabled={isSaving || isSubmitting}
                  className={`w-full rounded-2xl border px-4 py-3 text-left ${
                    isActive
                      ? "border-emerald-500 bg-emerald-50 text-emerald-800"
                      : "border-slate-200 bg-white text-slate-700"
                  } disabled:cursor-not-allowed disabled:opacity-60`}
                >
                  <p className="text-xs font-semibold uppercase tracking-wide">{section.code}</p>
                  <p className="mt-1 text-sm font-medium">{section.title}</p>
                </button>
              );
            })}
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Catatan Penilaian</h2>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-slate-600">
            <li>Waktu berjalan setelah exam dimulai.</li>
            <li>Jawaban disimpan saat kamu menyimpan atau berpindah bagian.</li>
            <li>Speaking dan writing dapat menunggu review sebelum hasil final diterbitkan.</li>
          </ul>
        </section>
      </aside>
    </div>
  );
}
