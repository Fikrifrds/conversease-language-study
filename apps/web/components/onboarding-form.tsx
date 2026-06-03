"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowRight, CheckCircle2 } from "lucide-react";
import { getOnboardingProfile, saveOnboardingProfile } from "@/lib/learning-api";

const goalOptions = [
  "Daily conversation",
  "Job interview",
  "Work or meeting",
  "Pronunciation",
  "Start from zero"
];

const confidenceOptions = [
  "Saya malu bicara",
  "Saya paham sedikit tapi sulit merespons",
  "Saya bisa membaca tapi sulit speaking"
];

const targetOptions = [
  { label: "10 minutes/day", minutes: 10 },
  { label: "15 minutes/day", minutes: 15 },
  { label: "30 minutes/day", minutes: 30 }
];

export function OnboardingForm() {
  const router = useRouter();
  const [primaryGoal, setPrimaryGoal] = useState(goalOptions[0]);
  const [confidenceLevel, setConfidenceLevel] = useState(confidenceOptions[0]);
  const [dailyTargetMinutes, setDailyTargetMinutes] = useState(targetOptions[0].minutes);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let ignore = false;

    async function loadOnboarding() {
      try {
        const profile = await getOnboardingProfile();

        if (!ignore && profile) {
          setPrimaryGoal(profile.primaryGoal);
          setConfidenceLevel(profile.confidenceLevel);
          setDailyTargetMinutes(profile.dailyTargetMinutes);
        }
      } catch {
        if (!ignore) {
          setError("Preferensi belum bisa dimuat.");
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }

    loadOnboarding();

    return () => {
      ignore = true;
    };
  }, []);

  async function handleContinue() {
    setError("");
    setIsSaving(true);

    try {
      await saveOnboardingProfile({
        primaryGoal,
        confidenceLevel,
        dailyTargetMinutes
      });
      router.replace("/dashboard");
    } catch {
      setError("Preferensi belum bisa disimpan. Coba lagi sebentar.");
      setIsSaving(false);
    }
  }

  return (
    <div className="mt-8 space-y-5">
      <OptionGroup
        title="Primary goal"
        options={goalOptions.map((label) => ({ label, value: label }))}
        value={primaryGoal}
        onChange={setPrimaryGoal}
      />
      <OptionGroup
        title="Current confidence"
        options={confidenceOptions.map((label) => ({ label, value: label }))}
        value={confidenceLevel}
        onChange={setConfidenceLevel}
      />
      <OptionGroup
        title="Daily practice target"
        options={targetOptions.map((option) => ({
          label: option.label,
          value: String(option.minutes)
        }))}
        value={String(dailyTargetMinutes)}
        onChange={(value) => setDailyTargetMinutes(Number(value))}
      />

      {error ? <p className="rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">{error}</p> : null}

      <section className="rounded-lg bg-ink p-5 text-white">
        <p className="text-sm text-white/70">Recommended Path</p>
        <h2 className="mt-2 text-2xl font-semibold">A1 - Start Simple Conversations</h2>
        <p className="mt-2 text-white/75">
          Today&apos;s Mission: Greeting & Introducing Yourself
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={handleContinue}
            disabled={isLoading || isSaving}
            className="focus-ring inline-flex items-center gap-2 rounded-lg bg-white px-4 py-3 text-sm font-semibold text-ink hover:bg-mint disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSaving ? "Saving" : "Continue"}
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </button>
          <Link
            href="/dashboard"
            className="focus-ring inline-flex items-center gap-2 rounded-lg border border-white/20 px-4 py-3 text-sm font-semibold text-white hover:bg-white/10"
          >
            Skip for now
          </Link>
        </div>
      </section>
    </div>
  );
}

function OptionGroup({
  title,
  options,
  value,
  onChange
}: {
  title: string;
  options: Array<{ label: string; value: string }>;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold">{title}</h2>
      <div className="mt-4 grid gap-3 md:grid-cols-3">
        {options.map((option) => {
          const selected = option.value === value;

          return (
            <button
              key={option.value}
              type="button"
              onClick={() => onChange(option.value)}
              className={`focus-ring flex min-h-16 items-center justify-between gap-3 rounded-lg p-4 text-left ${
                selected ? "bg-mint" : "bg-paper hover:bg-mint"
              }`}
            >
              <span className="text-sm font-medium">{option.label}</span>
              {selected ? <CheckCircle2 className="h-4 w-4 shrink-0 text-leaf" aria-hidden="true" /> : null}
            </button>
          );
        })}
      </div>
    </section>
  );
}
