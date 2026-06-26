import { AppShell } from "@/components/app-shell";
import { ConversationPartnerWorkspace } from "@/components/conversation-partner-workspace";
import { noindexMetadata } from "@/lib/seo";

export const metadata = noindexMetadata("Conversation Partner");

export default function ConversationPartnerPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        <ConversationPartnerWorkspace />
      </section>
    </AppShell>
  );
}
