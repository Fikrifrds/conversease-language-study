import { getAuthToken } from "@/lib/auth-api";

export type LessonVisualSlot = "hero" | "card-1" | "card-2" | "card-3";

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

async function responseError(response: Response) {
  const raw = await response.text();
  try {
    const parsed = JSON.parse(raw) as { detail?: unknown };
    if (typeof parsed.detail === "string") {
      if (parsed.detail === "together_api_key_missing") {
        return "TOGETHER_API_KEY belum dikonfigurasi.";
      }
      return parsed.detail;
    }
  } catch {
    // The API may return plain text for proxy or infrastructure errors.
  }
  return raw || `Image generation failed (${response.status})`;
}
