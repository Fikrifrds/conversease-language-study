"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { CheckCircle2, Clipboard, CreditCard, LogIn, ReceiptText, ShieldCheck } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { Modal } from "@/components/modal";
import { getAuthSession } from "@/lib/auth-api";
import {
  confirmManualTransfer,
  createCheckout,
  type PaymentKind,
  type PaymentOrder
} from "@/lib/billing-api";
import { plans, topups } from "@/lib/data";
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

function orderMetadata(order: PaymentOrder, key: string, fallback = "-") {
  const value = order.metadata[key];
  if (value === null || value === undefined || value === "") {
    return fallback;
  }
  return String(value);
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
  const [senderName, setSenderName] = useState("");
  const [senderBank, setSenderBank] = useState("");
  const [notes, setNotes] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [authPrompt, setAuthPrompt] = useState(false);

  const topupItems: CheckoutItem[] = topups.map((topup) => ({
    key: topup.key,
    name: topup.name,
    price: topup.price,
    cadence: `${topup.minutes} menit tambahan`,
    access: "Top-up Conversation Coach",
    paymentKind: "topup"
  }));

  async function handleChoose(item: CheckoutItem) {
    setSelectedItem(item);
    setCheckoutOrder(null);
    setMessage("");
    setError("");

    const session = getAuthSession();
    if (!session) {
      setAuthPrompt(true);
      return;
    }

    setAuthPrompt(false);
    setSenderName((current) => current || session.user.name);
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
        senderName,
        senderBank,
        notes
      });
      setCheckoutOrder(result.order);
      trackEvent("purchase_pending", { package_key: checkoutOrder.packageKey });
      setMessage("Konfirmasi terkirim. Admin akan mengecek transfer dan mengaktifkan akses.");
    } catch {
      setError("Konfirmasi belum bisa dikirim. Pastikan tanggal dan nama pengirim sudah diisi.");
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
    setMessage("");
    setError("");
  }

  return (
    <AppShell>
      <section className="mx-auto max-w-7xl px-4 pb-10 pt-8 sm:px-6 lg:px-8">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm md:p-7">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase text-leaf">Harga</p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Pilih paket yang paling pas</h1>
            <p className="mt-3 leading-7 text-ink/70">
              Semua paket Pro membuka English track lengkap A1-C1 dalam satu akses. Pembayaran
              via transfer manual dengan nominal unik agar cepat diverifikasi admin.
            </p>
          </div>

          <div className="mt-5 grid gap-3 text-sm text-ink/70 md:grid-cols-3">
            <div className="rounded-lg bg-paper p-4">
              <p className="font-semibold text-ink">Pilih paket</p>
              <p className="mt-1">Klik paket Pro atau top-up.</p>
            </div>
            <div className="rounded-lg bg-mint p-4">
              <p className="font-semibold text-ink">Transfer nominal unik</p>
              <p className="mt-1">Nominal termasuk kode 3 digit.</p>
            </div>
            <div className="rounded-lg bg-paper p-4">
              <p className="font-semibold text-ink">Konfirmasi</p>
              <p className="mt-1">Admin approve setelah transfer valid.</p>
            </div>
          </div>
        </div>

        <div className="mt-6 grid gap-4 lg:grid-cols-4">
          {plans.map((plan) => {
            const item: CheckoutItem = {
              key: plan.key,
              name: plan.name,
              price: plan.price,
              cadence: plan.cadence,
              access: plan.access,
              paymentKind: "subscription"
            };
            const isFree = plan.key === "free";
            const highlighted = plan.key === "pro_3_months";

            return (
              <section
                key={plan.key}
                className={`flex min-h-[330px] flex-col rounded-lg border p-5 shadow-sm ${
                  highlighted ? "border-leaf bg-mint" : "border-ink/10 bg-white"
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <h2 className="text-xl font-semibold">{plan.name}</h2>
                  {highlighted ? (
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
                {isFree ? (
                  <Link
                    href="/register"
                    className="focus-ring mt-auto inline-flex w-full items-center justify-center gap-2 rounded-lg border border-ink/15 bg-white px-4 py-3 text-sm font-semibold text-ink hover:bg-mint"
                  >
                    Mulai Gratis
                  </Link>
                ) : (
                  <button
                    type="button"
                    onClick={() => handleChoose(item)}
                    disabled={activePackage === plan.key}
                    className="focus-ring mt-auto inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    <CreditCard className="h-4 w-4" aria-hidden="true" />
                    {activePackage === plan.key ? "Menyiapkan..." : "Pilih Paket"}
                  </button>
                )}
              </section>
            );
          })}
        </div>

        <section className="mt-8 rounded-lg border border-ink/10 bg-white p-5 shadow-sm md:p-6">
          <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <h2 className="text-xl font-semibold">Top-up opsional</h2>
              <p className="mt-1 text-sm text-ink/60">
                Tambahan menit latihan jika kuota bulanan habis.
              </p>
            </div>
            <p className="text-sm text-ink/55">Bisa dipakai untuk latihan English track.</p>
          </div>
          <div className="mt-5 grid gap-3 md:grid-cols-3">
            {topupItems.map((topup) => (
              <button
                key={topup.key}
                type="button"
                onClick={() => handleChoose(topup)}
                disabled={activePackage === topup.key}
                className="focus-ring rounded-lg border border-ink/10 bg-paper p-4 text-left transition hover:border-leaf/40 hover:bg-mint disabled:cursor-not-allowed disabled:opacity-60"
              >
                <p className="font-semibold">{topup.name}</p>
                <p className="mt-1 text-sm text-ink/60">{topup.cadence}</p>
                <p className="mt-3 text-2xl font-semibold text-coral">{topup.price}</p>
                <p className="mt-3 text-xs font-semibold uppercase text-leaf">
                  {activePackage === topup.key ? "Menyiapkan..." : "Pilih top-up"}
                </p>
              </button>
            ))}
          </div>
        </section>
      </section>

      {selectedItem ? (
        <CheckoutModal
          item={selectedItem}
          order={checkoutOrder}
          authPrompt={authPrompt}
          transferDate={transferDate}
          senderName={senderName}
          senderBank={senderBank}
          notes={notes}
          message={message}
          error={error}
          isSubmitting={activePackage === selectedItem.key}
          onClose={closeModal}
          onCopy={handleCopy}
          onTransferDateChange={setTransferDate}
          onSenderNameChange={setSenderName}
          onSenderBankChange={setSenderBank}
          onNotesChange={setNotes}
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
  senderName,
  senderBank,
  notes,
  message,
  error,
  isSubmitting,
  onClose,
  onCopy,
  onTransferDateChange,
  onSenderNameChange,
  onSenderBankChange,
  onNotesChange,
  onConfirm
}: {
  item: CheckoutItem;
  order: PaymentOrder | null;
  authPrompt: boolean;
  transferDate: string;
  senderName: string;
  senderBank: string;
  notes: string;
  message: string;
  error: string;
  isSubmitting: boolean;
  onClose: () => void;
  onCopy: (value: string) => void;
  onTransferDateChange: (value: string) => void;
  onSenderNameChange: (value: string) => void;
  onSenderBankChange: (value: string) => void;
  onNotesChange: (value: string) => void;
  onConfirm: () => void;
}) {
  const canConfirm = order?.status === "pending";
  const accountNumber = order ? orderMetadata(order, "bank_account_number") : "";
  const bankName = order ? orderMetadata(order, "bank_name", "BCA") : "BCA";
  const holder = order ? orderMetadata(order, "bank_account_holder", "Conversease") : "Conversease";

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

            <div className="rounded-lg border border-ink/10 p-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm text-ink/50">Bank tujuan</p>
                  <p className="mt-1 text-lg font-semibold">{bankName}</p>
                </div>
                <Image src="/images/Logo_BCA_Biru.png" alt="BCA" width={140} height={40} className="h-7 w-auto" />
              </div>
              <div className="mt-4 flex items-center gap-3 rounded-lg bg-paper px-4 py-3">
                <p className="flex-1 text-center font-mono text-lg tracking-normal">{accountNumber}</p>
                <button
                  type="button"
                  onClick={() => onCopy(accountNumber)}
                  className="focus-ring rounded-md p-2 text-ink/60 hover:bg-white hover:text-ink"
                  aria-label="Salin nomor rekening"
                  title="Salin nomor rekening"
                >
                  <Clipboard className="h-4 w-4" aria-hidden="true" />
                </button>
              </div>
              <p className="mt-3 text-center text-sm text-ink/60">a.n. {holder}</p>
            </div>

            {canConfirm ? (
              <div className="grid gap-3 sm:grid-cols-2">
                <label className="text-sm font-medium text-ink/70">
                  Tanggal transfer
                  <input
                    type="date"
                    value={transferDate}
                    onChange={(event) => onTransferDateChange(event.target.value)}
                    className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
                  />
                </label>
                <label className="text-sm font-medium text-ink/70">
                  Nama pengirim
                  <input
                    type="text"
                    value={senderName}
                    onChange={(event) => onSenderNameChange(event.target.value)}
                    className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
                    placeholder="Nama di rekening"
                  />
                </label>
                <label className="text-sm font-medium text-ink/70">
                  Bank pengirim
                  <input
                    type="text"
                    value={senderBank}
                    onChange={(event) => onSenderBankChange(event.target.value)}
                    className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
                    placeholder="Opsional"
                  />
                </label>
                <label className="text-sm font-medium text-ink/70">
                  Catatan
                  <input
                    type="text"
                    value={notes}
                    onChange={(event) => onNotesChange(event.target.value)}
                    className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
                    placeholder="Opsional"
                  />
                </label>
                <button
                  type="button"
                  onClick={onConfirm}
                  disabled={isSubmitting || !transferDate || senderName.trim().length < 2}
                  className="focus-ring flex min-h-12 items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60 sm:col-span-2"
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
