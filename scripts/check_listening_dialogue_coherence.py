from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

from app.services.audio_generation import DialogueTurn, listening_script_to_dialogue_turns


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    file_path: str
    lesson_slug: str | None
    context: list[str]


YES_NO_PREFIXES = (
    "did ",
    "do ",
    "does ",
    "are ",
    "is ",
    "was ",
    "were ",
    "can ",
    "could ",
    "would ",
    "will ",
    "have ",
    "has ",
    "had ",
    "should ",
    "may ",
    "might ",
)

YES_PREFIXES = ("yes", "yeah", "yep", "sure", "of course", "i did", "i do", "i can", "i will")
NO_PREFIXES = ("no", "nope", "not really", "i didn't", "i dont", "i can't", "i cannot", "i won't")

WH_PREFIXES = ("what", "where", "when", "why", "how", "which", "who", "whom", "whose")

_WS_RE = re.compile(r"\s+")
_TIME_MARKERS = (
    "yesterday",
    "last night",
    "tonight",
    "today",
    "tomorrow",
    "this morning",
    "this afternoon",
    "this evening",
    "now",
)
_CONNECTOR_PREFIXES = (
    "and ",
    "so ",
    "then ",
    "also ",
    "by the way",
    "anyway",
)


def normalize_text(text: str) -> str:
    return _WS_RE.sub(" ", text.strip().lower())


def is_question(text: str) -> bool:
    return text.strip().endswith("?")


def is_yes_no_question(text: str) -> bool:
    t = normalize_text(text)
    return any(t.startswith(prefix) for prefix in YES_NO_PREFIXES)


def is_wh_question(text: str) -> bool:
    t = normalize_text(text)
    return any(t.startswith(prefix + " ") or t == prefix for prefix in WH_PREFIXES)


def looks_like_yes_no_answer(text: str) -> bool:
    t = normalize_text(text)
    return t.startswith(YES_PREFIXES) or t.startswith(NO_PREFIXES) or t.startswith(("we have", "how about", "that works"))


def looks_like_bare_yes_no(text: str) -> bool:
    t = normalize_text(text).rstrip(".!")
    return t in {"yes", "no", "yeah", "yep", "nope"}


def has_answer_then_question(text: str) -> bool:
    t = text.strip()
    if not t.endswith("?"):
        return False
    if "?" not in t:
        return False
    return "." in t or "!" in t or ";" in t


def extract_time_marker(text: str) -> str | None:
    t = normalize_text(text)
    for marker in _TIME_MARKERS:
        if marker in t:
            return marker
    return None


def starts_with_connector(text: str) -> bool:
    t = normalize_text(text)
    return any(t.startswith(prefix) for prefix in _CONNECTOR_PREFIXES)


def is_request_like_question(text: str) -> bool:
    t = normalize_text(text).rstrip("?")
    return t.startswith(
        (
            "can i have ",
            "can i get ",
            "could i have ",
            "could i get ",
            "may i have ",
            "may i get ",
        )
    )


def extract_lesson_slug(listening_script_path: Path) -> str | None:
    parts = list(listening_script_path.parts)
    if "lessons" in parts:
        return None
    if "curriculum" not in parts:
        return None
    if "lesson-" not in "/".join(parts):
        return None
    for part in reversed(parts):
        if part.startswith("lesson-"):
            return part.replace("lesson-", "", 1)
    return None


def build_context(turns: list[DialogueTurn], start: int, end: int) -> list[str]:
    context: list[str] = []
    for idx in range(max(0, start), min(len(turns), end)):
        context.append(f"{turns[idx].speaker}: {turns[idx].text}")
    return context


def check_file(path: Path) -> list[Issue]:
    turns = listening_script_to_dialogue_turns(path)
    issues: list[Issue] = []
    lesson_slug = extract_lesson_slug(path)

    if len(turns) < 4:
        issues.append(
            Issue(
                code="too_few_turns",
                message=f"Dialogue terlalu pendek ({len(turns)} turns).",
                file_path=str(path),
                lesson_slug=lesson_slug,
                context=build_context(turns, 0, len(turns)),
            )
        )
        return issues

    normalized_questions_recent: list[str] = []
    last_question_by_speaker: dict[str, tuple[str, str | None]] = {}
    for i, turn in enumerate(turns):
        text = turn.text

        if is_question(text):
            q_norm = normalize_text(text).rstrip("?")
            normalized_questions_recent.append(q_norm)
            if len(normalized_questions_recent) > 5:
                normalized_questions_recent = normalized_questions_recent[-5:]

            current_marker = extract_time_marker(text)
            previous_question = last_question_by_speaker.get(turn.speaker)
            if (
                previous_question
                and current_marker
                and previous_question[1]
                and current_marker != previous_question[1]
                and not starts_with_connector(text)
            ):
                issues.append(
                    Issue(
                        code="abrupt_time_shift_question",
                        message="Pertanyaan pindah time reference (mis. last night -> yesterday) tanpa connector (And/So/Then).",
                        file_path=str(path),
                        lesson_slug=lesson_slug,
                        context=build_context(turns, i - 3, i + 2),
                    )
                )

            last_question_by_speaker[turn.speaker] = (q_norm, current_marker)

            if normalized_questions_recent.count(q_norm) >= 2:
                issues.append(
                    Issue(
                        code="repeated_question",
                        message="Pertanyaan yang sama muncul berulang dekat-dekat.",
                        file_path=str(path),
                        lesson_slug=lesson_slug,
                        context=build_context(turns, i - 3, i + 3),
                    )
                )

            if i == len(turns) - 1:
                issues.append(
                    Issue(
                        code="question_without_answer",
                        message="Pertanyaan di akhir dialog tidak punya jawaban setelahnya.",
                        file_path=str(path),
                        lesson_slug=lesson_slug,
                        context=build_context(turns, i - 2, i + 2),
                    )
                )
                continue

            next_turn = turns[i + 1]
            next_text = next_turn.text

            if (
                is_question(next_text)
                and not has_answer_then_question(next_text)
                and not looks_like_yes_no_answer(next_text)
                and not is_request_like_question(text)
            ):
                issues.append(
                    Issue(
                        code="question_followed_by_question",
                        message="Pertanyaan diikuti pertanyaan lagi (tanpa jawaban) — sering terasa tidak nyambung.",
                        file_path=str(path),
                        lesson_slug=lesson_slug,
                        context=build_context(turns, i - 2, i + 3),
                    )
                )

            if is_yes_no_question(text) and not is_request_like_question(text) and not looks_like_yes_no_answer(next_text):
                issues.append(
                    Issue(
                        code="yesno_question_non_yesno_answer",
                        message="Yes/No question tapi jawaban berikutnya tidak terlihat seperti ya/tidak.",
                        file_path=str(path),
                        lesson_slug=lesson_slug,
                        context=build_context(turns, i - 1, i + 3),
                    )
                )

            if is_wh_question(text) and looks_like_bare_yes_no(next_text):
                issues.append(
                    Issue(
                        code="wh_question_bare_yesno",
                        message="WH-question tapi jawaban hanya 'Yes/No' (sering tidak nyambung).",
                        file_path=str(path),
                        lesson_slug=lesson_slug,
                        context=build_context(turns, i - 1, i + 3),
                    )
                )

    return issues


def iter_listening_scripts(root: Path) -> list[Path]:
    return sorted(root.glob("content/curriculum/english/*/units/*/lesson-*/listening_script.md"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path", default=None)
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    scripts = iter_listening_scripts(repo_root)

    all_issues: list[Issue] = []
    for script in scripts:
        all_issues.extend(check_file(script))

    payload = {
        "file_count": len(scripts),
        "issue_count": len(all_issues),
        "issues": [
            {
                "code": issue.code,
                "message": issue.message,
                "file_path": issue.file_path,
                "lesson_slug": issue.lesson_slug,
                "context": issue.context,
            }
            for issue in all_issues
        ],
    }

    if args.json_path:
        out_path = Path(args.json_path)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Checked {payload['file_count']} listening_script.md files.")
    print(f"Found {payload['issue_count']} potential issues.")

    if args.fail_on_issues and payload["issue_count"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
