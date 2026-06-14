import type { Metadata } from "next";
import "./globals.css";
import { Analytics } from "@/components/analytics";

export const metadata: Metadata = {
  title: "Conversease",
  description: "Belajar Inggris lewat percakapan nyata untuk orang Indonesia.",
  icons: {
    icon: "/favicon.ico"
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id">
      <body>
        <Analytics />
        {children}
      </body>
    </html>
  );
}
