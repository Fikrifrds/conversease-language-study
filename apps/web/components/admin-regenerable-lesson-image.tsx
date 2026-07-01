"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";
import { Check, ClipboardCopy, Loader2, RefreshCw, Upload } from "lucide-react";
import { getAuthSession, onAuthSessionChanged } from "@/lib/auth-api";
import {
  getLessonVisualPrompt,
  regenerateLessonVisual,
  uploadLessonVisual,
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
  const [isCopying, setIsCopying] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [version, setVersion] = useState("current");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const uploadInput = useRef<HTMLInputElement>(null);

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
    setNotice("");
    try {
      const result = await regenerateLessonVisual(lessonSlug, slot);
      setVersion(result.version);
      setNotice("Gambar baru tersimpan dan masuk visual library.");
    } catch (generationError) {
      setError(
        generationError instanceof Error ? generationError.message : "Image generation failed."
      );
    } finally {
      setIsGenerating(false);
    }
  }

  async function copyPrompt() {
    setIsCopying(true);
    setError("");
    setNotice("");
    try {
      const result = await getLessonVisualPrompt(lessonSlug, slot);
      await navigator.clipboard.writeText(result.prompt);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch (copyError) {
      setError(copyError instanceof Error ? copyError.message : "Prompt gagal disalin.");
    } finally {
      setIsCopying(false);
    }
  }

  async function uploadImage(file: File) {
    setIsUploading(true);
    setError("");
    setNotice("");
    try {
      const result = await uploadLessonVisual(lessonSlug, slot, file);
      setVersion(result.version);
      setNotice("Upload berhasil dan masuk visual library.");
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : "Upload gambar gagal.");
    } finally {
      setIsUploading(false);
      if (uploadInput.current) {
        uploadInput.current.value = "";
      }
    }
  }

  const isBusy = isGenerating || isCopying || isUploading;

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
        <div className="absolute right-2 top-2 flex max-w-[calc(100%-1rem)] flex-wrap justify-end gap-1.5">
          <button
            type="button"
            onClick={copyPrompt}
            disabled={isBusy}
            className="focus-ring inline-flex items-center gap-1.5 rounded-lg border border-white/70 bg-ink/90 px-3 py-2 text-xs font-semibold text-white shadow-soft backdrop-blur transition hover:bg-ink disabled:cursor-wait disabled:opacity-75"
          >
            {isCopying ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : copied ? <Check className="h-3.5 w-3.5" /> : <ClipboardCopy className="h-3.5 w-3.5" />}
            {copied ? "Copied" : "Copy prompt"}
          </button>
          <button
            type="button"
            onClick={() => uploadInput.current?.click()}
            disabled={isBusy}
            className="focus-ring inline-flex items-center gap-1.5 rounded-lg border border-white/70 bg-ink/90 px-3 py-2 text-xs font-semibold text-white shadow-soft backdrop-blur transition hover:bg-ink disabled:cursor-wait disabled:opacity-75"
          >
            {isUploading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Upload className="h-3.5 w-3.5" />}
            {isUploading ? "Uploading..." : "Upload image"}
          </button>
          <input
            ref={uploadInput}
            type="file"
            accept="image/png,image/jpeg,image/webp"
            className="sr-only"
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) void uploadImage(file);
            }}
          />
          <button
            type="button"
            aria-label={`Regenerate ${slot} image`}
            onClick={regenerate}
            disabled={isBusy}
            className="focus-ring inline-flex items-center gap-1.5 rounded-lg border border-white/70 bg-ink/90 px-3 py-2 text-xs font-semibold text-white shadow-soft backdrop-blur transition hover:bg-ink disabled:cursor-wait disabled:opacity-75"
          >
            {isGenerating ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <RefreshCw className="h-3.5 w-3.5" />}
            {isGenerating ? "Generating..." : "Regenerate image"}
          </button>
        </div>
      ) : null}
      {error ? (
        <p
          role="alert"
          className="absolute bottom-2 left-2 right-2 rounded-lg bg-red-950/90 px-3 py-2 text-xs font-medium text-white shadow-soft"
        >
          {error}
        </p>
      ) : null}
      {notice ? (
        <p className="absolute bottom-2 left-2 right-2 rounded-lg bg-emerald-950/90 px-3 py-2 text-xs font-medium text-white shadow-soft">
          {notice}
        </p>
      ) : null}
    </div>
  );
}
