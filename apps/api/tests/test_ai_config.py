import unittest

from app.domain.ai import TASK_MODEL_CONFIGS


class AIConfigTest(unittest.TestCase):
    def test_all_tasks_use_together_provider(self):
        for task_name, model_config in TASK_MODEL_CONFIGS.items():
            with self.subTest(task_name=task_name):
                self.assertEqual(model_config.provider, "together")

    def test_grading_tasks_use_default_chat_model(self):
        # The conversation partner reply uses a separate, lower-latency chat model;
        # all other tasks (grading/feedback/summary) use the default chat model.
        for task_name, model_config in TASK_MODEL_CONFIGS.items():
            if task_name == "conversation_partner_reply":
                continue
            with self.subTest(task_name=task_name):
                self.assertEqual(
                    model_config.model, "meta-llama/Llama-3.3-70B-Instruct-Turbo"
                )

    def test_partner_reply_uses_partner_chat_model(self):
        self.assertEqual(
            TASK_MODEL_CONFIGS["conversation_partner_reply"].model,
            "deepseek-ai/DeepSeek-V4-Pro",
        )


if __name__ == "__main__":
    unittest.main()
