"use client";

import { useEffect, useMemo, useState } from "react";
import Image from "next/image";
import { Loader2, RefreshCw } from "lucide-react";
import { getAuthSession, onAuthSessionChanged } from "@/lib/auth-api";
import {
  regenerateLessonVisual,
  type LessonVisualSlot
} from "@/lib/admin-lesson-visuals-api";

type AdminRegenerableLessonImageProps = {
  lessonSlug: string;
  slot: LessonVisualSlot;
  defaultSrc: string;
  alt: string;
  width: number;
  height: number;
  className?: string;
  priority?: boolean;
};

export function AdminRegenerableLessonImage({
  lessonSlug,
  slot,
  defaultSrc,
  alt,
  width,
  height,
  className,
  priority = false
}: AdminRegenerableLessonImageProps) {
  const [isAdmin, setIsAdmin] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [version, setVersion] = useState("current");
  const [error, setError] = useState("");

  useEffect(() => {
    const syncAdmin = () => setIsAdmin(getAuthSession()?.user.role === "admin");
    syncAdmin();
    return onAuthSessionChanged(syncAdmin);
  }, []);

  const src = useMemo(() => {
    const query = new URLSearchParams({ fallback: defaultSrc, v: version });
    return `/lesson-visuals/${encodeURIComponent(lessonSlug)}/${slot}?${query.toString()}`;
  }, [defaultSrc, lessonSlug, slot, version]);

  async function regenerate() {
    const approved = window.confirm(
      "Generate ulang gambar ini dengan GPT Image 2? Gambar lama untuk lesson ini akan diganti."
    );
    if (!approved) {
      return;
    }

    setIsGenerating(true);
    setError("");
    try {
      const result = await regenerateLessonVisual(lessonSlug, slot);
      setVersion(result.version);
    } catch (generationError) {
      setError(
        generationError instanceof Error ? generationError.message : "Image generation failed."
      );
    } finally {
      setIsGenerating(false);
    }
  }

  return (
    <div className="relative w-full">
      <Image
        key={src}
        src={src}
        alt={alt}
        width={width}
        height={height}
        className={className}
        priority={priority}
        sizes={slot === "hero" ? "(max-width: 1024px) 100vw, 66vw" : "(max-width: 768px) 100vw, 33vw"}
      />
      {isAdmin ? (
        <button
          type="button"
          aria-label={`Regenerate ${slot} image`}
          onClick={regenerate}
          disabled={isGenerating}
          className="focus-ring absolute right-2 top-2 inline-flex items-center gap-1.5 rounded-lg border border-white/70 bg-ink/90 px-3 py-2 text-xs font-semibold text-white shadow-soft backdrop-blur transition hover:bg-ink disabled:cursor-wait disabled:opacity-75"
        >
          {isGenerating ? (
            <Loader2 className="h-3.5 w-3.5 animate-spin" aria-hidden="true" />
          ) : (
            <RefreshCw className="h-3.5 w-3.5" aria-hidden="true" />
          )}
          {isGenerating ? "Generating..." : "Regenerate image"}
        </button>
      ) : null}
      {error ? (
        <p
          role="alert"
          className="absolute bottom-2 left-2 right-2 rounded-lg bg-red-950/90 px-3 py-2 text-xs font-medium text-white shadow-soft"
        >
          {error}
        </p>
      ) : null}
    </div>
  );
}
