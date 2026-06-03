import { getAuthSession } from "@/lib/auth-api";

export type SavedPractice = {
  sessionId?: string;
  completedTurns: number;
  totalTurns: number;
  completed: boolean;
  lastScore: number;
  updatedAt: string;
};

export const defaultPracticeStorageKey = "conversease.practice.saying-hello-and-goodbye";

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
