import { AppShell } from "@/components/app-shell";
import { ConversationCoachWorkspace } from "@/components/conversation-coach-workspace";
import { StudyDayMarker } from "@/components/study-day-marker";

export default function ConversationCoachPage() {
  return (
    <AppShell requireAuth>
      <StudyDayMarker />
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <ConversationCoachWorkspace />
      </section>
    </AppShell>
  );
}
