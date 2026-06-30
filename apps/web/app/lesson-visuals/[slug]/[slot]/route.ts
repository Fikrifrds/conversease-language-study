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

  const override = await readFirst(overrideCandidates(slug, slot));
  const image = override ?? (await readFallback(request));
  if (!image) {
    return new Response("Image not found", { status: 404 });
  }

  return new Response(new Uint8Array(image), {
    headers: {
      "Content-Type": "image/png",
      "Cache-Control": "public, max-age=300, stale-while-revalidate=3600",
      "X-Content-Type-Options": "nosniff"
    }
  });
}

function overrideCandidates(slug: string, slot: string) {
  const configuredRoot = process.env.LESSON_VISUAL_OVERRIDES_DIR;
  const roots = configuredRoot
    ? [configuredRoot]
    : [
        path.join(process.cwd(), "public", "images", "lesson-visual-overrides"),
        path.join(process.cwd(), "apps", "web", "public", "images", "lesson-visual-overrides")
      ];

  return roots.map((root) => path.join(root, slug, `${slot}.png`));
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
