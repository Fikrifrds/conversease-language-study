export function SectionHeading({
  eyebrow,
  title,
  children,
  tone = "default"
}: {
  eyebrow?: string;
  title: string;
  children?: React.ReactNode;
  tone?: "default" | "light";
}) {
  const isLight = tone === "light";

  return (
    <div className="max-w-3xl">
      {eyebrow ? (
        <p className={`text-sm font-semibold uppercase ${isLight ? "text-sun" : "text-leaf"}`}>
          {eyebrow}
        </p>
      ) : null}
      <h2 className={`mt-2 text-3xl font-semibold sm:text-4xl ${isLight ? "text-white" : "text-ink"}`}>
        {title}
      </h2>
      {children ? (
        <p className={`mt-3 text-base leading-7 ${isLight ? "text-white/70" : "text-ink/70"}`}>
          {children}
        </p>
      ) : null}
    </div>
  );
}
