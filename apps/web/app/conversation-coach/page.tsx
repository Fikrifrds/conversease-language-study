import { AppShell } from "@/components/app-shell";
import { ConversationCoachWorkspace } from "@/components/conversation-coach-workspace";

export default function ConversationCoachPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <ConversationCoachWorkspace />
      </section>
    </AppShell>
  );
}
