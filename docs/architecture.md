# Conversease Architecture

## Product Loop

Every lesson should lead users through:

```txt
Listen -> Understand -> Repeat -> Respond -> Converse -> Get Feedback -> Improve
```

The MVP implementation is split into a Next.js frontend, a FastAPI backend, and a background worker layer. Integrations are provider-oriented so Conversease can start with manual transfer, Resend, Together AI, AssemblyAI, MiniMax Audio, and later Midtrans without hardcoding those vendors into product workflows.

## Monorepo

```txt
apps/
  web/      Next.js product UI
  api/      FastAPI backend and domain services
  worker/   Async jobs for email, STT, TTS, reminders, payments
packages/
  shared/   Shared constants and typed contracts
content/
  curriculum/
  email_templates/
infra/
  nginx/
docs/
```

## Backend Boundaries

- `app/domain`: pure business logic and interfaces. These modules should stay unit-testable without external services.
- `app/services`: orchestration across providers, repositories, jobs, and domain rules.
- `app/api`: HTTP route adapters.
- `app/data`: file-backed curriculum, email templates, and controlled-beta CMS editing services.
- `app/providers`: concrete vendor clients.

## First Milestones

1. Ship public pages and a read-only learning experience for A1 Unit 1 Lesson 1.
2. Add auth and onboarding persistence.
3. Add database models and migrations.
4. Implement Conversation Coach turn flow with typed answers and recorded-audio STT.
5. Implement manual-transfer billing, Resend admin notifications, and later Midtrans payment activation.
