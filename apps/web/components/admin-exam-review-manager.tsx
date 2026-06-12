"use client";

import { useEffect, useState } from "react";
import { ClipboardCheck, Mic, PenLine, RefreshCcw, Save } from "lucide-react";
import {
  listExamReviewQueue,
  scoreExamReviewEntry,
  type ExamReviewQueueEntry
} from "@/lib/admin-exam-api";
import type { AuthUser } from "@/lib/auth-api";

const statusOptions = [
  { label: "Pending", value: "pending" },
  { label: "Completed", value: "completed" }
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

function isPlayableAudioUrl(value: string | null): value is string {
  return Boolean(value && (value.startsWith("http://") || value.startsWith("https://")));
}

export function AdminExamReviewManager({ adminUser }: { adminUser: AuthUser }) {
  const [status, setStatus] = useState("pending");
  const [entries, setEntries] = useState<ExamReviewQueueEntry[]>([]);
  const [selectedEntry, setSelectedEntry] = useState<ExamReviewQueueEntry | null>(null);
  const [scorePoints, setScorePoints] = useState(0);
  const [notes, setNotes] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    void loadEntries();
    // Refresh when the status filter changes.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [status]);

  useEffect(() => {
    setScorePoints(0);
    setNotes("");
  }, [selectedEntry?.id]);

  async function loadEntries() {
    setIsLoading(true);
    setError("");
    try {
      const data = await listExamReviewQueue(status);
      setEntries(data);
      setSelectedEntry((current) =>
        current ? data.find((entry) => entry.id === current.id) ?? null : null
      );
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "Failed to load review queue.");
    } finally {
      setIsLoading(false);
    }
  }

  async function submitScore() {
    if (!selectedEntry) {
      return;
    }
    setIsSaving(true);
    setMessage("");
    setError("");
    try {
      const result = await scoreExamReviewEntry({
        queueId: selectedEntry.id,
        scorePoints,
        notes: notes.trim() || undefined
      });
      setMessage(
        result.status === "published"
          ? `Score saved. Result published: ${Math.round(result.scorePercent)}% (${result.passed ? "passed" : "not passed"}).`
          : `Score saved. Result still pending other reviews.`
      );
      setSelectedEntry(null);
      await loadEntries();
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : "Failed to save score.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="flex items-center gap-2 text-2xl font-bold">
            <ClipboardCheck className="h-6 w-6 text-leaf" />
            Exam Review Queue
          </h1>
          <p className="mt-1 text-sm text-ink/60">
            Score speaking and writing answers from real exam attempts. Reviewer: {adminUser.name || adminUser.email}
          </p>
        </div>
        <div className="flex items-end gap-2">
          <label className="block text-sm">
            <span className="mb-1 block font-semibold">Status</span>
            <select
              value={status}
              onChange={(event) => {
                setSelectedEntry(null);
                setStatus(event.target.value);
              }}
              className="focus-ring h-10 rounded-lg border border-ink/15 bg-white px-3"
            >
              {statusOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            onClick={() => void loadEntries()}
            disabled={isLoading}
            className="focus-ring inline-flex h-10 items-center gap-2 rounded-lg bg-white px-4 text-sm font-semibold hover:bg-mint disabled:opacity-60"
          >
            <RefreshCcw className="h-4 w-4" />
            Refresh
          </button>
        </div>
      </div>

      {message ? <p className="rounded-lg bg-mint px-4 py-3 text-sm font-semibold text-leaf">{message}</p> : null}
      {error ? <p className="rounded-lg bg-[#ffe9e6] px-4 py-3 text-sm font-semibold text-[#b3361f]">{error}</p> : null}

      <div className="grid gap-6 lg:grid-cols-[1fr_1.2fr]">
        <section className="rounded-2xl border border-ink/10 bg-white p-4">
          <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-ink/60">
            {status === "pending" ? "Waiting for review" : "Reviewed"} ({entries.length})
          </h2>
          {isLoading ? <p className="px-2 py-6 text-sm text-ink/60">Loading queue...</p> : null}
          {!isLoading && entries.length === 0 ? (
            <p className="px-2 py-6 text-sm text-ink/60">No items in this queue.</p>
          ) : null}
          <ul className="space-y-2">
            {entries.map((entry) => (
              <li key={entry.id}>
                <button
                  type="button"
                  onClick={() => setSelectedEntry(entry)}
                  className={`focus-ring w-full rounded-xl border px-4 py-3 text-left text-sm ${
                    selectedEntry?.id === entry.id
                      ? "border-leaf bg-mint"
                      : "border-ink/10 bg-paper hover:border-leaf/40"
                  }`}
                >
                  <span className="flex items-center gap-2 font-semibold">
                    {entry.itemType === "audio_response" ? (
                      <Mic className="h-4 w-4 text-leaf" />
                    ) : (
                      <PenLine className="h-4 w-4 text-leaf" />
                    )}
                    {entry.itemType === "audio_response" ? "Speaking" : "Writing"}
                    <span className="ml-auto text-xs font-normal text-ink/50">{formatDate(entry.createdAt)}</span>
                  </span>
                  <span className="mt-1 block truncate text-ink/70">{entry.promptText}</span>
                  <span className="mt-1 block text-xs text-ink/50">
                    Session {entry.sessionId.slice(0, 8)}... · max {entry.scorePointsMax} pts
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </section>

        <section className="rounded-2xl border border-ink/10 bg-white p-5">
          {!selectedEntry ? (
            <p className="py-10 text-center text-sm text-ink/60">Select an item from the queue to review it.</p>
          ) : (
            <div className="space-y-5">
              <div>
                <h2 className="text-lg font-bold">
                  {selectedEntry.itemType === "audio_response" ? "Speaking answer" : "Writing answer"}
                </h2>
                <p className="mt-1 whitespace-pre-wrap rounded-xl bg-paper px-4 py-3 text-sm">{selectedEntry.promptText}</p>
              </div>

              <div>
                <h3 className="text-sm font-bold uppercase tracking-wide text-ink/60">Learner response</h3>
                {isPlayableAudioUrl(selectedEntry.fileUrl) ? (
                  <audio controls src={selectedEntry.fileUrl} className="mt-2 w-full" />
                ) : null}
                {selectedEntry.itemType === "audio_response" && !isPlayableAudioUrl(selectedEntry.fileUrl) ? (
                  <p className="mt-2 rounded-lg bg-[#fff7e0] px-3 py-2 text-xs text-[#8a6d1a]">
                    Audio recording is not available on the server for this answer
                    {selectedEntry.audioDurationSeconds
                      ? ` (recorded ${Math.round(selectedEntry.audioDurationSeconds)}s locally)`
                      : ""}
                    . Review the typed answer below.
                  </p>
                ) : null}
                <p className="mt-2 min-h-[3rem] whitespace-pre-wrap rounded-xl border border-ink/10 px-4 py-3 text-sm">
                  {selectedEntry.textResponse?.trim() || "(no text answer)"}
                </p>
              </div>

              {selectedEntry.rubricCriteria ? (
                <div>
                  <h3 className="text-sm font-bold uppercase tracking-wide text-ink/60">Rubric</h3>
                  <ul className="mt-2 space-y-1 text-sm">
                    {Object.entries(selectedEntry.rubricCriteria).map(([key, rubric]) => (
                      <li key={key} className="flex gap-2">
                        <span className="font-semibold capitalize">{key.replace(/_/g, " ")}</span>
                        <span className="text-ink/50">({Math.round(rubric.weight * 100)}%)</span>
                        <span className="text-ink/70">— {rubric.criteria}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {selectedEntry.status === "pending" ? (
                <div className="space-y-3 rounded-xl bg-paper p-4">
                  <label className="block text-sm">
                    <span className="mb-1 block font-semibold">
                      Score (0 - {selectedEntry.scorePointsMax} points)
                    </span>
                    <input
                      type="number"
                      min={0}
                      max={selectedEntry.scorePointsMax}
                      value={scorePoints}
                      onChange={(event) =>
                        setScorePoints(
                          Math.max(0, Math.min(selectedEntry.scorePointsMax, Number(event.target.value) || 0))
                        )
                      }
                      className="focus-ring h-10 w-32 rounded-lg border border-ink/15 bg-white px-3"
                    />
                  </label>
                  <label className="block text-sm">
                    <span className="mb-1 block font-semibold">Notes (optional)</span>
                    <textarea
                      value={notes}
                      onChange={(event) => setNotes(event.target.value)}
                      rows={3}
                      className="focus-ring w-full rounded-lg border border-ink/15 bg-white px-3 py-2"
                      placeholder="Feedback for audit trail"
                    />
                  </label>
                  <button
                    type="button"
                    onClick={() => void submitScore()}
                    disabled={isSaving}
                    className="focus-ring inline-flex h-11 items-center gap-2 rounded-xl bg-ink px-5 text-sm font-semibold text-white hover:bg-leaf disabled:opacity-60"
                  >
                    <Save className="h-4 w-4" />
                    {isSaving ? "Saving..." : "Save score"}
                  </button>
                </div>
              ) : (
                <p className="rounded-lg bg-mint px-4 py-3 text-sm font-semibold text-leaf">
                  This answer has already been reviewed.
                </p>
              )}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
