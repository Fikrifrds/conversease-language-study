import { AppShell } from "@/components/app-shell";
import { LevelTestCatalog } from "@/components/level-test-catalog";
import { noindexMetadata } from "@/lib/seo";

export const metadata = noindexMetadata("Level Tests");

export default function LevelTestsPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase text-leaf">Level Tests</p>
          <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Pilih track dan level test</h1>
          <p className="mt-3 leading-7 text-ink/70">
            English dan Arabic kini punya flow lengkap dari A1 sampai C1: mulai tes, isi jawaban per
            section, simpan draft, lalu kirim untuk dinilai.
          </p>
        </div>

        <div className="mt-8">
          <LevelTestCatalog />
        </div>
      </section>
    </AppShell>
  );
}
