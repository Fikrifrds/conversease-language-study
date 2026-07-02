export type VisualPlacementAsset = {
  asset_id: string;
  width: number;
  height: number;
  alt: string;
};

export type VisualPlacementManifest = {
  version: string;
  placements: Record<string, Record<string, Record<string, VisualPlacementAsset>>>;
};

export async function getVisualPlacementManifest(): Promise<VisualPlacementManifest | null> {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
  try {
    const response = await fetch(`${apiBaseUrl}/visual-placements/manifest`, {
      cache: "no-store"
    });
    if (!response.ok) return null;
    const payload = (await response.json()) as { data?: VisualPlacementManifest };
    return payload.data ?? null;
  } catch {
    return null;
  }
}
