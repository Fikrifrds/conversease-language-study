# Conversease Worker

Background job responsibilities:

- `process_speech_transcription`
- `generate_conversation_feedback`
- `generate_tts_audio`
- `send_email_job`
- `process_resend_webhook`
- `subscription_expiry_checker`
- `minutes_low_checker`
- `weekly_progress_email`
- `level_test_reminder_checker`
- `payment_webhook_processor`

The first API slice exposes the domain boundaries these jobs will call. Celery or RQ can be wired here after database models and queues are introduced.

