import io
import tempfile
import unittest
import wave
from pathlib import Path

from app.services.audio_generation import (
    assign_dialogue_voices,
    concatenate_wav_audio,
    infer_voice_gender,
    listening_script_to_dialogue_turns,
    listening_script_to_tts_text,
)


class AudioGenerationTest(unittest.TestCase):
    def test_dialogue_parser_strips_speaker_names_from_tts_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "listening_script.md"
            path.write_text(
                "# Dialogue Script\n\n"
                "**Alya:** Hi, good morning.\n"
                "**Ben:** Good morning. How are you?\n\n"
                "## Audio Direction\n"
                "- Tone: friendly\n",
                encoding="utf-8",
            )

            turns = listening_script_to_dialogue_turns(path)

            self.assertEqual([turn.speaker for turn in turns], ["Alya", "Ben"])
            self.assertEqual([turn.text for turn in turns], ["Hi, good morning.", "Good morning. How are you?"])
            self.assertEqual(listening_script_to_tts_text(path), "Hi, good morning.\nGood morning. How are you?")

    def test_dialogue_voice_assignment_uses_distinct_gendered_voices(self):
        turns = [
            _turn("Alya", "Hi."),
            _turn("Ben", "Hello."),
            _turn("John", "Good morning."),
        ]

        voices = assign_dialogue_voices(turns, fallback_voice_id="English_expressive_narrator")

        self.assertEqual(voices["Alya"], "English_CalmWoman")
        self.assertEqual(voices["Ben"], "English_Trustworth_Man")
        self.assertEqual(voices["John"], "English_magnetic_voiced_man")

    def test_voice_gender_inference_uses_name_id_and_raw_metadata(self):
        self.assertEqual(
            infer_voice_gender(
                voice_id="English_Upbeat_Woman",
                voice_name="Upbeat Woman",
                description="Bright female voice.",
            ),
            "female",
        )
        self.assertEqual(
            infer_voice_gender(
                voice_id="English_Deep_VoicedGentleman",
                voice_name="Deep-voiced Gentleman",
            ),
            "male",
        )
        self.assertEqual(
            infer_voice_gender(
                voice_id="custom_voice",
                voice_name="Custom Voice",
                raw_gender="female",
            ),
            "female",
        )

    def test_concatenate_wav_audio_combines_chunks_with_pause(self):
        first = wav_chunk(frame_count=320)
        second = wav_chunk(frame_count=320)

        audio_bytes, duration = concatenate_wav_audio([first, second], pause_seconds=0.1)

        with wave.open(io.BytesIO(audio_bytes), "rb") as reader:
            self.assertEqual(reader.getnchannels(), 1)
            self.assertEqual(reader.getframerate(), 32000)
            self.assertEqual(reader.getnframes(), 3840)
        self.assertAlmostEqual(duration, 0.12, places=2)


def _turn(speaker: str, text: str):
    from app.services.audio_generation import DialogueTurn

    return DialogueTurn(speaker=speaker, text=text)


def wav_chunk(*, frame_count: int) -> bytes:
    output = io.BytesIO()
    with wave.open(output, "wb") as writer:
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(32000)
        writer.writeframes(b"\x00\x00" * frame_count)
    return output.getvalue()


if __name__ == "__main__":
    unittest.main()
