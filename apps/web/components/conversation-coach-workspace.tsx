"use client";

import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Search, X } from "lucide-react";
import { ConversationCoachPractice } from "@/components/conversation-coach-practice";
import { coachScenarios, courses } from "@/lib/data";
import { readLatestPracticeSlug, saveLatestPracticeSlug } from "@/lib/practice-storage";

type Scenario = {
  slug: string;
  label: string;
  description: string;
  language?: string;
  languageLabel?: string;
  levelCode?: string;
  scenarioKey?: string;
  mode?: string;
};

type LessonMeta = {
  courseKey: string;
  languageLabel: string;
  levelCode: string;
  courseTitle: string;
  unitTitle: string;
  unitIndex: number;
  lessonIndex: number;
  lessonTitle: string;
};

type ScenarioWithMeta = Scenario &
  LessonMeta & {
    searchableText: string;
  };

type UnitGroup = {
  key: string;
  unitTitle: string;
  unitIndex: number;
  scenarios: ScenarioWithMeta[];
};

type LevelGroup = {
  key: string;
  languageLabel: string;
  levelCode: string;
  courseTitle: string;
  units: UnitGroup[];
  count: number;
};

const rawScenarios: Scenario[] = [...coachScenarios];

const lessonMetaBySlug = new Map<string, LessonMeta>();

courses.forEach((course) => {
  course.units.forEach((unit, unitIndex) => {
    unit.lessons.forEach((lesson, lessonIndex) => {
      lessonMetaBySlug.set(lesson.slug, {
        courseKey: `${course.language}-${course.level}`,
        languageLabel: course.languageLabel,
        levelCode: course.level,
        courseTitle: course.title,
        unitTitle: unit.title,
        unitIndex,
        lessonIndex,
        lessonTitle: lesson.title
      });
    });
  });
});

const scenarioBySlug = new Map(rawScenarios.map((scenario) => [scenario.slug, scenario]));
const orderedScenarios: ScenarioWithMeta[] = [];
const orderedSlugs = new Set<string>();

courses.forEach((course) => {
  course.units.forEach((unit) => {
    unit.lessons.forEach((lesson) => {
      const scenario = scenarioBySlug.get(lesson.slug);
      const meta = lessonMetaBySlug.get(lesson.slug);

      if (!scenario || !meta) {
        return;
      }

      orderedSlugs.add(scenario.slug);
      orderedScenarios.push({
        ...scenario,
        ...meta,
        searchableText: ""
      });
    });
  });
});

rawScenarios.forEach((scenario) => {
  if (orderedSlugs.has(scenario.slug)) {
    return;
  }

  const levelCode = scenario.levelCode ?? "A1";
  const languageLabel = scenario.languageLabel ?? "English";
  orderedScenarios.push({
    ...scenario,
    courseKey: `${scenario.language ?? "english"}-${levelCode}`,
    languageLabel,
    levelCode,
    courseTitle: `${levelCode} Conversation Coach`,
    unitTitle: scenario.description || "Skenario tambahan",
    unitIndex: 999,
    lessonIndex: 0,
    lessonTitle: scenario.label,
    searchableText: ""
  });
});

const scenarios = orderedScenarios.map((scenario) => ({
  ...scenario,
  searchableText: normalize(
    [
      scenario.levelCode,
      scenario.languageLabel,
      scenario.courseTitle,
      `unit ${scenario.unitIndex + 1}`,
      scenario.unitTitle,
      `lesson ${scenario.lessonIndex + 1}`,
      scenario.lessonTitle,
      scenario.label,
      scenario.description
    ].join(" ")
  )
}));

function normalize(value: string) {
  return value.trim().toLowerCase();
}

function lessonLabel(scenario: ScenarioWithMeta) {
  return `Lesson ${String(scenario.lessonIndex + 1).padStart(2, "0")}`;
}

function unitLabel(scenario: ScenarioWithMeta) {
  if (scenario.unitIndex >= 999) {
    return "Unit lainnya";
  }

  return `Unit ${String(scenario.unitIndex + 1).padStart(2, "0")}`;
}

function groupScenarios(items: ScenarioWithMeta[]) {
  const levelGroups: LevelGroup[] = [];
  const levelByKey = new Map<string, LevelGroup>();
  const unitByKey = new Map<string, UnitGroup>();

  items.forEach((scenario) => {
    let levelGroup = levelByKey.get(scenario.courseKey);

    if (!levelGroup) {
      levelGroup = {
        key: scenario.courseKey,
        languageLabel: scenario.languageLabel,
        levelCode: scenario.levelCode,
        courseTitle: scenario.courseTitle,
        units: [],
        count: 0
      };
      levelByKey.set(scenario.courseKey, levelGroup);
      levelGroups.push(levelGroup);
    }

    const unitKey = `${scenario.courseKey}-${scenario.unitIndex}-${scenario.unitTitle}`;
    let unitGroup = unitByKey.get(unitKey);

    if (!unitGroup) {
      unitGroup = {
        key: unitKey,
        unitTitle: scenario.unitTitle,
        unitIndex: scenario.unitIndex,
        scenarios: []
      };
      unitByKey.set(unitKey, unitGroup);
      levelGroup.units.push(unitGroup);
    }

    unitGroup.scenarios.push(scenario);
    levelGroup.count += 1;
  });

  return levelGroups;
}

export function ConversationCoachWorkspace() {
  const [activeSlug, setActiveSlug] = useState(scenarios[0].slug);
  const [isPickerOpen, setIsPickerOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [levelFilter, setLevelFilter] = useState<string>("all");
  const searchParams = useSearchParams();

  useEffect(() => {
    const fromQuery = searchParams.get("scenario");
    const preferred = fromQuery || readLatestPracticeSlug();

    if (!preferred) {
      return;
    }

    if (scenarios.some((scenario) => scenario.slug === preferred)) {
      setActiveSlug(preferred);
    }
  }, [searchParams]);

  const activeScenario = scenarios.find((scenario) => scenario.slug === activeSlug) ?? scenarios[0];
  const activeLevel = activeScenario.levelCode;
  const courseFilters = [
    { key: "all", label: "Semua" },
    ...Array.from(
      new Map(
        scenarios.map((scenario) => [
          scenario.courseKey,
          {
            key: scenario.courseKey,
            label: `${scenario.languageLabel} ${scenario.levelCode}`
          }
        ])
      ).values()
    )
  ];

  const filteredScenarios = useMemo(() => scenarios.filter((scenario) => {
    if (levelFilter !== "all" && scenario.courseKey !== levelFilter) {
      return false;
    }

    const q = normalize(query);
    if (!q) {
      return true;
    }

    return scenario.searchableText.includes(q);
  }), [levelFilter, query]);

  const groupedScenarios = useMemo(() => groupScenarios(filteredScenarios), [filteredScenarios]);
  const visibleUnitCount = groupedScenarios.reduce((total, level) => total + level.units.length, 0);

  return (
    <div className="space-y-5">
      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-leaf">Conversation Coach</p>
            <h1 className="mt-2 text-2xl font-semibold">Roleplay Terarah</h1>
            <p className="mt-2 text-sm leading-6 text-ink/60">
              Pilih skenario singkat, jawab, lalu dapat feedback yang jelas.
            </p>
          </div>
          <button
            type="button"
            onClick={() => setIsPickerOpen((current) => !current)}
            className="focus-ring inline-flex items-center justify-center rounded-lg border border-ink/20 bg-white px-4 py-3 text-sm font-semibold hover:bg-mint"
          >
            {isPickerOpen ? "Tutup daftar skenario" : "Ganti skenario"}
          </button>
        </div>

        <div className="mt-4 rounded-lg bg-paper p-4">
          <p className="text-xs font-semibold uppercase text-ink/50">Skenario aktif</p>
          <p className="mt-2 font-semibold">{activeScenario.lessonTitle}</p>
          <p className="mt-1 text-sm leading-6 text-ink/60">{activeScenario.description}</p>
          <div className="mt-3 flex flex-wrap items-center gap-2 text-xs font-semibold text-ink/60">
            <span className="rounded-lg bg-white px-2 py-1">Level {activeLevel}</span>
            <span className="rounded-lg bg-white px-2 py-1">{activeScenario.languageLabel}</span>
            <span className="rounded-lg bg-white px-2 py-1">{unitLabel(activeScenario)}</span>
            <span className="rounded-lg bg-white px-2 py-1">{lessonLabel(activeScenario)}</span>
            <span className="rounded-lg bg-white px-2 py-1">{activeScenario.unitTitle}</span>
          </div>
        </div>

        {isPickerOpen ? (
          <div className="mt-5 space-y-4">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="relative w-full sm:max-w-md">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink/40" aria-hidden="true" />
                <input
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  placeholder="Cari skenario…"
                  className="focus-ring w-full rounded-lg border border-ink/10 bg-white py-3 pl-9 pr-10 text-sm"
                />
                {query.trim() ? (
                  <button
                    type="button"
                    onClick={() => setQuery("")}
                    className="focus-ring absolute right-2 top-1/2 inline-flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg hover:bg-mint"
                    aria-label="Hapus pencarian"
                  >
                    <X className="h-4 w-4 text-ink/60" aria-hidden="true" />
                  </button>
                ) : null}
              </div>

              <div className="flex flex-wrap gap-2">
                {courseFilters.map((level) => {
                  const selected = levelFilter === level.key;
                  return (
                    <button
                      key={level.key}
                      type="button"
                      onClick={() => setLevelFilter(level.key)}
                      className={`focus-ring rounded-lg border px-3 py-2 text-xs font-semibold ${
                        selected ? "border-leaf bg-mint text-ink" : "border-ink/10 bg-white text-ink/70 hover:bg-mint"
                      }`}
                      aria-pressed={selected}
                    >
                      {level.label}
                    </button>
                  );
                })}
              </div>
            </div>

            <p className="text-sm text-ink/60">
              Menampilkan {filteredScenarios.length} skenario dalam {visibleUnitCount} unit.
            </p>

            {groupedScenarios.length ? (
              <div className="space-y-5">
                {groupedScenarios.map((level) => (
                  <section key={level.key} className="overflow-hidden rounded-lg border border-ink/10 bg-white">
                    <div className="flex flex-col gap-2 border-b border-ink/10 bg-paper px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
                      <div>
                        <p className="text-xs font-semibold uppercase text-leaf">
                          {level.languageLabel} · Level {level.levelCode}
                        </p>
                        <h3 className="mt-1 font-semibold">{level.courseTitle}</h3>
                      </div>
                      <span className="w-fit rounded-lg bg-white px-3 py-1 text-xs font-semibold text-ink/60">
                        {level.count} skenario
                      </span>
                    </div>

                    <div className="divide-y divide-ink/10">
                      {level.units.map((unit) => (
                        <div key={unit.key} className="p-4">
                          <div className="mb-3 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
                            <div>
                              <p className="text-xs font-semibold uppercase text-ink/45">
                                {unit.unitIndex >= 999 ? "Unit lainnya" : `Unit ${unit.unitIndex + 1}`}
                              </p>
                              <h4 className="mt-1 text-sm font-semibold">{unit.unitTitle}</h4>
                            </div>
                            <span className="text-xs font-semibold text-ink/45">
                              {unit.scenarios.length} lesson
                            </span>
                          </div>

                          <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
                            {unit.scenarios.map((scenario) => {
                              const selected = scenario.slug === activeSlug;

                              return (
                                <button
                                  key={scenario.slug}
                                  type="button"
                                  onClick={() => {
                                    setActiveSlug(scenario.slug);
                                    saveLatestPracticeSlug(scenario.slug);
                                    setIsPickerOpen(false);
                                  }}
                                  aria-pressed={selected}
                                  className={`focus-ring rounded-lg border p-4 text-left transition-colors ${
                                    selected ? "border-leaf bg-mint" : "border-ink/10 bg-paper hover:bg-mint"
                                  }`}
                                >
                                  <div className="flex flex-wrap items-center gap-2">
                                    <span className={`rounded-md px-2 py-1 text-[11px] font-semibold ${
                                      selected ? "bg-white text-leaf" : "bg-white text-ink/55"
                                    }`}>
                                      {lessonLabel(scenario)}
                                    </span>
                                    <span className="text-[11px] font-semibold uppercase text-ink/45">
                                      {scenario.languageLabel} · {scenario.levelCode}
                                    </span>
                                  </div>
                                  <p className="mt-3 text-sm font-semibold leading-5">{scenario.lessonTitle}</p>
                                  <p className="mt-1 text-xs leading-5 text-ink/60">{scenario.description}</p>
                                </button>
                              );
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  </section>
                ))}
              </div>
            ) : (
              <div className="rounded-lg border border-ink/10 bg-paper p-4 text-sm leading-6 text-ink/60">
                Tidak ada skenario yang cocok dengan filter ini.
              </div>
            )}
          </div>
        ) : null}
      </section>

      <ConversationCoachPractice key={activeSlug} lessonSlug={activeSlug} />
    </div>
  );
}
