"""Guard: apps/web/lib/data.ts must stay generated from the curriculum.

The lesson array in data.ts is produced by scripts/generate_web_lesson_data.py
from the curriculum files (the single source of truth). This test regenerates it
in-memory and fails if the committed file differs — i.e. if someone edited the
curriculum without regenerating, or hand-edited the generated block.

To fix a failure:
    PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_web_lesson_data.py
"""
import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
GENERATOR = REPO_ROOT / "scripts" / "generate_web_lesson_data.py"
DATA_TS = REPO_ROOT / "apps" / "web" / "lib" / "data.ts"


def _load_generator():
    spec = importlib.util.spec_from_file_location("generate_web_lesson_data", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WebLessonDataInSyncTest(unittest.TestCase):
    def test_data_ts_matches_curriculum(self):
        generator = _load_generator()
        expected = generator.generate()
        actual = DATA_TS.read_text(encoding="utf-8")
        self.assertEqual(
            actual,
            expected,
            "apps/web/lib/data.ts is out of sync with the curriculum. Run:\n"
            "  PYTHONPATH=apps/api apps/api/.venv/bin/python "
            "scripts/generate_web_lesson_data.py",
        )


if __name__ == "__main__":
    unittest.main()
