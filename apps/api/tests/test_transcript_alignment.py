import re
import unittest
from pathlib import Path

from app.services.audio_generation import listening_script_to_dialogue_turns


REPO_ROOT = Path(__file__).resolve().parents[3]
ARABIC_A1_ROOT = REPO_ROOT / "content" / "curriculum" / "arabic" / "A1"


def _transcript_dialogue_lines(path: Path) -> list[str]:
    lines: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^- \*\*([^*]+):\*\*\s*(.*?)\s*->", line)
        if match:
            lines.append(f"{match.group(1)}: {match.group(2)}")
    return lines


class TranscriptAlignmentTest(unittest.TestCase):
    def test_arabic_a1_transcript_side_matches_listening_script(self):
        failures: list[str] = []
        for script_path in sorted(ARABIC_A1_ROOT.glob("**/listening_script.md")):
            transcript_path = script_path.with_name("transcript_translation.md")
            if not transcript_path.exists():
                continue

            script_lines = [
                f"{turn.speaker}: {turn.text}"
                for turn in listening_script_to_dialogue_turns(script_path)
            ]
            transcript_lines = _transcript_dialogue_lines(transcript_path)
            if script_lines != transcript_lines:
                lesson_dir = script_path.parent.relative_to(ARABIC_A1_ROOT)
                failures.append(
                    f"{lesson_dir}: listening_script.md and "
                    "transcript_translation.md are not aligned"
                )

        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
