"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, ClipboardCheck, Loader2 } from "lucide-react";
import { CEFR_LEVELS, COURSE_LANGUAGES, levelTestRoute } from "@conversease/shared";
import { getLevelTest, listMyLevelTestAttempts, type LevelTest, type LevelTestAttempt } from "@/lib/learning-api";

type CatalogEntry = {
  language: string;
  levelCode: string;
  test: LevelTest | null;
  latestAttempt: LevelTestAttempt | null;
};

export function LevelTestCatalog() {
  const [entries, setEntries] = useState<CatalogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let ignore = false;

    async function loadCatalog() {
      setIsLoading(true);
      setError("");
      try {
        const results = await Promise.all(
          COURSE_LANGUAGES.flatMap((language) =>
            CEFR_LEVELS.map(async (levelCode): Promise<CatalogEntry | null> => {
              try {
                const test = await getLevelTest(levelCode, language);
                const attempts = await listMyLevelTestAttempts(test.attemptLevelCode);
                return {
                  language,
                  levelCode,
                  test,
                  latestAttempt: attempts[0] ?? null
                };
              } catch {
                // A missing test for a given language/level (e.g. 404) shouldn't
                // wipe out the rest of the catalog — skip just this entry.
                return null;
              }
            })
          )
        );
        const nextEntries = results.filter((entry): entry is CatalogEntry => entry !== null);
        if (!ignore) {
          setEntries(nextEntries);
        }
      } catch {
        if (!ignore) {
          setError("Daftar level test belum bisa dimuat.");
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }

    void loadCatalog();

    return () => {
      ignore = true;
    };
  }, []);

  if (isLoading) {
    return (
      <section className="rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
        <Loader2 className="h-6 w-6 animate-spin text-leaf" aria-hidden="true" />
        <p className="mt-3 text-sm text-ink/60">Memuat level test...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
        <p className="text-sm text-ink/70">{error}</p>
      </section>
    );
  }

  return (
    <div className="space-y-8">
      {COURSE_LANGUAGES.map((language) => {
        const trackEntries = entries.filter((entry) => entry.language === language);

        return (
          <section key={language}>
            <div className="mb-4 flex items-end justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase text-leaf">Track Level Test</p>
                <h2 className="mt-1 text-2xl font-semibold">{languageLabel(language)} Track</h2>
              </div>
              <p className="text-sm font-semibold text-ink/45">{trackEntries.length} level test</p>
            </div>
            <div className="grid gap-4 lg:grid-cols-2">
              {trackEntries.map((entry) => (
                <article key={`${entry.language}-${entry.levelCode}`} className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-semibold uppercase text-leaf">
                        {languageLabel(entry.language)} {entry.levelCode} Level Test
                      </p>
                      <h2 className="mt-2 break-words text-2xl font-semibold">
                        {entry.test?.title ?? `${entry.levelCode} Test`}
                      </h2>
                      <p className="mt-3 break-words text-sm leading-6 text-ink/65">
                        {entry.test?.description ?? "Level test belum tersedia."}
                      </p>
                    </div>
                    <span
                      className={`rounded-lg px-3 py-2 text-sm font-semibold ${statusClassName(entry.test?.status ?? "planned")}`}
                    >
                      {formatStatus(entry.test?.status ?? "planned")}
                    </span>
                  </div>

                  <div className="mt-5 grid gap-3 sm:grid-cols-3">
                    <Metric label="Ambang" value={entry.test ? String(entry.test.overallThreshold) : "-"} />
                    <Metric
                      label="Lesson Min"
                      value={entry.test ? `${entry.test.lessonCompletionRequiredPercent}%` : "-"}
                    />
                    <Metric
                      label="Status"
                      value={entry.latestAttempt ? formatAttemptStatus(entry.latestAttempt.status) : "Belum mulai"}
                    />
                  </div>

                  <div className="mt-5 rounded-lg bg-paper p-4 text-sm text-ink/70">
                    <div className="flex items-start gap-2">
                      <ClipboardCheck className="mt-0.5 h-4 w-4 shrink-0 text-leaf" aria-hidden="true" />
                      <div>
                        <p className="font-semibold text-ink">Alur tes</p>
                        <p className="mt-1">
                          Kerjakan tiap bagian, simpan jawaban, lalu kirim untuk dinilai.
                        </p>
                      </div>
                    </div>
                  </div>

                  <Link
                    href={levelTestRoute(entry.levelCode, entry.language)}
                    className="focus-ring mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf"
                  >
                    {entry.latestAttempt?.status === "in_progress" ? "Lanjutkan Tes" : "Buka Level Test"}
                    <ArrowRight className="h-4 w-4" aria-hidden="true" />
                  </Link>
                </article>
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-paper p-4">
      <p className="text-xs font-semibold uppercase text-ink/50">{label}</p>
      <p className="mt-2 text-xl font-semibold">{value}</p>
    </div>
  );
}

function formatAttemptStatus(status: LevelTestAttempt["status"]) {
  if (status === "in_progress") {
    return "Draft";
  }
  if (status === "submitted") {
    return "Terkirim";
  }
  return "Selesai";
}

function formatStatus(status: string) {
  if (status === "published") {
    return "Terbit";
  }
  if (status === "planned") {
    return "Draft";
  }
  return status;
}

function languageLabel(language: string) {
  return language === "arabic" ? "Arabic" : "English";
}

function statusClassName(status: string) {
  if (status === "published") {
    return "bg-mint text-leaf";
  }
  if (status === "planned") {
    return "bg-paper text-ink/75";
  }
  return "bg-paper text-ink/75";
}
