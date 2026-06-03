from __future__ import annotations

import argparse
from pathlib import Path
import sys

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from app.core.config import settings
from app.db.session import engine_options


def build_config(config_path: str) -> Config:
    config = Config(config_path)
    config.set_main_option("sqlalchemy.url", settings.database_url)
    return config


def load_applied_revisions(database_url: str) -> set[str]:
    engine = create_engine(database_url, **engine_options(database_url))
    with engine.connect() as connection:
        return load_applied_revisions_from_connection(connection)


def load_applied_revisions_from_connection(connection: Connection) -> set[str]:
    context = MigrationContext.configure(connection)
    return set(context.get_current_heads())


def expected_revision_heads(config: Config) -> set[str]:
    script = ScriptDirectory.from_config(config)
    return set(script.get_heads())


def migration_head_check(config: Config, applied_heads: set[str]) -> dict[str, object]:
    expected_heads = expected_revision_heads(config)
    return {
        "ok": applied_heads == expected_heads,
        "applied_heads": sorted(applied_heads),
        "expected_heads": sorted(expected_heads),
        "pending_heads": sorted(expected_heads - applied_heads),
        "unexpected_heads": sorted(applied_heads - expected_heads),
    }


def migration_rows(config: Config, applied_heads: set[str]) -> list[tuple[str, str, str]]:
    script = ScriptDirectory.from_config(config)
    applied_revisions: set[str] = set()
    for head in applied_heads:
        applied_revisions.update(revision.revision for revision in script.iterate_revisions(head, "base"))

    rows: list[tuple[str, str, str]] = []

    for revision in reversed(list(script.walk_revisions())):
        status = "applied" if revision.revision in applied_revisions else "pending"
        rows.append((revision.revision, status, revision.path))

    return rows


def main() -> int:
    default_config = Path(__file__).resolve().parents[2] / "alembic.ini"
    parser = argparse.ArgumentParser(description="Show Conversease migration status.")
    parser.add_argument("--config", default=str(default_config), help="Path to alembic.ini")
    args = parser.parse_args()

    config = build_config(args.config)
    try:
        applied_heads = load_applied_revisions(settings.database_url)
    except Exception as exc:
        print(f"Could not read migration status: {exc}", file=sys.stderr)
        return 1

    rows = migration_rows(config, applied_heads)
    if not rows:
        print("No migration files found.")
        return 0

    print("Revision      Status   File")
    print("------------  -------  ----")
    for revision, status, path in rows:
        print(f"{revision:<12}  {status:<7}  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
