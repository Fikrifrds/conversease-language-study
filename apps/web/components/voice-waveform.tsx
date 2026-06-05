const waveformBars = [0.35, 0.6, 0.85, 1, 0.85, 0.6, 0.35];

/** Live microphone waveform shown while the user is speaking. */
export function VoiceWaveform({ level, label = "Mendengarkan…" }: { level: number; label?: string }) {
  return (
    <span className="inline-flex items-center gap-2 text-leaf">
      <span className="inline-flex h-6 items-center gap-[3px]" aria-hidden="true">
        {waveformBars.map((weight, index) => {
          const height = 4 + Math.round(level * weight * 20);
          return (
            <span
              key={index}
              className="w-[3px] rounded-full bg-leaf transition-[height] duration-75"
              style={{ height: `${height}px` }}
            />
          );
        })}
      </span>
      {label ? <span className="font-medium text-ink/70">{label}</span> : null}
    </span>
  );
}
