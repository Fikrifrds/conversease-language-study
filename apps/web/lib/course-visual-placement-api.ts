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

type NextRequestInit = RequestInit & { next?: { revalidate: number } };

export async function getVisualPlacementManifest(): Promise<VisualPlacementManifest | null> {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
  const init: NextRequestInit =
    typeof window === "undefined"
      ? { next: { revalidate: 300 } }
      : { cache: "default" };
  try {
    const response = await fetch(`${apiBaseUrl}/visual-placements/manifest`, init);
    if (!response.ok) return null;
    const payload = (await response.json()) as { data?: VisualPlacementManifest };
    return payload.data ?? null;
  } catch {
    return null;
  }
}
