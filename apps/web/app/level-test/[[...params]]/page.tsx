import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { RealExamPanel } from "@/components/real-exam-panel";

// Only A1 has a published, graded exam today. Other levels render a
// coming-soon notice instead of an empty exam runner.
const AVAILABLE_EXAM_LEVELS = new Set(["A1"]);

export default function LevelTestPage({ params }: { params: { params?: string[] } }) {
  const segments = params.params ?? [];
  const levelCode = (segments.length > 1 ? segments[1] : segments[0] ?? "A1").toUpperCase();

  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        {AVAILABLE_EXAM_LEVELS.has(levelCode) ? (
          <RealExamPanel levelCode={levelCode} />
        ) : (
          <ExamComingSoon levelCode={levelCode} />
        )}
      </section>
    </AppShell>
  );
}

function ExamComingSoon({ levelCode }: { levelCode: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
      <p className="text-sm font-semibold uppercase tracking-wide text-emerald-700">Exam {levelCode}</p>
      <h1 className="mt-2 text-2xl font-semibold text-slate-900">Exam {levelCode} segera hadir</h1>
      <p className="mx-auto mt-3 max-w-md text-sm leading-7 text-slate-600">
        Saat ini exam resmi yang sudah tersedia adalah level A1. Level lain sedang disiapkan.
      </p>
      <Link
        href="/level-test/A1"
        className="mt-6 inline-flex items-center justify-center rounded-xl bg-emerald-600 px-4 py-3 text-sm font-semibold text-white hover:bg-emerald-700"
      >
        Buka Exam A1
      </Link>
    </div>
  );
}
