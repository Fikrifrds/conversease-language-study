"use client";

import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import {
  CheckCircle2,
  ClipboardCheck,
  MailCheck,
  RefreshCcw,
  Search,
  Send,
  ShieldCheck,
  XCircle
} from "lucide-react";
import {
  approveAdminPaymentOrder,
  getAdminPaymentOrder,
  listAdminPaymentOrders,
  rejectAdminPaymentOrder,
  resendAdminPaymentDecisionEmail
} from "@/lib/admin-payment-api";
import type { PaymentMetadataValue, PaymentOrder } from "@/lib/billing-api";
import type { AuthUser } from "@/lib/auth-api";

const statusOptions = [
  { label: "Confirmed", value: "confirmed" },
  { label: "Pending", value: "pending" },
  { label: "Approved", value: "success" },
  { label: "Rejected", value: "failed" },
  { label: "Expired", value: "expired" },
  { label: "All", value: "" }
];

function formatRupiah(value: number) {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0
  })
    .format(value)
    .replace(/\s/g, "");
}

function formatDate(value: string | null) {
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

function metadataValue(order: PaymentOrder | null, key: string, fallback = "-") {
  const value = order?.metadata[key];

  if (value === null || value === undefined || value === "") {
    return fallback;
  }

  if (typeof value === "object") {
    return fallback;
  }

  return String(value);
}

type CustomerDecisionEmail = {
  template_key?: string;
  recipient_email?: string;
  sent?: boolean;
  provider?: string;
  provider_id?: string | null;
  error?: string | null;
  attempt_count?: number;
  attempted_at?: string;
  trigger?: string;
};

function metadataObject(value: PaymentMetadataValue | undefined): Record<string, PaymentMetadataValue> | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return null;
  }

  return value;
}

function customerDecisionEmail(order: PaymentOrder): CustomerDecisionEmail | null {
  const value = metadataObject(order.metadata.customer_decision_email);

  if (!value) {
    return null;
  }

  return {
    template_key: typeof value.template_key === "string" ? value.template_key : undefined,
    recipient_email: typeof value.recipient_email === "string" ? value.recipient_email : undefined,
    sent: typeof value.sent === "boolean" ? value.sent : undefined,
    provider: typeof value.provider === "string" ? value.provider : undefined,
    provider_id: typeof value.provider_id === "string" ? value.provider_id : null,
    error: typeof value.error === "string" ? value.error : null,
    attempt_count: typeof value.attempt_count === "number" ? value.attempt_count : undefined,
    attempted_at: typeof value.attempted_at === "string" ? value.attempted_at : undefined,
    trigger: typeof value.trigger === "string" ? value.trigger : undefined
  };
}

function canSendDecisionEmail(order: PaymentOrder) {
  return order.status === "success" || order.status === "failed";
}

function statusTone(status: string) {
  if (status === "success") {
    return "bg-mint text-leaf";
  }
  if (status === "confirmed") {
    return "bg-[#e8f0ff] text-[#1f3f91]";
  }
  if (status === "failed") {
    return "bg-[#fde7df] text-coral";
  }
  if (status === "expired") {
    return "bg-[#f5ece5] text-ink/60";
  }
  return "bg-paper text-ink/70";
}

export function AdminPaymentManager({ adminUser }: { adminUser: AuthUser }) {
  const searchParams = useSearchParams();
  const deepLinkOrderId = searchParams.get("order_id") ?? "";
  const deepLinkUniqueCode = searchParams.get("unique_code") ?? "";
  const [adminName, setAdminName] = useState(adminUser.name || adminUser.email);
  const [status, setStatus] = useState("confirmed");
  const [query, setQuery] = useState(deepLinkOrderId || deepLinkUniqueCode);
  const [orders, setOrders] = useState<PaymentOrder[]>([]);
  const [selectedOrder, setSelectedOrder] = useState<PaymentOrder | null>(null);
  const [notes, setNotes] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [actionOrderId, setActionOrderId] = useState<string | null>(null);
  const [notificationOrderId, setNotificationOrderId] = useState<string | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (deepLinkOrderId) {
      void loadOrder(deepLinkOrderId);
      return;
    }

    if (deepLinkUniqueCode) {
      void loadOrders({ uniqueCode: Number(deepLinkUniqueCode), nextStatus: "" });
      return;
    }
    void loadOrders();
    // Deep link values should only bootstrap once when the admin screen opens.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [deepLinkOrderId, deepLinkUniqueCode]);

  const selectedCanApprove = selectedOrder?.status === "confirmed" || selectedOrder?.status === "pending";

  const totals = useMemo(() => {
    return orders.reduce(
      (acc, order) => {
        acc.count += 1;
        acc.amount += order.amountIdr;
        if (order.status === "confirmed") {
          acc.confirmed += 1;
        }
        return acc;
      },
      { amount: 0, confirmed: 0, count: 0 },
    );
  }, [orders]);

  async function loadOrders(input?: { uniqueCode?: number; nextStatus?: string }) {
    setIsLoading(true);
    setMessage("");
    setError("");

    try {
      const nextOrders = await listAdminPaymentOrders({
        status: input?.nextStatus ?? status,
        uniqueCode: input?.uniqueCode,
        limit: 100
      });
      setOrders(nextOrders);
      setSelectedOrder(nextOrders[0] ?? null);
      setMessage(nextOrders.length ? `${nextOrders.length} order dimuat.` : "Tidak ada order pada filter ini.");
    } catch {
      setError("Order belum bisa dimuat. Pastikan akunmu punya role admin atau cek koneksi API.");
    } finally {
      setIsLoading(false);
    }
  }

  async function loadOrder(orderId: string) {
    setIsLoading(true);
    setMessage("");
    setError("");

    try {
      const order = await getAdminPaymentOrder({ orderId });
      setOrders([order]);
      setSelectedOrder(order);
      setMessage("Order dari link email berhasil dimuat.");
    } catch {
      setError("Order tidak ditemukan atau akses admin belum valid.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSearch() {
    const cleanQuery = query.trim();

    if (!cleanQuery) {
      await loadOrders();
      return;
    }

    if (cleanQuery.startsWith("order-")) {
      await loadOrder(cleanQuery);
      return;
    }

    const numericCode = Number(cleanQuery.replace(/\D/g, ""));
    if (!numericCode) {
      setError("Gunakan order id atau kode unik 3 digit.");
      return;
    }

    await loadOrders({ uniqueCode: numericCode, nextStatus: "" });
  }

  async function handleDecision(decision: "approve" | "reject") {
    if (!selectedOrder) {
      return;
    }

    setActionOrderId(selectedOrder.id);
    setMessage("");
    setError("");

    try {
      const nextOrder =
        decision === "approve"
          ? await approveAdminPaymentOrder({
              orderId: selectedOrder.id,
              approvedBy: adminName,
              notes
            })
          : await rejectAdminPaymentOrder({
              orderId: selectedOrder.id,
              approvedBy: adminName,
              notes
            });

      setSelectedOrder(nextOrder);
      setOrders((current) => current.map((order) => (order.id === nextOrder.id ? nextOrder : order)));
      const delivery = customerDecisionEmail(nextOrder);
      const deliveryMessage = delivery?.sent ? "Email user terkirim." : "Email user belum terkirim.";
      setMessage(
        decision === "approve"
          ? `Order approved dan akses sudah aktif. ${deliveryMessage}`
          : `Order ditolak. ${deliveryMessage}`,
      );
    } catch {
      setError("Action gagal. Cek status order, role admin, atau koneksi API.");
    } finally {
      setActionOrderId(null);
    }
  }

  async function handleResendDecisionEmail() {
    if (!selectedOrder) {
      return;
    }

    setNotificationOrderId(selectedOrder.id);
    setMessage("");
    setError("");

    try {
      const result = await resendAdminPaymentDecisionEmail({
        orderId: selectedOrder.id,
        requestedBy: adminName
      });
      setSelectedOrder(result.order);
      setOrders((current) => current.map((order) => (order.id === result.order.id ? result.order : order)));
      setMessage(
        result.email.sent
          ? "Email keputusan pembayaran dikirim ke user."
          : `Order tetap tersimpan, tapi email belum terkirim: ${result.email.error ?? "cek provider email"}.`,
      );
    } catch {
      setError("Email keputusan belum bisa dikirim. Cek status order, role admin, atau koneksi API.");
    } finally {
      setNotificationOrderId(null);
    }
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[0.38fr_0.62fr]">
      <section className="space-y-5">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-start gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-mint">
              <ShieldCheck className="h-5 w-5 text-leaf" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">Admin Access</p>
              <h1 className="mt-1 text-2xl font-semibold">Manual Transfer Approval</h1>
              <p className="mt-2 text-sm leading-6 text-ink/60">
                Cocokkan nominal unik dengan mutasi BCA sebelum approve.
              </p>
            </div>
          </div>

          <div className="mt-5 grid gap-3">
            <div className="rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">
              Login sebagai <span className="font-semibold text-ink">{adminUser.email}</span>
            </div>
            <label className="text-sm font-medium text-ink/70">
              Approved by
              <input
                type="text"
                value={adminName}
                onChange={(event) => setAdminName(event.target.value)}
                className="focus-ring mt-2 w-full rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
              />
            </label>
          </div>
        </div>

        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-semibold">Queue</h2>
            <button
              type="button"
              onClick={() => loadOrders()}
              disabled={isLoading}
              className="focus-ring inline-flex h-9 items-center justify-center gap-2 rounded-lg bg-ink px-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              <RefreshCcw className="h-4 w-4" aria-hidden="true" />
              Refresh
            </button>
          </div>

          <div className="mt-4 grid gap-2 sm:grid-cols-2">
            {statusOptions.map((option) => (
              <button
                key={option.label}
                type="button"
                onClick={() => {
                  setStatus(option.value);
                  void loadOrders({ nextStatus: option.value });
                }}
                className={`focus-ring min-h-10 rounded-lg px-3 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-60 ${
                  status === option.value ? "bg-ink text-white" : "bg-paper text-ink/70 hover:bg-mint"
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>

          <div className="mt-4 flex flex-col gap-2 sm:flex-row">
            <input
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="focus-ring min-w-0 flex-1 rounded-lg border border-ink/15 bg-white px-3 py-2 text-sm text-ink"
              placeholder="Kode unik atau order id"
            />
            <button
              type="button"
              onClick={handleSearch}
              disabled={isLoading}
              className="focus-ring inline-flex h-10 w-10 items-center justify-center rounded-lg bg-mint text-leaf disabled:cursor-not-allowed disabled:opacity-60"
              aria-label="Cari order"
              title="Cari order"
            >
              <Search className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>

          <div className="mt-4 grid gap-2 text-sm sm:grid-cols-3">
            <Metric label="Orders" value={totals.count} />
            <Metric label="Confirmed" value={totals.confirmed} />
            <Metric label="Amount" value={formatRupiah(totals.amount)} />
          </div>

          {message ? <p className="mt-4 rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">{message}</p> : null}
          {error ? <p className="mt-4 rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">{error}</p> : null}
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[0.42fr_0.58fr]">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <h2 className="font-semibold">Payment Orders</h2>
          <div className="mt-4 space-y-3">
            {orders.map((order) => (
              <button
                key={order.id}
                type="button"
                onClick={() => setSelectedOrder(order)}
                className={`focus-ring w-full rounded-lg border p-4 text-left ${
                  selectedOrder?.id === order.id ? "border-leaf bg-mint" : "border-ink/10 bg-paper hover:bg-mint"
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-semibold">{metadataValue(order, "package_name", order.packageKey)}</p>
                    <p className="mt-1 text-xs text-ink/50">{order.id}</p>
                  </div>
                  <span className={`rounded-md px-2 py-1 text-xs font-semibold ${statusTone(order.status)}`}>
                    {order.status}
                  </span>
                </div>
                <div className="mt-3 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
                  <p className="text-2xl font-semibold text-[#1f3f91]">{formatRupiah(order.amountIdr)}</p>
                  <p className="rounded-md bg-white px-2 py-1 font-mono text-sm">#{order.uniqueCode ?? "-"}</p>
                </div>
                <p className="mt-3 text-xs text-ink/50">Updated {formatDate(order.updatedAt)}</p>
              </button>
            ))}

            {!orders.length ? (
              <div className="rounded-lg bg-paper p-5 text-sm leading-6 text-ink/60">
                Klik refresh, atau buka link dari email konfirmasi transfer.
              </div>
            ) : null}
          </div>
        </div>

        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          {selectedOrder ? (
            <PaymentDetail
              order={selectedOrder}
              notes={notes}
              canApprove={Boolean(selectedCanApprove)}
              actionOrderId={actionOrderId}
              notificationOrderId={notificationOrderId}
              onNotesChange={setNotes}
              onApprove={() => handleDecision("approve")}
              onReject={() => handleDecision("reject")}
              onResendDecisionEmail={handleResendDecisionEmail}
            />
          ) : (
            <div className="grid min-h-[420px] place-items-center rounded-lg bg-paper p-6 text-center">
              <div>
                <ShieldCheck className="mx-auto h-8 w-8 text-leaf" aria-hidden="true" />
                <h2 className="mt-4 text-xl font-semibold">Pilih order</h2>
                <p className="mt-2 text-sm leading-6 text-ink/60">
                  Detail transfer dan action approval akan muncul di sini.
                </p>
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function PaymentDetail({
  order,
  notes,
  canApprove,
  actionOrderId,
  notificationOrderId,
  onNotesChange,
  onApprove,
  onReject,
  onResendDecisionEmail
}: {
  order: PaymentOrder;
  notes: string;
  canApprove: boolean;
  actionOrderId: string | null;
  notificationOrderId: string | null;
  onNotesChange: (value: string) => void;
  onApprove: () => void;
  onReject: () => void;
  onResendDecisionEmail: () => void;
}) {
  const isActing = actionOrderId === order.id;
  const isNotifying = notificationOrderId === order.id;
  const delivery = customerDecisionEmail(order);
  const notificationReady = canSendDecisionEmail(order);

  return (
    <div>
      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase text-leaf">Payment Detail</p>
          <h2 className="mt-2 text-2xl font-semibold">{metadataValue(order, "package_name", order.packageKey)}</h2>
          <p className="mt-1 text-sm text-ink/50">{order.id}</p>
        </div>
        <span className={`rounded-md px-3 py-2 text-sm font-semibold ${statusTone(order.status)}`}>
          {order.status}
        </span>
      </div>

      <div className="mt-5 rounded-lg border border-leaf/20 bg-mint p-4">
        <p className="text-sm text-ink/70">Nominal yang harus cocok di mutasi</p>
        <p className="mt-2 text-4xl font-semibold text-[#1f3f91]">{formatRupiah(order.amountIdr)}</p>
        <p className="mt-1 text-sm text-[#2563eb]">
          Harga {formatRupiah(order.baseAmountIdr ?? order.amountIdr)} + kode{" "}
          {String(order.uniqueCode ?? "").padStart(3, "0")}
        </p>
      </div>

      <dl className="mt-5 grid gap-3 md:grid-cols-2">
        <DetailItem label="User ID" value={order.userId} />
        <DetailItem label="Payment kind" value={order.paymentKind} />
        <DetailItem label="Nama pengirim" value={metadataValue(order, "sender_name")} />
        <DetailItem label="Bank pengirim" value={metadataValue(order, "sender_bank")} />
        <DetailItem label="Tanggal transfer" value={order.transferDate ?? metadataValue(order, "transfer_date")} />
        <DetailItem label="Confirmed at" value={formatDate(order.confirmedAt)} />
        <DetailItem label="Bank tujuan" value={metadataValue(order, "bank_name")} />
        <DetailItem label="Rekening tujuan" value={metadataValue(order, "bank_account_number")} />
      </dl>

      <div className="mt-5 rounded-lg bg-paper p-4">
        <p className="text-xs font-semibold uppercase text-ink/50">Catatan user</p>
        <p className="mt-2 text-sm leading-6 text-ink/70">{metadataValue(order, "user_notes", "Tidak ada catatan.")}</p>
      </div>

      {notificationReady ? (
        <div className="mt-5 rounded-lg border border-ink/10 bg-paper p-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase text-ink/50">Email user</p>
              <div className="mt-2 flex items-center gap-2">
                <MailCheck
                  className={`h-5 w-5 ${delivery?.sent ? "text-leaf" : "text-coral"}`}
                  aria-hidden="true"
                />
                <p className="text-sm font-semibold text-ink">
                  {delivery ? (delivery.sent ? "Terkirim" : "Belum terkirim") : "Belum ada catatan"}
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={onResendDecisionEmail}
              disabled={isNotifying}
              className="focus-ring inline-flex min-h-10 items-center justify-center gap-2 rounded-lg bg-white px-3 text-sm font-semibold text-ink shadow-sm disabled:cursor-not-allowed disabled:opacity-60"
            >
              <Send className="h-4 w-4" aria-hidden="true" />
              {isNotifying ? "Sending" : "Resend"}
            </button>
          </div>

          <dl className="mt-4 grid gap-2 text-sm md:grid-cols-2">
            <DetailItem label="Recipient" value={delivery?.recipient_email ?? "-"} />
            <DetailItem label="Attempt" value={delivery?.attempt_count ? String(delivery.attempt_count) : "-"} />
            <DetailItem label="Last attempt" value={formatDate(delivery?.attempted_at ?? null)} />
            <DetailItem label="Provider" value={delivery?.provider ?? "-"} />
          </dl>

          {delivery?.error ? (
            <p className="mt-3 rounded-lg bg-[#fde7df] px-3 py-2 text-sm leading-6 text-ink/70">
              {delivery.error}
            </p>
          ) : null}
        </div>
      ) : null}

      <label className="mt-5 block text-sm font-medium text-ink/70">
        Admin notes
        <textarea
          value={notes}
          onChange={(event) => onNotesChange(event.target.value)}
          rows={3}
          className="focus-ring mt-2 w-full resize-none rounded-lg border border-ink/15 bg-white px-3 py-3 text-ink"
          placeholder="Contoh: cocok dengan mutasi BCA"
        />
      </label>

      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        <button
          type="button"
          onClick={onApprove}
          disabled={!canApprove || isActing}
          className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
        >
          <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
          {isActing ? "Processing" : "Approve & Activate"}
        </button>
        <button
          type="button"
          onClick={onReject}
          disabled={!canApprove || isActing}
          className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border border-coral px-4 text-sm font-semibold text-coral disabled:cursor-not-allowed disabled:opacity-60"
        >
          <XCircle className="h-4 w-4" aria-hidden="true" />
          Reject
        </button>
      </div>

      {order.status === "success" ? (
        <div className="mt-5 flex items-start gap-3 rounded-lg bg-mint p-4">
          <ClipboardCheck className="mt-0.5 h-5 w-5 text-leaf" aria-hidden="true" />
          <p className="text-sm leading-6 text-ink/65">
            Order sudah approved oleh {order.approvedBy ?? "admin"} pada {formatDate(order.approvedAt)}.
          </p>
        </div>
      ) : null}
    </div>
  );
}

function DetailItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-paper p-4">
      <dt className="text-xs font-semibold uppercase text-ink/50">{label}</dt>
      <dd className="mt-1 break-words text-sm font-semibold text-ink">{value || "-"}</dd>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-lg bg-paper p-3">
      <p className="text-[11px] font-semibold uppercase text-ink/50">{label}</p>
      <p className="mt-1 truncate text-sm font-semibold">{value}</p>
    </div>
  );
}
