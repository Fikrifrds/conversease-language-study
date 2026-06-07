import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { ReviewWorkspace } from "@/components/review-workspace";

export default function ReviewPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-leaf">Review</p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Review Hari Ini</h1>
            <p className="mt-3 max-w-3xl text-base leading-7 text-ink/70">
              Ulangi pattern dan phrase penting dari lesson yang sudah kamu kerjakan supaya makin cepat dan bisa dipakai di konteks lain.
            </p>
          </div>
          <Link
            href="/dashboard"
            className="focus-ring inline-flex items-center justify-center rounded-lg border border-ink/20 bg-white px-4 py-3 text-sm font-semibold hover:bg-mint"
          >
            Kembali ke Dashboard
          </Link>
        </div>

        <ReviewWorkspace />
      </section>
    </AppShell>
  );
}

