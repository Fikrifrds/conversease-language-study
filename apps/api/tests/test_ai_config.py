import unittest

from app.domain.ai import TASK_MODEL_CONFIGS


class AIConfigTest(unittest.TestCase):
    def test_together_tasks_use_minimax_m27_by_default(self):
        for task_name, model_config in TASK_MODEL_CONFIGS.items():
            with self.subTest(task_name=task_name):
                self.assertEqual(model_config.provider, "together")
                self.assertEqual(model_config.model, "MiniMaxAI/MiniMax-M2.7")


if __name__ == "__main__":
    unittest.main()
