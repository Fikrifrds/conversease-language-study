"use client";

import Link from "next/link";
import { AdminGuard } from "@/components/admin-guard";
import { AdminLevelTestReviewManager } from "@/components/admin-level-test-review-manager";
import { BrandMark } from "@/components/brand-mark";

export default function AdminLevelTestsPage() {
  return (
    <AdminGuard>
      {(adminUser) => (
        <main className="min-h-screen bg-paper text-ink">
          <header className="border-b border-ink/10 bg-paper/90 backdrop-blur">
            <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
              <BrandMark href="/" size="sm" />
              <nav className="flex items-center gap-2">
                <Link
                  href="/admin/cms"
                  className="focus-ring inline-flex h-10 items-center justify-center rounded-lg bg-white px-4 text-sm font-semibold hover:bg-mint"
                >
                  CMS
                </Link>
                <Link
                  href="/admin/payments"
                  className="focus-ring inline-flex h-10 items-center justify-center rounded-lg bg-white px-4 text-sm font-semibold hover:bg-mint"
                >
                  Payments
                </Link>
                <Link
                  href="/admin/users"
                  className="focus-ring inline-flex h-10 items-center justify-center rounded-lg bg-white px-4 text-sm font-semibold hover:bg-mint"
                >
                  Users
                </Link>
                <Link
                  href="/level-tests"
                  className="focus-ring inline-flex h-10 items-center justify-center rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf"
                >
                  Level Tests
                </Link>
              </nav>
            </div>
          </header>
          <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
            <AdminLevelTestReviewManager adminUser={adminUser} />
          </section>
        </main>
      )}
    </AdminGuard>
  );
}
