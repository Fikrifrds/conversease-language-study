import { AppShell } from "@/components/app-shell";
import { LevelTestPanel } from "@/components/level-test-panel";

export default function LevelTestPage({ params }: { params: { level: string } }) {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <LevelTestPanel levelCode={params.level.toUpperCase()} />
      </section>
    </AppShell>
  );
}
