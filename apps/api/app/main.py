from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    admin_ai,
    admin_cms,
    admin_users,
    auth,
    billing,
    conversation,
    conversation_partner,
    email,
    exam_runner,
    exams,
    health,
    learning,
)
from app.core.config import settings
from app.core.observability import (
    RequestContextMiddleware,
    configure_logging,
    unhandled_exception_handler,
)
from app.core.rate_limit import RateLimitMiddleware


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="Conversease API",
        version=settings.release_version,
        description="Conversation-first English learning platform API.",
    )

    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(learning.router, prefix="/api", tags=["learning"])
    app.include_router(conversation.router, prefix="/api", tags=["conversation"])
    app.include_router(conversation_partner.router, prefix="/api", tags=["conversation-partner"])
    app.include_router(billing.router, prefix="/api", tags=["billing"])
    app.include_router(admin_ai.router, prefix="/api", tags=["admin-ai"])
    app.include_router(admin_cms.router, prefix="/api", tags=["admin-cms"])
    app.include_router(admin_users.router, prefix="/api", tags=["admin-users"])
    app.include_router(email.router, prefix="/api", tags=["email"])
    app.include_router(exams.router, prefix="/api", tags=["exams"])
    app.include_router(exam_runner.router, prefix="/api", tags=["exam-runner"])
    return app


app = create_app()
