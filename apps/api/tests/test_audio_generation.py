import io
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

from app.services.audio_generation import (
    MiniMaxAudioResult,
    assign_dialogue_voices,
    concatenate_wav_audio,
    infer_voice_gender,
    listening_script_to_dialogue_turns,
    listening_script_to_tts_text,
    synthesize_dialogue_minimax_tts,
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

        self.assertEqual(voices["Alya"], "English_radiant_girl")
        self.assertEqual(voices["Ben"], "English_Gentle-voiced_man")
        self.assertEqual(voices["John"], "English_Trustworth_Man")

    def test_dialogue_voice_assignment_cycles_clear_voice_pool(self):
        turns = [
            _turn("Alya", "Hi."),
            _turn("Sara", "Hello."),
            _turn("Mina", "Good morning."),
            _turn("Ben", "Hi."),
            _turn("John", "Hello."),
            _turn("David", "Good morning."),
        ]

        voices = assign_dialogue_voices(turns, fallback_voice_id="English_expressive_narrator")

        self.assertEqual(voices["Alya"], "English_radiant_girl")
        self.assertEqual(voices["Sara"], "English_Graceful_Lady")
        self.assertEqual(voices["Mina"], "English_compelling_lady1")
        self.assertEqual(voices["Ben"], "English_Gentle-voiced_man")
        self.assertEqual(voices["John"], "English_Trustworth_Man")
        self.assertEqual(voices["David"], "English_Diligent_Man")

    def test_dialogue_voice_assignment_keeps_personas_stable_across_order(self):
        turns = [
            _turn("John", "Good morning."),
            _turn("Ben", "Hello."),
            _turn("Alya", "Hi."),
        ]

        voices = assign_dialogue_voices(turns, fallback_voice_id="English_expressive_narrator")

        self.assertEqual(voices["Alya"], "English_radiant_girl")
        self.assertEqual(voices["Ben"], "English_Gentle-voiced_man")
        self.assertEqual(voices["John"], "English_Trustworth_Man")

    def test_dialogue_voice_assignment_avoids_reusing_voice_for_new_speaker(self):
        turns = [
            _turn("Ben", "Hello."),
            _turn("John", "Good morning."),
            _turn("Daniel", "Nice to meet you."),
        ]

        voices = assign_dialogue_voices(turns, fallback_voice_id="English_expressive_narrator")

        self.assertNotEqual(voices["Daniel"], voices["Ben"])
        self.assertNotEqual(voices["Daniel"], voices["John"])

    def test_dialogue_voice_assignment_keeps_dimas_male(self):
        turns = [
            _turn("Officer", "Hi. What is your name?"),
            _turn("Dimas", "My name is Dimas."),
            _turn("Officer", "How do you spell it?"),
            _turn("Dimas", "D-I-M-A-S."),
        ]

        voices = assign_dialogue_voices(turns, fallback_voice_id="English_expressive_narrator")

        self.assertEqual(voices["Officer"], "English_CalmWoman")
        self.assertEqual(voices["Dimas"], "English_Diligent_Man")
        self.assertNotIn(voices["Dimas"], {"English_radiant_girl", "English_Graceful_Lady"})

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


class AudioGenerationPayloadTest(unittest.IsolatedAsyncioTestCase):
    async def test_dialogue_synthesis_sends_exact_turn_text_to_minimax(self):
        turns = [
            _turn("Alya", "Hi, good morning."),
            _turn("Ben", "Good morning. How are you?"),
            _turn("Alya", "I'm good, thank you."),
        ]
        sent_texts: list[str] = []

        async def fake_synthesize_minimax_tts(**kwargs):
            sent_texts.append(kwargs["text"])
            audio = wav_chunk(frame_count=320)
            return MiniMaxAudioResult(
                audio_bytes=audio,
                duration_seconds=0.01,
                audio_format="wav",
                audio_size=len(audio),
                trace_id=f"trace-{len(sent_texts)}",
                usage_characters=len(kwargs["text"]),
                voice_id=kwargs["voice_id"],
                speaker_voices={},
                line_count=1,
            )

        with patch(
            "app.services.audio_generation.synthesize_minimax_tts",
            side_effect=fake_synthesize_minimax_tts,
        ):
            result = await synthesize_dialogue_minimax_tts(
                turns=turns,
                model="speech-2.8-hd",
                fallback_voice_id="English_expressive_narrator",
                speed=1,
                language_boost="English",
            )

        self.assertEqual(
            sent_texts,
            [
                "Hi, good morning.",
                "Good morning. How are you?",
                "I'm good, thank you.",
            ],
        )
        self.assertEqual(result.line_count, 3)
        self.assertEqual(result.voice_id, "multi_speaker")


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
