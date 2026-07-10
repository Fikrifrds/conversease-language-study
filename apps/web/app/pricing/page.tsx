"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import {
  CheckCircle2,
  Clipboard,
  CreditCard,
  LogIn,
  ReceiptText,
  ShieldCheck,
  Sparkles,
  Star,
  Zap
} from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { Modal } from "@/components/modal";
import { getAuthSession } from "@/lib/auth-api";
import {
  bankLogo,
  confirmManualTransfer,
  createCheckout,
  orderBankAccounts,
  type PaymentKind,
  type PaymentOrder
} from "@/lib/billing-api";
import { plans } from "@/lib/data";
import { trackEvent } from "@/lib/analytics";

type CheckoutItem = {
  key: string;
  name: string;
  price: string;
  cadence: string;
  access: string;
  paymentKind: PaymentKind;
};

const MONTHLY_BASE_IDR = 49_000;

function formatRupiah(value: number) {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0
  })
    .format(value)
    .replace(/\s/g, "");
}

function formatDateTime(value: string | null) {
  if (!value) {
    return "-";
  }

  return new Intl.DateTimeFormat("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }).format(new Date(value));
}

function todayInputValue() {
  return new Date().toISOString().slice(0, 10);
}

function statusLabel(status: string) {
  if (status === "pending") {
    return "Menunggu transfer";
  }
  if (status === "confirmed") {
    return "Menunggu approval admin";
  }
  if (status === "success") {
    return "Disetujui";
  }
  if (status === "failed") {
    return "Ditolak";
  }
  if (status === "expired") {
    return "Kedaluwarsa";
  }
  return status;
}

function monthlyPriceIdr(priceIdr: number, months: number) {
  if (months <= 0) {
    return 0;
  }
  return Math.round(priceIdr / months);
}

function savingsPercent(priceIdr: number, months: number) {
  if (months <= 1) {
    return 0;
  }
  const full = MONTHLY_BASE_IDR * months;
  return Math.max(0, Math.round(((full - priceIdr) / full) * 100));
}

export default function PricingPage() {
  const [selectedItem, setSelectedItem] = useState<CheckoutItem | null>(null);
  const [checkoutOrder, setCheckoutOrder] = useState<PaymentOrder | null>(null);
  const [activePackage, setActivePackage] = useState<string | null>(null);
  const [transferDate, setTransferDate] = useState(todayInputValue);
  const [targetBank, setTargetBank] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [authPrompt, setAuthPrompt] = useState(false);

  async function handleChoose(item: CheckoutItem) {
    setSelectedItem(item);
    setCheckoutOrder(null);
    setTargetBank("");
    setMessage("");
    setError("");

    const session = getAuthSession();
    if (!session) {
      setAuthPrompt(true);
      return;
    }

    setAuthPrompt(false);
    setActivePackage(item.key);

    try {
      trackEvent("begin_checkout", { package_key: item.key, payment_kind: item.paymentKind });
      const order = await createCheckout({ packageKey: item.key, paymentKind: item.paymentKind });
      setCheckoutOrder(order);
      setMessage("Transfer nominal tepat agar pembayaran mudah dicocokkan.");
    } catch {
      setError("Instruksi transfer belum bisa dibuat. Coba ulang sebentar.");
    } finally {
      setActivePackage(null);
    }
  }

  async function handleConfirmTransfer() {
    if (!checkoutOrder) {
      return;
    }

    setActivePackage(checkoutOrder.packageKey);
    setMessage("");
    setError("");

    try {
      const result = await confirmManualTransfer({
        orderId: checkoutOrder.id,
        transferDate,
        targetBank
      });
      setCheckoutOrder(result.order);
      trackEvent("purchase_pending", { package_key: checkoutOrder.packageKey });
      setMessage("Konfirmasi terkirim. Admin akan mengecek transfer dan mengaktifkan akses.");
    } catch {
      setError("Konfirmasi belum bisa dikirim. Pastikan bank tujuan dan tanggal transfer sudah dipilih.");
    } finally {
      setActivePackage(null);
    }
  }

  async function handleCopy(value: string) {
    try {
      await navigator.clipboard.writeText(value.replace(/\s/g, ""));
      setMessage("Nomor rekening disalin.");
    } catch {
      setError("Nomor rekening belum bisa disalin otomatis.");
    }
  }

  function closeModal() {
    setSelectedItem(null);
    setCheckoutOrder(null);
    setAuthPrompt(false);
    setTargetBank("");
    setMessage("");
    setError("");
  }

  const proPlans = plans.filter((plan) => plan.key.startsWith("pro_"));
  const checkoutItems: CheckoutItem[] = proPlans.map((plan) => ({
    key: plan.key,
    name: plan.name,
    price: plan.price,
    cadence: plan.cadence,
    access: plan.access,
    paymentKind: "subscription"
  }));

  return (
    <AppShell>
      <section className="relative overflow-hidden">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 -z-10"
          style={{
            background:
              "radial-gradient(ellipse 70% 50% at 50% -10%, rgba(249,115,22,0.16), transparent 55%), radial-gradient(ellipse 40% 40% at 90% 20%, rgba(250,204,21,0.12), transparent 50%), radial-gradient(ellipse 35% 35% at 8% 60%, rgba(249,115,22,0.08), transparent 45%)"
          }}
        />

        <div className="mx-auto max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
          <div className="mx-auto max-w-2xl text-center">
            <span className="inline-flex items-center gap-1.5 rounded-full border border-leaf/25 bg-white/80 px-3.5 py-1.5 text-xs font-semibold uppercase tracking-wider text-leaf shadow-sm backdrop-blur">
              <Sparkles className="h-3.5 w-3.5" aria-hidden="true" />
              Pro All Access
            </span>
            <h1 className="mt-5 text-3xl font-semibold tracking-tight text-ink sm:text-5xl sm:leading-[1.1]">
              Buka English A1–C1.
              <span className="mt-1 block bg-gradient-to-r from-leaf to-coral bg-clip-text text-transparent">
                Satu paket, akses penuh.
              </span>
            </h1>
            <p className="mx-auto mt-4 max-w-lg text-base leading-7 text-ink/65 sm:text-lg">
              Feedback percakapan detail, exam resmi tiap level, dan Conversation Coach — pilih durasi yang cocok untuk ritme belajarmu.
            </p>
          </div>

          <div className="mx-auto mt-8 flex flex-wrap items-center justify-center gap-2 sm:gap-3">
            {[
              { icon: Zap, label: "Aktif cepat setelah diverifikasi" },
              { icon: Star, label: "Track lengkap A1–C1" },
              { icon: Sparkles, label: "Feedback percakapan detail" }
            ].map(({ icon: Icon, label }) => (
              <div
                key={label}
                className="inline-flex items-center gap-2 rounded-full border border-ink/8 bg-white/70 px-3.5 py-2 text-xs font-medium text-ink/70 shadow-sm backdrop-blur sm:text-sm"
              >
                <Icon className="h-3.5 w-3.5 text-leaf" aria-hidden="true" />
                {label}
              </div>
            ))}
          </div>

          <div className="mt-12 grid items-stretch gap-5 pt-2 md:grid-cols-3 md:gap-4 lg:gap-6">
            {proPlans.map((plan, index) => {
              const item = checkoutItems[index];
              const preparing = activePackage === item.key;
              const highlighted = plan.key === "pro_3_months";
              const monthly = monthlyPriceIdr(plan.priceIdr, plan.months);
              const savePct = savingsPercent(plan.priceIdr, plan.months);

              return (
                <section
                  key={plan.key}
                  className={`relative flex flex-col rounded-3xl transition duration-300 ${
                    highlighted
                      ? "z-10 border-2 border-leaf bg-white shadow-soft md:-mt-3 md:mb-[-0.75rem] md:scale-[1.03]"
                      : "border border-ink/10 bg-white/90 shadow-sm hover:-translate-y-1 hover:border-leaf/30 hover:shadow-soft"
                  }`}
                >
                  {highlighted ? (
                    <div className="absolute inset-x-0 top-0 h-1 rounded-t-3xl bg-gradient-to-r from-leaf via-sun to-leaf" aria-hidden="true" />
                  ) : null}

                  <div
                    className={`px-6 pb-5 pt-6 text-center ${
                      highlighted ? "rounded-t-[1.35rem] bg-gradient-to-b from-mint via-mint/80 to-white" : "rounded-t-3xl bg-gradient-to-b from-paper to-white"
                    }`}
                  >
                    {plan.badge ? (
                      <span
                        className={`mb-3 inline-flex items-center gap-1 rounded-full px-3.5 py-1 text-[0.7rem] font-bold uppercase tracking-wide ${
                          highlighted ? "bg-ink text-white" : "bg-sun text-ink"
                        }`}
                      >
                        {highlighted ? <Star className="h-3 w-3 fill-sun text-sun" aria-hidden="true" /> : null}
                        {plan.badge}
                      </span>
                    ) : (
                      <span className="mb-3 inline-flex h-6 items-center text-[0.7rem] opacity-0" aria-hidden="true">
                        —
                      </span>
                    )}

                    <p className="text-sm font-medium text-ink/50">{plan.cadence}</p>
                    <h2 className="mt-1 text-xl font-semibold tracking-tight">{plan.name}</h2>

                    <div className="mt-5">
                      <p className="text-[2.35rem] font-semibold leading-none tracking-tight text-ink sm:text-4xl">
                        {plan.price}
                      </p>
                      <p className="mt-2 text-sm text-ink/55">
                        {plan.months > 1 ? (
                          <>
                            ≈ <span className="font-semibold text-ink/75">{formatRupiah(monthly)}</span>
                            <span className="text-ink/45"> / bulan</span>
                          </>
                        ) : (
                          <>untuk {plan.cadence}</>
                        )}
                      </p>
                    </div>

                    {savePct > 0 ? (
                      <p className="mt-3 inline-flex rounded-full bg-leaf/10 px-3 py-1 text-xs font-semibold text-coral">
                        Hemat {savePct}% vs bulanan
                      </p>
                    ) : (
                      <p className="mt-3 text-xs font-medium text-ink/40">Fleksibel, bayar per bulan</p>
                    )}
                  </div>

                  <div className="flex flex-1 flex-col px-6 pb-6 pt-2">
                    <ul className="space-y-3">
                      {plan.features.map((feature) => (
                        <li key={feature} className="flex gap-2.5 text-sm leading-snug text-ink/80">
                          <CheckCircle2
                            className={`mt-0.5 h-5 w-5 shrink-0 ${highlighted ? "text-leaf" : "text-leaf/80"}`}
                            aria-hidden="true"
                          />
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>

                    <p className="mt-5 text-xs leading-5 text-ink/50">{plan.coachAllowance}</p>

                    <button
                      type="button"
                      onClick={() => handleChoose(item)}
                      disabled={preparing}
                      className={`focus-ring mt-auto inline-flex w-full items-center justify-center gap-2 rounded-2xl px-4 py-3.5 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-60 ${
                        highlighted
                          ? "bg-leaf text-white shadow-md shadow-leaf/25 hover:bg-coral"
                          : "bg-ink text-white hover:bg-leaf"
                      }`}
                    >
                      <CreditCard className="h-4 w-4" aria-hidden="true" />
                      {preparing ? "Menyiapkan..." : highlighted ? "Mulai sekarang" : "Pilih paket"}
                    </button>
                  </div>
                </section>
              );
            })}
          </div>

          <p className="mt-10 text-center text-sm text-ink/55">
            Belum siap upgrade?{" "}
            <Link href="/register" className="font-semibold text-leaf underline-offset-2 hover:underline">
              Mulai gratis dulu
            </Link>
          </p>
        </div>
      </section>

      {selectedItem ? (
        <CheckoutModal
          item={selectedItem}
          order={checkoutOrder}
          authPrompt={authPrompt}
          transferDate={transferDate}
          targetBank={targetBank}
          message={message}
          error={error}
          isSubmitting={activePackage === selectedItem.key}
          onClose={closeModal}
          onCopy={handleCopy}
          onTransferDateChange={setTransferDate}
          onTargetBankChange={setTargetBank}
          onConfirm={handleConfirmTransfer}
        />
      ) : null}
    </AppShell>
  );
}

function CheckoutModal({
  item,
  order,
  authPrompt,
  transferDate,
  targetBank,
  message,
  error,
  isSubmitting,
  onClose,
  onCopy,
  onTransferDateChange,
  onTargetBankChange,
  onConfirm
}: {
  item: CheckoutItem;
  order: PaymentOrder | null;
  authPrompt: boolean;
  transferDate: string;
  targetBank: string;
  message: string;
  error: string;
  isSubmitting: boolean;
  onClose: () => void;
  onCopy: (value: string) => void;
  onTransferDateChange: (value: string) => void;
  onTargetBankChange: (value: string) => void;
  onConfirm: () => void;
}) {
  const canConfirm = order?.status === "pending";
  const bankAccounts = order ? orderBankAccounts(order) : [];
  const recordedBank = order ? String(order.metadata["bank_name"] ?? "") : "";
  const activeBank = canConfirm ? targetBank : recordedBank;
  const selectedAccount = bankAccounts.find((account) => account.bankName === activeBank) ?? null;

  return (
    <Modal
      eyebrow="Checkout"
      title={item.name}
      description={`${item.access} / ${item.cadence}`}
      size="lg"
      closeLabel="Tutup checkout"
      onClose={onClose}
    >
      {authPrompt ? (
        <div className="mt-5 rounded-lg border border-leaf/20 bg-mint p-5">
          <LogIn className="h-6 w-6 text-leaf" aria-hidden="true" />
          <h3 className="mt-3 text-lg font-semibold">Login dulu untuk membuat instruksi transfer</h3>
          <p className="mt-2 text-sm leading-6 text-ink/70">
            Setelah login, kembali ke pricing dan pilih paket ini lagi. Order akan terhubung ke akunmu.
          </p>
          <div className="mt-5 flex flex-col gap-2 sm:flex-row">
            <Link
              href="/login"
              className="focus-ring inline-flex min-h-11 items-center justify-center rounded-lg bg-ink px-4 py-2 text-sm font-semibold text-white hover:bg-leaf"
            >
              Login
            </Link>
            <Link
              href="/register"
              className="focus-ring inline-flex min-h-11 items-center justify-center rounded-lg border border-ink/15 bg-white px-4 py-2 text-sm font-semibold text-ink hover:bg-paper"
            >
              Buat akun
            </Link>
          </div>
        </div>
      ) : null}

      {!authPrompt && !order && !error ? (
        <div className="mt-5 rounded-lg bg-paper p-5 text-sm font-semibold text-ink/60">Menyiapkan instruksi transfer...</div>
      ) : null}

      {order ? (
        <div className="mt-5 space-y-4">
          <div className="rounded-lg border border-leaf/20 bg-mint p-4">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-ink/70">Transfer tepat sampai 3 digit terakhir</p>
                <p className="mt-2 text-3xl font-semibold text-[#1f3f91]">{formatRupiah(order.amountIdr)}</p>
                <p className="mt-1 text-sm text-[#2563eb]">
                  Harga {formatRupiah(order.baseAmountIdr ?? order.amountIdr)} + kode{" "}
                  {String(order.uniqueCode ?? "").padStart(3, "0")}
                </p>
              </div>
              <span className="rounded-lg bg-white px-3 py-2 text-sm font-semibold text-coral">
                {statusLabel(order.status)}
              </span>
            </div>
            {order.expiresAt ? (
              <p className="mt-3 text-sm text-ink/65">Konfirmasi sebelum {formatDateTime(order.expiresAt)}</p>
            ) : null}
          </div>

          <div className="space-y-3">
            {canConfirm ? (
              <>
                <p className="text-sm font-medium text-ink/70">
                  {bankAccounts.length > 1 ? "1. Pilih bank tujuan transfer" : "Bank tujuan transfer"}
                </p>
                <div className="grid gap-2.5 sm:grid-cols-2">
                  {bankAccounts.map((account) => {
                    const logo = bankLogo(account.bankName);
                    const selected = account.bankName === targetBank;
                    return (
                      <button
                        key={`${account.bankName}-${account.accountNumber}`}
                        type="button"
                        onClick={() => onTargetBankChange(account.bankName)}
                        aria-pressed={selected}
                        className={`focus-ring flex items-center justify-between gap-3 rounded-xl border p-4 text-left transition ${
                          selected
                            ? "border-leaf bg-mint ring-1 ring-leaf"
                            : "border-ink/10 bg-white hover:border-leaf/40"
                        }`}
                      >
                        <div>
                          <p className="text-xs uppercase tracking-wide text-ink/45">Bank tujuan</p>
                          <p className="mt-1 text-base font-semibold">{account.bankName}</p>
                        </div>
                        {logo ? (
                          <Image src={logo.src} alt={account.bankName} width={logo.width} height={logo.height} className="h-6 w-auto" />
                        ) : null}
                      </button>
                    );
                  })}
                </div>
              </>
            ) : null}

            {selectedAccount ? (
              <div className="rounded-xl border border-leaf/25 bg-white p-4">
                <p className="text-sm text-ink/55">
                  Transfer ke rekening <span className="font-semibold text-ink">{selectedAccount.bankName}</span> berikut:
                </p>
                <div className="mt-3 flex items-center gap-3 rounded-lg bg-paper px-4 py-3">
                  <p className="flex-1 text-center font-mono text-xl tracking-wide">{selectedAccount.accountNumber}</p>
                  <button
                    type="button"
                    onClick={() => onCopy(selectedAccount.accountNumber)}
                    className="focus-ring rounded-md p-2 text-ink/60 hover:bg-white hover:text-ink"
                    aria-label={`Salin nomor rekening ${selectedAccount.bankName}`}
                    title="Salin nomor rekening"
                  >
                    <Clipboard className="h-4 w-4" aria-hidden="true" />
                  </button>
                </div>
                <p className="mt-3 text-center text-sm text-ink/60">a.n. {selectedAccount.accountHolder}</p>
              </div>
            ) : canConfirm ? (
              <p className="rounded-lg bg-paper px-4 py-3 text-sm text-ink/55">
                Pilih bank tujuan di atas untuk melihat nomor rekening.
              </p>
            ) : null}
          </div>

          {canConfirm ? (
            <div className="space-y-3">
              <label className="block text-sm font-medium text-ink/70">
                2. Tanggal transfer
                <input
                  type="date"
                  value={transferDate}
                  onChange={(event) => onTransferDateChange(event.target.value)}
                  className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
                />
              </label>
              <button
                type="button"
                onClick={onConfirm}
                disabled={isSubmitting || !targetBank || !transferDate}
                className="focus-ring flex min-h-12 w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
              >
                <ReceiptText className="h-4 w-4" aria-hidden="true" />
                {isSubmitting ? "Mengirim konfirmasi..." : "Saya Sudah Transfer"}
              </button>
            </div>
          ) : (
            <div className="flex items-start gap-3 rounded-lg bg-paper p-4">
              <ShieldCheck className="mt-0.5 h-5 w-5 text-leaf" aria-hidden="true" />
              <p className="text-sm leading-6 text-ink/65">
                Konfirmasi sudah masuk. Admin akan mencocokkan nominal unik dan approve akses.
              </p>
            </div>
          )}
        </div>
      ) : null}

      {message ? <p className="mt-4 rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">{message}</p> : null}
      {error ? <p className="mt-4 rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">{error}</p> : null}
    </Modal>
  );
}
