"use client";

import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  BookOpen,
  CheckCircle2,
  Clock3,
  ExternalLink,
  FileText,
  Headphones,
  ListChecks,
  PlayCircle,
  RefreshCcw,
  RotateCcw,
  Save,
  ShieldCheck,
  Sparkles,
  Volume2,
  XCircle,
  type LucideIcon
} from "lucide-react";
import type { ReactNode } from "react";
import type { AuthUser } from "@/lib/auth-api";
import {
  generateAdminLessonAudio,
  getAdminAudioSettings,
  getAdminCmsLesson,
  getAdminCmsSummary,
  getAdminEmailTemplate,
  getAdminVoicePreviews,
  previewAdminVoiceAudio,
  rollbackAdminCmsRevision,
  updateAdminCmsLesson,
  updateAdminEmailTemplate,
  type AdminContentReadiness,
  type AdminContentReadinessLesson,
  type AdminContentReadinessOverview,
  type AdminContentRevision,
  type AdminAudioSettings,
  type AdminCmsLesson,
  type AdminCmsSummary,
  type AdminEmailTemplate,
  type AdminVoicePreviewAudio
} from "@/lib/admin-cms-api";

const adminNameStorageKey = "conversease.admin_name";
const audioModelStorageKey = "conversease.admin_audio_model";
const audioVoiceStorageKey = "conversease.admin_audio_voice";
const audioSpeedStorageKey = "conversease.admin_audio_speed";
const statusOptions = ["draft", "review", "published", "archived"];

type Tab = "readiness" | "curriculum" | "email";

export function AdminCmsManager({ adminUser }: { adminUser: AuthUser }) {
  const [adminName, setAdminName] = useState(adminUser.name || adminUser.email);
  const [summary, setSummary] = useState<AdminCmsSummary | null>(null);
  const [tab, setTab] = useState<Tab>("readiness");
  const [selectedLesson, setSelectedLesson] = useState<AdminCmsLesson | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<AdminEmailTemplate | null>(null);
  const [audioSettings, setAudioSettings] = useState<AdminAudioSettings | null>(null);
  const [audioModel, setAudioModel] = useState("");
  const [audioVoiceId, setAudioVoiceId] = useState("");
  const [audioSpeed, setAudioSpeed] = useState(1);
  const [voicePreview, setVoicePreview] = useState<AdminVoicePreviewAudio | null>(null);
  const [voicePreviewsByVoiceId, setVoicePreviewsByVoiceId] = useState<Record<string, AdminVoicePreviewAudio>>({});
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [restoringRevisionId, setRestoringRevisionId] = useState("");
  const [generatingLessonSlug, setGeneratingLessonSlug] = useState("");
  const [isPreviewingVoice, setIsPreviewingVoice] = useState(false);
  const [isLoadingVoicePreviews, setIsLoadingVoicePreviews] = useState(false);

  useEffect(() => {
    const storedName = window.sessionStorage.getItem(adminNameStorageKey);
    if (storedName) {
      setAdminName(storedName);
    }
  }, []);

  useEffect(() => {
    if (adminName.trim()) {
      window.sessionStorage.setItem(adminNameStorageKey, adminName);
    }
  }, [adminName]);

  useEffect(() => {
    if (audioModel) {
      window.localStorage.setItem(audioModelStorageKey, audioModel);
    }
  }, [audioModel]);

  useEffect(() => {
    if (audioVoiceId) {
      window.localStorage.setItem(audioVoiceStorageKey, audioVoiceId);
    }
  }, [audioVoiceId]);

  useEffect(() => {
    window.localStorage.setItem(audioSpeedStorageKey, String(audioSpeed));
  }, [audioSpeed]);

  useEffect(() => {
    setVoicePreview(null);
  }, [audioModel, audioVoiceId, audioSpeed]);

  useEffect(() => {
    if (!audioModel) {
      setVoicePreviewsByVoiceId({});
      return;
    }

    let cancelled = false;
    setIsLoadingVoicePreviews(true);
    void getAdminVoicePreviews({ model: audioModel, speed: audioSpeed })
      .then((previews) => {
        if (cancelled) {
          return;
        }
        setVoicePreviewsByVoiceId(
          Object.fromEntries(previews.map((preview) => [preview.voiceId, preview]))
        );
      })
      .catch(() => {
        if (!cancelled) {
          setVoicePreviewsByVoiceId({});
        }
      })
      .finally(() => {
        if (!cancelled) {
          setIsLoadingVoicePreviews(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [audioModel, audioSpeed]);

  useEffect(() => {
    void loadSummary();
    // Load once when this admin screen opens.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const validationOk = (summary?.curriculum.validationIssues.length ?? 1) === 0;

  async function loadSummary() {
    setIsLoading(true);
    setMessage("");
    setError("");

    try {
      const [nextSummary, nextAudioSettings] = await Promise.all([
        getAdminCmsSummary(),
        getAdminAudioSettings()
      ]);
      setSummary(nextSummary);
      setAudioSettings(nextAudioSettings);
      setAudioModel((current) => current || storedAudioModel(nextAudioSettings.defaultModel));
      setAudioVoiceId((current) => current || storedAudioVoice(nextAudioSettings.defaultVoiceId));
      setAudioSpeed((current) => (current === 1 ? storedAudioSpeed() : current));
      setSelectedLesson(nextSummary.curriculum.lessons[0] ?? null);
      setSelectedTemplate(nextSummary.emailTemplates[0] ?? null);
      setMessage("CMS content berhasil dimuat.");
    } catch {
      setError("CMS belum bisa dimuat. Pastikan akunmu punya role admin atau cek koneksi API.");
    } finally {
      setIsLoading(false);
    }
  }

  async function generateLessonAudio(lesson: AdminContentReadinessLesson) {
    if (!audioModel || !audioVoiceId) {
      setError("Pilih model dan voice sebelum generate audio.");
      return;
    }

    setGeneratingLessonSlug(lesson.slug);
    setMessage("");
    setError("");

    try {
      const audio = await generateAdminLessonAudio({
        generatedBy: adminName,
        lessonSlug: lesson.slug,
        model: audioModel,
        voiceId: audioVoiceId,
        speed: audioSpeed
      });
      const nextSummary = await getAdminCmsSummary();
      setSummary(nextSummary);
      setMessage(`Audio ${audio.title} berhasil dibuat (${formatDuration(audio.durationSeconds)}).`);
    } catch (caughtError) {
      setError(audioGenerationErrorMessage(caughtError));
    } finally {
      setGeneratingLessonSlug("");
    }
  }

  async function previewVoiceAudio() {
    if (!audioModel || !audioVoiceId) {
      setError("Pilih model dan voice sebelum preview suara.");
      return;
    }

    setIsPreviewingVoice(true);
    setMessage("");
    setError("");

    try {
      const preview = await previewAdminVoiceAudio({
        generatedBy: adminName,
        model: audioModel,
        voiceId: audioVoiceId,
        speed: audioSpeed
      });
      setVoicePreview(preview);
      setVoicePreviewsByVoiceId((current) => ({ ...current, [preview.voiceId]: preview }));
      setMessage(
        `Preview voice ${preview.voiceId} ${
          preview.cached ? "siap dari cache" : "berhasil dibuat"
        } (${formatDuration(preview.durationSeconds)}).`
      );
    } catch (caughtError) {
      setError(audioGenerationErrorMessage(caughtError));
    } finally {
      setIsPreviewingVoice(false);
    }
  }

  async function selectLesson(slug: string) {
    setError("");
    try {
      setSelectedLesson(await getAdminCmsLesson(slug));
    } catch {
      setError("Lesson belum bisa dimuat.");
    }
  }

  async function selectTemplate(templateKey: string) {
    setError("");
    try {
      setSelectedTemplate(await getAdminEmailTemplate(templateKey));
    } catch {
      setError("Email template belum bisa dimuat.");
    }
  }

  async function rollbackRevision(revision: AdminContentRevision) {
    setRestoringRevisionId(revision.id);
    setMessage("");
    setError("");

    try {
      const result = await rollbackAdminCmsRevision({
        revisionId: revision.id,
        restoredBy: adminName,
        notes: `Restored from ${revision.resourceKey} v${revision.version}`
      });
      await loadSummary();

      if (result.resourceType === "curriculum_lesson") {
        setTab("curriculum");
        setSelectedLesson(result.data);
      } else {
        setTab("email");
        setSelectedTemplate(result.data);
      }

      setMessage(`${revision.resourceKey} berhasil direstore ke v${revision.version}.`);
    } catch {
      setError("Revision belum bisa direstore. Cek role admin, revision, atau validasi content.");
    } finally {
      setRestoringRevisionId("");
    }
  }

  return (
    <div className="space-y-5">
      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
          <div className="flex items-start gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-mint">
              <ShieldCheck className="h-5 w-5 text-leaf" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">Admin CMS</p>
              <h1 className="mt-1 text-2xl font-semibold">Content Control</h1>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-ink/60">
                Review, edit, dan validasi kurikulum serta email template sebelum rilis.
              </p>
            </div>
          </div>

          <div className="grid gap-3 sm:grid-cols-[minmax(220px,1fr)_180px] xl:w-[560px]">
            <label className="text-sm font-medium text-ink/70">
              Operator
              <input
                value={adminName}
                onChange={(event) => setAdminName(event.target.value)}
                className="focus-ring mt-2 h-11 w-full rounded-lg border border-ink/15 bg-white px-3 text-ink"
                placeholder="Nama admin"
              />
            </label>
            <button
              type="button"
              onClick={loadSummary}
              disabled={isLoading}
              className="focus-ring mt-auto inline-flex h-11 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
            >
              <RefreshCcw className="h-4 w-4" aria-hidden="true" />
              {isLoading ? "Loading" : "Refresh"}
            </button>
          </div>
        </div>

        <div className="mt-5 grid gap-3 lg:grid-cols-[1fr_1fr_1fr]">
          <div className="rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">
            Login sebagai <span className="font-semibold text-ink">{adminUser.email}</span>
          </div>

          {summary ? (
            validationOk ? (
              <div className="flex items-center gap-2 rounded-lg bg-mint px-4 py-3 text-sm font-semibold text-ink/70">
                <ShieldCheck className="h-4 w-4 text-leaf" aria-hidden="true" />
                Curriculum validation passed.
              </div>
            ) : (
              <div className="rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">
                {summary.curriculum.validationIssues.map((issue) => (
                  <p key={issue}>{issue}</p>
                ))}
              </div>
            )
          ) : (
            <div className="rounded-lg bg-paper px-4 py-3 text-sm text-ink/60">
              Load CMS untuk melihat status validasi content.
            </div>
          )}

          {error ? (
            <div className="rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">{error}</div>
          ) : message ? (
            <div className="rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">{message}</div>
          ) : (
            <div className="rounded-lg bg-paper px-4 py-3 text-sm text-ink/60">Siap untuk review content.</div>
          )}
        </div>
      </section>

      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-wrap gap-2">
          <TabButton active={tab === "readiness"} icon={ListChecks} onClick={() => setTab("readiness")}>
            Readiness
          </TabButton>
          <TabButton active={tab === "curriculum"} icon={BookOpen} onClick={() => setTab("curriculum")}>
            Curriculum
          </TabButton>
          <TabButton active={tab === "email"} icon={FileText} onClick={() => setTab("email")}>
            Email Templates
          </TabButton>
        </div>

        {tab === "readiness" ? (
          <ReadinessPanel
            overview={summary?.curriculum.readinessOverview ?? null}
            levels={summary?.curriculum.readinessLevels ?? []}
            audioSettings={audioSettings}
            audioModel={audioModel}
            audioVoiceId={audioVoiceId}
            audioSpeed={audioSpeed}
            voicePreview={voicePreview ?? voicePreviewsByVoiceId[audioVoiceId] ?? null}
            generatingLessonSlug={generatingLessonSlug}
            isPreviewingVoice={isPreviewingVoice}
            isLoadingVoicePreviews={isLoadingVoicePreviews}
            onAudioModelChange={setAudioModel}
            onAudioVoiceChange={setAudioVoiceId}
            onAudioSpeedChange={setAudioSpeed}
            onGenerateAudio={generateLessonAudio}
            onPreviewVoice={previewVoiceAudio}
          />
        ) : tab === "curriculum" ? (
          <CurriculumEditor
            updatedBy={adminName}
            lessons={summary?.curriculum.lessons ?? []}
            selectedLesson={selectedLesson}
            onSelectLesson={selectLesson}
            onSaved={(lesson) => {
              setSelectedLesson(lesson);
              setMessage("Lesson tersimpan dan curriculum cache sudah diperbarui.");
              void loadSummary();
            }}
            onError={setError}
          />
        ) : (
          <EmailTemplateEditor
            updatedBy={adminName}
            templates={summary?.emailTemplates ?? []}
            selectedTemplate={selectedTemplate}
            onSelectTemplate={selectTemplate}
            onSaved={(template) => {
              setSelectedTemplate(template);
              setMessage("Email template tersimpan.");
              void loadSummary();
            }}
            onError={setError}
          />
        )}
      </section>

      <ChangeLogPanel
        revisions={summary?.recentRevisions ?? []}
        restoringRevisionId={restoringRevisionId}
        onRollback={rollbackRevision}
      />
    </div>
  );
}

function ChangeLogPanel({
  revisions,
  restoringRevisionId,
  onRollback
}: {
  revisions: AdminContentRevision[];
  restoringRevisionId: string;
  onRollback: (revision: AdminContentRevision) => void;
}) {
  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-2">
        <Clock3 className="h-5 w-5 text-leaf" aria-hidden="true" />
        <h2 className="font-semibold">Change Log</h2>
      </div>
      {revisions.length ? (
        <div className="mt-3 grid gap-2 md:grid-cols-2 xl:grid-cols-3">
          {revisions.map((revision) => (
            <div key={revision.id} className="rounded-lg bg-paper p-3 text-sm">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-semibold">
                    {revision.resourceKey} v{revision.version}
                  </p>
                  <p className="mt-1 text-xs text-ink/55">
                    {revision.resourceType} / {revision.action} / {revision.changedBy}
                  </p>
                </div>
                {revision.resourceType === "curriculum_lesson" || revision.resourceType === "email_template" ? (
                  <button
                    type="button"
                    onClick={() => onRollback(revision)}
                    disabled={restoringRevisionId === revision.id}
                    className="focus-ring inline-flex min-h-8 items-center justify-center gap-1 rounded-lg bg-white px-2 text-xs font-semibold text-ink hover:bg-mint disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    <RotateCcw className="h-3.5 w-3.5" aria-hidden="true" />
                    {restoringRevisionId === revision.id ? "Restoring" : "Restore"}
                  </button>
                ) : (
                  <span className="inline-flex min-h-8 items-center rounded-lg bg-white px-2 text-xs font-semibold text-ink/55">
                    Audit
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="mt-3 text-sm leading-6 text-ink/60">Belum ada revision yang tercatat.</p>
      )}
    </section>
  );
}

function ReadinessPanel({
  overview,
  levels,
  audioSettings,
  audioModel,
  audioVoiceId,
  audioSpeed,
  voicePreview,
  generatingLessonSlug,
  isPreviewingVoice,
  isLoadingVoicePreviews,
  onAudioModelChange,
  onAudioVoiceChange,
  onAudioSpeedChange,
  onGenerateAudio,
  onPreviewVoice
}: {
  overview: AdminContentReadinessOverview | null;
  levels: AdminContentReadiness[];
  audioSettings: AdminAudioSettings | null;
  audioModel: string;
  audioVoiceId: string;
  audioSpeed: number;
  voicePreview: AdminVoicePreviewAudio | null;
  generatingLessonSlug: string;
  isPreviewingVoice: boolean;
  isLoadingVoicePreviews: boolean;
  onAudioModelChange: (value: string) => void;
  onAudioVoiceChange: (value: string) => void;
  onAudioSpeedChange: (value: number) => void;
  onGenerateAudio: (lesson: AdminContentReadinessLesson) => void;
  onPreviewVoice: () => void;
}) {
  if (!overview) {
    return <p className="mt-5 rounded-lg bg-paper p-5 text-sm text-ink/60">Load CMS dulu.</p>;
  }

  const stats = [
    { label: "Planned", value: overview.plannedLessonCount },
    { label: "Implemented", value: overview.implementedLessonCount },
    { label: "Text ready", value: overview.textReadyCount },
    { label: "Audio ready", value: overview.audioReadyCount },
    { label: "Beta ready", value: overview.betaReadyCount },
    { label: "Production ready", value: overview.productionReadyCount }
  ];

  return (
    <div className="mt-5 space-y-5">
      <AudioSettingsPanel
        settings={audioSettings}
        model={audioModel}
        voiceId={audioVoiceId}
        speed={audioSpeed}
        preview={voicePreview}
        isPreviewing={isPreviewingVoice}
        isLoadingPreviewCache={isLoadingVoicePreviews}
        onModelChange={onAudioModelChange}
        onVoiceChange={onAudioVoiceChange}
        onSpeedChange={onAudioSpeedChange}
        onPreview={onPreviewVoice}
      />

      <div className="grid gap-3 md:grid-cols-3 xl:grid-cols-6">
        {stats.map((stat) => (
          <div key={stat.label} className="rounded-lg bg-paper p-4">
            <p className="text-xs font-semibold uppercase text-ink/45">{stat.label}</p>
            <p className="mt-2 text-2xl font-semibold">{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="grid gap-4">
        {levels.map((level) => (
          <LevelReadinessCard
            key={`${level.course.language}-${level.course.levelCode}`}
            readiness={level}
            audioReadyToGenerate={Boolean(audioSettings?.minimaxConfigured && audioSettings.s3Configured)}
            generatingLessonSlug={generatingLessonSlug}
            onGenerateAudio={onGenerateAudio}
          />
        ))}
      </div>
    </div>
  );
}

function AudioSettingsPanel({
  settings,
  model,
  voiceId,
  speed,
  preview,
  isPreviewing,
  isLoadingPreviewCache,
  onModelChange,
  onVoiceChange,
  onSpeedChange,
  onPreview
}: {
  settings: AdminAudioSettings | null;
  model: string;
  voiceId: string;
  speed: number;
  preview: AdminVoicePreviewAudio | null;
  isPreviewing: boolean;
  isLoadingPreviewCache: boolean;
  onModelChange: (value: string) => void;
  onVoiceChange: (value: string) => void;
  onSpeedChange: (value: number) => void;
  onPreview: () => void;
}) {
  const configured = Boolean(settings?.minimaxConfigured && settings.s3Configured);
  const voiceOptions = settings?.voices ?? [];
  const modelOptions = settings?.models ?? [];
  const selectedVoice = voiceOptions.find((voice) => voice.voiceId === voiceId);

  return (
    <div className="rounded-lg bg-paper p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-lg bg-white">
            <Volume2 className="h-5 w-5 text-leaf" aria-hidden="true" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase text-leaf">Audio Generator</p>
            <h2 className="mt-1 font-semibold">MiniMax listening audio</h2>
            <p className="mt-1 text-sm text-ink/55">
              Pilih default voice dan model untuk generate audio listening lesson.
            </p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2 text-xs font-semibold">
          <StatusPill
            icon={Sparkles}
            label={settings?.minimaxConfigured ? "MiniMax ready" : "MiniMax missing"}
            tone={settings?.minimaxConfigured ? "ok" : "danger"}
          />
          <StatusPill
            icon={Headphones}
            label={settings?.s3Configured ? "S3 ready" : "S3 missing"}
            tone={settings?.s3Configured ? "ok" : "danger"}
          />
        </div>
      </div>

      <div className="mt-4 grid gap-3 lg:grid-cols-[1fr_1.4fr_140px]">
        <label className="text-sm font-medium text-ink/70">
          Model
          <select
            value={model}
            onChange={(event) => onModelChange(event.target.value)}
            disabled={!settings}
            className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink disabled:cursor-not-allowed disabled:opacity-60"
          >
            {!modelOptions.length ? <option value="">Loading</option> : null}
            {modelOptions.map((modelOption) => (
              <option key={modelOption} value={modelOption}>
                {modelOption}
              </option>
            ))}
          </select>
        </label>

        <label className="text-sm font-medium text-ink/70">
          Voice
          <select
            value={voiceId}
            onChange={(event) => onVoiceChange(event.target.value)}
            disabled={!settings}
            className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink disabled:cursor-not-allowed disabled:opacity-60"
          >
            {!voiceOptions.length ? <option value="">Loading</option> : null}
            {voiceOptions.map((voice) => (
              <option key={voice.voiceId} value={voice.voiceId}>
                {voice.voiceName} / {voice.voiceId}
              </option>
            ))}
          </select>
        </label>

        <label className="text-sm font-medium text-ink/70">
          Speed
          <input
            type="number"
            min={0.5}
            max={2}
            step={0.05}
            value={speed}
            onChange={(event) => onSpeedChange(clampAudioSpeed(Number(event.target.value)))}
            className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
          />
        </label>
      </div>

      <div className="mt-3 grid gap-3 lg:grid-cols-[minmax(0,1fr)_180px]">
        <div className="rounded-lg bg-white p-3 text-sm text-ink/65">
          <p className="font-semibold text-ink">
            {selectedVoice ? selectedVoice.voiceName : "Voice preview"}
          </p>
          <p className="mt-1 text-xs text-ink/50">
            {selectedVoice
              ? `${selectedVoice.voiceId}${selectedVoice.description ? ` / ${selectedVoice.description}` : ""}`
              : "Pilih voice untuk mendengar contoh suara."}
          </p>
          {preview?.audioUrl ? (
            <div className="mt-3">
              <audio controls preload="metadata" src={preview.playbackUrl || preview.audioUrl} className="h-10 w-full" />
              <p className="mt-2 text-xs text-ink/45">
                {preview.cached ? "Cached preview" : "Fresh preview"} / {preview.model} / {preview.voiceId} /{" "}
                {formatDuration(preview.durationSeconds)}
              </p>
            </div>
          ) : isLoadingPreviewCache ? (
            <p className="mt-3 text-xs font-semibold text-ink/45">Loading cached preview...</p>
          ) : null}
        </div>
        <button
          type="button"
          onClick={onPreview}
          disabled={!configured || !model || !voiceId || isPreviewing || isLoadingPreviewCache}
          className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60 lg:mt-auto"
        >
          <PlayCircle className="h-4 w-4" aria-hidden="true" />
          {isPreviewing ? "Preparing" : isLoadingPreviewCache ? "Loading" : "Preview Voice"}
        </button>
      </div>

      {!configured ? (
        <p className="mt-3 rounded-lg bg-white px-3 py-2 text-sm text-ink/60">
          Generate audio aktif setelah <code>MINIMAX_API_KEY</code>, <code>S3_BUCKET</code>,{" "}
          <code>AWS_ACCESS_KEY_ID</code>, <code>AWS_SECRET_ACCESS_KEY</code>, dan{" "}
          <code>AWS_REGION</code> tersedia di API.
        </p>
      ) : null}
    </div>
  );
}

function LevelReadinessCard({
  readiness,
  audioReadyToGenerate,
  generatingLessonSlug,
  onGenerateAudio
}: {
  readiness: AdminContentReadiness;
  audioReadyToGenerate: boolean;
  generatingLessonSlug: string;
  onGenerateAudio: (lesson: AdminContentReadinessLesson) => void;
}) {
  return (
    <div className="rounded-lg border border-ink/10 bg-white p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase text-leaf">
            {readiness.course.language} / {readiness.course.levelCode}
          </p>
          <h2 className="mt-1 text-xl font-semibold">{readiness.course.courseTitle}</h2>
          <p className="mt-1 text-sm text-ink/55">{readiness.course.courseSlug}</p>
        </div>
        <div className="flex flex-wrap gap-2 text-xs font-semibold">
          <StatusPill
            icon={ListChecks}
            label={`${readiness.summary.plannedLessonCount} planned`}
            tone="neutral"
          />
          <StatusPill icon={CheckCircle2} label={`${readiness.summary.textReadyCount} text`} tone="ok" />
          <StatusPill icon={Headphones} label={`${readiness.summary.audioReadyCount} audio`} tone="warn" />
          <StatusPill
            icon={ShieldCheck}
            label={`${readiness.summary.productionReadyCount} prod`}
            tone="neutral"
          />
        </div>
      </div>

      <div className="mt-4 grid gap-4">
        {readiness.units.map((unit) => (
          <div key={unit.unitKey} className="rounded-lg border border-ink/10 bg-white p-4">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase text-leaf">{unit.status}</p>
                <h2 className="mt-1 text-lg font-semibold">{unit.title}</h2>
                <p className="mt-1 text-sm text-ink/55">{unit.unitKey}</p>
              </div>
              <div className="flex flex-wrap gap-2 text-xs font-semibold">
                <StatusPill icon={CheckCircle2} label={`${unit.textReadyCount}/${unit.lessonCount} text`} tone="ok" />
                <StatusPill icon={Headphones} label={`${unit.audioReadyCount}/${unit.lessonCount} audio`} tone="warn" />
                <StatusPill
                  icon={ShieldCheck}
                  label={`${unit.productionReadyCount}/${unit.lessonCount} prod`}
                  tone="neutral"
                />
              </div>
            </div>

            <div className="mt-4 grid gap-3">
              {unit.lessons.map((lesson) => (
                <details key={lesson.lessonKey} className="rounded-lg bg-paper p-4">
                  <summary className="cursor-pointer list-none">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold">{lesson.title}</p>
                        <p className="mt-1 text-xs text-ink/50">
                          {lesson.lessonKey} / {lesson.slug || "slug pending"}
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        <ReadinessPill ready={lesson.textReady} label="Text" />
                        <ReadinessPill ready={lesson.audioReady} label="Audio" />
                        <ReadinessPill ready={lesson.productionReady} label="Production" />
                      </div>
                    </div>
                  </summary>

                  <div className="mt-4 grid gap-3">
                    <div className="flex flex-wrap gap-2">
                      <StatusPill
                        icon={lesson.implemented ? CheckCircle2 : AlertTriangle}
                        label={readinessStatusLabel(lesson.status)}
                        tone={lesson.productionReady ? "ok" : lesson.implemented ? "warn" : "danger"}
                      />
                      {lesson.reviewStatus ? (
                        <StatusPill icon={ShieldCheck} label={`review: ${lesson.reviewStatus}`} tone="neutral" />
                      ) : null}
                      {lesson.publishStatus ? (
                        <StatusPill icon={BookOpen} label={`publish: ${lesson.publishStatus}`} tone="neutral" />
                      ) : null}
                    </div>

                    {lesson.implemented && lesson.textReady ? (
                      <div className="flex flex-wrap items-center gap-2">
                        <button
                          type="button"
                          onClick={() => onGenerateAudio(lesson)}
                          disabled={!audioReadyToGenerate || generatingLessonSlug === lesson.slug}
                          className="focus-ring inline-flex min-h-10 items-center justify-center gap-2 rounded-lg bg-ink px-3 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
                        >
                          <Sparkles className="h-4 w-4" aria-hidden="true" />
                          {generatingLessonSlug === lesson.slug
                            ? "Generating audio"
                            : lesson.audioReady
                              ? "Regenerate Audio"
                              : "Generate Audio"}
                        </button>
                      </div>
                    ) : null}

                    {lesson.audioAsset?.playbackUrl || lesson.audioAsset?.audioUrl ? (
                      <div className="rounded-lg bg-white p-3">
                        <div className="flex flex-wrap items-start justify-between gap-3">
                          <div>
                            <p className="text-sm font-semibold text-ink">Listening audio</p>
                            <p className="mt-1 text-xs text-ink/50">
                              {lesson.audioAsset.model || "model unknown"} /{" "}
                              {lesson.audioAsset.lineCount > 1
                                ? `${lesson.audioAsset.lineCount} dialogue lines`
                                : lesson.audioAsset.voiceId || "voice unknown"}{" "}
                              /{" "}
                              {formatDuration(lesson.audioAsset.durationSeconds)}
                            </p>
                          </div>
                          <a
                            href={lesson.audioAsset.playbackUrl || lesson.audioAsset.audioUrl}
                            target="_blank"
                            rel="noreferrer"
                            className="focus-ring inline-flex min-h-8 items-center justify-center gap-1 rounded-lg bg-paper px-2 text-xs font-semibold text-ink hover:bg-mint"
                          >
                            <ExternalLink className="h-3.5 w-3.5" aria-hidden="true" />
                            Open
                          </a>
                        </div>
                        <audio
                          controls
                          preload="metadata"
                          src={lesson.audioAsset.playbackUrl || lesson.audioAsset.audioUrl}
                          className="mt-3 h-10 w-full"
                        />
                        {Object.keys(lesson.audioAsset.speakerVoices).length ? (
                          <p className="mt-2 text-xs text-ink/50">
                            {Object.entries(lesson.audioAsset.speakerVoices)
                              .map(([speaker, voice]) => `${speaker}: ${voice}`)
                              .join(" / ")}
                          </p>
                        ) : null}
                        <p className="mt-2 break-all text-xs text-ink/45">{lesson.audioAsset.storageKey}</p>
                      </div>
                    ) : null}

                    {lesson.missingItems.length ? (
                      <div className="rounded-lg bg-white p-3 text-sm text-ink/65">
                        <p className="font-semibold text-ink">Missing</p>
                        <p className="mt-1">{lesson.missingItems.join(", ")}</p>
                      </div>
                    ) : null}

                    <div className="grid gap-2 md:grid-cols-2">
                      {lesson.checks.map((check) => (
                        <div key={check.key} className="flex items-start gap-2 rounded-lg bg-white p-3 text-sm">
                          {check.ready ? (
                            <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-leaf" aria-hidden="true" />
                          ) : (
                            <XCircle className="mt-0.5 h-4 w-4 shrink-0 text-coral" aria-hidden="true" />
                          )}
                          <div>
                            <p className="font-semibold">{check.label}</p>
                            <p className="mt-0.5 text-xs text-ink/50">
                              {check.filename}
                              {check.trackerColumn ? ` / tracker: ${check.trackerValue || "missing"}` : ""}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </details>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function CurriculumEditor({
  updatedBy,
  lessons,
  selectedLesson,
  onSelectLesson,
  onSaved,
  onError
}: {
  updatedBy: string;
  lessons: AdminCmsLesson[];
  selectedLesson: AdminCmsLesson | null;
  onSelectLesson: (slug: string) => void;
  onSaved: (lesson: AdminCmsLesson) => void;
  onError: (message: string) => void;
}) {
  const [draft, setDraft] = useState<AdminCmsLesson | null>(selectedLesson);
  const [targetPhrasesText, setTargetPhrasesText] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    setDraft(selectedLesson);
    setTargetPhrasesText(selectedLesson?.roleplay.targetPhrases.join("\n") ?? "");
  }, [selectedLesson]);

  async function saveLesson() {
    if (!draft) {
      return;
    }

    setIsSaving(true);
    onError("");

    try {
      const saved = await updateAdminCmsLesson({
        updatedBy,
        lessonSlug: draft.slug,
        title: draft.title,
        status: draft.status,
        estimatedMinutes: draft.estimatedMinutes,
        conversationGoal: draft.conversationGoal,
        roleplayOpeningLine: draft.roleplay.openingLine,
        roleplayLearnerGoal: draft.roleplay.learnerGoal,
        roleplayMaxTurns: draft.roleplay.maxTurns,
        roleplayTargetPhrases: targetPhrasesText.split("\n").map((item) => item.trim()).filter(Boolean),
        expectedContentHash: draft.contentHash
      });
      onSaved(saved);
    } catch (error) {
      onError(contentSaveErrorMessage(error, "Lesson"));
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="mt-5 grid gap-5 xl:grid-cols-[0.34fr_0.66fr]">
      <div className="space-y-2">
        {lessons.map((lesson) => (
          <button
            key={lesson.slug}
            type="button"
            onClick={() => onSelectLesson(lesson.slug)}
            className={`focus-ring w-full rounded-lg p-4 text-left ${
              selectedLesson?.slug === lesson.slug ? "bg-mint" : "bg-paper hover:bg-mint"
            }`}
          >
            <p className="text-xs font-semibold uppercase text-leaf">{lesson.status}</p>
            <p className="mt-2 font-semibold">{lesson.title}</p>
            <p className="mt-1 text-xs text-ink/50">{lesson.slug}</p>
          </button>
        ))}
        {!lessons.length ? <p className="rounded-lg bg-paper p-4 text-sm text-ink/60">Load CMS dulu.</p> : null}
      </div>

      {draft ? (
        <div className="grid gap-4">
          <div className="grid gap-3 md:grid-cols-[1fr_160px]">
            <TextInput
              label="Lesson title"
              value={draft.title}
              onChange={(value) => setDraft({ ...draft, title: value })}
            />
            <label className="text-sm font-medium text-ink/70">
              Status
              <select
                value={draft.status}
                onChange={(event) => setDraft({ ...draft, status: event.target.value })}
                className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
              >
                {statusOptions.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <label className="text-sm font-medium text-ink/70">
            Conversation goal
            <textarea
              value={draft.conversationGoal}
              onChange={(event) => setDraft({ ...draft, conversationGoal: event.target.value })}
              rows={3}
              className="focus-ring mt-2 w-full resize-none rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
            />
          </label>

          <div className="grid gap-3 md:grid-cols-[1fr_120px]">
            <TextInput
              label="Roleplay opening"
              value={draft.roleplay.openingLine}
              onChange={(value) =>
                setDraft({ ...draft, roleplay: { ...draft.roleplay, openingLine: value } })
              }
            />
            <NumberInput
              label="Max turns"
              value={draft.roleplay.maxTurns}
              onChange={(value) => setDraft({ ...draft, roleplay: { ...draft.roleplay, maxTurns: value } })}
            />
          </div>

          <label className="text-sm font-medium text-ink/70">
            Learner goal
            <textarea
              value={draft.roleplay.learnerGoal}
              onChange={(event) =>
                setDraft({ ...draft, roleplay: { ...draft.roleplay, learnerGoal: event.target.value } })
              }
              rows={3}
              className="focus-ring mt-2 w-full resize-none rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
            />
          </label>

          <label className="text-sm font-medium text-ink/70">
            Target phrases, one per line
            <textarea
              value={targetPhrasesText}
              onChange={(event) => setTargetPhrasesText(event.target.value)}
              rows={5}
              className="focus-ring mt-2 w-full resize-none rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
            />
          </label>

          <button
            type="button"
            onClick={saveLesson}
            disabled={isSaving}
            className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Save className="h-4 w-4" aria-hidden="true" />
            {isSaving ? "Saving" : "Save Lesson"}
          </button>
        </div>
      ) : (
        <p className="rounded-lg bg-paper p-5 text-sm text-ink/60">Pilih lesson untuk diedit.</p>
      )}
    </div>
  );
}

function EmailTemplateEditor({
  updatedBy,
  templates,
  selectedTemplate,
  onSelectTemplate,
  onSaved,
  onError
}: {
  updatedBy: string;
  templates: AdminEmailTemplate[];
  selectedTemplate: AdminEmailTemplate | null;
  onSelectTemplate: (templateKey: string) => void;
  onSaved: (template: AdminEmailTemplate) => void;
  onError: (message: string) => void;
}) {
  const [rawBody, setRawBody] = useState(selectedTemplate?.rawBody ?? "");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    setRawBody(selectedTemplate?.rawBody ?? "");
  }, [selectedTemplate]);

  const preview = useMemo(() => selectedTemplate, [selectedTemplate]);

  async function saveTemplate() {
    if (!selectedTemplate) {
      return;
    }

    setIsSaving(true);
    onError("");

    try {
      const saved = await updateAdminEmailTemplate({
        updatedBy,
        templateKey: selectedTemplate.templateKey,
        rawBody,
        expectedContentHash: selectedTemplate.contentHash
      });
      onSaved(saved);
    } catch (error) {
      onError(contentSaveErrorMessage(error, "Email template"));
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="mt-5 grid gap-5 xl:grid-cols-[0.34fr_0.66fr]">
      <div className="space-y-2">
        {templates.map((template) => (
          <button
            key={template.templateKey}
            type="button"
            onClick={() => onSelectTemplate(template.templateKey)}
            className={`focus-ring w-full rounded-lg p-4 text-left ${
              selectedTemplate?.templateKey === template.templateKey ? "bg-mint" : "bg-paper hover:bg-mint"
            }`}
          >
            <p className="font-semibold">{template.templateKey}</p>
            <p className="mt-2 text-sm text-ink/60">{template.subject}</p>
          </button>
        ))}
        {!templates.length ? <p className="rounded-lg bg-paper p-4 text-sm text-ink/60">Load CMS dulu.</p> : null}
      </div>

      {selectedTemplate ? (
        <div className="grid gap-4">
          {preview ? (
            <div className="grid gap-3 rounded-lg bg-paper p-4 text-sm">
              <p><span className="font-semibold">Subject:</span> {preview.subject}</p>
              <p><span className="font-semibold">Preheader:</span> {preview.preheader}</p>
              <p><span className="font-semibold">CTA:</span> {preview.ctaLabel}</p>
            </div>
          ) : null}
          <label className="text-sm font-medium text-ink/70">
            Markdown template
            <textarea
              value={rawBody}
              onChange={(event) => setRawBody(event.target.value)}
              rows={18}
              className="focus-ring mt-2 w-full resize-y rounded-lg border border-ink/15 bg-white px-3 py-3 font-mono text-sm leading-6 text-ink"
            />
          </label>
          <button
            type="button"
            onClick={saveTemplate}
            disabled={isSaving}
            className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Save className="h-4 w-4" aria-hidden="true" />
            {isSaving ? "Saving" : "Save Template"}
          </button>
        </div>
      ) : (
        <p className="rounded-lg bg-paper p-5 text-sm text-ink/60">Pilih email template untuk diedit.</p>
      )}
    </div>
  );
}

function TabButton({
  active,
  icon: Icon,
  onClick,
  children
}: {
  active: boolean;
  icon: LucideIcon;
  onClick: () => void;
  children: ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`focus-ring inline-flex min-h-10 items-center justify-center gap-2 rounded-lg px-4 text-sm font-semibold ${
        active ? "bg-ink text-white" : "bg-paper text-ink/70 hover:bg-mint"
      }`}
    >
      <Icon className="h-4 w-4" aria-hidden="true" />
      {children}
    </button>
  );
}

function TextInput({
  label,
  value,
  onChange
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="text-sm font-medium text-ink/70">
      {label}
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
      />
    </label>
  );
}

function NumberInput({
  label,
  value,
  onChange
}: {
  label: string;
  value: number;
  onChange: (value: number) => void;
}) {
  return (
    <label className="text-sm font-medium text-ink/70">
      {label}
      <input
        type="number"
        min={1}
        max={20}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
      />
    </label>
  );
}

function ReadinessPill({ ready, label }: { ready: boolean; label: string }) {
  return (
    <span
      className={`inline-flex min-h-8 items-center gap-1.5 rounded-lg px-2.5 text-xs font-semibold ${
        ready ? "bg-mint text-leaf" : "bg-[#fde7df] text-coral"
      }`}
    >
      {ready ? <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" /> : <XCircle className="h-3.5 w-3.5" aria-hidden="true" />}
      {label}
    </span>
  );
}

function StatusPill({
  icon: Icon,
  label,
  tone
}: {
  icon: LucideIcon;
  label: string;
  tone: "ok" | "warn" | "danger" | "neutral";
}) {
  const className =
    tone === "ok"
      ? "bg-mint text-leaf"
      : tone === "warn"
        ? "bg-[#fff4d5] text-[#7a5600]"
        : tone === "danger"
          ? "bg-[#fde7df] text-coral"
          : "bg-paper text-ink/60";

  return (
    <span className={`inline-flex min-h-8 items-center gap-1.5 rounded-lg px-2.5 ${className}`}>
      <Icon className="h-3.5 w-3.5" aria-hidden="true" />
      {label}
    </span>
  );
}

function readinessStatusLabel(status: string) {
  const labels: Record<string, string> = {
    production_ready: "production ready",
    beta_ready_needs_audio: "beta ready, needs audio",
    implemented_needs_content: "needs content",
    planned_missing_content: "planned"
  };
  return labels[status] ?? status;
}

function formatDuration(durationSeconds: number) {
  if (!Number.isFinite(durationSeconds) || durationSeconds <= 0) {
    return "0s";
  }
  if (durationSeconds < 60) {
    return `${Math.round(durationSeconds)}s`;
  }
  const minutes = Math.floor(durationSeconds / 60);
  const seconds = Math.round(durationSeconds % 60);
  return `${minutes}m ${seconds}s`;
}

function storedAudioModel(fallback: string) {
  return window.localStorage.getItem(audioModelStorageKey) || fallback;
}

function storedAudioVoice(fallback: string) {
  return window.localStorage.getItem(audioVoiceStorageKey) || fallback;
}

function storedAudioSpeed() {
  const rawValue = window.localStorage.getItem(audioSpeedStorageKey);
  const value = rawValue ? Number(rawValue) : 1;
  if (!Number.isFinite(value) || value < 0.5 || value > 2) {
    return 1;
  }
  return value;
}

function clampAudioSpeed(value: number) {
  if (!Number.isFinite(value)) {
    return 1;
  }
  return Math.min(2, Math.max(0.5, value));
}

function audioGenerationErrorMessage(error: unknown) {
  const message = error instanceof Error ? error.message : "";
  if (message.includes("minimax_api_key_missing")) {
    return "Generate audio belum bisa berjalan karena MINIMAX_API_KEY belum terbaca di API.";
  }
  if (message.includes("s3_config_missing")) {
    return "Generate audio belum bisa upload karena konfigurasi S3 belum lengkap.";
  }
  if (message.includes("boto3_missing")) {
    return "Generate audio belum bisa upload karena dependency boto3 belum terinstall di venv API.";
  }
  if (message.includes("invalid_minimax_tts_model")) {
    return "Model MiniMax belum valid. Pilih model dari daftar.";
  }
  if (message.includes("lesson_not_found")) {
    return "Lesson belum ditemukan di content files.";
  }
  if (message.includes("listening_script")) {
    return "Listening script belum siap untuk generate audio.";
  }
  if (message.includes("minimax_request_failed") || message.includes("minimax_error")) {
    return "MiniMax belum berhasil membuat audio. Cek API key, quota, voice, atau coba ulang.";
  }
  return "Audio belum bisa digenerate. Cek konfigurasi MiniMax, S3, dan content lesson.";
}

function contentSaveErrorMessage(error: unknown, label: string) {
  const message = error instanceof Error ? error.message : "";
  if (message.includes("content_changed_reload_required")) {
    return `${label} sudah berubah sejak terakhir diload. Reload CMS dulu sebelum menyimpan.`;
  }
  if (label === "Email template") {
    return "Email template belum bisa disimpan. Pastikan heading, Subject, Preheader, CTA, html, dan txt lengkap.";
  }
  return "Lesson belum bisa disimpan. Cek field dan validasi YAML.";
}
