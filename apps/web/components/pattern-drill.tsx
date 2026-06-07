"use client";

import { useMemo, useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

const slots: Record<string, string[]> = {
  adjective: ["good", "happy", "tired", "busy", "ready", "excited", "nervous", "okay"],
  name: ["Alya", "Ben", "Mina", "Ilham", "Faris", "Dimas", "Siti", "Rina"],
  place: ["Indonesia", "Jakarta", "Bandung", "Surabaya", "Bali", "Singapore", "Malaysia", "Japan"],
  time: ["today", "tomorrow", "this morning", "this afternoon", "tonight", "at 7", "at 9", "next week"],
  event: ["the class", "the meeting", "the interview", "the appointment", "the call", "the flight"],
  role: ["a student", "a teacher", "an engineer", "a designer", "a manager", "a customer"],
  subject: ["English", "math", "design", "coding", "marketing", "history"],
  noun: ["the details", "the address", "the schedule", "the plan", "the price", "the problem"],
  verb: ["help", "repeat that", "send it", "explain", "check", "confirm"],
  detail: ["two two five five", "Ben", "dot com", "nine o'clock", "tomorrow", "online"]
};

function stablePick(seed: string, items: string[]) {
  if (!items.length) {
    return "";
  }
  let hash = 0;
  for (let i = 0; i < seed.length; i += 1) {
    hash = (hash * 31 + seed.charCodeAt(i)) >>> 0;
  }
  return items[hash % items.length] ?? items[0] ?? "";
}

function normalizeSlotKey(raw: string) {
  const cleaned = raw.trim().toLowerCase();
  if (cleaned.includes("place")) return "place";
  if (cleaned.includes("name")) return "name";
  if (cleaned.includes("time")) return "time";
  if (cleaned.includes("event")) return "event";
  if (cleaned.includes("role")) return "role";
  if (cleaned.includes("subject")) return "subject";
  if (cleaned.includes("adjective") || cleaned.includes("adj")) return "adjective";
  if (cleaned.includes("verb")) return "verb";
  if (cleaned.includes("detail")) return "detail";
  if (cleaned.includes("noun")) return "noun";
  return "noun";
}

function substitute(pattern: string, seed: string) {
  let out = pattern;
  const matches = Array.from(pattern.matchAll(/\+\s*([a-zA-Z_-]+)/g));
  if (!matches.length) {
    return pattern;
  }
  for (const match of matches) {
    const slotKey = normalizeSlotKey(match[1] ?? "");
    const replacement = stablePick(`${seed}:${slotKey}`, slots[slotKey] ?? slots.noun);
    out = out.replace(match[0], replacement);
  }
  return out.replace(/\s{2,}/g, " ").trim();
}

export function PatternDrill({
  pattern,
  seedKey,
  defaultOpen = false
}: {
  pattern: string;
  seedKey: string;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);

  const variations = useMemo(() => {
    const items: string[] = [];
    for (let i = 0; i < 5; i += 1) {
      items.push(substitute(pattern, `${seedKey}:${i}`));
    }
    return items;
  }, [pattern, seedKey]);

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
            Ucapkan 2 kalimat baru memakai pola yang sama. Mulai dari contoh berikut:
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

