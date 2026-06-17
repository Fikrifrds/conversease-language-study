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
            <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-3 sm:px-6 md:flex-row md:items-center md:justify-between lg:px-8">
              <BrandMark href="/" size="sm" />
              <nav className="flex w-full flex-wrap items-center gap-2 overflow-x-auto md:w-auto md:justify-end">
                <Link
                  href="/admin/cms"
                  className="focus-ring inline-flex h-10 items-center justify-center whitespace-nowrap rounded-lg bg-white px-4 text-sm font-semibold hover:bg-mint"
                >
                  CMS
                </Link>
                <Link
                  href="/admin/payments"
                  className="focus-ring inline-flex h-10 items-center justify-center whitespace-nowrap rounded-lg bg-white px-4 text-sm font-semibold hover:bg-mint"
                >
                  Payments
                </Link>
                <Link
                  href="/admin/level-tests"
                  className="focus-ring inline-flex h-10 items-center justify-center whitespace-nowrap rounded-lg bg-white px-4 text-sm font-semibold hover:bg-mint"
                >
                  Level Tests
                </Link>
                <Link
                  href="/dashboard"
                  className="focus-ring inline-flex h-10 items-center justify-center whitespace-nowrap rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf"
                >
                  Dashboard
                </Link>
              </nav>
            </div>
          </header>
          <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
            <AdminUsersManager adminUser={adminUser} />
          </section>
        </main>
      )}
    </AdminGuard>
  );
}
