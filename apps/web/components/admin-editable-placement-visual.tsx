"use client";
/* eslint-disable @next/next/no-img-element */

import { type ReactNode, useEffect, useRef, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Check, ClipboardCopy, Images, Link2, Loader2, Pencil, RefreshCw, Upload, X } from "lucide-react";
import { getAuthSession, onAuthSessionChanged } from "@/lib/auth-api";
import {
  getPlacementVisualLibrary,
  importPlacementVisual,
  regeneratePlacementVisual,
  selectPlacementVisual,
  uploadPlacementVisual,
  type PlacementVisualAsset,
  type VisualPlacementOwnerType,
  type VisualPlacementSlot
} from "@/lib/admin-visual-placement-api";

type Props = {
  ownerType: VisualPlacementOwnerType;
  ownerKey: string;
  slot: VisualPlacementSlot;
  label: string;
  prompt: string;
  children: ReactNode;
  wrapperClassName?: string;
  replacementClassName: string;
  sizes: string;
  href?: string;
};

export function AdminEditablePlacementVisual({
  ownerType,
  ownerKey,
  slot,
  label,
  prompt,
  children,
  wrapperClassName = "",
  replacementClassName,
  sizes,
  href
}: Props) {
  const target = { ownerType, ownerKey, slot } as const;
  const [isAdmin, setIsAdmin] = useState(false);
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [library, setLibrary] = useState<PlacementVisualAsset[] | null>(null);
  const [replacement, setReplacement] = useState<{ src: string; alt: string } | null>(null);
  const uploadInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const sync = () => setIsAdmin(getAuthSession()?.user.role === "admin");
    sync();
    return onAuthSessionChanged(sync);
  }, []);

  async function run(action: () => Promise<PlacementVisualAsset>, message: string) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const asset = await action();
      setReplacement({
        src: `/visual-assets/${asset.asset_id}?variant=original`,
        alt: asset.description?.subject || label
      });
      setLibrary(null);
      setOpen(false);
      setNotice(message);
    } catch (actionError) {
      setError(actionError instanceof Error ? actionError.message : "Operasi visual gagal.");
    } finally {
      setBusy(false);
      if (uploadInput.current) uploadInput.current.value = "";
    }
  }

  async function generate() {
    if (!window.confirm(`Generate visual baru untuk ${label}? Visual akan tetap hingga diganti manual.`)) return;
    await run(() => regeneratePlacementVisual(target, prompt), "Visual baru tersimpan dan dipasang permanen.");
  }

  async function importUrl() {
    const url = window.prompt("Paste URL gambar HTTPS. File akan diunduh dan disimpan ke S3.");
    if (!url?.trim()) return;
    await run(() => importPlacementVisual(target, prompt, url.trim()), "Gambar URL sudah disimpan dan dipasang.");
  }

  async function loadLibrary() {
    setBusy(true);
    setError("");
    try {
      const result = await getPlacementVisualLibrary(target);
      setLibrary(result.data.assets);
    } catch (libraryError) {
      setError(libraryError instanceof Error ? libraryError.message : "Library gagal dibuka.");
    } finally {
      setBusy(false);
    }
  }

  async function copyPrompt() {
    setBusy(true);
    setError("");
    try {
      await navigator.clipboard.writeText(prompt);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      setError("Prompt gagal disalin.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className={`relative ${wrapperClassName}`}>
      {replacement ? (
        <div className={`relative overflow-hidden bg-paper ${replacementClassName}`}>
          <Image src={replacement.src} alt={replacement.alt} fill sizes={sizes} className="object-cover" />
        </div>
      ) : children}

      {href ? (
        <Link href={href} aria-label={`Buka ${label}`} className="focus-ring absolute inset-0 z-10" />
      ) : null}

      {isAdmin ? (
        <button
          type="button"
          onClick={(event) => {
            event.preventDefault();
            event.stopPropagation();
            setOpen(true);
            setError("");
          }}
          className="focus-ring absolute right-2 top-2 z-20 inline-flex items-center gap-1.5 rounded-lg border border-white/70 bg-ink/90 px-3 py-2 text-xs font-semibold text-white shadow-soft backdrop-blur hover:bg-ink"
        >
          <Pencil className="h-3.5 w-3.5" />
          Edit visual
        </button>
      ) : null}

      {notice ? (
        <p className="absolute bottom-2 left-2 right-2 z-20 rounded-lg bg-emerald-950/90 px-3 py-2 text-xs font-medium text-white">
          {notice}
        </p>
      ) : null}

      {open ? (
        <div className="fixed inset-0 z-[70] flex items-center justify-center bg-black/60 p-4" onClick={() => !busy && setOpen(false)}>
          <div className="max-h-[88vh] w-full max-w-5xl overflow-auto rounded-2xl bg-white shadow-2xl" onClick={(event) => event.stopPropagation()}>
            <header className="sticky top-0 z-10 flex items-start justify-between gap-4 border-b border-line bg-white p-5">
              <div>
                <h2 className="text-lg font-bold text-ink">Edit visual</h2>
                <p className="mt-1 text-sm text-muted">{label} · manual/pinned · rasio 16:9</p>
              </div>
              <button type="button" disabled={busy} onClick={() => setOpen(false)} className="focus-ring rounded-lg p-2 hover:bg-sand">
                <X className="h-5 w-5" />
              </button>
            </header>

            <div className="space-y-5 p-5">
              <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-5">
                <ActionButton icon={copied ? Check : ClipboardCopy} label={copied ? "Copied" : "Copy prompt"} onClick={copyPrompt} disabled={busy} />
                <ActionButton icon={Upload} label="Upload image" onClick={() => uploadInput.current?.click()} disabled={busy} />
                <ActionButton icon={Link2} label="Import URL" onClick={importUrl} disabled={busy} />
                <ActionButton icon={Images} label="Library" onClick={loadLibrary} disabled={busy} />
                <ActionButton icon={RefreshCw} label="Generate" onClick={generate} disabled={busy} />
                <input
                  ref={uploadInput}
                  type="file"
                  accept="image/png,image/jpeg,image/webp"
                  className="sr-only"
                  onChange={(event) => {
                    const file = event.target.files?.[0];
                    if (file) void run(() => uploadPlacementVisual(target, prompt, file), "Upload tersimpan dan dipasang permanen.");
                  }}
                />
              </div>

              {busy ? <div className="flex justify-center py-8"><Loader2 className="h-7 w-7 animate-spin" /></div> : null}
              {error ? <p role="alert" className="rounded-lg bg-red-50 px-4 py-3 text-sm font-medium text-red-900">{error}</p> : null}

              {library && !busy ? (
                library.length ? (
                  <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {library.map((asset) => (
                      <article key={asset.asset_id} className={`overflow-hidden rounded-xl border ${asset.is_current ? "border-orange-500 ring-2 ring-orange-200" : "border-line"}`}>
                        <img src={asset.preview_url} alt={asset.description?.subject || "Visual library"} loading="lazy" className="aspect-video w-full object-cover" />
                        <div className="space-y-2 p-3">
                          <p className="line-clamp-2 text-sm font-semibold">{asset.description?.subject || asset.model}</p>
                          <p className="text-xs text-muted">{asset.model} · {(asset.byte_count / 1024).toFixed(0)} KB</p>
                          <button
                            type="button"
                            disabled={asset.is_current}
                            onClick={() => void run(() => selectPlacementVisual(target, asset.asset_id), "Gambar library sudah dipasang permanen.")}
                            className="focus-ring w-full rounded-lg bg-ink px-3 py-2 text-xs font-semibold text-white disabled:opacity-50"
                          >
                            {asset.is_current ? "Sedang digunakan" : "Gunakan gambar"}
                          </button>
                        </div>
                      </article>
                    ))}
                  </div>
                ) : <p className="py-10 text-center text-muted">Belum ada gambar hero 16:9 di library.</p>
              ) : null}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

function ActionButton({ icon: Icon, label, onClick, disabled }: { icon: typeof Upload; label: string; onClick: () => void; disabled: boolean }) {
  return (
    <button type="button" onClick={onClick} disabled={disabled} className="focus-ring inline-flex items-center justify-center gap-2 rounded-lg bg-ink px-3 py-2.5 text-xs font-semibold text-white disabled:opacity-60">
      <Icon className="h-4 w-4" />
      {label}
    </button>
  );
}
