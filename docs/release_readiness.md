# Release Readiness

This document tracks the Conversease MVP release candidate.

## Ready For Local QA

- Public landing, pricing, login, register, onboarding, dashboard, courses, lessons, Conversation Coach, progress, A1 final test, billing, and settings.
- Authenticated app guard with Google login, email/password login, login return path, logout, email verification, and password reset.
- Local PostgreSQL database `conversease_db` with file-based Alembic migrations; SQLite remains available only as a no-`DATABASE_URL` development fallback.
- Auth-backed Conversation Coach persistence.
- Conversation Coach roleplay prompts and replies are lesson-specific; feedback is LLM-backed (Together/OpenAI via `LLM_DEFAULT_PROVIDER` + API key) with a deterministic keyword fallback when the LLM is not configured or fails.
- Onboarding and lesson progress persistence.
- Billing access model with subscription, payment order, top-up, and minute ledger tables.
- Manual transfer Bank Jago checkout with unique payment code, enforced confirmation expiry, user confirmation, admin email notification, admin approval UI, and admin approval endpoints.
- Admin email diagnostics can list, render, and send test emails through `/api/admin/email-templates`, `/api/admin/test-email/render`, and `/api/admin/test-email/send`.
- Admin CMS page for controlled editing of curriculum lesson metadata, lesson roleplay setup, and email templates, with content revision audit logs, revision rollback, and stale edit protection.
- Admin CMS Readiness tab shows per-level, per-unit, per-lesson content and audio checklist from every `content/curriculum/*/*/content_plan.yaml`, actual content files, `audio_manifest.yaml`, and `content/production_tracker.csv`.
- Admin CMS has a batch audio queue for generating all missing text-ready listening audio or regenerating every text-ready lesson after script edits.
- Admin A1 final-test review page for beta manual scoring of submitted attempts and official user report updates.
- Sandbox package activation remains available for local QA only and is disabled in production.
- Full A1 curriculum with all 40 lessons published across 8 units (greetings, spelling/numbers/contact, daily routine, work/study, places/directions, food/shopping, help/requests, review/final). 32 of 40 lessons are audio-ready; 8 still need audio generation.
- A2, B1, B2, and C1 curriculum text is complete (40 lessons per level) but not yet published: audio is not generated and publish status is unset in `content/production_tracker.csv`.
- Real Exam system (A1): database-backed templates/sections/items, exam runner UI, automatic scoring for objective items (MCQ, fill-blank, matching), weighted section results, and an admin review queue for speaking/writing responses. The A1 exam is seeded via `apps/api/scripts/seed_a1_exam.py` (32 items per the Real Exam PRD) and listening items need audio generation before public use.
- API course/lesson data is loaded from `content/curriculum` YAML files and validated by `scripts/validate_curriculum.py`, including required lesson support files and `content/production_tracker.csv`.
- Content readiness report is available at `scripts/content_readiness_report.py`; audio-specific audit is available at `scripts/audio_readiness_report.py`.
- Published A1 final conversation test is loaded from `content/curriculum/english/A1/final_evaluation.yaml`, validated for weights and minimums, exposed at `/api/level-tests/A1`, and persisted through authenticated attempt start, submit, report, and admin-reviewed scoring endpoints.
- Production env validation rejects unsafe production defaults and placeholder secrets from `.env.production.example`.
- API liveness, readiness, and runtime metrics endpoints are available at `/api/health`, `/api/ready`, and `/api/metrics`; readiness verifies database connectivity and Alembic migration head.
- API request tracing, structured request logging, security headers, backup script, backup verification helper, and operations runbook are available.
- Web app security headers are configured through Next.js and verified by the post-deploy smoke script.
- In-memory rate limiting protects auth and admin endpoints during controlled beta; configure external edge/WAF limits before public paid traffic.
- Release preflight script is available at `scripts/release_preflight.py` for API/web env, database, migration, curriculum, email-template rendering, payment/email, backup-tooling, and optional integration checks.
- Post-deploy HTTP smoke script is available at `scripts/release_smoke.py` for API health/readiness/metrics, public curriculum, A1 test, plans, web pages, and admin email diagnostics.
- GitHub Actions release gates are configured for API migrations, curriculum validation, release preflight, API lint/tests, and web lint/typecheck/build.
- Playwright E2E smoke (`npm run test:e2e`) covers the critical no-auth path: public pages render and protected routes redirect to login. Run `npm run test:e2e:install` once to fetch the browser; set `E2E_BASE_URL` to run against a deployed environment.
- Real Exam enforces a per-template attempt policy (PRD default: 3 attempts, then a 30-day cooldown) stored in the template's `metadata_json`; an unfinished attempt is resumed instead of consuming a new one. Attempt standing is exposed at `/api/exam-runner/attempt-status/{template_id}`.
- Deployment notes are documented in `docs/deployment.md`.

## Verification Commands

Run from the repository root:

```bash
apps/api/.venv/bin/alembic -c apps/api/alembic.ini upgrade head
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.migration_status
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/content_readiness_report.py --format markdown
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/audio_readiness_report.py --missing-only --text-ready-only
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/validate_curriculum.py
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_preflight.py
PYTHONPATH=apps/api apps/api/.venv/bin/python -m ruff check apps/api/app apps/api/tests scripts/release_preflight.py scripts/release_smoke.py scripts/validate_curriculum.py
apps/api/.venv/bin/python -m unittest discover -s apps/api/tests -t apps/api
npm run lint --workspace apps/web
npm run typecheck --workspace apps/web
npm run build --workspace apps/web
PAYMENT_ADMIN_API_KEY=test-admin-key-with-32-chars PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_smoke.py
```

CI runs the static and database-backed release gates through `.github/workflows/release-gates.yml` on pull requests, pushes to `main`, and manual dispatch. Run the HTTP smoke command after API and web are deployed or running locally.

## Production Blockers

- Manual transfer can support controlled paid beta after `RESEND_API_KEY`, `PAYMENT_ADMIN_API_KEY`, admin email, and Bank Jago account details are configured. Admin approval/rejection sends a user email, records delivery status, and supports resend from the payment detail.
- Manual transfer checkout links can be reopened by the owning user through `/billing?order_id=<order-id>` to recover instructions and current order status.
- Midtrans automatic checkout/webhook is not required for beta, but remains a blocker for fully automated public paid checkout.
- Full public A1 release still needs the remaining 8 A1 lessons audio-ready (text is complete for all 40).
- Full multi-level release needs A2-C1 audio generated and lessons published; all four levels are text-ready but unpublished.
- A1 Real Exam needs listening audio generated for its items and at least one full QA pass (start → answer all sections → submit → admin review → published result) before exposing it to users.
- Conversation Coach supports turn-based recorded-audio STT (Whisper via Together by default, AssemblyAI optional) and LLM feedback with deterministic fallback. Verify production AI configuration through `GET /api/admin/ai/status` and `POST /api/admin/ai/test-llm`. Exam speaking uploads are auto-transcribed (best-effort) so admin review shows a transcript next to the audio; official fully-automated speaking assessment remains future work.
- Admin CMS is file-backed for controlled beta. Full production CMS still needs media/audio asset upload, automated TTS publishing, and draft review workflow before multi-editor editorial operations.
- Production database should use PostgreSQL via `DATABASE_URL`, not local SQLite.
- Configure production env from `.env.production.example` with real non-placeholder values and verify `APP_ENV=production` starts only with PostgreSQL, HTTPS URLs, explicit CORS, a strong JWT secret, Google OAuth credentials, admin payment key, and Resend key.
- Configure external uptime monitoring, error tracking, and edge/WAF rate limiting before public paid traffic.

## Release Policy

Treat the current build as an MVP beta candidate. It is suitable for controlled QA and product demos after all verification commands pass. Public paid release should wait until the production blockers above are closed.
