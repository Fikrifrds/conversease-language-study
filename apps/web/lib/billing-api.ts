import { getAuthToken } from "@/lib/auth-api";

export type BillingAccess = {
  planKey: string;
  planName: string;
  isPro: boolean;
  status: string;
  expiresAt: string | null;
  minutes: {
    subscriptionMinutes: number;
    topupMinutes: number;
    totalMinutes: number;
  };
};

export type PaymentKind = "subscription" | "topup";

export type PaymentMetadataValue =
  | string
  | number
  | boolean
  | null
  | PaymentMetadataValue[]
  | { [key: string]: PaymentMetadataValue };

export type PaymentOrder = {
  id: string;
  userId: string;
  packageKey: string;
  paymentKind: PaymentKind;
  status: string;
  amountIdr: number;
  baseAmountIdr: number | null;
  uniqueCode: number | null;
  provider: string;
  providerReference: string;
  checkoutUrl: string;
  metadata: Record<string, PaymentMetadataValue>;
  transferDate: string | null;
  expiresAt: string | null;
  confirmedAt: string | null;
  approvedAt: string | null;
  approvedBy: string | null;
  adminNotes: string | null;
  createdAt: string;
  updatedAt: string;
};

export type BankAccount = {
  bankName: string;
  accountNumber: string;
  accountHolder: string;
};

function metadataString(value: PaymentMetadataValue | undefined, fallback = ""): string {
  if (value === null || value === undefined || value === "") {
    return fallback;
  }
  return typeof value === "string" || typeof value === "number" || typeof value === "boolean"
    ? String(value)
    : fallback;
}

// All destination accounts for a manual-transfer order. Reads the bank_accounts
// list, falling back to the legacy single bank_* fields for older orders.
export function orderBankAccounts(order: PaymentOrder): BankAccount[] {
  const raw = order.metadata["bank_accounts"];
  if (Array.isArray(raw) && raw.length) {
    return raw
      .filter((entry): entry is { [key: string]: PaymentMetadataValue } =>
        Boolean(entry) && typeof entry === "object" && !Array.isArray(entry)
      )
      .map((entry) => ({
        bankName: metadataString(entry["bank_name"]),
        accountNumber: metadataString(entry["bank_account_number"]),
        accountHolder: metadataString(entry["bank_account_holder"]),
      }))
      .filter((account) => account.bankName && account.accountNumber);
  }
  const bankName = metadataString(order.metadata["bank_name"]);
  const accountNumber = metadataString(order.metadata["bank_account_number"]);
  if (!bankName || !accountNumber) {
    return [];
  }
  return [
    {
      bankName,
      accountNumber,
      accountHolder: metadataString(order.metadata["bank_account_holder"]),
    },
  ];
}

// Logo asset for a bank by name; null when we have no logo to show.
export function bankLogo(bankName: string): { src: string; width: number; height: number } | null {
  const name = bankName.trim().toLowerCase();
  if (name.includes("bca")) {
    return { src: "/images/Logo_BCA_Biru.png", width: 140, height: 40 };
  }
  if (name.includes("jago")) {
    return { src: "/images/bank-jago.png", width: 92, height: 30 };
  }
  return null;
}

type ApiResponse<T> = {
  data: T;
};

type ApiBillingAccess = {
  plan_key: string;
  plan_name: string;
  is_pro: boolean;
  status: string;
  expires_at: string | null;
  minutes: {
    subscription_minutes: number;
    topup_minutes: number;
    total_minutes: number;
  };
};

type ApiPaymentOrder = {
  id: string;
  user_id: string;
  package_key: string;
  payment_kind: PaymentKind;
  status: string;
  amount_idr: number;
  base_amount_idr: number | null;
  unique_code: number | null;
  provider: string;
  provider_reference: string;
  checkout_url: string;
  metadata: Record<string, PaymentMetadataValue>;
  transfer_date: string | null;
  expires_at: string | null;
  confirmed_at: string | null;
  approved_at: string | null;
  approved_by: string | null;
  admin_notes: string | null;
  created_at: string;
  updated_at: string;
};

type ApiActivationResponse = {
  order: ApiPaymentOrder;
  access: ApiBillingAccess;
};

function apiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getAuthToken();

  if (!token) {
    throw new Error("Authentication required");
  }

  const response = await fetch(`${apiBaseUrl()}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...init?.headers
    }
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function mapAccess(access: ApiBillingAccess): BillingAccess {
  return {
    planKey: access.plan_key,
    planName: access.plan_name,
    isPro: access.is_pro,
    status: access.status,
    expiresAt: access.expires_at,
    minutes: {
      subscriptionMinutes: access.minutes.subscription_minutes,
      topupMinutes: access.minutes.topup_minutes,
      totalMinutes: access.minutes.total_minutes
    }
  };
}

function mapOrder(order: ApiPaymentOrder): PaymentOrder {
  return {
    id: order.id,
    userId: order.user_id,
    packageKey: order.package_key,
    paymentKind: order.payment_kind,
    status: order.status,
    amountIdr: order.amount_idr,
    baseAmountIdr: order.base_amount_idr,
    uniqueCode: order.unique_code,
    provider: order.provider,
    providerReference: order.provider_reference,
    checkoutUrl: order.checkout_url,
    metadata: order.metadata,
    transferDate: order.transfer_date,
    expiresAt: order.expires_at,
    confirmedAt: order.confirmed_at,
    approvedAt: order.approved_at,
    approvedBy: order.approved_by,
    adminNotes: order.admin_notes,
    createdAt: order.created_at,
    updatedAt: order.updated_at
  };
}

export async function getBillingAccess(): Promise<BillingAccess> {
  const response = await requestJson<ApiResponse<ApiBillingAccess>>("/me/billing/access");
  return mapAccess(response.data);
}

export async function activateSandboxPackage(input: {
  packageKey: string;
  paymentKind: PaymentKind;
}): Promise<{ order: PaymentOrder; access: BillingAccess }> {
  const response = await requestJson<ApiResponse<ApiActivationResponse>>("/billing/sandbox-activate", {
    method: "POST",
    body: JSON.stringify({
      package_key: input.packageKey,
      payment_kind: input.paymentKind
    })
  });

  return {
    order: mapOrder(response.data.order),
    access: mapAccess(response.data.access)
  };
}

export async function createCheckout(input: {
  packageKey: string;
  paymentKind: PaymentKind;
}): Promise<PaymentOrder> {
  const response = await requestJson<ApiResponse<ApiPaymentOrder>>("/billing/checkout", {
    method: "POST",
    body: JSON.stringify({
      package_key: input.packageKey,
      payment_kind: input.paymentKind
    })
  });

  return mapOrder(response.data);
}

export async function getCheckoutOrder(orderId: string): Promise<PaymentOrder> {
  const response = await requestJson<ApiResponse<ApiPaymentOrder>>(`/billing/checkout/${orderId}`);
  return mapOrder(response.data);
}

export async function getBillingOrders(): Promise<PaymentOrder[]> {
  const response = await requestJson<ApiResponse<ApiPaymentOrder[]>>("/me/billing/orders");
  return response.data.map(mapOrder);
}

export async function confirmManualTransfer(input: {
  orderId: string;
  transferDate: string;
  targetBank: string;
}): Promise<{ order: PaymentOrder; emailSent: boolean }> {
  const response = await requestJson<
    ApiResponse<{ order: ApiPaymentOrder; email: { sent: boolean } }>
  >(`/billing/checkout/${input.orderId}/confirm-transfer`, {
    method: "POST",
    body: JSON.stringify({
      transfer_date: input.transferDate,
      target_bank: input.targetBank
    })
  });

  return {
    order: mapOrder(response.data.order),
    emailSent: response.data.email.sent
  };
}
