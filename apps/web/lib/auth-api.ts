export type AuthUser = {
  id: string;
  name: string;
  email: string;
  role: "student" | "admin";
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
  role?: "student" | "admin";
  email_verified_at: string | null;
};

type AuthResponse = {
  access_token: string;
  token_type: "bearer";
  user: ApiAuthUser;
};

const authStorageKey = "conversease.auth.session";
const authCookieKey = "conversease_auth_session";
const authSessionChangedEvent = "conversease:auth-session-changed";
const fallbackSessionMaxAgeSeconds = 60 * 60 * 24 * 7;

export class ApiRequestError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail || `API request failed: ${status}`);
    this.name = "ApiRequestError";
    this.status = status;
    this.detail = detail;
  }
}

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
    throw new ApiRequestError(response.status, detail);
  }

  return response.json() as Promise<T>;
}

export function saveAuthSession(session: AuthSession) {
  window.localStorage.setItem(authStorageKey, JSON.stringify(session));
  writeAuthCookie(session);
  dispatchAuthSessionChanged();
}

export function getAuthSession(): AuthSession | null {
  const raw = window.localStorage.getItem(authStorageKey) ?? readAuthCookie();
  if (!raw) {
    return null;
  }

  try {
    const value = JSON.parse(raw) as Partial<AuthSession>;
    if (!value.accessToken || !value.user?.id || !value.user.email) {
      return null;
    }
    const session: AuthSession = {
      accessToken: value.accessToken,
      user: {
        id: value.user.id,
        name: value.user.name ?? "",
        email: value.user.email,
        role: value.user.role === "admin" ? "admin" : "student",
        emailVerifiedAt: value.user.emailVerifiedAt ?? null
      }
    };

    window.localStorage.setItem(authStorageKey, JSON.stringify(session));
    return session;
  } catch {
    return null;
  }
}

export function getAuthToken(): string | null {
  return getAuthSession()?.accessToken ?? null;
}

export function clearAuthSession() {
  window.localStorage.removeItem(authStorageKey);
  clearAuthCookie();
  dispatchAuthSessionChanged();
}

export function onAuthSessionChanged(callback: () => void) {
  window.addEventListener("storage", callback);
  window.addEventListener(authSessionChangedEvent, callback);

  return () => {
    window.removeEventListener("storage", callback);
    window.removeEventListener(authSessionChangedEvent, callback);
  };
}

function dispatchAuthSessionChanged() {
  window.dispatchEvent(new Event(authSessionChangedEvent));
}

function writeAuthCookie(session: AuthSession) {
  const value = encodeURIComponent(JSON.stringify(session));
  const maxAge = sessionMaxAgeSeconds(session.accessToken);
  document.cookie = [
    `${authCookieKey}=${value}`,
    "Path=/",
    `Max-Age=${maxAge}`,
    "SameSite=Lax",
    cookieDomain(),
    secureCookieFlag()
  ]
    .filter(Boolean)
    .join("; ");
}

function readAuthCookie() {
  if (typeof document === "undefined") {
    return null;
  }

  const cookies = document.cookie ? document.cookie.split("; ") : [];
  const match = cookies.find((cookie) => cookie.startsWith(`${authCookieKey}=`));
  return match ? decodeURIComponent(match.slice(authCookieKey.length + 1)) : null;
}

function clearAuthCookie() {
  const baseAttributes = ["Path=/", "Max-Age=0", "SameSite=Lax", secureCookieFlag()].filter(Boolean);
  document.cookie = [`${authCookieKey}=`, ...baseAttributes].join("; ");

  const domain = cookieDomain();
  if (domain) {
    document.cookie = [`${authCookieKey}=`, ...baseAttributes, domain].join("; ");
  }
}

function cookieDomain() {
  if (typeof window === "undefined") {
    return "";
  }

  const hostname = window.location.hostname;
  if (hostname === "conversease.com" || hostname.endsWith(".conversease.com")) {
    return "Domain=.conversease.com";
  }

  return "";
}

function secureCookieFlag() {
  return typeof window !== "undefined" && window.location.protocol === "https:" ? "Secure" : "";
}

function sessionMaxAgeSeconds(accessToken: string) {
  const expiresAt = jwtExpiresAtSeconds(accessToken);
  if (!expiresAt) {
    return fallbackSessionMaxAgeSeconds;
  }

  return Math.max(60, expiresAt - Math.floor(Date.now() / 1000));
}

function jwtExpiresAtSeconds(token: string): number | null {
  try {
    const payload = token.split(".")[1];
    if (!payload) {
      return null;
    }

    const base64 = payload.replace(/-/g, "+").replace(/_/g, "/").padEnd(
      Math.ceil(payload.length / 4) * 4,
      "="
    );
    const decoded = JSON.parse(window.atob(base64)) as { exp?: unknown };
    return typeof decoded.exp === "number" ? decoded.exp : null;
  } catch {
    return null;
  }
}

function mapUser(user: ApiAuthUser): AuthUser {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    role: user.role === "admin" ? "admin" : "student",
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
