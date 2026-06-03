"use client";

import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  BookOpen,
  CheckCircle2,
  Clock3,
  FileText,
  Headphones,
  KeyRound,
  ListChecks,
  RefreshCcw,
  RotateCcw,
  Save,
  ShieldCheck,
  XCircle,
  type LucideIcon
} from "lucide-react";
import type { ReactNode } from "react";
import {
  getAdminCmsLesson,
  getAdminCmsSummary,
  getAdminEmailTemplate,
  rollbackAdminCmsRevision,
  updateAdminCmsLesson,
  updateAdminEmailTemplate,
  type AdminContentReadiness,
  type AdminContentRevision,
  type AdminCmsLesson,
  type AdminCmsSummary,
  type AdminEmailTemplate
} from "@/lib/admin-cms-api";

const adminKeyStorageKey = "conversease.admin_key";
const adminNameStorageKey = "conversease.admin_name";
const statusOptions = ["draft", "review", "published", "archived"];

type Tab = "readiness" | "curriculum" | "email";

export function AdminCmsManager() {
  const [apiKey, setApiKey] = useState("");
  const [adminName, setAdminName] = useState("admin");
  const [summary, setSummary] = useState<AdminCmsSummary | null>(null);
  const [tab, setTab] = useState<Tab>("readiness");
  const [selectedLesson, setSelectedLesson] = useState<AdminCmsLesson | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<AdminEmailTemplate | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [restoringRevisionId, setRestoringRevisionId] = useState("");

  useEffect(() => {
    const storedKey = window.sessionStorage.getItem(adminKeyStorageKey);
    if (storedKey) {
      setApiKey(storedKey);
    }
    const storedName = window.sessionStorage.getItem(adminNameStorageKey);
    if (storedName) {
      setAdminName(storedName);
    }
  }, []);

  useEffect(() => {
    if (apiKey) {
      window.sessionStorage.setItem(adminKeyStorageKey, apiKey);
    }
  }, [apiKey]);

  useEffect(() => {
    if (adminName.trim()) {
      window.sessionStorage.setItem(adminNameStorageKey, adminName);
    }
  }, [adminName]);

  const validationOk = (summary?.curriculum.validationIssues.length ?? 1) === 0;

  async function loadSummary() {
    if (!apiKey) {
      setError("Masukkan admin key dulu.");
      return;
    }

    setIsLoading(true);
    setMessage("");
    setError("");

    try {
      const nextSummary = await getAdminCmsSummary(apiKey);
      setSummary(nextSummary);
      setSelectedLesson(nextSummary.curriculum.lessons[0] ?? null);
      setSelectedTemplate(nextSummary.emailTemplates[0] ?? null);
      setMessage("CMS content berhasil dimuat.");
    } catch {
      setError("CMS belum bisa dimuat. Cek admin key atau koneksi API.");
    } finally {
      setIsLoading(false);
    }
  }

  async function selectLesson(slug: string) {
    if (!apiKey) {
      return;
    }
    setError("");
    try {
      setSelectedLesson(await getAdminCmsLesson(apiKey, slug));
    } catch {
      setError("Lesson belum bisa dimuat.");
    }
  }

  async function selectTemplate(templateKey: string) {
    if (!apiKey) {
      return;
    }
    setError("");
    try {
      setSelectedTemplate(await getAdminEmailTemplate(apiKey, templateKey));
    } catch {
      setError("Email template belum bisa dimuat.");
    }
  }

  async function rollbackRevision(revision: AdminContentRevision) {
    if (!apiKey) {
      setError("Masukkan admin key dulu.");
      return;
    }

    setRestoringRevisionId(revision.id);
    setMessage("");
    setError("");

    try {
      const result = await rollbackAdminCmsRevision({
        apiKey,
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
      setError("Revision belum bisa direstore. Cek admin key, revision, atau validasi content.");
    } finally {
      setRestoringRevisionId("");
    }
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[0.32fr_0.68fr]">
      <section className="space-y-5">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-start gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-mint">
              <KeyRound className="h-5 w-5 text-leaf" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">Admin CMS</p>
              <h1 className="mt-1 text-2xl font-semibold">Content Control</h1>
              <p className="mt-2 text-sm leading-6 text-ink/60">
                Review, edit, dan validasi kurikulum serta email template sebelum rilis.
              </p>
            </div>
          </div>

          <label className="mt-5 block text-sm font-medium text-ink/70">
            Admin key
            <input
              type="password"
              value={apiKey}
              onChange={(event) => setApiKey(event.target.value)}
              className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
              placeholder="Paste admin key"
            />
          </label>

          <label className="mt-4 block text-sm font-medium text-ink/70">
            Operator
            <input
              value={adminName}
              onChange={(event) => setAdminName(event.target.value)}
              className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
              placeholder="Nama admin"
            />
          </label>

          <button
            type="button"
            onClick={loadSummary}
            disabled={!apiKey || isLoading}
            className="focus-ring mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
          >
            <RefreshCcw className="h-4 w-4" aria-hidden="true" />
            {isLoading ? "Loading" : "Load CMS"}
          </button>
        </div>

        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-2">
            <ShieldCheck className={`h-5 w-5 ${validationOk ? "text-leaf" : "text-coral"}`} aria-hidden="true" />
            <h2 className="font-semibold">Validation</h2>
          </div>
          {summary ? (
            validationOk ? (
              <p className="mt-3 rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">Curriculum validation passed.</p>
            ) : (
              <div className="mt-3 rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">
                {summary.curriculum.validationIssues.map((issue) => (
                  <p key={issue}>{issue}</p>
                ))}
              </div>
            )
          ) : (
            <p className="mt-3 text-sm leading-6 text-ink/60">Load CMS untuk melihat status validasi content.</p>
          )}
          {message ? <p className="mt-3 rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">{message}</p> : null}
          {error ? <p className="mt-3 rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">{error}</p> : null}
        </div>

        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-2">
            <Clock3 className="h-5 w-5 text-leaf" aria-hidden="true" />
            <h2 className="font-semibold">Change Log</h2>
          </div>
          {summary?.recentRevisions.length ? (
            <div className="mt-3 space-y-2">
              {summary.recentRevisions.map((revision) => (
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
                    <button
                      type="button"
                      onClick={() => rollbackRevision(revision)}
                      disabled={!apiKey || restoringRevisionId === revision.id}
                      className="focus-ring inline-flex min-h-8 items-center justify-center gap-1 rounded-lg bg-white px-2 text-xs font-semibold text-ink hover:bg-mint disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      <RotateCcw className="h-3.5 w-3.5" aria-hidden="true" />
                      {restoringRevisionId === revision.id ? "Restoring" : "Restore"}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="mt-3 text-sm leading-6 text-ink/60">Belum ada revision yang tercatat.</p>
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
          <ReadinessPanel readiness={summary?.curriculum.readiness ?? null} />
        ) : tab === "curriculum" ? (
          <CurriculumEditor
            apiKey={apiKey}
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
            apiKey={apiKey}
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
    </div>
  );
}

function ReadinessPanel({ readiness }: { readiness: AdminContentReadiness | null }) {
  if (!readiness) {
    return <p className="mt-5 rounded-lg bg-paper p-5 text-sm text-ink/60">Load CMS dulu.</p>;
  }

  const stats = [
    { label: "Planned", value: readiness.summary.plannedLessonCount },
    { label: "Implemented", value: readiness.summary.implementedLessonCount },
    { label: "Text ready", value: readiness.summary.textReadyCount },
    { label: "Audio ready", value: readiness.summary.audioReadyCount },
    { label: "Beta ready", value: readiness.summary.betaReadyCount },
    { label: "Production ready", value: readiness.summary.productionReadyCount }
  ];

  return (
    <div className="mt-5 space-y-5">
      <div className="grid gap-3 md:grid-cols-3 xl:grid-cols-6">
        {stats.map((stat) => (
          <div key={stat.label} className="rounded-lg bg-paper p-4">
            <p className="text-xs font-semibold uppercase text-ink/45">{stat.label}</p>
            <p className="mt-2 text-2xl font-semibold">{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="grid gap-4">
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
  apiKey,
  updatedBy,
  lessons,
  selectedLesson,
  onSelectLesson,
  onSaved,
  onError
}: {
  apiKey: string;
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
    if (!apiKey || !draft) {
      return;
    }

    setIsSaving(true);
    onError("");

    try {
      const saved = await updateAdminCmsLesson({
        apiKey,
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
            disabled={!apiKey || isSaving}
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
  apiKey,
  updatedBy,
  templates,
  selectedTemplate,
  onSelectTemplate,
  onSaved,
  onError
}: {
  apiKey: string;
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
    if (!apiKey || !selectedTemplate) {
      return;
    }

    setIsSaving(true);
    onError("");

    try {
      const saved = await updateAdminEmailTemplate({
        apiKey,
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
            disabled={!apiKey || isSaving}
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
