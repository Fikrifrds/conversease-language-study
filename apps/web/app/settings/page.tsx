import { Bell, ShieldCheck } from "lucide-react";
import { AppShell } from "@/components/app-shell";

export default function SettingsPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-4xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <p className="text-sm font-semibold uppercase text-leaf">Settings</p>
        <h1 className="mt-2 text-3xl font-semibold">Account preferences</h1>
        <div className="mt-8 space-y-5">
          <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <Bell className="h-5 w-5 text-leaf" aria-hidden="true" />
                <h2 className="text-lg font-semibold">Notifications</h2>
              </div>
              <span className="rounded-lg bg-[#fff2dc] px-3 py-1 text-xs font-semibold text-ink/70">
                Segera hadir
              </span>
            </div>
            <p className="mt-3 text-sm leading-6 text-ink/60">
              Pengaturan notifikasi belum bisa diubah. Untuk sekarang, email penting (verifikasi,
              billing, reminder) tetap aktif secara default.
            </p>
            <div className="mt-5 space-y-3">
              {["Learning reminders", "Weekly progress", "Subscription reminders", "Evaluation reminders"].map((item) => (
                <label key={item} className="flex cursor-not-allowed items-center justify-between rounded-lg bg-paper p-4 opacity-60">
                  <span className="font-medium">{item}</span>
                  <input className="h-5 w-5 accent-leaf" type="checkbox" defaultChecked disabled />
                </label>
              ))}
            </div>
          </section>
          <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-leaf" aria-hidden="true" />
              <h2 className="text-lg font-semibold">Security emails</h2>
            </div>
            <p className="mt-3 text-sm leading-6 text-ink/60">
              Verification, password reset, billing, and security messages stay enabled.
            </p>
          </section>
        </div>
      </section>
    </AppShell>
  );
}
