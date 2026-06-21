"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { BookOpen, Headphones, Loader2, Lock, Mic, RotateCcw, Send, Sparkles } from "lucide-react";
import { productRoutes } from "@conversease/shared";
import { ConversationCheck } from "@/components/conversation-check";
import { ConversationCoachPractice } from "@/components/conversation-coach-practice";
import { LessonAudioPlayer } from "@/components/lesson-audio-player";
import { PronunciationRepeatPractice } from "@/components/pronunciation-repeat-practice";
import { SimpleMarkdown } from "@/components/simple-markdown";
import { SpeakClearlyPractice } from "@/components/speak-clearly-practice";
import { versionedAssetSrc } from "@/lib/assets";
import { ApiRequestError, getLessonFull, type LessonContent } from "@/lib/learning-api";

const ARABIC_LESSON_COPY = {
  situationSetup: "Situasi Latihan",
  listenToDialogue: "Dengarkan Dialog",
  usefulPhrases: "Frasa Penting",
  vocabulary: "Kosa Kata Baru",
  vocabularyItems: "kata",
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
  vocabulary: "New Vocabulary",
  vocabularyItems: "items",
  grammarForConversation: "Grammar for Conversation",
  speakClearly: "Speak Clearly",
  conversationCheck: "Conversation Check",
  readingSupport: "Reading Support",
  writingSupport: "Writing Support",
  practiceRoleplay: "Practice Roleplay",
  backToDashboard: "Back to Dashboard"
};

type GateState =
  | { status: "loading" }
  | { status: "locked" }
  | { status: "error" }
  | { status: "unlocked"; lesson: LessonContent };

/**
 * Renders the paywalled portion of a lesson. The content is fetched at runtime
 * from the authenticated /lessons/{slug}/full endpoint, which returns it only
 * to Pro/admin users — free users get a 403 and the locked overlay below. The
 * gated content is therefore never shipped in the page bundle.
 */
export function LessonGatedBody({ slug }: { slug: string }) {
  const [state, setState] = useState<GateState>({ status: "loading" });

  useEffect(() => {
    let ignore = false;

    async function load() {
      try {
        const lesson = await getLessonFull(slug);
        if (!ignore) {
          setState({ status: "unlocked", lesson });
        }
      } catch (error) {
        if (ignore) {
          return;
        }
        if (error instanceof ApiRequestError && error.status === 403) {
          setState({ status: "locked" });
        } else {
          setState({ status: "error" });
        }
      }
    }

    load();

    return () => {
      ignore = true;
    };
  }, [slug]);

  if (state.status === "loading") {
    return (
      <div className="mt-8 flex items-center justify-center gap-2 rounded-lg border border-ink/10 bg-white p-10 text-sm text-ink/60">
        <Loader2 className="h-5 w-5 animate-spin text-leaf" aria-hidden="true" />
        Menyiapkan materi lesson...
      </div>
    );
  }

  if (state.status === "error") {
    return (
      <div className="mt-8 rounded-lg border border-ink/10 bg-white p-6 text-center text-sm text-ink/60">
        Materi lesson gagal dimuat. Coba muat ulang halaman.
      </div>
    );
  }

  if (state.status === "locked") {
    return <LessonPaywall />;
  }

  return <UnlockedBody lesson={state.lesson} />;
}

function LessonPaywall() {
  return (
    <div className="relative mt-8">
      {/* Blurred teaser placeholder: no real lesson content is rendered here, so
          nothing leaks to free users. The gradient fades it into the card. */}
      <div className="relative max-h-[360px] overflow-hidden rounded-lg" aria-hidden="true">
        <div className="space-y-3 blur-sm">
          {Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="rounded-lg bg-paper p-4">
              <div className="h-3 w-24 rounded bg-ink/10" />
              <div className="mt-3 h-3 w-3/4 rounded bg-ink/10" />
              <div className="mt-2 h-3 w-2/3 rounded bg-ink/10" />
            </div>
          ))}
        </div>
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-white/0 via-white/60 to-white" />
      </div>

      <div className="relative -mt-28 px-2 sm:px-6">
        <div className="mx-auto max-w-xl rounded-lg border border-ink/10 bg-white/95 p-6 text-center shadow-soft backdrop-blur sm:p-8">
          <div className="mx-auto grid h-12 w-12 place-items-center rounded-lg bg-mint">
            <Lock className="h-6 w-6 text-leaf" aria-hidden="true" />
          </div>
          <h2 className="mt-5 text-2xl font-semibold">Lanjutkan lesson ini dengan Pro</h2>
          <p className="mt-3 text-sm leading-6 text-ink/65">
            Kamu sedang melihat pratinjau gratis. Buka dialog lengkap, latihan respons, roleplay,
            audio, dan seluruh materi lesson dengan langganan Pro.
          </p>
          <Link
            href={productRoutes.pricing}
            className="focus-ring mt-6 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-leaf px-5 py-3 text-sm font-semibold text-white transition hover:bg-ink sm:w-auto"
          >
            <Sparkles className="h-4 w-4" aria-hidden="true" />
            Upgrade ke Pro
          </Link>
          <p className="mt-4 text-xs text-ink/50">
            Sudah berlangganan?{" "}
            <Link href={productRoutes.billing} className="font-semibold text-leaf hover:underline">
              Cek status langganan
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

function UnlockedBody({ lesson }: { lesson: LessonContent }) {
  const isArabic = lesson.language === "arabic";
  const copy = isArabic ? ARABIC_LESSON_COPY : DEFAULT_LESSON_COPY;

  return (
    <>
      <div className="mt-6 rounded-lg border border-ink/10 bg-white p-4">
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
        {lesson.visuals?.cards?.length ? (
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            {lesson.visuals.cards.map((visual) => (
              <figure key={visual.src} className="overflow-hidden rounded-lg border border-ink/10 bg-paper">
                <Image
                  src={versionedAssetSrc(visual.src)}
                  alt={visual.alt}
                  width={visual.width}
                  height={visual.height}
                  className="aspect-square w-full object-cover"
                />
                <figcaption
                  dir={isArabic ? "rtl" : "auto"}
                  className={`px-3 py-3 text-sm font-semibold text-ink ${isArabic ? "text-right text-base" : ""}`}
                >
                  {visual.label}
                </figcaption>
              </figure>
            ))}
          </div>
        ) : null}
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

      {lesson.vocabulary?.length ? (
        <section className="mt-8">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-leaf" aria-hidden="true" />
              <h2 className="text-xl font-semibold">{copy.vocabulary}</h2>
            </div>
            <span className="rounded-lg bg-mint px-3 py-1 text-xs font-bold uppercase text-leaf">
              {lesson.vocabulary.length} {copy.vocabularyItems}
            </span>
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            {lesson.vocabulary.map((item) => (
              <div key={`${item.word}-${item.meaning}`} className="rounded-lg border border-ink/10 bg-paper p-4">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <p dir={isArabic ? "rtl" : "auto"} className={`font-semibold ${isArabic ? "text-right text-lg leading-8" : ""}`}>
                    {item.word}
                  </p>
                  <p className="rounded-lg bg-mint px-3 py-1 text-sm font-semibold text-leaf">
                    {item.meaning}
                  </p>
                </div>
                <p className="mt-3 text-sm leading-6 text-ink/60">{item.usage}</p>
              </div>
            ))}
          </div>
        </section>
      ) : null}

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
    </>
  );
}
