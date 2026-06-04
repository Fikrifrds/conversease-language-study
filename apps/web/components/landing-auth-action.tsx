"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getAuthSession, onAuthSessionChanged, type AuthSession } from "@/lib/auth-api";

const buttonClassName =
  "focus-ring rounded-lg bg-white px-4 py-2 text-sm font-semibold text-ink hover:bg-mint";

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
      {session ? "Dashboard" : "Login"}
    </Link>
  );
}
