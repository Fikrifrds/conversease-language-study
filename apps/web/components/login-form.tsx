"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Mail } from "lucide-react";
import { GoogleAuthButton } from "@/components/google-auth-button";
import { loginUser, saveAuthSession } from "@/lib/auth-api";

function safeNextPath(defaultNextPath = "/dashboard") {
  const value = new URL(window.location.href).searchParams.get("next");

  if (value?.startsWith("/") && !value.startsWith("//")) {
    return value;
  }

  return defaultNextPath;
}

export function LoginForm({
  defaultNextPath = "/dashboard",
  onSuccess
}: {
  defaultNextPath?: string;
  onSuccess?: (nextPath: string) => void;
}) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const googleError = new URL(window.location.href).searchParams.get("google_error");
    if (googleError) {
      setError("Login Google belum berhasil. Silakan coba lagi atau gunakan email.");
    }
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const session = await loginUser({ email, password });
      saveAuthSession(session);
      const nextPath = safeNextPath(defaultNextPath);
      if (onSuccess) {
        onSuccess(nextPath);
        return;
      }
      router.replace(nextPath);
    } catch {
      setError("Email atau password belum cocok.");
      setIsSubmitting(false);
    }
  }

  return (
    <div className="mt-6 space-y-4">
      <GoogleAuthButton label="Masuk dengan Google" defaultNextPath={defaultNextPath} />
      <div className="flex items-center gap-3 text-xs font-semibold uppercase text-ink/40">
        <span className="h-px flex-1 bg-ink/10" />
        <span>Email</span>
        <span className="h-px flex-1 bg-ink/10" />
      </div>
      <form onSubmit={handleSubmit} className="space-y-3">
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
          autoComplete="current-password"
          minLength={8}
          required
        />
      </label>
      {error ? <p className="rounded-lg bg-[#fde7df] px-3 py-2 text-sm text-ink/70">{error}</p> : null}
      <div className="text-right">
        <Link className="text-sm font-semibold text-leaf" href="/forgot-password">
          Lupa password?
        </Link>
      </div>
      <button
        type="submit"
        disabled={isSubmitting}
        className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink disabled:cursor-not-allowed disabled:bg-ink/30"
      >
        <Mail className="h-4 w-4" aria-hidden="true" />
        {isSubmitting ? "Memproses…" : "Masuk"}
      </button>
      <p className="pt-2 text-sm text-ink/60">
        Belum punya akun?{" "}
        <Link className="font-semibold text-leaf" href={`/register?next=${encodeURIComponent(defaultNextPath)}`}>
          Buat akun
        </Link>
      </p>
      </form>
    </div>
  );
}
