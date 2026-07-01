"use client";
/* eslint-disable @next/next/no-img-element */

import { useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";
import { Check, ClipboardCopy, Images, Link2, Loader2, RefreshCw, Upload, X } from "lucide-react";
import { getAuthSession, onAuthSessionChanged } from "@/lib/auth-api";
import {
  getLessonVisualPrompt,
  getLessonVisualLibrary,
  regenerateLessonVisual,
  selectLessonVisualLibraryAsset,
  uploadLessonVisual,
  uploadLessonVisualFromUrl,
  type LessonVisualLibraryAsset,
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
  const [isImportingUrl, setIsImportingUrl] = useState(false);
  const [copied, setCopied] = useState(false);
  const [libraryOpen, setLibraryOpen] = useState(false);
  const [libraryLoading, setLibraryLoading] = useState(false);
  const [libraryAssets, setLibraryAssets] = useState<LessonVisualLibraryAsset[]>([]);
  const [version, setVersion] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const uploadInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const syncAdmin = () => setIsAdmin(getAuthSession()?.user.role === "admin");
    syncAdmin();
    return onAuthSessionChanged(syncAdmin);
  }, []);

  useEffect(() => {
    let active = true;
    const metadataUrl = `/lesson-visuals/${encodeURIComponent(lessonSlug)}/${slot}?metadata=1`;
    fetch(metadataUrl, { cache: "no-store" })
      .then(async (response) => {
        if (!response.ok) throw new Error("Visual metadata unavailable");
        return (await response.json()) as { version?: unknown };
      })
      .then((payload) => {
        if (active && typeof payload.version === "string") {
          setVersion(payload.version);
        }
      })
      .catch(() => {
        if (active) setVersion(`refresh-${Date.now()}`);
      });
    return () => {
      active = false;
    };
  }, [lessonSlug, slot]);

  const src = useMemo(() => {
    if (!version) return null;
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

  async function uploadFromUrl() {
    const url = window.prompt("Paste URL gambar HTTPS. Gambar akan langsung diunduh dan disimpan.");
    if (!url?.trim()) {
      return;
    }

    setIsImportingUrl(true);
    setError("");
    setNotice("");
    try {
      const result = await uploadLessonVisualFromUrl(lessonSlug, slot, url.trim());
      setVersion(result.version);
      setNotice("Gambar dari URL sudah diunduh, disimpan, dan masuk visual library.");
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : "Import URL gagal.");
    } finally {
      setIsImportingUrl(false);
    }
  }

  async function openLibrary() {
    setLibraryOpen(true);
    setLibraryLoading(true);
    setError("");
    try {
      const result = await getLessonVisualLibrary(lessonSlug, slot);
      setLibraryAssets(result.data.assets);
    } catch (libraryError) {
      setError(libraryError instanceof Error ? libraryError.message : "Visual library gagal dibuka.");
      setLibraryOpen(false);
    } finally {
      setLibraryLoading(false);
    }
  }

  async function activateLibraryAsset(assetId: string) {
    setLibraryLoading(true);
    try {
      const result = await selectLessonVisualLibraryAsset(lessonSlug, slot, assetId);
      setVersion(result.version);
      setLibraryOpen(false);
      setNotice("Gambar dari visual library sudah diaktifkan.");
    } catch (libraryError) {
      setError(libraryError instanceof Error ? libraryError.message : "Gambar gagal dipilih.");
    } finally {
      setLibraryLoading(false);
    }
  }

  const isBusy = isGenerating || isCopying || isUploading || isImportingUrl;

  return (
    <div className="relative w-full">
      {src ? (
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
      ) : (
        <div
          aria-hidden="true"
          className="w-full animate-pulse bg-sand/40"
          style={{ aspectRatio: `${width} / ${height}` }}
        />
      )}
      {isAdmin ? (
        <div className="absolute right-2 top-2 flex max-w-[calc(100%-1rem)] flex-wrap justify-end gap-1.5">
          <button
            type="button"
            onClick={openLibrary}
            disabled={isBusy}
            className="focus-ring inline-flex items-center gap-1.5 rounded-lg border border-white/70 bg-ink/90 px-3 py-2 text-xs font-semibold text-white shadow-soft backdrop-blur transition hover:bg-ink disabled:cursor-wait disabled:opacity-75"
          >
            <Images className="h-3.5 w-3.5" />
            Library
          </button>
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
          <button
            type="button"
            onClick={uploadFromUrl}
            disabled={isBusy}
            className="focus-ring inline-flex items-center gap-1.5 rounded-lg border border-white/70 bg-ink/90 px-3 py-2 text-xs font-semibold text-white shadow-soft backdrop-blur transition hover:bg-ink disabled:cursor-wait disabled:opacity-75"
          >
            {isImportingUrl ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Link2 className="h-3.5 w-3.5" />}
            {isImportingUrl ? "Importing..." : "Import URL"}
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
      {libraryOpen ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="max-h-[85vh] w-full max-w-5xl overflow-auto rounded-2xl bg-white p-5 shadow-2xl">
            <div className="mb-4 flex items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-bold text-ink">Visual library</h2>
                <p className="text-sm text-muted">Pilih gambar dari library global untuk slot {slot}.</p>
              </div>
              <button type="button" onClick={() => setLibraryOpen(false)} className="focus-ring rounded-lg p-2 hover:bg-sand">
                <X className="h-5 w-5" />
              </button>
            </div>
            {libraryLoading && libraryAssets.length === 0 ? (
              <div className="flex justify-center py-16"><Loader2 className="h-7 w-7 animate-spin" /></div>
            ) : libraryAssets.length === 0 ? (
              <p className="py-12 text-center text-muted">Belum ada gambar di library.</p>
            ) : (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {libraryAssets.map((asset) => (
                  <article key={asset.asset_id} className={`overflow-hidden rounded-xl border ${asset.is_active ? "border-orange-500 ring-2 ring-orange-200" : "border-line"}`}>
                    <img
                      src={asset.preview_url}
                      alt={asset.description?.subject ?? "Lesson visual"}
                      loading="lazy"
                      decoding="async"
                      className="w-full object-cover"
                      style={{ aspectRatio: `${asset.width} / ${asset.height}` }}
                    />
                    <div className="space-y-2 p-3">
                      <p className="line-clamp-2 text-sm font-semibold text-ink">{asset.description?.subject || asset.model}</p>
                      <p className="text-xs text-muted">{asset.model} · {(asset.byte_count / 1024).toFixed(0)} KB</p>
                      <button
                        type="button"
                        disabled={asset.is_active || libraryLoading}
                        onClick={() => activateLibraryAsset(asset.asset_id)}
                        className="focus-ring w-full rounded-lg bg-ink px-3 py-2 text-xs font-semibold text-white disabled:opacity-50"
                      >
                        {asset.is_active ? "Sedang digunakan" : "Gunakan gambar"}
                      </button>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
}
