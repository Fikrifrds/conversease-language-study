export type AuthUser = {
  id: string;
  name: string;
  email: string;
  emailVerifiedAt: string | null;
};

export type AuthSession = {
  accessToken: string;
  user: AuthUser;
};

type ApiAuthUser = {
  id: string;
  name: string;
  email: string;
  email_verified_at: string | null;
};

type AuthResponse = {
  access_token: string;
  token_type: "bearer";
  user: ApiAuthUser;
};

const authStorageKey = "conversease.auth.session";

function apiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl()}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers
    }
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function saveAuthSession(session: AuthSession) {
  window.localStorage.setItem(authStorageKey, JSON.stringify(session));
}

export function getAuthSession(): AuthSession | null {
  const raw = window.localStorage.getItem(authStorageKey);
  if (!raw) {
    return null;
  }

  try {
    const value = JSON.parse(raw) as Partial<AuthSession>;
    if (!value.accessToken || !value.user?.id || !value.user.email) {
      return null;
    }
    return {
      accessToken: value.accessToken,
      user: {
        id: value.user.id,
        name: value.user.name ?? "",
        email: value.user.email,
        emailVerifiedAt: value.user.emailVerifiedAt ?? null
      }
    };
  } catch {
    return null;
  }
}

export function getAuthToken(): string | null {
  return getAuthSession()?.accessToken ?? null;
}

export function clearAuthSession() {
  window.localStorage.removeItem(authStorageKey);
}

function mapUser(user: ApiAuthUser): AuthUser {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    emailVerifiedAt: user.email_verified_at
  };
}

export async function registerUser(input: {
  name: string;
  email: string;
  password: string;
}): Promise<AuthSession> {
  const response = await requestJson<AuthResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(input)
  });
  return {
    accessToken: response.access_token,
    user: mapUser(response.user)
  };
}

export async function loginUser(input: { email: string; password: string }): Promise<AuthSession> {
  const response = await requestJson<AuthResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(input)
  });
  return {
    accessToken: response.access_token,
    user: mapUser(response.user)
  };
}

export function googleLoginUrl(nextPath = "/dashboard") {
  return `${apiBaseUrl()}/auth/google/login?next=${encodeURIComponent(nextPath)}`;
}

export async function getGoogleAuthStatus(): Promise<{ enabled: boolean }> {
  const response = await requestJson<{ data: { enabled: boolean } }>("/auth/google/status");
  return response.data;
}

export async function consumeGoogleLoginToken(token: string): Promise<AuthSession> {
  const response = await requestJson<AuthResponse>("/auth/google/session", {
    method: "POST",
    body: JSON.stringify({ token })
  });

  return {
    accessToken: response.access_token,
    user: mapUser(response.user)
  };
}

export async function getCurrentUser(): Promise<AuthUser> {
  const token = getAuthToken();
  if (!token) {
    throw new Error("Authentication required");
  }
  const response = await requestJson<ApiAuthUser>("/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return mapUser(response);
}

export async function requestEmailVerification(): Promise<{
  alreadyVerified: boolean;
  email: string;
  delivery?: { sent: boolean; provider: string; error: string | null; url: string | null };
}> {
  const token = getAuthToken();
  if (!token) {
    throw new Error("Authentication required");
  }

  const response = await requestJson<{
    data: {
      already_verified: boolean;
      email: string;
      delivery?: { sent: boolean; provider: string; error: string | null; url: string | null };
    };
  }>("/auth/request-email-verification", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  return {
    alreadyVerified: response.data.already_verified,
    email: response.data.email,
    delivery: response.data.delivery
  };
}

export async function verifyEmailToken(token: string): Promise<AuthUser> {
  const response = await requestJson<{ data: { verified: boolean; user: ApiAuthUser } }>("/auth/verify-email", {
    method: "POST",
    body: JSON.stringify({ token })
  });

  return mapUser(response.data.user);
}

export async function forgotPassword(email: string): Promise<void> {
  await requestJson<{ data: { requested: boolean } }>("/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email })
  });
}

export async function resetPassword(input: { token: string; password: string }): Promise<void> {
  await requestJson<{ data: { reset: boolean; user: ApiAuthUser } }>("/auth/reset-password", {
    method: "POST",
    body: JSON.stringify({
      token: input.token,
      password: input.password
    })
  });
}
