import unittest

from app.domain.ai import TASK_MODEL_CONFIGS


class AIConfigTest(unittest.TestCase):
    def test_together_tasks_use_default_chat_model(self):
        for task_name, model_config in TASK_MODEL_CONFIGS.items():
            with self.subTest(task_name=task_name):
                self.assertEqual(model_config.provider, "together")
                self.assertEqual(
                    model_config.model, "meta-llama/Llama-3.3-70B-Instruct-Turbo"
                )


if __name__ == "__main__":
    unittest.main()
