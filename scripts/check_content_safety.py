from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    category: str
    pattern: str
    file_path: str
    line_number: int
    line: str


PATTERNS: dict[str, list[str]] = {
    "haram_alcohol": [
        r"\b(alcohol|beer|wine|vodka|whiskey|rum|cocktail|drunk|hangover)\b",
        r"\b(minum( minuman)? keras|mabuk|arak)\b",
    ],
    "haram_pork": [
        r"\b(pork|bacon|ham)\b",
        r"\b(babi)\b",
    ],
    "haram_gambling": [
        r"\b(casino|gambl(e|ing)|bet(ting)?|lottery)\b",
        r"\b(judi|taruhan)\b",
    ],
    "adult_content": [
        r"\b(sex|sexual|nude|porn)\b",
        r"\b(seks|pornografi|telanjang)\b",
    ],
    "self_harm_violence": [
        r"\b(suicide|self-harm|kill yourself|murder|rape)\b",
        r"\b(bunuh diri|melukai diri|pembunuhan|perkosa)\b",
    ],
    "profanity": [
        r"\b(fuck|shit|bitch|asshole)\b",
        r"\b(anjing|bangsat|kontol|memek)\b",
    ],
    "hate_language": [
        r"\b(hate)\b",
        r"\b(kafir)\b",
    ],
}


def iter_content_files(repo_root: Path) -> list[Path]:
    content_root = repo_root / "content" / "curriculum" / "english"
    if not content_root.exists():
        return []
    files: list[Path] = []
    files.extend(content_root.glob("**/*.md"))
    files.extend(content_root.glob("**/*.yaml"))
    return sorted(set(files))


def scan_file(path: Path, compiled: list[tuple[str, str, re.Pattern[str]]]) -> list[Finding]:
    findings: list[Finding] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return findings
    for idx, line in enumerate(lines, start=1):
        haystack = line.lower()
        for category, raw, regex in compiled:
            if regex.search(haystack):
                findings.append(
                    Finding(
                        category=category,
                        pattern=raw,
                        file_path=str(path),
                        line_number=idx,
                        line=line.rstrip(),
                    )
                )
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path", default=None)
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    files = iter_content_files(repo_root)

    compiled: list[tuple[str, str, re.Pattern[str]]] = []
    for category, patterns in PATTERNS.items():
        for raw in patterns:
            compiled.append((category, raw, re.compile(raw, flags=re.IGNORECASE)))

    findings: list[Finding] = []
    for path in files:
        findings.extend(scan_file(path, compiled))

    payload = {
        "file_count": len(files),
        "finding_count": len(findings),
        "findings": [
            {
                "category": f.category,
                "pattern": f.pattern,
                "file_path": f.file_path,
                "line_number": f.line_number,
                "line": f.line,
            }
            for f in findings
        ],
    }

    if args.json_path:
        out_path = Path(args.json_path)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Scanned {payload['file_count']} files.")
    print(f"Found {payload['finding_count']} safety findings.")

    if args.fail_on_issues and payload["finding_count"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

