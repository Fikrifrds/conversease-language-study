import { readFile } from "node:fs/promises";
import path from "node:path";
import { lessonsBySlug } from "@/lib/data";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const visualSlots = new Set(["hero", "card-1", "card-2", "card-3"]);
const safeSlugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

export async function GET(
  request: Request,
  { params }: { params: { slug: string; slot: string } }
) {
  const { slug, slot } = params;
  const lesson = lessonsBySlug[slug];

  if (
    !safeSlugPattern.test(slug) ||
    !visualSlots.has(slot) ||
    !lesson ||
    lesson.language !== "english"
  ) {
    return new Response("Image not found", { status: 404 });
  }

  const requestUrl = new URL(request.url);
  const active = await readActiveVisual(slug, slot);
  if (requestUrl.searchParams.get("metadata") === "1") {
    return Response.json(
      { version: active?.version ?? "fallback" },
      { headers: { "Cache-Control": "no-store, max-age=0" } }
    );
  }

  const remoteImage = active ? await readRemoteImage(active.asset_url) : null;
  const image = remoteImage?.bytes ?? (await readFallback(request));
  if (!image) {
    return new Response("Image not found", { status: 404 });
  }

  return new Response(new Uint8Array(image), {
    headers: {
      "Content-Type": remoteImage?.contentType ?? "image/png",
      "Cache-Control": imageCacheControl(requestUrl.searchParams.get("v")),
      "X-Content-Type-Options": "nosniff"
    }
  });
}

type ActiveVisual = { version: string; asset_url: string };

async function readActiveVisual(slug: string, slot: string): Promise<ActiveVisual | null> {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
  const response = await fetch(
    `${apiBaseUrl}/lesson-visuals/${encodeURIComponent(slug)}/${slot}/active`,
    { cache: "no-store" }
  );
  if (response.status === 404) return null;
  if (!response.ok) throw new Error(`Active lesson visual lookup failed (${response.status})`);
  const payload = (await response.json()) as { data?: Partial<ActiveVisual> };
  return typeof payload.data?.version === "string" && typeof payload.data.asset_url === "string"
    ? { version: payload.data.version, asset_url: payload.data.asset_url }
    : null;
}

async function readRemoteImage(url: string) {
  if (!url.startsWith("https://")) return null;
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error(`Lesson visual download failed (${response.status})`);
  return {
    bytes: Buffer.from(await response.arrayBuffer()),
    contentType: response.headers.get("content-type") ?? "image/png"
  };
}

function imageCacheControl(version: string | null) {
  return version && version !== "current"
    ? "public, max-age=31536000, immutable"
    : "no-store, max-age=0";
}

async function readFallback(request: Request) {
  const fallback = new URL(request.url).searchParams.get("fallback");
  if (
    !fallback ||
    !fallback.startsWith("/images/") ||
    !fallback.toLowerCase().endsWith(".png") ||
    fallback.includes("\\") ||
    fallback.includes("\0")
  ) {
    return null;
  }

  const relativePath = fallback.slice(1);
  const publicRoots = [
    path.resolve(process.cwd(), "public"),
    path.resolve(process.cwd(), "apps", "web", "public")
  ];
  const candidates = publicRoots.flatMap((root) => {
    const candidate = path.resolve(root, relativePath);
    return candidate.startsWith(`${root}${path.sep}`) ? [candidate] : [];
  });

  return readFirst(candidates);
}

async function readFirst(candidates: string[]) {
  for (const candidate of candidates) {
    try {
      return await readFile(candidate);
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ENOENT") {
        throw error;
      }
    }
  }
  return null;
}
