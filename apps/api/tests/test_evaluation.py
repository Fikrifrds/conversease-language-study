import unittest

from app.domain.evaluation import evaluate_level_attempt, weighted_score


class EvaluationRulesTest(unittest.TestCase):
    def test_weighted_score_matches_a1_weights(self):
        score = weighted_score(
            {
                "speaking_conversation": 80,
                "listening": 70,
                "pronunciation_fluency": 60,
                "useful_phrases": 70,
                "grammar": 70,
                "reading": 80,
                "writing": 80,
            }
        )

        self.assertEqual(score, 72)

    def test_critical_skill_blocks_pass(self):
        result = evaluate_level_attempt(
            scores={
                "speaking_conversation": 59,
                "listening": 90,
                "pronunciation_fluency": 90,
                "useful_phrases": 90,
                "grammar": 90,
                "reading": 90,
                "writing": 90,
            },
            lesson_completion_percent=100,
        )

        self.assertFalse(result.passed)
        self.assertIn("critical:speaking_conversation", result.missing_requirements)

    def test_passes_when_all_requirements_met(self):
        result = evaluate_level_attempt(
            scores={
                "speaking_conversation": 70,
                "listening": 70,
                "pronunciation_fluency": 70,
                "useful_phrases": 70,
                "grammar": 70,
                "reading": 70,
                "writing": 70,
            },
            lesson_completion_percent=85,
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.overall_score, 70)


if __name__ == "__main__":
    unittest.main()

