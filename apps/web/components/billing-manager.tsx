"use client";

import Image from "next/image";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { CheckCircle2, Clipboard, CreditCard, Landmark, MailWarning, ReceiptText, XCircle } from "lucide-react";
import { Modal } from "@/components/modal";
import {
  bankLogo,
  cancelManualTransfer,
  confirmManualTransfer,
  createCheckout,
  getBillingAccess,
  getBillingOrders,
  getCheckoutOrder,
  orderBankAccounts,
  type BillingAccess,
  type PaymentKind,
  type PaymentOrder
} from "@/lib/billing-api";
import { getAuthSession, requestEmailVerification } from "@/lib/auth-api";
import { plans } from "@/lib/data";
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

function statusBadgeClass(status: string) {
  if (status === "success") {
    return "bg-mint text-leaf";
  }
  if (status === "failed" || status === "expired") {
    return "bg-[#fde7df] text-coral";
  }
  return "bg-paper text-ink/60";
}

export function BillingManager() {
  const searchParams = useSearchParams();
  const deepLinkOrderId = searchParams.get("order_id") ?? "";
  const [access, setAccess] = useState<BillingAccess | null>(null);
  const [orders, setOrders] = useState<PaymentOrder[]>([]);
  const [checkoutOrder, setCheckoutOrder] = useState<PaymentOrder | null>(null);
  const [activePackage, setActivePackage] = useState<string | null>(null);
  const [transferDate, setTransferDate] = useState(todayInputValue);
  const [targetBank, setTargetBank] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isUpgradeModalOpen, setIsUpgradeModalOpen] = useState(false);
  const [showPaymentInstructions, setShowPaymentInstructions] = useState(false);
  const [cancellingOrderId, setCancellingOrderId] = useState<string | null>(null);
  const [emailVerified, setEmailVerified] = useState(true);
  const [isSendingVerification, setIsSendingVerification] = useState(false);

  useEffect(() => {
    setEmailVerified(Boolean(getAuthSession()?.user.emailVerifiedAt));
  }, []);

  useEffect(() => {
    let ignore = false;

    async function loadBilling() {
      try {
        const [nextAccess, nextOrders] = await Promise.all([getBillingAccess(), getBillingOrders()]);

        if (!ignore) {
          setAccess(nextAccess);
          setOrders(nextOrders);
        }
      } catch {
        if (!ignore) {
          setError("Status billing belum bisa dimuat.");
        }
      }
    }

    loadBilling();

    return () => {
      ignore = true;
    };
  }, []);

  useEffect(() => {
    if (checkoutOrder || deepLinkOrderId) {
      return;
    }

    const activeOrder = orders.find((order) => order.status === "pending" || order.status === "confirmed");
    if (activeOrder) {
      setCheckoutOrder(activeOrder);
    }
    // Runs once orders finish loading; deepLinkOrderId's own effect owns setting
    // checkoutOrder when a link is present, so this only fills in otherwise.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [orders]);

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
    const [nextAccess, nextOrders] = await Promise.all([getBillingAccess(), getBillingOrders()]);
    setAccess(nextAccess);
    setOrders(nextOrders);
  }

  async function handleCheckout(packageKey: string, paymentKind: PaymentKind) {
    setActivePackage(packageKey);
    setTargetBank("");
    setShowPaymentInstructions(false);
    setError("");
    setMessage("");

    try {
      trackEvent("begin_checkout", { package_key: packageKey, payment_kind: paymentKind });
      const order = await createCheckout({ packageKey, paymentKind });
      setCheckoutOrder(order);
      setIsUpgradeModalOpen(true);
      setMessage("Instruksi transfer sudah dibuat. Gunakan nominal tepat agar mudah diverifikasi.");
    } catch {
      setError("Instruksi transfer belum bisa dibuat. Coba ulang sebentar.");
    } finally {
      setActivePackage(null);
    }
  }

  function handleViewPaymentInstructions() {
    setShowPaymentInstructions(true);
    setIsUpgradeModalOpen(true);
  }

  async function handleCancelOrder() {
    if (!checkoutOrder) {
      return;
    }

    setCancellingOrderId(checkoutOrder.id);
    setError("");
    setMessage("");

    try {
      await cancelManualTransfer(checkoutOrder.id);
      setCheckoutOrder(null);
      setIsUpgradeModalOpen(false);
      setShowPaymentInstructions(false);
      setMessage("Order dibatalkan.");
      await refreshAccess();
    } catch {
      setError("Order belum bisa dibatalkan. Coba ulang sebentar.");
    } finally {
      setCancellingOrderId(null);
    }
  }

  async function handleResendVerification() {
    setIsSendingVerification(true);
    setError("");
    setMessage("");

    try {
      const result = await requestEmailVerification();
      if (result.alreadyVerified) {
        setEmailVerified(true);
        setMessage("Email kamu sudah terverifikasi. Silakan lanjut upgrade.");
      } else {
        setMessage(`Link verifikasi dikirim ke ${result.email}. Cek inbox lalu kembali ke sini.`);
      }
    } catch {
      setError("Link verifikasi belum bisa dikirim. Coba ulang sebentar.");
    } finally {
      setIsSendingVerification(false);
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
        targetBank
      });
      setCheckoutOrder(result.order);
      // Manual-transfer confirmation: payment claimed, pending admin approval.
      trackEvent("purchase_pending", { package_key: checkoutOrder.packageKey });
      setMessage("Konfirmasi terkirim. Admin akan mengecek pembayaran dan approve akses.");
      await refreshAccess();
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

  const hasOpenOrder = checkoutOrder && ["pending", "confirmed"].includes(checkoutOrder.status);
  const proPlan = plans.find((plan) => plan.key === "pro_3_months");
  const isProActive = access?.planKey === proPlan?.key;

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

      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-leaf">Langganan</p>
            <h2 className="mt-2 text-2xl font-semibold">
              {isProActive ? proPlan?.name : "Belum ada paket Pro aktif"}
            </h2>
          </div>

          {isProActive ? (
            <span className="inline-flex w-fit items-center gap-1 rounded-full bg-mint px-3 py-1 text-xs font-semibold text-leaf">
              <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
              Aktif
            </span>
          ) : hasOpenOrder ? (
            <p className="text-sm text-ink/55">Selesaikan order aktif dulu sebelum membuat order baru.</p>
          ) : proPlan && emailVerified ? (
            <button
              type="button"
              onClick={() => handleCheckout(proPlan.key, "subscription")}
              disabled={activePackage !== null}
              className="focus-ring inline-flex w-fit items-center justify-center gap-2 rounded-lg bg-ink px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
            >
              <CreditCard className="h-4 w-4" aria-hidden="true" />
              {activePackage === proPlan.key ? "Menyiapkan…" : `Upgrade ke ${proPlan.name}`}
            </button>
          ) : null}
        </div>

        {!isProActive && !hasOpenOrder && !emailVerified ? (
          <div className="mt-5 flex flex-col gap-3 rounded-lg border border-coral/25 bg-[#fdf3ef] p-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-3">
              <MailWarning className="mt-0.5 h-5 w-5 shrink-0 text-coral" aria-hidden="true" />
              <p className="text-sm leading-6 text-ink/70">
                Verifikasi email dulu sebelum upgrade. Cek link verifikasi di inbox kamu, atau kirim ulang.
              </p>
            </div>
            <button
              type="button"
              onClick={handleResendVerification}
              disabled={isSendingVerification}
              className="focus-ring inline-flex w-fit shrink-0 items-center justify-center gap-2 rounded-lg bg-ink px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-leaf disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSendingVerification ? "Mengirim…" : "Kirim ulang link verifikasi"}
            </button>
          </div>
        ) : null}

        {checkoutOrder && hasOpenOrder ? (
          <ActiveOrderCard
            order={checkoutOrder}
            isCancelling={cancellingOrderId === checkoutOrder.id}
            onViewInstructions={handleViewPaymentInstructions}
            onCancel={handleCancelOrder}
          />
        ) : null}
      </section>

      {checkoutOrder && isUpgradeModalOpen ? (
        <Modal
          eyebrow="Instruksi Pembayaran"
          title={orderMetadata(checkoutOrder, "package_name", checkoutOrder.packageKey)}
          size="lg"
          closeLabel="Tutup instruksi pembayaran"
          onClose={() => setIsUpgradeModalOpen(false)}
        >
          <TransferInstruction
            order={checkoutOrder}
            transferDate={transferDate}
            targetBank={targetBank}
            showPaymentInstructions={showPaymentInstructions}
            isSubmitting={activePackage === checkoutOrder.packageKey}
            isCancelling={cancellingOrderId === checkoutOrder.id}
            onTransferDateChange={setTransferDate}
            onTargetBankChange={setTargetBank}
            onShowPaymentInstructions={() => setShowPaymentInstructions(true)}
            onConfirm={handleConfirmTransfer}
            onCancel={handleCancelOrder}
            onCopy={handleCopy}
          />
        </Modal>
      ) : null}

      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <h2 className="text-xl font-semibold">Riwayat transaksi</h2>
        {orders.length === 0 ? (
          <p className="mt-3 rounded-lg bg-paper px-4 py-3 text-sm text-ink/55">
            Belum ada transaksi. Order akan muncul di sini setelah kamu membuat instruksi transfer.
          </p>
        ) : (
          <ul className="mt-4 divide-y divide-ink/10">
            {orders.map((order) => (
              <li key={order.id} className="flex flex-wrap items-center justify-between gap-3 py-3">
                <div>
                  <p className="font-semibold">{orderMetadata(order, "package_name", order.packageKey)}</p>
                  <p className="mt-1 text-sm text-ink/55">
                    {formatDate(order.createdAt)} · {formatRupiah(order.amountIdr)}
                  </p>
                </div>
                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${statusBadgeClass(order.status)}`}
                >
                  {statusLabel(order.status)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

function TransferInstruction({
  order,
  transferDate,
  targetBank,
  showPaymentInstructions,
  isSubmitting,
  isCancelling,
  onTransferDateChange,
  onTargetBankChange,
  onShowPaymentInstructions,
  onConfirm,
  onCancel,
  onCopy
}: {
  order: PaymentOrder;
  transferDate: string;
  targetBank: string;
  showPaymentInstructions: boolean;
  isSubmitting: boolean;
  isCancelling: boolean;
  onTransferDateChange: (value: string) => void;
  onTargetBankChange: (value: string) => void;
  onShowPaymentInstructions: () => void;
  onConfirm: () => void;
  onCancel: () => void;
  onCopy: (value: string) => void;
}) {
  const bankAccounts = orderBankAccounts(order);
  const canConfirm = order.status === "pending";
  const recordedBank = orderMetadata(order, "bank_name", "");
  const activeBank = canConfirm ? targetBank : recordedBank;
  const selectedAccount = bankAccounts.find((account) => account.bankName === activeBank) ?? null;

  return (
    <div>
      <div className="rounded-lg border border-leaf/20 bg-mint p-4">
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

      {showPaymentInstructions ? (
        <div className="mt-4 space-y-3">
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
                        <p className="text-xs uppercase tracking-wide text-ink/45">Bank Tujuan</p>
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
      ) : (
        <button
          type="button"
          onClick={onShowPaymentInstructions}
          className="focus-ring mt-4 flex min-h-11 w-full items-center justify-center gap-2 rounded-lg border border-ink/15 bg-white px-4 text-sm font-semibold text-ink hover:bg-paper"
        >
          <Landmark className="h-4 w-4" aria-hidden="true" />
          Lihat cara pembayaran
        </button>
      )}

      {showPaymentInstructions ? (
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <Metric label="Status" value={statusLabel(order.status)} />
          <Metric label="Berlaku sampai" value={formatDateTime(order.expiresAt)} />
        </div>
      ) : null}

      {canConfirm && showPaymentInstructions ? (
        <label className="mt-5 block text-sm font-medium text-ink/70">
          2. Tanggal transfer
          <input
            type="date"
            value={transferDate}
            onChange={(event) => onTransferDateChange(event.target.value)}
            className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
          />
        </label>
      ) : null}

      {order.status === "confirmed" ? (
        <div className="mt-5 flex items-start gap-3 rounded-lg bg-paper p-4">
          <Landmark className="mt-0.5 h-5 w-5 text-leaf" aria-hidden="true" />
          <p className="text-sm leading-6 text-ink/65">
            Konfirmasi sudah masuk. Admin akan mencocokkan nominal unik dan mengaktifkan akses setelah transfer valid.
          </p>
        </div>
      ) : null}

      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        <button
          type="button"
          onClick={onCancel}
          disabled={isCancelling || isSubmitting}
          className="focus-ring flex min-h-12 items-center justify-center gap-2 rounded-lg border border-coral px-4 text-sm font-semibold text-coral disabled:cursor-not-allowed disabled:opacity-60"
        >
          <XCircle className="h-4 w-4" aria-hidden="true" />
          {isCancelling ? "Membatalkan…" : "Batalkan Order"}
        </button>
        {canConfirm ? (
          <button
            type="button"
            onClick={onConfirm}
            disabled={isSubmitting || isCancelling || !targetBank || !transferDate}
            className="focus-ring flex min-h-12 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
          >
            <ReceiptText className="h-4 w-4" aria-hidden="true" />
            {isSubmitting ? "Mengirim konfirmasi…" : "Saya Sudah Transfer"}
          </button>
        ) : null}
      </div>
    </div>
  );
}

function ActiveOrderCard({
  order,
  isCancelling,
  onViewInstructions,
  onCancel
}: {
  order: PaymentOrder;
  isCancelling: boolean;
  onViewInstructions: () => void;
  onCancel: () => void;
}) {
  return (
    <div className="mt-5 rounded-lg border border-leaf/25 bg-mint p-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase text-leaf">Order aktif</p>
          <p className="mt-1 text-xl font-semibold">{formatRupiah(order.amountIdr)}</p>
          <p className="mt-1 text-sm text-ink/60">
            {orderMetadata(order, "package_name", order.packageKey)} · {statusLabel(order.status)}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={onViewInstructions}
            className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white hover:bg-leaf"
          >
            <Landmark className="h-4 w-4" aria-hidden="true" />
            Lihat cara pembayaran
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={isCancelling}
            className="focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg border border-coral px-4 text-sm font-semibold text-coral disabled:cursor-not-allowed disabled:opacity-60"
          >
            <XCircle className="h-4 w-4" aria-hidden="true" />
            {isCancelling ? "Membatalkan…" : "Batalkan"}
          </button>
        </div>
      </div>
    </div>
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
