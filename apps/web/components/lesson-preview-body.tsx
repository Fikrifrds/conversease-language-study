"use client";

import Link from "next/link";
import { ArrowRight, BookOpen, Headphones, Lock, MessageCircle, Mic } from "lucide-react";

interface LessonPreviewBodyProps {
  slug: string;
  title: string;
  conversationGoal: string;
  language: string;
}

export function LessonPreviewBody({ slug, title, conversationGoal, language }: LessonPreviewBodyProps) {
  const isEnglish = language === "english";

  return (
    <div className="mt-6 space-y-6">
      {/* Conversation Goal - Public */}
      <section className="rounded-lg bg-mint p-5">
        <h2 className="flex items-center gap-2 text-lg font-semibold">
          <MessageCircle className="h-5 w-5 text-leaf" />
          {isEnglish ? "Conversation Goal" : "Target Percakapan"}
        </h2>
        <p className="mt-3 leading-7 text-ink/80">{conversationGoal}</p>
      </section>

      {/* What you'll learn - Public */}
      <section className="rounded-lg border border-ink/10 bg-white p-5">
        <h2 className="flex items-center gap-2 text-lg font-semibold">
          <BookOpen className="h-5 w-5 text-leaf" />
          {isEnglish ? "What You'll Learn" : "Yang Akan Dipelajari"}
        </h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          {[
            { icon: Headphones, label: isEnglish ? "Listening" : "Mendengarkan", desc: isEnglish ? "Dialog dan audio" : "Dialog dan audio" },
            { icon: BookOpen, label: isEnglish ? "Vocabulary" : "Kosa Kata", desc: isEnglish ? "Kata dan frasa baru" : "Kata dan frasa baru" },
            { icon: Mic, label: isEnglish ? "Speaking" : "Berbicara", desc: isEnglish ? "Latihan pengucapan" : "Latihan pengucapan" },
            { icon: MessageCircle, label: isEnglish ? "Conversation" : "Percakapan", desc: isEnglish ? "Roleplay terarah" : "Roleplay terarah" },
          ].map((item) => (
            <div key={item.label} className="flex items-start gap-3 rounded-lg bg-paper p-4">
              <item.icon className="mt-0.5 h-5 w-5 shrink-0 text-leaf" />
              <div>
                <p className="font-semibold">{item.label}</p>
                <p className="text-sm text-ink/60">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Locked content overlay */}
      <div className="relative overflow-hidden rounded-lg border border-ink/10 bg-white">
        {/* Blurred preview */}
        <div className="blur-sm select-none pointer-events-none p-5 opacity-50">
          <div className="space-y-4">
            <div className="h-4 w-3/4 rounded bg-ink/10" />
            <div className="h-4 w-1/2 rounded bg-ink/10" />
            <div className="h-4 w-5/6 rounded bg-ink/10" />
            <div className="mt-6 h-32 rounded-lg bg-ink/5" />
            <div className="h-4 w-2/3 rounded bg-ink/10" />
            <div className="h-4 w-1/2 rounded bg-ink/10" />
          </div>
        </div>

        {/* Lock overlay */}
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm">
          <div className="rounded-full bg-mint p-4">
            <Lock className="h-8 w-8 text-leaf" />
          </div>
          <h3 className="mt-4 text-xl font-semibold">
            {isEnglish ? "Full Lesson Content" : "Konten Lesson Lengkap"}
          </h3>
          <p className="mt-2 max-w-md text-center text-sm text-ink/60">
            {isEnglish
              ? "Access the complete lesson with dialogue, vocabulary, grammar, pronunciation practice, and Conversation Coach."
              : "Akses lesson lengkap dengan dialog, kosa kata, grammar, latihan pengucapan, dan Conversation Coach."}
          </p>
          <div className="mt-6 flex flex-col gap-3 sm:flex-row">
            <Link
              href="/register"
              className="focus-ring inline-flex items-center gap-2 rounded-lg bg-leaf px-6 py-3 text-sm font-semibold text-white hover:bg-ink"
            >
              {isEnglish ? "Sign Up Free" : "Daftar Gratis"}
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/login"
              className="focus-ring inline-flex items-center gap-2 rounded-lg border border-ink/20 px-6 py-3 text-sm font-semibold hover:bg-paper"
            >
              {isEnglish ? "Log In" : "Masuk"}
            </Link>
          </div>
        </div>
      </div>

      {/* CTA section */}
      <section className="rounded-lg bg-ink p-6 text-center text-white">
        <h2 className="text-xl font-semibold">
          {isEnglish ? "Start Learning English Today" : "Mulai Belajar Bahasa Inggris Hari Ini"}
        </h2>
        <p className="mt-2 text-white/70">
          {isEnglish
            ? "Bangun kebiasaan speaking dengan latihan English berbasis percakapan."
            : "Bergabung dengan ribuan pelajar Indonesia yang meningkatkan bahasa Inggris mereka melalui latihan berbasis percakapan."}
        </p>
        <Link
          href="/register"
          className="focus-ring mt-4 inline-flex items-center gap-2 rounded-lg bg-leaf px-6 py-3 text-sm font-semibold text-white hover:bg-ink"
        >
          {isEnglish ? "Get Started Free" : "Mulai Gratis"}
          <ArrowRight className="h-4 w-4" />
        </Link>
      </section>
    </div>
  );
}
