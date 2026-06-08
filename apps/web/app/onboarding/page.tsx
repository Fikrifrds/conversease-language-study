import { AppShell } from "@/components/app-shell";
import { OnboardingForm } from "@/components/onboarding-form";

export default function OnboardingPage() {
  return (
    <AppShell requireAuth>
      <section className="mx-auto max-w-5xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <p className="text-sm font-semibold uppercase text-leaf">Onboarding</p>
        <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">Atur jalur percakapanmu</h1>
        <OnboardingForm />
      </section>
    </AppShell>
  );
}
