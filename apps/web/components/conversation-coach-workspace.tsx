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
  { slug: "contact-details-mission", label: "Contact Mission", description: "Gabungkan nama, nomor, dan email." }
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
