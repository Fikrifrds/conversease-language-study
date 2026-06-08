"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { Mail } from "lucide-react";
import { forgotPassword } from "@/lib/auth-api";

export function ForgotPasswordForm() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setError("");
    setIsSubmitting(true);

    try {
      await forgotPassword(email);
      setMessage("Jika email terdaftar, tautan reset password akan dikirim.");
    } catch {
      setError("Permintaan reset belum bisa diproses. Coba lagi sebentar.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mt-6 space-y-3">
      <label className="block">
        <span className="text-sm font-medium">Email</span>
        <input
          className="focus-ring mt-2 w-full rounded-lg border border-ink/20 bg-paper px-4 py-3"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          autoComplete="email"
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
        <Mail className="h-4 w-4" aria-hidden="true" />
        {isSubmitting ? "Mengirim…" : "Kirim Tautan Reset"}
      </button>
      <p className="pt-2 text-sm text-ink/60">
        Sudah ingat password?{" "}
        <Link className="font-semibold text-leaf" href="/login">
          Masuk
        </Link>
      </p>
    </form>
  );
}
