import { AppShell } from "@/components/app-shell";
import { LevelTestCatalog } from "@/components/level-test-catalog";
import { noindexMetadata } from "@/lib/seo";

export const metadata = noindexMetadata("Exam");

export default function LevelTestsPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase text-leaf">Exam Resmi</p>
          <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Exam English</h1>
          <p className="mt-3 leading-7 text-ink/70">
            Exam resmi menilai listening, reading, grammar, speaking, dan writing dengan bobot per
            section. Saat ini exam A1 sudah tersedia; level berikutnya menyusul.
          </p>
        </div>

        <div className="mt-8">
          <LevelTestCatalog />
        </div>
      </section>
    </AppShell>
  );
}
