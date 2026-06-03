type ApiResponse<T> = {
  data: T;
};

export type AdminCmsLesson = {
  slug: string;
  contentHash: string;
  title: string;
  status: string;
  estimatedMinutes: number;
  conversationGoal: string;
  unitTitle: string;
  sections: string[];
  roleplay: {
    scenarioKey: string;
    openingLine: string;
    learnerGoal: string;
    maxTurns: number;
    targetPhrases: string[];
  };
};

export type AdminEmailTemplate = {
  templateKey: string;
  contentHash: string;
  subject: string;
  preheader: string;
  ctaLabel: string;
  rawBody: string;
};

export type AdminContentRevision = {
  id: string;
  resourceType: string;
  resourceKey: string;
  version: number;
  action: string;
  changedBy: string;
  contentHash: string;
  metadata: Record<string, unknown>;
  createdAt: string;
};

export type AdminCmsSummary = {
  curriculum: {
    course: {
      slug: string;
      title: string;
      levelCode: string;
      unitCount: number;
      lessonCount: number;
    };
    lessons: AdminCmsLesson[];
    validationIssues: string[];
  };
  emailTemplates: AdminEmailTemplate[];
  recentRevisions: AdminContentRevision[];
};

export type AdminCmsRollbackResult =
  | {
      resourceType: "curriculum_lesson";
      data: AdminCmsLesson;
      revision: AdminContentRevision;
      rolledBackFrom: AdminContentRevision;
    }
  | {
      resourceType: "email_template";
      data: AdminEmailTemplate;
      revision: AdminContentRevision;
      rolledBackFrom: AdminContentRevision;
    };

type ApiAdminLesson = {
  slug: string;
  content_hash: string;
  title: string;
  status: string;
  estimated_minutes: number;
  conversation_goal: string;
  unit_title: string;
  sections: string[];
  roleplay: {
    scenario_key: string;
    opening_line: string;
    learner_goal: string;
    max_turns: number;
    target_phrases: string[];
  };
};

type ApiAdminEmailTemplate = {
  template_key: string;
  content_hash: string;
  subject: string;
  preheader: string;
  cta_label: string;
  raw_body: string;
};

type ApiAdminContentRevision = {
  id: string;
  resource_type: string;
  resource_key: string;
  version: number;
  action: string;
  changed_by: string;
  content_hash: string;
  metadata: Record<string, unknown>;
  created_at: string;
};

function apiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

async function adminRequestJson<T>(path: string, apiKey: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl()}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      "x-admin-api-key": apiKey,
      ...init?.headers
    }
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function mapLesson(lesson: ApiAdminLesson): AdminCmsLesson {
  return {
    slug: lesson.slug,
    contentHash: lesson.content_hash,
    title: lesson.title,
    status: lesson.status,
    estimatedMinutes: lesson.estimated_minutes,
    conversationGoal: lesson.conversation_goal,
    unitTitle: lesson.unit_title,
    sections: lesson.sections,
    roleplay: {
      scenarioKey: lesson.roleplay.scenario_key,
      openingLine: lesson.roleplay.opening_line,
      learnerGoal: lesson.roleplay.learner_goal,
      maxTurns: lesson.roleplay.max_turns,
      targetPhrases: lesson.roleplay.target_phrases
    }
  };
}

function mapEmailTemplate(template: ApiAdminEmailTemplate): AdminEmailTemplate {
  return {
    templateKey: template.template_key,
    contentHash: template.content_hash,
    subject: template.subject,
    preheader: template.preheader,
    ctaLabel: template.cta_label,
    rawBody: template.raw_body
  };
}

function mapRevision(revision: ApiAdminContentRevision): AdminContentRevision {
  return {
    id: revision.id,
    resourceType: revision.resource_type,
    resourceKey: revision.resource_key,
    version: revision.version,
    action: revision.action,
    changedBy: revision.changed_by,
    contentHash: revision.content_hash,
    metadata: revision.metadata,
    createdAt: revision.created_at
  };
}

export async function getAdminCmsSummary(apiKey: string): Promise<AdminCmsSummary> {
  const response = await adminRequestJson<
    ApiResponse<{
      curriculum: {
        course: {
          slug: string;
          title: string;
          level_code: string;
          unit_count: number;
          lesson_count: number;
        };
        lessons: ApiAdminLesson[];
        validation_issues: string[];
      };
      email_templates: ApiAdminEmailTemplate[];
      recent_revisions: ApiAdminContentRevision[];
    }>
  >("/admin/cms/summary", apiKey);

  return {
    curriculum: {
      course: {
        slug: response.data.curriculum.course.slug,
        title: response.data.curriculum.course.title,
        levelCode: response.data.curriculum.course.level_code,
        unitCount: response.data.curriculum.course.unit_count,
        lessonCount: response.data.curriculum.course.lesson_count
      },
      lessons: response.data.curriculum.lessons.map(mapLesson),
      validationIssues: response.data.curriculum.validation_issues
    },
    emailTemplates: response.data.email_templates.map(mapEmailTemplate),
    recentRevisions: response.data.recent_revisions.map(mapRevision)
  };
}

export async function getAdminCmsLesson(apiKey: string, lessonSlug: string): Promise<AdminCmsLesson> {
  const response = await adminRequestJson<ApiResponse<ApiAdminLesson>>(
    `/admin/cms/curriculum/lessons/${lessonSlug}`,
    apiKey
  );
  return mapLesson(response.data);
}

export async function updateAdminCmsLesson(input: {
  apiKey: string;
  updatedBy: string;
  lessonSlug: string;
  title: string;
  status: string;
  estimatedMinutes: number;
  conversationGoal: string;
  roleplayOpeningLine: string;
  roleplayLearnerGoal: string;
  roleplayMaxTurns: number;
  roleplayTargetPhrases: string[];
  expectedContentHash: string;
}): Promise<AdminCmsLesson> {
  const response = await adminRequestJson<ApiResponse<ApiAdminLesson>>(
    `/admin/cms/curriculum/lessons/${input.lessonSlug}`,
    input.apiKey,
    {
      method: "PATCH",
      body: JSON.stringify({
        updated_by: input.updatedBy,
        expected_content_hash: input.expectedContentHash,
        title: input.title,
        status: input.status,
        estimated_minutes: input.estimatedMinutes,
        conversation_goal: input.conversationGoal,
        roleplay_opening_line: input.roleplayOpeningLine,
        roleplay_learner_goal: input.roleplayLearnerGoal,
        roleplay_max_turns: input.roleplayMaxTurns,
        roleplay_target_phrases: input.roleplayTargetPhrases
      })
    }
  );
  return mapLesson(response.data);
}

export async function getAdminEmailTemplate(apiKey: string, templateKey: string): Promise<AdminEmailTemplate> {
  const response = await adminRequestJson<ApiResponse<ApiAdminEmailTemplate>>(
    `/admin/cms/email-templates/${templateKey}`,
    apiKey
  );
  return mapEmailTemplate(response.data);
}

export async function updateAdminEmailTemplate(input: {
  apiKey: string;
  updatedBy: string;
  templateKey: string;
  rawBody: string;
  expectedContentHash: string;
}): Promise<AdminEmailTemplate> {
  const response = await adminRequestJson<ApiResponse<ApiAdminEmailTemplate>>(
    `/admin/cms/email-templates/${input.templateKey}`,
    input.apiKey,
    {
      method: "PATCH",
      body: JSON.stringify({
        updated_by: input.updatedBy,
        expected_content_hash: input.expectedContentHash,
        raw_body: input.rawBody
      })
    }
  );
  return mapEmailTemplate(response.data);
}

export async function rollbackAdminCmsRevision(input: {
  apiKey: string;
  revisionId: string;
  restoredBy: string;
  notes?: string;
}): Promise<AdminCmsRollbackResult> {
  const response = await adminRequestJson<
    ApiResponse<ApiAdminLesson | ApiAdminEmailTemplate> & {
      revision: ApiAdminContentRevision;
      rolled_back_from: ApiAdminContentRevision;
    }
  >(`/admin/cms/revisions/${input.revisionId}/rollback`, input.apiKey, {
    method: "POST",
    body: JSON.stringify({
      restored_by: input.restoredBy,
      notes: input.notes ?? ""
    })
  });

  const revision = mapRevision(response.revision);
  const rolledBackFrom = mapRevision(response.rolled_back_from);

  if (revision.resourceType === "curriculum_lesson") {
    return {
      resourceType: "curriculum_lesson",
      data: mapLesson(response.data as ApiAdminLesson),
      revision,
      rolledBackFrom
    };
  }

  if (revision.resourceType === "email_template") {
    return {
      resourceType: "email_template",
      data: mapEmailTemplate(response.data as ApiAdminEmailTemplate),
      revision,
      rolledBackFrom
    };
  }

  throw new Error(`Unsupported rollback resource type: ${revision.resourceType}`);
}
