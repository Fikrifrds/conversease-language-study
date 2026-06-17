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

const ARABIC_SECTION_LABELS: Record<string, string> = {
  "Conversation Goal": "Target Percakapan",
  "Listen": "Dengarkan",
  "Useful Phrases": "Frasa Penting",
  "Speak Clearly": "Latihan Pengucapan",
  "Respond": "Latihan Respons",
  "Conversation Coach": "Roleplay Terarah"
};

const ARABIC_LESSON_COPY = {
  situationSetup: "Situasi Latihan",
  listenToDialogue: "Dengarkan Dialog",
  usefulPhrases: "Frasa Penting",
  grammarForConversation: "Pola Percakapan",
  speakClearly: "Latihan Pengucapan",
  conversationCheck: "Cek Pemahaman",
  readingSupport: "Bantuan Membaca",
  writingSupport: "Bantuan Menulis",
  practiceRoleplay: "Latihan Roleplay",
  backToDashboard: "Kembali ke Dashboard"
};

const DEFAULT_LESSON_COPY = {
  situationSetup: "Situation Setup",
  listenToDialogue: "Listen to a Dialogue",
  usefulPhrases: "Useful Phrases",
  grammarForConversation: "Grammar for Conversation",
  speakClearly: "Speak Clearly",
  conversationCheck: "Conversation Check",
  readingSupport: "Reading Support",
  writingSupport: "Writing Support",
  practiceRoleplay: "Practice Roleplay",
  backToDashboard: "Back to Dashboard"
};

export function generateStaticParams() {
  return lessonCatalog.map((lesson) => ({ slug: lesson.slug }));
}

export default function LessonPage({ params }: { params: { slug: string } }) {
  const lesson = lessonsBySlug[params.slug];

  if (!lesson) {
    notFound();
  }

  const isArabic = lesson.language === "arabic";
  const copy = isArabic ? ARABIC_LESSON_COPY : DEFAULT_LESSON_COPY;
  const progressSections = lesson.sections.map((section) =>
    isArabic ? ARABIC_SECTION_LABELS[section.label] ?? section.label : section.label
  );

  return (
    <AppShell requireAuth>
      <StudyDayMarker />
      <section className="mx-auto max-w-7xl px-4 pb-8 pt-8 md:pb-0 sm:px-6 lg:px-8">
        <div className="grid gap-6 lg:grid-cols-[0.72fr_0.28fr]">
          <article className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
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
            <div className="mt-4 rounded-lg border border-ink/10 bg-white p-4">
              <SimpleMarkdown markdown={lesson.conversationGoalDetails} />
            </div>

            <section className="mt-6">
              <h2 className="text-xl font-semibold">{copy.situationSetup}</h2>
              <p className="mt-2 leading-7 text-ink/70">{lesson.setup}</p>
            </section>

            <section className="mt-8">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-2">
                  <Headphones className="h-5 w-5 text-leaf" aria-hidden="true" />
                  <h2 className="text-xl font-semibold">{copy.listenToDialogue}</h2>
                </div>
                <LessonAudioPlayer lessonSlug={lesson.slug} />
              </div>
              <div className="mt-4 space-y-3">
                {lesson.dialogue.map((line, index) => (
                  <div key={`${line.speaker}-${index}`} className="grid gap-2 rounded-lg bg-paper p-4 lg:grid-cols-[120px_1fr_1fr]">
                    <span className="font-semibold text-leaf">{line.speaker}</span>
                    <p dir={isArabic ? "rtl" : "auto"} className={isArabic ? "text-right leading-8" : undefined}>
                      {line.text}
                    </p>
                    <p className="text-ink/60">{lesson.translation[index]}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="mt-8">
              <h2 className="text-xl font-semibold">{copy.usefulPhrases}</h2>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                {lesson.phrases.map((item) => (
                  <div key={item.phrase} className="rounded-lg border border-ink/10 bg-white p-4">
                    <p dir={isArabic ? "rtl" : "auto"} className={`font-semibold ${isArabic ? "text-right text-lg" : ""}`}>
                      {item.phrase}
                    </p>
                    <p className="mt-1 text-sm text-coral">{item.meaning}</p>
                    <p className="mt-2 text-sm leading-6 text-ink/60">{item.usage}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="mt-8 rounded-lg bg-[#fff2dc] p-5">
              <h2 className="text-xl font-semibold">{copy.grammarForConversation}</h2>
              <p className="mt-2 leading-7 text-ink/75">{lesson.grammar}</p>
              <div className="mt-4 rounded-lg bg-white/60 p-4">
                <SimpleMarkdown markdown={lesson.grammarNotes} dropLeadingHeading />
              </div>
            </section>

            <section className="mt-8">
              <div className="flex items-center gap-2">
                <Mic className="h-5 w-5 text-leaf" aria-hidden="true" />
                <h2 className="text-xl font-semibold">{copy.speakClearly}</h2>
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
              <h2 className="text-xl font-semibold">{copy.conversationCheck}</h2>
              <ConversationCheck items={lesson.quiz} />
            </section>

            <section className="mt-8 rounded-lg border border-ink/10 bg-white p-5">
              <h2 className="text-xl font-semibold">{copy.readingSupport}</h2>
              <div className="mt-4">
                <SimpleMarkdown markdown={lesson.readingSupport} dropLeadingHeading />
              </div>
            </section>

            <section className="mt-8 rounded-lg border border-ink/10 bg-white p-5">
              <h2 className="text-xl font-semibold">{copy.writingSupport}</h2>
              <div className="mt-4">
                <SimpleMarkdown markdown={lesson.writingSupport} dropLeadingHeading />
              </div>
            </section>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:flex-wrap">
              <Link
                href="#conversation-coach"
                className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink sm:w-auto"
              >
                <Send className="h-4 w-4" aria-hidden="true" />
                {copy.practiceRoleplay}
              </Link>
              <Link
                href="/dashboard"
                className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-lg border border-ink/20 px-4 py-3 text-sm font-semibold hover:bg-mint sm:w-auto"
              >
                <RotateCcw className="h-4 w-4" aria-hidden="true" />
                {copy.backToDashboard}
              </Link>
            </div>
          </article>

          <aside className="space-y-4 xl:sticky xl:top-24 xl:self-start">
            <LessonProgressPanel
              lessonSlug={lesson.slug}
              sections={progressSections}
            />
          </aside>
        </div>
      </section>
    </AppShell>
  );
}
