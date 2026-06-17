"use client";

import Image from "next/image";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { CheckCircle2, Clipboard, Landmark, ReceiptText } from "lucide-react";
import { getAuthSession } from "@/lib/auth-api";
import {
  confirmManualTransfer,
  createCheckout,
  getBillingAccess,
  getCheckoutOrder,
  type BillingAccess,
  type PaymentKind,
  type PaymentOrder
} from "@/lib/billing-api";
import { plans, topups } from "@/lib/data";
import { trackEvent } from "@/lib/analytics";

function formatDate(value: string | null) {
  if (!value) {
    return "Tidak ada expiry";
  }

  return new Intl.DateTimeFormat("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric"
  }).format(new Date(value));
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

function formatRupiah(value: number) {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0
  })
    .format(value)
    .replace(/\s/g, "");
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

export function BillingManager() {
  const searchParams = useSearchParams();
  const deepLinkOrderId = searchParams.get("order_id") ?? "";
  const [access, setAccess] = useState<BillingAccess | null>(null);
  const [checkoutOrder, setCheckoutOrder] = useState<PaymentOrder | null>(null);
  const [activePackage, setActivePackage] = useState<string | null>(null);
  const [transferDate, setTransferDate] = useState(todayInputValue);
  const [senderName, setSenderName] = useState("");
  const [senderBank, setSenderBank] = useState("");
  const [notes, setNotes] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let ignore = false;
    const session = getAuthSession();

    if (session?.user.name) {
      setSenderName((current) => current || session.user.name);
    }

    async function loadAccess() {
      try {
        const nextAccess = await getBillingAccess();

        if (!ignore) {
          setAccess(nextAccess);
        }
      } catch {
        if (!ignore) {
          setError("Status billing belum bisa dimuat.");
        }
      }
    }

    loadAccess();

    return () => {
      ignore = true;
    };
  }, []);

  useEffect(() => {
    if (!deepLinkOrderId) {
      return;
    }

    let ignore = false;

    async function loadCheckoutOrder() {
      setError("");

      try {
        const order = await getCheckoutOrder(deepLinkOrderId);

        if (ignore) {
          return;
        }

        setCheckoutOrder(order);
        if (order.status === "pending") {
          setMessage("Instruksi transfer dari link order berhasil dimuat.");
        } else if (order.status === "confirmed") {
          setMessage("Konfirmasi transfer sudah masuk dan sedang menunggu approval admin.");
        } else if (order.status === "success") {
          setMessage("Pembayaran sudah approved. Akses kamu sudah diperbarui.");
          await refreshAccess();
        } else if (order.status === "expired") {
          setMessage("Order ini sudah expired. Buat instruksi transfer baru jika masih ingin membeli paket.");
        } else if (order.status === "failed") {
          setMessage("Order ini ditolak. Buat instruksi transfer baru atau hubungi support.");
        }
      } catch {
        if (!ignore) {
          setError("Order dari link belum bisa dimuat. Pastikan kamu login dengan akun yang membuat order.");
        }
      }
    }

    void loadCheckoutOrder();

    return () => {
      ignore = true;
    };
    // refreshAccess is intentionally not a dependency to avoid reloading a deep link after access refresh.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [deepLinkOrderId]);

  async function refreshAccess() {
    const nextAccess = await getBillingAccess();
    setAccess(nextAccess);
  }

  async function handleCheckout(packageKey: string, paymentKind: PaymentKind) {
    setActivePackage(packageKey);
    setError("");
    setMessage("");

    try {
      trackEvent("begin_checkout", { package_key: packageKey, payment_kind: paymentKind });
      const order = await createCheckout({ packageKey, paymentKind });
      setCheckoutOrder(order);
      setMessage("Instruksi transfer sudah dibuat. Gunakan nominal tepat agar mudah diverifikasi.");
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
    setError("");
    setMessage("");

    try {
      const result = await confirmManualTransfer({
        orderId: checkoutOrder.id,
        transferDate,
        senderName,
        senderBank,
        notes
      });
      setCheckoutOrder(result.order);
      // Manual-transfer confirmation: payment claimed, pending admin approval.
      trackEvent("purchase_pending", { package_key: checkoutOrder.packageKey });
      setMessage("Konfirmasi terkirim. Admin akan mengecek pembayaran dan approve akses.");
      await refreshAccess();
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

  const hasOpenOrder = checkoutOrder && ["pending", "confirmed"].includes(checkoutOrder.status);

  return (
    <div className="space-y-5">
      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div className="max-w-2xl">
            <p className="text-sm font-semibold uppercase text-leaf">Billing</p>
            <h1 className="mt-2 text-3xl font-semibold">{access?.planName ?? "Memuat"}</h1>
            <p className="mt-2 text-sm leading-6 text-ink/60">
              {access?.isPro
                ? `Akses Pro aktif sampai ${formatDate(access.expiresAt)}.`
                : "Akses Free aktif. Upgrade kapan saja saat kamu siap latihan lebih rutin."}
            </p>
          </div>
          <div className="rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">
            Transfer manual, nominal unik, lalu konfirmasi dari halaman ini.
          </div>
        </div>

        <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <Metric label="Menit tersedia" value={access?.minutes.totalMinutes ?? 0} />
          <Metric label="Dari langganan" value={access?.minutes.subscriptionMinutes ?? 0} />
          <Metric label="Dari top-up" value={access?.minutes.topupMinutes ?? 0} />
          <Metric label="Status" value={access?.status ?? "-"} />
        </div>

        {message ? <p className="mt-4 rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">{message}</p> : null}
        {error ? <p className="mt-4 rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">{error}</p> : null}
      </section>

      {checkoutOrder ? (
        <TransferInstruction
          order={checkoutOrder}
          transferDate={transferDate}
          senderName={senderName}
          senderBank={senderBank}
          notes={notes}
          isSubmitting={activePackage === checkoutOrder.packageKey}
          onTransferDateChange={setTransferDate}
          onSenderNameChange={setSenderName}
          onSenderBankChange={setSenderBank}
          onNotesChange={setNotes}
          onConfirm={handleConfirmTransfer}
          onCopy={handleCopy}
        />
      ) : null}

      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-leaf">Langganan</p>
            <h2 className="mt-2 text-2xl font-semibold">Pilih paket Pro</h2>
          </div>
          {hasOpenOrder ? (
            <p className="text-sm text-ink/55">Selesaikan order aktif dulu sebelum membuat order baru.</p>
          ) : null}
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-3">
          {plans.filter((plan) => plan.key !== "free").map((plan) => (
            <button
              key={plan.key}
              type="button"
              onClick={() => handleCheckout(plan.key, "subscription")}
              disabled={activePackage !== null || Boolean(hasOpenOrder) || access?.planKey === plan.key}
              className={`focus-ring rounded-lg border p-4 text-left transition hover:border-leaf disabled:cursor-not-allowed disabled:opacity-60 ${
                access?.planKey === plan.key ? "border-leaf bg-mint" : "border-ink/10 bg-paper"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-semibold">{plan.name}</p>
                  <p className="mt-1 text-sm text-ink/60">{plan.cadence}</p>
                </div>
                {access?.planKey === plan.key ? (
                  <CheckCircle2 className="h-5 w-5 text-leaf" aria-hidden="true" />
                ) : null}
              </div>
              <p className="mt-4 text-2xl font-semibold">{plan.price}</p>
              <p className="mt-2 text-sm text-ink/60">{plan.access}</p>
              <p className="mt-4 text-xs font-semibold uppercase text-coral">
                {access?.planKey === plan.key
                  ? "Aktif"
                  : activePackage === plan.key
                    ? "Menyiapkan…"
                    : "Buat instruksi transfer"}
              </p>
            </button>
          ))}
        </div>
      </section>

      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
          <div>
            <h2 className="text-xl font-semibold">Top-up opsional</h2>
            <p className="mt-1 text-sm text-ink/60">Tambahan menit latihan setelah kuota bulanan habis.</p>
          </div>
          <p className="text-sm text-ink/55">Bisa dipakai untuk English atau Arabic.</p>
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-3">
          {topups.map((topup) => (
            <button
              key={topup.key}
              type="button"
              onClick={() => handleCheckout(topup.key, "topup")}
              disabled={activePackage !== null || Boolean(hasOpenOrder)}
              className="focus-ring rounded-lg border border-ink/10 bg-paper p-4 text-left transition hover:border-leaf hover:bg-mint disabled:cursor-not-allowed disabled:opacity-60"
            >
              <p className="font-semibold">{topup.name}</p>
              <p className="mt-1 text-sm text-ink/60">{topup.minutes} menit tambahan</p>
              <p className="mt-3 text-2xl font-semibold text-coral">{topup.price}</p>
              <p className="mt-3 text-xs font-semibold uppercase text-leaf">
                {activePackage === topup.key ? "Menyiapkan…" : "Buat instruksi transfer"}
              </p>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

function TransferInstruction({
  order,
  transferDate,
  senderName,
  senderBank,
  notes,
  isSubmitting,
  onTransferDateChange,
  onSenderNameChange,
  onSenderBankChange,
  onNotesChange,
  onConfirm,
  onCopy
}: {
  order: PaymentOrder;
  transferDate: string;
  senderName: string;
  senderBank: string;
  notes: string;
  isSubmitting: boolean;
  onTransferDateChange: (value: string) => void;
  onSenderNameChange: (value: string) => void;
  onSenderBankChange: (value: string) => void;
  onNotesChange: (value: string) => void;
  onConfirm: () => void;
  onCopy: (value: string) => void;
}) {
  const accountNumber = orderMetadata(order, "bank_account_number");
  const bankName = orderMetadata(order, "bank_name", "Bank Jago");
  const holder = orderMetadata(order, "bank_account_holder", "Conversease");
  const packageName = orderMetadata(order, "package_name", order.packageKey);
  const canConfirm = order.status === "pending";

  return (
    <section className="rounded-lg border border-leaf/30 bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase text-leaf">Instruksi Pembayaran</p>
          <h2 className="mt-2 text-2xl font-semibold">{packageName}</h2>
          <p className="mt-2 text-sm text-ink/60">Order {order.id}</p>
        </div>
        <div className="rounded-lg bg-paper px-3 py-2 text-sm font-semibold text-coral">
          {statusLabel(order.status)}
        </div>
      </div>

      <div className="mt-5 rounded-lg border border-leaf/20 bg-mint p-4">
        <p className="text-sm text-ink/70">Transfer sesuai nominal berikut</p>
        <p className="mt-2 text-3xl font-semibold text-[#1f3f91]">{formatRupiah(order.amountIdr)}</p>
        <p className="mt-1 text-sm text-[#2563eb]">
          Harga {formatRupiah(order.baseAmountIdr ?? order.amountIdr)} + kode{" "}
          {String(order.uniqueCode ?? "").padStart(3, "0")}
        </p>
        {order.expiresAt ? (
          <p className="mt-3 rounded-md bg-white/70 px-3 py-2 text-sm font-medium text-ink/70">
            Konfirmasi sebelum {formatDateTime(order.expiresAt)}
          </p>
        ) : null}
      </div>

      <div className="mt-4 rounded-lg border border-ink/10 p-4">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm text-ink/50">Bank Tujuan</p>
            <p className="mt-2 text-lg font-semibold">{bankName}</p>
          </div>
          <Image
            src="/images/bank-jago.png"
            alt="Bank Jago"
            width={92}
            height={30}
            className="h-7 w-auto"
          />
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

      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        <Metric label="Bank" value={bankName} />
        <Metric label="Status" value={statusLabel(order.status)} />
        <Metric label="Berlaku sampai" value={formatDateTime(order.expiresAt)} />
      </div>

      {canConfirm ? (
        <div className="mt-5 grid gap-4 md:grid-cols-2">
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
            className="focus-ring flex min-h-12 items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60 md:col-span-2"
          >
            <ReceiptText className="h-4 w-4" aria-hidden="true" />
            {isSubmitting ? "Mengirim konfirmasi…" : "Saya Sudah Transfer"}
          </button>
        </div>
      ) : (
        <div className="mt-5 flex items-start gap-3 rounded-lg bg-paper p-4">
          <Landmark className="mt-0.5 h-5 w-5 text-leaf" aria-hidden="true" />
          <p className="text-sm leading-6 text-ink/65">
            Konfirmasi sudah masuk. Admin akan mencocokkan nominal unik dan mengaktifkan akses setelah transfer valid.
          </p>
        </div>
      )}
    </section>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-lg bg-paper p-4">
      <p className="text-xs font-semibold uppercase text-ink/50">{label}</p>
      <p className="mt-1 text-lg font-semibold">{value}</p>
    </div>
  );
}
