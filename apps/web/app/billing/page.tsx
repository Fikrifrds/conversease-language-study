import { Suspense } from "react";
import { AppShell } from "@/components/app-shell";
import { BillingManager } from "@/components/billing-manager";

export default function BillingPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <Suspense fallback={<div className="rounded-lg bg-white p-5 shadow-sm">Loading billing...</div>}>
          <BillingManager />
        </Suspense>
      </section>
    </AppShell>
  );
}
