# Database Migrations

Conversease uses Alembic for file-based database migrations.

## Files

- Config: `apps/api/alembic.ini`
- Migration environment: `apps/api/migrations/env.py`
- Migration files: `apps/api/migrations/versions/*.py`
- Applied migration tracker table: `alembic_version`

Every schema change must be added as a migration file in `apps/api/migrations/versions`.
Do not apply manual SQL changes without a matching migration file.

## Commands

Run from the repository root:

```bash
apps/api/.venv/bin/alembic -c apps/api/alembic.ini upgrade head
```

Show current applied revision:

```bash
apps/api/.venv/bin/alembic -c apps/api/alembic.ini current
```

Show all migration files:

```bash
apps/api/.venv/bin/alembic -c apps/api/alembic.ini history
```

Show applied vs pending files:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.migration_status
```

Create a new migration file:

```bash
apps/api/.venv/bin/alembic -c apps/api/alembic.ini revision -m "describe schema change"
```

Rollback one migration:

```bash
apps/api/.venv/bin/alembic -c apps/api/alembic.ini downgrade -1
```

## Current Revisions

- `202606030001`: conversation practice tables
- `202606030002`: auth users and user ownership
- `202606030003`: onboarding profile and lesson progress tables
- `202606030004`: billing access, payment order, and minute ledger tables
- `202606030005`: manual transfer payment tracking fields
- `202606030006`: email verification and password reset tokens
- `202606030007`: Admin CMS content revision audit trail
- `202606030008`: persisted A1 level test attempts and reports
- `202606030009`: admin review fields for A1 level test attempts

## Local Development

The app's built-in fallback uses SQLite when `DATABASE_URL` is omitted:

```text
apps/api/conversease_dev.db
```

Use `.env.local` for local development. The recommended local database is
`conversease_db` so schema behavior stays close to production:

```bash
DATABASE_URL=postgresql+psycopg://conversease:conversease@localhost:5432/conversease_db
```

Production or staging should also use PostgreSQL via `DATABASE_URL`, for example:

```bash
DATABASE_URL=postgresql+psycopg://user:password@host:5432/conversease_db
```
