"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getAuthSession, onAuthSessionChanged, type AuthSession } from "@/lib/auth-api";

const buttonClassName =
  "focus-ring inline-flex min-h-11 items-center justify-center rounded-full bg-ink px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-leaf";

export function LandingAuthAction() {
  const [session, setSession] = useState<AuthSession | null>(null);

  useEffect(() => {
    function syncSession() {
      setSession(getAuthSession());
    }

    syncSession();
    return onAuthSessionChanged(syncSession);
  }, []);

  return (
    <Link href={session ? "/dashboard" : "/login"} className={buttonClassName}>
      {session ? "Dashboard" : "Masuk"}
    </Link>
  );
}
