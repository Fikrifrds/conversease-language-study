"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Loader2 } from "lucide-react";
import { consumeGoogleLoginToken, saveAuthSession } from "@/lib/auth-api";

function safeNextPath(value: string | null) {
  if (value?.startsWith("/") && !value.startsWith("//")) {
    return value;
  }

  return "/dashboard";
}

export function GoogleCallbackPanel() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState("");

  useEffect(() => {
    let ignore = false;
    const token = searchParams.get("token");
    const nextPath = safeNextPath(searchParams.get("next"));

    async function finishLogin() {
      if (!token) {
        setError("Token login Google tidak ditemukan.");
        return;
      }

      try {
        const session = await consumeGoogleLoginToken(token);
        if (!ignore) {
          saveAuthSession(session);
          router.replace(nextPath);
        }
      } catch {
        if (!ignore) {
          setError("Login Google belum berhasil. Silakan coba lagi.");
        }
      }
    }

    finishLogin();

    return () => {
      ignore = true;
    };
  }, [router, searchParams]);

  if (error) {
    return (
      <div>
        <h1 className="text-2xl font-semibold">Login Google belum berhasil</h1>
        <p className="mt-3 text-sm leading-6 text-ink/60">{error}</p>
        <Link
          href="/login"
          className="focus-ring mt-5 inline-flex w-full items-center justify-center rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink"
        >
          Kembali ke Login
        </Link>
      </div>
    );
  }

  return (
    <div className="text-center">
      <div className="mx-auto grid h-12 w-12 place-items-center rounded-lg bg-mint">
        <Loader2 className="h-6 w-6 animate-spin text-leaf" aria-hidden="true" />
      </div>
      <h1 className="mt-5 text-2xl font-semibold">Menyelesaikan login</h1>
      <p className="mt-3 text-sm leading-6 text-ink/60">Sebentar, sesi belajarmu sedang disiapkan.</p>
    </div>
  );
}
