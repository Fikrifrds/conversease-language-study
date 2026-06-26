"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, Clock, Loader2, ShieldCheck } from "lucide-react";
import { CEFR_LEVELS } from "@conversease/shared";
import { listExamTemplatesByLevel, type ExamTemplateSummary } from "@/lib/learning-api";

// Only A1 has a published, graded exam today. The rest render as coming-soon.
const AVAILABLE_EXAM_LEVELS = new Set(["A1"]);

export function LevelTestCatalog() {
  const [templatesByLevel, setTemplatesByLevel] = useState<Record<string, ExamTemplateSummary | null>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let ignore = false;

    async function loadCatalog() {
      setIsLoading(true);
      setError("");
      try {
        const entries = await Promise.all(
          CEFR_LEVELS.filter((level) => AVAILABLE_EXAM_LEVELS.has(level)).map(async (level) => {
            const templates = await listExamTemplatesByLevel(level);
            const active = templates.find((template) => template.status === "active") ?? templates[0] ?? null;
            return [level, active] as const;
          })
        );
        if (!ignore) {
          setTemplatesByLevel(Object.fromEntries(entries));
        }
      } catch {
        if (!ignore) {
          setError("Daftar exam belum bisa dimuat.");
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
        <p className="mt-3 text-sm text-ink/60">Memuat exam...</p>
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
    <div className="grid gap-4 lg:grid-cols-2">
      {CEFR_LEVELS.map((level) => {
        const template = templatesByLevel[level] ?? null;
        const isAvailable = AVAILABLE_EXAM_LEVELS.has(level) && template !== null;

        if (!isAvailable) {
          return <ComingSoonCard key={level} level={level} />;
        }

        return (
          <article key={level} className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0 flex-1">
                <p className="text-sm font-semibold uppercase text-leaf">English {level} Exam Resmi</p>
                <h2 className="mt-2 break-words text-2xl font-semibold">{template!.title}</h2>
                <p className="mt-3 break-words text-sm leading-6 text-ink/65">
                  {template!.description ?? "Exam resmi untuk level ini."}
                </p>
              </div>
              <span className="rounded-lg bg-mint px-3 py-2 text-sm font-semibold text-leaf">Tersedia</span>
            </div>

            <div className="mt-5 grid gap-3 sm:grid-cols-2">
              <Metric label="Durasi" value={`${template!.durationMinutes} menit`} />
              <Metric label="Nilai lulus" value={`${template!.passingScorePercent}%`} />
            </div>

            <div className="mt-5 rounded-lg bg-paper p-4 text-sm text-ink/70">
              <div className="flex items-start gap-2">
                <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-leaf" aria-hidden="true" />
                <div>
                  <p className="font-semibold text-ink">Exam berbobot</p>
                  <p className="mt-1">
                    Listening, reading, grammar, speaking, dan writing dinilai otomatis dan oleh penilai.
                  </p>
                </div>
              </div>
            </div>

            <Link
              href={`/level-test/${level}`}
              className="focus-ring mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf"
            >
              Buka Exam
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </article>
        );
      })}
    </div>
  );
}

function ComingSoonCard({ level }: { level: string }) {
  return (
    <article className="rounded-lg border border-dashed border-ink/15 bg-paper p-6 text-center shadow-sm">
      <div className="mx-auto grid h-12 w-12 place-items-center rounded-lg bg-white">
        <Clock className="h-6 w-6 text-ink/50" aria-hidden="true" />
      </div>
      <span className="mt-4 inline-block rounded-lg bg-white px-3 py-1 text-xs font-semibold uppercase text-ink/60">
        Coming Soon
      </span>
      <h3 className="mt-3 text-xl font-semibold">English {level} Exam</h3>
      <p className="mx-auto mt-2 max-w-sm text-sm leading-6 text-ink/60">
        Exam resmi level {level} sedang disiapkan. Saat ini exam A1 sudah bisa kamu kerjakan.
      </p>
    </article>
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
