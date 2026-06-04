"use client";

import Link from "next/link";
import { AdminGuard } from "@/components/admin-guard";
import { AdminUsersManager } from "@/components/admin-users-manager";
import { BrandMark } from "@/components/brand-mark";

export default function AdminUsersPage() {
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
                  href="/admin/level-tests"
                  className="focus-ring inline-flex h-10 items-center justify-center rounded-lg bg-white px-4 text-sm font-semibold hover:bg-mint"
                >
                  Level Tests
                </Link>
                <Link
                  href="/dashboard"
                  className="focus-ring inline-flex h-10 items-center justify-center rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf"
                >
                  Dashboard
                </Link>
              </nav>
            </div>
          </header>
          <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
            <AdminUsersManager adminUser={adminUser} />
          </section>
        </main>
      )}
    </AdminGuard>
  );
}
