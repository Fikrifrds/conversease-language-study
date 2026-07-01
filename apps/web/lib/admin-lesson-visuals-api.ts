import { getAuthToken } from "@/lib/auth-api";

export type LessonVisualSlot = "hero" | "card-1" | "card-2" | "card-3";

const MAX_LESSON_VISUAL_UPLOAD_BYTES = 30 * 1024 * 1024;

export type RegeneratedLessonVisual = {
  slug: string;
  slot: LessonVisualSlot;
  model: string;
  version: string;
  byteCount: number;
  libraryAssetId: string;
  libraryRelativePath: string;
  assetUrl: string;
  generatedBy: string;
};

type ApiRegeneratedLessonVisual = {
  data: {
    slug: string;
    slot: LessonVisualSlot;
    model: string;
    version: string;
    byte_count: number;
    library_asset_id: string;
    library_relative_path: string;
    asset_url: string;
    generated_by: string;
  };
};

type ApiLessonVisualPrompt = {
  data: {
    slug: string;
    slot: LessonVisualSlot;
    prompt: string;
    width: number;
    height: number;
  };
};

function apiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

export async function regenerateLessonVisual(
  slug: string,
  slot: LessonVisualSlot
): Promise<RegeneratedLessonVisual> {
  const token = getAuthToken();
  if (!token) {
    throw new Error("Admin login required");
  }

  const response = await fetch(
    `${apiBaseUrl()}/admin/lessons/${encodeURIComponent(slug)}/visuals/${slot}/regenerate`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      }
    }
  );

  if (!response.ok) {
    throw new Error(await responseError(response));
  }

  const payload = (await response.json()) as ApiRegeneratedLessonVisual;
  return mapRegeneratedLessonVisual(payload);
}

export async function getLessonVisualPrompt(slug: string, slot: LessonVisualSlot) {
  const response = await adminFetch(
    `${apiBaseUrl()}/admin/lessons/${encodeURIComponent(slug)}/visuals/${slot}/prompt`
  );
  if (!response.ok) {
    throw new Error(await responseError(response));
  }
  return ((await response.json()) as ApiLessonVisualPrompt).data;
}

export async function uploadLessonVisual(
  slug: string,
  slot: LessonVisualSlot,
  image: File
): Promise<RegeneratedLessonVisual> {
  if (image.size > MAX_LESSON_VISUAL_UPLOAD_BYTES) {
    throw new Error("Ukuran file terlalu besar. Maksimum 30 MB.");
  }
  const formData = new FormData();
  formData.append("image", image);
  const response = await adminFetch(
    `${apiBaseUrl()}/admin/lessons/${encodeURIComponent(slug)}/visuals/${slot}/upload`,
    { method: "POST", body: formData }
  );
  if (!response.ok) {
    throw new Error(await responseError(response));
  }
  return mapRegeneratedLessonVisual((await response.json()) as ApiRegeneratedLessonVisual);
}

export async function uploadLessonVisualFromUrl(
  slug: string,
  slot: LessonVisualSlot,
  url: string
): Promise<RegeneratedLessonVisual> {
  const response = await adminFetch(
    `${apiBaseUrl()}/admin/lessons/${encodeURIComponent(slug)}/visuals/${slot}/upload-url`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    }
  );
  if (!response.ok) {
    throw new Error(await responseError(response));
  }
  return mapRegeneratedLessonVisual((await response.json()) as ApiRegeneratedLessonVisual);
}

function mapRegeneratedLessonVisual(
  payload: ApiRegeneratedLessonVisual
): RegeneratedLessonVisual {
  return {
    slug: payload.data.slug,
    slot: payload.data.slot,
    model: payload.data.model,
    version: payload.data.version,
    byteCount: payload.data.byte_count,
    libraryAssetId: payload.data.library_asset_id,
    libraryRelativePath: payload.data.library_relative_path,
    assetUrl: payload.data.asset_url,
    generatedBy: payload.data.generated_by
  };
}

function adminFetch(url: string, init: RequestInit = {}) {
  const token = getAuthToken();
  if (!token) {
    throw new Error("Admin login required");
  }
  return fetch(url, {
    ...init,
    headers: {
      ...init.headers,
      Authorization: `Bearer ${token}`
    }
  });
}

async function responseError(response: Response) {
  const raw = await response.text();
  try {
    const parsed = JSON.parse(raw) as { detail?: unknown };
    if (typeof parsed.detail === "string") {
      if (parsed.detail === "together_api_key_missing") {
        return "TOGETHER_API_KEY belum dikonfigurasi.";
      }
      if (parsed.detail === "uploaded_image_size_invalid") {
        return "Ukuran file terlalu besar. Maksimum 30 MB.";
      }
      if (parsed.detail === "uploaded_image_format_invalid") {
        return "Format gambar harus PNG, JPEG, atau WebP.";
      }
      if (parsed.detail === "uploaded_image_aspect_ratio_invalid") {
        return "Rasio gambar tidak sesuai dengan slot ini.";
      }
      if (parsed.detail === "remote_image_url_invalid") {
        return "URL gambar tidak valid. Gunakan URL HTTPS langsung.";
      }
      if (parsed.detail === "remote_image_url_forbidden") {
        return "URL menuju alamat jaringan yang tidak diizinkan.";
      }
      if (parsed.detail === "remote_image_content_type_invalid") {
        return "URL tidak mengembalikan file PNG, JPEG, atau WebP.";
      }
      if (parsed.detail === "remote_image_download_failed") {
        return "Gambar gagal diunduh. Link mungkin sudah kedaluwarsa atau tidak dapat diakses server.";
      }
      if (parsed.detail === "remote_image_auth_required") {
        return "Link ini hanya bisa dibuka dengan sesi login pemiliknya. Download gambar dari ChatGPT, lalu gunakan Upload image.";
      }
      if (parsed.detail === "remote_image_too_many_redirects") {
        return "URL gambar memiliki terlalu banyak redirect.";
      }
      return parsed.detail;
    }
  } catch {
    // The API may return plain text for proxy or infrastructure errors.
  }
  return raw || `Image generation failed (${response.status})`;
}
