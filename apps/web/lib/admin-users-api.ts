import { getAuthToken } from "@/lib/auth-api";

type ApiResponse<T> = {
  data: T;
};

type ApiAdminUser = {
  id: string;
  name: string;
  email: string;
  role: "student" | "admin";
  looks_suspicious: boolean;
  email_verified_at: string | null;
  created_at: string;
  updated_at: string;
};

export type AdminUser = {
  id: string;
  name: string;
  email: string;
  role: "student" | "admin";
  looksSuspicious: boolean;
  emailVerifiedAt: string | null;
  createdAt: string;
  updatedAt: string;
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

function mapUser(user: ApiAdminUser): AdminUser {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    role: user.role,
    looksSuspicious: user.looks_suspicious,
    emailVerifiedAt: user.email_verified_at,
    createdAt: user.created_at,
    updatedAt: user.updated_at
  };
}

export async function listAdminUsers(input?: {
  search?: string;
  limit?: number;
  emailVerified?: boolean;
  minAccountAgeDays?: number;
  suspiciousOnly?: boolean;
}): Promise<AdminUser[]> {
  const params = new URLSearchParams();
  if (input?.search) {
    params.set("search", input.search);
  }
  if (typeof input?.emailVerified === "boolean") {
    params.set("email_verified", String(input.emailVerified));
  }
  if (typeof input?.minAccountAgeDays === "number" && input.minAccountAgeDays > 0) {
    params.set("min_account_age_days", String(input.minAccountAgeDays));
  }
  if (input?.suspiciousOnly) {
    params.set("suspicious_only", "true");
  }
  params.set("limit", String(input?.limit ?? 100));

  const response = await adminRequestJson<ApiResponse<ApiAdminUser[]>>(
    `/admin/users?${params.toString()}`
  );
  return response.data.map(mapUser);
}

export async function updateAdminUserRole(input: {
  userId: string;
  role: "student" | "admin";
}): Promise<AdminUser> {
  const response = await adminRequestJson<ApiResponse<ApiAdminUser>>(
    `/admin/users/${input.userId}/role`,
    {
      method: "PATCH",
      body: JSON.stringify({ role: input.role })
    }
  );
  return mapUser(response.data);
}

export async function deleteAdminUser(input: { userId: string }): Promise<void> {
  await adminRequestJson<ApiResponse<{ deleted: boolean; user_id: string }>>(
    `/admin/users/${input.userId}`,
    {
      method: "DELETE"
    }
  );
}

export async function bulkDeleteAdminUsers(input: { userIds: string[] }): Promise<{
  deleted: number;
  userIds: string[];
}> {
  const response = await adminRequestJson<ApiResponse<{ deleted: number; user_ids: string[] }>>(
    "/admin/users/bulk-delete",
    {
      method: "POST",
      body: JSON.stringify({ user_ids: input.userIds })
    }
  );

  return {
    deleted: response.data.deleted,
    userIds: response.data.user_ids
  };
}
