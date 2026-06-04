import type { PaymentKind, PaymentMetadataValue, PaymentOrder } from "@/lib/billing-api";
import { getAuthToken } from "@/lib/auth-api";

type ApiResponse<T> = {
  data: T;
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

type ApiPaymentNotificationResponse = {
  order: ApiPaymentOrder;
  email: {
    sent: boolean;
    provider: string;
    provider_id: string | null;
    error: string | null;
  };
};

function apiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

async function adminRequestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getAuthToken();
  if (!token) {
    throw new Error("Admin login required");
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
    const detail = await response.text();
    throw new Error(detail || `API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
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

export async function listAdminPaymentOrders(input: {
  status?: string;
  uniqueCode?: number;
  limit?: number;
}): Promise<PaymentOrder[]> {
  const params = new URLSearchParams();

  if (input.status) {
    params.set("status", input.status);
  }

  if (input.uniqueCode) {
    params.set("unique_code", String(input.uniqueCode));
  }

  params.set("limit", String(input.limit ?? 50));

  const response = await adminRequestJson<ApiResponse<ApiPaymentOrder[]>>(
    `/admin/payment-orders?${params.toString()}`
  );
  return response.data.map(mapOrder);
}

export async function getAdminPaymentOrder(input: {
  orderId: string;
}): Promise<PaymentOrder> {
  const response = await adminRequestJson<ApiResponse<ApiPaymentOrder>>(
    `/admin/payment-orders/${input.orderId}`
  );
  return mapOrder(response.data);
}

export async function approveAdminPaymentOrder(input: {
  orderId: string;
  approvedBy: string;
  notes?: string;
}): Promise<PaymentOrder> {
  const response = await adminRequestJson<ApiResponse<ApiPaymentOrder>>(
    `/admin/payment-orders/${input.orderId}/approve`,
    {
      method: "POST",
      body: JSON.stringify({
        approved_by: input.approvedBy,
        notes: input.notes ?? ""
      })
    },
  );
  return mapOrder(response.data);
}

export async function rejectAdminPaymentOrder(input: {
  orderId: string;
  approvedBy: string;
  notes?: string;
}): Promise<PaymentOrder> {
  const response = await adminRequestJson<ApiResponse<ApiPaymentOrder>>(
    `/admin/payment-orders/${input.orderId}/reject`,
    {
      method: "POST",
      body: JSON.stringify({
        approved_by: input.approvedBy,
        notes: input.notes ?? ""
      })
    },
  );
  return mapOrder(response.data);
}

export async function resendAdminPaymentDecisionEmail(input: {
  orderId: string;
  requestedBy: string;
}): Promise<{ order: PaymentOrder; email: ApiPaymentNotificationResponse["email"] }> {
  const response = await adminRequestJson<ApiResponse<ApiPaymentNotificationResponse>>(
    `/admin/payment-orders/${input.orderId}/resend-decision-email`,
    {
      method: "POST",
      body: JSON.stringify({
        requested_by: input.requestedBy
      })
    },
  );
  return {
    order: mapOrder(response.data.order),
    email: response.data.email
  };
}
