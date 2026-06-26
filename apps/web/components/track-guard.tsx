"use client";

import { useEffect, useState, type ReactNode } from "react";
import Link from "next/link";
import { Clock, Loader2 } from "lucide-react";
import { isLanguageVisible } from "@conversease/shared";
import { getAuthSession } from "@/lib/auth-api";

// Blocks direct access to a coming-soon track's pages (e.g. Arabic course or
// lesson) for non-admins, even via a direct URL. Admins see the content.
export function TrackGuard({ language, children }: { language: string; children: ReactNode }) {
  const [state, setState] = useState<"checking" | "allowed" | "blocked">("checking");

  useEffect(() => {
    const isAdmin = getAuthSession()?.user.role === "admin";
    setState(isLanguageVisible(language, isAdmin) ? "allowed" : "blocked");
  }, [language]);

  if (state === "checking") {
    return (
      <section className="mx-auto flex max-w-7xl items-center gap-3 px-4 py-16 text-ink/60 sm:px-6 lg:px-8">
        <Loader2 className="h-5 w-5 animate-spin text-leaf" aria-hidden="true" />
        Memuat...
      </section>
    );
  }

  if (state === "blocked") {
    return (
      <section className="mx-auto max-w-2xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="rounded-lg border border-dashed border-ink/15 bg-paper p-8 text-center shadow-sm">
          <div className="mx-auto grid h-12 w-12 place-items-center rounded-lg bg-white">
            <Clock className="h-6 w-6 text-ink/50" aria-hidden="true" />
          </div>
          <span className="mt-4 inline-block rounded-lg bg-white px-3 py-1 text-xs font-semibold uppercase text-ink/60">
            Coming Soon
          </span>
          <h1 className="mt-3 text-2xl font-semibold">Track ini segera hadir</h1>
          <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-ink/60">
            Materi ini sedang disiapkan. Untuk sekarang, fokuslah pada English track yang sudah siap.
          </p>
          <Link
            href="/courses"
            className="focus-ring mt-6 inline-flex h-11 items-center justify-center rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf"
          >
            Kembali ke Kurikulum
          </Link>
        </div>
      </section>
    );
  }

  return <>{children}</>;
}
