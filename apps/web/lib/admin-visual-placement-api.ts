import { getAuthToken } from "@/lib/auth-api";

export type VisualPlacementOwnerType = "course" | "unit";
export type VisualPlacementSlot = "cover" | "detail-hero" | "thumbnail";

export type PlacementVisualAsset = {
  asset_id: string;
  model: string;
  width: number;
  height: number;
  byte_count: number;
  preview_url: string;
  is_current: boolean;
  description?: { subject?: string; context?: string; setting?: string };
};

type PlacementTarget = {
  ownerType: VisualPlacementOwnerType;
  ownerKey: string;
  slot: VisualPlacementSlot;
};

const MAX_UPLOAD_BYTES = 30 * 1024 * 1024;

function apiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

function targetUrl(target: PlacementTarget) {
  return `${apiBaseUrl()}/admin/visual-placements/${target.ownerType}/${encodeURIComponent(target.ownerKey)}/${target.slot}`;
}

export async function regeneratePlacementVisual(target: PlacementTarget, prompt: string) {
  return requestAsset(`${targetUrl(target)}/regenerate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt })
  });
}

export async function uploadPlacementVisual(target: PlacementTarget, prompt: string, image: File) {
  if (image.size > MAX_UPLOAD_BYTES) throw new Error("Ukuran file terlalu besar. Maksimum 30 MB.");
  const body = new FormData();
  body.append("prompt", prompt);
  body.append("image", image);
  return requestAsset(`${targetUrl(target)}/upload`, { method: "POST", body });
}

export async function importPlacementVisual(target: PlacementTarget, prompt: string, url: string) {
  return requestAsset(`${targetUrl(target)}/upload-url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, url })
  });
}

export async function getPlacementVisualLibrary(target: PlacementTarget) {
  const response = await adminFetch(`${targetUrl(target)}/library`);
  if (!response.ok) throw new Error(await responseError(response));
  return (await response.json()) as {
    data: { current_asset_id: string | null; assets: PlacementVisualAsset[] };
  };
}

export async function selectPlacementVisual(target: PlacementTarget, assetId: string) {
  return requestAsset(`${targetUrl(target)}/library/select`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ asset_id: assetId })
  });
}

async function requestAsset(url: string, init: RequestInit) {
  const response = await adminFetch(url, init);
  if (!response.ok) throw new Error(await responseError(response));
  return ((await response.json()) as { data: PlacementVisualAsset }).data;
}

function adminFetch(url: string, init: RequestInit = {}) {
  const token = getAuthToken();
  if (!token) throw new Error("Admin login required");
  return fetch(url, {
    ...init,
    cache: "no-store",
    headers: { ...init.headers, Authorization: `Bearer ${token}` }
  });
}

async function responseError(response: Response) {
  const raw = await response.text();
  try {
    const detail = (JSON.parse(raw) as { detail?: unknown }).detail;
    if (detail === "uploaded_image_aspect_ratio_invalid") return "Gunakan gambar rasio 16:9.";
    if (detail === "uploaded_image_size_invalid") return "Ukuran file terlalu besar. Maksimum 30 MB.";
    if (detail === "uploaded_image_format_invalid") return "Format gambar harus PNG, JPEG, atau WebP.";
    if (detail === "together_api_key_missing") return "TOGETHER_API_KEY belum dikonfigurasi.";
    if (detail === "s3_config_missing") return "Konfigurasi S3 belum lengkap.";
    if (detail === "remote_image_auth_required") return "URL membutuhkan sesi login. Download lalu upload file-nya.";
    if (typeof detail === "string") return detail;
  } catch {
    // Proxy responses may be plain text.
  }
  return raw || `Operasi visual gagal (${response.status}).`;
}
