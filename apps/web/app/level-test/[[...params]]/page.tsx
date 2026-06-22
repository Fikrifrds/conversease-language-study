import { AppShell } from "@/components/app-shell";
import { LevelTestPanel } from "@/components/level-test-panel";

export default function LevelTestPage({ params }: { params: { params?: string[] } }) {
  const segments = params.params ?? [];
  const language = segments.length > 1 ? segments[0].toLowerCase() : "english";
  const levelCode = (segments.length > 1 ? segments[1] : segments[0] ?? "A1").toUpperCase();

  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        <LevelTestPanel language={language} levelCode={levelCode} />
      </section>
    </AppShell>
  );
}
