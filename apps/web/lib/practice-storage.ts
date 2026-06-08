import { getAuthSession } from "@/lib/auth-api";

export type SavedPractice = {
  sessionId?: string;
  completedTurns: number;
  totalTurns: number;
  completed: boolean;
  lastScore: number;
  updatedAt: string;
};

export const practiceStoragePrefix = "conversease.practice";
export const latestPracticeStorageKey = `${practiceStoragePrefix}.latest`;
export const defaultPracticeStorageKey = `${practiceStoragePrefix}.saying-hello-and-goodbye`;

export function practiceStorageKeyForLesson(lessonSlug: string) {
  return `${practiceStoragePrefix}.${lessonSlug}`;
}

function scopedStorageKey(baseKey = defaultPracticeStorageKey) {
  const session = getAuthSession();

  if (!session?.user.id) {
    return null;
  }

  return `${baseKey}.${session.user.id}`;
}

export function readSavedPractice(baseKey = defaultPracticeStorageKey): SavedPractice | null {
  const key = scopedStorageKey(baseKey);

  if (!key) {
    return null;
  }

  const raw = window.localStorage.getItem(key);

  if (!raw) {
    return null;
  }

  try {
    const value = JSON.parse(raw) as Partial<SavedPractice>;

    if (
      typeof value.completedTurns !== "number" ||
      typeof value.totalTurns !== "number" ||
      typeof value.completed !== "boolean" ||
      typeof value.lastScore !== "number" ||
      typeof value.updatedAt !== "string"
    ) {
      return null;
    }

    return {
      sessionId: value.sessionId,
      completedTurns: value.completedTurns,
      totalTurns: value.totalTurns,
      completed: value.completed,
      lastScore: value.lastScore,
      updatedAt: value.updatedAt
    };
  } catch {
    return null;
  }
}

export function saveSavedPractice(practice: SavedPractice, baseKey = defaultPracticeStorageKey) {
  const key = scopedStorageKey(baseKey);

  if (key) {
    window.localStorage.setItem(key, JSON.stringify(practice));
  }
}

export function removeSavedPractice(baseKey = defaultPracticeStorageKey) {
  const key = scopedStorageKey(baseKey);

  if (key) {
    window.localStorage.removeItem(key);
  }
}

export function readLatestPracticeSlug(): string | null {
  if (typeof window === "undefined") {
    return null;
  }

  const key = scopedStorageKey(latestPracticeStorageKey);
  if (!key) {
    return null;
  }

  const raw = window.localStorage.getItem(key);
  const value = raw?.trim();

  if (!value) {
    return null;
  }

  return value;
}

export function saveLatestPracticeSlug(lessonSlug: string) {
  const key = scopedStorageKey(latestPracticeStorageKey);
  if (!key) {
    return;
  }

  window.localStorage.setItem(key, lessonSlug);
}

function readPracticeForLesson(lessonSlug: string): SavedPractice | null {
  const direct = readSavedPractice(practiceStorageKeyForLesson(lessonSlug));
  if (direct) {
    return direct;
  }

  const legacyKey = `${defaultPracticeStorageKey}.${lessonSlug}`;
  const legacy = readSavedPractice(legacyKey);
  if (legacy) {
    saveSavedPractice(legacy, practiceStorageKeyForLesson(lessonSlug));
    removeSavedPractice(legacyKey);
    return legacy;
  }

  if (lessonSlug !== "saying-hello-and-goodbye") {
    return null;
  }

  const fallback = readSavedPractice(defaultPracticeStorageKey);
  if (fallback) {
    return fallback;
  }

  const duplicatedLegacy = readSavedPractice(`${defaultPracticeStorageKey}.saying-hello-and-goodbye`);
  if (duplicatedLegacy) {
    saveSavedPractice(duplicatedLegacy, practiceStorageKeyForLesson(lessonSlug));
    removeSavedPractice(`${defaultPracticeStorageKey}.saying-hello-and-goodbye`);
    return duplicatedLegacy;
  }

  return null;
}

export function readLatestSavedPractice(): { lessonSlug: string; practice: SavedPractice } | null {
  const latestSlug = readLatestPracticeSlug();
  if (latestSlug) {
    const practice = readPracticeForLesson(latestSlug);
    if (practice) {
      return { lessonSlug: latestSlug, practice };
    }
  }

  const session = getAuthSession();
  const userId = session?.user.id;
  if (!userId || typeof window === "undefined") {
    return null;
  }

  let best: { lessonSlug: string; practice: SavedPractice } | null = null;
  let bestTime = 0;

  for (let i = 0; i < window.localStorage.length; i += 1) {
    const key = window.localStorage.key(i);
    if (!key) {
      continue;
    }
    if (!key.startsWith(practiceStoragePrefix)) {
      continue;
    }
    if (!key.endsWith(`.${userId}`)) {
      continue;
    }

    const baseKey = key.slice(0, -(userId.length + 1));
    if (baseKey === latestPracticeStorageKey) {
      continue;
    }

    let candidateSlug: string | null = null;
    if (baseKey === defaultPracticeStorageKey) {
      candidateSlug = "saying-hello-and-goodbye";
    } else if (baseKey.startsWith(`${defaultPracticeStorageKey}.`)) {
      candidateSlug = baseKey.slice(`${defaultPracticeStorageKey}.`.length);
    } else if (baseKey.startsWith(`${practiceStoragePrefix}.`)) {
      candidateSlug = baseKey.slice(`${practiceStoragePrefix}.`.length);
    }

    if (!candidateSlug) {
      continue;
    }

    const practice = readSavedPractice(baseKey);
    if (!practice) {
      continue;
    }

    const time = new Date(practice.updatedAt).getTime();
    const score = Number.isNaN(time) ? 0 : time;
    if (score >= bestTime) {
      best = { lessonSlug: candidateSlug, practice };
      bestTime = score;
    }
  }

  if (best) {
    const migrated = readPracticeForLesson(best.lessonSlug) ?? best.practice;
    saveLatestPracticeSlug(best.lessonSlug);
    return { lessonSlug: best.lessonSlug, practice: migrated };
  }

  return null;
}
