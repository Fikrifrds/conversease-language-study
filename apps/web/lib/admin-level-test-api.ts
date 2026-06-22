import type { LevelTest, LevelTestAttempt } from "@/lib/learning-api";
import { getAuthToken } from "@/lib/auth-api";

type ApiResponse<T> = {
  data: T;
};

type ApiLevelTest = {
  language?: string;
  language_code?: string;
  level_code: string;
  attempt_level_code?: string;
  title: string;
  status: string;
  description: string;
  overall_threshold: number;
  lesson_completion_required_percent: number;
  critical_skills: string[];
  sections: Array<{
    key: string;
    title: string;
    weight: number;
    minimum_score: number;
    task: {
      type: string;
      prompt: string;
      success_criteria: string[];
    };
  }>;
};

type ApiLevelTestAttempt = {
  id: string;
  user_id: string;
  level_code: string;
  status: "in_progress" | "submitted" | "reviewed";
  lesson_completion_percent: number | null;
  scores: Record<string, number>;
  responses: Record<string, unknown>;
  evaluation_snapshot: ApiLevelTest;
  overall_score: number | null;
  passed: boolean | null;
  missing_requirements: string[];
  weak_skills: string[];
  started_at: string;
  submitted_at: string | null;
  reviewed_at: string | null;
  reviewed_by: string | null;
  admin_notes: string | null;
  updated_at: string;
};

function apiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

async function adminRequestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getAuthToken();
  if (!token) {
    throw new Error("Admin login required");
  }

  const response = await fetch(`${apiBaseUrl()}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...init?.headers
    }
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function mapLevelTest(test: ApiLevelTest): LevelTest {
  return {
    language: test.language ?? "english",
    languageCode: test.language_code ?? "en",
    levelCode: test.level_code,
    attemptLevelCode: test.attempt_level_code ?? test.level_code,
    title: test.title,
    status: test.status,
    description: test.description,
    overallThreshold: test.overall_threshold,
    lessonCompletionRequiredPercent: test.lesson_completion_required_percent,
    criticalSkills: test.critical_skills,
    sections: test.sections.map((section) => ({
      key: section.key,
      title: section.title,
      weight: section.weight,
      minimumScore: section.minimum_score,
      task: {
        type: section.task.type,
        prompt: section.task.prompt,
        successCriteria: section.task.success_criteria
      }
    }))
  };
}

function mapAttempt(attempt: ApiLevelTestAttempt): LevelTestAttempt {
  return {
    id: attempt.id,
    userId: attempt.user_id,
    levelCode: attempt.level_code,
    status: attempt.status,
    lessonCompletionPercent: attempt.lesson_completion_percent,
    scores: attempt.scores,
    responses: attempt.responses,
    evaluationSnapshot: mapLevelTest(attempt.evaluation_snapshot),
    overallScore: attempt.overall_score,
    passed: attempt.passed,
    missingRequirements: attempt.missing_requirements,
    weakSkills: attempt.weak_skills,
    startedAt: attempt.started_at,
    submittedAt: attempt.submitted_at,
    reviewedAt: attempt.reviewed_at,
    reviewedBy: attempt.reviewed_by,
    adminNotes: attempt.admin_notes,
    updatedAt: attempt.updated_at
  };
}

export async function listAdminLevelTestAttempts(input: {
  levelCode?: string;
  status?: string;
  limit?: number;
}): Promise<LevelTestAttempt[]> {
  const params = new URLSearchParams();
  params.set("level_code", input.levelCode ?? "A1");
  if (input.status) {
    params.set("status", input.status);
  }
  params.set("limit", String(input.limit ?? 50));

  const response = await adminRequestJson<ApiResponse<ApiLevelTestAttempt[]>>(
    `/admin/level-test-attempts?${params.toString()}`
  );
  return response.data.map(mapAttempt);
}

export async function getAdminLevelTestAttempt(input: {
  attemptId: string;
}): Promise<LevelTestAttempt> {
  const response = await adminRequestJson<ApiResponse<ApiLevelTestAttempt>>(
    `/admin/level-test-attempts/${input.attemptId}`
  );
  return mapAttempt(response.data);
}

export async function scoreAdminLevelTestAttempt(input: {
  attemptId: string;
  reviewedBy: string;
  lessonCompletionPercent?: number | null;
  scores: Record<string, number>;
  notes?: string;
}): Promise<LevelTestAttempt> {
  const response = await adminRequestJson<ApiResponse<ApiLevelTestAttempt>>(
    `/admin/level-test-attempts/${input.attemptId}/score`,
    {
      method: "POST",
      body: JSON.stringify({
        reviewed_by: input.reviewedBy,
        lesson_completion_percent: input.lessonCompletionPercent ?? undefined,
        scores: input.scores,
        notes: input.notes ?? ""
      })
    }
  );
  return mapAttempt(response.data);
}
