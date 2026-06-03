import { Suspense } from "react";
import { BrandMark } from "@/components/brand-mark";
import { GoogleCallbackPanel } from "@/components/google-callback-panel";

export default function GoogleCallbackPage() {
  return (
    <main className="grid min-h-screen bg-paper px-4 py-10 text-ink">
      <section className="m-auto w-full max-w-md rounded-lg border border-ink/10 bg-white p-6 shadow-sm">
        <BrandMark />
        <div className="mt-8">
          <Suspense fallback={<p className="text-sm text-ink/60">Menyiapkan sesi...</p>}>
            <GoogleCallbackPanel />
          </Suspense>
        </div>
      </section>
    </main>
  );
}
