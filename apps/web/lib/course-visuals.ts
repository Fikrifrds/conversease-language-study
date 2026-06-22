import { lessonsBySlug } from "@/lib/data";

type LessonRef = {
  slug: string;
};

type UnitRef = {
  title?: string;
  outcome?: string;
  lessons: LessonRef[];
};

type CourseRef = {
  slug?: string;
  language?: string;
  units: UnitRef[];
};

type VisualAsset = "hero" | "card-1" | "card-2" | "card-3";
type SceneBase = "classroom" | "health" | "service" | "travel" | "workplace";
type VisualScene = `${SceneBase}-${"female" | "male"}`;
type VisualSpec = [VisualScene, VisualAsset];

type CourseVisual = {
  src: string;
  width: number;
  height: number;
  alt: string;
};

const HERO_WIDTH = 1672;
const HERO_HEIGHT = 941;
const CARD_SIZE = 1254;

const COURSE_VISUAL_SETS: Record<string, VisualSpec[]> = {
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

const DEFAULT_UNIT_BASE_SETS: SceneBase[][] = [
  ["classroom", "service", "travel"],
  ["service", "workplace", "classroom"],
  ["travel", "classroom", "service"],
  ["workplace", "classroom", "service"],
  ["travel", "service", "classroom"],
  ["service", "travel", "workplace"],
  ["health", "service", "classroom"],
  ["classroom", "travel", "workplace"]
];

const UNIT_TOPIC_BASE_SETS: Array<{ pattern: RegExp; bases: SceneBase[] }> = [
  {
    pattern: /foundation|greeting|introduc|class|instruction/i,
    bases: ["classroom", "service", "travel"]
  },
  {
    pattern: /social|small talk|follow-up|weekend|plan|invitation|invite|accept|declin|reschedule/i,
    bases: ["classroom", "service", "travel"]
  },
  {
    pattern: /health|symptom|appointment/i,
    bases: ["health", "service", "classroom"]
  },
  {
    pattern: /travel|transport|direction|\bplaces?\b|checking in|ticket|departure|delay|recommendation/i,
    bases: ["travel", "service", "classroom"]
  },
  {
    pattern: /contact|phone|email|number/i,
    bases: ["service", "workplace", "classroom"]
  },
  {
    pattern: /food|drink|shopping|prices|service|customer|client/i,
    bases: ["service", "travel", "workplace"]
  },
  {
    pattern: /story|stories|past|experience|routine|time|preference|goal|progress/i,
    bases: ["classroom", "travel", "workplace"]
  },
  {
    pattern: /clear argument|nuanced|opinion|debate|analysis|media|information|listening|response|certainty|doubt|viewpoint|evidence/i,
    bases: ["classroom", "workplace", "travel"]
  },
  {
    pattern: /negotiation|compromise|client|customer|concern|option/i,
    bases: ["service", "workplace", "travel"]
  },
  {
    pattern: /presenting|presentation|presentations|present /i,
    bases: ["classroom", "workplace", "service"]
  },
  {
    pattern: /work|study|meeting|professional|negotiation|presentation|leadership|stakeholder|task|feedback|argument|proposal|priority/i,
    bases: ["workplace", "classroom", "service"]
  },
  {
    pattern: /problem|help|request|solution|tradeoff|cause|framing/i,
    bases: ["health", "service", "workplace"]
  },
  {
    pattern: /community|culture|family|cross-cultural|local norm/i,
    bases: ["travel", "classroom", "service"]
  }
];

const UNIT_ASSET_PATTERNS: VisualAsset[][] = [
  ["hero", "card-1", "card-2"],
  ["card-1", "hero", "card-3"],
  ["card-2", "hero", "card-1"],
  ["hero", "card-2", "card-3"],
  ["card-3", "card-1", "hero"],
  ["card-2", "card-3", "hero"],
  ["hero", "card-3", "card-1"],
  ["card-1", "card-2", "hero"]
];

export function lessonHeroVisual(lessonSlug: string) {
  return lessonsBySlug[lessonSlug]?.visuals?.hero ?? null;
}

export function unitHeroVisual(unit: UnitRef) {
  return unitHeroVisuals(unit, 1)[0] ?? null;
}

export function courseUnitVisuals(course: CourseRef, unit: UnitRef, unitIndex: number, maxCount = 3) {
  const curatedVisuals = curatedUnitVisuals(course, unit, unitIndex);
  if (curatedVisuals.length) {
    return curatedVisuals.slice(0, maxCount);
  }

  return unitHeroVisuals(unit, maxCount);
}

export function unitHeroVisuals(unit: UnitRef, maxCount = 3) {
  const seen = new Set<string>();
  const visuals: CourseVisual[] = [];

  for (const lesson of unit.lessons) {
    const visual = lessonHeroVisual(lesson.slug);
    if (!visual || seen.has(visual.src)) {
      continue;
    }
    visuals.push(visual);
    seen.add(visual.src);
    if (visuals.length >= maxCount) {
      return visuals;
    }
  }

  const firstHero = visuals[0];
  if (firstHero) {
    for (const cardVisual of cardVisualsForHero(firstHero)) {
      if (seen.has(cardVisual.src)) {
        continue;
      }
      visuals.push(cardVisual);
      seen.add(cardVisual.src);
      if (visuals.length >= maxCount) {
        break;
      }
    }
  }

  return visuals;
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

  return (COURSE_VISUAL_SETS[slug] ?? []).map((spec) => visualFromSpec(spec, "ringkasan course"));
}

function curatedUnitVisuals(course: CourseRef, unit: UnitRef, unitIndex: number): CourseVisual[] {
  const bases = basesForUnit(unit, unitIndex);
  const gender = preferredGenderForCourse(course);
  const assets = UNIT_ASSET_PATTERNS[unitIndex % UNIT_ASSET_PATTERNS.length];
  const unitLabel = unit.title ? `unit ${unit.title}` : "unit course";

  return bases.map((base, index) => {
    const scene: VisualScene = `${base}-${gender}`;
    return visualFromSpec([scene, assets[index] ?? "hero"], unitLabel);
  });
}

function basesForUnit(unit: UnitRef, unitIndex: number): SceneBase[] {
  const text = [unit.title, unit.outcome].filter(Boolean).join(" ");
  const topicBases = UNIT_TOPIC_BASE_SETS.find((preset) => preset.pattern.test(text))?.bases ?? [];
  const defaultBases = DEFAULT_UNIT_BASE_SETS[unitIndex % DEFAULT_UNIT_BASE_SETS.length];
  return uniqueBases([...topicBases, ...defaultBases]).slice(0, 3);
}

function uniqueBases(bases: SceneBase[]) {
  const seen = new Set<SceneBase>();
  return bases.filter((base) => {
    if (seen.has(base)) {
      return false;
    }
    seen.add(base);
    return true;
  });
}

function preferredGenderForCourse(course: CourseRef): "female" | "male" {
  if (course.language === "arabic" || course.slug?.startsWith("arabic-")) {
    return "female";
  }

  return "male";
}

function visualFromSpec([scene, asset]: VisualSpec, purpose: string): CourseVisual {
  const isHero = asset === "hero";
  const filename = isHero ? "hero.png" : `${asset}.png`;
  const sceneLabel = scene.replace("-", " ");
  return {
    src: `/images/lesson-visual-library/${scene}/${filename}`,
    width: isHero ? HERO_WIDTH : CARD_SIZE,
    height: isHero ? HERO_HEIGHT : CARD_SIZE,
    alt: `Ilustrasi ${sceneLabel} untuk ${purpose}.`
  };
}

function cardVisualsForHero(hero: CourseVisual): CourseVisual[] {
  const basePath = hero.src.replace(/\/hero\.png$/, "");
  if (basePath === hero.src) {
    return [];
  }

  return [1, 2, 3].map((index) => ({
    src: `${basePath}/card-${index}.png`,
    width: CARD_SIZE,
    height: CARD_SIZE,
    alt: hero.alt
  }));
}
