# Implementation Status

## Current Release Candidate Scope

- Monorepo scaffold for web, API, worker, shared package, content, infra, and docs.
- Next.js product shell and release-candidate pages:
  - Landing
  - Login
  - Register
  - Forgot password
  - Reset password
  - Verify email
  - Onboarding
  - Dashboard
  - Courses
  - Course detail
  - Lesson detail
  - Conversation Coach
  - Progress
  - A1 final test
  - Pricing
  - Billing
  - Admin payment approval
  - Admin CMS
  - Admin A1 test review
  - Settings
- Brand assets: transparent logo PNG, favicon, and object-only realistic hero image.
- FastAPI routes for health, auth, learning, level tests, conversation practice, billing/access, email, admin payment approval, admin CMS, and admin level-test review.
- API observability middleware with request IDs, structured logs, security headers, and in-memory runtime metrics.
- Next.js web security headers for content type sniffing, framing, referrer policy, and browser permissions.
- API rate limiting for sensitive auth and admin endpoints.
- File-based Alembic migrations through `202606030009`.
- Persistent database-backed flows:
  - Google OAuth login with one-time callback session token
  - Email/password auth with email verification and reset password tokens
  - Authenticated Conversation Coach sessions with lesson-specific A1 roleplay scripts
  - Onboarding profile
  - Lesson progress
  - Subscription access
  - Manual-transfer payment order records with unique code confirmation and admin approval UI
  - Conversation Coach minute ledger
  - A1 final test attempts, submitted reports, and admin-reviewed official reports
- Unit 1 A1 curriculum with 5 published lessons loaded from `content/curriculum` YAML files.
- Published A1 lessons include listening scripts, transcript translations, conversation goals, grammar notes, pronunciation drills, reading support, writing support, quizzes, roleplay configs, and production tracker rows for release auditing.
- Published A1 final conversation test with weighted skill sections, task prompts, readiness preview scoring, persisted submitted reports, and admin manual review for beta official scores.
- Curriculum release validation via `scripts/validate_curriculum.py`, including published lesson support files and `content/production_tracker.csv`.
- Production release preflight via `scripts/release_preflight.py` for API/web config, DB, migration, curriculum, manual transfer/email, email template rendering, backup tooling, and optional automation readiness.
- Post-deploy HTTP smoke checks via `scripts/release_smoke.py` for API/web readiness and admin email diagnostics.
- Admin CMS editing for lesson metadata, roleplay prompts, target phrases, and Markdown email templates, protected by logged-in admin user role, with database-backed content revision audit logs, rollback, and stale edit protection.
- Conversation Coach API feedback and next prompts are aligned to the active lesson slug; the web app uses synced API feedback when available and keeps local fallback for offline/dev resilience.
- Conversation Coach recorded-audio turns using AssemblyAI pre-recorded STT (`universal-3-pro` with `universal-2` fallback), with transcript metadata stored on conversation turns.
- Pure backend domain rules for:
  - A1 evaluation threshold
  - Conversation Coach minute balance and consumption priority
  - Email template rendering and idempotency keys
  - LLM provider interface and task model config
  - Payment provider interface
- Initial Resend email template drafts plus auth/payment email delivery services.
- Admin email diagnostics for template listing, render validation, and sending a Resend test email before beta launch.
- PostgreSQL backup script with checksum, manifest, and restore verification helper.

## Remaining Before Production Integrations

1. Configure production manual-transfer env: Resend key, payment admin key, admin email, and Bank Jago account details.
2. Configure Google OAuth client credentials in the production platform.
3. Replace deterministic Conversation Coach feedback and final-test readiness preview with production AI grading jobs for automated official speaking assessment.
4. Extend Admin CMS for media/audio uploads and draft approval before full editorial production use.
5. Configure external error tracking, uptime checks, and edge/WAF rate limits in the production platform.
6. Add Midtrans checkout/webhook when payment automation is needed beyond manual-transfer beta.
