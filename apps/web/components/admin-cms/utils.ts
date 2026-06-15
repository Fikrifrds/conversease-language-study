export function languageLabel(language: string) {
  const labels: Record<string, string> = {
    arabic: "Arabic",
    english: "English"
  };
  return labels[language] ?? language.charAt(0).toUpperCase() + language.slice(1);
}

export function formatDuration(durationSeconds: number) {
  if (!Number.isFinite(durationSeconds) || durationSeconds <= 0) {
    return "0s";
  }
  if (durationSeconds < 60) {
    return `${Math.round(durationSeconds)}s`;
  }
  const minutes = Math.floor(durationSeconds / 60);
  const seconds = Math.round(durationSeconds % 60);
  return `${minutes}m ${seconds}s`;
}

export function clampAudioSpeed(value: number) {
  if (!Number.isFinite(value)) {
    return 1;
  }
  return Math.min(2, Math.max(0.5, value));
}

export function audioGenerationErrorMessage(error: unknown) {
  const message = error instanceof Error ? error.message : "";
  if (message.includes("minimax_api_key_missing")) {
    return "Generate audio belum bisa berjalan karena MINIMAX_API_KEY belum terbaca di API.";
  }
  if (message.includes("s3_config_missing")) {
    return "Generate audio belum bisa upload karena konfigurasi S3 belum lengkap.";
  }
  if (message.includes("boto3_missing")) {
    return "Generate audio belum bisa upload karena dependency boto3 belum terinstall di venv API.";
  }
  if (message.includes("invalid_minimax_tts_model")) {
    return "Model MiniMax belum valid. Pilih model dari daftar.";
  }
  if (message.includes("lesson_not_found")) {
    return "Lesson belum ditemukan di content files.";
  }
  if (message.includes("listening_script")) {
    return "Listening script belum siap untuk generate audio.";
  }
  if (message.includes("minimax_request_failed") || message.includes("minimax_error")) {
    return "MiniMax belum berhasil membuat audio. Cek API key, quota, voice, atau coba ulang.";
  }
  return "Audio belum bisa digenerate. Cek konfigurasi MiniMax, S3, dan content lesson.";
}

export function contentSaveErrorMessage(error: unknown, label: string) {
  const message = error instanceof Error ? error.message : "";
  if (message.includes("content_changed_reload_required")) {
    return `${label} sudah berubah sejak terakhir diload. Reload CMS dulu sebelum menyimpan.`;
  }
  if (label === "Email template") {
    return "Email template belum bisa disimpan. Pastikan heading, Subject, Preheader, CTA, html, dan txt lengkap.";
  }
  return "Lesson belum bisa disimpan. Cek field dan validasi YAML.";
}
