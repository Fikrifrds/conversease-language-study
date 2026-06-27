"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, Home, MessageCircle, Mic, TrendingUp } from "lucide-react";
import { productRoutes } from "@conversease/shared";
import { AuthGuard } from "@/components/auth-guard";
import { BrandMark } from "@/components/brand-mark";
import { EmailVerificationNotice } from "@/components/email-verification-notice";
import { UserAccountMenu } from "@/components/user-account-menu";

// Primary learning destinations. Secondary items (A1 Test, Billing) live in the
// account dropdown to keep the bar uncluttered.
const navItems = [
  { href: productRoutes.dashboard, label: "Dashboard", shortLabel: "Dashboard", icon: Home },
  { href: productRoutes.courses, label: "Kelas", shortLabel: "Kelas", icon: BookOpen },
  { href: productRoutes.conversationCoach, label: "Coach", shortLabel: "Coach", icon: MessageCircle },
  { href: productRoutes.conversationPartner, label: "Partner", shortLabel: "Partner", icon: Mic },
  { href: productRoutes.progress, label: "Progress", shortLabel: "Progress", icon: TrendingUp }
];

type AppShellProps = {
  children: ReactNode;
  requireAuth?: boolean;
};

export function AppShell({ children, requireAuth = false }: AppShellProps) {
  const pathname = usePathname();

  function isActive(href: string) {
    if (href === productRoutes.dashboard) {
      return pathname === href;
    }
    return pathname.startsWith(href);
  }

  const shell = (
    <div className="min-h-screen bg-paper text-ink">
      <header className="sticky top-0 z-30 border-b border-ink/10 bg-paper/[0.92] shadow-[0_1px_0_rgba(28,25,23,0.03)] backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3 sm:px-6 lg:px-8">
          <BrandMark href={productRoutes.home} size="sm" />
          <nav className="hidden items-center gap-1 rounded-lg border border-ink/10 bg-white/70 p-1 shadow-sm md:flex" aria-label="Navigasi utama">
            {navItems.map((item) => {
              const active = isActive(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  aria-current={active ? "page" : undefined}
                  className={`focus-ring inline-flex h-9 items-center gap-2 rounded-lg px-3 text-sm font-semibold transition ${
                    active
                      ? "bg-mint text-ink shadow-sm"
                      : "text-ink/[0.68] hover:bg-paper hover:text-ink"
                  }`}
                >
                  <item.icon className="h-4 w-4" aria-hidden="true" />
                  {item.label}
                </Link>
              );
            })}
          </nav>
          <div className="flex items-center gap-2">
            <UserAccountMenu />
          </div>
        </div>
      </header>
      {requireAuth ? <EmailVerificationNotice /> : null}
      <main className="pb-[calc(4.5rem+env(safe-area-inset-bottom))] md:pb-0">{children}</main>
      <nav
        className="fixed inset-x-0 bottom-0 z-40 border-t border-ink/10 bg-paper/[0.96] pb-[env(safe-area-inset-bottom)] shadow-[0_-10px_35px_rgba(28,25,23,0.08)] backdrop-blur md:hidden"
        aria-label="Navigasi mobile"
      >
        <div className="grid grid-cols-5 px-1">
          {navItems.map((item) => {
            const active = isActive(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={`focus-ring my-1 flex min-h-14 flex-col items-center justify-center gap-1 rounded-lg px-1 text-[10px] font-semibold ${
                  active ? "bg-mint text-ink" : "text-ink/[0.62]"
                }`}
              >
                <item.icon className="h-4 w-4" aria-hidden="true" />
                <span className="max-w-full truncate px-1">{item.shortLabel}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );

  return requireAuth ? <AuthGuard>{shell}</AuthGuard> : shell;
}
