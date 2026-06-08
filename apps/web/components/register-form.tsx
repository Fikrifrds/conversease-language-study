"use client";

import { FormEvent, useState } from "react";
import { ArrowRight } from "lucide-react";
import { GoogleAuthButton } from "@/components/google-auth-button";
import { registerUser, saveAuthSession } from "@/lib/auth-api";


export function RegisterForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const session = await registerUser({ name, email, password });
      saveAuthSession(session);
      window.location.href = "/onboarding";
    } catch {
      setError("Akun belum bisa dibuat. Cek email dan password, lalu coba lagi.");
      setIsSubmitting(false);
    }
  }

  return (
    <div className="mt-6 space-y-4">
      <GoogleAuthButton label="Daftar dengan Google" defaultNextPath="/onboarding" />
      <div className="flex items-center gap-3 text-xs font-semibold uppercase text-ink/40">
        <span className="h-px flex-1 bg-ink/10" />
        <span>Email</span>
        <span className="h-px flex-1 bg-ink/10" />
      </div>
      <form onSubmit={handleSubmit} className="space-y-3">
      <label className="block">
        <span className="text-sm font-medium">Nama</span>
        <input
          className="focus-ring mt-2 w-full rounded-lg border border-ink/20 bg-paper px-4 py-3"
          value={name}
          onChange={(event) => setName(event.target.value)}
          autoComplete="name"
          minLength={2}
          required
        />
      </label>
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
      <label className="block">
        <span className="text-sm font-medium">Password</span>
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
      {error ? <p className="rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{error}</p> : null}
      <button
        type="submit"
        disabled={isSubmitting}
        className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:bg-ink/30"
      >
        {isSubmitting ? "Membuat akun…" : "Lanjut"}
        <ArrowRight className="h-4 w-4" aria-hidden="true" />
      </button>
      </form>
    </div>
  );
}
