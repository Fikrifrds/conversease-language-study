import type { LucideIcon } from "lucide-react";
import type { AdminCmsLanguageOption } from "@/lib/admin-cms-api";
import type { LanguageFilter } from "./types";
import { languageLabel } from "./utils";

export function LanguageFilterControl({
  languages,
  value,
  onChange
}: {
  languages: AdminCmsLanguageOption[];
  value: LanguageFilter;
  onChange: (value: LanguageFilter) => void;
}) {
  if (!languages.length) {
    return null;
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="mr-1 text-xs font-semibold uppercase text-ink/45">Language</span>
      {languages.map((language) => (
        <FilterButton
          key={language.language}
          active={value === language.language}
          onClick={() => onChange(language.language)}
        >
          {languageLabel(language.language)}
        </FilterButton>
      ))}
    </div>
  );
}

function FilterButton({
  active,
  onClick,
  children
}: {
  active: boolean;
  onClick: () => void;
  children: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`focus-ring inline-flex min-h-9 items-center rounded-lg px-3 text-sm font-semibold ${
        active ? "bg-ink text-white" : "bg-paper text-ink/65 hover:bg-mint"
      }`}
    >
      {children}
    </button>
  );
}

export function SectionNavButton({
  active,
  icon: Icon,
  label,
  description,
  onClick
}: {
  active: boolean;
  icon: LucideIcon;
  label: string;
  description: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`focus-ring flex min-w-52 shrink-0 items-start gap-3 rounded-lg px-3 py-3 text-left transition lg:w-full lg:min-w-0 ${
        active ? "bg-ink text-white" : "bg-paper text-ink/70 hover:bg-mint"
      }`}
    >
      <Icon className={`mt-0.5 h-4 w-4 shrink-0 ${active ? "text-white" : "text-leaf"}`} aria-hidden="true" />
      <span className="min-w-0">
        <span className="block text-sm font-semibold">{label}</span>
        <span className={`mt-1 block text-xs leading-4 ${active ? "text-white/70" : "text-ink/45"}`}>
          {description}
        </span>
      </span>
    </button>
  );
}
