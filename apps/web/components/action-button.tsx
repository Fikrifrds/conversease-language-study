import Link from "next/link";
import type { LucideIcon } from "lucide-react";

type ActionButtonProps = {
  href: string;
  children: React.ReactNode;
  icon?: LucideIcon;
  tone?: "dark" | "light" | "leaf" | "outline" | "glass";
};

export function ActionButton({ href, children, icon: Icon, tone = "dark" }: ActionButtonProps) {
  const tones = {
    dark: "bg-ink text-white hover:bg-leaf",
    light: "bg-white text-ink hover:bg-mint",
    leaf: "bg-leaf text-white hover:bg-ink",
    outline: "border border-ink/20 bg-transparent text-ink hover:bg-mint",
    glass: "border border-white/30 bg-white/10 text-white hover:bg-white/20"
  };

  return (
    <Link
      href={href}
      className={`focus-ring inline-flex min-h-11 items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition ${tones[tone]}`}
    >
      {Icon ? <Icon className="h-4 w-4" aria-hidden="true" /> : null}
      <span>{children}</span>
    </Link>
  );
}
