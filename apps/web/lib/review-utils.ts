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

export function selectReviewLessonSlugs(lessons: LearningLessonSummary[], dateKey: string, count: number) {
  const completed = lessons
    .filter((lesson) => lesson.progressStatus === "completed")
    .slice()
    .sort((a, b) => {
      const aTime = a.updatedAt ? new Date(a.updatedAt).getTime() : 0;
      const bTime = b.updatedAt ? new Date(b.updatedAt).getTime() : 0;
      return bTime - aTime;
    });

  const pool = completed.length
    ? completed.map((lesson) => lesson.slug)
    : lessons.filter((lesson) => lesson.progressStatus !== "completed").map((lesson) => lesson.slug);

  const unique: string[] = [];
  for (const slug of pool) {
    if (unique.length >= count) {
      break;
    }
    if (!unique.includes(slug)) {
      unique.push(slug);
    }
  }

  if (unique.length < count) {
    const remaining = pool.filter((slug) => !unique.includes(slug));
    while (unique.length < count && remaining.length) {
      unique.push(remaining.shift() as string);
    }
  }

  return unique.slice(0, count).filter(Boolean);
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

