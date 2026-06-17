import Link from "next/link";
import { BookOpen, CheckCircle2, CreditCard, Languages, ShieldCheck, Sparkles } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { plans, topups } from "@/lib/data";

const packagingOptions = [
  {
    title: "English",
    status: "Future standalone",
    price: "Rp49.000/bulan",
    description: "Untuk learner yang hanya butuh English conversation track dari A1 sampai C1.",
    icon: BookOpen
  },
  {
    title: "Arabic",
    status: "Future standalone",
    price: "TBD setelah beta",
    description: "Untuk learner yang fokus Arabic formal, conversation, classroom instruction, dan reading support.",
    icon: Languages
  },
  {
    title: "All Access",
    status: "Recommended",
    price: "Current Pro",
    description: "Satu membership untuk English aktif dan Arabic beta selama fase release awal.",
    icon: Sparkles
  }
];

export default function PricingPage() {
  return (
    <AppShell>
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="grid gap-6 lg:grid-cols-[0.62fr_0.38fr] lg:items-end">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase text-leaf">Harga</p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Pilih akses belajar Conversease</h1>
            <p className="mt-3 leading-7 text-ink/70">
              Untuk release sekarang, Pro adalah All Access: English aktif dan Arabic beta berada
              dalam satu membership. Setelah Arabic stabil, paket dapat dipisah menjadi English,
              Arabic, dan All Access.
            </p>
          </div>
          <div className="rounded-lg border border-leaf/25 bg-mint p-5">
            <div className="flex items-start gap-3">
              <ShieldCheck className="mt-0.5 h-5 w-5 text-leaf" aria-hidden="true" />
              <div>
                <p className="text-sm font-semibold text-ink">Keputusan pricing saat ini</p>
                <p className="mt-2 text-sm leading-6 text-ink/65">
                  Tidak perlu paket Arabic terpisah selama beta. Ini mengurangi kompleksitas billing
                  dan memberi waktu untuk mengukur demand Arabic sebelum menetapkan harga mandiri.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {packagingOptions.map((option) => {
            const Icon = option.icon;
            return (
              <section key={option.title} className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-xs font-semibold uppercase text-leaf">{option.status}</p>
                    <h2 className="mt-1 text-xl font-semibold">{option.title}</h2>
                  </div>
                  <Icon className="h-5 w-5 text-leaf" aria-hidden="true" />
                </div>
                <p className="mt-4 text-2xl font-semibold">{option.price}</p>
                <p className="mt-3 text-sm leading-6 text-ink/60">{option.description}</p>
              </section>
            );
          })}
        </div>

        <div className="mt-8 grid gap-4 lg:grid-cols-4">
          {plans.map((plan) => (
            <section
              key={plan.key}
              className={`rounded-lg border p-5 shadow-sm ${
                plan.key === "pro_3_months" ? "border-leaf bg-mint" : "border-ink/10 bg-white"
              }`}
            >
              <h2 className="text-xl font-semibold">{plan.name}</h2>
              <p className="mt-2 text-sm leading-6 text-ink/60">{plan.description}</p>
              <p className="mt-5 text-3xl font-semibold">{plan.price}</p>
              <p className="mt-1 text-sm text-ink/60">{plan.cadence}</p>
              <p className="mt-4 rounded-lg bg-paper px-3 py-2 text-sm font-semibold">{plan.access}</p>
              <ul className="mt-5 space-y-3">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex gap-2 text-sm">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-leaf" aria-hidden="true" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              <p className="mt-5 rounded-lg border border-ink/10 bg-white/70 px-3 py-2 text-xs leading-5 text-ink/60">
                {plan.coachAllowance}.
                {plan.key === "free"
                  ? " Ini hanya untuk mencoba sesi praktik."
                  : " Membership mencakup English aktif dan Arabic beta; top-up bersifat opsional."}
              </p>
              <Link
                href="/billing"
                className="focus-ring mt-6 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf"
              >
                <CreditCard className="h-4 w-4" aria-hidden="true" />
                Pilih Paket
              </Link>
            </section>
          ))}
        </div>

        <section className="mt-8 rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <h2 className="text-xl font-semibold">Top-up opsional Conversation Coach</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-ink/60">
            Top-up tetap lintas track. Pakai untuk latihan speaking tambahan di English atau Arabic
            setelah kuota pendamping bulanannya habis.
          </p>
          <div className="mt-5 grid gap-3 md:grid-cols-3">
            {topups.map((topup) => (
              <div key={topup.key} className="rounded-lg bg-paper p-4">
                <p className="font-semibold">{topup.name}</p>
                <p className="mt-1 text-sm text-ink/60">{topup.minutes} menit latihan tambahan</p>
                <p className="mt-4 text-2xl font-semibold text-coral">{topup.price}</p>
              </div>
            ))}
          </div>
        </section>
      </section>
    </AppShell>
  );
}
