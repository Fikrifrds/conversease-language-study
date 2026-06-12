import { getAuthToken } from "@/lib/auth-api";

export type ExamReviewQueueEntry = {
  id: string;
  responseId: string;
  sessionId: string;
  examTemplateId: string;
  itemType: string;
  status: string;
  promptText: string;
  scorePointsMax: number;
  rubricCriteria: Record<string, { weight: number; criteria: string }> | null;
  textResponse: string | null;
  fileUrl: string | null;
  playbackUrl: string | null;
  audioDurationSeconds: number | null;
  createdAt: string;
};

export type ExamReviewResult = {
  id: string;
  sessionId: string;
  status: string;
  totalScore: number;
  maxPossibleScore: number;
  scorePercent: number;
  passed: boolean;
};

type ApiExamReviewQueueEntry = {
  id: string;
  response_id: string;
  session_id: string;
  exam_template_id: string;
  item_type: string;
  status: string;
  prompt_text: string;
  score_points_max: number;
  rubric_criteria: Record<string, { weight: number; criteria: string }> | null;
  text_response: string | null;
  file_url: string | null;
  playback_url: string | null;
  audio_duration_seconds: number | null;
  created_at: string;
};

type ApiExamReviewResult = {
  id: string;
  session_id: string;
  status: string;
  total_score: number;
  max_possible_score: number;
  score_percent: number;
  passed: boolean;
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

function mapEntry(entry: ApiExamReviewQueueEntry): ExamReviewQueueEntry {
  return {
    id: entry.id,
    responseId: entry.response_id,
    sessionId: entry.session_id,
    examTemplateId: entry.exam_template_id,
    itemType: entry.item_type,
    status: entry.status,
    promptText: entry.prompt_text,
    scorePointsMax: entry.score_points_max,
    rubricCriteria: entry.rubric_criteria,
    textResponse: entry.text_response,
    fileUrl: entry.file_url,
    playbackUrl: entry.playback_url,
    audioDurationSeconds: entry.audio_duration_seconds,
    createdAt: entry.created_at
  };
}

export async function listExamReviewQueue(status: string): Promise<ExamReviewQueueEntry[]> {
  const entries = await adminRequestJson<ApiExamReviewQueueEntry[]>(
    `/exams/admin/review-queue?queue_status=${encodeURIComponent(status)}`
  );
  return entries.map(mapEntry);
}

export async function scoreExamReviewEntry(input: {
  queueId: string;
  scorePoints: number;
  notes?: string;
}): Promise<ExamReviewResult> {
  const result = await adminRequestJson<ApiExamReviewResult>(
    `/exams/admin/review-queue/${encodeURIComponent(input.queueId)}/score`,
    {
      method: "POST",
      body: JSON.stringify({
        score_points: input.scorePoints,
        notes: input.notes || null
      })
    }
  );
  return {
    id: result.id,
    sessionId: result.session_id,
    status: result.status,
    totalScore: result.total_score,
    maxPossibleScore: result.max_possible_score,
    scorePercent: result.score_percent,
    passed: result.passed
  };
}
