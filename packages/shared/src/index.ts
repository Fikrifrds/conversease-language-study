export const CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1"] as const;

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

export function levelTestRoute(levelCode: string) {
  return `/level-test/${levelCode.toUpperCase()}`;
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
