"use client";

import { useMemo, useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

function sentenceCase(text: string) {
  if (!text) {
    return text;
  }
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function scaffoldFromPattern(pattern: string) {
  const replaced = pattern.replace(/\+\s*([a-zA-Z_-]+)/g, (_, rawSlot: string) => {
    const label = rawSlot.replace(/[_-]+/g, " ").trim().toLowerCase();
    return `[${label}]`;
  });
  return sentenceCase(replaced.replace(/\s{2,}/g, " ").trim());
}

function blankFromPattern(pattern: string) {
  const replaced = pattern.replace(/\+\s*[a-zA-Z_-]+/g, "_____");
  return sentenceCase(replaced.replace(/\s{2,}/g, " ").trim());
}

export function PatternDrill({
  pattern,
  example,
  seedKey,
  defaultOpen = false
}: {
  pattern: string;
  example?: string;
  seedKey: string;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);

  const variations = useMemo(() => {
    const items = [example?.trim(), scaffoldFromPattern(pattern), blankFromPattern(pattern)].filter(Boolean);
    return Array.from(new Set(items));
  }, [example, pattern, seedKey]);

  return (
    <div className="mt-3 rounded-lg border border-ink/10 bg-white p-4">
      <button
        type="button"
        onClick={() => setOpen((current) => !current)}
        className="focus-ring flex w-full items-center justify-between gap-3 text-left"
      >
        <span className="text-sm font-semibold text-ink">Latihan variasi (1 menit)</span>
        {open ? <ChevronUp className="h-4 w-4 text-ink/60" aria-hidden="true" /> : <ChevronDown className="h-4 w-4 text-ink/60" aria-hidden="true" />}
      </button>

      {open ? (
        <div className="mt-3 space-y-3">
          <p className="text-sm leading-6 text-ink/60">
            Ucapkan 2 kalimat baru memakai pola yang sama. Mulai dari scaffold lesson berikut:
          </p>
          <ul className="list-disc space-y-1 pl-5 text-sm leading-6 text-ink/75">
            {variations.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
