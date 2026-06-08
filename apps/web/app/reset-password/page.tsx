import { Suspense } from "react";
import { BrandMark } from "@/components/brand-mark";
import { ResetPasswordForm } from "@/components/reset-password-form";

export default function ResetPasswordPage() {
  return (
    <main className="grid min-h-screen bg-paper px-4 py-10 text-ink">
      <section className="m-auto w-full max-w-md rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
        <BrandMark />
        <h1 className="mt-8 text-3xl font-semibold">Password baru</h1>
        <Suspense fallback={<div className="mt-6 rounded-lg bg-paper p-4 text-sm">Memuat...</div>}>
          <ResetPasswordForm />
        </Suspense>
      </section>
    </main>
  );
}
