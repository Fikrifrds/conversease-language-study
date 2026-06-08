"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { MailCheck } from "lucide-react";
import {
  getAuthSession,
  getCurrentUser,
  requestEmailVerification,
  saveAuthSession,
  type AuthUser
} from "@/lib/auth-api";

export function EmailVerificationNotice() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    let ignore = false;
    const session = getAuthSession();

    if (session?.user) {
      setUser(session.user);
    }

    async function refresh() {
      try {
        const nextUser = await getCurrentUser();

        if (!ignore && session) {
          saveAuthSession({ accessToken: session.accessToken, user: nextUser });
          setUser(nextUser);
        }
      } catch {
        // AuthGuard handles invalid sessions.
      }
    }

    refresh();

    return () => {
      ignore = true;
    };
  }, []);

  if (!user || user.emailVerifiedAt) {
    return null;
  }

  async function handleResend() {
    setIsSending(true);
    setMessage("");

    try {
      const result = await requestEmailVerification();
      setMessage(result.delivery?.sent ? "Email verifikasi sudah dikirim." : "Permintaan verifikasi tersimpan.");
    } catch {
      setMessage("Email verifikasi belum bisa dikirim.");
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="border-b border-leaf/20 bg-mint">
      <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-3 text-sm text-ink/75 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
        <div className="flex items-start gap-2">
          <MailCheck className="mt-0.5 h-4 w-4 text-leaf" aria-hidden="true" />
          <p>
            Email <span className="font-semibold">{user.email}</span> belum diverifikasi.
            {message ? <span className="ml-1">{message}</span> : null}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleResend}
            disabled={isSending}
            className="focus-ring rounded-md bg-ink px-3 py-2 text-xs font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSending ? "Mengirim…" : "Kirim Ulang"}
          </button>
          <Link href="/verify-email" className="font-semibold text-coral">
            Verifikasi
          </Link>
        </div>
      </div>
    </div>
  );
}
