import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Kurikulum Bahasa Inggris",
  description:
    "Jelajahi kurikulum Conversease: lesson percakapan bahasa Inggris terstruktur dari level A1 sampai C1, lengkap dengan dialog, frasa berguna, dan latihan.",
  alternates: { canonical: "/courses" }
};

export default function CoursesLayout({ children }: { children: React.ReactNode }) {
  return children;
}
