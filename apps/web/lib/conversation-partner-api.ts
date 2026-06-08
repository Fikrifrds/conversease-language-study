import { getAuthToken } from "@/lib/auth-api";
import { ApiRequestError } from "@/lib/conversation-api";

export type PartnerTopic = {
  key: string;
  levelCode: string;
  title: string;
  description: string;
  partnerRole: string;
  goals: string[];
  openingLine: string;
  maxTurns: number;
};

export type PartnerSession = {
  sessionId: string;
  topic: PartnerTopic;
  openingLine: string;
  openingAudio: string | null;
  completedTurns: number;
  maxTurns: number;
};

export type PartnerTurnResult = {
  sessionId: string;
  userTranscript: string;
  partnerReply: string;
  partnerAudio: string | null;
  onTopic: boolean;
  shouldEnd: boolean;
  completedTurns: number;
  maxTurns: number;
};

export type PartnerSummary = {
  sessionId: string;
  summary: string;
  indonesianExplanation: string;
  scores: { speaking: number; grammar: number; fluency: number };
  completedTurns: number;
};

export type PartnerSessionSummaryRow = {
  sessionId: string;
  topicKey: string;
  topicTitle: string;
  levelCode: string;
  status: string;
  completedTurns: number;
  maxTurns: number | null;
  overallScore: number | null;
  scores: { speaking: number; grammar: number; fluency: number } | null;
  updatedAt: string;
};

export type PartnerSessionDetail = PartnerSessionSummaryRow & {
  messages: { role: "partner" | "user"; text: string }[];
  summary: {
    summary: string;
    indonesian_explanation: string;
    scores: { speaking: number; grammar: number; fluency: number };
    overall: number;
  } | null;
};

type ApiResponse<T> = { data: T };

function apiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

function authHeaders(): Record<string, string> {
  const token = getAuthToken();
  if (!token) {
    throw new Error("Authentication required");
  }
  return { Authorization: `Bearer ${token}` };
}

async function readError(response: Response): Promise<never> {
  const detail = await response.text();
  throw new ApiRequestError(response.status, detail || `API request failed: ${response.status}`);
}

type ApiTopic = {
  key: string;
  level_code: string;
  title: string;
  description: string;
  partner_role: string;
  goals: string[];
  opening_line: string;
  max_turns: number;
};

function mapTopic(topic: ApiTopic): PartnerTopic {
  return {
    key: topic.key,
    levelCode: topic.level_code,
    title: topic.title,
    description: topic.description,
    partnerRole: topic.partner_role,
    goals: topic.goals,
    openingLine: topic.opening_line,
    maxTurns: topic.max_turns
  };
}

export async function listPartnerTopics(levelCode = "A1"): Promise<PartnerTopic[]> {
  const response = await fetch(
    `${apiBaseUrl()}/conversation-partner/topics?level_code=${encodeURIComponent(levelCode)}`,
    { headers: authHeaders() }
  );
  if (!response.ok) {
    return readError(response);
  }
  const payload = (await response.json()) as ApiResponse<ApiTopic[]>;
  return payload.data.map(mapTopic);
}

export async function createPartnerSession(topicKey: string): Promise<PartnerSession> {
  const response = await fetch(`${apiBaseUrl()}/conversation-partner/sessions`, {
    method: "POST",
    headers: { ...authHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ topic_key: topicKey })
  });
  if (!response.ok) {
    return readError(response);
  }
  const payload = (await response.json()) as ApiResponse<{
    session_id: string;
    topic: ApiTopic;
    opening_line: string;
    opening_audio: string | null;
    completed_turns: number;
    max_turns: number;
  }>;
  return {
    sessionId: payload.data.session_id,
    topic: mapTopic(payload.data.topic),
    openingLine: payload.data.opening_line,
    openingAudio: payload.data.opening_audio,
    completedTurns: payload.data.completed_turns,
    maxTurns: payload.data.max_turns
  };
}

export async function submitPartnerAudioTurn(
  sessionId: string,
  audio: Blob
): Promise<PartnerTurnResult> {
  const formData = new FormData();
  formData.append("audio", audio, recordedAudioFilename(audio.type));

  const response = await fetch(
    `${apiBaseUrl()}/conversation-partner/sessions/${sessionId}/turns/audio`,
    { method: "POST", headers: authHeaders(), body: formData }
  );
  if (!response.ok) {
    return readError(response);
  }
  const payload = (await response.json()) as ApiResponse<{
    session_id: string;
    user_transcript: string;
    partner_reply: string;
    partner_audio: string | null;
    on_topic: boolean;
    should_end: boolean;
    completed_turns: number;
    max_turns: number;
  }>;
  return {
    sessionId: payload.data.session_id,
    userTranscript: payload.data.user_transcript,
    partnerReply: payload.data.partner_reply,
    partnerAudio: payload.data.partner_audio,
    onTopic: payload.data.on_topic,
    shouldEnd: payload.data.should_end,
    completedTurns: payload.data.completed_turns,
    maxTurns: payload.data.max_turns
  };
}

export async function fetchPartnerSummary(sessionId: string): Promise<PartnerSummary> {
  const response = await fetch(
    `${apiBaseUrl()}/conversation-partner/sessions/${sessionId}/summary`,
    { method: "POST", headers: authHeaders() }
  );
  if (!response.ok) {
    return readError(response);
  }
  const payload = (await response.json()) as ApiResponse<{
    session_id: string;
    summary: string;
    indonesian_explanation: string;
    scores: { speaking: number; grammar: number; fluency: number };
    completed_turns: number;
  }>;
  return {
    sessionId: payload.data.session_id,
    summary: payload.data.summary,
    indonesianExplanation: payload.data.indonesian_explanation,
    scores: payload.data.scores,
    completedTurns: payload.data.completed_turns
  };
}

type ApiSessionRow = {
  session_id: string;
  topic_key: string;
  topic_title: string;
  level_code: string;
  status: string;
  completed_turns: number;
  max_turns: number | null;
  overall_score: number | null;
  scores: { speaking: number; grammar: number; fluency: number } | null;
  updated_at: string;
};

function mapSessionRow(row: ApiSessionRow): PartnerSessionSummaryRow {
  return {
    sessionId: row.session_id,
    topicKey: row.topic_key,
    topicTitle: row.topic_title,
    levelCode: row.level_code,
    status: row.status,
    completedTurns: row.completed_turns,
    maxTurns: row.max_turns,
    overallScore: row.overall_score,
    scores: row.scores,
    updatedAt: row.updated_at
  };
}

export async function listPartnerSessions(): Promise<PartnerSessionSummaryRow[]> {
  const response = await fetch(`${apiBaseUrl()}/conversation-partner/sessions`, {
    headers: authHeaders()
  });
  if (!response.ok) {
    return readError(response);
  }
  const payload = (await response.json()) as ApiResponse<ApiSessionRow[]>;
  return payload.data.map(mapSessionRow);
}

export async function fetchPartnerSessionDetail(sessionId: string): Promise<PartnerSessionDetail> {
  const response = await fetch(
    `${apiBaseUrl()}/conversation-partner/sessions/${sessionId}`,
    { headers: authHeaders() }
  );
  if (!response.ok) {
    return readError(response);
  }
  const payload = (await response.json()) as ApiResponse<
    ApiSessionRow & {
      messages: { role: "partner" | "user"; text: string }[];
      summary: PartnerSessionDetail["summary"];
    }
  >;
  return {
    ...mapSessionRow(payload.data),
    messages: payload.data.messages,
    summary: payload.data.summary
  };
}

function recordedAudioFilename(contentType: string) {
  if (contentType.includes("mp4")) {
    return "partner-turn.m4a";
  }
  if (contentType.includes("ogg")) {
    return "partner-turn.ogg";
  }
  if (contentType.includes("wav")) {
    return "partner-turn.wav";
  }
  return "partner-turn.webm";
}
