# Operations Runbook

This runbook covers the controlled beta release operations for Conversease.

## Release Checklist

Run from the repository root:

```bash
apps/api/.venv/bin/alembic -c apps/api/alembic.ini upgrade head
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.migration_status
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/validate_curriculum.py
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_preflight.py
apps/api/.venv/bin/python -m unittest discover -s apps/api/tests -t apps/api
npm run lint --workspace apps/web
npm run typecheck --workspace apps/web
npm run build --workspace apps/web
```

The checklist must confirm `/api/level-tests/A1` returns the published final test, `/level-test/A1` renders in the web app, a submitted attempt produces a saved report, and `/admin/level-tests` can mark a submitted attempt as `reviewed`.

Production env must include:

- `RELEASE_VERSION`
- `APP_ENV=production`
- `DATABASE_URL` using PostgreSQL
- `PUBLIC_APP_URL` and `API_BASE_URL` using HTTPS
- `NEXT_PUBLIC_API_BASE_URL` matching `API_BASE_URL + /api`
- `CORS_ORIGINS_RAW` with explicit production origins
- `JWT_SECRET` with at least 32 characters
- `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET`
- `RESEND_API_KEY`
- `PAYMENT_ADMIN_API_KEY`
- Bank Jago manual-transfer account details
- Rate limit env values, unless using the documented defaults

Production secrets must be real values. Do not deploy with `.env.production.example` placeholders such as `replace-with...` or `<...>`.

Before accepting paid beta users, send a real admin test email:

```bash
curl -X POST https://api.conversease.com/api/admin/test-email/send \
  -H "Content-Type: application/json" \
  -H "x-admin-api-key: $PAYMENT_ADMIN_API_KEY" \
  -d '{"template_key":"minutes_low","recipient_email":"denahku.team@gmail.com"}'
```

The response must show `"sent": true` and include a Resend provider id.

After deploying, run the automated HTTP smoke script:

```bash
API_BASE_URL=https://api.conversease.com \
PUBLIC_APP_URL=https://app.conversease.com \
PAYMENT_ADMIN_API_KEY="$PAYMENT_ADMIN_API_KEY" \
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_smoke.py
```

It must return `"status": "pass"` before traffic is sent to the release.

## Health Checks

Liveness:

```bash
curl https://api.conversease.com/api/health
```

Readiness:

```bash
curl https://api.conversease.com/api/ready
```

Expected readiness:

```json
{"status":"ready","service":"conversease-api","checks":{"database":"ok","migrations":"ok","applied_heads":["202606030009"],"expected_heads":["202606030009"]}}
```

Every response includes `x-request-id`. When reporting an issue, copy this header from the failing API response.

If readiness returns `503` with `migrations=pending`, run the file-based Alembic migrations before sending traffic to the release.

Runtime metrics:

```bash
curl https://api.conversease.com/api/metrics
```

Use this for quick beta diagnostics: rising `5xx` buckets, unexpected `4xx` spikes, high average request duration, or traffic not reaching expected paths. Metrics reset on process restart.

## Backup

Create a PostgreSQL backup:

```bash
DATABASE_URL="$DATABASE_URL" BACKUP_DIR=/secure/backups bash scripts/backup_postgres.sh
```

Each backup writes a `.dump`, `.sha256`, and `.manifest.json` file.

Recommended schedule:

- Daily backup during beta.
- Retain at least 14 daily backups.
- Store backups outside the app server when possible.
- Test restore into staging at least once before public paid traffic.

Verify checksum and dump catalog:

```bash
BACKUP_FILE=/secure/backups/conversease-YYYYMMDDTHHMMSSZ.dump \
  bash scripts/verify_postgres_backup.sh
```

Restore test into disposable staging:

```bash
BACKUP_FILE=/secure/backups/conversease-YYYYMMDDTHHMMSSZ.dump \
  RESTORE_DATABASE_URL="$STAGING_DATABASE_URL" \
  ALLOW_RESTORE_CLEAN=true \
  bash scripts/verify_postgres_backup.sh
```

## Manual Payment Incident

If a user says payment is not active:

1. Ask for the exact transfer amount and email.
2. Ask the user to reopen `/billing?order_id=<order-id>` if they have the order link; the same account can recover the current order status there.
3. Open `/admin/payments`.
4. Search by unique code or order id.
5. Confirm the order status is `confirmed`; pending orders older than `MANUAL_TRANSFER_EXPIRE_HOURS` are expired by the API when opened/listed and should not be approved.
6. Match exact amount, transfer date, and sender name against Bank Jago mutation.
7. Approve only after the mutation matches.
8. Confirm the order detail shows `Email user` as sent. If email delivery fails, the order can still be approved; check `RESEND_API_KEY`, Resend logs, and `/api/admin/test-email/send`, then use Resend from `/admin/payments`.
9. Copy the API `x-request-id` if an approval fails.

## Content Update

For controlled beta content edits:

1. Open `/admin/cms`.
2. Login with an account whose email is listed in `ADMIN_EMAILS_RAW` or promoted from `/admin/users`.
3. Edit one lesson or one email template at a time.
4. Save, then reload the CMS summary and confirm the change appears in Change Log.
5. If a content edit needs to be reverted, click Restore on the target revision in Change Log and confirm a new `rollback` revision appears.
6. If save returns `content_changed_reload_required`, reload CMS and reapply the edit to the latest content.
7. Run `PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/validate_curriculum.py`.
8. Confirm `content/production_tracker.csv` has one row for each published lesson and every core content column is `done`.
9. Run the release checklist before deploying the edited content.

Do not give broad editorial access until draft approval is added.

## A1 Final Test Review

For beta manual scoring:

1. Open `/admin/level-tests`.
2. Login with an admin account.
3. Load `Submitted` attempts.
4. Select one attempt and review the user's final-test responses/recording from the support context.
5. Enter section scores from 0 to 100, lesson completion percentage, reviewer name, and notes.
6. Save official review.
7. Ask the user to reopen `/level-test/A1` and confirm the report status is `reviewed`.

Do not score `in_progress` attempts. Automated public speaking assessment still requires the AI/STT/TTS worker pipeline.

## Auth Incident

If a user cannot verify email or reset password:

1. Confirm `RESEND_API_KEY` is configured.
2. Render a template through `/api/admin/test-email/render` and confirm there are no unresolved variables.
3. Send a real test email through `/api/admin/test-email/send`.
4. Ask the user to request a new link from `/verify-email` or `/forgot-password`.
5. Check API logs by `x-request-id`.
6. Confirm app URLs use production HTTPS domains.

## Error Response

Unexpected API errors return:

```json
{"detail":"Internal server error","request_id":"req-..."}
```

Use the `request_id` to find the structured request log line.
