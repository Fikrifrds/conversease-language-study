"use client";

import { useEffect, useRef, useState } from "react";

type Stat = {
  /** Raw display value, e.g. "200+", "A1–C1", "Indonesia". */
  value: string;
  label: string;
};

const STATS: Stat[] = [
  { value: "200+", label: "lesson percakapan" },
  { value: "A1–C1", label: "jalur CEFR lengkap" },
  { value: "Indonesia", label: "bahasa feedback" }
];

/** Parses a leading integer + suffix (e.g. "200+" -> { target: 200, suffix: "+" }). */
function parseNumeric(value: string): { target: number; suffix: string } | null {
  const match = value.match(/^(\d+)(.*)$/);
  if (!match) {
    return null;
  }
  return { target: Number(match[1]), suffix: match[2] };
}

const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);

function useCountUp(target: number, active: boolean, duration = 1400) {
  const [value, setValue] = useState(0);

  useEffect(() => {
    if (!active || target <= 0) {
      return;
    }

    let raf = 0;
    const start = performance.now();

    function tick(now: number) {
      const progress = Math.min((now - start) / duration, 1);
      setValue(Math.round(easeOutCubic(progress) * target));
      if (progress < 1) {
        raf = requestAnimationFrame(tick);
      }
    }

    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, active, duration]);

  return value;
}

function StatCard({ stat, active, className = "" }: { stat: Stat; active: boolean; className?: string }) {
  const parsed = parseNumeric(stat.value);
  const counted = useCountUp(parsed?.target ?? 0, active && parsed !== null);
  const display = parsed !== null ? `${counted}${parsed.suffix}` : stat.value;

  return (
    <div className={className}>
      <dt className="text-lg font-semibold leading-none text-ink sm:text-xl">{display}</dt>
      <dd className="mt-1.5 text-[0.7rem] font-medium leading-4 text-ink/55 sm:text-xs">{stat.label}</dd>
    </div>
  );
}

/**
 * Animated stat row. Cards lift in with a stagger; the numeric stat (e.g. "200+")
 * counts up when the row scrolls into view. Non-numeric values render as-is.
 */
export function LandingStats({ className = "" }: { className?: string }) {
  const ref = useRef<HTMLDListElement | null>(null);
  const [active, setActive] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) {
      return;
    }

    if (typeof IntersectionObserver === "undefined") {
      setActive(true);
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActive(true);
            observer.disconnect();
            break;
          }
        }
      },
      { threshold: 0.4 }
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  return (
    <dl ref={ref} className={className}>
      {STATS.map((stat, index) => (
        <div
          key={stat.label}
          className={`rounded-xl bg-paper/90 px-3 py-4 sm:px-4 ${
            active ? "animate-bubble-in" : "opacity-0"
          }`}
          style={{ animationDelay: `${index * 120}ms` }}
        >
          <StatCard stat={stat} active={active} />
        </div>
      ))}
    </dl>
  );
}
