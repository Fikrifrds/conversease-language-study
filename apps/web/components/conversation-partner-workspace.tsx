"use client";

import { useEffect, useState } from "react";
import { ConversationPartnerChat } from "@/components/conversation-partner-chat";
import { ConversationPartnerHistory } from "@/components/conversation-partner-history";
import { listPartnerTopics, type PartnerTopic } from "@/lib/conversation-partner-api";

const levels = ["A1", "A2", "B1", "B2", "C1"];

export function ConversationPartnerWorkspace() {
  const [level, setLevel] = useState("A1");
  const [topics, setTopics] = useState<PartnerTopic[]>([]);
  const [activeTopic, setActiveTopic] = useState<PartnerTopic | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  // Bumped when a conversation ends so the history list refreshes immediately.
  const [historyKey, setHistoryKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError("");
    setActiveTopic(null);

    listPartnerTopics(level)
      .then((result) => {
        if (cancelled) {
          return;
        }
        setTopics(result);
      })
      .catch(() => {
        if (!cancelled) {
          setError("Gagal memuat topik. Coba lagi.");
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
  }, [level]);

  return (
    <div className="space-y-5">
      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <p className="text-sm font-semibold uppercase text-leaf">Conversation Partner</p>
        <h1 className="mt-2 text-2xl font-semibold">Ngobrol untuk Latihan Speaking</h1>
        <p className="mt-2 text-sm leading-6 text-ink/60">
          Pilih level dan topik. Partner akan mengajakmu ngobrol lewat suara, tetap pada topik, sampai
          tujuan tercapai. Tekan rekam dan mulai bicara.
        </p>

        <div className="mt-5">
          <p className="text-xs font-semibold uppercase text-ink/45">Level</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {levels.map((code) => {
              const selected = code === level;
              return (
                <button
                  key={code}
                  type="button"
                  onClick={() => setLevel(code)}
                  aria-pressed={selected}
                  className={`focus-ring rounded-lg border px-4 py-2 text-sm font-semibold transition-colors ${
                    selected ? "border-leaf bg-mint" : "border-ink/10 bg-paper hover:bg-mint"
                  }`}
                >
                  {code}
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-5">
          <p className="text-xs font-semibold uppercase text-ink/45">Topik</p>
          {loading ? (
            <p className="mt-3 text-sm text-ink/50">Memuat topik…</p>
          ) : error ? (
            <p className="mt-3 rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{error}</p>
          ) : topics.length === 0 ? (
            <p className="mt-3 text-sm text-ink/50">
              Belum ada topik untuk level {level}. Coba level A1 dulu.
            </p>
          ) : (
            <div className="mt-2 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {topics.map((topic) => {
                const selected = activeTopic?.key === topic.key;
                return (
                  <button
                    key={topic.key}
                    type="button"
                    onClick={() => setActiveTopic(topic)}
                    aria-pressed={selected}
                    className={`focus-ring rounded-lg border p-4 text-left transition-colors ${
                      selected ? "border-leaf bg-mint" : "border-ink/10 bg-paper hover:bg-mint"
                    }`}
                  >
                    <p className="text-sm font-semibold">{topic.title}</p>
                    <p className="mt-1 text-xs leading-5 text-ink/60">{topic.description}</p>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </section>

      {activeTopic ? (
        <ConversationPartnerChat
          key={activeTopic.key}
          topic={activeTopic}
          onSessionEnd={() => setHistoryKey((value) => value + 1)}
        />
      ) : (
        <section className="rounded-lg border border-dashed border-ink/15 bg-paper p-8 text-center text-sm text-ink/50">
          Pilih topik di atas untuk mulai ngobrol.
        </section>
      )}

      <ConversationPartnerHistory refreshKey={historyKey} />
    </div>
  );
}
