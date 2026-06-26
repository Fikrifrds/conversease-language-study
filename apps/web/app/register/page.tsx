import type { Metadata } from "next";
import { BrandMark } from "@/components/brand-mark";
import { RegisterForm } from "@/components/register-form";

export const metadata: Metadata = {
  title: "Daftar Gratis",
  description:
    "Daftar gratis di Conversease dan mulai belajar bahasa Inggris lewat percakapan nyata, dari level A1 sampai C1.",
  alternates: { canonical: "/register" }
};

export default function RegisterPage() {
  return (
    <main className="grid min-h-screen bg-paper px-4 py-10 text-ink">
      <section className="m-auto w-full max-w-md rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
        <BrandMark />
        <h1 className="mt-8 text-3xl font-semibold">Buat akun</h1>
        <RegisterForm />
      </section>
    </main>
  );
}
