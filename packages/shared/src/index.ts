export const CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1"] as const;
export const COURSE_LANGUAGES = ["english", "arabic"] as const;

export type CourseLanguage = (typeof COURSE_LANGUAGES)[number];

export type TrackStatus = "active" | "coming_soon";

// Track availability. "coming_soon" tracks are only usable by admins; regular
// users see a disabled "Coming Soon" card. Flip to "active" to launch a track.
export const TRACKS: { language: CourseLanguage; status: TrackStatus }[] = [
  { language: "english", status: "active" },
  { language: "arabic", status: "coming_soon" }
];

// Public production origin, used for metadataBase, canonical URLs, sitemap, and
// robots. Override with NEXT_PUBLIC_SITE_URL at deploy time if the host changes.
export const SITE_URL = "https://conversease.com";

export const skillLabels = {
  speaking_conversation: "Speaking",
  listening: "Listening",
  pronunciation_fluency: "Pronunciation",
  useful_phrases: "Useful Phrases",
  grammar: "Grammar",
  reading: "Reading",
  writing: "Writing"
} as const;

export const productRoutes = {
  home: "/",
  dashboard: "/dashboard",
  courses: "/courses",
  conversationCoach: "/conversation-coach",
  conversationPartner: "/conversation-partner",
  pricing: "/pricing",
  billing: "/billing",
  progress: "/progress",
  levelTests: "/level-tests",
  levelTestA1: "/level-test/A1"
} as const;

export function levelTestRoute(levelCode: string, language = "english") {
  const normalizedLanguage = language.toLowerCase();
  if (normalizedLanguage === "english" || normalizedLanguage === "en") {
    return `/level-test/${levelCode.toUpperCase()}`;
  }
  return `/level-test/${normalizedLanguage}/${levelCode.toUpperCase()}`;
}

export const a1Thresholds = {
  overall: 70,
  lessonCompletion: 80,
  speaking_conversation: 60,
  listening: 60,
  pronunciation_fluency: 55,
  useful_phrases: 60,
  grammar: 60,
  reading: 55,
  writing: 55
} as const;
