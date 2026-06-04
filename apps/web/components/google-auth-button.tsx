"use client";

import { useEffect, useState } from "react";
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

function GoogleLogo({ className = "h-5 w-5" }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path
        fill="#4285F4"
        d="M23.49 12.27c0-.82-.07-1.42-.22-2.04H12.24v3.95h6.48c-.13.98-.84 2.45-2.42 3.44l-.02.13 3.51 2.45.24.02c2.2-1.83 3.46-4.53 3.46-7.95Z"
      />
      <path
        fill="#34A853"
        d="M12.24 22.62c3.15 0 5.8-.94 7.73-2.56l-3.68-2.63c-.99.62-2.31 1.05-4.05 1.05a7.02 7.02 0 0 1-6.65-4.35l-.14.01-3.65 2.55-.05.12a11.72 11.72 0 0 0 10.49 5.81Z"
      />
      <path
        fill="#FBBC05"
        d="M5.59 14.13a6.53 6.53 0 0 1-.37-2.13c0-.74.13-1.46.35-2.13v-.14L1.87 7.13l-.12.05A10.08 10.08 0 0 0 .6 12c0 1.75.42 3.4 1.15 4.82l3.84-2.69Z"
      />
      <path
        fill="#EA4335"
        d="M12.24 5.52c2.19 0 3.66.86 4.5 1.58l3.3-2.91C18.01 2.44 15.39 1.38 12.24 1.38A11.72 11.72 0 0 0 1.75 7.18l3.82 2.69a7.08 7.08 0 0 1 6.67-4.35Z"
      />
    </svg>
  );
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
        className="focus-ring inline-flex w-full items-center justify-center gap-3 rounded-lg border border-ink/15 bg-white px-4 py-3 text-sm font-semibold text-ink shadow-[0_1px_1px_rgba(17,16,14,0.04)] transition hover:border-ink/25 hover:bg-[#f8fafc]"
        href={googleLoginUrl(currentNextPath(defaultNextPath))}
      >
        <GoogleLogo />
        {label}
      </a>
    );
  }

  return (
    <button
      type="button"
      disabled
      className="inline-flex w-full cursor-not-allowed items-center justify-center gap-3 rounded-lg border border-ink/10 bg-paper px-4 py-3 text-sm font-semibold text-ink/45"
    >
      <GoogleLogo className="h-5 w-5 opacity-50 grayscale" />
      {isLoading ? "Menyiapkan Google" : label}
    </button>
  );
}
