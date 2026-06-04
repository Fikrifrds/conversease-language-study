# Deployment Guide

This guide describes a production-oriented deployment for Conversease.

## Required Services

- PostgreSQL 16 or newer
- Redis 7 or newer
- API runtime for `apps/api`
- Web runtime for `apps/web`
- Reverse proxy or platform routing with HTTPS
- Resend account for auth and payment email delivery

SQLite is only for local development. Production startup fails when `APP_ENV=production` and `DATABASE_URL` points to SQLite.

## Environment

Copy `.env.production.example` to `.env.production` on the server and replace all placeholder values. Production startup rejects template placeholders such as `replace-with...` and `<...>`. In production, set at minimum:

```bash
APP_ENV=production
RELEASE_VERSION=2026.06.03
LOG_LEVEL=INFO
ENABLE_REQUEST_LOGGING=true
PUBLIC_APP_URL=https://app.conversease.com
API_BASE_URL=https://api.conversease.com
CORS_ORIGINS_RAW=https://app.conversease.com
DATABASE_URL=postgresql+psycopg://user:password@host:5432/conversease_db
REDIS_URL=redis://host:6379/0
JWT_SECRET=<at-least-32-random-characters>
GOOGLE_OAUTH_CLIENT_ID=<google-oauth-client-id>
GOOGLE_OAUTH_CLIENT_SECRET=<google-oauth-client-secret>
# Optional if different from API_BASE_URL + /api/auth/google/callback
GOOGLE_OAUTH_REDIRECT_URI=https://api.conversease.com/api/auth/google/callback
ADMIN_EMAILS_RAW=<first-admin-email@example.com>
NEXT_PUBLIC_API_BASE_URL=https://api.conversease.com/api
PAYMENT_ADMIN_EMAIL=denahku.team@gmail.com
PAYMENT_ADMIN_API_KEY=<at-least-24-random-characters>
MANUAL_TRANSFER_BANK_NAME="Bank Jago"
MANUAL_TRANSFER_ACCOUNT_NUMBER="5001 6527 8492"
MANUAL_TRANSFER_ACCOUNT_HOLDER="Fikri Firdaus"
MANUAL_TRANSFER_UNIQUE_CODE_MIN=101
MANUAL_TRANSFER_UNIQUE_CODE_MAX=999
MANUAL_TRANSFER_EXPIRE_HOURS=12
RESEND_API_KEY=<resend-api-key>
EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS=24
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES=60
RATE_LIMIT_ENABLED=true
RATE_LIMIT_WINDOW_SECONDS=60
AUTH_RATE_LIMIT_REQUESTS=30
ADMIN_RATE_LIMIT_REQUESTS=120
```

Manual transfer is the beta payment path. Provider credentials below can stay empty for controlled beta, but public paid automation requires:

```bash
MIDTRANS_SERVER_KEY=
MIDTRANS_CLIENT_KEY=
MIDTRANS_IS_PRODUCTION=true
TOGETHER_API_KEY=
ASSEMBLYAI_API_KEY=
MINIMAX_API_KEY=
```

`NEXT_PUBLIC_API_BASE_URL` is baked into the web build. For production it must be HTTPS, include the `/api` path, and match `API_BASE_URL + /api`. The release preflight fails production deploys when these values drift.

## Manual Transfer Operations

User checkout creates a `manual_transfer` order with:

- `base_amount_idr`: package price
- `unique_code`: 3-digit matching code
- `amount_idr`: exact transfer amount users must send
- `status=pending`
- `expires_at`: transfer confirmation deadline

The API keeps unique codes unique across active manual-transfer orders (`pending` and `confirmed`). Pending orders automatically expire after `MANUAL_TRANSFER_EXPIRE_HOURS`; expiration is applied when creating/listing/opening manual payment orders and when a stale order is confirmed or approved. Expired, failed, or success order codes can be reused later. If every configured code is currently active, checkout returns `503` so the user is not given a confusing duplicate transfer amount.

After the user confirms transfer, the API stores transfer date/sender details, changes status to `confirmed`, and emails `PAYMENT_ADMIN_EMAIL` with a deep link to:

```text
https://app.conversease.com/admin/payments?order_id=<order-id>&unique_code=<code>
```

The admin logs in with an account whose email is listed in `ADMIN_EMAILS_RAW`, opens that page, matches the exact amount against the Bank Jago mutation, then approves or rejects the order. Approval activates the subscription/top-up immediately and is idempotent: approving the same successful order again does not grant duplicate subscription or minutes. Approve/reject decisions send a user email (`payment_manual_approved` or `payment_manual_rejected`) so the user gets confirmation without refreshing billing manually. The delivery result is stored in order metadata under `customer_decision_email` and shown in `/admin/payments`. If `RESEND_API_KEY` is missing or Resend is down, the order decision still completes; fix email delivery, then use **Resend** from the order detail.

The user can reopen `/billing?order_id=<order-id>` while logged in to the same account to recover the exact transfer instructions and current status after refresh, browser close, or email follow-up. The API returns `404` for orders owned by another user.

API fallback commands are also available.

List confirmed orders:

```bash
curl https://api.conversease.com/api/admin/payment-orders?status=confirmed \
  -H "x-admin-api-key: $PAYMENT_ADMIN_API_KEY"
```

Find an order by unique code:

```bash
curl "https://api.conversease.com/api/admin/payment-orders?unique_code=492" \
  -H "x-admin-api-key: $PAYMENT_ADMIN_API_KEY"
```

Approve after matching bank mutation:

```bash
curl -X POST https://api.conversease.com/api/admin/payment-orders/<order-id>/approve \
  -H "Content-Type: application/json" \
  -H "x-admin-api-key: $PAYMENT_ADMIN_API_KEY" \
  -d '{"approved_by":"Admin","notes":"Matched Bank Jago mutation"}'
```

Before opening paid beta, render and send a test email to confirm templates, Resend, and admin delivery:

```bash
curl -X POST https://api.conversease.com/api/admin/test-email/render \
  -H "Content-Type: application/json" \
  -H "x-admin-api-key: $PAYMENT_ADMIN_API_KEY" \
  -d '{"template_key":"minutes_low"}'
```

```bash
curl -X POST https://api.conversease.com/api/admin/test-email/send \
  -H "Content-Type: application/json" \
  -H "x-admin-api-key: $PAYMENT_ADMIN_API_KEY" \
  -d '{"template_key":"minutes_low","recipient_email":"denahku.team@gmail.com"}'
```

The send endpoint rejects unresolved template variables with `422`, and returns the Resend provider id when delivery succeeds.

## Admin CMS Operations

The controlled beta CMS is available at:

```text
https://app.conversease.com/admin/cms
```

Use a logged-in admin account. The page can edit:

- Published lesson metadata in `content/curriculum/**/lesson.yaml`
- Conversation Coach roleplay setup in `conversation_coach_roleplay.yaml`
- Markdown email templates in `content/email_templates`
- Recent content revisions through the Change Log restore action

Every save records a `content_revisions` audit row with resource type, resource key, version, operator name, content hash, and before/after snapshots. Every restore creates a new `rollback` revision instead of deleting earlier history. CMS saves use a content hash and reject stale edits with `409 content_changed_reload_required`, so admins must reload before saving if another edit landed first.

After every content edit, run:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/validate_curriculum.py
apps/api/.venv/bin/python -m unittest discover -s apps/api/tests -t apps/api
npm run build --workspace apps/web
```

`scripts/validate_curriculum.py` also validates `content/production_tracker.csv`. Any lesson marked `published` must have every core content column marked `done`; `audio_generated=no` is allowed for beta because generated production audio is not required for manual-feedback beta.

For production teams with more than one editor, add draft/review workflow before allowing broad editorial access.

## A1 Final Test Review Operations

The controlled beta admin review page is available at:

```text
https://app.conversease.com/admin/level-tests
```

Use a logged-in admin account. The page can:

- Load A1 attempts by status: `submitted`, `reviewed`, `in_progress`, or all.
- Score each weighted final-test section from 0 to 100.
- Adjust lesson completion percentage when needed.
- Save reviewer name and notes.
- Update the user's saved report to `reviewed` with the official score and pass/fail result.

Only score attempts that have already been submitted. `in_progress` attempts cannot be reviewed.

API fallback commands are also available.

List submitted attempts:

```bash
curl "https://api.conversease.com/api/admin/level-test-attempts?level_code=A1&status=submitted" \
  -H "x-admin-api-key: $PAYMENT_ADMIN_API_KEY"
```

Score a submitted attempt:

```bash
curl -X POST https://api.conversease.com/api/admin/level-test-attempts/<attempt-id>/score \
  -H "Content-Type: application/json" \
  -H "x-admin-api-key: $PAYMENT_ADMIN_API_KEY" \
  -d '{"reviewed_by":"Admin","lesson_completion_percent":100,"scores":{"task_completion":90,"fluency":85,"pronunciation":82,"grammar":88,"vocabulary":86,"listening_response":84,"interaction":87},"notes":"Reviewed from beta final test recording."}'
```

## Build

API image:

```bash
docker build -t conversease-api -f apps/api/Dockerfile .
```

Web image:

```bash
docker build -t conversease-web -f apps/web/Dockerfile .
```

## Database Migration

Run migrations before starting a new API release:

```bash
apps/api/.venv/bin/alembic -c apps/api/alembic.ini upgrade head
```

For containerized deploys, run the equivalent command inside the API image:

```bash
alembic -c alembic.ini upgrade head
```

Check applied vs pending migration files:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.migration_status
```

## Release Preflight

Before promoting a beta release, run the preflight against the same environment that will run the API:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_preflight.py
```

The command prints a JSON report and exits non-zero for release-blocking failures. It checks API runtime config, web runtime API URL, manual transfer/email readiness, database connectivity, Alembic head, curriculum content, email template rendering, backup tooling, and optional automation integrations.

Warnings are acceptable for controlled beta when they only cover Midtrans or AI/STT/TTS automation. To make warnings fail in a stricter release pipeline:

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_preflight.py --strict-warnings
```

## Start Commands

API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Web:

```bash
node apps/web/server.js
```

The Docker Compose development setup runs API migrations before starting the API service.

## Health Checks

Liveness:

```bash
curl https://api.conversease.com/api/health
```

Readiness, including database connectivity and applied migration head:

```bash
curl https://api.conversease.com/api/ready
```

Expected readiness response:

```json
{"status":"ready","service":"conversease-api","checks":{"database":"ok","migrations":"ok","applied_heads":["202606030009"],"expected_heads":["202606030009"]}}
```

Every API response includes `x-request-id` for support and incident tracing.

Runtime metrics:

```bash
curl https://api.conversease.com/api/metrics
```

The metrics response includes uptime, total requests, average request duration, status-code buckets, method counts, and a capped path-count map. These in-memory metrics reset when the API process restarts and should complement, not replace, external uptime and error monitoring.

## Rate Limiting

The API applies in-memory rate limits to sensitive auth and admin endpoints:

- Auth endpoints: `AUTH_RATE_LIMIT_REQUESTS` per `RATE_LIMIT_WINDOW_SECONDS` per client IP/path.
- Admin endpoints: `ADMIN_RATE_LIMIT_REQUESTS` per `RATE_LIMIT_WINDOW_SECONDS` per client IP/path.

This protects controlled beta traffic on a single API process. Before broad public paid traffic, also configure rate limiting at the edge or WAF layer so limits apply consistently across multiple API instances.

## Post-Deploy Smoke Test

Run the automated HTTP smoke script against the deployed API and web app:

```bash
API_BASE_URL=https://api.conversease.com \
PUBLIC_APP_URL=https://app.conversease.com \
PAYMENT_ADMIN_API_KEY="$PAYMENT_ADMIN_API_KEY" \
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_smoke.py
```

The script checks API health/readiness/metrics, public curriculum, A1 lesson/test data, plans, core web pages, web security headers, and admin email-template diagnostics when `PAYMENT_ADMIN_API_KEY` is provided, including manual payment approval/rejection template rendering.

Then finish the human smoke flow:

1. Open the landing page.
2. Register a new account.
3. Verify the account email from the received Resend link.
4. Login with Google and confirm the callback reaches dashboard or the requested return path.
5. Request a password reset and confirm login works with the new password.
6. Complete onboarding.
7. Open dashboard and verify the first mission appears.
8. Open a lesson and mark it complete.
9. Confirm dashboard advances to the next lesson.
10. Open `/level-test/A1` and verify the final test loads with seven weighted skill sections.
11. Start and submit an A1 test attempt, then confirm the saved report appears.
12. Run the A1 readiness preview and confirm a passing score shows when all skill scores meet the thresholds.
13. Open billing and verify current access loads.
14. Create a manual transfer checkout and verify the Bank Jago instructions show exact amount and unique code.
15. Reload `/billing?order_id=<order-id>` and verify the same instructions/status are restored for the same logged-in user.
16. Confirm transfer and verify the order status changes to `confirmed`.
17. Approve the order from `/admin/payments`, verify the quota/access updates, verify the user receives the approval email, and use Resend if the order detail shows email delivery failed.
18. Open `/admin/cms` while logged in as an admin, and verify curriculum plus email templates are readable.
19. Open `/admin/level-tests` while logged in as an admin, save an official review, and verify the user report status changes to `reviewed`.
20. Run one Conversation Coach turn and confirm progress is saved.
21. Check `/api/ready` again after smoke testing.

## Backup And Restore

Minimum PostgreSQL backup:

```bash
DATABASE_URL="$DATABASE_URL" BACKUP_DIR=/secure/backups bash scripts/backup_postgres.sh
```

Each backup creates:

- `conversease-YYYYMMDDTHHMMSSZ.dump`
- `conversease-YYYYMMDDTHHMMSSZ.dump.sha256`
- `conversease-YYYYMMDDTHHMMSSZ.dump.manifest.json`

Verify checksum and dump catalog:

```bash
BACKUP_FILE=/secure/backups/conversease-YYYYMMDDTHHMMSSZ.dump \
  bash scripts/verify_postgres_backup.sh
```

Restore test to a disposable staging database:

```bash
BACKUP_FILE=/secure/backups/conversease-YYYYMMDDTHHMMSSZ.dump \
  RESTORE_DATABASE_URL="$STAGING_DATABASE_URL" \
  ALLOW_RESTORE_CLEAN=true \
  bash scripts/verify_postgres_backup.sh
```

Before public paid traffic, schedule automated daily backups and run restore verification into a staging database.

See `docs/operations_runbook.md` for release, incident, backup, and restore procedures.
See `docs/linux_nginx_deploy.md` for a complete single-server Linux + Nginx deployment runbook.

## Release Gate

Run these commands before promoting a release:

```bash
apps/api/.venv/bin/python -m unittest discover -s apps/api/tests -t apps/api
npm run lint --workspace apps/web
npm run typecheck --workspace apps/web
npm run build --workspace apps/web
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.migration_status
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_preflight.py
```

The same gates are enforced in GitHub Actions by `.github/workflows/release-gates.yml`.

Controlled paid beta can use manual transfer after Resend and admin approval are configured.
Fully automated public checkout still requires Midtrans webhook verification, AI/STT/TTS workers, monitoring, CMS draft workflow, and backup scheduling.
