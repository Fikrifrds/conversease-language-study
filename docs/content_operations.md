# Content Operations

This document is the working guide for Conversease curriculum production.

## Release State

The app is technically ready for controlled beta, but the full English learning
path is not complete for a public release across all supported levels.

Current English A1-C1 status:

- Planned lessons: 200
- Implemented lessons: 5
- Text-ready lessons: 5
- Audio-ready lessons: 0
- Beta-ready lessons: 5
- Production-ready lessons: 0

Controlled beta can use Unit 1 with text-based listening scripts and
Conversation Coach. Full public release should complete all planned lessons for
the intended launch level set and generate listening/phrase audio.

## Admin Checks

Admin can check content in the web app:

```text
/admin/cms
```

Admin access uses the logged-in user role. Bootstrap the first admin by adding
their email to `ADMIN_EMAILS_RAW`, then have that user login again. The Admin CMS has:

- Readiness: level, unit, lesson, file, tracker, and audio checklist.
- Curriculum: edit lesson title, status, goal, and roleplay metadata.
- Email Templates: edit and validate email templates.
- Change Log: view and rollback CMS edits.
- Users: promote or demote other admin users without opening the database.

For CLI checks:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/content_readiness_report.py --format markdown
```

Use JSON output for automation:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/content_readiness_report.py --format json
```

## Level Checklist

Each supported level has a file-based roadmap:

```text
content/curriculum/english/A1/content_plan.yaml
content/curriculum/english/A2/content_plan.yaml
content/curriculum/english/B1/content_plan.yaml
content/curriculum/english/B2/content_plan.yaml
content/curriculum/english/C1/content_plan.yaml
```

Current level readiness:

| Level | Planned Lessons | Implemented | Text Ready | Audio Ready | Current Gap |
|---|---:|---:|---:|---:|---|
| A1 | 40 | 5 | 5 | 0 | Unit 1 text-ready, audio missing; Units 2-8 missing files |
| A2 | 40 | 0 | 0 | 0 | All lesson files missing |
| B1 | 40 | 0 | 0 | 0 | All lesson files missing |
| B2 | 40 | 0 | 0 | 0 | All lesson files missing |
| C1 | 40 | 0 | 0 | 0 | All lesson files missing |

A1 planned units:

| Unit | Status | Lessons | Current Gap |
|---|---:|---:|---|
| Unit 1: Greeting & Introducing Yourself | beta-ready | 5 | Audio not generated |
| Unit 2: Spelling, Numbers & Contact Details | planned | 5 | All lesson files missing |
| Unit 3: Daily Routine & Time | planned | 5 | All lesson files missing |
| Unit 4: Work, Study & Preferences | planned | 5 | All lesson files missing |
| Unit 5: Places & Directions | planned | 5 | All lesson files missing |
| Unit 6: Food, Shopping & Prices | planned | 5 | All lesson files missing |
| Unit 7: Help, Problems & Requests | planned | 5 | All lesson files missing |
| Unit 8: A1 Review & Final Conversation | planned | 5 | All lesson files missing |

## Required Files Per Lesson

Every lesson must have these files:

| File | Purpose |
|---|---|
| `lesson.yaml` | lesson metadata, required sections, completion rules |
| `lesson.md` | main lesson explanation and learner flow |
| `conversation_goal.md` | concise outcome and success behavior |
| `listening_script.md` | dialogue text and audio direction |
| `transcript_translation.md` | Indonesian support translation |
| `useful_phrases.yaml` | phrases, Indonesian meaning, usage note, common mistake |
| `grammar_for_conversation.md` | practical grammar for speaking |
| `pronunciation_drill.md` | pronunciation targets and repeat drills |
| `response_prompts.yaml` | guided learner response prompts |
| `conversation_coach_roleplay.yaml` | scenario, opening line, goal, rubric |
| `quiz.yaml` | comprehension and usage quiz |
| `reading_support.md` | short reading reinforcement |
| `writing_support.md` | short writing reinforcement |
| `audio_manifest.yaml` | generated audio asset metadata |

The production tracker must also be updated:

```text
content/production_tracker.csv
```

Text columns should be `done` when reviewed. Set `audio_generated=done` only
after audio URLs and duration are filled in `audio_manifest.yaml`.

## Lesson Generation Prompt

Use this prompt to generate one complete lesson package.

```text
You are creating Conversease English {level_code} curriculum for Indonesian learners.

Generate production-ready content for:
- Level: {level_code}
- Unit: {unit_key} - {unit_title}
- Lesson: {lesson_key} - {lesson_title}
- Conversation outcome: {conversation_outcome}
- Learner source language: Indonesian
- Target language: English

Constraints:
- Conversation-first, not grammar-first.
- Match the CEFR level exactly:
  - A1: very short, concrete, beginner-safe phrases.
  - A2: everyday routines, simple past/future, short reasons.
  - B1: connected speech, experiences, opinions, workplace basics.
  - B2: professional discussions, arguments, tradeoffs, presentations.
  - C1: nuanced, precise, strategic communication.
- Explain support notes in Indonesian.
- No slang unless explicitly useful.
- Avoid cultural assumptions.
- Keep examples practical for Indonesian adult learners.
- Do not include images of living beings. If visual ideas are needed, use objects, documents, signs, UI, maps, or faceless/isometric non-detailed figures.

Return these files with exact filenames:
1. lesson.yaml
2. lesson.md
3. conversation_goal.md
4. listening_script.md
5. transcript_translation.md
6. useful_phrases.yaml
7. grammar_for_conversation.md
8. pronunciation_drill.md
9. response_prompts.yaml
10. conversation_coach_roleplay.yaml
11. quiz.yaml
12. reading_support.md
13. writing_support.md
14. audio_manifest.yaml with status: not_generated

Quality rules:
- listening_script.md must have a short two-speaker dialogue, 5-8 lines.
- useful_phrases.yaml must have 5-8 phrases with meaning_id, usage_note, and common_mistake.
- quiz.yaml must have at least 3 questions.
- conversation_coach_roleplay.yaml must include scenario_key, mode, level_code, opening_line, learner_goal, max_turns, target_phrases, and rubric.
- Every filename must be valid YAML or Markdown.
```

## Listening Script Prompt

Use this when only the listening section is missing or weak.

```text
Create an English {level_code} listening dialogue for Indonesian learners.

Lesson:
- Unit: {unit_title}
- Lesson: {lesson_title}
- Conversation goal: {conversation_goal}

Requirements:
- 2 speakers.
- 5-8 short turns.
- Slow, clear, natural English.
- Include 3-5 target phrases from the lesson.
- Avoid idioms and advanced grammar.
- Add Indonesian transcript translation below the English dialogue.
- Add Audio Direction with speed, tone, pause style, and voice notes.

Output:
1. listening_script.md
2. transcript_translation.md
```

## Quiz Prompt

```text
Create {level_code} quiz.yaml for this Conversease lesson:
- Level: {level_code}
- Lesson title: {lesson_title}
- Conversation goal: {conversation_goal}
- Target phrases: {target_phrases}
- Listening script: {listening_script}

Requirements:
- 3-5 questions.
- Use multiple_choice or short_answer.
- Test listening comprehension, phrase meaning, and correct response.
- Questions must be simple and unambiguous.
- correct_answer must exactly match one option for multiple_choice.

Return valid YAML only.
```

## Roleplay Prompt

```text
Create conversation_coach_roleplay.yaml for English {level_code}.

Lesson:
- lesson_key: {lesson_key}
- title: {lesson_title}
- conversation_goal: {conversation_goal}

Requirements:
- scenario_key must be lowercase snake_case.
- mode: lesson_practice_coach
- level_code: {level_code}
- opening_line: one simple English sentence from the coach.
- learner_goal: one clear sentence explaining what learner must do.
- max_turns: 6-8.
- target_phrases: 4-6 useful phrases.
- rubric minimum scores for speaking, relevance, grammar.

Return valid YAML only.
```

## MiniMax Audio Prompt

Use this prompt in MiniMax TTS or the selected TTS provider. If the provider does
not support multi-speaker generation in one pass, generate each speaker
separately and combine the files in audio editing software.

```text
Generate English {level_code} learning audio.

Style:
- clear classroom audio
- slow natural speed
- friendly but professional
- short pauses between turns
- no background music
- no sound effects

Dialogue:
{listening_script_dialogue}

Voice direction:
- Speaker A: clear adult voice, warm, medium pitch
- Speaker B: clear adult voice, calm, medium-low pitch
- Pronunciation: standard, easy to understand for beginners
- Export: mp3, 44.1 kHz or provider default high quality
```

After generation:

1. Open Admin CMS, choose the MiniMax model and voice in the Audio Generator panel.
2. Click `Generate Audio` on a text-ready lesson.
3. The API calls MiniMax T2A, uploads the mp3 to S3, updates `audio_manifest.yaml`, and sets `audio_generated=done` in `content/production_tracker.csv`.
4. Run readiness and curriculum validation before release.

Generate voice preview cache once per model/speed so the voice dropdown can play stored samples:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.generate_voice_previews --model speech-2.8-hd --speed 1
```

The CMS generator currently fills the listening dialogue asset (`dialogue_main`) from `listening_script.md`. Phrase pronunciation assets can be generated as a separate follow-up asset when needed.

Required API env for CMS generation:

```bash
MINIMAX_API_KEY=
MINIMAX_API_BASE_URL=https://api.minimax.io
MINIMAX_TTS_MODEL=speech-2.8-hd
MINIMAX_TTS_VOICE_ID=English_expressive_narrator
MINIMAX_TTS_LANGUAGE_BOOST=English
S3_BUCKET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=ap-southeast-1
S3_PUBLIC_BASE_URL=
```

Example `audio_manifest.yaml` after audio is ready:

```yaml
lesson_key: lesson-01-saying-hello
status: done
provider: minimax
assets:
  - key: dialogue_main
    type: dialogue
    script_file: listening_script.md
    audio_url: https://cdn.example.com/audio/english/A1/unit-01/lesson-01/dialogue_main.mp3
    duration_seconds: 24
  - key: phrases
    type: phrase_pronunciation
    source_file: useful_phrases.yaml
    audio_url: https://cdn.example.com/audio/english/A1/unit-01/lesson-01/phrases.mp3
    duration_seconds: 18
```

## Review Workflow

For each lesson:

1. Generate the lesson package.
2. Place files under:

```text
content/curriculum/english/A1/units/{unit_key}/{lesson_key}/
```

Replace `A1` with the target level code for A2, B1, B2, or C1.

3. Add the lesson key to the unit's `unit.yaml` when the level has an active
   course loader. Planned future levels can be tracked from `content_plan.yaml`
   before their runtime course loader is enabled.
4. Update `content/production_tracker.csv`.
5. Run:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/content_readiness_report.py --format markdown
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/validate_curriculum.py
```

6. Open `/admin/cms`, load Admin CMS, and check the Readiness tab.
7. Mark lesson `published` only after all text fields pass review.
8. Mark audio ready only after TTS output is reviewed by a human.

## Release Rule

- Controlled beta: minimum A1 Unit 1 text-ready, app smoke test passes, payments/admin email tested.
- Full A1 public release: all 40 A1 lessons text-ready, all listening/phrase audio generated, final evaluation reviewed, and release preflight passes.
- Full multi-level public release: every launched level in A1-C1 is text-ready, audio-ready, reviewed, and visible in Admin CMS Readiness.
