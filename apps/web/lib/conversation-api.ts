import { getAuthToken } from "@/lib/auth-api";

export type ApiPracticeSummary = {
  sessionId: string;
  completedTurns: number;
  totalTurns: number;
  completed: boolean;
  lastScore: number;
  updatedAt: string;
};

export type ApiTurnFeedback = {
  betterVersion: string;
  explanation: string;
  nextPractice: string;
  scores: {
    speaking: number;
    grammar: number;
    fluency: number;
  };
};

export type ApiTurnResult = {
  sessionId: string;
  userTranscript: string;
  coachReply: string | null;
  feedback: ApiTurnFeedback;
  summary: ApiPracticeSummary;
  transcription?: {
    inputSource: string;
    provider: string;
    model: string;
    transcriptId: string;
    confidence: number | null;
    audioDurationSeconds: number | null;
  } | null;
};

type ApiResponse<T> = {
  data: T;
};

type ApiTurnResponse = {
  session_id: string;
  user_transcript: string;
  conversation_coach_reply: string | null;
  completed_turns: number;
  total_turns: number;
  completed: boolean;
  last_score: number;
  updated_at: string;
  feedback: {
    better_version: string;
    indonesian_explanation: string;
    scores: {
      speaking: number;
      grammar: number;
      fluency: number;
    };
    next_practice: string[];
  };
  transcription?: null | {
    input_source: string;
    provider: string;
    model: string;
    transcript_id: string;
    confidence: number | null;
    audio_duration_seconds: number | null;
  };
};

const defaultLessonSlug = "saying-hello-and-goodbye";

export class ApiRequestError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiRequestError";
    this.status = status;
  }
}

function apiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getAuthToken();
  if (!token) {
    throw new Error("Authentication required");
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
    throw new ApiRequestError(response.status, detail || `API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function createConversationSession(
  lessonSlug = defaultLessonSlug
): Promise<{ sessionId: string; firstCoachMessage: string }> {
  const response = await requestJson<
    ApiResponse<{
      id: string;
      first_coach_message: string;
    }>
  >("/conversation-sessions", {
    method: "POST",
    body: JSON.stringify({
      language_code: "en",
      level_code: "A1",
      mode: "lesson_practice_coach",
      scenario_key: "greeting_intro",
      lesson_slug: lessonSlug
    })
  });

  return {
    sessionId: response.data.id,
    firstCoachMessage: response.data.first_coach_message
  };
}

export async function submitConversationTurn(sessionId: string, transcript: string): Promise<ApiTurnResult> {
  const response = await requestJson<ApiResponse<ApiTurnResponse>>(`/conversation-sessions/${sessionId}/turns`, {
    method: "POST",
    body: JSON.stringify({
      transcript
    })
  });

  return mapTurnResponse(response.data);
}

export async function submitConversationAudioTurn(sessionId: string, audio: Blob): Promise<ApiTurnResult> {
  const token = getAuthToken();
  if (!token) {
    throw new Error("Authentication required");
  }

  const formData = new FormData();
  formData.append("audio", audio, recordedAudioFilename(audio.type));

  const response = await fetch(`${apiBaseUrl()}/conversation-sessions/${sessionId}/turns/audio`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: formData
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new ApiRequestError(response.status, detail || `API request failed: ${response.status}`);
  }

  const payload = (await response.json()) as ApiResponse<ApiTurnResponse>;
  return mapTurnResponse(payload.data);
}

function mapTurnResponse(data: ApiTurnResponse): ApiTurnResult {
  return {
    sessionId: data.session_id,
    userTranscript: data.user_transcript,
    coachReply: data.conversation_coach_reply,
    feedback: {
      betterVersion: data.feedback.better_version,
      explanation: data.feedback.indonesian_explanation,
      nextPractice: data.feedback.next_practice[0] ?? "Review this roleplay again.",
      scores: data.feedback.scores
    },
    summary: {
      sessionId: data.session_id,
      completedTurns: data.completed_turns,
      totalTurns: data.total_turns,
      completed: data.completed,
      lastScore: data.last_score,
      updatedAt: data.updated_at
    },
    transcription: data.transcription
      ? {
          inputSource: data.transcription.input_source,
          provider: data.transcription.provider,
          model: data.transcription.model,
          transcriptId: data.transcription.transcript_id,
          confidence: data.transcription.confidence,
          audioDurationSeconds: data.transcription.audio_duration_seconds
        }
      : null
  };
}

function recordedAudioFilename(contentType: string) {
  if (contentType.includes("mp4")) {
    return "conversation-turn.m4a";
  }
  if (contentType.includes("ogg")) {
    return "conversation-turn.ogg";
  }
  if (contentType.includes("wav")) {
    return "conversation-turn.wav";
  }
  return "conversation-turn.webm";
}

export async function getLatestPractice(lessonSlug = defaultLessonSlug): Promise<ApiPracticeSummary | null> {
  const response = await requestJson<
    ApiResponse<null | {
      session_id: string;
      completed_turns: number;
      total_turns: number;
      completed: boolean;
      last_score: number;
      updated_at: string;
    }>
  >(`/conversation-practice/latest?lesson_slug=${encodeURIComponent(lessonSlug)}`);

  if (!response.data) {
    return null;
  }

  return {
    sessionId: response.data.session_id,
    completedTurns: response.data.completed_turns,
    totalTurns: response.data.total_turns,
    completed: response.data.completed,
    lastScore: response.data.last_score,
    updatedAt: response.data.updated_at
  };
}

export async function resetLatestPractice(lessonSlug = defaultLessonSlug): Promise<void> {
  await requestJson<ApiResponse<{ reset: boolean }>>(
    `/conversation-practice/latest?lesson_slug=${encodeURIComponent(lessonSlug)}`,
    {
      method: "DELETE"
    }
  );
}
