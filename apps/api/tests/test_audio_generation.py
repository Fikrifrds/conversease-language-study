import io
import tempfile
import unittest
import wave
from array import array
from pathlib import Path
from unittest.mock import patch

from app.data.curriculum import curriculum_root
from app.services.audio_generation import (
    CURATED_MINIMAX_VOICE_IDS,
    ELEVENLABS_ARABIC_FEMALE_DIALOGUE_VOICES,
    ELEVENLABS_ARABIC_MALE_DIALOGUE_VOICES,
    ELEVENLABS_ARABIC_VOICE_METADATA,
    ENGLISH_CURATED_MINIMAX_VOICE_IDS,
    FALLBACK_MINIMAX_VOICES,
    TTS_PROVIDER_ELEVENLABS,
    TTS_PROVIDER_MINIMAX,
    LessonAudioReference,
    MiniMaxAudioResult,
    assign_elevenlabs_dialogue_voices,
    assign_dialogue_voices,
    concatenate_pcm16_audio,
    concatenate_wav_audio,
    default_tts_provider_for_language,
    filter_voice_options,
    infer_speaker_gender,
    infer_voice_gender,
    listening_script_to_dialogue_turns,
    listening_script_to_tts_text,
    naturalize_dialogue_turn_text,
    synthesize_dialogue_elevenlabs_tts,
    synthesize_dialogue_minimax_tts,
    update_production_tracker_audio,
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

    def test_dialogue_parser_extracts_trailing_scene_pause(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "listening_script.md"
            path.write_text(
                "# Dialogue Script\n\n"
                "**Khalid:** شكرًا. سأذهب إلى المقهى. <#0.9#>\n"
                "**Cafe Staff:** مرحبًا، ماذا تريد؟\n",
                encoding="utf-8",
            )

            turns = listening_script_to_dialogue_turns(path)

            self.assertEqual([turn.speaker for turn in turns], ["Khalid", "Cafe Staff"])
            self.assertEqual(turns[0].text, "شكرًا. سأذهب إلى المقهى.")
            self.assertEqual(turns[0].pause_after_seconds, 0.9)
            self.assertEqual(turns[1].pause_after_seconds, 0.0)

    def test_naturalize_dialogue_turn_keeps_meaningful_colon_text(self):
        text = "بَرِيدِي الْإِلِكْتُرُونِيُّ: أَحْمَدُ نُقْطَةٌ وَاحِدٌ."

        self.assertEqual(naturalize_dialogue_turn_text(text), text)

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
        self.assertEqual(voices["Sara"], "English_CalmWoman")
        self.assertEqual(voices["Mina"], "English_Upbeat_Woman")
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

    def test_dialogue_voice_assignment_keeps_raka_male(self):
        turns = [
            _turn("Nina", "Hello. What's your name?"),
            _turn("Raka", "My name is Raka."),
            _turn("Nina", "Sorry, can you repeat that?"),
            _turn("Raka", "Raka. R-A-K-A."),
        ]

        voices = assign_dialogue_voices(turns, fallback_voice_id="English_expressive_narrator")

        self.assertEqual(voices["Nina"], "English_Upbeat_Woman")
        self.assertEqual(voices["Raka"], "English_Gentle-voiced_man")
        self.assertNotIn(voices["Raka"], {"English_radiant_girl", "English_Graceful_Lady", "English_CalmWoman"})

    def test_dialogue_voice_assignment_keeps_unit_one_personas_gendered(self):
        turns = [
            _turn("Lina", "Hi, my name is Lina."),
            _turn("Adi", "Hi Lina. I'm Adi."),
            _turn("Maya", "Hi, I'm Maya."),
            _turn("Omar", "Nice to meet you, Maya."),
            _turn("Nina", "Hello. What's your name?"),
            _turn("Raka", "My name is Raka."),
            _turn("Sara", "Hi, my name is Sara."),
        ]

        voices = assign_dialogue_voices(turns, fallback_voice_id="English_expressive_narrator")

        self.assertEqual(voices["Lina"], "English_Upbeat_Woman")
        self.assertEqual(voices["Adi"], "English_Diligent_Man")
        self.assertEqual(voices["Maya"], "English_radiant_girl")
        self.assertEqual(voices["Omar"], "English_Trustworth_Man")
        self.assertEqual(voices["Nina"], "English_Upbeat_Woman")
        self.assertEqual(voices["Raka"], "English_Gentle-voiced_man")
        self.assertEqual(voices["Sara"], "English_CalmWoman")

    def test_a1_dialogue_speakers_keep_expected_voice_gender(self):
        for script_path in sorted((curriculum_root() / "english" / "A1" / "units").glob("*/*/listening_script.md")):
            turns = listening_script_to_dialogue_turns(script_path)
            voices = assign_dialogue_voices(turns, fallback_voice_id="English_expressive_narrator")

            for speaker, voice_id in voices.items():
                expected_gender = infer_speaker_gender(speaker)
                if expected_gender == "unknown":
                    continue

                with self.subTest(script=str(script_path), speaker=speaker):
                    self.assertEqual(
                        infer_voice_gender(voice_id=voice_id),
                        expected_gender,
                    )

    def test_arabic_dialogue_voice_assignment_uses_arabic_pool_for_unknown_speakers(self):
        turns = [
            _turn("Ustadh", "مرحبا."),
            _turn("Khalid", "أنا خالد."),
            _turn("Noura", "أنا من إندونيسيا."),
        ]

        voices = assign_dialogue_voices(
            turns,
            fallback_voice_id="Arabic_FriendlyGuy",
            language="arabic",
        )

        self.assertEqual(voices["Ustadh"], "Arabic_FriendlyGuy")
        self.assertEqual(voices["Khalid"], "Arabic_FriendlyGuy")
        self.assertEqual(voices["Noura"], "Arabic_CalmWoman")

    def test_arabic_dialogue_voice_assignment_keeps_staff_roles_arabic(self):
        turns = [
            _turn("Khalid", "أين المقهى؟"),
            _turn("Cafe Staff", "ماذا تريد؟"),
            _turn("Shopkeeper", "السعر خمسة ريالات."),
        ]

        voices = assign_dialogue_voices(
            turns,
            fallback_voice_id="Arabic_FriendlyGuy",
            language="arabic",
        )

        self.assertEqual(voices["Khalid"], "Arabic_FriendlyGuy")
        self.assertEqual(voices["Cafe Staff"], "Arabic_CalmWoman")
        self.assertEqual(voices["Shopkeeper"], "Arabic_FriendlyGuy")

    def test_arabic_defaults_to_elevenlabs_provider(self):
        self.assertEqual(default_tts_provider_for_language("arabic"), TTS_PROVIDER_ELEVENLABS)
        self.assertEqual(default_tts_provider_for_language("english"), TTS_PROVIDER_MINIMAX)

    def test_elevenlabs_arabic_dialogue_voice_assignment_uses_configured_gender_voices(self):
        turns = [
            _turn("Khalid", "مرحبا."),
            _turn("Noura", "أهلا."),
        ]

        voices = assign_elevenlabs_dialogue_voices(
            turns,
            fallback_voice_id="fallback-voice",
            language="arabic",
        )

        self.assertEqual(voices["Khalid"], "t9akNmCDhz230CEXOYmn")
        self.assertEqual(voices["Noura"], "kdUY91gH5xyDHapxlthT")

    def test_elevenlabs_arabic_teacher_and_student_do_not_share_voice(self):
        turns = [
            _turn("Muallim", "السلام عليكم."),
            _turn("Ahmad", "وعليكم السلام."),
        ]

        voices = assign_elevenlabs_dialogue_voices(
            turns,
            fallback_voice_id="3nav5pHC1EYvWOd5LmnA",
            language="arabic",
        )

        self.assertEqual(voices["Muallim"], "3nav5pHC1EYvWOd5LmnA")
        self.assertEqual(voices["Ahmad"], "RjFuvnufLX42TYe37ekK")
        self.assertNotEqual(voices["Muallim"], voices["Ahmad"])

    def test_elevenlabs_arabic_persona_collision_uses_another_male_voice(self):
        turns = [
            _turn("Muallim", "السلام عليكم."),
            _turn("Ustadh", "أهلا وسهلا."),
        ]

        voices = assign_elevenlabs_dialogue_voices(
            turns,
            fallback_voice_id="3nav5pHC1EYvWOd5LmnA",
            language="arabic",
        )

        self.assertNotEqual(voices["Muallim"], voices["Ustadh"])
        self.assertIn(voices["Ustadh"], ELEVENLABS_ARABIC_MALE_DIALOGUE_VOICES)

    def test_elevenlabs_arabic_unknown_speakers_keep_gendered_voice_pool(self):
        turns = [
            _turn("Female", "أهلا."),
            _turn("Male", "مرحبا."),
        ]

        voices = assign_elevenlabs_dialogue_voices(
            turns,
            fallback_voice_id="3nav5pHC1EYvWOd5LmnA",
            language="arabic",
        )

        self.assertIn(voices["Female"], ELEVENLABS_ARABIC_FEMALE_DIALOGUE_VOICES)
        self.assertIn(voices["Male"], ELEVENLABS_ARABIC_MALE_DIALOGUE_VOICES)

    def test_elevenlabs_arabic_staff_roles_use_role_specific_voices(self):
        turns = [
            _turn("Khalid", "أين المقهى؟"),
            _turn("Layla", "المقهى بجانب المكتبة."),
            _turn("Cafe Staff", "ماذا تريد؟"),
            _turn("Shopkeeper", "السعر خمسة ريالات."),
        ]

        voices = assign_elevenlabs_dialogue_voices(
            turns,
            fallback_voice_id="3nav5pHC1EYvWOd5LmnA",
            language="arabic",
        )

        self.assertEqual(voices["Khalid"], "t9akNmCDhz230CEXOYmn")
        self.assertEqual(voices["Layla"], "kdUY91gH5xyDHapxlthT")
        self.assertEqual(voices["Cafe Staff"], "gVzwmdZzRgBrNjXaTmi5")
        self.assertEqual(voices["Shopkeeper"], "3GnbqfjaW8xI6hRTVx4Y")

    def test_elevenlabs_arabic_uses_only_curated_gendered_voices(self):
        turns = [
            _turn("Muallim", "مرحبا."),
            _turn("Ahmad", "أهلا."),
            _turn("Fatimah", "أنا جاهزة."),
            _turn("Noura", "وأنا أيضا."),
        ]

        voices = assign_elevenlabs_dialogue_voices(
            turns,
            fallback_voice_id="legacy-non-curated-voice",
            language="arabic",
        )

        self.assertEqual(len(set(voices.values())), len(voices))
        for speaker in ("Muallim", "Ahmad"):
            self.assertIn(voices[speaker], ELEVENLABS_ARABIC_MALE_DIALOGUE_VOICES)
            self.assertEqual(ELEVENLABS_ARABIC_VOICE_METADATA[voices[speaker]]["gender"], "male")
        for speaker in ("Fatimah", "Noura"):
            self.assertIn(voices[speaker], ELEVENLABS_ARABIC_FEMALE_DIALOGUE_VOICES)
            self.assertEqual(ELEVENLABS_ARABIC_VOICE_METADATA[voices[speaker]]["gender"], "female")

    def test_arabic_a1_a2_dialogue_speakers_have_explicit_gendered_elevenlabs_voices(self):
        for level_code in ("A1", "A2"):
            root = curriculum_root() / "arabic" / level_code / "units"
            for script_path in sorted(root.glob("*/*/listening_script.md")):
                turns = listening_script_to_dialogue_turns(script_path)
                voices = assign_elevenlabs_dialogue_voices(
                    turns,
                    fallback_voice_id="3nav5pHC1EYvWOd5LmnA",
                    language="arabic",
                )

                for speaker, voice_id in voices.items():
                    expected_gender = infer_speaker_gender(speaker)
                    with self.subTest(level=level_code, script=str(script_path), speaker=speaker):
                        self.assertIn(expected_gender, {"male", "female"})
                        self.assertEqual(
                            ELEVENLABS_ARABIC_VOICE_METADATA[voice_id]["gender"],
                            expected_gender,
                        )

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

    def test_voice_options_are_limited_to_curated_solid_set(self):
        noisy_minimax_result = [
            {"voice_id": "English_SlowQuietVoice", "voice_name": "Slow Quiet Voice", "category": "system"},
            {"voice_id": "custom_loud_but_unreviewed", "voice_name": "Custom Voice", "category": "voice_cloning"},
            {"voice_id": "English_Gentle-voiced_man", "voice_name": "Gentle-voiced Man", "category": "system"},
            {"voice_id": "English_CalmWoman", "voice_name": "Calm Woman", "category": "system"},
        ]

        voices = filter_voice_options(noisy_minimax_result, language="English")

        self.assertEqual([voice["voice_id"] for voice in voices], list(ENGLISH_CURATED_MINIMAX_VOICE_IDS))
        self.assertTrue(all(voice["category"] == "curated" for voice in voices))
        self.assertNotIn("English_SlowQuietVoice", {voice["voice_id"] for voice in voices})
        self.assertNotIn("custom_loud_but_unreviewed", {voice["voice_id"] for voice in voices})

    def test_fallback_voices_match_curated_solid_set(self):
        self.assertEqual(
            [voice["voice_id"] for voice in FALLBACK_MINIMAX_VOICES],
            list(CURATED_MINIMAX_VOICE_IDS),
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

    def test_concatenate_wav_audio_uses_scene_pause_override(self):
        first = wav_chunk(frame_count=320)
        second = wav_chunk(frame_count=320)

        audio_bytes, duration = concatenate_wav_audio(
            [first, second],
            pause_seconds=0.1,
            pause_after_seconds=[0.9, 0],
        )

        with wave.open(io.BytesIO(audio_bytes), "rb") as reader:
            self.assertEqual(reader.getnframes(), 29440)
        self.assertAlmostEqual(duration, 0.92, places=2)

    def test_concatenate_wav_audio_normalizes_chunk_volume(self):
        quiet = wav_chunk(frame_count=320, amplitude=1000)
        loud = wav_chunk(frame_count=320, amplitude=12000)

        audio_bytes, _ = concatenate_wav_audio([quiet, loud], pause_seconds=0)

        with wave.open(io.BytesIO(audio_bytes), "rb") as reader:
            sample_bytes = reader.readframes(reader.getnframes())

        samples = array("h")
        samples.frombytes(sample_bytes)
        first_peak = max(abs(sample) for sample in samples[:320])
        second_peak = max(abs(sample) for sample in samples[320:640])

        self.assertGreater(first_peak, 25000)
        self.assertGreater(second_peak, 25000)
        self.assertLess(abs(first_peak - second_peak), 4)

    def test_concatenate_pcm16_audio_wraps_dialogue_as_wav_with_pause(self):
        first = pcm_chunk(frame_count=240)
        second = pcm_chunk(frame_count=240)

        audio_bytes, duration = concatenate_pcm16_audio(
            [first, second],
            sample_rate=24000,
            pause_seconds=0.1,
        )

        with wave.open(io.BytesIO(audio_bytes), "rb") as reader:
            self.assertEqual(reader.getnchannels(), 1)
            self.assertEqual(reader.getframerate(), 24000)
            self.assertEqual(reader.getnframes(), 2880)
        self.assertAlmostEqual(duration, 0.12, places=2)

    def test_production_tracker_audio_update_matches_language_prefixed_level(self):
        with tempfile.TemporaryDirectory() as directory:
            tracker_path = Path(directory) / "production_tracker.csv"
            tracker_path.write_text(
                "level,unit,lesson,lesson_md,listening_script,audio_generated,phrases,grammar,"
                "pronunciation,response_prompts,conversation_coach,quiz,reading,writing,review_status,publish_status\n"
                "arabic/A1,unit-01-fusha-foundations,lesson-02-name-and-origin,done,done,not_generated,"
                "done,done,done,done,done,done,done,done,,\n",
                encoding="utf-8",
            )
            lesson = LessonAudioReference(
                language="arabic",
                level_code="A1",
                unit_key="unit-01-fusha-foundations",
                lesson_key="lesson-02-name-and-origin",
                lesson_slug="arabic-name-and-origin",
                title="Name and Origin",
                lesson_dir=Path(directory),
                listening_script_path=Path(directory) / "listening_script.md",
                audio_manifest_path=Path(directory) / "audio_manifest.yaml",
            )

            with patch("app.services.audio_generation.production_tracker_path", return_value=tracker_path):
                update_production_tracker_audio(lesson, status="done")

            self.assertIn(
                "arabic/A1,unit-01-fusha-foundations,lesson-02-name-and-origin,done,done,done",
                tracker_path.read_text(encoding="utf-8"),
            )


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

    async def test_dialogue_synthesis_sends_clean_turn_text_to_elevenlabs(self):
        turns = [
            _turn("Muallim", "Muallim: السلام عليكم."),
            _turn("Ahmad", "اسمي أحمد."),
        ]
        sent_texts: list[str] = []
        sent_voice_ids: list[str] = []

        async def fake_synthesize_elevenlabs_tts(**kwargs):
            sent_texts.append(kwargs["text"])
            sent_voice_ids.append(kwargs["voice_id"])
            audio = pcm_chunk(frame_count=240)
            return MiniMaxAudioResult(
                audio_bytes=audio,
                duration_seconds=0.01,
                audio_format="pcm",
                audio_size=len(audio),
                trace_id=f"trace-{len(sent_texts)}",
                usage_characters=len(kwargs["text"]),
                voice_id=kwargs["voice_id"],
                speaker_voices={},
                line_count=1,
            )

        with patch(
            "app.services.audio_generation.synthesize_elevenlabs_tts",
            side_effect=fake_synthesize_elevenlabs_tts,
        ):
            result = await synthesize_dialogue_elevenlabs_tts(
                turns=turns,
                model="eleven_v3",
                fallback_voice_id="3nav5pHC1EYvWOd5LmnA",
                speed=0.9,
                language="arabic",
            )

        self.assertEqual(sent_texts, ["السلام عليكم.", "اسمي أحمد."])
        self.assertEqual(sent_voice_ids, ["3nav5pHC1EYvWOd5LmnA", "RjFuvnufLX42TYe37ekK"])
        self.assertNotEqual(result.speaker_voices["Muallim"], result.speaker_voices["Ahmad"])
        self.assertEqual(result.audio_format, "wav")
        with wave.open(io.BytesIO(result.audio_bytes), "rb") as reader:
            self.assertEqual(reader.getframerate(), 24000)
            self.assertGreater(reader.getnframes(), 480)


def _turn(speaker: str, text: str):
    from app.services.audio_generation import DialogueTurn

    return DialogueTurn(speaker=speaker, text=text)


def wav_chunk(*, frame_count: int, amplitude: int = 0) -> bytes:
    output = io.BytesIO()
    with wave.open(output, "wb") as writer:
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(32000)
        writer.writeframes(amplitude.to_bytes(2, "little", signed=True) * frame_count)
    return output.getvalue()


def pcm_chunk(*, frame_count: int, amplitude: int = 0) -> bytes:
    return amplitude.to_bytes(2, "little", signed=True) * frame_count


if __name__ == "__main__":
    unittest.main()
