"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, RotateCcw } from "lucide-react";
import {
  fetchPartnerSession,
  type PartnerSessionDetail,
  type PartnerTopic
} from "@/lib/conversation-partner-api";

export function ConversationPartnerHistory({
  topic,
  sessionId,
  onReplay,
  replaying
}: {
  topic: PartnerTopic;
  sessionId: string;
  onReplay: () => void;
  replaying: boolean;
}) {
  const [detail, setDetail] = useState<PartnerSessionDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError("");
    fetchPartnerSession(sessionId)
      .then((result) => {
        if (!cancelled) {
          setDetail(result);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setError("Gagal memuat riwayat percakapan. Coba lagi.");
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [sessionId]);

  const summary = detail?.summary ?? null;

  return (
    <div className="grid gap-5 lg:grid-cols-[0.72fr_0.28fr]">
      <section className="rounded-lg border border-ink/10 bg-white shadow-sm">
        <div className="border-b border-ink/10 p-5">
          <p className="text-sm font-semibold uppercase text-leaf">{topic.title}</p>
          <h2 className="mt-2 text-2xl font-semibold">Riwayat Percakapan</h2>
          <p className="mt-2 text-sm leading-6 text-ink/70">
            Kamu sudah menyelesaikan latihan ini. Berikut percakapan terakhirmu. Tekan{" "}
            <span className="font-semibold">Ulang Latihan</span> untuk mengulang dari awal.
          </p>
        </div>

        <div className="space-y-4 p-5">
          {loading ? (
            <p className="text-sm text-ink/50">Memuat riwayat…</p>
          ) : error ? (
            <p className="rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{error}</p>
          ) : (
            (detail?.messages ?? []).map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[86%] rounded-lg p-4 text-sm leading-6 ${
                    message.role === "user" ? "bg-leaf text-white" : "bg-paper text-ink"
                  }`}
                >
                  <p>{message.text}</p>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="border-t border-ink/10 p-5">
          <button
            type="button"
            onClick={onReplay}
            disabled={replaying}
            className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-leaf px-6 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:opacity-50"
          >
            <RotateCcw className="h-4 w-4" aria-hidden="true" />
            {replaying ? "Mengulang…" : "Ulang Latihan"}
          </button>
        </div>
      </section>

      <aside className="space-y-4">
        <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <h2 className="font-semibold">Ringkasan & Skor</h2>
          {summary ? (
            <div className="mt-4 space-y-4 text-sm leading-6">
              <div>
                <p className="font-semibold">Catatan</p>
                <p className="mt-1 text-ink/70">{summary.summary}</p>
              </div>
              <div>
                <p className="font-semibold">Penjelasan</p>
                <p className="mt-1 text-ink/70">{summary.indonesianExplanation}</p>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center">
                {[
                  ["Speaking", summary.scores.speaking],
                  ["Grammar", summary.scores.grammar],
                  ["Fluency", summary.scores.fluency]
                ].map(([label, value]) => (
                  <div key={label} className="rounded-lg bg-paper p-3">
                    <p className="text-lg font-semibold">{value}</p>
                    <p className="text-xs text-ink/60">{label}</p>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sm leading-6 text-ink/60">
              Ringkasan tidak tersedia untuk sesi ini.
            </p>
          )}
        </section>

        <section className="rounded-lg bg-ink p-5 text-white">
          <div className="flex items-center gap-2 text-sm font-semibold">
            <CheckCircle2 className="h-4 w-4 text-leaf" aria-hidden="true" />
            Selesai
          </div>
          <p className="mt-2 text-sm leading-6 text-white/70">
            Partner berperan sebagai {topic.partnerRole}.
          </p>
        </section>
      </aside>
    </div>
  );
}
