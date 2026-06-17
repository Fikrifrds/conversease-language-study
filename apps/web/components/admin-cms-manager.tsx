"use client";

import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  BookOpen,
  ChevronDown,
  CheckCircle2,
  ClipboardList,
  Clock3,
  ExternalLink,
  FileText,
  Headphones,
  History,
  ListChecks,
  Mail,
  RefreshCcw,
  Search,
  ShieldCheck,
  Sparkles,
  Volume2,
  XCircle,
  type LucideIcon
} from "lucide-react";
import type { AuthUser } from "@/lib/auth-api";
import {
  generateAdminLessonAudio,
  generateAdminExamItemAudio,
  generateAdminExamTemplateAudio,
  getAdminAudioSettings,
  getAdminCmsLesson,
  getAdminCmsOverview,
  getAdminCmsReadiness,
  getAdminEmailTemplate,
  listAdminExamAudioTemplates,
  listAdminCmsLessons,
  listAdminCmsRevisions,
  listAdminEmailTemplates,
  getAdminVoicePreviews,
  rollbackAdminCmsRevision,
  type AdminAudioVoice,
  type AdminExamAudioTemplate,
  type AdminExamListeningItem,
  type AdminContentReadiness,
  type AdminContentReadinessLesson,
  type AdminContentReadinessOverview,
  type AdminContentRevision,
  type AdminAudioSettings,
  type AdminCmsLesson,
  type AdminCmsOverview,
  type AdminCmsLanguageOption,
  type AdminEmailTemplate,
  type AdminVoicePreviewAudio
} from "@/lib/admin-cms-api";
import { ChangeLogPanel, CurriculumEditor, EmailTemplateEditor } from "./admin-cms/editors";
import { LanguageFilterControl, SectionNavButton } from "./admin-cms/navigation";
import type { BulkAudioQueueItem, BulkAudioQueueStatus, LanguageFilter, Tab } from "./admin-cms/types";
import {
  audioGenerationErrorMessage,
  clampAudioSpeed,
  formatDuration
} from "./admin-cms/utils";

const adminNameStorageKey = "conversease.admin_name";
const audioProviderStorageKey = "conversease.admin_audio_provider";
const audioModelStorageKey = "conversease.admin_audio_model";
const audioVoiceStorageKey = "conversease.admin_audio_voice";
const audioSpeedStorageKey = "conversease.admin_audio_speed";
const bulkAudioMaxAttempts = 2;

export function AdminCmsManager({ adminUser }: { adminUser: AuthUser }) {
  const [adminName, setAdminName] = useState(adminUser.name || adminUser.email);
  const [overview, setOverview] = useState<AdminCmsOverview | null>(null);
  const [readinessOverview, setReadinessOverview] = useState<AdminContentReadinessOverview | null>(null);
  const [readinessLevels, setReadinessLevels] = useState<AdminContentReadiness[]>([]);
  const [cmsLessons, setCmsLessons] = useState<AdminCmsLesson[]>([]);
  const [emailTemplates, setEmailTemplates] = useState<AdminEmailTemplate[]>([]);
  const [recentRevisions, setRecentRevisions] = useState<AdminContentRevision[]>([]);
  const [tab, setTab] = useState<Tab>("readiness");
  const [languageFilter, setLanguageFilter] = useState<LanguageFilter>("english");
  const [selectedLesson, setSelectedLesson] = useState<AdminCmsLesson | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<AdminEmailTemplate | null>(null);
  const [audioSettings, setAudioSettings] = useState<AdminAudioSettings | null>(null);
  const [audioProvider, setAudioProvider] = useState("minimax");
  const [audioModel, setAudioModel] = useState("");
  const [audioVoiceId, setAudioVoiceId] = useState("");
  const [audioSpeed, setAudioSpeed] = useState(1);
  const [voicePreviewsByVoiceId, setVoicePreviewsByVoiceId] = useState<Record<string, AdminVoicePreviewAudio>>({});
  const [examAudioTemplates, setExamAudioTemplates] = useState<AdminExamAudioTemplate[]>([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingReadiness, setIsLoadingReadiness] = useState(false);
  const [isLoadingLessons, setIsLoadingLessons] = useState(false);
  const [isLoadingEmailTemplates, setIsLoadingEmailTemplates] = useState(false);
  const [isLoadingRevisions, setIsLoadingRevisions] = useState(false);
  const [restoringRevisionId, setRestoringRevisionId] = useState("");
  const [generatingLessonSlug, setGeneratingLessonSlug] = useState("");
  const [generatingExamTemplateId, setGeneratingExamTemplateId] = useState("");
  const [generatingExamItemId, setGeneratingExamItemId] = useState("");
  const [isLoadingAudioSettings, setIsLoadingAudioSettings] = useState(false);
  const [isLoadingVoicePreviews, setIsLoadingVoicePreviews] = useState(false);
  const [isLoadingExamTemplates, setIsLoadingExamTemplates] = useState(false);
  const [hasLoadedExamTemplates, setHasLoadedExamTemplates] = useState(false);
  const [hasLoadedEmailTemplates, setHasLoadedEmailTemplates] = useState(false);
  const [hasLoadedRevisions, setHasLoadedRevisions] = useState(false);
  const [bulkAudioQueue, setBulkAudioQueue] = useState<BulkAudioQueueItem[]>([]);
  const [isBulkGeneratingAudio, setIsBulkGeneratingAudio] = useState(false);
  const audioLanguageContext: LanguageFilter | "all" = tab === "examAudio" ? "all" : languageFilter;

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
    if (audioProvider) {
      window.localStorage.setItem(audioProviderStorageKey, audioProvider);
    }
  }, [audioProvider]);

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
    if (!audioProvider || !audioModel) {
      setVoicePreviewsByVoiceId({});
      return;
    }

    let cancelled = false;
    setIsLoadingVoicePreviews(true);
    void getAdminVoicePreviews({
      provider: audioProvider,
      model: audioModel,
      speed: audioSpeed,
      sampleText: audioPreviewSampleText(audioLanguageContext)
    })
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
  }, [audioProvider, audioModel, audioSpeed, audioLanguageContext]);

  useEffect(() => {
    if (!audioSettings) {
      return;
    }

    const nextProvider = defaultAudioProviderForLanguage(audioSettings, audioLanguageContext, audioProvider);
    if (nextProvider !== audioProvider) {
      setAudioProvider(nextProvider);
    }
    setAudioModel((current) =>
      audioModelMatchesProvider(current, nextProvider, audioSettings)
        ? current
        : defaultAudioModelForProvider(audioSettings, nextProvider)
    );
    setAudioVoiceId((current) =>
      audioVoiceMatchesLanguage(current, audioLanguageContext, audioSettings.voices, nextProvider)
        ? current
        : defaultAudioVoiceIdForLanguage(audioSettings, audioLanguageContext, nextProvider)
    );
    setAudioSpeed((current) => defaultAudioSpeedForLanguage(audioLanguageContext, current));
  }, [audioSettings, audioLanguageContext, audioProvider]);

  useEffect(() => {
    void loadOverview();
    // Load lightweight overview once when this admin screen opens.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (tab === "readiness" || tab === "lessonAudio") {
      void loadReadiness(languageFilter);
    }
    if (tab === "curriculum") {
      void loadLessons(languageFilter);
    }
    if (tab === "email") {
      void loadEmailTemplates();
    }
    if (tab === "changelog") {
      void loadRevisions();
    }
    if (tab === "lessonAudio" || tab === "examAudio") {
      void loadAudioSettings();
    }
    if (tab === "examAudio") {
      void loadExamAudioTemplates();
    }
    // Section data is loaded lazily to keep the first CMS screen lighter.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab, languageFilter]);

  const validationOk = (overview?.validationIssues.length ?? 1) === 0;
  const languageOptions = overview?.languages ?? [];

  async function loadOverview() {
    setIsLoading(true);
    setMessage("");
    setError("");

    try {
      const nextOverview = await getAdminCmsOverview();
      setOverview(nextOverview);
      if (!nextOverview.languages.some((language) => language.language === languageFilter)) {
        setLanguageFilter(nextOverview.languages[0]?.language ?? "english");
      }
      setMessage("CMS overview berhasil dimuat.");
    } catch {
      setError("CMS belum bisa dimuat. Pastikan akunmu punya role admin atau cek koneksi API.");
    } finally {
      setIsLoading(false);
    }
  }

  async function reloadActiveSection() {
    await loadOverview();
    if (tab === "readiness" || tab === "lessonAudio") {
      await loadReadiness(languageFilter);
    } else if (tab === "curriculum") {
      await loadLessons(languageFilter);
    } else if (tab === "email") {
      await loadEmailTemplates({ force: true });
    } else if (tab === "changelog") {
      await loadRevisions({ force: true });
    }
  }

  async function loadReadiness(language: LanguageFilter) {
    setIsLoadingReadiness(true);
    setError("");
    try {
      const payload = await getAdminCmsReadiness({ language });
      setReadinessOverview(payload.readinessOverview);
      setReadinessLevels(payload.readinessLevels);
    } catch {
      setError("Readiness belum bisa dimuat untuk bahasa ini.");
    } finally {
      setIsLoadingReadiness(false);
    }
  }

  async function loadLessons(language: LanguageFilter) {
    setIsLoadingLessons(true);
    setError("");
    try {
      const payload = await listAdminCmsLessons({ language });
      setCmsLessons(payload.lessons);
      setSelectedLesson((current) => {
        if (current && payload.lessons.some((lesson) => lesson.slug === current.slug)) {
          return current;
        }
        return payload.lessons[0] ?? null;
      });
    } catch {
      setError("Curriculum lesson belum bisa dimuat untuk bahasa ini.");
    } finally {
      setIsLoadingLessons(false);
    }
  }

  async function loadEmailTemplates(options?: { force?: boolean }) {
    if (!options?.force && (hasLoadedEmailTemplates || isLoadingEmailTemplates)) {
      return;
    }

    setIsLoadingEmailTemplates(true);
    setError("");
    try {
      const templates = await listAdminEmailTemplates();
      setEmailTemplates(templates);
      setSelectedTemplate((current) => {
        if (current && templates.some((template) => template.templateKey === current.templateKey)) {
          return current;
        }
        return templates[0] ?? null;
      });
      setHasLoadedEmailTemplates(true);
    } catch {
      setError("Email templates belum bisa dimuat.");
    } finally {
      setIsLoadingEmailTemplates(false);
    }
  }

  async function loadRevisions(options?: { force?: boolean }) {
    if (!options?.force && (hasLoadedRevisions || isLoadingRevisions)) {
      return;
    }

    setIsLoadingRevisions(true);
    setError("");
    try {
      setRecentRevisions(await listAdminCmsRevisions({ limit: 50 }));
      setHasLoadedRevisions(true);
    } catch {
      setError("Change log belum bisa dimuat.");
    } finally {
      setIsLoadingRevisions(false);
    }
  }

  async function loadAudioSettings() {
    if (audioSettings || isLoadingAudioSettings) {
      return;
    }

    setIsLoadingAudioSettings(true);
    try {
      const nextAudioSettings = await getAdminAudioSettings();
      const nextProvider = defaultAudioProviderForLanguage(
        nextAudioSettings,
        audioLanguageContext,
        storedAudioProvider(nextAudioSettings.defaultProvider)
      );
      setAudioSettings(nextAudioSettings);
      setAudioProvider(nextProvider);
      setAudioModel((current) =>
        audioModelMatchesProvider(current, nextProvider, nextAudioSettings)
          ? current
          : storedAudioModel(defaultAudioModelForProvider(nextAudioSettings, nextProvider), nextProvider)
      );
      setAudioVoiceId((current) => {
        const storedVoice = current || storedAudioVoice(defaultAudioVoiceIdForLanguage(nextAudioSettings, audioLanguageContext, nextProvider));
        return audioVoiceMatchesLanguage(storedVoice, audioLanguageContext, nextAudioSettings.voices, nextProvider)
          ? storedVoice
          : defaultAudioVoiceIdForLanguage(nextAudioSettings, audioLanguageContext, nextProvider);
      });
      setAudioSpeed((current) => (current === 1 ? storedAudioSpeed() : current));
    } catch {
      setError("Audio settings belum bisa dimuat.");
    } finally {
      setIsLoadingAudioSettings(false);
    }
  }

  async function loadExamAudioTemplates() {
    if (hasLoadedExamTemplates || isLoadingExamTemplates) {
      return;
    }
    await reloadExamAudioTemplates();
  }

  async function reloadExamAudioTemplates() {
    setIsLoadingExamTemplates(true);
    try {
      setExamAudioTemplates(await listAdminExamAudioTemplates());
      setHasLoadedExamTemplates(true);
    } finally {
      setIsLoadingExamTemplates(false);
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
        provider: audioProvider,
        model: audioModel,
        voiceId: audioVoiceId,
        speed: audioSpeed
      });
      await loadReadiness(languageFilter);
      setMessage(`Audio ${audio.title} berhasil dibuat (${formatDuration(audio.durationSeconds)}).`);
    } catch (caughtError) {
      setError(audioGenerationErrorMessage(caughtError));
    } finally {
      setGeneratingLessonSlug("");
    }
  }

  async function generateBulkLessonAudio(lessons: BulkAudioQueueItem[]) {
    if (!audioModel || !audioVoiceId) {
      setError("Pilih model dan voice sebelum bulk generate audio.");
      return;
    }
    if (!lessons.length) {
      setMessage("Tidak ada lesson yang perlu digenerate.");
      return;
    }

    setBulkAudioQueue(lessons);
    setIsBulkGeneratingAudio(true);
    setGeneratingLessonSlug("");
    setMessage(`Bulk audio dimulai untuk ${lessons.length} lesson.`);
    setError("");

    let successCount = 0;
    let failedCount = 0;

    try {
      for (const lesson of lessons) {
        updateBulkAudioItem(lesson.lessonSlug, { status: "running", attempts: 1, error: "" });

        let generated = false;
        let lastError = "";
        for (let attempt = 1; attempt <= bulkAudioMaxAttempts; attempt += 1) {
          updateBulkAudioItem(lesson.lessonSlug, { status: "running", attempts: attempt, error: "" });
          try {
            const audio = await generateAdminLessonAudio({
              generatedBy: adminName,
              lessonSlug: lesson.lessonSlug,
              provider: audioProvider,
              model: audioModel,
              voiceId: audioVoiceId,
              speed: audioSpeed
            });
            updateBulkAudioItem(lesson.lessonSlug, {
              status: "done",
              attempts: attempt,
              durationSeconds: audio.durationSeconds,
              error: ""
            });
            successCount += 1;
            generated = true;
            break;
          } catch (caughtError) {
            lastError = audioGenerationErrorMessage(caughtError);
            updateBulkAudioItem(lesson.lessonSlug, {
              status: attempt < bulkAudioMaxAttempts ? "pending" : "failed",
              attempts: attempt,
              error: lastError
            });
          }
        }

        if (!generated) {
          failedCount += 1;
        }
      }

      await loadReadiness(languageFilter);
      setMessage(`Bulk audio selesai: ${successCount} berhasil, ${failedCount} gagal.`);
      if (failedCount) {
        setError("Sebagian audio gagal dibuat. Cek queue status lalu jalankan ulang untuk item yang gagal.");
      }
    } finally {
      setIsBulkGeneratingAudio(false);
      setGeneratingLessonSlug("");
    }
  }

  function updateBulkAudioItem(lessonSlug: string, patch: Partial<BulkAudioQueueItem>) {
    setBulkAudioQueue((current) =>
      current.map((item) => (item.lessonSlug === lessonSlug ? { ...item, ...patch } : item))
    );
  }

  async function selectLesson(slug: string) {
    setError("");
    try {
      setSelectedLesson(await getAdminCmsLesson(slug));
    } catch {
      setError("Lesson belum bisa dimuat.");
    }
  }

  async function generateExamTemplateAudio(template: AdminExamAudioTemplate, onlyMissing: boolean) {
    if (!audioModel || !audioVoiceId) {
      setError("Pilih model dan voice sebelum generate audio exam.");
      return;
    }
    setGeneratingExamTemplateId(template.id);
    setMessage("");
    setError("");
    try {
      const result = await generateAdminExamTemplateAudio({
        generatedBy: adminName,
        templateId: template.id,
        provider: audioProvider,
        model: audioModel,
        voiceId: audioVoiceId,
        speed: audioSpeed,
        onlyMissing
      });
      await reloadExamAudioTemplates();
      setMessage(
        `${result.generatedCount} audio exam (listening & speaking) untuk ${template.title} berhasil ${onlyMissing ? "di-update" : "diregenerate"}.`
      );
    } catch (caughtError) {
      setError(audioGenerationErrorMessage(caughtError));
    } finally {
      setGeneratingExamTemplateId("");
    }
  }

  async function generateExamItemAudio(templateId: string, item: AdminExamListeningItem) {
    if (!audioModel || !audioVoiceId) {
      setError("Pilih model dan voice sebelum generate audio exam.");
      return;
    }
    setGeneratingExamItemId(item.id);
    setMessage("");
    setError("");
    try {
      const generated = await generateAdminExamItemAudio({
        generatedBy: adminName,
        itemId: item.id,
        provider: audioProvider,
        model: audioModel,
        voiceId: audioVoiceId,
        speed: audioSpeed
      });
      setExamAudioTemplates((current) =>
        current.map((template) =>
          template.id !== templateId
            ? template
            : {
                ...template,
                listeningAudioReadyCount: template.listeningItems.some((entry) => entry.id === generated.id)
                  ? template.listeningItems.reduce(
                      (count, entry) =>
                        count + (entry.id === generated.id ? 1 : entry.audioReady ? 1 : 0),
                      0
                    )
                  : template.listeningAudioReadyCount,
                listeningItems: template.listeningItems.map((entry) => (entry.id === generated.id ? generated : entry))
              }
        )
      );
      await reloadExamAudioTemplates();
      setMessage(`Audio untuk item exam #${item.sequenceOrder} berhasil dibuat.`);
    } catch (caughtError) {
      setError(audioGenerationErrorMessage(caughtError));
    } finally {
      setGeneratingExamItemId("");
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
      await loadRevisions({ force: true });

      if (result.resourceType === "curriculum_lesson") {
        setTab("curriculum");
        setSelectedLesson(result.data);
        await loadLessons(languageFilter);
      } else {
        setTab("email");
        setSelectedTemplate(result.data);
        await loadEmailTemplates({ force: true });
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
              <h1 className="mt-1 text-2xl font-semibold">Kontrol Konten</h1>
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
              onClick={reloadActiveSection}
              disabled={isLoading}
              className="focus-ring mt-auto inline-flex h-11 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
            >
              <RefreshCcw className="h-4 w-4" aria-hidden="true" />
              {isLoading ? "Memuat" : "Muat Ulang"}
            </button>
          </div>
        </div>

        <div className="mt-5 grid gap-3 lg:grid-cols-[1fr_1fr_1fr]">
          <div className="rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">
            Login sebagai <span className="font-semibold text-ink">{adminUser.email}</span>
          </div>

          {overview ? (
            validationOk ? (
              <div className="flex items-center gap-2 rounded-lg bg-mint px-4 py-3 text-sm font-semibold text-ink/70">
                <ShieldCheck className="h-4 w-4 text-leaf" aria-hidden="true" />
                Validasi kurikulum lolos.
              </div>
            ) : (
              <div className="rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">
                {overview.validationIssues.map((issue) => (
                  <p key={issue}>{issue}</p>
                ))}
              </div>
            )
          ) : (
            <div className="rounded-lg bg-paper px-4 py-3 text-sm text-ink/60">
              Muat overview untuk melihat status validasi content.
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
        <div className="grid gap-5 lg:grid-cols-[240px_minmax(0,1fr)]">
          <nav className="flex gap-2 overflow-x-auto pb-1 lg:block lg:space-y-2 lg:overflow-visible lg:pb-0">
            <SectionNavButton
              active={tab === "readiness"}
              icon={ListChecks}
              label="Readiness"
              description="Status konten per bahasa"
              onClick={() => setTab("readiness")}
            />
            <SectionNavButton
              active={tab === "curriculum"}
              icon={BookOpen}
              label="Curriculum"
              description="Edit metadata lesson"
              onClick={() => setTab("curriculum")}
            />
            <SectionNavButton
              active={tab === "lessonAudio"}
              icon={Headphones}
              label="Lesson Audio"
              description="Generate audio lesson"
              onClick={() => setTab("lessonAudio")}
            />
            <SectionNavButton
              active={tab === "examAudio"}
              icon={ClipboardList}
              label="Exam Audio"
              description="Audio untuk exam"
              onClick={() => setTab("examAudio")}
            />
            <SectionNavButton
              active={tab === "email"}
              icon={Mail}
              label="Email"
              description="Template email"
              onClick={() => setTab("email")}
            />
            <SectionNavButton
              active={tab === "changelog"}
              icon={History}
              label="Change Log"
              description="Revision dan rollback"
              onClick={() => setTab("changelog")}
            />
          </nav>

          <div className="min-w-0">
            {tab === "readiness" ? (
              <ReadinessPanel
                overview={readinessOverview}
                levels={readinessLevels}
                languages={languageOptions}
                languageFilter={languageFilter}
                isLoading={isLoadingReadiness}
                onLanguageFilterChange={setLanguageFilter}
              />
            ) : tab === "curriculum" ? (
              <CurriculumEditor
                updatedBy={adminName}
                lessons={cmsLessons}
                isLoading={isLoadingLessons}
                selectedLesson={selectedLesson}
                onSelectLesson={selectLesson}
                onSaved={(lesson) => {
                  setSelectedLesson(lesson);
                  setMessage("Lesson tersimpan dan curriculum cache sudah diperbarui.");
                  void loadLessons(languageFilter);
                  void loadReadiness(languageFilter);
                }}
                onError={setError}
              />
            ) : tab === "lessonAudio" ? (
              <LessonAudioPanel
                levels={readinessLevels}
                languages={languageOptions}
                languageFilter={languageFilter}
                isLoading={isLoadingReadiness}
                onLanguageFilterChange={setLanguageFilter}
                audioSettings={audioSettings}
                audioProvider={audioProvider}
                audioModel={audioModel}
                audioVoiceId={audioVoiceId}
                audioSpeed={audioSpeed}
                voicePreview={voicePreviewsByVoiceId[audioVoiceId] ?? null}
                voicePreviewsByVoiceId={voicePreviewsByVoiceId}
                generatingLessonSlug={generatingLessonSlug}
                bulkAudioQueue={bulkAudioQueue}
                isBulkGeneratingAudio={isBulkGeneratingAudio}
                isLoadingAudioSettings={isLoadingAudioSettings}
                isLoadingVoicePreviews={isLoadingVoicePreviews}
                onAudioProviderChange={setAudioProvider}
                onAudioModelChange={setAudioModel}
                onAudioVoiceChange={setAudioVoiceId}
                onAudioSpeedChange={setAudioSpeed}
                onGenerateAudio={generateLessonAudio}
                onBulkGenerateAudio={generateBulkLessonAudio}
              />
            ) : tab === "examAudio" ? (
              <div className="grid gap-5">
                <AudioSettingsPanel
                  settings={audioSettings}
                  language="all"
                  isLoading={isLoadingAudioSettings}
                  provider={audioProvider}
                  model={audioModel}
                  voiceId={audioVoiceId}
                  speed={audioSpeed}
                  preview={voicePreviewsByVoiceId[audioVoiceId] ?? null}
                  voicePreviewsByVoiceId={voicePreviewsByVoiceId}
                  isLoadingPreviewCache={isLoadingVoicePreviews}
                  onProviderChange={setAudioProvider}
                  onModelChange={setAudioModel}
                  onVoiceChange={setAudioVoiceId}
                  onSpeedChange={setAudioSpeed}
                />
                <ExamAudioPanel
                  templates={examAudioTemplates}
                  audioReadyToGenerate={Boolean(audioSettings && audioProviderConfigured(audioSettings, audioProvider) && audioSettings.s3Configured)}
                  isLoading={isLoadingExamTemplates}
                  hasLoaded={hasLoadedExamTemplates}
                  generatingTemplateId={generatingExamTemplateId}
                  generatingItemId={generatingExamItemId}
                  onReload={reloadExamAudioTemplates}
                  onGenerateTemplate={generateExamTemplateAudio}
                  onGenerateItem={generateExamItemAudio}
                />
              </div>
            ) : tab === "email" ? (
              <EmailTemplateEditor
                updatedBy={adminName}
                templates={emailTemplates}
                isLoading={isLoadingEmailTemplates}
                selectedTemplate={selectedTemplate}
                onSelectTemplate={selectTemplate}
                onSaved={(template) => {
                  setSelectedTemplate(template);
                  setMessage("Email template tersimpan.");
                  void loadEmailTemplates({ force: true });
                }}
                onError={setError}
              />
            ) : (
              <ChangeLogPanel
                revisions={recentRevisions}
                isLoading={isLoadingRevisions}
                restoringRevisionId={restoringRevisionId}
                onRollback={rollbackRevision}
              />
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

function ReadinessPanel({
  overview,
  levels,
  languages,
  languageFilter,
  isLoading,
  onLanguageFilterChange
}: {
  overview: AdminContentReadinessOverview | null;
  levels: AdminContentReadiness[];
  languages: AdminCmsLanguageOption[];
  languageFilter: LanguageFilter;
  isLoading: boolean;
  onLanguageFilterChange: (value: LanguageFilter) => void;
}) {
  if (isLoading && !overview) {
    return <p className="rounded-lg bg-paper p-5 text-sm text-ink/60">Memuat readiness...</p>;
  }
  if (!overview) {
    return <p className="rounded-lg bg-paper p-5 text-sm text-ink/60">Pilih bahasa atau muat ulang CMS.</p>;
  }

  const filteredLevels = filterReadinessLevels(levels, languageFilter);
  const operations = readinessOperations(filteredLevels);
  const stats = [
    { label: "Planned", value: overview.plannedLessonCount },
    { label: "Implemented", value: overview.implementedLessonCount },
    { label: "Text ready", value: overview.textReadyCount },
    { label: "Audio ready", value: overview.audioReadyCount },
    { label: "Beta ready", value: overview.betaReadyCount },
    { label: "Production ready", value: overview.productionReadyCount }
  ];

  return (
    <div className="space-y-5">
      <div className="grid gap-3 md:grid-cols-3 xl:grid-cols-6">
        {stats.map((stat) => (
          <div key={stat.label} className="rounded-lg bg-paper p-4">
            <p className="text-xs font-semibold uppercase text-ink/45">{stat.label}</p>
            <p className="mt-2 text-2xl font-semibold">{stat.value}</p>
          </div>
        ))}
      </div>

      <LanguageFilterControl
        languages={languages}
        value={languageFilter}
        onChange={onLanguageFilterChange}
      />

      {isLoading ? <p className="rounded-lg bg-paper p-3 text-sm text-ink/60">Refreshing readiness...</p> : null}

      <ProductionOpsPanel
        operations={operations}
        language={languageFilter}
        mode="readiness"
      />

      <div className="grid gap-4">
        {filteredLevels.map((level) => (
          <LevelReadinessCard
            key={`${level.course.language}-${level.course.levelCode}`}
            readiness={level}
            audioReadyToGenerate={false}
            generatingLessonSlug=""
          />
        ))}
        {!filteredLevels.length ? (
          <p className="rounded-lg bg-paper p-5 text-sm text-ink/60">Belum ada readiness untuk filter ini.</p>
        ) : null}
      </div>
    </div>
  );
}

function LessonAudioPanel({
  levels,
  languages,
  languageFilter,
  isLoading,
  onLanguageFilterChange,
  audioSettings,
  audioProvider,
  audioModel,
  audioVoiceId,
  audioSpeed,
  voicePreview,
  voicePreviewsByVoiceId,
  generatingLessonSlug,
  bulkAudioQueue,
  isBulkGeneratingAudio,
  isLoadingAudioSettings,
  isLoadingVoicePreviews,
  onAudioProviderChange,
  onAudioModelChange,
  onAudioVoiceChange,
  onAudioSpeedChange,
  onGenerateAudio,
  onBulkGenerateAudio
}: {
  levels: AdminContentReadiness[];
  languages: AdminCmsLanguageOption[];
  languageFilter: LanguageFilter;
  isLoading: boolean;
  onLanguageFilterChange: (value: LanguageFilter) => void;
  audioSettings: AdminAudioSettings | null;
  audioProvider: string;
  audioModel: string;
  audioVoiceId: string;
  audioSpeed: number;
  voicePreview: AdminVoicePreviewAudio | null;
  voicePreviewsByVoiceId: Record<string, AdminVoicePreviewAudio>;
  generatingLessonSlug: string;
  bulkAudioQueue: BulkAudioQueueItem[];
  isBulkGeneratingAudio: boolean;
  isLoadingAudioSettings: boolean;
  isLoadingVoicePreviews: boolean;
  onAudioProviderChange: (value: string) => void;
  onAudioModelChange: (value: string) => void;
  onAudioVoiceChange: (value: string) => void;
  onAudioSpeedChange: (value: number) => void;
  onGenerateAudio: (lesson: AdminContentReadinessLesson) => void;
  onBulkGenerateAudio: (lessons: BulkAudioQueueItem[]) => void;
}) {
  const filteredLevels = filterReadinessLevels(levels, languageFilter);
  const missingBulkCandidates = bulkAudioCandidates(filteredLevels, { includeAudioReady: false });
  const allTextReadyBulkCandidates = bulkAudioCandidates(filteredLevels, { includeAudioReady: true });
  const audioReadyToGenerate = Boolean(audioSettings && audioProviderConfigured(audioSettings, audioProvider) && audioSettings.s3Configured);
  const operations = readinessOperations(filteredLevels);

  return (
    <div className="space-y-5">
      <AudioSettingsPanel
        settings={audioSettings}
        language={languageFilter}
        isLoading={isLoadingAudioSettings}
        provider={audioProvider}
        model={audioModel}
        voiceId={audioVoiceId}
        speed={audioSpeed}
        preview={voicePreview}
        voicePreviewsByVoiceId={voicePreviewsByVoiceId}
        isLoadingPreviewCache={isLoadingVoicePreviews}
        onProviderChange={onAudioProviderChange}
        onModelChange={onAudioModelChange}
        onVoiceChange={onAudioVoiceChange}
        onSpeedChange={onAudioSpeedChange}
      />

      <LanguageFilterControl
        languages={languages}
        value={languageFilter}
        onChange={onLanguageFilterChange}
      />

      {isLoading ? <p className="rounded-lg bg-paper p-3 text-sm text-ink/60">Refreshing lesson audio...</p> : null}

      <ProductionOpsPanel
        operations={operations}
        language={languageFilter}
        mode="audio"
      />

      <BulkAudioPanel
        missingCandidates={missingBulkCandidates}
        allTextReadyCandidates={allTextReadyBulkCandidates}
        queue={bulkAudioQueue}
        isRunning={isBulkGeneratingAudio}
        audioReadyToGenerate={audioReadyToGenerate}
        onStart={onBulkGenerateAudio}
      />

      <div className="grid gap-4">
        {filteredLevels.map((level) => (
          <LevelReadinessCard
            key={`${level.course.language}-${level.course.levelCode}`}
            readiness={level}
            audioReadyToGenerate={audioReadyToGenerate && !isBulkGeneratingAudio}
            generatingLessonSlug={generatingLessonSlug}
            onGenerateAudio={onGenerateAudio}
            onGenerateUnitAudio={onBulkGenerateAudio}
          />
        ))}
        {!filteredLevels.length ? (
          <p className="rounded-lg bg-paper p-5 text-sm text-ink/60">Belum ada lesson audio untuk filter ini.</p>
        ) : null}
      </div>
    </div>
  );
}

function ProductionOpsPanel({
  operations,
  language,
  mode
}: {
  operations: ReadinessOperations;
  language: LanguageFilter;
  mode: "readiness" | "audio";
}) {
  const action =
    operations.missingTextCount > 0
      ? "Lengkapi text readiness sebelum audio."
      : operations.missingAudioCount > 0
        ? "Generate missing audio per unit atau jalankan batch."
        : operations.productionGapCount > 0
          ? "Review publish status sebelum release."
          : "Track siap untuk release check.";
  const actionTone =
    operations.missingTextCount > 0 || operations.missingAudioCount > 0
      ? "warn"
      : operations.productionGapCount > 0
        ? "neutral"
        : "ok";

  return (
    <section className="rounded-lg border border-ink/10 bg-white p-4 shadow-sm">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase text-leaf">
            {languageLabelForOps(language)} / production operations
          </p>
          <h2 className="mt-1 text-lg font-semibold">
            {mode === "audio" ? "Audio release queue" : "Release readiness summary"}
          </h2>
          <p className="mt-1 max-w-3xl text-sm leading-6 text-ink/60">
            Ringkasan ini membantu admin menentukan apakah fokus berikutnya content, audio, atau publish review.
          </p>
        </div>
        <StatusPill icon={ListChecks} label={action} tone={actionTone} />
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-4">
        <OpsMetric label="Text missing" value={operations.missingTextCount} tone={operations.missingTextCount ? "danger" : "ok"} />
        <OpsMetric label="Audio missing" value={operations.missingAudioCount} tone={operations.missingAudioCount ? "warn" : "ok"} />
        <OpsMetric label="Production gap" value={operations.productionGapCount} tone={operations.productionGapCount ? "warn" : "ok"} />
        <OpsMetric label="Regenerate candidates" value={operations.textReadyCount} tone="neutral" />
      </div>

      {operations.firstBlockingLessons.length ? (
        <div className="mt-4 rounded-lg bg-paper p-3">
          <p className="text-xs font-semibold uppercase text-ink/45">First blocking lessons</p>
          <div className="mt-2 grid gap-2 md:grid-cols-2">
            {operations.firstBlockingLessons.map((lesson) => (
              <div key={lesson.slug || lesson.lessonKey} className="rounded-lg bg-white px-3 py-2">
                <p className="truncate text-sm font-semibold text-ink">{lesson.title}</p>
                <p className="mt-1 truncate text-xs text-ink/50">{lesson.slug || lesson.lessonKey}</p>
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </section>
  );
}

function OpsMetric({
  label,
  value,
  tone
}: {
  label: string;
  value: number;
  tone: "ok" | "warn" | "danger" | "neutral";
}) {
  const toneClass =
    tone === "ok"
      ? "bg-mint text-leaf"
      : tone === "warn"
        ? "bg-[#fff4d5] text-[#7a5600]"
        : tone === "danger"
          ? "bg-[#fde7df] text-coral"
          : "bg-paper text-ink/60";
  return (
    <div className={`rounded-lg px-4 py-3 ${toneClass}`}>
      <p className="text-xs font-semibold uppercase opacity-75">{label}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
    </div>
  );
}

function AudioSettingsPanel({
  settings,
  language,
  isLoading,
  provider,
  model,
  voiceId,
  speed,
  preview,
  voicePreviewsByVoiceId,
  isLoadingPreviewCache,
  onProviderChange,
  onModelChange,
  onVoiceChange,
  onSpeedChange
}: {
  settings: AdminAudioSettings | null;
  language: LanguageFilter | "all";
  isLoading: boolean;
  provider: string;
  model: string;
  voiceId: string;
  speed: number;
  preview: AdminVoicePreviewAudio | null;
  voicePreviewsByVoiceId: Record<string, AdminVoicePreviewAudio>;
  isLoadingPreviewCache: boolean;
  onProviderChange: (value: string) => void;
  onModelChange: (value: string) => void;
  onVoiceChange: (value: string) => void;
  onSpeedChange: (value: number) => void;
}) {
  const configured = Boolean(settings && audioProviderConfigured(settings, provider) && settings.s3Configured);
  const voiceOptions = filterVoicesForLanguage(settings?.voices ?? [], language, provider);
  const modelOptions = audioModelsForProvider(settings, provider);
  const selectedVoice = voiceOptions.find((voice) => voice.voiceId === voiceId);
  const providerOptions = settings?.providers ?? [];

  return (
    <div className="rounded-lg bg-paper p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-lg bg-white">
            <Volume2 className="h-5 w-5 text-leaf" aria-hidden="true" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase text-leaf">Audio Generator</p>
            <h2 className="mt-1 font-semibold">Listening audio</h2>
            <p className="mt-1 text-sm text-ink/55">
              Pilih default voice dan model untuk generate audio listening lesson.
            </p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2 text-xs font-semibold">
          {isLoading ? <StatusPill icon={RefreshCcw} label="Loading settings" tone="neutral" /> : null}
          <StatusPill
            icon={Sparkles}
            label={settings?.minimaxConfigured ? "MiniMax ready" : "MiniMax missing"}
            tone={settings?.minimaxConfigured ? "ok" : "danger"}
          />
          <StatusPill
            icon={Sparkles}
            label={settings?.elevenlabsConfigured ? "ElevenLabs ready" : "ElevenLabs missing"}
            tone={settings?.elevenlabsConfigured ? "ok" : "danger"}
          />
          <StatusPill
            icon={Headphones}
            label={settings?.s3Configured ? "S3 ready" : "S3 missing"}
            tone={settings?.s3Configured ? "ok" : "danger"}
          />
        </div>
      </div>

      <div className="mt-4 grid gap-3 lg:grid-cols-[180px_1fr_140px]">
        <label className="text-sm font-medium text-ink/70">
          Provider
          <select
            value={provider}
            onChange={(event) => {
              const nextProvider = event.target.value;
              onProviderChange(nextProvider);
              if (settings) {
                onModelChange(defaultAudioModelForProvider(settings, nextProvider));
                onVoiceChange(defaultAudioVoiceIdForLanguage(settings, language, nextProvider));
              }
            }}
            disabled={!settings}
            className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink disabled:cursor-not-allowed disabled:opacity-60"
          >
            {!providerOptions.length ? <option value="">Loading</option> : null}
            {providerOptions.map((providerOption) => (
              <option key={providerOption.key} value={providerOption.key}>
                {providerOption.label}
              </option>
            ))}
          </select>
        </label>

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

      <div className="mt-3">
        <VoicePicker
          voices={voiceOptions}
          selectedVoiceId={voiceId}
          previewByVoiceId={voicePreviewsByVoiceId}
          disabled={!settings}
          onChange={onVoiceChange}
        />
      </div>

      <div className="mt-3 rounded-lg bg-white p-4 text-sm text-ink/65">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p className="font-semibold text-ink">
              {selectedVoice ? selectedVoice.voiceName : "Voice preview"}
            </p>
            <p className="mt-1 max-w-3xl text-xs leading-5 text-ink/50">
              {selectedVoice
                ? `${selectedVoice.voiceId}${selectedVoice.description ? ` / ${selectedVoice.description}` : ""}`
                : "Pilih voice untuk mendengar contoh suara."}
            </p>
          </div>
          {selectedVoice ? <VoiceGenderPill gender={selectedVoice.gender} /> : null}
        </div>

        {preview?.audioUrl ? (
          <div className="mt-3">
            <audio controls preload="metadata" src={preview.playbackUrl || preview.audioUrl} className="h-10 w-full" />
            <p className="mt-2 text-xs text-ink/45">
              Cached preview / {preview.model} / {preview.voiceId} / {formatDuration(preview.durationSeconds)}
            </p>
          </div>
        ) : isLoadingPreviewCache ? (
          <p className="mt-3 text-xs font-semibold text-ink/45">Loading cached preview...</p>
        ) : selectedVoice ? (
          <p className="mt-3 rounded-lg bg-mint px-3 py-2 text-xs font-semibold text-ink/55">
            Preview cache belum tersedia untuk voice ini.
          </p>
        ) : null}
      </div>

      {!configured ? (
        <p className="mt-3 rounded-lg bg-white px-3 py-2 text-sm text-ink/60">
          Generate audio aktif setelah provider API key, <code>S3_BUCKET</code>,{" "}
          <code>AWS_ACCESS_KEY_ID</code>, <code>AWS_SECRET_ACCESS_KEY</code>, dan{" "}
          <code>AWS_REGION</code> tersedia di API.
        </p>
      ) : null}
    </div>
  );
}

function BulkAudioPanel({
  missingCandidates,
  allTextReadyCandidates,
  queue,
  isRunning,
  audioReadyToGenerate,
  onStart
}: {
  missingCandidates: BulkAudioQueueItem[];
  allTextReadyCandidates: BulkAudioQueueItem[];
  queue: BulkAudioQueueItem[];
  isRunning: boolean;
  audioReadyToGenerate: boolean;
  onStart: (lessons: BulkAudioQueueItem[]) => void;
}) {
  const summary = bulkQueueSummary(queue);
  const runningItem = queue.find((item) => item.status === "running") ?? null;

  return (
    <div className="rounded-lg border border-leaf/25 bg-mint p-4">
      <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div className="flex items-start gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-lg bg-white">
            <Sparkles className="h-5 w-5 text-leaf" aria-hidden="true" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase text-leaf">Batch Audio Queue</p>
            <h2 className="mt-1 font-semibold">Generate listening audio sekaligus</h2>
            <p className="mt-1 max-w-2xl text-sm leading-6 text-ink/60">
              Queue berjalan berurutan, retry otomatis sampai 2 kali, lalu refresh readiness setelah selesai.
            </p>
            <div className="mt-2 flex flex-wrap gap-2 text-xs font-semibold">
              <StatusPill icon={Headphones} label={`${missingCandidates.length} missing`} tone="warn" />
              <StatusPill icon={ListChecks} label={`${allTextReadyCandidates.length} text-ready`} tone="neutral" />
              {queue.length ? (
                <StatusPill icon={CheckCircle2} label={`${summary.done}/${queue.length} done`} tone="ok" />
              ) : null}
            </div>
          </div>
        </div>

        <div className="grid gap-2 sm:grid-cols-2">
          <button
            type="button"
            onClick={() => onStart(missingCandidates)}
            disabled={!audioReadyToGenerate || isRunning || !missingCandidates.length}
            className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-leaf px-4 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Headphones className="h-4 w-4" aria-hidden="true" />
            Generate All Missing Audio
          </button>
          <button
            type="button"
            onClick={() => onStart(allTextReadyCandidates)}
            disabled={!audioReadyToGenerate || isRunning || !allTextReadyCandidates.length}
            className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
          >
            <RefreshCcw className="h-4 w-4" aria-hidden="true" />
            Regenerate Text-Ready Audio
          </button>
        </div>
      </div>

      {queue.length ? (
        <div className="mt-4 rounded-lg bg-white p-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="text-sm font-semibold text-ink">
              {isRunning && runningItem ? `Running: ${runningItem.lessonTitle}` : "Last bulk run"}
            </p>
            <div className="flex flex-wrap gap-2 text-xs font-semibold">
              <StatusPill icon={Clock3} label={`${summary.pending} queued`} tone="neutral" />
              <StatusPill icon={CheckCircle2} label={`${summary.done} done`} tone="ok" />
              <StatusPill icon={XCircle} label={`${summary.failed} failed`} tone={summary.failed ? "danger" : "neutral"} />
            </div>
          </div>

          <div className="mt-3 grid max-h-72 gap-2 overflow-y-auto pr-1">
            {queue.map((item) => (
              <div key={item.lessonSlug} className="grid gap-2 rounded-lg bg-paper p-3 md:grid-cols-[1fr_auto]">
                <div className="min-w-0">
                  <p className="truncate text-sm font-semibold text-ink">{item.lessonTitle}</p>
                  <p className="mt-1 truncate text-xs text-ink/50">
                    {item.levelCode} / {item.unitTitle} / attempt {item.attempts || 0}
                  </p>
                  {item.error ? <p className="mt-1 text-xs text-coral">{item.error}</p> : null}
                </div>
                <div className="flex flex-wrap items-center gap-2 md:justify-end">
                  <BulkStatusPill status={item.status} />
                  {item.durationSeconds ? (
                    <span className="text-xs font-semibold text-ink/45">{formatDuration(item.durationSeconds)}</span>
                  ) : null}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}

function ExamAudioPanel({
  templates,
  audioReadyToGenerate,
  isLoading,
  hasLoaded,
  generatingTemplateId,
  generatingItemId,
  onReload,
  onGenerateTemplate,
  onGenerateItem
}: {
  templates: AdminExamAudioTemplate[];
  audioReadyToGenerate: boolean;
  isLoading: boolean;
  hasLoaded: boolean;
  generatingTemplateId: string;
  generatingItemId: string;
  onReload: () => void;
  onGenerateTemplate: (template: AdminExamAudioTemplate, onlyMissing: boolean) => void;
  onGenerateItem: (templateId: string, item: AdminExamListeningItem) => void;
}) {
  return (
    <div className="rounded-lg border border-ink/10 bg-white p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-lg bg-paper">
            <Headphones className="h-5 w-5 text-leaf" aria-hidden="true" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase text-leaf">Exam Audio</p>
            <h2 className="mt-1 font-semibold">Generate audio untuk exam (listening & speaking)</h2>
            <p className="mt-1 max-w-3xl text-sm leading-6 text-ink/60">
              Pilih template exam lalu generate audio per item atau sekaligus. Tombol Generate Missing juga
              meng-update item yang audionya outdated karena teks soal sudah berubah sejak audio dibuat.
            </p>
          </div>
        </div>
        {isLoading ? (
          <span className="rounded-lg bg-paper px-3 py-2 text-xs font-semibold text-ink/55">Loading exams...</span>
        ) : (
          <button
            type="button"
            onClick={onReload}
            className="focus-ring inline-flex min-h-10 items-center justify-center gap-2 rounded-lg bg-paper px-3 text-sm font-semibold text-ink hover:bg-mint"
          >
            <RefreshCcw className="h-4 w-4" aria-hidden="true" />
            Reload Exam Audio
          </button>
        )}
      </div>

      <div className="mt-4 grid gap-4">
        {templates.length ? (
          templates.map((template) => {
            const itemGroups = [
              { label: "Listening", items: template.listeningItems },
              { label: "Speaking", items: template.speakingItems }
            ].filter((group) => group.items.length > 0);
            const totalItemCount = template.listeningItemCount + template.speakingItemCount;
            const pendingCount =
              totalItemCount -
              template.listeningAudioReadyCount -
              template.speakingAudioReadyCount +
              template.listeningAudioStaleCount +
              template.speakingAudioStaleCount;
            const staleCount = template.listeningAudioStaleCount + template.speakingAudioStaleCount;
            return (
              <div key={template.id} className="rounded-lg border border-ink/10 bg-paper p-4">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <p className="text-xs font-semibold uppercase text-leaf">
                      {template.levelCode} / {template.code}
                    </p>
                    <h3 className="mt-1 text-lg font-semibold">{template.title}</h3>
                    <p className="mt-1 text-sm text-ink/55">
                      Listening {template.listeningAudioReadyCount}/{template.listeningItemCount} · Speaking{" "}
                      {template.speakingAudioReadyCount}/{template.speakingItemCount}
                      {staleCount ? ` · ${staleCount} outdated` : ""}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => onGenerateTemplate(template, true)}
                      disabled={!audioReadyToGenerate || generatingTemplateId === template.id || !pendingCount}
                      className="focus-ring inline-flex min-h-10 items-center justify-center gap-2 rounded-lg bg-leaf px-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      <Sparkles className="h-4 w-4" aria-hidden="true" />
                      {generatingTemplateId === template.id ? "Generating" : "Generate Missing"}
                    </button>
                    <button
                      type="button"
                      onClick={() => onGenerateTemplate(template, false)}
                      disabled={!audioReadyToGenerate || generatingTemplateId === template.id || !totalItemCount}
                      className="focus-ring inline-flex min-h-10 items-center justify-center gap-2 rounded-lg bg-ink px-3 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      <RefreshCcw className="h-4 w-4" aria-hidden="true" />
                      Regenerate All
                    </button>
                  </div>
                </div>

                {itemGroups.map((group) => (
                  <div key={group.label} className="mt-4">
                    <p className="text-xs font-semibold uppercase text-ink/45">{group.label}</p>
                    <div className="mt-2 grid gap-3">
                      {group.items.map((item) => (
                        <div key={item.id} className="rounded-lg bg-white p-3">
                          <div className="flex flex-wrap items-start justify-between gap-3">
                            <div className="min-w-0">
                              <p className="text-sm font-semibold text-ink">Item {item.sequenceOrder}</p>
                              <p className="mt-1 text-sm text-ink/65">{item.promptText}</p>
                              {item.stimulusText ? (
                                <p className="mt-2 whitespace-pre-wrap text-xs leading-5 text-ink/50">{item.stimulusText}</p>
                              ) : null}
                            </div>
                            <div className="flex flex-wrap items-center gap-2">
                              {item.audioStale ? (
                                <span className="inline-flex min-h-8 items-center gap-1.5 rounded-lg bg-[#fff3d6] px-2.5 text-xs font-semibold text-[#9a6b00]">
                                  <RefreshCcw className="h-3.5 w-3.5" aria-hidden="true" />
                                  Outdated
                                </span>
                              ) : (
                                <ReadinessPill ready={item.audioReady} label="Audio" />
                              )}
                              <button
                                type="button"
                                onClick={() => onGenerateItem(template.id, item)}
                                disabled={!audioReadyToGenerate || generatingItemId === item.id}
                                className="focus-ring inline-flex min-h-9 items-center justify-center gap-2 rounded-lg bg-ink px-3 text-xs font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
                              >
                                <Sparkles className="h-3.5 w-3.5" aria-hidden="true" />
                                {generatingItemId === item.id ? "Generating" : item.audioReady ? "Regenerate" : "Generate"}
                              </button>
                            </div>
                          </div>

                          {item.audioMetadata && (item.audioMetadata.playback_url || item.stimulusAudioUrl) ? (
                            <div className="mt-3 rounded-lg bg-paper p-3">
                              <audio
                                controls
                                preload="metadata"
                                src={String(item.audioMetadata.playback_url || item.stimulusAudioUrl)}
                                className="h-10 w-full"
                              />
                              <p className="mt-2 text-xs text-ink/45">
                                {String(item.audioMetadata.provider || "provider unknown")} /{" "}
                                {String(item.audioMetadata.model || "model unknown")} /{" "}
                                {String(item.audioMetadata.voice_id || "voice unknown")}
                              </p>
                            </div>
                          ) : null}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            );
          })
        ) : (
          <div className="rounded-lg bg-paper p-4 text-sm text-ink/60">
            {hasLoaded ? "Belum ada template exam yang tersedia." : "Buka tab ini untuk memuat template exam."}
          </div>
        )}
      </div>
    </div>
  );
}

function BulkStatusPill({ status }: { status: BulkAudioQueueStatus }) {
  const label = status === "done" ? "Done" : status === "failed" ? "Failed" : status === "running" ? "Running" : "Queued";
  const tone =
    status === "done"
      ? "bg-mint text-ink/70"
      : status === "failed"
        ? "bg-[#fde7df] text-[#9a3f1b]"
        : status === "running"
          ? "bg-[#fff0d5] text-[#83540f]"
          : "bg-white text-ink/55";
  return <span className={`inline-flex h-7 items-center rounded-lg px-2 text-xs font-semibold ${tone}`}>{label}</span>;
}

type VoiceGenderFilter = "all" | "female" | "male";

const voiceGenderFilters: Array<{ key: VoiceGenderFilter; label: string }> = [
  { key: "all", label: "All" },
  { key: "female", label: "Female" },
  { key: "male", label: "Male" }
];

function VoicePicker({
  voices,
  selectedVoiceId,
  previewByVoiceId,
  disabled,
  onChange
}: {
  voices: AdminAudioVoice[];
  selectedVoiceId: string;
  previewByVoiceId: Record<string, AdminVoicePreviewAudio>;
  disabled: boolean;
  onChange: (value: string) => void;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [genderFilter, setGenderFilter] = useState<VoiceGenderFilter>("all");
  const [query, setQuery] = useState("");
  const selectedVoice = voices.find((voice) => voice.voiceId === selectedVoiceId) ?? null;
  const filteredVoices = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    return voices.filter((voice) => {
      const matchesGender = genderFilter === "all" || voice.gender === genderFilter;
      const searchable = `${voice.voiceName} ${voice.voiceId} ${voice.description}`.toLowerCase();
      return matchesGender && (!normalizedQuery || searchable.includes(normalizedQuery));
    });
  }, [genderFilter, query, voices]);

  return (
    <div className="relative">
      <p className="mb-2 text-sm font-medium text-ink/70">Voice</p>
      <button
        type="button"
        onClick={() => setIsOpen((current) => !current)}
        disabled={disabled}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        className="focus-ring flex min-h-[76px] w-full items-center justify-between gap-4 rounded-lg border border-ink/10 bg-white px-4 py-3 text-left shadow-sm transition hover:border-leaf/40 disabled:cursor-not-allowed disabled:opacity-60"
      >
        <span className="min-w-0">
          <span className="flex flex-wrap items-center gap-2">
            <span className="truncate text-base font-semibold text-ink">
              {selectedVoice ? selectedVoice.voiceName : "Pilih voice"}
            </span>
            {selectedVoice ? <VoiceGenderPill gender={selectedVoice.gender} /> : null}
            {selectedVoice && previewByVoiceId[selectedVoice.voiceId] ? (
              <span className="inline-flex h-7 items-center rounded-lg bg-mint px-2 text-xs font-semibold text-ink/65">
                Cached
              </span>
            ) : null}
          </span>
          <span className="mt-1 block truncate text-xs text-ink/50">
            {selectedVoice ? selectedVoice.voiceId : "Belum ada voice terpilih."}
          </span>
        </span>
        <ChevronDown
          className={`h-5 w-5 shrink-0 text-ink/45 transition ${isOpen ? "rotate-180" : ""}`}
          aria-hidden="true"
        />
      </button>

      {isOpen ? (
        <div className="absolute left-0 right-0 z-30 mt-2 rounded-lg border border-ink/10 bg-white p-3 shadow-xl">
          <div className="grid gap-3 md:grid-cols-[1fr_auto]">
            <label className="relative block">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink/35" />
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                className="focus-ring h-10 w-full rounded-lg border border-ink/10 bg-paper pl-9 pr-3 text-sm text-ink"
                placeholder="Search voice"
              />
            </label>
            <div className="flex rounded-lg bg-paper p-1">
              {voiceGenderFilters.map((filter) => (
                <button
                  key={filter.key}
                  type="button"
                  onClick={() => setGenderFilter(filter.key)}
                  className={`focus-ring h-8 rounded-md px-3 text-xs font-semibold ${
                    genderFilter === filter.key ? "bg-ink text-white" : "text-ink/55 hover:bg-white"
                  }`}
                >
                  {filter.label}
                </button>
              ))}
            </div>
          </div>

          <div role="listbox" className="mt-3 grid max-h-80 gap-2 overflow-y-auto pr-1">
            {filteredVoices.length ? (
              filteredVoices.map((voice) => {
                const isSelected = voice.voiceId === selectedVoiceId;
                const hasPreview = Boolean(previewByVoiceId[voice.voiceId]);
                return (
                  <button
                    key={voice.voiceId}
                    type="button"
                    role="option"
                    aria-selected={isSelected}
                    onClick={() => {
                      onChange(voice.voiceId);
                      setIsOpen(false);
                    }}
                    className={`focus-ring grid gap-2 rounded-lg border px-3 py-3 text-left transition ${
                      isSelected
                        ? "border-leaf bg-mint"
                        : "border-ink/10 bg-white hover:border-leaf/35 hover:bg-paper"
                    }`}
                  >
                    <span className="flex items-start justify-between gap-3">
                      <span className="min-w-0">
                        <span className="block truncate text-sm font-semibold text-ink">{voice.voiceName}</span>
                        <span className="mt-1 block truncate text-xs text-ink/45">{voice.voiceId}</span>
                      </span>
                      <span className="flex shrink-0 items-center gap-2">
                        <VoiceGenderPill gender={voice.gender} />
                        {hasPreview ? (
                          <span className="inline-flex h-7 items-center rounded-lg bg-white px-2 text-xs font-semibold text-ink/55">
                            Audio
                          </span>
                        ) : null}
                        {isSelected ? <CheckCircle2 className="h-4 w-4 text-leaf" aria-hidden="true" /> : null}
                      </span>
                    </span>
                    {voice.description ? (
                      <span className="line-clamp-2 text-xs leading-5 text-ink/50">{voice.description}</span>
                    ) : null}
                  </button>
                );
              })
            ) : (
              <div className="rounded-lg bg-paper px-3 py-4 text-sm text-ink/55">Voice tidak ditemukan.</div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
}

function VoiceGenderPill({ gender }: { gender: AdminAudioVoice["gender"] }) {
  const label = gender === "female" ? "Female" : gender === "male" ? "Male" : "Neutral";
  const tone =
    gender === "female"
      ? "bg-[#fde7df] text-[#9a3f1b]"
      : gender === "male"
        ? "bg-[#e7f0ed] text-[#315f55]"
        : "bg-paper text-ink/55";
  return (
    <span className={`inline-flex h-7 items-center rounded-lg px-2 text-xs font-semibold ${tone}`}>
      {label}
    </span>
  );
}

function LevelReadinessCard({
  readiness,
  audioReadyToGenerate,
  generatingLessonSlug,
  onGenerateAudio,
  onGenerateUnitAudio
}: {
  readiness: AdminContentReadiness;
  audioReadyToGenerate: boolean;
  generatingLessonSlug: string;
  onGenerateAudio?: (lesson: AdminContentReadinessLesson) => void;
  onGenerateUnitAudio?: (lessons: BulkAudioQueueItem[]) => void;
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
        {readiness.units.map((unit) => {
          const missingUnitAudio = unitAudioCandidates(readiness, unit, { includeAudioReady: false });
          const allUnitAudio = unitAudioCandidates(readiness, unit, { includeAudioReady: true });
          return (
          <div key={unit.unitKey} className="rounded-lg border border-ink/10 bg-white p-4">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase text-leaf">{unit.status}</p>
                <h2 className="mt-1 text-lg font-semibold">{unit.title}</h2>
                <p className="mt-1 text-sm text-ink/55">{unit.unitKey}</p>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <div className="flex flex-wrap gap-2 text-xs font-semibold">
                  <StatusPill icon={CheckCircle2} label={`${unit.textReadyCount}/${unit.lessonCount} text`} tone="ok" />
                  <StatusPill icon={Headphones} label={`${unit.audioReadyCount}/${unit.lessonCount} audio`} tone="warn" />
                  <StatusPill
                    icon={ShieldCheck}
                    label={`${unit.productionReadyCount}/${unit.lessonCount} prod`}
                    tone="neutral"
                  />
                </div>
                {onGenerateUnitAudio ? (
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => onGenerateUnitAudio(missingUnitAudio)}
                      disabled={!audioReadyToGenerate || !missingUnitAudio.length}
                      className="focus-ring inline-flex min-h-9 items-center justify-center gap-2 rounded-lg bg-leaf px-3 text-xs font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      <Headphones className="h-3.5 w-3.5" aria-hidden="true" />
                      Generate Missing Unit
                    </button>
                    <button
                      type="button"
                      onClick={() => onGenerateUnitAudio(allUnitAudio)}
                      disabled={!audioReadyToGenerate || !allUnitAudio.length}
                      className="focus-ring inline-flex min-h-9 items-center justify-center gap-2 rounded-lg bg-ink px-3 text-xs font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      <RefreshCcw className="h-3.5 w-3.5" aria-hidden="true" />
                      Regenerate Unit
                    </button>
                  </div>
                ) : null}
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

                    {onGenerateAudio && lesson.implemented && lesson.textReady ? (
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
                              {lesson.audioAsset.provider || "provider unknown"} /{" "}
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
        );
        })}
      </div>
    </div>
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

function filterReadinessLevels(
  levels: AdminContentReadiness[],
  languageFilter: LanguageFilter
): AdminContentReadiness[] {
  return levels.filter((level) => level.course.language === languageFilter);
}

type ReadinessOperations = {
  textReadyCount: number;
  missingTextCount: number;
  missingAudioCount: number;
  productionGapCount: number;
  firstBlockingLessons: AdminContentReadinessLesson[];
};

function readinessOperations(levels: AdminContentReadiness[]): ReadinessOperations {
  const lessons = levels.flatMap((level) => level.units.flatMap((unit) => unit.lessons));
  const firstBlockingLessons = lessons
    .filter((lesson) => !lesson.textReady || !lesson.audioReady || !lesson.productionReady)
    .slice(0, 4);

  return {
    textReadyCount: lessons.filter((lesson) => lesson.implemented && lesson.textReady).length,
    missingTextCount: lessons.filter((lesson) => lesson.implemented && !lesson.textReady).length,
    missingAudioCount: lessons.filter((lesson) => lesson.implemented && lesson.textReady && !lesson.audioReady).length,
    productionGapCount: lessons.filter((lesson) => lesson.implemented && lesson.textReady && !lesson.productionReady).length,
    firstBlockingLessons
  };
}

function languageLabelForOps(language: LanguageFilter) {
  if (language.toLowerCase() === "arabic") {
    return "Arabic";
  }
  if (language.toLowerCase() === "english") {
    return "English";
  }
  return language;
}

function bulkAudioCandidates(
  levels: AdminContentReadiness[],
  { includeAudioReady }: { includeAudioReady: boolean }
): BulkAudioQueueItem[] {
  const seenSlugs = new Set<string>();
  const candidates: BulkAudioQueueItem[] = [];

  for (const level of levels) {
    for (const unit of level.units) {
      for (const lesson of unit.lessons) {
        if (!lesson.slug || !lesson.implemented || !lesson.textReady) {
          continue;
        }
        if (!includeAudioReady && lesson.audioReady) {
          continue;
        }
        if (seenSlugs.has(lesson.slug)) {
          continue;
        }
        seenSlugs.add(lesson.slug);
        candidates.push({
          lessonSlug: lesson.slug,
          lessonTitle: lesson.title,
          levelCode: level.course.levelCode,
          unitTitle: unit.title,
          status: "pending",
          attempts: 0,
          error: ""
        });
      }
    }
  }

  return candidates;
}

function unitAudioCandidates(
  level: AdminContentReadiness,
  unit: AdminContentReadiness["units"][number],
  { includeAudioReady }: { includeAudioReady: boolean }
): BulkAudioQueueItem[] {
  return unit.lessons
    .filter((lesson) => lesson.slug && lesson.implemented && lesson.textReady)
    .filter((lesson) => includeAudioReady || !lesson.audioReady)
    .map((lesson) => ({
      lessonSlug: lesson.slug,
      lessonTitle: lesson.title,
      levelCode: level.course.levelCode,
      unitTitle: unit.title,
      status: "pending" as BulkAudioQueueStatus,
      attempts: 0,
      error: ""
    }));
}

function bulkQueueSummary(queue: BulkAudioQueueItem[]) {
  return queue.reduce(
    (summary, item) => {
      if (item.status === "done") {
        summary.done += 1;
      } else if (item.status === "failed") {
        summary.failed += 1;
      } else if (item.status === "running") {
        summary.running += 1;
      } else {
        summary.pending += 1;
      }
      return summary;
    },
    { pending: 0, running: 0, done: 0, failed: 0 }
  );
}

function filterVoicesForLanguage(voices: AdminAudioVoice[], language: LanguageFilter | "all", provider: string) {
  return voices.filter((voice) => audioVoiceMatchesLanguage(voice.voiceId, language, voices, provider));
}

function audioVoiceMatchesLanguage(
  voiceId: string,
  language: LanguageFilter | "all",
  voices: AdminAudioVoice[],
  provider: string
) {
  if (!voiceId || language === "all") {
    const voice = voices.find((item) => item.voiceId === voiceId);
    return Boolean(voiceId && (!provider || voice?.provider === provider));
  }
  const voice = voices.find((item) => item.voiceId === voiceId);
  if (provider && voice?.provider !== provider) {
    return false;
  }
  const normalizedLanguage = language.toLowerCase();
  if (normalizedLanguage === "arabic") {
    return provider === "elevenlabs" || voice?.language?.toLowerCase() === "arabic";
  }
  if (normalizedLanguage === "english") {
    return provider === "minimax" && (voiceId.toLowerCase().startsWith("english_") || voice?.language?.toLowerCase() === "english");
  }
  return true;
}

function defaultAudioProviderForLanguage(
  settings: AdminAudioSettings,
  language: LanguageFilter | "all",
  currentProvider: string
) {
  const availableProviders = new Set(settings.providers.map((provider) => provider.key));
  if (language.toLowerCase() === "arabic" && availableProviders.has("elevenlabs")) {
    return "elevenlabs";
  }
  if (language.toLowerCase() === "english" && availableProviders.has("minimax")) {
    return "minimax";
  }
  if (currentProvider && availableProviders.has(currentProvider)) {
    return currentProvider;
  }
  return settings.defaultProvider || settings.providers[0]?.key || "minimax";
}

function defaultAudioVoiceIdForLanguage(
  settings: AdminAudioSettings,
  language: LanguageFilter | "all",
  provider: string
) {
  const voices = settings.voices.filter((voice) => voice.provider === provider);
  if (provider === "elevenlabs") {
    return (
      voices.find((voice) => voice.voiceId === audioProviderConfig(settings, provider)?.defaultVoiceId)?.voiceId ??
      voices.find((voice) => voice.gender === "male")?.voiceId ??
      voices[0]?.voiceId ??
      audioProviderConfig(settings, provider)?.defaultVoiceId ??
      settings.defaultVoiceId
    );
  }
  if (language.toLowerCase() === "arabic") {
    return (
      voices.find((voice) => voice.voiceId === "Arabic_FriendlyGuy")?.voiceId ??
      voices.find((voice) => voice.voiceId.toLowerCase().startsWith("arabic_"))?.voiceId ??
      audioProviderConfig(settings, provider)?.defaultVoiceId ??
      settings.defaultVoiceId
    );
  }
  if (language.toLowerCase() === "english" || provider === "minimax") {
    return (
      voices.find((voice) => voice.voiceId === settings.defaultVoiceId)?.voiceId ??
      voices.find((voice) => voice.voiceId.toLowerCase().startsWith("english_"))?.voiceId ??
      audioProviderConfig(settings, provider)?.defaultVoiceId ??
      settings.defaultVoiceId
    );
  }
  return voices[0]?.voiceId ?? audioProviderConfig(settings, provider)?.defaultVoiceId ?? settings.defaultVoiceId;
}

function audioProviderConfig(settings: AdminAudioSettings, provider: string) {
  return settings.providers.find((item) => item.key === provider) ?? null;
}

function audioProviderConfigured(settings: AdminAudioSettings, provider: string) {
  return Boolean(audioProviderConfig(settings, provider)?.configured);
}

function audioModelsForProvider(settings: AdminAudioSettings | null, provider: string) {
  if (!settings) {
    return [];
  }
  return audioProviderConfig(settings, provider)?.models ?? settings.models;
}

function defaultAudioModelForProvider(settings: AdminAudioSettings, provider: string) {
  return audioProviderConfig(settings, provider)?.defaultModel ?? settings.defaultModel;
}

function audioModelMatchesProvider(model: string, provider: string, settings: AdminAudioSettings) {
  return Boolean(model && audioModelsForProvider(settings, provider).includes(model));
}

function defaultAudioSpeedForLanguage(language: LanguageFilter | "all", current: number) {
  if (language.toLowerCase() === "arabic" && current >= 1) {
    return 0.9;
  }
  if (language.toLowerCase() === "english" && Math.abs(current - 0.9) < 0.001) {
    return 1;
  }
  return current;
}

function audioPreviewSampleText(language: LanguageFilter | "all") {
  if (language.toLowerCase() === "arabic") {
    return "مرحبًا. اسمي أحمد. أنا أتعلم العربية الفصحى بوضوح وهدوء.";
  }
  return undefined;
}

function storedAudioProvider(fallback: string) {
  return window.localStorage.getItem(audioProviderStorageKey) || fallback;
}

function storedAudioModel(fallback: string, provider: string) {
  const storedModel = window.localStorage.getItem(audioModelStorageKey);
  if (!storedModel) {
    return fallback;
  }
  if (provider === "elevenlabs" && storedModel.startsWith("eleven_")) {
    return storedModel;
  }
  if (provider === "minimax" && storedModel.startsWith("speech-")) {
    return storedModel;
  }
  return fallback;
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
