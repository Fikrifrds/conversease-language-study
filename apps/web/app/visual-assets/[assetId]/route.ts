export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const safeAssetId = /^[a-zA-Z0-9-]{8,64}$/;

export async function GET(
  request: Request,
  { params }: { params: { assetId: string } }
) {
  if (!safeAssetId.test(params.assetId)) {
    return new Response("Image not found", { status: 404 });
  }
  const requestUrl = new URL(request.url);
  const variant = requestUrl.searchParams.get("variant") === "thumbnail" ? "thumbnail" : "original";
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
  const metadataResponse = await fetch(
    `${apiBaseUrl}/visual-assets/${encodeURIComponent(params.assetId)}`,
    { cache: "no-store" }
  );
  if (!metadataResponse.ok) {
    return new Response("Image not found", { status: metadataResponse.status });
  }
  const payload = (await metadataResponse.json()) as {
    data?: { asset_url?: string; preview_url?: string };
  };
  const remoteUrl = variant === "thumbnail" ? payload.data?.preview_url : payload.data?.asset_url;
  if (!remoteUrl?.startsWith("https://")) {
    return new Response("Image not found", { status: 404 });
  }
  const imageResponse = await fetch(remoteUrl, { cache: "no-store" });
  if (!imageResponse.ok) {
    return new Response("Image not found", { status: imageResponse.status });
  }
  return new Response(new Uint8Array(await imageResponse.arrayBuffer()), {
    headers: {
      "Content-Type": imageResponse.headers.get("content-type") ?? "image/png",
      "Cache-Control": "public, max-age=31536000, immutable",
      "X-Content-Type-Options": "nosniff"
    }
  });
}
