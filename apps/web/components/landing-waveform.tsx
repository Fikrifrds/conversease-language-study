"use client";

import { useEffect, useRef } from "react";

const BAR_COUNT = 28;
const ROLL_INTERVAL = 110; // ms between new target amplitudes
const LERP = 0.28; // smoothing per frame (higher = snappier)

/**
 * A speech-like audio waveform driven by requestAnimationFrame.
 *
 * CSS keyframes can only loop a fixed, repeating pattern, which always reads
 * as synthetic. Instead we simulate a voiceprint: every ~110ms we roll a new
 * "energy" burst (with occasional pauses, like gaps between words) and per-bar
 * amplitudes (a sin envelope so the middle is louder, times random noise), then
 * smoothly interpolate each bar toward its target every frame. The result never
 * repeats and behaves like real speech — lively while `active`, settling to a
 * low baseline when nobody is speaking.
 *
 * Bars scale from their vertical center (transform-origin: center) so they grow
 * symmetrically, like a proper waveform segment. Under prefers-reduced-motion
 * the loop is skipped and bars render at a calm static height.
 */
export function LandingWaveform({ active }: { active: boolean }) {
  const barsRef = useRef<Array<HTMLSpanElement | null>>([]);
  const rafRef = useRef<number | null>(null);
  const lastRollRef = useRef(0);
  const targetsRef = useRef<number[]>(new Array(BAR_COUNT).fill(0.3));
  const currentRef = useRef<number[]>(new Array(BAR_COUNT).fill(0.3));

  useEffect(() => {
    const reduced =
      typeof window !== "undefined" &&
      typeof window.matchMedia === "function" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function applyHeights() {
      const bars = barsRef.current;
      const cur = currentRef.current;
      for (let i = 0; i < bars.length; i++) {
        const el = bars[i];
        if (el) {
          el.style.transform = `scaleY(${cur[i]})`;
        }
      }
    }

    if (reduced) {
      const cur = currentRef.current;
      for (let i = 0; i < BAR_COUNT; i++) {
        cur[i] = 0.14 + 0.1 * Math.sin((Math.PI * i) / (BAR_COUNT - 1));
      }
      applyHeights();
      return;
    }

    // A new "syllable": a burst of energy, or occasionally a pause.
    function rollEnergy() {
      if (Math.random() < 0.16) {
        return 0.08 + Math.random() * 0.14; // brief pause / dip between words
      }
      return 0.55 + Math.random() * 0.45; // active burst
    }

    function rollTargets() {
      const energy = active ? rollEnergy() : 0;
      const tgt = targetsRef.current;
      for (let i = 0; i < BAR_COUNT; i++) {
        const shape = Math.sin((Math.PI * i) / (BAR_COUNT - 1)); // 0..1..0 envelope
        const noise = 0.4 + Math.random() * 0.6;
        const amp = active ? energy * (0.25 + 0.75 * shape) * noise : 0.05;
        tgt[i] = Math.min(1, Math.max(0.04, amp));
      }
    }

    function tick(now: number) {
      if (now - lastRollRef.current > ROLL_INTERVAL) {
        lastRollRef.current = now;
        rollTargets();
      }

      const cur = currentRef.current;
      const tgt = targetsRef.current;
      let settling = false;
      for (let i = 0; i < BAR_COUNT; i++) {
        const delta = tgt[i] - cur[i];
        cur[i] += delta * LERP;
        if (Math.abs(delta) > 0.004) {
          settling = true;
        }
      }
      applyHeights();

      // Keep animating while speaking, or until bars have settled to baseline.
      if (active || settling) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        rafRef.current = null;
      }
    }

    lastRollRef.current = performance.now();
    rollTargets();
    rafRef.current = requestAnimationFrame(tick);

    return () => {
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
      }
    };
  }, [active]);

  return (
    <div className="flex h-10 items-center gap-1 overflow-visible" style={{ height: 40, minHeight: 40 }} aria-hidden="true">
      {Array.from({ length: BAR_COUNT }).map((_, i) => (
        <span
          key={i}
          ref={(el) => {
            barsRef.current[i] = el;
          }}
          className="h-full flex-1 rounded-full bg-leaf"
          style={{
            transform: "scaleY(0.3)",
            transformOrigin: "center",
            opacity: 0.5 + 0.5 * Math.sin((Math.PI * i) / (BAR_COUNT - 1))
          }}
        />
      ))}
    </div>
  );
}
