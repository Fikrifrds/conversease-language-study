"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { CheckCircle2, Headphones, Mic2, Play } from "lucide-react";
import { LandingWaveform } from "@/components/landing-waveform";
import { mission } from "@/lib/data";


/**
 * Animated conversation preview for the hero.
 *
 * Loops through a realistic listen -> think -> reply -> feedback beat so the
 * product's core loop plays out visually:
 *   0  partner prompt is "speaking" (waveform live)
 *   1  typing dots (you're composing a reply)
 *   2  your reply + "Clear" badge pop in
 *   3  feedback panel slides in
 *   -> back to 0
 */
export function LandingHeroPreview() {
  const [phase, setPhase] = useState(0);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const next = [1, 2, 3, 0];
    const wait = [2200, 1300, 1500, 3400];
    timer.current = setTimeout(() => setPhase(next[phase]), wait[phase]);
    return () => {
      if (timer.current) {
        clearTimeout(timer.current);
      }
    };
  }, [phase]);

  const isSpeaking = phase === 0;
  const isTyping = phase === 1;
  const hasReplied = phase === 2 || phase === 3;
  const showFeedback = phase === 3;

  return (
    <div
      className="relative overflow-hidden rounded-[2rem] border border-ink/10 bg-ink p-3 shadow-[0_30px_80px_rgba(124,45,18,0.2)] sm:p-5"
      aria-label="Pratinjau latihan percakapan Conversease"
    >
      <div className="hero-aurora pointer-events-none absolute inset-0 opacity-40" aria-hidden="true" />

      <div className="relative overflow-hidden rounded-[1.4rem] border border-white/10 bg-paper">
        <div className="flex items-center gap-3 border-b border-ink/10 bg-white px-4 py-3 sm:px-5">
          <div className="flex gap-1.5" aria-hidden="true">
            <span className="h-2.5 w-2.5 rounded-full bg-leaf" />
            <span className="h-2.5 w-2.5 rounded-full bg-sun" />
            <span className="h-2.5 w-2.5 rounded-full bg-ink/15" />
          </div>
          <div className="min-w-0 flex-1 rounded-full bg-paper px-3 py-1.5 text-center text-[0.65rem] font-medium text-ink/40 sm:text-xs">
            conversease.app / practice
          </div>
          <span className="hidden text-xs font-semibold text-ink/45 sm:inline">Lesson</span>
        </div>

        <div className="p-4 sm:p-6">
          <div className="animate-rise flex items-start justify-between gap-4" style={{ animationDelay: "120ms" }}>
            <div className="min-w-0">
              <p className="text-[0.65rem] font-semibold uppercase tracking-[0.14em] text-coral">Misi hari ini</p>
              <h2 className="mt-1 text-lg font-semibold leading-tight sm:text-2xl">{mission.title}</h2>
            </div>
            <span className="shrink-0 rounded-full bg-sun px-3 py-1 text-xs font-bold text-ink">{mission.level}</span>
          </div>

          <div className="animate-rise mt-4 rounded-2xl border border-ink/10 bg-white p-4 shadow-sm sm:p-5" style={{ animationDelay: "220ms" }}>
            <div className="flex items-center justify-between gap-3">
              <span className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.12em] text-coral">
                <Headphones className="h-4 w-4" aria-hidden="true" />
                Listen &amp; reply
              </span>
              <button
                className="grid h-8 w-8 place-items-center rounded-full bg-mint text-leaf transition hover:scale-110 hover:bg-leaf hover:text-white"
                type="button"
                aria-label="Putar dialog contoh"
              >
                <Play className="h-3.5 w-3.5 fill-current" aria-hidden="true" />
              </button>
            </div>
            <p className="mt-3 text-base font-semibold leading-snug sm:text-xl">
              “Good morning. How are you?”
            </p>
            <p className="mt-1 hidden text-sm text-ink/50 sm:block">
              Selamat pagi. Apa kabar?
            </p>

            <LandingWaveform active={isSpeaking} />

            {isTyping ? (
              <div className="mt-3 flex items-center gap-1.5 rounded-2xl bg-paper px-4 py-3" aria-label="Sedang mengetik">
                {[0, 1, 2].map((dot) => (
                  <span
                    key={dot}
                    className="typing-dot h-2 w-2 rounded-full bg-leaf"
                    style={{ animationDelay: `${dot * 160}ms` }}
                  />
                ))}
                <span className="ml-1 text-xs text-ink/40">menyusun respons…</span>
              </div>
            ) : null}
          </div>

          {hasReplied ? (
            <div className="animate-bubble-in mt-3 grid grid-cols-[1fr_auto] gap-3">
              <div className="rounded-2xl border border-ink/10 bg-white px-4 py-3">
                <p className="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-ink/35">Your response</p>
                <p className="mt-1 text-sm font-semibold sm:text-base">I’m good, thank you. Nice to meet you.</p>
              </div>
              <div className="grid min-w-20 place-items-center rounded-2xl bg-mint px-3 text-center">
                <CheckCircle2 className="animate-pop h-5 w-5 text-leaf" aria-hidden="true" />
                <span className="text-[0.65rem] font-semibold text-coral">Clear</span>
              </div>
            </div>
          ) : null}

          {showFeedback ? (
            <div className="animate-bubble-in mt-3 flex items-center gap-3 rounded-2xl bg-[#fde7df] px-4 py-3 text-sm">
              <span className="relative grid h-8 w-8 shrink-0 place-items-center rounded-full bg-white text-leaf">
                <Mic2 className="h-4 w-4" aria-hidden="true" />
                <span className="mic-pulse-ring absolute inset-0 rounded-full bg-leaf/40" aria-hidden="true" />
              </span>
              <div className="min-w-0">
                <p className="font-semibold text-coral">Feedback langsung</p>
                <p className="truncate text-xs text-ink/55">Responsmu sudah natural dan mudah dipahami.</p>
              </div>
            </div>
          ) : null}

          <Link
            href={`/lessons/${mission.lessonSlug}`}
            className="focus-ring group relative mt-3 inline-flex w-full items-center justify-center gap-2 overflow-hidden rounded-xl bg-leaf px-4 py-3 text-sm font-semibold text-white transition hover:bg-ink"
          >
            <span className="cta-sheen pointer-events-none absolute inset-0" aria-hidden="true" />
            <Play className="h-4 w-4 transition group-hover:translate-x-0.5" aria-hidden="true" />
            Mulai Misi Gratis
          </Link>
        </div>
      </div>
    </div>
  );
}
