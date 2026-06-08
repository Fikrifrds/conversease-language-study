type WeeklyStreakState = {
  days: number[];
  updatedAt: string;
};

function pad2(value: number) {
  return String(value).padStart(2, "0");
}

function localDateKey(date: Date) {
  return `${date.getFullYear()}-${pad2(date.getMonth() + 1)}-${pad2(date.getDate())}`;
}

function startOfWeek(date: Date) {
  const copy = new Date(date);
  copy.setHours(0, 0, 0, 0);
  const day = copy.getDay();
  const diff = (day + 6) % 7;
  copy.setDate(copy.getDate() - diff);
  return copy;
}

function dayIndexFromMonday(date: Date) {
  const day = date.getDay();
  return (day + 6) % 7;
}

function storageKeyFor(weekKey: string) {
  return `streak.weekly.${weekKey}`;
}

export function getWeeklyStreakTarget() {
  return 3;
}

export function getWeeklyStreak(today: Date = new Date()) {
  const weekStart = startOfWeek(today);
  const weekKey = localDateKey(weekStart);
  const key = storageKeyFor(weekKey);

  if (typeof window === "undefined") {
    return { weekKey, days: Array.from({ length: 7 }, () => false), count: 0 };
  }

  try {
    const raw = window.localStorage.getItem(key);
    const parsed = raw ? (JSON.parse(raw) as WeeklyStreakState) : null;
    const seen = new Set<number>((parsed?.days ?? []).filter((d) => Number.isInteger(d) && d >= 0 && d <= 6));
    const days = Array.from({ length: 7 }, (_, index) => seen.has(index));
    return { weekKey, days, count: days.filter(Boolean).length };
  } catch {
    return { weekKey, days: Array.from({ length: 7 }, () => false), count: 0 };
  }
}

export function markStudyDay(today: Date = new Date()) {
  if (typeof window === "undefined") {
    return;
  }

  const weekKey = localDateKey(startOfWeek(today));
  const dayIndex = dayIndexFromMonday(today);
  const key = storageKeyFor(weekKey);

  try {
    const existingRaw = window.localStorage.getItem(key);
    const existing = existingRaw ? (JSON.parse(existingRaw) as WeeklyStreakState) : null;
    const set = new Set<number>((existing?.days ?? []).filter((d) => Number.isInteger(d) && d >= 0 && d <= 6));
    set.add(dayIndex);
    const payload: WeeklyStreakState = {
      days: Array.from(set).sort((a, b) => a - b),
      updatedAt: new Date().toISOString()
    };
    window.localStorage.setItem(key, JSON.stringify(payload));
    window.dispatchEvent(new Event("weekly_streak_updated"));
  } catch {}
}

