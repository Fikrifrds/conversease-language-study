"use client";

import { useEffect, useState } from "react";
import { Chrome } from "lucide-react";
import { getGoogleAuthStatus, googleLoginUrl } from "@/lib/auth-api";

function currentNextPath(defaultNextPath: string) {
  if (typeof window === "undefined") {
    return defaultNextPath;
  }

  const requested = new URL(window.location.href).searchParams.get("next");
  if (requested?.startsWith("/") && !requested.startsWith("//")) {
    return requested;
  }

  return defaultNextPath;
}

export function GoogleAuthButton({
  label,
  defaultNextPath = "/dashboard"
}: {
  label: string;
  defaultNextPath?: string;
}) {
  const [enabled, setEnabled] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let ignore = false;

    async function loadStatus() {
      try {
        const status = await getGoogleAuthStatus();
        if (!ignore) {
          setEnabled(status.enabled);
        }
      } catch {
        if (!ignore) {
          setEnabled(false);
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }

    loadStatus();

    return () => {
      ignore = true;
    };
  }, []);

  if (enabled) {
    return (
      <a
        className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-lg border border-ink/15 bg-white px-4 py-3 text-sm font-semibold hover:bg-mint"
        href={googleLoginUrl(currentNextPath(defaultNextPath))}
      >
        <Chrome className="h-4 w-4" aria-hidden="true" />
        {label}
      </a>
    );
  }

  return (
    <button
      type="button"
      disabled
      className="inline-flex w-full cursor-not-allowed items-center justify-center gap-2 rounded-lg border border-ink/10 bg-paper px-4 py-3 text-sm font-semibold text-ink/45"
    >
      <Chrome className="h-4 w-4" aria-hidden="true" />
      {isLoading ? "Menyiapkan Google" : label}
    </button>
  );
}
