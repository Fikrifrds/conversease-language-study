"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Award,
  ChevronDown,
  CreditCard,
  LogOut,
  Settings,
  ShieldCheck,
  Sparkles,
  Timer,
  UserCircle
} from "lucide-react";
import { productRoutes } from "@conversease/shared";
import {
  ApiRequestError,
  clearAuthSession,
  getAuthSession,
  getCurrentUser,
  saveAuthSession,
  type AuthSession
} from "@/lib/auth-api";
import { getBillingAccess, type BillingAccess } from "@/lib/billing-api";

export function UserAccountMenu() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<AuthSession | null>(null);
  const [access, setAccess] = useState<BillingAccess | null>(null);
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement | null>(null);
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const firstMenuItemRef = useRef<HTMLAnchorElement | null>(null);

  useEffect(() => {
    let ignore = false;
    const storedSession = getAuthSession();

    setMounted(true);
    setSession(storedSession);

    if (!storedSession) {
      return () => {
        ignore = true;
      };
    }

    const activeSession = storedSession;

    async function refreshUser() {
      try {
        const user = await getCurrentUser();
        if (!ignore) {
          const nextSession = { accessToken: activeSession.accessToken, user };
          saveAuthSession(nextSession);
          setSession(nextSession);
        }
      } catch (error) {
        if (!(error instanceof ApiRequestError) || ![401, 403].includes(error.status)) {
          return;
        }
        clearAuthSession();
        if (!ignore) {
          setSession(null);
        }
      }
    }

    async function loadAccess() {
      try {
        const nextAccess = await getBillingAccess();
        if (!ignore) {
          setAccess(nextAccess);
        }
      } catch {
        /* billing info is best-effort */
      }
    }

    refreshUser();
    loadAccess();

    return () => {
      ignore = true;
    };
  }, []);

  useEffect(() => {
    function onClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setOpen(false);
        triggerRef.current?.focus();
      }
    }

    if (open) {
      document.addEventListener("mousedown", onClickOutside);
      document.addEventListener("keydown", onKeyDown);
    }
    return () => {
      document.removeEventListener("mousedown", onClickOutside);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open]);

  useEffect(() => {
    if (!open) {
      return;
    }
    const frame = window.requestAnimationFrame(() => {
      firstMenuItemRef.current?.focus();
    });
    return () => window.cancelAnimationFrame(frame);
  }, [open]);

  function handleLogout() {
    clearAuthSession();
    setSession(null);
    setOpen(false);
    router.replace("/login");
  }

  if (!mounted) {
    return <div className="h-10 w-28 rounded-lg bg-ink/5" aria-hidden="true" />;
  }

  if (!session) {
    return (
      <Link
        href="/login"
        className="focus-ring inline-flex h-10 items-center justify-center rounded-lg border border-ink/15 px-3 text-sm font-semibold hover:bg-mint"
      >
        Masuk
      </Link>
    );
  }

  const isAdmin = session.user.role === "admin";
  const isPro = access?.isPro ?? false;
  const minutes = access?.minutes.totalMinutes;

  return (
    <div className="flex items-center gap-1.5">
      {/* Compact minutes chip — Conversation Coach quota. */}
      <span
        className="hidden h-9 items-center gap-1 rounded-lg border border-ink/10 bg-white px-2.5 text-sm font-semibold text-ink/80 sm:inline-flex"
        title="Sisa menit Conversation Coach"
      >
        <Timer className="h-4 w-4 text-leaf" aria-hidden="true" />
        {minutes ?? "—"}
      </span>

      {/* Free users get a compact Upgrade button; Pro users don't see it. */}
      {!isPro ? (
        <Link
          href="/pricing"
          className="focus-ring inline-flex h-9 items-center gap-1 rounded-lg bg-ink px-3 text-sm font-semibold text-white hover:bg-leaf"
        >
          <Sparkles className="h-4 w-4" aria-hidden="true" />
          <span className="hidden sm:inline">Upgrade</span>
        </Link>
      ) : null}

      <div className="relative" ref={menuRef}>
        <button
          ref={triggerRef}
          type="button"
          onClick={() => setOpen((value) => !value)}
          aria-haspopup="menu"
          aria-expanded={open}
          className="focus-ring inline-flex h-9 items-center gap-1.5 rounded-lg border border-ink/15 px-2 text-sm font-semibold text-ink/80 hover:bg-mint sm:px-2.5"
        >
          <UserCircle className="h-5 w-5 shrink-0 text-leaf" aria-hidden="true" />
          <span className="hidden max-w-[110px] truncate sm:block">{session.user.name}</span>
          {isPro ? (
            <span className="rounded bg-leaf px-1.5 py-0.5 text-[10px] font-bold uppercase leading-none text-white">
              Pro
            </span>
          ) : null}
          <ChevronDown className="h-4 w-4 shrink-0 text-ink/50" aria-hidden="true" />
        </button>

        {open ? (
          <div
            role="menu"
            className="absolute right-0 z-50 mt-2 w-[min(15rem,calc(100vw-1rem))] overflow-hidden rounded-lg border border-ink/10 bg-white shadow-lg"
          >
            <div className="border-b border-ink/10 px-4 py-3">
              <p className="truncate text-sm font-semibold text-ink">{session.user.name}</p>
              <p className="truncate text-xs text-ink/55">{session.user.email}</p>
              <div className="mt-2 flex items-center gap-2">
                <span
                  className={`inline-flex items-center gap-1 rounded-lg px-2 py-0.5 text-xs font-bold ${
                    isPro ? "bg-mint text-leaf" : "bg-paper text-ink/60"
                  }`}
                >
                  {isPro ? <Sparkles className="h-3 w-3" aria-hidden="true" /> : null}
                  {isPro ? "Pro" : "Free"}
                </span>
                <span className="inline-flex items-center gap-1 text-xs text-ink/60">
                  <Timer className="h-3 w-3 text-leaf" aria-hidden="true" />
                  {minutes ?? "—"} menit
                </span>
              </div>
            </div>

            <nav className="py-1" aria-label="Akun">
              <MenuLink
                href={productRoutes.billing}
                icon={CreditCard}
                onClick={() => setOpen(false)}
                itemRef={firstMenuItemRef}
              >
                Tagihan & Paket
              </MenuLink>
              <MenuLink href={productRoutes.levelTests} icon={Award} onClick={() => setOpen(false)}>
                Level Tests
              </MenuLink>
              <MenuLink href="/settings" icon={Settings} onClick={() => setOpen(false)}>
                Pengaturan
              </MenuLink>
              {isAdmin ? (
                <MenuLink href="/admin/cms" icon={ShieldCheck} onClick={() => setOpen(false)}>
                  Admin
                </MenuLink>
              ) : null}
            </nav>

            <div className="border-t border-ink/10 py-1">
              <button
                type="button"
                onClick={handleLogout}
                role="menuitem"
                className="focus-ring flex w-full items-center gap-2 px-4 py-2.5 text-left text-sm font-medium text-ink/80 hover:bg-[#fde7df] hover:text-ink"
              >
                <LogOut className="h-4 w-4" aria-hidden="true" />
                Keluar
              </button>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}

function MenuLink({
  href,
  icon: Icon,
  onClick,
  children,
  itemRef
}: {
  href: string;
  icon: typeof CreditCard;
  onClick: () => void;
  children: React.ReactNode;
  itemRef?: React.Ref<HTMLAnchorElement>;
}) {
  return (
    <Link
      ref={itemRef}
      href={href}
      role="menuitem"
      onClick={onClick}
      className="focus-ring flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-ink/80 hover:bg-mint hover:text-ink"
    >
      <Icon className="h-4 w-4 text-ink/55" aria-hidden="true" />
      {children}
    </Link>
  );
}
