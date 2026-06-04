"use client";

import { useState } from "react";
import { ConversationCoachPractice } from "@/components/conversation-coach-practice";

const scenarios = [
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
  { slug: "cafe-and-shop-mission", label: "Cafe Mission", description: "Gabungkan order, harga, dan bayar." }
];

export function ConversationCoachWorkspace() {
  const [activeSlug, setActiveSlug] = useState(scenarios[0].slug);

  return (
    <div className="space-y-5">
      <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <p className="text-sm font-semibold uppercase text-leaf">Pilih Skenario</p>
        <h1 className="mt-2 text-2xl font-semibold">Conversation Coach</h1>
        <p className="mt-2 text-sm leading-6 text-ink/60">
          Pilih roleplay yang ingin kamu latih. Setiap skenario punya turn dan feedback sendiri.
        </p>
        <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
          {scenarios.map((scenario) => {
            const selected = scenario.slug === activeSlug;

            return (
              <button
                key={scenario.slug}
                type="button"
                onClick={() => setActiveSlug(scenario.slug)}
                aria-pressed={selected}
                className={`focus-ring rounded-lg border p-4 text-left transition-colors ${
                  selected ? "border-leaf bg-mint" : "border-ink/10 bg-paper hover:bg-mint"
                }`}
              >
                <p className="text-sm font-semibold">{scenario.label}</p>
                <p className="mt-1 text-xs leading-5 text-ink/60">{scenario.description}</p>
              </button>
            );
          })}
        </div>
      </section>

      <ConversationCoachPractice key={activeSlug} lessonSlug={activeSlug} />
    </div>
  );
}
