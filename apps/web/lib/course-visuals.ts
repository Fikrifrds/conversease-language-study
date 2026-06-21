import { lessonsBySlug } from "@/lib/data";

type LessonRef = {
  slug: string;
};

type UnitRef = {
  lessons: LessonRef[];
};

type CourseRef = {
  units: UnitRef[];
};

export function lessonHeroVisual(lessonSlug: string) {
  return lessonsBySlug[lessonSlug]?.visuals?.hero ?? null;
}

export function unitHeroVisual(unit: UnitRef) {
  const firstVisualLesson = unit.lessons.find((lesson) => lessonHeroVisual(lesson.slug));
  return firstVisualLesson ? lessonHeroVisual(firstVisualLesson.slug) : null;
}

export function courseHeroVisuals(course: CourseRef, maxCount = 3) {
  const seen = new Set<string>();
  const visuals = [];

  for (const unit of course.units) {
    const visual = unitHeroVisual(unit);
    if (!visual || seen.has(visual.src)) {
      continue;
    }
    visuals.push(visual);
    seen.add(visual.src);
    if (visuals.length >= maxCount) {
      break;
    }
  }

  return visuals;
}

export function courseHeroVisual(course: CourseRef) {
  return courseHeroVisuals(course, 1)[0] ?? null;
}
