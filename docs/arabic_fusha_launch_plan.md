# Arabic Fusha Launch Plan

## Product Positioning

Conversease should move from "English conversation practice" to a broader
language-learning brand with distinct tracks:

- Conversease English: practical speaking for work, study, travel, and everyday
  confidence.
- Conversease Arabic Fusha: formal Arabic for Indonesian Muslim learners who
  want to understand structured conversation, study circles, Saudi scholars,
  hadith language, and foundational Islamic texts.

Arabic Fusha is not positioned as street dialect Arabic. It should clearly say:

- Fusha / Modern Standard Arabic first.
- Built for Indonesian learners.
- Conversation-first, but with stronger reading/listening support than English.
- Inspired by communicative Arabic-course structure, without copying licensed
  material such as Arabiyyah Baina Yadaik.

Working promise:

> Belajar Bahasa Arab Fusha secara bertahap: dari bunyi, kosakata, dan dialog
> formal, sampai mulai memahami kajian, ungkapan ulama, dan teks hadits dasar.

## Curriculum Direction

Arabic needs an extra foundation layer that English does not need:

1. Script and sound
   - Arabic letters, harakat, long vowels, sukun, shaddah, tanwin.
   - Focus sounds for Indonesian learners: `ع`, `ح`, `خ`, `ق`, `ص`, `ض`, `ط`, `ظ`,
     hamzah, and vowel length.
2. Fusha conversation
   - Greetings, introductions, origin, family, study, class, mosque, book,
     teacher/student interactions, asking for repetition.
3. Formal listening
   - Common study-circle phrases: `قال الشيخ`, `معنى الحديث`, `الدليل على ذلك`,
     `هذه مسألة مهمة`, `انتبه`, `نعم`, `أحسنت`.
4. Hadith and Islamic register
   - Language analysis of short, safe texts.
   - Avoid making legal/theological claims without human review.

The first implementation should be a small pilot:

- Language: Arabic Fusha
- Level: A1
- Unit count: 1
- Lesson count: 5
- UI language: Indonesian
- Target text: Arabic with transliteration optional
- Audio: optional after text flow is stable
- Pronunciation scoring: beta only until Arabic normalization is implemented

Suggested first unit:

1. Sapaan Fusha dan adab memulai percakapan
2. Menyebut nama dan asal
3. Instruksi kelas dan kajian
4. Bertanya saat belum paham
5. Mini mission: perkenalan Fusha singkat

## Pricing Recommendation

Do not launch Arabic as permanently bundled with English by accident.

During the pilot, Arabic can be included for existing Pro users as a beta benefit
because the current billing model only has one Pro entitlement. This is simple,
friendly to early users, and lets us validate the course before adding billing
complexity.

For public launch, move toward product-scoped access:

- Free: selected intro lessons from each track.
- English Pro: English track access + shared coach minutes.
- Arabic Pro: Arabic track access + shared coach minutes.
- All Access: English + Arabic + future tracks + shared coach minutes.
- Top-up minutes: shared across tracks.

Recommended beta stance:

> Arabic Fusha pilot is included for active Pro users while in beta. After public
> launch, Conversease may offer separate English, Arabic, and All Access plans.
> Existing active Pro users keep beta access until their current subscription
> period ends.

This avoids surprising English buyers, avoids underpricing Arabic forever, and
lets Arabic target a different audience and willingness-to-pay later.

## Technical Implications

The current app is mostly English-centric:

- `content/curriculum/english/<LEVEL>` is assumed in several loaders/generators.
- Web generated data is built from English levels only.
- Billing access is a single `is_pro` check.
- Learning progress defaults to English A1.
- Conversation feedback prompt is explicitly for English A1 beginners.
- Pronunciation matching normalizes Latin words only.
- Text-to-speech voice registry is curated for English voices.

Implementation should avoid a large rewrite at the start. The first technical
target is "multi-language ready enough for Arabic A1 pilot".

## Implementation Sequence

### Phase 1 - Product and Data Foundation

- Add a language-aware course model in curriculum loading.
- Ensure course payloads include `language` and `language_code`.
- Keep lesson slugs globally unique for now, e.g. prefix Arabic slugs with
  `arabic-` or use unique course context in routes later.
- Generate web data from all active language folders, not English only.
- Add Arabic A1 pilot content scaffold.

### Phase 2 - UI Positioning

- Update landing/pricing/courses copy from "English only" to track-based
  Conversease.
- Add track labels: English and Arabic Fusha.
- Render Arabic target text with `dir="rtl"` or `dir="auto"`.
- Keep Indonesian explanations left-to-right.

### Phase 3 - Billing Entitlements

Short term:

- Keep current `is_pro` access for Arabic beta.
- Make pricing copy clear that beta access is temporary.

Long term:

- Add product-scoped entitlements, for example `english`, `arabic`, `all_access`.
- Add plan metadata such as `included_tracks`.
- Gate courses by track instead of only `level_code`.
- Keep top-up minutes shared.

### Phase 4 - Coach and Speech

- Make conversation feedback prompts language-aware.
- Add Arabic-specific deterministic fallback scoring.
- Add Arabic text normalization:
  - remove optional harakat for matching,
  - normalize hamzah/alif variants where appropriate,
  - normalize ta marbuta/ha only when pedagogically safe,
  - compare Arabic tokens without Latin regex assumptions.
- Pass Arabic language hints to STT/TTS where provider supports it.

### Phase 5 - Audio and Review

- Curate Arabic TTS voices separately from English voices.
- Add human QA checklist for Arabic audio.
- Add religious-content review for hadith/kajian lessons.

## First Concrete Build Task

Start with a narrow implementation PR:

1. Add Arabic Fusha product/curriculum plan.
2. Scaffold `content/curriculum/arabic/A1` with one 5-lesson unit.
3. Generalize course discovery enough that Arabic can appear in admin readiness
   and eventually in web course data.
4. Do not change paid access behavior yet; Arabic beta uses existing Pro until
   product-scoped entitlements are implemented.

