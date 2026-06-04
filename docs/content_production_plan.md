# Content Production Plan

Rencana eksekusi untuk membuat lesson yang belum ada, mengikuti
`docs/content_operations.md` (source of truth) dan `content/production_tracker.csv`.

## Status Sekarang (fakta)

- Total direncanakan: **200 lesson** (5 level x 8 unit x 5 lesson).
- Total A1 direncanakan: **40 lesson** (8 unit x 5 lesson).
- Sudah `implemented` (text-ready): **35 lesson**
  - Unit 1: 5 lesson (semua).
  - Unit 2: 5 lesson (semua).
  - Unit 3: 5 lesson (semua).
  - Unit 4: 5 lesson (semua).
  - Unit 5: 5 lesson (semua).
  - Unit 6: 5 lesson (semua).
  - Unit 7: 5 lesson (semua).
- Audio-ready: **0 lesson** (semua `audio_manifest.yaml` masih `not_generated`).

Sisa A1 yang belum dibuat: **5 lesson** (Unit 8).

## Aturan Wajib Yang Memengaruhi Eksekusi

1. **Dua tempat per lesson.** Frontend lesson page (`/lessons/[slug]`) render dari
   `apps/web/lib/data.ts` (`lessonCatalog`), bukan dari API. Backend course/progress
   render dari `content/curriculum`. Jadi setiap lesson baru wajib ada di:
   - Backend: 14 file di `content/curriculum/.../<lesson>/` + baris di
     `content/production_tracker.csv` + status di `content_plan.yaml` + `unit.yaml`.
   - Frontend: entri `lessonCatalog` + roleplay di `conversation-coach-practice.tsx`
     (`turnsByLessonSlug`) + scenario di `conversation-coach-workspace.tsx` +
     mapping di `course.units` (`data.ts`).
   Ini menegakkan aturan doc: "Jangan publish lesson kalau roleplay slug belum jalan."

2. **Gate per batch** (dari doc, sebelum dianggap selesai):
   ```bash
   PYTHONPATH=apps/api python scripts/content_readiness_report.py --format markdown
   PYTHONPATH=apps/api python scripts/audio_readiness_report.py --missing-only --text-ready-only
   PYTHONPATH=apps/api python scripts/validate_curriculum.py
   npm run build && npm run lint && npm run typecheck && npm run test:api
   ```

3. **Tes berbasis hitungan harus diupdate** tiap menambah lesson
   (`test_content_readiness.py`, `test_curriculum_content.py`, `test_admin_cms.py`,
   `test_learning_progress.py`).

4. **Persona/voice** ikut registry `DIALOGUE_PERSONA_VOICES` di
   `apps/api/app/services/audio_generation.py`. Karakter baru yang berulang
   ditambahkan ke registry.

## Strategi: per unit, dua pass (sesuai doc)

Doc menyarankan "produce per unit, not per random lesson" dan "two-pass":
Pass 1 = tulis teks (manifest `not_generated`), Pass 2 = QA, Pass 3 = generate audio.

### Wave A1 (urutan eksekusi)

| Batch | Scope | Lesson | Output |
|---|---|---|---|
| A1-B1 | Selesaikan Unit 2 | 4 lesson (giving-phone-numbers, sharing-email-addresses, asking-for-repetition, contact-details-mission) | Done: Unit 2 fully text-ready |
| A1-B2 | Unit 3 Daily Routine & Time | 5 lesson | Done: Unit 3 text-ready |
| A1-B3 | Unit 4 Work, Study & Preferences | 5 lesson | Done: Unit 4 text-ready |
| A1-B4 | Unit 5 Places & Directions | 5 lesson | Done: Unit 5 text-ready |
| A1-B5 | Unit 6 Food, Shopping & Prices | 5 lesson | Done: Unit 6 text-ready |
| A1-B6 | Unit 7 Help, Problems & Requests | 5 lesson | Done: Unit 7 text-ready |
| A1-B7 | Unit 8 A1 Review & Final | 5 lesson | A1 text-complete (40/40) |
| A1-AUDIO | Generate audio semua A1 text-ready | 40 lesson | A1 production-ready |

Setelah A1 selesai dan tervalidasi, ulangi pola sama untuk A2 -> B1 -> B2 -> C1
(masing-masing 40 lesson; total sisa 160). Plan detail per level dibuat saat A1 tuntas.

## Per-Lesson Checklist (Pass 1 teks)

Untuk tiap lesson, buat 14 file (template `content/curriculum/templates/`):
`lesson.yaml`, `lesson.md`, `conversation_goal.md`, `listening_script.md`,
`transcript_translation.md`, `useful_phrases.yaml`, `grammar_for_conversation.md`,
`pronunciation_drill.md`, `response_prompts.yaml`, `conversation_coach_roleplay.yaml`,
`quiz.yaml`, `reading_support.md`, `writing_support.md`, `audio_manifest.yaml`
(`status: not_generated`).

Lalu update: `content_plan.yaml` status -> `implemented`, `unit.yaml` (status
`published` + daftar lesson), `production_tracker.csv` baris baru, dan frontend
(`data.ts` + coach turns + workspace + `course.units`).

Review checklist (doc): slug/title cocok plan, outcome konsisten lintas file,
dialogue natural & sesuai level (A1: 5-8 turn, kalimat pendek, 1 outcome),
phrase family konsisten di dialogue/phrases/prompts/quiz/roleplay, roleplay
`target_phrases` = output learner, quiz jawaban exact match, audio direction
jelas gender/persona, manifest masih `not_generated`.

## Pass 3: Audio (per batch atau setelah A1 text-complete)

Prasyarat env: `MINIMAX_API_KEY`, `MINIMAX_API_BASE_URL`, `MINIMAX_TTS_MODEL`,
`S3_BUCKET`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`.

Jalur:
1. Generate voice preview cache: `python -m app.db.generate_voice_previews`.
2. Admin CMS -> Readiness -> Batch audio queue -> `Generate All Missing Audio`.
3. Review audio (tidak ada nama speaker terbaca, pergantian suara natural, gender
   sesuai persona, pace lambat, audio == listening_script).
4. Commit `content/curriculum` (manifest terupdate) + `production_tracker.csv`.

## Release Rule (doc)

- Beta lesson: text-ready + roleplay usable.
- Production lesson: text-ready + reviewed + published + audio generated + audio
  reviewed + manifest committed + tracker committed.
- Full A1 release: 40/40 A1 production-ready.

## Estimasi & Cara Kerja

- Authoring teks ditulis manual (tidak ada generator otomatis di repo). Aman dari
  "mengarang massal" karena tiap lesson lewat review checklist + validator + build.
- Saran realistis: kerjakan **1 batch (1 unit = 5 lesson) per iterasi**, lalu
  jalankan semua gate, commit, baru lanjut unit berikutnya. Ini menjaga kualitas
  dan reviewability, sesuai "produce per unit" di doc.
- Audio (Pass 3) memerlukan kredensial MiniMax + S3 yang aktif; idealnya dijalankan
  lewat Admin CMS batch queue, bukan otomatis di sini.
