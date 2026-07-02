export function placementVisualPrompt({
  label,
  context,
  language,
  kind
}: {
  label: string;
  context: string;
  language: string;
  kind: string;
}) {
  return `Create a polished 16:9 editorial illustration for Conversease language learning.
Lesson: ${label}
Situation: ${kind}. ${context}
Language track: ${language}.

Show a believable real-life conversation involving two or three adult learners in a warm, contemporary Indonesian setting. The scene must clearly communicate the topic through body language, relevant objects, and environment. Use the established Conversease visual style: refined hand-painted digital illustration, warm natural light, earthy cream, olive, navy, and wood tones, clean composition, culturally respectful modest clothing, expressive gestures, and calm professional warmth. No text, letters, logos, watermarks, UI, collage, split panels, speech bubbles, or signage. Keep important people safely inside the frame so the image crops well on responsive cards. Render at 1024×576 pixels.`;
}
