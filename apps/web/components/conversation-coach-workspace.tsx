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
  levelCode?: string;
  scenarioKey?: string;
  mode?: string;
};

type LessonMeta = {
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
  levelCode: string;
  courseTitle: string;
  units: UnitGroup[];
  count: number;
};

const legacyScenarios: Scenario[] = [
  { slug: "saying-hello-and-goodbye", label: "Greeting & Goodbye", description: "Buka dan tutup percakapan singkat." },
  { slug: "saying-your-name", label: "Saying Your Name", description: "Perkenalkan namamu secara natural." },
  { slug: "asking-someones-name", label: "Asking a Name", description: "Tanyakan nama orang dengan sopan." },
  { slug: "saying-where-you-are-from", label: "Where Are You From", description: "Jawab asalmu dan tanyakan balik." },
  { slug: "first-conversation-mission", label: "First Conversation", description: "Gabungkan semuanya dalam satu misi." },
  { slug: "spelling-your-name", label: "Spelling Your Name", description: "Eja namamu huruf demi huruf." },
  { slug: "giving-phone-numbers", label: "Phone Numbers", description: "Sebutkan nomor dan cek ulang." },
  { slug: "sharing-email-addresses", label: "Email Address", description: "Sebutkan email dengan at dan dot." },
  { slug: "asking-for-repetition", label: "Ask to Repeat", description: "Minta pengulangan dengan sopan." },
  { slug: "contact-details-mission", label: "Contact Mission", description: "Gabungkan nama, nomor, dan email." },
  { slug: "telling-the-time", label: "Telling Time", description: "Tanya dan jawab jam kelas." },
  { slug: "talking-about-daily-routines", label: "Daily Routine", description: "Ceritakan rutinitas sederhana." },
  { slug: "days-and-simple-schedules", label: "Class Schedule", description: "Bahas hari dan jam kelas." },
  { slug: "asking-when-something-happens", label: "When It Happens", description: "Tanya waktu sebuah event." },
  { slug: "routine-conversation-mission", label: "Routine Mission", description: "Gabungkan routine dan schedule." },
  { slug: "saying-what-you-do", label: "What You Do", description: "Sebutkan kerja atau studi." },
  { slug: "asking-about-work-or-study", label: "Work or Study", description: "Tanyakan aktivitas utama." },
  { slug: "talking-about-likes", label: "Preferences", description: "Bahas hal yang disukai." },
  { slug: "saying-what-you-can-do", label: "Can Do", description: "Sebutkan kemampuan sederhana." },
  { slug: "work-study-conversation-mission", label: "Work Mission", description: "Gabungkan kerja, suka, dan bisa." },
  { slug: "asking-where-a-place-is", label: "Where Is It", description: "Tanyakan lokasi tempat." },
  { slug: "simple-place-words", label: "Place Words", description: "Sebutkan cafe, library, dan tujuan." },
  { slug: "understanding-simple-directions", label: "Simple Directions", description: "Ikuti go straight dan turn left." },
  { slug: "asking-how-to-get-there", label: "How To Get There", description: "Minta arahan dua langkah." },
  { slug: "finding-a-place-mission", label: "Place Mission", description: "Gabungkan lokasi dan arahan." },
  { slug: "ordering-a-drink", label: "Order Drink", description: "Pesan minuman dan pilih ukuran." },
  { slug: "asking-about-prices", label: "Ask Prices", description: "Tanyakan harga item sederhana." },
  { slug: "buying-a-simple-item", label: "Buy Item", description: "Beli satu barang dan bayar." },
  { slug: "saying-what-you-want", label: "What You Want", description: "Sebutkan pilihan makanan/minuman." },
  { slug: "cafe-and-shop-mission", label: "Cafe Mission", description: "Gabungkan order, harga, dan bayar." },
  { slug: "saying-you-do-not-understand", label: "Not Understand", description: "Katakan belum paham dan minta ulang." },
  { slug: "asking-for-help", label: "Ask Help", description: "Minta bantuan untuk masalah sederhana." },
  { slug: "making-simple-requests", label: "Simple Request", description: "Buat request sopan dengan please." },
  { slug: "apologizing-and-thanking", label: "Sorry & Thanks", description: "Minta maaf dan ucapkan terima kasih." },
  { slug: "help-and-problem-mission", label: "Help Mission", description: "Gabungkan masalah, request, dan thanks." },
  { slug: "review-introductions", label: "Review Intro", description: "Ulangi greeting, nama, asal, dan closing." },
  { slug: "review-routines-and-time", label: "Review Routine", description: "Ulangi rutinitas, hari, dan jam kelas." },
  { slug: "review-places-and-shopping", label: "Review Places", description: "Ulangi lokasi, arahan, order, dan harga." },
  { slug: "final-test-practice", label: "Final Practice", description: "Latihan pertanyaan final test A1." },
  { slug: "a1-final-conversation", label: "A1 Final", description: "Gabungkan semua skill inti A1." }
];

const rawScenarios: Scenario[] = [
  ...legacyScenarios,
  ...coachScenarios.filter((scenario) => !legacyScenarios.some((legacy) => legacy.slug === scenario.slug))
];

const lessonMetaBySlug = new Map<string, LessonMeta>();

courses.forEach((course) => {
  course.units.forEach((unit, unitIndex) => {
    unit.lessons.forEach((lesson, lessonIndex) => {
      lessonMetaBySlug.set(lesson.slug, {
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
  orderedScenarios.push({
    ...scenario,
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
    let levelGroup = levelByKey.get(scenario.levelCode);

    if (!levelGroup) {
      levelGroup = {
        key: scenario.levelCode,
        levelCode: scenario.levelCode,
        courseTitle: scenario.courseTitle,
        units: [],
        count: 0
      };
      levelByKey.set(scenario.levelCode, levelGroup);
      levelGroups.push(levelGroup);
    }

    const unitKey = `${scenario.levelCode}-${scenario.unitIndex}-${scenario.unitTitle}`;
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
  const levels = ["all", "A1", "A2", "B1", "B2", "C1"];

  const filteredScenarios = useMemo(() => scenarios.filter((scenario) => {
    if (levelFilter !== "all" && scenario.levelCode !== levelFilter) {
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
                {levels.map((level) => {
                  const selected = levelFilter === level;
                  const label = level === "all" ? "Semua" : level;
                  return (
                    <button
                      key={level}
                      type="button"
                      onClick={() => setLevelFilter(level)}
                      className={`focus-ring rounded-lg border px-3 py-2 text-xs font-semibold ${
                        selected ? "border-leaf bg-mint text-ink" : "border-ink/10 bg-white text-ink/70 hover:bg-mint"
                      }`}
                      aria-pressed={selected}
                    >
                      {label}
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
                        <p className="text-xs font-semibold uppercase text-leaf">Level {level.levelCode}</p>
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
                                      {scenario.levelCode}
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
