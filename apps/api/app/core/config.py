from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


API_ROOT = Path(__file__).resolve().parents[2]


def is_placeholder_value(value: str) -> bool:
    normalized = value.strip().lower()
    if not normalized:
        return False

    return (
        normalized.startswith("replace-with")
        or (normalized.startswith("<") and normalized.endswith(">"))
        or normalized in {"changeme", "change-me", "placeholder", "todo"}
    )


class Settings(BaseSettings):
    release_version: str = "dev"
    app_env: str = "development"
    log_level: str = "INFO"
    enable_request_logging: bool = True
    public_app_url: str = "http://localhost:3000"
    api_base_url: str = "http://localhost:8000"
    database_url: str = f"sqlite:///{API_ROOT / 'conversease_dev.db'}"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "dev-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7
    email_verification_token_expire_hours: int = 24
    password_reset_token_expire_minutes: int = 60
    google_oauth_client_id: str = ""
    google_oauth_client_secret: str = ""
    google_oauth_redirect_uri: str = ""
    admin_emails_raw: str = ""
    llm_default_provider: str = "together"
    email_from: str = "Conversease <no-reply@mail.conversease.com>"
    email_reply_to: str = "support@conversease.com"
    cors_origins_raw: str = "http://localhost:3000"
    midtrans_server_key: str = ""
    midtrans_client_key: str = ""
    midtrans_is_production: bool = False
    payment_admin_email: str = "denahku.team@gmail.com"
    payment_admin_api_key: str = ""
    manual_transfer_bank_name: str = "Bank Jago"
    manual_transfer_account_number: str = "5001 6527 8492"
    manual_transfer_account_holder: str = "Fikri Firdaus"
    manual_transfer_unique_code_min: int = 101
    manual_transfer_unique_code_max: int = 999
    manual_transfer_expire_hours: int = 12
    resend_api_key: str = ""
    together_api_key: str = ""
    together_api_base_url: str = "https://api.together.xyz"
    together_chat_model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    together_partner_chat_model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    together_timeout_seconds: int = 30
    stt_provider: str = "whisper_together"
    whisper_model: str = "openai/whisper-large-v3"
    whisper_language: str = "en"
    whisper_timeout_seconds: int = 60
    whisper_max_audio_bytes: int = 15 * 1024 * 1024
    assemblyai_api_key: str = ""
    assemblyai_api_base_url: str = "https://api.assemblyai.com"
    assemblyai_speech_models_raw: str = "universal-3-pro,universal-2"
    assemblyai_transcript_timeout_seconds: int = 60
    assemblyai_poll_interval_seconds: float = 1.5
    assemblyai_max_audio_bytes: int = 15 * 1024 * 1024
    minimax_api_key: str = ""
    minimax_api_base_url: str = "https://api.minimax.io"
    minimax_tts_model: str = "speech-2.8-hd"
    minimax_tts_voice_id: str = "English_expressive_narrator"
    minimax_tts_language_boost: str = "English"
    minimax_tts_timeout_seconds: int = 90
    s3_bucket: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "ap-southeast-1"
    s3_public_base_url: str = ""
    s3_presigned_url_expires_seconds: int = 3600
    rate_limit_enabled: bool = True
    rate_limit_window_seconds: int = 60
    auth_rate_limit_requests: int = 30
    admin_rate_limit_requests: int = 120

    model_config = SettingsConfigDict(env_file=(".env", ".env.local"), extra="ignore")

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]

    @property
    def admin_emails(self) -> List[str]:
        return [email.strip().lower() for email in self.admin_emails_raw.split(",") if email.strip()]

    @property
    def assemblyai_speech_models(self) -> List[str]:
        return [model.strip() for model in self.assemblyai_speech_models_raw.split(",") if model.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if not self.is_production:
            return self

        errors = []

        if self.database_url.startswith("sqlite"):
            errors.append("DATABASE_URL must use PostgreSQL in production")

        if self.jwt_secret == "dev-secret" or len(self.jwt_secret) < 32:
            errors.append("JWT_SECRET must be set to a strong value with at least 32 characters")
        elif is_placeholder_value(self.jwt_secret):
            errors.append("JWT_SECRET must not use a placeholder value")

        if not self.cors_origins or any(origin.startswith("http://localhost") for origin in self.cors_origins):
            errors.append("CORS_ORIGINS_RAW must contain explicit production origins")

        if not self.public_app_url.startswith("https://"):
            errors.append("PUBLIC_APP_URL must use https in production")

        if not self.api_base_url.startswith("https://"):
            errors.append("API_BASE_URL must use https in production")

        if not self.release_version or self.release_version == "dev":
            errors.append("RELEASE_VERSION must be set in production")

        if not self.google_oauth_client_id or not self.google_oauth_client_secret:
            errors.append("Google OAuth credentials must be set in production")
        elif is_placeholder_value(self.google_oauth_client_id) or is_placeholder_value(
            self.google_oauth_client_secret
        ):
            errors.append("Google OAuth credentials must not use placeholder values")

        if self.google_oauth_redirect_uri and not self.google_oauth_redirect_uri.startswith("https://"):
            errors.append("GOOGLE_OAUTH_REDIRECT_URI must use https in production")

        if not self.payment_admin_api_key or len(self.payment_admin_api_key) < 24:
            errors.append("PAYMENT_ADMIN_API_KEY must be set to at least 24 characters")
        elif is_placeholder_value(self.payment_admin_api_key):
            errors.append("PAYMENT_ADMIN_API_KEY must not use a placeholder value")

        if not self.payment_admin_email:
            errors.append("PAYMENT_ADMIN_EMAIL must be set in production")

        if not self.resend_api_key:
            errors.append("RESEND_API_KEY must be set in production for payment confirmations")
        elif is_placeholder_value(self.resend_api_key):
            errors.append("RESEND_API_KEY must not use a placeholder value")

        if (
            not self.manual_transfer_bank_name
            or not self.manual_transfer_account_number
            or not self.manual_transfer_account_holder
        ):
            errors.append("Manual transfer bank details must be set in production")

        if self.manual_transfer_unique_code_min < 1:
            errors.append("MANUAL_TRANSFER_UNIQUE_CODE_MIN must be positive")

        if self.manual_transfer_unique_code_max > 999:
            errors.append("MANUAL_TRANSFER_UNIQUE_CODE_MAX must be at most 999")

        if self.manual_transfer_unique_code_min >= self.manual_transfer_unique_code_max:
            errors.append("MANUAL_TRANSFER_UNIQUE_CODE_MIN must be lower than max")

        if self.manual_transfer_expire_hours < 1:
            errors.append("MANUAL_TRANSFER_EXPIRE_HOURS must be positive")

        if self.rate_limit_enabled and self.rate_limit_window_seconds < 1:
            errors.append("RATE_LIMIT_WINDOW_SECONDS must be positive")

        if self.rate_limit_enabled and self.auth_rate_limit_requests < 1:
            errors.append("AUTH_RATE_LIMIT_REQUESTS must be positive")

        if self.rate_limit_enabled and self.admin_rate_limit_requests < 1:
            errors.append("ADMIN_RATE_LIMIT_REQUESTS must be positive")

        if errors:
            raise ValueError("; ".join(errors))

        return self


def validate_settings_for_startup() -> None:
    get_settings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
