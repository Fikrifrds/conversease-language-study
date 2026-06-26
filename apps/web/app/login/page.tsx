import type { Metadata } from "next";
import { BrandMark } from "@/components/brand-mark";
import { LoginForm } from "@/components/login-form";

export const metadata: Metadata = {
  title: "Masuk",
  description: "Masuk ke akun Conversease untuk melanjutkan belajar bahasa Inggris lewat percakapan.",
  alternates: { canonical: "/login" }
};

export default function LoginPage() {
  return (
    <main className="grid min-h-screen bg-paper px-4 py-10 text-ink">
      <section className="m-auto w-full max-w-md rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
        <BrandMark />
        <h1 className="mt-8 text-3xl font-semibold">Masuk</h1>
        <LoginForm />
      </section>
    </main>
  );
}
