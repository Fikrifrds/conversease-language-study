# Review for TRAE — A2 Unit 01 (Social Small Talk)

Reviewer: Claude. Scope reviewed: `content/curriculum/english/A2/units/unit-01-social-small-talk/`
(5 lessons) + `A2/LEVEL_SPEC.md`, `A2/final_evaluation.yaml`, `A2/content_plan.yaml`,
and `scripts/generate_a2_unit_01_social_small_talk.py`.

**Before doing anything, read [docs/content_authoring_guide.md](content_authoring_guide.md)** —
it is the single entry point and links to the detailed rules.

---

## ✅ What you did well (keep doing this)

- All 5 lessons have the full 14-file set, matching A1.
- Every `lesson.yaml` includes the required **`grammar_summary`** field. 👍
- **Dialogue and transcript_translation line counts match** in every lesson
  (8/8, 8/8, 8/8, 8/8, 12/12) — this is the most important rule.
- No back-to-back same-speaker turns. Transcript uses the arrow format consistently.
- Dialogue quality is good: coherent, natural, and correctly **A2-level** (longer
  turns, follow-up questions, empathetic reactions, connected speech — a real step
  up from A1).
- Audio `status: not_generated` is correct (audio not generated yet).

## 🔴 Must fix (the content is good but NOT wired up, and a test is red)

### 1. A2 is not connected to the app — it won't render, and `data.ts` was not regenerated
The web lesson page renders from the **generated** `apps/web/lib/data.ts`. That
file (and the loader that feeds it) is currently **A1-only**, so your A2 lessons
will not appear anywhere. Make the pipeline multi-level, then regenerate:

- `apps/api/app/data/curriculum.py`: it is hardcoded to A1
  (`LEVEL_CODE = "A1"` at line 13; `a1_root()` line 105; `load_a1_course()`
  line 110, used at 245/286/414/418/420). Generalize loading to a given level
  (e.g. `load_course(level_code)`), keeping A1 behavior intact.
- `scripts/generate_web_lesson_data.py`: it calls `load_a1_course()` (line 159)
  and its header says "A1 is the single source of truth". Make it emit lessons
  for all implemented levels (A1 + A2), preserving curriculum order.
- Then regenerate (do NOT hand-edit `data.ts`):
  ```bash
  PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_web_lesson_data.py
  ```
- The sync test `apps/api/tests/test_web_lesson_data_in_sync.py` must pass after
  regeneration.

### 2. A test is failing because the lesson count changed
`apps/api/tests/test_admin_cms.py:30` still asserts
`implemented_lesson_count == 40`, but it is now 45 (40 A1 + 5 A2). Update it to
the new number (and double-check any other count assertions). You already updated
`tests/test_content_readiness.py` — apply the same to `test_admin_cms.py`.
Run the whole suite and make it green (except `test_learning_progress.py`, which
was already failing before your work and is unrelated):
```bash
cd apps/api && .venv/bin/python -m pytest tests -q
```

### 3. `production_tracker.csv` has no A2 rows
You set `status: implemented` in `A2/content_plan.yaml`, but
`content/production_tracker.csv` has **0 A2 rows**. Add a row per A2 lesson
(same columns as A1) with `audio_generated = not_generated`, so readiness/tracker
validation stays consistent. Confirm with:
```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/audio_readiness_report.py --level A2
```

## 🟡 Cleanup / nice to have

- **Remove the throwaway scaffolding script**
  `scripts/generate_a2_unit_01_social_small_talk.py`. It was only used once to
  write the files; it is not referenced anywhere and is now clutter. The lesson
  files are the source of truth, not that script.
- Re-read `A2/LEVEL_SPEC.md` and `A2/final_evaluation.yaml` once more for
  consistency with the 5 lessons (skills covered, thresholds).

## How to verify your fix end-to-end
1. `scripts/generate_web_lesson_data.py` runs clean and `git diff apps/web/lib/data.ts`
   shows the 5 A2 lessons added (dialogue with no audio tags, translations aligned).
2. `npx tsc --noEmit` and `npx next build` in `apps/web` pass; the A2 lesson pages
   appear in the build output.
3. `cd apps/api && .venv/bin/python -m pytest tests -q` is green except the
   pre-existing `test_learning_progress` failure.

## For future content (so it's right the first time)
- Always start from [docs/content_authoring_guide.md](content_authoring_guide.md)
  and copy from the templates in `content/curriculum/templates/`
  (now includes `lesson.template.yaml`, `listening_script.template.md`,
  `transcript_translation.template.md`).
- Edit content in the **curriculum files only** — `data.ts` is generated; never
  hand-edit it. Run the generator and make the sync test pass.
- After authoring, update **all** the bookkeeping in one go: `content_plan.yaml`,
  `unit.yaml`, **`production_tracker.csv`**, and any **count-based tests** you
  change the totals for.
- Keep `listening_script.md` and `transcript_translation.md` the same length and
  order; keep audio `not_generated` until generated.
- Don't leave one-off generator scripts behind; the files are the deliverable.
