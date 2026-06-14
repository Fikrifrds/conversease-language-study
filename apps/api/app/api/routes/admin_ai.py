"""Admin AI diagnostics.

Lets operators verify from production which AI integrations are active:
LLM feedback (Conversation Coach), speech-to-text, and TTS. Mirrors the
admin email diagnostics pattern.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.admin_deps import require_admin_api_key
from app.core.config import settings
from app.core.llm_usage import llm_usage_registry
from app.domain.ai import TASK_MODEL_CONFIGS, ChatMessage
from app.services.llm import LLMError, get_llm_provider

router = APIRouter()


@router.get("/admin/ai/status")
async def get_ai_status(_: bool = Depends(require_admin_api_key)) -> dict:
    """Report which AI providers are configured (no external calls)."""
    llm_provider = get_llm_provider()
    stt_configured = (
        bool(settings.assemblyai_api_key)
        if settings.stt_provider == "assemblyai"
        else bool(settings.together_api_key)
    )
    return {
        "data": {
            "llm": {
                "configured": llm_provider is not None,
                "provider": settings.llm_default_provider,
                "feedback_model": TASK_MODEL_CONFIGS["conversation_feedback"].model,
                "partner_model": TASK_MODEL_CONFIGS["conversation_partner_reply"].model,
            },
            "stt": {
                "configured": stt_configured,
                "provider": settings.stt_provider,
            },
            "tts": {
                "configured": bool(settings.minimax_api_key),
                "provider": "minimax",
            },
        }
    }


@router.post("/admin/ai/test-llm")
async def test_llm_completion(_: bool = Depends(require_admin_api_key)) -> dict:
    """Run one tiny live completion to prove the LLM provider works end to end."""
    provider = get_llm_provider()
    if provider is None:
        raise HTTPException(status_code=503, detail="llm_not_configured")

    try:
        result = await provider.generate_chat_completion(
            messages=[
                ChatMessage(role="system", content="Reply with exactly: OK"),
                ChatMessage(role="user", content="Health check"),
            ],
            model_config=TASK_MODEL_CONFIGS["conversation_feedback"],
        )
    except LLMError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {
        "data": {
            "provider": settings.llm_default_provider,
            "model": TASK_MODEL_CONFIGS["conversation_feedback"].model,
            "output": result.content.strip()[:200],
        }
    }


@router.get("/admin/ai/usage")
async def get_ai_usage(_: bool = Depends(require_admin_api_key)) -> dict:
    """Aggregated LLM token usage and estimated cost since the process started.

    In-memory and per-process (resets on restart); for live cost visibility.
    """
    return {"data": llm_usage_registry.snapshot()}
