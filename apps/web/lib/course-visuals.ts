import { lessonsBySlug } from "@/lib/data";

type LessonRef = {
  slug: string;
};

type UnitRef = {
  lessons: LessonRef[];
};

type CourseRef = {
  slug?: string;
  units: UnitRef[];
};

type CourseVisual = {
  src: string;
  width: number;
  height: number;
  alt: string;
};

const HERO_WIDTH = 1672;
const HERO_HEIGHT = 941;
const CARD_SIZE = 1254;

const COURSE_VISUAL_SETS: Record<string, Array<[string, "hero" | "card-1" | "card-2" | "card-3"]>> = {
  "english-a1-start-simple-conversations": [
    ["classroom-male", "hero"],
    ["service-male", "card-1"],
    ["travel-male", "card-2"]
  ],
  "english-a2-everyday-conversations": [
    ["travel-male", "hero"],
    ["health-male", "card-1"],
    ["service-male", "card-2"]
  ],
  "english-b1-confident-everyday-speaking": [
    ["travel-male", "card-1"],
    ["workplace-male", "hero"],
    ["classroom-male", "card-3"]
  ],
  "english-b2-professional-discussions": [
    ["workplace-male", "card-1"],
    ["service-male", "card-3"],
    ["classroom-male", "card-2"]
  ],
  "english-c1-advanced-fluency": [
    ["workplace-male", "hero"],
    ["workplace-male", "card-2"],
    ["classroom-male", "card-1"]
  ],
  "arabic-a1-fusha-foundations": [
    ["classroom-female", "hero"],
    ["service-male", "card-1"],
    ["travel-female", "card-2"]
  ],
  "arabic-a2-everyday-conversations": [
    ["travel-male", "hero"],
    ["health-female", "card-1"],
    ["service-male", "card-2"]
  ],
  "arabic-b1-connected-conversations": [
    ["travel-female", "card-1"],
    ["workplace-male", "hero"],
    ["classroom-female", "card-3"]
  ],
  "arabic-b2-professional-discussions": [
    ["workplace-female", "card-1"],
    ["service-male", "card-3"],
    ["classroom-female", "card-2"]
  ],
  "arabic-c1-advanced-fluency": [
    ["workplace-male", "hero"],
    ["workplace-female", "card-2"],
    ["classroom-male", "card-1"]
  ]
};

export function lessonHeroVisual(lessonSlug: string) {
  return lessonsBySlug[lessonSlug]?.visuals?.hero ?? null;
}

export function unitHeroVisual(unit: UnitRef) {
  const firstVisualLesson = unit.lessons.find((lesson) => lessonHeroVisual(lesson.slug));
  return firstVisualLesson ? lessonHeroVisual(firstVisualLesson.slug) : null;
}

export function courseHeroVisuals(course: CourseRef, maxCount = 3) {
  const curatedVisuals = curatedCourseVisuals(course.slug);
  if (curatedVisuals.length) {
    return curatedVisuals.slice(0, maxCount);
  }

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

function curatedCourseVisuals(slug?: string): CourseVisual[] {
  if (!slug) {
    return [];
  }

  return (COURSE_VISUAL_SETS[slug] ?? []).map(([scene, asset]) => {
    const isHero = asset === "hero";
    const filename = isHero ? "hero.png" : `${asset}.png`;
    const sceneLabel = scene.replace("-", " ");
    return {
      src: `/images/lesson-visual-library/${scene}/${filename}`,
      width: isHero ? HERO_WIDTH : CARD_SIZE,
      height: isHero ? HERO_HEIGHT : CARD_SIZE,
      alt: `Ilustrasi ${sceneLabel} untuk ringkasan course.`
    };
  });
}
