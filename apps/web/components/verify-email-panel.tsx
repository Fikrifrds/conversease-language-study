"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { MailCheck } from "lucide-react";
import {
  getAuthSession,
  requestEmailVerification,
  saveAuthSession,
  verifyEmailToken
} from "@/lib/auth-api";

export function VerifyEmailPanel() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") ?? "";
  const [status, setStatus] = useState<"idle" | "verifying" | "success" | "error">(
    token ? "verifying" : "idle",
  );
  const [message, setMessage] = useState(token ? "Memverifikasi email..." : "");
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    if (!token) {
      return;
    }

    let ignore = false;

    async function verify() {
      try {
        const user = await verifyEmailToken(token);
        const session = getAuthSession();

        if (!ignore) {
          if (session) {
            saveAuthSession({ accessToken: session.accessToken, user });
          }
          setStatus("success");
          setMessage("Email berhasil diverifikasi.");
        }
      } catch {
        if (!ignore) {
          setStatus("error");
          setMessage("Link verifikasi tidak valid atau sudah kedaluwarsa.");
        }
      }
    }

    verify();

    return () => {
      ignore = true;
    };
  }, [token]);

  async function handleResend() {
    setIsSending(true);
    setMessage("");

    try {
      const result = await requestEmailVerification();
      setStatus(result.alreadyVerified ? "success" : "idle");
      setMessage(result.alreadyVerified ? "Email kamu sudah verified." : "Email verifikasi sudah diminta.");
    } catch {
      setStatus("error");
      setMessage("Silakan login dulu untuk meminta email verifikasi baru.");
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="mt-6 space-y-4">
      <div className="grid h-12 w-12 place-items-center rounded-lg bg-mint">
        <MailCheck className="h-6 w-6 text-leaf" aria-hidden="true" />
      </div>
      {message ? (
        <p
          className={`rounded-lg px-4 py-3 text-sm text-ink/70 ${
            status === "error" ? "bg-[#fde7df]" : "bg-mint"
          }`}
        >
          {message}
        </p>
      ) : null}
      {!token ? (
        <button
          type="button"
          onClick={handleResend}
          disabled={isSending}
          className="focus-ring inline-flex w-full items-center justify-center rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:bg-ink/30"
        >
          {isSending ? "Mengirim" : "Kirim Email Verifikasi"}
        </button>
      ) : null}
      {status === "success" ? (
        <Link className="block text-sm font-semibold text-leaf" href="/dashboard">
          Ke Dashboard
        </Link>
      ) : null}
    </div>
  );
}
