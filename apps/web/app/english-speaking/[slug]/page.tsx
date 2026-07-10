import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowRight, Headphones, MessageCircle, Mic, Volume2 } from "lucide-react";
import { SITE_URL } from "@conversease/shared";
import { englishSpeakingPages, englishSpeakingPagesBySlug } from "@/lib/english-speaking-pages";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? SITE_URL;

export function generateStaticParams() {
  return englishSpeakingPages.map((page) => ({ slug: page.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const page = englishSpeakingPagesBySlug[params.slug];
  if (!page) {
    return { title: "English speaking practice", robots: { index: false, follow: false } };
  }
  return {
    title: page.title,
    description: page.description,
    alternates: { canonical: `/english-speaking/${page.slug}` },
    openGraph: {
      title: `${page.title} | Conversease`,
      description: page.description,
      url: `${siteUrl}/english-speaking/${page.slug}`,
      siteName: "Conversease",
      type: "article"
    }
  };
}

export default function EnglishSpeakingPage({ params }: { params: { slug: string } }) {
  const page = englishSpeakingPagesBySlug[params.slug];
  if (!page) {
    notFound();
  }

  const lessonHref = `/lessons/${page.lessonSlug}`;

  return (
    <main className="min-h-screen bg-paper text-ink">
      <header className="border-b border-ink/10 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-5 sm:px-6">
          <Link href="/" className="font-semibold text-ink">Conversease</Link>
          <Link href="/register" className="focus-ring rounded-full bg-ink px-4 py-2 text-sm font-semibold text-white hover:bg-leaf">
            Mulai gratis
          </Link>
        </div>
      </header>

      <article className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:py-16">
        <div className="max-w-3xl">
          <div className="flex flex-wrap items-center gap-2 text-xs font-bold uppercase tracking-wide text-leaf">
            <span className="rounded-full bg-mint px-3 py-1">English speaking</span>
            <span className="rounded-full bg-[#fff2dc] px-3 py-1 text-coral">{page.level}</span>
          </div>
          <h1 className="mt-5 text-4xl font-semibold tracking-tight sm:text-5xl">{page.title}</h1>
          <p className="mt-5 text-lg leading-8 text-ink/70">{page.description}</p>
        </div>

        <div className="mt-10 grid gap-5 lg:grid-cols-[1fr_0.75fr]">
          <section className="rounded-2xl border border-ink/10 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-2">
              <MessageCircle className="h-5 w-5 text-leaf" aria-hidden="true" />
              <h2 className="text-xl font-semibold">Situasi percakapan</h2>
            </div>
            <p className="mt-3 leading-7 text-ink/70">{page.context}</p>
            <p className="mt-4 rounded-xl bg-mint p-4 text-sm leading-6 text-ink/75">
              <span className="font-semibold text-ink">Target:</span> {page.outcome}
            </p>
          </section>

          <section className="rounded-2xl bg-ink p-6 text-white">
            <div className="flex items-center gap-2">
              <Headphones className="h-5 w-5 text-sun" aria-hidden="true" />
              <h2 className="text-xl font-semibold">Cara berlatih</h2>
            </div>
            <ol className="mt-4 space-y-3 text-sm leading-6 text-white/75">
              <li><span className="font-semibold text-white">1.</span> Dengarkan dialog dua kali.</li>
              <li><span className="font-semibold text-white">2.</span> Baca transcript hanya saat perlu.</li>
              <li><span className="font-semibold text-white">3.</span> Ucapkan responsmu tanpa script.</li>
              <li><span className="font-semibold text-white">4.</span> Ulangi setelah mendapat feedback.</li>
            </ol>
          </section>
        </div>

        <section className="mt-5 rounded-2xl border border-ink/10 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-2">
            <Volume2 className="h-5 w-5 text-leaf" aria-hidden="true" />
            <h2 className="text-xl font-semibold">Contoh dialog</h2>
          </div>
          <div className="mt-5 space-y-3">
            {page.dialogue.map((line, index) => (
              <div key={`${line.speaker}-${index}`} className="grid gap-2 rounded-xl bg-paper p-4 sm:grid-cols-[100px_1fr]">
                <span className="font-semibold text-leaf">{line.speaker}</span>
                <p className="leading-7">{line.text}</p>
              </div>
            ))}
          </div>
          <p className="mt-4 text-sm leading-6 text-ink/55">Di lesson lengkap, dialog ini tersedia dengan audio dan latihan listening bertahap.</p>
        </section>

        <section className="mt-5 grid gap-5 md:grid-cols-[1fr_1fr]">
          <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold">Useful phrases</h2>
            <div className="mt-4 space-y-3">
              {page.phrases.map((item) => (
                <div key={item.phrase} className="rounded-xl bg-paper p-4">
                  <p className="font-semibold">{item.phrase}</p>
                  <p className="mt-1 text-sm text-ink/60">{item.meaning}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-2xl bg-[#fff2dc] p-6">
            <div className="flex items-center gap-2">
              <Mic className="h-5 w-5 text-coral" aria-hidden="true" />
              <h2 className="text-xl font-semibold">Speaking challenge</h2>
            </div>
            <p className="mt-4 leading-7 text-ink/75">{page.challenge}</p>
            <Link href={lessonHref} className="focus-ring mt-6 inline-flex items-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white hover:bg-leaf">
              Buka lesson dan latihan
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </div>
        </section>

        <section className="mt-8 rounded-2xl bg-leaf p-6 text-white sm:p-8">
          <p className="text-sm font-semibold uppercase tracking-wide text-white/70">Lanjutkan latihan</p>
          <h2 className="mt-2 text-2xl font-semibold">{page.lessonTitle}</h2>
          <p className="mt-3 max-w-2xl leading-7 text-white/80">
            Dengarkan dialog, rekam jawabanmu, dan lakukan roleplay dengan Conversation Coach.
          </p>
          <Link href={lessonHref} className="focus-ring mt-5 inline-flex items-center gap-2 rounded-lg bg-white px-5 py-3 text-sm font-semibold text-ink hover:bg-mint">
            Mulai latihan English
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Link>
        </section>
      </article>
    </main>
  );
}
