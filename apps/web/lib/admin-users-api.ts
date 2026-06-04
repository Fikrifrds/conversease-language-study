import { getAuthToken } from "@/lib/auth-api";

type ApiResponse<T> = {
  data: T;
};

type ApiAdminUser = {
  id: string;
  name: string;
  email: string;
  role: "student" | "admin";
  email_verified_at: string | null;
  created_at: string;
  updated_at: string;
};

export type AdminUser = {
  id: string;
  name: string;
  email: string;
  role: "student" | "admin";
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
    emailVerifiedAt: user.email_verified_at,
    createdAt: user.created_at,
    updatedAt: user.updated_at
  };
}

export async function listAdminUsers(input?: {
  search?: string;
  limit?: number;
}): Promise<AdminUser[]> {
  const params = new URLSearchParams();
  if (input?.search) {
    params.set("search", input.search);
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
