"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { KeyRound } from "lucide-react";
import { resetPassword } from "@/lib/auth-api";

export function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") ?? "";
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setError("");
    setIsSubmitting(true);

    try {
      await resetPassword({ token, password });
      setMessage("Password berhasil diperbarui. Silakan masuk.");
      setPassword("");
    } catch {
      setError("Tautan reset tidak valid atau sudah kedaluwarsa.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (!token) {
    return (
      <div className="mt-6 rounded-lg bg-[#fde7df] px-4 py-3 text-sm leading-6 text-ink/70">
        Tautan reset password tidak lengkap. Minta tautan baru dari halaman lupa password.
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="mt-6 space-y-3">
      <label className="block">
        <span className="text-sm font-medium">Password baru</span>
        <input
          className="focus-ring mt-2 w-full rounded-lg border border-ink/20 bg-paper px-4 py-3"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          autoComplete="new-password"
          minLength={8}
          required
        />
      </label>
      {message ? <p className="rounded-lg bg-mint px-3 py-2 text-sm text-ink/70">{message}</p> : null}
      {error ? <p className="rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{error}</p> : null}
      <button
        type="submit"
        disabled={isSubmitting}
        className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:bg-ink/30"
      >
        <KeyRound className="h-4 w-4" aria-hidden="true" />
        {isSubmitting ? "Menyimpan…" : "Perbarui Password"}
      </button>
      {message ? (
        <Link className="block pt-2 text-sm font-semibold text-leaf" href="/login">
          Masuk
        </Link>
      ) : null}
    </form>
  );
}
