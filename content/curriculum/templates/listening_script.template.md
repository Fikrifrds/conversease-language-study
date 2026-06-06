# Dialogue Script

<!--
Each line: **Speaker:** spoken text
- 5-8 turns for A1. One speaker per line; never two lines from the same speaker
  in a row (merge them into one line instead).
- Speaker names drive the audio voice. Reuse existing character names so voices
  stay consistent (see DIALOGUE_PERSONA_VOICES in
  apps/api/app/services/audio_generation.py). Recurring generic roles like
  Staff / Officer must be added to that registry with an explicit voice.
- Keep dialogue coherent: no abrupt topic jumps; a character must not switch
  roles illogically (a passer-by who gives directions is NOT the cafe cashier —
  use a separate speaker). Connect scenes with a transition line and/or a pause.

OPTIONAL audio expressiveness (model speech-2.8-hd only), use 1-2 per dialogue:
- Interjection tags: (laughs), (chuckle), (breath), (sighs), ... inside the text.
- Pause control: <#0.8#> (seconds) between speakable segments, e.g. a scene change.
These tags are AUDIO-ONLY and are stripped automatically before display.

IMPORTANT: transcript_translation.md must have the SAME number of lines, in the
SAME order. After editing, regenerate the web data:
  PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_web_lesson_data.py
-->

**SpeakerA:** First English line.
**SpeakerB:** Reply in English.
**SpeakerA:** Next English line.

## Audio Direction

- Level: A1
- Speed: slow and natural
- Tone: friendly, clear, supportive
- Voices: <describe each speaker, e.g. female staff, male learner>
