# Arabic Content Standard

Arabic A1 is the baseline quality standard for all future Arabic levels.
Use this document before creating Arabic A2, B1, B2, or C1 content, whether the
content is written in this repo or generated elsewhere with another model.

## Source Of Truth

- Arabic content lives in `content/curriculum/arabic/<LEVEL>`.
- Arabic A1 is the reference implementation:
  `content/curriculum/arabic/A1`.
- Use `content/curriculum/arabic/A1/LEVEL_SPEC.md` for tone and learner support.
- Use `scripts/generate_arabic_a1_curriculum.py` as the generator pattern.
- Audio readiness is decided by `audio_manifest.yaml`, not by S3 alone.

## Non-Negotiable Quality Rules

1. Keep Arabic Fusha / Modern Standard Arabic. Do not mix dialect unless a
   future level explicitly teaches dialect awareness.
2. Arabic lines must be vocalized with harakat where they are used for learning
   or TTS.
3. Indonesian support must be clear, concise, and natural.
4. Every lesson teaches one conversation outcome. Grammar supports the outcome;
   grammar is not the center.
5. Dialogue, useful phrases, response prompts, quiz, roleplay, reading, and
   writing must reuse the same phrase family.
6. Speaker logic must be realistic. If the learner moves from asking directions
   to buying something, introduce a new speaker such as `Cafe Staff` and add a
   pause tag like `<#0.9#>`.
7. Speaker gender must match the persona name and voice registry.
8. Do not use religious source text, hadith, dhikr, or devotional phrases with
   generated TTS until a separate religious review and approved audio process
   exists.
9. Do not use human or living-being images. Arabic visuals should use objects,
   documents, maps, signs, UI, or faceless isometric assets only.

## Arabic A1 Baseline

A1 proves the format that later levels must preserve:

- 8 units, 40 lessons.
- Each unit has 4 skill-building lessons and 1 mission lesson.
- Unit 8 is review and final conversation.
- Each lesson has:
  - `lesson.yaml`
  - `lesson.md`
  - `conversation_goal.md`
  - `listening_script.md`
  - `transcript_translation.md`
  - `useful_phrases.yaml`
  - `grammar_for_conversation.md`
  - `pronunciation_drill.md`
  - `response_prompts.yaml`
  - `conversation_coach_roleplay.yaml`
  - `quiz.yaml`
  - `reading_support.md`
  - `writing_support.md`
  - `audio_manifest.yaml`

## Level Progression

### A1

- Very short formal phrases.
- 5-8 dialogue turns.
- One idea per turn.
- Heavy Indonesian support.
- Focus: greetings, identity, classroom, time, family, places, shopping, help.

### A2

- Short everyday conversations with simple reasons and follow-up questions.
- 6-10 dialogue turns.
- One short scene or two connected scenes with an explicit transition.
- Introduce simple past, near future, preferences, availability, arrangements,
  health, service, and short personal experience.
- Keep Indonesian support, but allow slightly longer Arabic sentences.

### B1

- Connected conversation with simple narration, opinions, and plans.
- 8-12 dialogue turns.
- Learner can explain a problem, compare options, and respond to follow-up.

### B2

- Professional and structured conversation.
- Learner can negotiate, clarify tradeoffs, summarize, and handle meetings.

### C1

- Nuanced formal communication.
- Learner can explain subtle meaning, adapt register, present arguments, and
  manage strategic conversation.

## Dialogue Rules

- Use speaker labels only as metadata: `**Khalid:** ...`.
- Speaker names must not be spoken by TTS.
- Do not put two turns in one speaker line.
- Do not let the same non-learner speaker change roles in a new location.
- For scene transitions:
  - add a transition line, and
  - add `<#0.8#>` to `<#1.2#>` after the transition line.
- Avoid colon-sensitive mistakes in Arabic TTS:
  - It is valid to use Arabic text such as
    `بَرِيدِي الْإِلِكْتُرُونِيُّ: أَحْمَدُ نُقْطَةٌ وَاحِدٌ.`
  - After changing such lines, regenerate audio and listen for the full phrase.

## Speaker And Voice Rules

- Reuse known personas when possible:
  - Male: Ahmad, Khalid, Zayd, Omar, Raka, Adi.
  - Female: Maryam, Layla, Noura, Fatimah, Lina, Sara.
- If a new named character is introduced, add it intentionally and check gender.
- Generic roles should be explicit:
  - `Muallim`, `Muallimah`, `Officer`, `Cafe Staff`, `Shopkeeper`, `Doctor`,
    `Receptionist`, `Driver`.
- Arabic voice selection must use the curated Arabic voice pool in
  `apps/api/app/services/audio_generation.py`.
- If `listening_script.md` changes, set `audio_manifest.yaml` to
  `needs_regeneration` and regenerate audio.

## External Generation Prompt

Use this prompt when creating Arabic content with another model:

```text
You are writing Conversease Arabic Fusha curriculum for Indonesian adult
learners. Use Arabic A1 in this repo as the quality baseline.

Requirements:
- Formal Arabic / MSA only.
- Arabic lines must be vocalized with harakat.
- Indonesian explanations must be natural and concise.
- One conversation outcome per lesson.
- Keep dialogue coherent and realistic.
- Do not jump scenes without a transition line and pause tag.
- If a new location or service role appears, add a new speaker.
- Match speaker gender to persona name.
- Keep listening_script.md and transcript_translation.md aligned line by line.
- Reuse the lesson phrase family across useful phrases, response prompts, quiz,
  roleplay, reading, and writing.
- Do not include religious source text or devotional phrases.
- Do not include images of people or living beings.

Before returning the lesson, self-check:
1. Are all dialogue turns coherent?
2. Does every Arabic learner-facing line have harakat?
3. Do speaker genders and roles make sense?
4. Do transcript lines exactly match listening_script order?
5. Would this fit the target CEFR level?
```

## Review Checklist

Before committing Arabic content:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_web_lesson_data.py
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/check_arabic_listening_vocalization.py
PYTHONPATH=apps/api apps/api/.venv/bin/python -m unittest \
  apps/api/tests/test_transcript_alignment.py \
  apps/api/tests/test_web_lesson_data_in_sync.py \
  apps/api/tests/test_audio_generation.py \
  apps/api/tests/test_content_readiness.py
git diff --check
```

