import { AppShell } from "@/components/app-shell";
import { ConversationCoachWorkspace } from "@/components/conversation-coach-workspace";
import { StudyDayMarker } from "@/components/study-day-marker";
import { noindexMetadata } from "@/lib/seo";

export const metadata = noindexMetadata("Conversation Coach");

export default function ConversationCoachPage() {
  return (
    <AppShell requireAuth>
      <StudyDayMarker />
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        <ConversationCoachWorkspace />
      </section>
    </AppShell>
  );
}
