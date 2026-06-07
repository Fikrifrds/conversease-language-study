#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"
OUTPUT = API_ROOT / "app" / "domain" / "generated_roleplay_scripts.py"

sys.path.insert(0, str(API_ROOT))
from app.data.curriculum import load_course  # noqa: E402


def py_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_expected_keywords(values: Any) -> str:
    if not isinstance(values, list):
        return "()"
    items = [py_string(str(v)) for v in values if str(v).strip()]
    if not items:
        return "()"
    if len(items) == 1:
        return f"({items[0]},)"
    return f"({', '.join(items)})"


def render_turn(turn: dict[str, Any]) -> str:
    coach = py_string(str(turn.get("coach") or "").strip())
    hint = py_string(str(turn.get("hint") or "").strip())
    sample = py_string(str(turn.get("sample_answer") or "").strip())
    focus = py_string(str(turn.get("focus") or "").strip())
    expected = render_expected_keywords(turn.get("expected_keywords"))
    explanation = str(turn.get("indonesian_explanation") or "").strip()
    explanation_part = (
        f", indonesian_explanation={py_string(explanation)}" if explanation else ""
    )
    return (
        "CoachTurn("
        f"coach={coach}, hint={hint}, sample_answer={sample}, focus={focus}, "
        f"expected_keywords={expected}{explanation_part}"
        ")"
    )


def collect_generated_scripts() -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for level_code in ("A1", "A2", "B1", "B2", "C1"):
        course = load_course(level_code=level_code)
        for unit in course.get("units", []):
            for lesson in unit.get("lessons", []):
                roleplay = lesson.get("roleplay") or {}
                turns = roleplay.get("turns")
                if not isinstance(turns, list) or not turns:
                    continue
                out[str(lesson["slug"])] = turns
    return out


def render_output(scripts: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = []
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from dataclasses import dataclass")
    lines.append("")
    lines.append("")
    lines.append("@dataclass(frozen=True)")
    lines.append("class CoachTurn:")
    lines.append("    coach: str")
    lines.append("    hint: str")
    lines.append("    sample_answer: str")
    lines.append("    focus: str")
    lines.append("    expected_keywords: tuple[str, ...] = ()")
    lines.append('    indonesian_explanation: str = ""')
    lines.append("")
    lines.append("")
    lines.append("GENERATED_ROLEPLAY_SCRIPTS: dict[str, tuple[CoachTurn, ...]] = {")
    for slug in sorted(scripts):
        lines.append(f"    {py_string(slug)}: (")
        for turn in scripts[slug]:
            lines.append(f"        {render_turn(turn)},")
        lines.append("    ),")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def generate() -> str:
    scripts = collect_generated_scripts()
    return render_output(scripts)


def main() -> int:
    OUTPUT.write_text(generate(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

