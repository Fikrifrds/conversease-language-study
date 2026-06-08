import Link from "next/link";
import { notFound } from "next/navigation";
import { Headphones, Mic, RotateCcw, Send } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { ConversationCheck } from "@/components/conversation-check";
import { ConversationCoachPractice } from "@/components/conversation-coach-practice";
import { LessonAudioPlayer } from "@/components/lesson-audio-player";
import { LessonProgressPanel } from "@/components/lesson-progress-panel";
import { PronunciationRepeatPractice } from "@/components/pronunciation-repeat-practice";
import { SimpleMarkdown } from "@/components/simple-markdown";
import { SpeakClearlyPractice } from "@/components/speak-clearly-practice";
import { StudyDayMarker } from "@/components/study-day-marker";
import { lessonCatalog, lessonsBySlug, lessonPlacementLabel } from "@/lib/data";

export function generateStaticParams() {
  return lessonCatalog.map((lesson) => ({ slug: lesson.slug }));
}

export default function LessonPage({ params }: { params: { slug: string } }) {
  const lesson = lessonsBySlug[params.slug];

  if (!lesson) {
    notFound();
  }

  return (
    <AppShell requireAuth>
      <StudyDayMarker />
      <section className="mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <div className="grid gap-6 lg:grid-cols-[0.72fr_0.28fr]">
          <article className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
            {lessonPlacementLabel(lesson.slug) ? (
              <p className="text-xs font-semibold uppercase tracking-wide text-coral">
                {lessonPlacementLabel(lesson.slug)}
              </p>
            ) : null}
            <p className="mt-1 text-sm font-semibold uppercase text-leaf">{lesson.unit}</p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">{lesson.title}</h1>
            <p className="mt-4 rounded-lg bg-mint p-4 leading-7 text-ink/80">{lesson.conversationGoal}</p>
            <div className="mt-4 rounded-lg border border-ink/10 bg-white p-4">
              <SimpleMarkdown markdown={lesson.conversationGoalDetails} />
            </div>

            <section className="mt-6">
              <h2 className="text-xl font-semibold">Situation Setup</h2>
              <p className="mt-2 leading-7 text-ink/70">{lesson.setup}</p>
            </section>

            <section className="mt-8">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-2">
                  <Headphones className="h-5 w-5 text-leaf" aria-hidden="true" />
                  <h2 className="text-xl font-semibold">Listen to a Dialogue</h2>
                </div>
                <LessonAudioPlayer lessonSlug={lesson.slug} />
              </div>
              <div className="mt-4 space-y-3">
                {lesson.dialogue.map((line, index) => (
                  <div key={`${line.speaker}-${index}`} className="grid gap-2 rounded-lg bg-paper p-4 md:grid-cols-[140px_1fr_1fr]">
                    <span className="font-semibold text-leaf">{line.speaker}</span>
                    <p>{line.text}</p>
                    <p className="text-ink/60">{lesson.translation[index]}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="mt-8">
              <h2 className="text-xl font-semibold">Useful Phrases</h2>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                {lesson.phrases.map((item) => (
                  <div key={item.phrase} className="rounded-lg border border-ink/10 bg-white p-4">
                    <p className="font-semibold">{item.phrase}</p>
                    <p className="mt-1 text-sm text-coral">{item.meaning}</p>
                    <p className="mt-2 text-sm leading-6 text-ink/60">{item.usage}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="mt-8 rounded-lg bg-[#fff2dc] p-5">
              <h2 className="text-xl font-semibold">Grammar for Conversation</h2>
              <p className="mt-2 leading-7 text-ink/75">{lesson.grammar}</p>
              <div className="mt-4 rounded-lg bg-white/60 p-4">
                <SimpleMarkdown markdown={lesson.grammarNotes} dropLeadingHeading />
              </div>
            </section>

            <section className="mt-8">
              <div className="flex items-center gap-2">
                <Mic className="h-5 w-5 text-leaf" aria-hidden="true" />
                <h2 className="text-xl font-semibold">Speak Clearly</h2>
              </div>
              <div className="mt-4 rounded-lg border border-ink/10 bg-white p-4">
                <SimpleMarkdown markdown={lesson.pronunciationDrill} dropLeadingHeading />
              </div>
              <PronunciationRepeatPractice drillMarkdown={lesson.pronunciationDrill} />
              <SpeakClearlyPractice prompts={lesson.prompts} />
            </section>

            <section className="mt-8" id="conversation-coach">
              <ConversationCoachPractice compact lessonSlug={lesson.slug} />
            </section>

            <section className="mt-8 rounded-lg border border-ink/10 bg-white p-5">
              <h2 className="text-xl font-semibold">Conversation Check</h2>
              <ConversationCheck items={lesson.quiz} />
            </section>

            <section className="mt-8 rounded-lg border border-ink/10 bg-white p-5">
              <h2 className="text-xl font-semibold">Reading Support</h2>
              <div className="mt-4">
                <SimpleMarkdown markdown={lesson.readingSupport} dropLeadingHeading />
              </div>
            </section>

            <section className="mt-8 rounded-lg border border-ink/10 bg-white p-5">
              <h2 className="text-xl font-semibold">Writing Support</h2>
              <div className="mt-4">
                <SimpleMarkdown markdown={lesson.writingSupport} dropLeadingHeading />
              </div>
            </section>

            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                href="#conversation-coach"
                className="focus-ring inline-flex items-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink"
              >
                <Send className="h-4 w-4" aria-hidden="true" />
                Practice Roleplay
              </Link>
              <Link
                href="/dashboard"
                className="focus-ring inline-flex items-center gap-2 rounded-lg border border-ink/20 px-4 py-3 text-sm font-semibold hover:bg-mint"
              >
                <RotateCcw className="h-4 w-4" aria-hidden="true" />
                Back to Dashboard
              </Link>
            </div>
          </article>

          <aside className="space-y-4 lg:sticky lg:top-24 lg:self-start">
            <LessonProgressPanel
              lessonSlug={lesson.slug}
              sections={lesson.sections.map((section) => section.label)}
            />
          </aside>
        </div>
      </section>
    </AppShell>
  );
}
