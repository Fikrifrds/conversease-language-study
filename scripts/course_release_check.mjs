#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..");
const webPublicRoot = path.join(repoRoot, "apps", "web", "public");
const curriculumRoot = path.join(repoRoot, "content", "curriculum");
const requiredLevels = ["A1", "A2", "B1", "B2", "C1"];
const requiredLessonFiles = [
  "lesson.yaml",
  "conversation_goal.md",
  "lesson.md",
  "listening_script.md",
  "audio_manifest.yaml",
  "conversation_coach_roleplay.yaml",
  "visuals.yaml",
  "response_prompts.yaml",
  "quiz.yaml",
  "vocabulary.yaml",
  "useful_phrases.yaml",
  "pronunciation_drill.md",
  "grammar_for_conversation.md",
  "reading_support.md",
  "writing_support.md",
  "transcript_translation.md"
];

const args = new Set(process.argv.slice(2));
const jsonOutput = args.has("--json");

const failures = [];
const warnings = [];

const courseVisualSets = {
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

const defaultUnitBaseSets = [
  ["classroom", "service", "travel"],
  ["service", "workplace", "classroom"],
  ["travel", "classroom", "service"],
  ["workplace", "classroom", "service"],
  ["travel", "service", "classroom"],
  ["service", "travel", "workplace"],
  ["health", "service", "classroom"],
  ["classroom", "travel", "workplace"]
];

const unitTopicBaseSets = [
  { pattern: /foundation|greeting|introduc|class|instruction/i, bases: ["classroom", "service", "travel"] },
  {
    pattern: /social|small talk|follow-up|weekend|plan|invitation|invite|accept|declin|reschedule/i,
    bases: ["classroom", "service", "travel"]
  },
  { pattern: /health|symptom|appointment/i, bases: ["health", "service", "classroom"] },
  {
    pattern: /travel|transport|direction|\bplaces?\b|checking in|ticket|departure|delay|recommendation/i,
    bases: ["travel", "service", "classroom"]
  },
  { pattern: /contact|phone|email|number/i, bases: ["service", "workplace", "classroom"] },
  { pattern: /food|drink|shopping|prices|service|customer|client/i, bases: ["service", "travel", "workplace"] },
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
  { pattern: /problem|help|request|solution|tradeoff|cause|framing/i, bases: ["health", "service", "workplace"] },
  {
    pattern: /community|culture|family|cross-cultural|local norm/i,
    bases: ["travel", "classroom", "service"]
  }
];

const unitAssetPatterns = [
  ["hero", "card-1", "card-2"],
  ["card-1", "hero", "card-3"],
  ["card-2", "hero", "card-1"],
  ["hero", "card-2", "card-3"],
  ["card-3", "card-1", "hero"],
  ["card-2", "card-3", "hero"],
  ["hero", "card-3", "card-1"],
  ["card-1", "card-2", "hero"]
];

function addFailure(code, message, details = {}) {
  failures.push({ code, message, details });
}

function addWarning(code, message, details = {}) {
  warnings.push({ code, message, details });
}

function stripAssetQuery(src) {
  return src.split("?")[0];
}

function publicAssetPath(src) {
  const cleanSrc = stripAssetQuery(src);
  if (!cleanSrc.startsWith("/")) {
    return null;
  }
  return path.join(webPublicRoot, cleanSrc);
}

function assetExists(src) {
  const assetPath = publicAssetPath(src);
  return Boolean(assetPath && fs.existsSync(assetPath));
}

function visualKey(src) {
  const match = stripAssetQuery(src).match(/lesson-visual-library\/([^/]+)\/([^/]+)$/);
  return match ? `${match[1]}/${match[2]}` : stripAssetQuery(src);
}

function sceneKey(src) {
  const match = stripAssetQuery(src).match(/lesson-visual-library\/([^/]+)\//);
  return match ? match[1] : stripAssetQuery(src);
}

function walkDirs(root) {
  const dirs = [];
  const stack = [root];
  while (stack.length) {
    const current = stack.pop();
    if (!current || !fs.existsSync(current)) {
      continue;
    }
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      if (!entry.isDirectory()) {
        continue;
      }
      const next = path.join(current, entry.name);
      dirs.push(next);
      stack.push(next);
    }
  }
  return dirs;
}

function yamlScalar(content, key) {
  const match = content.match(new RegExp(`^${key}:\\s*['"]?([^\\n'"]+)['"]?\\s*$`, "m"));
  return match ? match[1].trim() : "";
}

function buildLessonDirMap() {
  const bySlug = new Map();
  for (const dir of walkDirs(curriculumRoot)) {
    const lessonYaml = path.join(dir, "lesson.yaml");
    if (!fs.existsSync(lessonYaml)) {
      continue;
    }
    const slug = yamlScalar(fs.readFileSync(lessonYaml, "utf8"), "slug");
    if (slug) {
      bySlug.set(slug, dir);
    }
  }
  return bySlug;
}

function nonEmptyFile(filePath) {
  return fs.existsSync(filePath) && fs.statSync(filePath).size > 0;
}

function listeningTurnCount(content) {
  return content.split("\n").filter((line) => /^\s*\*\*[^*]+:\*\*/.test(line)).length;
}

function routeSafe(route) {
  return route.startsWith("/") && !/\s/.test(route) && !route.includes("//");
}

function visualFromSpec([scene, asset]) {
  const filename = asset === "hero" ? "hero.png" : `${asset}.png`;
  return {
    src: `/images/lesson-visual-library/${scene}/${filename}`
  };
}

function courseHeroVisuals(course) {
  return (courseVisualSets[course.slug] ?? []).map(visualFromSpec);
}

function uniqueItems(items) {
  const seen = new Set();
  return items.filter((item) => {
    if (seen.has(item)) {
      return false;
    }
    seen.add(item);
    return true;
  });
}

function basesForUnit(unit, unitIndex) {
  const text = [unit.title, unit.outcome].filter(Boolean).join(" ");
  const topicBases = unitTopicBaseSets.find((preset) => preset.pattern.test(text))?.bases ?? [];
  const defaultBases = defaultUnitBaseSets[unitIndex % defaultUnitBaseSets.length];
  return uniqueItems([...topicBases, ...defaultBases]).slice(0, 3);
}

function preferredGenderForCourse(course) {
  return course.language === "arabic" || course.slug?.startsWith("arabic-") ? "female" : "male";
}

function courseUnitVisuals(course, unit, unitIndex) {
  const gender = preferredGenderForCourse(course);
  const assets = unitAssetPatterns[unitIndex % unitAssetPatterns.length];
  return basesForUnit(unit, unitIndex).map((base, index) => visualFromSpec([`${base}-${gender}`, assets[index] ?? "hero"]));
}

async function loadWebModules() {
  try {
    const dataUrl = pathToFileURL(path.join(repoRoot, "apps", "web", "lib", "data.ts")).href;
    const data = await import(dataUrl);
    return { data };
  } catch (error) {
    addFailure(
      "web_data_import_failed",
      "Could not import generated web course data. Run with the repository Node runtime after web data generation.",
      { error: `${error.name}: ${error.message}` }
    );
    return null;
  }
}

function checkTrackCoverage(courses) {
  for (const language of ["english", "arabic"]) {
    const levels = courses.filter((course) => course.language === language).map((course) => course.level).sort();
    const missing = requiredLevels.filter((level) => !levels.includes(level));
    const extra = levels.filter((level) => !requiredLevels.includes(level));
    if (missing.length || extra.length) {
      addFailure("track_level_coverage", `${language} track level coverage is not release-ready.`, {
        language,
        expected: requiredLevels,
        actual: levels,
        missing,
        extra
      });
    }
  }
}

function checkCourseStructure(courses, lessonsBySlug, courseHeroVisuals, courseUnitVisuals) {
  const courseSlugs = new Set();
  const lessonSlugs = new Set();

  for (const course of courses) {
    if (courseSlugs.has(course.slug)) {
      addFailure("duplicate_course_slug", "Course slug is duplicated.", { slug: course.slug });
    }
    courseSlugs.add(course.slug);

    const courseLessons = course.units.flatMap((unit) => unit.lessons);
    if (course.units.length !== 8 || courseLessons.length !== 40) {
      addFailure("course_shape", "Course must have 8 units and 40 lessons.", {
        course: course.slug,
        unitCount: course.units.length,
        lessonCount: courseLessons.length
      });
    }

    if (!routeSafe(`/courses/${course.slug}`)) {
      addFailure("unsafe_course_route", "Course route contains unsafe characters.", { course: course.slug });
    }

    const courseVisuals = courseHeroVisuals(course);
    if (courseVisuals.length < 3) {
      addFailure("course_visual_count", "Course card should have at least 3 visual panels.", { course: course.slug });
    }
    for (const visual of courseVisuals) {
      if (!assetExists(visual.src)) {
        addFailure("missing_course_visual_asset", "Course visual asset is missing.", {
          course: course.slug,
          visual: visual.src
        });
      }
    }

    const unitVisualSignatures = [];
    for (const [unitIndex, unit] of course.units.entries()) {
      if (unit.lessons.length !== 5) {
        addFailure("unit_lesson_count", "Each unit should have 5 lessons.", {
          course: course.slug,
          unit: unit.title,
          lessonCount: unit.lessons.length
        });
      }

      const unitVisuals = courseUnitVisuals(course, unit, unitIndex);
      if (unitVisuals.length < 3) {
        addFailure("unit_visual_count", "Each unit should have at least 3 visual panels.", {
          course: course.slug,
          unit: unit.title,
          visualCount: unitVisuals.length
        });
      }

      const unitScenes = new Set(unitVisuals.map((visual) => sceneKey(visual.src)));
      if (unitScenes.size < Math.min(2, unitVisuals.length)) {
        addWarning("low_unit_scene_variety", "Unit visual panels use too few distinct settings.", {
          course: course.slug,
          unit: unit.title,
          visuals: unitVisuals.map((visual) => visualKey(visual.src))
        });
      }

      unitVisualSignatures.push(unitVisuals.map((visual) => visualKey(visual.src)).join("|"));
      for (const visual of unitVisuals) {
        if (!assetExists(visual.src)) {
          addFailure("missing_unit_visual_asset", "Unit visual asset is missing.", {
            course: course.slug,
            unit: unit.title,
            visual: visual.src
          });
        }
      }

      for (const lesson of unit.lessons) {
        if (lessonSlugs.has(lesson.slug)) {
          addFailure("duplicate_lesson_slug", "Lesson slug is duplicated.", { slug: lesson.slug });
        }
        lessonSlugs.add(lesson.slug);

        if (!lessonsBySlug[lesson.slug]) {
          addFailure("missing_lesson_catalog_entry", "Course references a lesson missing from lessonCatalog.", {
            course: course.slug,
            unit: unit.title,
            lesson: lesson.slug
          });
        }
        if (!routeSafe(`/lessons/${lesson.slug}`)) {
          addFailure("unsafe_lesson_route", "Lesson route contains unsafe characters.", { lesson: lesson.slug });
        }
      }
    }

    if (new Set(unitVisualSignatures).size < Math.max(1, course.units.length - 1)) {
      addWarning("low_course_unit_mosaic_variety", "Course unit visual mosaics may feel repetitive.", {
        course: course.slug,
        unitVisualSignatures
      });
    }
  }
}

function checkLessonCatalog(lessonCatalog, lessonDirBySlug) {
  for (const lesson of lessonCatalog) {
    if (!lesson.title || !lesson.conversationGoal || !lesson.unit) {
      addFailure("lesson_catalog_copy", "Lesson catalog entry is missing title, unit, or conversation goal.", {
        lesson: lesson.slug
      });
    }

    const hero = lesson.visuals?.hero;
    if (!hero?.src) {
      addFailure("lesson_missing_hero_visual", "Lesson catalog entry has no hero visual.", { lesson: lesson.slug });
    } else if (!assetExists(hero.src)) {
      addFailure("missing_lesson_hero_asset", "Lesson hero visual asset is missing.", {
        lesson: lesson.slug,
        visual: hero.src
      });
    }

    const lessonDir = lessonDirBySlug.get(lesson.slug);
    if (!lessonDir) {
      addFailure("missing_lesson_source_dir", "Lesson catalog slug has no matching curriculum lesson.yaml source.", {
        lesson: lesson.slug
      });
      continue;
    }

    for (const filename of requiredLessonFiles) {
      const filePath = path.join(lessonDir, filename);
      if (!nonEmptyFile(filePath)) {
        addFailure("missing_required_lesson_file", "Required lesson source file is missing or empty.", {
          lesson: lesson.slug,
          file: path.relative(repoRoot, filePath)
        });
      }
    }

    const listeningPath = path.join(lessonDir, "listening_script.md");
    if (fs.existsSync(listeningPath)) {
      const turnCount = listeningTurnCount(fs.readFileSync(listeningPath, "utf8"));
      if (turnCount < 4) {
        addFailure("listening_script_too_short", "Listening script should have at least 4 dialogue turns.", {
          lesson: lesson.slug,
          turnCount,
          file: path.relative(repoRoot, listeningPath)
        });
      }
    }
  }
}

function renderHuman(payload) {
  const lines = [
    "Conversease course release check",
    `Courses: ${payload.summary.courseCount}`,
    `Units: ${payload.summary.unitCount}`,
    `Lessons: ${payload.summary.lessonCount}`,
    `Failures: ${payload.failures.length}`,
    `Warnings: ${payload.warnings.length}`
  ];

  if (payload.failures.length) {
    lines.push("", "Failures:");
    for (const issue of payload.failures.slice(0, 25)) {
      lines.push(`- ${issue.code}: ${issue.message} ${JSON.stringify(issue.details)}`);
    }
  }

  if (payload.warnings.length) {
    lines.push("", "Warnings:");
    for (const issue of payload.warnings.slice(0, 25)) {
      lines.push(`- ${issue.code}: ${issue.message} ${JSON.stringify(issue.details)}`);
    }
  }

  return `${lines.join("\n")}\n`;
}

const modules = await loadWebModules();
if (modules) {
  const { courses, lessonsBySlug, lessonCatalog } = modules.data;
  const lessonDirBySlug = buildLessonDirMap();

  if (courses.length !== 10) {
    addFailure("course_count", "Release should expose exactly 10 courses: 2 tracks x 5 levels.", {
      courseCount: courses.length
    });
  }

  checkTrackCoverage(courses);
  checkCourseStructure(courses, lessonsBySlug, courseHeroVisuals, courseUnitVisuals);
  checkLessonCatalog(lessonCatalog, lessonDirBySlug);
}

const payload = {
  checkedAt: new Date().toISOString(),
  summary: modules
    ? {
        courseCount: modules.data.courses.length,
        unitCount: modules.data.courses.reduce((sum, course) => sum + course.units.length, 0),
        lessonCount: modules.data.lessonCatalog.length
      }
    : {
        courseCount: 0,
        unitCount: 0,
        lessonCount: 0
      },
  failures,
  warnings
};

process.stdout.write(jsonOutput ? `${JSON.stringify(payload, null, 2)}\n` : renderHuman(payload));
process.exitCode = failures.length ? 1 : 0;
