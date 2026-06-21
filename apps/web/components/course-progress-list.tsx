"use client";

import { useEffect, useMemo, useState, type MouseEvent } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowRight, CheckCircle2, CircleDot, PlayCircle } from "lucide-react";
import { LoginForm } from "@/components/login-form";
import { Modal } from "@/components/modal";
import { versionedAssetSrc } from "@/lib/assets";
import { getAuthSession } from "@/lib/auth-api";
import { unitHeroVisual } from "@/lib/course-visuals";
import { getCourseProgress, type LearningProgressSummary } from "@/lib/learning-api";
import { course as defaultCourse, type courses } from "@/lib/data";

type Course = (typeof courses)[number];

export function CourseProgressList({ course = defaultCourse }: { course?: Course }) {
  const router = useRouter();
  const [summary, setSummary] = useState<LearningProgressSummary | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loginTarget, setLoginTarget] = useState("");

  useEffect(() => {
    let ignore = false;
    const session = getAuthSession();
    setIsAuthenticated(Boolean(session));

    if (!session) {
      setSummary(null);
      return () => {
        ignore = true;
      };
    }

    async function loadProgress() {
      try {
        const nextSummary = await getCourseProgress(course.slug);

        if (!ignore) {
          setSummary(nextSummary);
        }
      } catch {
        if (!ignore) {
          setSummary(null);
        }
      }
    }

    loadProgress();

    return () => {
      ignore = true;
    };
  }, [course.slug]);

  const progressBySlug = useMemo(
    () => new Map((summary?.lessons ?? []).map((lesson) => [lesson.slug, lesson])),
    [summary]
  );

  function requestLesson(event: MouseEvent<HTMLAnchorElement>, href: string) {
    if (isAuthenticated) {
      return;
    }

    event.preventDefault();
    setLoginTarget(href);
  }

  function handleLoginSuccess(nextPath: string) {
    setIsAuthenticated(true);
    setLoginTarget("");
    router.push(nextPath);
  }

  return (
    <>
      <div className="mt-8 space-y-5">
        {course.units.map((unit, unitIndex) => {
          const activeLessons = unit.lessons.filter((lesson) => ["published", "beta"].includes(lesson.status));
          const unitVisual = unitHeroVisual(unit);
          const completedLessons = activeLessons.filter(
            (lesson) => progressBySlug.get(lesson.slug)?.progressStatus === "completed"
          ).length;
          const progressPercent = activeLessons.length
            ? Math.round((completedLessons / activeLessons.length) * 100)
            : 0;

          return (
            <section
              key={unit.title}
              id={`unit-${unitIndex + 1}`}
              className="scroll-mt-24 rounded-lg border border-ink/10 bg-white p-5 shadow-sm md:p-6"
            >
              <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
                <div className="flex min-w-0 flex-col gap-4 sm:flex-row">
                  {unitVisual ? (
                    <div className="relative aspect-[16/9] w-full overflow-hidden rounded-lg bg-paper sm:w-44 sm:shrink-0">
                      <Image
                        src={versionedAssetSrc(unitVisual.src)}
                        alt={unitVisual.alt}
                        fill
                        sizes="(min-width: 640px) 176px, 100vw"
                        className="object-cover"
                      />
                    </div>
                  ) : null}
                  <div className="min-w-0">
                    <span className="text-xs font-semibold uppercase text-coral">Unit {unitIndex + 1}</span>
                    <h2 className="mt-2 break-words text-xl font-semibold">{unit.title}</h2>
                    <p className="mt-2 max-w-2xl text-sm leading-6 text-ink/70">{unit.outcome}</p>
                  </div>
                </div>
                {summary ? (
                  <div className="w-full lg:max-w-xs">
                    <div className="mb-2 flex justify-between text-sm">
                      <span>Progress</span>
                      <span>{progressPercent}%</span>
                    </div>
                    <div className="h-2 rounded-lg bg-ink/10">
                      <div className="h-2 rounded-lg bg-leaf" style={{ width: `${progressPercent}%` }} />
                    </div>
                  </div>
                ) : (
                  <div className="rounded-lg bg-mint px-4 py-3 text-sm font-semibold text-ink/70">
                    Preview modul publik
                  </div>
                )}
              </div>

              {activeLessons.length ? (
                <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
                  {activeLessons.map((lesson, lessonIndex) => {
                    const lessonProgress = progressBySlug.get(lesson.slug);
                    const completed = lessonProgress?.progressStatus === "completed";
                    const inProgress = lessonProgress?.progressStatus === "in_progress";
                    const statusLabel = !summary ? "Preview" : completed ? "Selesai" : inProgress ? "Lanjutkan" : "Mulai";
                    const lessonHref = `/lessons/${lesson.slug}`;

                    return (
                      <Link
                        key={lesson.slug}
                        href={lessonHref}
                        onClick={(event) => requestLesson(event, lessonHref)}
                        className="focus-ring group rounded-lg border border-transparent bg-paper p-4 transition hover:border-leaf/20 hover:bg-mint"
                      >
                        <div className="flex items-center justify-between gap-3">
                          <span className="text-xs font-semibold uppercase text-leaf">
                            {course.level} · U{unitIndex + 1} · L{lessonIndex + 1}
                          </span>
                          <span className="flex items-center gap-2">
                            <span className={`text-xs font-semibold uppercase ${
                              completed ? "text-leaf" : inProgress ? "text-coral" : "text-ink/45"
                            }`}>
                              {statusLabel}
                            </span>
                            {completed ? (
                              <CheckCircle2 className="h-4 w-4 text-leaf" aria-hidden="true" />
                            ) : inProgress ? (
                              <CircleDot className="h-4 w-4 text-coral" aria-hidden="true" />
                            ) : (
                              <PlayCircle className="h-4 w-4 text-ink/40 group-hover:text-leaf" aria-hidden="true" />
                            )}
                          </span>
                        </div>
                        <h3 className="mt-3 font-semibold leading-snug text-ink">{lesson.title}</h3>
                        <div className="mt-3 flex items-center justify-between gap-3 text-sm text-ink/60">
                          <span>{lesson.minutes} menit</span>
                          <ArrowRight className="h-4 w-4 opacity-0 transition group-hover:translate-x-0.5 group-hover:opacity-100" aria-hidden="true" />
                        </div>
                      </Link>
                    );
                  })}
                </div>
              ) : null}
            </section>
          );
        })}
      </div>
      {loginTarget ? (
        <LessonLoginModal
          targetPath={loginTarget}
          onClose={() => setLoginTarget("")}
          onSuccess={handleLoginSuccess}
        />
      ) : null}
    </>
  );
}

function LessonLoginModal({
  targetPath,
  onClose,
  onSuccess
}: {
  targetPath: string;
  onClose: () => void;
  onSuccess: (nextPath: string) => void;
}) {
  return (
    <Modal
      eyebrow="Mulai lesson"
      title="Login untuk lanjut belajar"
      description="Katalog course bisa dilihat bebas. Untuk membuka lesson, simpan progress, dan memutar audio, silakan login dulu."
      size="sm"
      closeLabel="Tutup login"
      onClose={onClose}
    >
      <LoginForm defaultNextPath={targetPath} onSuccess={onSuccess} />
    </Modal>
  );
}
