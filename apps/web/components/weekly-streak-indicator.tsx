"use client";

import { useEffect, useMemo, useState } from "react";
import { CalendarDays } from "lucide-react";
import { getWeeklyStreak, getWeeklyStreakTarget } from "@/lib/weekly-streak";

const dayLabels = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"];

export function WeeklyStreakIndicator() {
  const target = useMemo(() => getWeeklyStreakTarget(), []);
  const [state, setState] = useState(() => getWeeklyStreak());

  useEffect(() => {
    function refresh() {
      setState(getWeeklyStreak());
    }
    refresh();
    window.addEventListener("weekly_streak_updated", refresh);
    window.addEventListener("storage", refresh);
    return () => {
      window.removeEventListener("weekly_streak_updated", refresh);
      window.removeEventListener("storage", refresh);
    };
  }, []);

  return (
    <div className="mt-5 rounded-lg bg-paper p-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <CalendarDays className="h-4 w-4 text-leaf" aria-hidden="true" />
            <p className="text-sm font-semibold">Minggu ini</p>
          </div>
          <p className="mt-2 text-2xl font-semibold">
            {state.count}/{target}
          </p>
          <p className="mt-1 text-sm text-ink/60">Target santai: {target} hari latihan.</p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-7 gap-2">
        {state.days.map((done, index) => (
          <div key={dayLabels[index]} className="text-center">
            <div className={`mx-auto h-3 w-3 rounded-full ${done ? "bg-leaf" : "bg-ink/15"}`} />
            <p className="mt-1 text-[11px] font-medium text-ink/60">{dayLabels[index]}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

