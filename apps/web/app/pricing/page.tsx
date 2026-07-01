"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { CheckCircle2, Clipboard, CreditCard, LogIn, ReceiptText, ShieldCheck } from "lucide-react";
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

  const proPlan = plans.find((plan) => plan.key === "pro_3_months")!;
  const proItem: CheckoutItem = {
    key: proPlan.key,
    name: proPlan.name,
    price: proPlan.price,
    cadence: proPlan.cadence,
    access: proPlan.access,
    paymentKind: "subscription"
  };
  const preparing = activePackage === proPlan.key;

  return (
    <AppShell>
      <section className="mx-auto max-w-2xl px-4 pb-16 pt-10 sm:px-6">
        <div className="text-center">
          <p className="text-sm font-semibold uppercase tracking-wide text-leaf">Pro All Access</p>
          <h1 className="mt-3 text-3xl font-semibold sm:text-4xl">Satu paket, akses penuh 3 bulan</h1>
          <p className="mx-auto mt-3 max-w-md leading-7 text-ink/65">
            Buka English track lengkap A1–C1 dengan feedback percakapan detail dan exam resmi tiap level.
          </p>
        </div>

        <section className="mt-8 overflow-hidden rounded-2xl border border-leaf/25 bg-white shadow-sm">
          <div className="bg-mint px-6 py-7 text-center sm:px-8">
            <span className="inline-flex rounded-full bg-white px-3 py-1 text-xs font-semibold text-leaf">
              Best value
            </span>
            <p className="mt-4 text-5xl font-semibold text-ink">{proPlan.price}</p>
            <p className="mt-1 text-sm text-ink/60">untuk {proPlan.cadence} akses penuh</p>
          </div>

          <div className="px-6 py-7 sm:px-8">
            <ul className="space-y-3">
              {proPlan.features.map((feature) => (
                <li key={feature} className="flex gap-3 text-sm text-ink/80">
                  <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-leaf" aria-hidden="true" />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>
            <p className="mt-5 text-xs leading-5 text-ink/55">{proPlan.coachAllowance}</p>

            <button
              type="button"
              onClick={() => handleChoose(proItem)}
              disabled={preparing}
              className="focus-ring mt-6 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-ink px-4 py-3.5 text-sm font-semibold text-white transition hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
            >
              <CreditCard className="h-4 w-4" aria-hidden="true" />
              {preparing ? "Menyiapkan..." : "Pilih Paket Ini"}
            </button>

            <p className="mt-4 text-center text-xs text-ink/55">
              Pembayaran via transfer manual dengan nominal unik — diverifikasi admin dalam waktu singkat.
            </p>
          </div>
        </section>

        <p className="mt-6 text-center text-sm text-ink/55">
          Belum siap upgrade?{" "}
          <Link href="/register" className="font-semibold text-leaf hover:underline">
            Mulai gratis dulu
          </Link>
        </p>
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
