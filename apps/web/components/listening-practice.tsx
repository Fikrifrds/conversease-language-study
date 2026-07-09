"use client";

import { useState } from "react";
import { BookOpen, Eye, Headphones, Languages } from "lucide-react";
import { LessonAudioPlayer } from "@/components/lesson-audio-player";

type DialogueLine = {
  speaker: string;
  text: string;
};

type ListeningPracticeProps = {
  lessonSlug: string;
  dialogue: DialogueLine[];
  translation: string[];
};

/**
 * Keeps listening first: learners hear the dialogue before choosing to reveal
 * the English transcript or Indonesian meaning. Both reveals are intentional,
 * so the written support stays available without becoming the default path.
 */
export function ListeningPractice({ lessonSlug, dialogue, translation }: ListeningPracticeProps) {
  const [showTranscript, setShowTranscript] = useState(false);
  const [showTranslation, setShowTranslation] = useState(false);

  return (
    <section className="mt-8 rounded-2xl border border-ink/10 bg-white p-5 shadow-sm sm:p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-leaf">Listening first</p>
          <h2 className="mt-2 text-xl font-semibold">Dengar dulu, lihat bantuan saat perlu</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-ink/65">
            Putar dialog dua kali. Coba tangkap siapa yang berbicara dan inti percakapannya sebelum membuka teks.
          </p>
        </div>
        <LessonAudioPlayer lessonSlug={lessonSlug} />
      </div>

      <div className="mt-5 flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => setShowTranscript((current) => !current)}
          className="focus-ring inline-flex items-center gap-2 rounded-lg border border-ink/15 px-3 py-2 text-sm font-semibold hover:bg-mint"
          aria-pressed={showTranscript}
        >
          <Eye className="h-4 w-4" aria-hidden="true" />
          {showTranscript ? "Sembunyikan transcript" : "Buka transcript English"}
        </button>
        <button
          type="button"
          onClick={() => setShowTranslation((current) => !current)}
          disabled={!showTranscript}
          className="focus-ring inline-flex items-center gap-2 rounded-lg border border-ink/15 px-3 py-2 text-sm font-semibold hover:bg-mint disabled:cursor-not-allowed disabled:opacity-45"
          aria-pressed={showTranslation}
        >
          <Languages className="h-4 w-4" aria-hidden="true" />
          {showTranslation ? "Sembunyikan arti" : "Buka arti Indonesia"}
        </button>
      </div>

      {showTranscript ? (
        <div className="mt-5 space-y-3" aria-live="polite">
          {dialogue.map((line, index) => (
            <div key={`${line.speaker}-${index}`} className="grid gap-2 rounded-xl bg-paper p-4 lg:grid-cols-[120px_1fr_1fr]">
              <span className="font-semibold text-leaf">{line.speaker}</span>
              <p>{line.text}</p>
              <p className="text-ink/60">{showTranslation ? translation[index] : "Arti tersedia setelah kamu memilih bantuan."}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="mt-5 flex items-start gap-3 rounded-xl bg-mint p-4 text-sm leading-6 text-ink/70">
          <Headphones className="mt-0.5 h-5 w-5 shrink-0 text-leaf" aria-hidden="true" />
          <p>Setelah mendengar, coba sebutkan kembali satu frasa yang kamu ingat. Lalu lanjut ke latihan pengucapan di bawah.</p>
        </div>
      )}

      <div className="mt-5 flex items-center gap-2 text-sm text-ink/55">
        <BookOpen className="h-4 w-4 text-coral" aria-hidden="true" />
        Transcript dan arti adalah bantuan—bukan langkah pertama.
      </div>
    </section>
  );
}
