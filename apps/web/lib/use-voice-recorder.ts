"use client";

import { useEffect, useRef, useState } from "react";

export type RecorderStatus = "idle" | "recording" | "processing";

type UseVoiceRecorderOptions = {
  // Called with the recorded audio once the user stops (manually or via silence).
  onResult: (blob: Blob) => void | Promise<void>;
  onError?: (message: string) => void;
  maxSeconds?: number;
  // Auto-stop when the user goes silent after speaking (hands-free).
  autoStopOnSilence?: boolean;
};

const SILENCE_MS = 1800; // stop after this much silence following speech
const SPEECH_RMS_THRESHOLD = 0.015; // RMS above this counts as speech
const MIN_SPEECH_MS = 600; // require this much speech before silence can end the turn

function preferredRecordingMimeType() {
  if (typeof MediaRecorder === "undefined") {
    return "";
  }
  const candidates = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/ogg;codecs=opus"];
  return candidates.find((candidate) => MediaRecorder.isTypeSupported(candidate)) ?? "";
}

/**
 * Shared microphone recorder used across Conversation Partner, Conversation
 * Coach, and Speak Clearly so they all behave identically: optional VAD
 * auto-stop on silence, a live mic level for the waveform, and a hard max
 * duration. The recorded audio is delivered to `onResult` for transcription.
 */
export function useVoiceRecorder({
  onResult,
  onError,
  maxSeconds = 30,
  autoStopOnSilence = true
}: UseVoiceRecorderOptions) {
  const [status, setStatus] = useState<RecorderStatus>("idle");
  const [seconds, setSeconds] = useState(0);
  const [micLevel, setMicLevel] = useState(0);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const discardRef = useRef(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const rafRef = useRef<number | null>(null);
  const speechStartedAtRef = useRef<number | null>(null);
  const lastSpeechAtRef = useRef<number>(0);
  const onResultRef = useRef(onResult);
  onResultRef.current = onResult;

  useEffect(() => {
    return () => {
      stopVad();
      clearTimers();
      stopStream();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function clearTimers() {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }

  function stopStream() {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
  }

  function stopVad() {
    if (rafRef.current !== null) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }
    if (audioContextRef.current) {
      void audioContextRef.current.close().catch(() => undefined);
      audioContextRef.current = null;
    }
    speechStartedAtRef.current = null;
    setMicLevel(0);
  }

  function startVad(stream: MediaStream) {
    const AudioCtx =
      window.AudioContext ??
      (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!AudioCtx) {
      return; // VAD unavailable; manual stop / max timeout still work
    }
    const context = new AudioCtx();
    audioContextRef.current = context;
    const source = context.createMediaStreamSource(stream);
    const analyser = context.createAnalyser();
    analyser.fftSize = 1024;
    source.connect(analyser);
    const data = new Uint8Array(analyser.fftSize);
    speechStartedAtRef.current = null;
    lastSpeechAtRef.current = performance.now();

    const tick = () => {
      if (!audioContextRef.current) {
        return;
      }
      analyser.getByteTimeDomainData(data);
      let sumSquares = 0;
      for (let i = 0; i < data.length; i += 1) {
        const value = (data[i] - 128) / 128;
        sumSquares += value * value;
      }
      const rms = Math.sqrt(sumSquares / data.length);
      const now = performance.now();
      setMicLevel(Math.min(1, rms / 0.3));

      if (rms > SPEECH_RMS_THRESHOLD) {
        if (speechStartedAtRef.current === null) {
          speechStartedAtRef.current = now;
        }
        lastSpeechAtRef.current = now;
      } else if (
        autoStopOnSilence &&
        speechStartedAtRef.current !== null &&
        now - speechStartedAtRef.current > MIN_SPEECH_MS &&
        now - lastSpeechAtRef.current > SILENCE_MS
      ) {
        stopVad();
        stop();
        return;
      }

      rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
  }

  async function start() {
    if (status !== "idle") {
      return;
    }
    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
      onError?.("Browser belum mendukung rekam audio.");
      return;
    }

    setSeconds(0);
    discardRef.current = false;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = preferredRecordingMimeType();
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      chunksRef.current = [];
      streamRef.current = stream;
      mediaRecorderRef.current = recorder;

      startVad(stream);

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = () => {
        stopVad();
        clearTimers();
        stopStream();
        const wasDiscarded = discardRef.current;
        const blob = new Blob(chunksRef.current, {
          type: recorder.mimeType || mimeType || "audio/webm"
        });
        chunksRef.current = [];
        mediaRecorderRef.current = null;
        discardRef.current = false;
        setStatus("idle");
        if (!wasDiscarded) {
          void onResultRef.current(blob);
        }
      };

      recorder.start();
      setStatus("recording");
      intervalRef.current = setInterval(() => {
        setSeconds((current) => Math.min(current + 1, maxSeconds));
      }, 1000);
      timeoutRef.current = setTimeout(() => stop(), maxSeconds * 1000);
    } catch {
      stopVad();
      clearTimers();
      stopStream();
      mediaRecorderRef.current = null;
      setStatus("idle");
      onError?.("Mic belum bisa diakses. Cek izin microphone browser.");
    }
  }

  function stop() {
    const recorder = mediaRecorderRef.current;
    if (!recorder || recorder.state === "inactive") {
      return;
    }
    setStatus("processing");
    clearTimers();
    recorder.stop();
  }

  function cancel() {
    discardRef.current = true;
    stop();
  }

  return { status, seconds, micLevel, start, stop, cancel };
}
