import { AppShell } from "@/components/app-shell";
import { RealExamPanel } from "@/components/real-exam-panel";

export default function LevelTestPage({ params }: { params: { level: string } }) {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <RealExamPanel levelCode={params.level.toUpperCase()} />
      </section>
    </AppShell>
  );
}
