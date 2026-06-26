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

// Friendly Indonesian label + accent for a raw session status, so the UI never
// shows the API's bare "in_progress"/"expired" strings.
function sessionStatusBadge(status: string): { label: string; className: string } {
  switch (status) {
    case "in_progress":
      return { label: "Sedang berlangsung", className: "bg-mint text-leaf" };
    case "submitted":
      return { label: "Sudah dikirim", className: "bg-mint text-leaf" };
    case "expired":
      return { label: "Waktu habis", className: "bg-[#fde7df] text-coral" };
    default:
      return { label: "Tersimpan", className: "bg-paper text-ink/70" };
  }
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
        if (disposed) {
          return;
        }
        setTimeRemaining(status.timeRemainingSeconds);
        // Time ran out — reflect it in the session state so the badge, timer,
        // and actions update on load, not only after a failed save.
        if (status.timeRemainingSeconds === 0) {
          setManifest((current) =>
            current && current.status === "in_progress" ? { ...current, status: "expired" } : current
          );
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

  const isExpired = manifest?.status === "expired" || (Boolean(manifest) && timeRemaining === 0);

  async function restartAfterExpiry() {
    if (!manifest || !activeTemplate) {
      return;
    }
    setIsStarting(true);
    setError("");
    setNotice("");
    try {
      // Terminate the expired session server-side (submit flips it to a used
      // state) so the next start creates a fresh attempt instead of resuming it.
      await submitRealExam(manifest.sessionId).catch(() => undefined);
      window.localStorage.removeItem(sessionStorageKey(levelCode));
      setManifest(null);
      setContent(null);
      setTimeRemaining(null);
      setDrafts({});
      await startExam();
    } finally {
      setIsStarting(false);
    }
  }

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
              className="flex cursor-pointer items-start gap-3 rounded-lg border border-ink/10 px-4 py-3 text-sm text-ink/70"
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
              className="w-full rounded-lg border border-ink/10 px-4 py-3 text-sm outline-none ring-0 focus:border-leaf"
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
            <div key={leftItem.id} className="grid gap-3 rounded-lg border border-ink/10 p-4 md:grid-cols-[1fr_220px]">
              <p className="text-sm text-ink/70">{leftItem.text}</p>
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
                className="rounded-lg border border-ink/10 px-3 py-2 text-sm outline-none focus:border-leaf"
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
              className="inline-flex items-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              <Mic className="h-4 w-4" />
              {recorder.status === "recording" && activeSpeakingItemId === item.id ? "Merekam..." : "Rekam jawaban"}
            </button>
            {recorder.status === "recording" && activeSpeakingItemId === item.id ? (
              <button
                type="button"
                onClick={() => recorder.stop()}
                className="inline-flex items-center gap-2 rounded-lg border border-ink/20 px-4 py-3 text-sm font-semibold text-ink/70"
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
            className="w-full rounded-lg border border-ink/10 px-4 py-3 text-sm outline-none focus:border-leaf"
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
        className="w-full rounded-lg border border-ink/10 px-4 py-3 text-sm outline-none focus:border-leaf"
      />
    );
  }

  if (isLoading) {
    return (
      <section className="rounded-lg border border-ink/10 bg-white p-8 shadow-sm">
        <div className="flex items-center gap-3 text-ink/70">
          <Loader2 className="h-5 w-5 animate-spin" />
          <span>Memuat exam...</span>
        </div>
      </section>
    );
  }

  if (!activeTemplate) {
    return (
      <section className="rounded-lg border border-ink/10 bg-white p-8 shadow-sm">
        <div className="flex items-start gap-3 text-ink/70">
          <AlertCircle className="mt-0.5 h-5 w-5 text-coral" />
          <div>
            <p className="font-semibold">Exam aktif untuk {levelCode.toUpperCase()} belum diterbitkan.</p>
            <p className="mt-1 text-sm text-ink/50">Setelah template exam dipublikasikan, halaman ini akan langsung bisa dipakai.</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
      <section className="space-y-5">
        <div className="rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-leaf">
                Exam Resmi {activeTemplate.levelCode}
              </p>
              <h1 className="mt-2 text-3xl font-semibold text-ink">{activeTemplate.title}</h1>
              <p className="mt-3 max-w-3xl text-sm leading-7 text-ink/65">
                {activeTemplate.description ?? "Sesi exam resmi untuk level ini."}
              </p>
            </div>
            <div className={`rounded-lg px-5 py-4 ${isExpired ? "bg-[#fde7df] text-coral" : "bg-ink text-white"}`}>
              <p className={`text-xs uppercase tracking-wide ${isExpired ? "text-coral/80" : "text-white/70"}`}>
                Sisa Waktu
              </p>
              <p className="mt-2 flex items-center gap-2 text-2xl font-semibold">
                <Clock3 className="h-5 w-5" />
                {formatSeconds(timeRemaining)}
              </p>
            </div>
          </div>
          <div className="mt-5 flex flex-wrap items-center gap-3 text-sm">
            <span className="rounded-full bg-mint px-3 py-1 font-medium text-leaf">
              {activeTemplate.durationMinutes} menit
            </span>
            <span className="rounded-full bg-paper px-3 py-1 font-medium text-ink/70">
              Nilai lulus {activeTemplate.passingScorePercent}%
            </span>
            {attemptStatus && attemptStatus.maxAttempts !== null ? (
              <span className="rounded-full bg-paper px-3 py-1 font-medium text-ink/70">
                {attemptStatus.hasOpenSession && !isExpired
                  ? "Lanjutkan percobaan"
                  : `${attemptStatus.attemptsRemaining ?? 0} dari ${attemptStatus.maxAttempts} kesempatan tersisa`}
              </span>
            ) : null}
            {manifest ? (
              <span className={`rounded-full px-3 py-1 font-medium ${sessionStatusBadge(manifest.status).className}`}>
                {sessionStatusBadge(manifest.status).label}
              </span>
            ) : null}
            {!manifest || isExpired ? (
              <button
                type="button"
                onClick={() => void (isExpired ? restartAfterExpiry() : startExam())}
                disabled={isStarting || (!isExpired && attemptStatus ? !attemptStatus.canStart : false)}
                className="focus-ring inline-flex items-center gap-2 rounded-lg bg-leaf px-4 py-3 font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isStarting ? <Loader2 className="h-4 w-4 animate-spin" /> : <PlayCircle className="h-4 w-4" />}
                {isExpired
                  ? "Mulai percobaan baru"
                  : attemptStatus?.hasOpenSession
                    ? "Lanjutkan exam"
                    : "Mulai exam"}
              </button>
            ) : null}
          </div>
        </div>

        {isExpired ? (
          <div className="rounded-lg border border-coral/30 bg-[#fde7df] px-4 py-3 text-sm text-coral">
            Waktu exam sudah habis. Jawaban baru tidak bisa disimpan lagi — gunakan tombol{" "}
            <span className="font-semibold">Mulai percobaan baru</span> di atas untuk mengulang.
          </div>
        ) : error ? (
          <div className="rounded-lg border border-coral/30 bg-[#fde7df] px-4 py-3 text-sm text-coral">{error}</div>
        ) : null}
        {notice ? (
          <div className="rounded-lg border border-leaf/30 bg-mint px-4 py-3 text-sm text-leaf">{notice}</div>
        ) : null}

        {!manifest && lastResult ? (
          <div className="rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-ink/50">Hasil exam terakhir</p>
                {lastResult.status === "published" ? (
                  <p className="mt-2 text-2xl font-semibold text-ink">
                    {Math.round(lastResult.scorePercent)}%{" "}
                    <span className={lastResult.passed ? "text-leaf" : "text-coral"}>
                      {lastResult.passed ? "Lulus" : "Belum lulus"}
                    </span>
                  </p>
                ) : (
                  <p className="mt-2 text-lg font-semibold text-ink">
                    Nilai sementara {Math.round(lastResult.scorePercent)}% - jawaban speaking/writing masih direview.
                  </p>
                )}
              </div>
              <span
                className={`rounded-full px-3 py-1 text-xs font-semibold ${
                  lastResult.status === "published" ? "bg-mint text-leaf" : "bg-[#fde7df] text-coral"
                }`}
              >
                {lastResult.status === "published" ? "Final" : "Menunggu review"}
              </span>
            </div>
            <div className="mt-4 grid gap-2 sm:grid-cols-2">
              {Object.entries(lastResult.sectionScores).map(([code, section]) => (
                <div key={code} className="rounded-lg bg-paper px-4 py-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium capitalize text-ink/70">
                      {code.replace(/_/g, " ").toLowerCase()}
                    </span>
                    <span className="text-ink/65">
                      {section.score}/{section.max} ({Math.round(section.percentage)}%)
                    </span>
                  </div>
                  <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-ink/10">
                    <div
                      className="h-full rounded-full bg-leaf"
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
            <div className="rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-ink/50">
                    Bagian {content.currentSectionNumber} dari {content.totalSections}
                  </p>
                  <h2 className="mt-2 text-2xl font-semibold text-ink">{content.section.title}</h2>
                  <p className="mt-2 text-sm text-ink/65">{content.section.description}</p>
                </div>
                <span className="rounded-full bg-paper px-3 py-1 text-sm font-medium text-ink/70">
                  {content.section.durationMinutes} min
                </span>
              </div>
            </div>

            {content.items.map((item, index) => (
              <article key={item.id} className="rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-ink/50">
                      Soal {index + 1}
                    </p>
                    <h3 className="mt-2 text-lg font-semibold text-ink">{item.promptText}</h3>
                  </div>
                  <span className="rounded-full bg-paper px-3 py-1 text-xs font-medium text-ink/70">
                    {item.scorePoints} pts
                  </span>
                </div>

                {item.stimulusText ? (
                  <div className="mt-4 rounded-lg bg-paper p-4">
                    {/* Hide the listening transcript when real audio exists — reading it would
                        defeat the listening test. Gapped (fill-blank) text stays visible. */}
                    {content.section.code === "LISTENING" &&
                    item.stimulusAudioUrl &&
                    !item.stimulusText.includes("[BLANK]") ? (
                      <p className="text-sm font-medium text-ink/65">
                        Dengarkan audio, lalu jawab. Audio bisa diputar ulang.
                      </p>
                    ) : (
                      <p className="whitespace-pre-wrap text-sm leading-7 text-ink/70">{item.stimulusText}</p>
                    )}
                    <div className="mt-3 flex flex-wrap gap-3">
                      {item.stimulusAudioUrl ? (
                        <audio controls src={item.stimulusAudioUrl} className="max-w-full" />
                      ) : (
                        <button
                          type="button"
                          onClick={() => speakStimulus(item)}
                          className="inline-flex items-center gap-2 rounded-lg border border-ink/20 px-4 py-2 text-sm font-semibold text-ink/70"
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

            <div className="flex flex-wrap justify-between gap-3 rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
              <button
                type="button"
                onClick={() => void saveCurrentSection()}
                disabled={isSaving || isSubmitting}
                className="inline-flex items-center gap-2 rounded-lg border border-ink/20 px-4 py-3 text-sm font-semibold text-ink/70 disabled:cursor-not-allowed disabled:opacity-60"
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
                    className="inline-flex items-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
                    Simpan dan lanjut
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={() => void finishExam()}
                    disabled={isSaving || isSubmitting}
                    className="inline-flex items-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
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
        <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold text-ink">Bagian</h2>
          <div className="mt-4 space-y-3">
            {(manifest?.sections ?? []).map((section) => {
              const isActive = content?.section.id === section.id;
              return (
                <button
                  key={section.id}
                  type="button"
                  onClick={() => void openSection(section.id)}
                  disabled={isSaving || isSubmitting}
                  className={`w-full rounded-lg border px-4 py-3 text-left ${
                    isActive
                      ? "border-leaf bg-mint text-leaf"
                      : "border-ink/10 bg-white text-ink/70"
                  } disabled:cursor-not-allowed disabled:opacity-60`}
                >
                  <p className="text-xs font-semibold uppercase tracking-wide">{section.code}</p>
                  <p className="mt-1 text-sm font-medium">{section.title}</p>
                </button>
              );
            })}
          </div>
        </section>

        <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold text-ink">Catatan Penilaian</h2>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-ink/65">
            <li>Waktu berjalan setelah exam dimulai.</li>
            <li>Jawaban disimpan saat kamu menyimpan atau berpindah bagian.</li>
            <li>Speaking dan writing dapat menunggu review sebelum hasil final diterbitkan.</li>
          </ul>
        </section>
      </aside>
    </div>
  );
}
