"use client";

import { useEffect, useState } from "react";
import { Mic, TrendingUp } from "lucide-react";
import { readLatestSavedPractice, type SavedPractice } from "@/lib/practice-storage";

const skillLabels = [
  ["speaking", "Kejelasan"],
  ["fluency", "Kelancaran"],
  ["grammar", "Struktur"]
] as const;

export function SpeakingSkillSummary() {
  const [practice, setPractice] = useState<SavedPractice | null>(null);

  useEffect(() => {
    setPractice(readLatestSavedPractice()?.practice ?? null);
  }, []);

  const scores = practice?.lastSkillScores;
  const overall = practice?.lastScore ?? 0;

  return (
    <section className="mt-5 rounded-lg border border-ink/10 bg-white p-5 shadow-sm sm:p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Mic className="h-5 w-5 text-leaf" aria-hidden="true" />
            <p className="text-sm font-semibold uppercase text-leaf">Speaking snapshot</p>
          </div>
          <h2 className="mt-2 text-xl font-semibold">Kemampuan dari latihan terakhir</h2>
          <p className="mt-2 text-sm leading-6 text-ink/60">
            Skor ini berasal dari feedback roleplay terakhir dan dipakai untuk menentukan fokus latihanmu berikutnya.
          </p>
        </div>
        <div className="rounded-xl bg-mint px-5 py-3 text-center">
          <p className="text-xs font-semibold uppercase text-ink/55">Overall</p>
          <p className="mt-1 text-3xl font-semibold">{practice ? overall : "–"}</p>
        </div>
      </div>

      {scores ? (
        <div className="mt-5 grid gap-3 sm:grid-cols-3">
          {skillLabels.map(([key, label]) => (
            <div key={key} className="rounded-xl bg-paper p-4">
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-semibold">{label}</p>
                <p className="font-semibold text-leaf">{scores[key]}</p>
              </div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-ink/10">
                <div className="h-full rounded-full bg-leaf" style={{ width: `${scores[key]}%` }} />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="mt-5 flex items-start gap-3 rounded-xl bg-paper p-4 text-sm leading-6 text-ink/65">
          <TrendingUp className="mt-0.5 h-5 w-5 shrink-0 text-coral" aria-hidden="true" />
          <p>Selesaikan satu roleplay dengan suara atau teks untuk melihat baseline speaking-mu.</p>
        </div>
      )}
    </section>
  );
}
