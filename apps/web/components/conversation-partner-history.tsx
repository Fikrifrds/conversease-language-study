"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, CircleDot, History, X } from "lucide-react";
import {
  fetchPartnerSessionDetail,
  listPartnerSessions,
  type PartnerSessionDetail,
  type PartnerSessionSummaryRow
} from "@/lib/conversation-partner-api";

function formatWhen(iso: string) {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return "";
  }
  return date.toLocaleDateString("id-ID", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit"
  });
}

// A refreshKey change (incremented when a session ends) re-pulls the list so a
// just-finished conversation appears without a page reload.
export function ConversationPartnerHistory({ refreshKey = 0 }: { refreshKey?: number }) {
  const [sessions, setSessions] = useState<PartnerSessionSummaryRow[] | null>(null);
  const [openId, setOpenId] = useState<string | null>(null);
  const [detail, setDetail] = useState<PartnerSessionDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    listPartnerSessions()
      .then((rows) => {
        if (!cancelled) {
          setSessions(rows);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setSessions([]);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [refreshKey]);

  async function openDetail(sessionId: string) {
    setOpenId(sessionId);
    setDetail(null);
    setDetailLoading(true);
    try {
      setDetail(await fetchPartnerSessionDetail(sessionId));
    } catch {
      setDetail(null);
    } finally {
      setDetailLoading(false);
    }
  }

  function closeDetail() {
    setOpenId(null);
    setDetail(null);
  }

  if (sessions !== null && sessions.length === 0) {
    return null;
  }

  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-2">
        <History className="h-5 w-5 text-leaf" aria-hidden="true" />
        <h2 className="text-lg font-semibold">Riwayat Latihan</h2>
      </div>

      {sessions === null ? (
        <p className="mt-3 text-sm text-ink/50">Memuat riwayat…</p>
      ) : (
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {sessions.map((session) => {
            const done = session.status === "completed";
            return (
              <button
                key={session.sessionId}
                type="button"
                onClick={() => openDetail(session.sessionId)}
                className="focus-ring rounded-lg border border-ink/10 bg-paper p-4 text-left transition hover:bg-mint"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-semibold uppercase text-coral">
                    {session.levelCode} · {session.topicTitle}
                  </span>
                  {done ? (
                    <span className="inline-flex items-center gap-1 text-xs font-semibold text-leaf">
                      <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" />
                      Selesai
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-xs font-semibold text-ink/45">
                      <CircleDot className="h-3.5 w-3.5" aria-hidden="true" />
                      Berjalan
                    </span>
                  )}
                </div>
                <div className="mt-3 flex items-end justify-between">
                  <div>
                    <p className="text-2xl font-semibold">
                      {session.overallScore !== null ? session.overallScore : "—"}
                    </p>
                    <p className="text-xs text-ink/50">Skor rata-rata</p>
                  </div>
                  <p className="text-xs text-ink/50">
                    {session.completedTurns}
                    {session.maxTurns ? `/${session.maxTurns}` : ""} turn
                  </p>
                </div>
                <p className="mt-2 text-xs text-ink/45">{formatWhen(session.updatedAt)}</p>
              </button>
            );
          })}
        </div>
      )}

      {openId ? (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-ink/40 p-4"
          role="dialog"
          aria-modal="true"
          onClick={closeDetail}
        >
          <div
            className="max-h-[85vh] w-full max-w-2xl overflow-y-auto rounded-lg bg-white p-6 shadow-lg"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-semibold uppercase text-leaf">
                  {detail ? `${detail.levelCode} · ${detail.topicTitle}` : "Riwayat"}
                </p>
                <h3 className="mt-1 text-xl font-semibold">Detail Percakapan</h3>
              </div>
              <button
                type="button"
                onClick={closeDetail}
                className="focus-ring rounded-lg p-1 text-ink/50 hover:bg-mint hover:text-ink"
                aria-label="Tutup"
              >
                <X className="h-5 w-5" aria-hidden="true" />
              </button>
            </div>

            {detailLoading ? (
              <p className="mt-4 text-sm text-ink/50">Memuat detail…</p>
            ) : detail ? (
              <>
                {detail.summary ? (
                  <div className="mt-4 rounded-lg bg-mint p-4 text-sm leading-6">
                    <p className="font-semibold">Catatan</p>
                    <p className="mt-1 text-ink/70">{detail.summary.summary}</p>
                    <p className="mt-2 text-ink/70">{detail.summary.indonesian_explanation}</p>
                    <div className="mt-3 grid grid-cols-3 gap-2 text-center">
                      {[
                        ["Speaking", detail.summary.scores.speaking],
                        ["Grammar", detail.summary.scores.grammar],
                        ["Fluency", detail.summary.scores.fluency]
                      ].map(([label, value]) => (
                        <div key={label} className="rounded-lg bg-white p-2">
                          <p className="text-lg font-semibold">{value}</p>
                          <p className="text-xs text-ink/60">{label}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <p className="mt-4 rounded-lg bg-[#fff2dc] px-3 py-2 text-sm text-ink/70">
                    Percakapan ini belum selesai, jadi belum ada skor.
                  </p>
                )}

                <div className="mt-5 space-y-3">
                  {detail.messages.map((message, index) => (
                    <div
                      key={`${message.role}-${index}`}
                      className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                      <div
                        className={`max-w-[86%] rounded-lg p-3 text-sm leading-6 ${
                          message.role === "user" ? "bg-leaf text-white" : "bg-paper text-ink"
                        }`}
                      >
                        {message.text}
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <p className="mt-4 text-sm text-ink/50">Detail tidak dapat dimuat.</p>
            )}
          </div>
        </div>
      ) : null}
    </section>
  );
}
