from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from app.core.config import settings


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    model: str
    temperature: float
    max_tokens: int


@dataclass(frozen=True)
class LLMResult:
    content: str
    raw: Optional[Dict[str, Any]] = None


class LLMProvider(ABC):
    @abstractmethod
    async def generate_chat_completion(
        self,
        messages: List[ChatMessage],
        model_config: ModelConfig,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> LLMResult:
        raise NotImplementedError


DEFAULT_TOGETHER_CHAT_MODEL = settings.together_chat_model


TASK_MODEL_CONFIGS = {
    "conversation_coach_reply": ModelConfig(
        provider="together",
        model=DEFAULT_TOGETHER_CHAT_MODEL,
        temperature=0.7,
        max_tokens=800,
    ),
    "conversation_feedback": ModelConfig(
        provider="together",
        model=DEFAULT_TOGETHER_CHAT_MODEL,
        temperature=0.2,
        max_tokens=1200,
    ),
    "level_evaluation_grading": ModelConfig(
        provider="together",
        model=DEFAULT_TOGETHER_CHAT_MODEL,
        temperature=0.1,
        max_tokens=2000,
    ),
}
