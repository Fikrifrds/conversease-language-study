import { Suspense } from "react";
import { AppShell } from "@/components/app-shell";
import { BillingManager } from "@/components/billing-manager";
import { noindexMetadata } from "@/lib/seo";

export const metadata = noindexMetadata("Tagihan");

export default function BillingPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        <Suspense fallback={<div className="rounded-lg bg-white p-5 shadow-sm">Memuat tagihan...</div>}>
          <BillingManager />
        </Suspense>
      </section>
    </AppShell>
  );
}
