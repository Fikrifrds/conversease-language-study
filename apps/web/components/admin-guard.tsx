"use client";

import { useEffect, useState, type ReactNode } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LockKeyhole, ShieldCheck } from "lucide-react";
import { BrandMark } from "@/components/brand-mark";
import {
  ApiRequestError,
  clearAuthSession,
  getAuthSession,
  getCurrentUser,
  saveAuthSession,
  type AuthUser
} from "@/lib/auth-api";

type AdminState = "checking" | "authorized" | "forbidden" | "redirecting";

function currentReturnPath() {
  const path = `${window.location.pathname}${window.location.search}${window.location.hash}`;
  return path.startsWith("/") && !path.startsWith("//") ? path : "/admin/cms";
}

function loginPath(nextPath: string) {
  return `/login?next=${encodeURIComponent(nextPath)}`;
}

export function AdminGuard({ children }: { children: (user: AuthUser) => ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [state, setState] = useState<AdminState>("checking");
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    let ignore = false;
    const session = getAuthSession();
    const nextPath = currentReturnPath();

    if (!session) {
      setState("redirecting");
      router.replace(loginPath(nextPath));
      return () => {
        ignore = true;
      };
    }

    const activeSession = session;

    async function validateAdminSession() {
      try {
        const nextUser = await getCurrentUser();

        if (ignore) {
          return;
        }

        saveAuthSession({ accessToken: activeSession.accessToken, user: nextUser });
        setUser(nextUser);
        setState(nextUser.role === "admin" ? "authorized" : "forbidden");
      } catch (error) {
        if (!(error instanceof ApiRequestError) || ![401, 403].includes(error.status)) {
          return;
        }

        clearAuthSession();

        if (!ignore) {
          setState("redirecting");
          router.replace(loginPath(nextPath));
        }
      }
    }

    validateAdminSession();

    return () => {
      ignore = true;
    };
  }, [pathname, router]);

  if (state === "authorized" && user) {
    return children(user);
  }

  if (state === "forbidden") {
    return (
      <main className="grid min-h-screen bg-paper px-4 py-10 text-ink">
        <section className="m-auto w-full max-w-md rounded-lg border border-ink/10 bg-white p-6 text-center shadow-sm">
          <div className="flex justify-center">
            <BrandMark />
          </div>
          <div className="mx-auto mt-8 grid h-12 w-12 place-items-center rounded-lg bg-[#fde7df]">
            <LockKeyhole className="h-6 w-6 text-coral" aria-hidden="true" />
          </div>
          <h1 className="mt-5 text-2xl font-semibold">Akses admin belum aktif</h1>
          <p className="mt-3 text-sm leading-6 text-ink/60">
            Akun ini sudah login, tapi belum memiliki role admin Conversease.
          </p>
          <Link
            href="/dashboard"
            className="focus-ring mt-6 inline-flex h-11 items-center justify-center rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf"
          >
            Kembali ke Dashboard
          </Link>
        </section>
      </main>
    );
  }

  return (
    <main className="grid min-h-screen bg-paper px-4 py-10 text-ink">
      <section className="m-auto w-full max-w-md rounded-lg border border-ink/10 bg-white p-6 text-center shadow-sm">
        <div className="flex justify-center">
          <BrandMark />
        </div>
        <div className="mx-auto mt-8 grid h-12 w-12 place-items-center rounded-lg bg-mint">
          <ShieldCheck className="h-6 w-6 text-leaf" aria-hidden="true" />
        </div>
        <h1 className="mt-5 text-2xl font-semibold">
          {state === "redirecting" ? "Menuju login" : "Mengecek akses admin"}
        </h1>
        <p className="mt-3 text-sm leading-6 text-ink/60">
          {state === "redirecting"
            ? "Silakan login untuk melanjutkan ke admin Conversease."
            : "Sebentar, kami validasi sesi dan role akunmu."}
        </p>
      </section>
    </main>
  );
}
