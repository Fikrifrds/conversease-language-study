import type { Metadata } from "next";
import { SITE_URL } from "@conversease/shared";
import "./globals.css";
import { Analytics } from "@/components/analytics";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? SITE_URL;

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Conversease — Belajar Bahasa Inggris lewat Percakapan",
    template: "%s | Conversease"
  },
  description:
    "Belajar bahasa Inggris lewat percakapan nyata. Dengar dialog, praktik bicara, lalu dapat feedback langsung dalam bahasa Indonesia — dari level A1 sampai C1.",
  applicationName: "Conversease",
  alternates: {
    canonical: "/"
  },
  icons: {
    icon: "/favicon.ico"
  },
  openGraph: {
    type: "website",
    siteName: "Conversease",
    locale: "id_ID",
    url: siteUrl,
    title: "Conversease — Belajar Bahasa Inggris lewat Percakapan",
    description:
      "Belajar bahasa Inggris lewat percakapan nyata untuk orang Indonesia, dari level A1 sampai C1."
  },
  twitter: {
    card: "summary_large_image",
    title: "Conversease — Belajar Bahasa Inggris lewat Percakapan",
    description:
      "Belajar bahasa Inggris lewat percakapan nyata untuk orang Indonesia, dari level A1 sampai C1."
  },
  robots: {
    index: true,
    follow: true
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
