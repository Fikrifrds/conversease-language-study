import { getAuthToken } from "@/lib/auth-api";

export type OnboardingProfile = {
  primaryGoal: string;
  confidenceLevel: string;
  dailyTargetMinutes: number;
  recommendedCourseSlug: string;
  recommendedLevelCode: string;
  completed: boolean;
  updatedAt: string;
};

export type LessonProgress = {
  lessonSlug: string;
  courseSlug: string;
  title: string;
  status: "in_progress" | "completed";
  completedSections: string[];
  totalSections: number;
  startedAt: string;
  completedAt: string | null;
  updatedAt: string;
};

export type LearningLessonSummary = {
  slug: string;
  title: string;
  unitTitle: string;
  conversationGoal: string;
  estimatedMinutes: number;
  status: string;
  progressStatus: "not_started" | "in_progress" | "completed";
  completedSections: string[];
  totalSections: number;
  updatedAt: string | null;
};

export type LearningLessonAudioAsset = {
  key: string;
  type: string;
  audioUrl: string;
  playbackUrl: string;
  durationSeconds: number;
  provider: string;
  model: string;
  voiceId: string;
  speakerVoices: Record<string, string>;
  lineCount: number;
  audioFormat: string;
  storageKey: string;
  generatedAt: string;
  generatedBy: string;
};

export type LearningProgressSummary = {
  onboarding: OnboardingProfile | null;
  course: {
    slug: string;
    title: string;
    levelCode: string;
    completionPercent: number;
    completedLessons: number;
    totalLessons: number;
  };
  currentMission: LearningLessonSummary | null;
  lessons: LearningLessonSummary[];
};

export type LevelTestSection = {
  key: string;
  title: string;
  weight: number;
  minimumScore: number;
  task: {
    type: string;
    prompt: string;
    successCriteria: string[];
  };
};

export type LevelTest = {
  levelCode: string;
  title: string;
  status: string;
  description: string;
  overallThreshold: number;
  lessonCompletionRequiredPercent: number;
  criticalSkills: string[];
  sections: LevelTestSection[];
};

export type LevelTestPreviewResult = {
  overallScore: number;
  passed: boolean;
  missingRequirements: string[];
  weakSkills: string[];
};

export type LevelTestAttempt = {
  id: string;
  userId: string;
  levelCode: string;
  status: "in_progress" | "submitted" | "reviewed";
  lessonCompletionPercent: number | null;
  scores: Record<string, number>;
  responses: Record<string, unknown>;
  evaluationSnapshot: LevelTest;
  overallScore: number | null;
  passed: boolean | null;
  missingRequirements: string[];
  weakSkills: string[];
  startedAt: string;
  submittedAt: string | null;
  reviewedAt: string | null;
  reviewedBy: string | null;
  adminNotes: string | null;
  updatedAt: string;
};

export type ExamTemplateSummary = {
  id: string;
  code: string;
  levelCode: string;
  title: string;
  description: string | null;
  durationMinutes: number;
  passingScorePercent: number;
  status: string;
  version: number;
  createdAt: string;
  updatedAt: string;
};

export type ExamRunnerSession = {
  sessionId: string;
  examTemplateId: string;
  status: string;
  startedAt: string;
  expiresAt: string;
  timeRemainingSeconds: number;
  currentSectionId: string | null;
  currentItemId: string | null;
};

export type ExamManifestSection = {
  id: string;
  code: string;
  title: string;
  description: string | null;
  sequenceOrder: number;
  durationMinutes: number;
};

export type ExamManifest = {
  sessionId: string;
  examTemplateId: string;
  status: string;
  currentSectionId: string | null;
  currentItemId: string | null;
  sections: ExamManifestSection[];
};

export type ExamRunnerItemOption = {
  id: string;
  text: string;
};

export type ExamRunnerItem = {
  id: string;
  itemType: string;
  sequenceOrder: number;
  promptText: string;
  stimulusText: string | null;
  stimulusAudioUrl: string | null;
  stimulusImageUrl: string | null;
  options: ExamRunnerItemOption[] | null;
  optionsData: Record<string, unknown> | unknown[] | null;
  scorePoints: number;
};

export type ExamRunnerSectionContent = {
  sessionId: string;
  section: ExamManifestSection;
  items: ExamRunnerItem[];
  totalSections: number;
  currentSectionNumber: number;
};

export type ExamRunnerStatus = {
  sessionId: string;
  status: string;
  startedAt: string | null;
  expiresAt: string | null;
  submittedAt: string | null;
  timeRemainingSeconds: number | null;
  progress: Record<
    string,
    {
      totalItems: number;
      completedItems: number;
      sectionCode: string;
    }
  >;
};

type ApiResponse<T> = {
  data: T;
};

type ApiOnboarding = {
  primary_goal: string;
  confidence_level: string;
  daily_target_minutes: number;
  recommended_course_slug: string;
  recommended_level_code: string;
  completed: boolean;
  updated_at: string;
};

type ApiLessonProgress = {
  lesson_slug: string;
  course_slug: string;
  title: string;
  status: "in_progress" | "completed";
  completed_sections: string[];
  total_sections: number;
  started_at: string;
  completed_at: string | null;
  updated_at: string;
};

type ApiLearningLessonSummary = {
  slug: string;
  title: string;
  unit_title: string;
  conversation_goal: string;
  estimated_minutes: number;
  status: string;
  progress_status: "not_started" | "in_progress" | "completed";
  completed_sections: string[];
  total_sections: number;
  updated_at: string | null;
};

type ApiLearningLessonAudioAsset = {
  key: string;
  type: string;
  audio_url: string;
  playback_url: string;
  duration_seconds: number;
  provider: string;
  model: string;
  voice_id: string;
  speaker_voices: Record<string, string>;
  line_count: number;
  audio_format: string;
  storage_key: string;
  generated_at: string;
  generated_by: string;
};

type ApiLearningProgressSummary = {
  onboarding: ApiOnboarding | null;
  course: {
    slug: string;
    title: string;
    level_code: string;
    completion_percent: number;
    completed_lessons: number;
    total_lessons: number;
  };
  current_mission: ApiLearningLessonSummary | null;
  lessons: ApiLearningLessonSummary[];
};

type ApiLevelTestSection = {
  key: string;
  title: string;
  weight: number;
  minimum_score: number;
  task: {
    type: string;
    prompt: string;
    success_criteria: string[];
  };
};

type ApiLevelTest = {
  level_code: string;
  title: string;
  status: string;
  description: string;
  overall_threshold: number;
  lesson_completion_required_percent: number;
  critical_skills: string[];
  sections: ApiLevelTestSection[];
};

type ApiLevelTestPreviewResult = {
  overall_score: number;
  passed: boolean;
  missing_requirements: string[];
  weak_skills: string[];
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

type ApiExamTemplateSummary = {
  id: string;
  code: string;
  level_code: string;
  title: string;
  description: string | null;
  duration_minutes: number;
  passing_score_percent: number;
  status: string;
  version: number;
  created_at: string;
  updated_at: string;
};

type ApiExamRunnerSession = {
  session_id: string;
  exam_template_id: string;
  status: string;
  started_at: string;
  expires_at: string;
  time_remaining_seconds: number;
  current_section_id: string | null;
  current_item_id: string | null;
};

type ApiExamManifestSection = {
  id: string;
  code: string;
  title: string;
  description: string | null;
  sequence_order: number;
  duration_minutes: number;
};

type ApiExamManifest = {
  session_id: string;
  exam_template_id: string;
  status: string;
  current_section_id: string | null;
  current_item_id: string | null;
  sections: ApiExamManifestSection[];
};

type ApiExamRunnerItemOption = {
  id: string;
  text: string;
};

type ApiExamRunnerItem = {
  id: string;
  item_type: string;
  sequence_order: number;
  prompt_text: string;
  stimulus_text: string | null;
  stimulus_audio_url: string | null;
  stimulus_image_url: string | null;
  options: ApiExamRunnerItemOption[] | null;
  options_data: Record<string, unknown> | unknown[] | null;
  score_points: number;
};

type ApiExamRunnerSectionContent = {
  session_id: string;
  section: ApiExamManifestSection;
  items: ApiExamRunnerItem[];
  total_sections: number;
  current_section_number: number;
};

type ApiExamRunnerStatus = {
  session_id: string;
  status: string;
  started_at: string | null;
  expires_at: string | null;
  submitted_at: string | null;
  time_remaining_seconds: number | null;
  progress: Record<
    string,
    {
      total_items: number;
      completed_items: number;
      section_code: string;
    }
  >;
};

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
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function mapOnboarding(profile: ApiOnboarding): OnboardingProfile {
  return {
    primaryGoal: profile.primary_goal,
    confidenceLevel: profile.confidence_level,
    dailyTargetMinutes: profile.daily_target_minutes,
    recommendedCourseSlug: profile.recommended_course_slug,
    recommendedLevelCode: profile.recommended_level_code,
    completed: profile.completed,
    updatedAt: profile.updated_at
  };
}

function mapLessonSummary(lesson: ApiLearningLessonSummary): LearningLessonSummary {
  return {
    slug: lesson.slug,
    title: lesson.title,
    unitTitle: lesson.unit_title,
    conversationGoal: lesson.conversation_goal,
    estimatedMinutes: lesson.estimated_minutes,
    status: lesson.status,
    progressStatus: lesson.progress_status,
    completedSections: lesson.completed_sections,
    totalSections: lesson.total_sections,
    updatedAt: lesson.updated_at
  };
}

function mapLessonProgress(progress: ApiLessonProgress): LessonProgress {
  return {
    lessonSlug: progress.lesson_slug,
    courseSlug: progress.course_slug,
    title: progress.title,
    status: progress.status,
    completedSections: progress.completed_sections,
    totalSections: progress.total_sections,
    startedAt: progress.started_at,
    completedAt: progress.completed_at,
    updatedAt: progress.updated_at
  };
}

function mapLessonAudioAsset(asset: ApiLearningLessonAudioAsset): LearningLessonAudioAsset {
  return {
    key: asset.key,
    type: asset.type,
    audioUrl: asset.audio_url,
    playbackUrl: asset.playback_url,
    durationSeconds: asset.duration_seconds,
    provider: asset.provider,
    model: asset.model,
    voiceId: asset.voice_id,
    speakerVoices: asset.speaker_voices ?? {},
    lineCount: asset.line_count ?? 0,
    audioFormat: asset.audio_format,
    storageKey: asset.storage_key,
    generatedAt: asset.generated_at,
    generatedBy: asset.generated_by
  };
}

function mapLevelTest(test: ApiLevelTest): LevelTest {
  return {
    levelCode: test.level_code,
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

function mapLevelTestAttempt(attempt: ApiLevelTestAttempt): LevelTestAttempt {
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

function mapExamTemplateSummary(template: ApiExamTemplateSummary): ExamTemplateSummary {
  return {
    id: template.id,
    code: template.code,
    levelCode: template.level_code,
    title: template.title,
    description: template.description,
    durationMinutes: template.duration_minutes,
    passingScorePercent: template.passing_score_percent,
    status: template.status,
    version: template.version,
    createdAt: template.created_at,
    updatedAt: template.updated_at
  };
}

function mapExamManifestSection(section: ApiExamManifestSection): ExamManifestSection {
  return {
    id: section.id,
    code: section.code,
    title: section.title,
    description: section.description,
    sequenceOrder: section.sequence_order,
    durationMinutes: section.duration_minutes
  };
}

function mapExamRunnerSession(session: ApiExamRunnerSession): ExamRunnerSession {
  return {
    sessionId: session.session_id,
    examTemplateId: session.exam_template_id,
    status: session.status,
    startedAt: session.started_at,
    expiresAt: session.expires_at,
    timeRemainingSeconds: session.time_remaining_seconds,
    currentSectionId: session.current_section_id,
    currentItemId: session.current_item_id
  };
}

function mapExamManifest(manifest: ApiExamManifest): ExamManifest {
  return {
    sessionId: manifest.session_id,
    examTemplateId: manifest.exam_template_id,
    status: manifest.status,
    currentSectionId: manifest.current_section_id,
    currentItemId: manifest.current_item_id,
    sections: manifest.sections.map(mapExamManifestSection)
  };
}

function mapExamSectionContent(content: ApiExamRunnerSectionContent): ExamRunnerSectionContent {
  return {
    sessionId: content.session_id,
    section: mapExamManifestSection(content.section),
    items: content.items.map((item) => ({
      id: item.id,
      itemType: item.item_type,
      sequenceOrder: item.sequence_order,
      promptText: item.prompt_text,
      stimulusText: item.stimulus_text,
      stimulusAudioUrl: item.stimulus_audio_url,
      stimulusImageUrl: item.stimulus_image_url,
      options: item.options,
      optionsData: item.options_data,
      scorePoints: item.score_points
    })),
    totalSections: content.total_sections,
    currentSectionNumber: content.current_section_number
  };
}

function mapExamRunnerStatus(status: ApiExamRunnerStatus): ExamRunnerStatus {
  return {
    sessionId: status.session_id,
    status: status.status,
    startedAt: status.started_at,
    expiresAt: status.expires_at,
    submittedAt: status.submitted_at,
    timeRemainingSeconds: status.time_remaining_seconds,
    progress: Object.fromEntries(
      Object.entries(status.progress).map(([sectionId, value]) => [
        sectionId,
        {
          totalItems: value.total_items,
          completedItems: value.completed_items,
          sectionCode: value.section_code
        }
      ])
    )
  };
}

export async function getOnboardingProfile(): Promise<OnboardingProfile | null> {
  const response = await requestJson<ApiResponse<ApiOnboarding | null>>("/me/onboarding");
  return response.data ? mapOnboarding(response.data) : null;
}

export async function saveOnboardingProfile(input: {
  primaryGoal: string;
  confidenceLevel: string;
  dailyTargetMinutes: number;
}): Promise<OnboardingProfile> {
  const response = await requestJson<ApiResponse<ApiOnboarding>>("/me/onboarding", {
    method: "PUT",
    body: JSON.stringify({
      primary_goal: input.primaryGoal,
      confidence_level: input.confidenceLevel,
      daily_target_minutes: input.dailyTargetMinutes
    })
  });

  return mapOnboarding(response.data);
}

export async function getLearningProgress(): Promise<LearningProgressSummary> {
  const response = await requestJson<ApiResponse<ApiLearningProgressSummary>>(
    "/me/learning-progress"
  );

  return {
    onboarding: response.data.onboarding ? mapOnboarding(response.data.onboarding) : null,
    course: {
      slug: response.data.course.slug,
      title: response.data.course.title,
      levelCode: response.data.course.level_code,
      completionPercent: response.data.course.completion_percent,
      completedLessons: response.data.course.completed_lessons,
      totalLessons: response.data.course.total_lessons
    },
    currentMission: response.data.current_mission
      ? mapLessonSummary(response.data.current_mission)
      : null,
    lessons: response.data.lessons.map(mapLessonSummary)
  };
}

export type CourseSummary = {
  slug: string;
  levelCode: string;
  title: string;
  unitCount: number;
  unlocked: boolean;
  requiresPro: boolean;
  accessible: boolean;
};

export async function listCourses(): Promise<CourseSummary[]> {
  const response = await requestJson<
    ApiResponse<
      Array<{
        course_slug: string;
        level_code: string;
        course_title: string;
        units: unknown[];
        unlocked: boolean;
        requires_pro: boolean;
        accessible: boolean;
      }>
    >
  >("/courses");

  return response.data.map((course) => ({
    slug: course.course_slug,
    levelCode: course.level_code,
    title: course.course_title,
    unitCount: course.units.length,
    unlocked: course.unlocked,
    requiresPro: course.requires_pro,
    accessible: course.accessible
  }));
}

export async function getLessonProgress(lessonSlug: string): Promise<LessonProgress | null> {
  const response = await requestJson<ApiResponse<ApiLessonProgress | null>>(
    `/lessons/${lessonSlug}/progress`
  );
  return response.data ? mapLessonProgress(response.data) : null;
}

export async function getLessonAudio(lessonSlug: string): Promise<LearningLessonAudioAsset | null> {
  const response = await requestJson<ApiResponse<ApiLearningLessonAudioAsset | null>>(
    `/lessons/${lessonSlug}/audio`
  );
  return response.data ? mapLessonAudioAsset(response.data) : null;
}

export async function startLessonProgress(lessonSlug: string): Promise<LessonProgress> {
  const response = await requestJson<ApiResponse<ApiLessonProgress>>(
    `/lessons/${lessonSlug}/progress/start`,
    {
      method: "POST"
    }
  );
  return mapLessonProgress(response.data);
}

export async function completeLessonProgress(
  lessonSlug: string,
  completedSections?: string[]
): Promise<LessonProgress> {
  const response = await requestJson<ApiResponse<ApiLessonProgress>>(
    `/lessons/${lessonSlug}/progress/complete`,
    {
      method: "POST",
      body: JSON.stringify({
        completed_sections: completedSections
      })
    }
  );
  return mapLessonProgress(response.data);
}

export async function getLevelTest(levelCode: string): Promise<LevelTest> {
  const response = await requestJson<ApiResponse<ApiLevelTest>>(`/level-tests/${levelCode}`);
  return mapLevelTest(response.data);
}

export async function previewLevelTestAttempt(input: {
  levelCode: string;
  lessonCompletionPercent: number;
  scores: Record<string, number>;
}): Promise<LevelTestPreviewResult> {
  const response = await requestJson<ApiResponse<ApiLevelTestPreviewResult>>(
    `/level-tests/${input.levelCode}/attempts/preview`,
    {
      method: "POST",
      body: JSON.stringify({
        lesson_completion_percent: input.lessonCompletionPercent,
        scores: input.scores
      })
    }
  );

  return {
    overallScore: response.data.overall_score,
    passed: response.data.passed,
    missingRequirements: response.data.missing_requirements,
    weakSkills: response.data.weak_skills
  };
}

export async function listMyLevelTestAttempts(levelCode: string): Promise<LevelTestAttempt[]> {
  const response = await requestJson<ApiResponse<ApiLevelTestAttempt[]>>(
    `/me/level-test-attempts?level_code=${encodeURIComponent(levelCode)}`
  );
  return response.data.map(mapLevelTestAttempt);
}

export async function startLevelTestAttempt(levelCode: string): Promise<LevelTestAttempt> {
  const response = await requestJson<ApiResponse<ApiLevelTestAttempt>>(
    `/level-tests/${levelCode}/attempts`,
    { method: "POST" }
  );
  return mapLevelTestAttempt(response.data);
}

export async function saveLevelTestDraft(input: {
  attemptId: string;
  lessonCompletionPercent?: number;
  scores?: Record<string, number>;
  responses?: Record<string, unknown>;
}): Promise<LevelTestAttempt> {
  const response = await requestJson<ApiResponse<ApiLevelTestAttempt>>(
    `/level-test-attempts/${input.attemptId}/draft`,
    {
      method: "PATCH",
      body: JSON.stringify({
        lesson_completion_percent: input.lessonCompletionPercent,
        scores: input.scores,
        responses: input.responses
      })
    }
  );
  return mapLevelTestAttempt(response.data);
}

export async function submitLevelTestAttempt(input: {
  attemptId: string;
  lessonCompletionPercent: number;
  scores: Record<string, number>;
  responses?: Record<string, unknown>;
}): Promise<LevelTestAttempt> {
  const response = await requestJson<ApiResponse<ApiLevelTestAttempt>>(
    `/level-test-attempts/${input.attemptId}/submit`,
    {
      method: "POST",
      body: JSON.stringify({
        lesson_completion_percent: input.lessonCompletionPercent,
        scores: input.scores,
        responses: input.responses ?? {}
      })
    }
  );
  return mapLevelTestAttempt(response.data);
}

export async function getLevelTestAttemptReport(attemptId: string): Promise<LevelTestAttempt> {
  const response = await requestJson<ApiResponse<ApiLevelTestAttempt>>(
    `/level-test-attempts/${attemptId}/report`
  );
  return mapLevelTestAttempt(response.data);
}

export async function listExamTemplatesByLevel(levelCode: string): Promise<ExamTemplateSummary[]> {
  const response = await requestJson<ApiExamTemplateSummary[]>(
    `/exams/templates/level/${encodeURIComponent(levelCode)}`
  );
  return response.map(mapExamTemplateSummary);
}

export async function startRealExam(examTemplateId: string): Promise<ExamRunnerSession> {
  const response = await requestJson<ApiExamRunnerSession>("/exam-runner/start", {
    method: "POST",
    body: JSON.stringify({
      exam_template_id: examTemplateId
    })
  });
  return mapExamRunnerSession(response);
}

export async function getExamManifest(sessionId: string): Promise<ExamManifest> {
  const response = await requestJson<ApiExamManifest>(`/exam-runner/manifest/${sessionId}`);
  return mapExamManifest(response);
}

export async function getExamSectionContent(
  sessionId: string,
  sectionId: string
): Promise<ExamRunnerSectionContent> {
  const response = await requestJson<ApiExamRunnerSectionContent>(
    `/exam-runner/content/${sessionId}/${sectionId}`
  );
  return mapExamSectionContent(response);
}

export async function saveExamItemResponse(input: {
  sessionId: string;
  itemId: string;
  sectionId: string;
  responseType: string;
  textResponse?: string | null;
  selectedOptionIds?: string[] | null;
  matchedPairs?: Record<string, string> | null;
  fileUrl?: string | null;
  audioDurationSeconds?: number | null;
  timeSpentSeconds?: number | null;
}) {
  return requestJson<{ response_id: string; item_id: string; status: string; message: string }>(
    `/exam-runner/respond/${input.sessionId}`,
    {
      method: "POST",
      body: JSON.stringify({
        item_id: input.itemId,
        section_id: input.sectionId,
        response_type: input.responseType,
        text_response: input.textResponse ?? null,
        selected_option_ids: input.selectedOptionIds ?? null,
        matched_pairs: input.matchedPairs ?? null,
        file_url: input.fileUrl ?? null,
        audio_duration_seconds: input.audioDurationSeconds ?? null,
        time_spent_seconds: input.timeSpentSeconds ?? null
      })
    }
  );
}

export async function navigateExamSession(input: {
  sessionId: string;
  targetSectionId?: string | null;
  targetItemId?: string | null;
}) {
  return requestJson<{
    session_id: string;
    current_section_id: string | null;
    current_item_id: string | null;
    message: string;
  }>(`/exam-runner/navigate/${input.sessionId}`, {
    method: "POST",
    body: JSON.stringify({
      target_section_id: input.targetSectionId ?? null,
      target_item_id: input.targetItemId ?? null
    })
  });
}

export async function getExamRunnerStatus(sessionId: string): Promise<ExamRunnerStatus> {
  const response = await requestJson<ApiExamRunnerStatus>(`/exam-runner/status/${sessionId}`);
  return mapExamRunnerStatus(response);
}

export async function submitRealExam(sessionId: string) {
  return requestJson<{
    session_id: string;
    status: string;
    submitted_at: string;
    result_status: string;
    score_percent: number;
    passed: boolean;
    pending_review_count: number;
    message: string;
  }>(`/exam-runner/submit/${sessionId}`, {
    method: "POST"
  });
}
