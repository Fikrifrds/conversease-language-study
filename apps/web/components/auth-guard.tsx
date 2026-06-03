"use client";

import { useEffect, useState, type ReactNode } from "react";
import { usePathname, useRouter } from "next/navigation";
import { ShieldCheck } from "lucide-react";
import { BrandMark } from "@/components/brand-mark";
import { clearAuthSession, getAuthSession, getCurrentUser, saveAuthSession } from "@/lib/auth-api";

type AuthState = "checking" | "authenticated" | "redirecting";

function currentReturnPath() {
  const path = `${window.location.pathname}${window.location.search}${window.location.hash}`;
  return path.startsWith("/") && !path.startsWith("//") ? path : "/dashboard";
}

function loginPath(nextPath: string) {
  return `/login?next=${encodeURIComponent(nextPath)}`;
}

export function AuthGuard({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [authState, setAuthState] = useState<AuthState>("checking");

  useEffect(() => {
    let ignore = false;
    const session = getAuthSession();
    const nextPath = currentReturnPath();

    if (!session) {
      setAuthState("redirecting");
      router.replace(loginPath(nextPath));
      return () => {
        ignore = true;
      };
    }

    const activeSession = session;
    setAuthState("authenticated");

    async function validateSession() {
      try {
        const user = await getCurrentUser();

        if (!ignore) {
          saveAuthSession({ accessToken: activeSession.accessToken, user });
          setAuthState("authenticated");
        }
      } catch {
        clearAuthSession();

        if (!ignore) {
          setAuthState("redirecting");
          router.replace(loginPath(nextPath));
        }
      }
    }

    validateSession();

    return () => {
      ignore = true;
    };
  }, [pathname, router]);

  if (authState === "authenticated") {
    return children;
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
          {authState === "redirecting" ? "Menuju login" : "Menyiapkan ruang belajar"}
        </h1>
        <p className="mt-3 text-sm leading-6 text-ink/60">
          {authState === "redirecting"
            ? "Silakan login untuk melanjutkan sesi Conversease."
            : "Sebentar, kami mengecek sesi akunmu."}
        </p>
      </section>
    </main>
  );
}
