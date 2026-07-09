import type { Metadata } from "next";
import Image from "next/image";
import { notFound } from "next/navigation";
import { AdminRegenerableLessonImage } from "@/components/admin-regenerable-lesson-image";
import { AppShell } from "@/components/app-shell";
import { LessonGatedBody } from "@/components/lesson-gated-body";
import { LessonPreviewBody } from "@/components/lesson-preview-body";
import { LessonProgressPanel } from "@/components/lesson-progress-panel";
import { StudyDayMarker } from "@/components/study-day-marker";
import { TrackGuard } from "@/components/track-guard";
import { versionedAssetSrc } from "@/lib/assets";
import { lessonCatalog, lessonsBySlug, lessonPlacementLabel } from "@/lib/data";

const ARABIC_SECTION_LABELS: Record<string, string> = {
  "Conversation Goal": "Target Percakapan",
  "Listen": "Dengarkan",
  "Useful Phrases": "Frasa Penting",
  "Vocabulary": "Kosa Kata Baru",
  "Speak Clearly": "Latihan Pengucapan",
  "Respond": "Latihan Respons",
  "Conversation Coach": "Roleplay Terarah"
};

export function generateStaticParams() {
  return lessonCatalog.map((lesson) => ({ slug: lesson.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const lesson = lessonsBySlug[params.slug];

  if (!lesson) {
    return { title: "Lesson tidak ditemukan", robots: { index: false, follow: false } };
  }

  // Only English lessons are public-facing for now; keep Arabic out of search
  // results while that track is still in coming-soon.
  if (lesson.language !== "english") {
    return { title: lesson.title, robots: { index: false, follow: false } };
  }

  const description = lesson.conversationGoal;
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://conversease.com";

  return {
    title: `${lesson.title} | Conversease`,
    description,
    alternates: { canonical: `/lessons/${lesson.slug}` },
    openGraph: {
      title: `${lesson.title} | Conversease`,
      description,
      url: `${siteUrl}/lessons/${lesson.slug}`,
      siteName: "Conversease",
      type: "website",
      images: lesson.visuals?.hero?.src ? [{ url: lesson.visuals.hero.src, width: 1200, height: 676 }] : [],
    },
    twitter: {
      card: "summary_large_image",
      title: `${lesson.title} | Conversease`,
      description,
    },
  };
}

export default function LessonPage({ params }: { params: { slug: string } }) {
  const lesson = lessonsBySlug[params.slug];

  if (!lesson) {
    notFound();
  }

  const isArabic = lesson.language === "arabic";
  const progressSections = lesson.sections.map((section) =>
    isArabic ? ARABIC_SECTION_LABELS[section.label] ?? section.label : section.label
  );

  return (
    <AppShell>
      <TrackGuard language={lesson.language}>
      <StudyDayMarker />
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        <div className="grid gap-6 lg:grid-cols-[minmax(0,0.72fr)_minmax(0,0.28fr)]">
          <article className="min-w-0 rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            {lessonPlacementLabel(lesson.slug) ? (
              <p className="text-xs font-semibold uppercase tracking-wide text-coral">
                {lessonPlacementLabel(lesson.slug)}
              </p>
            ) : null}
            <div className="mt-2 flex flex-wrap gap-2">
              <span className="rounded-lg bg-mint px-3 py-1 text-xs font-bold uppercase text-leaf">
                {lesson.languageLabel}
              </span>
              <span className="rounded-lg bg-paper px-3 py-1 text-xs font-bold uppercase text-ink/60">
                {lesson.unit}
              </span>
            </div>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">{lesson.title}</h1>
            <p className="mt-4 rounded-lg bg-mint p-4 leading-7 text-ink/80">{lesson.conversationGoal}</p>

            {lesson.visuals ? (
              <section className="mt-6">
                <figure className="overflow-hidden rounded-lg border border-ink/10 bg-paper">
                  {isArabic ? (
                    <Image
                      src={versionedAssetSrc(lesson.visuals.hero.src)}
                      alt={lesson.visuals.hero.alt}
                      width={lesson.visuals.hero.width}
                      height={lesson.visuals.hero.height}
                      className="h-auto w-full"
                      priority
                    />
                  ) : (
                    <AdminRegenerableLessonImage
                      lessonSlug={lesson.slug}
                      slot="hero"
                      defaultSrc={lesson.visuals.hero.src}
                      alt={lesson.visuals.hero.alt}
                      width={lesson.visuals.hero.width}
                      height={lesson.visuals.hero.height}
                      className="h-auto w-full"
                      priority
                    />
                  )}
                  {lesson.visuals.hero.caption ? (
                    <figcaption className="px-4 py-3 text-sm leading-6 text-ink/60">
                      {lesson.visuals.hero.caption}
                    </figcaption>
                  ) : null}
                </figure>
              </section>
            ) : null}

            {/* JSON-LD Structured Data */}
            <script
              type="application/ld+json"
              dangerouslySetInnerHTML={{
                __html: JSON.stringify({
                  "@context": "https://schema.org",
                  "@type": "LearningResource",
                  "name": lesson.title,
                  "description": lesson.conversationGoal,
                  "educationalLevel": lesson.unit?.includes("A1") ? "Beginner" : lesson.unit?.includes("A2") ? "Elementary" : "Intermediate",
                  "learningResourceType": "Lesson",
                  "inLanguage": "en",
                  "teaches": lesson.conversationGoal,
                  "provider": {
                    "@type": "Organization",
                    "name": "Conversease",
                    "url": "https://conversease.com"
                  },
                  "isPartOf": {
                    "@type": "Course",
                    "name": `English ${lesson.unit}`,
                    "provider": {
                      "@type": "Organization",
                      "name": "Conversease"
                    }
                  }
                })
              }}
            />

            {/* Public preview for SEO, gated full content for authenticated users */}
            <LessonPreviewBody
              slug={lesson.slug}
              title={lesson.title}
              conversationGoal={lesson.conversationGoal}
              language={lesson.language}
            />
            <LessonGatedBody slug={lesson.slug} />
          </article>

          <aside className="space-y-4 xl:sticky xl:top-24 xl:self-start">
            <LessonProgressPanel
              lessonSlug={lesson.slug}
              sections={progressSections}
            />
          </aside>
        </div>
      </section>
      </TrackGuard>
    </AppShell>
  );
}
