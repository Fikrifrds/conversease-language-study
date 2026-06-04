"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { LogOut, ShieldCheck, UserCircle } from "lucide-react";
import {
  ApiRequestError,
  clearAuthSession,
  getAuthSession,
  getCurrentUser,
  saveAuthSession,
  type AuthSession
} from "@/lib/auth-api";

export function UserAccountMenu() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<AuthSession | null>(null);

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

    refreshUser();

    return () => {
      ignore = true;
    };
  }, []);

  function handleLogout() {
    clearAuthSession();
    setSession(null);
    router.replace("/login");
  }

  if (!mounted) {
    return <div className="h-10 w-20 rounded-lg bg-ink/5" aria-hidden="true" />;
  }

  if (!session) {
    return (
      <Link
        href="/login"
        className="focus-ring inline-flex h-10 items-center justify-center rounded-lg border border-ink/15 px-3 text-sm font-semibold hover:bg-mint"
      >
        Login
      </Link>
    );
  }

  return (
    <div className="flex items-center gap-2">
      {session.user.role === "admin" ? (
        <Link
          href="/admin/cms"
          className="focus-ring inline-flex h-10 w-10 items-center justify-center rounded-lg border border-ink/15 text-leaf hover:bg-mint"
          title="Admin"
          aria-label="Admin"
        >
          <ShieldCheck className="h-4 w-4" aria-hidden="true" />
        </Link>
      ) : null}
      <Link
        href="/settings"
        className="focus-ring inline-flex h-10 w-10 items-center justify-center gap-2 rounded-lg border border-ink/15 text-sm font-semibold text-ink/80 hover:bg-mint sm:w-auto sm:max-w-[180px] sm:justify-start sm:px-3"
        title={session.user.name}
      >
        <UserCircle className="h-4 w-4 shrink-0 text-leaf" aria-hidden="true" />
        <span className="hidden truncate sm:block">{session.user.name}</span>
      </Link>
      <button
        type="button"
        onClick={handleLogout}
        className="focus-ring inline-flex h-10 w-10 items-center justify-center rounded-lg border border-ink/15 text-ink/70 hover:bg-[#fde7df] hover:text-ink"
        title="Logout"
        aria-label="Logout"
      >
        <LogOut className="h-4 w-4" aria-hidden="true" />
      </button>
    </div>
  );
}
