import { lessonsBySlug } from "@/lib/data";
import type { LearningLessonSummary, ReviewLessonContent } from "@/lib/learning-api";

export type ReviewItem = {
  lessonSlug: string;
  lessonTitle: string;
  unitTitle: string;
  phrase: string;
  pattern: string | null;
};

// Gated review content (phrases, patterns, dialogue, ...) is fetched from the
// Pro-gated API rather than bundled, so the helpers below take a slug-keyed map.
export type ReviewContentMap = Record<string, ReviewLessonContent>;

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

export function buildReviewItems(
  slugs: string[],
  dateKey: string,
  content: ReviewContentMap
): ReviewItem[] {
  return slugs
    .map((slug) => ({ slug, meta: lessonsBySlug[slug], body: content[slug] }))
    .filter((entry) => entry.meta && entry.body)
    .map(({ slug, meta, body }) => {
      const phraseIndex = stableIndex(`${dateKey}:${slug}:phrase`, body.phrases.length);
      const patternIndex = stableIndex(`${dateKey}:${slug}:pattern`, body.patterns.length || 1);
      const phrase = body.phrases[phraseIndex]?.phrase || body.dialogue[0]?.text || meta.title;
      const pattern = body.patterns.length ? body.patterns[patternIndex] : null;

      return {
        lessonSlug: slug,
        lessonTitle: meta.title,
        unitTitle: meta.unit,
        phrase,
        pattern
      };
    });
}

export function collectPatternBank(
  lessonSlugs: string[],
  limit: number,
  content: ReviewContentMap
) {
  const entries: { pattern: string; lessonSlug: string; lessonTitle: string; unitTitle: string }[] = [];
  for (const slug of lessonSlugs) {
    const meta = lessonsBySlug[slug];
    const body = content[slug];
    if (!meta || !body) {
      continue;
    }
    for (const pattern of body.patterns) {
      entries.push({ pattern, lessonSlug: slug, lessonTitle: meta.title, unitTitle: meta.unit });
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
