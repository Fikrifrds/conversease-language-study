# English lesson visual prompts

The repository contains one prompt pack for every English lesson under:

```text
content/visual-prompts/english/<LEVEL>/<UNIT>/<LESSON>/PROMPT.md
```

Example:

```text
content/visual-prompts/english/A1/
└── unit-01-greeting-introducing-yourself/
    └── lesson-01-saying-hello/
        └── PROMPT.md
```

Each pack is derived from the lesson's actual dialogue, audio voice mapping, situation, goal, and useful phrases. It contains four independent prompts:

- one 1672×941 hero prompt;
- three 1254×1254 dialogue-card prompts.

The prompts enforce the correct speaker count and genders, conversation-specific setting, character continuity, and the project's syariah rules. For same-gender dialogue, only the named speakers may appear anywhere in the image: no staff, visitors, silhouettes, reflections, or other background people. Mixed-gender dialogue requires a clearly public scene with two distant modestly dressed adult men so the speakers are not shown in seclusion.

Male characters wear loose modest trousers ending above the ankle bones, with socks and closed shoes. Female characters wear a long khimar covering the chest, loose opaque full-length clothing, socks, and closed shoes.

“Faceless” is defined literally: every visible face must be a completely blank, smooth shape without eyes, eyebrows, nose, mouth, facial hair, or feature-like marks. The generated prompts repeat this as a non-negotiable rule near the beginning so external image models are less likely to reinterpret faceless as merely simplified facial features.

Use [the generated index](../content/visual-prompts/english/INDEX.csv) to locate any lesson. Generate only the images that need replacement. Existing images, `visuals.yaml`, and web data remain untouched; asset replacement is intentionally manual.

To refresh the prompt files after curriculum or dialogue changes:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_english_visual_prompts.py
```

To verify that all prompt files are current:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_english_visual_prompts.py --check
```
