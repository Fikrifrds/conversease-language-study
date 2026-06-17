import Image from "next/image";
import Link from "next/link";
import { ArrowRight, CheckCircle2, Play } from "lucide-react";
import { ActionButton } from "@/components/action-button";
import { BrandMark } from "@/components/brand-mark";
import { LandingAuthAction } from "@/components/landing-auth-action";
import { LandingCoachCta } from "@/components/landing-coach-cta";
import { SectionHeading } from "@/components/section-heading";
import { learningLoop, mission, plans } from "@/lib/data";

export default function HomePage() {
  return (
    <main className="bg-paper text-ink">
      <section className="relative min-h-[70svh] overflow-hidden sm:min-h-[82svh]">
        <Image
          src="/images/hero-realistic.png"
          alt="Suasana meja belajar percakapan yang nyata"
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="hero-mask absolute inset-0" />
        <header className="relative z-10 mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-4 sm:px-6 lg:px-8">
          <BrandMark tone="light" />
          <nav className="hidden items-center gap-2 text-sm font-medium text-white/90 md:flex">
            <Link className="rounded-lg px-3 py-2 hover:bg-white/10" href="/courses">
              Kurikulum
            </Link>
            <Link className="rounded-lg px-3 py-2 hover:bg-white/10" href="/conversation-coach">
              Conversation Coach
            </Link>
            <Link className="rounded-lg px-3 py-2 hover:bg-white/10" href="/pricing">
              Harga
            </Link>
          </nav>
          <LandingAuthAction />
        </header>
        <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 md:hidden lg:px-8">
          <nav className="flex gap-2 overflow-x-auto pb-2" aria-label="Navigasi landing mobile">
            <Link className="focus-ring shrink-0 rounded-lg bg-white/10 px-3 py-2 text-sm font-medium text-white" href="/courses">
              Kurikulum
            </Link>
            <Link
              className="focus-ring shrink-0 rounded-lg bg-white/10 px-3 py-2 text-sm font-medium text-white"
              href="/conversation-coach"
            >
              Conversation Coach
            </Link>
            <Link className="focus-ring shrink-0 rounded-lg bg-white/10 px-3 py-2 text-sm font-medium text-white" href="/pricing">
              Harga
            </Link>
          </nav>
        </div>
        <div className="relative z-10 mx-auto grid max-w-7xl gap-10 px-4 pb-16 pt-12 sm:px-6 sm:pt-16 lg:grid-cols-[0.95fr_1.05fr] lg:px-8 lg:pt-24">
          <div className="max-w-2xl text-white">
            <p className="text-sm font-semibold uppercase text-sun">Bahasa jadi bisa dipakai</p>
            <h1 className="mt-4 text-4xl font-semibold leading-[1.02] sm:text-6xl lg:text-7xl">
              Conversease
            </h1>
            <p className="mt-5 max-w-xl text-lg leading-8 text-white/90">
              Belajar bahasa lewat percakapan terarah. Mulai dari English speaking, lalu masuk ke
              Arabic beta untuk memahami dialog formal, instruksi kelas, dan bacaan pendek.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:flex-wrap">
              <ActionButton href="/register" icon={ArrowRight} tone="light">
                Mulai Belajar Gratis
              </ActionButton>
              <LandingCoachCta />
            </div>
          </div>
          <div className="self-end lg:pl-8">
            <div className="max-w-md rounded-lg border border-white/20 bg-white/90 p-4 shadow-soft backdrop-blur">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs font-semibold uppercase text-leaf">Misi Hari Ini</p>
                  <h2 className="mt-1 text-xl font-semibold">{mission.title}</h2>
                </div>
                <span className="rounded-lg bg-sun px-3 py-1 text-xs font-bold text-ink">
                  {mission.level}
                </span>
              </div>
              <p className="mt-3 text-sm leading-6 text-ink/70">{mission.prompt}</p>
              <div className="mt-4 grid gap-2 text-sm sm:grid-cols-3">
                <div className="rounded-lg bg-mint p-3">
                  <p className="font-semibold">Dengar</p>
                  <p className="text-ink/60">Dialog</p>
                </div>
                <div className="rounded-lg bg-[#fff2dc] p-3">
                  <p className="font-semibold">Ulangi</p>
                  <p className="text-ink/60">Frasa</p>
                </div>
                <div className="rounded-lg bg-[#fde7df] p-3">
                  <p className="font-semibold">Bicara</p>
                  <p className="text-ink/60">Coach</p>
                </div>
              </div>
              <Link
                href={`/lessons/${mission.lessonSlug}`}
                className="focus-ring mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-semibold text-white hover:bg-ink"
              >
                <Play className="h-4 w-4" aria-hidden="true" />
                Mulai Misi
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="border-b border-ink/10 bg-white">
        <div className="mx-auto grid max-w-7xl gap-4 px-4 py-6 sm:px-6 md:grid-cols-6 lg:px-8">
          {learningLoop.map((item) => (
            <div key={item.label} className="flex items-center gap-2 rounded-lg bg-paper px-3 py-3">
              <item.icon className="h-4 w-4 text-leaf" aria-hidden="true" />
              <span className="text-sm font-semibold">{item.label}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <SectionHeading eyebrow="Learning Tracks" title="English aktif, Arabic mulai beta">
          Conversease tetap conversation-first: dengar, pahami, tirukan, respons, lalu dapat
          feedback yang jelas untuk tiap track bahasa.
        </SectionHeading>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            ["English Conversation", "Mulai dari greeting, self-introduction, daily routine, simple questions, sampai evaluasi A1."],
            ["Arabic", "Fondasi Arabic formal untuk sapaan umum, perkenalan, instruksi kelas, dan frasa ketika belum paham."],
            ["Bicara dengan Jelas", "Ulangi frasa berguna dan bangun rasa percaya diri pelafalan langkah demi langkah."],
            ["Feedback Percakapan", "Versi lebih baik, penjelasan Indonesia, skor, dan latihan berikutnya."]
          ].map(([title, text]) => (
            <article key={title} className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
              <CheckCircle2 className="h-5 w-5 text-leaf" aria-hidden="true" />
              <h3 className="mt-4 text-lg font-semibold">{title}</h3>
              <p className="mt-2 text-sm leading-6 text-ink/70">{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="bg-ink text-white">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-16 sm:px-6 lg:grid-cols-[0.8fr_1.2fr] lg:px-8">
          <SectionHeading eyebrow="Harga" title="Free + Pro" tone="light">
            Pro membuka kurikulum aktif, feedback detail, evaluasi level, laporan progress, dan
            akses Arabic selama beta. Setelah launch publik, English, Arabic, dan All Access
            bisa dipisahkan sebagai paket berbeda.
          </SectionHeading>
          <div className="grid gap-3 md:grid-cols-2">
            {plans.slice(0, 4).map((plan) => (
              <Link
                key={plan.key}
                href="/pricing"
                className="focus-ring rounded-lg border border-white/10 bg-white/10 p-4 hover:bg-white/20"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="font-semibold">{plan.name}</h3>
                    <p className="mt-1 text-sm text-white/70">{plan.access}</p>
                  </div>
                  <span className="text-lg font-semibold text-sun">{plan.price}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <footer className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-8 text-sm text-ink/60 sm:px-6 md:flex-row md:items-center md:justify-between lg:px-8">
        <p>Conversease. Dari paham menjadi berani bicara.</p>
        <div className="flex flex-wrap gap-4">
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/courses">Kursus</Link>
          <Link href="/pricing">Harga</Link>
        </div>
      </footer>
    </main>
  );
}
