import { BrandMark } from "@/components/brand-mark";
import { ForgotPasswordForm } from "@/components/forgot-password-form";

export default function ForgotPasswordPage() {
  return (
    <main className="grid min-h-screen bg-paper px-4 py-10 text-ink">
      <section className="m-auto w-full max-w-md rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
        <BrandMark />
        <h1 className="mt-8 text-3xl font-semibold">Reset password</h1>
        <p className="mt-3 text-sm leading-6 text-ink/60">
          Masukkan email akun untuk menerima tautan reset password.
        </p>
        <ForgotPasswordForm />
      </section>
    </main>
  );
}
