#!/usr/bin/env python3
"""Generate one copy-paste visual prompt pack for every English lesson."""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
ENGLISH_ROOT = REPO_ROOT / "content" / "curriculum" / "english"
OUTPUT_ROOT = (
    REPO_ROOT
    / "content"
    / "visual-prompts"
    / "english"
)
LEVEL_ORDER = {"A1": 0, "A2": 1, "B1": 2, "B2": 3, "C1": 4}
FEMALE_VOICE_MARKERS = ("woman", "girl", "lady", "female")

MALE_STYLES = (
    "an olive long-sleeved modest shirt, loose dark trousers ending above the ankle bones, visible socks, and closed shoes",
    "a navy long-sleeved modest shirt, loose beige trousers ending above the ankle bones, visible socks, and closed shoes",
    "a warm gray long-sleeved modest shirt, loose dark trousers ending above the ankle bones, visible socks, and closed shoes",
    "a muted brown long-sleeved modest shirt, loose charcoal trousers ending above the ankle bones, visible socks, and closed shoes",
)
FEMALE_STYLES = (
    "an olive full-length khimar covering the chest, a loose opaque abaya, socks, and closed shoes",
    "a navy full-length khimar covering the chest, a loose opaque abaya, socks, and closed shoes",
    "a warm taupe full-length khimar covering the chest, a loose opaque abaya, socks, and closed shoes",
    "a muted plum full-length khimar covering the chest, a loose opaque abaya, socks, and closed shoes",
)

SETTING_RULES = (
    (("clinic", "symptom", "appointment", "health"), "a bright public clinic reception or consultation area"),
    (("hotel", "check_in"), "a well-lit hotel reception lobby"),
    (("shop", "shopping", "store", "item", "size", "color", "price"), "a tidy public retail shop with relevant products visible"),
    (("cafe", "drink", "food", "small_talk", "invitation", "inviting", "friend"), "a bright public café or community lounge with other visitors visible"),
    (("train", "ticket", "station", "gate", "transport"), "a clear public train station concourse"),
    (("taxi", "driver"), "a taxi pickup area with the vehicle and public surroundings visible"),
    (("direction", "place", "neighborhood"), "an open public campus or neighborhood information area with clear landmarks"),
    (("presentation", "presenting"), "an open professional presentation room with an audience visible"),
    (("client", "customer", "negotiation", "objection", "middle_ground"), "an open professional client-service area with colleagues visible in the background"),
    (("article", "source", "media", "information"), "a public library media workspace with reference materials and colleagues visible"),
    (("community", "culture", "cross_cultural", "local_norm", "tactful", "professionalism"), "a public community or professional training center with other visitors visible"),
    (("leadership", "coaching", "learning_goal", "learning_progress", "learning_challenge", "goal", "progress", "next_step", "advanced_listening", "listening", "implied", "heard", "long_turn", "follow_up", "followup"), "an open learning and coaching studio with other learners visible in the background"),
    (("class", "study", "teacher", "name", "spelling", "contact", "routine", "schedule", "time", "greeting", "introducing"), "a bright open English classroom shortly before or after class"),
    (("review", "final_test", "final_conversation", "test_practice"), "an open language assessment room with another staff member or learner visible in the background"),
    (("help", "request", "apologizing", "understand"), "an open learning-center help desk with relevant task materials visible"),
    (("work", "meeting", "stakeholder", "manager", "argument", "debate", "discussion", "feedback", "proposal", "risk", "problem", "solution", "advice", "decision", "tradeoff", "viewpoint", "opinion", "certainty", "disagree", "pros_cons", "compare", "preference", "priorities"), "an open modern workplace collaboration area with relevant documents or objects visible"),
    (("travel", "weekend", "yesterday", "story", "experience", "event"), "a bright public travel lounge or café where a personal story is being shared"),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate external-image prompts and upload folders for English lessons."
    )
    parser.add_argument("--check", action="store_true", help="Check generated files without writing.")
    args = parser.parse_args(argv)

    generated: dict[Path, str] = {}
    index_rows: list[dict[str, str]] = []
    for lesson_dir in lesson_dirs():
        prompt_path = output_dir(lesson_dir) / "PROMPT.md"
        generated[prompt_path] = build_prompt(lesson_dir)
        index_rows.append(index_row(lesson_dir, prompt_path))

    generated[OUTPUT_ROOT / "README.md"] = build_readme()
    generated[OUTPUT_ROOT / "INDEX.csv"] = build_index(index_rows)

    changed = [path for path, content in generated.items() if read_text(path) != content]
    if args.check:
        if changed:
            print(f"{len(changed)} English visual prompt files need regeneration:")
            for path in changed[:40]:
                print(path.relative_to(REPO_ROOT))
            if len(changed) > 40:
                print(f"... and {len(changed) - 40} more")
            return 1
        print(f"All {len(index_rows)} English lesson prompt packs are current.")
        return 0

    for path in changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(generated[path], encoding="utf-8")

    print(
        f"Generated {len(index_rows)} English lesson prompt packs "
        f"({len(changed)} files changed)."
    )
    return 0


def lesson_dirs() -> list[Path]:
    dirs = [path.parent for path in ENGLISH_ROOT.glob("*/units/*/*/lesson.yaml")]
    return sorted(dirs, key=lesson_sort_key)


def lesson_sort_key(lesson_dir: Path) -> tuple[int, int, int]:
    _, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    return (
        LEVEL_ORDER.get(level, 99),
        numeric_prefix(unit_key),
        numeric_prefix(lesson_key),
    )


def lesson_identity(lesson_dir: Path) -> tuple[str, str, str, str]:
    parts = lesson_dir.relative_to(REPO_ROOT / "content" / "curriculum").parts
    return parts[0], parts[1], parts[3], parts[4]


def output_dir(lesson_dir: Path) -> Path:
    _, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    return OUTPUT_ROOT / level / unit_key / lesson_key


def build_prompt(lesson_dir: Path) -> str:
    _, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    lesson = read_yaml(lesson_dir / "lesson.yaml")
    unit = read_yaml(lesson_dir.parent / "unit.yaml")
    phrases = read_yaml(lesson_dir / "useful_phrases.yaml").get("phrases", [])
    dialogue = dialogue_turns(lesson_dir / "listening_script.md")
    voices = speaker_voices(lesson_dir / "audio_manifest.yaml")
    speakers = unique_speakers(dialogue)
    missing_voices = [speaker for speaker in speakers if speaker not in voices]
    if missing_voices:
        raise ValueError(
            f"Missing audio voice mapping for {', '.join(missing_voices)} in "
            f"{(lesson_dir / 'audio_manifest.yaml').relative_to(REPO_ROOT)}"
        )
    characters = character_profiles(speakers, voices)
    genders = [gender_for_voice(voices.get(speaker, "")) for speaker in speakers]
    situation = extract_section(lesson_dir / "lesson.md", "Situation")
    setting = setting_for(lesson, unit)
    mode = communication_mode(lesson)
    shared_rules = shared_visual_rules(speakers, genders, characters, mode)
    dialogue_excerpt = "\n".join(
        f"- {speaker}: {text}" for speaker, text in dialogue[: min(6, len(dialogue))]
    )
    unit_number = numeric_prefix(unit_key)
    lesson_number = numeric_prefix(lesson_key)
    target = output_dir(lesson_dir).relative_to(REPO_ROOT)

    hero_prompt = f"""Create a 16:9 hero illustration at 1672×941 pixels for an English lesson.

Lesson: {lesson.get('title', lesson_key)} ({level}, Unit {unit_number}, Lesson {lesson_number})
Conversation goal: {lesson.get('conversation_goal', '')}
Situation: {situation}
Scene: {setting} {mode}

Cast and continuity:
{characters_as_lines(characters)}

Show the key conversational moment naturally. The body language, props, and background must make the setting and relationship immediately understandable even without text. Use this dialogue only to understand the action; do not render the words in the image:
{dialogue_excerpt}

{shared_rules}

Composition: wide establishing shot, all foreground speakers clearly visible, useful negative space, no cropped hands or feet, and no extra foreground characters."""

    card_prompts: list[str] = []
    card_labels: list[str] = []
    for index in range(3):
        phrase = phrase_text(phrases, index, lesson.get("title", lesson_key))
        focus_speaker, focus_line = matching_turn(dialogue, phrase, index)
        card_labels.append(phrase)
        card_prompts.append(
            f"""Create a square companion illustration at 1254×1254 pixels for card {index + 1} of the same English lesson.

Use the completed hero image as the visual reference. Keep exactly the same characters, clothing colors, room or location, time of day, and illustration style.

Card focus: “{phrase}”
Conversation moment: {focus_speaker} says “{focus_line}”. Show this meaning through natural gesture, attention, and relevant props; do not render the quote or any other words in the image.
Scene: {setting} {mode}

Cast and continuity:
{characters_as_lines(characters)}

{shared_rules}

Composition: medium or close conversational shot, clear focus on {focus_speaker}, all needed conversation partners still contextually visible, and no cropped hands."""
        )

    prompt_sections = [
        "# Lesson Visual Prompt",
        "",
        f"- Level: **{level}**",
        f"- Unit {unit_number}: **{unit.get('title', unit_key)}**",
        f"- Lesson {lesson_number}: **{lesson.get('title', lesson_key)}**",
        f"- Lesson key: `{lesson_key}`",
        f"- Web slug: `{lesson.get('slug', '')}`",
        f"- Dialogue speakers: **{', '.join(speakers)}**",
        f"- Prompt folder: `{target}`",
        "",
        "## Suggested outputs",
        "",
        "| File | Size | Purpose |",
        "|---|---:|---|",
        "| `hero.png` | 1672×941 | Main lesson image |",
        f"| `card-1.png` | 1254×1254 | {card_labels[0]} |",
        f"| `card-2.png` | 1254×1254 | {card_labels[1]} |",
        f"| `card-3.png` | 1254×1254 | {card_labels[2]} |",
        "",
        "## Hero prompt",
        "",
        "```text",
        hero_prompt,
        "```",
    ]
    for index, card_prompt in enumerate(card_prompts, start=1):
        prompt_sections.extend(
            [
                "",
                f"## Card {index} prompt — {card_labels[index - 1]}",
                "",
                "```text",
                card_prompt,
                "```",
            ]
        )
    prompt_sections.extend(
        [
            "",
            "Use only the prompts you need. Image generation and asset replacement are intentionally manual.",
            "",
        ]
    )
    return "\n".join(prompt_sections)


def shared_visual_rules(
    speakers: list[str], genders: list[str], characters: list[str], mode: str
) -> str:
    male_count = genders.count("male")
    female_count = genders.count("female")
    if female_count == 0:
        cast_rule = f"Show exactly {male_count} adult {'man' if male_count == 1 else 'men'} in the foreground and no women in the foreground."
    elif male_count == 0:
        cast_rule = f"Show exactly {female_count} adult {'woman' if female_count == 1 else 'women'} in the foreground and no men in the foreground."
    else:
        cast_rule = (
            f"Show exactly {male_count} adult {'man' if male_count == 1 else 'men'} and "
            f"{female_count} adult {'woman' if female_count == 1 else 'women'} as the named foreground speakers. "
            "They must be in an open public or professional setting with other people visible at a respectful distance; never depict one man and one woman secluded together in an enclosed room."
        )

    return f"""Visual rules:
- {cast_rule}
- The foreground cast must match the named dialogue speakers: {', '.join(speakers)}. Do not change their genders, duplicate them, or replace them with generic people.
- Clean faceless editorial illustration with a hand-drawn feel, subtle paper grain, natural proportions, warm daylight, restrained cream/orange/olive/navy palette, and consistent character design.
- Women, when present, wear a long khimar fully covering the chest, loose opaque full-length clothing, socks, and closed shoes. No hair, neck, chest, ankles, or feet exposed.
- Men wear modest opaque clothing with loose trousers whose hems clearly end above the ankle bones, with socks and closed shoes. Everyone maintains respectful distance; no touching or handshakes.
- No private mixed-gender seclusion. {mode}
- No temple, shrine, church, statue, idol, religious building, or religious symbol.
- No readable text, speech bubbles, captions, logos, flags, watermarks, or branded products.
- Avoid glossy 3D rendering, plastic skin, dramatic AI haze, fantasy lighting, distorted anatomy, extra fingers, duplicated limbs, or overly staged poses."""


def character_profiles(speakers: list[str], voices: dict[str, str]) -> list[str]:
    profiles: list[str] = []
    male_index = 0
    female_index = 0
    for speaker in speakers:
        gender = gender_for_voice(voices.get(speaker, ""))
        if gender == "female":
            clothing = FEMALE_STYLES[female_index % len(FEMALE_STYLES)]
            female_index += 1
            profiles.append(f"{speaker}: adult woman wearing {clothing}")
        else:
            clothing = MALE_STYLES[male_index % len(MALE_STYLES)]
            male_index += 1
            profiles.append(f"{speaker}: adult man wearing {clothing}")
    return profiles


def setting_for(lesson: dict[str, Any], unit: dict[str, Any]) -> str:
    lesson_text = " ".join(
        [
            str(lesson.get("conversation_situation") or ""),
            str(lesson.get("title") or ""),
        ]
    ).lower()
    setting = match_setting(lesson_text)
    if setting:
        return setting + "."

    unit_text = " ".join(
        [
            lesson_text,
            str(unit.get("unit_key") or ""),
            str(unit.get("title") or ""),
        ]
    ).lower()
    setting = match_setting(unit_text)
    if setting:
        return setting + "."
    return "an open, well-lit public learning space whose props clearly match the conversation topic."


def match_setting(text: str) -> str:
    for keywords, setting in SETTING_RULES:
        if any(keyword in text for keyword in keywords):
            return setting
    return ""


def communication_mode(lesson: dict[str, Any]) -> str:
    situation = str(lesson.get("conversation_situation") or "").lower()
    if "by_phone" in situation or "client_call" in situation:
        return (
            "Use a clear split-scene composition: the speakers are in separate appropriate locations connected by phone, not physically together."
        )
    return "The speakers are physically present in the same appropriate scene."


def dialogue_turns(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8").split("## Audio Direction", 1)[0]
    turns: list[tuple[str, str]] = []
    for line in text.splitlines():
        match = re.match(r"^\s*\*\*([^:*#][^:*]{0,40}):\*\*\s*(.+?)\s*$", line)
        if match:
            turns.append((match.group(1).strip(), match.group(2).strip()))
    if not turns:
        raise ValueError(f"No dialogue turns found in {path.relative_to(REPO_ROOT)}")
    return turns


def speaker_voices(path: Path) -> dict[str, str]:
    manifest = read_yaml(path)
    for asset in manifest.get("assets", []):
        mapping = asset.get("speaker_voices") if isinstance(asset, dict) else None
        if isinstance(mapping, dict) and mapping:
            return {str(name): str(voice) for name, voice in mapping.items()}
    raise ValueError(f"No speaker voice mapping found in {path.relative_to(REPO_ROOT)}")


def gender_for_voice(voice: str) -> str:
    normalized = voice.lower()
    return "female" if any(marker in normalized for marker in FEMALE_VOICE_MARKERS) else "male"


def unique_speakers(dialogue: list[tuple[str, str]]) -> list[str]:
    return list(dict.fromkeys(speaker for speaker, _ in dialogue))


def matching_turn(
    dialogue: list[tuple[str, str]], phrase: str, fallback_index: int
) -> tuple[str, str]:
    needle = normalize_phrase(phrase)
    for speaker, line in dialogue:
        haystack = normalize_phrase(line)
        if needle and (needle in haystack or haystack in needle):
            return speaker, line
    return dialogue[min(fallback_index, len(dialogue) - 1)]


def phrase_text(phrases: Any, index: int, fallback: str) -> str:
    if isinstance(phrases, list) and index < len(phrases) and isinstance(phrases[index], dict):
        value = str(phrases[index].get("phrase") or "").strip()
        if value:
            return value
    return fallback


def normalize_phrase(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def extract_section(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    body = text[match.end() :].split("\n##", 1)[0]
    return " ".join(body.strip().split())


def characters_as_lines(characters: list[str]) -> str:
    return "\n".join(f"- {profile}." for profile in characters)


def index_row(lesson_dir: Path, prompt_path: Path) -> dict[str, str]:
    _, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    lesson = read_yaml(lesson_dir / "lesson.yaml")
    return {
        "level": level,
        "unit": f"{numeric_prefix(unit_key):02d}",
        "lesson": f"{numeric_prefix(lesson_key):02d}",
        "lesson_key": lesson_key,
        "slug": str(lesson.get("slug") or ""),
        "title": str(lesson.get("title") or ""),
        "prompt_file": str(prompt_path.relative_to(REPO_ROOT)),
    }


def build_index(rows: list[dict[str, str]]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def build_readme() -> str:
    return """# English lesson visual prompts

This folder contains one production prompt pack for every English lesson. It does not change lesson assets automatically.

Example:

```text
A1/unit-01-greeting-introducing-yourself/lesson-01-saying-hello/
└── PROMPT.md
```

Workflow:

1. Use `INDEX.csv` to find a lesson.
2. Open its `PROMPT.md`.
3. Generate only the hero or cards you want to replace.
4. Replace and wire the selected assets manually.

Existing lesson images and visual mappings are intentionally untouched.
"""


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML must contain a mapping: {path.relative_to(REPO_ROOT)}")
    return data


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def numeric_prefix(value: str) -> int:
    match = re.search(r"(?:unit|lesson)-(\d+)", value)
    return int(match.group(1)) if match else 0


if __name__ == "__main__":
    sys.exit(main())
