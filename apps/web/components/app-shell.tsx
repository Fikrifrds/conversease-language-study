import type { ReactNode } from "react";
import Link from "next/link";
import { Award, BookOpen, CreditCard, Home, MessageCircle, TrendingUp } from "lucide-react";
import { productRoutes } from "@conversease/shared";
import { AuthGuard } from "@/components/auth-guard";
import { BrandMark } from "@/components/brand-mark";
import { EmailVerificationNotice } from "@/components/email-verification-notice";
import { UserAccountMenu } from "@/components/user-account-menu";

const navItems = [
  { href: productRoutes.dashboard, label: "Dashboard", icon: Home },
  { href: productRoutes.courses, label: "Courses", icon: BookOpen },
  { href: productRoutes.conversationCoach, label: "Conversation Coach", icon: MessageCircle },
  { href: productRoutes.progress, label: "Progress", icon: TrendingUp },
  { href: productRoutes.levelTestA1, label: "A1 Test", icon: Award },
  { href: productRoutes.billing, label: "Billing", icon: CreditCard }
];

type AppShellProps = {
  children: ReactNode;
  requireAuth?: boolean;
};

export function AppShell({ children, requireAuth = false }: AppShellProps) {
  const shell = (
    <div className="min-h-screen bg-paper text-ink">
      <header className="sticky top-0 z-30 border-b border-ink/10 bg-paper/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
          <BrandMark href={productRoutes.home} size="sm" />
          <nav className="hidden items-center gap-1 md:flex" aria-label="Primary">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="focus-ring inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-ink/75 hover:bg-mint hover:text-ink"
              >
                <item.icon className="h-4 w-4" aria-hidden="true" />
                {item.label}
              </Link>
            ))}
          </nav>
          <div className="flex items-center gap-2">
            <Link
              href="/pricing"
              className="focus-ring hidden h-10 items-center justify-center rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf sm:inline-flex"
            >
              Upgrade
            </Link>
            <UserAccountMenu />
          </div>
        </div>
      </header>
      {requireAuth ? <EmailVerificationNotice /> : null}
      <main>{children}</main>
      <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-ink/10 bg-paper md:hidden" aria-label="Mobile">
        <div className="grid grid-cols-6">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="focus-ring flex min-h-14 flex-col items-center justify-center gap-1 text-[11px] font-medium text-ink/70"
            >
              <item.icon className="h-4 w-4" aria-hidden="true" />
              <span className="max-w-full truncate px-1">{item.label}</span>
            </Link>
          ))}
        </div>
      </nav>
    </div>
  );

  return requireAuth ? <AuthGuard>{shell}</AuthGuard> : shell;
}
