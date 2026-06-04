"use client";

import { useState } from "react";
import { CheckCircle2, Eye } from "lucide-react";

type QuizItem = {
  question: string;
  answer: string;
};

export function ConversationCheck({ items }: { items: QuizItem[] }) {
  const [revealed, setRevealed] = useState<Record<number, boolean>>({});

  return (
    <div className="mt-4 space-y-3">
      {items.map((item, index) => {
        const isRevealed = Boolean(revealed[index]);

        return (
          <div key={item.question} className="rounded-lg bg-paper p-4">
            <p className="font-medium">{item.question}</p>
            {isRevealed ? (
              <p className="mt-2 flex items-center gap-2 text-sm text-leaf">
                <CheckCircle2 className="h-4 w-4 shrink-0" aria-hidden="true" />
                {item.answer}
              </p>
            ) : (
              <button
                type="button"
                onClick={() => setRevealed((current) => ({ ...current, [index]: true }))}
                className="focus-ring mt-3 inline-flex items-center gap-2 rounded-lg border border-ink/15 px-3 py-2 text-sm font-semibold hover:bg-mint"
              >
                <Eye className="h-4 w-4" aria-hidden="true" />
                Pikirkan dulu, lalu cek jawaban
              </button>
            )}
          </div>
        );
      })}
    </div>
  );
}
