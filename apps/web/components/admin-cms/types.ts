export type Tab = "readiness" | "curriculum" | "lessonAudio" | "examAudio" | "email" | "changelog";

export type LanguageFilter = string;

export type BulkAudioQueueStatus = "pending" | "running" | "done" | "failed" | "skipped";

export type BulkAudioQueueItem = {
  lessonSlug: string;
  lessonTitle: string;
  levelCode: string;
  unitTitle: string;
  status: BulkAudioQueueStatus;
  attempts: number;
  durationSeconds?: number;
  error?: string;
};
