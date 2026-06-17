import Link from "next/link";
import { CheckCircle2, CreditCard } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { plans, topups } from "@/lib/data";

export default function PricingPage() {
  return (
    <AppShell>
      <section className="mx-auto max-w-6xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase text-leaf">Harga</p>
          <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Pilih paket yang paling pas</h1>
          <p className="mt-3 leading-7 text-ink/70">
            Saat ini semua paket Pro sudah termasuk English aktif dan Arabic beta dalam satu akses.
          </p>
        </div>

        <div className="mt-5 inline-flex rounded-lg border border-leaf/20 bg-mint px-4 py-3 text-sm text-ink/70">
          Free untuk coba dulu. Pro untuk akses penuh dan latihan rutin.
        </div>

        <div className="mt-8 grid gap-4 lg:grid-cols-4">
          {plans.map((plan) => (
            <section
              key={plan.key}
              className={`rounded-lg border p-5 shadow-sm ${
                plan.key === "pro_3_months" ? "border-leaf bg-mint" : "border-ink/10 bg-white"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <h2 className="text-xl font-semibold">{plan.name}</h2>
                {plan.key === "pro_3_months" ? (
                  <span className="rounded-full bg-white px-2.5 py-1 text-xs font-semibold text-leaf">
                    Best value
                  </span>
                ) : null}
              </div>
              <p className="mt-4 text-3xl font-semibold">{plan.price}</p>
              <p className="mt-1 text-sm text-ink/60">{plan.cadence}</p>
              <p className="mt-4 rounded-lg bg-paper px-3 py-2 text-sm font-semibold">{plan.access}</p>
              <ul className="mt-5 space-y-2.5">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex gap-2 text-sm">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-leaf" aria-hidden="true" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              <p className="mt-5 text-xs leading-5 text-ink/60">{plan.coachAllowance}</p>
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
          <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <h2 className="text-xl font-semibold">Top-up opsional</h2>
              <p className="mt-1 text-sm text-ink/60">
                Tambahan menit latihan jika kuota bulanan habis.
              </p>
            </div>
            <p className="text-sm text-ink/55">Bisa dipakai untuk English atau Arabic.</p>
          </div>
          <div className="mt-5 grid gap-3 md:grid-cols-3">
            {topups.map((topup) => (
              <div key={topup.key} className="rounded-lg bg-paper p-4">
                <p className="font-semibold">{topup.name}</p>
                <p className="mt-1 text-sm text-ink/60">{topup.minutes} menit tambahan</p>
                <p className="mt-3 text-2xl font-semibold text-coral">{topup.price}</p>
              </div>
            ))}
          </div>
        </section>
      </section>
    </AppShell>
  );
}
