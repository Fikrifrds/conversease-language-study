# Content Authoring Guide — START HERE

**This is the single entry point for creating or regenerating any learning
content (dialogues, lessons, audio) in this repo.** Read this first, every time,
regardless of which model or tool does the generation. It keeps quality
consistent across people, sessions, and LLMs. It is short on purpose and links
to the authoritative detail elsewhere — follow the links rather than guessing.

If you only remember one thing: **content must be conversation-first, coherent,
and consistent with the existing files for that lesson.**

---

## 1. The non-negotiable rules

1. **Conversation-first.** Every lesson teaches the learner to handle one real
   conversation. Grammar is a tool, never the center.
2. **One outcome per lesson.** Dialogue, useful phrases, response prompts, quiz,
   and roleplay must reuse the *same* phrase family.
3. **Match the CEFR level.** A1 = very short, concrete sentences, 1 idea per
   turn. Complexity rises with level. See "Quality Standard" in
   [content_operations.md](content_operations.md).
4. **Dialogues must be coherent.** No abrupt topic jumps, no same speaker twice
   in a row, no character switching roles illogically (e.g. a passer-by giving
   directions must NOT become the cafe cashier — introduce a separate speaker).
   For multi-skill "mission"/"review" lessons, connect the scenes with a natural
   transition line and/or a pause.
5. **Indonesian support is clear and concise**, never stiff.
6. **No human/living-being images.** Visuals = objects, UI, signs, maps,
   faceless isometric only.
7. **Never publish** a lesson whose roleplay slug the backend/frontend can't run.

## 2. Files a lesson needs

Each lesson is a folder of markdown/yaml files (listening_script, useful_phrases,
quiz, roleplay, etc.). The required set and per-file purpose is listed under
"Required Files Per Lesson" in [content_operations.md](content_operations.md).
Level scope/targets: `content/curriculum/english/<LEVEL>/LEVEL_SPEC.md`.

Copy from the templates in
[`content/curriculum/templates/`](../content/curriculum/templates/) — they encode
the exact format the loader/generator expect:
`lesson.template.yaml` (note the **required `grammar_summary`** field),
`lesson.template.md`, `listening_script.template.md`,
`transcript_translation.template.md`, `useful_phrases.template.yaml`,
`quiz.template.yaml`, `conversation_coach_roleplay.template.yaml`,
`final_evaluation.template.yaml`.

**Creating or editing a lesson — do these in order:**
1. Edit/author the curriculum files (use the templates).
2. Keep `listening_script.md` and `transcript_translation.md` the same number of
   lines, in the same order.
3. Regenerate the web data (see §5) — the page renders from generated `data.ts`.
4. If `listening_script.md` changed, mark audio stale (§5) and regenerate audio.
5. Run the checks in §6.

## 3. Writing `listening_script.md` (the dialogue + audio source)

Audio is generated from `listening_script.md` via MiniMax T2A v2
(model `speech-2.8-hd`). Beyond plain text you may use two expressive markers —
**sparingly (1-2 per dialogue), keeping it A1-clear**:

- **Interjection tags** (2.8 models only): `(laughs)`, `(chuckle)`, `(breath)`,
  `(sighs)`, etc. — e.g. a relieved `(laughs) It works!`
- **Pause control** `<#x#>` (seconds) — e.g. a scene change:
  `Have a nice day. <#0.9#>`

Full tag list, rules, and the "MiniMax has no ambient/background sound"
caveat are in the "Format `listening_script.md`" section of
[content_operations.md](content_operations.md). Keep the first lesson of a level
(absolute beginners) clean — no interjections.

> **⚠️ The lesson page renders from generated code — never hand-edit it.**
> The curriculum files are the single source of truth. `apps/web/lib/data.ts`
> (the lessons array between the `// <generated:lessons>` markers) is GENERATED
> from them. After editing any lesson content, regenerate:
> ```bash
> PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_web_lesson_data.py
> ```
> What feeds the generator:
> - `dialogue` ← `listening_script.md` (audio tags `(chuckle)`/`<#..#>` are
>   stripped automatically for display).
> - `translation` ← `transcript_translation.md` (must be the same number of lines
>   as the dialogue, in the same order — the generator fails loudly otherwise).
> - `phrases`/`prompts`/`quiz` ← `useful_phrases.yaml` / `response_prompts.yaml` /
>   `quiz.yaml`; `grammar` ← `grammar_summary` in `lesson.yaml`;
>   `setup` ← the "Situation"/"Situation Setup" section of `lesson.md`.
>
> A CI test (`apps/api/tests/test_web_lesson_data_in_sync.py`) fails if `data.ts`
> is out of sync, so you cannot forget to regenerate.

## 4. Voices / personas (so audio sounds consistent)

The voice registry is **code, and code is the source of truth**:
[`apps/api/app/services/audio_generation.py`](../apps/api/app/services/audio_generation.py)
— see `CURATED_MINIMAX_VOICE_IDS` (the only allowed voices) and
`DIALOGUE_PERSONA_VOICES` (speaker name → voice).

Rules:
- Reuse an existing character name to keep its voice consistent.
- A speaker's name must imply its intended gender; do not let an important
  speaker fall back to the automatic hash voice.
- Recurring generic roles (`Officer`, `Staff`, `Teacher`, `Cashier`) must be
  added to `DIALOGUE_PERSONA_VOICES` with an explicit voice.
- `Audio Direction` in the script must match the personas, e.g.
  `Voices: female staff, male learner`.

## 5. When you change a script, the audio is now stale

Editing `listening_script.md` invalidates the existing audio. You MUST:
1. Set the lesson's `audio_manifest.yaml` → `status: not_generated`.
2. Set the `audio_generated` column for that lesson in
   [`content/production_tracker.csv`](../content/production_tracker.csv) →
   `not_generated`. (Allowed values: `done`, `no`, `not_generated`.)
3. Regenerate audio (see "Workflow Generate Audio" /
   "Admin CMS Batch Audio" in [content_operations.md](content_operations.md)).

Readiness is computed from these files — keep them honest. Verify with:
```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/audio_readiness_report.py --level A1
```

## 6. Before you finish — verify

- Re-read the dialogue end-to-end for coherence (rule #4).
- Run the content checks:
  ```bash
  apps/api/.venv/bin/python -m pytest apps/api/tests/test_content_readiness.py apps/api/tests/test_curriculum_content.py -q
  ```
- Use the "Review Checklist" in [content_operations.md](content_operations.md).

---

## Where the detail lives (authoritative sources)

| Topic | Source |
| --- | --- |
| Full operations: audio workflow, quality standard, persona rules, external-generation prompt, review checklist | [docs/content_operations.md](content_operations.md) |
| Production plan, per-lesson checklist, release rule | [docs/content_production_plan.md](content_production_plan.md) |
| Voice registry & allowed voices (source of truth) | [apps/api/app/services/audio_generation.py](../apps/api/app/services/audio_generation.py) |
| Lesson/file templates | [content/curriculum/templates/](../content/curriculum/templates/) |
| Level scope & targets | `content/curriculum/english/<LEVEL>/LEVEL_SPEC.md` |
| Behavioral coding guidelines | [CLAUDE.md](../CLAUDE.md) |
