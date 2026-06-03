from dataclasses import dataclass
from typing import Dict, Iterable, List


SKILL_MINIMUMS_A1 = {
    "speaking_conversation": 60,
    "listening": 60,
    "pronunciation_fluency": 55,
    "useful_phrases": 60,
    "grammar": 60,
    "reading": 55,
    "writing": 55,
}

SKILL_WEIGHTS_A1 = {
    "speaking_conversation": 0.30,
    "listening": 0.25,
    "pronunciation_fluency": 0.15,
    "useful_phrases": 0.10,
    "grammar": 0.10,
    "reading": 0.05,
    "writing": 0.05,
}


@dataclass(frozen=True)
class LevelEvaluationResult:
    overall_score: int
    passed: bool
    missing_requirements: List[str]
    weak_skills: List[str]


def weighted_score(scores: Dict[str, int], weights: Dict[str, float] = SKILL_WEIGHTS_A1) -> int:
    total = 0.0
    for skill, weight in weights.items():
        total += max(0, min(scores.get(skill, 0), 100)) * weight
    return round(total)


def evaluate_level_attempt(
    scores: Dict[str, int],
    lesson_completion_percent: int,
    overall_threshold: int = 70,
    skill_minimums: Dict[str, int] = SKILL_MINIMUMS_A1,
    skill_weights: Dict[str, float] = SKILL_WEIGHTS_A1,
    critical_skills: Iterable[str] = ("speaking_conversation", "listening"),
    lesson_completion_required_percent: int = 80,
) -> LevelEvaluationResult:
    overall = weighted_score(scores, skill_weights)
    missing: List[str] = []
    weak: List[str] = []

    if overall < overall_threshold:
        missing.append(f"overall_score>={overall_threshold}")

    if lesson_completion_percent < lesson_completion_required_percent:
        missing.append(f"lesson_completion>={lesson_completion_required_percent}")

    for skill, minimum in skill_minimums.items():
        if scores.get(skill, 0) < minimum:
            weak.append(skill)
            missing.append(f"{skill}>={minimum}")

    for skill in critical_skills:
        if scores.get(skill, 0) < skill_minimums[skill]:
            marker = f"critical:{skill}"
            if marker not in missing:
                missing.append(marker)

    return LevelEvaluationResult(
        overall_score=overall,
        passed=len(missing) == 0,
        missing_requirements=missing,
        weak_skills=weak,
    )
