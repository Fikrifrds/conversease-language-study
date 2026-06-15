"use client";

import { useEffect, useMemo, useState } from "react";
import { Clock3, RotateCcw, Save } from "lucide-react";
import {
  updateAdminCmsLesson,
  updateAdminEmailTemplate,
  type AdminCmsLesson,
  type AdminContentRevision,
  type AdminEmailTemplate
} from "@/lib/admin-cms-api";
import { contentSaveErrorMessage } from "./utils";

const statusOptions = ["draft", "review", "published", "archived"];

export function ChangeLogPanel({
  revisions,
  isLoading,
  restoringRevisionId,
  onRollback
}: {
  revisions: AdminContentRevision[];
  isLoading: boolean;
  restoringRevisionId: string;
  onRollback: (revision: AdminContentRevision) => void;
}) {
  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-2">
        <Clock3 className="h-5 w-5 text-leaf" aria-hidden="true" />
        <h2 className="font-semibold">Change Log</h2>
      </div>
      {isLoading ? (
        <p className="mt-3 rounded-lg bg-paper p-4 text-sm text-ink/60">Memuat revision...</p>
      ) : revisions.length ? (
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

export function CurriculumEditor({
  updatedBy,
  lessons,
  isLoading,
  selectedLesson,
  onSelectLesson,
  onSaved,
  onError
}: {
  updatedBy: string;
  lessons: AdminCmsLesson[];
  isLoading: boolean;
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
        {isLoading ? <p className="rounded-lg bg-paper p-4 text-sm text-ink/60">Memuat lessons...</p> : null}
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
        {!isLoading && !lessons.length ? (
          <p className="rounded-lg bg-paper p-4 text-sm text-ink/60">Belum ada lesson untuk bahasa ini.</p>
        ) : null}
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
              onChange={(value) => setDraft({ ...draft, roleplay: { ...draft.roleplay, openingLine: value } })}
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

export function EmailTemplateEditor({
  updatedBy,
  templates,
  isLoading,
  selectedTemplate,
  onSelectTemplate,
  onSaved,
  onError
}: {
  updatedBy: string;
  templates: AdminEmailTemplate[];
  isLoading: boolean;
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
        {isLoading ? <p className="rounded-lg bg-paper p-4 text-sm text-ink/60">Memuat email templates...</p> : null}
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
        {!isLoading && !templates.length ? (
          <p className="rounded-lg bg-paper p-4 text-sm text-ink/60">Belum ada email template.</p>
        ) : null}
      </div>

      {selectedTemplate ? (
        <div className="grid gap-4">
          {preview ? (
            <div className="grid gap-3 rounded-lg bg-paper p-4 text-sm">
              <p>
                <span className="font-semibold">Subject:</span> {preview.subject}
              </p>
              <p>
                <span className="font-semibold">Preheader:</span> {preview.preheader}
              </p>
              <p>
                <span className="font-semibold">CTA:</span> {preview.ctaLabel}
              </p>
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
