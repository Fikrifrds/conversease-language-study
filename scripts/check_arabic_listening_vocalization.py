#!/usr/bin/env python3
"""Check Arabic listening scripts are vocalized for learner display and TTS."""
from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ARABIC_ROOT = REPO_ROOT / "content" / "curriculum" / "arabic"
ARABIC_LETTERS = re.compile(r"[\u0621-\u064a]")
ARABIC_TOKEN = re.compile(r"[\u0621-\u064a\u064b-\u0652\u0670]+")
HARAKAT = set("\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670")


def unchecked_tokens(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8").split("## Audio Direction", 1)[0]
    bare_tokens: list[str] = []
    for token in ARABIC_TOKEN.findall(text):
        letter_count = len(ARABIC_LETTERS.findall(token))
        if letter_count >= 3 and not any(char in HARAKAT for char in token):
            bare_tokens.append(token)
    return bare_tokens


def main() -> int:
    failures: list[tuple[Path, list[str]]] = []
    for path in sorted(ARABIC_ROOT.glob("*/units/*/*/listening_script.md")):
        tokens = unchecked_tokens(path)
        if tokens:
            failures.append((path, tokens))

    if not failures:
        print("Arabic listening scripts are vocalized.")
        return 0

    print("Arabic listening scripts still contain unvocalized tokens:", file=sys.stderr)
    for path, tokens in failures:
        rel_path = path.relative_to(REPO_ROOT)
        sample = ", ".join(tokens[:12])
        print(f"- {rel_path}: {sample}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
