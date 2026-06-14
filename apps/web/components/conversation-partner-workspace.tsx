"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { CheckCircle2, RotateCcw } from "lucide-react";
import { ConversationPartnerChat } from "@/components/conversation-partner-chat";
import { ConversationPartnerHistory } from "@/components/conversation-partner-history";
import {
  fetchTopicProgress,
  listPartnerTopics,
  resetTopicProgress,
  type PartnerTopic,
  type TopicProgressMap
} from "@/lib/conversation-partner-api";

const levels = ["A1", "A2", "B1", "B2", "C1"];

export function ConversationPartnerWorkspace() {
  const [level, setLevel] = useState("A1");
  const [topics, setTopics] = useState<PartnerTopic[]>([]);
  const [activeTopic, setActiveTopic] = useState<PartnerTopic | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [progress, setProgress] = useState<TopicProgressMap>({});
  const [resettingKey, setResettingKey] = useState<string | null>(null);
  // Topic the learner chose to redo this session. While set, we show the fresh
  // chat instead of the completed-history view even though progress still marks
  // the topic done (progress refreshes asynchronously after the reset).
  const [replayKey, setReplayKey] = useState<string | null>(null);
  const activeSectionRef = useRef<HTMLElement | null>(null);

  const reloadProgress = useCallback(() => {
    fetchTopicProgress()
      .then(setProgress)
      .catch(() => {
        /* progress is best-effort */
      });
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError("");
    setActiveTopic(null);

    listPartnerTopics(level)
      .then((result) => {
        if (!cancelled) {
          setTopics(result);
        }
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

  useEffect(() => {
    reloadProgress();
  }, [reloadProgress]);

  useEffect(() => {
    if (!activeTopic || !activeSectionRef.current) {
      return;
    }

    const frame = window.requestAnimationFrame(() => {
      activeSectionRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    });

    return () => window.cancelAnimationFrame(frame);
  }, [activeTopic]);

  function selectTopic(topic: PartnerTopic) {
    if (topic.key !== activeTopic?.key) {
      setReplayKey(null);
    }
    setActiveTopic(topic);
  }

  async function handleReset(topicKey: string) {
    setResettingKey(topicKey);
    try {
      await resetTopicProgress(topicKey);
      if (activeTopic?.key === topicKey) {
        setActiveTopic(null);
      }
      setReplayKey((current) => (current === topicKey ? null : current));
      reloadProgress();
    } catch {
      /* ignore; keep current state */
    } finally {
      setResettingKey(null);
    }
  }

  // Redo a completed topic: clear its saved progress, then keep the topic active
  // and flag it for replay so the fresh chat renders right away.
  async function handleReplay(topicKey: string) {
    setResettingKey(topicKey);
    try {
      await resetTopicProgress(topicKey);
      setReplayKey(topicKey);
      reloadProgress();
    } catch {
      /* ignore; keep current state */
    } finally {
      setResettingKey(null);
    }
  }

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
                const topicProgress = progress[topic.key];
                const done = topicProgress?.completed ?? false;
                const inProgress = topicProgress?.hasOpenSession ?? false;
                const score = topicProgress?.bestScore ?? null;
                return (
                  <div
                    key={topic.key}
                    className={`rounded-lg border p-4 transition-colors ${
                      selected ? "border-leaf bg-mint" : "border-ink/10 bg-paper hover:bg-mint"
                    }`}
                  >
                    <button
                      type="button"
                      onClick={() => selectTopic(topic)}
                      aria-pressed={selected}
                      className="focus-ring block w-full text-left"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <p className="text-sm font-semibold">{topic.title}</p>
                        {done ? (
                          <span className="inline-flex shrink-0 items-center gap-1 text-xs font-semibold text-leaf">
                            <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" />
                            Selesai
                          </span>
                        ) : inProgress ? (
                          <span className="shrink-0 text-xs font-semibold text-coral">Berjalan</span>
                        ) : null}
                      </div>
                      <p className="mt-1 text-xs leading-5 text-ink/60">{topic.description}</p>
                      {done && score !== null ? (
                        <p className="mt-2 text-xs font-medium text-ink/70">
                          Skor terbaik: <span className="font-semibold">{score}</span>
                        </p>
                      ) : null}
                    </button>
                    {done || inProgress ? (
                      <button
                        type="button"
                        onClick={() => handleReset(topic.key)}
                        disabled={resettingKey === topic.key}
                        className="focus-ring mt-3 inline-flex items-center gap-1 text-xs font-semibold text-ink/55 hover:text-coral disabled:opacity-50"
                      >
                        <RotateCcw className="h-3.5 w-3.5" aria-hidden="true" />
                        {resettingKey === topic.key ? "Mereset…" : "Reset"}
                      </button>
                    ) : null}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </section>

      {activeTopic ? (
        (() => {
          const activeProgress = progress[activeTopic.key];
          const showHistory =
            activeProgress?.completed &&
            activeProgress.sessionId &&
            replayKey !== activeTopic.key;
          if (showHistory) {
            return (
              <section ref={activeSectionRef} id="partner-session">
                <ConversationPartnerHistory
                  key={`history-${activeTopic.key}-${activeProgress.sessionId}`}
                  topic={activeTopic}
                  sessionId={activeProgress.sessionId!}
                  onReplay={() => handleReplay(activeTopic.key)}
                  replaying={resettingKey === activeTopic.key}
                />
              </section>
            );
          }
          return (
            <section ref={activeSectionRef} id="partner-session">
              <ConversationPartnerChat
                key={`chat-${activeTopic.key}`}
                topic={activeTopic}
                resumeSessionId={
                  replayKey === activeTopic.key ? null : activeProgress?.openSessionId ?? null
                }
                onSessionEnd={reloadProgress}
              />
            </section>
          );
        })()
      ) : (
        <section className="rounded-lg border border-dashed border-ink/15 bg-paper p-8 text-center text-sm text-ink/50">
          Pilih topik di atas untuk mulai ngobrol.
        </section>
      )}
    </div>
  );
}
