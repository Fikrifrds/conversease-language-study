// Lightweight Google Analytics 4 helpers. Safe no-ops when GA is not configured
// (no measurement id) or when called during SSR.

export const GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID ?? "";

export const analyticsEnabled = GA_MEASUREMENT_ID.length > 0;

type GtagParams = Record<string, string | number | boolean | null | undefined>;

declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
    dataLayer?: unknown[];
  }
}

export function trackPageview(path: string) {
  if (!analyticsEnabled || typeof window === "undefined" || !window.gtag) {
    return;
  }
  window.gtag("event", "page_view", { page_path: path });
}

/**
 * Emit a funnel/conversion event. Names follow GA4 snake_case convention, e.g.
 * "sign_up", "exam_start", "exam_submit", "begin_checkout".
 */
export function trackEvent(name: string, params: GtagParams = {}) {
  if (!analyticsEnabled || typeof window === "undefined" || !window.gtag) {
    return;
  }
  window.gtag("event", name, params);
}
