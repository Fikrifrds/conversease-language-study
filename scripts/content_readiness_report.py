from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"


def ensure_api_import_path() -> None:
    api_path = str(API_ROOT)
    if api_path not in sys.path:
        sys.path.insert(0, api_path)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Conversease content readiness reports.")
    parser.add_argument("--language", default=None, help="Optional curriculum language folder filter.")
    parser.add_argument("--level", default=None, help="Optional level code filter.")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args(argv)

    ensure_api_import_path()
    from app.data.content_readiness import all_content_readiness_summary, render_markdown_report

    readiness = all_content_readiness_summary(language=args.language, level_code=args.level)
    if args.format == "json":
        print(json.dumps(readiness, indent=2, sort_keys=True))
    else:
        print(render_markdown_report(readiness), end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
