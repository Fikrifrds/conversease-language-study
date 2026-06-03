import { AppShell } from "@/components/app-shell";
import { ConversationCoachPractice } from "@/components/conversation-coach-practice";

export default function ConversationCoachPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <ConversationCoachPractice />
      </section>
    </AppShell>
  );
}
