# Content Operations Guide

> **Start at [content_authoring_guide.md](content_authoring_guide.md).** That is
> the single entry point for content work; this file is the detailed reference it
> links to.

Panduan ini adalah source of truth untuk produksi kurikulum Conversease, baik
content dibuat langsung di repo, di remote server, atau di tempat lain dengan
model seperti Claude Opus 4.8.

## Source Of Truth

Conversease memakai content file-backed:

- Lesson text tersimpan di repo: `content/curriculum/...`
- Audio file tersimpan di S3.
- Metadata audio wajib tersimpan di repo lewat `audio_manifest.yaml`.
- Checklist release tersimpan di `content/production_tracker.csv`.

S3 object saja tidak cukup untuk menyatakan lesson sudah audio-ready. Audio baru
dianggap siap kalau metadata di repo juga siap dan ikut commit.

## Cara Mengetahui Audio Sudah Tergenerate

Untuk satu lesson, cek tiga lapis berikut.

1. `audio_manifest.yaml`

Lesson dianggap punya listening audio kalau file manifest berisi:

```yaml
lesson_key: lesson-01-spelling-your-name
status: generated
provider: minimax
assets:
  - key: dialogue_main
    type: dialogue
    script_file: listening_script.md
    audio_url: https://...
    duration_seconds: 17
    provider: minimax
    model: speech-2.8-hd
    voice_id: multi_speaker
    speaker_voices:
      Officer: English_CalmWoman
      Dimas: English_Diligent_Man
    storage_key: conversease/audio/...
    generated_by: Fikri Firdaus
    generated_at: "2026-06-04T..."
```

Status valid: `generated`, `done`, atau `published`. Yang wajib untuk readiness
adalah asset `dialogue_main` punya `audio_url` dan `duration_seconds`. Asset
lain seperti `phrases` boleh belum ada.

2. `content/production_tracker.csv`

Kolom `audio_generated` harus menjadi `done` setelah audio direview manusia.
Tracker ini adalah checklist editorial, bukan pengganti manifest.

3. Admin CMS atau CLI

CMS:

```text
/admin/cms -> Readiness
```

Setiap lesson menampilkan pill `Audio`. Jika audio ada, detail lesson akan
menampilkan audio player, storage key, model, durasi, dan speaker voices.

CLI:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/audio_readiness_report.py --level A1
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/audio_readiness_report.py --level A1 --missing-only --text-ready-only
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/audio_readiness_report.py --lesson spelling-your-name --format json
```

Readiness umum:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/content_readiness_report.py --format markdown
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/validate_curriculum.py
```

Catatan S3: kalau bucket private, membuka `audio_url` langsung bisa menghasilkan
`AccessDenied`. Itu normal. Platform memakai `playback_url` presigned dari API
untuk memutar audio.

## Format `listening_script.md` (MiniMax T2A v2)

Audio dialog dibuat dari `listening_script.md` lewat MiniMax T2A v2
(`/v1/t2a_v2`, model `speech-2.8-hd`). Selain teks biasa, dua marker berikut
boleh dipakai untuk membuat dialog lebih hidup. Pakai secukupnya (1-2 per
dialog) agar tetap jelas untuk pembelajar A1.

Referensi: https://platform.minimax.io/docs/api-reference/speech-t2a-http

### Interjection tags

Hanya didukung model `speech-2.8-hd` / `speech-2.8-turbo` (kita pakai
`speech-2.8-hd`). Tulis tag di dalam teks ucapan, mis. `Hello! (laughs)`.

Tag yang tersedia: `(laughs)`, `(chuckle)`, `(coughs)`, `(clear-throat)`,
`(groans)`, `(breath)`, `(pant)`, `(inhale)`, `(exhale)`, `(gasps)`, `(sniffs)`,
`(sighs)`, `(snorts)`, `(burps)`, `(lip-smacking)`, `(humming)`, `(hissing)`,
`(emm)`, `(sneezes)`.

### Pause control

Jeda dalam ucapan ditulis `<#x#>` dengan `x` = durasi detik, rentang
`[0.01, 99.99]` (maks 2 desimal). Marker harus berada di antara segmen yang
bisa diucapkan dan tidak boleh berurutan (`<#1#><#1#>` tidak valid). Berguna
untuk jeda pendek saat ganti scene, mis. setelah Ben pamit dan sebelum staff
cafe menyapa: `... Have a nice day. <#0.8#>`.

Catatan: pergantian baris (newline) menandai jeda paragraf alami antar turn.
MiniMax T2A **tidak** punya parameter ambient/background sound (lalu lintas,
burung, dll) — transisi scene hanya bisa pakai pause.

### Saat script diubah

Setiap kali `listening_script.md` diubah, dua hal jadi usang:

1. **Audio** lama. Set `audio_manifest.yaml` -> `status: not_generated` dan kolom
   `audio_generated` di `content/production_tracker.csv` jadi `not_generated`,
   lalu generate ulang (lihat workflow di bawah).
2. **`apps/web/lib/data.ts`** (lesson page render dari sini). Ini di-generate dari
   kurikulum — **jangan edit tangan**. Regenerate:
   ```bash
   PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_web_lesson_data.py
   ```
   Kalau dialog diubah, pastikan `transcript_translation.md` jumlah barisnya sama
   dengan dialog (generator gagal kalau tidak). Test
   `apps/api/tests/test_web_lesson_data_in_sync.py` menjaga data.ts tetap sinkron.

## Workflow Generate Audio

1. Pastikan `.env.production` atau env API berisi:

```bash
MINIMAX_API_KEY=
MINIMAX_API_BASE_URL=https://api.minimax.io
MINIMAX_TTS_MODEL=speech-2.8-hd
MINIMAX_TTS_LANGUAGE_BOOST=English
S3_BUCKET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=ap-southeast-1
```

2. Generate preview voice cache agar picker di CMS bisa memutar contoh suara:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.generate_voice_previews --model speech-2.8-hd --speed 1
```

3. Buka Admin CMS:

```text
/admin/cms -> Readiness
```

4. Pilih model, speed, dan default voice di panel `Audio Generator`.

5. Gunakan panel `Batch audio queue`:

- `Generate All Missing Audio`: generate semua lesson text-ready yang belum
  punya `dialogue_main`.
- `Regenerate Text-Ready Audio`: regenerate semua lesson text-ready, termasuk
  yang sudah punya audio. Pakai ini kalau script berubah.

6. Review audio di CMS. Pastikan:

- Tidak ada nama speaker yang dibacakan.
- Pergantian suara antar speaker terdengar natural.
- Male/female sesuai persona.
- Pace cukup lambat untuk level.
- Audio sesuai persis dengan `listening_script.md`.

7. Commit perubahan file hasil generate:

```bash
git status --short
git add content/curriculum content/production_tracker.csv
git commit -m "Generate listening audio for <scope>"
```

Jika generate dilakukan di remote server, jangan lupa push commit manifest dan
tracker dari server, atau salin perubahan manifest/tracker kembali ke repo kerja.
Tanpa commit metadata, deploy berikutnya bisa menganggap audio belum ada.

## Required Files Per Lesson

Setiap lesson wajib punya file berikut:

| File | Purpose |
|---|---|
| `lesson.yaml` | metadata, slug, status, completion rules |
| `lesson.md` | lesson flow dan penjelasan utama |
| `conversation_goal.md` | outcome dan success behavior |
| `listening_script.md` | dialogue utama dan audio direction |
| `transcript_translation.md` | terjemahan Indonesia |
| `useful_phrases.yaml` | phrase, meaning, usage, common mistake |
| `grammar_for_conversation.md` | grammar praktis untuk bicara |
| `pronunciation_drill.md` | drill repeat dan focus sound |
| `response_prompts.yaml` | prompt jawaban learner |
| `conversation_coach_roleplay.yaml` | scenario coach dan rubric |
| `quiz.yaml` | comprehension dan phrase checks |
| `reading_support.md` | reinforcement pendek |
| `writing_support.md` | latihan tulis pendek |
| `audio_manifest.yaml` | metadata audio S3 |

Template tersedia di:

```text
content/curriculum/templates/
```

## Quality Standard

Semua content harus conversation-first.

Level rules:

- A1: kalimat sangat pendek, concrete, 1 tujuan per lesson, 5-8 dialogue turns.
- A2: everyday situations, short reasons, simple past/future, masih rendah beban kognitif.
- B1: connected speech, opinions, experiences, workplace basics.
- B2: professional conversation, tradeoffs, meetings, negotiation, presentation.
- C1: nuanced, precise, strategic communication, tetapi tetap bisa dilatih lewat roleplay.

Consistency rules:

- Satu lesson hanya punya satu primary conversation outcome.
- Dialogue, useful phrases, response prompts, quiz, dan roleplay harus memakai phrase family yang sama.
- Jangan membuat grammar sebagai pusat lesson. Grammar hanya alat untuk menyelesaikan conversation.
- Indonesian support harus jelas, ringkas, dan tidak kaku.
- Hindari slang kecuali sengaja diajarkan dan cocok level.
- Jangan pakai gambar manusia atau makhluk bernyawa. Jika perlu visual, gunakan object, UI, document, sign, map, atau faceless isometric yang tidak detail.
- Jangan publish lesson kalau text-ready tetapi roleplay backend/frontend belum bisa menjalankan slug-nya.

## Persona And Voice Rules

Audio generation memakai persona registry di:

```text
apps/api/app/services/audio_generation.py
```

Production voice list sengaja dibatasi ke curated set yang solid. Jangan expose semua
voice MiniMax ke CMS/audio batch karena beberapa voice terlalu pelan, terlalu slow,
atau gendernya mudah terasa salah.

Curated voice set:

```python
CURATED_MINIMAX_VOICE_IDS = (
    "English_expressive_narrator",
    "English_Gentle-voiced_man",
    "English_Trustworth_Man",
    "English_Diligent_Man",
    "English_radiant_girl",
    "English_CalmWoman",
    "English_Upbeat_Woman",
)
```

Registry utama adalah **`DIALOGUE_PERSONA_VOICES`** di
`apps/api/app/services/audio_generation.py`. **Kode adalah source of truth** —
jangan menyalin daftarnya ke sini (mudah usang). Buka file itu untuk daftar
nama → voice terkini (mis. `ben`, `mina`, `sara`, `officer`, `staff`, dst).

Rules:

- Jika karakter sudah ada, pakai nama/persona yang sama agar suaranya konsisten.
- Jika karakter baru muncul berulang, tambahkan ke registry.
- Nama harus mewakili gender yang diinginkan dan cocok dengan konteks.
- Male/female wajib sesuai nama. Jangan biarkan nama Indonesia jatuh ke hash otomatis.
- Untuk role umum seperti `Officer`, `Teacher`, `Cashier`, tentukan voice eksplisit kalau dipakai berulang.
- Jangan biarkan karakter penting jatuh ke fallback hash kalau gender/suara harus spesifik.
- Audio direction di `listening_script.md` harus cocok dengan persona, misalnya `Voices: one female officer, one male learner`.

Contoh baik:

```markdown
**Officer:** Hi. What is your name?
**Dimas:** My name is Dimas.
**Officer:** How do you spell it?
**Dimas:** It's spelled D-I-M-A-S.

## Audio Direction

- Level: A1
- Speed: slow and natural
- Tone: friendly, clear, supportive
- Voices: female officer, male learner
```

## Prompt For External Content Generation

Gunakan prompt ini saat membuat content di luar repo.

```text
You are producing Conversease curriculum content.

Product:
- Conversation-first language learning app for Indonesian adult learners.
- Learners practice listening, understanding, repeating, responding, roleplay, and feedback.
- Content must feel like one unified curriculum, not isolated worksheets.

Target lesson:
- Language: English
- Level: {level_code}
- Unit key: {unit_key}
- Unit title: {unit_title}
- Unit outcome: {unit_outcome}
- Lesson key: {lesson_key}
- Slug: {lesson_slug}
- Lesson title: {lesson_title}
- Primary conversation outcome: {conversation_goal}
- Previous lesson summary: {previous_lesson_summary}
- Next lesson summary: {next_lesson_summary}

Use these standards:
- Match CEFR {level_code} exactly.
- Conversation-first, not grammar-first.
- Keep phrase family consistent across all files.
- Indonesian explanations must be clear and short.
- Do not introduce advanced vocabulary unless needed for the conversation.
- Do not use images or references to living beings.
- Dialogue must be realistic and easy to record with TTS.
- Speaker names must map to persona rules. Reuse existing characters when possible.
- If adding a new character, state gender, role, and recommended MiniMax voice.

Return a complete file package with exact filenames:
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
14. audio_manifest.yaml

Hard requirements:
- YAML must be valid.
- Markdown must be plain and concise.
- listening_script.md must have 5-8 turns for A1/A2, 6-10 for B1/B2, 8-12 for C1.
- transcript_translation.md must match every dialogue line.
- useful_phrases.yaml must have meaning_id, usage_note, common_mistake.
- response_prompts.yaml must train the learner's side of the conversation.
- conversation_coach_roleplay.yaml target_phrases must be phrases the learner should produce, not only phrases the coach says.
- audio_manifest.yaml starts with status: not_generated.

Before final answer, self-review:
- Is this lesson aligned with the unit outcome?
- Is it different enough from previous lesson but still connected?
- Are the phrase family, dialogue, quiz, and roleplay consistent?
- Is the difficulty exactly right for {level_code}?
- Are speaker persona and voice direction clear?
```

## Review Checklist

Reviewer harus cek:

- `lesson.yaml` slug dan title cocok dengan `content_plan.yaml`.
- `lesson.md` outcome sama dengan `conversation_goal.md`.
- Dialogue natural, pendek, dan sesuai level.
- Tidak ada line yang membuat TTS membaca nama speaker sebagai bagian dialog.
- Translation lengkap dan barisnya sejajar.
- Useful phrases tidak terlalu banyak dan semuanya dipakai atau relevan.
- Roleplay target phrases adalah output learner.
- Quiz jawaban benar exact match untuk multiple choice.
- Audio direction jelas soal gender/persona.
- `audio_manifest.yaml` masih `not_generated` sebelum audio dibuat.
- Setelah generate, `dialogue_main` punya URL, duration, storage key, model, speaker voices.

## Strategy To Finish A1-C1 Quickly

Target scope:

- 5 levels: A1, A2, B1, B2, C1.
- 8 units per level.
- 5 lessons per unit.
- Total 200 lessons.

Recommended production pipeline:

1. Lock style guide and persona registry.

   Do this once before mass generation. Jangan mulai ratusan lesson sebelum
   prompt, persona, dan review checklist stabil.

2. Produce per unit, not per random lesson.

   Generate 5 lessons in one unit as one package so progression is coherent.
   Review unit arc first, then review individual files.

3. Use two-pass generation.

   Pass 1: generate all text packages with `audio_manifest.yaml status: not_generated`.
   Pass 2: human QA and polish.
   Pass 3: batch audio generation.

4. Parallelize by level with one owner per level.

   Each owner uses the same prompt and checklist. One lead editor checks
   cross-level consistency.

5. Use gates, not trust.

   Every batch must pass:

   ```bash
   PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/content_readiness_report.py --format markdown
   PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/audio_readiness_report.py --missing-only --text-ready-only
   PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/validate_curriculum.py
   npm run build
   ```

6. Release in waves.

   - Wave 1: complete A1 text and audio.
   - Wave 2: complete A2 text and audio.
   - Wave 3: complete B1.
   - Wave 4: complete B2.
   - Wave 5: complete C1.

   Do not wait for C1 to validate product learning flow. But do not mark full
   multi-level release until all launched levels pass production readiness.

7. Keep generated metadata in git.

   After audio generation, commit `audio_manifest.yaml` and
   `content/production_tracker.csv`. This is what lets the team know which audio
   exists even though the binary audio is in S3.

## Admin CMS Batch Audio

Batch audio is in:

```text
/admin/cms -> Readiness -> Batch audio queue
```

Buttons:

- `Generate All Missing Audio`: only missing text-ready lessons.
- `Regenerate Text-Ready Audio`: every text-ready lesson, including existing audio.

If buttons are disabled, check:

- Admin account role.
- `MINIMAX_API_KEY`.
- `S3_BUCKET`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`.
- Text readiness. Planned lessons without files cannot generate audio.
- Voice/model selected in Audio Generator panel.

After queue finishes, refresh CMS and run:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/audio_readiness_report.py --missing-only --text-ready-only
```

## Release Rule

- Beta lesson: text-ready and roleplay usable.
- Production lesson: text-ready, reviewed, published, listening audio generated,
  audio reviewed by human, manifest committed, tracker committed.
- Full A1 release: all 40 A1 lessons production-ready.
- Full A1-C1 release: all 200 planned lessons production-ready.
