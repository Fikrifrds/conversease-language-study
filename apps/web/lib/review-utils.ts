import { lessonsBySlug } from "@/lib/data";
import type { LearningLessonSummary } from "@/lib/learning-api";

export type ReviewItem = {
  lessonSlug: string;
  lessonTitle: string;
  unitTitle: string;
  phrase: string;
  pattern: string | null;
};

function stableIndex(seed: string, size: number) {
  if (size <= 0) {
    return 0;
  }
  let hash = 0;
  for (let i = 0; i < seed.length; i += 1) {
    hash = (hash * 31 + seed.charCodeAt(i)) >>> 0;
  }
  return hash % size;
}

function stableScore(seed: string) {
  let hash = 0;
  for (let i = 0; i < seed.length; i += 1) {
    hash = (hash * 31 + seed.charCodeAt(i)) >>> 0;
  }
  return hash;
}

export function selectReviewLessonSlugs(lessons: LearningLessonSummary[], dateKey: string, count: number) {
  const completed = lessons.filter((lesson) => lesson.progressStatus === "completed");
  const inProgress = lessons.filter((lesson) => lesson.progressStatus !== "completed");

  const completedSorted = completed
    .slice()
    .sort((a, b) => {
      const aTime = a.updatedAt ? new Date(a.updatedAt).getTime() : 0;
      const bTime = b.updatedAt ? new Date(b.updatedAt).getTime() : 0;
      return aTime - bTime;
    });

  const oldest = completedSorted.slice(0, Math.min(2, completedSorted.length));
  const newest = completedSorted.slice(-Math.min(1, completedSorted.length));

  const selected: string[] = [];
  for (const lesson of [...oldest, ...newest]) {
    if (!selected.includes(lesson.slug)) {
      selected.push(lesson.slug);
    }
  }

  const remainingCompleted = completedSorted
    .filter((lesson) => !selected.includes(lesson.slug))
    .slice()
    .sort((a, b) => stableScore(`${dateKey}:${a.slug}`) - stableScore(`${dateKey}:${b.slug}`));

  for (const lesson of remainingCompleted) {
    if (selected.length >= count) {
      break;
    }
    selected.push(lesson.slug);
  }

  if (selected.length < count) {
    const fallback = inProgress
      .slice()
      .sort((a, b) => stableScore(`${dateKey}:${a.slug}`) - stableScore(`${dateKey}:${b.slug}`));
    for (const lesson of fallback) {
      if (selected.length >= count) {
        break;
      }
      if (!selected.includes(lesson.slug)) {
        selected.push(lesson.slug);
      }
    }
  }

  return selected.slice(0, count).filter(Boolean);
}

export function buildReviewItems(slugs: string[], dateKey: string): ReviewItem[] {
  return slugs
    .map((slug) => lessonsBySlug[slug])
    .filter(Boolean)
    .map((lesson) => {
      const phraseIndex = stableIndex(`${dateKey}:${lesson.slug}:phrase`, lesson.phrases.length);
      const patternIndex = stableIndex(`${dateKey}:${lesson.slug}:pattern`, lesson.patterns.length || 1);
      const phrase = lesson.phrases[phraseIndex]?.phrase || lesson.dialogue[0]?.text || lesson.title;
      const pattern = lesson.patterns.length ? lesson.patterns[patternIndex] : null;

      return {
        lessonSlug: lesson.slug,
        lessonTitle: lesson.title,
        unitTitle: lesson.unit,
        phrase,
        pattern
      };
    });
}

export function collectPatternBank(lessonSlugs: string[], limit: number) {
  const entries: { pattern: string; lessonSlug: string; lessonTitle: string; unitTitle: string }[] = [];
  for (const slug of lessonSlugs) {
    const lesson = lessonsBySlug[slug];
    if (!lesson) {
      continue;
    }
    for (const pattern of lesson.patterns) {
      entries.push({ pattern, lessonSlug: slug, lessonTitle: lesson.title, unitTitle: lesson.unit });
    }
  }

  const seen = new Set<string>();
  const unique: typeof entries = [];
  for (const entry of entries) {
    const key = `${entry.pattern}`;
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    unique.push(entry);
    if (unique.length >= limit) {
      break;
    }
  }
  return unique;
}
