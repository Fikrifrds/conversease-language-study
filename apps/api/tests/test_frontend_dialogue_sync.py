import re
import unittest
from pathlib import Path

from app.data.curriculum import A1_COURSE, get_lesson_or_none, repo_root
from app.services.audio_generation import listening_script_to_dialogue_turns


class FrontendDialogueSyncTest(unittest.TestCase):
    def test_frontend_dialogues_match_a1_listening_scripts(self):
        frontend_dialogues = parse_frontend_lesson_dialogues(
            repo_root() / "apps" / "web" / "lib" / "data.ts"
        )

        for unit in A1_COURSE["units"]:
            for lesson in unit["lessons"]:
                slug = lesson["slug"]
                with self.subTest(slug=slug):
                    self.assertIn(slug, frontend_dialogues)
                    content_lesson = get_lesson_or_none(slug)
                    self.assertIsNotNone(content_lesson)
                    lesson_dir = Path(content_lesson["content_files"]["lesson"]).parent
                    turns = listening_script_to_dialogue_turns(lesson_dir / "listening_script.md")
                    expected = [(turn.speaker, turn.text) for turn in turns]

                    self.assertEqual(frontend_dialogues[slug], expected)


def parse_frontend_lesson_dialogues(path: Path) -> dict[str, list[tuple[str, str]]]:
    source = path.read_text(encoding="utf-8")
    lesson_catalog = extract_between(source, "export const lessonCatalog = [", "\n];\n\nexport const lessonsBySlug")
    dialogues: dict[str, list[tuple[str, str]]] = {}

    for block in top_level_object_blocks(lesson_catalog):
        slug_match = re.search(r'slug:\s*"([^"]+)"', block)
        if not slug_match:
            continue

        dialogue_body = extract_array_body(block, "dialogue")
        if dialogue_body is None:
            continue

        dialogues[slug_match.group(1)] = [
            (match.group(1), unescape_ts_string(match.group(2)))
            for match in re.finditer(
                r'\{\s*speaker:\s*"([^"]+)",\s*text:\s*"((?:\\.|[^"])*)"\s*\}',
                dialogue_body,
            )
        ]

    return dialogues


def extract_between(source: str, start_marker: str, end_marker: str) -> str:
    start = source.index(start_marker) + len(start_marker)
    end = source.index(end_marker, start)
    return source[start:end]


def extract_array_body(block: str, key: str) -> str | None:
    match = re.search(rf"\b{re.escape(key)}:\s*\[", block)
    if not match:
        return None
    open_index = block.index("[", match.start())
    close_index = matching_delimiter_index(block, open_index, "[", "]")
    return block[open_index + 1 : close_index]


def top_level_object_blocks(source: str) -> list[str]:
    blocks: list[str] = []
    index = 0
    while index < len(source):
        if source[index] != "{":
            index += 1
            continue
        end_index = matching_delimiter_index(source, index, "{", "}")
        blocks.append(source[index : end_index + 1])
        index = end_index + 1
    return blocks


def matching_delimiter_index(source: str, start: int, open_char: str, close_char: str) -> int:
    depth = 0
    quote: str | None = None
    escaped = False

    for index in range(start, len(source)):
        char = source[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue

        if char in {'"', "'", "`"}:
            quote = char
            continue
        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return index

    raise ValueError(f"Could not find matching delimiter for {open_char} at {start}")


def unescape_ts_string(value: str) -> str:
    return value.replace(r"\"", '"').replace(r"\\", "\\")


if __name__ == "__main__":
    unittest.main()
