from __future__ import annotations

import argparse
import asyncio
from typing import Any

from app.db.session import SessionLocal
from app.repositories.audio_voice_previews import DEFAULT_VOICE_PREVIEW_SAMPLE_TEXT
from app.services.audio_generation import AudioGenerationError, audio_generation_settings
from app.services.audio_preview_cache import get_or_generate_voice_preview


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate cached MiniMax voice preview audio.")
    parser.add_argument("--model", default=None, help="MiniMax TTS model. Defaults to API env setting.")
    parser.add_argument("--speed", type=float, default=1.0, help="Voice speed, 0.5 to 2.0.")
    parser.add_argument(
        "--voice-id",
        action="append",
        default=[],
        help="Specific voice_id to generate. Repeatable. Defaults to every available voice.",
    )
    parser.add_argument("--sample-text", default=DEFAULT_VOICE_PREVIEW_SAMPLE_TEXT)
    parser.add_argument("--generated-by", default="system")
    parser.add_argument("--force", action="store_true", help="Regenerate even if a cached preview exists.")
    parser.add_argument("--limit", type=int, default=0, help="Optional max number of voices for smoke tests.")
    parser.add_argument("--stop-on-error", action="store_true", help="Stop as soon as one voice fails.")
    return parser.parse_args()


async def main() -> int:
    args = parse_args()
    settings_payload = await audio_generation_settings()
    voices = selected_voices(settings_payload.get("voices", []), voice_ids=args.voice_id)
    if args.limit > 0:
        voices = voices[: args.limit]

    if not voices:
        print("No voices found.")
        return 1

    generated_count = 0
    cached_count = 0
    failures: list[tuple[str, str]] = []

    with SessionLocal() as db:
        for index, voice in enumerate(voices, start=1):
            voice_id = str(voice.get("voice_id") or "").strip()
            if not voice_id:
                continue
            try:
                preview = await get_or_generate_voice_preview(
                    db,
                    model=args.model,
                    voice_id=voice_id,
                    speed=args.speed,
                    sample_text=args.sample_text,
                    generated_by=args.generated_by,
                    force=args.force,
                )
            except AudioGenerationError as exc:
                failures.append((voice_id, str(exc)))
                print(f"[{index}/{len(voices)}] failed {voice_id}: {exc}")
                if args.stop_on_error:
                    break
                continue

            if preview.get("cached"):
                cached_count += 1
                status = "cached"
            else:
                generated_count += 1
                status = "generated"
            print(f"[{index}/{len(voices)}] {status} {voice_id} -> {preview['object_key']}")

    print(
        "Done. "
        f"generated={generated_count} cached={cached_count} failed={len(failures)} total={len(voices)}"
    )
    return 1 if failures else 0


def selected_voices(voices: list[dict[str, Any]], *, voice_ids: list[str]) -> list[dict[str, Any]]:
    wanted = {voice_id.strip() for voice_id in voice_ids if voice_id.strip()}
    if not wanted:
        return voices
    return [voice for voice in voices if str(voice.get("voice_id") or "").strip() in wanted]


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
