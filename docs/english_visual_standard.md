# English Lesson Visual Standard

English lesson artwork uses a curated scene library. Scene selection must follow the actual
`conversation_situation` and listening dialogue, not an isolated keyword in the lesson title.

## Art direction

- Polished faceless digital editorial illustration.
- Warm Indonesian setting, natural wood, cream, olive, charcoal, beige, and subdued navy.
- Soft natural daylight and painterly shading; not photorealistic, chibi, or glossy 3D.
- Hero: `1672 × 941` landscape. Cards: three `1254 × 1254` crops from the same scene.
- No readable text, logos, trademarks, or watermarks inside the artwork.

## Syariah constraints

- A woman wears loose, opaque, non-form-fitting clothing; a long khimar covering her hair,
  neck, shoulders, and chest; a long skirt or abaya; opaque socks; and closed shoes.
- No bare ankle or foot skin is shown.
- A man and woman are not shown alone together in an enclosed or secluded place.
- Mixed-gender scenes, when a lesson genuinely requires one, must be clearly public or include
  other visible people. Prefer same-gender pairs or groups when the learning action is unchanged.
- No physical contact or suggestive pose.

## Curated scenes

The maintained English scenes live under
`apps/web/public/images/lesson-visual-library/english-*` and are assigned in
`scripts/generate_lesson_visuals.py`.

- Classroom, registration, online learning, directions, cafe ordering, and technical help.
- Test interview, social cafe, transport, retail shop, clinic, travel story, and hotel.
- Workplace meeting, learning coaching, community and culture, presentation, client meeting,
  problem solving, debate, and leadership coaching.

When adding a scene, add its four production assets (`hero.png`, `card-1.png`, `card-2.png`, and
`card-3.png`), its Indonesian alt-text description, and an explicit unit or lesson mapping. Do not
restore automatic fallback rotation for English.
