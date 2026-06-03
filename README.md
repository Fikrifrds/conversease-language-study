# Conversease

Conversation-first English learning platform for Indonesian learners.

This repository starts the MVP foundation from the PRD:

- `apps/web`: Next.js frontend for landing, onboarding, dashboard, lessons, Conversation Coach, pricing, and billing.
- `apps/api`: FastAPI backend skeleton with learning, billing/minutes, email, AI, and conversation domains.
- `apps/worker`: background worker placeholder for STT, TTS, email, billing, and reminder jobs.
- `packages/shared`: shared product constants and contracts.
- `content`: curriculum and email template seeds.
- `infra`: Docker and Nginx deployment scaffolding.
- `docs`: architecture and implementation notes.

## First Run

Create local environment config:

```bash
cp .env.example .env.local
```

Install frontend dependencies:

```bash
npm install
```

Run the web app:

```bash
npm run dev --workspace apps/web
```

Run backend tests that do not require external services:

```bash
python3 -m unittest discover -s apps/api/tests -t apps/api
```

Run database migrations:

```bash
apps/api/.venv/bin/alembic -c apps/api/alembic.ini upgrade head
```

The local `.env.local` should target PostgreSQL database `conversease_db`.
For direct host development, create it on local PostgreSQL. Docker Compose creates
the same database name inside the `postgres` service and overrides database/cache
hostnames for containers.

Check applied vs pending migration files:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.migration_status
```

Run the API after creating a Python virtual environment and installing dependencies:

```bash
cd apps/api
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

See `docs/database_migrations.md` for the full migration workflow,
`docs/content_operations.md` for curriculum production, `docs/deployment.md`
for deployment, `docs/linux_nginx_deploy.md` for a Linux + Nginx remote server
runbook, and `docs/release_readiness.md` for the current release checklist.

## MVP Focus

The first implementation slice covers:

1. Product-facing web shell and core pages.
2. A1 Unit 1 structured curriculum and lesson content.
3. Billing access, payment order records, and Conversation Coach minute ledger.
4. Provider abstraction points for LLM, email, STT, TTS, and payments.
5. Idempotent email and payment webhook surfaces.
6. Unit-testable threshold and minutes logic.
