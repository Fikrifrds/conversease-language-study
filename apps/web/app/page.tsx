import Link from "next/link";
import {
  ArrowRight,
  BookOpenCheck,
  CheckCircle2,
  Headphones,
  MessageCircle,
  Repeat2,
  Sparkles
} from "lucide-react";
import { SITE_URL } from "@conversease/shared";
import { ActionButton } from "@/components/action-button";
import { BrandMark } from "@/components/brand-mark";
import { LandingAuthAction } from "@/components/landing-auth-action";
import { LandingCoachCta } from "@/components/landing-coach-cta";
import { LandingHeroPreview } from "@/components/landing-hero-preview";
import { LandingStats } from "@/components/landing-stats";
import { Reveal } from "@/components/reveal";
import { SectionHeading } from "@/components/section-heading";
import { learningLoop, plans } from "@/lib/data";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? SITE_URL;

const organizationJsonLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Conversease",
  url: siteUrl,
  description:
    "Belajar bahasa Inggris lewat percakapan nyata untuk orang Indonesia, dari level A1 sampai C1.",
  logo: `${siteUrl}/favicon.ico`
};

const learningSteps = [
  {
    icon: Headphones,
    number: "01",
    title: "Dengar dan pahami",
    description: "Dengar dialog yang jelas, lalu pahami konteks dan maknanya dalam bahasa Indonesia."
  },
  {
    icon: Repeat2,
    number: "02",
    title: "Tirukan dan respons",
    description: "Ulangi frasa yang benar, lalu pakai langsung untuk menjawab dalam percakapan."
  },
  {
    icon: Sparkles,
    number: "03",
    title: "Perbaiki dengan feedback",
    description: "Lihat versi yang lebih natural, penjelasan singkat, dan latihan berikutnya."
  }
];

const levelPath = [
  ["A1", "Mulai bicara", "Greeting, perkenalan, dan kebutuhan harian."],
  ["A2", "Percakapan rutin", "Belanja, perjalanan, pekerjaan, dan rencana."],
  ["B1", "Lebih mandiri", "Cerita, opini, masalah, dan pengalaman."],
  ["B2", "Lebih percaya diri", "Diskusi, presentasi, dan situasi profesional."],
  ["C1", "Komunikasi matang", "Nuansa, strategi, dan percakapan kompleks."]
];

export default function HomePage() {
  return (
    <main className="bg-paper text-ink">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationJsonLd) }}
      />

      <section className="landing-hero-bg relative overflow-hidden">
        <div className="landing-grid pointer-events-none absolute inset-0 opacity-50" aria-hidden="true" />
        {/* Ambient floating speech bubbles — a quiet nod to "conversation". */}
        <div className="pointer-events-none absolute inset-0 z-0 hidden overflow-hidden lg:block" aria-hidden="true">
          <span className="animate-float absolute left-[5%] top-[20%] rounded-2xl rounded-tl-sm bg-white/70 px-3 py-2 text-xs font-semibold text-coral shadow-sm backdrop-blur-sm">Hi</span>
          <span className="animate-float-alt absolute right-[9%] top-[14%] rounded-2xl rounded-tr-sm bg-leaf/15 px-3 py-2 text-xs font-semibold text-coral shadow-sm backdrop-blur-sm">Halo!</span>
          <span className="animate-float absolute bottom-[16%] left-[11%] rounded-2xl rounded-bl-sm bg-mint/80 px-3 py-2 text-xs font-semibold text-coral shadow-sm" style={{ animationDelay: "1.6s" }}>Hello</span>
          <span className="animate-float-alt absolute bottom-[24%] right-[7%] rounded-2xl rounded-br-sm bg-white/70 px-3 py-2 text-xs font-semibold text-coral shadow-sm backdrop-blur-sm" style={{ animationDelay: "2.4s" }}>مرحبا</span>
        </div>
        <header className="relative z-20 mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-5 sm:px-6 lg:px-8">
          <BrandMark />
          <nav className="hidden items-center gap-1 rounded-full border border-ink/10 bg-white/75 p-1 text-sm font-medium text-ink/75 shadow-sm backdrop-blur-md md:flex">
            <Link className="rounded-full px-4 py-2 transition hover:bg-mint hover:text-ink" href="/courses">
              Kurikulum
            </Link>
            <Link
              className="rounded-full px-4 py-2 transition hover:bg-mint hover:text-ink"
              href="/conversation-coach"
            >
              Conversation Coach
            </Link>
            <Link className="rounded-full px-4 py-2 transition hover:bg-mint hover:text-ink" href="/pricing">
              Harga
            </Link>
          </nav>
          <LandingAuthAction />
        </header>

        <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 md:hidden lg:px-8">
          <nav className="flex gap-2 overflow-x-auto pb-2" aria-label="Navigasi landing mobile">
            {[
              ["Kurikulum", "/courses"],
              ["Conversation Coach", "/conversation-coach"],
              ["Harga", "/pricing"]
            ].map(([label, href]) => (
              <Link
                key={href}
                className="focus-ring shrink-0 rounded-full border border-ink/10 bg-white/75 px-4 py-2 text-sm font-medium text-ink/75 shadow-sm backdrop-blur-sm"
                href={href}
              >
                {label}
              </Link>
            ))}
          </nav>
        </div>

        <div className="relative z-10 mx-auto grid max-w-7xl gap-12 px-4 pb-20 pt-10 sm:px-6 sm:pt-14 lg:grid-cols-[0.88fr_1.12fr] lg:items-center lg:gap-16 lg:px-8 lg:pb-28 lg:pt-20">
          <div className="max-w-2xl">
            <div className="animate-rise inline-flex items-center gap-2 rounded-full border border-leaf/20 bg-white/80 px-3 py-2 text-xs font-semibold uppercase tracking-[0.12em] text-coral shadow-sm">
              <MessageCircle className="animate-badge-pulse h-4 w-4 text-leaf" aria-hidden="true" />
              Conversation-first English · A1–C1
            </div>
            <h1 className="animate-rise mt-6 text-5xl font-semibold leading-[0.98] tracking-[-0.045em] text-ink sm:text-6xl lg:text-[4.6rem]" style={{ animationDelay: "80ms" }}>
              Paham English,
              <span className="mt-2 block text-leaf">berani bicara.</span>
            </h1>
            <p className="animate-rise mt-6 max-w-xl text-base font-medium leading-8 text-ink/70 sm:text-lg" style={{ animationDelay: "160ms" }}>
              Belajar English lewat percakapan nyata. Dengar dialog, praktik bicara, lalu dapat
              feedback langsung dalam bahasa Indonesia.
            </p>
            <div className="animate-rise mt-8 flex flex-col gap-3 sm:flex-row sm:flex-wrap" style={{ animationDelay: "240ms" }}>
              <ActionButton href="/register" icon={ArrowRight} tone="leaf" className="w-full px-6 sm:w-auto">
                Mulai Belajar Gratis
              </ActionButton>
              <LandingCoachCta className="w-full px-6 sm:w-auto" />
            </div>
            <div className="animate-rise mt-5 hidden flex-wrap gap-x-5 gap-y-2 text-sm font-medium text-ink/60 sm:flex" style={{ animationDelay: "320ms" }}>
              {["Tanpa kartu kredit", "Mulai dari level kamu", "Feedback dalam bahasa Indonesia"].map((item) => (
                <span key={item} className="inline-flex items-center gap-1.5">
                  <CheckCircle2 className="h-4 w-4 text-leaf" aria-hidden="true" />
                  {item}
                </span>
              ))}
            </div>
            <LandingStats className="mt-8 hidden max-w-xl grid-cols-3 gap-2 rounded-2xl border border-ink/10 bg-white/70 p-2 shadow-sm backdrop-blur-md sm:grid" />
          </div>

          <div className="animate-rise relative" style={{ animationDelay: "200ms" }}>
            <LandingHeroPreview />
            <LandingStats className="mt-6 grid grid-cols-3 gap-2 rounded-2xl border border-ink/10 bg-white/80 p-2 shadow-sm sm:hidden" />
          </div>
        </div>
      </section>

      <section className="border-y border-ink/10 bg-white" aria-label="Alur belajar Conversease">
        <Reveal className="mx-auto grid max-w-7xl grid-cols-2 gap-2 px-4 py-5 sm:px-6 md:grid-cols-3 lg:grid-cols-6 lg:px-8">
          {learningLoop.map((item, index) => (
            <div
              key={item.label}
              className="group flex min-h-12 items-center gap-2.5 rounded-xl bg-paper px-3 py-3 transition hover:-translate-y-0.5 hover:bg-mint hover:shadow-sm"
            >
              <span className="text-[0.65rem] font-bold text-ink/30">0{index + 1}</span>
              <item.icon className="h-4 w-4 text-leaf transition group-hover:scale-125" aria-hidden="true" />
              <span className="text-sm font-semibold">{item.label}</span>
            </div>
          ))}
        </Reveal>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-28">
        <Reveal className="grid items-end gap-6 lg:grid-cols-[1fr_0.65fr]">
          <SectionHeading eyebrow="Cara belajar" title="Bukan cuma nonton materi">
            Setiap lesson membawa kamu dari memahami percakapan sampai berani memberi respons
            dengan kalimatmu sendiri.
          </SectionHeading>
          <p className="max-w-lg text-base leading-7 text-ink/60 lg:justify-self-end">
            Satu pola yang konsisten membuat progres terasa jelas—tanpa bingung harus belajar apa
            setelahnya.
          </p>
        </Reveal>
        <div className="mt-10 grid gap-4 lg:grid-cols-3">
          {learningSteps.map((step, index) => (
            <Reveal key={step.number} delay={index * 120} className="h-full">
              <article className="group h-full rounded-3xl border border-ink/10 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-soft sm:p-7">
                <div className="flex items-center justify-between">
                  <span className="grid h-12 w-12 place-items-center rounded-2xl bg-mint text-leaf transition group-hover:scale-110 group-hover:bg-leaf group-hover:text-white">
                    <step.icon className="h-6 w-6" aria-hidden="true" />
                  </span>
                  <span className="text-sm font-bold tracking-[0.16em] text-ink/20">{step.number}</span>
                </div>
                <h3 className="mt-8 text-xl font-semibold">{step.title}</h3>
                <p className="mt-3 text-sm leading-7 text-ink/65">{step.description}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="bg-ink text-white">
        <div className="mx-auto grid max-w-7xl gap-10 px-4 py-20 sm:px-6 lg:grid-cols-[0.72fr_1.28fr] lg:items-center lg:px-8 lg:py-24">
          <Reveal>
            <p className="text-sm font-semibold uppercase tracking-[0.12em] text-sun">Kurikulum terarah</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-[-0.03em] sm:text-4xl">
              Mulai dari levelmu, lanjut tanpa menebak.
            </h2>
            <p className="mt-4 max-w-xl text-base leading-7 text-white/65">
              Lima level CEFR membawa kamu dari percakapan dasar sampai komunikasi profesional dan
              akademik yang lebih matang.
            </p>
            <ActionButton href="/courses" icon={BookOpenCheck} tone="light" className="mt-7 px-6">
              Lihat Semua Kurikulum
            </ActionButton>
          </Reveal>
          <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
            {levelPath.map(([level, title, description], index) => (
              <Reveal key={level} delay={index * 90} className={index === 4 ? "sm:col-span-2 xl:col-span-1" : ""}>
                <Link
                  href="/courses"
                  className={`focus-ring block h-full rounded-2xl border p-5 transition hover:-translate-y-1 hover:bg-white/15 hover:shadow-soft ${
                    index === 0 ? "border-leaf/60 bg-leaf/20" : "border-white/10 bg-white/[0.07]"
                  }`}
                >
                  <span className="inline-flex rounded-full bg-white/10 px-2.5 py-1 text-xs font-bold text-sun">
                    {level}
                  </span>
                  <h3 className="mt-5 font-semibold">{title}</h3>
                  <p className="mt-2 text-xs leading-5 text-white/55">{description}</p>
                </Link>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-24">
        <Reveal className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <SectionHeading eyebrow="Harga" title="Mulai gratis, upgrade saat siap">
            Free cukup untuk mencoba alurnya. Pro membuka kurikulum English lengkap A1–C1,
            feedback detail, evaluasi level, progress, dan Conversation Coach.
          </SectionHeading>
          <ActionButton href="/pricing" icon={ArrowRight} tone="outline" className="shrink-0 px-6">
            Bandingkan Paket
          </ActionButton>
        </Reveal>
        <div className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {plans.slice(0, 4).map((plan, index) => (
            <Reveal key={plan.key} delay={index * 100} className="h-full">
              <Link
                href="/pricing"
                className={`focus-ring relative block h-full rounded-2xl border p-5 transition hover:-translate-y-1 hover:shadow-soft ${
                  index === 3 ? "border-leaf bg-ink text-white" : "border-ink/10 bg-white"
                }`}
              >
                {index === 3 ? (
                  <span className="absolute right-4 top-4 rounded-full bg-sun px-2.5 py-1 text-[0.65rem] font-bold uppercase text-ink">
                    Paling hemat
                  </span>
                ) : null}
                <h3 className="font-semibold">{plan.name}</h3>
                <p className={`mt-2 text-sm ${index === 3 ? "text-white/60" : "text-ink/55"}`}>{plan.access}</p>
                <p className={`mt-8 text-xl font-semibold ${index === 3 ? "text-sun" : "text-leaf"}`}>{plan.price}</p>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      <footer className="border-t border-ink/10 bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-5 px-4 py-8 text-sm text-ink/60 sm:px-6 md:flex-row md:items-center md:justify-between lg:px-8">
          <div>
            <BrandMark size="sm" />
            <p className="mt-2">Dari paham menjadi berani bicara.</p>
          </div>
          <div className="flex flex-wrap gap-5 font-medium">
            <Link className="hover:text-leaf" href="/dashboard">Dashboard</Link>
            <Link className="hover:text-leaf" href="/courses">Kursus</Link>
            <Link className="hover:text-leaf" href="/pricing">Harga</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
